#!/usr/bin/env python3
"""Exact unrestricted LR3 orientation audit; Python standard library only."""

from collections import Counter, deque
from itertools import permutations
import json


def rotate(c):
    k = c.index(0)
    return c[k:] + c[:k]


def orient(c):
    c = rotate(c)
    rev = c[:1] + c[:0:-1]
    return min(c, rev), int(rev < c)


def events(c):
    n = len(c)
    for i in range(n):
        d = list(c)
        j = (i + 2) % n
        d[i], d[j] = d[j], d[i]
        yield orient(tuple(d))


def parity(c):
    return min(tuple(sorted(c[::2])), tuple(sorted(c[1::2])))


def negative_witness(n, graph):
    root = tuple(range(n))
    start, goal = (root, 0), (root, 1)
    q, prev = deque([start]), {start: None}
    while goal not in prev:
        c, b = q.popleft()
        for i, (d, sign) in enumerate(graph[c]):
            nxt = (d, b ^ sign)
            if nxt not in prev:
                prev[nxt] = ((c, b), i)
                q.append(nxt)
    steps, end = [], goal
    while end != start:
        parent, i = prev[end]
        steps.append(i)
        end = parent
    steps.reverse()
    # Independently replay whole segment reversals, without reorienting.
    raw = root
    for i in steps:
        c, flipped = orient(raw)
        assert raw == rotate(raw)
        if flipped:
            i = (-i - 2) % n
        rotated = raw[i:] + raw[:i]
        raw = rotate(rotated[:3][::-1] + rotated[3:])
    assert raw == root[:1] + root[:0:-1]
    return steps


def audit(n):
    states = sorted(c for p in permutations(range(1, n))
                    if (c := (0,) + p)[1] < c[-1])
    graph = {c: list(events(c)) for c in states}
    for c, outgoing in graph.items():
        for d, bit in set(outgoing):
            assert outgoing.count((d, bit)) == graph[d].count((c, bit))
    seen, census, sectors = set(), Counter(), set()
    for root in states:
        if root in seen:
            continue
        q, potential, unbalanced = [root], {root: 0}, False
        while q:
            c = q.pop()
            for d, sign in graph[c]:
                bit = potential[c] ^ sign
                if d in potential:
                    unbalanced |= potential[d] != bit
                else:
                    potential[d] = bit
                    q.append(d)
        seen.update(potential)
        if n % 2 == 0:
            labels = {parity(c) for c in potential}
            assert len(labels) == 1 and sectors.isdisjoint(labels)
            sectors.update(labels)
        census[len(potential), unbalanced] += 1
    return {
        "n": n, "states": len(states),
        "undirected_event_count": len(states) * n // 2,
        "simple_graph": all(len({d for d, _ in row}) == n and
                            all(d != c for d, _ in row)
                            for c, row in graph.items()),
        "components": [{"size": size, "unbalanced": unbalanced, "count": count}
                       for (size, unbalanced), count in sorted(census.items())],
        "even_parity_sectors": len(sectors),
        "shortest_negative_loop_at_identity": negative_witness(n, graph),
    }


if __name__ == "__main__":
    print(json.dumps([audit(n) for n in (5, 6, 7, 8)], indent=2))
