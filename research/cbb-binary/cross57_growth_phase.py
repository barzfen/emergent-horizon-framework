"""Count coloured LR3 lifts under one insertion and check the phase criteria."""

from itertools import product
from math import isclose, pi, sqrt

from cross41_growth_and_return import colours
from cross53_local_phase import labelled_attempt, preparation
from cross54_local_bell import follow, transport
from cross56_diagonal_phase import pulse


def rooted(tour):
    start = tour.index(0)
    return tour[start:] + tour[:start]


def proper(tour, types):
    return all(types[v] != types[w] for v, w in zip(tour, tour[1:] + tour[:1]))


def reverse_three(tour, edge):
    left, right = (edge + 1) % len(tour), (edge + 3) % len(tour)
    result = list(tour)
    result[left], result[right] = result[right], result[left]
    return tuple(result)


def refine(tour, types, edge):
    n = len(tour)
    new_type = 3 - types[tour[edge]] - types[tour[(edge + 1) % n]]
    return rooted(tour[:edge + 1] + (n,) + tour[edge + 1:]), types + (new_type,)


def lifts(parent, target, types):
    n = len(parent)
    endpoints = {refine(target, types, edge): edge for edge in range(n)}
    surviving = {}
    for edge in range(n):
        child, child_types = refine(parent, types, edge)
        for start in range(n + 1):
            moved = reverse_three(child, start)
            if proper(moved, child_types):
                target_edge = endpoints.get((rooted(moved), child_types))
                if target_edge is not None:
                    assert edge not in surviving
                    surviving[edge] = target_edge
    return surviving


def verify_count(types, start):
    n = len(types)
    parent = tuple(range(n))
    target = reverse_three(parent, start)
    left, right = (start + 1) % n, (start + 3) % n
    if types[left] == types[right] or not proper(target, types):
        return False
    surviving = lifts(parent, rooted(target), types)
    blocked = {(start + offset) % n for offset in range(4)}
    assert set(surviving) == set(range(n)) - blocked
    for edge, matched_edge in surviving.items():
        assert (parent[edge], parent[(edge + 1) % n]) == (
            rooted(target)[matched_edge], rooted(target)[(matched_edge + 1) % n]
        )
    # First-hand coefficient norms for the normalized uniform fibre lift.
    fraction = len(surviving) / n
    for diagonal in (-2, -1, 0, 0.5, 1, 2):
        norms = []
        for mode in (1, -1):
            coefficients = [(diagonal + mode) if edge in surviving else 0 for edge in range(n)]
            mean = sum(coefficients) / n
            assert isclose(mean, fraction * (diagonal + mode), abs_tol=1e-12)
            norm = sqrt(sum((value - mean) ** 2 for value in coefficients) / n)
            assert isclose(norm, abs(diagonal + mode) * sqrt(fraction * (1 - fraction)), abs_tol=1e-12)
            norms.append(norm)
        assert max(norms) >= sqrt(fraction * (1 - fraction)) - 1e-12
    return True


def check_echo(pairs, diagonal):
    branches, _ = preparation(pairs)
    route = transport(pairs)
    mixer, relay = 12 + 2 * pairs, 9 + 2 * pairs
    state = {branches[0]: 1}
    for start in route:
        state = pulse(state, start, pi / 2, diagonal)
    state = pulse(state, mixer, pi / 4, diagonal)
    for _ in range(2):
        state = pulse(state, relay, pi / 2, diagonal)
    state = pulse(state, mixer, -pi / 4, diagonal)
    for start in reversed(route):
        state = pulse(state, start, -pi / 2, diagonal)
    return abs(state.get(branches[0], 0)) ** 2


def main():
    count = 0
    for n in range(5, 9):
        for tail in product(range(3), repeat=n - 1):
            types = (0,) + tail
            if proper(tuple(range(n)), types):
                count += sum(verify_count(types, start) for start in range(n))
    print(f"Checked {count} eligible indexed reversals on all rooted colour words of sizes 5–8.")
    assert count == 148
    for pairs in range(21):
        branches, _ = preparation(pairs)
        before_relay = labelled_attempt(follow(branches[0], transport(pairs)), 12 + 2 * pairs)
        assert verify_count(tuple(colours(before_relay[0])), 9 + 2 * pairs)
        assert isclose(check_echo(pairs, 0), 0, abs_tol=1e-12)
        assert isclose(check_echo(pairs, -1), 1, abs_tol=1e-12)
    print("Verified the lift count and same-generator echo on all 21 Bell-carrier sizes.")


if __name__ == "__main__":
    main()
