#!/usr/bin/env python3
"""Join boundary path pairings and reduce their completion rows over GF(2)."""

from argparse import ArgumentParser
from collections import Counter, defaultdict
from functools import cache
from itertools import chain, combinations
from pathlib import Path

from verify_hc_01 import adjacency
from verify_hc_02 import graph6
from verify_hc_03 import WITNESSES
from verify_hc_04 import enumerate_finish_masks


@cache
def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    first, *rest = vertices
    return tuple(
        ((first, mate),) + matching
        for mate in rest
        for matching in perfect_matchings(tuple(v for v in rest if v != mate))
    )


def compatible(left, right):
    """Test connectivity of two perfect matchings on the same nonempty boundary."""
    mates = tuple({a: b for edge in matching for a, b in (edge, edge[::-1])}
                  for matching in (left, right))
    start = left[0][0]
    visited = {start}
    pending = [start]
    while pending:
        v = pending.pop()
        for partner in mates:
            u = partner[v]
            if u not in visited:
                visited.add(u)
                pending.append(u)
    return len(visited) == 2 * len(left)


@cache
def completion_row(order, matching):
    return sum(
        1 << column for column, outside in enumerate(perfect_matchings(tuple(range(order))))
        if compatible(matching, outside)
    )


def independent_rows(rows):
    """Yield original keys whose binary rows extend the current span."""
    pivots = {}
    for key, row in rows:
        while row:
            pivot = row.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = row
                yield key
                break
            row ^= pivots[pivot]


def representative_states(states, row_function=completion_row):
    by_degree = defaultdict(list)
    for degrees, matching in states:
        by_degree[degrees].append(matching)
    result = set()
    for degrees, matchings in by_degree.items():
        if len(matchings) == 1:
            result.add((degrees, matchings[0]))
            continue
        endpoints = sorted(v for edge in matchings[0] for v in edge)
        number = {v: i for i, v in enumerate(endpoints)}
        rows = (
            (matching, row_function(len(endpoints), tuple((number[a], number[b]) for a, b in matching)))
            for matching in sorted(matchings)
        )
        result.update((degrees, matching) for matching in independent_rows(rows))
    return result


def join_matchings(left, right):
    """Join paths through shared ends. A return of None means a closed cycle."""
    mates = {}
    for a, b in chain(left, right):
        if mates.get(a) == b:
            return None
        first = mates.pop(a, a)
        last = mates.pop(b, b)
        mates[first] = last
        mates[last] = first
    return tuple(sorted((a, b) for a, b in mates.items() if a < b))


def piece_boundary(neighbors, endpoints, edges):
    incidence = Counter(v for edge in edges for v in edge)
    return tuple(sorted(v for v in incidence if v in endpoints or incidence[v] < len(neighbors[v])))


def piece_states(neighbors, endpoints, edges, balanced, compressed, stats, *,
                 split_edges=None, reduce_states=representative_states):
    """Return the boundary and states of a nonempty subset of the graph's edges."""
    boundary = piece_boundary(neighbors, endpoints, edges)
    boundary_set = set(boundary)
    if len(edges) == 1:
        edge = edges[0]
        # Keep or omit the edge. A nonterminal forgotten here already needs degree two.
        states = set()
        if len(boundary) == 2:
            states.update({((0, 0), ()), ((1, 1), (edge,))})
    else:
        if split_edges is None:
            split = len(edges) // 2 if balanced else len(edges) - 1
            first_edges, second_edges = edges[:split], edges[split:]
        else:
            first_edges, second_edges = split_edges(edges)
        options = {"split_edges": split_edges, "reduce_states": reduce_states}
        left, left_states = piece_states(neighbors, endpoints, first_edges, balanced, compressed, stats, **options)
        right, right_states = piece_states(neighbors, endpoints, second_edges, balanced, compressed, stats, **options)
        active = tuple(sorted(set(left) | set(right)))
        forgotten = tuple(v for v in active if v not in boundary_set)
        right_degrees = [(dict(zip(right, degree)), matching) for degree, matching in right_states]
        states = set()
        stats["join pairs"] += len(left_states) * len(right_states)
        stats["peak join boundary"] = max(stats["peak join boundary"], len(active))
        for degree, first in left_states:
            left_degree = dict(zip(left, degree))
            for right_degree, second in right_degrees:
                joined = {v: left_degree.get(v, 0) + right_degree.get(v, 0) for v in active}
                if any(joined[v] != 2 for v in forgotten):
                    continue
                if any(joined[v] > (1 if v in endpoints else 2) for v in boundary):
                    continue
                matching = join_matchings(first, second)
                if matching is not None:
                    states.add((tuple(joined[v] for v in boundary), matching))

    stats["before reduction"] += len(states)
    stats["peak boundary"] = max(stats["peak boundary"], len(boundary))
    if compressed:
        states = reduce_states(states)
    stats["retained"] += len(states)
    stats["peak states"] = max(stats["peak states"], len(states))
    return boundary, states


