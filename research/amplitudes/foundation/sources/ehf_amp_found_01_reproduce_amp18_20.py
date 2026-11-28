#!/usr/bin/env python3
"""
EHF-AMP-FOUND-01 reproducibility rebuild for AMP-18F and AMP-20.

Purpose
-------
Recompute the heavy Parke-Taylor relation-rank layer behind:

1. AMP-18F: n=9 -> n=8 anchor-1 collinear residues generate the full
   15-dimensional local relation space in 34 of 35 target fibres, with one
   exceptional target at rank 14.
2. AMP-20: adding anchor-2 collinear residues closes the exceptional missing
   direction in the common ambient n=8 ordering space.

The script is self-contained. It uses only Python's standard library and NumPy.
It writes checkpointed relation bases, CSV summaries, JSON metadata, and a log.
A full n=9 run is intentionally heavy; resume is supported through cached .npz
basis files.

Examples
--------
Smoke test (small n=7 -> 6):

    python3 ehf_amp_found_01_reproduce_amp18_20.py \
      --stage smoke \
      --out-dir runs/ehf_amp_found_01_smoke

Full reproduction:

    python3 ehf_amp_found_01_reproduce_amp18_20.py \
      --stage all \
      --out-dir runs/ehf_amp_found_01_amp18_20

Re-run using caches after interruption:

    python3 ehf_amp_found_01_reproduce_amp18_20.py \
      --stage all \
      --out-dir runs/ehf_amp_found_01_amp18_20

Notes
-----
- The relation-basis routine intentionally follows the numerical procedure in
  the archived AMP-18/20 scripts: random complex spinors, real/imaginary row
  stacking, iterative equilibration, and an SVD nullspace threshold.
- Fresh independent kinematics are used to validate every cached basis.
- No L2/L3 move rule enters this computation. It uses only canonical ordering
  space, parity-position fibres, Parke-Taylor functions, and collinear deletion.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from itertools import permutations
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Mapping, MutableMapping, Optional, Sequence, Tuple

import numpy as np

Cycle = Tuple[int, ...]
FibreKey = Tuple[Tuple[int, ...], Tuple[int, ...]]


# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------


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


# -----------------------------------------------------------------------------
# Canonical ordering and fibre definitions
# -----------------------------------------------------------------------------


def canon(c: Iterable[int]) -> Cycle:
    c = tuple(c)
    p = c.index(1)
    rep = c[p:] + c[:p]
    rev = (rep[0],) + rep[:0:-1]
    return rep if rep <= rev else rev


def pi_key(c: Sequence[int]) -> FibreKey:
    """Ordered parity-position fibre key, made deterministic for serialization."""
    even = tuple(sorted(c[0::2]))
    odd = tuple(sorted(c[1::2]))
    return even, odd


def key_text(key: FibreKey) -> str:
    return f"E={','.join(map(str, key[0]))}|O={','.join(map(str, key[1]))}"


def canonical_cycles(n: int) -> List[Cycle]:
    """Canonical Hamilton cycles with label 1 anchored and reflection removed."""
    return [(1,) + p for p in permutations(range(2, n + 1)) if p[0] < p[-1]]


def fibres(n: int) -> Dict[FibreKey, List[Cycle]]:
    grouped: MutableMapping[FibreKey, List[Cycle]] = defaultdict(list)
    for c in canonical_cycles(n):
        grouped[pi_key(c)].append(c)
    return {k: sorted(v) for k, v in sorted(grouped.items(), key=lambda kv: kv[0])}


def relabel_after_deletion(seq: Sequence[int], missing: int, n: int) -> Cycle:
    mapping: Dict[int, int] = {}
    x = 1
    for value in range(1, n + 1):
        if value == missing:
            continue
        mapping[value] = x
        x += 1
    return tuple(mapping[v] for v in seq)


# -----------------------------------------------------------------------------
# Parke-Taylor numerical linear algebra
# -----------------------------------------------------------------------------


@dataclass
class RelationBasis:
    basis: np.ndarray  # shape (fibre_size, relation_dim), real orthonormal columns
    relation_dim: int
    numerical_rank: int
    singular_values: np.ndarray
    validation_max_relative_residual: float
    training_rows: int
    from_cache: bool


def parke_taylor_matrix(
    chamber: Sequence[Cycle],
    n: int,
    seed: int,
    rows: int,
) -> np.ndarray:
    """Random-kinematics Parke-Taylor evaluation matrix, shape rows x states."""
    size = len(chamber)
    arr = np.asarray(chamber, dtype=np.int64) - 1
    nxt = np.roll(arr, -1, axis=1)
    rng = np.random.default_rng(seed)
    matrix = np.empty((rows, size), dtype=np.complex128)

    for t in range(rows):
        lam = rng.normal(size=(n, 2)) + 1j * rng.normal(size=(n, 2))
        brackets = (
            lam[:, 0][:, None] * lam[:, 1][None, :]
            - lam[:, 1][:, None] * lam[:, 0][None, :]
        )
        denom = np.prod(brackets[arr, nxt], axis=1)
        matrix[t] = 1.0 / denom
    return matrix


def validate_basis(
    chamber: Sequence[Cycle],
    n: int,
    basis: np.ndarray,
    seed: int,
    rows: int,
) -> float:
    if basis.shape[1] == 0:
        return 0.0
    matrix = parke_taylor_matrix(chamber, n, seed, rows)
    residuals = matrix @ basis
    numerator = np.linalg.norm(residuals, axis=0)
    denominator = np.linalg.norm(basis, axis=0)
    denominator[denominator == 0] = 1.0
    return float(np.max(numerator / denominator))


def chamber_digest(chamber: Sequence[Cycle]) -> str:
    h = hashlib.sha256()
    for c in chamber:
        h.update(bytes(c))
    return h.hexdigest()[:16]


def relation_basis_cache_path(
    cache_dir: Path,
    n: int,
    fibre_index: int,
    chamber: Sequence[Cycle],
    seed: int,
) -> Path:
    digest = chamber_digest(chamber)
    return cache_dir / f"n{n}_f{fibre_index:03d}_s{len(chamber)}_seed{seed}_{digest}.npz"


def compute_relation_basis(
    chamber: Sequence[Cycle],
    n: int,
    train_seed: int,
    validation_seed: int,
    rows_multiplier: float,
    min_rows: int,
    validation_rows: int,
    svd_relative_tolerance: float,
) -> RelationBasis:
    size = len(chamber)
    training_rows = max(int(math.ceil(rows_multiplier * size)), min_rows)
    complex_matrix = parke_taylor_matrix(chamber, n, train_seed, training_rows)
    a = np.vstack([complex_matrix.real, complex_matrix.imag])
    column_scales = np.ones(size, dtype=np.float64)

    # Preserve the equilibration strategy used by the archived scripts.
    for _ in range(4):
        row_norms = np.linalg.norm(a, axis=1, keepdims=True)
        row_norms[row_norms == 0] = 1.0
        a /= row_norms

        col_norms = np.linalg.norm(a, axis=0)
        col_norms[col_norms == 0] = 1.0
        a /= col_norms[None, :]
        column_scales *= col_norms

    _, singular_values, vh = np.linalg.svd(a, full_matrices=True)
    if singular_values.size == 0 or singular_values[0] == 0:
        numerical_rank = 0
    else:
        numerical_rank = int(
            np.count_nonzero(singular_values > singular_values[0] * svd_relative_tolerance)
        )
    relation_dim = size - numerical_rank

    if relation_dim:
        basis = vh[numerical_rank:].T / column_scales[:, None]
        basis, _ = np.linalg.qr(basis, mode="reduced")
    else:
        basis = np.zeros((size, 0), dtype=np.float64)

    validation = validate_basis(
        chamber,
        n,
        basis,
        validation_seed,
        validation_rows,
    )
    return RelationBasis(
        basis=basis,
        relation_dim=relation_dim,
        numerical_rank=numerical_rank,
        singular_values=singular_values,
        validation_max_relative_residual=validation,
        training_rows=training_rows,
        from_cache=False,
    )


def load_or_compute_relation_basis(
    chamber: Sequence[Cycle],
    n: int,
    fibre_index: int,
    cache_dir: Path,
    train_seed: int,
    validation_seed: int,
    rows_multiplier: float,
    min_rows: int,
    validation_rows: int,
    svd_relative_tolerance: float,
    force_rebuild: bool,
) -> RelationBasis:
    cache_path = relation_basis_cache_path(cache_dir, n, fibre_index, chamber, train_seed)

    if cache_path.exists() and not force_rebuild:
        data = np.load(cache_path, allow_pickle=False)
        basis = data["basis"]
        singular_values = data["singular_values"]
        result = RelationBasis(
            basis=basis,
            relation_dim=int(data["relation_dim"]),
            numerical_rank=int(data["numerical_rank"]),
            singular_values=singular_values,
            validation_max_relative_residual=float(data["validation_residual"]),
            training_rows=int(data["training_rows"]),
            from_cache=True,
        )
        # Revalidate cached results at fresh kinematics. This is cheap relative to SVD.
        result.validation_max_relative_residual = validate_basis(
            chamber,
            n,
            result.basis,
            validation_seed,
            validation_rows,
        )
        return result

    result = compute_relation_basis(
        chamber=chamber,
        n=n,
        train_seed=train_seed,
        validation_seed=validation_seed,
        rows_multiplier=rows_multiplier,
        min_rows=min_rows,
        validation_rows=validation_rows,
        svd_relative_tolerance=svd_relative_tolerance,
    )
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        cache_path,
        basis=result.basis,
        relation_dim=np.int64(result.relation_dim),
        numerical_rank=np.int64(result.numerical_rank),
        singular_values=result.singular_values,
        validation_residual=np.float64(result.validation_max_relative_residual),
        training_rows=np.int64(result.training_rows),
    )
    return result


# -----------------------------------------------------------------------------
# Residue maps
# -----------------------------------------------------------------------------


def anchor_one_local_residue_block(
    source: Sequence[Cycle],
    source_basis: np.ndarray,
    deleted_label: int,
    n: int,
    target_fibres: Mapping[FibreKey, Sequence[Cycle]],
    target_indices: Mapping[FibreKey, Mapping[Cycle, int]],
) -> Optional[Tuple[FibreKey, np.ndarray]]:
    """AMP-18 anchor-1 residue, returned in one target-fibre coordinate space."""
    if source_basis.shape[1] == 0:
        return None
    source_index = {c: i for i, c in enumerate(source)}
    mapped: List[Tuple[Cycle, int, Cycle]] = []

    for c in source:
        if c[1] == deleted_label:
            reduced = (1,) + c[2:]
            sign = +1
        elif c[-1] == deleted_label:
            reduced = c[:-1]
            sign = -1
        else:
            continue
        image = canon(relabel_after_deletion(reduced, deleted_label, n))
        mapped.append((c, sign, image))

    if not mapped:
        return None

    target_key = pi_key(mapped[0][2])
    if any(pi_key(image) != target_key for _, _, image in mapped):
        raise RuntimeError("Anchor-1 residue failed the single-target-fibre property.")

    target_size = len(target_fibres[target_key])
    pushed = np.zeros((target_size, source_basis.shape[1]), dtype=np.float64)
    target_index = target_indices[target_key]
    for c, sign, image in mapped:
        pushed[target_index[image]] += sign * source_basis[source_index[c]]

    nonzero = np.linalg.norm(pushed, axis=0) > 1e-12
    return target_key, pushed[:, nonzero]


def full_anchor_residue_blocks(
    anchor: int,
    n: int,
    source_fibres: Mapping[FibreKey, Sequence[Cycle]],
    source_bases: Mapping[FibreKey, RelationBasis],
    target_all_cycles: Sequence[Cycle],
) -> Iterator[Tuple[FibreKey, int, np.ndarray]]:
    """Yield full ambient (n-1)-ordering residue blocks for one anchor."""
    target_index = {c: i for i, c in enumerate(target_all_cycles)}
    target_dim = len(target_all_cycles)

    for source_key, source in source_fibres.items():
        relation_basis = source_bases[source_key].basis
        if relation_basis.shape[1] == 0:
            continue
        source_index = {c: i for i, c in enumerate(source)}
        by_channel: MutableMapping[int, List[Tuple[int, int, Cycle]]] = defaultdict(list)

        for c in source:
            position = c.index(anchor)
            after = c[(position + 1) % n]
            before = c[(position - 1) % n]
            for deleted_label, sign in ((after, +1), (before, -1)):
                reduced = tuple(x for x in c if x != deleted_label)
                image = canon(relabel_after_deletion(reduced, deleted_label, n))
                by_channel[deleted_label].append(
                    (source_index[c], sign, image)
                )

        for deleted_label, rows in sorted(by_channel.items()):
            block = np.zeros((target_dim, relation_basis.shape[1]), dtype=np.float64)
            for source_row, sign, image in rows:
                block[target_index[image]] += sign * relation_basis[source_row]
            nonzero = np.linalg.norm(block, axis=0) > 1e-12
            if np.any(nonzero):
                yield source_key, deleted_label, block[:, nonzero]


# -----------------------------------------------------------------------------
# Linear span utilities
# -----------------------------------------------------------------------------


def matrix_rank_relative(matrix: np.ndarray, tolerance: float) -> Tuple[int, np.ndarray]:
    if matrix.size == 0:
        return 0, np.zeros(0)
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    if singular_values.size == 0 or singular_values[0] == 0:
        return 0, singular_values
    rank = int(np.count_nonzero(singular_values > singular_values[0] * tolerance))
    return rank, singular_values


def append_orthonormal_span(
    q: np.ndarray,
    block: np.ndarray,
    relative_tolerance: float,
    absolute_tolerance: float = 1e-11,
) -> Tuple[np.ndarray, int]:
    """Append independent directions from block to an existing orthonormal Q."""
    if block.size == 0 or block.shape[1] == 0:
        return q, 0
    residual = block.astype(np.float64, copy=True)

    if q.shape[1]:
        # Two passes reduce loss of orthogonality for a large accumulated basis.
        residual -= q @ (q.T @ residual)
        residual -= q @ (q.T @ residual)

    u, singular_values, _ = np.linalg.svd(residual, full_matrices=False)
    if singular_values.size == 0 or singular_values[0] == 0:
        return q, 0
    threshold = max(absolute_tolerance, singular_values[0] * relative_tolerance)
    rank = int(np.count_nonzero(singular_values > threshold))
    if rank == 0:
        return q, 0

    new = u[:, :rank]
    if q.shape[1]:
        new -= q @ (q.T @ new)
        new, _ = np.linalg.qr(new, mode="reduced")
    q_new = np.hstack([q, new])
    return q_new, rank


def vector_span_residual(vector: np.ndarray, q: np.ndarray) -> float:
    denominator = np.linalg.norm(vector)
    if denominator == 0:
        return 0.0
    residual = vector - q @ (q.T @ vector) if q.shape[1] else vector
    return float(np.linalg.norm(residual) / denominator)


# -----------------------------------------------------------------------------
# CSV and JSON helpers
# -----------------------------------------------------------------------------


def write_csv(path: Path, rows: Sequence[Mapping[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


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


# -----------------------------------------------------------------------------
# Main experiment
# -----------------------------------------------------------------------------


def build_all_bases(
    n: int,
    fibre_map: Mapping[FibreKey, Sequence[Cycle]],
    cache_dir: Path,
    args: argparse.Namespace,
    seed_offset: int,
) -> Tuple[Dict[FibreKey, RelationBasis], List[Dict[str, object]]]:
    results: Dict[FibreKey, RelationBasis] = {}
    summary_rows: List[Dict[str, object]] = []
    items = list(fibre_map.items())

    print(f"\nBuilding/loading relation bases for n={n}: {len(items)} fibres")
    started = time.time()
    for index, (key, chamber) in enumerate(items, start=1):
        t0 = time.time()
        result = load_or_compute_relation_basis(
            chamber=chamber,
            n=n,
            fibre_index=index - 1,
            cache_dir=cache_dir,
            train_seed=args.seed + seed_offset,
            validation_seed=args.seed + seed_offset + 100_000 + index,
            rows_multiplier=args.rows_multiplier,
            min_rows=args.min_rows,
            validation_rows=args.validation_rows,
            svd_relative_tolerance=args.svd_tolerance,
            force_rebuild=args.force_rebuild,
        )
        results[key] = result
        elapsed = time.time() - t0
        gap_decades = None
        if 0 < result.numerical_rank < len(result.singular_values):
            top_null = result.singular_values[result.numerical_rank]
            last_kept = result.singular_values[result.numerical_rank - 1]
            if top_null > 0:
                gap_decades = math.log10(last_kept / top_null)
        summary_rows.append(
            {
                "n": n,
                "fibre_index": index - 1,
                "fibre_key": key_text(key),
                "fibre_size": len(chamber),
                "numerical_rank": result.numerical_rank,
                "relation_dim": result.relation_dim,
                "training_rows": result.training_rows,
                "validation_max_relative_residual": f"{result.validation_max_relative_residual:.17g}",
                "singular_gap_decades": "" if gap_decades is None else f"{gap_decades:.8f}",
                "from_cache": result.from_cache,
                "elapsed_seconds": f"{elapsed:.3f}",
            }
        )
        status = "cache" if result.from_cache else "computed"
        print(
            f"  [{index:02d}/{len(items):02d}] size={len(chamber):4d} "
            f"r={result.relation_dim:4d} validation={result.validation_max_relative_residual:.2e} "
            f"{status}, {elapsed:.1f}s"
        )
    print(f"Completed n={n} bases in {(time.time() - started) / 60:.2f} minutes.")
    return results, summary_rows


def run_amp18(
    n: int,
    source_fibres: Mapping[FibreKey, Sequence[Cycle]],
    target_fibres: Mapping[FibreKey, Sequence[Cycle]],
    source_bases: Mapping[FibreKey, RelationBasis],
    target_bases: Mapping[FibreKey, RelationBasis],
    args: argparse.Namespace,
) -> Tuple[List[Dict[str, object]], Dict[FibreKey, np.ndarray]]:
    print(f"\nAMP-18F residue generation audit: n={n} -> n={n-1}, anchor=1")
    target_indices = {
        key: {cycle: i for i, cycle in enumerate(chamber)}
        for key, chamber in target_fibres.items()
    }
    arrivals: MutableMapping[FibreKey, List[np.ndarray]] = defaultdict(list)
    residue_block_count = 0

    for source_index, (source_key, source) in enumerate(source_fibres.items(), start=1):
        relation_basis = source_bases[source_key].basis
        if relation_basis.shape[1] == 0:
            continue
        for deleted_label in range(2, n + 1):
            result = anchor_one_local_residue_block(
                source=source,
                source_basis=relation_basis,
                deleted_label=deleted_label,
                n=n,
                target_fibres=target_fibres,
                target_indices=target_indices,
            )
            if result is None:
                continue
            target_key, block = result
            if block.shape[1]:
                arrivals[target_key].append(block)
                residue_block_count += 1
        if source_index % 5 == 0 or source_index == len(source_fibres):
            print(
                f"  source fibres processed: {source_index}/{len(source_fibres)}; "
                f"nonzero residue blocks: {residue_block_count}"
            )

    target_rows: List[Dict[str, object]] = []
    arrival_matrices: Dict[FibreKey, np.ndarray] = {}
    full_count = 0
    partial_count = 0

    print("\nTarget fibre rank table")
    print("  target size | r_target | image vectors | span rank | fresh residual | result")
    for target_index, (target_key, chamber) in enumerate(target_fibres.items()):
        blocks = arrivals.get(target_key, [])
        matrix = np.hstack(blocks) if blocks else np.zeros((len(chamber), 0))
        arrival_matrices[target_key] = matrix
        rank, singular_values = matrix_rank_relative(matrix, args.span_tolerance)
        target_relation_dim = target_bases[target_key].relation_dim

        if matrix.shape[1]:
            validation_matrix = parke_taylor_matrix(
                chamber,
                n - 1,
                args.seed + 900_000 + target_index,
                args.residue_validation_rows,
            )
            norms = np.linalg.norm(matrix, axis=0)
            mask = norms > 1e-12
            if np.any(mask):
                residual = float(
                    np.max(
                        np.linalg.norm(validation_matrix @ matrix[:, mask], axis=0)
                        / norms[mask]
                    )
                )
            else:
                residual = 0.0
        else:
            residual = float("nan")

        complete = rank == target_relation_dim
        full_count += int(complete)
        partial_count += int(not complete)
        even_set = target_key[0] if 1 in target_key[0] else target_key[1]
        row = {
            "target_index": target_index,
            "target_key": key_text(target_key),
            "anchor_containing_set": ",".join(map(str, even_set)),
            "target_size": len(chamber),
            "target_relation_dim": target_relation_dim,
            "anchor1_image_vectors": matrix.shape[1],
            "anchor1_span_rank": rank,
            "anchor1_fresh_max_relative_residual": f"{residual:.17g}",
            "rank_deficit": target_relation_dim - rank,
            "complete": complete,
            "smallest_nonzero_span_singular_value": (
                ""
                if rank == 0
                else f"{singular_values[rank - 1]:.17g}"
            ),
            "first_discarded_span_singular_value": (
                ""
                if rank >= len(singular_values)
                else f"{singular_values[rank]:.17g}"
            ),
        }
        target_rows.append(row)
        verdict = "FULL" if complete else "PARTIAL"
        print(
            f"  {len(chamber):11d} | {target_relation_dim:8d} | "
            f"{matrix.shape[1]:13d} | {rank:9d} | {residual:14.2e} | {verdict}"
        )

    print(
        f"\nAMP-18F summary: full={full_count}, partial={partial_count}, "
        f"targets={len(target_fibres)}"
    )
    return target_rows, arrival_matrices


def build_anchor_span(
    anchor: int,
    n: int,
    source_fibres: Mapping[FibreKey, Sequence[Cycle]],
    source_bases: Mapping[FibreKey, RelationBasis],
    target_all_cycles: Sequence[Cycle],
    args: argparse.Namespace,
    initial_q: Optional[np.ndarray] = None,
    stop_vector: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, Dict[str, object]]:
    q = (
        np.zeros((len(target_all_cycles), 0), dtype=np.float64)
        if initial_q is None
        else initial_q.copy()
    )
    pending: List[np.ndarray] = []
    pending_cols = 0
    blocks_seen = 0
    vectors_seen = 0
    independent_added = 0
    closure_residual = None
    started = time.time()

    def flush_pending(q_current: np.ndarray) -> np.ndarray:
        nonlocal pending, pending_cols, independent_added, closure_residual
        if not pending:
            return q_current
        block = np.hstack(pending)
        before = q_current.shape[1]
        q_current, added = append_orthonormal_span(
            q_current,
            block,
            relative_tolerance=args.span_tolerance,
            absolute_tolerance=args.span_absolute_tolerance,
        )
        independent_added += added
        pending = []
        pending_cols = 0
        if stop_vector is not None:
            closure_residual = vector_span_residual(stop_vector, q_current)
        print(
            f"    span flush: ambient rank {before} -> {q_current.shape[1]} "
            f"(+{added}); closure residual="
            f"{'n/a' if closure_residual is None else f'{closure_residual:.3e}'}"
        )
        return q_current

    for source_key, deleted_label, block in full_anchor_residue_blocks(
        anchor=anchor,
        n=n,
        source_fibres=source_fibres,
        source_bases=source_bases,
        target_all_cycles=target_all_cycles,
    ):
        blocks_seen += 1
        vectors_seen += block.shape[1]
        pending.append(block)
        pending_cols += block.shape[1]

        if pending_cols >= args.orthogonalization_block_columns:
            q = flush_pending(q)
            if (
                stop_vector is not None
                and closure_residual is not None
                and closure_residual < args.closure_stop_tolerance
            ):
                print(
                    f"    Closure reached after {blocks_seen} blocks and "
                    f"{vectors_seen} vectors; stopping anchor {anchor} early."
                )
                break

    q = flush_pending(q)
    if stop_vector is not None:
        closure_residual = vector_span_residual(stop_vector, q)

    metadata = {
        "anchor": anchor,
        "blocks_seen": blocks_seen,
        "vectors_seen": vectors_seen,
        "final_span_rank": q.shape[1],
        "independent_directions_added": independent_added,
        "closure_residual": closure_residual,
        "elapsed_seconds": time.time() - started,
    }
    return q, metadata


def run_amp20(
    n: int,
    source_fibres: Mapping[FibreKey, Sequence[Cycle]],
    target_fibres: Mapping[FibreKey, Sequence[Cycle]],
    source_bases: Mapping[FibreKey, RelationBasis],
    target_bases: Mapping[FibreKey, RelationBasis],
    anchor1_arrivals: Mapping[FibreKey, np.ndarray],
    args: argparse.Namespace,
) -> Dict[str, object]:
    if n != 9:
        raise ValueError("AMP-20 exceptional-fibre closure is currently defined for n=9 -> 8.")

    exceptional_set = tuple(sorted(int(x) for x in args.exceptional_set.split(",")))
    exceptional_key: Optional[FibreKey] = None
    for key in target_fibres:
        anchor_containing = key[0] if 1 in key[0] else key[1]
        if tuple(anchor_containing) == exceptional_set:
            exceptional_key = key
            break
    if exceptional_key is None:
        raise RuntimeError(f"Could not find exceptional target fibre {exceptional_set}.")

    chamber = target_fibres[exceptional_key]
    target_basis = target_bases[exceptional_key].basis
    relation_dim = target_bases[exceptional_key].relation_dim
    anchor1_local = anchor1_arrivals[exceptional_key]
    local_rank, local_singular_values = matrix_rank_relative(
        anchor1_local,
        args.span_tolerance,
    )

    print("\nAMP-20 all-anchor closure audit")
    print(f"  Exceptional target: {key_text(exceptional_key)}")
    print(f"  Fibre size: {len(chamber)}")
    print(f"  Target relation dimension: {relation_dim}")
    print(f"  Anchor-1 local image rank: {local_rank}/{relation_dim}")

    coordinates = target_basis.T @ anchor1_local
    u, coordinate_singular_values, _ = np.linalg.svd(coordinates, full_matrices=True)
    coordinate_rank = (
        0
        if coordinate_singular_values.size == 0 or coordinate_singular_values[0] == 0
        else int(
            np.count_nonzero(
                coordinate_singular_values
                > coordinate_singular_values[0] * args.span_tolerance
            )
        )
    )
    missing_dimension = relation_dim - coordinate_rank
    if missing_dimension != 1:
        raise RuntimeError(
            f"Expected one missing exceptional direction, found {missing_dimension}."
        )
    missing_coordinate = u[:, coordinate_rank : coordinate_rank + 1]
    missing_local = target_basis @ missing_coordinate

    all_target_cycles = canonical_cycles(n - 1)
    all_target_index = {c: i for i, c in enumerate(all_target_cycles)}
    missing_full = np.zeros((len(all_target_cycles), 1), dtype=np.float64)
    for i, cycle in enumerate(chamber):
        missing_full[all_target_index[cycle], 0] = missing_local[i, 0]

    print("\n  Building full anchor-1 residue span...")
    q1, anchor1_meta = build_anchor_span(
        anchor=1,
        n=n,
        source_fibres=source_fibres,
        source_bases=source_bases,
        target_all_cycles=all_target_cycles,
        args=args,
        initial_q=None,
        stop_vector=None,
    )
    anchor1_missing_residual = vector_span_residual(missing_full, q1)
    print(
        f"  Missing-direction residual against anchor-1 full span: "
        f"{anchor1_missing_residual:.3e}"
    )

    print("\n  Adding anchor-2 residue directions...")
    q12, anchor2_meta = build_anchor_span(
        anchor=2,
        n=n,
        source_fibres=source_fibres,
        source_bases=source_bases,
        target_all_cycles=all_target_cycles,
        args=args,
        initial_q=q1,
        stop_vector=missing_full,
    )
    combined_residual = vector_span_residual(missing_full, q12)
    print(f"\n  Combined anchor-1 + anchor-2 residual: {combined_residual:.3e}")
    print(
        "  Verdict: "
        + (
            "GAP DISSOLVES UNDER RE-ANCHORING"
            if combined_residual < args.closure_verdict_tolerance
            else "MISSING DIRECTION NOT CLOSED AT REQUESTED TOLERANCE"
        )
    )

    return {
        "exceptional_target_key": key_text(exceptional_key),
        "exceptional_target_size": len(chamber),
        "target_relation_dim": relation_dim,
        "anchor1_local_rank": local_rank,
        "anchor1_local_rank_deficit": relation_dim - local_rank,
        "coordinate_rank": coordinate_rank,
        "missing_dimension": missing_dimension,
        "anchor1_missing_full_span_residual": anchor1_missing_residual,
        "combined_anchor1_anchor2_residual": combined_residual,
        "closure_verdict_tolerance": args.closure_verdict_tolerance,
        "gap_dissolves": combined_residual < args.closure_verdict_tolerance,
        "anchor1_span": anchor1_meta,
        "anchor2_extension": anchor2_meta,
        "anchor1_local_singular_values": local_singular_values.tolist(),
        "coordinate_singular_values": coordinate_singular_values.tolist(),
    }


def run_experiment(args: argparse.Namespace) -> Dict[str, object]:
    out_dir = Path(args.out_dir).resolve()
    cache_dir = out_dir / "cache"
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    n = 7 if args.stage == "smoke" else 9
    target_n = n - 1

    print("=" * 92)
    print("EHF-AMP-FOUND-01: AMP-18F / AMP-20 REPRODUCIBILITY REBUILD")
    print("=" * 92)
    print(f"stage:                    {args.stage}")
    print(f"source multiplicity n:    {n}")
    print(f"target multiplicity:      {target_n}")
    print(f"output directory:         {out_dir}")
    print(f"seed:                     {args.seed}")
    print(f"SVD tolerance:            {args.svd_tolerance}")
    print(f"span tolerance:           {args.span_tolerance}")
    print(f"rows multiplier:          {args.rows_multiplier}")
    print(f"minimum training rows:    {args.min_rows}")
    print(f"validation rows:          {args.validation_rows}")
    print(f"force rebuild:            {args.force_rebuild}")
    print()

    started = time.time()
    source_fibre_map = fibres(n)
    target_fibre_map = fibres(target_n)
    print(
        f"Ordering/fibre counts: source states={sum(map(len, source_fibre_map.values()))}, "
        f"source fibres={len(source_fibre_map)}; target states={sum(map(len, target_fibre_map.values()))}, "
        f"target fibres={len(target_fibre_map)}"
    )

    target_bases, target_basis_rows = build_all_bases(
        n=target_n,
        fibre_map=target_fibre_map,
        cache_dir=cache_dir,
        args=args,
        seed_offset=7,
    )
    write_csv(
        out_dir / f"relation_basis_summary_n{target_n}.csv",
        target_basis_rows,
        fieldnames=list(target_basis_rows[0].keys()),
    )

    source_bases, source_basis_rows = build_all_bases(
        n=n,
        fibre_map=source_fibre_map,
        cache_dir=cache_dir,
        args=args,
        seed_offset=1,
    )
    write_csv(
        out_dir / f"relation_basis_summary_n{n}.csv",
        source_basis_rows,
        fieldnames=list(source_basis_rows[0].keys()),
    )

    target_rows, anchor1_arrivals = run_amp18(
        n=n,
        source_fibres=source_fibre_map,
        target_fibres=target_fibre_map,
        source_bases=source_bases,
        target_bases=target_bases,
        args=args,
    )
    write_csv(
        out_dir / f"amp18_target_rank_summary_n{n}_to_n{target_n}.csv",
        target_rows,
        fieldnames=list(target_rows[0].keys()),
    )

    amp20_result = None
    if args.stage in {"all", "amp20"}:
        amp20_result = run_amp20(
            n=n,
            source_fibres=source_fibre_map,
            target_fibres=target_fibre_map,
            source_bases=source_bases,
            target_bases=target_bases,
            anchor1_arrivals=anchor1_arrivals,
            args=args,
        )

    full_targets = sum(bool(row["complete"]) for row in target_rows)
    partial_targets = len(target_rows) - full_targets
    summary = {
        "script": Path(__file__).name,
        "stage": args.stage,
        "n_source": n,
        "n_target": target_n,
        "source_state_count": sum(map(len, source_fibre_map.values())),
        "source_fibre_count": len(source_fibre_map),
        "target_state_count": sum(map(len, target_fibre_map.values())),
        "target_fibre_count": len(target_fibre_map),
        "amp18_full_target_count": full_targets,
        "amp18_partial_target_count": partial_targets,
        "amp18_partial_targets": [
            row for row in target_rows if not bool(row["complete"])
        ],
        "amp20": amp20_result,
        "parameters": vars(args),
        "elapsed_seconds": time.time() - started,
    }

    with (out_dir / "summary.json").open("w") as handle:
        json.dump(json_safe(summary), handle, indent=2, sort_keys=True)

    print("\n" + "=" * 92)
    print("FINAL SUMMARY")
    print("=" * 92)
    print(f"AMP-18 full targets:       {full_targets}/{len(target_rows)}")
    print(f"AMP-18 partial targets:    {partial_targets}")
    if amp20_result is not None:
        print(
            f"AMP-20 combined residual:  "
            f"{amp20_result['combined_anchor1_anchor2_residual']:.3e}"
        )
        print(f"AMP-20 gap dissolves:      {amp20_result['gap_dissolves']}")
    print(f"elapsed:                   {(time.time() - started) / 60:.2f} minutes")
    print(f"summary:                   {out_dir / 'summary.json'}")
    print("=" * 92)
    return summary


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reproduce AMP-18F target ranks and AMP-20 re-anchoring closure."
    )
    parser.add_argument(
        "--stage",
        choices=["smoke", "amp18", "amp20", "all"],
        default="all",
        help="smoke uses n=7->6; amp18 runs n=9->8 target ranks; amp20/all also run closure.",
    )
    parser.add_argument(
        "--out-dir",
        default="runs/ehf_amp_found_01_amp18_20",
        help="Output and cache directory.",
    )
    parser.add_argument("--seed", type=int, default=11)
    parser.add_argument("--rows-multiplier", type=float, default=3.0)
    parser.add_argument("--min-rows", type=int, default=400)
    parser.add_argument("--validation-rows", type=int, default=160)
    parser.add_argument("--residue-validation-rows", type=int, default=160)
    parser.add_argument("--svd-tolerance", type=float, default=1e-9)
    parser.add_argument("--span-tolerance", type=float, default=1e-9)
    parser.add_argument("--span-absolute-tolerance", type=float, default=1e-11)
    parser.add_argument("--orthogonalization-block-columns", type=int, default=256)
    parser.add_argument("--closure-stop-tolerance", type=float, default=1e-10)
    parser.add_argument("--closure-verdict-tolerance", type=float, default=1e-6)
    parser.add_argument(
        "--exceptional-set",
        default="1,4,5,6",
        help="Anchor-containing label set of the exceptional n=8 fibre.",
    )
    parser.add_argument(
        "--force-rebuild",
        action="store_true",
        help="Ignore cached relation bases and recompute them.",
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
        sys.stdout = Tee(original_stdout, log_handle)
        sys.stderr = Tee(original_stderr, log_handle)
        try:
            print(f"\n\n===== RUN START {time.strftime('%Y-%m-%d %H:%M:%S')} =====")
            run_experiment(args)
            print(f"===== RUN END {time.strftime('%Y-%m-%d %H:%M:%S')} =====")
            return 0
        except KeyboardInterrupt:
            print("\nInterrupted. Cached relation bases already written can be reused on restart.")
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
