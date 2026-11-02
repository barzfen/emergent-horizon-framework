#!/usr/bin/env python3
"""
EHF-AMP-FOUND-02F: Exact Symbolic Channel Operator and Schur-Scalar Derivation
===============================================================================

02D found a rational four-level spectrum for the reflection-aware 8 -> 7
residue operator. 02E identified the symmetry mechanism: ten S6-conjugate
rank-11 channels, each carrying a multiplicity-free representation of

    H = (S3 x S3) semidirect C2

with irreducible dimensions 2,4,4,1.

02F converts one reference channel operator into an exact rational matrix,
derives its minimal polynomial without assuming the four eigenvalues, builds
the exact spectral projectors, and computes the Schur scalars and stabilizer
characters exactly.

The reference channel is the complement pair

    {2,3,4} <-> {5,6,7}.

For the supplied 02D operator bundle its target support has 36 canonical
seven-point states. The numerically constructed Gram operator is rationally
reconstructed entry-by-entry. All subsequent algebra is performed exactly
with SymPy rationals.

The probe establishes, conditional on the rational reconstruction:

  * an exact 36 x 36 rational reference-channel matrix;
  * exact rank 11 and kernel dimension 25;
  * a minimal polynomial derived from exact power dependence;
  * exact spectral projectors and multiplicities;
  * exact H-equivariance of the reconstructed matrix;
  * exact irreducibility and inequivalence of the four nonzero blocks from
    stabilizer-character inner products;
  * exact Schur scalars on the 2+4+4+1 blocks;
  * the same exact polynomial and multiplicity certificate for all ten
    complement-pair channels;
  * optional cross-seed equality of the reconstructed reference matrix.

This is a computer-assisted exact certificate. A handwritten theorem still
requires a direct derivation of the rational matrix entries from the
Parke--Taylor relation projector, rather than rational reconstruction from
high-precision numerical operator data.

Example
-------

    caffeinate -i python3 scripts/ehf_amp_found_02f_exact_symbolic_channel_operator.py \
      --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
      --symmetry-script scripts/ehf_amp_found_02e_complement_pair_symmetry_certificate.py \
      --operator-data runs/ehf_amp_found_02d_seed11/operator_data.npz \
      --comparison-operator-data runs/ehf_amp_found_02d_seed29/operator_data.npz \
      --out-dir runs/ehf_amp_found_02f
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import itertools
import json
import math
import sys
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import numpy as np
import sympy as sp

Cycle = Tuple[int, ...]
FibreKey = Tuple[Tuple[int, ...], Tuple[int, ...]]
Permutation = Tuple[int, ...]


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
        raise FileNotFoundError(f"Script not found: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to import: {path}")
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
    if isinstance(value, sp.Basic):
        return str(value)
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


def rationalise_scalar(value: float, max_denominator: int, zero_tolerance: float) -> sp.Rational:
    if abs(float(value)) <= zero_tolerance:
        return sp.Rational(0, 1)
    fraction = Fraction(float(value)).limit_denominator(max_denominator)
    return sp.Rational(fraction.numerator, fraction.denominator)


def rationalise_matrix(
    matrix: np.ndarray,
    max_denominator: int,
    zero_tolerance: float,
) -> Tuple[sp.Matrix, float, int]:
    exact_rows: List[List[sp.Rational]] = []
    max_error = 0.0
    denominator_lcm = 1
    for row in np.asarray(matrix, dtype=float):
        exact_row: List[sp.Rational] = []
        for raw in row:
            value = rationalise_scalar(float(raw), max_denominator, zero_tolerance)
            exact_row.append(value)
            max_error = max(max_error, abs(float(value) - float(raw)))
            denominator_lcm = math.lcm(denominator_lcm, int(value.q))
        exact_rows.append(exact_row)
    return sp.Matrix(exact_rows), max_error, denominator_lcm


def matrix_support(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    row_norms = np.linalg.norm(np.asarray(matrix, dtype=float), axis=1)
    return np.flatnonzero(row_norms > tolerance)


def matrix_polynomial(matrix: sp.Matrix, coefficients: Sequence[sp.Rational]) -> sp.Matrix:
    """Evaluate ascending-power coefficients c_0 + c_1 K + ... exactly."""
    n = matrix.rows
    result = sp.zeros(n)
    power = sp.eye(n)
    for coefficient in coefficients:
        result += coefficient * power
        power = power * matrix
    return result


def derive_minimal_polynomial(
    matrix: sp.Matrix,
    max_degree: int,
) -> List[sp.Rational]:
    """
    Find the first exact linear dependence among I,K,...,K^d.

    Returns monic coefficients in ascending powers.
    """
    n = matrix.rows
    powers = [sp.eye(n)]
    for degree in range(1, max_degree + 1):
        powers.append(powers[-1] * matrix)
        columns = [power.reshape(n * n, 1) for power in powers]
        dependence = sp.Matrix.hstack(*columns).nullspace()
        if not dependence:
            continue
        for vector in dependence:
            if vector[-1] == 0:
                continue
            coefficients = [sp.simplify(entry / vector[-1]) for entry in vector]
            if matrix_polynomial(matrix, coefficients) != sp.zeros(n):
                continue
            return coefficients
    raise RuntimeError(f"No minimal-polynomial dependence found up to degree {max_degree}")


def polynomial_expression(coefficients: Sequence[sp.Rational], symbol: sp.Symbol) -> sp.Expr:
    return sp.expand(sum(coefficient * symbol**power for power, coefficient in enumerate(coefficients)))


def rational_roots_from_squarefree_linear_polynomial(poly: sp.Poly) -> List[sp.Rational]:
    constant, factors = sp.factor_list(poly.as_expr())
    del constant
    roots: List[sp.Rational] = []
    for factor, multiplicity in factors:
        factor_poly = sp.Poly(factor, poly.gens[0], domain=sp.QQ)
        if factor_poly.degree() != 1 or multiplicity != 1:
            raise RuntimeError(f"Expected distinct linear factors; got {factor}^{multiplicity}")
        a, b = factor_poly.all_coeffs()
        root = sp.Rational(-b, a)
        roots.append(root)
    return sorted(roots)


def exact_spectral_projectors(matrix: sp.Matrix, roots: Sequence[sp.Rational]) -> Dict[sp.Rational, sp.Matrix]:
    identity = sp.eye(matrix.rows)
    projectors: Dict[sp.Rational, sp.Matrix] = {}
    for root in roots:
        projector = identity
        for other in roots:
            if other == root:
                continue
            projector = projector * (matrix - other * identity) / (root - other)
        projectors[root] = projector
    return projectors


def signed_character(projector: sp.Matrix, local_dest: Sequence[int], local_signs: Sequence[int]) -> sp.Rational:
    """
    For R[dest[i], i] = sign[i], compute tr(P R) exactly.
    """
    return sp.simplify(
        sum(sp.Integer(local_signs[i]) * projector[i, local_dest[i]] for i in range(projector.rows))
    )


def character_inner_product(left: Sequence[sp.Rational], right: Sequence[sp.Rational]) -> sp.Rational:
    if len(left) != len(right):
        raise ValueError("Character vectors have different lengths")
    return sp.simplify(sum(a * b for a, b in zip(left, right)) / len(left))


def permutation_text(perm: Permutation) -> str:
    return ",".join(str(x) for x in perm)


def cycle_text(cycle: Cycle) -> str:
    return ",".join(str(x) for x in cycle)


def block_columns(slices: Mapping[FibreKey, slice], keys: Iterable[FibreKey]) -> List[int]:
    columns: List[int] = []
    for key in keys:
        sl = slices[key]
        columns.extend(range(sl.start, sl.stop))
    return columns


def load_operator_data(path: Path) -> Tuple[np.ndarray, List[str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with np.load(path, allow_pickle=True) as data:
        operator = np.asarray(data["residue_operator_on_local_source"], dtype=float)
        pair_keys = [str(value) for value in data["pair_keys"]]
    return operator, pair_keys


def exact_entry_histogram(matrix: sp.Matrix) -> List[Dict[str, object]]:
    counts = Counter(str(value) for value in matrix)
    values = sorted((sp.Rational(text), count) for text, count in counts.items())
    return [
        {
            "exact_value": str(value),
            "float_value": fmt(float(value)),
            "multiplicity": count,
        }
        for value, count in values
    ]


def exact_dense_matrix_rows(
    matrix: sp.Matrix,
    support_states: Sequence[Cycle],
    support_indices: Sequence[int],
) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for i in range(matrix.rows):
        row: Dict[str, object] = {
            "row_local_index": i,
            "row_ambient_index": int(support_indices[i]),
            "row_cycle": cycle_text(support_states[i]),
        }
        for j in range(matrix.cols):
            row[f"c{j:02d}"] = str(matrix[i, j])
        rows.append(row)
    return rows


def analyse_exact_channel(
    numerical_k: np.ndarray,
    support_tolerance: float,
    max_denominator: int,
    rational_tolerance: float,
    roots: Optional[Sequence[sp.Rational]] = None,
    minimal_coefficients: Optional[Sequence[sp.Rational]] = None,
) -> Dict[str, object]:
    support = matrix_support(numerical_k, support_tolerance)
    restricted = numerical_k[np.ix_(support, support)]
    off_support = numerical_k.copy()
    off_support[np.ix_(support, support)] = 0.0
    exact, max_error, denominator_lcm = rationalise_matrix(
        restricted,
        max_denominator=max_denominator,
        zero_tolerance=rational_tolerance,
    )
    rank = int(exact.rank())

    result: Dict[str, object] = {
        "support": support,
        "restricted_numerical": restricted,
        "exact_matrix": exact,
        "support_size": int(len(support)),
        "rank": rank,
        "kernel_dimension": int(len(support) - rank),
        "rational_reconstruction_max_error": max_error,
        "denominator_lcm": denominator_lcm,
        "off_support_frobenius_norm": float(np.linalg.norm(off_support)),
    }

    if minimal_coefficients is not None:
        result["minimal_polynomial_identity"] = (
            matrix_polynomial(exact, minimal_coefficients) == sp.zeros(exact.rows)
        )

    if roots is not None:
        projectors = exact_spectral_projectors(exact, roots)
        multiplicities = [int(sp.trace(projectors[root])) for root in roots]
        result["projector_multiplicities"] = multiplicities
        result["projector_idempotent"] = all(
            projector * projector == projector for projector in projectors.values()
        )
        result["projector_sum_identity"] = (
            sum(projectors.values(), sp.zeros(exact.rows)) == sp.eye(exact.rows)
        )
        result["spectral_reconstruction_identity"] = (
            sum((root * projectors[root] for root in roots), sp.zeros(exact.rows)) == exact
        )
    return result


def run(args: argparse.Namespace) -> Dict[str, object]:
    started = time.time()
    base_script = Path(args.base_script).resolve()
    symmetry_script = Path(args.symmetry_script).resolve()
    operator_data_path = Path(args.operator_data).resolve()
    comparison_path = Path(args.comparison_operator_data).resolve() if args.comparison_operator_data else None
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    base = load_module(base_script, "ehf_amp_found_02f_base")
    symmetry = load_module(symmetry_script, "ehf_amp_found_02f_symmetry")
    residue_operator, serialized_pair_keys = load_operator_data(operator_data_path)
    comparison_operator = None
    if comparison_path is not None:
        comparison_operator, _ = load_operator_data(comparison_path)

    states7: List[Cycle] = list(base.canonical_cycles(7))
    fibre_keys8: List[FibreKey] = list(base.fibres(8).keys())
    active_keys, inactive_keys, pairs, pair_ids = symmetry.build_pairs(base)

    if residue_operator.shape != (len(states7), 525):
        raise RuntimeError(f"Unexpected residue operator shape: {residue_operator.shape}")
    if len(fibre_keys8) != 35:
        raise RuntimeError(f"Expected 35 n=8 fibres, found {len(fibre_keys8)}")
    block_dim = residue_operator.shape[1] // len(fibre_keys8)
    if block_dim != 15:
        raise RuntimeError(f"Expected 15 relation coordinates per n=8 fibre, found {block_dim}")
    slices = {
        key: slice(index * block_dim, (index + 1) * block_dim)
        for index, key in enumerate(fibre_keys8)
    }

    expected_pair_texts = [
        f"{base.key_text(left)} <-> {base.key_text(right)}"
        for left, right in pairs
    ]
    if set(expected_pair_texts) != set(serialized_pair_keys):
        raise RuntimeError("02D pair labels do not match reconstructed complement pairs")

    reference_pair_id = symmetry.canonical_pair_id((2, 3, 4))
    reference_index = pair_ids.index(reference_pair_id)
    reference_left, reference_right = pairs[reference_index]
    reference_columns = block_columns(slices, (reference_left, reference_right))
    reference_a = residue_operator[:, reference_columns]
    reference_k_numerical = reference_a @ reference_a.T

    print("=" * 122)
    print("EHF-AMP-FOUND-02F: EXACT SYMBOLIC CHANNEL OPERATOR AND SCHUR-SCALAR DERIVATION")
    print("=" * 122)
    print(f"base script:                       {base_script}")
    print(f"symmetry script:                   {symmetry_script}")
    print(f"02D operator data:                 {operator_data_path}")
    print(f"comparison operator data:          {comparison_path if comparison_path else 'not supplied'}")
    print(f"output directory:                  {out_dir}")
    print(f"reference pair:                    {symmetry.pair_text(reference_pair_id)}")
    print(f"max rational denominator:          {args.max_denominator}")
    print(f"rational reconstruction tolerance: {args.rational_tolerance}")

    # ------------------------------------------------------------------
    # Exact reference-channel matrix.
    # ------------------------------------------------------------------
    reference = analyse_exact_channel(
        reference_k_numerical,
        support_tolerance=args.support_tolerance,
        max_denominator=args.max_denominator,
        rational_tolerance=args.rational_tolerance,
    )
    support = np.asarray(reference["support"], dtype=int)
    exact_k: sp.Matrix = reference["exact_matrix"]
    support_states = [states7[int(index)] for index in support]

    if reference["rational_reconstruction_max_error"] > args.rational_tolerance:
        raise RuntimeError(
            "Rational reconstruction error exceeds tolerance: "
            f"{reference['rational_reconstruction_max_error']:.3e}"
        )
    if reference["off_support_frobenius_norm"] > args.rational_tolerance:
        raise RuntimeError(
            "Reference channel has unexpected off-support mass: "
            f"{reference['off_support_frobenius_norm']:.3e}"
        )

    x = sp.Symbol("x")
    minimal_coefficients = derive_minimal_polynomial(
        exact_k,
        max_degree=args.max_minimal_polynomial_degree,
    )
    minimal_expression = polynomial_expression(minimal_coefficients, x)
    minimal_poly = sp.Poly(minimal_expression, x, domain=sp.QQ)
    roots = rational_roots_from_squarefree_linear_polynomial(minimal_poly)
    projectors = exact_spectral_projectors(exact_k, roots)

    projector_multiplicities = {root: int(sp.trace(projectors[root])) for root in roots}
    projector_identities = {
        root: {
            "idempotent": projectors[root] * projectors[root] == projectors[root],
            "eigen_projector": exact_k * projectors[root] == root * projectors[root],
            "rank_from_trace": int(sp.trace(projectors[root])),
        }
        for root in roots
    }
    projector_sum_identity = (
        sum(projectors.values(), sp.zeros(exact_k.rows)) == sp.eye(exact_k.rows)
    )
    spectral_reconstruction_identity = (
        sum((root * projectors[root] for root in roots), sp.zeros(exact_k.rows)) == exact_k
    )

    characteristic_expression = sp.expand(
        sp.prod((x - root) ** projector_multiplicities[root] for root in roots)
    )
    characteristic_factorisation = sp.factor(characteristic_expression)

    trace_moments = {
        power: sp.trace(exact_k**power)
        for power in range(1, args.trace_moment_order + 1)
    }

    print("\nExact reference-channel operator")
    print(f"  target support size:               {reference['support_size']}")
    print(f"  exact rank / kernel:               {reference['rank']}/{reference['kernel_dimension']}")
    print(f"  reconstruction max error:          {reference['rational_reconstruction_max_error']:.3e}")
    print(f"  exact denominator LCM:             {reference['denominator_lcm']}")
    print(f"  minimal polynomial degree:         {minimal_poly.degree()}")
    print(f"  minimal polynomial:                {sp.factor(minimal_expression)}")
    print(f"  exact roots:                       {[str(root) for root in roots]}")
    print(
        "  projector multiplicities:          "
        f"{[projector_multiplicities[root] for root in roots]}"
    )

    # ------------------------------------------------------------------
    # Exact stabilizer action and character certificate.
    # ------------------------------------------------------------------
    support_position = {int(ambient): local for local, ambient in enumerate(support)}
    support_set = set(support_position)
    stabilizer: List[Permutation] = []
    for perm in itertools.permutations(range(2, 8)):
        mapped = symmetry.canonical_pair_id(
            symmetry.apply_perm_to_subset(reference_pair_id[0], perm)
        )
        if mapped == reference_pair_id:
            stabilizer.append(perm)

    if len(stabilizer) != 72:
        raise RuntimeError(f"Expected stabilizer order 72, found {len(stabilizer)}")

    nonzero_roots = [root for root in roots if root != 0]
    characters: Dict[sp.Rational, List[sp.Rational]] = {
        root: [] for root in nonzero_roots
    }
    character_rows: List[Dict[str, object]] = []
    exact_covariance = True
    support_invariant = True

    for element_index, perm in enumerate(stabilizer):
        dest, signs = symmetry.signed_action(states7, perm)
        if any(int(dest[int(ambient)]) not in support_set for ambient in support):
            support_invariant = False
            break
        local_dest = [
            support_position[int(dest[int(ambient)])]
            for ambient in support
        ]
        local_signs = [int(signs[int(ambient)]) for ambient in support]

        for i in range(exact_k.rows):
            for j in range(exact_k.cols):
                if exact_k[local_dest[i], local_dest[j]] != (
                    local_signs[i] * local_signs[j] * exact_k[i, j]
                ):
                    exact_covariance = False
                    break
            if not exact_covariance:
                break

        mapped_first = symmetry.apply_perm_to_subset(reference_pair_id[0], perm)
        swaps_blocks = tuple(sorted(mapped_first)) == reference_pair_id[1]
        row: Dict[str, object] = {
            "element_index": element_index,
            "permutation": permutation_text(perm),
            "cycle_type": ",".join(map(str, symmetry.permutation_cycle_type(perm))),
            "swaps_complement_blocks": swaps_blocks,
        }
        for root in nonzero_roots:
            value = signed_character(projectors[root], local_dest, local_signs)
            characters[root].append(value)
            row[f"chi_{str(root).replace('/', '_over_')}"] = str(value)
        character_rows.append(row)

    if not support_invariant:
        raise RuntimeError("Reference support is not invariant under the 72-element stabilizer")
    if not exact_covariance:
        raise RuntimeError("Exact rational reference operator failed stabilizer covariance")

    character_inner_products: Dict[Tuple[sp.Rational, sp.Rational], sp.Rational] = {}
    character_inner_rows: List[Dict[str, object]] = []
    for left_root in nonzero_roots:
        row: Dict[str, object] = {"left_root": str(left_root)}
        for right_root in nonzero_roots:
            value = character_inner_product(
                characters[left_root],
                characters[right_root],
            )
            character_inner_products[(left_root, right_root)] = value
            row[f"with_{str(right_root).replace('/', '_over_')}"] = str(value)
        character_inner_rows.append(row)

    block_rows: List[Dict[str, object]] = []
    all_blocks_irreducible = True
    all_blocks_inequivalent = True
    for root in nonzero_roots:
        dimension = projector_multiplicities[root]
        scalar = sp.simplify(
            sp.trace(exact_k * projectors[root]) / sp.trace(projectors[root])
        )
        character_norm = character_inner_products[(root, root)]
        irreducible = character_norm == 1
        inequivalent = all(
            character_inner_products[(root, other)] == 0
            for other in nonzero_roots
            if other != root
        )
        all_blocks_irreducible &= irreducible
        all_blocks_inequivalent &= inequivalent
        block_rows.append(
            {
                "root": str(root),
                "dimension": dimension,
                "schur_scalar": str(scalar),
                "projector_idempotent": projector_identities[root]["idempotent"],
                "K_times_P_equals_scalar_P": projector_identities[root]["eigen_projector"],
                "character_inner_product": str(character_norm),
                "irreducible_exact": irreducible,
                "inequivalent_to_other_nonzero_blocks": inequivalent,
                "unique_character_values": ";".join(
                    str(value) for value in sorted(set(characters[root]))
                ),
            }
        )

    full_nonzero_character = [
        sum(characters[root][index] for root in nonzero_roots)
        for index in range(len(stabilizer))
    ]
    full_character_norm = character_inner_product(
        full_nonzero_character,
        full_nonzero_character,
    )

    print("\nExact stabilizer and Schur certificate")
    print(f"  stabilizer order:                  {len(stabilizer)}")
    print(f"  exact support invariance:          {support_invariant}")
    print(f"  exact K covariance:                {exact_covariance}")
    print(
        "  nonzero block dimensions:          "
        f"{[projector_multiplicities[root] for root in nonzero_roots]}"
    )
    print(
        "  exact Schur scalars:               "
        f"{[str(sp.simplify(sp.trace(exact_k * projectors[root]) / sp.trace(projectors[root]))) for root in nonzero_roots]}"
    )
    print(
        "  exact character norms:             "
        f"{[str(character_inner_products[(root, root)]) for root in nonzero_roots]}"
    )
    print(f"  full nonzero character norm:       {full_character_norm}")

    # ------------------------------------------------------------------
    # Exact audit for all ten channels.
    # ------------------------------------------------------------------
    all_channel_rows: List[Dict[str, object]] = []
    all_ten_polynomial = True
    all_ten_multiplicities = True
    all_ten_rank_11 = True
    max_channel_reconstruction_error = 0.0

    reference_multiplicities = [projector_multiplicities[root] for root in roots]
    for pair_index, ((left, right), pair_id) in enumerate(zip(pairs, pair_ids)):
        columns = block_columns(slices, (left, right))
        a_pair = residue_operator[:, columns]
        k_pair = a_pair @ a_pair.T
        channel = analyse_exact_channel(
            k_pair,
            support_tolerance=args.support_tolerance,
            max_denominator=args.max_denominator,
            rational_tolerance=args.rational_tolerance,
            roots=roots,
            minimal_coefficients=minimal_coefficients,
        )
        max_channel_reconstruction_error = max(
            max_channel_reconstruction_error,
            float(channel["rational_reconstruction_max_error"]),
        )
        polynomial_ok = bool(channel["minimal_polynomial_identity"])
        multiplicities_ok = (
            list(channel["projector_multiplicities"]) == reference_multiplicities
        )
        rank_ok = int(channel["rank"]) == 11
        all_ten_polynomial &= polynomial_ok
        all_ten_multiplicities &= multiplicities_ok
        all_ten_rank_11 &= rank_ok

        all_channel_rows.append(
            {
                "pair_index": pair_index,
                "pair_id": symmetry.pair_text(pair_id),
                "left_child": base.key_text(left),
                "right_child": base.key_text(right),
                "support_size": channel["support_size"],
                "rank": channel["rank"],
                "kernel_dimension": channel["kernel_dimension"],
                "denominator_lcm": channel["denominator_lcm"],
                "rational_reconstruction_max_error": fmt(
                    channel["rational_reconstruction_max_error"]
                ),
                "off_support_frobenius_norm": fmt(
                    channel["off_support_frobenius_norm"]
                ),
                "minimal_polynomial_identity_exact": polynomial_ok,
                "projector_multiplicities": ";".join(
                    map(str, channel["projector_multiplicities"])
                ),
                "multiplicities_match_reference": multiplicities_ok,
                "projector_idempotent_exact": channel["projector_idempotent"],
                "projector_sum_identity_exact": channel["projector_sum_identity"],
                "spectral_reconstruction_exact": channel[
                    "spectral_reconstruction_identity"
                ],
            }
        )

    print("\nTen-channel exact transport audit")
    print(f"  exact rank-11 channels:             {sum(row['rank'] == 11 for row in all_channel_rows)}/10")
    print(f"  exact minimal-polynomial identity:  {sum(bool(row['minimal_polynomial_identity_exact']) for row in all_channel_rows)}/10")
    print(f"  exact multiplicity match:           {sum(bool(row['multiplicities_match_reference']) for row in all_channel_rows)}/10")
    print(f"  max rational reconstruction error:  {max_channel_reconstruction_error:.3e}")

    # ------------------------------------------------------------------
    # Cross-seed exact equality.
    # ------------------------------------------------------------------
    cross_seed_performed = comparison_operator is not None
    cross_seed_exact_equal = None
    cross_seed_numerical_difference = None
    cross_seed_reconstruction_error = None
    if comparison_operator is not None:
        comparison_a = comparison_operator[:, reference_columns]
        comparison_k = comparison_a @ comparison_a.T
        comparison_support = matrix_support(comparison_k, args.support_tolerance)
        if not np.array_equal(comparison_support, support):
            raise RuntimeError("Cross-seed reference support differs")
        comparison_restricted = comparison_k[np.ix_(support, support)]
        comparison_exact, comparison_error, _ = rationalise_matrix(
            comparison_restricted,
            max_denominator=args.max_denominator,
            zero_tolerance=args.rational_tolerance,
        )
        cross_seed_exact_equal = comparison_exact == exact_k
        cross_seed_numerical_difference = float(
            np.linalg.norm(
                comparison_restricted - reference["restricted_numerical"]
            )
        )
        cross_seed_reconstruction_error = comparison_error

        print("\nCross-seed exact reconstruction")
        print(f"  exact rational matrices equal:      {cross_seed_exact_equal}")
        print(f"  numerical matrix difference:        {cross_seed_numerical_difference:.3e}")
        print(f"  comparison reconstruction error:    {comparison_error:.3e}")

    # ------------------------------------------------------------------
    # Output files.
    # ------------------------------------------------------------------
    support_rows = [
        {
            "local_index": local,
            "ambient_index": int(ambient),
            "canonical_cycle": cycle_text(states7[int(ambient)]),
        }
        for local, ambient in enumerate(support)
    ]
    dense_matrix_rows = exact_dense_matrix_rows(
        exact_k,
        support_states=support_states,
        support_indices=support,
    )
    entry_histogram_rows = exact_entry_histogram(exact_k)

    trace_rows = [
        {
            "power": power,
            "exact_trace": str(value),
            "float_trace": fmt(float(value)),
        }
        for power, value in trace_moments.items()
    ]

    polynomial_certificate = {
        "reference_pair": symmetry.pair_text(reference_pair_id),
        "support_size": int(reference["support_size"]),
        "rank": int(reference["rank"]),
        "kernel_dimension": int(reference["kernel_dimension"]),
        "denominator_lcm": int(reference["denominator_lcm"]),
        "rational_reconstruction_max_error": fmt(
            reference["rational_reconstruction_max_error"]
        ),
        "minimal_polynomial_coefficients_ascending": [
            str(value) for value in minimal_coefficients
        ],
        "minimal_polynomial_expanded": str(minimal_expression),
        "minimal_polynomial_factored": str(sp.factor(minimal_expression)),
        "minimal_polynomial_degree": minimal_poly.degree(),
        "minimal_polynomial_identity_exact": (
            matrix_polynomial(exact_k, minimal_coefficients) == sp.zeros(exact_k.rows)
        ),
        "roots": [str(root) for root in roots],
        "projector_multiplicities": {
            str(root): projector_multiplicities[root]
            for root in roots
        },
        "characteristic_polynomial_factored": str(characteristic_factorisation),
        "projector_sum_identity_exact": projector_sum_identity,
        "spectral_reconstruction_identity_exact": spectral_reconstruction_identity,
        "trace_moments": {
            str(power): str(value)
            for power, value in trace_moments.items()
        },
    }

    symmetry_certificate = {
        "stabilizer": "(S3 x S3) semidirect C2",
        "stabilizer_order": len(stabilizer),
        "support_invariant_exact": support_invariant,
        "operator_covariant_exact": exact_covariance,
        "nonzero_roots": [str(root) for root in nonzero_roots],
        "nonzero_block_dimensions": [
            projector_multiplicities[root] for root in nonzero_roots
        ],
        "character_inner_product_matrix": {
            str(left): {
                str(right): str(character_inner_products[(left, right)])
                for right in nonzero_roots
            }
            for left in nonzero_roots
        },
        "all_nonzero_blocks_irreducible_exact": all_blocks_irreducible,
        "all_nonzero_blocks_pairwise_inequivalent_exact": all_blocks_inequivalent,
        "full_nonzero_character_inner_product": str(full_character_norm),
        "schur_scalars": {
            str(root): str(
                sp.simplify(
                    sp.trace(exact_k * projectors[root])
                    / sp.trace(projectors[root])
                )
            )
            for root in nonzero_roots
        },
    }

    exact_certificate = {
        "polynomial_certificate": polynomial_certificate,
        "symmetry_certificate": symmetry_certificate,
        "ten_channel_certificate": {
            "channel_count": len(all_channel_rows),
            "all_rank_11_exact": all_ten_rank_11,
            "all_satisfy_same_minimal_polynomial_exact": all_ten_polynomial,
            "all_have_same_projector_multiplicities_exact": all_ten_multiplicities,
            "max_rational_reconstruction_error": fmt(
                max_channel_reconstruction_error
            ),
        },
        "cross_seed_certificate": {
            "performed": cross_seed_performed,
            "exact_rational_reference_matrices_equal": cross_seed_exact_equal,
            "numerical_reference_matrix_difference": (
                fmt(cross_seed_numerical_difference)
                if cross_seed_numerical_difference is not None
                else None
            ),
            "comparison_rational_reconstruction_max_error": (
                fmt(cross_seed_reconstruction_error)
                if cross_seed_reconstruction_error is not None
                else None
            ),
        },
        "guardrail": (
            "All algebra after rational reconstruction is exact. The remaining "
            "proof obligation is to derive the rational reference-channel matrix "
            "directly from exact Parke--Taylor relation identities rather than "
            "inferring it from floating operator data."
        ),
    }

    write_csv(out_dir / "reference_support_states.csv", support_rows)
    write_csv(out_dir / "exact_reference_channel_matrix.csv", dense_matrix_rows)
    write_csv(out_dir / "exact_entry_histogram.csv", entry_histogram_rows)
    write_csv(out_dir / "exact_schur_blocks.csv", block_rows)
    write_csv(out_dir / "exact_stabilizer_characters.csv", character_rows)
    write_csv(out_dir / "exact_character_inner_products.csv", character_inner_rows)
    write_csv(out_dir / "exact_trace_moments.csv", trace_rows)
    write_csv(out_dir / "ten_channel_exact_audit.csv", all_channel_rows)

    with (out_dir / "exact_symbolic_certificate.json").open("w") as handle:
        json.dump(json_safe(exact_certificate), handle, indent=2)

    elapsed = time.time() - started
    summary = {
        "script": Path(__file__).name,
        "parameters": vars(args),
        "reference_pair": symmetry.pair_text(reference_pair_id),
        "reference_support_size": int(reference["support_size"]),
        "reference_rank": int(reference["rank"]),
        "reference_kernel_dimension": int(reference["kernel_dimension"]),
        "rational_reconstruction_max_error": fmt(
            reference["rational_reconstruction_max_error"]
        ),
        "exact_denominator_lcm": int(reference["denominator_lcm"]),
        "minimal_polynomial_factored": str(sp.factor(minimal_expression)),
        "minimal_polynomial_derived_without_assumed_roots": True,
        "exact_roots": [str(root) for root in roots],
        "exact_multiplicities": [
            projector_multiplicities[root] for root in roots
        ],
        "exact_nonzero_block_dimensions": [
            projector_multiplicities[root] for root in nonzero_roots
        ],
        "exact_schur_scalars": [str(root) for root in nonzero_roots],
        "exact_stabilizer_covariance": exact_covariance,
        "exact_irreducible_nonzero_blocks": all_blocks_irreducible,
        "exact_pairwise_inequivalent_nonzero_blocks": all_blocks_inequivalent,
        "all_ten_rank_11": all_ten_rank_11,
        "all_ten_same_minimal_polynomial": all_ten_polynomial,
        "all_ten_same_multiplicities": all_ten_multiplicities,
        "cross_seed_exact_equal": cross_seed_exact_equal,
        "computer_assisted_exact_certificate": (
            reference["rational_reconstruction_max_error"] <= args.rational_tolerance
            and projector_sum_identity
            and spectral_reconstruction_identity
            and exact_covariance
            and all_blocks_irreducible
            and all_blocks_inequivalent
            and all_ten_rank_11
            and all_ten_polynomial
            and all_ten_multiplicities
            and (cross_seed_exact_equal is not False)
        ),
        "elapsed_seconds": elapsed,
        "output_files": [
            "summary.json",
            "run.log",
            "exact_symbolic_certificate.json",
            "reference_support_states.csv",
            "exact_reference_channel_matrix.csv",
            "exact_entry_histogram.csv",
            "exact_schur_blocks.csv",
            "exact_stabilizer_characters.csv",
            "exact_character_inner_products.csv",
            "exact_trace_moments.csv",
            "ten_channel_exact_audit.csv",
        ],
    }

    with (out_dir / "summary.json").open("w") as handle:
        json.dump(json_safe(summary), handle, indent=2)

    print("\n" + "=" * 122)
    print("FINAL SUMMARY")
    print("=" * 122)
    print(f"Exact rational reference matrix:     {reference['rational_reconstruction_max_error'] <= args.rational_tolerance}")
    print(f"Minimal polynomial derived exactly:  True")
    print(f"Exact roots:                         {[str(root) for root in roots]}")
    print(f"Exact multiplicities:                {[projector_multiplicities[root] for root in roots]}")
    print(f"Exact stabilizer covariance:         {exact_covariance}")
    print(f"Four irreducible Schur blocks:       {all_blocks_irreducible and all_blocks_inequivalent}")
    print(f"All ten channels exact:              {all_ten_rank_11 and all_ten_polynomial and all_ten_multiplicities}")
    print(f"Cross-seed exact matrix equality:    {cross_seed_exact_equal if cross_seed_performed else 'not tested'}")
    print(f"Computer-assisted exact certificate: {summary['computer_assisted_exact_certificate']}")
    print(f"elapsed:                             {elapsed:.2f} seconds")
    print(f"summary:                             {out_dir / 'summary.json'}")
    print("=" * 122)

    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Exact symbolic reference-channel operator and Schur-scalar certificate."
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--symmetry-script", required=True)
    parser.add_argument("--operator-data", required=True)
    parser.add_argument("--comparison-operator-data")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--max-denominator", type=int, default=60)
    parser.add_argument("--support-tolerance", type=float, default=1e-10)
    parser.add_argument("--rational-tolerance", type=float, default=1e-12)
    parser.add_argument("--max-minimal-polynomial-degree", type=int, default=8)
    parser.add_argument("--trace-moment-order", type=int, default=6)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    log_path = out_dir / "run.log"
    with log_path.open("w") as log:
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = Tee(original_stdout, log)
        sys.stderr = Tee(original_stderr, log)
        try:
            print(f"===== RUN START {time.strftime('%Y-%m-%d %H:%M:%S')} =====")
            run(args)
            print(f"===== RUN END {time.strftime('%Y-%m-%d %H:%M:%S')} =====")
            return 0
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr


if __name__ == "__main__":
    raise SystemExit(main())
