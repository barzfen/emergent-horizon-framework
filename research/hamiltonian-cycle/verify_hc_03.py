#!/usr/bin/env python3
"""Check two-vertex separators in the first biconnected completion conflicts."""

from argparse import ArgumentParser
from collections import Counter
from itertools import combinations, product
from pathlib import Path

from verify_hc_01 import adjacency, legal_suffixes
from verify_hc_02 import graph6, mixed_mark_witnesses, spanning_finish_masks, stable_colours


WITNESSES = {
    "HCOe`Z{": (256,),
    "HCOe`Z~": (256,),
    "HCOe`^{": (256,),
    "HCOe`^~": (256,),
    "HCOebIg": (7, 56, 63, 448, 455, 504, 511),
    "HCOfCsn": (21, 42, 63, 448, 469, 490, 511),
    "HCQtbPk": (292,),
}


def components(neighbors, vertices):
    remaining = set(vertices)
    while remaining:
        start = remaining.pop()
        pending = [start]
        component = {start}
        while pending:
            adjacent = remaining & neighbors[pending.pop()]
            component.update(adjacent)
            remaining.difference_update(adjacent)
            pending.extend(adjacent)
        yield component


def is_connected(neighbors, vertices):
    parts = components(neighbors, vertices)
    return next(parts, None) is not None and next(parts, None) is None


def separators(neighbors, vertices, max_size):
    for size in range(1, max_size + 1):
        for cut in combinations(sorted(vertices), size):
            parts = list(components(neighbors, vertices.difference(cut)))
            if len(parts) >= 2:
                yield cut, parts


def satisfies_component_bound(pair, cut, parts):
    x, y = pair
    max_segments = len(cut) + 1 - (x in cut) - (y in cut)
    if len(parts) > max_segments:
        return False
    if len(parts) == max_segments and x not in cut and y not in cut:
        return not any(x in part and y in part for part in parts)
    return True


def cut_pairs(neighbors, vertices, max_size):
    if not is_connected(neighbors, vertices):
        return set()
    if len(vertices) == 1:
        vertex = next(iter(vertices))
        return {(vertex, vertex)}
    pairs = set(combinations(sorted(vertices), 2))
    for cut, parts in separators(neighbors, vertices, max_size):
        pairs = {pair for pair in pairs if satisfies_component_bound(pair, cut, parts)}
    return pairs | {(y, x) for x, y in pairs}


def quotient_pairs(neighbors, cut, parts):
    """Enumerate component runs before, between, and after the cut vertices."""
    a, b = cut
    size = len(parts)
    a_token, b_token = size, size + 1
    token = {v: i for i, part in enumerate(parts) for v in part}
    token.update({a: a_token, b: b_token})
    links = {
        a_token: {i for i, part in enumerate(parts) if neighbors[a] & part},
        b_token: {i for i, part in enumerate(parts) if neighbors[b] & part},
    }
    if b in neighbors[a]:
        links[a_token].add(b_token)
    accepted = set()
    for runs in product(range(-1, size), repeat=3):
        counts = Counter(runs)
        if any(not 1 <= counts[i] <= len(part) for i, part in enumerate(parts)):
            continue
        for first, second in ((a_token, b_token), (b_token, a_token)):
            word = tuple(t for t in (runs[0], first, runs[1], second, runs[2]) if t != -1)
            if all(v in links.get(u, ()) or u in links.get(v, ()) for u, v in zip(word, word[1:])):
                accepted.add((word[0], word[-1]))
    return token, accepted


def after_terminal_deletion(neighbors, vertices, max_size):
    allowed = set()
    for y in vertices:
        shortened = cut_pairs(neighbors, vertices - {y}, max_size)
        allowed.update((x, y) for x, z in shortened if z in neighbors[y])
    return allowed


def controls(neighbors):
    vertices = set(range(len(neighbors)))
    counts = cut_pairs(neighbors, vertices, 2)
    quotient = counts
    for cut, parts in separators(neighbors, vertices, 2):
        if len(cut) == 2:
            token, allowed = quotient_pairs(neighbors, cut, parts)
            quotient = {(x, y) for x, y in quotient if (token[x], token[y]) in allowed}
    after_one_cut = after_terminal_deletion(neighbors, vertices, 1)
    after_two_cuts = after_terminal_deletion(neighbors, vertices, 2)
    return {
        "component counts": counts,
        "contracted components": quotient,
        "delete either terminal, cuts up to one": {
            (x, y) for x, y in quotient if (x, y) in after_one_cut and (y, x) in after_one_cut
        },
        "delete either terminal, cuts up to two": {
            (x, y) for x, y in quotient if (x, y) in after_two_cuts and (y, x) in after_two_cuts
        },
    }


