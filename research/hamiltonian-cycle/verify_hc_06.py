#!/usr/bin/env python3
"""Benchmark graph-based edge splits and basis-column matching reduction."""

from argparse import ArgumentParser
from collections import Counter, deque
from functools import cache
from itertools import combinations
from random import Random
from statistics import median
from time import process_time
from typing import NamedTuple

from verify_hc_01 import adjacency
from verify_hc_05 import (compatible, completion_row, edge_list, has_spanning_path,
                          independent_rows, perfect_matchings, piece_boundary, representative_states)


class Case(NamedTuple):
    name: str
    neighbors: list
    x: int
    y: int


@cache
def basis_columns(order):
    """The X_t matchings of Cygan, Kratsch and Nederlof, Definition 3.1."""
    if order == 2:
        return (((0, 1),),)
    columns = []
    old_end, new_left, new_right = order - 3, order - 2, order - 1
    for previous in basis_columns(order - 2):
        last_pair = next(edge for edge in previous if old_end in edge)
        mate = last_pair[0]  # The previous largest vertex is the second member of this pair.
        switched = [edge for edge in previous if edge != last_pair]
        switched.extend(((mate, new_left), (old_end, new_right)))
        columns.append(tuple(sorted(switched)))
        columns.append(previous + ((new_left, new_right),))
    return tuple(columns)


@cache
def basis_row(order, matching):
    return sum(1 << i for i, outside in enumerate(basis_columns(order)) if compatible(matching, outside))


def reduce_with_basis(states):
    return representative_states(states, row_function=basis_row)


def audit_basis():
    print("Open ends | All columns | Basis columns | Same representatives")
    for order in (2, 4, 6, 8):
        all_matchings = perfect_matchings(tuple(range(order)))
        compact = basis_columns(order)
        full_rows = [(matching, completion_row(order, matching)) for matching in all_matchings]
        short_rows = [(matching, basis_row(order, matching)) for matching in all_matchings]
        flip = len(compact) - 1
        short_by_matching = dict(short_rows)
        for matching, row in full_rows:
            short = short_by_matching[matching]
            reversed_bits = sum(1 << (i ^ flip) for i in range(len(compact)) if short & (1 << i))
            recovered = sum(1 << i for i, (_, outside) in enumerate(short_rows)
                            if (reversed_bits & outside).bit_count() % 2)
            if recovered != row:
                raise AssertionError((order, matching, row, recovered))
        full_basis = list(independent_rows(full_rows))
        short_basis = list(independent_rows(short_rows))
        if full_basis != short_basis or len(short_basis) != len(compact):
            raise AssertionError((order, full_basis, short_basis))
        print(f"{order} | {len(all_matchings)} | {len(compact)} | yes")


def grid(name, height, width, *, seed=None, exit_vertex=None):
    order = height * width
    ids = list(range(order))
    if seed is not None:
        Random(seed).shuffle(ids)
    edges = []
    for v in range(order):
        row, column = divmod(v, width)
        if column + 1 < width:
            edges.append((ids[v], ids[v + 1]))
        if row + 1 < height:
            edges.append((ids[v], ids[v + width]))
    return Case(name, adjacency(order, edges), ids[0], ids[order - 1 if exit_vertex is None else exit_vertex])


def cases():
    return (
        grid("ladder-12", 2, 6, exit_vertex=5),
        grid("ladder-16", 2, 8, seed=196),
        grid("grid-15-ordered", 3, 5),
        grid("grid-15-relabelled", 3, 5, seed=196),
        grid("grid-15-no", 3, 5, seed=196, exit_vertex=13),
        grid("grid-20", 4, 5, seed=196, exit_vertex=14),
        grid("grid-24", 3, 8, seed=196),
        Case("complete-bipartite-8", adjacency(8, [(v, u) for v in range(4) for u in range(4, 8)]), 0, 1),
        Case("complete-bipartite-10", adjacency(10, [(v, u) for v in range(5) for u in range(5, 10)]), 0, 1),
        Case("clique-9", adjacency(9, combinations(range(9), 2)), 0, 8),
    )


def reference_path(case):
    adjacent = [sum(1 << u for u in row) for row in case.neighbors]

    @cache
    def visit(v, unseen):
        if v == case.y:
            return not unseen
        candidates = adjacent[v] & unseen
        while candidates:
            bit = candidates & -candidates
            if visit(bit.bit_length() - 1, unseen ^ bit):
                return True
            candidates ^= bit
        return False

    return visit(case.x, ((1 << len(adjacent)) - 1) ^ (1 << case.x))


def breadth_first_distances(neighbors, source):
    distance = {source: 0}
    queue = deque([source])
    while queue:
        v = queue.popleft()
        for u in neighbors[v]:
            if u not in distance:
                distance[u] = distance[v] + 1
                queue.append(u)
    return distance


def order_by_distance(edges, distance, missing):
    def edge_key(edge):
        distances = sorted(distance.get(v, missing) for v in edge)
        return distances[1], distances[0], edge

    return tuple(sorted(edges, key=edge_key))


