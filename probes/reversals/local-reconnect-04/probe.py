"""Bounded local reconnection audit on the REV-02 carrier."""
from collections import Counter, deque
from itertools import permutations
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "rare-channel-02" / "results.json"


def edge(a, b):
    return tuple(sorted((a, b)))


def cycle_edges(cycle):
    return frozenset(edge(a, b) for a, b in zip(cycle, cycle[1:] + cycle[:1]))


def adjacency(edges, n):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def distance(adj, start, end):
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        vertex, steps = queue.popleft()
        if vertex == end:
            return steps
        for other in adj[vertex] - seen:
            seen.add(other)
            queue.append((other, steps + 1))
    return None


def admissible(adj, ones):
    return all(
        len(neighbours) <= 3
        and any((v in ones) == (w in ones) for w in neighbours)
        for v, neighbours in enumerate(adj)
    ) and all(distance(adj, 0, v) is not None for v in range(len(adj)))


def direct_schedules(source, target, n, ones):
    edits = [(False, e) for e in sorted(source - target)]
    edits += [(True, e) for e in sorted(target - source)]
    assert len(edits) == 4
    minima = {}
    for order in permutations(edits):
        graph = source
        radius = 0
        for add, pair in order:
            if add:
                radius = max(radius, distance(adjacency(graph, n), *pair))
            graph = graph | {pair} if add else graph - {pair}
            if not admissible(adjacency(graph, n), ones):
                break
        else:
            pattern = "".join("+" if add else "-" for add, _ in order)
            minima[pattern] = min(radius, minima.get(pattern, n))
    return minima


def slides(graph, n, ones):
    adj = adjacency(graph, n)
    for pivot in range(n):
        for old_end in sorted(adj[pivot]):
            for new_end in sorted(adj[old_end] - adj[pivot] - {pivot}):
                if len(adj[pivot]) == 3 or len(adj[new_end]) == 3:
                    continue
                # The addition forms a triangle, so removing the old edge
                # keeps the graph connected and leaves a two-edge detour.
                remove = edge(pivot, old_end)
                add = edge(pivot, new_end)
                if not any(
                    (old_end in ones) == (v in ones)
                    for v in adj[old_end] - {pivot}
                ):
                    continue
                if not any(
                    (pivot in ones) == (v in ones)
                    for v in (adj[pivot] - {old_end}) | {new_end}
                ):
                    continue
                yield (graph | {add}) - {remove}, (add, remove)


def slide_ball(source, n, ones):
    paths = {source: ()}
    frontier = [source]
    for _ in range(3):
        next_frontier = []
        for graph in frontier:
            for target, move in slides(graph, n, ones):
                if target not in paths:
                    paths[target] = paths[graph] + (move,)
                    next_frontier.append(target)
        frontier = next_frontier
    return paths


def run():
    prior = json.loads(SOURCE.read_text())
    carrier = prior["carrier"]
    tours = carrier["states"]
    ones = set(prior["ones"])
    n = len(tours[0])
    graphs = [cycle_edges(cycle) for cycle in tours]
    groups = {v: i for i, group in enumerate(carrier["fast_groups"]) for v in group}
    balls = [slide_ball(g, n, ones) for g in graphs]
    counts = {}
    records = []
    short_edges = {tuple(pair) for pair in carrier["fast_edges"]}
    for i, j in carrier["fast_edges"] + carrier["slow_edges"]:
        category = ("short" if (i, j) in short_edges else
                    "blocked LR4" if groups[i] != groups[j] else "other LR4")
        stats = counts.setdefault(category, {
            "edges": 0, "direct_minimum_radius": Counter(),
            "cut_join_cut_join_radius_both_directions": Counter(),
            "triangle_slide_distance_up_to_six": Counter(),
        })
        stats["edges"] += 1
        forward = direct_schedules(graphs[i], graphs[j], n, ones)
        backward = direct_schedules(graphs[j], graphs[i], n, ones)
        stats["direct_minimum_radius"][max(min(forward.values()), min(backward.values()))] += 1
        alternating = [d.get("-+-+") for d in (forward, backward)]
        stats["cut_join_cut_join_radius_both_directions"][
            str(max(alternating)) if all(x is not None for x in alternating) else "unavailable"
        ] += 1
        common = balls[i].keys() & balls[j].keys()
        path = None
        if common:
            middle = min(common, key=lambda g: (
                len(balls[i][g]) + len(balls[j][g]), sorted(g)
            ))
            path = balls[i][middle] + tuple((b, a) for a, b in reversed(balls[j][middle]))
        stats["triangle_slide_distance_up_to_six"][str(len(path)) if path else ">6"] += 1
        records.append({"edge": [i, j], "category": category, "direct_forward": forward,
                        "direct_backward": backward, "slides": path})
    return {"source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            "summary": counts, "records": records}


if __name__ == "__main__":
    result = run()
    (HERE / "results.json").write_text(json.dumps(result, separators=(",", ":")) + "\n")
    print(json.dumps(result["summary"], indent=2))