def verify_controls():
    agreement = Counter()
    resolved = Counter()
    for record, expected_marks in WITNESSES.items():
        neighbors = graph6(record)
        marks = tuple(marked for marked, _, _ in mixed_mark_witnesses(neighbors))
        if marks != expected_marks:
            raise AssertionError((record, expected_marks, marks))
        finishes = spanning_finish_masks(neighbors)
        checks = controls(neighbors)
        for marked in marks:
            exact = {v for v, ends in enumerate(finishes) if ends & marked}
            colours = stable_colours(neighbors, marked)
            feasible_colours = {colours[v] for v in exact}
            mixed_bad = {v for v, colour in enumerate(colours) if colour in feasible_colours} - exact
            for name, pairs in checks.items():
                remaining = {x for x, y in pairs if marked & (1 << y)}
                if not exact <= remaining:
                    raise AssertionError((record, marked, name, exact - remaining))
                agreement[name] += remaining == exact
                resolved[name] += not (remaining & mixed_bad)
    expected = [(8, 10), (8, 10), (16, 18), (19, 19)]
    actual = [(agreement[name], resolved[name]) for name in agreement]
    if actual != expected:
        raise AssertionError(actual)
    print("Control | exact entry set | all false entries in mixed classes removed")
    for name in agreement:
        print(f"{name} | {agreement[name]}/19 | {resolved[name]}/19")


def verify_lifted_examples():
    for old_record, new_record in (("GCOe`W", "HCOe`Z{"), ("GCOe`[", "HCOe`^{")):
        old = graph6(old_record)
        lifted = [row | ({8} if v < 6 else set()) for v, row in enumerate(old)] + [set(range(6))]
        if lifted != graph6(new_record):
            raise AssertionError(new_record)
        colours = stable_colours(lifted, 1 << 8)
        if colours[0] != colours[1] or any(separators(lifted, set(range(9)), 1)):
            raise AssertionError((new_record, colours))
        full_edges = [(0, 1), (0, 2), (1, 2), (0, 11), (1, 3), (2, 4)]
        full_edges.extend((v + 3, u + 3) for v, row in enumerate(lifted) for u in row if v < u)
        full = adjacency(12, full_edges)
        unvisited = frozenset(range(3, 12))
        good = legal_suffixes(full, (0, 2, 1), unvisited)
        bad = legal_suffixes(full, (0, 1, 2), unvisited)
        if (3, 6, 9, 4, 7, 10, 5, 8, 11) not in good or bad:
            raise AssertionError((new_record, good, bad))
    print("Verified both lifted examples as full twelve-vertex inputs.")


def clique_separator_example(connectivity):
    base = graph6("GCOe`W")
    base_edges = [(v, u) for v, row in enumerate(base) for u in row if v < u]
    outside = len(base) + connectivity - 1
    order = outside + connectivity
    hubs = tuple(range(outside, order))
    edges = base_edges + list(combinations(hubs, 2))
    edges.extend((v, hub) for v in range(outside) for hub in hubs)
    return adjacency(order, edges), hubs


def verify_higher_connectivity():
    for connectivity in (3, 4):
        neighbors, hubs = clique_separator_example(connectivity)
        order = len(neighbors)
        vertices = set(range(order))
        terminal = hubs[0]
        if any(separators(neighbors, vertices, connectivity - 1)):
            raise AssertionError((connectivity, "unexpected smaller cut"))
        if len(list(components(neighbors, vertices.difference(hubs)))) != connectivity:
            raise AssertionError((connectivity, "unexpected components after deleting the hubs"))
        colours = stable_colours(neighbors, 1 << terminal)
        success, failure = spanning_finish_masks(neighbors)[:2]
        if colours[0] != colours[1] or not (success & (1 << terminal)) or (failure & (1 << terminal)):
            raise AssertionError((connectivity, colours, success, failure))
        if connectivity == 4 and any((1, terminal) not in pairs for pairs in controls(neighbors).values()):
            raise AssertionError("The four-connected example should survive all the cut controls")
        print(f"Verified {connectivity}-connected residual counterexample on {order} vertices.")


def census(paths):
    for path in paths:
        total = biconnected = higher_connectivity_failures = 0
        failures = {}
        with path.open(encoding="ascii") as records:
            for line in records:
                record = line.strip()
                if record in ("", ">>graph6<<"):
                    continue
                total += 1
                neighbors = graph6(record)
                vertices = set(range(len(neighbors)))
                if len(vertices) < 3 or any(len(row) < 2 for row in neighbors):
                    continue
                if any(separators(neighbors, vertices, 1)):
                    continue
                biconnected += 1
                marks = tuple(marked for marked, _, _ in mixed_mark_witnesses(neighbors))
                if marks:
                    failures[record] = marks
                    higher_connectivity_failures += not any(separators(neighbors, vertices, 2))
        if path.name == "graph9c.g6" and (total, biconnected, failures) != (261080, 194066, WITNESSES):
            raise AssertionError((path, total, biconnected, failures))
        print(f"{path.name}: {total:,} graphs, {biconnected:,} biconnected, "
              f"{len(failures)} failing graphs, {sum(map(len, failures.values()))} failing marks, "
              f"{higher_connectivity_failures} failures without a two-vertex cut")


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("graph6", nargs="*", type=Path, help="connected graph catalogues")
    args = parser.parse_args()
    verify_lifted_examples()
    verify_controls()
    verify_higher_connectivity()
    census(args.graph6)


if __name__ == "__main__":
    main()
