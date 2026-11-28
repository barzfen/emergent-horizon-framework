#!/usr/bin/env python3
"""Test inexpensive cut candidates and a parity-aware degree estimate."""

from argparse import ArgumentParser
from collections import Counter
from itertools import combinations, product
from math import prod
from statistics import median
from time import process_time
from typing import NamedTuple

from verify_hc_01 import adjacency
from verify_hc_05 import edge_list, piece_boundary, piece_states
from verify_hc_06 import (breadth_first_distances, build_plan, cases, order_by_distance,
                          piece_adjacency, reference_path, time_solver, width_score)


class MeasuredCut(NamedTuple):
    width: tuple
    compatible_bound: int
    raw_bound: int
    compatible_profiles: int
    compatible_records: int
    raw_records: int


def farthest(distance):
    return max(distance, key=lambda v: (distance[v], -v))


def sampled_cuts(edges):
    local = piece_adjacency(edges)
    first = farthest(breadth_first_distances(local, min(local)))
    first_distances = breadth_first_distances(local, first)
    second_distances = breadth_first_distances(local, farthest(first_distances))
    orders = dict.fromkeys((edges, order_by_distance(edges, first_distances, len(local)),
                            order_by_distance(edges, second_distances, len(local))))
    size = len(edges)
    positions = sorted({(size + 2) // 3, size // 2, (2 * size) // 3})
    seen = set()
    for order in orders:
        for split in positions:
            left, right = order[:split], order[split:]
            key = frozenset((frozenset(left), frozenset(right)))
            if key not in seen:
                seen.add(key)
                yield left, right


def even_assignments(limits):
    # The total number of assignments is product(limit + 1). The even-minus-odd
    # difference is zero with a limit of one, and otherwise one.
    choices = prod(d + 1 for d in limits)
    return (choices + (1 not in limits)) // 2


def degree_estimate(terminals, parent, left, right, left_boundary, right_boundary):
    left_incidence = Counter(v for edge in left for v in edge)
    right_incidence = Counter(v for edge in right for v in edge)
    left_limits = {v: min(1 if v in terminals else 2, left_incidence[v]) for v in left_boundary}
    right_limits = {v: min(1 if v in terminals else 2, right_incidence[v]) for v in right_boundary}
    # State bit 0 is the left sum parity, state bit 1 the right sum parity.
    parity = [1, 0, 0, 0]
    for v in left_boundary | right_boundary:
        cap = 1 if v in terminals else 2
        minimum = 0 if v in parent else cap
        local = Counter((a % 2) | ((b % 2) << 1)
                        for a, b in product(range(left_limits.get(v, 0) + 1),
                                            range(right_limits.get(v, 0) + 1))
                        if minimum <= a + b <= cap)
        parity = [sum(parity[p ^ flip] * count for flip, count in local.items()) for p in range(4)]
    raw = even_assignments(left_limits.values()) * even_assignments(right_limits.values())
    return parity[0], raw


def cut_scores(case, piece):
    terminals = {case.x, case.y}
    parent = set(piece_boundary(case.neighbors, terminals, piece))
    for left, right in sampled_cuts(piece):
        first = set(piece_boundary(case.neighbors, terminals, left))
        second = set(piece_boundary(case.neighbors, terminals, right))
        width = width_score(first, second, len(left), len(right))
        degree = degree_estimate(terminals, parent, left, right, first, second)
        yield left, right, width, degree


def sampled_plan(case, edges, by_degree):
    terminals = {case.x, case.y}
    splits = {}
    peak = 0
    pending = [edges]
    while pending:
        piece = pending.pop()
        peak = max(peak, len(piece_boundary(case.neighbors, terminals, piece)))
        if len(piece) == 1:
            continue
        if by_degree:
            left, right, _, _ = min(cut_scores(case, piece), key=lambda row: row[3] + row[2])
        else:
            def score(cut):
                left, right = cut
                first = set(piece_boundary(case.neighbors, terminals, left))
                second = set(piece_boundary(case.neighbors, terminals, right))
                return width_score(first, second, len(left), len(right))

            left, right = min(sampled_cuts(piece), key=score)
        splits[piece] = left, right
        pending.extend((left, right))
    return splits, peak


def plans(case, edges):
    return {
        "sorted": lambda: build_plan(case, edges, False),
        "all-seed width": lambda: build_plan(case, edges, True),
        "sampled width": lambda: sampled_plan(case, edges, False),
        "sampled degree": lambda: sampled_plan(case, edges, True),
    }


def time_plan(build, repeats):
    times = []
    for _ in range(repeats):
        start = process_time()
        plan, peak = build()
        times.append(process_time() - start)
    return plan, peak, 1000 * median(times)


def benchmark(case, edges, repeats):
    expected = reference_path(case)
    for name, build in plans(case, edges).items():
        plan, peak, plan_ms = time_plan(build, repeats)
        stats, solve_ms = time_solver(case, expected, plan, repeats, "basis")
        print(f"{case.name} | {name} | {expected} | {peak} | {stats['join pairs']} | "
              f"{stats['degree-compatible pairs']} | {plan_ms:.3f} | {solve_ms:.3f} | "
              f"{plan_ms + solve_ms:.3f}", flush=True)


def actual_counts(terminals, parent, first, second):
    left, left_states = first
    right, right_states = second
    active = sorted(set(left) | set(right))
    caps = [1 if v in terminals else 2 for v in active]
    minima = [0 if v in parent else cap for v, cap in zip(active, caps)]

    def degree_groups(boundary, states):
        profiles = Counter(degrees for degrees, _ in states)
        indexes = {v: i for i, v in enumerate(boundary)}
        return [(tuple(degrees[indexes[v]] if v in indexes else 0 for v in active), count)
                for degrees, count in profiles.items()]

    left_groups = degree_groups(left, left_states)
    right_groups = degree_groups(right, right_states)
    profiles = records = 0
    for (left_degrees, count_left), (right_degrees, count_right) in product(left_groups, right_groups):
        if all(low <= a + b <= high for low, high, a, b in zip(minima, caps, left_degrees, right_degrees)):
            profiles += 1
            records += count_left * count_right
    return profiles, records, len(left_groups) * len(right_groups), len(left_states) * len(right_states)


def verify_relaxation():
    left = ((0, 2), (0, 3))
    right = ((1, 3), (2, 3))
    neighbors = adjacency(4, left + right)
    terminals = {1, 3}
    first, second = [piece_states(neighbors, terminals, part, True, False, Counter()) for part in (left, right)]
    estimate = degree_estimate(terminals, terminals, left, right, set(first[0]), set(second[0]))
    actual = actual_counts(terminals, terminals, first, second)
    # The relaxed right profile (1, 1, 0) on vertices (1, 2, 3) cannot be realised by its two edges.
    if estimate != (1, 8) or actual != (0, 0, 3, 3):
        raise AssertionError((estimate, actual))
    print("Four-vertex control: the estimate admits one profile pair, the actual cut admits zero.")


def measured_cuts(case, edges):
    terminals = {case.x, case.y}
    plan, _ = sampled_plan(case, edges, False)

    def states(piece):
        key = tuple(sorted(piece))
        if key not in cached:
            cached[key] = piece_states(case.neighbors, terminals, key, True, False, Counter())
        return cached[key]

    cached = {}
    for piece in (edges, *plan[edges]):
        if len(piece) < 6:
            continue
        boundary = set(piece_boundary(case.neighbors, terminals, piece))
        rows = []
        for left, right, width, (degree, raw) in cut_scores(case, piece):
            profiles, records, raw_profiles, raw_records = actual_counts(terminals, boundary, states(left), states(right))
            if profiles > degree or raw_profiles > raw:
                raise AssertionError((case.name, piece, degree, profiles, raw, raw_profiles))
            rows.append(MeasuredCut(width, degree, raw, profiles, records, raw_records))
        yield rows


def compare_predictions(groups):
    cuts = [cut for group in groups for cut in group]
    exact = sum(cut.compatible_bound == cut.compatible_profiles for cut in cuts)
    median_factor = median(cut.compatible_bound / cut.compatible_profiles for cut in cuts if cut.compatible_profiles)
    print(f"The compatible upper bound was exact on {exact}/{len(cuts)} cuts. "
          f"Its median overestimate factor on positive counts was {median_factor:.3f}.")
    print("Target | Predictor | Correct order | Tied prediction | Reversed order")
    targets = (("compatible profile pairs", lambda cut: cut.compatible_profiles),
               ("compatible record pairs", lambda cut: cut.compatible_records),
               ("attempted record pairs", lambda cut: cut.raw_records))
    predictors = (("width", lambda cut: cut.width),
                  ("compatible estimate", lambda cut: cut.compatible_bound),
                  ("raw profile estimate", lambda cut: cut.raw_bound),
                  ("degree score", lambda cut: (cut.compatible_bound, cut.raw_bound, *cut.width)))
    for label, target in targets:
        for name, prediction in predictors:
            counts = Counter()
            for rows in groups:
                for a, b in combinations(rows, 2):
                    if target(a) == target(b):
                        continue
                    if prediction(a) == prediction(b):
                        counts["tied"] += 1
                    elif (prediction(a) < prediction(b)) == (target(a) < target(b)):
                        counts["correct"] += 1
                    else:
                        counts["reversed"] += 1
            print(f"{label} | {name} | {counts['correct']} | {counts['tied']} | {counts['reversed']}")


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=int, default=9)
    parser.add_argument("--case", action="append", choices=[case.name for case in cases()])
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    selected = [case for case in cases() if not args.case or case.name in args.case]
    verify_relaxation()
    print("Graph | Plan | Path | Width | Join pairs | Degree-compatible pairs | Plan ms | Solve ms | Total ms")
    for case in selected:
        benchmark(case, edge_list(case.neighbors), args.repeats)
    groups = [group for case in selected for group in measured_cuts(case, edge_list(case.neighbors))]
    print(f"Compared {sum(map(len, groups))} candidate cuts across {len(groups)} fixed pieces.")
    compare_predictions(groups)


if __name__ == "__main__":
    main()
