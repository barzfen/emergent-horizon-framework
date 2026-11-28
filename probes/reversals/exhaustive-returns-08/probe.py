"""Exhaust the seam-order slide graph and audit first-return reachability."""
from collections import Counter, deque
from functools import cache
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent / "pi-closure-06" / "probe.py"
spec = importlib.util.spec_from_file_location("rev06", PREVIOUS)
rev06 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rev06)
rev04, rev05 = rev06.rev04, rev06.rev05
AUDIT = HERE.parent / "carrier-audit-07" / "results.json"


def components(vertices, adjacent):
    unseen = set(vertices)
    groups = []
    while unseen:
        first = min(unseen)
        unseen.remove(first)
        group = [first]
        for vertex in group:
            for other in adjacent(vertex):
                if other in unseen:
                    unseen.remove(other)
                    group.append(other)
        groups.append(sorted(group))
    return groups


def run():
    data = json.loads(rev05.PARENT.read_text())
    carrier = data["carrier"]
    tours = carrier["states"]
    graphs = [rev04.cycle_edges(tour) for tour in tours]
    n = len(tours[0])
    even = set(data["Pi"])
    ones = set(data["ones"])
    assert all(set(tour[::2]) == even for tour in tours)
    original_index = {graph: i for i, graph in enumerate(graphs)}

    @cache
    def completed(graph):
        return all(len(ns) == 2 for ns in rev04.adjacency(graph, n))

    @cache
    def moves(graph):
        legal = []
        for target, (join, cut) in rev04.slides(graph, n, ones):
            if not rev06.compatible(join, even):
                continue
            if 0 in join or 0 in cut:
                anchor = sorted(b for a, b in target if a == 0)
                if len(anchor) == 2 and anchor[0] in even and anchor[1] not in even:
                    continue
            legal.append((target, (join, cut)))
        return tuple(legal)

    @cache
    def adjacent(graph):
        return frozenset(target for target, _ in moves(graph))

    # Multiple starting cycles permit a full census even if some lie in
    # different components. Completed cycles are expanded for this census.
    seen = set(graphs)
    frontier = list(graphs)
    for graph in frontier:
        for target in adjacent(graph):
            if target not in seen:
                seen.add(target)
                frontier.append(target)
    assert all(graph in adjacent(target) for graph in seen for target in adjacent(graph))
    completed_graphs = {graph for graph in seen if completed(graph)}
    for graph in completed_graphs:
        assert rev06.certificate(graph, rev04.adjacency(graph, n), even)
    extras = sorted(completed_graphs - set(graphs), key=lambda graph: sorted(graph))
    cycles = graphs + extras
    index = {graph: i for i, graph in enumerate(cycles)}

    def first_returns(source):
        paths = {source: ()}
        returned = {}
        queue = deque([source])
        while queue:
            graph = queue.popleft()
            for target, edit in moves(graph):
                if completed(target):
                    if target not in returned:
                        returned[target] = paths[graph] + (edit,)
                elif target not in paths:
                    paths[target] = paths[graph] + (edit,)
                    queue.append(target)
        return returned

    paths = [first_returns(source) for source in cycles]
    for i, returns in enumerate(paths):
        for graph, edits in returns.items():
            reverse = paths[index[graph]][cycles[i]]
            assert len(edits) == len(reverse)

    # Independently recover endpoint reachability from open components.
    open_graphs = seen - completed_graphs
    open_parts = components(open_graphs, adjacent)
    endpoint_neighbours = [set() for _ in cycles]
    boundary_sizes = Counter()
    for part in open_parts:
        boundary = {index[other] for graph in part
                    for other in adjacent(graph) if other in index}
        boundary_sizes[len(boundary)] += 1
        for i in boundary:
            endpoint_neighbours[i].update(boundary)
    for i, graph in enumerate(cycles):
        endpoint_neighbours[i].update(index[v] for v in adjacent(graph) if v in index)
        assert endpoint_neighbours[i] == {index[v] for v in paths[i]}

    previous = json.loads(AUDIT.read_text())
    blocked = []
    for entry in previous["directions"]:
        i, j = entry["source"], entry["target"]
        if i > j:
            continue
        route = paths[i].get(cycles[j])
        distance = len(route) if route is not None else None
        assert (distance is not None and distance <= 6) == entry["seam_first_return_within_six"]
        blocked.append({"source": i, "target": j, "minimum_slides": distance,
                        "witness": route})

    macro_parts = components(range(len(cycles)), endpoint_neighbours.__getitem__)
    short_parts = carrier["fast_groups"]
    short_group = {i: k for k, part in enumerate(short_parts) for i in part}
    quotient = [set() for _ in short_parts]
    for i in range(len(graphs)):
        for j in endpoint_neighbours[i]:
            if j in short_group:
                quotient[short_group[i]].add(short_group[j])
    quotient_parts = components(range(len(quotient)), quotient.__getitem__)

    first_return_edges = [
        [i, index[graph], len(route)] for i, returns in enumerate(paths)
        for graph, route in returns.items() if i < index[graph]
    ]
    summary = {
        "reachable_graph_states": len(seen),
        "open_graph_states": len(open_graphs),
        "open_components": len(open_parts),
        "open_component_boundary_size_histogram": dict(sorted(boundary_sizes.items())),
        "completed_cycles": len(cycles),
        "completed_cycles_outside_carrier": len(extras),
        "blocked_pair_minimum_slide_counts": dict(Counter(
            str(row["minimum_slides"]) if row["minimum_slides"] is not None else "unreachable"
            for row in blocked)),
        "first_return_edges_between_distinct_cycles": len(first_return_edges),
        "maximum_first_return_distance": max(distance for _, _, distance in first_return_edges),
        "first_return_component_sizes": sorted(map(len, macro_parts)),
        "short_region_quotient_components": quotient_parts,
    }
    assert len(original_index) == 96 and len(blocked) == 76
    return {
        "summary": summary,
        "source_sha256": hashlib.sha256(rev05.PARENT.read_bytes()).hexdigest(),
        "rev07_sha256": hashlib.sha256(AUDIT.read_bytes()).hexdigest(),
        "blocked_pairs": blocked,
        "first_return_edges": sorted(first_return_edges),
        "first_return_components": macro_parts,
        "extra_completed_graphs": [sorted(graph) for graph in extras],
    }


if __name__ == "__main__":
    result = run()
    (HERE / "results.json").write_text(json.dumps(result, separators=(",", ":")) + "\n")
    print(json.dumps(result["summary"], indent=2))
