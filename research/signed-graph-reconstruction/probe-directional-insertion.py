#!/usr/bin/env python3
"""Exact directional insertion control for SIGN-03; standard library only."""

from fractions import Fraction
from itertools import permutations

N = 7
ANCHOR = 0
MARKED = {1, 2, 3}
TARGET = MARKED | {N}


def rotate(c):
    i = c.index(ANCHOR)
    return c[i:] + c[:i]


def mirror(c):
    return c[:1] + c[:0:-1]


def successors(c):
    for i in range(N):
        w = c[i:] + c[:i]
        yield rotate(w[:3][::-1] + w[3:])


def hits(c, edge):
    j = edge + 1
    child = c[:j] + (N,) + c[j:]
    return set(child[j % 2::2]) == TARGET


def independently_hits(c, edge):
    # Build the child adjacency instead of reading parity from its tuple.
    x, y = c[edge], c[(edge+1) % N]
    graph = {v: set() for v in range(N+1)}
    for u, v in zip(c, c[1:] + c[:1]):
        if {u, v} != {x, y}:
            graph[u].add(v)
            graph[v].add(u)
    graph[N] = {x, y}
    graph[x].add(N)
    graph[y].add(N)
    same = {N}
    frontier = [N]
    while frontier:
        u = frontier.pop()
        for v in graph[u]:
            for w in graph[v] - same:
                same.add(w)
                frontier.append(w)
    return same == TARGET


def score(c):
    return tuple(map(int, (hits(c, 0), hits(c, N-1)))) + (
        sum(hits(c, i) for i in range(N)),)


def average(c, k):
    paths = [c]
    for _ in range(k):
        paths = [d for a in paths for d in successors(a)]
    forward, backward, uniform = map(sum, zip(*(score(a) for a in paths)))
    count = len(paths)
    return (Fraction(forward, count), Fraction(backward, count),
            Fraction(forward + backward, 2*count),
            Fraction(uniform, N*count))


def main():
    # Lexicographically first rooted labelling of 0001011 with the fixed marks.
    a = (0, 4, 5, 1, 6, 2, 3)
    b = mirror(a)
    for k in range(4):
        row_a, row_b = average(a, k), average(b, k)
        assert row_a == (row_b[1], row_b[0], *row_b[2:])
        if k == 1:
            assert row_a == (0, Fraction(1, 7), Fraction(1, 14), Fraction(1, 49))
        print(k, *map(str, row_a), "|", *map(str, row_b))
    separation = 0
    for p in permutations(range(1, N)):
        c = (0,) + p
        assert all(hits(c, i) == independently_hits(c, i) for i in range(N))
        f, r, rnd, u = average(c, 1)
        mf, mr, mrnd, mu = average(mirror(c), 1)
        assert (f, r, rnd, u) == (mr, mf, mrnd, mu)
        separation += f != mf
    print("Size-7 mirror pairs separated after one reversal:", separation // 2, "/ 360")


if __name__ == "__main__":
    main()
