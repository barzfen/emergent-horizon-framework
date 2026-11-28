#!/usr/bin/env python3
"""
EHF-AMP-FOUND-02A: Growth–Factorisation Compatibility
=====================================================

Purpose
-------
Test whether the exact state-level inverse relation between anchor-side vertex
insertion and anchor-collinear deletion survives at the level of local
Parke–Taylor relation spaces.

The probe distinguishes four statements that must not be conflated:

1. State section (exact combinatorics): deleting the newly inserted label
   recovers the original cycle.
2. Coefficient lift: insert the same relation coefficients into the larger
   ordering space. This need not itself be a relation at the larger
   multiplicity.
3. Factorisation inheritance: residues of genuine (n+1)-point local relations
   may or may not span the complete n-point local relation space.
4. Channel-new directions: the kernel of the residue map on a child relation
   space consists of relations invisible to that particular growth channel.
   This is channel-relative, not an absolute claim of physical novelty.

Default transitions: 6->7, 7->8, 8->9.

The script imports the tested relation-basis machinery from
`ehf_amp_found_01_reproduce_amp18_20.py` and reuses its cache directory.
Only NumPy and the Python standard library are required.

Example
-------

    caffeinate -i python3 scripts/ehf_amp_found_02a_growth_factorisation_compatibility.py \
      --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
      --base-run-dir runs/ehf_amp_found_01_amp18_20 \
      --out-dir runs/ehf_amp_found_02a_growth_factorisation_seed11 \
      --seed 11

Smoke test:

    python3 scripts/ehf_amp_found_02a_growth_factorisation_compatibility.py \
      --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
      --base-run-dir runs/ehf_amp_found_01_amp18_20 \
      --out-dir runs/ehf_amp_found_02a_smoke \
      --transitions 6:7 \
      --no-exceptional-audit
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

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


def load_base_module(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Base script not found: {path}")
    spec = importlib.util.spec_from_file_location("ehf_amp_found_01_base", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to import base script: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def parse_transitions(text: str) -> List[Tuple[int, int]]:
    result: List[Tuple[int, int]] = []
    for item in text.split(","):
        item = item.strip()
        if not item:
            continue
        left, right = item.split(":", 1)
        n, m = int(left), int(right)
        if m != n + 1:
            raise ValueError(f"Transition must have m=n+1, got {n}:{m}")
        result.append((n, m))
    if not result:
        raise ValueError("At least one transition is required.")
    return result


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    fieldnames: List[str] = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)
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


def fmt(x: float) -> str:
    return f"{x:.17g}"


def safe_rank(matrix: np.ndarray, relative_tolerance: float, absolute_tolerance: float) -> Tuple[int, np.ndarray]:
    if matrix.size == 0 or matrix.shape[1] == 0:
        return 0, np.zeros(0, dtype=float)
    matrix = np.asarray(matrix, dtype=float)
    if not np.all(np.isfinite(matrix)):
        raise ValueError("Non-finite value encountered in rank calculation.")
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    if singular_values.size == 0 or singular_values[0] == 0:
        return 0, singular_values
    threshold = max(absolute_tolerance, singular_values[0] * relative_tolerance)
    return int(np.count_nonzero(singular_values > threshold)), singular_values


def orthonormal_span(matrix: np.ndarray, relative_tolerance: float, absolute_tolerance: float) -> np.ndarray:
    if matrix.size == 0 or matrix.shape[1] == 0:
        return np.zeros((matrix.shape[0], 0), dtype=float)
    u, s, _ = np.linalg.svd(np.asarray(matrix, dtype=float), full_matrices=False)
    if s.size == 0 or s[0] == 0:
        return np.zeros((matrix.shape[0], 0), dtype=float)
    threshold = max(absolute_tolerance, s[0] * relative_tolerance)
    rank = int(np.count_nonzero(s > threshold))
    return u[:, :rank]


def max_subspace_residual(vectors: np.ndarray, q: np.ndarray) -> float:
    if vectors.size == 0 or vectors.shape[1] == 0:
        return 0.0
    residual = vectors - q @ (q.T @ vectors) if q.shape[1] else vectors
    numerators = np.linalg.norm(residual, axis=0)
    denominators = np.linalg.norm(vectors, axis=0)
    mask = denominators > 1e-14
    if not np.any(mask):
        return 0.0
    return float(np.max(numerators[mask] / denominators[mask]))


def vector_residual(vector: np.ndarray, q: np.ndarray) -> float:
    denominator = float(np.linalg.norm(vector))
    if denominator == 0:
        return 0.0
    residual = vector - q @ (q.T @ vector) if q.shape[1] else vector
    return float(np.linalg.norm(residual) / denominator)


def pt_residual(base, chamber: Sequence[Cycle], n: int, vectors: np.ndarray, seed: int, rows: int) -> float:
    if vectors.size == 0 or vectors.shape[1] == 0:
        return 0.0
    matrix = base.parke_taylor_matrix(chamber, n, seed, rows)
    norms = np.linalg.norm(vectors, axis=0)
    mask = norms > 1e-13
    if not np.any(mask):
        return 0.0
    return float(np.max(np.linalg.norm(matrix @ vectors[:, mask], axis=0) / norms[mask]))


def intersection_basis(
    q1: np.ndarray,
    q2: np.ndarray,
    containment_tolerance: float,
) -> Tuple[np.ndarray, np.ndarray]:
    """Return an orthonormal basis for span(q1) ∩ span(q2), plus principal cosines."""
    if q1.shape[1] == 0 or q2.shape[1] == 0:
        return np.zeros((q1.shape[0], 0), dtype=float), np.zeros(0, dtype=float)
    u, s, _ = np.linalg.svd(q1.T @ q2, full_matrices=False)
    keep = s >= (1.0 - containment_tolerance)
    if not np.any(keep):
        return np.zeros((q1.shape[0], 0), dtype=float), s
    basis = q1 @ u[:, keep]
    basis, _ = np.linalg.qr(basis, mode="reduced")
    return basis, s


def insert_cycle(base, cycle: Cycle, gap: int, new_label: int) -> Cycle:
    raw = cycle[:gap] + (new_label,) + cycle[gap:]
    return base.canon(raw)


def insertion_sign(image: Cycle, new_label: int) -> int:
    if image[1] == new_label:
        return +1
    if image[-1] == new_label:
        return -1
    raise RuntimeError("Anchor-side insertion did not leave the new label adjacent to anchor 1.")


def delete_new_label(base, image: Cycle, new_label: int) -> Tuple[int, Cycle]:
    if image[1] == new_label:
        sign = +1
        reduced = (1,) + image[2:]
    elif image[-1] == new_label:
        sign = -1
        reduced = image[:-1]
    else:
        raise RuntimeError("New label is not adjacent to anchor 1.")
    # new_label is the maximum, so no nontrivial relabelling is needed.
    return sign, base.canon(reduced)


@dataclass
class BasisRecord:
    fibres: Dict[FibreKey, List[Cycle]]
    bases: Dict[FibreKey, object]


def seed_offset_for_n(n: int) -> int:
    # Matches the successful AMP-18 cache convention: even n used +7, odd n +1.
    return 7 if n % 2 == 0 else 1


def build_bases_for_n(base, n: int, cache_dir: Path, args, summary_rows: List[Dict[str, object]]) -> BasisRecord:
    fibre_map = base.fibres(n)
    bases: Dict[FibreKey, object] = {}
    print(f"\nBuilding/loading n={n} local relation bases: {len(fibre_map)} fibres")
    started = time.time()
    offset = seed_offset_for_n(n)
    for index, (key, chamber) in enumerate(fibre_map.items()):
        t0 = time.time()
        result = base.load_or_compute_relation_basis(
            chamber=chamber,
            n=n,
            fibre_index=index,
            cache_dir=cache_dir,
            train_seed=args.seed + offset,
            validation_seed=args.seed + offset + 100_000 + index,
            rows_multiplier=args.rows_multiplier,
            min_rows=args.min_rows,
            validation_rows=args.validation_rows,
            svd_relative_tolerance=args.svd_tolerance,
            force_rebuild=args.force_rebuild,
        )
        bases[key] = result
        summary_rows.append({
            "n": n,
            "fibre_index": index,
            "fibre_key": base.key_text(key),
            "fibre_size": len(chamber),
            "relation_dim": result.relation_dim,
            "numerical_rank": result.numerical_rank,
            "validation_max_relative_residual": fmt(result.validation_max_relative_residual),
            "from_cache": result.from_cache,
            "elapsed_seconds": f"{time.time()-t0:.3f}",
        })
        if (index + 1) % 10 == 0 or index + 1 == len(fibre_map):
            print(
                f"  [{index+1:02d}/{len(fibre_map):02d}] size={len(chamber):4d} "
                f"r={result.relation_dim:4d} validation={result.validation_max_relative_residual:.2e} "
                f"{'cache' if result.from_cache else 'computed'}"
            )
    print(f"Completed n={n} bases in {(time.time()-started)/60:.2f} minutes.")
    return BasisRecord(fibres=fibre_map, bases=bases)


def build_oriented_insertion_matrix(
    base,
    parent: Sequence[Cycle],
    child: Sequence[Cycle],
    gap: int,
    new_label: int,
) -> Tuple[np.ndarray, float, List[int]]:
    child_index = {c: i for i, c in enumerate(child)}
    matrix = np.zeros((len(child), len(parent)), dtype=float)
    signs: List[int] = []
    max_section_error = 0.0
    for j, cycle in enumerate(parent):
        image = insert_cycle(base, cycle, gap, new_label)
        sign = insertion_sign(image, new_label)
        signs.append(sign)
        matrix[child_index[image], j] = sign
        residue_sign, back = delete_new_label(base, image, new_label)
        max_section_error = max(
            max_section_error,
            0.0 if (back == cycle and residue_sign * sign == 1) else 1.0,
        )
    return matrix, max_section_error, signs


def build_child_residue_operator_map(
    base,
    child: Sequence[Cycle],
    parent_fibres: Mapping[FibreKey, Sequence[Cycle]],
    new_label: int,
) -> Dict[FibreKey, Tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """Build residue blocks from one child fibre into every parent fibre it reaches.

    For odd->even growth, a fixed child fibre can residue into more than one
    parent fibre. That is structural, not an error. The output therefore keeps
    one signed operator block per reached parent fibre.
    """
    grouped: MutableMapping[FibreKey, List[Tuple[int, int, Cycle]]] = defaultdict(list)
    for child_row, cycle in enumerate(child):
        if cycle[1] == new_label:
            sign = +1
            reduced = (1,) + cycle[2:]
        elif cycle[-1] == new_label:
            sign = -1
            reduced = cycle[:-1]
        else:
            continue
        image = base.canon(reduced)
        grouped[base.pi_key(image)].append((child_row, sign, image))

    result: Dict[FibreKey, Tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
    for parent_key, mapped in grouped.items():
        parent = parent_fibres[parent_key]
        parent_index = {c: i for i, c in enumerate(parent)}
        full = np.zeros((len(parent), len(child)), dtype=float)
        plus = np.zeros_like(full)
        minus = np.zeros_like(full)
        for child_row, sign, image in mapped:
            row = parent_index[image]
            full[row, child_row] += sign
            if sign == +1:
                plus[row, child_row] += 1.0
            else:
                minus[row, child_row] -= 1.0
        result[parent_key] = (full, plus, minus)
    return result


def embed_local_matrix(
    chamber: Sequence[Cycle],
    matrix: np.ndarray,
    global_index: Mapping[Cycle, int],
    global_size: int,
) -> np.ndarray:
    out = np.zeros((global_size, matrix.shape[1]), dtype=float)
    if matrix.shape[1] == 0:
        return out
    rows = [global_index[c] for c in chamber]
    out[rows, :] = matrix
    return out


def assemble_global_residue_operators(
    operator_map: Mapping[FibreKey, Tuple[np.ndarray, np.ndarray, np.ndarray]],
    parent_fibres: Mapping[FibreKey, Sequence[Cycle]],
    parent_global_index: Mapping[Cycle, int],
    parent_global_size: int,
    child_size: int,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    full_global = np.zeros((parent_global_size, child_size), dtype=float)
    plus_global = np.zeros_like(full_global)
    minus_global = np.zeros_like(full_global)
    for parent_key, (full, plus, minus) in operator_map.items():
        parent = parent_fibres[parent_key]
        rows = [parent_global_index[c] for c in parent]
        full_global[rows, :] += full
        plus_global[rows, :] += plus
        minus_global[rows, :] += minus
    return full_global, plus_global, minus_global



def relation_subspace_within_span(
    base,
    states: Sequence[Cycle],
    n: int,
    span_q: np.ndarray,
    args,
    train_seed: int,
    validation_seed: int,
) -> Tuple[np.ndarray, Dict[str, object]]:
    """Return the part of span_q that is a genuine global PT relation space.

    In the expected factorisation-compatible case every column of span_q is
    already relational, so a fresh validation check avoids a larger SVD. If
    that check fails, solve for the nullspace of PT evaluations restricted to
    span_q and validate the recovered subspace independently.
    """
    if span_q.shape[1] == 0:
        return span_q, {
            "raw_rank": 0,
            "relation_rank": 0,
            "raw_validation_residual": 0.0,
            "filtered_validation_residual": 0.0,
            "filter_applied": False,
            "training_rows": 0,
        }

    raw_validation = pt_residual(
        base, states, n, span_q, validation_seed, args.residue_validation_rows
    )
    if raw_validation < args.relation_verdict_tolerance:
        return span_q, {
            "raw_rank": span_q.shape[1],
            "relation_rank": span_q.shape[1],
            "raw_validation_residual": raw_validation,
            "filtered_validation_residual": raw_validation,
            "filter_applied": False,
            "training_rows": args.residue_validation_rows,
        }

    # The non-relation quotient of the full ordering space has dimension at
    # most (n-2)! in the constant-coefficient KK layer. Sample beyond that
    # bound rather than scaling with the much larger ambient state count.
    quotient_rank_bound = math.factorial(max(1, n - 2))
    training_rows = max(
        args.min_rows,
        quotient_rank_bound + 80,
        int(math.ceil(1.25 * quotient_rank_bound)),
    )
    matrix = base.parke_taylor_matrix(states, n, train_seed, training_rows)
    restricted_complex = matrix @ span_q
    a = np.vstack([restricted_complex.real, restricted_complex.imag])
    column_scales = np.ones(span_q.shape[1], dtype=float)
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
        threshold = max(
            args.rank_absolute_tolerance,
            singular_values[0] * args.rank_tolerance,
        )
        numerical_rank = int(np.count_nonzero(singular_values > threshold))

    relation_dim = span_q.shape[1] - numerical_rank
    if relation_dim:
        coeff = vh[numerical_rank:].T / column_scales[:, None]
        relation_q = span_q @ coeff
        relation_q = orthonormal_span(
            relation_q, args.rank_tolerance, args.rank_absolute_tolerance
        )
    else:
        relation_q = np.zeros((span_q.shape[0], 0), dtype=float)

    filtered_validation = pt_residual(
        base,
        states,
        n,
        relation_q,
        validation_seed + 1,
        args.residue_validation_rows,
    )
    return relation_q, {
        "raw_rank": span_q.shape[1],
        "relation_rank": relation_q.shape[1],
        "raw_validation_residual": raw_validation,
        "filtered_validation_residual": filtered_validation,
        "filter_applied": True,
        "training_rows": training_rows,
        "evaluation_numerical_rank": numerical_rank,
        "smallest_nonzero_evaluation_sv": (
            "" if numerical_rank == 0 else fmt(float(singular_values[numerical_rank - 1]))
        ),
        "first_discarded_evaluation_sv": (
            "" if numerical_rank >= len(singular_values) else fmt(float(singular_values[numerical_rank]))
        ),
    }

def run_transition(
    base,
    n: int,
    m: int,
    parent_record: BasisRecord,
    child_record: BasisRecord,
    args,
    insertion_rows: List[Dict[str, object]],
    child_residue_rows: List[Dict[str, object]],
    parent_rows: List[Dict[str, object]],
    child_birth_rows: List[Dict[str, object]],
):
    print("\n" + "=" * 100)
    print(f"TRANSITION {n} -> {m}: growth insertion versus factorisation deletion")
    print("=" * 100)
    new_label = m
    parent_fibres = parent_record.fibres
    child_fibres = child_record.fibres
    parent_states = base.canonical_cycles(n)
    parent_global_index = {c: i for i, c in enumerate(parent_states)}
    parent_global_size = len(parent_states)

    insertion_blocks_by_child: MutableMapping[FibreKey, List[np.ndarray]] = defaultdict(list)
    insertion_sources_by_child: MutableMapping[FibreKey, List[str]] = defaultdict(list)
    branch_child_map: Dict[Tuple[FibreKey, str], FibreKey] = {}

    # ------------------------------------------------------------------
    # Q0/Q1: exact state section and naive relation-coefficient lift.
    # ------------------------------------------------------------------
    for parent_index, (parent_key, parent) in enumerate(parent_fibres.items()):
        parent_basis = parent_record.bases[parent_key].basis
        for branch, gap in (("A+", 1), ("A-", n)):
            images = [insert_cycle(base, c, gap, new_label) for c in parent]
            child_key = base.pi_key(images[0])
            if any(base.pi_key(x) != child_key for x in images):
                raise RuntimeError(f"{branch} insertion from one parent fibre was not child-fibre single-valued.")
            child = child_fibres[child_key]
            child_basis = child_record.bases[child_key].basis
            insertion_matrix, section_error, signs = build_oriented_insertion_matrix(
                base, parent, child, gap, new_label
            )
            lifted = insertion_matrix @ parent_basis
            insertion_blocks_by_child[child_key].append(lifted)
            insertion_sources_by_child[child_key].append(f"{base.key_text(parent_key)}:{branch}")
            branch_child_map[(parent_key, branch)] = child_key

            containment = max_subspace_residual(lifted, child_basis)
            lift_pt = pt_residual(
                base,
                child,
                m,
                lifted,
                args.seed + 200_000 + 1000 * n + 10 * parent_index + (0 if branch == "A+" else 1),
                args.residue_validation_rows,
            )
            q_lift = orthonormal_span(lifted, args.rank_tolerance, args.rank_absolute_tolerance)
            inter, principal = intersection_basis(child_basis, q_lift, args.containment_tolerance)
            projected = child_basis @ (child_basis.T @ lifted) if child_basis.shape[1] else np.zeros_like(lifted)
            projected_rank, _ = safe_rank(projected, args.rank_tolerance, args.rank_absolute_tolerance)

            insertion_rows.append({
                "n_parent": n,
                "n_child": m,
                "parent_key": base.key_text(parent_key),
                "branch": branch,
                "child_key": base.key_text(child_key),
                "parent_size": len(parent),
                "child_size": len(child),
                "parent_relation_dim": parent_basis.shape[1],
                "child_relation_dim": child_basis.shape[1],
                "state_section_max_error": fmt(section_error),
                "oriented_sign_plus_count": signs.count(+1),
                "oriented_sign_minus_count": signs.count(-1),
                "naive_lift_vector_count": lifted.shape[1],
                "naive_lift_pt_residual": fmt(lift_pt),
                "naive_lift_containment_residual": fmt(containment),
                "naive_lift_relation_intersection_dim": inter.shape[1],
                "naive_lift_projected_rank": projected_rank,
                "principal_cosine_min": "" if principal.size == 0 else fmt(float(principal[-1])),
                "principal_cosine_max": "" if principal.size == 0 else fmt(float(principal[0])),
                "naive_lift_is_relation": containment < args.containment_tolerance and lift_pt < args.relation_verdict_tolerance,
            })

    # ------------------------------------------------------------------
    # Q2/Q3: genuine child relations under the physical global residue map.
    # A child fibre may scatter into several parent fibres. We therefore form
    # the residue in the complete parent ordering space and only afterward ask
    # which local parent relation directions lie in the global residue span.
    # ------------------------------------------------------------------
    global_full_images: List[np.ndarray] = []
    global_plus_images: List[np.ndarray] = []
    global_minus_images: List[np.ndarray] = []
    incoming_children_by_parent: MutableMapping[FibreKey, set] = defaultdict(set)
    child_operator_cache: Dict[
        FibreKey,
        Tuple[
            Dict[FibreKey, Tuple[np.ndarray, np.ndarray, np.ndarray]],
            np.ndarray,
            np.ndarray,
            np.ndarray,
        ],
    ] = {}

    for child_index, (child_key, child) in enumerate(child_fibres.items()):
        operator_map = build_child_residue_operator_map(base, child, parent_fibres, new_label)
        child_basis = child_record.bases[child_key].basis
        if not operator_map:
            child_residue_rows.append({
                "n_parent": n,
                "n_child": m,
                "child_key": base.key_text(child_key),
                "child_size": len(child),
                "child_relation_dim": child_basis.shape[1],
                "has_anchor_adjacent_new_label": False,
                "parent_fibre_count_reached": 0,
            })
            continue

        full_op, plus_op, minus_op = assemble_global_residue_operators(
            operator_map,
            parent_fibres,
            parent_global_index,
            parent_global_size,
            len(child),
        )
        child_operator_cache[child_key] = (operator_map, full_op, plus_op, minus_op)
        for parent_key in operator_map:
            incoming_children_by_parent[parent_key].add(child_key)

        full_image = full_op @ child_basis
        plus_image = plus_op @ child_basis
        minus_image = minus_op @ child_basis
        full_rank, full_sv = safe_rank(full_image, args.rank_tolerance, args.rank_absolute_tolerance)
        plus_rank, _ = safe_rank(plus_image, args.rank_tolerance, args.rank_absolute_tolerance)
        minus_rank, _ = safe_rank(minus_image, args.rank_tolerance, args.rank_absolute_tolerance)
        global_full_images.append(full_image)
        global_plus_images.append(plus_image)
        global_minus_images.append(minus_image)

        full_pt = pt_residual(
            base, parent_states, n, full_image,
            args.seed + 300_000 + 1000 * n + child_index,
            args.residue_validation_rows,
        )
        plus_pt = pt_residual(
            base, parent_states, n, plus_image,
            args.seed + 400_000 + 1000 * n + child_index,
            args.residue_validation_rows,
        )
        minus_pt = pt_residual(
            base, parent_states, n, minus_image,
            args.seed + 500_000 + 1000 * n + child_index,
            args.residue_validation_rows,
        )

        # Diagnostic only: local blocks need not separately be relations when
        # the global residue scatters across parent fibres.
        block_relation_count = 0
        block_pt_max = 0.0
        block_containment_max = 0.0
        for block_index, (parent_key, (full_block, _, _)) in enumerate(operator_map.items()):
            parent = parent_fibres[parent_key]
            parent_basis = parent_record.bases[parent_key].basis
            block_image = full_block @ child_basis
            block_pt = pt_residual(
                base, parent, n, block_image,
                args.seed + 550_000 + 10_000 * n + 100 * child_index + block_index,
                args.residue_validation_rows,
            )
            block_containment = max_subspace_residual(block_image, parent_basis)
            block_pt_max = max(block_pt_max, block_pt)
            block_containment_max = max(block_containment_max, block_containment)
            if block_pt < args.relation_verdict_tolerance and block_containment < args.containment_tolerance:
                block_relation_count += 1

        child_residue_rows.append({
            "n_parent": n,
            "n_child": m,
            "child_key": base.key_text(child_key),
            "parent_keys": ";".join(base.key_text(k) for k in operator_map),
            "parent_fibre_count_reached": len(operator_map),
            "child_size": len(child),
            "child_relation_dim": child_basis.shape[1],
            "has_anchor_adjacent_new_label": True,
            "global_full_residue_image_rank": full_rank,
            "global_full_residue_kernel_dim": child_basis.shape[1] - full_rank,
            "global_full_residue_pt_residual": fmt(full_pt),
            "global_plus_only_image_rank": plus_rank,
            "global_plus_only_pt_residual": fmt(plus_pt),
            "global_minus_only_image_rank": minus_rank,
            "global_minus_only_pt_residual": fmt(minus_pt),
            "local_block_count": len(operator_map),
            "local_blocks_individually_relational": block_relation_count,
            "max_local_block_pt_residual": fmt(block_pt_max),
            "max_local_block_containment_residual": fmt(block_containment_max),
            "smallest_nonzero_full_sv": "" if full_rank == 0 else fmt(float(full_sv[full_rank - 1])),
            "first_discarded_full_sv": "" if full_rank >= len(full_sv) else fmt(float(full_sv[full_rank])),
        })

    full_global_matrix = (
        np.hstack(global_full_images)
        if global_full_images
        else np.zeros((parent_global_size, 0), dtype=float)
    )
    plus_global_matrix = (
        np.hstack(global_plus_images)
        if global_plus_images
        else np.zeros((parent_global_size, 0), dtype=float)
    )
    minus_global_matrix = (
        np.hstack(global_minus_images)
        if global_minus_images
        else np.zeros((parent_global_size, 0), dtype=float)
    )
    full_q = orthonormal_span(full_global_matrix, args.rank_tolerance, args.rank_absolute_tolerance)
    plus_q = orthonormal_span(plus_global_matrix, args.rank_tolerance, args.rank_absolute_tolerance)
    minus_q = orthonormal_span(minus_global_matrix, args.rank_tolerance, args.rank_absolute_tolerance)
    global_full_rank = full_q.shape[1]
    global_plus_rank = plus_q.shape[1]
    global_minus_rank = minus_q.shape[1]
    relation_valid_q, relation_filter = relation_subspace_within_span(
        base,
        parent_states,
        n,
        full_q,
        args,
        args.seed + 605_000 + 1000 * n,
        args.seed + 610_000 + 1000 * n,
    )
    global_relation_valid_rank = relation_valid_q.shape[1]
    global_full_pt = float(relation_filter["raw_validation_residual"])
    global_relation_valid_pt = float(relation_filter["filtered_validation_residual"])

    # ------------------------------------------------------------------
    # Q2 aggregate: which local parent relation spaces are contained in the
    # complete global residue span after nonlocal components may cancel?
    # ------------------------------------------------------------------
    full_parent_count = 0
    for parent_index, (parent_key, parent) in enumerate(parent_fibres.items()):
        parent_basis = parent_record.bases[parent_key].basis
        parent_basis_global = embed_local_matrix(
            parent, parent_basis, parent_global_index, parent_global_size
        )
        full_inter, full_principal = intersection_basis(
            parent_basis_global, relation_valid_q, args.containment_tolerance
        )
        plus_inter, _ = intersection_basis(
            parent_basis_global, plus_q, args.containment_tolerance
        )
        minus_inter, _ = intersection_basis(
            parent_basis_global, minus_q, args.containment_tolerance
        )
        relation_dim = parent_basis.shape[1]
        inherited_rank = full_inter.shape[1]
        complete = inherited_rank == relation_dim
        full_parent_count += int(complete)
        parent_rows.append({
            "n_parent": n,
            "n_child": m,
            "parent_key": base.key_text(parent_key),
            "parent_size": len(parent),
            "parent_relation_dim": relation_dim,
            "incoming_child_fibre_count": len(incoming_children_by_parent.get(parent_key, set())),
            "global_raw_residue_span_rank": global_full_rank,
            "global_relation_valid_residue_span_rank": global_relation_valid_rank,
            "global_plus_residue_span_rank": global_plus_rank,
            "global_minus_residue_span_rank": global_minus_rank,
            "full_residue_inherited_rank": inherited_rank,
            "full_residue_missing_dim": relation_dim - inherited_rank,
            "plus_only_aggregate_rank": plus_inter.shape[1],
            "minus_only_aggregate_rank": minus_inter.shape[1],
            "parent_relation_residual_to_global_residue_span": fmt(
                max_subspace_residual(parent_basis_global, relation_valid_q)
            ),
            "global_raw_residue_pt_residual": fmt(global_full_pt),
            "global_relation_valid_residue_pt_residual": fmt(global_relation_valid_pt),
            "global_relation_filter_applied": relation_filter["filter_applied"],
            "smallest_parent_to_residue_principal_cosine": "" if full_principal.size == 0 else fmt(float(full_principal[-1])),
            "largest_parent_to_residue_principal_cosine": "" if full_principal.size == 0 else fmt(float(full_principal[0])),
            "complete_parent_inheritance": complete,
        })

    # ------------------------------------------------------------------
    # Q4: coefficient-inherited intersections and channel-new dimensions.
    # ------------------------------------------------------------------
    for child_key, child in child_fibres.items():
        child_basis = child_record.bases[child_key].basis
        lifted_blocks = insertion_blocks_by_child.get(child_key, [])
        lift_matrix = np.hstack(lifted_blocks) if lifted_blocks else np.zeros((len(child), 0), dtype=float)
        lift_q = orthonormal_span(lift_matrix, args.rank_tolerance, args.rank_absolute_tolerance)
        inter, principal = intersection_basis(child_basis, lift_q, args.containment_tolerance)
        if child_key in child_operator_cache:
            operator_map, full_op, _, _ = child_operator_cache[child_key]
            residue_image = full_op @ child_basis
            residue_rank, _ = safe_rank(residue_image, args.rank_tolerance, args.rank_absolute_tolerance)
            parent_count_reached = len(operator_map)
        else:
            residue_rank = 0
            parent_count_reached = 0
        child_birth_rows.append({
            "n_parent": n,
            "n_child": m,
            "child_key": base.key_text(child_key),
            "child_size": len(child),
            "child_relation_dim": child_basis.shape[1],
            "growth_parent_branch_count": len(lifted_blocks),
            "growth_parent_branches": ";".join(insertion_sources_by_child.get(child_key, [])),
            "residue_parent_fibre_count": parent_count_reached,
            "naive_insertion_ambient_rank": lift_q.shape[1],
            "coefficient_inherited_relation_dim": inter.shape[1],
            "coefficient_new_relation_dim": child_basis.shape[1] - inter.shape[1],
            "factorisation_residue_rank": residue_rank,
            "factorisation_kernel_dim": child_basis.shape[1] - residue_rank,
            "largest_principal_cosine": "" if principal.size == 0 else fmt(float(principal[0])),
            "smallest_principal_cosine": "" if principal.size == 0 else fmt(float(principal[-1])),
        })

    print(
        f"Transition {n}->{m}: raw global max-label residue span rank "
        f"{global_full_rank}/{parent_global_size}, PT residual {global_full_pt:.2e}."
    )
    print(
        f"Transition {n}->{m}: relation-valid residue span rank "
        f"{global_relation_valid_rank}/{parent_global_size}, PT residual {global_relation_valid_pt:.2e}."
    )
    print(
        f"Transition {n}->{m}: global residue span fully contains "
        f"{full_parent_count}/{len(parent_fibres)} parent local relation spaces."
    )
    naive_true = sum(
        bool(row["naive_lift_is_relation"])
        for row in insertion_rows
        if row["n_parent"] == n and row["n_child"] == m
    )
    branch_total = 2 * len(parent_fibres)
    print(
        f"Transition {n}->{m}: unchanged-coefficient insertion is a larger-n relation "
        f"for {naive_true}/{branch_total} parent-branch cases."
    )

    return {
        "branch_child_map": branch_child_map,
        "insertion_blocks_by_child": insertion_blocks_by_child,
        "child_operator_cache": child_operator_cache,
        "full_parent_count": full_parent_count,
        "parent_count": len(parent_fibres),
        "naive_relation_count": naive_true,
        "branch_count": branch_total,
        "global_raw_residue_span_rank": global_full_rank,
        "global_relation_valid_residue_span_rank": global_relation_valid_rank,
        "global_raw_residue_pt_residual": global_full_pt,
        "global_relation_valid_residue_pt_residual": global_relation_valid_pt,
        "global_relation_filter": relation_filter,
    }


def exceptional_missing_direction_audit(
    base,
    records: Mapping[int, BasisRecord],
    transition_results: Mapping[Tuple[int, int], Mapping[str, object]],
    args,
) -> Dict[str, object]:
    print("\n" + "=" * 100)
    print("EXCEPTIONAL n=8 RELATION: WAS THE AMP-18 MISSING DIRECTION BORN AT 7->8?")
    print("=" * 100)
    required = {7, 8, 9}
    if not required.issubset(records):
        return {"performed": False, "reason": "Requires relation bases for n=7,8,9."}

    rec7, rec8, rec9 = records[7], records[8], records[9]
    target_set = tuple(sorted(int(x) for x in args.exceptional_set.split(",") if x.strip()))
    star_key = None
    for key in rec8.fibres:
        anchor_set = key[0] if 1 in key[0] else key[1]
        if tuple(anchor_set) == target_set:
            star_key = key
            break
    if star_key is None:
        return {"performed": False, "reason": f"Exceptional fibre not found: {target_set}"}

    star = rec8.fibres[star_key]
    nstar = rec8.bases[star_key].basis
    target_indices = {
        key: {c: i for i, c in enumerate(chamber)}
        for key, chamber in rec8.fibres.items()
    }
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
    arrival_matrix = np.hstack(arrivals) if arrivals else np.zeros((len(star), 0), dtype=float)
    arrival_rank, arrival_sv = safe_rank(arrival_matrix, args.rank_tolerance, args.rank_absolute_tolerance)
    coords = nstar.T @ arrival_matrix
    u, s, _ = np.linalg.svd(coords, full_matrices=False)
    coord_rank = 0 if s.size == 0 or s[0] == 0 else int(
        np.count_nonzero(s > max(args.rank_absolute_tolerance, s[0] * args.rank_tolerance))
    )
    missing_dim = nstar.shape[1] - coord_rank
    if missing_dim != 1:
        return {
            "performed": False,
            "reason": f"Expected one-dimensional AMP-18 gap, found {missing_dim}.",
            "arrival_rank": arrival_rank,
            "coordinate_rank": coord_rank,
        }
    missing_local = nstar @ u[:, coord_rank:coord_rank + 1]
    missing_local /= np.linalg.norm(missing_local)

    operator_map = build_child_residue_operator_map(base, star, rec7.fibres, 8)
    if not operator_map:
        return {"performed": False, "reason": "Exceptional n=8 fibre has no anchor-adjacent label-8 states."}
    parent_states = base.canonical_cycles(7)
    parent_index = {c: i for i, c in enumerate(parent_states)}
    full_op, plus_op, minus_op = assemble_global_residue_operators(
        operator_map, rec7.fibres, parent_index, len(parent_states), len(star)
    )
    residue = full_op @ missing_local
    residue_plus = plus_op @ missing_local
    residue_minus = minus_op @ missing_local
    residue_norm = float(np.linalg.norm(residue))
    residue_pt = pt_residual(
        base, parent_states, 7, residue, args.seed + 880_001, args.residue_validation_rows
    )

    block_norms: Dict[str, str] = {}
    block_relation_residuals: Dict[str, Dict[str, str]] = {}
    for block_index, (parent_key, (full_block, _, _)) in enumerate(operator_map.items()):
        parent = rec7.fibres[parent_key]
        parent_basis = rec7.bases[parent_key].basis
        block_residue = full_block @ missing_local
        block_norms[base.key_text(parent_key)] = fmt(float(np.linalg.norm(block_residue)))
        block_relation_residuals[base.key_text(parent_key)] = {
            "pt_residual": fmt(pt_residual(
                base, parent, 7, block_residue,
                args.seed + 881_000 + block_index,
                args.residue_validation_rows,
            )),
            "containment_residual": fmt(max_subspace_residual(block_residue, parent_basis)),
        }

    restricted = full_op @ nstar
    rrank, rsv = safe_rank(restricted, args.rank_tolerance, args.rank_absolute_tolerance)
    _, _, vh = np.linalg.svd(restricted, full_matrices=True)
    kernel_coords = vh[rrank:].T if rrank < nstar.shape[1] else np.zeros((nstar.shape[1], 0), dtype=float)
    kernel_basis = nstar @ kernel_coords if kernel_coords.shape[1] else np.zeros((len(star), 0), dtype=float)
    missing_to_kernel = vector_residual(missing_local, kernel_basis)

    transition = transition_results.get((7, 8))
    lift_blocks = [] if transition is None else transition["insertion_blocks_by_child"].get(star_key, [])
    lift_matrix = np.hstack(lift_blocks) if lift_blocks else np.zeros((len(star), 0), dtype=float)
    lift_q = orthonormal_span(lift_matrix, args.rank_tolerance, args.rank_absolute_tolerance)
    inherited_intersection, principal = intersection_basis(nstar, lift_q, args.containment_tolerance)
    missing_to_raw_lift = vector_residual(missing_local, lift_q)
    missing_to_inherited_relation = vector_residual(missing_local, inherited_intersection)

    verdict = "UNRESOLVED"
    if missing_to_kernel < args.containment_tolerance and missing_to_inherited_relation > 1e-3:
        verdict = "CHANNEL_NEW_CANDIDATE"
    elif missing_to_inherited_relation < args.containment_tolerance:
        verdict = "COEFFICIENT_INHERITED"
    elif residue_norm > args.relation_verdict_tolerance:
        verdict = "RESIDUE_VISIBLE_NOT_NAIVELY_INHERITED"

    result = {
        "performed": True,
        "exceptional_key": base.key_text(star_key),
        "exceptional_relation_dim": nstar.shape[1],
        "amp18_arrival_rank": arrival_rank,
        "amp18_coordinate_rank": coord_rank,
        "amp18_missing_dim": missing_dim,
        "amp18_smallest_nonzero_sv": "" if arrival_rank == 0 else fmt(float(arrival_sv[arrival_rank - 1])),
        "amp18_first_discarded_sv": "" if arrival_rank >= len(arrival_sv) else fmt(float(arrival_sv[arrival_rank])),
        "growth_parent_keys_under_delete_8": [base.key_text(k) for k in operator_map],
        "growth_parent_fibre_count_under_delete_8": len(operator_map),
        "delete_8_restricted_global_rank": rrank,
        "delete_8_global_kernel_dim": nstar.shape[1] - rrank,
        "missing_direction_delete_8_global_residue_norm": fmt(residue_norm),
        "missing_direction_delete_8_plus_norm": fmt(float(np.linalg.norm(residue_plus))),
        "missing_direction_delete_8_minus_norm": fmt(float(np.linalg.norm(residue_minus))),
        "missing_direction_delete_8_global_pt_residual": fmt(residue_pt),
        "missing_direction_delete_8_parent_block_norms": block_norms,
        "missing_direction_delete_8_parent_block_relation_diagnostics": block_relation_residuals,
        "missing_direction_residual_to_delete_8_global_kernel": fmt(missing_to_kernel),
        "raw_insertion_span_rank_into_exceptional": lift_q.shape[1],
        "coefficient_inherited_relation_dim_into_exceptional": inherited_intersection.shape[1],
        "missing_direction_residual_to_raw_insertion_span": fmt(missing_to_raw_lift),
        "missing_direction_residual_to_coefficient_inherited_relation_space": fmt(missing_to_inherited_relation),
        "largest_insertion_relation_principal_cosine": "" if principal.size == 0 else fmt(float(principal[0])),
        "verdict": verdict,
        "interpretation_guardrail": (
            "'Channel-new' means invisible to the complete global max-label residue and outside the "
            "unchanged-coefficient insertion intersection. It is not an absolute claim that the relation "
            "has no origin under other charts, channels, or nontrivial lift maps."
        ),
    }

    print(f"Exceptional fibre:                    {result['exceptional_key']}")
    print(f"AMP-18 relation rank:                 {coord_rank}/{nstar.shape[1]}")
    print(f"Delete-8 parent fibres reached:       {len(operator_map)}")
    print(f"Delete-8 global rank on exceptional:  {rrank}/{nstar.shape[1]}")
    print(f"Missing vector global residue norm:   {residue_norm:.3e}")
    print(f"Missing vector residual to kernel:    {missing_to_kernel:.3e}")
    print(f"Inherited relation intersection:      {inherited_intersection.shape[1]}/{nstar.shape[1]}")
    print(f"Missing residual to inherited:        {missing_to_inherited_relation:.3e}")
    print(f"Guarded verdict:                      {verdict}")
    return result

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe relation-level compatibility of n-growth insertion and factorisation deletion.")
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--base-run-dir", required=True, help="Existing AMP-18 run directory; its cache is reused.")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--transitions", default="6:7,7:8,8:9")
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
    parser.add_argument("--exceptional-set", default="1,4,5,6")
    parser.add_argument("--exceptional-audit", dest="exceptional_audit", action="store_true", default=True)
    parser.add_argument("--no-exceptional-audit", dest="exceptional_audit", action="store_false")
    parser.add_argument("--force-rebuild", action="store_true")
    return parser.parse_args()


def run(args: argparse.Namespace) -> Dict[str, object]:
    started = time.time()
    base_script = Path(args.base_script).resolve()
    base_run_dir = Path(args.base_run_dir).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = base_run_dir / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    transitions = parse_transitions(args.transitions)
    needed_n = sorted({x for pair in transitions for x in pair})
    if args.exceptional_audit:
        needed_n = sorted(set(needed_n) | {7, 8, 9})

    base = load_base_module(base_script)

    print("=" * 100)
    print("EHF-AMP-FOUND-02A: GROWTH–FACTORISATION COMPATIBILITY")
    print("=" * 100)
    print(f"base script:                 {base_script}")
    print(f"shared cache:                {cache_dir}")
    print(f"output directory:            {out_dir}")
    print(f"transitions:                 {transitions}")
    print(f"seed:                        {args.seed}")
    print(f"exceptional audit:           {args.exceptional_audit}")
    print(f"rank tolerance:              {args.rank_tolerance}")
    print(f"containment tolerance:       {args.containment_tolerance}")

    basis_rows: List[Dict[str, object]] = []
    insertion_rows: List[Dict[str, object]] = []
    child_residue_rows: List[Dict[str, object]] = []
    parent_rows: List[Dict[str, object]] = []
    child_birth_rows: List[Dict[str, object]] = []

    records: Dict[int, BasisRecord] = {}
    for n in needed_n:
        records[n] = build_bases_for_n(base, n, cache_dir, args, basis_rows)

    transition_results: Dict[Tuple[int, int], Dict[str, object]] = {}
    for n, m in transitions:
        transition_results[(n, m)] = run_transition(
            base, n, m, records[n], records[m], args,
            insertion_rows, child_residue_rows, parent_rows, child_birth_rows,
        )

    exceptional = (
        exceptional_missing_direction_audit(base, records, transition_results, args)
        if args.exceptional_audit
        else {"performed": False, "reason": "Disabled by command line."}
    )

    write_csv(out_dir / "relation_basis_summary.csv", basis_rows)
    write_csv(out_dir / "insertion_branch_summary.csv", insertion_rows)
    write_csv(out_dir / "child_residue_summary.csv", child_residue_rows)
    write_csv(out_dir / "parent_inheritance_summary.csv", parent_rows)
    write_csv(out_dir / "child_relation_birth_summary.csv", child_birth_rows)
    with (out_dir / "exceptional_relation_audit.json").open("w") as handle:
        json.dump(json_safe(exceptional), handle, indent=2, sort_keys=True)

    transition_summary = []
    for (n, m), result in transition_results.items():
        transition_summary.append({
            "n_parent": n,
            "n_child": m,
            "complete_parent_inheritance_count": result["full_parent_count"],
            "parent_fibre_count": result["parent_count"],
            "naive_relation_branch_count": result["naive_relation_count"],
            "branch_count": result["branch_count"],
        })

    summary = {
        "script": Path(__file__).name,
        "transitions": transition_summary,
        "exceptional_audit": exceptional,
        "parameters": vars(args),
        "elapsed_seconds": time.time() - started,
        "output_files": [
            "relation_basis_summary.csv",
            "insertion_branch_summary.csv",
            "child_residue_summary.csv",
            "parent_inheritance_summary.csv",
            "child_relation_birth_summary.csv",
            "exceptional_relation_audit.json",
            "summary.json",
            "run.log",
        ],
    }
    with (out_dir / "summary.json").open("w") as handle:
        json.dump(json_safe(summary), handle, indent=2, sort_keys=True)

    print("\n" + "=" * 100)
    print("FINAL SUMMARY")
    print("=" * 100)
    for row in transition_summary:
        print(
            f"{row['n_parent']}->{row['n_child']}: parent inheritance "
            f"{row['complete_parent_inheritance_count']}/{row['parent_fibre_count']}; "
            f"naive relation lifts {row['naive_relation_branch_count']}/{row['branch_count']}"
        )
    if exceptional.get("performed"):
        print(f"Exceptional guarded verdict: {exceptional['verdict']}")
    else:
        print(f"Exceptional audit: not performed ({exceptional.get('reason', 'unknown reason')})")
    print(f"elapsed: {(time.time()-started)/60:.2f} minutes")
    print(f"summary: {out_dir / 'summary.json'}")
    print("=" * 100)
    return summary


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
            print(f"\n\n===== RUN START {time.strftime('%Y-%m-%d %H:%M:%S')} =====")
            run(args)
            print(f"===== RUN END {time.strftime('%Y-%m-%d %H:%M:%S')} =====")
            return 0
        except KeyboardInterrupt:
            print("\nInterrupted. Existing relation-basis caches remain reusable.")
            return 130
        except Exception as exc:
            print(f"\nERROR: {type(exc).__name__}: {exc}")
            import traceback
            traceback.print_exc()
            return 1
        finally:
            sys.stdout, sys.stderr = original_stdout, original_stderr


if __name__ == "__main__":
    raise SystemExit(main())
