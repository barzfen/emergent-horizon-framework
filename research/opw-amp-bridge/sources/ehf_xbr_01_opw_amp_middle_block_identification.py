#!/usr/bin/env python3
"""
EHF-XBR-01
==========
OPW Universal-Core / AMP Middle-Block Growth Identification

This cross-branch audit compares three distinct n=7 -> n=9 growth channels:

D_OPW:
    the OPW3 universal descriptor core {(3,3),(3,4)} in the zero-based
    sequential-gap convention;

D_AMP:
    the amplitude-branch middle-block channel: the two newest labels occupy
    positions 4 and 5 in either order, with parent obtained by deleting them;

G_ANCHOR:
    the two-step anchor-growth composite from GROW-01, inserting each newest
    label immediately right or left of the anchor.

The central test is whether D_OPW and D_AMP are exactly the same state-level
map after the zero-based/one-based label translation.

The probe also reproduces the already documented reconciliation between the
middle-block channel D and the anchor channel G:

    D(P) = {A(P), smaller(P)}
    G(P) = {A(P), A(flip P)}

at chamber identity level.

No amplitude ranks or spectral results are transferred automatically.  Only
map-level identities are established here.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Set, Tuple

SCRIPT_VERSION = "ehf_xbr_01_2026-07-25"

Cycle = Tuple[int, ...]
Descriptor = Tuple[int, int]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_base(path: Path):
    spec = importlib.util.spec_from_file_location("ehf_opw3_base", path)
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
    components: List[List[int]] = []
    component_of: Dict[int, int] = {}

    for start in range(len(adjacency)):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        component: List[int] = []
        while stack:
            u = stack.pop()
            component.append(u)
            for v in adjacency[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        component.sort()
        components.append(component)

    components.sort(key=lambda component: (-len(component), component[0]))
    for component_id, component in enumerate(components):
        for state in component:
            component_of[state] = component_id

    return components, component_of


def insert_after_gap(
    cycle: Sequence[int],
    gap: int,
    new_label: int,
) -> Cycle:
    arr = list(cycle)
    arr.insert(gap + 1, new_label)
    return tuple(arr)


def grow_by_descriptor(
    base,
    source: Cycle,
    source_n: int,
    descriptor: Descriptor,
) -> Cycle:
    gap1, gap2 = descriptor
    intermediate = insert_after_gap(source, gap1, source_n)
    child = insert_after_gap(intermediate, gap2, source_n + 1)
    return base.canonical_cycle(child)


def insert_anchor_branch(
    cycle: Sequence[int],
    new_label: int,
    branch: str,
) -> Cycle:
    """
    GROW-01 convention translated to zero-based anchored cycles.

    RIGHT: insert at position 1, immediately right of anchor 0.
    LEFT:  append at the final position, immediately left of anchor 0.
    """
    if branch == "RIGHT":
        return tuple(cycle[:1]) + (new_label,) + tuple(cycle[1:])
    if branch == "LEFT":
        return tuple(cycle) + (new_label,)
    raise ValueError(f"unknown anchor branch {branch}")


def anchor_composite_children(
    base,
    source: Cycle,
    source_n: int,
) -> Set[Cycle]:
    children: Set[Cycle] = set()
    for first_branch in ("RIGHT", "LEFT"):
        intermediate_raw = insert_anchor_branch(
            source,
            source_n,
            first_branch,
        )
        intermediate = base.canonical_cycle(intermediate_raw)
        for second_branch in ("RIGHT", "LEFT"):
            child_raw = insert_anchor_branch(
                intermediate,
                source_n + 1,
                second_branch,
            )
            children.add(base.canonical_cycle(child_raw))
    return children


def pi_text(label) -> str:
    return "|".join(",".join(str(x) for x in side) for side in label)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Identify the OPW3 universal descriptor core with the AMP middle-block growth map."
    )
    parser.add_argument("--base-script", required=True)
    parser.add_argument("--source-n", type=int, default=7)
    parser.add_argument("--out-dir", default="runs/ehf_xbr_01")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    source_n = args.source_n
    target_n = source_n + 2
    if source_n != 7:
        raise ValueError(
            "XBR-01 is definition-locked to the documented 7->9 reconciliation"
        )

    base_path = Path(args.base_script).resolve()
    base = load_base(base_path)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 126)
    print("EHF-XBR-01: OPW UNIVERSAL-CORE / AMP MIDDLE-BLOCK GROWTH IDENTIFICATION")
    print("=" * 126)
    print(f"script version:       {SCRIPT_VERSION}")
    print(f"base engine:          {base_path}")
    print(f"transition:           {source_n}->{target_n}")
    print(f"output directory:     {out_dir.resolve()}")
    print(f"strict:               {args.strict}")
    print()

    started = time.perf_counter()
    checks: Dict[str, bool] = {}
    source_rows: List[dict] = []

    source_cycles = base.generate_cycles(source_n)
    source_index = {cycle: i for i, cycle in enumerate(source_cycles)}
    source_pi = [base.pi_label(cycle) for cycle in source_cycles]
    source_build = base.build_preserve_graph(
        source_cycles,
        source_index,
        source_pi,
        "OPW3",
        base.GRAPH_LENGTHS["OPW3"],
    )
    source_components, source_component_of = connected_components(
        source_build.adjacency
    )

    target_cycles = base.generate_cycles(target_n)
    target_index = {cycle: i for i, cycle in enumerate(target_cycles)}
    target_pi = [base.pi_label(cycle) for cycle in target_cycles]
    target_build = base.build_preserve_graph(
        target_cycles,
        target_index,
        target_pi,
        "OPW3",
        base.GRAPH_LENGTHS["OPW3"],
    )
    target_components, target_component_of = connected_components(
        target_build.adjacency
    )

    core_descriptors = ((3, 3), (3, 4))

    # OPW descriptor map.
    opw_incidences: Set[Tuple[int, int]] = set()
    opw_children_by_source: Dict[int, Set[int]] = defaultdict(set)

    for source_id, source in enumerate(source_cycles):
        for descriptor in core_descriptors:
            child = grow_by_descriptor(
                base,
                source,
                source_n,
                descriptor,
            )
            target_id = target_index[child]
            opw_incidences.add((source_id, target_id))
            opw_children_by_source[source_id].add(target_id)

    # AMP middle-block reverse definition:
    # one-based {c[4],c[5]}={8,9}, hence zero-based {c[4],c[5]}={7,8}.
    amp_incidences: Set[Tuple[int, int]] = set()
    amp_children_by_source: Dict[int, Set[int]] = defaultdict(set)

    for target_id, child in enumerate(target_cycles):
        if {child[4], child[5]} != {source_n, source_n + 1}:
            continue
        parent = base.canonical_cycle(
            tuple(label for label in child if label < source_n)
        )
        source_id = source_index[parent]
        amp_incidences.add((source_id, target_id))
        amp_children_by_source[source_id].add(target_id)

    state_map_equal = opw_incidences == amp_incidences
    checks["opw_descriptor_equals_amp_middle_block_state_map"] = (
        state_map_equal
    )
    checks["opw_two_children_per_source_state"] = all(
        len(opw_children_by_source[source_id]) == 2
        for source_id in range(len(source_cycles))
    )
    checks["amp_two_children_per_source_state"] = all(
        len(amp_children_by_source[source_id]) == 2
        for source_id in range(len(source_cycles))
    )
    checks["middle_block_incidence_count_720"] = (
        len(opw_incidences) == 720
        and len(amp_incidences) == 720
    )

    # One-based translation sanity.
    one_based_middle_ok = all(
        {
            target_cycles[target_id][4] + 1,
            target_cycles[target_id][5] + 1,
        }
        == {8, 9}
        for _, target_id in opw_incidences
    )
    checks["zero_to_one_based_middle_block_translation"] = one_based_middle_ok

    # Chamber-level maps.
    d_children_by_parent: Dict[int, Set[int]] = defaultdict(set)
    for source_id, target_id in opw_incidences:
        d_children_by_parent[source_component_of[source_id]].add(
            target_component_of[target_id]
        )

    g_children_by_parent: Dict[int, Set[int]] = defaultdict(set)
    for source_id, source in enumerate(source_cycles):
        for child in anchor_composite_children(
            base,
            source,
            source_n,
        ):
            target_id = target_index[child]
            g_children_by_parent[source_component_of[source_id]].add(
                target_component_of[target_id]
            )

    d_coverage = set().union(*d_children_by_parent.values())
    g_coverage = set().union(*g_children_by_parent.values())
    union_coverage = d_coverage | g_coverage
    orphan_components = set(range(len(target_components))) - union_coverage

    two_d = all(
        len(d_children_by_parent[parent_id]) == 2
        for parent_id in range(len(source_components))
    )
    two_g = all(
        len(g_children_by_parent[parent_id]) == 2
        for parent_id in range(len(source_components))
    )
    one_shared = all(
        len(
            d_children_by_parent[parent_id]
            & g_children_by_parent[parent_id]
        )
        == 1
        for parent_id in range(len(source_components))
    )

    checks["middle_block_two_chambers_per_parent"] = two_d
    checks["anchor_composite_two_chambers_per_parent"] = two_g
    checks["channels_share_exactly_one_child_per_parent"] = one_shared
    checks["middle_block_coverage_38"] = len(d_coverage) == 38
    checks["anchor_coverage_20"] = len(g_coverage) == 20
    checks["union_coverage_39"] = len(union_coverage) == 39
    checks["union_orphans_30"] = len(orphan_components) == 30

    affine_ladder_ok = True
    shared_is_large_ok = True
    d_only_is_small_ok = True

    for parent_id, parent_component in enumerate(source_components):
        parent_size = len(parent_component)
        d_children = d_children_by_parent[parent_id]
        g_children = g_children_by_parent[parent_id]
        shared = d_children & g_children
        d_only = d_children - g_children
        g_only = g_children - d_children

        d_sizes = sorted(
            len(target_components[component_id])
            for component_id in d_children
        )
        expected_d_sizes = sorted(
            [9 * parent_size + 108, 9 * parent_size + 144]
        )
        affine_ladder_ok &= d_sizes == expected_d_sizes

        shared_id = next(iter(shared))
        d_only_id = next(iter(d_only))
        g_only_id = next(iter(g_only))

        shared_size = len(target_components[shared_id])
        d_only_size = len(target_components[d_only_id])
        g_only_size = len(target_components[g_only_id])

        shared_is_large_ok &= shared_size == 9 * parent_size + 144
        d_only_is_small_ok &= d_only_size == 9 * parent_size + 108

        source_rows.append({
            "source_component_id": parent_id,
            "source_pi_label": pi_text(
                source_pi[parent_component[0]]
            ),
            "source_component_size": parent_size,
            "D_middle_block_children": json.dumps(sorted(d_children)),
            "D_middle_block_child_sizes": json.dumps(d_sizes),
            "G_anchor_children": json.dumps(sorted(g_children)),
            "G_anchor_child_sizes": json.dumps(sorted(
                len(target_components[component_id])
                for component_id in g_children
            )),
            "shared_child": shared_id,
            "shared_child_size": shared_size,
            "D_only_child": d_only_id,
            "D_only_child_size": d_only_size,
            "G_only_child": g_only_id,
            "G_only_child_size": g_only_size,
            "shared_is_9s_plus_144": (
                shared_size == 9 * parent_size + 144
            ),
            "D_only_is_9s_plus_108": (
                d_only_size == 9 * parent_size + 108
            ),
        })

    checks["middle_block_affine_ladder"] = affine_ladder_ok
    checks["shared_child_is_plus_144"] = shared_is_large_ok
    checks["middle_block_only_child_is_plus_108"] = d_only_is_small_ok

    orphan_sizes = sorted(
        len(target_components[component_id])
        for component_id in orphan_components
    )
    largest_target_sizes = sorted(
        (len(component) for component in target_components),
        reverse=True,
    )[:4]
    largest_are_orphans = all(
        any(
            len(target_components[component_id]) == size
            for component_id in orphan_components
        )
        for size in largest_target_sizes
    )
    checks["all_four_largest_size_occurrences_have_orphans"] = (
        largest_are_orphans
    )

    write_csv(
        out_dir / "source_channel_reconciliation.csv",
        source_rows,
    )

    checks = {key: bool(value) for key, value in checks.items()}
    strict_pass = all(checks.values())
    elapsed = time.perf_counter() - started

    summary = {
        "probe": "EHF-XBR-01",
        "title": "OPW Universal-Core / AMP Middle-Block Growth Identification",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "arguments": vars(args),
        "base_script": str(base_path),
        "checks": checks,
        "strict_pass": strict_pass,
        "source_states": len(source_cycles),
        "target_states": len(target_cycles),
        "source_components": len(source_components),
        "target_components": len(target_components),
        "opw_middle_block_incidences": len(opw_incidences),
        "amp_middle_block_incidences": len(amp_incidences),
        "state_maps_equal": state_map_equal,
        "middle_block_coverage": len(d_coverage),
        "anchor_coverage": len(g_coverage),
        "union_coverage": len(union_coverage),
        "orphan_count": len(orphan_components),
        "orphan_component_ids": sorted(orphan_components),
        "orphan_sizes": orphan_sizes,
        "largest_target_sizes": largest_target_sizes,
        "interpretation": (
            "The OPW3 universal descriptors (3,3) and (3,4) are exactly the "
            "amplitude branch's middle-block insertion channel after the "
            "zero-based/one-based label translation. The separate GROW-01 "
            "anchor composite is not the same map; it shares only the +144 "
            "child per source chamber."
        ),
        "transfer_guardrail": (
            "Only the common growth map and its map-level theorems transfer "
            "automatically. Amplitude-relation theorems and OPW spectral "
            "theorems remain functor-specific."
        ),
        "elapsed_seconds": elapsed,
        "verdict": (
            "EHF_XBR_01_OPW_AMP_MIDDLE_BLOCK_IDENTIFICATION_PASS"
            if strict_pass else
            "EHF_XBR_01_OPW_AMP_MIDDLE_BLOCK_IDENTIFICATION_FAIL"
        ),
    }

    with (out_dir / "run_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)

    print(
        f"[state map] OPW descriptors={(3,3),(3,4)} "
        f"incidences={len(opw_incidences)}"
    )
    print(
        f"  AMP middle-block incidences={len(amp_incidences)} "
        f"exactly-equal={state_map_equal}"
    )
    print(
        f"  one-based translation: "
        f"{{c[4],c[5]}}={{8,9}} -> {one_based_middle_ok}"
    )
    print()
    print(
        f"[chamber reconciliation] D coverage={len(d_coverage)} "
        f"G coverage={len(g_coverage)} union={len(union_coverage)} "
        f"orphans={len(orphan_components)}"
    )
    print(
        f"  two-branch D={two_d} G={two_g} "
        f"one-shared-child={one_shared}"
    )
    print(
        f"  D ladder={affine_ladder_ok} "
        f"shared=9s+144={shared_is_large_ok} "
        f"D-only=9s+108={d_only_is_small_ok}"
    )
    print(
        f"  largest target sizes={largest_target_sizes} "
        f"represented among orphans={largest_are_orphans}"
    )
    print()
    print("=" * 126)
    print(f"strict checks:        {sum(checks.values())}/{len(checks)}")
    print(f"verdict:              {summary['verdict']}")
    print(f"elapsed:              {elapsed:.2f}s")
    print("=" * 126)

    if args.strict and not strict_pass:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
