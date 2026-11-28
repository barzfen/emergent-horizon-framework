#!/usr/bin/env python3
"""
EHF-AMP-FOUND-01B: True All-Anchor Residue Closure
==================================================

Purpose
-------
Test the genuine atlas-gluing question left open by AMP-18/20:

    Rebuild the n=9 parity-position fibre partition separately for every
    reference anchor a=1,...,9; recompute the local Parke-Taylor relation
    spaces in each anchor-relative chart; take the collinear residues in the
    channel of that same anchor; transport all residues into one common n=8
    canonical-ordering space; and test, with rank-aware linear algebra,
    whether the exceptional fifteenth n=8 fibre relation is recovered.

This differs critically from the archived AMP-20 calculation. AMP-20 changed
which leg defined the collinear channel but retained the anchor-1 source fibre
partition. This probe changes BOTH:

    anchor-relative source chart + matching anchor-relative residue channel.

The probe also avoids the old wide-QR failure. Every span is built by SVD-based
incremental orthogonalisation, and closure is measured by true subspace
projection residuals and principal-angle intersection dimensions.

Requirements
------------
- Python 3
- NumPy
- ehf_amp_found_01_reproduce_amp18_20.py in the same scripts directory
  (or supply --base-script)

Recommended first run
---------------------

    caffeinate -i python3 scripts/ehf_amp_found_01b_true_all_anchor_residue_closure.py \
      --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
      --base-run-dir runs/ehf_amp_found_01_amp18_20 \
      --out-dir runs/ehf_amp_found_01b_true_all_anchor_seed11 \
      --seed 11

Independent repeat
------------------

    caffeinate -i python3 scripts/ehf_amp_found_01b_true_all_anchor_residue_closure.py \
      --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
      --base-run-dir runs/ehf_amp_found_01_amp18_20_seed29 \
      --out-dir runs/ehf_amp_found_01b_true_all_anchor_seed29 \
      --seed 29

Notes
-----
- No L2/L3 move rule enters this computation.
- The mathematical layer is the Hamilton-cycle / colour-ordering basis,
  anchor-relative parity-position fibres, Parke-Taylor relations, and
  collinear deletion residues.
- Relation-basis caches make interrupted runs resumable.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Mapping, MutableMapping, Optional, Sequence, Tuple

import numpy as np

Cycle = Tuple[int, ...]
FibreKey = Tuple[Tuple[int, ...], Tuple[int, ...]]


# -----------------------------------------------------------------------------
# Dynamic import of the audited AMP-18 rebuild
# -----------------------------------------------------------------------------


def load_base_module(path: Path):
    path = path.resolve()
    if not path.exists():
        raise FileNotFoundError(f"Base script not found: {path}")
    spec = importlib.util.spec_from_file_location("ehf_amp_found_01_base", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module specification from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


# -----------------------------------------------------------------------------
# Anchor-relative charts
# -----------------------------------------------------------------------------


def anchor_representative(cycle: Sequence[int], anchor: int) -> Cycle:
    """Rotate an undirected cycle to `anchor` and reflection-reduce there."""
    c = tuple(cycle)
    p = c.index(anchor)
    rep = c[p:] + c[:p]
    rev = (rep[0],) + rep[:0:-1]
    return rep if rep <= rev else rev


def anchor_pi_key(cycle: Sequence[int], anchor: int) -> FibreKey:
    rep = anchor_representative(cycle, anchor)
    return tuple(sorted(rep[0::2])), tuple(sorted(rep[1::2]))


def anchor_fibres(
    n: int,
    anchor: int,
    all_cycles: Sequence[Cycle],
) -> Dict[FibreKey, List[Cycle]]:
    """
    Partition the same global canonical ordering coordinates by Pi_anchor.

    Members remain in the common anchor-1 canonical coordinate convention.
    Only the chart partition changes.
    """
    grouped: MutableMapping[FibreKey, List[Cycle]] = defaultdict(list)
    for cycle in all_cycles:
        grouped[anchor_pi_key(cycle, anchor)].append(cycle)
    return {
        key: sorted(values)
        for key, values in sorted(grouped.items(), key=lambda item: item[0])
    }


def key_text(key: FibreKey) -> str:
    return f"E={','.join(map(str, key[0]))}|O={','.join(map(str, key[1]))}"


def parse_int_list(text: str) -> List[int]:
    values: List[int] = []
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        value = int(part)
        if value not in values:
            values.append(value)
    return values


# -----------------------------------------------------------------------------
# Subspace diagnostics
# -----------------------------------------------------------------------------


def vector_residual(vector: np.ndarray, q: np.ndarray) -> float:
    denominator = float(np.linalg.norm(vector))
    if denominator == 0.0:
        return 0.0
    if q.shape[1] == 0:
        return 1.0
    residual = vector - q @ (q.T @ vector)
    return float(np.linalg.norm(residual) / denominator)


def subspace_intersection_diagnostics(
    target_basis_full: np.ndarray,
    q: np.ndarray,
    containment_tolerance: float,
) -> Dict[str, object]:
    """
    Principal-angle diagnostics for target relation subspace V and span Q.

    target_basis_full and q must have orthonormal columns. Singular values of
    V^T Q are cosines of principal angles. Values near 1 count exact/common
    directions. If all target directions are contained in Q, all dim(V)
    singular values are 1.
    """
    target_dim = target_basis_full.shape[1]
    if target_dim == 0:
        return {
            "target_dim": 0,
            "intersection_dim": 0,
            "principal_cosines": [],
            "worst_containment_residual": 0.0,
        }
    if q.shape[1] == 0:
        cosines = np.zeros(target_dim, dtype=np.float64)
    else:
        cosines = np.linalg.svd(target_basis_full.T @ q, compute_uv=False)
        if cosines.size < target_dim:
            cosines = np.pad(cosines, (0, target_dim - cosines.size))
        cosines = np.clip(cosines[:target_dim], 0.0, 1.0)
    intersection_dim = int(np.count_nonzero((1.0 - cosines) <= containment_tolerance))
    smallest_cosine = float(cosines[-1]) if cosines.size else 0.0
    worst_residual = float(math.sqrt(max(0.0, 1.0 - smallest_cosine**2)))
    return {
        "target_dim": target_dim,
        "intersection_dim": intersection_dim,
        "principal_cosines": cosines.tolist(),
        "worst_containment_residual": worst_residual,
    }


def validate_span_as_relations(
    pt_matrix: np.ndarray,
    q: np.ndarray,
) -> float:
    if q.shape[1] == 0:
        return 0.0
    residuals = pt_matrix @ q
    # q has orthonormal real columns, so each denominator is 1.
    return float(np.max(np.linalg.norm(residuals, axis=0)))


def spectrum_signature(
    fibre_map: Mapping[FibreKey, Sequence[Cycle]],
    basis_map: Mapping[FibreKey, object],
) -> Tuple[Tuple[int, int], ...]:
    return tuple(
        sorted(
            (len(fibre_map[key]), int(basis_map[key].relation_dim))
            for key in fibre_map
        )
    )


def signature_digest(signature: Tuple[Tuple[int, int], ...]) -> str:
    payload = json.dumps(signature, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


# -----------------------------------------------------------------------------
# Incremental rank-aware residue span
# -----------------------------------------------------------------------------


def process_anchor_residue_span(
    *,
    base,
    anchor: int,
    n: int,
    source_fibres: Mapping[FibreKey, Sequence[Cycle]],
    source_bases: Mapping[FibreKey, object],
    target_cycles: Sequence[Cycle],
    initial_cumulative_q: np.ndarray,
    missing_vector: np.ndarray,
    target_basis_full: np.ndarray,
    target_pt_validation: np.ndarray,
    args: argparse.Namespace,
) -> Tuple[np.ndarray, np.ndarray, Dict[str, object]]:
    """Build anchor-alone and cumulative spans from true anchor-relative data."""
    anchor_q = np.zeros((len(target_cycles), 0), dtype=np.float64)
    cumulative_q = initial_cumulative_q.copy()
    cumulative_rank_before = cumulative_q.shape[1]

    pending: List[np.ndarray] = []
    pending_columns = 0
    blocks_seen = 0
    vectors_seen = 0
    anchor_independent_added = 0
    cumulative_independent_added = 0
    started = time.time()

    def flush() -> None:
        nonlocal anchor_q, cumulative_q, pending, pending_columns
        nonlocal anchor_independent_added, cumulative_independent_added
        if not pending:
            return
        block = np.hstack(pending)
        anchor_before = anchor_q.shape[1]
        cumulative_before = cumulative_q.shape[1]
        anchor_q, anchor_added = base.append_orthonormal_span(
            anchor_q,
            block,
            relative_tolerance=args.span_tolerance,
            absolute_tolerance=args.span_absolute_tolerance,
        )
        cumulative_q, cumulative_added = base.append_orthonormal_span(
            cumulative_q,
            block,
            relative_tolerance=args.span_tolerance,
            absolute_tolerance=args.span_absolute_tolerance,
        )
        anchor_independent_added += anchor_added
        cumulative_independent_added += cumulative_added
        pending = []
        pending_columns = 0
        print(
            f"    flush: anchor rank {anchor_before}->{anchor_q.shape[1]} "
            f"(+{anchor_added}); cumulative {cumulative_before}->{cumulative_q.shape[1]} "
            f"(+{cumulative_added}); missing residual="
            f"{vector_residual(missing_vector, cumulative_q):.3e}"
        )

    for source_key, deleted_label, block in base.full_anchor_residue_blocks(
        anchor=anchor,
        n=n,
        source_fibres=source_fibres,
        source_bases=source_bases,
        target_all_cycles=target_cycles,
    ):
        del source_key, deleted_label
        blocks_seen += 1
        vectors_seen += block.shape[1]
        pending.append(block)
        pending_columns += block.shape[1]
        if pending_columns >= args.orthogonalization_block_columns:
            flush()

    flush()

    # Re-orthogonalise each completed span to control cumulative roundoff.
    if anchor_q.shape[1]:
        anchor_q, _ = np.linalg.qr(anchor_q, mode="reduced")
    if cumulative_q.shape[1]:
        cumulative_q, _ = np.linalg.qr(cumulative_q, mode="reduced")

    anchor_missing_residual = vector_residual(missing_vector, anchor_q)
    cumulative_missing_residual = vector_residual(missing_vector, cumulative_q)
    anchor_intersection = subspace_intersection_diagnostics(
        target_basis_full,
        anchor_q,
        args.subspace_containment_tolerance,
    )
    cumulative_intersection = subspace_intersection_diagnostics(
        target_basis_full,
        cumulative_q,
        args.subspace_containment_tolerance,
    )
    anchor_relation_validation = validate_span_as_relations(target_pt_validation, anchor_q)
    cumulative_relation_validation = validate_span_as_relations(
        target_pt_validation,
        cumulative_q,
    )

    metadata = {
        "anchor": anchor,
        "blocks_seen": blocks_seen,
        "vectors_seen": vectors_seen,
        "anchor_span_rank": anchor_q.shape[1],
        "anchor_independent_directions_added": anchor_independent_added,
        "anchor_missing_residual": anchor_missing_residual,
        "anchor_exceptional_intersection_dim": anchor_intersection["intersection_dim"],
        "anchor_exceptional_worst_containment_residual": anchor_intersection[
            "worst_containment_residual"
        ],
        "anchor_relation_validation_max_residual": anchor_relation_validation,
        "cumulative_rank_before": cumulative_rank_before,
        "cumulative_span_rank": cumulative_q.shape[1],
        "cumulative_independent_directions_added": cumulative_independent_added,
        "cumulative_missing_residual": cumulative_missing_residual,
        "cumulative_exceptional_intersection_dim": cumulative_intersection[
            "intersection_dim"
        ],
        "cumulative_exceptional_worst_containment_residual": cumulative_intersection[
            "worst_containment_residual"
        ],
        "cumulative_relation_validation_max_residual": cumulative_relation_validation,
        "elapsed_seconds": time.time() - started,
    }
    return anchor_q, cumulative_q, metadata


# -----------------------------------------------------------------------------
# Missing-direction construction from the reproduced AMP-18 baseline
# -----------------------------------------------------------------------------


def find_exceptional_key(
    target_fibres: Mapping[FibreKey, Sequence[Cycle]],
    exceptional_set: Tuple[int, ...],
) -> FibreKey:
    for key in target_fibres:
        containing_anchor = key[0] if 1 in key[0] else key[1]
        if tuple(containing_anchor) == exceptional_set:
            return key
    raise RuntimeError(f"Exceptional target set not found: {exceptional_set}")


def extract_missing_direction(
    *,
    base,
    target_fibres: Mapping[FibreKey, Sequence[Cycle]],
    target_bases: Mapping[FibreKey, object],
    anchor1_arrivals: Mapping[FibreKey, np.ndarray],
    exceptional_key: FibreKey,
    target_all_cycles: Sequence[Cycle],
    span_tolerance: float,
) -> Tuple[np.ndarray, np.ndarray, Dict[str, object]]:
    chamber = target_fibres[exceptional_key]
    target_basis_local = target_bases[exceptional_key].basis
    relation_dim = int(target_bases[exceptional_key].relation_dim)
    anchor1_local = anchor1_arrivals[exceptional_key]

    local_rank, local_singular_values = base.matrix_rank_relative(
        anchor1_local,
        span_tolerance,
    )
    coordinates = target_basis_local.T @ anchor1_local
    u, coordinate_singular_values, _ = np.linalg.svd(coordinates, full_matrices=True)
    if coordinate_singular_values.size == 0 or coordinate_singular_values[0] == 0:
        coordinate_rank = 0
    else:
        coordinate_rank = int(
            np.count_nonzero(
                coordinate_singular_values
                > coordinate_singular_values[0] * span_tolerance
            )
        )
    missing_dim = relation_dim - coordinate_rank
    if missing_dim != 1:
        raise RuntimeError(
            f"Expected one exceptional missing direction; found {missing_dim}."
        )

    missing_coordinate = u[:, coordinate_rank : coordinate_rank + 1]
    missing_local = target_basis_local @ missing_coordinate

    target_index = {cycle: i for i, cycle in enumerate(target_all_cycles)}
    missing_full = np.zeros((len(target_all_cycles), 1), dtype=np.float64)
    target_basis_full = np.zeros(
        (len(target_all_cycles), relation_dim),
        dtype=np.float64,
    )
    for local_i, cycle in enumerate(chamber):
        global_i = target_index[cycle]
        missing_full[global_i, 0] = missing_local[local_i, 0]
        target_basis_full[global_i, :] = target_basis_local[local_i, :]

    metadata = {
        "exceptional_target_key": key_text(exceptional_key),
        "exceptional_target_size": len(chamber),
        "target_relation_dim": relation_dim,
        "anchor1_local_image_vectors": anchor1_local.shape[1],
        "anchor1_local_rank": local_rank,
        "coordinate_rank": coordinate_rank,
        "missing_dimension": missing_dim,
        "anchor1_local_singular_values": local_singular_values.tolist(),
        "coordinate_singular_values": coordinate_singular_values.tolist(),
    }
    return missing_full, target_basis_full, metadata


# -----------------------------------------------------------------------------
# Main experiment
# -----------------------------------------------------------------------------


def run(args: argparse.Namespace) -> Dict[str, object]:
    base = load_base_module(Path(args.base_script))
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_root = out_dir / "cache"
    cache_root.mkdir(parents=True, exist_ok=True)
    base_run_dir = Path(args.base_run_dir).resolve()

    n = 9
    target_n = 8
    anchors = parse_int_list(args.anchors)
    if not anchors:
        raise ValueError("At least one anchor is required.")
    if any(anchor < 1 or anchor > n for anchor in anchors):
        raise ValueError(f"Anchors must lie in 1..{n}: {anchors}")

    print("=" * 100)
    print("EHF-AMP-FOUND-01B: TRUE ALL-ANCHOR RESIDUE CLOSURE")
    print("=" * 100)
    print(f"source multiplicity:              n={n}")
    print(f"target multiplicity:              n={target_n}")
    print(f"anchors in cumulative order:      {anchors}")
    print(f"seed:                             {args.seed}")
    print(f"base script:                      {Path(args.base_script).resolve()}")
    print(f"base run/cache directory:         {base_run_dir}")
    print(f"output directory:                 {out_dir}")
    print(f"SVD tolerance:                    {args.svd_tolerance}")
    print(f"span relative tolerance:          {args.span_tolerance}")
    print(f"span absolute tolerance:          {args.span_absolute_tolerance}")
    print(f"closure verdict tolerance:        {args.closure_verdict_tolerance}")
    print(f"subspace containment tolerance:   {args.subspace_containment_tolerance}")
    print()

    started = time.time()
    source_cycles = base.canonical_cycles(n)
    target_cycles = base.canonical_cycles(target_n)
    source_anchor1_fibres = anchor_fibres(n, 1, source_cycles)
    target_anchor1_fibres = anchor_fibres(target_n, 1, target_cycles)

    # Confirm our true-anchor implementation reproduces the audited anchor-1 maps.
    if source_anchor1_fibres != base.fibres(n):
        raise RuntimeError("anchor_fibres(n,1) does not reproduce the base source partition.")
    if target_anchor1_fibres != base.fibres(target_n):
        raise RuntimeError("anchor_fibres(n-1,1) does not reproduce the base target partition.")

    print(
        f"Ordering counts: source={len(source_cycles)}, target={len(target_cycles)}; "
        f"anchor-1 fibres source={len(source_anchor1_fibres)}, "
        f"target={len(target_anchor1_fibres)}"
    )

    # Reuse the previously audited anchor-1 caches when available.
    base_cache = base_run_dir / "cache"
    target_cache = base_cache if base_cache.exists() else cache_root / "anchor_1"
    anchor1_cache = base_cache if base_cache.exists() else cache_root / "anchor_1"

    target_bases, target_basis_rows = base.build_all_bases(
        n=target_n,
        fibre_map=target_anchor1_fibres,
        cache_dir=target_cache,
        args=args,
        seed_offset=7,
    )
    for row in target_basis_rows:
        row["anchor"] = 1
        row["layer"] = "target_anchor1"

    anchor1_bases, anchor1_basis_rows = base.build_all_bases(
        n=n,
        fibre_map=source_anchor1_fibres,
        cache_dir=anchor1_cache,
        args=args,
        seed_offset=1,
    )
    for row in anchor1_basis_rows:
        row["anchor"] = 1
        row["layer"] = "source"

    # Reproduce AMP-18 locally and extract the one missing direction.
    amp18_rows, anchor1_arrivals = base.run_amp18(
        n=n,
        source_fibres=source_anchor1_fibres,
        target_fibres=target_anchor1_fibres,
        source_bases=anchor1_bases,
        target_bases=target_bases,
        args=args,
    )
    exceptional_set = tuple(sorted(parse_int_list(args.exceptional_set)))
    exceptional_key = find_exceptional_key(target_anchor1_fibres, exceptional_set)
    missing_full, exceptional_basis_full, missing_meta = extract_missing_direction(
        base=base,
        target_fibres=target_anchor1_fibres,
        target_bases=target_bases,
        anchor1_arrivals=anchor1_arrivals,
        exceptional_key=exceptional_key,
        target_all_cycles=target_cycles,
        span_tolerance=args.span_tolerance,
    )

    print("\nExceptional target and missing direction")
    print(f"  target:                    {missing_meta['exceptional_target_key']}")
    print(f"  target relation dim:       {missing_meta['target_relation_dim']}")
    print(f"  anchor-1 local rank:       {missing_meta['anchor1_local_rank']}/15")
    print(f"  missing dimension:         {missing_meta['missing_dimension']}")

    # Fresh target PT matrix used to verify every completed residue span remains
    # in the global n=8 relation space.
    target_pt_validation = base.parke_taylor_matrix(
        target_cycles,
        target_n,
        args.seed + 880_000,
        args.residue_validation_rows,
    )

    baseline_signature = spectrum_signature(source_anchor1_fibres, anchor1_bases)
    baseline_digest = signature_digest(baseline_signature)
    expected_local_relation_total = sum(
        int(anchor1_bases[key].relation_dim) for key in source_anchor1_fibres
    )
    expected_global_target_relation_dim = len(target_cycles) - math.factorial(target_n - 2)

    print("\nBaseline invariants")
    print(f"  n=9 fibre spectrum digest:       {baseline_digest}")
    print(f"  n=9 local relation total:        {expected_local_relation_total}")
    print(f"  expected global n=8 relation dim:{expected_global_target_relation_dim}")

    cumulative_q = np.zeros((len(target_cycles), 0), dtype=np.float64)
    anchor_rows: List[Dict[str, object]] = []
    all_basis_rows: List[Dict[str, object]] = list(target_basis_rows) + list(anchor1_basis_rows)
    anchor_metadata: List[Dict[str, object]] = []

    for anchor in anchors:
        print("\n" + "-" * 100)
        print(f"TRUE ANCHOR {anchor}: rebuild Pi_{anchor} chart and use anchor-{anchor} residues")
        print("-" * 100)

        if anchor == 1:
            source_fibre_map = source_anchor1_fibres
            source_bases = anchor1_bases
            basis_rows: List[Dict[str, object]] = []
        else:
            source_fibre_map = anchor_fibres(n, anchor, source_cycles)
            anchor_cache = cache_root / f"anchor_{anchor}"
            source_bases, basis_rows = base.build_all_bases(
                n=n,
                fibre_map=source_fibre_map,
                cache_dir=anchor_cache,
                args=args,
                seed_offset=1000 * anchor + 1,
            )
            for row in basis_rows:
                row["anchor"] = anchor
                row["layer"] = "source"
            all_basis_rows.extend(basis_rows)

        signature = spectrum_signature(source_fibre_map, source_bases)
        digest = signature_digest(signature)
        spectrum_match = signature == baseline_signature
        local_relation_total = sum(
            int(source_bases[key].relation_dim) for key in source_fibre_map
        )
        print(f"  source fibres:             {len(source_fibre_map)}")
        print(f"  local relation total:      {local_relation_total}")
        print(f"  spectrum digest:           {digest}")
        print(f"  matches anchor 1 spectrum: {spectrum_match}")
        if not spectrum_match:
            raise RuntimeError(f"Anchor {anchor} relation spectrum differs from anchor 1.")

        anchor_q, cumulative_q, meta = process_anchor_residue_span(
            base=base,
            anchor=anchor,
            n=n,
            source_fibres=source_fibre_map,
            source_bases=source_bases,
            target_cycles=target_cycles,
            initial_cumulative_q=cumulative_q,
            missing_vector=missing_full,
            target_basis_full=exceptional_basis_full,
            target_pt_validation=target_pt_validation,
            args=args,
        )
        meta.update(
            {
                "source_fibre_count": len(source_fibre_map),
                "local_relation_total": local_relation_total,
                "spectrum_digest": digest,
                "spectrum_match_anchor1": spectrum_match,
            }
        )
        anchor_metadata.append(meta)

        if cumulative_q.shape[1] > expected_global_target_relation_dim:
            raise RuntimeError(
                "Cumulative residue rank exceeds the expected global n=8 relation "
                f"dimension: {cumulative_q.shape[1]} > {expected_global_target_relation_dim}."
            )
        if (
            meta["anchor_relation_validation_max_residual"]
            > args.relation_validation_tolerance
        ):
            raise RuntimeError(
                f"Anchor {anchor} residue span failed the fresh Parke-Taylor "
                "relation check: "
                f"{meta['anchor_relation_validation_max_residual']:.3e} > "
                f"{args.relation_validation_tolerance:.3e}."
            )
        if (
            meta["cumulative_relation_validation_max_residual"]
            > args.relation_validation_tolerance
        ):
            raise RuntimeError(
                f"Cumulative residue span through anchor {anchor} failed the fresh "
                "Parke-Taylor relation check: "
                f"{meta['cumulative_relation_validation_max_residual']:.3e} > "
                f"{args.relation_validation_tolerance:.3e}."
            )

        closed = meta["cumulative_missing_residual"] < args.closure_verdict_tolerance
        row = {
            "anchor": anchor,
            "source_fibre_count": len(source_fibre_map),
            "local_relation_total": local_relation_total,
            "spectrum_digest": digest,
            "spectrum_match_anchor1": spectrum_match,
            "blocks_seen": meta["blocks_seen"],
            "vectors_seen": meta["vectors_seen"],
            "anchor_span_rank": meta["anchor_span_rank"],
            "anchor_missing_residual": f"{meta['anchor_missing_residual']:.17g}",
            "anchor_exceptional_intersection_dim": meta[
                "anchor_exceptional_intersection_dim"
            ],
            "anchor_relation_validation_max_residual": f"{meta['anchor_relation_validation_max_residual']:.17g}",
            "cumulative_rank_before": meta["cumulative_rank_before"],
            "cumulative_independent_directions_added": meta[
                "cumulative_independent_directions_added"
            ],
            "cumulative_span_rank": meta["cumulative_span_rank"],
            "cumulative_rank_fraction_of_global_relation_dim": f"{meta['cumulative_span_rank'] / expected_global_target_relation_dim:.17g}",
            "cumulative_missing_residual": f"{meta['cumulative_missing_residual']:.17g}",
            "cumulative_exceptional_intersection_dim": meta[
                "cumulative_exceptional_intersection_dim"
            ],
            "cumulative_exceptional_worst_containment_residual": f"{meta['cumulative_exceptional_worst_containment_residual']:.17g}",
            "cumulative_relation_validation_max_residual": f"{meta['cumulative_relation_validation_max_residual']:.17g}",
            "gap_closed": closed,
            "elapsed_seconds": f"{meta['elapsed_seconds']:.6f}",
        }
        anchor_rows.append(row)

        print("\n  Anchor summary")
        print(f"    anchor-alone span rank:       {meta['anchor_span_rank']}")
        print(f"    anchor-alone missing residual:{meta['anchor_missing_residual']:.3e}")
        print(
            f"    anchor-alone target overlap:  "
            f"{meta['anchor_exceptional_intersection_dim']}/15"
        )
        print(f"    cumulative span rank:         {meta['cumulative_span_rank']}")
        print(
            f"    cumulative missing residual:  "
            f"{meta['cumulative_missing_residual']:.3e}"
        )
        print(
            f"    cumulative target overlap:    "
            f"{meta['cumulative_exceptional_intersection_dim']}/15"
        )
        print(
            f"    cumulative PT residual:       "
            f"{meta['cumulative_relation_validation_max_residual']:.3e}"
        )
        print(f"    gap closed:                    {closed}")

        if args.save_span_bases:
            np.savez_compressed(
                out_dir / f"anchor_{anchor}_span_basis_seed{args.seed}.npz",
                q=anchor_q,
            )
            np.savez_compressed(
                out_dir / f"cumulative_through_anchor_{anchor}_basis_seed{args.seed}.npz",
                q=cumulative_q,
            )

        if closed and args.stop_on_closure:
            print(f"\nClosure reached after anchor {anchor}; stopping by request.")
            break

    final_meta = anchor_metadata[-1] if anchor_metadata else None
    final_residual = (
        float(final_meta["cumulative_missing_residual"])
        if final_meta is not None
        else 1.0
    )
    final_intersection = (
        int(final_meta["cumulative_exceptional_intersection_dim"])
        if final_meta is not None
        else 0
    )
    final_rank = cumulative_q.shape[1]
    gap_closed = final_residual < args.closure_verdict_tolerance
    full_exceptional_containment = final_intersection == int(missing_meta["target_relation_dim"])

    # Write machine-readable outputs.
    base.write_csv(
        out_dir / "all_anchor_cumulative_summary.csv",
        anchor_rows,
        fieldnames=list(anchor_rows[0].keys()) if anchor_rows else [],
    )
    if all_basis_rows:
        # Union of keys, preserving first appearance.
        fields: List[str] = []
        for row in all_basis_rows:
            for key in row:
                if key not in fields:
                    fields.append(key)
        base.write_csv(
            out_dir / "all_anchor_relation_basis_summary.csv",
            all_basis_rows,
            fieldnames=fields,
        )
    base.write_csv(
        out_dir / "amp18_baseline_target_summary.csv",
        amp18_rows,
        fieldnames=list(amp18_rows[0].keys()),
    )
    np.savez_compressed(
        out_dir / "exceptional_missing_direction_seed%d.npz" % args.seed,
        missing_full=missing_full,
        exceptional_relation_basis_full=exceptional_basis_full,
    )
    if args.save_final_span:
        np.savez_compressed(
            out_dir / "true_all_anchor_final_span_seed%d.npz" % args.seed,
            q=cumulative_q,
        )

    summary = {
        "probe": "EHF-AMP-FOUND-01B",
        "title": "True All-Anchor Residue Closure",
        "script": Path(__file__).name,
        "seed": args.seed,
        "source_n": n,
        "target_n": target_n,
        "anchors_requested": anchors,
        "anchors_completed": [row["anchor"] for row in anchor_rows],
        "source_state_count": len(source_cycles),
        "target_state_count": len(target_cycles),
        "source_fibre_count_per_anchor": len(source_anchor1_fibres),
        "target_anchor1_fibre_count": len(target_anchor1_fibres),
        "baseline_source_spectrum_digest": baseline_digest,
        "baseline_local_relation_total": expected_local_relation_total,
        "expected_global_target_relation_dim": expected_global_target_relation_dim,
        "missing_direction": missing_meta,
        "anchor_results": anchor_metadata,
        "final_cumulative_span_rank": final_rank,
        "final_rank_fraction_of_global_relation_dim": final_rank
        / expected_global_target_relation_dim,
        "final_missing_direction_residual": final_residual,
        "final_exceptional_intersection_dim": final_intersection,
        "final_exceptional_relation_dim": int(missing_meta["target_relation_dim"]),
        "gap_closed": gap_closed,
        "full_exceptional_relation_space_contained": full_exceptional_containment,
        "closure_verdict_tolerance": args.closure_verdict_tolerance,
        "parameters": vars(args),
        "elapsed_seconds": time.time() - started,
    }
    with (out_dir / "summary.json").open("w") as handle:
        json.dump(base.json_safe(summary), handle, indent=2, sort_keys=True)

    print("\n" + "=" * 100)
    print("FINAL TRUE ALL-ANCHOR VERDICT")
    print("=" * 100)
    print(f"anchors completed:                       {summary['anchors_completed']}")
    print(
        f"final residue span rank:                 {final_rank}/"
        f"{expected_global_target_relation_dim} global relation dimensions"
    )
    print(f"final missing-direction residual:        {final_residual:.6e}")
    print(
        f"exceptional relation-space intersection:{final_intersection}/"
        f"{missing_meta['target_relation_dim']}"
    )
    print(f"gap closed:                              {gap_closed}")
    print(
        f"full exceptional space contained:        "
        f"{full_exceptional_containment}"
    )
    print(f"elapsed:                                 {(time.time() - started)/60:.2f} minutes")
    print(f"summary:                                 {out_dir / 'summary.json'}")
    print("=" * 100)
    return summary


# -----------------------------------------------------------------------------
# CLI and logging
# -----------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="EHF-AMP-FOUND-01B: true all-anchor residue closure audit."
    )
    parser.add_argument(
        "--base-script",
        default="scripts/ehf_amp_found_01_reproduce_amp18_20.py",
        help="Path to the audited AMP-18/20 reproducibility module.",
    )
    parser.add_argument(
        "--base-run-dir",
        default="runs/ehf_amp_found_01_amp18_20",
        help="Existing AMP-18 run directory whose anchor-1 caches may be reused.",
    )
    parser.add_argument(
        "--out-dir",
        default="runs/ehf_amp_found_01b_true_all_anchor",
        help="Output and anchor-specific cache directory.",
    )
    parser.add_argument(
        "--anchors",
        default="1,2,3,4,5,6,7,8,9",
        help="Comma-separated anchors in cumulative gluing order.",
    )
    parser.add_argument("--seed", type=int, default=11)
    parser.add_argument("--rows-multiplier", type=float, default=3.0)
    parser.add_argument("--min-rows", type=int, default=400)
    parser.add_argument("--validation-rows", type=int, default=160)
    parser.add_argument("--residue-validation-rows", type=int, default=64)
    parser.add_argument("--svd-tolerance", type=float, default=1e-9)
    parser.add_argument("--span-tolerance", type=float, default=1e-9)
    parser.add_argument("--span-absolute-tolerance", type=float, default=1e-11)
    parser.add_argument("--orthogonalization-block-columns", type=int, default=256)
    parser.add_argument("--closure-stop-tolerance", type=float, default=1e-10)
    parser.add_argument("--closure-verdict-tolerance", type=float, default=1e-6)
    parser.add_argument("--subspace-containment-tolerance", type=float, default=1e-7)
    parser.add_argument(
        "--relation-validation-tolerance",
        type=float,
        default=1e-7,
        help="Abort if a residue span fails a fresh global Parke-Taylor relation check.",
    )
    parser.add_argument(
        "--exceptional-set",
        default="1,4,5,6",
        help="Anchor-1-containing set of the exceptional n=8 target fibre.",
    )
    parser.add_argument(
        "--force-rebuild",
        action="store_true",
        help="Ignore all anchor relation-basis caches.",
    )
    parser.add_argument(
        "--stop-on-closure",
        action="store_true",
        help="Stop after the first cumulative anchor set that closes the gap.",
    )
    parser.add_argument(
        "--save-span-bases",
        action="store_true",
        help="Save each anchor-alone and cumulative orthonormal span basis.",
    )
    parser.add_argument(
        "--save-final-span",
        action="store_true",
        help="Save the final cumulative all-anchor span basis.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    log_path = out_dir / "run.log"

    with log_path.open("a", buffering=1) as log_handle:
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        # Reuse the base module's Tee only after loading would complicate startup;
        # this tiny local implementation is sufficient.
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

        sys.stdout = Tee(original_stdout, log_handle)
        sys.stderr = Tee(original_stderr, log_handle)
        try:
            print(f"\n\n===== RUN START {time.strftime('%Y-%m-%d %H:%M:%S')} =====")
            run(args)
            print(f"===== RUN END {time.strftime('%Y-%m-%d %H:%M:%S')} =====")
            return 0
        except KeyboardInterrupt:
            print("\nInterrupted. Completed relation-basis caches can be reused on restart.")
            return 130
        except Exception as exc:
            print(f"\nERROR: {type(exc).__name__}: {exc}")
            import traceback

            traceback.print_exc()
            return 1
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr


if __name__ == "__main__":
    raise SystemExit(main())
