"""Check structural ordering and its symmetry limits on finite trees."""

from collections import deque
from functools import cache
from graphlib import TopologicalSorter
from itertools import groupby, pairwise, permutations, product
from math import factorial, prod

from check_comparison_cycles import adjacency, cycle_from, successor


def rooted_codes(neighbours):
    @cache
    def code(vertex, parent=None):
        children = sorted(code(child, vertex) for child in neighbours[vertex] if child != parent)
        return "(" + "".join(children) + ")"

    return code


def propagate_codes(neighbours, last_ready_first):
    pending = deque((vertex, incident[0]) for vertex, incident in enumerate(neighbours) if len(incident) == 1)
    messages = {}
    while pending:
        sender, recipient = pending.pop() if last_ready_first else pending.popleft()
        pieces = sorted(
            messages[(other, sender)] for other in neighbours[sender] if other != recipient
        )
        messages[(sender, recipient)] = "(" + "".join(pieces) + ")"
        for target in neighbours[recipient]:
            if target != sender and all(
                (other, recipient) in messages for other in neighbours[recipient] if other != target
            ):
                pending.append((recipient, target))
    return messages


def next_tree_order(trees, size):
    next_trees = {}
    for edges in trees:
        for parent in range(size):
            grown = edges + [(parent, size)]
            code = rooted_codes(adjacency(size + 1, grown))
            canonical = min(code(vertex) for vertex in range(size + 1))
            next_trees.setdefault(canonical, grown)
    return list(next_trees.values())


def tied_groups(neighbours, code):
    groups_by_vertex = []
    for vertex, incident in enumerate(neighbours):
        by_shape = sorted((code(other, vertex), other) for other in incident)
        groups = [
            tuple(other for _, other in group)
            for _, group in groupby(by_shape, key=lambda item: item[0])
        ]
        groups_by_vertex.append(groups)
    return groups_by_vertex


def orders_for_vertex(groups):
    return [
        tuple(other for group in arrangement for other in group)
        for arrangement in product(*(permutations(group) for group in groups))
    ]


def realize(local_orders):
    schedule = TopologicalSorter()
    for vertex, incident in enumerate(local_orders):
        events = [tuple(sorted((vertex, other))) for other in incident]
        for event in events:
            schedule.add(event)
        for earlier, later in pairwise(events):
            schedule.add(later, earlier)
    return tuple(schedule.static_order())


def cycle_graph_code(neighbours, destinations):
    readings = []
    for start in range(len(neighbours)):
        orbit = cycle_from(destinations, start)
        index = {vertex: place for place, vertex in enumerate(orbit)}
        reading = tuple(
            tuple(sorted(index[other] for other in neighbours[vertex])) for vertex in orbit
        )
        readings.append(reading)
    return min(readings)


def check_tied_orders(neighbours, groups):
    permutations_seen = set()
    labelled_count = prod(
        factorial(len(group)) for groups_at_site in groups for group in groups_at_site
    )
    equivalence_code = None
    for local_orders in product(*(orders_for_vertex(groups_at_site) for groups_at_site in groups)):
        destinations = successor(len(neighbours), realize(local_orders))
        assert len(cycle_from(destinations, 0)) == len(neighbours)
        code = cycle_graph_code(neighbours, destinations)
        if equivalence_code is None:
            equivalence_code = code
        assert code == equivalence_code
        permutations_seen.add(destinations)
    assert len(permutations_seen) == labelled_count
    return labelled_count


def check_tree_census():
    known_counts = [1, 1, 1, 2, 3, 6, 11, 23, 47, 106, 235, 551, 1301, 3159]
    trees = [[]]
    tie_resolutions = 0
    print("Sites | All tree shapes | Shapes with no tied branch types")
    for size, total in enumerate(known_counts, start=1):
        assert len(trees) == total
        tie_free = 0
        for edges in trees:
            neighbours = adjacency(size, edges)
            code = rooted_codes(neighbours)
            groups = tied_groups(neighbours, code)
            tie_free += all(len(group) == 1 for site in groups for group in site)
            if 2 <= size <= 8:
                expected = {(u, v): code(u, v) for u, incident in enumerate(neighbours) for v in incident}
                assert propagate_codes(neighbours, last_ready_first=False) == expected
                assert propagate_codes(neighbours, last_ready_first=True) == expected
                tie_resolutions += check_tied_orders(neighbours, groups)
        print(f"{size:>5} | {total:>15,} | {tie_free:>30,}")
        if size < len(known_counts):
            trees = next_tree_order(trees, size)
    print(f"Checked {tie_resolutions:,} tie resolutions on all tree shapes of orders 2–8.")
    print("First-ready and last-ready scheduling both reproduced the recursive branch codes.")


def three_arms(lengths):
    edges = []
    next_site = 1
    for length in lengths:
        current = 0
        for _ in range(length):
            edges.append((current, next_site))
            current = next_site
            next_site += 1
    return adjacency(next_site, edges)


def clipped_code(neighbours, vertex, parent, depth):
    if depth == 0:
        return "()"
    children = sorted(
        clipped_code(neighbours, other, vertex, depth - 1)
        for other in neighbours[vertex]
        if other != parent
    )
    return "(" + "".join(children) + ")"


def unoriented_cycle_code(neighbours, destinations):
    inverse = [0] * len(destinations)
    for site, target in enumerate(destinations):
        inverse[target] = site
    return min(cycle_graph_code(neighbours, destinations), cycle_graph_code(neighbours, inverse))


def check_scope():
    for length in (1, 2, 4, 8, 16):
        neighbours = three_arms((length, length + 1, length + 2))
        for radius in range(1, length + 3):
            codes = {clipped_code(neighbours, other, 0, radius - 1) for other in neighbours[0]}
            assert (len(codes) == 3) == (radius == length + 2)

    neighbours = three_arms((1, 2, 3))
    code = rooted_codes(neighbours)
    by_size = [
        sorted(incident, key=lambda u: (len(code(u, v)), code(u, v)))
        for v, incident in enumerate(neighbours)
    ]
    even_first = [
        sorted(incident, key=lambda u: ((len(code(u, v)) // 2) % 2, len(code(u, v)), code(u, v)))
        for v, incident in enumerate(neighbours)
    ]
    cycles = [successor(len(neighbours), realize(order)) for order in (by_size, even_first)]
    assert unoriented_cycle_code(neighbours, cycles[0]) != unoriented_cycle_code(neighbours, cycles[1])
    print("Verified the unbounded-radius family and the ranking-convention counterexample.")


if __name__ == "__main__":
    check_tree_census()
    check_scope()
