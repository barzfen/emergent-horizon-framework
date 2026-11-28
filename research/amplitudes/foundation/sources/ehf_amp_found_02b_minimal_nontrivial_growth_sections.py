#!/usr/bin/env python3
"""
EHF-AMP-FOUND-02B: Minimal Nontrivial Growth Sections
======================================================

Construct explicit right inverses of the reflection-aware delete-8 residue map
on the complete chamber-local seven-point Parke--Taylor relation sector.

The probe starts from the independently reproduced 02A facts:

* the direct sum of n=7 chamber-local relation spaces has dimension 38;
* reflection-aware residues of n=8 chamber-local relations contain that entire
  38-dimensional sector;
* unchanged-coefficient state insertion fails for every genuine relation.

02B therefore solves the actual linear section problem

    D_8 L = identity on R_7^local,

where D_8 is the signed anchor-collinear delete-8 operator and the image of L is
required to lie in the direct sum of n=8 chamber-local relation spaces.

The canonical section reported by the probe is the Moore--Penrose minimum-
Euclidean-norm section.  This is an exact algebraic construction, but not yet a
claim that the Euclidean norm or the resulting dense map is physically
preferred.  Additional diagnostics test branch-only, direct-child, incident-
child, sparse-block and exceptional-direction structure.

Example
-------

    caffeinate -i python3 scripts/ehf_amp_found_02b_minimal_nontrivial_growth_sections.py \
      --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
      --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
      --base-run-dir runs/ehf_amp_found_01_amp18_20 \
      --out-dir runs/ehf_amp_found_02b_seed11 \
      --seed 11
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
import time
from dataclasses import dataclass
from itertools import combinations
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


def rank_from_singular_values(
    singular_values: np.ndarray,
    relative_tolerance: float,
    absolute_tolerance: float,
) -> int:
    if singular_values.size == 0 or singular_values[0] == 0:
        return 0
    threshold = max(absolute_tolerance, singular_values[0] * relative_tolerance)
    return int(np.count_nonzero(singular_values > threshold))


def orthonormal_span(
    matrix: np.ndarray,
    relative_tolerance: float,
    absolute_tolerance: float,
) -> Tuple[np.ndarray, np.ndarray, int]:
    if matrix.size == 0 or matrix.shape[1] == 0:
        return np.zeros((matrix.shape[0], 0), dtype=float), np.zeros(0), 0
    u, s, _ = np.linalg.svd(np.asarray(matrix, dtype=float), full_matrices=False)
    rank = rank_from_singular_values(s, relative_tolerance, absolute_tolerance)
    return u[:, :rank], s, rank


def max_column_relative_residual(target: np.ndarray, approximation: np.ndarray) -> float:
    if target.size == 0 or target.shape[1] == 0:
        return 0.0
    delta = target - approximation
    den = np.linalg.norm(target, axis=0)
    mask = den > 1e-14
    if not np.any(mask):
        return 0.0
    return float(np.max(np.linalg.norm(delta[:, mask], axis=0) / den[mask]))


def span_containment_residual(
    target: np.ndarray,
    source: np.ndarray,
    relative_tolerance: float,
    absolute_tolerance: float,
) -> Tuple[float, int, np.ndarray]:
    q, s, rank = orthonormal_span(source, relative_tolerance, absolute_tolerance)
    approximation = q @ (q.T @ target) if rank else np.zeros_like(target)
    return max_column_relative_residual(target, approximation), rank, s


@dataclass
class SolveResult:
    coefficients: np.ndarray
    rank: int
    singular_values: np.ndarray
    reconstruction_residual: float
    source_norm: float
    smallest_nonzero_sv: float
    first_discarded_sv: float


def minimum_norm_solve(
    source: np.ndarray,
    target: np.ndarray,
    relative_tolerance: float,
    absolute_tolerance: float,
) -> SolveResult:
    """Solve source @ X = target using the rank-truncated Moore--Penrose inverse."""
    if source.shape[1] == 0:
        coeff = np.zeros((0, target.shape[1]), dtype=float)
        return SolveResult(
            coefficients=coeff,
            rank=0,
            singular_values=np.zeros(0),
            reconstruction_residual=max_column_relative_residual(target, np.zeros_like(target)),
            source_norm=0.0,
            smallest_nonzero_sv=0.0,
            first_discarded_sv=0.0,
        )
    u, s, vh = np.linalg.svd(np.asarray(source, dtype=float), full_matrices=False)
    rank = rank_from_singular_values(s, relative_tolerance, absolute_tolerance)
    if rank:
        coeff = vh[:rank].T @ ((u[:, :rank].T @ target) / s[:rank, None])
    else:
        coeff = np.zeros((source.shape[1], target.shape[1]), dtype=float)
    approximation = source @ coeff
    residual = max_column_relative_residual(target, approximation)
    return SolveResult(
        coefficients=coeff,
        rank=rank,
        singular_values=s,
        reconstruction_residual=residual,
        source_norm=float(np.linalg.norm(coeff)),
        smallest_nonzero_sv=float(s[rank - 1]) if rank else 0.0,
        first_discarded_sv=float(s[rank]) if rank < len(s) else 0.0,
    )


def pt_residual(base, states: Sequence[Cycle], n: int, vectors: np.ndarray, seed: int, rows: int) -> float:
    if vectors.size == 0 or vectors.shape[1] == 0:
        return 0.0
    matrix = base.parke_taylor_matrix(states, n, seed, rows)
    norms = np.linalg.norm(vectors, axis=0)
    mask = norms > 1e-13
    if not np.any(mask):
        return 0.0
    return float(np.max(np.linalg.norm(matrix @ vectors[:, mask], axis=0) / norms[mask]))


def cosine_abs(x: np.ndarray, y: np.ndarray) -> float:
    nx = float(np.linalg.norm(x))
    ny = float(np.linalg.norm(y))
    if nx == 0 or ny == 0:
        return 0.0
    return float(abs(np.vdot(x.ravel(), y.ravel())) / (nx * ny))


@dataclass
class GlobalBasis:
    states: List[Cycle]
    state_index: Dict[Cycle, int]
    basis: np.ndarray
    slices: Dict[FibreKey, slice]
    keys: List[FibreKey]
    relation_dims: Dict[FibreKey, int]


def build_global_local_basis(base, record) -> GlobalBasis:
    n = len(next(iter(record.fibres.values()))[0])
    states = base.canonical_cycles(n)
    state_index = {c: i for i, c in enumerate(states)}
    total = sum(record.bases[key].basis.shape[1] for key in record.fibres)
    matrix = np.zeros((len(states), total), dtype=float)
    slices: Dict[FibreKey, slice] = {}
    relation_dims: Dict[FibreKey, int] = {}
    keys: List[FibreKey] = []
    cursor = 0
    for key, chamber in record.fibres.items():
        local = record.bases[key].basis
        dim = local.shape[1]
        sl = slice(cursor, cursor + dim)
        slices[key] = sl
        relation_dims[key] = dim
        keys.append(key)
        if dim:
            rows = [state_index[c] for c in chamber]
            matrix[np.ix_(rows, range(cursor, cursor + dim))] = local
        cursor += dim
    gram_error = float(np.linalg.norm(matrix.T @ matrix - np.eye(total))) if total else 0.0
    if gram_error > 1e-7:
        raise RuntimeError(f"Global direct-sum basis is not orthonormal; Gram error={gram_error:.3e}")
    return GlobalBasis(states, state_index, matrix, slices, keys, relation_dims)


def build_delete_operator(base, helper, source_states: Sequence[Cycle], target_states: Sequence[Cycle], new_label: int):
    target_index = {c: i for i, c in enumerate(target_states)}
    full = np.zeros((len(target_states), len(source_states)), dtype=float)
    plus = np.zeros_like(full)
    minus = np.zeros_like(full)
    reached_parent_keys: Dict[FibreKey, set] = {}
    child_to_parent_keys: Dict[FibreKey, set] = {}
    for column, cycle in enumerate(source_states):
        if cycle[1] != new_label and cycle[-1] != new_label:
            continue
        sign, image, side_sign, _, _ = helper.delete_new_label(base, cycle, new_label)
        row = target_index[image]
        full[row, column] += sign
        if side_sign == +1:
            plus[row, column] += sign
        else:
            minus[row, column] += sign
        child_key = base.pi_key(cycle)
        parent_key = base.pi_key(image)
        child_to_parent_keys.setdefault(child_key, set()).add(parent_key)
        reached_parent_keys.setdefault(parent_key, set()).add(child_key)
    return full, plus, minus, child_to_parent_keys, reached_parent_keys


def direct_growth_children(base, helper, parent: Sequence[Cycle], new_label: int) -> Tuple[List[FibreKey], Dict[str, List[FibreKey]]]:
    n = len(parent[0])
    result: Dict[str, List[FibreKey]] = {}
    for name, gap in (("plus", 1), ("minus", n)):
        keys = sorted({base.pi_key(helper.insert_cycle(base, c, gap, new_label)) for c in parent})
        result[name] = keys
    union = sorted(set(result["plus"]) | set(result["minus"]))
    return union, result


def block_columns(slices: Mapping[FibreKey, slice], keys: Iterable[FibreKey]) -> List[int]:
    columns: List[int] = []
    for key in keys:
        sl = slices[key]
        columns.extend(range(sl.start, sl.stop))
    return columns


def solve_with_blocks(
    a: np.ndarray,
    target: np.ndarray,
    source_slices: Mapping[FibreKey, slice],
    keys: Sequence[FibreKey],
    args,
) -> SolveResult:
    columns = block_columns(source_slices, keys)
    return minimum_norm_solve(
        a[:, columns] if columns else np.zeros((a.shape[0], 0)),
        target,
        args.rank_tolerance,
        args.rank_absolute_tolerance,
    )


def greedy_block_cover(
    a: np.ndarray,
    target: np.ndarray,
    source_slices: Mapping[FibreKey, slice],
    candidates: Sequence[FibreKey],
    args,
) -> Tuple[List[FibreKey], SolveResult, List[Dict[str, object]]]:
    """Greedy block-sparse exact section; an upper bound, not a proof of minimum cardinality."""
    selected: List[FibreKey] = []
    remaining = list(candidates)
    trace: List[Dict[str, object]] = []
    current = solve_with_blocks(a, target, source_slices, selected, args)
    while current.reconstruction_residual > args.containment_tolerance and remaining:
        best_key: Optional[FibreKey] = None
        best_result: Optional[SolveResult] = None
        for key in remaining:
            trial = solve_with_blocks(a, target, source_slices, selected + [key], args)
            if best_result is None:
                best_key, best_result = key, trial
                continue
            if trial.reconstruction_residual < best_result.reconstruction_residual - 1e-12:
                best_key, best_result = key, trial
            elif abs(trial.reconstruction_residual - best_result.reconstruction_residual) <= 1e-12:
                if trial.rank > best_result.rank:
                    best_key, best_result = key, trial
                elif trial.rank == best_result.rank and trial.source_norm < best_result.source_norm:
                    best_key, best_result = key, trial
        if best_key is None or best_result is None:
            break
        selected.append(best_key)
        remaining.remove(best_key)
        current = best_result
        trace.append({
            "step": len(selected),
            "added_key": best_key,
            "selected_count": len(selected),
            "source_rank": current.rank,
            "reconstruction_residual": current.reconstruction_residual,
        })
        if len(selected) >= args.greedy_max_blocks:
            break

    # Backward prune while exactness is retained.
    if current.reconstruction_residual <= args.containment_tolerance:
        changed = True
        while changed:
            changed = False
            for key in list(selected):
                trial_keys = [x for x in selected if x != key]
                trial = solve_with_blocks(a, target, source_slices, trial_keys, args)
                if trial.reconstruction_residual <= args.containment_tolerance:
                    selected = trial_keys
                    current = trial
                    changed = True
                    break
    return selected, current, trace


def reconstruct_exceptional_direction(base, helper, rec8, rec9, args):
    target_set = tuple(sorted(int(x) for x in args.exceptional_set.split(",") if x.strip()))
    star_key = None
    for key in rec8.fibres:
        anchor_set = key[0] if 1 in key[0] else key[1]
        if tuple(anchor_set) == target_set:
            star_key = key
            break
    if star_key is None:
        raise RuntimeError(f"Exceptional fibre not found: {target_set}")

    star = rec8.fibres[star_key]
    nstar = rec8.bases[star_key].basis
    target_indices = {key: {c: i for i, c in enumerate(ch)} for key, ch in rec8.fibres.items()}
    arrivals: List[np.ndarray] = []
    for source_key, source in rec9.fibres.items():
        source_basis = rec9.bases[source_key].basis
        if source_basis.shape[1] == 0:
            continue
        for deleted_label in range(2, 10):
            result = base.anchor_one_local_residue_block(
                source=source,
                source_basis=source_basis,
                deleted_label=deleted_label,
                n=9,
                target_fibres=rec8.fibres,
                target_indices=target_indices,
            )
            if result is not None and result[0] == star_key and result[1].shape[1]:
                arrivals.append(result[1])
    arrival = np.hstack(arrivals) if arrivals else np.zeros((len(star), 0))
    coords = nstar.T @ arrival
    u, s, _ = np.linalg.svd(coords, full_matrices=False)
    rank = rank_from_singular_values(s, args.rank_tolerance, args.rank_absolute_tolerance)
    missing_dim = nstar.shape[1] - rank
    if missing_dim != 1:
        raise RuntimeError(f"Expected one-dimensional AMP-18 gap, found {missing_dim}")
    missing_local = nstar @ u[:, rank:rank + 1]
    missing_local /= np.linalg.norm(missing_local)
    return star_key, star, missing_local, rank, s


def run(args: argparse.Namespace) -> Dict[str, object]:
    started = time.time()
    base_script = Path(args.base_script).resolve()
    helper_script = Path(args.helper_script).resolve()
    base_run_dir = Path(args.base_run_dir).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = base_run_dir / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    base = load_module(base_script, "ehf_amp_found_01_base_for_02b")
    helper = load_module(helper_script, "ehf_amp_found_02a_helper_for_02b")

    print("=" * 108)
    print("EHF-AMP-FOUND-02B: MINIMAL NONTRIVIAL GROWTH SECTIONS")
    print("=" * 108)
    print(f"base script:                  {base_script}")
    print(f"reflection-aware helper:      {helper_script}")
    print(f"shared cache:                 {cache_dir}")
    print(f"output directory:             {out_dir}")
    print(f"seed:                         {args.seed}")
    print(f"rank tolerance:               {args.rank_tolerance}")
    print(f"containment tolerance:        {args.containment_tolerance}")

    basis_rows: List[Dict[str, object]] = []
    rec7 = helper.build_bases_for_n(base, 7, cache_dir, args, basis_rows)
    rec8 = helper.build_bases_for_n(base, 8, cache_dir, args, basis_rows)
    rec9 = helper.build_bases_for_n(base, 9, cache_dir, args, basis_rows) if args.exceptional_audit else None

    g7 = build_global_local_basis(base, rec7)
    g8 = build_global_local_basis(base, rec8)
    print(f"\nDirect-sum local relation dimensions: n=7 -> {g7.basis.shape[1]}, n=8 -> {g8.basis.shape[1]}")

    d, dplus, dminus, child_to_parents, parent_to_children = build_delete_operator(
        base, helper, g8.states, g7.states, 8
    )
    a = d @ g8.basis
    aplus = dplus @ g8.basis
    aminus = dminus @ g8.basis

    full_solve = minimum_norm_solve(a, g7.basis, args.rank_tolerance, args.rank_absolute_tolerance)
    c = full_solve.coefficients
    lift = g8.basis @ c
    reconstructed = d @ lift
    section_residual = max_column_relative_residual(g7.basis, reconstructed)
    source_pt = pt_residual(base, g8.states, 8, lift, args.seed + 920_001, args.validation_rows)
    target_pt = pt_residual(base, g7.states, 7, reconstructed, args.seed + 920_002, args.validation_rows)
    section_plus_image = dplus @ lift
    section_minus_image = dminus @ lift
    section_branch_sum_residual = max_column_relative_residual(
        reconstructed, section_plus_image + section_minus_image
    )
    section_plus_pt = pt_residual(
        base, g7.states, 7, section_plus_image, args.seed + 920_003, args.validation_rows
    )
    section_minus_pt = pt_residual(
        base, g7.states, 7, section_minus_image, args.seed + 920_004, args.validation_rows
    )
    section_plus_local_residual = max_column_relative_residual(
        section_plus_image, g7.basis @ (g7.basis.T @ section_plus_image)
    )
    section_minus_local_residual = max_column_relative_residual(
        section_minus_image, g7.basis @ (g7.basis.T @ section_minus_image)
    )

    aq, a_s, a_rank = orthonormal_span(a, args.rank_tolerance, args.rank_absolute_tolerance)
    target_containment = max_column_relative_residual(g7.basis, aq @ (aq.T @ g7.basis))
    local_kernel_dim = g8.basis.shape[1] - a_rank

    plus_solve = minimum_norm_solve(aplus, g7.basis, args.rank_tolerance, args.rank_absolute_tolerance)
    minus_solve = minimum_norm_solve(aminus, g7.basis, args.rank_tolerance, args.rank_absolute_tolerance)

    # Controls: raw source column must lie in span(A); an ambient complement vector must not.
    pos = a[:, :1]
    pos_residual = max_column_relative_residual(pos, aq @ (aq.T @ pos)) if pos.shape[1] else 0.0
    rng = np.random.default_rng(args.seed + 920_100)
    negative = rng.normal(size=(len(g7.states), 1))
    negative -= aq @ (aq.T @ negative)
    negative_projection = aq @ (aq.T @ negative)
    neg_residual = max_column_relative_residual(negative, negative_projection)

    print("\nGlobal section audit")
    print(f"  residue image rank:                  {a_rank}/{g8.basis.shape[1]}")
    print(f"  local source kernel dimension:       {local_kernel_dim}")
    print(f"  target local-sector dimension:       {g7.basis.shape[1]}")
    print(f"  target containment residual:         {target_containment:.3e}")
    print(f"  minimum-norm section residual:       {section_residual:.3e}")
    print(f"  lifted n=8 PT residual:              {source_pt:.3e}")
    print(f"  reconstructed n=7 PT residual:       {target_pt:.3e}")
    print(f"  plus-only section residual:          {plus_solve.reconstruction_residual:.3e}")
    print(f"  minus-only section residual:         {minus_solve.reconstruction_residual:.3e}")

    singular_rows: List[Dict[str, object]] = []
    for index, value in enumerate(full_solve.singular_values):
        singular_rows.append({
            "index": index,
            "singular_value": fmt(value),
            "kept": index < full_solve.rank,
            "relative_to_largest": fmt(value / full_solve.singular_values[0]) if full_solve.singular_values[0] else "0",
        })

    parent_rows: List[Dict[str, object]] = []
    block_weight_rows: List[Dict[str, object]] = []
    greedy_trace_rows: List[Dict[str, object]] = []

    nonzero_parent_keys = [key for key in g7.keys if g7.relation_dims[key] > 0]
    child_keys = list(g8.keys)

    for parent_key in nonzero_parent_keys:
        psl = g7.slices[parent_key]
        target = g7.basis[:, psl]
        direct_keys, direct_by_branch = direct_growth_children(base, helper, rec7.fibres[parent_key], 8)
        incident_keys = sorted(parent_to_children.get(parent_key, set()))

        direct_result = solve_with_blocks(a, target, g8.slices, direct_keys, args)
        incident_result = solve_with_blocks(a, target, g8.slices, incident_keys, args)
        plus_direct_keys = direct_by_branch["plus"]
        minus_direct_keys = direct_by_branch["minus"]
        plus_child_full_result = solve_with_blocks(a, target, g8.slices, plus_direct_keys, args)
        minus_child_full_result = solve_with_blocks(a, target, g8.slices, minus_direct_keys, args)
        plus_child_matching_result = solve_with_blocks(aplus, target, g8.slices, plus_direct_keys, args)
        minus_child_matching_result = solve_with_blocks(aminus, target, g8.slices, minus_direct_keys, args)

        single_exact: List[FibreKey] = []
        best_single_key: Optional[FibreKey] = None
        best_single_residual = float("inf")
        for child_key in incident_keys:
            result = solve_with_blocks(a, target, g8.slices, [child_key], args)
            if result.reconstruction_residual < best_single_residual:
                best_single_key = child_key
                best_single_residual = result.reconstruction_residual
            if result.reconstruction_residual <= args.containment_tolerance:
                single_exact.append(child_key)

        if args.run_greedy:
            greedy_keys, greedy_result, trace = greedy_block_cover(
                a, target, g8.slices, incident_keys if incident_keys else child_keys, args
            )
            for row in trace:
                greedy_trace_rows.append({
                    "scope": "parent",
                    "parent_key": base.key_text(parent_key),
                    "step": row["step"],
                    "added_child_key": base.key_text(row["added_key"]),
                    "selected_count": row["selected_count"],
                    "source_rank": row["source_rank"],
                    "reconstruction_residual": fmt(row["reconstruction_residual"]),
                })
        else:
            greedy_keys = []
            greedy_result = SolveResult(
                coefficients=np.zeros((0, target.shape[1])), rank=0,
                singular_values=np.zeros(0), reconstruction_residual=float("nan"),
                source_norm=0.0, smallest_nonzero_sv=0.0, first_discarded_sv=0.0,
            )

        coeff_block = c[:, psl]
        total_sq = float(np.linalg.norm(coeff_block) ** 2)
        direct_sq = 0.0
        incident_sq = 0.0
        support_count = 0
        for child_key in child_keys:
            csl = g8.slices[child_key]
            weight = float(np.linalg.norm(coeff_block[csl, :]) ** 2)
            fraction = weight / total_sq if total_sq else 0.0
            if fraction > args.support_fraction_threshold:
                support_count += 1
            if child_key in direct_keys:
                direct_sq += weight
            if child_key in incident_keys:
                incident_sq += weight
            block_weight_rows.append({
                "parent_key": base.key_text(parent_key),
                "child_key": base.key_text(child_key),
                "parent_relation_dim": g7.relation_dims[parent_key],
                "child_relation_dim": g8.relation_dims[child_key],
                "coefficient_frobenius_norm": fmt(np.sqrt(weight)),
                "squared_weight_fraction": fmt(fraction),
                "is_direct_growth_child": child_key in direct_keys,
                "is_incident_residue_child": child_key in incident_keys,
                "above_support_threshold": fraction > args.support_fraction_threshold,
            })

        parent_rows.append({
            "parent_key": base.key_text(parent_key),
            "parent_size": len(rec7.fibres[parent_key]),
            "parent_relation_dim": g7.relation_dims[parent_key],
            "direct_plus_child_keys": ";".join(base.key_text(k) for k in direct_by_branch["plus"]),
            "direct_minus_child_keys": ";".join(base.key_text(k) for k in direct_by_branch["minus"]),
            "direct_child_count": len(direct_keys),
            "incident_child_count": len(incident_keys),
            "direct_child_section_residual": fmt(direct_result.reconstruction_residual),
            "direct_child_section_exists": direct_result.reconstruction_residual <= args.containment_tolerance,
            "plus_direct_child_full_residue_section_residual": fmt(plus_child_full_result.reconstruction_residual),
            "plus_direct_child_full_residue_section_exists": plus_child_full_result.reconstruction_residual <= args.containment_tolerance,
            "minus_direct_child_full_residue_section_residual": fmt(minus_child_full_result.reconstruction_residual),
            "minus_direct_child_full_residue_section_exists": minus_child_full_result.reconstruction_residual <= args.containment_tolerance,
            "plus_direct_child_matching_branch_residual": fmt(plus_child_matching_result.reconstruction_residual),
            "plus_direct_child_matching_branch_section_exists": plus_child_matching_result.reconstruction_residual <= args.containment_tolerance,
            "minus_direct_child_matching_branch_residual": fmt(minus_child_matching_result.reconstruction_residual),
            "minus_direct_child_matching_branch_section_exists": minus_child_matching_result.reconstruction_residual <= args.containment_tolerance,
            "incident_child_section_residual": fmt(incident_result.reconstruction_residual),
            "incident_child_section_exists": incident_result.reconstruction_residual <= args.containment_tolerance,
            "single_child_exact_count": len(single_exact),
            "single_child_exact_keys": ";".join(base.key_text(k) for k in single_exact),
            "best_single_child_key": "" if best_single_key is None else base.key_text(best_single_key),
            "best_single_child_residual": "" if best_single_key is None else fmt(best_single_residual),
            "greedy_incident_child_count": len(greedy_keys),
            "greedy_incident_child_keys": ";".join(base.key_text(k) for k in greedy_keys),
            "greedy_incident_section_residual": fmt(greedy_result.reconstruction_residual),
            "global_min_norm_section_frobenius_norm": fmt(np.sqrt(total_sq)),
            "global_min_norm_child_support_count": support_count,
            "global_min_norm_direct_weight_fraction": fmt(direct_sq / total_sq if total_sq else 0.0),
            "global_min_norm_incident_weight_fraction": fmt(incident_sq / total_sq if total_sq else 0.0),
        })

    if args.run_greedy:
        global_greedy_keys, global_greedy_result, global_trace = greedy_block_cover(
            a, g7.basis, g8.slices, child_keys, args
        )
        for row in global_trace:
            greedy_trace_rows.append({
                "scope": "global",
                "parent_key": "ALL_NONZERO_LOCAL_RELATIONS",
                "step": row["step"],
                "added_child_key": base.key_text(row["added_key"]),
                "selected_count": row["selected_count"],
                "source_rank": row["source_rank"],
                "reconstruction_residual": fmt(row["reconstruction_residual"]),
            })
    else:
        global_greedy_keys = []
        global_greedy_result = SolveResult(
            coefficients=np.zeros((0, g7.basis.shape[1])), rank=0,
            singular_values=np.zeros(0), reconstruction_residual=float("nan"),
            source_norm=0.0, smallest_nonzero_sv=0.0, first_discarded_sv=0.0,
        )

    print("\nLocality audit")
    print(f"  nonzero parent fibres:               {len(nonzero_parent_keys)}")
    print(f"  direct-child sections:               {sum(bool(r['direct_child_section_exists']) for r in parent_rows)}/{len(parent_rows)}")
    print(f"  plus-child/full-residue sections:    {sum(bool(r['plus_direct_child_full_residue_section_exists']) for r in parent_rows)}/{len(parent_rows)}")
    print(f"  minus-child/full-residue sections:   {sum(bool(r['minus_direct_child_full_residue_section_exists']) for r in parent_rows)}/{len(parent_rows)}")
    print(f"  plus matching-branch sections:       {sum(bool(r['plus_direct_child_matching_branch_section_exists']) for r in parent_rows)}/{len(parent_rows)}")
    print(f"  minus matching-branch sections:      {sum(bool(r['minus_direct_child_matching_branch_section_exists']) for r in parent_rows)}/{len(parent_rows)}")
    print(f"  incident-child sections:             {sum(bool(r['incident_child_section_exists']) for r in parent_rows)}/{len(parent_rows)}")
    print(f"  parent fibres with a one-child lift: {sum(int(r['single_child_exact_count']) > 0 for r in parent_rows)}/{len(parent_rows)}")
    if args.run_greedy:
        print(f"  greedy global child-block cover:     {len(global_greedy_keys)} blocks, residual {global_greedy_result.reconstruction_residual:.3e}")
    else:
        print("  greedy block audit:                  skipped (enable with --run-greedy)")

    exceptional: Dict[str, object] = {"performed": False, "reason": "Disabled."}
    if args.exceptional_audit:
        assert rec9 is not None
        star_key, star, missing_local, amp18_rank, amp18_sv = reconstruct_exceptional_direction(
            base, helper, rec8, rec9, args
        )
        vstar = np.zeros((len(g8.states), 1), dtype=float)
        star_rows = [g8.state_index[x] for x in star]
        vstar[star_rows, :] = missing_local
        residue = d @ vstar
        residue_local_coordinates = g7.basis.T @ residue
        residue_local_reconstruction = g7.basis @ residue_local_coordinates
        residue_to_local = max_column_relative_residual(residue, residue_local_reconstruction)

        global_lift = lift @ residue_local_coordinates
        global_reconstruction = d @ global_lift
        global_residual = max_column_relative_residual(residue, global_reconstruction)

        star_slice = g8.slices[star_key]
        astar = a[:, star_slice]
        local_star_solve = minimum_norm_solve(
            astar, residue, args.rank_tolerance, args.rank_absolute_tolerance
        )
        local_star_lift = g8.basis[:, star_slice] @ local_star_solve.coefficients
        local_star_residual = max_column_relative_residual(residue, d @ local_star_lift)

        global_difference = vstar - global_lift
        local_difference = vstar - local_star_lift
        global_kernel_error = float(np.linalg.norm(d @ global_difference))
        local_kernel_error = float(np.linalg.norm(d @ local_difference))

        global_coeff = c @ residue_local_coordinates
        total_sq = float(np.linalg.norm(global_coeff) ** 2)
        star_sq = float(np.linalg.norm(global_coeff[star_slice, :]) ** 2)
        support = []
        for child_key in child_keys:
            sl = g8.slices[child_key]
            fraction = float(np.linalg.norm(global_coeff[sl, :]) ** 2) / total_sq if total_sq else 0.0
            if fraction > args.support_fraction_threshold:
                support.append((child_key, fraction))
        support.sort(key=lambda item: item[1], reverse=True)

        exceptional = {
            "performed": True,
            "exceptional_key": base.key_text(star_key),
            "amp18_arrival_rank": amp18_rank,
            "amp18_relation_dim": rec8.bases[star_key].basis.shape[1],
            "amp18_smallest_nonzero_coordinate_sv": fmt(amp18_sv[amp18_rank - 1]),
            "amp18_first_discarded_coordinate_sv": fmt(amp18_sv[amp18_rank]),
            "residue_norm": fmt(float(np.linalg.norm(residue))),
            "residue_residual_to_n7_local_sector": fmt(residue_to_local),
            "global_min_norm_lift_reconstruction_residual": fmt(global_residual),
            "global_min_norm_lift_norm": fmt(float(np.linalg.norm(global_lift))),
            "original_exceptional_direction_norm": fmt(float(np.linalg.norm(vstar))),
            "global_min_norm_lift_cosine_with_original": fmt(cosine_abs(global_lift, vstar)),
            "global_min_norm_lift_relative_distance_to_original": fmt(float(np.linalg.norm(global_difference) / np.linalg.norm(vstar))),
            "global_difference_delete_norm": fmt(global_kernel_error),
            "global_min_norm_exceptional_fibre_weight_fraction": fmt(star_sq / total_sq if total_sq else 0.0),
            "global_min_norm_child_support_count": len(support),
            "global_min_norm_child_support": [
                {"child_key": base.key_text(key), "squared_weight_fraction": fmt(frac)}
                for key, frac in support
            ],
            "local_exceptional_residue_rank": local_star_solve.rank,
            "local_exceptional_kernel_dim": rec8.bases[star_key].basis.shape[1] - local_star_solve.rank,
            "local_star_min_norm_reconstruction_residual": fmt(local_star_residual),
            "local_star_min_norm_lift_norm": fmt(float(np.linalg.norm(local_star_lift))),
            "local_star_min_norm_lift_cosine_with_original": fmt(cosine_abs(local_star_lift, vstar)),
            "local_star_min_norm_relative_distance_to_original": fmt(float(np.linalg.norm(local_difference) / np.linalg.norm(vstar))),
            "local_difference_delete_norm": fmt(local_kernel_error),
            "original_is_local_moore_penrose_lift": (
                local_star_residual <= args.containment_tolerance
                and float(np.linalg.norm(local_difference) / np.linalg.norm(vstar)) <= args.containment_tolerance
            ),
            "interpretation_guardrail": (
                "The Moore--Penrose section is canonical only after choosing the ambient Euclidean inner product. "
                "Exact reconstruction proves existence of a constant linear right inverse, not that this dense section "
                "is the physical or combinatorially natural growth law."
            ),
        }
        print("\nExceptional-direction section audit")
        print(f"  residue lies in n=7 local sector:    residual {residue_to_local:.3e}")
        print(f"  global min-norm lift cosine:         {cosine_abs(global_lift, vstar):.6f}")
        print(f"  local-star min-norm lift cosine:     {cosine_abs(local_star_lift, vstar):.6f}")
        print(f"  original is local MP lift:           {exceptional['original_is_local_moore_penrose_lift']}")

    write_csv(out_dir / "relation_basis_summary.csv", basis_rows)
    write_csv(out_dir / "residue_singular_spectrum.csv", singular_rows)
    write_csv(out_dir / "parent_section_summary.csv", parent_rows)
    write_csv(out_dir / "section_block_weights.csv", block_weight_rows)
    write_csv(out_dir / "greedy_block_trace.csv", greedy_trace_rows)
    with (out_dir / "exceptional_section_audit.json").open("w") as handle:
        json.dump(json_safe(exceptional), handle, indent=2, sort_keys=True)

    np.savez_compressed(
        out_dir / "section_operator_data.npz",
        section_coordinate_matrix=c,
        section_ambient_matrix=lift,
        target_local_basis=g7.basis,
        residue_singular_values=full_solve.singular_values,
        plus_residue_singular_values=plus_solve.singular_values,
        minus_residue_singular_values=minus_solve.singular_values,
        source_fibre_keys=np.array([base.key_text(k) for k in g8.keys]),
        target_fibre_keys=np.array([base.key_text(k) for k in g7.keys]),
    )

    summary = {
        "script": Path(__file__).name,
        "n_parent": 7,
        "n_child": 8,
        "source_local_relation_dim": g8.basis.shape[1],
        "target_local_relation_dim": g7.basis.shape[1],
        "residue_image_rank": a_rank,
        "source_local_kernel_dim": local_kernel_dim,
        "target_containment_residual": target_containment,
        "minimum_norm_section_residual": section_residual,
        "minimum_norm_section_frobenius_norm": float(np.linalg.norm(c)),
        "lifted_source_pt_residual": source_pt,
        "reconstructed_target_pt_residual": target_pt,
        "section_branch_sum_residual": section_branch_sum_residual,
        "section_plus_image_frobenius_norm": float(np.linalg.norm(section_plus_image)),
        "section_minus_image_frobenius_norm": float(np.linalg.norm(section_minus_image)),
        "section_plus_image_pt_residual": section_plus_pt,
        "section_minus_image_pt_residual": section_minus_pt,
        "section_plus_image_residual_to_local_sector": section_plus_local_residual,
        "section_minus_image_residual_to_local_sector": section_minus_local_residual,
        "smallest_nonzero_residue_sv": full_solve.smallest_nonzero_sv,
        "first_discarded_residue_sv": full_solve.first_discarded_sv,
        "residue_condition_number_on_image": (
            float(full_solve.singular_values[0] / full_solve.singular_values[a_rank - 1]) if a_rank else None
        ),
        "plus_only_rank": plus_solve.rank,
        "plus_only_section_residual": plus_solve.reconstruction_residual,
        "minus_only_rank": minus_solve.rank,
        "minus_only_section_residual": minus_solve.reconstruction_residual,
        "positive_control_residual": pos_residual,
        "negative_control_residual": neg_residual,
        "nonzero_parent_fibre_count": len(nonzero_parent_keys),
        "direct_child_section_count": sum(bool(r["direct_child_section_exists"]) for r in parent_rows),
        "plus_direct_child_full_residue_section_count": sum(bool(r["plus_direct_child_full_residue_section_exists"]) for r in parent_rows),
        "minus_direct_child_full_residue_section_count": sum(bool(r["minus_direct_child_full_residue_section_exists"]) for r in parent_rows),
        "plus_direct_child_matching_branch_section_count": sum(bool(r["plus_direct_child_matching_branch_section_exists"]) for r in parent_rows),
        "minus_direct_child_matching_branch_section_count": sum(bool(r["minus_direct_child_matching_branch_section_exists"]) for r in parent_rows),
        "incident_child_section_count": sum(bool(r["incident_child_section_exists"]) for r in parent_rows),
        "single_child_section_parent_count": sum(int(r["single_child_exact_count"]) > 0 for r in parent_rows),
        "greedy_audit_performed": args.run_greedy,
        "greedy_global_child_block_count": len(global_greedy_keys) if args.run_greedy else None,
        "greedy_global_child_block_keys": [base.key_text(k) for k in global_greedy_keys],
        "greedy_global_section_residual": global_greedy_result.reconstruction_residual if args.run_greedy else None,
        "exceptional_audit": exceptional,
        "parameters": vars(args),
        "elapsed_seconds": time.time() - started,
        "interpretation_guardrail": (
            "The global Moore--Penrose section is the unique minimum-Euclidean-norm algebraic right inverse. "
            "It is not automatically sparse, fibre-local, symmetry-natural or physical. Greedy block counts are "
            "upper bounds, not proofs of minimum block cardinality."
        ),
        "output_files": [
            "summary.json",
            "run.log",
            "relation_basis_summary.csv",
            "residue_singular_spectrum.csv",
            "parent_section_summary.csv",
            "section_block_weights.csv",
            "greedy_block_trace.csv",
            "exceptional_section_audit.json",
            "section_operator_data.npz",
        ],
    }
    with (out_dir / "summary.json").open("w") as handle:
        json.dump(json_safe(summary), handle, indent=2, sort_keys=True)

    print("\n" + "=" * 108)
    print("FINAL SUMMARY")
    print("=" * 108)
    print(f"Exact local-sector section:           {section_residual <= args.containment_tolerance}")
    print(f"Residue image rank:                   {a_rank}")
    print(f"Source kernel dimension:              {local_kernel_dim}")
    print(f"Direct-child sections:                {summary['direct_child_section_count']}/{len(nonzero_parent_keys)}")
    print(f"Incident-child sections:              {summary['incident_child_section_count']}/{len(nonzero_parent_keys)}")
    print(f"Single-child section parents:         {summary['single_child_section_parent_count']}/{len(nonzero_parent_keys)}")
    print(f"Greedy global child-block cover:      {len(global_greedy_keys) if args.run_greedy else 'not run'}")
    if exceptional.get("performed"):
        print(f"Exceptional is local MP lift:         {exceptional['original_is_local_moore_penrose_lift']}")
    print(f"elapsed:                              {(time.time()-started)/60:.2f} minutes")
    print(f"summary:                              {out_dir / 'summary.json'}")
    print("=" * 108)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Construct explicit nontrivial 7->8 amplitude-relation growth sections.")
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--helper-script", required=True, help="Reflection-aware EHF-AMP-FOUND-02A v0.3 script.")
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
    parser.add_argument("--greedy-max-blocks", type=int, default=35)
    parser.add_argument("--run-greedy", action="store_true", help="Run optional block-sparse greedy searches (slower).")
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
