#!/usr/bin/env python3
"""Exact orientation-lift versus unsigned marked-gap audit (stdlib only)."""

from collections import Counter
from itertools import permutations
import json


def rotations(word):
    return [word[i:] + word[:i] for i in range(len(word))]


def marked_necklace(cycle, marked):
    return min(rotations(tuple(int(v in marked) for v in cycle)))


def mirror(necklace):
    return min(rotations(necklace[::-1]))


def bracelet(necklace):
    return min(necklace, mirror(necklace))


def targets(cycle, marked):
    n = len(cycle)
    hits = 0
    for i in range(n):
        child = cycle[:i+1] + (n,) + cycle[i+1:]
        hits += set(child[(i+1) % 2::2]) == marked | {n}
    return hits


def audit(n, marked):
    cycles = [(0,) + p for p in permutations(range(1, n))]
    tag = {c: marked_necklace(c, marked) for c in cycles}
    directed, unsigned, hits = {}, {}, {}
    for c in cycles:
        key = tag[c]
        group = bracelet(key)
        successors = []
        for i in range(n):
            d = list(c)
            j = (i+2) % n
            d[i], d[j] = d[j], d[i]
            d = tuple(d)
            k = d.index(0)
            successors.append(tag[d[k:] + d[:k]])
        counts = Counter(successors)
        reduced = Counter(map(bracelet, successors))
        assert directed.setdefault(key, counts) == counts
        assert unsigned.setdefault(group, reduced) == reduced
        h = targets(c, marked)
        independent = all(not (c[i] in marked and c[(i+1) % n] in marked)
                          for i in range(n))
        assert h == int(independent)
        assert hits.setdefault(group, h) == h
    for key, counts in directed.items():
        assert directed[mirror(key)] == Counter({mirror(k): v
                                                 for k, v in counts.items()})
    if n == 7:
        keys = sorted(unsigned, key=lambda key: sorted(
            (j-i) % n for i, j in zip(
                [i for i, bit in enumerate(key) if bit],
                [i for i, bit in enumerate(key) if bit][1:] +
                [key.index(1)])))
        assert [[unsigned[a][b] for b in keys] for a in keys] == [
            [3, 2, 2, 0], [1, 4, 1, 1], [2, 2, 3, 0], [0, 2, 0, 5]]
    # Integer counts for k reversal events followed by one insertion.
    fine = {key: hits[bracelet(key)] for key in directed}
    coarse = dict(hits)
    for k in range(9):
        assert all(v == coarse[bracelet(key)] for key, v in fine.items()), k
        fine = {key: sum(w*fine[t] for t, w in row.items())
                for key, row in directed.items()}
        coarse = {key: sum(w*coarse[t] for t, w in row.items())
                  for key, row in unsigned.items()}
    pairs = [key for key in sorted(directed) if key < mirror(key)]
    if n == 7:
        (a,) = pairs
        # Positive control: an oriented readout is not predicted by the bracelet.
        assert directed[a][a] != directed[mirror(a)][a]
    return dict(n=n, marked=sorted(marked), oriented_cycles=len(cycles),
                oriented_necklaces=len(directed), unsigned_bracelets=len(unsigned),
                mirror_pairs=[["".join(map(str, key)), "".join(map(str, mirror(key)))]
                              for key in pairs],
                horizons_verified=list(range(9)))


if __name__ == "__main__":
    print(json.dumps([audit(n, set(range(1, (n+1)//2))) for n in (5, 7, 9)],
                     indent=2))
