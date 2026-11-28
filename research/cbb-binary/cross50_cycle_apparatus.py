"""Represent the classical protocol memory as a fourth legal LR3 move."""

from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import log2

from cross41_growth_and_return import read, split_edge
from cross46_local_clock import INITIAL
from cross48_reversal_interference import labelled_path, successors, support
from cross49_route_recorder import ARRIVAL, P, Q, R, pulse, record


M = 8


def four_cubes():
    expected = {11: 12, 12: 11, 13: 10}
    for slot in range(10, 17):
        seed = split_edge(INITIAL, slot)
        carrier_starts = (2, 18, 6)
        carrier_support = set.union(*(support(i, len(seed)) for i in carrier_starts))
        options = [
            start for start, _ in successors(seed)
            if carrier_support.isdisjoint(support(start, len(seed)))
        ]
        assert options == ([expected[slot]] if slot in expected else [])
        if options:
            yield slot, seed, dict(zip((P, Q, R, M), carrier_starts + (options[0],)))


def build_cube(seed, starts):
    size = len(seed)
    assert all(
        support(a, size).isdisjoint(support(b, size))
        for a, b in combinations(starts.values(), 2)
    )
    cube = {}
    for bits in range(16):
        path = [start for bit, start in starts.items() if bits & bit]
        word = seed
        for start in path:
            word = dict(successors(word))[start]
        cube[bits] = word, labelled_path(size, path)
    assert len({word for word, _ in cube.values()}) == 16
    assert len({tuple(labels) for _, labels in cube.values()}) == 16
    for bits, (word, labels) in cube.items():
        for bit, start in starts.items():
            a, b = (start + 1) % size, (start + 3) % size
            new_labels = labels.copy()
            new_labels[a], new_labels[b] = new_labels[b], new_labels[a]
            assert cube[bits ^ bit] == (dict(successors(word))[start], new_labels)
            assert (read(word, start, 4) != read(seed, start, 4)) == bool(bits & bit)
    return cube


def coherent_outputs(writes):
    arms = pulse((1,) + (0,) * 7)
    for _ in range(writes):
        arms = record(arms)
    return {state: Fraction(amplitude ** 2, 4)
            for state, amplitude in enumerate(pulse(arms)) if amplitude}


def move(cube, starts, state, bit):
    target = state ^ bit
    if bit:
        assert cube[target][0] == dict(successors(cube[state][0]))[starts[bit]]
    return target


def classical_outputs(cube, writes, starts):
    counts = Counter()
    shared_arm_memory = Counter()
    for first, writer_coin, recombination_coin in product((P, Q), range(2), range(2)):
        state = first
        if writes:
            writer_move = R if first == P else M if writer_coin else 0
            state = move(cube, starts, state, writer_move)
        if writes == 2:
            # Undo the realized write by reading its bit, with no saved writer coin.
            state = move(cube, starts, state, state & (R | M))
        # The common recombiner decodes the actual word, with no protocol input.
        word, _ = cube[state]
        seed, _ = cube[0]
        observed = sum(bit for bit, start in starts.items()
                       if read(word, start, 4) != read(seed, start, 4))
        assert observed == state
        if first == Q:
            shared_arm_memory[bool(observed & M)] += 1
        use_other = bool(observed & M) or (bool(observed & R) and recombination_coin)
        arm = observed & ARRIVAL
        second = (ARRIVAL ^ arm) if use_other else arm
        target = move(cube, starts, observed, second)

        # The output 110 identifies exactly the cases with M set.
        # A common reversible cleanup restores M on the reached outputs.
        if (target & ~M) == ARRIVAL:
            target = move(cube, starts, target, M)
        assert not target & M
        counts[target] += 1
    return {state: Fraction(count, 8) for state, count in counts.items()}, shared_arm_memory


def total_variation(a, b):
    return sum(abs(a.get(state, 0) - b.get(state, 0)) for state in a.keys() | b.keys()) / 2


def check_partial_memory():
    target_plain = coherent_outputs(0)
    target_tagged = coherent_outputs(1)
    for distinguishability in map(lambda i: Fraction(i, 16), range(9)):
        error = Fraction(1, 8) - distinguishability / 4
        # A binary apparatus channel encodes the repeat decision on the Q arm.
        repeat_plain = Fraction(3, 4) + distinguishability / 2
        repeat_tagged = repeat_plain - distinguishability
        assert 0 <= repeat_tagged <= repeat_plain <= 1
        plain = {0: (1 + repeat_plain) / 2, ARRIVAL: (1 - repeat_plain) / 2}
        tagged = {
            0: repeat_tagged / 2, ARRIVAL: (1 - repeat_tagged) / 2,
            R: Fraction(1, 4), ARRIVAL | R: Fraction(1, 4),
        }
        assert total_variation(plain, target_plain) == error
        assert total_variation(tagged, target_tagged) == error
    assert coherent_outputs(2) == coherent_outputs(0)


def binary_entropy(p):
    return -p * log2(p) - (1 - p) * log2(1 - p)


def main():
    found = []
    for slot, seed, starts in four_cubes():
        cube = build_cube(seed, starts)
        for writes in range(3):
            actual, memory = classical_outputs(cube, writes, starts)
            assert actual == coherent_outputs(writes)
            expected = {False: 2, True: 2} if writes == 1 else {False: 4}
            assert memory == expected
        found.append((slot, starts[M]))
    assert found == [(11, 12), (12, 11), (13, 10)]
    check_partial_memory()
    required_bits = binary_entropy(0.25) - 0.5
    print(f"Three labelled 16-state constructions: {found}.")
    print("Classical and coherent joint tables agree, and the apparatus bit resets at the output.")
    print("Tight joint-table errors checked for shared-arm distinguishability from 0 to 1/2.")
    print(f"Sharp conditional setting information on the Q arm: {required_bits:.9f} bits.")
    print(f"Conditional setting information averaged across both arms: {required_bits / 2:.9f} bits.")


if __name__ == "__main__":
    main()
