"""Prepare opposite recorder phases with matched LR3 loops and test classical controls."""

from collections import Counter
from fractions import Fraction
from itertools import product

from cross49_route_recorder import ARRIVAL, P, Q, R, pulse, record
from cross50_cycle_apparatus import M, build_cube, four_cubes, move, total_variation


PRECEDING = {P: 0, Q: P, R: P | Q, M: P | Q | R}
SHAM = (P, P, Q, Q)
LOOP = (P, Q, P, Q)


def lifted_flip(state, bit):
    return state ^ bit, (-1) ** ((state & PRECEDING[bit]).bit_count())


def merge_recorder_arms(cube, starts):
    # Integer numerator of (R + M) / sqrt(2) applied to the all-zero word.
    # The next conditional move acts on the M arm and leaves the R arm alone.
    prepared = [0] * 16
    for arm in (R, M):
        assert move(cube, starts, 0, arm) == arm
        destination, sign = (arm, 1) if arm & R else lifted_flip(arm, M)
        assert destination == (arm if arm & R else move(cube, starts, arm, M))
        prepared[destination] += sign
    assert prepared == [1, 1] + [0] * 14
    return tuple(prepared)


def apply_loop(cube, starts, basis, sequence, controlled=True):
    state, phase = basis, 1
    for bit in sequence:
        if not controlled or state & R:
            next_state, sign = lifted_flip(state, bit)
            assert move(cube, starts, state, bit) == next_state
            state, phase = next_state, phase * sign
    assert cube[state] == cube[basis]
    return phase


def apply_phases(prepared, phases):
    return tuple(amplitude * phase for amplitude, phase in zip(prepared, phases))


def recombine(prepared, denominator):
    # The supplied CROSS-49 pulse and recorder interaction act on the M=0 slice.
    assert not any(prepared[M:])
    final = pulse(record(pulse(prepared[:M])))
    assert sum(x * x for x in final) == 4 * denominator
    return {state: Fraction(x * x, 4 * denominator) for state, x in enumerate(final) if x}


def check_phases(cube, starts):
    prepared = merge_recorder_arms(cube, starts)
    sham = [apply_loop(cube, starts, state, SHAM) for state in cube]
    loop = [apply_loop(cube, starts, state, LOOP) for state in cube]
    global_loop = [apply_loop(cube, starts, state, LOOP, controlled=False) for state in cube]
    assert sham == [1] * 16
    assert loop == [(-1 if state & R else 1) for state in cube]
    assert global_loop == [-1] * 16
    assert Counter(SHAM) == Counter(LOOP)

    plus = apply_phases(prepared, sham)
    minus = apply_phases(prepared, loop)
    assert tuple(x * x for x in plus) == tuple(x * x for x in minus)
    plus_output = recombine(plus, 2)
    minus_output = recombine(minus, 2)
    assert plus_output == {ARRIVAL: Fraction(1, 2), ARRIVAL | R: Fraction(1, 2)}
    assert minus_output == {0: Fraction(1, 2), R: Fraction(1, 2)}
    assert recombine(apply_phases(prepared, global_loop), 2) == plus_output

    dephased = Counter()
    for state in (0, R):
        basis = tuple(int(i == state) for i in cube)
        assert recombine(basis, 1) == recombine(apply_phases(basis, loop), 1)
        for target, chance in recombine(basis, 1).items():
            dephased[target] += chance / 2
    assert dephased == {state: Fraction(1, 4) for state in (0, R, ARRIVAL, ARRIVAL | R)}
    return plus_output, minus_output


def classical_output(cube, starts, mode, setting, coin):
    counts = Counter()
    for recorder, first in product((0, R), (P, Q)):
        state = recorder
        if setting and (mode == "flag" or recorder):
            state = move(cube, starts, state, M)
        # With a full flag, repeat when it is set and switch otherwise.
        # With a branch-only flag, flip a fair coin on the shared unmarked arm.
        repeat = bool(state & M) if mode == "flag" or recorder else bool(coin)
        state = move(cube, starts, state, first)
        state = move(cube, starts, state, first if repeat else ARRIVAL ^ first)
        if mode == "flag" and (state & ARRIVAL) == 0:
            state = move(cube, starts, state, M)
        counts[state] += Fraction(1, 4)
    return counts


def check_partial_memory(cube, starts, targets):
    for distance in (Fraction(i, 4) for i in range(5)):
        for setting, target in enumerate(targets):
            counts = Counter()
            for recorder, first in product((0, R), (P, Q)):
                correct = Fraction(1) if recorder else (1 + distance) / 2
                for estimate, chance in ((setting, correct), (1 - setting, 1 - correct)):
                    state = move(cube, starts, recorder, M if estimate else 0)
                    state = move(cube, starts, state, first)
                    state = move(cube, starts, state, first if state & M else ARRIVAL ^ first)
                    if (state & ARRIVAL) == 0:
                        state = move(cube, starts, state, M)
                    assert not state & M
                    counts[state] += chance / 4
            assert total_variation(counts, target) == (1 - distance) / 4


def check_classical(cube, starts, targets):
    for setting, target in enumerate(targets):
        exact = classical_output(cube, starts, "flag", setting, 0)
        assert exact == target  # The output apparatus bit is also zero.
        branch_only = Counter()
        for coin in (0, 1):
            for state, chance in classical_output(cube, starts, "branch", setting, coin).items():
                branch_only[state & ~M] += chance / 2
        assert total_variation(branch_only, target) == Fraction(1, 4)


def main():
    for slot, seed, starts in four_cubes():
        cube = build_cube(seed, starts)
        targets = check_phases(cube, starts)
        check_classical(cube, starts, targets)
        check_partial_memory(cube, starts, targets)
        print(f"Insertion {slot}: matched loops, exact coherent outputs and classical controls passed.")
    print("Arrival is 1 versus 0. Branch-only memory has tight error 1/4. A full flag fits exactly.")


if __name__ == "__main__":
    main()
