"""Verify which old swap comparisons change when a tree gains one leaf."""

from itertools import combinations, groupby, product

from check_branch_shape_order import (
    next_tree_order,
    orders_for_vertex,
    realize,
    rooted_codes,
    three_arms,
)
from check_comparison_cycles import adjacency, successor


def add_leaf(neighbours, attachment):
    grown = [incident.copy() for incident in neighbours]
    grown[attachment].append(len(neighbours))
    grown.append([attachment])
    return grown


def rankings(neighbours):
    code = rooted_codes(neighbours)
    return [
        {other: (len(code(other, site)) // 2, code(other, site)) for other in incident}
        for site, incident in enumerate(neighbours)
    ]


def direction(left, right):
    return (left > right) - (left < right)


def changes(old, grown):
    changed_sites = set()
    strict_reversals = set()
    for site, incident in enumerate(old):
        for left, right in combinations(incident, 2):
            before = direction(incident[left], incident[right])
            after = direction(grown[site][left], grown[site][right])
            if before != after:
                changed_sites.add(site)
            if before * after == -1:
                strict_reversals.add(site)
    return changed_sites, strict_reversals


def delete_leaf(destinations):
    leaf = len(destinations) - 1
    return tuple(destinations[leaf] if target == leaf else target for target in destinations[:-1])


def check_cycle_projection(old, grown, strict):
    size = len(old)
    new_orders = [sorted(incident, key=incident.__getitem__) for incident in grown]
    restricted = [[other for other in order if other < size] for order in new_orders[:-1]]
    child = successor(size + 1, realize(new_orders))
    assert delete_leaf(child) == successor(size, realize(restricted))
    if not strict:
        shared_orders = [
            sorted(incident, key=lambda other: (incident[other], grown[site][other]))
            for site, incident in enumerate(old)
        ]
        for site, order in enumerate(shared_orders):
            assert [grown[site][other] for other in order] == sorted(
                grown[site][other] for other in order
            )


def cycle_family(ranking, erase_leaf=False):
    local_choices = []
    for incident in ranking:
        ranked = sorted(incident, key=incident.__getitem__)
        groups = [tuple(group) for _, group in groupby(ranked, key=incident.__getitem__)]
        local_choices.append(orders_for_vertex(groups))

    cycles = set()
    for orders in product(*local_choices):
        cycle = successor(len(ranking), realize(orders))
        cycles.add(delete_leaf(cycle) if erase_leaf else cycle)
    return cycles


def check_census():
    trees = [[]]
    tested = 0
    projection_checks = 0
    family_checks = 0
    first_strict = None
    print("Sites | Attachments | Family preserved | Overlap with change | Disjoint | Max sites changed")
    for size in range(1, 15):
        preserved = overlap = disjoint = most_changed = 0
        for edges in trees:
            neighbours = adjacency(size, edges)
            codes = rooted_codes(neighbours)
            old = rankings(neighbours)
            attachment_types = set()
            for attachment in range(size):
                if codes(attachment) in attachment_types:
                    continue
                attachment_types.add(codes(attachment))
                grown = rankings(add_leaf(neighbours, attachment))
                affected, strict = changes(old, grown)
                assert attachment not in affected
                assert len(affected) <= (size + 1).bit_length() - 2
                most_changed = max(most_changed, len(affected))
                preserved += not affected
                overlap += bool(affected) and not strict
                disjoint += bool(strict)
                if strict and first_strict is None:
                    first_strict = (size, tuple(edges), attachment, tuple(sorted(strict)))
                if size <= 10:
                    check_cycle_projection(old, grown, strict)
                    projection_checks += 1
                if size <= 7:
                    parent_family = cycle_family(old)
                    child_family = cycle_family(grown, erase_leaf=True)
                    assert (parent_family == child_family) == (not affected)
                    assert parent_family.isdisjoint(child_family) == bool(strict)
                    family_checks += 1
        total = preserved + overlap + disjoint
        tested += total
        print(
            f"{size:>5} | {total:>11,} | {preserved:>16,} | "
            f"{overlap:>19,} | {disjoint:>8,} | {most_changed:>17}"
        )
        if size < 14:
            trees = next_tree_order(trees, size)
    print(f"Examined {tested:,} inequivalent attachments and checked {projection_checks:,} cycle projections.")
    print(f"Enumerated both exact cycle families for {family_checks:,} attachments through seven sites.")
    print(f"First strict reversal (size, edges, attachment, sites): {first_strict}")
    assert first_strict[0] == 6


def check_distance_examples():
    for distance in (4, 5, 8, 16, 32, 64):
        parent = three_arms((1, 2, 2 * distance - 3))
        tip = len(parent) - 1
        target = tip - distance
        old = rankings(parent)
        grown = rankings(add_leaf(parent, tip))
        assert target in changes(old, grown)[1]
        for ranking in (old, grown):
            assert all(len(set(row.values())) == len(row) for row in ranking)
    print("Strict reversals verified up to distance 64, with distinct branch types everywhere.")


def check_sharp_bound():
    edges = []
    previous = 0
    for count in range(1, 8):
        size = len(edges) + 1
        copy = [(left + size + 1, right + size + 1) for left, right in edges]
        edges += [(previous, size), (size, previous + size + 1)] + copy
        previous = size
        new_size = len(edges) + 1
        assert new_size == 2 ** (count + 1) - 1
        tree = adjacency(new_size, edges)
        affected, _ = changes(rankings(tree), rankings(add_leaf(tree, 0)))
        assert len(affected) == count
    print("Sharp bound verified for the recursive examples through seven changed sites.")


if __name__ == "__main__":
    check_census()
    check_distance_examples()
    check_sharp_bound()
