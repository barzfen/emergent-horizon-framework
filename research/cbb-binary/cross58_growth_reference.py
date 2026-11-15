"""Check parity-conjugate growth and stationarity outside the selected reversal lift."""

from collections import defaultdict
from cmath import exp
from fractions import Fraction
from itertools import product
from math import cos, isclose, pi, sin, sqrt


def parity(tour):
    return (-1) ** sum(a > b for i, a in enumerate(tour) for b in tour[i + 1:])


def proper(tour, colours):
    return all(colours[a] != colours[b] for a, b in zip(tour, tour[1:] + tour[:1]))


def children(state):
    tour, colours = state
    size = len(tour)
    for slot, first in enumerate(tour):
        second = tour[(slot + 1) % size]
        new_colour = 3 - colours[first] - colours[second]
        yield tour[:slot + 1] + (size,) + tour[slot + 1:], colours + (new_colour,)


def reversal(state, start):
    tour, colours = state
    first, last = (start + 1) % len(tour), (start + 3) % len(tour)
    if colours[tour[first]] == colours[tour[last]]:
        return state
    moved = list(tour)
    moved[first], moved[last] = moved[last], moved[first]
    moved = tuple(moved)
    return (moved, colours) if proper(moved, colours) else state


def grow(vector, staggered):
    result = defaultdict(complex)
    for state, amplitude in vector.items():
        size = len(state[0])
        for slot, child in enumerate(children(state)):
            sign = (-1) ** (size - 1 - slot)
            assert parity(child[0]) == sign * parity(state[0])
            result[child] += amplitude * (sign if staggered else 1) / sqrt(size)
    return dict(result)


def conjugate(vector):
    return {state: parity(state[0]) * value.conjugate() for state, value in vector.items()}


def pulse(vector, start, time, diagonal):
    result = defaultdict(complex)
    for state, amplitude in vector.items():
        target = reversal(state, start)
        if target == state:
            result[state] += amplitude
        else:
            assert parity(state[0]) == -parity(target[0])
            weight = exp(-1j * time * diagonal) * amplitude
            result[state] += cos(time) * weight
            result[target] -= 1j * sin(time) * weight
    return dict(result)


def equal(left, right):
    return all(abs(left.get(state, 0) - right.get(state, 0)) < 1e-12
               for state in left.keys() | right.keys())


def check_gauge():
    seed = (tuple(range(5)), (0, 1, 0, 1, 2))
    positive = {seed: 1 + 0j}
    paired = conjugate(positive)
    for stage in range(3):
        positive, paired = grow(positive, False), grow(paired, True)
        assert equal(paired, conjugate(positive))
        for start, time in ((2, pi / 4), (3 + stage, pi / 7), (0, pi / 2)):
            positive = pulse(positive, start, time, -1)
            paired = pulse(paired, start, time, 1)
            assert equal(paired, conjugate(positive))
    assert isclose(sum(abs(a) ** 2 for a in positive.values()), 1, abs_tol=1e-12)


def outside_growth_fibre(state):
    size = len(state[0])
    fibre = set(children(state))
    for child in sorted(fibre):
        for start in range(size + 1):
            target = reversal(child, start)
            tour = target[0]
            parent = tuple(label for label in tour if label != size)
            root = parent.index(0)
            if parent[root:] + parent[:root] != state[0]:
                # A fixed-window Hamiltonian has precisely one neighbour of target,
                # so no other child can cancel this off-fibre coefficient.
                assert target not in fibre and reversal(target, start) == child
                return child, start, target
    return None


def check_stationarity_obstruction():
    census = {}
    for size in range(5, 9):
        proper_count = escapes = 0
        for tail in product(range(3), repeat=size - 1):
            state = tuple(range(size)), (0,) + tail
            if not proper(*state):
                continue
            proper_count += 1
            witness = outside_growth_fibre(state)
            assert (witness is not None) == (len(set(state[1])) == 3)
            escapes += witness is not None
        census[size] = proper_count, escapes
    assert census == {5: (10, 10), 6: (22, 20), 7: (42, 42), 8: (86, 84)}
    print("Proper words and off-fibre witnesses:", census)
    seed = (tuple(range(5)), (0, 1, 0, 1, 2))
    _, start, target = outside_growth_fibre(seed)
    for staggered, diagonal in product((False, True), (-1, 0, 1)):
        grown = grow({seed: 1}, staggered)
        assert target not in grown
        assert isclose(abs(pulse(grown, start, pi / 2, diagonal)[target]) ** 2,
                       1 / 5, abs_tol=1e-12)


def check_fixed_reference():
    # Symmetric parent reference, all-slot growth, then project onto the
    # original coherent growth subspace. Use the CROSS-57 selected matching.
    for n in range(5, 103):
        for diagonal in (-1, 1):
            phases = [(-1j) ** (diagonal + 1)] * (n - 4) + [1] * 4
            overlap = sum(phases) / n
            expected = 1 if diagonal == -1 else Fraction((n - 8) ** 2, n ** 2)
            assert isclose(abs(overlap) ** 2, expected, abs_tol=1e-12)
    print("Equal-phase reference on 22 vertices: retention 1 versus 49/121.")


if __name__ == "__main__":
    check_gauge()
    check_stationarity_obstruction()
    check_fixed_reference()
    print("Full basis laws agree under paired conjugation, including three growth steps.")
