#!/usr/bin/env python3
"""
EHF-AMP-FOUND-02C: Branch-Reversal Equivariance and Full Residue-Image Sections
===============================================================================

This probe extends EHF-AMP-FOUND-02B in two directions.

1. Branch-reversal audit
------------------------
The canonical Hamilton-cycle representative fixes one orientation by requiring
c[1] < c[-1].  This convention names the two anchor-adjacent residue branches
"plus" (after anchor 1) and "minus" (before anchor 1).  Reversal exchanges the
branches and contributes the Parke--Taylor reflection character (-1)^n.

02C constructs the opposite canonical chart explicitly and tests

    D_plus(opposite)  = J_7 D_minus(standard) J_8^{-1},
    D_minus(opposite) = J_7 D_plus(standard)  J_8^{-1},

where J_n = (-1)^n I is the chart-transition map on coefficient coordinates.
It then repeats the branch-only section tests in the opposite chart.  This
separates chart-convention asymmetry from an invariant directional law.

2. Full residue-image section
-----------------------------
02B constructed a section only on the 38-dimensional direct sum of n=7
fibre-local relation spaces.  The complete reflection-aware delete-8 image of
the 525-dimensional n=8 fibre-local relation sector has rank 110.  02C builds
an explicit minimum-Euclidean-norm section on this entire image, decomposes it
into local and nonlocal target sectors, and includes the exceptional AMP-18
missing direction on equal footing.

The Moore--Penrose section is canonical only after choosing the ambient
Euclidean inner product.  It is an exact algebraic section, not yet a claim of
physical or combinatorial uniqueness.

Example
-------

    caffeinate -i python3 scripts/ehf_amp_found_02c_branch_reversal_full_image_sections.py \
      --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
      --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
      --section-script scripts/ehf_amp_found_02b_minimal_nontrivial_growth_sections.py \
      --base-run-dir runs/ehf_amp_found_01_amp18_20 \
      --out-dir runs/ehf_amp_found_02c_seed11 \
      --seed 11
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

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


def reverse_anchor_representative(cycle: Cycle) -> Cycle:
    return (cycle[0],) + cycle[:0:-1]


def rotate_to_anchor(sequence: Sequence[int]) -> Cycle:
    seq = tuple(sequence)
    p = seq.index(1)
    return seq[p:] + seq[:p]


def chart_representative(cycle: Cycle, orientation: str) -> Cycle:
    if orientation == "standard":
        return cycle
    if orientation == "opposite":
        return reverse_anchor_representative(cycle)
    raise ValueError(f"Unknown orientation: {orientation}")


def canonicalize_into_chart(base, sequence: Sequence[int], n: int, orientation: str):
    """Return abstract canonical state plus PT character for a chosen chart.

    Coordinates are indexed by the ordinary canonical state.  The chart merely
    chooses whether that abstract state is represented by c or reverse(c).
    """
    anchored = rotate_to_anchor(sequence)
    abstract = base.canon(anchored)
    chosen = chart_representative(abstract, orientation)
    if anchored == chosen:
        reversed_orientation = False
    elif anchored == reverse_anchor_representative(chosen):
        reversed_orientation = True
    else:
        raise RuntimeError("Raw ordering is neither the chosen chart representative nor its reversal.")
    character = (-1 if n % 2 else +1) if reversed_orientation else +1
    return abstract, character, reversed_orientation


def build_delete_operator_in_chart(
    base,
    source_states: Sequence[Cycle],
    target_states: Sequence[Cycle],
    new_label: int,
    source_orientation: str,
    target_orientation: str,
):
    target_index = {c: i for i, c in enumerate(target_states)}
    full = np.zeros((len(target_states), len(source_states)), dtype=float)
    plus = np.zeros_like(full)
    minus = np.zeros_like(full)
    reversal_count = 0
    active_count = 0
    for column, abstract_source in enumerate(source_states):
        represented = chart_representative(abstract_source, source_orientation)
        if represented[1] == new_label:
            side_sign = +1
            reduced = (1,) + represented[2:]
        elif represented[-1] == new_label:
            side_sign = -1
            reduced = represented[:-1]
        else:
            continue
        active_count += 1
        abstract_target, reflection_sign, reversed_orientation = canonicalize_into_chart(
            base, reduced, len(represented) - 1, target_orientation
        )
        if reversed_orientation:
            reversal_count += 1
        coefficient = side_sign * reflection_sign
        row = target_index[abstract_target]
        full[row, column] += coefficient
        if side_sign == +1:
            plus[row, column] += coefficient
        else:
            minus[row, column] += coefficient
    return full, plus, minus, active_count, reversal_count


def intersection_dimension(q1: np.ndarray, q2: np.ndarray, tolerance: float):
    if q1.shape[1] == 0 or q2.shape[1] == 0:
        return 0, np.zeros(0)
    s = np.linalg.svd(q1.T @ q2, compute_uv=False)
    return int(np.count_nonzero(s >= 1.0 - tolerance)), s


def block_weight_rows(base, global_basis, coefficients: np.ndarray, label: str, threshold: float):
    total_sq = float(np.linalg.norm(coefficients) ** 2)
    rows = []
    for key in global_basis.keys:
        sl = global_basis.slices[key]
        weight_sq = float(np.linalg.norm(coefficients[sl, :]) ** 2)
        fraction = weight_sq / total_sq if total_sq else 0.0
        rows.append({
            "section": label,
            "child_key": base.key_text(key),
            "child_relation_dim": global_basis.relation_dims[key],
            "coefficient_frobenius_norm": fmt(np.sqrt(weight_sq)),
            "squared_weight_fraction": fmt(fraction),
            "above_support_threshold": fraction > threshold,
        })
    return rows


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

    base = load_module(base_script, "ehf_amp_found_01_base_for_02c")
    helper = load_module(helper_script, "ehf_amp_found_02a_helper_for_02c")
    section = load_module(section_script, "ehf_amp_found_02b_helper_for_02c")

    print("=" * 112)
    print("EHF-AMP-FOUND-02C: BRANCH-REVERSAL EQUIVARIANCE AND FULL RESIDUE-IMAGE SECTIONS")
    print("=" * 112)
    print(f"base script:                  {base_script}")
    print(f"reflection-aware helper:      {helper_script}")
    print(f"section helper:               {section_script}")
    print(f"shared cache:                 {cache_dir}")
    print(f"output directory:             {out_dir}")
    print(f"seed:                         {args.seed}")
    print(f"rank tolerance:               {args.rank_tolerance}")
    print(f"containment tolerance:        {args.containment_tolerance}")

    basis_rows: List[Dict[str, object]] = []
    rec7 = helper.build_bases_for_n(base, 7, cache_dir, args, basis_rows)
    rec8 = helper.build_bases_for_n(base, 8, cache_dir, args, basis_rows)
    rec9 = helper.build_bases_for_n(base, 9, cache_dir, args, basis_rows) if args.exceptional_audit else None
    g7 = section.build_global_local_basis(base, rec7)
    g8 = section.build_global_local_basis(base, rec8)

    d, dplus, dminus, _, _ = section.build_delete_operator(base, helper, g8.states, g7.states, 8)
    standard_plus_active = int(np.count_nonzero(np.linalg.norm(dplus, axis=0) > 0))
    standard_minus_active = int(np.count_nonzero(np.linalg.norm(dminus, axis=0) > 0))
    a = d @ g8.basis
    aplus = dplus @ g8.basis
    aminus = dminus @ g8.basis

    q_image, image_sv, image_rank = section.orthonormal_span(
        a, args.rank_tolerance, args.rank_absolute_tolerance
    )
    full_section = section.minimum_norm_solve(
        a, q_image, args.rank_tolerance, args.rank_absolute_tolerance
    )
    full_lift = g8.basis @ full_section.coefficients
    full_reconstructed = d @ full_lift
    full_section_residual = section.max_column_relative_residual(q_image, full_reconstructed)
    full_lift_pt = section.pt_residual(
        base, g8.states, 8, full_lift, args.seed + 2_300_001, args.validation_rows
    )
    full_target_pt = section.pt_residual(
        base, g7.states, 7, q_image, args.seed + 2_300_002, args.validation_rows
    )

    local_basis = g7.basis
    local_to_image = section.max_column_relative_residual(
        local_basis, q_image @ (q_image.T @ local_basis)
    )
    residual_nonlocal = q_image - local_basis @ (local_basis.T @ q_image)
    q_nonlocal, nonlocal_sv, nonlocal_rank = section.orthonormal_span(
        residual_nonlocal, args.rank_tolerance, args.rank_absolute_tolerance
    )
    local_nonlocal_orthogonality = float(np.linalg.norm(local_basis.T @ q_nonlocal))
    combined_q, _, combined_rank = section.orthonormal_span(
        np.hstack([local_basis, q_nonlocal]), args.rank_tolerance, args.rank_absolute_tolerance
    )
    image_to_local_nonlocal = section.max_column_relative_residual(
        q_image, combined_q @ (combined_q.T @ q_image)
    )
    nonlocal_pt = section.pt_residual(
        base, g7.states, 7, q_nonlocal, args.seed + 2_300_003, args.validation_rows
    )
    nonlocal_section = section.minimum_norm_solve(
        a, q_nonlocal, args.rank_tolerance, args.rank_absolute_tolerance
    )
    nonlocal_lift = g8.basis @ nonlocal_section.coefficients
    nonlocal_section_residual = section.max_column_relative_residual(
        q_nonlocal, d @ nonlocal_lift
    )

    qplus, plus_sv, plus_rank = section.orthonormal_span(
        aplus, args.rank_tolerance, args.rank_absolute_tolerance
    )
    qminus, minus_sv, minus_rank = section.orthonormal_span(
        aminus, args.rank_tolerance, args.rank_absolute_tolerance
    )
    branch_intersection_dim, branch_principal_cosines = intersection_dimension(
        qplus, qminus, args.containment_tolerance
    )
    q_branch_sum, branch_sum_sv, branch_sum_rank = section.orthonormal_span(
        np.hstack([aplus, aminus]), args.rank_tolerance, args.rank_absolute_tolerance
    )
    image_to_branch_sum = section.max_column_relative_residual(
        q_image, q_branch_sum @ (q_branch_sum.T @ q_image)
    )
    local_in_plus = section.max_column_relative_residual(
        local_basis, qplus @ (qplus.T @ local_basis) if plus_rank else np.zeros_like(local_basis)
    )
    local_in_minus = section.max_column_relative_residual(
        local_basis, qminus @ (qminus.T @ local_basis) if minus_rank else np.zeros_like(local_basis)
    )
    nonlocal_in_plus = section.max_column_relative_residual(
        q_nonlocal, qplus @ (qplus.T @ q_nonlocal) if plus_rank else np.zeros_like(q_nonlocal)
    ) if nonlocal_rank else 0.0
    nonlocal_in_minus = section.max_column_relative_residual(
        q_nonlocal, qminus @ (qminus.T @ q_nonlocal) if minus_rank else np.zeros_like(q_nonlocal)
    ) if nonlocal_rank else 0.0

    print("\nFull residue-image section")
    print(f"  source local relation dimension:     {g8.basis.shape[1]}")
    print(f"  full residue image rank:             {image_rank}")
    print(f"  source kernel dimension:             {g8.basis.shape[1] - image_rank}")
    print(f"  full-image section residual:         {full_section_residual:.3e}")
    print(f"  lifted n=8 PT residual:              {full_lift_pt:.3e}")
    print(f"  target n=7 PT residual:              {full_target_pt:.3e}")
    print(f"  local target sector:                 {local_basis.shape[1]}")
    print(f"  nonlocal image complement:           {nonlocal_rank}")
    print(f"  local + nonlocal combined rank:      {combined_rank}")
    print(f"  image decomposition residual:        {image_to_local_nonlocal:.3e}")
    print(f"  nonlocal section residual:           {nonlocal_section_residual:.3e}")

    print("\nBranch image audit in the standard chart")
    print(f"  plus-active canonical states:        {standard_plus_active}")
    print(f"  minus-active canonical states:       {standard_minus_active}")
    print(f"  plus image rank:                     {plus_rank}")
    print(f"  minus image rank:                    {minus_rank}")
    print(f"  branch intersection dimension:       {branch_intersection_dim}")
    print(f"  independent branch-sum rank:         {branch_sum_rank}")
    print(f"  coupled full-residue image rank:     {image_rank}")
    print(f"  local sector residual to plus:       {local_in_plus:.3e}")
    print(f"  local sector residual to minus:      {local_in_minus:.3e}")
    print(f"  nonlocal sector residual to plus:    {nonlocal_in_plus:.3e}")
    print(f"  nonlocal sector residual to minus:   {nonlocal_in_minus:.3e}")

    # Rebuild the residue operator in the opposite representative chart.
    d_opp, dp_opp, dm_opp, opp_active, opp_reversals = build_delete_operator_in_chart(
        base, g8.states, g7.states, 8, "opposite", "opposite"
    )
    chi8 = +1  # (-1)^8
    chi7 = -1  # (-1)^7
    expected_dp_opp = chi7 * dminus * chi8
    expected_dm_opp = chi7 * dplus * chi8
    expected_d_opp = chi7 * d * chi8
    equiv_plus_error = relative_frobenius_error(dp_opp, expected_dp_opp)
    equiv_minus_error = relative_frobenius_error(dm_opp, expected_dm_opp)
    equiv_full_error = relative_frobenius_error(d_opp, expected_d_opp)

    b8_opp = chi8 * g8.basis
    b7_opp = chi7 * g7.basis
    ap_opp = dp_opp @ b8_opp
    am_opp = dm_opp @ b8_opp
    a_opp = d_opp @ b8_opp
    plus_opp_solve = section.minimum_norm_solve(
        ap_opp, b7_opp, args.rank_tolerance, args.rank_absolute_tolerance
    )
    minus_opp_solve = section.minimum_norm_solve(
        am_opp, b7_opp, args.rank_tolerance, args.rank_absolute_tolerance
    )
    full_opp_solve = section.minimum_norm_solve(
        a_opp, b7_opp, args.rank_tolerance, args.rank_absolute_tolerance
    )

    print("\nBranch-reversal equivariance")
    print(f"  opposite-chart active source states: {opp_active}")
    print(f"  target canonical reversals:          {opp_reversals}")
    print(f"  D+_opp vs J7 D-_std J8^-1 error:    {equiv_plus_error:.3e}")
    print(f"  D-_opp vs J7 D+_std J8^-1 error:    {equiv_minus_error:.3e}")
    print(f"  D_opp vs J7 D_std J8^-1 error:      {equiv_full_error:.3e}")
    print(f"  standard plus-only local residual:   {local_in_plus:.3e}")
    print(f"  standard minus-only local residual:  {local_in_minus:.3e}")
    print(f"  opposite plus-only section residual: {plus_opp_solve.reconstruction_residual:.3e}")
    print(f"  opposite minus-only section residual:{minus_opp_solve.reconstruction_residual:.3e}")

    exceptional = {"performed": False, "reason": "Exceptional audit disabled."}
    support_rows: List[Dict[str, object]] = []
    ystar_to_nonlocal = float("nan")
    global_star_solve = None
    vstar = np.zeros((len(g8.states), 0), dtype=float)
    ystar = np.zeros((len(g7.states), 0), dtype=float)
    global_star_lift = np.zeros((len(g8.states), 0), dtype=float)
    local_star_lift = np.zeros((len(g8.states), 0), dtype=float)
    if args.exceptional_audit:
        if rec9 is None:
            raise RuntimeError("Exceptional audit requested but n=9 bases were not built.")
        # Exceptional AMP-18 direction, now lifted in the complete 110-dimensional image.
        star_key, star, missing_local, amp18_rank, amp18_sv = section.reconstruct_exceptional_direction(
            base, helper, rec8, rec9, args
        )
        vstar = np.zeros((len(g8.states), 1), dtype=float)
        for i, cycle in enumerate(star):
            vstar[g8.state_index[cycle], 0] = missing_local[i, 0]
        ystar = d @ vstar
        ystar_norm = float(np.linalg.norm(ystar))
        ystar_pt = section.pt_residual(
            base, g7.states, 7, ystar, args.seed + 2_300_101, args.validation_rows
        )
        ystar_to_image = section.max_column_relative_residual(
            ystar, q_image @ (q_image.T @ ystar)
        )
        ystar_to_local = section.max_column_relative_residual(
            ystar, local_basis @ (local_basis.T @ ystar)
        )
        ystar_to_nonlocal = section.max_column_relative_residual(
            ystar, q_nonlocal @ (q_nonlocal.T @ ystar)
        )
        ystar_to_plus = section.max_column_relative_residual(
            ystar, qplus @ (qplus.T @ ystar) if plus_rank else np.zeros_like(ystar)
        )
        ystar_to_minus = section.max_column_relative_residual(
            ystar, qminus @ (qminus.T @ ystar) if minus_rank else np.zeros_like(ystar)
        )

        global_star_solve = section.minimum_norm_solve(
            a, ystar, args.rank_tolerance, args.rank_absolute_tolerance
        )
        global_star_lift = g8.basis @ global_star_solve.coefficients
        global_star_difference = vstar - global_star_lift
        global_star_difference_delete = float(np.linalg.norm(d @ global_star_difference))
        global_star_difference_pt = section.pt_residual(
            base, g8.states, 8, global_star_difference, args.seed + 2_300_102, args.validation_rows
        )

        star_slice = g8.slices[star_key]
        local_star_solve = section.minimum_norm_solve(
            a[:, star_slice], ystar, args.rank_tolerance, args.rank_absolute_tolerance
        )
        local_star_coeff = np.zeros((g8.basis.shape[1], 1), dtype=float)
        local_star_coeff[star_slice, :] = local_star_solve.coefficients
        local_star_lift = g8.basis @ local_star_coeff

        global_total_sq = float(np.linalg.norm(global_star_solve.coefficients) ** 2)
        support_rows = []
        exceptional_fraction = 0.0
        for key in g8.keys:
            sl = g8.slices[key]
            weight_sq = float(np.linalg.norm(global_star_solve.coefficients[sl, :]) ** 2)
            fraction = weight_sq / global_total_sq if global_total_sq else 0.0
            if key == star_key:
                exceptional_fraction = fraction
            if fraction > args.support_fraction_threshold:
                support_rows.append({
                    "child_key": base.key_text(key),
                    "squared_weight_fraction": fmt(fraction),
                    "coefficient_norm": fmt(np.sqrt(weight_sq)),
                    "is_exceptional_fibre": key == star_key,
                })
        support_rows.sort(key=lambda row: float(row["squared_weight_fraction"]), reverse=True)

        exceptional = {
            "performed": True,
            "exceptional_key": base.key_text(star_key),
            "amp18_arrival_rank": amp18_rank,
            "amp18_relation_dim": rec8.bases[star_key].basis.shape[1],
            "amp18_smallest_nonzero_coordinate_sv": fmt(amp18_sv[amp18_rank - 1]),
            "amp18_first_discarded_coordinate_sv": fmt(amp18_sv[amp18_rank]),
            "residue_norm": fmt(ystar_norm),
            "residue_pt_residual": fmt(ystar_pt),
            "residue_residual_to_full_image": fmt(ystar_to_image),
            "residue_residual_to_local_sector": fmt(ystar_to_local),
            "residue_residual_to_nonlocal_sector": fmt(ystar_to_nonlocal),
            "residue_residual_to_plus_image": fmt(ystar_to_plus),
            "residue_residual_to_minus_image": fmt(ystar_to_minus),
            "global_mp_reconstruction_residual": fmt(global_star_solve.reconstruction_residual),
            "global_mp_lift_norm": fmt(np.linalg.norm(global_star_lift)),
            "original_norm": fmt(np.linalg.norm(vstar)),
            "global_mp_cosine_with_original": fmt(section.cosine_abs(global_star_lift, vstar)),
            "global_mp_relative_distance_to_original": fmt(np.linalg.norm(global_star_difference) / np.linalg.norm(vstar)),
            "global_difference_delete_norm": fmt(global_star_difference_delete),
            "global_difference_pt_residual": fmt(global_star_difference_pt),
            "global_difference_is_source_kernel_vector": global_star_difference_delete <= args.containment_tolerance,
            "local_star_mp_reconstruction_residual": fmt(local_star_solve.reconstruction_residual),
            "local_star_mp_lift_norm": fmt(np.linalg.norm(local_star_lift)),
            "local_star_mp_cosine_with_original": fmt(section.cosine_abs(local_star_lift, vstar)),
            "local_star_mp_relative_distance_to_original": fmt(np.linalg.norm(local_star_lift - vstar) / np.linalg.norm(vstar)),
            "original_is_local_star_mp_lift": (
                local_star_solve.reconstruction_residual <= args.containment_tolerance
                and np.linalg.norm(local_star_lift - vstar) / np.linalg.norm(vstar) <= args.containment_tolerance
            ),
            "global_mp_exceptional_fibre_weight_fraction": fmt(exceptional_fraction),
            "global_mp_support_count": len(support_rows),
            "global_mp_support": support_rows,
            "interpretation_guardrail": (
                "The full-image Moore--Penrose lift is unique only for the chosen Euclidean inner product. "
                "Its difference from the original exceptional vector is a valid source-kernel relation, not an error."
            ),
        }

        print("\nExceptional direction in the full residue image")
        print(f"  residue PT residual:                 {ystar_pt:.3e}")
        print(f"  residual to full 110-d image:        {ystar_to_image:.3e}")
        print(f"  residual to local 38-d sector:       {ystar_to_local:.3e}")
        print(f"  residual to nonlocal complement:     {ystar_to_nonlocal:.3e}")
        print(f"  residual to plus branch image:       {ystar_to_plus:.3e}")
        print(f"  residual to minus branch image:      {ystar_to_minus:.3e}")
        print(f"  global MP reconstruction residual:   {global_star_solve.reconstruction_residual:.3e}")
        print(f"  global MP cosine with original:      {section.cosine_abs(global_star_lift, vstar):.6f}")
        print(f"  global MP lift norm:                 {np.linalg.norm(global_star_lift):.6f}")
        print(f"  original is local-star MP lift:      {exceptional['original_is_local_star_mp_lift']}")

    # Controls.
    positive = a[:, :1]
    pos_residual = section.max_column_relative_residual(
        positive, q_image @ (q_image.T @ positive)
    ) if positive.shape[1] else 0.0
    rng = np.random.default_rng(args.seed + 2_300_200)
    negative = rng.normal(size=(len(g7.states), 1))
    negative -= q_image @ (q_image.T @ negative)
    neg_residual = section.max_column_relative_residual(
        negative, q_image @ (q_image.T @ negative)
    )

    branch_rows = [
        {
            "space": "coupled_full_residue_image",
            "rank": image_rank,
            "local_sector_containment_residual": fmt(local_to_image),
            "nonlocal_sector_containment_residual": "0",
        },
        {
            "space": "plus_branch_image",
            "rank": plus_rank,
            "local_sector_containment_residual": fmt(local_in_plus),
            "nonlocal_sector_containment_residual": fmt(nonlocal_in_plus),
        },
        {
            "space": "minus_branch_image",
            "rank": minus_rank,
            "local_sector_containment_residual": fmt(local_in_minus),
            "nonlocal_sector_containment_residual": fmt(nonlocal_in_minus),
        },
        {
            "space": "independent_plus_minus_sum",
            "rank": branch_sum_rank,
            "local_sector_containment_residual": fmt(section.max_column_relative_residual(
                local_basis, q_branch_sum @ (q_branch_sum.T @ local_basis)
            )),
            "nonlocal_sector_containment_residual": fmt(section.max_column_relative_residual(
                q_nonlocal, q_branch_sum @ (q_branch_sum.T @ q_nonlocal)
            )) if nonlocal_rank else "0",
        },
    ]

    section_weight_rows = []
    section_weight_rows.extend(block_weight_rows(
        base, g8, full_section.coefficients, "full_110_image_section", args.support_fraction_threshold
    ))
    section_weight_rows.extend(block_weight_rows(
        base, g8, nonlocal_section.coefficients, "nonlocal_72_image_section", args.support_fraction_threshold
    ))

    spectrum_rows = []
    for name, values, rank in (
        ("coupled_full", image_sv, image_rank),
        ("plus", plus_sv, plus_rank),
        ("minus", minus_sv, minus_rank),
        ("independent_branch_sum", branch_sum_sv, branch_sum_rank),
        ("nonlocal_complement", nonlocal_sv, nonlocal_rank),
    ):
        for index, value in enumerate(values):
            spectrum_rows.append({
                "space": name,
                "index": index,
                "singular_value": fmt(value),
                "kept": index < rank,
                "relative_to_largest": fmt(value / values[0]) if len(values) and values[0] else "0",
            })

    reversal_audit = {
        "standard_chart_character_n8": chi8,
        "standard_plus_active_source_states": standard_plus_active,
        "standard_minus_active_source_states": standard_minus_active,
        "standard_chart_character_n7": chi7,
        "opposite_chart_active_source_states": opp_active,
        "opposite_chart_target_reversal_count": opp_reversals,
        "plus_equivariance_relative_frobenius_error": fmt(equiv_plus_error),
        "minus_equivariance_relative_frobenius_error": fmt(equiv_minus_error),
        "full_equivariance_relative_frobenius_error": fmt(equiv_full_error),
        "standard_plus_local_section_residual": fmt(local_in_plus),
        "standard_minus_local_section_residual": fmt(local_in_minus),
        "opposite_plus_local_section_residual": fmt(plus_opp_solve.reconstruction_residual),
        "opposite_minus_local_section_residual": fmt(minus_opp_solve.reconstruction_residual),
        "opposite_full_local_section_residual": fmt(full_opp_solve.reconstruction_residual),
        "branch_labels_swap_under_reversal": (
            equiv_plus_error <= args.containment_tolerance
            and equiv_minus_error <= args.containment_tolerance
            and plus_opp_solve.reconstruction_residual <= args.containment_tolerance
            and minus_opp_solve.reconstruction_residual > args.containment_tolerance
        ),
        "interpretation": (
            "If the branch labels swap and the one-sided section success swaps with them, the plus/minus asymmetry "
            "is a canonical-chart orientation effect rather than an invariant chirality."
        ),
    }

    full_image_audit = {
        "source_local_relation_dim": g8.basis.shape[1],
        "full_residue_image_rank": image_rank,
        "source_kernel_dim": g8.basis.shape[1] - image_rank,
        "full_image_section_residual": fmt(full_section_residual),
        "full_image_section_source_pt_residual": fmt(full_lift_pt),
        "full_image_target_pt_residual": fmt(full_target_pt),
        "local_sector_dim": local_basis.shape[1],
        "local_sector_residual_to_full_image": fmt(local_to_image),
        "nonlocal_complement_dim": nonlocal_rank,
        "nonlocal_complement_pt_residual": fmt(nonlocal_pt),
        "nonlocal_section_residual": fmt(nonlocal_section_residual),
        "local_nonlocal_orthogonality_error": fmt(local_nonlocal_orthogonality),
        "local_plus_nonlocal_rank": combined_rank,
        "image_residual_to_local_plus_nonlocal": fmt(image_to_local_nonlocal),
        "plus_image_rank": plus_rank,
        "minus_image_rank": minus_rank,
        "plus_minus_intersection_dim": branch_intersection_dim,
        "plus_minus_principal_cosines": [fmt(x) for x in branch_principal_cosines],
        "independent_branch_sum_rank": branch_sum_rank,
        "coupled_image_residual_to_independent_branch_sum": fmt(image_to_branch_sum),
        "positive_control_residual": fmt(pos_residual),
        "negative_control_residual": fmt(neg_residual),
    }

    write_csv(out_dir / "relation_basis_summary.csv", basis_rows)
    write_csv(out_dir / "branch_image_summary.csv", branch_rows)
    write_csv(out_dir / "residue_image_singular_spectrum.csv", spectrum_rows)
    write_csv(out_dir / "full_image_section_block_weights.csv", section_weight_rows)
    write_csv(out_dir / "exceptional_global_mp_support.csv", support_rows)
    with (out_dir / "branch_reversal_audit.json").open("w") as handle:
        json.dump(json_safe(reversal_audit), handle, indent=2, sort_keys=True)
    with (out_dir / "full_image_section_audit.json").open("w") as handle:
        json.dump(json_safe(full_image_audit), handle, indent=2, sort_keys=True)
    with (out_dir / "exceptional_full_image_audit.json").open("w") as handle:
        json.dump(json_safe(exceptional), handle, indent=2, sort_keys=True)

    np.savez_compressed(
        out_dir / "full_image_section_operator_data.npz",
        full_image_basis=q_image,
        local_target_basis=local_basis,
        nonlocal_target_basis=q_nonlocal,
        full_section_coordinate_matrix=full_section.coefficients,
        full_section_ambient_matrix=full_lift,
        nonlocal_section_coordinate_matrix=nonlocal_section.coefficients,
        coupled_residue_singular_values=image_sv,
        plus_residue_singular_values=plus_sv,
        minus_residue_singular_values=minus_sv,
        exceptional_original_vector=vstar,
        exceptional_residue=ystar,
        exceptional_global_mp_lift=global_star_lift,
        exceptional_local_star_mp_lift=local_star_lift,
        source_fibre_keys=np.array([base.key_text(k) for k in g8.keys]),
        target_fibre_keys=np.array([base.key_text(k) for k in g7.keys]),
    )

    summary = {
        "script": Path(__file__).name,
        "n_parent": 7,
        "n_child": 8,
        "full_image_audit": full_image_audit,
        "branch_reversal_audit": reversal_audit,
        "exceptional_audit": exceptional,
        "parameters": vars(args),
        "elapsed_seconds": time.time() - started,
        "output_files": [
            "summary.json",
            "run.log",
            "relation_basis_summary.csv",
            "branch_image_summary.csv",
            "residue_image_singular_spectrum.csv",
            "full_image_section_block_weights.csv",
            "exceptional_global_mp_support.csv",
            "branch_reversal_audit.json",
            "full_image_section_audit.json",
            "exceptional_full_image_audit.json",
            "full_image_section_operator_data.npz",
        ],
        "interpretation_guardrail": (
            "The branch-reversal audit distinguishes chart labels from invariant structure. "
            "The Moore--Penrose section is exact but depends on the chosen Euclidean inner product."
        ),
    }
    with (out_dir / "summary.json").open("w") as handle:
        json.dump(json_safe(summary), handle, indent=2, sort_keys=True)

    print("\n" + "=" * 112)
    print("FINAL SUMMARY")
    print("=" * 112)
    print(f"Exact section on full residue image:  {full_section_residual <= args.containment_tolerance}")
    print(f"Full residue image rank:              {image_rank}")
    print(f"Local/nonlocal decomposition:         {local_basis.shape[1]} + {nonlocal_rank} = {combined_rank}")
    print(f"Branch labels swap under reversal:    {reversal_audit['branch_labels_swap_under_reversal']}")
    if args.exceptional_audit:
        print(f"Exceptional lies in nonlocal sector:  {ystar_to_nonlocal <= args.containment_tolerance}")
        print(f"Exceptional global MP exact:          {global_star_solve.reconstruction_residual <= args.containment_tolerance}")
        print(f"Exceptional is local-star MP lift:    {exceptional['original_is_local_star_mp_lift']}")
    else:
        print("Exceptional audit:                    skipped")
    print(f"elapsed:                              {(time.time()-started)/60:.2f} minutes")
    print(f"summary:                              {out_dir / 'summary.json'}")
    print("=" * 112)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit branch-reversal equivariance and construct a section on the full 7-point residue image."
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
