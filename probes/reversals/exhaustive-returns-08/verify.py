"""Replay blocked-pair witnesses one edit at a time."""
from itertools import combinations
import json

from probe import HERE, rev05

parent = json.loads(rev05.PARENT.read_text())
carrier = parent["carrier"]
tours = carrier["states"]
even = set(parent["Pi"])
ones = set(parent["ones"])
result = json.loads((HERE / "results.json").read_text())


def edges(tour):
    return {frozenset((a, b)) for a, b in zip(tour, tour[1:] + tour[:1])}


def inspect(graph):
    neighbours = {v: set() for v in tours[0]}
    for pair in graph:
        a, b = pair
        neighbours[a].add(b)
        neighbours[b].add(a)
        assert ((a in even) != (b in even)) or (0 in pair and pair <= even)
    reached = {0}
    for _ in neighbours:
        reached.update({w for v in reached for w in neighbours[v]})
    assert reached == neighbours.keys()
    for v, ns in neighbours.items():
        assert 1 <= len(ns) <= 3
        assert any((w in ones) == (v in ones) for w in ns)
    return neighbours


group = {v: k for k, part in enumerate(carrier["fast_groups"]) for v in part}
expected = {tuple(pair) for pair in carrier["slow_edges"] if group[pair[0]] != group[pair[1]]}
records = result["blocked_pairs"]
assert {(row["source"], row["target"]) for row in records} == expected
assert len(records) == len(expected)
count = 0
for row in records:
    i, j = row["source"], row["target"]
    route = [(frozenset(add), frozenset(cut)) for add, cut in row["witness"]]
    assert len(route) == row["minimum_slides"]
    for start, target, edits in ((i, j, route), (j, i, [(cut, add) for add, cut in reversed(route)])):
        graph = edges(tours[start])
        for k, (add, cut) in enumerate(edits, 1):
            before = inspect(graph)
            a, b = add
            assert add not in graph and cut in graph and len(add & cut) == 1
            assert before[a] & before[b]
            graph.add(add)
            inspect(graph)
            graph.remove(cut)
            after = inspect(graph)
            a, b = cut
            assert after[a] & after[b]
            if len(after[0]) == 2:
                low, high = sorted(after[0])
                assert not (low in even and high not in even)
            assert all(len(ns) == 2 for ns in after.values()) == (k == len(edits))
            count += 2
        assert graph == edges(tours[target])

assert [(i, j) for i, j, _ in result["first_return_edges"]] == list(combinations(range(96), 2))
print(f"Replayed {len(records)} shortest blocked-pair witnesses in both directions ({count} edits).")
