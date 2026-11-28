#!/usr/bin/env python3
"""
EHF-XBR-05C: Exact Primitive Support-Graph and Longer-Loop Census

XBR-05A found 24 minimal triangles in the 11-channel Johnson base, but every
whole-kernel edge changes dimension. XBR-05B then found no exact primitive
type with constant multiplicity around a triangle (and one coarse-only
cross-group collision).

XBR-05C closes the remaining conventional-holonomy support question. For
every exactly certified primitive type tau and every multiplicity m occurring
in its channel support, it constructs the induced base graph on

    V(tau,m) = {A : multiplicity of tau in K_A is exactly m}.

The corresponding isotypic rank is d_tau*m. The probe computes connected
components, cycle rank E-V+C, girth, and the complete undirected simple-cycle
census on each support slice. A supported cycle is only a target for a later
transport construction: this script defines no edge map and computes no
holonomy matrix.

Coarse type collisions from XBR-05B are reconstructed in separate control
ledgers and can never contribute to the exact-support verdict.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Set, Tuple


SCRIPT_VERSION = "ehf_xbr_05c_v1_0_2026-07-31"
PROBE_NAME = "EHF-XBR-05C"
VERDICT_PASS = (
    "EHF_XBR_05C_EXACT_PRIMITIVE_SUPPORT_GRAPH_"
    "LONGER_LOOP_CENSUS_PASS"
)

Subset = Tuple[int, int, int]
Edge = Tuple[Subset, Subset]
Cycle = Tuple[Subset, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "pass", "passed"}


def integer(row: Mapping[str, object], *names: str) -> int:
    for name in names:
        value = row.get(name)
        if value not in (None, ""):
            return int(str(value))
    raise KeyError(f"none of the required integer fields is present: {names}")


def text_field(row: Mapping[str, object], *names: str) -> str:
    for name in names:
        value = row.get(name)
        if value not in (None, ""):
            return str(value).strip()
    return ""


def parse_subset(text: object) -> Subset:
    cleaned = str(text).strip()
    if (
        len(cleaned) >= 2
        and (cleaned[0], cleaned[-1]) in {("(", ")"), ("[", "]")}
    ):
        cleaned = cleaned[1:-1].strip()
    values = tuple(
        sorted(
            int(value.strip())
            for value in cleaned.split(",")
            if value.strip()
        )
    )
    if len(values) != 3 or len(set(values)) != 3:
        raise ValueError(f"invalid three-subset: {text!r}")
    if any(value not in range(2, 9) for value in values):
        raise ValueError(f"subset labels must lie in 2..8: {text!r}")
    return values  # type: ignore[return-value]


def subset_text(subset: Sequence[int]) -> str:
    return ",".join(map(str, subset))


def canonical_edge(left: Subset, right: Subset) -> Edge:
    if left == right:
        raise ValueError("an edge requires two distinct vertices")
    return (left, right) if left < right else (right, left)


def canonical_cycle(cycle: Sequence[Subset]) -> Cycle:
    values = tuple(cycle)
    if len(values) < 3 or len(set(values)) != len(values):
        raise ValueError(f"expected a simple cycle of length at least 3: {cycle!r}")
    orientations = (values, tuple(reversed(values)))
    candidates: List[Cycle] = []
    for orientation in orientations:
        for offset in range(len(orientation)):
            candidates.append(
                orientation[offset:] + orientation[:offset]
            )
    return min(candidates)


def cycle_word(cycle: Sequence[Subset]) -> str:
    closed = list(cycle) + [cycle[0]]
    return "->".join(subset_text(vertex) for vertex in closed)


def parse_semicolon_vertices(text: object) -> Cycle:
    vertices = tuple(
        parse_subset(piece)
        for piece in str(text).split(";")
        if piece.strip()
    )
    return canonical_cycle(vertices)


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


def write_csv(
    path: Path,
    rows: Sequence[Mapping[str, object]],
    *,
    fields_if_empty: Sequence[str] = (),
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    seen: Set[str] = set()
    for row in rows:
        for field in row:
            if field not in seen:
                seen.add(field)
                fields.append(field)
    if not fields:
        fields = list(fields_if_empty)
    if not fields:
        path.write_text("")
        return
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


def induced_edges(vertices: Iterable[Subset], base_edges: Set[Edge]) -> List[Edge]:
    vertex_set = set(vertices)
    return sorted(
        edge
        for edge in base_edges
        if edge[0] in vertex_set and edge[1] in vertex_set
    )


def adjacency(vertices: Iterable[Subset], edges: Iterable[Edge]) -> Dict[Subset, Set[Subset]]:
    result: Dict[Subset, Set[Subset]] = {
        vertex: set() for vertex in vertices
    }
    for left, right in edges:
        result[left].add(right)
        result[right].add(left)
    return result


def connected_components(
    vertices: Iterable[Subset],
    edges: Iterable[Edge],
) -> List[List[Subset]]:
    graph = adjacency(vertices, edges)
    unseen = set(graph)
    components: List[List[Subset]] = []
    while unseen:
        root = min(unseen)
        stack = [root]
        unseen.remove(root)
        component: List[Subset] = []
        while stack:
            current = stack.pop()
            component.append(current)
            for neighbor in sorted(graph[current], reverse=True):
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
        components.append(sorted(component))
    return sorted(components, key=lambda values: (values[0], len(values)))


def all_simple_cycles(
    vertices: Iterable[Subset],
    edges: Iterable[Edge],
    *,
    max_cycles: int,
) -> List[Cycle]:
    """Enumerate every undirected vertex-simple cycle exactly once."""
    vertex_list = sorted(set(vertices))
    graph = adjacency(vertex_list, edges)
    found: Set[Cycle] = set()

    def visit(
        start: Subset,
        current: Subset,
        path: List[Subset],
        seen: Set[Subset],
    ) -> None:
        for neighbor in sorted(graph[current]):
            if neighbor == start:
                if len(path) >= 3:
                    found.add(canonical_cycle(path))
                    if len(found) > max_cycles:
                        raise RuntimeError(
                            "simple-cycle census exceeded "
                            f"--max-enumerated-cycles-per-graph={max_cycles}"
                        )
                continue
            # Requiring start to be the least vertex eliminates all searches
            # rooted at a nonminimal member of the same undirected cycle.
            if neighbor <= start or neighbor in seen:
                continue
            visit(
                start,
                neighbor,
                path + [neighbor],
                seen | {neighbor},
            )

    for start in vertex_list:
        for neighbor in sorted(graph[start]):
            if neighbor > start:
                visit(start, neighbor, [start, neighbor], {start, neighbor})
    return sorted(found, key=lambda cycle: (len(cycle), cycle))


def cycle_is_valid(cycle: Cycle, edge_set: Set[Edge]) -> bool:
    if len(cycle) < 3 or len(set(cycle)) != len(cycle):
        return False
    return all(
        canonical_edge(cycle[index], cycle[(index + 1) % len(cycle)])
        in edge_set
        for index in range(len(cycle))
    )


def component_rows(
    *,
    support_graph_index: int,
    type_hash: str,
    multiplicity: int,
    primitive_dimension: int,
    vertices: Sequence[Subset],
    edges: Sequence[Edge],
    cycles: Sequence[Cycle],
) -> List[dict]:
    rows: List[dict] = []
    edge_set = set(edges)
    for component_index, component in enumerate(
        connected_components(vertices, edges)
    ):
        component_set = set(component)
        component_edges = [
            edge
            for edge in edges
            if edge[0] in component_set and edge[1] in component_set
        ]
        component_cycles = [
            cycle
            for cycle in cycles
            if set(cycle) <= component_set
        ]
        cycle_rank = len(component_edges) - len(component) + 1
        rows.append({
            "support_graph_index": support_graph_index,
            "component_index": component_index,
            "exact_primitive_type_hash": type_hash,
            "multiplicity": multiplicity,
            "primitive_dimension": primitive_dimension,
            "subbundle_rank": primitive_dimension * multiplicity,
            "vertex_count": len(component),
            "edge_count": len(component_edges),
            "cycle_rank": cycle_rank,
            "simple_cycle_count": len(component_cycles),
            "shortest_cycle_length": (
                min(map(len, component_cycles)) if component_cycles else ""
            ),
            "vertices": ";".join(subset_text(vertex) for vertex in component),
            "edges": ";".join(
                f"{subset_text(left)}--{subset_text(right)}"
                for left, right in component_edges
            ),
            "is_tree": cycle_rank == 0,
            "contains_closed_support_path": cycle_rank > 0,
            "all_component_cycles_valid": all(
                cycle_is_valid(cycle, edge_set)
                for cycle in component_cycles
            ),
        })
    return rows


def exact_support_census(
    final_rows: Sequence[Mapping[str, object]],
    base_edges: Set[Edge],
    *,
    max_cycles: int,
) -> Tuple[List[dict], List[dict], List[dict]]:
    by_type_vertex: Dict[
        str, Dict[Subset, List[Mapping[str, object]]]
    ] = defaultdict(lambda: defaultdict(list))
    for row in final_rows:
        type_hash = text_field(row, "exact_primitive_type_hash")
        if not type_hash:
            raise ValueError("final primitive row lacks exact type hash")
        by_type_vertex[type_hash][parse_subset(row["subset"])].append(row)

    support_rows: List[dict] = []
    components: List[dict] = []
    cycle_rows: List[dict] = []
    for type_hash, by_vertex in sorted(by_type_vertex.items()):
        flat = [row for values in by_vertex.values() for row in values]
        dimensions = {
            integer(row, "primitive_dimension") for row in flat
        }
        literal_groups = {
            text_field(row, "literal_group_hash") for row in flat
        }
        all_certified = all(
            truthy(row.get("rational_irreducible_certified"))
            for row in flat
        )
        if len(dimensions) != 1:
            raise ValueError(
                f"exact type {type_hash!r} has nonunique dimensions: "
                f"{sorted(dimensions)}"
            )
        primitive_dimension = next(iter(dimensions))
        multiplicity_by_vertex = {
            vertex: len(rows) for vertex, rows in by_vertex.items()
        }
        for multiplicity in sorted(set(multiplicity_by_vertex.values())):
            support_vertices = sorted(
                vertex
                for vertex, value in multiplicity_by_vertex.items()
                if value == multiplicity
            )
            support_edges = induced_edges(support_vertices, base_edges)
            support_components = connected_components(
                support_vertices, support_edges
            )
            cycles = all_simple_cycles(
                support_vertices,
                support_edges,
                max_cycles=max_cycles,
            )
            cycle_rank = (
                len(support_edges)
                - len(support_vertices)
                + len(support_components)
            )
            support_graph_index = len(support_rows)
            exact_identity = (
                all_certified
                and len(literal_groups) == 1
                and bool(next(iter(literal_groups), ""))
            )
            support_rows.append({
                "support_graph_index": support_graph_index,
                "exact_primitive_type_hash": type_hash,
                "primitive_dimension": primitive_dimension,
                "multiplicity": multiplicity,
                "subbundle_rank": primitive_dimension * multiplicity,
                "occurrence_count_on_slice": (
                    multiplicity * len(support_vertices)
                ),
                "vertex_count": len(support_vertices),
                "edge_count": len(support_edges),
                "connected_component_count": len(support_components),
                "component_sizes": ";".join(
                    map(str, sorted(map(len, support_components), reverse=True))
                ),
                "cycle_rank": cycle_rank,
                "simple_cycle_count": len(cycles),
                "shortest_cycle_length": (
                    min(map(len, cycles)) if cycles else ""
                ),
                "vertices": ";".join(
                    subset_text(vertex) for vertex in support_vertices
                ),
                "edges": ";".join(
                    f"{subset_text(left)}--{subset_text(right)}"
                    for left, right in support_edges
                ),
                "all_blocks_rationally_irreducible_certified": all_certified,
                "literal_group_hash_count_for_exact_type": len(literal_groups),
                "exact_identity_certified": exact_identity,
                "constant_rank_by_construction": True,
                "support_graph_is_forest": cycle_rank == 0,
                "contains_closed_support_path": cycle_rank > 0,
                "canonical_edge_transport_defined": False,
                "holonomy_matrix_computed": False,
            })
            components.extend(
                component_rows(
                    support_graph_index=support_graph_index,
                    type_hash=type_hash,
                    multiplicity=multiplicity,
                    primitive_dimension=primitive_dimension,
                    vertices=support_vertices,
                    edges=support_edges,
                    cycles=cycles,
                )
            )
            for local_index, cycle in enumerate(cycles):
                cycle_rows.append({
                    "support_graph_index": support_graph_index,
                    "cycle_index_within_support_graph": local_index,
                    "exact_primitive_type_hash": type_hash,
                    "primitive_dimension": primitive_dimension,
                    "multiplicity": multiplicity,
                    "subbundle_rank": primitive_dimension * multiplicity,
                    "length": len(cycle),
                    "loop_word": cycle_word(cycle),
                    "vertices": ";".join(
                        subset_text(vertex) for vertex in cycle
                    ),
                    "exact_constant_multiplicity_support_certified": (
                        exact_identity
                    ),
                    "edge_transport_certificates_required": len(cycle),
                    "canonical_edge_transport_defined": False,
                    "holonomy_matrix_computed": False,
                    "status": (
                        "closed_exact_support_path_transport_not_defined"
                    ),
                })
    return support_rows, components, cycle_rows


def coarse_control_census(
    final_rows: Sequence[Mapping[str, object]],
    source_control_rows: Sequence[Mapping[str, object]],
    base_edges: Set[Edge],
    *,
    max_cycles: int,
) -> Tuple[List[dict], List[dict], List[dict]]:
    controlled_hashes = sorted({
        text_field(row, "coarse_primitive_type_hash")
        for row in source_control_rows
        if text_field(row, "coarse_primitive_type_hash")
    })
    by_hash_vertex: Dict[
        str, Dict[Subset, List[Mapping[str, object]]]
    ] = defaultdict(lambda: defaultdict(list))
    for row in final_rows:
        coarse_hash = text_field(row, "coarse_primitive_type_hash")
        if coarse_hash in controlled_hashes:
            by_hash_vertex[coarse_hash][parse_subset(row["subset"])].append(row)

    graph_rows: List[dict] = []
    cycle_rows: List[dict] = []
    cycle_keys: Set[Tuple[str, Cycle]] = set()
    for coarse_hash in controlled_hashes:
        by_vertex = by_hash_vertex[coarse_hash]
        vertices = sorted(by_vertex)
        edges = induced_edges(vertices, base_edges)
        components = connected_components(vertices, edges)
        cycles = all_simple_cycles(vertices, edges, max_cycles=max_cycles)
        exact_hashes = sorted({
            text_field(row, "exact_primitive_type_hash")
            for rows in by_vertex.values()
            for row in rows
        })
        cycle_rank = len(edges) - len(vertices) + len(components)
        graph_rows.append({
            "coarse_primitive_type_hash": coarse_hash,
            "vertex_count": len(vertices),
            "edge_count": len(edges),
            "connected_component_count": len(components),
            "cycle_rank": cycle_rank,
            "simple_cycle_count": len(cycles),
            "shortest_cycle_length": min(map(len, cycles)) if cycles else "",
            "distinct_exact_primitive_type_count": len(exact_hashes),
            "exact_primitive_type_hashes": ";".join(exact_hashes),
            "vertices": ";".join(subset_text(vertex) for vertex in vertices),
            "candidate_only": True,
            "certified_common_module": False,
            "counted_as_exact_support": False,
            "holonomy_matrix_computed": False,
            "reason": (
                "coarse_cross_group_recurrence_is_not_an_exact_"
                "primitive_module_identity"
            ),
        })
        for local_index, cycle in enumerate(cycles):
            cycle_keys.add((coarse_hash, canonical_cycle(cycle)))
            cycle_rows.append({
                "coarse_primitive_type_hash": coarse_hash,
                "cycle_index_within_control_graph": local_index,
                "length": len(cycle),
                "loop_word": cycle_word(cycle),
                "vertices": ";".join(
                    subset_text(vertex) for vertex in cycle
                ),
                "multiplicity_profile": ";".join(
                    str(len(by_vertex[vertex])) for vertex in cycle
                ),
                "exact_type_profile": "|".join(
                    subset_text(vertex)
                    + ":"
                    + ",".join(sorted({
                        text_field(row, "exact_primitive_type_hash")
                        for row in by_vertex[vertex]
                    }))
                    for vertex in cycle
                ),
                "candidate_only": True,
                "certified_common_module": False,
                "counted_as_exact_support": False,
                "canonical_edge_transport_defined": False,
                "holonomy_matrix_computed": False,
            })

    reproduction_rows: List[dict] = []
    for row_index, row in enumerate(source_control_rows):
        coarse_hash = text_field(row, "coarse_primitive_type_hash")
        triangle = parse_semicolon_vertices(row["triangle"])
        reproduced = (coarse_hash, triangle) in cycle_keys
        reproduction_rows.append({
            "source_control_row_index": row_index,
            "source_triangle_index": row.get("triangle_index", ""),
            "coarse_primitive_type_hash": coarse_hash,
            "triangle": ";".join(subset_text(vertex) for vertex in triangle),
            "reproduced_in_coarse_support_graph": reproduced,
            "candidate_only": True,
            "counted_as_exact_support": False,
        })
    return graph_rows, cycle_rows, reproduction_rows


def exact_triangle_keys_from_05b(
    rows: Sequence[Mapping[str, object]],
) -> Set[Tuple[str, Cycle, int]]:
    result: Set[Tuple[str, Cycle, int]] = set()
    for row in rows:
        if not truthy(row.get("exact_primitive_persistence")):
            continue
        profile = [
            int(piece)
            for piece in text_field(row, "multiplicity_profile").split(";")
            if piece
        ]
        if not profile or len(set(profile)) != 1:
            raise ValueError(
                "05B exact persistence row lacks constant multiplicity"
            )
        result.add((
            text_field(row, "exact_primitive_type_hash"),
            parse_semicolon_vertices(row["triangle"]),
            profile[0],
        ))
    return result


def exact_triangle_keys_from_05c(
    cycle_rows: Sequence[Mapping[str, object]],
) -> Set[Tuple[str, Cycle, int]]:
    return {
        (
            text_field(row, "exact_primitive_type_hash"),
            parse_semicolon_vertices(row["vertices"]),
            integer(row, "multiplicity"),
        )
        for row in cycle_rows
        if integer(row, "length") == 3
    }


def markdown_report(
    summary: Mapping[str, object],
    support_rows: Sequence[Mapping[str, object]],
    cycle_rows: Sequence[Mapping[str, object]],
    coarse_graph_rows: Sequence[Mapping[str, object]],
    checks: Mapping[str, bool],
) -> str:
    counts = summary["counts"]  # type: ignore[index]
    scientific = summary["scientific_conclusion"]  # type: ignore[index]
    cyclic_supports = [
        row for row in support_rows if integer(row, "cycle_rank") > 0
    ]
    lines = [
        "# EHF-XBR-05C: Exact Primitive Support-Graph and Longer-Loop Census",
        "",
        f"Integrity verdict: `{summary['verdict']}`",
        "",
        f"Scientific outcome: `{scientific['status']}`",  # type: ignore[index]
        "",
        "## Definition lock",
        "",
        "For each exact primitive type and each multiplicity actually present, "
        "the probe takes the induced Johnson support graph. The resulting "
        "isotypic rank is constant by construction.",
        "",
        "A cycle in this graph certifies only a closed support path. It does "
        "not define edge transport or holonomy.",
        "",
        "## Census",
        "",
        f"- final certified primitive blocks: {counts['final_primitive_blocks']}",  # type: ignore[index]
        f"- exact primitive types: {counts['exact_primitive_types']}",  # type: ignore[index]
        f"- exact type/multiplicity support graphs: {counts['exact_support_graphs']}",  # type: ignore[index]
        f"- cyclic exact support graphs: {counts['cyclic_exact_support_graphs']}",  # type: ignore[index]
        f"- exact supported simple cycles: {counts['exact_supported_simple_cycles']}",  # type: ignore[index]
        f"- shortest exact supported cycle: {counts['shortest_exact_supported_cycle']}",  # type: ignore[index]
        f"- coarse-only control graphs: {counts['coarse_control_graphs']}",  # type: ignore[index]
        f"- coarse-only control cycles: {counts['coarse_control_cycles']}",  # type: ignore[index]
        "",
        "## Cyclic exact support graphs",
        "",
    ]
    if cyclic_supports:
        lines.extend([
            "| type hash | dim | multiplicity | rank | V | E | components | cycle rank | simple cycles | shortest |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ])
        for row in cyclic_supports:
            lines.append(
                f"| `{row['exact_primitive_type_hash']}` | "
                f"{row['primitive_dimension']} | {row['multiplicity']} | "
                f"{row['subbundle_rank']} | {row['vertex_count']} | "
                f"{row['edge_count']} | {row['connected_component_count']} | "
                f"{row['cycle_rank']} | {row['simple_cycle_count']} | "
                f"{row['shortest_cycle_length']} |"
            )
    else:
        lines.append(
            "Every exact constant-multiplicity primitive support graph is a forest."
        )
    lines.extend([
        "",
        "## Exact supported cycles",
        "",
    ])
    if cycle_rows:
        lines.extend([
            "| length | rank | loop | transport defined | holonomy computed |",
            "|---:|---:|---|---|---|",
        ])
        for row in cycle_rows:
            lines.append(
                f"| {row['length']} | {row['subbundle_rank']} | "
                f"`{row['loop_word']}` | "
                f"{row['canonical_edge_transport_defined']} | "
                f"{row['holonomy_matrix_computed']} |"
            )
    else:
        lines.append("No exact primitive support slice contains a closed path.")
    lines.extend([
        "",
        "## Coarse controls",
        "",
        f"{len(coarse_graph_rows)} coarse collision graph(s) were kept separate. "
        "They are not certified common modules and do not affect the exact verdict.",
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
        str(summary["claim_boundary"]),
        "",
    ])
    return "\n".join(lines)


def self_test() -> None:
    assert parse_subset("2,3,4") == (2, 3, 4)
    assert parse_subset("(4, 2, 3)") == (2, 3, 4)
    assert parse_subset("[3, 4, 2]") == (2, 3, 4)

    a = (2, 3, 4)
    b = (2, 3, 5)
    c = (2, 4, 5)
    d = (3, 4, 5)
    vertices = [a, b, c, d]
    # A square with one diagonal has cycle rank 2 but three simple cycles:
    # two triangles and the perimeter square.
    edges = {
        canonical_edge(a, b),
        canonical_edge(b, d),
        canonical_edge(d, c),
        canonical_edge(c, a),
        canonical_edge(a, d),
    }
    cycles = all_simple_cycles(vertices, edges, max_cycles=100)
    assert len(cycles) == 3
    assert sorted(map(len, cycles)) == [3, 3, 4]
    assert all(cycle_is_valid(cycle, edges) for cycle in cycles)
    assert len(edges) - len(vertices) + 1 == 2

    rows: List[dict] = []
    for vertex in vertices:
        rows.append({
            "subset": subset_text(vertex),
            "primitive_dimension": 2,
            "rational_irreducible_certified": True,
            "literal_group_hash": "g-cycle",
            "exact_primitive_type_hash": "exact-cycle",
            "coarse_primitive_type_hash": "coarse-cycle",
        })
    # A second copy at one vertex must be split into m=1 and m=2 slices;
    # it cannot be silently selected as a rank-2 copy on the m=1 slice.
    rows.append(dict(rows[0]))
    # A separate exact type remains at multiplicity one on all four vertices
    # and must recover all three supported simple cycles.
    for vertex in vertices:
        rows.append({
            "subset": subset_text(vertex),
            "primitive_dimension": 1,
            "rational_irreducible_certified": True,
            "literal_group_hash": "g-full-cycle",
            "exact_primitive_type_hash": "exact-full-cycle",
            "coarse_primitive_type_hash": "coarse-full-cycle",
        })
    support, components, supported_cycles = exact_support_census(
        rows, edges, max_cycles=100
    )
    assert len(support) == 3
    split_rows = [
        row
        for row in support
        if text_field(row, "exact_primitive_type_hash") == "exact-cycle"
    ]
    m1 = next(row for row in split_rows if integer(row, "multiplicity") == 1)
    m2 = next(row for row in split_rows if integer(row, "multiplicity") == 2)
    assert integer(m1, "vertex_count") == 3
    assert integer(m2, "vertex_count") == 1
    full_cycles = [
        row
        for row in supported_cycles
        if text_field(row, "exact_primitive_type_hash") == "exact-full-cycle"
    ]
    assert len(full_cycles) == 3
    assert sorted(integer(row, "length") for row in full_cycles) == [3, 3, 4]
    assert all(integer(row, "multiplicity") == 1 for row in full_cycles)
    assert all(
        not truthy(row["holonomy_matrix_computed"])
        for row in (*support, *supported_cycles)
    )
    assert all(integer(row, "cycle_rank") >= 0 for row in components)
    print("EHF-XBR-05C self-test PASS")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Census exact constant-multiplicity primitive support graphs "
            "and every supported simple cycle."
        )
    )
    parser.add_argument("--xbr05a-dir")
    parser.add_argument("--xbr05b-dir")
    parser.add_argument("--out-dir", default="runs/ehf_xbr_05c")
    parser.add_argument(
        "--max-enumerated-cycles-per-graph",
        type=int,
        default=100000,
    )
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0
    if not args.xbr05a_dir or not args.xbr05b_dir:
        parser.error("--xbr05a-dir and --xbr05b-dir are required")
    if args.max_enumerated_cycles_per_graph < 1:
        parser.error("--max-enumerated-cycles-per-graph must be positive")

    xbr05a_dir = Path(args.xbr05a_dir).resolve()
    xbr05b_dir = Path(args.xbr05b_dir).resolve()
    out_dir = Path(args.out_dir).resolve()
    paths = {
        "xbr05a_summary": xbr05a_dir / "run_summary.json",
        "xbr05a_vertices": xbr05a_dir / "null_channel_vertex_ledger.csv",
        "xbr05a_edges": xbr05a_dir / "null_channel_edge_ledger.csv",
        "xbr05b_summary": xbr05b_dir / "run_summary.json",
        "xbr05b_final_primitives": (
            xbr05b_dir / "final_primitive_module_ledger.csv"
        ),
        "xbr05b_persistence": (
            xbr05b_dir / "primitive_type_persistence_ledger.csv"
        ),
        "xbr05b_exact_triangle_candidates": (
            xbr05b_dir / "exact_triangle_subbundle_candidate_ledger.csv"
        ),
        "xbr05b_coarse_triangle_controls": (
            xbr05b_dir / "coarse_triangle_candidate_control_ledger.csv"
        ),
    }
    for path in paths.values():
        if not path.exists():
            raise FileNotFoundError(path)

    summary_05a = read_json(paths["xbr05a_summary"])
    vertex_rows = read_csv(paths["xbr05a_vertices"])
    edge_rows = read_csv(paths["xbr05a_edges"])
    summary_05b = read_json(paths["xbr05b_summary"])
    final_rows = read_csv(paths["xbr05b_final_primitives"])
    persistence_rows_05b = read_csv(paths["xbr05b_persistence"])
    exact_triangle_rows_05b = read_csv(
        paths["xbr05b_exact_triangle_candidates"]
    )
    coarse_triangle_rows_05b = read_csv(
        paths["xbr05b_coarse_triangle_controls"]
    )

    vertices: Dict[Subset, int] = {}
    duplicate_vertices = False
    for row in vertex_rows:
        vertex = parse_subset(row["subset"])
        duplicate_vertices |= vertex in vertices
        vertices[vertex] = integer(row, "kernel_dimension")

    base_edges: Set[Edge] = set()
    duplicate_edges = False
    for row in edge_rows:
        edge = canonical_edge(
            parse_subset(row["source_subset"]),
            parse_subset(row["target_subset"]),
        )
        duplicate_edges |= edge in base_edges
        base_edges.add(edge)

    support_rows, component_ledger, exact_cycle_rows = exact_support_census(
        final_rows,
        base_edges,
        max_cycles=args.max_enumerated_cycles_per_graph,
    )
    (
        coarse_graph_rows,
        coarse_cycle_rows,
        coarse_reproduction_rows,
    ) = coarse_control_census(
        final_rows,
        coarse_triangle_rows_05b,
        base_edges,
        max_cycles=args.max_enumerated_cycles_per_graph,
    )

    final_by_vertex: Dict[Subset, List[Mapping[str, object]]] = defaultdict(list)
    for row in final_rows:
        final_by_vertex[parse_subset(row["subset"])].append(row)
    channel_dimension_sums = {
        vertex: sum(
            integer(row, "primitive_dimension")
            for row in final_by_vertex.get(vertex, [])
        )
        for vertex in vertices
    }
    exact_hashes = {
        text_field(row, "exact_primitive_type_hash") for row in final_rows
    }
    dimensions_by_hash: Dict[str, Set[int]] = defaultdict(set)
    groups_by_hash: Dict[str, Set[str]] = defaultdict(set)
    for row in final_rows:
        type_hash = text_field(row, "exact_primitive_type_hash")
        dimensions_by_hash[type_hash].add(integer(row, "primitive_dimension"))
        groups_by_hash[type_hash].add(text_field(row, "literal_group_hash"))

    source_05b_counts = summary_05b.get("counts", {})
    locked_05b_outcome = (
        integer(source_05b_counts, "exact_persistence_candidates") == 0
        and integer(source_05b_counts, "triangles_with_exact_persistence") == 0
        and integer(source_05b_counts, "coarse_only_triangle_candidates") == 1
    )
    exact_triangles_05b = exact_triangle_keys_from_05b(
        exact_triangle_rows_05b
    )
    exact_triangles_05c = exact_triangle_keys_from_05c(exact_cycle_rows)

    support_graphs_with_cycles = [
        row for row in support_rows if integer(row, "cycle_rank") > 0
    ]
    shortest_exact_cycle = (
        min(integer(row, "length") for row in exact_cycle_rows)
        if exact_cycle_rows
        else None
    )
    all_support_edges_induced = all(
        integer(row, "edge_count")
        == len(induced_edges(
            [
                parse_subset(piece)
                for piece in text_field(row, "vertices").split(";")
                if piece
            ],
            base_edges,
        ))
        for row in support_rows
    )
    exact_cycle_edge_set = {
        canonical_edge(
            parse_subset(row["source_subset"]),
            parse_subset(row["target_subset"]),
        )
        for row in edge_rows
    }

    checks = {
        "source_xbr05a_strict_pass": truthy(summary_05a.get("strict_pass")),
        "source_xbr05b_strict_pass": truthy(summary_05b.get("strict_pass")),
        "source_xbr05b_locked_zero_exact_one_coarse_triangle_result": (
            locked_05b_outcome
        ),
        "eleven_unique_null_channel_vertices_loaded": (
            not duplicate_vertices and len(vertices) == 11
        ),
        "twenty_nine_unique_base_edges_loaded": (
            not duplicate_edges and len(base_edges) == 29
        ),
        "all_base_edges_join_known_johnson_adjacent_vertices": all(
            left in vertices
            and right in vertices
            and len(set(left).intersection(right)) == 2
            for left, right in base_edges
        ),
        "final_primitive_count_matches_xbr05b": (
            len(final_rows)
            == integer(source_05b_counts, "final_primitive_blocks")
        ),
        "exact_type_count_matches_xbr05b": (
            len(exact_hashes)
            == integer(source_05b_counts, "exact_primitive_types")
            == len(persistence_rows_05b)
        ),
        "all_final_primitives_certified_and_typed": all(
            truthy(row.get("rational_irreducible_certified"))
            and text_field(row, "exact_primitive_type_hash")
            and text_field(row, "coarse_primitive_type_hash")
            and text_field(row, "literal_group_hash")
            for row in final_rows
        ),
        "all_final_primitive_channels_are_base_vertices": (
            set(final_by_vertex) == set(vertices)
        ),
        "per_channel_primitive_dimensions_reconstruct_null_fibers": all(
            channel_dimension_sums[vertex] == vertices[vertex]
            for vertex in vertices
        ),
        "final_primitive_dimensions_sum_to_216": sum(
            integer(row, "primitive_dimension") for row in final_rows
        )
        == 216,
        "exact_type_hash_has_unique_dimension_and_literal_group": all(
            len(dimensions_by_hash[type_hash]) == 1
            and len(groups_by_hash[type_hash]) == 1
            and bool(next(iter(groups_by_hash[type_hash]), ""))
            for type_hash in exact_hashes
        ),
        "every_exact_type_multiplicity_slice_censused_once": (
            len({
                (
                    text_field(row, "exact_primitive_type_hash"),
                    integer(row, "multiplicity"),
                )
                for row in support_rows
            })
            == len(support_rows)
        ),
        "every_support_graph_is_the_full_induced_subgraph": (
            all_support_edges_induced
        ),
        "all_component_cycle_ranks_are_exact_and_nonnegative": all(
            integer(row, "cycle_rank")
            == integer(row, "edge_count") - integer(row, "vertex_count") + 1
            and integer(row, "cycle_rank") >= 0
            for row in component_ledger
        ),
        "support_cycle_rank_zero_iff_no_simple_cycle": all(
            (integer(row, "cycle_rank") == 0)
            == (integer(row, "simple_cycle_count") == 0)
            for row in support_rows
        ),
        "all_enumerated_exact_cycles_are_unique_valid_base_cycles": (
            len({
                (
                    text_field(row, "exact_primitive_type_hash"),
                    integer(row, "multiplicity"),
                    parse_semicolon_vertices(row["vertices"]),
                )
                for row in exact_cycle_rows
            })
            == len(exact_cycle_rows)
            and all(
                cycle_is_valid(
                    parse_semicolon_vertices(row["vertices"]),
                    exact_cycle_edge_set,
                )
                for row in exact_cycle_rows
            )
        ),
        "exact_triangle_census_reproduces_xbr05b": (
            exact_triangles_05c == exact_triangles_05b
        ),
        "coarse_control_count_matches_xbr05b": (
            len(coarse_triangle_rows_05b)
            == integer(
                source_05b_counts, "coarse_only_triangle_candidates"
            )
        ),
        "every_xbr05b_coarse_triangle_reproduced_as_control_cycle": all(
            truthy(row["reproduced_in_coarse_support_graph"])
            for row in coarse_reproduction_rows
        ),
        "no_coarse_control_promoted_to_exact_support": all(
            not truthy(row["counted_as_exact_support"])
            for row in (*coarse_graph_rows, *coarse_cycle_rows)
        ),
        "no_edge_transport_or_holonomy_matrix_computed": all(
            not truthy(row["canonical_edge_transport_defined"])
            and not truthy(row["holonomy_matrix_computed"])
            for row in (*support_rows, *exact_cycle_rows)
        ),
    }
    strict_pass = all(checks.values())
    verdict = (
        VERDICT_PASS
        if strict_pass
        else "EHF_XBR_05C_INTEGRITY_CHECK_FAILED"
    )

    if exact_cycle_rows:
        scientific_status = (
            "exact_longer_loop_support_found_transport_not_defined"
        )
        scientific_reason = (
            "At least one exact primitive type has a constant-multiplicity "
            "support graph containing a closed path. This is a legitimate "
            "target for constructing exact cross-channel edge transports, "
            "but no connection or holonomy is yet defined."
        )
        next_gate = (
            "Construct canonical reversible comparison maps on every edge "
            "of the shortest exact supported cycle, then certify reversal, "
            "immediate backtracks, gauge covariance, and provenance before "
            "any loop product."
        )
    elif coarse_cycle_rows:
        scientific_status = (
            "all_exact_support_graphs_are_forests_coarse_cycles_only"
        )
        scientific_reason = (
            "Every exact constant-multiplicity primitive support graph is a "
            "forest. Closed recurrence exists only after collapsing distinct "
            "exact representation types into a coarse signature, so it cannot "
            "support conventional primitive null-channel holonomy."
        )
        next_gate = (
            "Close the conventional exact-primitive holonomy route at n=9. "
            "Any continuation must define a different canonical subbundle or "
            "an explicit singular-transport or flag framework."
        )
    else:
        scientific_status = "all_exact_primitive_support_graphs_are_forests"
        scientific_reason = (
            "No exact constant-multiplicity primitive support graph contains "
            "a closed path of any length."
        )
        next_gate = (
            "Close the conventional exact-primitive holonomy route at n=9, "
            "or introduce and independently justify a different canonical "
            "fiber and transport law."
        )

    counts = {
        "null_channel_vertices": len(vertices),
        "base_edges": len(base_edges),
        "final_primitive_blocks": len(final_rows),
        "exact_primitive_types": len(exact_hashes),
        "exact_support_graphs": len(support_rows),
        "exact_support_components": len(component_ledger),
        "cyclic_exact_support_graphs": len(support_graphs_with_cycles),
        "exact_supported_simple_cycles": len(exact_cycle_rows),
        "shortest_exact_supported_cycle": (
            shortest_exact_cycle if shortest_exact_cycle is not None else "none"
        ),
        "exact_supported_triangles": sum(
            integer(row, "length") == 3 for row in exact_cycle_rows
        ),
        "exact_supported_longer_cycles": sum(
            integer(row, "length") >= 4 for row in exact_cycle_rows
        ),
        "coarse_source_triangle_controls": len(coarse_triangle_rows_05b),
        "coarse_control_graphs": len(coarse_graph_rows),
        "coarse_control_cycles": len(coarse_cycle_rows),
    }
    summary = {
        "probe": PROBE_NAME,
        "title": "Exact Primitive Support-Graph and Longer-Loop Census",
        "script_version": SCRIPT_VERSION,
        "utc_completed": utc_now(),
        "sources": {
            name: {
                "path": str(path),
                "sha256": sha256_file(path),
            }
            for name, path in paths.items()
        },
        "definition_lock": {
            "base_graph": (
                "XBR-05A induced Johnson graph on 11 singular channels"
            ),
            "fiber_slice": (
                "exact F8/F8B primitive isotypic support at fixed channel "
                "multiplicity m"
            ),
            "subbundle_rank": "primitive_dimension times multiplicity",
            "edge_relation": "full induced XBR-05A base-edge relation",
            "closed_path_test": "cycle rank E-V+C and complete simple cycles",
            "transport_defined": False,
            "holonomy_computed": False,
        },
        "counts": counts,
        "scientific_conclusion": {
            "status": scientific_status,
            "reason": scientific_reason,
            "conventional_closed_exact_support_path_available": bool(
                exact_cycle_rows
            ),
            "canonical_edge_transport_defined": False,
            "holonomy_computed": False,
            "next_gate": next_gate,
        },
        "checks": checks,
        "strict_pass": strict_pass,
        "verdict": verdict,
        "claim_boundary": (
            "Exact finite n=9 primitive support-graph and simple-cycle census "
            "only. A closed exact support path is not a connection; a coarse "
            "collision is not a module identity; no edge transport, holonomy "
            "matrix, physical phase, gauge field, particle, memory, or "
            "observable is asserted."
        ),
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        out_dir / "exact_primitive_support_graph_ledger.csv",
        support_rows,
    )
    write_csv(
        out_dir / "exact_primitive_support_component_ledger.csv",
        component_ledger,
    )
    write_csv(
        out_dir / "exact_primitive_simple_cycle_ledger.csv",
        exact_cycle_rows,
        fields_if_empty=(
            "support_graph_index",
            "exact_primitive_type_hash",
            "primitive_dimension",
            "multiplicity",
            "subbundle_rank",
            "length",
            "loop_word",
            "canonical_edge_transport_defined",
            "holonomy_matrix_computed",
        ),
    )
    write_csv(
        out_dir / "coarse_support_graph_control_ledger.csv",
        coarse_graph_rows,
        fields_if_empty=(
            "coarse_primitive_type_hash",
            "vertex_count",
            "edge_count",
            "cycle_rank",
            "candidate_only",
            "counted_as_exact_support",
        ),
    )
    write_csv(
        out_dir / "coarse_simple_cycle_control_ledger.csv",
        coarse_cycle_rows,
        fields_if_empty=(
            "coarse_primitive_type_hash",
            "length",
            "loop_word",
            "candidate_only",
            "counted_as_exact_support",
            "holonomy_matrix_computed",
        ),
    )
    write_csv(
        out_dir / "coarse_triangle_reproduction_ledger.csv",
        coarse_reproduction_rows,
        fields_if_empty=(
            "source_control_row_index",
            "coarse_primitive_type_hash",
            "triangle",
            "reproduced_in_coarse_support_graph",
            "candidate_only",
            "counted_as_exact_support",
        ),
    )
    write_json(out_dir / "run_summary.json", summary)
    (out_dir / "report.md").write_text(
        markdown_report(
            summary,
            support_rows,
            exact_cycle_rows,
            coarse_graph_rows,
            checks,
        )
    )

    print("=" * 108)
    print(
        "EHF-XBR-05C: EXACT PRIMITIVE SUPPORT-GRAPH "
        "AND LONGER-LOOP CENSUS"
    )
    print("=" * 108)
    print(f"final certified primitives:       {len(final_rows)}")
    print(f"exact primitive types:            {len(exact_hashes)}")
    print(f"type/multiplicity support graphs: {len(support_rows)}")
    print(
        f"cyclic exact support graphs:      "
        f"{len(support_graphs_with_cycles)}"
    )
    print(f"exact supported simple cycles:    {len(exact_cycle_rows)}")
    print(
        "shortest exact supported cycle:  "
        + (
            str(shortest_exact_cycle)
            if shortest_exact_cycle is not None
            else "none"
        )
    )
    print(f"coarse-only control graphs:       {len(coarse_graph_rows)}")
    print(f"coarse-only control cycles:       {len(coarse_cycle_rows)}")
    print(f"scientific outcome:               {scientific_status}")
    print(f"holonomy matrices computed:       0")
    print(f"strict checks:                    {sum(checks.values())}/{len(checks)}")
    print(f"output directory:                 {out_dir}")
    print(verdict)

    if args.strict and not strict_pass:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
