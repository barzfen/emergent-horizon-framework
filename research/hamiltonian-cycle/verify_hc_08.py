#!/usr/bin/env python3
"""Verify exact joins grouped and indexed by realised boundary degrees."""

from argparse import ArgumentParser
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

from verify_hc_02 import graph6
from verify_hc_04 import enumerate_finish_masks
from verify_hc_05 import edge_list, join_matchings, piece_states, scan_join
from verify_hc_06 import cases, reference_path, time_solver
from verify_hc_07 import plans


def align_records(active, boundary, states, coalesce):
    if coalesce:
        groups = defaultdict(list)
        for degrees, matching in states:
            groups[degrees].append(matching)
        rows = groups.items()
    else:
        rows = ((degrees, (matching,)) for degrees, matching in states)
    offsets = {v: i for i, v in enumerate(boundary)}
    return [(tuple(degrees[offsets[v]] if v in offsets else 0 for v in active), matchings)
            for degrees, matchings in rows]


def compatible_groups(left, right, forgotten, shared, stats):
    stats["degree checks"] += len(left) * len(right)
    for first, second in product(left, right):
        a, b = first[0], second[0]
        if all(a[i] + b[i] == 2 for i in forgotten) and all(a[i] + b[i] <= cap for i, cap in shared):
            yield first, second


def indexed_groups(left, right, forgotten, shared, stats):
    by_forgotten = defaultdict(int)
    zero = [0] * len(shared)
    at_most_one = [0] * len(shared)
    for j, (degrees, _) in enumerate(right):
        bit = 1 << j
        by_forgotten[tuple(degrees[i] for i in forgotten)] |= bit
        for k, (i, _) in enumerate(shared):
            if degrees[i] == 0:
                zero[k] |= bit
            if degrees[i] <= 1:
                at_most_one[k] |= bit
    stats["index lookups"] += len(left)
    intersections = 0
    for first in left:
        a = first[0]
        mask = by_forgotten.get(tuple(2 - a[i] for i in forgotten), 0)
        for k, (i, cap) in enumerate(shared):
            if not mask:
                break
            if a[i]:
                mask &= zero[k] if cap - a[i] == 0 else at_most_one[k]
                intersections += 1
        while mask:
            bit = mask & -mask
            yield first, right[bit.bit_length() - 1]
            mask ^= bit
    stats["bitset intersections"] += intersections


def join_groups(endpoints, boundary, left, left_states, right, right_states, stats, find_pairs, *, coalesce=True):
    if not left_states or not right_states:
        return set()
    active = tuple(sorted(set(left) | set(right)))
    offsets = {v: i for i, v in enumerate(active)}
    forgotten = tuple(i for i, v in enumerate(active) if v not in boundary)
    kept = tuple(offsets[v] for v in boundary)
    shared = tuple((offsets[v], 1 if v in endpoints else 2) for v in boundary if v in left and v in right)
    first_groups = align_records(active, left, left_states, coalesce)
    second_groups = align_records(active, right, right_states, coalesce)
    result = set()
    compatible_profiles = compatible_records = 0
    for (a, left_matchings), (b, right_matchings) in find_pairs(first_groups, second_groups, forgotten, shared, stats):
        degrees = tuple(a[i] + b[i] for i in kept)
        compatible_profiles += 1
        compatible_records += len(left_matchings) * len(right_matchings)
        for first, second in product(left_matchings, right_matchings):
            matching = join_matchings(first, second)
            if matching is not None:
                result.add((degrees, matching))
    if coalesce:
        stats["compatible profile pairs"] += compatible_profiles
    stats["degree-compatible pairs"] += compatible_records
    return result


def vector_join(endpoints, boundary, left, left_states, right, right_states, stats):
    return join_groups(endpoints, boundary, left, left_states, right, right_states, stats,
                       compatible_groups, coalesce=False)


def grouped_join(endpoints, boundary, left, left_states, right, right_states, stats):
    return join_groups(endpoints, boundary, left, left_states, right, right_states, stats, compatible_groups)