def edge_list(neighbors):
    return tuple(sorted((a, b) for a, row in enumerate(neighbors) for b in row if a < b))


def has_spanning_path(neighbors, x, y, balanced, compressed, stats, **options):
    endpoints = {x, y}
    if any(len(row) < (1 if v in endpoints else 2) for v, row in enumerate(neighbors)):
        return False
    boundary, states = piece_states(neighbors, endpoints, edge_list(neighbors), balanced, compressed, stats, **options)
    return ((1, 1), (boundary,)) in states


def audit_ranks():
    print("Path ends | matchings | distinct completion rows | rank | full-table minimum")
    for order, expected_rank, expected_cover in ((2, 1, 1), (4, 2, 2), (6, 4, 4), (8, 8, 5)):
        matchings = perfect_matchings(tuple(range(order)))
        rows = [(matching, completion_row(order, matching)) for matching in matchings]
        rank = len(list(independent_rows(rows)))
        if rank != expected_rank or len({row for _, row in rows}) != len(matchings):
            raise AssertionError((order, rank))
        cover = minimum_full_cover([row for _, row in rows], rank)
        if cover != expected_cover:
            raise AssertionError((order, cover))
        print(f"{order} | {len(matchings)} | {len(matchings)} | {rank} | {cover}")


def completion_support(family):
    result = 0
    for row in family:
        result |= row
    return result


def minimum_full_cover(rows, rank):
    """Relabel the boundary so a minimum cover contains the first matching."""
    target = completion_support(rows)
    for size in range(1, rank + 1):
        if any((rows[0] | completion_support(extra)) == target for extra in combinations(rows[1:], size - 1)):
            return size
    raise AssertionError("The row basis gives a cover of size at most the rank")


def compare_pair_marginals(family):
    """Compare attainable exterior completions with the union-of-pairs relaxation."""
    pairs = {edge for matching in family for edge in matching}
    recombined = [matching for matching in perfect_matchings(tuple(range(6))) if set(matching) <= pairs]
    actual = completion_support(completion_row(6, matching) for matching in family)
    relaxed = completion_support(completion_row(6, matching) for matching in recombined)
    return actual, relaxed