def breadth_first_order(neighbors, edges, source):
    return order_by_distance(edges, breadth_first_distances(neighbors, source), len(neighbors))


def piece_adjacency(edges):
    local = {v: set() for edge in edges for v in edge}
    for a, b in edges:
        local[a].add(b)
        local[b].add(a)
    return local


def width_score(left_boundary, right_boundary, left_size, right_size):
    return (max(len(left_boundary), len(right_boundary)), len(left_boundary | right_boundary),
            len(left_boundary) + len(right_boundary), abs(left_size - right_size))


def small_boundary_split(neighbors, terminals, edges):
    local = piece_adjacency(edges)
    orderings = dict.fromkeys([edges, *(breadth_first_order(local, edges, v) for v in sorted(local))])
    best_score = None
    for order in orderings:
        # Allow either child to take between one third and two thirds of the edges.
        size = len(order)
        for split in range((size + 2) // 3, (2 * size) // 3 + 1):
            left, right = order[:split], order[split:]
            left_boundary = set(piece_boundary(neighbors, terminals, left))
            right_boundary = set(piece_boundary(neighbors, terminals, right))
            score = width_score(left_boundary, right_boundary, len(left), len(right))
            if best_score is None or score < best_score:
                best_score = score
                best = left, right
    return best


def build_plan(case, edges, small_boundary):
    terminals = {case.x, case.y}
    splits = {}
    peak = 0
    pending = [edges]
    while pending:
        piece = pending.pop()
        peak = max(peak, len(piece_boundary(case.neighbors, terminals, piece)))
        if len(piece) == 1:
            continue
        if small_boundary:
            left, right = small_boundary_split(case.neighbors, terminals, piece)
        else:
            midpoint = len(piece) // 2
            left, right = piece[:midpoint], piece[midpoint:]
        splits[piece] = left, right
        pending.extend((left, right))
    return splits, peak


def time_plan(case, repeats, small_boundary):
    edges = edge_list(case.neighbors)
    times = []
    for _ in range(repeats):
        start = process_time()
        plan, peak = build_plan(case, edges, small_boundary)
        times.append(process_time() - start)
    return plan, peak, 1000 * median(times)


def clear_matching_caches():
    for function in (completion_row, perfect_matchings, basis_row, basis_columns):
        function.cache_clear()


def benchmark_rows(repeats):
    print("Open ends | Rows sampled | All columns | Basis columns | Full row ms | Compact row ms")
    for size in (8, 10):
        matchings = perfect_matchings(tuple(range(size)))
        sample = tuple(sorted(Random(731).sample(matchings, 64)))
        retained = []
        measured = []
        for row_function in (completion_row, basis_row):
            times = []
            for _ in range(repeats):
                clear_matching_caches()
                start = process_time()
                rows = [(matching, row_function(size, matching)) for matching in sample]
                times.append(process_time() - start)
            retained.append(list(independent_rows(rows)))
            measured.append(1000 * median(times))
        if retained[0] != retained[1]:
            raise AssertionError((size, retained))
        print(f"{size} | {len(sample)} | {len(matchings)} | {len(basis_columns(size))} | "
              f"{measured[0]:.3f} | {measured[1]:.3f}", flush=True)


def time_solver(case, expected, plan, repeats, mode):
    reduce_states = reduce_with_basis if mode == "basis" else representative_states
    times = []
    for _ in range(repeats):
        clear_matching_caches()
        stats = Counter()
        start = process_time()
        actual = has_spanning_path(case.neighbors, case.x, case.y, True, mode != "plain", stats,
                                   split_edges=plan.__getitem__, reduce_states=reduce_states)
        times.append(process_time() - start)
        if actual != expected:
            raise AssertionError((case.name, mode, expected, actual))
    return stats, 1000 * median(times)


def benchmark(case, repeats):
    expected = reference_path(case)
    for structural in (False, True):
        label = "small-boundary" if structural else "sorted"
        plan, peak, plan_ms = time_plan(case, repeats, structural)
        # Keep the full-column control bounded even on plans with many exposed vertices.
        modes = ("plain", "basis", "full") if peak <= 10 else ("plain", "basis")
        results = {}
        for mode in modes:
            stats, solver_ms = time_solver(case, expected, plan, repeats, mode)
            results[mode] = stats
            removed = stats["before reduction"] - stats["retained"]
            print(f"{case.name} | {label} | {mode} | {expected} | {peak} | {stats['peak states']} | "
                  f"{stats['join pairs']} | {removed} | {plan_ms:.3f} | {solver_ms:.3f}", flush=True)
        if "full" in results and results["basis"] != results["full"]:
            raise AssertionError((case.name, label, results["basis"], results["full"]))


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=int, default=5, help="CPU-time runs per configuration")
    parser.add_argument("--case", action="append", choices=[case.name for case in cases()])
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    audit_basis()
    benchmark_rows(args.repeats)
    print("Graph | Plan | Mode | Path | Boundary | Peak states | Join pairs | Dropped | Plan ms | Solve ms")
    for case in cases():
        if not args.case or case.name in args.case:
            benchmark(case, args.repeats)


if __name__ == "__main__":
    main()
