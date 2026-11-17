#!/usr/bin/env python3
"""Compose exact spanning paths from components of a given vertex separator."""

from argparse import ArgumentParser
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
from typing import NamedTuple

from verify_hc_01 import adjacency
from verify_hc_02 import graph6, path_start_masks, spanning_finish_masks
from verify_hc_03 import WITNESSES, clique_separator_example, components, separators


class Coverage(NamedTuple):
    exact: bool
    lengths: bool
    union: bool


class Decisions(NamedTuple):
    exact: bool
    lengths: bool
    union: bool
    single_visit: bool


class ComponentPaths:
    def __init__(self, neighbors, vertices):
        ordered = sorted(vertices)
        local = {v: i for i, v in enumerate(ordered)}
        self.point = {v: 1 << i for v, i in local.items()}
        self.attachment = [sum(self.point.get(u, 0) for u in row) for row in neighbors]
        self.starts = path_start_masks([{local[u] for u in neighbors[v] & vertices} for v in ordered])
        self.full = (1 << len(ordered)) - 1
        self._options = {}

    def allowed_masks(self, starts, ends):
        key = (starts, ends)
        if key in self._options:
            return self._options[key]
        options = tuple(
            mask for mask, choices in enumerate(self.starts)
            if any((ends & (1 << v)) and (origins & starts) for v, origins in enumerate(choices))
        )
        self._options[key] = options
        return options

    def coverage(self, visits):
        """Compare disjoint, length-only and vertex-wise coverage for these visits."""
        options = [self.allowed_masks(start, end) for start, end in visits]
        if not options or any(not masks for masks in options):
            return Coverage(False, False, False)
        if len(options) == 1:
            spans = self.full in options[0]
            return Coverage(spans, spans, spans)

        occupied = {0}
        for masks in options:
            occupied = {used | mask for used in occupied for mask in masks if not used & mask}
        if self.full in occupied:
            return Coverage(True, True, True)

        unions_by_length = []
        for masks in options:
            by_length = {}
            for mask in masks:
                length = mask.bit_count()
                by_length[length] = by_length.get(length, 0) | mask
            unions_by_length.append(by_length)
        length_match = False
        for lengths in product(*unions_by_length):
            if sum(lengths) != self.full.bit_count():
                continue
            length_match = True
            union = 0
            for index, length in enumerate(lengths):
                union |= unions_by_length[index][length]
            if union == self.full:
                return Coverage(False, True, True)
        return Coverage(False, length_match, False)


class SeparatorPaths:
    def __init__(self, neighbors, cut, parts):
        self.neighbors = neighbors
        self.cut = tuple(cut)
        self.tables = [ComponentPaths(neighbors, part) for part in parts]
        self.part_of = {v: i for i, part in enumerate(parts) for v in part}

    def decide(self, x, y):
        """Compare the four rules for a fixed pair of distinct global endpoints."""
        part_count = len(self.tables)
        if part_count > len(self.cut) + 1 - (x in self.cut) - (y in self.cut):
            return Decisions(False, False, False, False)
        first_part = self.part_of.get(x, -1)
        last_part = self.part_of.get(y, -1)
        exact = lengths = union = False
        for order in permutations(self.cut):
            if (first_part == -1 and order[0] != x) or (last_part == -1 and order[-1] != y):
                continue
            for middle in product(range(-1, part_count), repeat=len(order) - 1):
                labels = (first_part, *middle, last_part)
                if len(set(labels) - {-1}) != part_count:
                    continue
                if any(part == -1 and order[i] not in self.neighbors[order[i - 1]]
                       for i, part in enumerate(middle, 1)):
                    continue
                visits = [[] for _ in self.tables]
                for i, part in enumerate(labels):
                    if part == -1:
                        continue
                    table = self.tables[part]
                    left = table.point[x] if i == 0 else table.attachment[order[i - 1]]
                    right = table.point[y] if i == len(order) else table.attachment[order[i]]
                    visits[part].append((left, right))
                supports = [table.coverage(runs) for table, runs in zip(self.tables, visits)]
                exact_layout = all(row.exact for row in supports)
                if exact_layout and all(len(runs) == 1 for runs in visits):
                    return Decisions(True, True, True, True)
                exact |= exact_layout
                lengths |= all(row.lengths for row in supports)
                union |= all(row.union for row in supports)
        return Decisions(exact, lengths, union, False)