def verify_examples():
    outside = ((1, 2),)
    good, bad = ((0, 1), (2, 3)), ((0, 3), (1, 2))
    if join_matchings(good, outside) != ((0, 3),) or join_matchings(bad, outside) is not None:
        raise AssertionError("Splicing must distinguish equal degrees and catch a parallel-pair cycle")

    # A triangle has two routes with the same endpoint pairing and different use of vertex 2.
    inside = ((0, 1), (0, 2), (1, 2))
    outside = ((1, 3), (2, 3), (2, 4))
    neighbors = adjacency(5, inside + outside)
    boundary, states = piece_states(neighbors, {0, 4}, inside, True, False, Counter())
    same_pairing = {((1, 1, 0), ((0, 1),)), ((1, 1, 2), ((0, 1),))}
    if boundary != (0, 1, 2) or not same_pairing <= states:
        raise AssertionError((boundary, states))

    inside = ((0, 1), (0, 3), (0, 5), (1, 6), (2, 3), (2, 6),
              (3, 4), (3, 5), (3, 6), (4, 7), (5, 7), (6, 7))
    outside = ((0, 10), (1, 11), (2, 8), (3, 8), (4, 9), (5, 9))
    neighbors = adjacency(12, inside + outside)
    boundary, states = piece_states(neighbors, {10, 11}, inside, True, False, Counter())
    family = {matching for degrees, matching in states if degrees == (1,) * 6}
    expected = {
        ((0, 1), (2, 3), (4, 5)), ((0, 1), (2, 4), (3, 5)), ((0, 1), (2, 5), (3, 4)),
        ((0, 3), (1, 2), (4, 5)), ((0, 5), (1, 4), (2, 3)),
    }
    if boundary != tuple(range(6)) or family != expected:
        raise AssertionError((boundary, family))
    actual, relaxed = compare_pair_marginals(family)
    # The first exterior matching (01, 23, 45) is realised by the six exterior edges above.
    oracle = enumerate_finish_masks(neighbors)
    if (actual & 1) or not (relaxed & 1) or (oracle[10] & (1 << 11)):
        raise AssertionError((actual, relaxed, oracle))
    for balanced in (False, True):
        for compressed in (False, True):
            if has_spanning_path(neighbors, 10, 11, balanced, compressed, Counter()):
                raise AssertionError((balanced, compressed))
    print("Verified degree, subtour, and pair-marginal counterexamples.")


def audit_marginal_minimum(neighbors, totals):
    # At order seven there can be six open ends and just one additional vertex of degree two.
    for through in range(7):
        ports = tuple(v for v in range(7) if v != through)
        family = []
        for matching in perfect_matchings(tuple(range(6))):
            edges = [(ports[a], ports[b]) for a, b in matching]
            missing = [(a, b) for a, b in edges if b not in neighbors[a]]
            candidates = edges if not missing else missing
            if len(missing) <= 1 and any(a in neighbors[through] and b in neighbors[through]
                                         for a, b in candidates):
                family.append(matching)
        actual, relaxed = compare_pair_marginals(family)
        totals["marginal pieces"] += 1
        totals["marginal exterior checks"] += 15
        if actual != relaxed:
            raise AssertionError((edge_list(neighbors), through, family, actual, relaxed))


def check_pair(neighbors, x, y, expected, totals):
    totals["endpoint pairs"] += 1
    for balanced in (False, True):
        for compressed in (False, True):
            stats = Counter()
            actual = has_spanning_path(neighbors, x, y, balanced, compressed, stats)
            if actual != expected:
                raise AssertionError((edge_list(neighbors), x, y, balanced, compressed, actual, expected))
            totals["solver checks"] += 1
            if compressed:
                totals["removed rows"] += stats["before reduction"] - stats["retained"]


def check_graph(neighbors, totals):
    finishes = enumerate_finish_masks(neighbors)
    for x, y in combinations(range(len(neighbors)), 2):
        check_pair(neighbors, x, y, bool(finishes[x] & (1 << y)), totals)


def verify_hc03():
    totals = Counter()
    for record in WITNESSES:
        neighbors = graph6(record)
        finishes = enumerate_finish_masks(neighbors)
        terminal = len(neighbors) - 1
        for entry in range(terminal):
            check_pair(neighbors, entry, terminal, bool(finishes[entry] & (1 << terminal)), totals)
    print("HC-03 residual examples", dict(totals))


def census(paths):
    for path in paths:
        totals = Counter()
        with path.open(encoding="ascii") as lines:
            for line in lines:
                if line.strip() in ("", ">>graph6<<"):
                    continue
                totals["graphs"] += 1
                neighbors = graph6(line)
                if len(neighbors) == 7:
                    audit_marginal_minimum(neighbors, totals)
                else:
                    check_graph(neighbors, totals)
        print(path.name, dict(totals))


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("graph6", nargs="*", type=Path, help="connected catalogues, with order seven for the marginal minimum")
    args = parser.parse_args()
    audit_ranks()
    verify_examples()
    verify_hc03()
    census(args.graph6)


if __name__ == "__main__":
    main()
