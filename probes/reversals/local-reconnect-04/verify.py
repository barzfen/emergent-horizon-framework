"""Replay every recorded witness as separate edge additions and deletions."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
source = HERE.parent / "rare-channel-02" / "results.json"
parent = json.loads(source.read_text())
results = json.loads((HERE / "results.json").read_text())
assert results["source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
tours = parent["carrier"]["states"]
colours = [v in parent["ones"] for v in range(len(tours[0]))]
graphs = [
    {frozenset((x, y)) for x, y in zip(tour, tour[1:] + tour[:1])}
    for tour in tours
]


def neighbours(graph, vertex):
    return {next(iter(e - {vertex})) for e in graph if vertex in e}


def check(graph, size):
    assert len(graph) == size
    for vertex, colour in enumerate(colours):
        adjacent = neighbours(graph, vertex)
        assert 1 <= len(adjacent) <= 3
        assert any(colours[other] == colour for other in adjacent)
    seen = {0}
    for _ in colours:
        seen.update({other for v in seen for other in neighbours(graph, v)})
    assert len(seen) == len(colours)


def two_hops(graph, pair):
    a, b = pair
    return bool(neighbours(graph, a) & neighbours(graph, b))


expected = {tuple(e) for family in ("fast_edges", "slow_edges")
            for e in parent["carrier"][family]}
assert {tuple(row["edge"]) for row in results["records"]} == expected
assert len(results["records"]) == len(expected)
edit_checks = 0
for row in results["records"]:
    i, j = row["edge"]
    moves = row["slides"]
    assert moves
    for start, end, sequence in (
        (i, j, moves), (j, i, [(cut, join) for join, cut in reversed(moves)])
    ):
        graph = graphs[start].copy()
        for join, cut in sequence:
            join, cut = frozenset(join), frozenset(cut)
            assert join not in graph and cut in graph
            assert len(join & cut) == 1
            assert two_hops(graph, join)
            graph.add(join)
            check(graph, len(colours) + 1)
            graph.remove(cut)
            assert two_hops(graph, cut)
            check(graph, len(colours))
            edit_checks += 2
        assert graph == graphs[end]
print(f"Replayed {len(expected)} witnesses in both directions with {edit_checks} checked edits.")
