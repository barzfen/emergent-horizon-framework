"""Prepare and measure a Bell pair on two separated LR3 windows."""

from itertools import product
from math import cos, isclose, pi, sin, sqrt

from cross41_growth_and_return import read
from cross48_reversal_interference import support
from cross53_local_phase import labelled_attempt, preparation


def transport(pairs):
    starts = [6]
    for step in range(1, pairs + 1):
        starts.extend((6 + 2 * step, 4 + 2 * step))
    starts.extend((9 + 2 * pairs, 6 + 2 * pairs))
    return tuple(starts)


def follow(branch, starts):
    for start in starts:
        branch = labelled_attempt(branch, start)
    return branch


def prepare_pair(pairs):
    branches, _ = preparation(pairs)
    zero, _, _, both = branches
    route = transport(pairs)
    pulse, relay = 12 + 2 * pairs, 9 + 2 * pairs

    before_pulse = follow(zero, route)
    assert read(before_pulse[0], pulse, 4) == "-++-"
    arm = labelled_attempt(before_pulse, pulse)
    assert arm != before_pulse
    assert labelled_attempt(before_pulse, relay) == before_pulse
    assert labelled_attempt(arm, relay) == follow(both, route)
    assert follow(labelled_attempt(before_pulse, relay), reversed(route)) == zero
    assert follow(labelled_attempt(arm, relay), reversed(route)) == both

    # Apply the same mixing primitive used by the measurements.
    pulse_basis = (before_pulse, arm)
    amplitudes = rotate((1.0, 0.0), pulse_basis, pulse, pi / 4)
    output = [0.0] * len(branches)
    for branch, amplitude in zip(pulse_basis, amplitudes):
        relayed = labelled_attempt(branch, relay)
        destination = follow(relayed, reversed(route))
        output[branches.index(destination)] += amplitude
    assert all(isclose(a, b, abs_tol=1e-12)
               for a, b in zip(output, (1 / sqrt(2), 0, 0, 1 / sqrt(2))))
    return branches, tuple(output)


def rotate(vector, branches, start, angle):
    updated = [0.0] * len(vector)
    for index, (branch, amplitude) in enumerate(zip(branches, vector)):
        target = labelled_attempt(branch, start)
        if target == branch:
            updated[index] += amplitude
            continue
        orientation = 1 if read(branch[0], start, 4) == "-++-" else -1
        updated[index] += cos(angle) * amplitude
        updated[branches.index(target)] += orientation * sin(angle) * amplitude
    return tuple(updated)


def observed(window, branch, zero):
    return 1 if read(branch[0], window, 4) == read(zero[0], window, 4) else -1


def check_exact_bell_table():
    # A settings are Z and X. B uses (Z+X) and (Z-X), each divided by sqrt(2).
    # A pair of coefficients describes aZ+bX.
    expected = (1, 1, 1, -1)
    for index, ((a, b), (c, d)) in enumerate(product(((1, 0), (0, 1)), ((1, 1), (1, -1)))):
        # E(ZZ)=E(XX)=1 on the equal superposition of 00 and 11.
        # E(ZX)=E(XZ)=0. The dephased state retains only E(ZZ).
        assert a * c + b * d == expected[index]
        assert a * c == (1, 1, 0, 0)[index]
    assert sum(expected[:3]) - expected[3] == 4  # S = 4 / sqrt(2).

    # Each deterministic classical local policy has four preassigned answers.
    for a0, a1, b0, b1 in product((-1, 1), repeat=4):
        assert abs(a0 * (b0 + b1) + a1 * (b0 - b1)) == 2


def check_measurements(branches, pair, pairs):
    a_start, b_start = 6, 12 + 2 * pairs
    size = len(branches[0][0])
    # A sign window reads the colours of its five incident vertices.
    a_sites = support(a_start, size) | {(a_start + 4) % size}
    b_sites = support(b_start, size) | {(b_start + 4) % size}
    assert a_sites.isdisjoint(b_sites)
    zero = branches[0]
    for index, branch in enumerate(branches):
        assert labelled_attempt(branch, a_start) == branches[index ^ 1]
        assert labelled_attempt(branch, b_start) == branches[index ^ 2]
        assert observed(a_start, branch, zero) == (-1 if index & 1 else 1)
        assert observed(b_start, branch, zero) == (-1 if index & 2 else 1)

    mixture = ((1, 0, 0, 0), (0, 0, 0, 1))
    for (x, angle_a), (y, angle_b) in product(
        enumerate((0, pi / 4)), enumerate((-pi / 8, pi / 8))
    ):
        first = rotate(rotate(pair, branches, a_start, angle_a), branches, b_start, angle_b)
        second = rotate(rotate(pair, branches, b_start, angle_b), branches, a_start, angle_a)
        assert all(isclose(a, b, abs_tol=1e-12) for a, b in zip(first, second))
        diagonal = []
        for basis in mixture:
            diagonal.append(rotate(rotate(basis, branches, a_start, angle_a), branches, b_start, angle_b))
        for index, (branch, amplitude) in enumerate(zip(branches, first)):
            a = observed(a_start, branch, zero)
            b = observed(b_start, branch, zero)
            correlation = (-1 if x and y else 1) / sqrt(2)
            assert isclose(amplitude ** 2, (1 + a * b * correlation) / 4, abs_tol=1e-12)
            classical_probability = sum(row[index] ** 2 for row in diagonal) / 2
            assert isclose(classical_probability, (1 + a * b * (0 if x else 1 / sqrt(2))) / 4, abs_tol=1e-12)


def main():
    check_exact_bell_table()
    for pairs in range(21):
        branches, pair = prepare_pair(pairs)
        check_measurements(branches, pair, pairs)
    print("Checked labelled preparation and disjoint measurement on 21 cycles, from 22 to 102 vertices.")
    print("Coherent CHSH: 2*sqrt(2). Dephased control: sqrt(2). Classical local bound: 2.")


if __name__ == "__main__":
    main()
