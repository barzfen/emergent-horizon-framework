#!/usr/bin/env python3
"""
EHF-OPW3-AUDIT-08
=================
Residual Hidden-Sector Completion by LR3 Edge Labels and Growth History

Targets only OPW3 chambers whose slowest normalized-Laplacian mode remains
hidden after the Audit-07 parent-signature completion.

Candidate exact refinements:
  * baseline LR3 packet closure;
  * parent LR3 signature;
  * exact n-2 insertion descriptor;
  * parent signature plus insertion descriptor;
  * two-level growth history;
  * LR3 edge-labelled colour refinement;
  * LR3 edge-labelled refinement seeded by parent signature;
  * oriented LR3 square-incidence profile.

No physical particle or quantum interpretation is made.
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
from typing import Dict, Hashable, List, Mapping, Sequence, Set, Tuple

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh

SCRIPT_VERSION = "ehf_opw3_audit_08_2026-07-24"
Cycle = Tuple[int, ...]
Descriptor = Tuple[int, int]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_int_csv(text: str) -> List[int]:
    vals = [int(x.strip()) for x in text.split(",") if x.strip()]
    if not vals:
        raise argparse.ArgumentTypeError("expected integers")
    return vals


def load_base(path: Path):
    spec = importlib.util.spec_from_file_location("ehf_opw3_audit_01_base", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_csv(path: Path, rows: Sequence[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


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
    local = [
        sorted(index[v] for v in global_adjacency[state] if v in index)
        for state in vertices
    ]
    return local, index


def encode(values: Sequence[Hashable]) -> List[int]:
    uniq = sorted(set(values), key=repr)
    m = {v: i for i, v in enumerate(uniq)}
    return [m[v] for v in values]


def equitable_refinement(adjacency, initial_values):
    colors = encode(initial_values)
    while True:
        keys = []
        for u, nbrs in enumerate(adjacency):
            hist = Counter(colors[v] for v in nbrs)
            keys.append((colors[u], tuple(sorted(hist.items()))))
        uniq = sorted(set(keys), key=repr)
        m = {k: i for i, k in enumerate(uniq)}
        new = [m[k] for k in keys]
        if new == colors or len(set(new)) == len(set(colors)):
            return new
        colors = new


def labelled_refinement(labelled_adjacency, initial_values):
    colors = encode(initial_values)
    while True:
        keys = []
        for u, labelled_nbrs in enumerate(labelled_adjacency):
            signature = tuple(sorted((label, colors[v]) for label, v in labelled_nbrs))
            keys.append((colors[u], signature))
        uniq = sorted(set(keys), key=repr)
        m = {k: i for i, k in enumerate(uniq)}
        new = [m[k] for k in keys]
        if new == colors or len(set(new)) == len(set(colors)):
            return new
        colors = new


def quotient_chain(adjacency, colors):
    cells = sorted(set(colors))
    pos = {c: i for i, c in enumerate(cells)}
    members = defaultdict(list)
    for u, c in enumerate(colors):
        members[c].append(u)
    q = len(cells)
    counts = np.zeros((q, q), dtype=float)
    degrees = np.zeros(q, dtype=float)
    sizes = np.zeros(q, dtype=float)
    for c in cells:
        i = pos[c]
        reps = members[c]
        sizes[i] = len(reps)
        ref = None
        for u in reps:
            row = np.zeros(q, dtype=float)
            for v in adjacency[u]:
                row[pos[colors[v]]] += 1
            if ref is None:
                ref = row
            elif not np.array_equal(ref, row):
                raise RuntimeError("partition not equitable")
        counts[i] = ref
        degrees[i] = ref.sum()
    if q == 1 and degrees[0] == 0:
        return np.array([[1.0]]), np.array([1.0])
    p = np.divide(counts, degrees[:, None], out=np.zeros_like(counts), where=degrees[:, None] > 0)
    volume = float(np.dot(sizes, degrees))
    pi = sizes * degrees / volume
    return p, pi


def quotient_gap(adjacency, colors):
    p, pi = quotient_chain(adjacency, colors)
    if p.shape[0] <= 1:
        return 0.0
    root = np.sqrt(pi)
    s = np.divide(root[:, None] * p, root[None, :], out=np.zeros_like(p), where=root[None, :] > 0)
    s = 0.5 * (s + s.T)
    mu = np.linalg.eigvalsh(s)
    lam = np.sort(1.0 - mu)
    lam[np.abs(lam) < 1e-11] = 0
    return float(lam[1])


def full_gap(adjacency, dense_cutoff, tol):
    n = len(adjacency)
    rows, cols = [], []
    degree = np.array([len(r) for r in adjacency], dtype=float)
    for u, nbrs in enumerate(adjacency):
        for v in nbrs:
            rows.append(u)
            cols.append(v)
    a = sparse.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
    inv = 1.0 / np.sqrt(degree)
    s = sparse.diags(inv) @ a @ sparse.diags(inv)
    if n <= dense_cutoff:
        mu = np.linalg.eigvalsh(s.toarray())
        mu = np.sort(mu)[::-1]
    else:
        mu = eigsh(s, k=2, which="LA", tol=tol, return_eigenvectors=False)
        mu = np.sort(mu)[::-1]
    return float(max(0.0, 1.0 - mu[1]))


def insert_after_gap(cycle, gap, label):
    arr = list(cycle)
    arr.insert(gap + 1, label)
    return tuple(arr)


def growth_map(base, source_n, source_cycles, target_index):
    parent = [-1] * len(target_index)
    descriptor: List[Descriptor | None] = [None] * len(target_index)
    for sid, source in enumerate(source_cycles):
        for g1 in range(source_n):
            mid = insert_after_gap(source, g1, source_n)
            for g2 in range(source_n + 1):
                child = base.canonical_cycle(insert_after_gap(mid, g2, source_n + 1))
                tid = target_index[child]
                if parent[tid] != -1:
                    raise RuntimeError("duplicate growth child")
                parent[tid] = sid
                descriptor[tid] = (g1, g2)
    if any(x < 0 for x in parent) or any(x is None for x in descriptor):
        raise RuntimeError("incomplete growth map")
    return parent, descriptor


def source_packet_labels(source_components, source_adjacency, source_signatures):
    labels = [None] * len(source_adjacency)
    for cid, vertices in enumerate(source_components):
        local, _ = local_graph(source_adjacency, vertices)
        colors = equitable_refinement(local, [source_signatures[s] for s in vertices])
        for i, state in enumerate(vertices):
            labels[state] = (cid, colors[i])
    return labels


def global_labelled_lr3(base, cycles, index, pi_labels):
    labelled: List[List[Tuple[int, int]]] = [[] for _ in cycles]
    for i, cycle in enumerate(cycles):
        seen = {}
        for slot in range(len(cycle)):
            target = base.circular_reverse(cycle, slot, 3)
            j = index[target]
            if j != i and pi_labels[j] == pi_labels[i]:
                if j in seen:
                    raise RuntimeError("duplicate LR3 move image")
                seen[j] = slot
                labelled[i].append((slot, j))
        labelled[i].sort()
    return labelled


def local_labelled(global_labelled, vertices, index):
    return [
        sorted((slot, index[v]) for slot, v in global_labelled[state] if v in index)
        for state in vertices
    ]


def oriented_square_profiles(global_adjacency, global_labelled):
    edge_label = []
    for u, rows in enumerate(global_labelled):
        edge_label.append({v: slot for slot, v in rows})
    squares: Set[frozenset[int]] = set()
    for u, nbrs in enumerate(global_adjacency):
        for a, b in combinations(sorted(nbrs), 2):
            for x in global_adjacency[a].intersection(global_adjacency[b]):
                if x != u:
                    sq = frozenset((u, a, b, x))
                    if len(sq) == 4:
                        squares.add(sq)
    profiles = [Counter() for _ in global_adjacency]
    for sq in squares:
        verts = list(sq)
        for u in verts:
            inside = [v for v in global_adjacency[u] if v in sq]
            if len(inside) != 2:
                continue
            pair = tuple(sorted((edge_label[u][inside[0]], edge_label[u][inside[1]])))
            profiles[u][pair] += 1
    return [tuple(sorted(p.items())) for p in profiles], len(squares)


def pi_text(label):
    return "|".join(",".join(str(x) for x in side) for side in label)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-script", required=True)
    ap.add_argument("--ns", type=parse_int_csv, default=[7, 9])
    ap.add_argument("--dense-cutoff", type=int, default=180)
    ap.add_argument("--eigen-tolerance", type=float, default=1e-10)
    ap.add_argument("--gap-match-tolerance", type=float, default=1e-7)
    ap.add_argument("--out-dir", default="runs/ehf_opw3_audit_08")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    base_path = Path(args.base_script).resolve()
    base = load_base(base_path)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 122)
    print("EHF-OPW3-AUDIT-08: RESIDUAL COMPLETION BY LR3 EDGE LABELS AND GROWTH HISTORY")
    print("=" * 122)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"base engine:          {base_path}")
    print(f"n values:             {args.ns}")
    print(f"output directory:     {out_dir.resolve()}")
    print(f"strict:               {args.strict}")
    print()

    checks = {}
    rows = []
    summaries = {}
    started_all = time.perf_counter()

    for n in args.ns:
        started = time.perf_counter()
        cycles = base.generate_cycles(n)
        index = {c: i for i, c in enumerate(cycles)}
        pi_labels = [base.pi_label(c) for c in cycles]
        build = base.build_preserve_graph(cycles, index, pi_labels, "OPW3", base.GRAPH_LENGTHS["OPW3"])
        comps, _ = connected_components(build.adjacency)
        global_labelled = global_labelled_lr3(base, cycles, index, pi_labels)
        square_profile, square_total = oriented_square_profiles(build.adjacency, global_labelled)

        source_n = n - 2
        source_cycles = base.generate_cycles(source_n)
        source_index = {c: i for i, c in enumerate(source_cycles)}
        source_pi = [base.pi_label(c) for c in source_cycles]
        source_build = base.build_preserve_graph(source_cycles, source_index, source_pi, "OPW3", base.GRAPH_LENGTHS["OPW3"])
        source_comps, source_component_of = connected_components(source_build.adjacency)
        source_packets = source_packet_labels(source_comps, source_build.adjacency, source_build.accepted_slots)
        parent, descriptor = growth_map(base, source_n, source_cycles, index)

        # Grandparent history for the parent states.
        grand_n = source_n - 2
        grand_cycles = base.generate_cycles(grand_n)
        grand_index = {c: i for i, c in enumerate(grand_cycles)}
        grand_pi = [base.pi_label(c) for c in grand_cycles]
        grand_build = base.build_preserve_graph(grand_cycles, grand_index, grand_pi, "OPW3", base.GRAPH_LENGTHS["OPW3"])
        grand_comps, grand_component_of = connected_components(grand_build.adjacency)
        grand_packets = source_packet_labels(grand_comps, grand_build.adjacency, grand_build.accepted_slots)
        parent_of_source, descriptor_source = growth_map(base, grand_n, grand_cycles, source_index)

        residual = []
        print(f"[n={n}] states={len(cycles)} components={len(comps)} squares={square_total}")

        for cid, vertices in enumerate(comps):
            local, local_index = local_graph(build.adjacency, vertices)
            baseline_values = [build.accepted_slots[s] for s in vertices]
            baseline = equitable_refinement(local, baseline_values)
            fg = full_gap(local, args.dense_cutoff, args.eigen_tolerance)
            bg = quotient_gap(local, baseline)
            if len(set(baseline)) <= 1 or bg - fg <= args.gap_match_tolerance:
                continue

            parent_sig = [source_build.accepted_slots[parent[s]] for s in vertices]
            parent_component = [source_component_of[parent[s]] for s in vertices]
            parent_packet = [source_packets[parent[s]] for s in vertices]
            desc = [descriptor[s] for s in vertices]
            grand_sig = [grand_build.accepted_slots[parent_of_source[parent[s]]] for s in vertices]
            grand_component = [grand_component_of[parent_of_source[parent[s]]] for s in vertices]
            grand_packet = [grand_packets[parent_of_source[parent[s]]] for s in vertices]
            desc2 = [(descriptor_source[parent[s]], descriptor[s]) for s in vertices]
            oriented_square = [square_profile[s] for s in vertices]
            labelled_local = local_labelled(global_labelled, vertices, local_index)

            parent_seed = [(baseline_values[i], parent_sig[i]) for i in range(len(vertices))]
            parent_colors = equitable_refinement(local, parent_seed)
            pg = quotient_gap(local, parent_colors)
            if abs(pg - fg) <= args.gap_match_tolerance:
                continue

            residual.append(cid)

            candidates = {
                "BASELINE": ("ordinary", baseline_values),
                "PARENT_SIGNATURE": ("ordinary", parent_seed),
                "INSERTION_DESCRIPTOR": ("ordinary", [(baseline_values[i], desc[i]) for i in range(len(vertices))]),
                "PARENT_SIGNATURE_PLUS_DESCRIPTOR": ("ordinary", [(baseline_values[i], parent_sig[i], desc[i]) for i in range(len(vertices))]),
                "TWO_LEVEL_SIGNATURE_HISTORY": ("ordinary", [(baseline_values[i], parent_sig[i], grand_sig[i]) for i in range(len(vertices))]),
                "TWO_LEVEL_PACKET_HISTORY": ("ordinary", [(baseline_values[i], parent_packet[i], grand_packet[i]) for i in range(len(vertices))]),
                "TWO_LEVEL_DESCRIPTOR_HISTORY": ("ordinary", [(baseline_values[i], desc2[i]) for i in range(len(vertices))]),
                "ORIENTED_SQUARE_PROFILE": ("ordinary", [(baseline_values[i], oriented_square[i]) for i in range(len(vertices))]),
                "LR3_EDGE_LABELLED": ("labelled", baseline_values),
                "LR3_EDGE_LABELLED_PARENT_SIGNATURE": ("labelled", parent_seed),
            }

            for name, (kind, values) in candidates.items():
                colors = labelled_refinement(labelled_local, values) if kind == "labelled" else equitable_refinement(local, values)
                qg = quotient_gap(local, colors)
                visible = abs(qg - fg) <= args.gap_match_tolerance
                rows.append({
                    "n": n,
                    "component_id": cid,
                    "pi_label": pi_text(pi_labels[vertices[0]]),
                    "component_states": len(vertices),
                    "candidate": name,
                    "refinement_kind": kind,
                    "initial_labels": len(set(values)),
                    "final_cells": len(set(colors)),
                    "compression_ratio": len(set(colors)) / len(vertices),
                    "full_gap": fg,
                    "quotient_gap": qg,
                    "gap_ratio": qg / fg,
                    "slowest_mode_visible": visible,
                })
                checks[f"n{n}_c{cid}_{name}_gap_order"] = qg + args.gap_match_tolerance >= fg

        candidate_summary = {}
        here = [r for r in rows if r["n"] == n]
        for name in sorted({r["candidate"] for r in here}):
            rr = [r for r in here if r["candidate"] == name]
            rec = [r for r in rr if r["slowest_mode_visible"]]
            candidate_summary[name] = {
                "recovered": len(rec),
                "total": len(rr),
                "mean_compression": statistics.fmean(r["compression_ratio"] for r in rr) if rr else None,
            }

        summaries[f"n{n}"] = {
            "residual_components": residual,
            "residual_count": len(residual),
            "candidate_summary": candidate_summary,
            "elapsed_seconds": time.perf_counter() - started,
        }

        print(f"  residual after parent signature={len(residual)} components={residual}")
        for name, result in candidate_summary.items():
            print(
                f"    {name:<38} recovered={result['recovered']}/{result['total']} "
                f"mean-compression={result['mean_compression']:.6f}"
            )
        print(f"  elapsed={summaries[f'n{n}']['elapsed_seconds']:.2f}s")
        print()

    write_csv(out_dir / "residual_completion_summary.csv", rows)

    strict_pass = all(checks.values())
    summary = {
        "probe": "EHF-OPW3-AUDIT-08",
        "title": "Residual Hidden-Sector Completion by LR3 Edge Labels and Growth History",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "arguments": vars(args),
        "checks": checks,
        "strict_pass": strict_pass,
        "summaries": summaries,
        "guardrail": "All gaps are structural normalized-Laplacian diffusion gaps.",
        "elapsed_seconds": time.perf_counter() - started_all,
        "verdict": (
            "EHF_OPW3_AUDIT_08_RESIDUAL_COMPLETION_PASS"
            if strict_pass else
            "EHF_OPW3_AUDIT_08_RESIDUAL_COMPLETION_FAIL"
        ),
    }
    with (out_dir / "run_summary.json").open("w") as f:
        json.dump(summary, f, indent=2, sort_keys=True)

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
