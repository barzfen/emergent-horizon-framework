#!/usr/bin/env python3
"""Audit completion feasibility under stable, root-marked colour refinement."""

from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path

from verify_hc_01 import adjacency, cycle_witness, legal_suffixes


MINIMAL_RESIDUALS = ("GCOe`W", "GCOe`[")


def graph6(line):
    """Decode a small graph6 record in upper-triangle column order."""
    record = line.strip().removeprefix(">>graph6<<")
    order = ord(record[0]) - 63
    values = [ord(char) - 63 for char in record[1:]]
    edge_bits = order * (order - 1) // 2
    if not 1 <= order <= 62 or len(values) != (edge_bits + 5) // 6:
        raise ValueError(f"Invalid small graph6 record: {line!r}")
    if any(not 0 <= value < 64 for value in values):
        raise ValueError(f"Invalid graph6 character: {line!r}")
    bits = iter((value >> bit) & 1 for value in values for bit in range(5, -1, -1))
    edges = [(a, b) for b in range(order) for a in range(b) if next(bits)]
    return adjacency(order, edges)


def stable_colours(neighbors, marked):
    colours = tuple((len(row), bool(marked & (1 << v))) for v, row in enumerate(neighbors))
    while True:
        labels = {}
        refined = tuple(
            labels.setdefault((colours[v], tuple(sorted(colours[u] for u in row))), len(labels))
            for v, row in enumerate(neighbors)
        )
        if len(labels) == len(set(colours)):
            return refined
        colours = refined


def path_start_masks(neighbors):
    """For every vertex subset and path end, give the possible path starts."""
    order = len(neighbors)
    starts = [[0] * order for _ in range(1 << order)]
    for v in range(order):
        starts[1 << v][v] = 1 << v
    for subset, row in enumerate(starts):
        for end, possible_starts in enumerate(row):
            if possible_starts:
                for v in neighbors[end]:
                    bit = 1 << v
                    if not subset & bit:
                        starts[subset | bit][v] |= possible_starts
    return starts


def spanning_finish_masks(neighbors):
    """For every start vertex, give the possible ends of a spanning path."""
    # Reversing these spanning paths gives the possible finishes from each start.
    return path_start_masks(neighbors)[-1]


def candidate_marks(finish_masks, unmarked_colours):
    """Every mark that could disagree on a pair surviving unmarked refinement."""
    cells = defaultdict(list)
    for v, colour in enumerate(unmarked_colours):
        cells[colour].append(v)

    full = (1 << len(finish_masks)) - 1
    marks = set()
    for cell in cells.values():
        for good in cell:
            for bad in cell:
                if good == bad:
                    continue
                available = full ^ finish_masks[bad]
                pair = (1 << good) | (1 << bad)
                if (available & pair) != pair:
                    # Both must be unmarked if the pair cannot both be marked.
                    available &= ~pair
                required = available & finish_masks[good]
                if required:
                    marked = available
                    while marked:
                        if marked & required and (marked & pair) in (0, pair):
                            marks.add(marked)
                        marked = (marked - 1) & available
    return marks


def mixed_mark_witnesses(neighbors):
    """Yield every failing mark and one mixed-colour pair for each."""
    unmarked = stable_colours(neighbors, 0)
    if len(set(unmarked)) == len(neighbors):
        return
    finishes = spanning_finish_masks(neighbors)
    for marked in sorted(candidate_marks(finishes, unmarked)):
        seen = {}
        for v, colour in enumerate(stable_colours(neighbors, marked)):
            can_finish = bool(finishes[v] & marked)
            previous = seen.get((colour, not can_finish))
            if previous is not None:
                good, bad = (v, previous) if can_finish else (previous, v)
                yield marked, good, bad
                break
            seen[colour, can_finish] = v


def components_without(neighbors, omitted):
    remaining = set(range(len(neighbors))) - {omitted}
    while remaining:
        start = remaining.pop()
        component = {start}
        pending = [start]
        while pending:
            adjacent = neighbors[pending.pop()] & remaining
            component.update(adjacent)
            remaining.difference_update(adjacent)
            pending.extend(adjacent)
        yield component


def cut_vertex_candidates(neighbors, marked):
    """On a connected graph, find entries with an exit compatible with every cut vertex."""
    order = len(neighbors)
    exits = {v for v in range(order) if marked & (1 << v)}
    if order == 1:
        return exits
    candidates = [exits - {v} for v in range(order)]
    for v in range(order):
        components = tuple(components_without(neighbors, v))
        if len(components) > 2:
            return set()
        if len(components) == 2:
            left, right = components
            candidates[v].clear()
            for u in left:
                candidates[u].intersection_update(right)
            for u in right:
                candidates[u].intersection_update(left)
    return {v for v, allowed_exits in enumerate(candidates) if allowed_exits}


def verify_examples():
    edges, _, _, _ = cycle_witness(7)
    square_edges = [(a - 3, b - 3) for a, b in edges if a >= 3 and b >= 3]
    square = stable_colours(adjacency(4, square_edges), 1)
    if square[1] == square[2]:
        raise AssertionError("The two square entries should split under refinement")
    print("HC-01 square: the two entries split under neighbour refinement.")

    for record in MINIMAL_RESIDUALS:
        residual = graph6(record)
        marks = list(mixed_mark_witnesses(residual))
        if marks != [(63, 0, 1), (255, 0, 1)]:
            raise AssertionError((record, marks))
        for marked, good, bad in marks:
            full_edges = [(0, 1), (0, 2), (1, 2), (1, good + 3), (2, bad + 3)]
            full_edges.extend((0, v + 3) for v in range(8) if marked & (1 << v))
            full_edges.extend((v + 3, u + 3) for v, row in enumerate(residual) for u in row if v < u)
            full = adjacency(11, full_edges)
            unvisited = frozenset(range(3, 11))
            good_suffixes = legal_suffixes(full, (0, 2, 1), unvisited)
            bad_suffixes = legal_suffixes(full, (0, 1, 2), unvisited)
            if not good_suffixes or bad_suffixes:
                raise AssertionError((record, marked, good_suffixes, bad_suffixes))
            feasible = {v for v, ends in enumerate(spanning_finish_masks(residual)) if ends & marked}
            if cut_vertex_candidates(residual, marked) != feasible:
                raise AssertionError((record, marked, feasible))
        print(f"{record}: verified 11-vertex embeddings and cut-vertex control for both failing marks.")


def census(paths):
    for path in paths:
        count = failing_graphs = failing_marks = 0
        for record in path.read_text(encoding="ascii").splitlines():
            if record.strip() in ("", ">>graph6<<"):
                continue
            count += 1
            witnesses = list(mixed_mark_witnesses(graph6(record)))
            if witnesses:
                failing_graphs += 1
                failing_marks += len(witnesses)
                print(f"  {record}: (mark mask, good, bad) = {witnesses}")
        print(f"{path.name}: {count} graphs, {failing_graphs} failing graphs, {failing_marks} failing marks")


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("graph6", nargs="*", type=Path, help="catalogues for the exhaustive census")
    options = parser.parse_args()
    verify_examples()
    census(options.graph6)


if __name__ == "__main__":
    main()
