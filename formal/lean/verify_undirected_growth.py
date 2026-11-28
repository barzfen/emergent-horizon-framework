#!/usr/bin/env python3
"""Finite all-slot CBB growth audit for canonical undirected cycles n = 3..8.

This is computational evidence, not a substitute for a Lean theorem
for unbounded n. Every cycle is normalised to root 0 and the
lexicographically smaller of its forward and reversed orientations.
"""
from itertools import permutations
from math import factorial


def canonical(cycle):
    assert cycle[0] == 0, cycle
    reflected = (0,) + cycle[:0:-1]
    return min(cycle, reflected)


def cycles(n):
    return {
        (0,) + tail
        for tail in permutations(range(1, n))
        if tail <= tail[::-1]
    }


def check(n):
    parents = cycles(n)
    children = cycles(n + 1)
    assert len(parents) == factorial(n - 1) // 2
    assert len(children) == factorial(n) // 2
    observed = {}
    for parent in parents:
        for edge_slot in range(n):
            child = parent[:edge_slot + 1] + (n,) + parent[edge_slot + 1:]
            key = canonical(child)
            if key in observed:
                raise AssertionError(
                    f"Two histories for {key}: {observed[key]} and "
                    f"{(parent, edge_slot)}"
                )
            previous = canonical(tuple(x for x in key if x != n))
            assert previous == parent, (n, key, previous, parent)
            observed[key] = (parent, edge_slot)
    assert set(observed) == children
    assert len(observed) == n * len(parents)
    print(
        f"n={n}: {len(parents)} parents, {n} slots each, "
        f"{len(observed)} distinct children; pass"
    )


if __name__ == "__main__":
    for n in range(3, 9):
        check(n)
