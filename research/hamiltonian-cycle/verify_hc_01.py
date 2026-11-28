#!/usr/bin/env python3
"""Exhaustive small-graph audit of Hamiltonian prefix comparisons."""

from collections import Counter
from itertools import combinations, permutations
from math import comb


COLUMNS = (
    "graphs",
    "prefixes",
    "subset/end states",
    "exact attachment states",
    "open completable subset/end states",
    "open completable attachment states",
    "profile suffix conflicts",
    "profile decision conflicts",
)


def adjacency(order, edges):
    neighbors = [set() for _ in range(order)]
    for a, b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)
    return neighbors


def rooted_prefixes(neighbors):
    """Yield all simple paths starting at 0 and using at least one edge."""
    pending = [(0,)]
    while pending:
        path = pending.pop()
        if len(path) > 1:
            yield path
        pending.extend(path + (v,) for v in neighbors[path[-1]].difference(path))


def legal_suffixes(neighbors, path, unvisited):
    """Reference oracle. Try each ordering and check the whole closed tour."""
    valid = set()
    for suffix in permutations(sorted(unvisited)):
        tour = path + suffix + (path[0],)
        if all(b in neighbors[a] for a, b in zip(tour, tour[1:])):
            valid.add(suffix)
    return valid


def attachment_keys(neighbors, path, unvisited):
    if not unvisited:
        closes = path[0] in neighbors[path[-1]]
        return closes, closes

    root_attachment = neighbors[path[0]] & unvisited
    end_attachment = neighbors[path[-1]] & unvisited
    profile = Counter(
        (len(neighbors[v] & unvisited), v in root_attachment)
        for v in end_attachment
    )
    return frozenset(end_attachment), tuple(sorted(profile.items()))


def audit_order(order):
    edges = tuple(combinations(range(order), 2))
    vertices = frozenset(range(order))
    totals = Counter({"graphs": 1 << comb(order, 2)})
    for mask in range(1 << len(edges)):
        graph_edges = (edge for i, edge in enumerate(edges) if mask & (1 << i))
        neighbors = adjacency(order, graph_edges)
        standard = {}
        exact = {}
        profile = {}
        for path in rooted_prefixes(neighbors):
            totals["prefixes"] += 1
            unvisited = vertices.difference(path)
            suffixes = legal_suffixes(neighbors, path, unvisited)

            standard_key = (unvisited, path[-1])
            if standard.setdefault(standard_key, suffixes) != suffixes:
                raise AssertionError((order, mask, path, "standard state changed suffixes"))

            exact_attachment, degree_profile = attachment_keys(neighbors, path, unvisited)
            if exact.setdefault((unvisited, exact_attachment), suffixes) != suffixes:
                raise AssertionError((order, mask, path, "exact state changed suffixes"))

            profile.setdefault((unvisited, degree_profile), set()).add(frozenset(suffixes))

        totals["subset/end states"] += len(standard)
        totals["exact attachment states"] += len(exact)
        totals["open completable subset/end states"] += count_open_completable(standard)
        totals["open completable attachment states"] += count_open_completable(exact)
        totals["profile suffix conflicts"] += sum(len(sets) > 1 for sets in profile.values())
        totals["profile decision conflicts"] += sum(
            len(sets) > 1 and frozenset() in sets for sets in profile.values()
        )
    return totals


def count_open_completable(states):
    return sum(bool(unvisited and suffixes) for (unvisited, _), suffixes in states.items())


def cycle_witness(order):
    """A triangle of visited vertices and a residual cycle of length order - 3."""
    edges = [(0, 1), (1, 2), (0, 2), (0, 3), (1, 4), (2, 5)]
    edges.extend((v, v + 1) for v in range(3, order - 1))
    edges.append((order - 1, 3))
    unvisited = frozenset(range(3, order))
    neighbors = adjacency(order, edges)
    good, bad = (0, 2, 1), (0, 1, 2)
    good_exact, good_profile = attachment_keys(neighbors, good, unvisited)
    bad_exact, bad_profile = attachment_keys(neighbors, bad, unvisited)
    good_suffixes = legal_suffixes(neighbors, good, unvisited)
    bad_suffixes = legal_suffixes(neighbors, bad, unvisited)
    if (
        good_exact == bad_exact
        or good_profile != bad_profile
        or good_suffixes != {tuple(range(4, order)) + (3,)}
        or bad_suffixes
    ):
        raise AssertionError((order, good_profile, bad_profile, good_suffixes, bad_suffixes))
    return edges, good, bad, min(good_suffixes)


def main():
    print(" | ".join(("n", *COLUMNS)))
    for order in range(3, 7):
        totals = audit_order(order)
        if totals["profile decision conflicts"]:
            raise AssertionError((order, totals))
        print(" | ".join(map(str, (order, *(totals[column] for column in COLUMNS)))))

    edges, good, bad, suffix = cycle_witness(7)
    print(f"n=7 edges: {sorted(edges)}")
    print(f"Completable prefix: {good}; suffix: {suffix}")
    print(f"Uncompletable prefix: {bad}")
    for order in range(8, 11):
        cycle_witness(order)
    print("Residual-cycle witness family checked through n=10.")


if __name__ == "__main__":
    main()