def indexed_join(endpoints, boundary, left, left_states, right, right_states, stats):
    return join_groups(endpoints, boundary, left, left_states, right, right_states, stats, indexed_groups)


def audit_piece_joins(neighbors, totals):
    edges = edge_list(neighbors)
    finishes = enumerate_finish_masks(neighbors)

    def checked_join(endpoints, boundary, left, left_states, right, right_states, stats):
        args = (endpoints, boundary, left, left_states, right, right_states)
        scan_counts = Counter()
        baseline = scan_join(*args, scan_counts)
        stats.update(scan_counts)
        vector_counts = Counter()
        grouped_counts = Counter()
        indexed_counts = Counter()
        vector = vector_join(*args, vector_counts)
        grouped = grouped_join(*args, grouped_counts)
        indexed = indexed_join(*args, indexed_counts)
        if any(baseline != table for table in (vector, grouped, indexed)):
            raise AssertionError((edges, endpoints, boundary, baseline, vector, grouped, indexed))
        counts = (scan_counts, vector_counts, grouped_counts, indexed_counts)
        if len({row["degree-compatible pairs"] for row in counts}) != 1:
            raise AssertionError((edges, endpoints, counts))
        if grouped_counts["compatible profile pairs"] != indexed_counts["compatible profile pairs"]:
            raise AssertionError((edges, endpoints, grouped_counts, indexed_counts))
        totals["intermediate joins"] += 1
        return baseline

    for x, y in combinations(range(len(neighbors)), 2):
        totals["terminal pairs"] += 1
        expected = bool(finishes[x] & (1 << y))
        for balanced in (True, False):
            vertices, states = piece_states(neighbors, {x, y}, edges, balanced, False, Counter(),
                                            join_records=checked_join)
            actual = ((1, 1), (vertices,)) in states
            if actual != expected:
                raise AssertionError((edges, x, y, balanced, actual, expected))
            totals["terminal decisions"] += 1


def census(paths):
    totals = Counter()
    for path in paths:
        with path.open(encoding="ascii") as records:
            for line in records:
                if line.strip() in ("", ">>graph6<<"):
                    continue
                totals["graphs"] += 1
                audit_piece_joins(graph6(line), totals)
    print("Catalogue audit", dict(totals), flush=True)


def benchmark(case, repeats):
    expected = reference_path(case)
    for plan_name, build in plans(case, edge_list(case.neighbors)).items():
        if plan_name == "sampled degree":
            continue
        plan, _ = build()
        stable_counts = None
        for name, join in (("scan", scan_join), ("vector", vector_join),
                           ("grouped", grouped_join), ("indexed", indexed_join)):
            stats, solver_ms = time_solver(case, expected, plan, repeats, "basis", join_records=join)
            common = tuple(stats[k] for k in ("join pairs", "degree-compatible pairs", "before reduction", "retained"))
            if stable_counts is not None and stable_counts != common:
                raise AssertionError((case.name, plan_name, name, stable_counts, common))
            stable_counts = common
            print(f"{case.name} | {plan_name} | {name} | {expected} | {stats['join pairs']} | "
                  f"{stats['degree checks']} | {stats['index lookups']} | {stats['bitset intersections']} | "
                  f"{stats['degree-compatible pairs']} | {solver_ms:.3f}", flush=True)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=int, default=9)
    parser.add_argument("--case", action="append", choices=[case.name for case in cases()])
    parser.add_argument("--catalogue", nargs="+", type=Path, help="optional connected graph6 files")
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    if args.catalogue:
        census(args.catalogue)
    print("Graph | Plan | Join | Path | Cartesian pairs | Degree checks | Index lookups | "
          "Bitset intersections | Matching checks | Solve ms")
    for case in cases():
        if not args.case or case.name in args.case:
            benchmark(case, args.repeats)


if __name__ == "__main__":
    main()
