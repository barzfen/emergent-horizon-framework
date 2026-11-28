#!/usr/bin/env python3
"""
EHF-OPW3-AUDIT-01
=================
Definition Lock and Matched Structural Census

Rebuilds the odd preserve-world directly from canonical Hamilton cycles and
compares three Pi-preserving local-move graphs:

    OPW3  : circular reversals of length 3 only
    LR2   : circular reversals of length 2 only (ablation)
    OPW23 : circular reversals of lengths 2 and 3 (legacy/enriched comparison)

The script deliberately avoids importing old OPW code. Its purpose is to create
a clean, auditable foundation before any packet, spectral, or QM bridge claims
are reused.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import time
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timezone
from itertools import permutations
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Set, Tuple

Cycle = Tuple[int, ...]
PiLabel = Tuple[Tuple[int, ...], Tuple[int, ...]]
Edge = Tuple[int, int]

SCRIPT_VERSION = "ehf_opw3_audit_01_2026-07-22"
GRAPH_LENGTHS: Mapping[str, Tuple[int, ...]] = {
    "OPW3": (3,),
    "LR2": (2,),
    "OPW23": (2, 3),
}

# Independent-engine regression targets from the documented legacy OPW23 model.
KNOWN_OPW23 = {
    5: {
        "states": 12,
        "edges": 8,
        "components": 5,
        "component_sizes": [4, 3, 2, 2, 1],
        "degree_histogram": {0: 1, 1: 6, 2: 5},
    },
    7: {
        "states": 360,
        "edges": 840,
        "components": 19,
        "component_sizes": [
            36, 32, 28, 28, 24, 24, 24, 20, 20, 20,
            16, 16, 16, 12, 12, 12, 8, 8, 4,
        ],
        "degree_histogram": {2: 4, 3: 32, 4: 120, 5: 128, 6: 76},
    },
    9: {
        "states": 20160,
        "edges": 67200,
        "components": 69,
        "component_size_histogram": {
            576: 1, 540: 1, 504: 2, 468: 3, 432: 5, 396: 5,
            360: 7, 324: 7, 288: 8, 252: 7, 216: 7, 180: 5,
            144: 5, 108: 3, 72: 2, 36: 1,
        },
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_int_csv(text: str) -> List[int]:
    values = [int(x.strip()) for x in text.split(",") if x.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one integer")
    return values


def parse_graph_csv(text: str) -> List[str]:
    values = [x.strip().upper() for x in text.split(",") if x.strip()]
    bad = [x for x in values if x not in GRAPH_LENGTHS]
    if bad:
        raise argparse.ArgumentTypeError(
            f"unknown graph(s) {bad}; choose from {sorted(GRAPH_LENGTHS)}"
        )
    if not values:
        raise argparse.ArgumentTypeError("expected at least one graph")
    return values


def canonical_cycle(seq: Sequence[int]) -> Cycle:
    """Anchor label 0 and quotient the anchored reversal."""
    arr = list(seq)
    i0 = arr.index(0)
    rot = tuple(arr[i0:] + arr[:i0])
    rev = (0,) + tuple(reversed(rot[1:]))
    return min(rot, rev)


def generate_cycles(n: int) -> List[Cycle]:
    """Generate canonical undirected Hamilton cycles on K_n."""
    if n < 3:
        raise ValueError("n must be at least 3")
    cycles: List[Cycle] = []
    for p in permutations(range(1, n)):
        if p <= tuple(reversed(p)):
            cycles.append((0,) + p)
    return cycles


def circular_reverse(cycle: Cycle, start: int, length: int) -> Cycle:
    """Reverse a circular position segment and canonicalize the result."""
    n = len(cycle)
    if length <= 0 or length > n:
        raise ValueError("invalid circular reversal length")
    indices = [(start + k) % n for k in range(length)]
    arr = list(cycle)
    values = [cycle[i] for i in indices][::-1]
    for i, value in zip(indices, values):
        arr[i] = value
    return canonical_cycle(arr)


def pi_label(cycle: Cycle) -> PiLabel:
    """Unordered pair of sorted labels in zero-based even/odd positions."""
    even = tuple(sorted(cycle[0::2]))
    odd = tuple(sorted(cycle[1::2]))
    pair = sorted((even, odd))
    return (pair[0], pair[1])


def edge_count(adjacency: Sequence[Set[int]]) -> int:
    return sum(len(row) for row in adjacency) // 2


def connected_components(adjacency: Sequence[Set[int]]) -> List[List[int]]:
    seen: Set[int] = set()
    components: List[List[int]] = []
    for start in range(len(adjacency)):
        if start in seen:
            continue
        queue = deque([start])
        seen.add(start)
        component: List[int] = []
        while queue:
            u = queue.popleft()
            component.append(u)
            for v in adjacency[u]:
                if v not in seen:
                    seen.add(v)
                    queue.append(v)
        components.append(sorted(component))
    components.sort(key=lambda comp: (-len(comp), comp[0]))
    return components


def stable_counter(counter: Counter) -> Dict[str, int]:
    return {str(k): int(v) for k, v in sorted(counter.items())}


def pi_text(label: PiLabel) -> str:
    return "|".join(",".join(str(x) for x in side) for side in label)


@dataclass
class GraphBuild:
    name: str
    lengths: Tuple[int, ...]
    adjacency: List[Set[int]]
    edges: Set[Edge]
    accepted_slots: List[Tuple[Tuple[int, int], ...]]
    attempted_move_images: int
    accepted_move_images: int
    self_images: int
    missing_images: int
    duplicate_accepted_images: int


def build_preserve_graph(
    cycles: Sequence[Cycle],
    cycle_index: Mapping[Cycle, int],
    labels: Sequence[PiLabel],
    name: str,
    lengths: Tuple[int, ...],
) -> GraphBuild:
    adjacency: List[Set[int]] = [set() for _ in cycles]
    edges: Set[Edge] = set()
    accepted_slots: List[Tuple[Tuple[int, int], ...]] = []
    attempted = accepted = self_images = missing = duplicate_images = 0

    for i, cycle in enumerate(cycles):
        state_slots: List[Tuple[int, int]] = []
        seen_targets: Set[int] = set()
        for length in lengths:
            for start in range(len(cycle)):
                attempted += 1
                target = circular_reverse(cycle, start, length)
                j = cycle_index.get(target)
                if j is None:
                    missing += 1
                    continue
                if j == i:
                    self_images += 1
                    continue
                if labels[j] != labels[i]:
                    continue

                accepted += 1
                state_slots.append((start, length))
                if j in seen_targets:
                    duplicate_images += 1
                seen_targets.add(j)
                u, v = (i, j) if i < j else (j, i)
                edges.add((u, v))
                adjacency[i].add(j)
                adjacency[j].add(i)

        accepted_slots.append(tuple(sorted(state_slots)))

    return GraphBuild(
        name=name,
        lengths=lengths,
        adjacency=adjacency,
        edges=edges,
        accepted_slots=accepted_slots,
        attempted_move_images=attempted,
        accepted_move_images=accepted,
        self_images=self_images,
        missing_images=missing,
        duplicate_accepted_images=duplicate_images,
    )


def component_records(
    n: int,
    graph: GraphBuild,
    cycles: Sequence[Cycle],
    labels: Sequence[PiLabel],
) -> Tuple[List[dict], List[List[int]], Dict[int, int]]:
    components = connected_components(graph.adjacency)
    component_of: Dict[int, int] = {}
    rows: List[dict] = []

    for component_id, comp in enumerate(components):
        for state in comp:
            component_of[state] = component_id
        comp_set = set(comp)
        internal_edges = sum(1 for u, v in graph.edges if u in comp_set and v in comp_set)
        degree_hist = Counter(len(graph.adjacency[state]) for state in comp)
        pi_hist = Counter(labels[state] for state in comp)
        signature_hist = Counter(graph.accepted_slots[state] for state in comp)
        rows.append({
            "n": n,
            "graph": graph.name,
            "component_id": component_id,
            "states": len(comp),
            "edges": internal_edges,
            "degree_min": min(degree_hist) if degree_hist else 0,
            "degree_max": max(degree_hist) if degree_hist else 0,
            "regular": len(degree_hist) == 1,
            "degree_histogram": json.dumps(stable_counter(degree_hist), sort_keys=True),
            "pi_labels": len(pi_hist),
            "pi_pure": len(pi_hist) == 1,
            "pi_label": pi_text(next(iter(pi_hist))) if len(pi_hist) == 1 else "",
            "active_signatures": len(signature_hist),
            "largest_signature_class": max(signature_hist.values()) if signature_hist else 0,
            "representative_cycle": ",".join(str(x) for x in cycles[comp[0]]),
        })
    return rows, components, component_of


def exact_partition_signature(components: Sequence[Sequence[int]]) -> Set[frozenset[int]]:
    return {frozenset(comp) for comp in components}


def fibre_partition(labels: Sequence[PiLabel]) -> List[List[int]]:
    fibres: Dict[PiLabel, List[int]] = defaultdict(list)
    for i, label in enumerate(labels):
        fibres[label].append(i)
    out = [sorted(states) for states in fibres.values()]
    out.sort(key=lambda comp: (-len(comp), comp[0]))
    return out


def compare_partitions(
    n: int,
    name_a: str,
    comps_a: Sequence[Sequence[int]],
    name_b: str,
    comps_b: Sequence[Sequence[int]],
) -> dict:
    part_a = exact_partition_signature(comps_a)
    part_b = exact_partition_signature(comps_b)

    b_of: Dict[int, int] = {}
    for j, comp in enumerate(comps_b):
        for state in comp:
            b_of[state] = j
    a_refines_b = all(len({b_of[state] for state in comp}) == 1 for comp in comps_a)

    a_of: Dict[int, int] = {}
    for i, comp in enumerate(comps_a):
        for state in comp:
            a_of[state] = i
    b_refines_a = all(len({a_of[state] for state in comp}) == 1 for comp in comps_b)

    return {
        "n": n,
        "partition_a": name_a,
        "partition_b": name_b,
        "components_a": len(comps_a),
        "components_b": len(comps_b),
        "exactly_equal": part_a == part_b,
        "a_refines_b": a_refines_b,
        "b_refines_a": b_refines_a,
    }


def check_known_opw23(
    n: int,
    states: int,
    edges: int,
    components: Sequence[Sequence[int]],
    degree_hist: Counter,
) -> Tuple[bool | None, List[str]]:
    expected = KNOWN_OPW23.get(n)
    if expected is None:
        return None, []
    failures: List[str] = []
    if states != expected["states"]:
        failures.append(f"states {states} != {expected['states']}")
    if edges != expected["edges"]:
        failures.append(f"edges {edges} != {expected['edges']}")
    if len(components) != expected["components"]:
        failures.append(f"components {len(components)} != {expected['components']}")
    sizes = sorted((len(comp) for comp in components), reverse=True)
    if "component_sizes" in expected and sizes != expected["component_sizes"]:
        failures.append("component size list mismatch")
    if "component_size_histogram" in expected:
        if dict(Counter(sizes)) != expected["component_size_histogram"]:
            failures.append("component size histogram mismatch")
    if "degree_histogram" in expected and dict(degree_hist) != expected["degree_histogram"]:
        failures.append("degree histogram mismatch")
    return len(failures) == 0, failures


def write_csv(path: Path, rows: Sequence[dict], fieldnames: Sequence[str] | None = None) -> None:
    if fieldnames is None:
        if not rows:
            return
        fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rebuild OPW3 and compare it with LR2 and OPW23.")
    parser.add_argument("--ns", type=parse_int_csv, default=[5, 7, 9])
    parser.add_argument(
        "--graphs",
        type=parse_graph_csv,
        default=["OPW3", "LR2", "OPW23"],
        help="comma-separated subset of OPW3,LR2,OPW23",
    )
    parser.add_argument("--out-dir", default="runs/ehf_opw3_audit_01")
    parser.add_argument("--write-state-ledger", action="store_true")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 108)
    print("EHF-OPW3-AUDIT-01: DEFINITION LOCK AND MATCHED STRUCTURAL CENSUS")
    print("=" * 108)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"n values:             {args.ns}")
    print(f"graphs:               {args.graphs}")
    print(f"output directory:     {out_dir.resolve()}")
    print(f"strict:               {args.strict}")
    print()

    graph_rows: List[dict] = []
    component_rows: List[dict] = []
    degree_rows: List[dict] = []
    slot_rows: List[dict] = []
    signature_rows: List[dict] = []
    partition_rows: List[dict] = []
    state_rows: List[dict] = []
    all_checks: Dict[str, bool] = {}
    summaries: Dict[str, dict] = {}
    started_all = time.perf_counter()

    for n in args.ns:
        if n % 2 == 0:
            raise ValueError(f"OPW requires odd n; received n={n}")
        started = time.perf_counter()
        cycles = generate_cycles(n)
        expected_states = math.factorial(n - 1) // 2
        cycle_index = {cycle: i for i, cycle in enumerate(cycles)}
        labels = [pi_label(cycle) for cycle in cycles]
        pi_components = fibre_partition(labels)

        all_checks[f"n{n}_state_count"] = len(cycles) == expected_states
        all_checks[f"n{n}_state_unique"] = len(cycle_index) == len(cycles)
        print(f"[n={n}] canonical states={len(cycles)} expected={expected_states}")

        builds: Dict[str, GraphBuild] = {}
        comps_by_name: Dict[str, List[List[int]]] = {"PI_FIBRES": pi_components}

        for name in args.graphs:
            graph = build_preserve_graph(cycles, cycle_index, labels, name, GRAPH_LENGTHS[name])
            builds[name] = graph
            comp_rows, components, component_of = component_records(n, graph, cycles, labels)
            component_rows.extend(comp_rows)
            comps_by_name[name] = components

            degrees = Counter(len(row) for row in graph.adjacency)
            component_sizes = sorted((len(comp) for comp in components), reverse=True)
            component_size_hist = Counter(component_sizes)
            graph_edges = edge_count(graph.adjacency)
            adjacency_edge_consistency = graph_edges == len(graph.edges)
            symmetric_pass = all(u in graph.adjacency[v] for u, row in enumerate(graph.adjacency) for v in row)
            pi_pure_pass = all(row["pi_pure"] for row in comp_rows)
            fibre_connected_pass = exact_partition_signature(components) == exact_partition_signature(pi_components)

            all_checks[f"n{n}_{name}_missing_zero"] = graph.missing_images == 0
            all_checks[f"n{n}_{name}_edge_consistency"] = adjacency_edge_consistency
            all_checks[f"n{n}_{name}_symmetric"] = symmetric_pass
            all_checks[f"n{n}_{name}_pi_pure"] = pi_pure_pass

            regression_pass: bool | None = None
            regression_failures: List[str] = []
            if name == "OPW23":
                regression_pass, regression_failures = check_known_opw23(
                    n, len(cycles), graph_edges, components, degrees
                )
                if regression_pass is not None:
                    all_checks[f"n{n}_OPW23_legacy_regression"] = regression_pass

            graph_rows.append({
                "n": n,
                "graph": name,
                "move_lengths": ",".join(map(str, graph.lengths)),
                "states": len(cycles),
                "expected_states": expected_states,
                "edges": graph_edges,
                "components": len(components),
                "largest_component": component_sizes[0],
                "smallest_component": component_sizes[-1],
                "pi_fibres": len(pi_components),
                "components_equal_pi_fibres": fibre_connected_pass,
                "degree_min": min(degrees),
                "degree_max": max(degrees),
                "degree_mean": sum(k * v for k, v in degrees.items()) / len(cycles),
                "degree_histogram": json.dumps(stable_counter(degrees), sort_keys=True),
                "component_size_histogram": json.dumps(stable_counter(component_size_hist), sort_keys=True),
                "attempted_move_images": graph.attempted_move_images,
                "accepted_move_images": graph.accepted_move_images,
                "self_images": graph.self_images,
                "missing_images": graph.missing_images,
                "duplicate_accepted_images": graph.duplicate_accepted_images,
                "legacy_regression_pass": regression_pass,
                "legacy_regression_failures": " | ".join(regression_failures),
            })

            for degree, count in sorted(degrees.items()):
                degree_rows.append({"n": n, "graph": name, "degree": degree, "states": count})

            for length in graph.lengths:
                for slot in range(n):
                    active_count = sum((slot, length) in sig for sig in graph.accepted_slots)
                    slot_rows.append({
                        "n": n,
                        "graph": name,
                        "length": length,
                        "slot": slot,
                        "active_states": active_count,
                        "state_fraction": active_count / len(cycles),
                    })

            signature_hist = Counter(graph.accepted_slots)
            for signature, count in sorted(signature_hist.items(), key=lambda item: (-item[1], item[0])):
                lr3_slots = tuple(slot for slot, length in signature if length == 3)
                lr2_slots = tuple(slot for slot, length in signature if length == 2)
                signature_rows.append({
                    "n": n,
                    "graph": name,
                    "signature": json.dumps(signature),
                    "lr3_slots": ";".join(map(str, lr3_slots)),
                    "lr2_slots": ";".join(map(str, lr2_slots)),
                    "active_move_count": len(signature),
                    "states": count,
                    "state_fraction": count / len(cycles),
                })

            if args.write_state_ledger:
                for i, cycle in enumerate(cycles):
                    state_rows.append({
                        "n": n,
                        "state_id": i,
                        "cycle": ",".join(map(str, cycle)),
                        "pi_label": pi_text(labels[i]),
                        "graph": name,
                        "component_id": component_of[i],
                        "degree": len(graph.adjacency[i]),
                        "active_signature": json.dumps(graph.accepted_slots[i]),
                    })

            print(
                f"  {name:<5} edges={graph_edges:<7} components={len(components):<4} "
                f"degree={min(degrees)}..{max(degrees)} signatures={len(signature_hist):<4} "
                f"Pi-fibres-exact={fibre_connected_pass}"
            )
            if regression_pass is not None:
                print(f"        legacy OPW23 regression: {'PASS' if regression_pass else 'FAIL'}")

        if {"OPW3", "LR2", "OPW23"}.issubset(builds):
            e3, e2, e23 = builds["OPW3"].edges, builds["LR2"].edges, builds["OPW23"].edges
            union_pass = e23 == (e3 | e2)
            all_checks[f"n{n}_edge_union"] = union_pass
            all_checks[f"n{n}_OPW3_subset_OPW23"] = e3 <= e23
            all_checks[f"n{n}_LR2_subset_OPW23"] = e2 <= e23
            summaries[f"n{n}_edge_relation"] = {
                "OPW3_edges": len(e3),
                "LR2_edges": len(e2),
                "OPW23_edges": len(e23),
                "edge_overlap": len(e3 & e2),
                "edge_union_pass": union_pass,
            }
            print(
                f"        edge union: |E3|={len(e3)} |E2|={len(e2)} "
                f"|overlap|={len(e3 & e2)} |E23|={len(e23)} PASS={union_pass}"
            )

        names = list(comps_by_name)
        for i, name_a in enumerate(names):
            for name_b in names[i + 1:]:
                partition_rows.append(compare_partitions(n, name_a, comps_by_name[name_a], name_b, comps_by_name[name_b]))

        if "OPW3" in builds:
            signatures = [
                frozenset(slot for slot, length in sig if length == 3)
                for sig in builds["OPW3"].accepted_slots
            ]
            fixed_core = set(signatures[0])
            active_union: Set[int] = set()
            for sig in signatures:
                fixed_core.intersection_update(sig)
                active_union.update(sig)
            variable_slots = active_union - fixed_core
            observed = set(signatures)
            variable_patterns = {frozenset(sig - fixed_core) for sig in signatures}
            reconstructed = {frozenset(fixed_core | set(pattern)) for pattern in variable_patterns}
            summaries[f"n{n}_OPW3_signature_geometry"] = {
                "fixed_core_slots": sorted(fixed_core),
                "variable_slots": sorted(variable_slots),
                "observed_signatures": len(observed),
                "variable_patterns": len(variable_patterns),
                "fixed_core_plus_variable_reconstruction_pass": reconstructed == observed,
            }
            print(
                f"        OPW3 LR3 signature geometry: core={sorted(fixed_core)} "
                f"variable={sorted(variable_slots)} patterns={len(observed)}"
            )

        summaries[f"n{n}"] = {
            "states": len(cycles),
            "expected_states": expected_states,
            "pi_fibres": len(pi_components),
            "pi_fibre_size_histogram": stable_counter(Counter(len(comp) for comp in pi_components)),
            "elapsed_seconds": time.perf_counter() - started,
        }
        print(f"        elapsed={summaries[f'n{n}']['elapsed_seconds']:.2f}s")
        print()

    write_csv(out_dir / "graph_summary.csv", graph_rows)
    write_csv(out_dir / "component_summary.csv", component_rows)
    write_csv(out_dir / "degree_histogram.csv", degree_rows)
    write_csv(out_dir / "slot_activity.csv", slot_rows)
    write_csv(out_dir / "active_signature_summary.csv", signature_rows)
    write_csv(out_dir / "partition_comparison.csv", partition_rows)
    if args.write_state_ledger:
        write_csv(out_dir / "state_signature_ledger.csv", state_rows)

    strict_pass = all(all_checks.values())
    summary = {
        "probe": "EHF-OPW3-AUDIT-01",
        "title": "Definition Lock and Matched Structural Census",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "argv": vars(args),
        "definition_lock": {
            "state_space": "canonical undirected Hamilton cycles on K_n",
            "internal_labels": "0..n-1",
            "canonicalization": "anchor 0; quotient anchored reversal; lexicographic minimum",
            "Pi": "unordered pair of sorted zero-based even/odd position label sets on canonical representative",
            "OPW3": "Pi-preserving circular reversals of length 3 only",
            "LR2": "Pi-preserving circular reversals of length 2 only",
            "OPW23": "Pi-preserving circular reversals of lengths 2 and 3",
        },
        "checks": all_checks,
        "strict_pass": strict_pass,
        "summaries": summaries,
        "elapsed_seconds": time.perf_counter() - started_all,
        "verdict": (
            "EHF_OPW3_AUDIT_01_FOUNDATION_REBUILD_PASS"
            if strict_pass else "EHF_OPW3_AUDIT_01_FOUNDATION_REBUILD_FAIL"
        ),
    }
    with (out_dir / "run_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
    with (out_dir / "run.log").open("w") as handle:
        handle.write(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    print("=" * 108)
    print(f"strict checks:        {sum(all_checks.values())}/{len(all_checks)}")
    print(f"verdict:              {summary['verdict']}")
    print(f"elapsed:              {summary['elapsed_seconds']:.2f}s")
    print("=" * 108)
    if args.strict and not strict_pass:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
