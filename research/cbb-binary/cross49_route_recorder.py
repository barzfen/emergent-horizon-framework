"""Audit a reversible LR3 route recorder against coherent and classical controls."""

from collections import Counter
from fractions import Fraction
from itertools import combinations, product

from cross41_growth_and_return import read, split_edge
from cross46_local_clock import INITIAL
from cross48_reversal_interference import clifford_product, labelled_path, successors, support, swapped_positions


P, Q, R = 4, 2, 1
ARRIVAL = P | Q
MASKS = (P, Q, R)


def check_cube(signs, starts):
    size = len(signs)
    windows = [support(start, size) for start in starts]
    assert all(a.isdisjoint(b) for a, b in combinations(windows, 2))
    states = {}
    for bits in range(8):
        path = [start for bit, start in zip(MASKS, starts) if bits & bit]
        target = signs
        for start in path:
            target = dict(successors(target))[start]
        states[bits] = target, labelled_path(size, path)
    assert len({word for word, _ in states.values()}) == 8
    carrier_window, _, recorder_window = starts
    initial_carrier = read(signs, carrier_window, 4)
    initial_recorder = read(signs, recorder_window, 4)
    for bits, (word, _) in states.items():
        assert (read(word, carrier_window, 4) != initial_carrier) == bool(bits & P)
        assert (read(word, recorder_window, 4) != initial_recorder) == bool(bits & R)
    for bits, (word, labels) in states.items():
        for bit, start in zip(MASKS, starts):
            a, b = swapped_positions(start, size)
            changed = list(labels)
            changed[a], changed[b] = changed[b], changed[a]
            assert states[bits ^ bit] == (dict(successors(word))[start], changed)

    lifts = [{(a,): 1, (b,): -1} for a, b in (swapped_positions(i, size) for i in starts)]
    for lift in lifts:
        assert clifford_product(lift, lift) == {(): 2}
    for a, b in combinations(lifts, 2):
        assert clifford_product(a, b) == {blade: -c for blade, c in clifford_product(b, a).items()}


def flip(state, bit):
    preceding = {P: 0, Q: P, R: P | Q}
    sign = (-1) ** ((state & preceding[bit]).bit_count())
    return state ^ bit, sign


def pulse(vector):
    # Integer numerator of the coherent carrier pulse (P + Q) / sqrt(2).
    result = [0] * 8
    for state, amplitude in enumerate(vector):
        for bit in (P, Q):
            target, sign = flip(state, bit)
            result[target] += sign * amplitude
    return tuple(result)


def record(vector):
    # Controlled lifted R. On basis configurations the operation is an LR3 or identity.
    result = [0] * 8
    for state, amplitude in enumerate(vector):
        target, sign = flip(state, R) if state & P else (state, 1)
        result[target] = sign * amplitude
    return tuple(result)


def probability(vector, denominator):
    assert sum(amplitude ** 2 for amplitude in vector) == denominator
    return Fraction(sum(vector[state] ** 2 for state in (ARRIVAL, ARRIVAL | R)), denominator)


def check_coherent():
    basis = [tuple(int(i == state) for i in range(8)) for state in range(8)]
    for state in basis:
        assert record(record(state)) == state
    for a, b in product(range(8), repeat=2):
        assert sum(x * y for x, y in zip(pulse(basis[a]), pulse(basis[b]))) == 2 * (a == b)

    arms = pulse(basis[0])
    tagged = record(arms)
    assert tagged == (0, 0, 1, 0, 0, -1, 0, 0)
    assert pulse(arms) == (2, 0, 0, 0, 0, 0, 0, 0)
    assert probability(pulse(arms), 4) == 0
    assert probability(pulse(tagged), 4) == Fraction(1, 2)
    assert tuple(i for i, amplitude in enumerate(pulse(tagged)) if amplitude) == (0, 1, 6, 7)
    assert probability(pulse(record(tagged)), 4) == 0
    assert probability(record(pulse(tagged)), 4) == Fraction(1, 2)

    # Recorder phases differ, but their probabilities in the cycle basis agree.
    for relative_sign, expected in ((1, 1), (-1, 0)):
        prepared = (1, relative_sign) + (0,) * 6
        assert probability(pulse(record(pulse(prepared))), 8) == expected


def check_classical():
    for initial_tags in ((0,), (0, R)):
        for writes in (0, 1, 2):
            joint = Counter()
            for tag, first, second in product(initial_tags, (P, Q), (P, Q)):
                state = tag ^ first
                if first == P and writes % 2:
                    state ^= R
                joint[state ^ second] += 1
            total = sum(joint.values())
            assert sum(count for s, count in joint.items() if s & ARRIVAL == ARRIVAL) * 2 == total
            if initial_tags == (0,) and writes == 1:
                assert joint == {0: 1, 1: 1, 6: 1, 7: 1}

    # A common classical recombiner cannot fit both the plain and tagged joint tables.
    # x, y, z are its probabilities of returning to 000 from 100, 010, 101.
    # The LP bound is exact; the grid includes a tight legal strategy.
    candidates = []
    for x, y, z in product((Fraction(i, 4) for i in range(5)), repeat=3):
        plain, tagged = (x + y) / 2, (z + y) / 2
        assert tagged >= plain - Fraction(1, 2)
        candidates.append(max(1 - plain, abs(tagged - Fraction(1, 4))))
    assert min(candidates) == Fraction(1, 8)

    # Legal tight control: P arm always repeats, Q arm repeats 3/4 of the time,
    # tagged P arm uses either move uniformly. Check full joint total variation.
    plain = {0: Fraction(7, 8), ARRIVAL: Fraction(1, 8)}
    tagged = {0: Fraction(3, 8), ARRIVAL: Fraction(1, 8), R: Fraction(1, 4), ARRIVAL | R: Fraction(1, 4)}
    target_plain = {0: Fraction(1)}
    target_tagged = {state: Fraction(1, 4) for state in (0, R, ARRIVAL, ARRIVAL | R)}
    for observed, target in ((plain, target_plain), (tagged, target_tagged)):
        assert sum(abs(observed.get(s, 0) - target.get(s, 0)) for s in range(8)) / 2 == Fraction(1, 8)

    # A controller that remembers the first move can spoof either extreme with fair pooled choices.
    for repeat, expected in ((True, 0), (False, 1)):
        seconds = [first if repeat else ARRIVAL ^ first for first in (P, Q)]
        assert set(seconds) == {P, Q}
        assert sum((first ^ second) == ARRIVAL for first, second in zip((P, Q), seconds)) == 2 * expected


if __name__ == "__main__":
    check_cube(INITIAL, (2, 17, 6))
    for slot in range(6, 17):
        grown = split_edge(INITIAL, slot)
        if slot < 10:
            assert 6 not in dict(successors(grown))
        else:
            check_cube(grown, (2, 18, 6))
    check_coherent()
    check_classical()
    print("Eight labelled states and all reversal edges verified in the parent and seven grown cycles.")
    print("Arrival without a record / with a record / after undoing the write: 0, 1/2, 0.")
    print("Coherent recorder phases with identical basis probabilities give arrivals 1 and 0.")
    print("A common classical recombiner misses at least one joint distribution by 1/8 in total variation.")
    print("Independent classical pulses give 1/2; a history-dependent controller can spoof 0 or 1.")
