#!/usr/bin/env python3
"""
EHF-OPW3-AUDIT-05: LR3-Native Equitable Packet Reconstruction

Audit-02 showed that the four LR3 active signatures and the legacy sixteen
joint LR3/LR2 signatures are observables but not exact Markov lumpings. This
probe computes the coarsest exact equitable refinement of several initial
partitions inside every connected chamber.

An equitable partition has identical neighbour counts from every state in a
cell to every other cell. It therefore defines an exact quotient of adjacency
and the simple random walk.
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

SCRIPT_VERSION = "ehf_opw3_audit_05_2026-07-22"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_csv(text: str) -> List[str]:
    values = [x.strip().upper() for x in text.split(",") if x.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one value")
    return values


def parse_int_csv(text: str) -> List[int]:
    values = [int(x.strip()) for x in text.split(",") if x.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one integer")
    return values


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
    components: List[List[int]] = []
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
        components.append(comp)
    components.sort(key=lambda comp: (-len(comp), comp[0]))
    return components


def partition_key(components: Sequence[Sequence[int]]) -> Set[frozenset[int]]:
    return {frozenset(comp) for comp in components}


def encode_initial(values: Sequence[Hashable]) -> List[int]:
    unique = sorted(set(values), key=repr)
    mapping = {value: i for i, value in enumerate(unique)}
    return [mapping[value] for value in values]


def equitable_refinement(
    local_adjacency: Sequence[Sequence[int]],
    initial_values: Sequence[Hashable],
) -> Tuple[List[int], Dict[int, Hashable], int]:
    colors = encode_initial(initial_values)
    rounds = 0

    while True:
        keys = []
        for u, neighbours in enumerate(local_adjacency):
            histogram = Counter(colors[v] for v in neighbours)
            keys.append((colors[u], tuple(sorted(histogram.items()))))

        unique_keys = sorted(set(keys), key=repr)
        key_to_color = {key: i for i, key in enumerate(unique_keys)}
        new_colors = [key_to_color[key] for key in keys]

        if new_colors == colors:
            break
        if len(set(new_colors)) == len(set(colors)):
            colors = new_colors
            rounds += 1
            break
        colors = new_colors
        rounds += 1

    final_to_initial: Dict[int, Hashable] = {}
    for final_color in sorted(set(colors)):
        members = [i for i, color in enumerate(colors) if color == final_color]
        values = {initial_values[i] for i in members}
        if len(values) != 1:
            raise RuntimeError("refinement merged distinct initial labels")
        final_to_initial[final_color] = next(iter(values))

    return colors, final_to_initial, rounds


def exact_equitable_counts(
    local_adjacency: Sequence[Sequence[int]],
    colors: Sequence[int],
) -> Tuple[bool, Dict[int, Tuple[int, ...]], List[int]]:
    cells = sorted(set(colors))
    cell_to_col = {cell: j for j, cell in enumerate(cells)}
    reference: Dict[int, Tuple[int, ...]] = {}

    for u, color in enumerate(colors):
        counts = [0] * len(cells)
        for v in local_adjacency[u]:
            counts[cell_to_col[colors[v]]] += 1
        row = tuple(counts)
        if color not in reference:
            reference[color] = row
        elif reference[color] != row:
            return False, reference, cells

    return True, reference, cells


def local_graph(
    global_adjacency: Sequence[Set[int]],
    vertices: Sequence[int],
) -> List[List[int]]:
    index = {state: i for i, state in enumerate(vertices)}
    adjacency: List[List[int]] = [[] for _ in vertices]
    for state in vertices:
        u = index[state]
        adjacency[u] = sorted(
            index[target]
            for target in global_adjacency[state]
            if target in index
        )
    return adjacency


def pi_text(label) -> str:
    return "|".join(",".join(str(x) for x in side) for side in label)


def summary_stats(values: Sequence[float]) -> dict:
    if not values:
        return {"min": None, "median": None, "mean": None, "max": None}
    return {
        "min": float(min(values)),
        "median": float(statistics.median(values)),
        "mean": float(statistics.fmean(values)),
        "max": float(max(values)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Construct exact equitable packet refinements for OPW3."
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--ns", type=parse_int_csv, default=[5, 7, 9])
    parser.add_argument("--graphs", type=parse_csv, default=["OPW3", "OPW23"])
    parser.add_argument(
        "--initial-partitions",
        type=parse_csv,
        default=[
            "STRUCTURAL",
            "LR3_SIGNATURE",
            "LR2_SIGNATURE",
            "JOINT_SIGNATURE",
        ],
    )
    parser.add_argument("--out-dir", default="runs/ehf_opw3_audit_05")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    allowed_graphs = {"OPW3", "LR2", "OPW23"}
    allowed_partitions = {
        "STRUCTURAL",
        "LR3_SIGNATURE",
        "LR2_SIGNATURE",
        "JOINT_SIGNATURE",
    }
    if any(x not in allowed_graphs for x in args.graphs):
        raise ValueError(f"unknown graph in {args.graphs}")
    if any(x not in allowed_partitions for x in args.initial_partitions):
        raise ValueError(f"unknown partition in {args.initial_partitions}")

    base_path = Path(args.base_script).resolve()
    base = load_base(base_path)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 120)
    print("EHF-OPW3-AUDIT-05: LR3-NATIVE EQUITABLE PACKET RECONSTRUCTION")
    print("=" * 120)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"base engine:          {base_path}")
    print(f"n values:             {args.ns}")
    print(f"graphs:               {args.graphs}")
    print(f"initial partitions:   {args.initial_partitions}")
    print(f"output directory:     {out_dir.resolve()}")
    print(f"strict:               {args.strict}")
    print()

    checks: Dict[str, bool] = {}
    component_rows: List[dict] = []
    cell_rows: List[dict] = []
    transition_rows: List[dict] = []
    summaries: Dict[str, dict] = {}
    started_all = time.perf_counter()

    for n in args.ns:
        if n % 2 == 0:
            raise ValueError(f"OPW requires odd n; received {n}")

        started_n = time.perf_counter()
        cycles = base.generate_cycles(n)
        cycle_index = {cycle: i for i, cycle in enumerate(cycles)}
        labels = [base.pi_label(cycle) for cycle in cycles]

        builds = {
            name: base.build_preserve_graph(
                cycles=cycles,
                cycle_index=cycle_index,
                labels=labels,
                name=name,
                lengths=base.GRAPH_LENGTHS[name],
            )
            for name in ("OPW3", "LR2", "OPW23")
        }
        components = {
            name: connected_components(builds[name].adjacency)
            for name in ("OPW3", "LR2", "OPW23")
        }

        checks[f"n{n}_OPW3_OPW23_partition_equal"] = (
            partition_key(components["OPW3"])
            == partition_key(components["OPW23"])
        )

        lr3_signature = builds["OPW3"].accepted_slots
        lr2_signature = builds["LR2"].accepted_slots
        initial_values_global: Dict[str, List[Hashable]] = {
            "STRUCTURAL": [("ALL",)] * len(cycles),
            "LR3_SIGNATURE": list(lr3_signature),
            "LR2_SIGNATURE": list(lr2_signature),
            "JOINT_SIGNATURE": [
                (lr3_signature[i], lr2_signature[i])
                for i in range(len(cycles))
            ],
        }

        print(f"[n={n}] states={len(cycles)}")
        n_summary: Dict[str, dict] = {}

        for graph_name in args.graphs:
            graph_components = components[graph_name]
            for partition_name in args.initial_partitions:
                final_counts: List[float] = []
                compression: List[float] = []
                round_counts: List[float] = []

                for component_id, vertices in enumerate(graph_components):
                    adjacency = local_graph(builds[graph_name].adjacency, vertices)
                    initial_values = [
                        initial_values_global[partition_name][state]
                        for state in vertices
                    ]
                    initial_cell_count = len(set(initial_values))
                    colors, final_to_initial, rounds = equitable_refinement(
                        adjacency, initial_values
                    )
                    equitable, quotient_counts, cells = exact_equitable_counts(
                        adjacency, colors
                    )
                    final_cell_count = len(cells)

                    final_counts.append(float(final_cell_count))
                    compression.append(final_cell_count / len(vertices))
                    round_counts.append(float(rounds))

                    checks[
                        f"n{n}_{graph_name}_{partition_name}_c{component_id}_equitable"
                    ] = equitable
                    checks[
                        f"n{n}_{graph_name}_{partition_name}_c{component_id}_refines"
                    ] = final_cell_count >= initial_cell_count

                    members_by_cell: Dict[int, List[int]] = defaultdict(list)
                    for local_state, color in enumerate(colors):
                        members_by_cell[color].append(local_state)

                    total_degree = sum(len(neighbours) for neighbours in adjacency)
                    stationary_mass: Dict[int, float] = {}
                    for cell in cells:
                        degree_sum = sum(
                            len(adjacency[u]) for u in members_by_cell[cell]
                        )
                        stationary_mass[cell] = (
                            degree_sum / total_degree
                            if total_degree
                            else len(members_by_cell[cell]) / len(vertices)
                        )

                    row_sum_pass = True
                    detailed_balance_pass = True

                    for cell in cells:
                        members = members_by_cell[cell]
                        counts = quotient_counts[cell]
                        representative = members[0]
                        degree = len(adjacency[representative])
                        if any(len(adjacency[u]) != degree for u in members):
                            raise RuntimeError("equitable cell has inconsistent degree")

                        cell_rows.append({
                            "n": n,
                            "graph": graph_name,
                            "partition": partition_name,
                            "component_id": component_id,
                            "pi_label": pi_text(labels[vertices[0]]),
                            "component_states": len(vertices),
                            "initial_cells": initial_cell_count,
                            "refinement_rounds": rounds,
                            "final_cells": final_cell_count,
                            "cell_id": cell,
                            "cell_states": len(members),
                            "initial_label": repr(final_to_initial[cell]),
                            "degree": degree,
                            "stationary_mass": stationary_mass[cell],
                            "representative_cycle": ",".join(
                                str(x) for x in cycles[vertices[representative]]
                            ),
                        })

                        probabilities = []
                        for j, target_cell in enumerate(cells):
                            count = counts[j]
                            probability = count / degree if degree else 0.0
                            probabilities.append(probability)
                            if count:
                                transition_rows.append({
                                    "n": n,
                                    "graph": graph_name,
                                    "partition": partition_name,
                                    "component_id": component_id,
                                    "component_states": len(vertices),
                                    "source_cell": cell,
                                    "target_cell": target_cell,
                                    "edge_count_per_source_state": count,
                                    "source_degree": degree,
                                    "transition_probability": probability,
                                    "action_minus_log_probability": -math.log(probability),
                                })
                        if degree and abs(sum(probabilities) - 1.0) > 1e-12:
                            row_sum_pass = False

                    for i, cell_i in enumerate(cells):
                        counts_i = quotient_counts[cell_i]
                        degree_i = sum(counts_i)
                        for j, cell_j in enumerate(cells):
                            counts_j = quotient_counts[cell_j]
                            degree_j = sum(counts_j)
                            p_ij = counts_i[j] / degree_i if degree_i else 0.0
                            p_ji = counts_j[i] / degree_j if degree_j else 0.0
                            lhs = stationary_mass[cell_i] * p_ij
                            rhs = stationary_mass[cell_j] * p_ji
                            if abs(lhs - rhs) > 1e-12:
                                detailed_balance_pass = False
                                break
                        if not detailed_balance_pass:
                            break

                    checks[
                        f"n{n}_{graph_name}_{partition_name}_c{component_id}_rowsum"
                    ] = row_sum_pass
                    checks[
                        f"n{n}_{graph_name}_{partition_name}_c{component_id}_reversible"
                    ] = detailed_balance_pass

                    component_rows.append({
                        "n": n,
                        "graph": graph_name,
                        "partition": partition_name,
                        "component_id": component_id,
                        "pi_label": pi_text(labels[vertices[0]]),
                        "component_states": len(vertices),
                        "component_edges": sum(len(x) for x in adjacency) // 2,
                        "initial_cells": initial_cell_count,
                        "refinement_rounds": rounds,
                        "final_cells": final_cell_count,
                        "compression_ratio_cells_per_state": final_cell_count / len(vertices),
                        "mean_states_per_final_cell": len(vertices) / final_cell_count,
                        "largest_final_cell": max(len(v) for v in members_by_cell.values()),
                        "smallest_final_cell": min(len(v) for v in members_by_cell.values()),
                        "exact_equitable": equitable,
                        "transition_rows_sum_to_one": row_sum_pass,
                        "detailed_balance_pass": detailed_balance_pass,
                    })

                count_stats = summary_stats(final_counts)
                compression_stats = summary_stats(compression)
                rounds_stats = summary_stats(round_counts)
                key = f"{graph_name}:{partition_name}"
                n_summary[key] = {
                    "components": len(graph_components),
                    "final_cells_min": count_stats["min"],
                    "final_cells_median": count_stats["median"],
                    "final_cells_mean": count_stats["mean"],
                    "final_cells_max": count_stats["max"],
                    "compression_ratio_median": compression_stats["median"],
                    "compression_ratio_mean": compression_stats["mean"],
                    "refinement_rounds_median": rounds_stats["median"],
                    "refinement_rounds_max": rounds_stats["max"],
                }

                print(
                    f"  {graph_name:<5} {partition_name:<16} "
                    f"final-cells median={count_stats['median']:.1f} "
                    f"mean={count_stats['mean']:.2f} max={int(count_stats['max'])} "
                    f"compression mean={compression_stats['mean']:.4f}"
                )

        summaries[f"n{n}"] = {
            "states": len(cycles),
            "results": n_summary,
            "elapsed_seconds": time.perf_counter() - started_n,
        }
        print(f"  elapsed={summaries[f'n{n}']['elapsed_seconds']:.2f}s")
        print()

    write_csv(out_dir / "packet_component_summary.csv", component_rows)
    write_csv(out_dir / "packet_cell_summary.csv", cell_rows)
    write_csv(out_dir / "packet_transition_ledger.csv", transition_rows)

    strict_pass = all(checks.values())
    summary = {
        "probe": "EHF-OPW3-AUDIT-05",
        "title": "LR3-Native Equitable Packet Reconstruction",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "arguments": vars(args),
        "base_script": str(base_path),
        "checks": checks,
        "strict_pass": strict_pass,
        "summaries": summaries,
        "interpretation_guardrail": (
            "The packet chains are exact quotients of graph adjacency and the "
            "simple random walk. Their -log transition probabilities are "
            "stochastic actions only; no quantum phase or physical particle "
            "interpretation is made."
        ),
        "elapsed_seconds": time.perf_counter() - started_all,
        "verdict": (
            "EHF_OPW3_AUDIT_05_EQUITABLE_PACKET_RECONSTRUCTION_PASS"
            if strict_pass
            else "EHF_OPW3_AUDIT_05_EQUITABLE_PACKET_RECONSTRUCTION_FAIL"
        ),
    }

    with (out_dir / "run_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)

    print("=" * 120)
    print(f"strict checks:        {sum(checks.values())}/{len(checks)}")
    print(f"verdict:              {summary['verdict']}")
    print(f"elapsed:              {summary['elapsed_seconds']:.2f}s")
    print("=" * 120)

    if args.strict and not strict_pass:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
