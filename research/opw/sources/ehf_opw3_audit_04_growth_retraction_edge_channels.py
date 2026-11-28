#!/usr/bin/env python3
"""
EHF-OPW3-AUDIT-04
=================
Canonical Growth Retraction and LR3 Edge-Channel Decomposition

Rebuilds the exact odd growth map n -> n+2 by sequentially inserting the two
newest labels.  It compares OPW3, LR2 and legacy OPW23 active-signature
survival, rediscovers universally packet-preserving insertion descriptors, and
decomposes target OPW3 edges after deletion back to their source ancestors.

This is a combinatorial growth audit.  It does not identify growth steps with
physical time and does not yet define quantum dynamics.

Example
-------
python3 scripts/ehf_opw3_audit_04_growth_retraction_edge_channels.py \
  --base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --source-ns 5,7 \
  --out-dir runs/ehf_opw3_audit_04 \
  --strict
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
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Set, Tuple

SCRIPT_VERSION = "ehf_opw3_audit_04_2026-07-22"

Cycle = Tuple[int, ...]
Move = Tuple[int, int]
Descriptor = Tuple[int, int]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def write_csv(path: Path, rows: Sequence[dict], fieldnames: Sequence[str] | None = None) -> None:
    if fieldnames is None:
        if not rows:
            return
        fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def insert_after_gap(cycle: Sequence[int], gap: int, new_label: int) -> Cycle:
    """
    Insert new_label after the entry at zero-based cyclic gap index `gap`.

    The intermediate ordering is intentionally not canonicalized: the second
    insertion descriptor is defined on the n+1-entry intermediate ordering.
    """
    arr = list(cycle)
    if gap < 0 or gap >= len(arr):
        raise ValueError(f"gap {gap} outside 0..{len(arr)-1}")
    arr.insert(gap + 1, new_label)
    return tuple(arr)


def grow_by_descriptor(
    base,
    source: Cycle,
    source_n: int,
    descriptor: Descriptor,
) -> Cycle:
    g1, g2 = descriptor
    intermediate = insert_after_gap(source, g1, source_n)
    child = insert_after_gap(intermediate, g2, source_n + 1)
    return base.canonical_cycle(child)


def delete_newest_pair(base, child: Cycle, source_n: int) -> Cycle:
    reduced = [label for label in child if label < source_n]
    if len(reduced) != source_n:
        raise RuntimeError("newest-label deletion produced the wrong size")
    return base.canonical_cycle(reduced)


def all_descriptors(source_n: int) -> List[Descriptor]:
    return [
        (g1, g2)
        for g1 in range(source_n)
        for g2 in range(source_n + 1)
    ]


def legacy_core_descriptor_candidate(source_n: int) -> Set[Descriptor]:
    """
    Candidate core block from the old growth census, expressed in the present
    sequential-gap convention.

    Count:
        (n-6)(n-5)

    At n=7 this is {(3,3),(3,4)}.
    """
    return {
        (g1, g2)
        for g1 in range(3, source_n - 3)
        for g2 in range(3, source_n - 2)
    }


def variable_features(build) -> Tuple[Set[Move], Tuple[Move, ...]]:
    signatures = [set(sig) for sig in build.accepted_slots]
    fixed_core = set.intersection(*signatures)
    active_union = set.union(*signatures)
    variable = tuple(sorted(active_union - fixed_core))
    return fixed_core, variable


def bit_code(build, state_id: int, variable: Sequence[Move]) -> Tuple[int, ...]:
    signature = set(build.accepted_slots[state_id])
    return tuple(int(feature in signature) for feature in variable)


def hamming(a: Sequence[int], b: Sequence[int]) -> int:
    if len(a) != len(b):
        raise ValueError("cannot compare bit codes with different lengths")
    return sum(x != y for x, y in zip(a, b))


def connected_components(adjacency: Sequence[Set[int]]) -> Tuple[List[List[int]], Dict[int, int]]:
    seen: Set[int] = set()
    components: List[List[int]] = []
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
        components.append(comp)

    components.sort(key=lambda c: (-len(c), c[0]))
    for component_id, comp in enumerate(components):
        for state in comp:
            component_of[state] = component_id

    return components, component_of


def stable_counter(counter: Counter) -> str:
    return json.dumps(
        {str(key): int(value) for key, value in sorted(counter.items())},
        sort_keys=True,
    )


def descriptor_text(descriptor: Descriptor) -> str:
    return f"{descriptor[0]},{descriptor[1]}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit exact OPW3 n->n+2 growth and deletion channels."
    )
    parser.add_argument(
        "--base-script",
        required=True,
        help="path to Audit-01 foundation engine",
    )
    parser.add_argument(
        "--source-ns",
        type=parse_int_csv,
        default=[5, 7],
        help="odd source values; target is n+2",
    )
    parser.add_argument(
        "--out-dir",
        default="runs/ehf_opw3_audit_04",
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    base_path = Path(args.base_script).resolve()
    base = load_base(base_path)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 122)
    print("EHF-OPW3-AUDIT-04: CANONICAL GROWTH RETRACTION AND LR3 EDGE-CHANNEL DECOMPOSITION")
    print("=" * 122)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"base engine:          {base_path}")
    print(f"source n values:      {args.source_ns}")
    print(f"output directory:     {out_dir.resolve()}")
    print(f"strict:               {args.strict}")
    print()

    checks: Dict[str, bool] = {}
    growth_rows: List[dict] = []
    signature_rows: List[dict] = []
    descriptor_rows: List[dict] = []
    edge_rows: List[dict] = []
    ancestry_rows: List[dict] = []
    summaries: Dict[str, dict] = {}
    started_all = time.perf_counter()

    for source_n in args.source_ns:
        if source_n % 2 == 0:
            raise ValueError(f"source n must be odd; received {source_n}")
        target_n = source_n + 2
        started = time.perf_counter()

        source_cycles = base.generate_cycles(source_n)
        target_cycles = base.generate_cycles(target_n)
        source_index = {cycle: i for i, cycle in enumerate(source_cycles)}
        target_index = {cycle: i for i, cycle in enumerate(target_cycles)}
        source_pi = [base.pi_label(cycle) for cycle in source_cycles]
        target_pi = [base.pi_label(cycle) for cycle in target_cycles]

        source_builds = {
            name: base.build_preserve_graph(
                source_cycles,
                source_index,
                source_pi,
                name,
                base.GRAPH_LENGTHS[name],
            )
            for name in ("OPW3", "LR2", "OPW23")
        }
        target_builds = {
            name: base.build_preserve_graph(
                target_cycles,
                target_index,
                target_pi,
                name,
                base.GRAPH_LENGTHS[name],
            )
            for name in ("OPW3", "LR2", "OPW23")
        }

        source_components, source_component_of = connected_components(
            source_builds["OPW3"].adjacency
        )
        target_components, target_component_of = connected_components(
            target_builds["OPW3"].adjacency
        )

        descriptors = all_descriptors(source_n)
        expected_fibre_size = source_n * (source_n + 1)
        generated_owner: Dict[int, Tuple[int, Descriptor]] = {}
        parent_of_target: List[int] = [-1] * len(target_cycles)
        descriptor_of_target: List[Descriptor | None] = [None] * len(target_cycles)
        duplicate_children = 0
        deletion_failures = 0

        for source_id, source_cycle in enumerate(source_cycles):
            for descriptor in descriptors:
                child = grow_by_descriptor(
                    base=base,
                    source=source_cycle,
                    source_n=source_n,
                    descriptor=descriptor,
                )
                target_id = target_index.get(child)
                if target_id is None:
                    raise RuntimeError("generated child missing from target state space")

                if target_id in generated_owner:
                    duplicate_children += 1
                else:
                    generated_owner[target_id] = (source_id, descriptor)
                    parent_of_target[target_id] = source_id
                    descriptor_of_target[target_id] = descriptor

                recovered = delete_newest_pair(base, child, source_n)
                if recovered != source_cycle:
                    deletion_failures += 1

        target_coverage = len(generated_owner)
        fibre_hist = Counter(parent_of_target)
        fibre_hist.pop(-1, None)
        fibre_size_hist = Counter(fibre_hist.values())

        bijection_pass = (
            duplicate_children == 0
            and target_coverage == len(target_cycles)
            and deletion_failures == 0
            and fibre_size_hist == Counter({expected_fibre_size: len(source_cycles)})
        )
        checks[f"n{source_n}_to_{target_n}_growth_bijection"] = bijection_pass

        print(
            f"[{source_n}->{target_n}] source={len(source_cycles)} "
            f"target={len(target_cycles)} descriptors/source={len(descriptors)} "
            f"bijection={bijection_pass}"
        )

        growth_rows.append({
            "source_n": source_n,
            "target_n": target_n,
            "source_states": len(source_cycles),
            "target_states": len(target_cycles),
            "descriptors_per_source": len(descriptors),
            "expected_descriptors_per_source": expected_fibre_size,
            "generated_children": len(source_cycles) * len(descriptors),
            "unique_target_children": target_coverage,
            "duplicate_children": duplicate_children,
            "deletion_failures": deletion_failures,
            "fibre_size_histogram": stable_counter(fibre_size_hist),
            "bijection_pass": bijection_pass,
        })

        universal_by_graph: Dict[str, Set[Descriptor]] = {}

        for graph_name in ("OPW3", "LR2", "OPW23"):
            source_build = source_builds[graph_name]
            target_build = target_builds[graph_name]
            source_core, source_variable = variable_features(source_build)
            target_core, target_variable = variable_features(target_build)

            code_length_match = len(source_variable) == len(target_variable)
            checks[
                f"n{source_n}_{graph_name}_variable_code_length_match"
            ] = code_length_match

            overall_hamming = Counter()
            descriptor_hamming: Dict[Descriptor, Counter] = {
                descriptor: Counter() for descriptor in descriptors
            }

            if code_length_match:
                for target_id, source_id in enumerate(parent_of_target):
                    descriptor = descriptor_of_target[target_id]
                    if source_id < 0 or descriptor is None:
                        continue
                    source_code = bit_code(
                        source_build, source_id, source_variable
                    )
                    target_code = bit_code(
                        target_build, target_id, target_variable
                    )
                    distance = hamming(source_code, target_code)
                    overall_hamming[distance] += 1
                    descriptor_hamming[descriptor][distance] += 1

            universal = {
                descriptor
                for descriptor, hist in descriptor_hamming.items()
                if sum(hist.values()) == len(source_cycles)
                and hist.get(0, 0) == len(source_cycles)
            }
            universal_by_graph[graph_name] = universal

            preserve = overall_hamming.get(0, 0)
            total = sum(overall_hamming.values())
            preserve_rate = preserve / total if total else None

            signature_rows.append({
                "source_n": source_n,
                "target_n": target_n,
                "graph": graph_name,
                "source_fixed_core": json.dumps(sorted(source_core)),
                "target_fixed_core": json.dumps(sorted(target_core)),
                "source_variable_features": json.dumps(source_variable),
                "target_variable_features": json.dumps(target_variable),
                "code_bits": len(source_variable) if code_length_match else None,
                "code_length_match": code_length_match,
                "hamming_histogram": stable_counter(overall_hamming),
                "preserve_count": preserve,
                "total_children": total,
                "preserve_rate": preserve_rate,
                "universal_descriptor_count": len(universal),
                "universal_descriptors": json.dumps(sorted(universal)),
            })

            for descriptor in descriptors:
                hist = descriptor_hamming[descriptor]
                total_descriptor = sum(hist.values())
                descriptor_rows.append({
                    "source_n": source_n,
                    "target_n": target_n,
                    "graph": graph_name,
                    "g1": descriptor[0],
                    "g2": descriptor[1],
                    "children": total_descriptor,
                    "hamming_histogram": stable_counter(hist),
                    "preserve_count": hist.get(0, 0),
                    "preserve_rate": (
                        hist.get(0, 0) / total_descriptor
                        if total_descriptor else None
                    ),
                    "universally_preserving": descriptor in universal,
                })

            print(
                f"  {graph_name:<5} bits={len(source_variable) if code_length_match else 'NA'} "
                f"preserve={preserve_rate:.12f} "
                f"universal-descriptors={len(universal)}"
                if preserve_rate is not None else
                f"  {graph_name:<5} code-length mismatch"
            )

        candidate_core = legacy_core_descriptor_candidate(source_n)
        candidate_core_count = max(0, (source_n - 6) * (source_n - 5))
        checks[f"n{source_n}_candidate_core_count"] = (
            len(candidate_core) == candidate_core_count
        )

        if source_n >= 7:
            opw3_core_match = universal_by_graph["OPW3"] == candidate_core
            opw23_core_match = universal_by_graph["OPW23"] == candidate_core
            checks[f"n{source_n}_OPW3_universal_core_match"] = opw3_core_match
            checks[f"n{source_n}_OPW23_universal_core_match"] = opw23_core_match
        else:
            opw3_core_match = None
            opw23_core_match = None

        # Exact OPW3 edge collapse under deletion.
        source_opw3 = source_builds["OPW3"]
        target_opw3 = target_builds["OPW3"]

        vertical_by_parent = Counter()
        faithful_multiplicity = Counter()
        cross_chamber_multiplicity = Counter()
        same_chamber_nonedge_multiplicity = Counter()

        for child_u, child_v in target_opw3.edges:
            parent_u = parent_of_target[child_u]
            parent_v = parent_of_target[child_v]

            if parent_u == parent_v:
                vertical_by_parent[parent_u] += 1
                continue

            parent_edge = (
                (parent_u, parent_v)
                if parent_u < parent_v
                else (parent_v, parent_u)
            )
            if parent_edge in source_opw3.edges:
                faithful_multiplicity[parent_edge] += 1
            elif source_component_of[parent_u] != source_component_of[parent_v]:
                cross_chamber_multiplicity[parent_edge] += 1
            else:
                same_chamber_nonedge_multiplicity[parent_edge] += 1

        vertical_hist = Counter(vertical_by_parent.values())
        faithful_hist = Counter(faithful_multiplicity.values())
        cross_hist = Counter(cross_chamber_multiplicity.values())
        same_nonedge_hist = Counter(same_chamber_nonedge_multiplicity.values())

        source_edges_all_represented = (
            set(faithful_multiplicity) == set(source_opw3.edges)
        )
        vertical_uniform = (
            vertical_hist == Counter({3 * source_n - 5: len(source_cycles)})
        )
        faithful_expected = (source_n - 1) * (source_n - 2)
        faithful_uniform = (
            faithful_hist == Counter({
                faithful_expected: len(source_opw3.edges)
            })
        )
        no_same_chamber_shortcuts = len(same_chamber_nonedge_multiplicity) == 0

        vertical_total = sum(vertical_by_parent.values())
        faithful_total = sum(faithful_multiplicity.values())
        cross_total = sum(cross_chamber_multiplicity.values())
        same_nonedge_total = sum(same_chamber_nonedge_multiplicity.values())
        decomposed_total = (
            vertical_total + faithful_total + cross_total + same_nonedge_total
        )

        expected_cross_total = (
            len(source_cycles)
            * (source_n - 2)
            * (9 * source_n - 13)
            // 3
        )

        checks[f"n{source_n}_edge_decomposition_total"] = (
            decomposed_total == len(target_opw3.edges)
        )
        checks[f"n{source_n}_source_edges_all_represented"] = (
            source_edges_all_represented
        )
        checks[f"n{source_n}_vertical_uniform_formula"] = vertical_uniform
        checks[f"n{source_n}_faithful_uniform_formula"] = faithful_uniform
        checks[f"n{source_n}_no_same_chamber_shortcuts"] = (
            no_same_chamber_shortcuts
        )
        checks[f"n{source_n}_cross_total_formula"] = (
            cross_total == expected_cross_total
        )

        edge_rows.append({
            "source_n": source_n,
            "target_n": target_n,
            "source_states": len(source_cycles),
            "source_edges": len(source_opw3.edges),
            "target_edges": len(target_opw3.edges),
            "vertical_edges": vertical_total,
            "faithful_edges": faithful_total,
            "cross_source_chamber_edges": cross_total,
            "same_source_chamber_nonedge_edges": same_nonedge_total,
            "vertical_fraction": vertical_total / len(target_opw3.edges),
            "faithful_fraction": faithful_total / len(target_opw3.edges),
            "cross_source_chamber_fraction": cross_total / len(target_opw3.edges),
            "vertical_multiplicity_histogram": stable_counter(vertical_hist),
            "faithful_multiplicity_histogram": stable_counter(faithful_hist),
            "cross_pair_multiplicity_histogram": stable_counter(cross_hist),
            "same_chamber_nonedge_multiplicity_histogram": stable_counter(
                same_nonedge_hist
            ),
            "expected_vertical_per_source": 3 * source_n - 5,
            "expected_faithful_per_source_edge": faithful_expected,
            "expected_cross_total": expected_cross_total,
            "source_edges_all_represented": source_edges_all_represented,
            "no_same_chamber_shortcuts": no_same_chamber_shortcuts,
        })

        print(
            f"  OPW3 edge collapse: vertical={vertical_total} "
            f"faithful={faithful_total} cross-chamber={cross_total} "
            f"same-chamber-nonedge={same_nonedge_total}"
        )
        print(
            f"    vertical/source={next(iter(vertical_hist)) if len(vertical_hist)==1 else 'nonuniform'} "
            f"faithful/source-edge={next(iter(faithful_hist)) if len(faithful_hist)==1 else 'nonuniform'}"
        )

        # Component ancestry for all insertion and the OPW3 universal core.
        descriptor_channels = {
            "ALL": set(descriptors),
            "OPW3_UNIVERSAL_CORE": universal_by_graph["OPW3"],
        }

        for channel_name, allowed_descriptors in descriptor_channels.items():
            for source_component_id, source_component in enumerate(source_components):
                target_component_ids: Set[int] = set()
                child_count = 0
                for source_id in source_component:
                    source_cycle = source_cycles[source_id]
                    for descriptor in allowed_descriptors:
                        child = grow_by_descriptor(
                            base=base,
                            source=source_cycle,
                            source_n=source_n,
                            descriptor=descriptor,
                        )
                        target_id = target_index[child]
                        target_component_ids.add(target_component_of[target_id])
                        child_count += 1

                target_sizes = sorted(
                    len(target_components[target_component_id])
                    for target_component_id in target_component_ids
                )

                ancestry_rows.append({
                    "source_n": source_n,
                    "target_n": target_n,
                    "channel": channel_name,
                    "source_component_id": source_component_id,
                    "source_component_size": len(source_component),
                    "descriptors": len(allowed_descriptors),
                    "children": child_count,
                    "target_components_reached": len(target_component_ids),
                    "target_component_ids": json.dumps(
                        sorted(target_component_ids)
                    ),
                    "target_component_sizes": json.dumps(target_sizes),
                })

        core_rows_here = [
            row for row in ancestry_rows
            if row["source_n"] == source_n
            and row["channel"] == "OPW3_UNIVERSAL_CORE"
        ]
        if source_n == 7:
            two_branch = all(
                row["target_components_reached"] == 2
                for row in core_rows_here
            )
            affine_ladder = all(
                json.loads(row["target_component_sizes"])
                == sorted([
                    9 * row["source_component_size"] + 108,
                    9 * row["source_component_size"] + 144,
                ])
                for row in core_rows_here
            )
            checks["n7_OPW3_core_two_branch_ancestry"] = two_branch
            checks["n7_OPW3_core_affine_size_ladder"] = affine_ladder
            print(
                f"  OPW3 universal-core ancestry: two-branch={two_branch} "
                f"affine-ladder={affine_ladder}"
            )

        summaries[f"{source_n}_to_{target_n}"] = {
            "source_states": len(source_cycles),
            "target_states": len(target_cycles),
            "growth_bijection": bijection_pass,
            "OPW3_signature_preserve_rate": next(
                row["preserve_rate"]
                for row in signature_rows
                if row["source_n"] == source_n and row["graph"] == "OPW3"
            ),
            "OPW23_signature_preserve_rate": next(
                row["preserve_rate"]
                for row in signature_rows
                if row["source_n"] == source_n and row["graph"] == "OPW23"
            ),
            "OPW3_universal_descriptors": sorted(
                universal_by_graph["OPW3"]
            ),
            "OPW23_universal_descriptors": sorted(
                universal_by_graph["OPW23"]
            ),
            "candidate_core_descriptors": sorted(candidate_core),
            "edge_channels": {
                "vertical": vertical_total,
                "faithful": faithful_total,
                "cross_source_chamber": cross_total,
                "same_source_chamber_nonedge": same_nonedge_total,
            },
            "elapsed_seconds": time.perf_counter() - started,
        }

        print(f"  elapsed={summaries[f'{source_n}_to_{target_n}']['elapsed_seconds']:.2f}s")
        print()

    write_csv(out_dir / "growth_bijection_summary.csv", growth_rows)
    write_csv(out_dir / "signature_growth_summary.csv", signature_rows)
    write_csv(out_dir / "descriptor_preservation_ledger.csv", descriptor_rows)
    write_csv(out_dir / "opw3_edge_channel_summary.csv", edge_rows)
    write_csv(out_dir / "component_ancestry.csv", ancestry_rows)

    strict_pass = all(checks.values())
    summary = {
        "probe": "EHF-OPW3-AUDIT-04",
        "title": "Canonical Growth Retraction and LR3 Edge-Channel Decomposition",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "arguments": vars(args),
        "base_script": str(base_path),
        "checks": checks,
        "strict_pass": strict_pass,
        "summaries": summaries,
        "interpretation_guardrail": (
            "The insertion/deletion map is a combinatorial growth relation. "
            "No identification with Planck-time evolution, cosmological time, "
            "or a physical Hamiltonian is made."
        ),
        "elapsed_seconds": time.perf_counter() - started_all,
        "verdict": (
            "EHF_OPW3_AUDIT_04_GROWTH_RETRACTION_EDGE_CHANNEL_PASS"
            if strict_pass
            else "EHF_OPW3_AUDIT_04_GROWTH_RETRACTION_EDGE_CHANNEL_FAIL"
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
