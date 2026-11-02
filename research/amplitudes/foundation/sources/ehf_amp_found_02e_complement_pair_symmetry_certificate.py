#!/usr/bin/env python3
"""
EHF-AMP-FOUND-02E: Complement-Pair Symmetry Decomposition and Proof Certificate
================================================================================

This probe takes the operator certificate produced by EHF-AMP-FOUND-02D and
examines the exact finite symmetry mechanism suggested by the numerics.

The twenty active n=8 fibres are indexed by 3-subsets of {2,...,7}; quotienting
by complementation gives ten channels.  The label-permutation group S_6 acts on
these ten complement pairs.  For one reference pair, the expected stabilizer is

    H = (S_3 x S_3) semidirect C_2,  |H| = 72.

The probe constructs the signed S_6 action on canonical n=7 ordering
coordinates, verifies channel covariance, restricts the stabilizer action to one
11-dimensional channel, and tests the representation-theoretic proof skeleton:

  * S_6 is transitive on the ten channels;
  * the reference stabilizer has order 72;
  * the channel representation is multiplicity-free with commutant dimension 4;
  * the four spectral projectors have ranks 2,4,4,1;
  * each spectral block is irreducible under the stabilizer;
  * the channel operator commutes with the stabilizer;
  * all ten channel operators are conjugate by signed label permutations.

This is a computational symmetry certificate and proof guide.  It does not
replace an analytic derivation of the Parke--Taylor relation projector or the
rational eigenvalues.

Example
-------

    python3 scripts/ehf_amp_found_02e_complement_pair_symmetry_certificate.py \
      --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
      --operator-data runs/ehf_amp_found_02d_seed11/operator_data.npz \
      --comparison-operator-data runs/ehf_amp_found_02d_seed29/operator_data.npz \
      --out-dir runs/ehf_amp_found_02e
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import itertools
import json
import sys
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import numpy as np

Cycle = Tuple[int, ...]
FibreKey = Tuple[Tuple[int, ...], Tuple[int, ...]]
PairID = Tuple[Tuple[int, ...], Tuple[int, ...]]
Permutation = Tuple[int, ...]  # images of labels 2,3,4,5,6,7


class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data: str) -> int:
        for stream in self.streams:
            stream.write(data)
            stream.flush()
        return len(data)

    def flush(self) -> None:
        for stream in self.streams:
            stream.flush()


def load_module(path: Path, name: str):
    if not path.exists():
        raise FileNotFoundError(path)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def fmt(value: float) -> str:
    return f"{float(value):.17g}"


def json_safe(value):
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    return value


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    fields: List[str] = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                fields.append(key)
                seen.add(key)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def anchor_set(key: FibreKey) -> Tuple[int, ...]:
    if 1 in key[0]:
        return tuple(key[0])
    if 1 in key[1]:
        return tuple(key[1])
    raise ValueError(f"No anchor set in {key}")


def canonical_pair_id(subset: Iterable[int]) -> PairID:
    left = tuple(sorted(subset))
    universe = set(range(2, 8))
    right = tuple(sorted(universe - set(left)))
    return tuple(sorted((left, right)))  # type: ignore[return-value]


def pair_text(pair_id: PairID) -> str:
    return f"{','.join(map(str, pair_id[0]))}<->{','.join(map(str, pair_id[1]))}"


def build_pairs(base) -> Tuple[List[FibreKey], List[FibreKey], List[Tuple[FibreKey, FibreKey]], List[PairID]]:
    fibre_keys = list(base.fibres(8).keys())
    by_anchor = {anchor_set(key): key for key in fibre_keys}
    active = sorted([key for key in fibre_keys if 8 not in anchor_set(key)], key=anchor_set)
    inactive = sorted([key for key in fibre_keys if 8 in anchor_set(key)], key=anchor_set)
    pairs: List[Tuple[FibreKey, FibreKey]] = []
    ids: List[PairID] = []
    seen = set()
    for key in active:
        if key in seen:
            continue
        e = set(anchor_set(key))
        partner_anchor = tuple(sorted({1} | (set(range(2, 8)) - (e - {1}))))
        partner = by_anchor[partner_anchor]
        ordered = tuple(sorted((key, partner), key=anchor_set))
        pairs.append((ordered[0], ordered[1]))
        ids.append(canonical_pair_id(set(anchor_set(ordered[0])) - {1}))
        seen.update(ordered)
    order = np.argsort([pair_text(pid) for pid in ids])
    pairs = [pairs[int(i)] for i in order]
    ids = [ids[int(i)] for i in order]
    return active, inactive, pairs, ids


def permutation_map(perm: Permutation) -> Dict[int, int]:
    return {label: image for label, image in zip(range(2, 8), perm)}


def apply_perm_to_subset(subset: Iterable[int], perm: Permutation) -> Tuple[int, ...]:
    mapping = permutation_map(perm)
    return tuple(sorted(mapping[x] for x in subset))


def permutation_cycle_type(perm: Permutation) -> Tuple[int, ...]:
    mapping = permutation_map(perm)
    seen = set()
    lengths = []
    for start in range(2, 8):
        if start in seen:
            continue
        cur = start
        length = 0
        while cur not in seen:
            seen.add(cur)
            length += 1
            cur = mapping[cur]
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def signed_action(states: Sequence[Cycle], perm: Permutation) -> Tuple[np.ndarray, np.ndarray]:
    """Return destination rows and PT reflection signs for the n=7 action.

    J[dest[j], j] = sign[j].  Label 1 is fixed.  Recanonicalization by reversal
    contributes (-1)^7=-1.
    """
    index = {cycle: i for i, cycle in enumerate(states)}
    mapping = permutation_map(perm)
    dest = np.empty(len(states), dtype=np.int64)
    signs = np.ones(len(states), dtype=float)
    for column, cycle in enumerate(states):
        relabelled = (1,) + tuple(mapping[x] for x in cycle[1:])
        if relabelled[1] < relabelled[-1]:
            canonical = relabelled
            sign = 1.0
        else:
            canonical = (1,) + tuple(reversed(relabelled[1:]))
            sign = -1.0
        dest[column] = index[canonical]
        signs[column] = sign
    return dest, signs


def apply_signed_action(matrix: np.ndarray, dest: np.ndarray, signs: np.ndarray) -> np.ndarray:
    result = np.empty_like(matrix)
    result[dest, ...] = signs.reshape((-1,) + (1,) * (matrix.ndim - 1)) * matrix
    return result


def signed_action_matrix(dest: np.ndarray, signs: np.ndarray) -> np.ndarray:
    matrix = np.zeros((len(dest), len(dest)), dtype=float)
    matrix[dest, np.arange(len(dest))] = signs
    return matrix


def transform_symmetric(matrix: np.ndarray, dest: np.ndarray, signs: np.ndarray) -> np.ndarray:
    result = np.zeros_like(matrix)
    result[np.ix_(dest, dest)] = signs[:, None] * matrix * signs[None, :]
    return result


def subspace_residual(target: np.ndarray, basis: np.ndarray) -> float:
    if target.shape[1] == 0:
        return 0.0
    approximation = basis @ (basis.T @ target)
    denominator = np.linalg.norm(target, axis=0)
    mask = denominator > 1e-14
    if not np.any(mask):
        return 0.0
    return float(np.max(np.linalg.norm(target[:, mask] - approximation[:, mask], axis=0) / denominator[mask]))


def numerical_rank(values: np.ndarray, relative_tolerance: float, absolute_tolerance: float) -> int:
    values = np.asarray(values, dtype=float)
    if values.size == 0:
        return 0
    threshold = max(absolute_tolerance, relative_tolerance * float(np.max(np.abs(values))))
    return int(np.count_nonzero(np.abs(values) > threshold))


def commutant_dimension(
    matrices: Sequence[np.ndarray],
    relative_tolerance: float,
    absolute_tolerance: float,
) -> Tuple[int, np.ndarray]:
    if not matrices:
        raise ValueError("At least one matrix is required")
    dimension = matrices[0].shape[0]
    identity = np.eye(dimension)
    constraints = []
    for matrix in matrices:
        constraints.append(np.kron(matrix.T, identity) - np.kron(identity, matrix))
    system = np.vstack(constraints)
    singular_values = np.linalg.svd(system, compute_uv=False)
    rank = numerical_rank(singular_values, relative_tolerance, absolute_tolerance)
    return dimension * dimension - rank, singular_values


def polynomial_multiply(a: Sequence[Fraction], b: Sequence[Fraction]) -> List[Fraction]:
    out = [Fraction(0, 1)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def polynomial_from_roots(roots: Sequence[Tuple[Fraction, int]]) -> List[Fraction]:
    coefficients = [Fraction(1, 1)]  # ascending powers
    for root, multiplicity in roots:
        for _ in range(multiplicity):
            coefficients = polynomial_multiply(coefficients, [-root, Fraction(1, 1)])
    return coefficients


def format_polynomial(coefficients: Sequence[Fraction], variable: str = "x") -> str:
    terms: List[str] = []
    for power in range(len(coefficients) - 1, -1, -1):
        coefficient = coefficients[power]
        if coefficient == 0:
            continue
        sign = "-" if coefficient < 0 else "+"
        magnitude = abs(coefficient)
        if power == 0:
            body = str(magnitude)
        else:
            coeff_text = "" if magnitude == 1 else f"{magnitude}*"
            body = f"{coeff_text}{variable}" if power == 1 else f"{coeff_text}{variable}^{power}"
        if not terms:
            terms.append(("-" if sign == "-" else "") + body)
        else:
            terms.append(f" {sign} {body}")
    return "".join(terms) if terms else "0"


def spectral_projector(matrix: np.ndarray, root: Fraction, roots: Sequence[Fraction]) -> np.ndarray:
    dimension = matrix.shape[0]
    projector = np.eye(dimension)
    for other in roots:
        if other == root:
            continue
        projector = projector @ ((matrix - float(other) * np.eye(dimension)) / float(root - other))
    return 0.5 * (projector + projector.T)


@dataclass
class OperatorBundle:
    residue_operator: np.ndarray
    pair_bases: np.ndarray
    squared_singular_values: np.ndarray
    pair_keys_text: List[str]


def load_operator_bundle(path: Path) -> OperatorBundle:
    if not path.exists():
        raise FileNotFoundError(path)
    with np.load(path, allow_pickle=True) as data:
        return OperatorBundle(
            residue_operator=np.asarray(data["residue_operator_on_local_source"], dtype=float),
            pair_bases=np.asarray(data["pair_channel_bases"], dtype=float),
            squared_singular_values=np.asarray(data["squared_singular_values"], dtype=float),
            pair_keys_text=[str(x) for x in data["pair_keys"]],
        )


def run(args: argparse.Namespace) -> Dict[str, object]:
    started = time.time()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    base = load_module(Path(args.base_script).resolve(), "ehf_amp_found_02e_base")
    bundle = load_operator_bundle(Path(args.operator_data).resolve())
    comparison = load_operator_bundle(Path(args.comparison_operator_data).resolve()) if args.comparison_operator_data else None

    states7 = base.canonical_cycles(7)
    fibre_keys8 = list(base.fibres(8).keys())
    active_keys, inactive_keys, pairs, pair_ids = build_pairs(base)
    pair_index = {pid: i for i, pid in enumerate(pair_ids)}

    if bundle.residue_operator.shape != (len(states7), 525):
        raise RuntimeError(f"Unexpected residue operator shape: {bundle.residue_operator.shape}")
    if bundle.pair_bases.shape != (10, len(states7), 11):
        raise RuntimeError(f"Unexpected pair-basis shape: {bundle.pair_bases.shape}")
    if len(fibre_keys8) != 35 or any(len(base.fibres(8)[key]) != 72 for key in fibre_keys8):
        raise RuntimeError("Unexpected n=8 fibre geometry")

    # All n=8 relation blocks have dimension 15 in the 02D source direct sum.
    block_dim = bundle.residue_operator.shape[1] // len(fibre_keys8)
    if block_dim != 15:
        raise RuntimeError(f"Expected 15 relation coordinates per n=8 fibre, got {block_dim}")
    slices = {key: slice(i * block_dim, (i + 1) * block_dim) for i, key in enumerate(fibre_keys8)}

    # Verify pair ordering against 02D's serialized labels by matching sets of fibre texts.
    expected_pair_texts = []
    for left, right in pairs:
        expected_pair_texts.append(f"{base.key_text(left)} <-> {base.key_text(right)}")
    if set(expected_pair_texts) != set(bundle.pair_keys_text):
        raise RuntimeError("The 02D pair labels do not match the reconstructed complement pairs")
    reorder = [bundle.pair_keys_text.index(text) for text in expected_pair_texts]
    pair_bases = bundle.pair_bases[reorder]

    pair_operators: List[np.ndarray] = []
    pair_restricted_operators: List[np.ndarray] = []
    for (left, right), q in zip(pairs, pair_bases):
        columns = list(range(slices[left].start, slices[left].stop)) + list(range(slices[right].start, slices[right].stop))
        a_pair = bundle.residue_operator[:, columns]
        k_pair = a_pair @ a_pair.T
        pair_operators.append(k_pair)
        pair_restricted_operators.append(0.5 * (q.T @ k_pair @ q + (q.T @ k_pair @ q).T))

    print("=" * 118)
    print("EHF-AMP-FOUND-02E: COMPLEMENT-PAIR SYMMETRY DECOMPOSITION AND PROOF CERTIFICATE")
    print("=" * 118)
    print(f"base script:                    {Path(args.base_script).resolve()}")
    print(f"02D operator data:              {Path(args.operator_data).resolve()}")
    print(f"comparison operator data:       {Path(args.comparison_operator_data).resolve() if args.comparison_operator_data else 'not supplied'}")
    print(f"output directory:               {out_dir}")
    print(f"target states:                  {len(states7)}")
    print(f"active/inactive source fibres:  {len(active_keys)}/{len(inactive_keys)}")
    print(f"complement-pair channels:       {len(pairs)}")

    # ------------------------------------------------------------------
    # Signed S6 action and channel covariance.
    # ------------------------------------------------------------------
    permutations: List[Permutation] = list(itertools.permutations(range(2, 8)))
    actions: List[Tuple[np.ndarray, np.ndarray]] = []
    pair_maps: List[List[int]] = []
    max_action_orthogonality_error = 0.0
    max_channel_covariance_residual = 0.0
    orbit = set()
    transport_permutation_index: Dict[int, int] = {}

    for perm_index, perm in enumerate(permutations):
        dest, signs = signed_action(states7, perm)
        actions.append((dest, signs))
        max_action_orthogonality_error = max(
            max_action_orthogonality_error,
            float(np.max(np.abs(np.bincount(dest, minlength=len(states7)) - 1))),
        )
        mapping: List[int] = []
        for pid in pair_ids:
            transformed = canonical_pair_id(apply_perm_to_subset(pid[0], perm))
            mapping.append(pair_index[transformed])
        pair_maps.append(mapping)
        orbit.add(mapping[0])
        transport_permutation_index.setdefault(mapping[0], perm_index)
        for source_index, target_index in enumerate(mapping):
            moved = apply_signed_action(pair_bases[source_index], dest, signs)
            residual = subspace_residual(moved, pair_bases[target_index])
            max_channel_covariance_residual = max(max_channel_covariance_residual, residual)

    stabilizer_indices = [i for i, mapping in enumerate(pair_maps) if mapping[0] == 0]
    orbit_size = len(orbit)
    stabilizer_size = len(stabilizer_indices)

    print("\nSigned S6 channel action")
    print(f"  group elements enumerated:          {len(permutations)}")
    print(f"  reference-channel orbit size:       {orbit_size}")
    print(f"  reference stabilizer size:          {stabilizer_size}")
    print(f"  max signed-action permutation error:{max_action_orthogonality_error:.3e}")
    print(f"  max channel-covariance residual:    {max_channel_covariance_residual:.3e}")

    # ------------------------------------------------------------------
    # Stabilizer representation on the reference 11-dimensional channel.
    # ------------------------------------------------------------------
    q0 = pair_bases[0]
    k0 = pair_operators[0]
    m0 = pair_restricted_operators[0]
    stabilizer_reps: List[np.ndarray] = []
    stabilizer_perms: List[Permutation] = []
    max_stabilizer_invariance_residual = 0.0
    max_rep_orthogonality_error = 0.0
    max_k_commutator_error = 0.0

    for index in stabilizer_indices:
        perm = permutations[index]
        dest, signs = actions[index]
        moved_q = apply_signed_action(q0, dest, signs)
        max_stabilizer_invariance_residual = max(
            max_stabilizer_invariance_residual,
            subspace_residual(moved_q, q0),
        )
        rep = q0.T @ moved_q
        stabilizer_reps.append(rep)
        stabilizer_perms.append(perm)
        max_rep_orthogonality_error = max(
            max_rep_orthogonality_error,
            float(np.linalg.norm(rep.T @ rep - np.eye(11))),
        )
        max_k_commutator_error = max(
            max_k_commutator_error,
            float(np.linalg.norm(rep @ m0 - m0 @ rep) / max(1.0, np.linalg.norm(m0))),
        )

    character = np.array([np.trace(rep) for rep in stabilizer_reps])
    character_inner_product = float(np.mean(character * character))
    full_commutant_dim, full_commutant_sv = commutant_dimension(
        stabilizer_reps, args.rank_tolerance, args.absolute_tolerance
    )

    print("\nReference stabilizer representation")
    print(f"  expected stabilizer structure:      (S3 x S3) semidirect C2")
    print(f"  channel invariance residual:        {max_stabilizer_invariance_residual:.3e}")
    print(f"  representation orthogonality error:{max_rep_orthogonality_error:.3e}")
    print(f"  character inner product <chi,chi>: {character_inner_product:.12f}")
    print(f"  commutant dimension:                {full_commutant_dim}")
    print(f"  K/stabilizer commutator error:      {max_k_commutator_error:.3e}")

    # ------------------------------------------------------------------
    # Four spectral blocks and irreducibility certificate.
    # ------------------------------------------------------------------
    roots = [Fraction(1, 1), Fraction(6, 5), Fraction(8, 5), Fraction(9, 5)]
    expected_ranks = [2, 4, 4, 1]
    projectors: List[np.ndarray] = []
    block_rows: List[Dict[str, object]] = []
    character_rows: List[Dict[str, object]] = []
    max_projector_idempotency_error = 0.0
    max_projector_commutator_error = 0.0
    max_block_scalar_error = 0.0
    max_block_rep_orthogonality_error = 0.0
    block_commutant_dims: List[int] = []
    block_character_norms: List[float] = []
    observed_ranks: List[int] = []
    block_bases: List[np.ndarray] = []

    for root, expected_rank in zip(roots, expected_ranks):
        projector = spectral_projector(m0, root, roots)
        projectors.append(projector)
        eigenvalues, eigenvectors = np.linalg.eigh(projector)
        rank = int(np.count_nonzero(eigenvalues > 0.5))
        basis = eigenvectors[:, eigenvalues > 0.5]
        block_bases.append(basis)
        observed_ranks.append(rank)
        idempotency_error = float(np.linalg.norm(projector @ projector - projector))
        max_projector_idempotency_error = max(max_projector_idempotency_error, idempotency_error)
        scalar_error = float(np.linalg.norm(basis.T @ m0 @ basis - float(root) * np.eye(rank)))
        max_block_scalar_error = max(max_block_scalar_error, scalar_error)
        block_reps = [basis.T @ rep @ basis for rep in stabilizer_reps]
        block_comm_dim, _ = commutant_dimension(block_reps, args.rank_tolerance, args.absolute_tolerance)
        block_commutant_dims.append(block_comm_dim)
        block_character = np.array([np.trace(rep) for rep in block_reps])
        block_character_norm = float(np.mean(block_character * block_character))
        block_character_norms.append(block_character_norm)
        block_orthogonality_error = max(
            float(np.linalg.norm(rep.T @ rep - np.eye(rank))) for rep in block_reps
        )
        max_block_rep_orthogonality_error = max(max_block_rep_orthogonality_error, block_orthogonality_error)
        projector_commutator = max(
            float(np.linalg.norm(rep @ projector - projector @ rep)) for rep in stabilizer_reps
        )
        max_projector_commutator_error = max(max_projector_commutator_error, projector_commutator)
        block_rows.append({
            "eigenvalue": str(root),
            "expected_rank": expected_rank,
            "observed_rank": rank,
            "projector_idempotency_error": fmt(idempotency_error),
            "operator_scalar_error": fmt(scalar_error),
            "stabilizer_commutant_dimension": block_comm_dim,
            "character_inner_product": fmt(block_character_norm),
            "max_representation_orthogonality_error": fmt(block_orthogonality_error),
            "projector_stabilizer_commutator_error": fmt(projector_commutator),
        })

    projector_sum_error = float(np.linalg.norm(sum(projectors) - np.eye(11)))
    max_projector_overlap = 0.0
    for i in range(len(projectors)):
        for j in range(i + 1, len(projectors)):
            max_projector_overlap = max(max_projector_overlap, float(np.linalg.norm(projectors[i] @ projectors[j])))
    reconstructed_m0 = sum(float(root) * projector for root, projector in zip(roots, projectors))
    spectral_reconstruction_error = float(np.linalg.norm(m0 - reconstructed_m0))

    for row_index, (perm, rep) in enumerate(zip(stabilizer_perms, stabilizer_reps)):
        row: Dict[str, object] = {
            "stabilizer_index": row_index,
            "permutation_images_2_to_7": ",".join(map(str, perm)),
            "cycle_type": ",".join(map(str, permutation_cycle_type(perm))),
            "channel_character": fmt(np.trace(rep)),
        }
        for root, basis in zip(roots, block_bases):
            row[f"character_lambda_{str(root).replace('/', '_')}"] = fmt(np.trace(basis.T @ rep @ basis))
        character_rows.append(row)

    print("\nSpectral-block certificate")
    print(f"  projector ranks:                   {observed_ranks}")
    print(f"  expected ranks:                    {expected_ranks}")
    print(f"  block commutant dimensions:        {block_commutant_dims}")
    print(f"  block character norms:             {[round(x, 12) for x in block_character_norms]}")
    print(f"  projector-sum error:               {projector_sum_error:.3e}")
    print(f"  max projector overlap:             {max_projector_overlap:.3e}")
    print(f"  max projector idempotency error:   {max_projector_idempotency_error:.3e}")
    print(f"  K spectral reconstruction error:   {spectral_reconstruction_error:.3e}")

    # ------------------------------------------------------------------
    # Conjugacy transport of the complete channel operator.
    # ------------------------------------------------------------------
    transport_rows: List[Dict[str, object]] = []
    max_operator_transport_error = 0.0
    max_restricted_spectrum_error = 0.0
    for target_index in range(10):
        perm_index = transport_permutation_index[target_index]
        perm = permutations[perm_index]
        dest, signs = actions[perm_index]
        transported = transform_symmetric(k0, dest, signs)
        target_operator = pair_operators[target_index]
        error = float(np.linalg.norm(transported - target_operator) / max(1.0, np.linalg.norm(target_operator)))
        max_operator_transport_error = max(max_operator_transport_error, error)
        observed = np.linalg.eigvalsh(pair_restricted_operators[target_index])
        expected = np.linalg.eigvalsh(m0)
        spectrum_error = float(np.max(np.abs(np.sort(observed) - np.sort(expected))))
        max_restricted_spectrum_error = max(max_restricted_spectrum_error, spectrum_error)
        transport_rows.append({
            "target_pair_index": target_index,
            "target_pair": pair_text(pair_ids[target_index]),
            "transport_permutation_images_2_to_7": ",".join(map(str, perm)),
            "operator_conjugacy_relative_error": fmt(error),
            "restricted_spectrum_max_error": fmt(spectrum_error),
        })

    print("\nTen-channel transport")
    print(f"  max operator conjugacy error:       {max_operator_transport_error:.3e}")
    print(f"  max restricted-spectrum error:      {max_restricted_spectrum_error:.3e}")

    # ------------------------------------------------------------------
    # Optional cross-seed certificate comparison.
    # ------------------------------------------------------------------
    comparison_audit: Dict[str, object] = {"performed": False}
    if comparison is not None:
        comparison_reorder = [comparison.pair_keys_text.index(text) for text in expected_pair_texts]
        comparison_pair_bases = comparison.pair_bases[comparison_reorder]
        max_pair_subspace_error = 0.0
        for q, qc in zip(pair_bases, comparison_pair_bases):
            max_pair_subspace_error = max(max_pair_subspace_error, subspace_residual(q, qc), subspace_residual(qc, q))
        comparison_audit = {
            "performed": True,
            "max_squared_singular_value_difference": fmt(float(np.max(np.abs(np.sort(bundle.squared_singular_values) - np.sort(comparison.squared_singular_values))))),
            "max_pair_channel_subspace_residual": fmt(max_pair_subspace_error),
            "residue_operator_relative_difference": fmt(float(np.linalg.norm(bundle.residue_operator - comparison.residue_operator) / max(1.0, np.linalg.norm(bundle.residue_operator)))),
            "guardrail": (
                "The orthonormal source bases may differ across kinematic seeds, so the raw residue-operator matrix need not agree. "
                "The target channel subspaces and spectrum are the invariant comparisons."
            ),
        }
        print("\nCross-seed comparison")
        print(f"  max spectrum difference:            {float(comparison_audit['max_squared_singular_value_difference']):.3e}")
        print(f"  max pair-subspace residual:         {max_pair_subspace_error:.3e}")

    characteristic_coefficients = polynomial_from_roots(list(zip(roots, expected_ranks)))
    minimal_coefficients = polynomial_from_roots([(root, 1) for root in roots])
    exact_polynomials = {
        "characteristic_polynomial_ascending_coefficients": [str(x) for x in characteristic_coefficients],
        "characteristic_polynomial": format_polynomial(characteristic_coefficients),
        "minimal_polynomial_ascending_coefficients": [str(x) for x in minimal_coefficients],
        "minimal_polynomial": format_polynomial(minimal_coefficients),
        "factorized_characteristic_polynomial": "(x-1)^2 (x-6/5)^4 (x-8/5)^4 (x-9/5)",
        "factorized_minimal_polynomial": "(x-1)(x-6/5)(x-8/5)(x-9/5)",
    }

    group_audit = {
        "group": "S6 acting on labels 2,...,7",
        "group_order": len(permutations),
        "active_fibre_count": len(active_keys),
        "inactive_fibre_count": len(inactive_keys),
        "complement_pair_count": len(pairs),
        "reference_pair": pair_text(pair_ids[0]),
        "reference_orbit_size": orbit_size,
        "reference_stabilizer_size": stabilizer_size,
        "expected_stabilizer": "(S3 x S3) semidirect C2",
        "expected_stabilizer_order": 72,
        "max_channel_covariance_residual": fmt(max_channel_covariance_residual),
        "max_signed_action_permutation_error": fmt(max_action_orthogonality_error),
        "transitive_on_ten_channels": orbit_size == 10,
        "stabilizer_order_correct": stabilizer_size == 72,
    }

    stabilizer_audit = {
        "channel_dimension": 11,
        "stabilizer_size": stabilizer_size,
        "max_channel_invariance_residual": fmt(max_stabilizer_invariance_residual),
        "max_representation_orthogonality_error": fmt(max_rep_orthogonality_error),
        "character_inner_product": fmt(character_inner_product),
        "commutant_dimension": full_commutant_dim,
        "max_operator_commutator_error": fmt(max_k_commutator_error),
        "multiplicity_free_four_block_candidate": (
            abs(character_inner_product - 4.0) <= args.verdict_tolerance and full_commutant_dim == 4
        ),
        "interpretation": (
            "For a finite-group representation, <chi,chi> is the sum of squared irreducible multiplicities. "
            "The value 4 together with commutant dimension 4 supports four inequivalent multiplicity-one blocks."
        ),
    }

    spectral_audit = {
        "candidate_eigenvalues": [str(root) for root in roots],
        "expected_block_dimensions": expected_ranks,
        "observed_block_dimensions": observed_ranks,
        "block_commutant_dimensions": block_commutant_dims,
        "block_character_inner_products": [fmt(value) for value in block_character_norms],
        "projector_sum_error": fmt(projector_sum_error),
        "max_projector_overlap": fmt(max_projector_overlap),
        "max_projector_idempotency_error": fmt(max_projector_idempotency_error),
        "max_projector_stabilizer_commutator_error": fmt(max_projector_commutator_error),
        "max_block_scalar_error": fmt(max_block_scalar_error),
        "max_block_representation_orthogonality_error": fmt(max_block_rep_orthogonality_error),
        "spectral_reconstruction_error": fmt(spectral_reconstruction_error),
        "all_four_blocks_irreducible_under_stabilizer": (
            observed_ranks == expected_ranks
            and all(dim == 1 for dim in block_commutant_dims)
            and all(abs(value - 1.0) <= args.verdict_tolerance for value in block_character_norms)
        ),
        "guardrail": (
            "This is a numerical representation certificate. An analytic proof must identify the four stabilizer irreducibles "
            "and derive the scalar eigenvalues from exact combinatorial or amplitude identities."
        ),
    }

    transport_audit = {
        "transported_channel_count": 10,
        "max_operator_conjugacy_relative_error": fmt(max_operator_transport_error),
        "max_restricted_spectrum_error": fmt(max_restricted_spectrum_error),
        "all_channel_operators_conjugate": max_operator_transport_error <= args.verdict_tolerance,
    }

    verdicts = {
        "s6_transitive_on_complement_pair_channels": group_audit["transitive_on_ten_channels"],
        "reference_stabilizer_has_order_72": group_audit["stabilizer_order_correct"],
        "channel_covariance_supported": max_channel_covariance_residual <= args.verdict_tolerance,
        "four_block_multiplicity_free_stabilizer_decomposition_supported": stabilizer_audit["multiplicity_free_four_block_candidate"],
        "spectral_blocks_irreducible_under_stabilizer": spectral_audit["all_four_blocks_irreducible_under_stabilizer"],
        "channel_operator_is_stabilizer_equivariant": max_k_commutator_error <= args.verdict_tolerance,
        "all_ten_channel_operators_are_s6_conjugate": transport_audit["all_channel_operators_conjugate"],
        "candidate_dimensions_2_4_4_1_supported": observed_ranks == expected_ranks,
    }

    summary = {
        "script": Path(__file__).name,
        "parameters": vars(args),
        "group_action_audit": group_audit,
        "stabilizer_representation_audit": stabilizer_audit,
        "spectral_irrep_audit": spectral_audit,
        "channel_transport_audit": transport_audit,
        "cross_seed_comparison": comparison_audit,
        "exact_polynomials": exact_polynomials,
        "verdicts": verdicts,
        "elapsed_seconds": time.time() - started,
        "output_files": [
            "summary.json",
            "run.log",
            "group_action_audit.json",
            "stabilizer_representation_audit.json",
            "spectral_irrep_audit.json",
            "channel_transport_audit.json",
            "cross_seed_comparison.json",
            "exact_polynomials.json",
            "spectral_block_summary.csv",
            "stabilizer_character_rows.csv",
            "channel_transport_rows.csv",
        ],
    }

    (out_dir / "group_action_audit.json").write_text(json.dumps(json_safe(group_audit), indent=2))
    (out_dir / "stabilizer_representation_audit.json").write_text(json.dumps(json_safe(stabilizer_audit), indent=2))
    (out_dir / "spectral_irrep_audit.json").write_text(json.dumps(json_safe(spectral_audit), indent=2))
    (out_dir / "channel_transport_audit.json").write_text(json.dumps(json_safe(transport_audit), indent=2))
    (out_dir / "cross_seed_comparison.json").write_text(json.dumps(json_safe(comparison_audit), indent=2))
    (out_dir / "exact_polynomials.json").write_text(json.dumps(json_safe(exact_polynomials), indent=2))
    (out_dir / "summary.json").write_text(json.dumps(json_safe(summary), indent=2))
    write_csv(out_dir / "spectral_block_summary.csv", block_rows)
    write_csv(out_dir / "stabilizer_character_rows.csv", character_rows)
    write_csv(out_dir / "channel_transport_rows.csv", transport_rows)

    print("\n" + "=" * 118)
    print("FINAL SUMMARY")
    print("=" * 118)
    print(f"S6 transitive on ten channels:        {verdicts['s6_transitive_on_complement_pair_channels']}")
    print(f"Reference stabilizer order 72:        {verdicts['reference_stabilizer_has_order_72']}")
    print(f"Channel covariance supported:         {verdicts['channel_covariance_supported']}")
    print(f"Four multiplicity-free blocks:        {verdicts['four_block_multiplicity_free_stabilizer_decomposition_supported']}")
    print(f"Candidate block dimensions 2+4+4+1:  {verdicts['candidate_dimensions_2_4_4_1_supported']}")
    print(f"Each spectral block irreducible:      {verdicts['spectral_blocks_irreducible_under_stabilizer']}")
    print(f"K stabilizer-equivariant:             {verdicts['channel_operator_is_stabilizer_equivariant']}")
    print(f"All ten operators S6-conjugate:       {verdicts['all_ten_channel_operators_are_s6_conjugate']}")
    print(f"elapsed:                              {(time.time()-started)/60.0:.2f} minutes")
    print(f"summary:                              {out_dir / 'summary.json'}")
    print("=" * 118)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the EHF-AMP-FOUND-02E complement-pair symmetry certificate.")
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--operator-data", required=True, help="operator_data.npz from a full EHF-AMP-FOUND-02D run")
    parser.add_argument("--comparison-operator-data", default=None, help="Optional operator_data.npz from an independent 02D seed")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--rank-tolerance", type=float, default=1e-9)
    parser.add_argument("--absolute-tolerance", type=float, default=1e-11)
    parser.add_argument("--verdict-tolerance", type=float, default=1e-8)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    log_path = out_dir / "run.log"
    with log_path.open("a", buffering=1) as log_handle:
        original_stdout, original_stderr = sys.stdout, sys.stderr
        sys.stdout = Tee(original_stdout, log_handle)
        sys.stderr = Tee(original_stderr, log_handle)
        try:
            print(f"\n===== RUN START {time.strftime('%Y-%m-%d %H:%M:%S')} =====")
            run(args)
            print(f"===== RUN END {time.strftime('%Y-%m-%d %H:%M:%S')} =====")
            return 0
        except Exception as exc:
            import traceback
            print(f"\nERROR: {type(exc).__name__}: {exc}")
            traceback.print_exc()
            return 1
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr


if __name__ == "__main__":
    raise SystemExit(main())