def compare_pairs(neighbors, cut, parts, finishes):
    solver = SeparatorPaths(neighbors, cut, parts)
    counts = Counter()
    for x, y in combinations(range(len(neighbors)), 2):
        decisions = solver.decide(x, y)
        want = bool(finishes[x] & (1 << y))
        if decisions.exact != want:
            raise AssertionError((cut, x, y, decisions, want))
        counts["pairs"] += 1
        counts["length false positives"] += decisions.lengths and not want
        counts["union false positives"] += decisions.union and not want
        counts["single-visit false negatives"] += want and not decisions.single_visit
    return counts


def enumerate_finish_masks(neighbors):
    """Independent oracle that extends every simple path to a terminal or a dead end."""
    adjacent = [sum(1 << v for v in row) for row in neighbors]

    def walk(end, unseen):
        if not unseen:
            return 1 << end
        choices = adjacent[end] & unseen
        finishes = 0
        while choices:
            bit = choices & -choices
            finishes |= walk(bit.bit_length() - 1, unseen ^ bit)
            choices ^= bit
        return finishes

    full = (1 << len(neighbors)) - 1
    return [walk(v, full ^ (1 << v)) for v in range(len(neighbors))]


def verify_examples():
    # In every example the separator is {0, 1} and the queried pair is (2, 3).
    examples = (
        (5, [(0, 2), (0, 4), (1, 3), (1, 4), (2, 3)], Decisions(True, True, True, False)),
        (5, [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (2, 4)], Decisions(False, True, False, False)),
        (6, [(0, 2), (0, 3), (1, 3), (1, 4), (1, 5), (2, 4), (2, 5)], Decisions(False, True, True, False)),
    )
    for order, edges, expected in examples:
        neighbors = adjacency(order, edges)
        parts = list(components(neighbors, set(range(2, order))))
        actual = SeparatorPaths(neighbors, (0, 1), parts).decide(2, 3)
        if actual != expected or actual.exact != bool(enumerate_finish_masks(neighbors)[2] & (1 << 3)):
            raise AssertionError((order, edges, actual, expected))
    print("Verified minimal examples for all three simpler path tests.")


def verify_hc03():
    totals = Counter()
    for record in WITNESSES:
        neighbors = graph6(record)
        finishes = enumerate_finish_masks(neighbors)
        for cut, parts in separators(neighbors, set(range(len(neighbors))), 2):
            if len(cut) == 2:
                totals.update(compare_pairs(neighbors, cut, parts, finishes))
                totals["cuts"] += 1
    print(f"HC-03 minimal graphs: {totals['cuts']} cuts, {totals['pairs']} exact comparisons.")

    for connectivity in (3, 4):
        neighbors, cut = clique_separator_example(connectivity)
        parts = list(components(neighbors, set(range(len(neighbors))).difference(cut)))
        finishes = spanning_finish_masks(neighbors)
        result = compare_pairs(neighbors, cut, parts, finishes)
        print(f"HC-03 {connectivity}-connected example: {result['pairs']} exact comparisons.")


def census(paths):
    for path in paths:
        totals = Counter()
        with path.open(encoding="ascii") as records:
            for line in records:
                if line.strip() in ("", ">>graph6<<"):
                    continue
                neighbors = graph6(line)
                totals["graphs"] += 1
                finishes = None
                for cut, parts in separators(neighbors, set(range(len(neighbors))), 2):
                    if len(cut) != 2:
                        continue
                    if finishes is None:
                        finishes = enumerate_finish_masks(neighbors)
                        totals["graphs with cuts"] += 1
                    totals["cuts"] += 1
                    totals.update(compare_pairs(neighbors, cut, parts, finishes))
        print(path.name, dict(totals))


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("graph6", nargs="*", type=Path, help="connected graph catalogues")
    args = parser.parse_args()
    verify_examples()
    verify_hc03()
    census(args.graph6)


if __name__ == "__main__":
    main()
