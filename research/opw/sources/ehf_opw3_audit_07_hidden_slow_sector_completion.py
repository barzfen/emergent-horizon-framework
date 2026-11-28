#!/usr/bin/env python3
"""
EHF-OPW3-AUDIT-07
=================
Hidden Slow-Sector Families and Minimal Completion

Reconstructs OPW3 at n=7,9, identifies chambers whose exact LR3-signature
equitable quotient misses the full normalized-Laplacian gap, groups the misses
into repeated numerical families, and tests minimal refinements using:

  * LR3 square-incidence count;
  * n-2 ancestor chamber;
  * n-2 ancestor LR3 signature;
  * n-2 ancestor exact packet cell;
  * square count plus ancestor packet cell.

It also diagnoses any OPW23 chamber where LR3-, LR2-, and joint-signature
equitable closures differ.

Structural diffusion only: no particle, mass, energy, or quantum claim.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import statistics
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
from typing import Dict, Hashable, List, Sequence, Set, Tuple

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh

SCRIPT_VERSION = "ehf_opw3_audit_07_2026-07-24"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_int_csv(text: str) -> List[int]:
    out = [int(x.strip()) for x in text.split(",") if x.strip()]
    if not out:
        raise argparse.ArgumentTypeError("expected at least one integer")
    return out


def load_base(path: Path):
    spec = importlib.util.spec_from_file_location("ehf_opw3_audit_01_base", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load base script: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_csv(path: Path, rows: Sequence[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def connected_components(adjacency: Sequence[Set[int]]):
    seen: Set[int] = set()
    comps: List[List[int]] = []
    component_of: Dict[int, int] = {}
    for start in range(len(adjacency)):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        comp: List[int] = []
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in adjacency[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        comp.sort()
        comps.append(comp)
    comps.sort(key=lambda c: (-len(c), c[0]))
    for cid, comp in enumerate(comps):
        for state in comp:
            component_of[state] = cid
    return comps, component_of


def local_graph(global_adjacency: Sequence[Set[int]], vertices: Sequence[int]):
    index = {state: i for i, state in enumerate(vertices)}
    return [
        sorted(index[v] for v in global_adjacency[state] if v in index)
        for state in vertices
    ]


def encode(values: Sequence[Hashable]) -> List[int]:
    unique = sorted(set(values), key=repr)
    mapping = {value: i for i, value in enumerate(unique)}
    return [mapping[value] for value in values]


def equitable_refinement(
    adjacency: Sequence[Sequence[int]],
    initial_values: Sequence[Hashable],
) -> List[int]:
    colors = encode(initial_values)
    while True:
        keys = []
        for u, neighbours in enumerate(adjacency):
            hist = Counter(colors[v] for v in neighbours)
            keys.append((colors[u], tuple(sorted(hist.items()))))
        unique = sorted(set(keys), key=repr)
        mapping = {key: i for i, key in enumerate(unique)}
        new_colors = [mapping[key] for key in keys]
        if new_colors == colors:
            return colors
        if len(set(new_colors)) == len(set(colors)):
            return new_colors
        colors = new_colors


def partition_key(colors: Sequence[int], vertices: Sequence[int]):
    cells: Dict[int, List[int]] = defaultdict(list)
    for local_state, color in enumerate(colors):
        cells[color].append(vertices[local_state])
    return {frozenset(cell) for cell in cells.values()}


def quotient_chain(adjacency: Sequence[Sequence[int]], colors: Sequence[int]):
    cells = sorted(set(colors))
    pos = {cell: i for i, cell in enumerate(cells)}
    members: Dict[int, List[int]] = defaultdict(list)
    for u, color in enumerate(colors):
        members[color].append(u)

    q = len(cells)
    counts = np.zeros((q, q), dtype=float)
    degree = np.zeros(q, dtype=float)
    size = np.zeros(q, dtype=float)

    for cell in cells:
        i = pos[cell]
        reps = members[cell]
        size[i] = len(reps)
        reference = None
        for u in reps:
            row = np.zeros(q, dtype=float)
            for v in adjacency[u]:
                row[pos[colors[v]]] += 1.0
            if reference is None:
                reference = row
            elif not np.array_equal(reference, row):
                raise RuntimeError("partition is not equitable")
        counts[i] = reference
        degree[i] = reference.sum()

    if q == 1 and degree[0] == 0:
        return np.array([[1.0]]), np.array([1.0])

    p = np.divide(
        counts,
        degree[:, None],
        out=np.zeros_like(counts),
        where=degree[:, None] > 0,
    )
    volume = float(np.dot(size, degree))
    pi = size * degree / volume
    return p, pi


def quotient_spectrum(p: np.ndarray, pi: np.ndarray) -> np.ndarray:
    if p.shape[0] == 1:
        return np.array([0.0])
    root = np.sqrt(pi)
    s = np.divide(
        root[:, None] * p,
        root[None, :],
        out=np.zeros_like(p),
        where=root[None, :] > 0,
    )
    s = 0.5 * (s + s.T)
    mu = np.linalg.eigvalsh(s)
    lam = np.sort(1.0 - mu)
    lam[np.abs(lam) < 1e-11] = 0.0
    return lam


def normalized_modes(
    adjacency: Sequence[Sequence[int]],
    count: int,
    dense_cutoff: int,
    tolerance: float,
):
    n = len(adjacency)
    degree = np.array([len(row) for row in adjacency], dtype=float)
    if n == 1:
        return np.array([0.0]), np.array([[1.0]]), degree

    rows, cols = [], []
    for u, neighbours in enumerate(adjacency):
        for v in neighbours:
            rows.append(u)
            cols.append(v)
    a = sparse.csr_matrix(
        (np.ones(len(rows)), (rows, cols)),
        shape=(n, n),
        dtype=float,
    )
    inv = 1.0 / np.sqrt(degree)
    s = sparse.diags(inv) @ a @ sparse.diags(inv)

    requested = min(max(3, count), n)
    if n <= dense_cutoff or requested >= n:
        mu, vectors = np.linalg.eigh(s.toarray())
        order = np.argsort(mu)[::-1]
        mu = mu[order][:requested]
        vectors = vectors[:, order][:, :requested]
    else:
        k = min(requested, n - 1)
        mu, vectors = eigsh(
            s,
            k=k,
            which="LA",
            tol=tolerance,
            maxiter=max(5000, 100 * n),
        )
        order = np.argsort(mu)[::-1]
        mu = mu[order]
        vectors = vectors[:, order]

    lam = 1.0 - mu
    order = np.argsort(lam)
    lam = lam[order]
    vectors = vectors[:, order]
    lam[np.abs(lam) < 10 * tolerance] = 0.0
    return lam, vectors, degree


def quotient_basis(colors: Sequence[int], degree: np.ndarray) -> np.ndarray:
    columns = []
    for cell in sorted(set(colors)):
        vector = np.zeros(len(colors), dtype=float)
        members = [i for i, color in enumerate(colors) if color == cell]
        vector[members] = np.sqrt(degree[members])
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector /= norm
        columns.append(vector)
    return np.column_stack(columns)


def projection_mass(basis: np.ndarray, modes: np.ndarray) -> float:
    return float(np.linalg.norm(basis.T @ modes, ord="fro") ** 2 / modes.shape[1])


def square_incidence(adjacency: Sequence[Set[int]]):
    squares: Set[frozenset[int]] = set()
    for u, neighbour_set in enumerate(adjacency):
        for a, b in combinations(sorted(neighbour_set), 2):
            for x in adjacency[a].intersection(adjacency[b]):
                if x != u:
                    square = frozenset((u, a, b, x))
                    if len(square) == 4:
                        squares.add(square)
    incidence = [0] * len(adjacency)
    for square in squares:
        for vertex in square:
            incidence[vertex] += 1
    return incidence, len(squares)


def source_packet_labels(
    source_components: Sequence[Sequence[int]],
    source_adjacency: Sequence[Set[int]],
    source_signatures: Sequence[Hashable],
):
    labels: List[Tuple[int, int] | None] = [None] * len(source_adjacency)
    for cid, vertices in enumerate(source_components):
        local = local_graph(source_adjacency, vertices)
        colors = equitable_refinement(
            local,
            [source_signatures[state] for state in vertices],
        )
        for local_state, state in enumerate(vertices):
            labels[state] = (cid, colors[local_state])
    if any(label is None for label in labels):
        raise RuntimeError("source packet labels incomplete")
    return labels


def pi_text(label) -> str:
    return "|".join(",".join(str(x) for x in side) for side in label)


def action_entropy(p: np.ndarray, pi: np.ndarray) -> float:
    support = p > 0
    return float(np.sum((pi[:, None] * p)[support] * (-np.log(p[support]))))


def fingerprint(row: dict) -> str:
    return json.dumps([
        row["component_states"],
        row["quotient_cells"],
        round(row["full_normalized_gap"], 9),
        round(row["quotient_normalized_gap"], 9),
        round(row["entropy_rate_mean_action"], 9),
    ], separators=(",", ":"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit hidden OPW3 slow-sector families and minimal completions."
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--ns", type=parse_int_csv, default=[7, 9])
    parser.add_argument("--dense-cutoff", type=int, default=180)
    parser.add_argument("--eigen-tolerance", type=float, default=1e-10)
    parser.add_argument("--gap-match-tolerance", type=float, default=1e-7)
    parser.add_argument("--multiplicity-tolerance", type=float, default=1e-7)
    parser.add_argument("--out-dir", default="runs/ehf_opw3_audit_07")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    base_path = Path(args.base_script).resolve()
    base = load_base(base_path)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 122)
    print("EHF-OPW3-AUDIT-07: HIDDEN SLOW-SECTOR FAMILIES AND MINIMAL COMPLETION")
    print("=" * 122)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"base engine:          {base_path}")
    print(f"n values:             {args.ns}")
    print(f"output directory:     {out_dir.resolve()}")
    print(f"strict:               {args.strict}")
    print()

    checks: Dict[str, bool] = {}
    hidden_rows: List[dict] = []
    completion_rows: List[dict] = []
    family_rows: List[dict] = []
    exception_rows: List[dict] = []
    summaries: Dict[str, dict] = {}
    started_all = time.perf_counter()

    for n in args.ns:
        started = time.perf_counter()
        cycles = base.generate_cycles(n)
        index = {cycle: i for i, cycle in enumerate(cycles)}
        labels = [base.pi_label(cycle) for cycle in cycles]

        builds = {
            name: base.build_preserve_graph(
                cycles, index, labels, name, base.GRAPH_LENGTHS[name]
            )
            for name in ("OPW3", "LR2", "OPW23")
        }
        opw3_components, _ = connected_components(builds["OPW3"].adjacency)
        opw23_components, _ = connected_components(builds["OPW23"].adjacency)
        lr3_sig = builds["OPW3"].accepted_slots
        lr2_sig = builds["LR2"].accepted_slots

        square_count, square_total = square_incidence(builds["OPW3"].adjacency)
        checks[f"n{n}_square_count"] = square_total > 0

        source_n = n - 2
        source_cycles = base.generate_cycles(source_n)
        source_index = {cycle: i for i, cycle in enumerate(source_cycles)}
        source_labels_pi = [base.pi_label(cycle) for cycle in source_cycles]
        source_build = base.build_preserve_graph(
            source_cycles,
            source_index,
            source_labels_pi,
            "OPW3",
            base.GRAPH_LENGTHS["OPW3"],
        )
        source_components, source_component_of = connected_components(
            source_build.adjacency
        )
        source_packet = source_packet_labels(
            source_components,
            source_build.adjacency,
            source_build.accepted_slots,
        )

        parent_state = []
        for cycle in cycles:
            reduced = base.canonical_cycle(
                [label for label in cycle if label < source_n]
            )
            parent_state.append(source_index[reduced])

        print(
            f"[n={n}] states={len(cycles)} components={len(opw3_components)} "
            f"squares={square_total}"
        )

        hidden_ids = []
        for cid, vertices in enumerate(opw3_components):
            local = local_graph(builds["OPW3"].adjacency, vertices)
            baseline_values = [lr3_sig[state] for state in vertices]
            baseline_colors = equitable_refinement(local, baseline_values)
            p, pi = quotient_chain(local, baseline_colors)
            qspec = quotient_spectrum(p, pi)

            lam, vectors, degree = normalized_modes(
                local,
                count=8,
                dense_cutoff=args.dense_cutoff,
                tolerance=args.eigen_tolerance,
            )
            full_gap = float(lam[1])
            quotient_cells = len(set(baseline_colors))
            quotient_gap = float(qspec[1]) if quotient_cells > 1 else 0.0

            hidden = (
                quotient_cells > 1
                and quotient_gap - full_gap > args.gap_match_tolerance
            )
            if not hidden:
                continue

            hidden_ids.append(cid)
            mode_indices = [
                i for i in range(1, len(lam))
                if abs(float(lam[i]) - full_gap)
                <= args.multiplicity_tolerance
            ]
            modes = vectors[:, mode_indices]
            qbasis = quotient_basis(baseline_colors, degree)
            packet_mass = projection_mass(qbasis, modes)
            checks[f"n{n}_c{cid}_hidden_orthogonal"] = packet_mass <= 1e-6

            vertex_energy = np.sum(modes ** 2, axis=1) / modes.shape[1]
            cell_energy = []
            for cell in sorted(set(baseline_colors)):
                members = [
                    u for u, color in enumerate(baseline_colors)
                    if color == cell
                ]
                cell_energy.append(float(vertex_energy[members].sum()))
            positive = np.array([x for x in cell_energy if x > 0])

            square_values = [square_count[state] for state in vertices]
            parent_component_values = [
                source_component_of[parent_state[state]] for state in vertices
            ]
            parent_signature_values = [
                source_build.accepted_slots[parent_state[state]]
                for state in vertices
            ]
            parent_packet_values = [
                source_packet[parent_state[state]] for state in vertices
            ]

            row = {
                "n": n,
                "component_id": cid,
                "pi_label": pi_text(labels[vertices[0]]),
                "component_states": len(vertices),
                "quotient_cells": quotient_cells,
                "full_normalized_gap": full_gap,
                "quotient_normalized_gap": quotient_gap,
                "gap_ratio_quotient_over_full": quotient_gap / full_gap,
                "lowest_gap_multiplicity_retained": len(mode_indices),
                "packet_projection_mass_of_hidden_eigenspace": packet_mass,
                "max_packet_cell_energy_share": max(cell_energy),
                "packet_cell_energy_entropy": float(
                    -np.sum(positive * np.log(positive))
                ),
                "mean_inverse_participation_ratio": float(
                    np.mean(np.sum(modes ** 4, axis=0))
                ),
                "square_count_min": min(square_values),
                "square_count_max": max(square_values),
                "square_count_distinct": len(set(square_values)),
                "parent_components_realized": len(set(parent_component_values)),
                "parent_signatures_realized": len(set(parent_signature_values)),
                "parent_packets_realized": len(set(parent_packet_values)),
                "entropy_rate_mean_action": action_entropy(p, pi),
            }
            row["family_key"] = fingerprint(row)
            hidden_rows.append(row)

            candidates = {
                "LR3_BASELINE": baseline_values,
                "LR3_PLUS_SQUARE_COUNT": [
                    (baseline_values[i], square_values[i])
                    for i in range(len(vertices))
                ],
                "LR3_PLUS_PARENT_COMPONENT": [
                    (baseline_values[i], parent_component_values[i])
                    for i in range(len(vertices))
                ],
                "LR3_PLUS_PARENT_SIGNATURE": [
                    (baseline_values[i], parent_signature_values[i])
                    for i in range(len(vertices))
                ],
                "LR3_PLUS_PARENT_PACKET": [
                    (baseline_values[i], parent_packet_values[i])
                    for i in range(len(vertices))
                ],
                "LR3_PLUS_SQUARE_AND_PARENT_PACKET": [
                    (
                        baseline_values[i],
                        square_values[i],
                        parent_packet_values[i],
                    )
                    for i in range(len(vertices))
                ],
            }

            for name, values in candidates.items():
                colors = equitable_refinement(local, values)
                cp, cpi = quotient_chain(local, colors)
                cspec = quotient_spectrum(cp, cpi)
                cells = len(set(colors))
                gap = float(cspec[1]) if cells > 1 else 0.0
                visible = (
                    cells > 1
                    and abs(gap - full_gap) <= args.gap_match_tolerance
                )
                completion_rows.append({
                    "n": n,
                    "component_id": cid,
                    "pi_label": row["pi_label"],
                    "component_states": len(vertices),
                    "candidate": name,
                    "initial_labels_realized": len(set(values)),
                    "final_cells": cells,
                    "compression_ratio": cells / len(vertices),
                    "full_normalized_gap": full_gap,
                    "candidate_quotient_gap": gap,
                    "gap_ratio_candidate_over_full": gap / full_gap,
                    "slowest_mode_visible": visible,
                    "additional_cells_over_baseline": cells - quotient_cells,
                })

        families: Dict[str, List[dict]] = defaultdict(list)
        for row in hidden_rows:
            if row["n"] == n:
                families[row["family_key"]].append(row)
        for family_id, (key, rows) in enumerate(
            sorted(families.items(), key=lambda item: item[0])
        ):
            family_rows.append({
                "n": n,
                "family_id": family_id,
                "family_key": key,
                "members": len(rows),
                "component_ids": json.dumps(
                    sorted(row["component_id"] for row in rows)
                ),
                "pi_labels": json.dumps(
                    sorted(row["pi_label"] for row in rows)
                ),
                "component_states": rows[0]["component_states"],
                "quotient_cells": rows[0]["quotient_cells"],
                "full_normalized_gap": rows[0]["full_normalized_gap"],
                "quotient_normalized_gap": rows[0]["quotient_normalized_gap"],
                "gap_ratio": rows[0]["gap_ratio_quotient_over_full"],
            })

        # Diagnose OPW23 signature-closure exceptions.
        for cid, vertices in enumerate(opw23_components):
            local = local_graph(builds["OPW23"].adjacency, vertices)
            closures = {
                "LR3": equitable_refinement(
                    local, [lr3_sig[state] for state in vertices]
                ),
                "LR2": equitable_refinement(
                    local, [lr2_sig[state] for state in vertices]
                ),
                "JOINT": equitable_refinement(
                    local,
                    [(lr3_sig[state], lr2_sig[state]) for state in vertices],
                ),
            }
            parts = {
                name: partition_key(colors, vertices)
                for name, colors in closures.items()
            }
            if parts["LR3"] == parts["LR2"] == parts["JOINT"]:
                continue

            def intersection_profile(left, right):
                return dict(sorted(Counter(
                    sum(bool(a & b) for b in right) for a in left
                ).items()))

            exception_rows.append({
                "n": n,
                "graph": "OPW23",
                "component_id": cid,
                "pi_label": pi_text(labels[vertices[0]]),
                "component_states": len(vertices),
                "lr3_cells": len(parts["LR3"]),
                "lr2_cells": len(parts["LR2"]),
                "joint_cells": len(parts["JOINT"]),
                "lr3_equals_joint": parts["LR3"] == parts["JOINT"],
                "lr2_equals_joint": parts["LR2"] == parts["JOINT"],
                "lr3_to_lr2_intersection_profile": json.dumps(
                    intersection_profile(parts["LR3"], parts["LR2"])
                ),
                "lr2_to_lr3_intersection_profile": json.dumps(
                    intersection_profile(parts["LR2"], parts["LR3"])
                ),
                "same_vertex_set_hidden_in_OPW3": any(
                    frozenset(vertices) == frozenset(opw3_components[hid])
                    for hid in hidden_ids
                ),
            })

        completion_here = [row for row in completion_rows if row["n"] == n]
        candidate_summary = {}
        for candidate in sorted({row["candidate"] for row in completion_here}):
            rows = [row for row in completion_here if row["candidate"] == candidate]
            visible = [row for row in rows if row["slowest_mode_visible"]]
            total_states = sum(row["component_states"] for row in rows)
            visible_states = sum(row["component_states"] for row in visible)
            candidate_summary[candidate] = {
                "recovered": len(visible),
                "total": len(rows),
                "state_weighted_recovery_fraction": (
                    visible_states / total_states if total_states else None
                ),
                "mean_compression_ratio": (
                    statistics.fmean(row["compression_ratio"] for row in rows)
                    if rows else None
                ),
            }

        summaries[f"n{n}"] = {
            "states": len(cycles),
            "hidden_components": len(hidden_ids),
            "hidden_component_ids": hidden_ids,
            "fingerprint_families": len(families),
            "opw23_closure_exceptions": sum(
                row["n"] == n for row in exception_rows
            ),
            "completion_candidates": candidate_summary,
            "elapsed_seconds": time.perf_counter() - started,
        }

        print(
            f"  hidden={len(hidden_ids)} families={len(families)} "
            f"OPW23-exceptions={summaries[f'n{n}']['opw23_closure_exceptions']}"
        )
        for candidate, result in candidate_summary.items():
            print(
                f"    {candidate:<34} "
                f"recovered={result['recovered']}/{result['total']} "
                f"state-weighted={result['state_weighted_recovery_fraction']:.6f} "
                f"mean-compression={result['mean_compression_ratio']:.6f}"
            )
        print(f"  elapsed={summaries[f'n{n}']['elapsed_seconds']:.2f}s")
        print()

    write_csv(out_dir / "hidden_slow_sector_summary.csv", hidden_rows)
    write_csv(out_dir / "completion_candidate_summary.csv", completion_rows)
    write_csv(out_dir / "hidden_family_summary.csv", family_rows)
    write_csv(out_dir / "opw23_closure_exception_summary.csv", exception_rows)

    strict_pass = all(checks.values())
    summary = {
        "probe": "EHF-OPW3-AUDIT-07",
        "title": "Hidden Slow-Sector Families and Minimal Completion",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "arguments": vars(args),
        "base_script": str(base_path),
        "checks": checks,
        "strict_pass": strict_pass,
        "summaries": summaries,
        "guardrail": (
            "Hidden modes are normalized-Laplacian diffusion modes. "
            "A successful completion only means additional relational data make "
            "the mode visible to an exact quotient."
        ),
        "elapsed_seconds": time.perf_counter() - started_all,
        "verdict": (
            "EHF_OPW3_AUDIT_07_HIDDEN_SLOW_COMPLETION_PASS"
            if strict_pass else
            "EHF_OPW3_AUDIT_07_HIDDEN_SLOW_COMPLETION_FAIL"
        ),
    }
    with (out_dir / "run_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)

    print("=" * 122)
    print(f"strict checks:        {sum(checks.values())}/{len(checks)}")
    print(f"verdict:              {summary['verdict']}")
    print(f"elapsed:              {summary['elapsed_seconds']:.2f}s")
    print("=" * 122)

    if args.strict and not strict_pass:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
