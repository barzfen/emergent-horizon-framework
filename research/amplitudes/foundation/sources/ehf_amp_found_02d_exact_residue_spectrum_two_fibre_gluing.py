#!/usr/bin/env python3
"""
EHF-AMP-FOUND-02D: Exact Residue Spectrum and Two-Fibre Gluing Law
==================================================================

02C exposed four unusually rigid numerical patterns for the reflection-aware
8 -> 7 residue map on chamber-local Parke--Taylor relation spaces:

    source dimension       525,
    residue-image rank     110,
    squared singular values 1, 6/5, 8/5, 9/5,
    multiplicities          20, 40, 40, 10.

It also found that the full Moore--Penrose section uses exactly the twenty
n=8 fibres with label 8 in the non-anchor parity set, at equal total weight,
and that the AMP-18 exceptional residue has a 50/50 two-fibre ancestor.

02D tests the exact combinatorial mechanism suggested by those observations.
The twenty active fibres are paired by the involution

    phi(E) = {1} union ({2,...,7} minus (E minus {1})),

with label 8 retained in the opposite parity set.  The probe asks whether:

  * there are ten complementary flip pairs;
  * each active fibre has residue rank 11;
  * the two fibres in a flip pair have exactly the same 11-dimensional image;
  * the ten pair images form an orthogonal direct sum of the full rank-110 image;
  * every pair channel has squared singular spectrum

        1 (x2), 6/5 (x4), 8/5 (x4), 9/5 (x1);

  * the fibre-local dimension inside each pair channel equals the sum of the
    local relation dimensions of the seven-point parent fibres it reaches;
  * the minimum-norm preimage of every pair-channel target splits equally
    between the two complementary source fibres;
  * the exceptional AMP-18 50/50 ancestor is an instance of this general law.

The script also evaluates the candidate exact minimal polynomial

    K (K-I) (K-6I/5) (K-8I/5) (K-9I/5) = 0,

for K = A A^T, and reports rational trace moments.  Numerical agreement is a
strong theorem candidate, not an analytic proof.

Example
-------

    caffeinate -i python3 scripts/ehf_amp_found_02d_exact_residue_spectrum_two_fibre_gluing.py \
      --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
      --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
      --section-script scripts/ehf_amp_found_02b_minimal_nontrivial_growth_sections.py \
      --base-run-dir runs/ehf_amp_found_01_amp18_20 \
      --out-dir runs/ehf_amp_found_02d_seed11 \
      --seed 11
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import numpy as np

Cycle = Tuple[int, ...]
FibreKey = Tuple[Tuple[int, ...], Tuple[int, ...]]


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


def relative_frobenius_error(actual: np.ndarray, expected: np.ndarray) -> float:
    den = float(np.linalg.norm(expected))
    num = float(np.linalg.norm(actual - expected))
    return num / den if den else num


def anchor_set(key: FibreKey) -> Tuple[int, ...]:
    if 1 in key[0]:
        return tuple(key[0])
    if 1 in key[1]:
        return tuple(key[1])
    raise ValueError(f"Fibre key has no anchor set: {key}")


def block_columns(slices: Mapping[FibreKey, slice], keys: Iterable[FibreKey]) -> List[int]:
    columns: List[int] = []
    for key in keys:
        sl = slices[key]
        columns.extend(range(sl.start, sl.stop))
    return columns


def max_subspace_residual(section, target: np.ndarray, source_q: np.ndarray) -> float:
    if source_q.shape[1] == 0:
        return 0.0 if target.shape[1] == 0 else 1.0
    return section.max_column_relative_residual(target, source_q @ (source_q.T @ target))


def cluster_against_candidates(
    values: np.ndarray,
    candidates: Sequence[Fraction],
    tolerance: float,
) -> Tuple[List[Dict[str, object]], float, bool]:
    counts = {fraction: 0 for fraction in candidates}
    errors = {fraction: [] for fraction in candidates}
    unassigned: List[float] = []
    for raw in values:
        value = float(raw)
        nearest = min(candidates, key=lambda fraction: abs(value - float(fraction)))
        error = abs(value - float(nearest))
        if error <= tolerance:
            counts[nearest] += 1
            errors[nearest].append(error)
        else:
            unassigned.append(value)
    rows: List[Dict[str, object]] = []
    max_error = 0.0
    for fraction in candidates:
        local_max = max(errors[fraction]) if errors[fraction] else 0.0
        max_error = max(max_error, local_max)
        rows.append({
            "candidate": str(fraction),
            "candidate_float": fmt(float(fraction)),
            "multiplicity": counts[fraction],
            "max_absolute_error": fmt(local_max),
        })
    return rows, max_error, len(unassigned) == 0


def principal_cosines(q1: np.ndarray, q2: np.ndarray) -> np.ndarray:
    if q1.shape[1] == 0 or q2.shape[1] == 0:
        return np.zeros(0)
    return np.linalg.svd(q1.T @ q2, compute_uv=False)


def binary_cosine_error(cosines: np.ndarray) -> float:
    if cosines.size == 0:
        return 0.0
    return float(np.max(np.minimum(np.abs(cosines), np.abs(1.0 - cosines))))


def evaluate_minimal_polynomial(k: np.ndarray, roots: Sequence[Fraction]) -> Tuple[float, float]:
    identity = np.eye(k.shape[0])
    polynomial = k.copy()
    spectral_norm = float(np.linalg.norm(k, ord=2))
    scale = max(1.0, float(np.linalg.norm(k)))
    for root in roots:
        polynomial = polynomial @ (k - float(root) * identity)
        scale *= max(1.0, spectral_norm + abs(float(root)))
    return float(np.linalg.norm(polynomial)), float(np.linalg.norm(polynomial) / scale)


def fraction_moment(candidates: Sequence[Fraction], multiplicities: Sequence[int], power: int) -> Fraction:
    total = Fraction(0, 1)
    for value, multiplicity in zip(candidates, multiplicities):
        total += multiplicity * (value ** power)
    return total


def run(args: argparse.Namespace) -> Dict[str, object]:
    started = time.time()
    base_script = Path(args.base_script).resolve()
    helper_script = Path(args.helper_script).resolve()
    section_script = Path(args.section_script).resolve()
    base_run_dir = Path(args.base_run_dir).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = base_run_dir / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    base = load_module(base_script, "ehf_amp_found_01_base_for_02d")
    helper = load_module(helper_script, "ehf_amp_found_02a_helper_for_02d")
    section = load_module(section_script, "ehf_amp_found_02b_helper_for_02d")

    print("=" * 116)
    print("EHF-AMP-FOUND-02D: EXACT RESIDUE SPECTRUM AND TWO-FIBRE GLUING LAW")
    print("=" * 116)
    print(f"base script:                  {base_script}")
    print(f"reflection-aware helper:      {helper_script}")
    print(f"section helper:               {section_script}")
    print(f"shared cache:                 {cache_dir}")
    print(f"output directory:             {out_dir}")
    print(f"seed:                         {args.seed}")
    print(f"rank tolerance:               {args.rank_tolerance}")
    print(f"exact-value tolerance:        {args.exact_value_tolerance}")

    basis_rows: List[Dict[str, object]] = []
    rec7 = helper.build_bases_for_n(base, 7, cache_dir, args, basis_rows)
    rec8 = helper.build_bases_for_n(base, 8, cache_dir, args, basis_rows)
    rec9 = helper.build_bases_for_n(base, 9, cache_dir, args, basis_rows) if args.exceptional_audit else None
    g7 = section.build_global_local_basis(base, rec7)
    g8 = section.build_global_local_basis(base, rec8)

    d, _, _, child_to_parents, _ = section.build_delete_operator(base, helper, g8.states, g7.states, 8)
    a = d @ g8.basis
    u_full, singular_values, _ = np.linalg.svd(a, full_matrices=False)
    image_rank = section.rank_from_singular_values(
        singular_values, args.rank_tolerance, args.rank_absolute_tolerance
    )
    q_image = u_full[:, :image_rank]
    kept_singular_values = singular_values[:image_rank]
    squared_singular_values = kept_singular_values ** 2
    source_kernel_dim = g8.basis.shape[1] - image_rank

    local_basis = g7.basis
    residual_nonlocal = q_image - local_basis @ (local_basis.T @ q_image)
    q_nonlocal, _, nonlocal_rank = section.orthonormal_span(
        residual_nonlocal, args.rank_tolerance, args.rank_absolute_tolerance
    )

    # ------------------------------------------------------------------
    # Exact spectrum candidate.
    # ------------------------------------------------------------------
    candidate_eigenvalues = [Fraction(1, 1), Fraction(6, 5), Fraction(8, 5), Fraction(9, 5)]
    expected_multiplicities = [20, 40, 40, 10]
    spectrum_rows, spectrum_max_error, all_values_assigned = cluster_against_candidates(
        squared_singular_values, candidate_eigenvalues, args.exact_value_tolerance
    )
    observed_multiplicities = [int(row["multiplicity"]) for row in spectrum_rows]
    multiplicities_match = observed_multiplicities == expected_multiplicities

    # Because K=A A^T is symmetric positive semidefinite, its nonzero
    # eigenvalues are exactly the squared singular values of A.  Evaluating
    # the polynomial and trace moments spectrally avoids slow dense powers of
    # a 360 x 360 matrix while remaining mathematically equivalent.
    polynomial_values = squared_singular_values.copy()
    spectral_scale = np.maximum(1.0, np.abs(squared_singular_values))
    for root in candidate_eigenvalues:
        polynomial_values *= squared_singular_values - float(root)
        spectral_scale *= np.maximum(1.0, np.abs(squared_singular_values) + abs(float(root)))
    polynomial_abs = float(np.linalg.norm(polynomial_values))
    polynomial_rel = float(np.linalg.norm(polynomial_values / spectral_scale))

    trace_rows: List[Dict[str, object]] = []
    max_trace_error = 0.0
    for power in range(1, args.trace_moment_max_power + 1):
        observed = float(np.sum(squared_singular_values ** power))
        expected_fraction = fraction_moment(candidate_eigenvalues, expected_multiplicities, power)
        expected = float(expected_fraction)
        error = abs(observed - expected)
        max_trace_error = max(max_trace_error, error)
        trace_rows.append({
            "power": power,
            "observed_trace": fmt(observed),
            "expected_exact": str(expected_fraction),
            "expected_float": fmt(expected),
            "absolute_error": fmt(error),
        })

    spectral_alignment_rows: List[Dict[str, object]] = []
    for value, expected_mult in zip(candidate_eigenvalues, expected_multiplicities):
        mask = np.abs(squared_singular_values - float(value)) <= args.exact_value_tolerance
        q_lambda = q_image[:, mask]
        local_cosines = principal_cosines(q_lambda, local_basis)
        nonlocal_cosines = principal_cosines(q_lambda, q_nonlocal)
        spectral_alignment_rows.append({
            "eigenvalue": str(value),
            "eigenvalue_float": fmt(float(value)),
            "multiplicity": q_lambda.shape[1],
            "expected_multiplicity": expected_mult,
            "local_intersection_dim": int(np.count_nonzero(local_cosines >= 1.0 - args.containment_tolerance)),
            "nonlocal_intersection_dim": int(np.count_nonzero(nonlocal_cosines >= 1.0 - args.containment_tolerance)),
            "local_principal_cosine_binary_error": fmt(binary_cosine_error(local_cosines)),
            "nonlocal_principal_cosine_binary_error": fmt(binary_cosine_error(nonlocal_cosines)),
        })

    # The local sector is contained in the residue image.  In the image SVD
    # basis, K is diagonal and P_local has matrix C C^T, where C=U^T B_local.
    # This computes the exact commutator norm without forming dense K powers.
    local_coordinates = q_image.T @ local_basis
    p_local_image = local_coordinates @ local_coordinates.T
    eigenvalue_differences = squared_singular_values[:, None] - squared_singular_values[None, :]
    commutator_image = eigenvalue_differences * p_local_image
    local_commutator_error = float(
        np.linalg.norm(commutator_image) / max(1.0, np.linalg.norm(squared_singular_values))
    )

    print("\nExact residue-spectrum audit")
    print(f"  source local relation dimension:     {g8.basis.shape[1]}")
    print(f"  residue image rank:                  {image_rank}")
    print(f"  source kernel dimension:             {source_kernel_dim}")
    print(f"  squared spectrum multiplicities:     {observed_multiplicities}")
    print(f"  candidate multiplicities:            {expected_multiplicities}")
    print(f"  max candidate eigenvalue error:      {spectrum_max_error:.3e}")
    print(f"  minimal-polynomial relative error:   {polynomial_rel:.3e}")
    print(f"  max exact trace-moment error:        {max_trace_error:.3e}")
    print(f"  local projector commutator error:    {local_commutator_error:.3e}")

    # ------------------------------------------------------------------
    # Complementary fibre-pair construction.
    # ------------------------------------------------------------------
    by_anchor_set = {anchor_set(key): key for key in g8.keys}
    active_keys = sorted(
        [key for key in g8.keys if 8 not in anchor_set(key)],
        key=lambda key: anchor_set(key),
    )
    inactive_keys = sorted(
        [key for key in g8.keys if 8 in anchor_set(key)],
        key=lambda key: anchor_set(key),
    )

    def flip_key(key: FibreKey) -> FibreKey:
        e = set(anchor_set(key))
        flipped = tuple(sorted({1} | (set(range(2, 8)) - (e - {1}))))
        if flipped not in by_anchor_set:
            raise KeyError(f"Flip fibre not found for {base.key_text(key)} -> {flipped}")
        return by_anchor_set[flipped]

    pairs: List[Tuple[FibreKey, FibreKey]] = []
    seen = set()
    for key in active_keys:
        if key in seen:
            continue
        partner = flip_key(key)
        if partner not in active_keys:
            raise RuntimeError("Flip partner is not an active fibre.")
        ordered = tuple(sorted((key, partner), key=lambda item: anchor_set(item)))
        pairs.append((ordered[0], ordered[1]))
        seen.update(ordered)
    pairs.sort(key=lambda pair: anchor_set(pair[0]))

    expected_pair_spectrum = [Fraction(1, 1), Fraction(6, 5), Fraction(8, 5), Fraction(9, 5)]
    expected_pair_mult = [2, 4, 4, 1]
    expected_single_spectrum = [Fraction(1, 2), Fraction(3, 5), Fraction(4, 5), Fraction(9, 10)]
    expected_single_mult = [2, 4, 4, 1]

    pair_rows: List[Dict[str, object]] = []
    pair_qs: List[np.ndarray] = []
    pair_keys_text: List[str] = []
    pair_equal_image_flags: List[bool] = []
    pair_equal_split_flags: List[bool] = []
    pair_spectrum_flags: List[bool] = []
    single_spectrum_flags: List[bool] = []
    local_dims: List[int] = []
    nonlocal_dims: List[int] = []
    parent_dimension_flags: List[bool] = []
    max_pair_image_error = 0.0
    max_pair_spectrum_error = 0.0
    max_single_spectrum_error = 0.0
    max_equal_split_error = 0.0
    max_metric_match_error = 0.0

    for pair_index, (left_key, right_key) in enumerate(pairs):
        left_slice = g8.slices[left_key]
        right_slice = g8.slices[right_key]
        a_left = a[:, left_slice]
        a_right = a[:, right_slice]
        a_pair = np.hstack([a_left, a_right])

        q_left, sv_left, rank_left = section.orthonormal_span(
            a_left, args.rank_tolerance, args.rank_absolute_tolerance
        )
        q_right, sv_right, rank_right = section.orthonormal_span(
            a_right, args.rank_tolerance, args.rank_absolute_tolerance
        )
        q_pair, sv_pair, rank_pair = section.orthonormal_span(
            a_pair, args.rank_tolerance, args.rank_absolute_tolerance
        )
        pair_qs.append(q_pair)
        pair_text = f"{base.key_text(left_key)} <-> {base.key_text(right_key)}"
        pair_keys_text.append(pair_text)

        left_to_right = max_subspace_residual(section, q_left, q_right)
        right_to_left = max_subspace_residual(section, q_right, q_left)
        pair_image_error = max(left_to_right, right_to_left)
        max_pair_image_error = max(max_pair_image_error, pair_image_error)
        images_equal = (
            rank_left == rank_right == rank_pair == 11
            and pair_image_error <= args.containment_tolerance
        )
        pair_equal_image_flags.append(images_equal)

        pair_cluster_rows, pair_spectrum_error, pair_assigned = cluster_against_candidates(
            sv_pair[:rank_pair] ** 2, expected_pair_spectrum, args.exact_value_tolerance
        )
        pair_multiplicities = [int(row["multiplicity"]) for row in pair_cluster_rows]
        pair_spectrum_ok = pair_assigned and pair_multiplicities == expected_pair_mult
        pair_spectrum_flags.append(pair_spectrum_ok)
        max_pair_spectrum_error = max(max_pair_spectrum_error, pair_spectrum_error)

        left_cluster_rows, left_spectrum_error, left_assigned = cluster_against_candidates(
            sv_left[:rank_left] ** 2, expected_single_spectrum, args.exact_value_tolerance
        )
        right_cluster_rows, right_spectrum_error, right_assigned = cluster_against_candidates(
            sv_right[:rank_right] ** 2, expected_single_spectrum, args.exact_value_tolerance
        )
        left_mult = [int(row["multiplicity"]) for row in left_cluster_rows]
        right_mult = [int(row["multiplicity"]) for row in right_cluster_rows]
        single_ok = (
            left_assigned and right_assigned
            and left_mult == expected_single_mult
            and right_mult == expected_single_mult
        )
        single_spectrum_flags.append(single_ok)
        max_single_spectrum_error = max(max_single_spectrum_error, left_spectrum_error, right_spectrum_error)

        local_cosines = principal_cosines(q_pair, local_basis)
        nonlocal_cosines = principal_cosines(q_pair, q_nonlocal)
        local_dim = int(np.count_nonzero(local_cosines >= 1.0 - args.containment_tolerance))
        nonlocal_dim = int(np.count_nonzero(nonlocal_cosines >= 1.0 - args.containment_tolerance))
        local_dims.append(local_dim)
        nonlocal_dims.append(nonlocal_dim)
        local_binary_error = binary_cosine_error(local_cosines)
        nonlocal_binary_error = binary_cosine_error(nonlocal_cosines)

        left_solve = section.minimum_norm_solve(
            a_left, q_pair, args.rank_tolerance, args.rank_absolute_tolerance
        )
        right_solve = section.minimum_norm_solve(
            a_right, q_pair, args.rank_tolerance, args.rank_absolute_tolerance
        )
        pair_solve = section.minimum_norm_solve(
            a_pair, q_pair, args.rank_tolerance, args.rank_absolute_tolerance
        )
        left_dim = a_left.shape[1]
        pair_left_coeff = pair_solve.coefficients[:left_dim, :]
        pair_right_coeff = pair_solve.coefficients[left_dim:, :]
        left_sq = np.sum(pair_left_coeff ** 2, axis=0)
        right_sq = np.sum(pair_right_coeff ** 2, axis=0)
        total_sq = left_sq + right_sq
        fractions = np.divide(left_sq, total_sq, out=np.full_like(left_sq, 0.5), where=total_sq > 1e-24)
        equal_split_error = float(np.max(np.abs(fractions - 0.5))) if fractions.size else 0.0
        max_equal_split_error = max(max_equal_split_error, equal_split_error)

        left_metric = left_solve.coefficients.T @ left_solve.coefficients
        right_metric = right_solve.coefficients.T @ right_solve.coefficients
        metric_match_error = relative_frobenius_error(left_metric, right_metric)
        max_metric_match_error = max(max_metric_match_error, metric_match_error)
        equal_split = (
            pair_solve.reconstruction_residual <= args.containment_tolerance
            and equal_split_error <= args.equal_split_tolerance
            and metric_match_error <= args.containment_tolerance
        )
        pair_equal_split_flags.append(equal_split)

        parent_keys = sorted(
            set(child_to_parents.get(left_key, set())) | set(child_to_parents.get(right_key, set())),
            key=base.key_text,
        )
        predicted_local_dim = int(sum(g7.relation_dims[key] for key in parent_keys))
        parent_dimension_match = (
            local_dim == predicted_local_dim
            and local_binary_error <= args.containment_tolerance
            and nonlocal_binary_error <= args.containment_tolerance
        )
        parent_dimension_flags.append(parent_dimension_match)
        pair_rows.append({
            "pair_index": pair_index,
            "left_child": base.key_text(left_key),
            "right_child": base.key_text(right_key),
            "parent_keys_reached": ";".join(base.key_text(key) for key in parent_keys),
            "parent_relation_dims": ";".join(str(g7.relation_dims[key]) for key in parent_keys),
            "predicted_local_dim_from_parent_relations": predicted_local_dim,
            "left_rank": rank_left,
            "right_rank": rank_right,
            "pair_rank": rank_pair,
            "left_to_right_image_residual": fmt(left_to_right),
            "right_to_left_image_residual": fmt(right_to_left),
            "images_equal": images_equal,
            "single_fibre_squared_spectrum_multiplicities": ";".join(map(str, left_mult)),
            "single_fibre_spectrum_exact": single_ok,
            "pair_squared_spectrum_multiplicities": ";".join(map(str, pair_multiplicities)),
            "pair_spectrum_exact": pair_spectrum_ok,
            "local_intersection_dim": local_dim,
            "nonlocal_intersection_dim": nonlocal_dim,
            "local_dimension_matches_parent_relations": parent_dimension_match,
            "local_binary_principal_cosine_error": fmt(local_binary_error),
            "nonlocal_binary_principal_cosine_error": fmt(nonlocal_binary_error),
            "left_right_preimage_metric_error": fmt(metric_match_error),
            "max_column_equal_split_error": fmt(equal_split_error),
            "pair_mp_reconstruction_residual": fmt(pair_solve.reconstruction_residual),
            "equal_two_fibre_mp_split": equal_split,
        })

    q_pairs_all = np.hstack(pair_qs) if pair_qs else np.zeros((len(g7.states), 0))
    q_pairs_span, pair_sum_sv, pair_sum_rank = section.orthonormal_span(
        q_pairs_all, args.rank_tolerance, args.rank_absolute_tolerance
    )
    pair_sum_to_image = max_subspace_residual(section, q_image, q_pairs_span)
    image_to_pair_sum = max_subspace_residual(section, q_pairs_span, q_image)

    overlap_rows: List[Dict[str, object]] = []
    max_pair_overlap = 0.0
    for i, qi in enumerate(pair_qs):
        for j, qj in enumerate(pair_qs):
            overlap = float(np.linalg.norm(qi.T @ qj, ord=2)) if qi.shape[1] and qj.shape[1] else 0.0
            if i != j:
                max_pair_overlap = max(max_pair_overlap, overlap)
            overlap_rows.append({
                "pair_i": i,
                "pair_j": j,
                "pair_i_key": pair_keys_text[i],
                "pair_j_key": pair_keys_text[j],
                "largest_principal_cosine": fmt(overlap),
            })

    local_dim_pattern = sorted(local_dims, reverse=True)
    nonlocal_dim_pattern = sorted(nonlocal_dims)
    local_split_law = (
        all(parent_dimension_flags)
        and sum(local_dims) == local_basis.shape[1]
        and sum(nonlocal_dims) == nonlocal_rank
        and all(local_dim + nonlocal_dim == 11 for local_dim, nonlocal_dim in zip(local_dims, nonlocal_dims))
    )
    distinguished_pairs = [
        pair_rows[index] for index, dimension in enumerate(local_dims) if dimension == 11
    ]

    pair_channel_law = (
        len(active_keys) == 20
        and len(inactive_keys) == 15
        and len(pairs) == 10
        and all(pair_equal_image_flags)
        and pair_sum_rank == image_rank == 110
        and pair_sum_to_image <= args.containment_tolerance
        and image_to_pair_sum <= args.containment_tolerance
        and max_pair_overlap <= args.containment_tolerance
    )
    identical_pair_spectrum_law = all(pair_spectrum_flags) and all(single_spectrum_flags)
    equal_mp_split_law = all(pair_equal_split_flags)

    print("\nComplementary flip-pair channel audit")
    print(f"  active fibres (8 outside anchor set): {len(active_keys)}")
    print(f"  inactive fibres:                     {len(inactive_keys)}")
    print(f"  complementary pairs:                 {len(pairs)}")
    print(f"  equal-image rank-11 pairs:           {sum(pair_equal_image_flags)}/{len(pairs)}")
    print(f"  pair-channel sum rank:               {pair_sum_rank}")
    print(f"  max inter-pair principal cosine:     {max_pair_overlap:.3e}")
    print(f"  max pair-image equality residual:    {max_pair_image_error:.3e}")
    print(f"  identical pair spectra:              {sum(pair_spectrum_flags)}/{len(pairs)}")
    print(f"  identical single-fibre spectra:      {sum(single_spectrum_flags)}/{len(pairs)}")
    print(f"  local dimension pattern:             {local_dim_pattern}")
    print(f"  nonlocal dimension pattern:          {nonlocal_dim_pattern}")
    print(f"  parent-dimension matches:            {sum(parent_dimension_flags)}/{len(pairs)}")
    print(f"  equal two-fibre MP splits:           {sum(pair_equal_split_flags)}/{len(pairs)}")
    print(f"  max equal-split error:               {max_equal_split_error:.3e}")

    # ------------------------------------------------------------------
    # Exceptional direction as a generic pair-channel instance.
    # ------------------------------------------------------------------
    exceptional: Dict[str, object] = {"performed": False}
    if args.exceptional_audit:
        if rec9 is None:
            raise RuntimeError("Exceptional audit requested but n=9 bases were not built.")
        star_key, star_states, missing_local, amp18_rank, amp18_sv = section.reconstruct_exceptional_direction(
            base, helper, rec8, rec9, args
        )
        star_partner = flip_key(star_key)
        star_rows = [g8.state_index[cycle] for cycle in star_states]
        vstar = np.zeros((len(g8.states), 1), dtype=float)
        vstar[star_rows, :] = missing_local
        ystar = d @ vstar

        global_solve = section.minimum_norm_solve(
            a, ystar, args.rank_tolerance, args.rank_absolute_tolerance
        )
        global_lift = g8.basis @ global_solve.coefficients
        pair_columns = block_columns(g8.slices, [star_key, star_partner])
        pair_solve = section.minimum_norm_solve(
            a[:, pair_columns], ystar, args.rank_tolerance, args.rank_absolute_tolerance
        )
        pair_lift = g8.basis[:, pair_columns] @ pair_solve.coefficients
        star_columns = block_columns(g8.slices, [star_key])
        star_solve = section.minimum_norm_solve(
            a[:, star_columns], ystar, args.rank_tolerance, args.rank_absolute_tolerance
        )
        star_lift = g8.basis[:, star_columns] @ star_solve.coefficients

        support_rows = []
        total_sq = float(np.linalg.norm(global_solve.coefficients) ** 2)
        for key in g8.keys:
            sl = g8.slices[key]
            weight_sq = float(np.linalg.norm(global_solve.coefficients[sl, :]) ** 2)
            fraction = weight_sq / total_sq if total_sq else 0.0
            if fraction > args.support_fraction_threshold:
                support_rows.append({
                    "child_key": base.key_text(key),
                    "squared_weight_fraction": fmt(fraction),
                    "is_star": key == star_key,
                    "is_flip_partner": key == star_partner,
                })
        support_rows.sort(key=lambda row: float(row["squared_weight_fraction"]), reverse=True)

        difference = vstar - global_lift
        exceptional = {
            "performed": True,
            "exceptional_key": base.key_text(star_key),
            "flip_partner_key": base.key_text(star_partner),
            "amp18_arrival_rank": amp18_rank,
            "amp18_relation_dim": rec8.bases[star_key].basis.shape[1],
            "amp18_smallest_nonzero_coordinate_sv": fmt(amp18_sv[amp18_rank - 1]),
            "amp18_first_discarded_coordinate_sv": fmt(amp18_sv[amp18_rank]),
            "residue_norm": fmt(np.linalg.norm(ystar)),
            "residue_to_star_pair_image_residual": fmt(pair_solve.reconstruction_residual),
            "global_mp_reconstruction_residual": fmt(global_solve.reconstruction_residual),
            "pair_only_mp_reconstruction_residual": fmt(pair_solve.reconstruction_residual),
            "global_vs_pair_only_mp_relative_error": fmt(
                np.linalg.norm(global_lift - pair_lift) / max(1e-30, np.linalg.norm(global_lift))
            ),
            "global_mp_cosine_with_original": fmt(section.cosine_abs(global_lift, vstar)),
            "global_mp_norm": fmt(np.linalg.norm(global_lift)),
            "original_norm": fmt(np.linalg.norm(vstar)),
            "star_only_mp_cosine_with_original": fmt(section.cosine_abs(star_lift, vstar)),
            "star_only_mp_relative_error": fmt(
                np.linalg.norm(star_lift - vstar) / max(1e-30, np.linalg.norm(vstar))
            ),
            "difference_delete_norm": fmt(np.linalg.norm(d @ difference)),
            "support_count": len(support_rows),
            "support": support_rows,
            "is_generic_two_fibre_instance": (
                global_solve.reconstruction_residual <= args.containment_tolerance
                and pair_solve.reconstruction_residual <= args.containment_tolerance
                and np.linalg.norm(global_lift - pair_lift) / max(1e-30, np.linalg.norm(global_lift))
                    <= args.containment_tolerance
                and len(support_rows) == 2
                and {row["child_key"] for row in support_rows}
                    == {base.key_text(star_key), base.key_text(star_partner)}
                and max(abs(float(row["squared_weight_fraction"]) - 0.5) for row in support_rows)
                    <= args.equal_split_tolerance
            ),
            "guardrail": (
                "The 50/50 Moore--Penrose split is canonical only for the chosen Euclidean source metric. "
                "The equal-image flip-pair law and pair-channel ranks are metric-independent subspace statements."
            ),
        }

        print("\nExceptional AMP-18 direction")
        print(f"  star fibre:                         {base.key_text(star_key)}")
        print(f"  flip partner:                       {base.key_text(star_partner)}")
        print(f"  pair-only reconstruction residual:  {pair_solve.reconstruction_residual:.3e}")
        print(f"  global vs pair-only MP error:       {float(exceptional['global_vs_pair_only_mp_relative_error']):.3e}")
        print(f"  global MP support count:            {len(support_rows)}")
        print(f"  generic two-fibre instance:         {exceptional['is_generic_two_fibre_instance']}")

    exact_spectrum_supported = (
        image_rank == 110
        and all_values_assigned
        and multiplicities_match
        and spectrum_max_error <= args.exact_value_tolerance
        and polynomial_rel <= args.polynomial_tolerance
        and max_trace_error <= args.trace_tolerance
    )

    spectrum_audit = {
        "source_local_relation_dim": g8.basis.shape[1],
        "full_residue_image_rank": image_rank,
        "source_kernel_dim": source_kernel_dim,
        "candidate_squared_singular_values": [str(value) for value in candidate_eigenvalues],
        "observed_multiplicities": observed_multiplicities,
        "expected_multiplicities": expected_multiplicities,
        "max_candidate_absolute_error": fmt(spectrum_max_error),
        "minimal_polynomial_absolute_error": fmt(polynomial_abs),
        "minimal_polynomial_relative_error": fmt(polynomial_rel),
        "max_trace_moment_absolute_error": fmt(max_trace_error),
        "local_projector_commutator_error": fmt(local_commutator_error),
        "exact_rational_spectrum_supported": exact_spectrum_supported,
        "interpretation_guardrail": (
            "The candidate rational spectrum is numerically exact to tolerance. "
            "An analytic derivation is still required before calling it a theorem."
        ),
    }

    pair_audit = {
        "active_fibre_count": len(active_keys),
        "inactive_fibre_count": len(inactive_keys),
        "flip_pair_count": len(pairs),
        "equal_image_rank_11_pair_count": int(sum(pair_equal_image_flags)),
        "pair_channel_sum_rank": pair_sum_rank,
        "full_image_rank": image_rank,
        "pair_sum_to_full_image_residual": fmt(pair_sum_to_image),
        "full_image_to_pair_sum_residual": fmt(image_to_pair_sum),
        "max_inter_pair_principal_cosine": fmt(max_pair_overlap),
        "max_pair_image_equality_residual": fmt(max_pair_image_error),
        "max_pair_spectrum_error": fmt(max_pair_spectrum_error),
        "max_single_fibre_spectrum_error": fmt(max_single_spectrum_error),
        "local_dimension_pattern": local_dim_pattern,
        "nonlocal_dimension_pattern": nonlocal_dim_pattern,
        "distinguished_wholly_local_pairs": distinguished_pairs,
        "parent_dimension_match_count": int(sum(parent_dimension_flags)),
        "equal_two_fibre_mp_pair_count": int(sum(pair_equal_split_flags)),
        "max_equal_split_error": fmt(max_equal_split_error),
        "max_preimage_metric_match_error": fmt(max_metric_match_error),
        "ten_identical_orthogonal_flip_pair_channels": pair_channel_law and identical_pair_spectrum_law,
        "pair_local_dimension_equals_reached_parent_relation_sum": local_split_law,
        "equal_two_fibre_moore_penrose_law": equal_mp_split_law,
        "interpretation_guardrail": (
            "Equal pair images, ranks and orthogonal direct-sum structure are subspace statements. "
            "Equal Moore--Penrose weights additionally use the Euclidean metric on source coefficients."
        ),
    }

    summary = {
        "script": Path(__file__).name,
        "parameters": vars(args),
        "exact_spectrum_audit": spectrum_audit,
        "flip_pair_audit": pair_audit,
        "exceptional_audit": exceptional,
        "verdicts": {
            "exact_rational_residue_spectrum_supported": exact_spectrum_supported,
            "ten_identical_orthogonal_flip_pair_channels": pair_audit["ten_identical_orthogonal_flip_pair_channels"],
            "pair_local_dimension_equals_reached_parent_relation_sum": local_split_law,
            "equal_two_fibre_moore_penrose_law": equal_mp_split_law,
            "exceptional_is_generic_pair_instance": exceptional.get("is_generic_two_fibre_instance", False),
        },
        "elapsed_seconds": time.time() - started,
        "output_files": [
            "summary.json",
            "run.log",
            "exact_spectrum_audit.json",
            "flip_pair_audit.json",
            "exceptional_two_fibre_audit.json",
            "spectral_cluster_summary.csv",
            "trace_moment_audit.csv",
            "spectral_local_alignment.csv",
            "flip_pair_channel_summary.csv",
            "flip_pair_overlap_matrix.csv",
            "operator_data.npz",
        ],
    }

    write_csv(out_dir / "spectral_cluster_summary.csv", spectrum_rows)
    write_csv(out_dir / "trace_moment_audit.csv", trace_rows)
    write_csv(out_dir / "spectral_local_alignment.csv", spectral_alignment_rows)
    write_csv(out_dir / "flip_pair_channel_summary.csv", pair_rows)
    write_csv(out_dir / "flip_pair_overlap_matrix.csv", overlap_rows)
    (out_dir / "exact_spectrum_audit.json").write_text(json.dumps(json_safe(spectrum_audit), indent=2))
    (out_dir / "flip_pair_audit.json").write_text(json.dumps(json_safe(pair_audit), indent=2))
    (out_dir / "exceptional_two_fibre_audit.json").write_text(json.dumps(json_safe(exceptional), indent=2))
    (out_dir / "summary.json").write_text(json.dumps(json_safe(summary), indent=2))

    np.savez_compressed(
        out_dir / "operator_data.npz",
        residue_operator_on_local_source=a,
        full_image_basis=q_image,
        local_target_basis=local_basis,
        nonlocal_target_basis=q_nonlocal,
        squared_singular_values=squared_singular_values,
        pair_channel_bases=np.stack(pair_qs, axis=0) if pair_qs else np.zeros((0, len(g7.states), 0)),
        active_source_fibre_keys=np.array([base.key_text(key) for key in active_keys]),
        inactive_source_fibre_keys=np.array([base.key_text(key) for key in inactive_keys]),
        pair_keys=np.array(pair_keys_text),
    )

    print("\n" + "=" * 116)
    print("FINAL SUMMARY")
    print("=" * 116)
    print(f"Exact rational spectrum supported:    {exact_spectrum_supported}")
    print(f"Ten flip-pair channels:               {pair_audit['ten_identical_orthogonal_flip_pair_channels']}")
    print(f"Parent-dimension locality law:         {local_split_law}")
    print(f"Equal two-fibre MP law:               {equal_mp_split_law}")
    if args.exceptional_audit:
        print(f"Exceptional is generic pair instance: {exceptional.get('is_generic_two_fibre_instance', False)}")
    print(f"elapsed:                              {(time.time() - started) / 60.0:.2f} minutes")
    print(f"summary:                              {out_dir / 'summary.json'}")
    print("=" * 116)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Test the exact residue spectrum and complementary two-fibre gluing law at 8 -> 7."
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--helper-script", required=True, help="Reflection-aware EHF-AMP-FOUND-02A v0.3 script.")
    parser.add_argument("--section-script", required=True, help="EHF-AMP-FOUND-02B script used as a function library.")
    parser.add_argument("--base-run-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--seed", type=int, default=11)
    parser.add_argument("--rows-multiplier", type=float, default=3.0)
    parser.add_argument("--min-rows", type=int, default=400)
    parser.add_argument("--validation-rows", type=int, default=160)
    parser.add_argument("--residue-validation-rows", type=int, default=160)
    parser.add_argument("--svd-tolerance", type=float, default=1e-9)
    parser.add_argument("--rank-tolerance", type=float, default=1e-9)
    parser.add_argument("--rank-absolute-tolerance", type=float, default=1e-11)
    parser.add_argument("--containment-tolerance", type=float, default=1e-7)
    parser.add_argument("--relation-verdict-tolerance", type=float, default=1e-7)
    parser.add_argument("--exact-value-tolerance", type=float, default=1e-10)
    parser.add_argument("--polynomial-tolerance", type=float, default=1e-10)
    parser.add_argument("--trace-tolerance", type=float, default=1e-9)
    parser.add_argument("--equal-split-tolerance", type=float, default=1e-9)
    parser.add_argument("--trace-moment-max-power", type=int, default=5)
    parser.add_argument("--support-fraction-threshold", type=float, default=1e-8)
    parser.add_argument("--exceptional-set", default="1,4,5,6")
    parser.add_argument("--exceptional-audit", dest="exceptional_audit", action="store_true", default=True)
    parser.add_argument("--no-exceptional-audit", dest="exceptional_audit", action="store_false")
    parser.add_argument("--force-rebuild", action="store_true")
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
