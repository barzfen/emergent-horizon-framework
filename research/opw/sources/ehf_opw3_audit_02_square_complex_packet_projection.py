#!/usr/bin/env python3
"""
EHF-OPW3-AUDIT-02
=================
Square-Complex and Active-Signature Projection Survival

Uses the independently rebuilt engine from EHF-OPW3-AUDIT-01 and audits the
first non-generic structures needed before reconstructing the QM bridge:

  * exact triangles and 4-cycles in OPW3, LR2, and OPW23;
  * rank of the oriented square-boundary span over selected finite fields;
  * residual first-cycle dimension after attaching all square 2-cells;
  * LR3/LR2 fixed-core and variable-boundary signature geometry;
  * exact crosswalk from the 4 x 4 LR3/LR2 signature pair to the 16-state
    OPW23 active-signature candidate at n >= 7;
  * equitable-partition and Markov-lumpability tests for the 4-state and
    16-state active-signature candidates.

This probe does NOT yet claim that active signatures are the mature packet map,
or that square cycles uniquely determine physical phases.  It determines what
LR3 alone structurally supplies for the later QM rebuild.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence, Set, Tuple

SCRIPT_VERSION = "ehf_opw3_audit_02_2026-07-22"


def parse_int_csv(text: str) -> List[int]:
    values = [int(x.strip()) for x in text.split(",") if x.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one integer")
    return values


def parse_str_csv(text: str) -> List[str]:
    values = [x.strip().upper() for x in text.split(",") if x.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one value")
    return values


def load_base(path: Path):
    spec = importlib.util.spec_from_file_location("ehf_opw3_audit_01_base", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import base engine from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def canonical_cycle4(seq: Sequence[int]) -> Tuple[int, int, int, int]:
    seq = tuple(seq)
    candidates = []
    for base in (seq, tuple(reversed(seq))):
        for shift in range(4):
            candidates.append(base[shift:] + base[:shift])
    return min(candidates)


def enumerate_triangles(adjacency: Sequence[Set[int]], vertices: Sequence[int]) -> List[Tuple[int, int, int]]:
    vertex_set = set(vertices)
    triangles: List[Tuple[int, int, int]] = []
    for u in vertices:
        for v in adjacency[u]:
            if v <= u or v not in vertex_set:
                continue
            for w in adjacency[u].intersection(adjacency[v]):
                if w > v and w in vertex_set:
                    triangles.append((u, v, w))
    return triangles


def enumerate_squares(adjacency: Sequence[Set[int]], vertices: Sequence[int]) -> List[Tuple[int, int, int, int]]:
    """Enumerate all simple 4-cycles, including cycles with graph diagonals."""
    vertex_set = set(vertices)
    squares: Set[Tuple[int, int, int, int]] = set()
    verts = sorted(vertices)
    for i, u in enumerate(verts):
        nu = adjacency[u].intersection(vertex_set)
        for v in verts[i + 1:]:
            common = sorted(nu.intersection(adjacency[v]))
            if len(common) < 2:
                continue
            for x, y in combinations(common, 2):
                if len({u, v, x, y}) != 4:
                    continue
                squares.add(canonical_cycle4((u, x, v, y)))
    return sorted(squares)


def is_induced_square(square: Sequence[int], adjacency: Sequence[Set[int]]) -> bool:
    a, b, c, d = square
    return c not in adjacency[a] and d not in adjacency[b]


def component_edges(adjacency: Sequence[Set[int]], vertices: Sequence[int]) -> List[Tuple[int, int]]:
    vertex_set = set(vertices)
    return sorted(
        (u, v)
        for u in vertices
        for v in adjacency[u]
        if u < v and v in vertex_set
    )


def signed_square_row(
    square: Sequence[int], edge_index: Mapping[Tuple[int, int], int], p: int
) -> Dict[int, int]:
    row: Dict[int, int] = {}
    cycle = list(square) + [square[0]]
    for u, v in zip(cycle, cycle[1:]):
        edge = (u, v) if u < v else (v, u)
        idx = edge_index[edge]
        coeff = 1 if u < v else -1
        value = (row.get(idx, 0) + coeff) % p
        if value:
            row[idx] = value
        elif idx in row:
            del row[idx]
    return row


def sparse_mod_rank(rows: Iterable[Dict[int, int]], p: int) -> int:
    pivots: Dict[int, Dict[int, int]] = {}
    for original in rows:
        row = {k: v % p for k, v in original.items() if v % p}
        while row:
            pivot = max(row)
            coeff = row[pivot]
            if pivot not in pivots:
                inv = pow(coeff, -1, p)
                row = {k: (v * inv) % p for k, v in row.items() if (v * inv) % p}
                pivots[pivot] = row
                break
            base = pivots[pivot]
            factor = coeff
            for k, v in base.items():
                new = (row.get(k, 0) - factor * v) % p
                if new:
                    row[k] = new
                elif k in row:
                    del row[k]
    return len(pivots)


def gf2_rank_from_square_rows(
    squares: Sequence[Sequence[int]], edge_index: Mapping[Tuple[int, int], int]
) -> int:
    pivots: Dict[int, int] = {}
    for square in squares:
        bits = 0
        cycle = list(square) + [square[0]]
        for u, v in zip(cycle, cycle[1:]):
            edge = (u, v) if u < v else (v, u)
            bits ^= 1 << edge_index[edge]
        while bits:
            pivot = bits.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = bits
                break
            bits ^= pivots[pivot]
    return len(pivots)


def signature_geometry(accepted_slots: Sequence[Sequence[Tuple[int, int]]], length: int) -> dict:
    signatures = [
        frozenset(start for start, move_length in slots if move_length == length)
        for slots in accepted_slots
    ]
    if not signatures:
        return {
            "fixed_core": [], "active_union": [], "variable_slots": [],
            "patterns": [], "state_codes": [],
        }
    fixed_core = set.intersection(*(set(sig) for sig in signatures))
    active_union = set.union(*(set(sig) for sig in signatures))
    variable_slots = sorted(active_union - fixed_core)
    patterns = sorted({tuple(int(slot in sig) for slot in variable_slots) for sig in signatures})
    state_codes = [tuple(int(slot in sig) for slot in variable_slots) for sig in signatures]
    return {
        "fixed_core": sorted(fixed_core),
        "active_union": sorted(active_union),
        "variable_slots": variable_slots,
        "patterns": patterns,
        "state_codes": state_codes,
    }


def code_text(code: Sequence[int]) -> str:
    return "".join(str(x) for x in code) if code else "-"


def transition_vector(
    state: int,
    adjacency: Sequence[Set[int]],
    target_codes: Sequence[Tuple[int, ...]],
    code_order: Sequence[Tuple[int, ...]],
) -> Tuple[int, ...]:
    counts = Counter(target_codes[v] for v in adjacency[state])
    return tuple(counts[code] for code in code_order)


def probability_vector(counts: Sequence[int]) -> Tuple[Fraction, ...] | Tuple[str]:
    degree = sum(counts)
    if degree == 0:
        return ("isolated",)
    return tuple(Fraction(value, degree) for value in counts)


def partition_dynamics_summary(
    n: int,
    dynamics_name: str,
    adjacency: Sequence[Set[int]],
    components: Sequence[Sequence[int]],
    partition_name: str,
    state_codes: Sequence[Tuple[int, ...]],
) -> dict:
    code_order = sorted(set(state_codes))
    grouped: Dict[Tuple[int, ...], List[int]] = defaultdict(list)
    for state, code in enumerate(state_codes):
        grouped[code].append(state)

    global_count_pass = True
    global_prob_pass = True
    for code, states in grouped.items():
        count_vectors = [transition_vector(s, adjacency, state_codes, code_order) for s in states]
        prob_vectors = [probability_vector(v) for v in count_vectors]
        global_count_pass &= len(set(count_vectors)) == 1
        global_prob_pass &= len(set(prob_vectors)) == 1

    component_cells = 0
    count_passing_cells = 0
    prob_passing_cells = 0
    states_in_count_passing_cells = 0
    states_in_prob_passing_cells = 0

    for component in components:
        comp_groups: Dict[Tuple[int, ...], List[int]] = defaultdict(list)
        for state in component:
            comp_groups[state_codes[state]].append(state)
        for code, states in comp_groups.items():
            component_cells += 1
            count_vectors = [transition_vector(s, adjacency, state_codes, code_order) for s in states]
            prob_vectors = [probability_vector(v) for v in count_vectors]
            count_ok = len(set(count_vectors)) == 1
            prob_ok = len(set(prob_vectors)) == 1
            if count_ok:
                count_passing_cells += 1
                states_in_count_passing_cells += len(states)
            if prob_ok:
                prob_passing_cells += 1
                states_in_prob_passing_cells += len(states)

    return {
        "n": n,
        "dynamics_graph": dynamics_name,
        "partition": partition_name,
        "partition_cells": len(code_order),
        "global_equitable": global_count_pass,
        "global_markov_lumpable": global_prob_pass,
        "component_cells": component_cells,
        "component_equitable_cells": count_passing_cells,
        "component_markov_lumpable_cells": prob_passing_cells,
        "component_equitable_cell_fraction": count_passing_cells / component_cells if component_cells else 1.0,
        "component_markov_lumpable_cell_fraction": prob_passing_cells / component_cells if component_cells else 1.0,
        "state_fraction_in_equitable_component_cells": states_in_count_passing_cells / len(state_codes),
        "state_fraction_in_lumpable_component_cells": states_in_prob_passing_cells / len(state_codes),
    }


def write_csv(path: Path, rows: Sequence[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit OPW3 square geometry and active-signature projections.")
    parser.add_argument(
        "--base-script",
        default="scripts/ehf_opw3_audit_01_definition_lock_structural_census.py",
    )
    parser.add_argument("--ns", type=parse_int_csv, default=[5, 7, 9])
    parser.add_argument("--graphs", type=parse_str_csv, default=["OPW3", "LR2", "OPW23"])
    parser.add_argument("--square-rank-fields", type=parse_int_csv, default=[2, 3])
    parser.add_argument("--out-dir", default="runs/ehf_opw3_audit_02")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_path = Path(args.base_script).resolve()
    base = load_base(base_path)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    unknown = [name for name in args.graphs if name not in base.GRAPH_LENGTHS]
    if unknown:
        raise ValueError(f"unknown graph names: {unknown}")
    for p in args.square_rank_fields:
        if p < 2 or any(p % d == 0 for d in range(2, int(math.sqrt(p)) + 1)):
            raise ValueError(f"square-rank field must be prime; got {p}")

    print("=" * 116)
    print("EHF-OPW3-AUDIT-02: SQUARE-COMPLEX AND ACTIVE-SIGNATURE PROJECTION SURVIVAL")
    print("=" * 116)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"base engine:          {base_path}")
    print(f"n values:             {args.ns}")
    print(f"graphs:               {args.graphs}")
    print(f"square-rank fields:   {args.square_rank_fields}")
    print(f"output directory:     {out_dir.resolve()}")
    print(f"strict:               {args.strict}")
    print()

    started_all = time.perf_counter()
    checks: Dict[str, bool] = {}
    graph_rows: List[dict] = []
    component_rows: List[dict] = []
    crosswalk_rows: List[dict] = []
    dynamics_rows: List[dict] = []
    signature_rows: List[dict] = []
    summaries: Dict[str, dict] = {}

    for n in args.ns:
        started_n = time.perf_counter()
        cycles = base.generate_cycles(n)
        cycle_index = {cycle: i for i, cycle in enumerate(cycles)}
        labels = [base.pi_label(cycle) for cycle in cycles]
        builds = {
            name: base.build_preserve_graph(
                cycles, cycle_index, labels, name, base.GRAPH_LENGTHS[name]
            )
            for name in args.graphs
        }
        components_by_name = {
            name: base.connected_components(build.adjacency)
            for name, build in builds.items()
        }

        print(f"[n={n}] states={len(cycles)}")

        # Signature geometry and crosswalk.
        geometries: Dict[str, dict] = {}
        if "OPW3" in builds:
            geometries["LR3"] = signature_geometry(builds["OPW3"].accepted_slots, 3)
        if "LR2" in builds:
            geometries["LR2"] = signature_geometry(builds["LR2"].accepted_slots, 2)
        elif "OPW23" in builds:
            geometries["LR2"] = signature_geometry(builds["OPW23"].accepted_slots, 2)
        if "OPW23" in builds:
            geometries["OPW23_LR3"] = signature_geometry(builds["OPW23"].accepted_slots, 3)
            geometries["OPW23_LR2"] = signature_geometry(builds["OPW23"].accepted_slots, 2)

        for name, geometry in geometries.items():
            signature_rows.append({
                "n": n,
                "signature_family": name,
                "fixed_core_slots": json.dumps(geometry["fixed_core"]),
                "active_union_slots": json.dumps(geometry["active_union"]),
                "variable_slots": json.dumps(geometry["variable_slots"]),
                "pattern_count": len(geometry["patterns"]),
                "patterns": json.dumps(geometry["patterns"]),
            })

        partition_codes: Dict[str, List[Tuple[int, ...]]] = {}
        if "LR3" in geometries:
            partition_codes["LR3_SIGNATURE"] = geometries["LR3"]["state_codes"]
        if "LR2" in geometries:
            partition_codes["LR2_SIGNATURE"] = geometries["LR2"]["state_codes"]
        if "LR3" in geometries and "LR2" in geometries:
            lr3_codes = geometries["LR3"]["state_codes"]
            lr2_codes = geometries["LR2"]["state_codes"]
            joint_codes = [tuple(a) + tuple(b) for a, b in zip(lr3_codes, lr2_codes)]
            partition_codes["LR3xLR2_SIGNATURE"] = joint_codes

            joint_hist = Counter(zip(lr3_codes, lr2_codes))
            opw23_sig_map: Dict[Tuple[Tuple[int, ...], Tuple[int, ...]], Set[str]] = defaultdict(set)
            for state in range(len(cycles)):
                opw23_signature = ""
                if "OPW23" in builds:
                    opw23_signature = json.dumps(builds["OPW23"].accepted_slots[state])
                pair = (lr3_codes[state], lr2_codes[state])
                opw23_sig_map[pair].add(opw23_signature)

            for (c3, c2), count in sorted(joint_hist.items()):
                mapped = opw23_sig_map[(c3, c2)]
                crosswalk_rows.append({
                    "n": n,
                    "lr3_code": code_text(c3),
                    "lr2_code": code_text(c2),
                    "joint_code": code_text(tuple(c3) + tuple(c2)),
                    "states": count,
                    "state_fraction": count / len(cycles),
                    "opw23_signature_count": len(mapped),
                    "opw23_signature": next(iter(mapped)) if len(mapped) == 1 else "",
                })

            expected_joint = len(set(lr3_codes)) * len(set(lr2_codes))
            full_product = len(joint_hist) == expected_joint
            deterministic_crosswalk = all(len(values) == 1 for values in opw23_sig_map.values())
            injective_crosswalk = len({next(iter(v)) for v in opw23_sig_map.values() if len(v) == 1}) == len(opw23_sig_map)
            summaries[f"n{n}_signature_crosswalk"] = {
                "lr3_pattern_count": len(set(lr3_codes)),
                "lr2_pattern_count": len(set(lr2_codes)),
                "joint_pattern_count": len(joint_hist),
                "full_cartesian_product": full_product,
                "joint_to_OPW23_deterministic": deterministic_crosswalk,
                "joint_to_OPW23_injective": injective_crosswalk,
            }

            print(
                f"  signatures: LR3={len(set(lr3_codes))} LR2={len(set(lr2_codes))} "
                f"joint={len(joint_hist)} full-product={full_product}"
            )

        # Short cycles and square-complex ranks, component by component.
        for graph_name, build in builds.items():
            graph_started = time.perf_counter()
            graph_components = components_by_name[graph_name]
            totals = Counter()
            field_rank_totals = Counter()
            component_cycle_rank_total = 0

            for component_id, component in enumerate(graph_components):
                edges = component_edges(build.adjacency, component)
                edge_index = {edge: i for i, edge in enumerate(edges)}
                triangles = enumerate_triangles(build.adjacency, component)
                squares = enumerate_squares(build.adjacency, component)
                induced_squares = sum(is_induced_square(square, build.adjacency) for square in squares)
                cycle_rank = len(edges) - len(component) + 1
                component_cycle_rank_total += cycle_rank

                ranks: Dict[int, int] = {}
                for p in args.square_rank_fields:
                    if p == 2:
                        rank = gf2_rank_from_square_rows(squares, edge_index)
                    else:
                        rank = sparse_mod_rank(
                            (signed_square_row(square, edge_index, p) for square in squares), p
                        )
                    ranks[p] = rank
                    field_rank_totals[p] += rank
                    checks[f"n{n}_{graph_name}_c{component_id}_square_rank_le_cycle_rank_GF{p}"] = rank <= cycle_rank

                component_rows.append({
                    "n": n,
                    "graph": graph_name,
                    "component_id": component_id,
                    "vertices": len(component),
                    "edges": len(edges),
                    "cycle_rank": cycle_rank,
                    "triangles": len(triangles),
                    "squares": len(squares),
                    "induced_squares": induced_squares,
                    **{f"square_rank_GF{p}": ranks[p] for p in args.square_rank_fields},
                    **{f"square_h1_residual_GF{p}": cycle_rank - ranks[p] for p in args.square_rank_fields},
                })

                totals["triangles"] += len(triangles)
                totals["squares"] += len(squares)
                totals["induced_squares"] += induced_squares

            graph_rows.append({
                "n": n,
                "graph": graph_name,
                "states": len(cycles),
                "edges": len(build.edges),
                "components": len(graph_components),
                "cycle_rank": component_cycle_rank_total,
                "triangles": totals["triangles"],
                "squares": totals["squares"],
                "induced_squares": totals["induced_squares"],
                **{f"square_rank_GF{p}": field_rank_totals[p] for p in args.square_rank_fields},
                **{
                    f"square_h1_residual_GF{p}": component_cycle_rank_total - field_rank_totals[p]
                    for p in args.square_rank_fields
                },
                "elapsed_seconds": time.perf_counter() - graph_started,
            })

            print(
                f"  {graph_name:<5} triangles={totals['triangles']:<8} "
                f"squares={totals['squares']:<10} cycle-rank={component_cycle_rank_total:<8} "
                + " ".join(
                    f"sq-rank-GF{p}={field_rank_totals[p]} residual={component_cycle_rank_total-field_rank_totals[p]}"
                    for p in args.square_rank_fields
                )
            )

            for partition_name, state_codes in partition_codes.items():
                dynamics_rows.append(partition_dynamics_summary(
                    n=n,
                    dynamics_name=graph_name,
                    adjacency=build.adjacency,
                    components=graph_components,
                    partition_name=partition_name,
                    state_codes=state_codes,
                ))

        summaries[f"n{n}"] = {
            "states": len(cycles),
            "elapsed_seconds": time.perf_counter() - started_n,
        }
        print(f"  elapsed={summaries[f'n{n}']['elapsed_seconds']:.2f}s")
        print()

    write_csv(out_dir / "square_graph_summary.csv", graph_rows)
    write_csv(out_dir / "square_component_summary.csv", component_rows)
    write_csv(out_dir / "active_signature_geometry.csv", signature_rows)
    write_csv(out_dir / "active_signature_crosswalk.csv", crosswalk_rows)
    write_csv(out_dir / "signature_partition_dynamics.csv", dynamics_rows)

    strict_pass = all(checks.values())
    summary = {
        "probe": "EHF-OPW3-AUDIT-02",
        "title": "Square-Complex and Active-Signature Projection Survival",
        "script_version": SCRIPT_VERSION,
        "base_script": str(base_path),
        "arguments": vars(args),
        "checks": checks,
        "strict_pass": strict_pass,
        "summaries": summaries,
        "elapsed_seconds": time.perf_counter() - started_all,
        "verdict": (
            "EHF_OPW3_AUDIT_02_SQUARE_AND_SIGNATURE_CENSUS_PASS"
            if strict_pass
            else "EHF_OPW3_AUDIT_02_SQUARE_AND_SIGNATURE_CENSUS_FAIL"
        ),
        "caveat": (
            "Active signatures are candidate packet coordinates only; this probe does not "
            "identify them with the mature legacy packet map or assign physical phases."
        ),
    }
    with (out_dir / "run_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True, default=str)

    print("=" * 116)
    print(f"strict checks:        {sum(checks.values())}/{len(checks)}")
    print(f"verdict:              {summary['verdict']}")
    print(f"elapsed:              {summary['elapsed_seconds']:.2f}s")
    print("=" * 116)

    if args.strict and not strict_pass:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
