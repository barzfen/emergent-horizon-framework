#!/usr/bin/env python3
"""
EHF-OPW3-AUDIT-06
=================
Exact Packet-Closure Equivalence, Spectral Completeness, and Action Census

Audit-05 constructed exact equitable packet refinements.  This probe asks:

1. Do LR3, LR2, and joint LR3xLR2 signatures generate the same exact
   equitable closure, or merely closures with the same number of cells?
2. Does the LR3-native exact quotient contain the true slowest diffusion mode
   of each chamber, or are slower modes hidden inside quotient cells?
3. What exact stochastic action statistics follow from the quotient chain?

The quotient action is A_ab = -log P_ab.  It is a stochastic path cost, not a
quantum phase or a physical action.

Dependencies: numpy, scipy
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
from pathlib import Path
from typing import Dict, Hashable, List, Sequence, Set, Tuple

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh

SCRIPT_VERSION = "ehf_opw3_audit_06_v3_2026-07-24"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_int_csv(text: str) -> List[int]:
    out = [int(x.strip()) for x in text.split(",") if x.strip()]
    if not out:
        raise argparse.ArgumentTypeError("expected at least one integer")
    return out


def parse_csv(text: str) -> List[str]:
    out = [x.strip().upper() for x in text.split(",") if x.strip()]
    if not out:
        raise argparse.ArgumentTypeError("expected at least one value")
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


def connected_components(adjacency: Sequence[Set[int]]) -> List[List[int]]:
    seen: Set[int] = set()
    comps: List[List[int]] = []
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
    return comps


def local_graph(global_adjacency: Sequence[Set[int]], vertices: Sequence[int]):
    index = {state: i for i, state in enumerate(vertices)}
    local: List[List[int]] = [[] for _ in vertices]
    for state in vertices:
        u = index[state]
        local[u] = sorted(index[v] for v in global_adjacency[state] if v in index)
    return local


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

        # The new partition always refines the old one because the old colour
        # is part of every refinement key.  If the number of cells has not
        # increased, the partition is already stable even when the numeric
        # colour IDs have been permuted by canonical relabelling.
        if len(set(new_colors)) == len(set(colors)):
            return new_colors

        colors = new_colors


def partition_key(colors: Sequence[int], vertices: Sequence[int]) -> Set[frozenset[int]]:
    cells: Dict[int, List[int]] = defaultdict(list)
    for local_state, color in enumerate(colors):
        cells[color].append(vertices[local_state])
    return {frozenset(states) for states in cells.values()}


def refines(part_a: Set[frozenset[int]], part_b: Set[frozenset[int]]) -> bool:
    # A refines B when every A-cell is contained in one B-cell.
    for cell_a in part_a:
        if not any(cell_a <= cell_b for cell_b in part_b):
            return False
    return True


def quotient_chain(adjacency: Sequence[Sequence[int]], colors: Sequence[int]):
    ordered = sorted(set(colors))
    pos = {cell: i for i, cell in enumerate(ordered)}
    members: Dict[int, List[int]] = defaultdict(list)
    for u, color in enumerate(colors):
        members[color].append(u)

    q = len(ordered)
    counts = np.zeros((q, q), dtype=float)
    degrees = np.zeros(q, dtype=float)
    sizes = np.zeros(q, dtype=float)

    for cell in ordered:
        i = pos[cell]
        reps = members[cell]
        sizes[i] = len(reps)
        reference = None
        for u in reps:
            row = np.zeros(q, dtype=float)
            for v in adjacency[u]:
                row[pos[colors[v]]] += 1.0
            if reference is None:
                reference = row
            elif not np.array_equal(reference, row):
                raise RuntimeError("partition is not equitable")
        counts[i, :] = reference
        degrees[i] = reference.sum()

    p = np.divide(
        counts,
        degrees[:, None],
        out=np.zeros_like(counts),
        where=degrees[:, None] > 0,
    )

    # A zero-degree quotient cell can occur only for an isolated singleton
    # chamber.  Treat it as the canonical absorbing one-state Markov chain.
    for i, degree in enumerate(degrees):
        if degree == 0:
            p[i, i] = 1.0

    total_degree = float(np.dot(sizes, degrees))
    if total_degree > 0:
        pi = sizes * degrees / total_degree
    else:
        pi = sizes / sizes.sum()

    return ordered, counts, degrees, sizes, p, pi


def normalized_gap_from_adjacency(
    adjacency: Sequence[Sequence[int]],
    dense_cutoff: int,
    tol: float,
) -> float:
    n = len(adjacency)
    if n <= 1:
        return 0.0
    rows, cols = [], []
    degrees = np.zeros(n, dtype=float)
    for u, neighbours in enumerate(adjacency):
        degrees[u] = len(neighbours)
        for v in neighbours:
            rows.append(u)
            cols.append(v)
    a = sparse.csr_matrix(
        (np.ones(len(rows)), (rows, cols)),
        shape=(n, n),
        dtype=float,
    )
    inv = 1.0 / np.sqrt(degrees)
    s = sparse.diags(inv) @ a @ sparse.diags(inv)

    if n <= dense_cutoff:
        mu = np.linalg.eigvalsh(s.toarray())
        mu.sort()
        mu = mu[::-1]
        return float(max(0.0, 1.0 - mu[1]))

    vals = eigsh(s, k=2, which="LA", tol=tol, return_eigenvectors=False)
    vals = np.sort(vals)[::-1]
    return float(max(0.0, 1.0 - vals[1]))


def quotient_laplacian_spectrum(p: np.ndarray, pi: np.ndarray) -> np.ndarray:
    q = p.shape[0]
    if q <= 1:
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


def action_statistics(p: np.ndarray, pi: np.ndarray) -> dict:
    support = p > 0
    actions = -np.log(p[support])
    edge_weights = (pi[:, None] * p)[support]
    entropy_rate = float(np.sum(edge_weights * actions))
    return {
        "support_transitions": int(support.sum()),
        "distinct_action_values": int(len(np.unique(np.round(actions, 14)))),
        "action_min": float(actions.min()) if len(actions) else None,
        "action_median": float(np.median(actions)) if len(actions) else None,
        "action_mean_unweighted": float(actions.mean()) if len(actions) else None,
        "action_max": float(actions.max()) if len(actions) else None,
        "entropy_rate_mean_action": entropy_rate,
        "self_transition_cells": int(np.sum(np.diag(p) > 0)),
        "stationary_entropy": float(-np.sum(pi[pi > 0] * np.log(pi[pi > 0]))),
    }


def pi_text(label) -> str:
    return "|".join(",".join(str(x) for x in side) for side in label)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit exact packet closure equality, slow-mode visibility, and stochastic action."
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--ns", type=parse_int_csv, default=[5, 7, 9])
    parser.add_argument("--graphs", type=parse_csv, default=["OPW3", "OPW23"])
    parser.add_argument("--dense-cutoff", type=int, default=180)
    parser.add_argument("--eigen-tolerance", type=float, default=1e-10)
    parser.add_argument("--gap-match-tolerance", type=float, default=1e-7)
    parser.add_argument("--out-dir", default="runs/ehf_opw3_audit_06")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    allowed = {"OPW3", "OPW23"}
    bad = [x for x in args.graphs if x not in allowed]
    if bad:
        raise ValueError(f"unsupported graphs: {bad}")

    base_path = Path(args.base_script).resolve()
    base = load_base(base_path)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 122)
    print("EHF-OPW3-AUDIT-06: PACKET-CLOSURE EQUIVALENCE, SPECTRAL COMPLETENESS, AND ACTION CENSUS")
    print("=" * 122)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"base engine:          {base_path}")
    print(f"n values:             {args.ns}")
    print(f"graphs:               {args.graphs}")
    print(f"output directory:     {out_dir.resolve()}")
    print(f"strict:               {args.strict}")
    print()

    checks: Dict[str, bool] = {}
    closure_rows: List[dict] = []
    quotient_rows: List[dict] = []
    spectrum_rows: List[dict] = []
    summaries: Dict[str, dict] = {}
    started_all = time.perf_counter()

    for n in args.ns:
        started_n = time.perf_counter()
        cycles = base.generate_cycles(n)
        index = {c: i for i, c in enumerate(cycles)}
        labels = [base.pi_label(c) for c in cycles]
        builds = {
            name: base.build_preserve_graph(
                cycles, index, labels, name, base.GRAPH_LENGTHS[name]
            )
            for name in ("OPW3", "LR2", "OPW23")
        }
        comps = {
            name: connected_components(builds[name].adjacency)
            for name in ("OPW3", "OPW23")
        }

        lr3 = builds["OPW3"].accepted_slots
        lr2 = builds["LR2"].accepted_slots

        print(f"[n={n}] states={len(cycles)}")

        n_summary = {}
        for graph_name in args.graphs:
            visible_count = 0
            eligible_gap_components = 0
            total_components = len(comps[graph_name])
            weighted_visible_states = 0
            weighted_eligible_states = 0
            exact_signature_closure_count = 0
            quotient_cell_total = 0

            for component_id, vertices in enumerate(comps[graph_name]):
                local = local_graph(builds[graph_name].adjacency, vertices)

                initial = {
                    "STRUCTURAL": [("ALL",)] * len(vertices),
                    "LR3_SIGNATURE": [lr3[v] for v in vertices],
                    "LR2_SIGNATURE": [lr2[v] for v in vertices],
                    "JOINT_SIGNATURE": [(lr3[v], lr2[v]) for v in vertices],
                }
                colors = {
                    name: equitable_refinement(local, values)
                    for name, values in initial.items()
                }
                parts = {
                    name: partition_key(coloring, vertices)
                    for name, coloring in colors.items()
                }

                lr3_eq_lr2 = parts["LR3_SIGNATURE"] == parts["LR2_SIGNATURE"]
                lr3_eq_joint = parts["LR3_SIGNATURE"] == parts["JOINT_SIGNATURE"]
                all_signature_equal = lr3_eq_lr2 and lr3_eq_joint
                structural_refined_by_lr3 = refines(
                    parts["LR3_SIGNATURE"], parts["STRUCTURAL"]
                )

                # Equality of the three signature-seeded closures is a
                # scientific outcome, not an implementation invariant.
                checks[f"n{n}_{graph_name}_c{component_id}_structural_refined"] = (
                    structural_refined_by_lr3
                )
                if all_signature_equal:
                    exact_signature_closure_count += 1

                chosen_colors = colors["LR3_SIGNATURE"]
                ordered, counts, degrees, sizes, p, pi = quotient_chain(
                    local, chosen_colors
                )
                quotient_cell_total += len(ordered)

                full_gap = normalized_gap_from_adjacency(
                    local,
                    dense_cutoff=args.dense_cutoff,
                    tol=args.eigen_tolerance,
                )
                quotient_spectrum = quotient_laplacian_spectrum(p, pi)
                quotient_gap = (
                    float(quotient_spectrum[1])
                    if len(quotient_spectrum) > 1 else None
                )
                gap_visible = (
                    abs(full_gap - quotient_gap) <= args.gap_match_tolerance
                    if quotient_gap is not None else None
                )
                if quotient_gap is not None:
                    eligible_gap_components += 1
                    weighted_eligible_states += len(vertices)
                    if gap_visible:
                        visible_count += 1
                        weighted_visible_states += len(vertices)

                checks[f"n{n}_{graph_name}_c{component_id}_quotient_rows"] = bool(
                    np.allclose(p.sum(axis=1), 1.0, atol=1e-12)
                )
                checks[f"n{n}_{graph_name}_c{component_id}_gap_order"] = (
                    True if quotient_gap is None else
                    quotient_gap + args.gap_match_tolerance >= full_gap
                )

                action = action_statistics(p, pi)

                closure_rows.append({
                    "n": n,
                    "graph": graph_name,
                    "component_id": component_id,
                    "pi_label": pi_text(labels[vertices[0]]),
                    "component_states": len(vertices),
                    "structural_cells": len(parts["STRUCTURAL"]),
                    "lr3_cells": len(parts["LR3_SIGNATURE"]),
                    "lr2_cells": len(parts["LR2_SIGNATURE"]),
                    "joint_cells": len(parts["JOINT_SIGNATURE"]),
                    "lr3_equals_lr2": lr3_eq_lr2,
                    "lr3_equals_joint": lr3_eq_joint,
                    "all_signature_closures_equal": all_signature_equal,
                    "lr3_refines_structural": structural_refined_by_lr3,
                })

                quotient_rows.append({
                    "n": n,
                    "graph": graph_name,
                    "component_id": component_id,
                    "pi_label": pi_text(labels[vertices[0]]),
                    "component_states": len(vertices),
                    "quotient_cells": len(ordered),
                    "compression_ratio": len(ordered) / len(vertices),
                    "full_normalized_gap": full_gap,
                    "quotient_normalized_gap": quotient_gap,
                    "gap_ratio_quotient_over_full": (
                        quotient_gap / full_gap
                        if quotient_gap is not None and full_gap > 0 else None
                    ),
                    "slowest_mode_visible": gap_visible,
                    **action,
                })

                for mode_index, eigenvalue in enumerate(quotient_spectrum):
                    spectrum_rows.append({
                        "n": n,
                        "graph": graph_name,
                        "component_id": component_id,
                        "component_states": len(vertices),
                        "quotient_cells": len(ordered),
                        "mode_index": mode_index,
                        "quotient_normalized_laplacian_eigenvalue": float(eigenvalue),
                    })

            n_summary[graph_name] = {
                "components": total_components,
                "all_signature_closures_equal_components": exact_signature_closure_count,
                "slow_gap_eligible_components": eligible_gap_components,
                "slowest_mode_visible_components": visible_count,
                "slowest_mode_visible_component_fraction": (
                    visible_count / eligible_gap_components
                    if eligible_gap_components else None
                ),
                "slowest_mode_visible_state_weighted_fraction": (
                    weighted_visible_states / weighted_eligible_states
                    if weighted_eligible_states else None
                ),
                "total_exact_packet_cells": quotient_cell_total,
                "global_cells_per_state": quotient_cell_total / len(cycles),
            }

            print(
                f"  {graph_name:<5} signature-closure equality="
                f"{exact_signature_closure_count}/{total_components} "
                f"slow-gap visible={visible_count}/{eligible_gap_components} eligible "
                f"state-weighted={n_summary[graph_name]['slowest_mode_visible_state_weighted_fraction']:.6f} "
                f"global cells/state={n_summary[graph_name]['global_cells_per_state']:.6f}"
            )

        summaries[f"n{n}"] = {
            "states": len(cycles),
            "graphs": n_summary,
            "elapsed_seconds": time.perf_counter() - started_n,
        }
        print(f"  elapsed={summaries[f'n{n}']['elapsed_seconds']:.2f}s")
        print()

    write_csv(out_dir / "closure_equivalence_summary.csv", closure_rows)
    write_csv(out_dir / "quotient_action_spectral_summary.csv", quotient_rows)
    write_csv(out_dir / "quotient_spectrum_ledger.csv", spectrum_rows)

    strict_pass = all(checks.values())
    summary = {
        "probe": "EHF-OPW3-AUDIT-06",
        "title": "Exact Packet-Closure Equivalence, Spectral Completeness, and Action Census",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "arguments": vars(args),
        "base_script": str(base_path),
        "checks": checks,
        "strict_pass": strict_pass,
        "summaries": summaries,
        "interpretation_guardrail": (
            "The quotient is an exact reversible stochastic chain. "
            "A=-log(P) is a stochastic transition cost, not yet a quantum action. "
            "A hidden slow mode means the packet quotient omits the chamber's "
            "slowest diffusion direction; it does not imply missing physical particles."
        ),
        "elapsed_seconds": time.perf_counter() - started_all,
        "verdict": (
            "EHF_OPW3_AUDIT_06_V3_PACKET_CLOSURE_SPECTRAL_ACTION_PASS"
            if strict_pass else
            "EHF_OPW3_AUDIT_06_V3_PACKET_CLOSURE_SPECTRAL_ACTION_FAIL"
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
