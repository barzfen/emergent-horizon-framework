#!/usr/bin/env python3
"""
EHF-XBR-05A: Null-Channel Holonomy Definition Lock and Minimal Loop Census

This probe deliberately does not manufacture a holonomy matrix.

It consumes the exact EHF-XBR-04F6 singular-channel ledger, takes the channel
labels A subset {2,...,8}, |A|=3 as base vertices, and locks the candidate base
edge relation to Johnson adjacency:

    A ~ B  iff  |A intersect B| = 2.

The fiber at A is the exact chamber zero-mode space

    K_A = ker(Adj(C_A)).

Ordinary reversible (orthogonal/unitary) holonomy on whole fibers requires
constant fiber dimension along every edge used by transport.  XBR-05A audits
that prerequisite, enumerates the shortest simple loops in the induced
singular-channel graph, and refuses to define edge transport if the
prerequisite fails.

The integrity verdict and the scientific gate are separate:

* PASS means the definition lock and census were reproduced exactly.
* holonomy_defined=false means a later probe must supply a different,
  explicitly certified constant-rank subbundle or a theory of singular
  transport.  Products of arbitrary rectangular overlaps are not called
  holonomy.

No physical interpretation is assigned to a null fiber or loop.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Set, Tuple


SCRIPT_VERSION = "ehf_xbr_05a_v1_2026-07-31"
PROBE_NAME = "EHF-XBR-05A"
VERDICT_PASS = (
    "EHF_XBR_05A_NULL_CHANNEL_HOLONOMY_DEFINITION_LOCK_"
    "MINIMAL_LOOP_CENSUS_PASS"
)

Subset = Tuple[int, int, int]
Edge = Tuple[Subset, Subset]
Cycle = Tuple[Subset, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "pass", "passed"}


def parse_subset(text: str) -> Subset:
    values = tuple(sorted(int(value.strip()) for value in str(text).split(",")))
    if len(values) != 3 or len(set(values)) != 3:
        raise ValueError(f"invalid three-subset: {text!r}")
    if any(value not in range(2, 9) for value in values):
        raise ValueError(f"subset labels must lie in 2..8: {text!r}")
    return values  # type: ignore[return-value]


def subset_text(subset: Sequence[int]) -> str:
    return ",".join(map(str, subset))


def integer(row: Mapping[str, object], *names: str) -> int:
    for name in names:
        value = row.get(name)
        if value not in (None, ""):
            return int(str(value))
    raise KeyError(f"none of the required fields is present: {names}")


def read_csv(path: Path) -> List[dict]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open() as handle:
        return json.load(handle)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    fields: List[str] = []
    seen: Set[str] = set()
    for row in rows:
        for field in row:
            if field not in seen:
                seen.add(field)
                fields.append(field)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def johnson_distance(left: Subset, right: Subset) -> int:
    return 3 - len(set(left).intersection(right))


def induced_edges(vertices: Sequence[Subset]) -> List[Edge]:
    return [
        (left, right)
        for left, right in itertools.combinations(sorted(vertices), 2)
        if johnson_distance(left, right) == 1
    ]


def canonical_cycle(cycle: Sequence[Subset]) -> Cycle:
    values = tuple(cycle)
    candidates: List[Cycle] = []
    for oriented in (values, tuple(reversed(values))):
        for offset in range(len(values)):
            candidates.append(oriented[offset:] + oriented[:offset])
    return min(candidates)


def cycles_of_length(
    vertices: Sequence[Subset],
    edges: Sequence[Edge],
    length: int,
) -> List[Cycle]:
    edge_set = {frozenset(edge) for edge in edges}
    cycles: Set[Cycle] = set()
    for chosen in itertools.combinations(sorted(vertices), length):
        root = min(chosen)
        remainder = tuple(vertex for vertex in chosen if vertex != root)
        for ordering in itertools.permutations(remainder):
            candidate = (root,) + ordering
            pairs = [
                (candidate[index], candidate[(index + 1) % length])
                for index in range(length)
            ]
            if all(frozenset(pair) in edge_set for pair in pairs):
                cycles.add(canonical_cycle(candidate))
    return sorted(cycles)


def shortest_cycles(
    vertices: Sequence[Subset],
    edges: Sequence[Edge],
    max_length: int,
) -> Tuple[int, List[Cycle]]:
    for length in range(3, max_length + 1):
        cycles = cycles_of_length(vertices, edges, length)
        if cycles:
            return length, cycles
    return 0, []


def connected_components(
    vertices: Sequence[Subset],
    edges: Sequence[Edge],
) -> List[List[Subset]]:
    neighbors: Dict[Subset, Set[Subset]] = {vertex: set() for vertex in vertices}
    for left, right in edges:
        neighbors[left].add(right)
        neighbors[right].add(left)
    unseen = set(vertices)
    components: List[List[Subset]] = []
    while unseen:
        seed = min(unseen)
        stack = [seed]
        component: Set[Subset] = set()
        while stack:
            vertex = stack.pop()
            if vertex in component:
                continue
            component.add(vertex)
            stack.extend(sorted(neighbors[vertex] - component))
        unseen -= component
        components.append(sorted(component))
    return sorted(components, key=lambda item: (-len(item), item))


def loop_word(cycle: Sequence[Subset]) -> str:
    return " -> ".join(subset_text(vertex) for vertex in (*cycle, cycle[0]))


def markdown_report(
    channels: Sequence[Mapping[str, object]],
    edges: Sequence[Mapping[str, object]],
    loops: Sequence[Mapping[str, object]],
    checks: Mapping[str, bool],
    conclusion: Mapping[str, object],
    verdict: str,
) -> str:
    lines = [
        "# EHF-XBR-05A: Null-Channel Holonomy Definition Lock and Minimal Loop Census",
        "",
        f"Integrity verdict: `{verdict}`",
        "",
        "## Locked objects",
        "",
        "- Base vertices: the 11 nonzero singular proper channels from XBR-04F6.",
        "- Candidate base edges: Johnson distance one, equivalently two shared labels.",
        "- Fiber: the complete exact chamber adjacency kernel `K_A`.",
        "- Edge transport: intentionally undefined unless a reversible constant-rank connection is admissible.",
        "",
        "## Census",
        "",
        f"- vertices: {len(channels)}",
        f"- Johnson edges: {len(edges)}",
        f"- shortest loop length: {conclusion['shortest_loop_length']}",
        f"- shortest loops: {len(loops)}",
        f"- equal-dimension edges: {conclusion['equal_dimension_edges']}",
        f"- unequal-dimension edges: {conclusion['unequal_dimension_edges']}",
        "",
        "## Definition gate",
        "",
        f"`holonomy_defined = {str(conclusion['holonomy_defined']).lower()}`",
        "",
        str(conclusion["reason"]),
        "",
        "Every edge in the induced singular-channel graph changes the complete kernel dimension. "
        "Therefore a reversible orthogonal/unitary connection on the whole null fibers does not exist "
        "on this candidate base graph. Polar factors of rectangular overlaps would be partial "
        "isometries; immediate backtracks would not generally equal the identity.",
        "",
        "This does not prove that all null-sector holonomy is absent. It proves that a later audit must "
        "first identify a certified constant-rank subbundle, or explicitly define and justify a "
        "singular-transport category. Until then, no loop matrix is reported as holonomy.",
        "",
        "## Channel dimensions",
        "",
        "| channel | regime | chamber size | kernel dimension | Johnson degree |",
        "|---|---|---:|---:|---:|",
    ]
    for row in channels:
        lines.append(
            f"| {row['subset']} | {row['regime']} | {row['chamber_size']} | "
            f"{row['kernel_dimension']} | {row['johnson_degree_in_singular_graph']} |"
        )
    lines.extend([
        "",
        "## Integrity checks",
        "",
    ])
    for name, passed in checks.items():
        lines.append(f"- `{name}`: {passed}")
    lines.extend([
        "",
        "## Claim boundary",
        "",
        "This is an exact finite census and a definition-admissibility result at the audited n=9 scale. "
        "It does not identify null fibers, loops, or any future holonomy with a physical field, phase, "
        "particle, memory, or observable.",
        "",
    ])
    return "\n".join(lines)


def self_test() -> None:
    triangle = [(2, 3, 4), (2, 3, 5), (2, 4, 5)]
    edges = induced_edges(triangle)
    assert len(edges) == 3
    girth, loops = shortest_cycles(triangle, edges, 5)
    assert girth == 3 and len(loops) == 1
    assert canonical_cycle(tuple(reversed(loops[0]))) == loops[0]
    dimensions = {triangle[0]: 2, triangle[1]: 2, triangle[2]: 3}
    assert sum(dimensions[a] == dimensions[b] for a, b in edges) == 1
    assert connected_components(triangle, edges) == [sorted(triangle)]
    print("EHF-XBR-05A self-test PASS")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Lock the null-channel holonomy definition and census shortest loops."
    )
    parser.add_argument("--xbr04f6-dir")
    parser.add_argument("--out-dir", default="runs/ehf_xbr_05a")
    parser.add_argument("--max-loop-length", type=int, default=6)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0
    if not args.xbr04f6_dir:
        parser.error("--xbr04f6-dir is required")
    if args.max_loop_length < 3:
        parser.error("--max-loop-length must be at least 3")

    source_dir = Path(args.xbr04f6_dir).resolve()
    out_dir = Path(args.out_dir).resolve()
    ledger_path = source_dir / "kernel_channel_ledger.csv"
    summary_path = source_dir / "run_summary.json"
    source_summary = read_json(summary_path)
    source_rows = read_csv(ledger_path)

    by_subset: Dict[Subset, dict] = {}
    duplicate_subsets = False
    for row in source_rows:
        subset = parse_subset(row["subset"])
        if subset in by_subset:
            duplicate_subsets = True
        by_subset[subset] = row
    vertices = sorted(by_subset)
    edges = induced_edges(vertices)
    edge_set = {frozenset(edge) for edge in edges}
    dimensions = {
        subset: integer(
            row,
            "kernel_basis_dimension",
            "kernel_dimension",
            "chamber_adjacency_nullity",
        )
        for subset, row in by_subset.items()
    }
    chamber_sizes = {
        subset: integer(row, "source_chamber_size", "chamber_size")
        for subset, row in by_subset.items()
    }
    girth, minimal_loops = shortest_cycles(
        vertices, edges, args.max_loop_length
    )
    components = connected_components(vertices, edges)

    channel_rows: List[dict] = []
    for subset in vertices:
        degree = sum(subset in edge for edge in edges)
        source = by_subset[subset]
        channel_rows.append({
            "subset": subset_text(subset),
            "regime": source.get("regime", ""),
            "chamber_size": chamber_sizes[subset],
            "kernel_dimension": dimensions[subset],
            "johnson_degree_in_singular_graph": degree,
            "kernel_basis_sha256": source.get("kernel_basis_sha256", ""),
        })

    edge_rows: List[dict] = []
    equal_dimension_edges = 0
    for index, (left, right) in enumerate(edges):
        same_dimension = dimensions[left] == dimensions[right]
        equal_dimension_edges += int(same_dimension)
        edge_rows.append({
            "edge_index": index,
            "source_subset": subset_text(left),
            "target_subset": subset_text(right),
            "shared_labels": subset_text(sorted(set(left).intersection(right))),
            "removed_label": next(iter(set(left) - set(right))),
            "added_label": next(iter(set(right) - set(left))),
            "source_kernel_dimension": dimensions[left],
            "target_kernel_dimension": dimensions[right],
            "dimension_jump": dimensions[right] - dimensions[left],
            "constant_rank_whole_fiber": same_dimension,
            "ordinary_reversible_transport_admissible": same_dimension,
            "transport_status": (
                "unassigned_constant_rank_candidate"
                if same_dimension
                else "singular_dimension_change"
            ),
        })

    loop_rows: List[dict] = []
    for index, cycle in enumerate(minimal_loops):
        profile = [dimensions[vertex] for vertex in cycle]
        loop_edges = [
            (cycle[position], cycle[(position + 1) % len(cycle)])
            for position in range(len(cycle))
        ]
        constant_rank = len(set(profile)) == 1
        edge_admissible = all(
            dimensions[left] == dimensions[right]
            and frozenset((left, right)) in edge_set
            for left, right in loop_edges
        )
        loop_rows.append({
            "loop_index": index,
            "length": len(cycle),
            "loop_word": loop_word(cycle),
            "dimension_profile": ",".join(map(str, profile)),
            "constant_rank_loop": constant_rank,
            "all_edges_reversible_whole_fiber": edge_admissible,
            "holonomy_matrix_defined": False,
            "status": (
                "transport_definition_missing"
                if edge_admissible
                else "singular_dimension_change"
            ),
        })

    dimension_histogram = Counter(dimensions.values())
    component_sizes = [len(component) for component in components]
    no_reversible_edges = equal_dimension_edges == 0
    holonomy_defined = False
    reason = (
        "The candidate base graph contains loops, but it contains no "
        "constant-rank edge for the complete null fibers. Whole-fiber "
        "reversible holonomy is therefore not admissible."
        if no_reversible_edges
        else
        "Some constant-rank edges exist, but XBR-05A has not assigned a "
        "canonical gauge-covariant transport. Holonomy remains undefined."
    )

    checks = {
        "source_xbr04f6_strict_pass": truthy(source_summary.get("strict_pass")),
        "source_ledger_nonempty": bool(source_rows),
        "subsets_unique": not duplicate_subsets and len(vertices) == len(source_rows),
        "subsets_are_three_subsets_of_2_to_8": all(
            len(subset) == 3 and set(subset) <= set(range(2, 9))
            for subset in vertices
        ),
        "all_kernel_dimensions_positive": all(value > 0 for value in dimensions.values()),
        "aggregate_kernel_dimension_216": sum(dimensions.values()) == 216,
        "eleven_singular_channels": len(vertices) == 11,
        "induced_johnson_edge_count_29": len(edges) == 29,
        "singular_graph_connected": len(components) == 1,
        "shortest_loop_length_3": girth == 3,
        "minimal_triangle_count_24": len(minimal_loops) == 24,
        "no_equal_dimension_whole_fiber_edge": no_reversible_edges,
        "no_loop_falsely_assigned_holonomy": all(
            not row["holonomy_matrix_defined"] for row in loop_rows
        ),
    }
    strict_pass = all(checks.values())
    verdict = VERDICT_PASS if strict_pass else "EHF_XBR_05A_INTEGRITY_CHECK_FAILED"

    conclusion = {
        "base_graph": "induced Johnson J(7,3) graph on XBR-04F6 singular channels",
        "fiber": "complete exact chamber adjacency kernel K_A",
        "candidate_edge_relation": "Johnson distance one",
        "vertices": len(vertices),
        "edges": len(edges),
        "connected_components": len(components),
        "component_sizes": component_sizes,
        "shortest_loop_length": girth,
        "minimal_loop_count": len(minimal_loops),
        "equal_dimension_edges": equal_dimension_edges,
        "unequal_dimension_edges": len(edges) - equal_dimension_edges,
        "dimension_histogram": {
            str(key): value for key, value in sorted(dimension_histogram.items())
        },
        "holonomy_defined": holonomy_defined,
        "ordinary_whole_fiber_holonomy_admissible": not no_reversible_edges,
        "reason": reason,
        "next_gate": (
            "Identify and certify a constant-rank subbundle across a loop-rich "
            "subgraph, or define a singular-transport category with explicit "
            "backtrack and gauge laws."
        ),
    }
    summary = {
        "probe": PROBE_NAME,
        "title": "Null-Channel Holonomy Definition Lock and Minimal Loop Census",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "source": {
            "xbr04f6_directory": str(source_dir),
            "run_summary": str(summary_path),
            "kernel_channel_ledger": str(ledger_path),
            "kernel_channel_ledger_sha256": sha256_file(ledger_path),
        },
        "definition_lock": conclusion,
        "checks": checks,
        "strict_pass": strict_pass,
        "verdict": verdict,
        "claim_boundary": (
            "Exact finite n=9 definition and loop census only; no physical "
            "interpretation and no holonomy matrix asserted."
        ),
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / "null_channel_vertex_ledger.csv", channel_rows)
    write_csv(out_dir / "null_channel_edge_ledger.csv", edge_rows)
    write_csv(out_dir / "minimal_loop_ledger.csv", loop_rows)
    write_json(out_dir / "run_summary.json", summary)
    (out_dir / "report.md").write_text(
        markdown_report(
            channel_rows, edge_rows, loop_rows, checks, conclusion, verdict
        )
    )

    print("=" * 100)
    print("EHF-XBR-05A: NULL-CHANNEL HOLONOMY DEFINITION LOCK AND MINIMAL LOOP CENSUS")
    print("=" * 100)
    print(f"source channels:             {len(vertices)}")
    print(f"induced Johnson edges:       {len(edges)}")
    print(f"connected components:        {len(components)}")
    print(f"shortest loop length:        {girth}")
    print(f"shortest loops:              {len(minimal_loops)}")
    print(f"equal-dimension edges:       {equal_dimension_edges}")
    print(f"unequal-dimension edges:     {len(edges) - equal_dimension_edges}")
    print(f"holonomy defined:            {holonomy_defined}")
    print(f"strict checks:               {sum(checks.values())}/{len(checks)}")
    print(f"output directory:            {out_dir}")
    print(verdict)

    if args.strict and not strict_pass:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
