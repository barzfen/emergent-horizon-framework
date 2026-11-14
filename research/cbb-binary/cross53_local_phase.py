"""Audit phase readout with both the setting and readout subject to locality."""

from collections import Counter
from fractions import Fraction

from cross48_reversal_interference import swapped_positions
from cross49_route_recorder import R
from cross50_cycle_apparatus import M
from cross52_setting_isolation import attempt, setup


def labelled_attempt(branch, start):
    signs, labels = branch
    target = attempt(signs, start)
    if signs == target:
        return branch
    first, second = swapped_positions(start, len(signs))
    updated = list(labels)
    updated[first], updated[second] = updated[second], updated[first]
    return target, tuple(updated)


def preparation(pairs):
    (plain, marked, relative), _, region = setup(pairs)
    idle = plain, tuple(range(len(plain)))
    flagged = marked, relative
    return (idle, labelled_attempt(idle, 6), flagged, labelled_attempt(flagged, 6)), region


def reduction(pair, region, phase=1):
    """Return twice the reduced density matrix, in its local label basis."""
    outside = tuple(i for i in range(len(pair[0][1])) if i not in region)
    a, b = (tuple(labels[i] for i in region) for _, labels in pair)
    result = Counter(((a, a), (b, b)))
    left, right = (labels for _, labels in pair)
    assert left != right
    if all(left[i] == right[i] for i in outside):
        result[(a, b)] += phase
        result[(b, a)] += phase
    return result


def audit_region(pairs, budget, expected):
    branches, region = preparation(pairs)
    frontier = {branches}
    seen = set(frontier)
    for depth in range(budget + 1):
        for state in frontier:
            assert reduction(state[:2], region) == reduction(state[2:], region)
            tagged = state[0], state[3]
            assert reduction(tagged, region, 1) == reduction(tagged, region, -1)
        if depth != budget:
            frontier = {
                next_state
                for state in frontier
                for start in range(len(branches[0][0]))
                if (next_state := tuple(labelled_attempt(branch, start) for branch in state)) not in seen
            }
            seen.update(frontier)
    assert len(seen) == expected
    print(f"{len(branches[0][0])} vertices: {len(seen)} joint states through {budget} attempts.")


def check_leak_after_deadline():
    branches, region = preparation(3)
    for start in (12, 15, 12, 10, 8):
        branches = tuple(labelled_attempt(branch, start) for branch in branches)
    assert reduction(branches[:2], region) != reduction(branches[2:], region)
    print("At the fifth attempt the remote flag can change the reduced state on 34 vertices.")


def check_two_readers():
    # Numerators for |00> +/- |11>, followed by H on the two individual bits.
    # Bit masks use the actual R and M coordinates of the reversal cube.
    branches, _ = preparation(3)
    branch_map = dict(zip((0, R, M, R | M), branches))
    size = len(branches[0][0])
    for bits, branch in branch_map.items():
        assert labelled_attempt(branch, 6) == branch_map[bits ^ R]
        assert labelled_attempt(branch, 18) == branch_map[bits ^ M]
    assert size == 34

    for setting in (0, 1):
        # The remote setting is the supplied diagonal phase on the M window.
        phase = (-1) ** setting
        joint = {
            out: Fraction((1 + phase * (-1) ** (out.bit_count())) ** 2, 8)
            for out in branch_map
        }
        assert sum(joint.values()) == 1
        for reader in (R, M):
            assert sum(p for out, p in joint.items() if out & reader) == Fraction(1, 2)
        assert sum(p for out, p in joint.items() if out.bit_count() % 2 == setting) == 1
        print(f"Remote setting {setting}: unbiased local marginals, joint parity {setting}.")

    # Exact classical control: pre-share one fair bit; M XORs the setting into it.
    for setting in (0, 1):
        classical = {(bit * R) | ((bit ^ setting) * M): Fraction(1, 2) for bit in (0, 1)}
        assert classical == {
            out: Fraction(1, 2) for out in branch_map if out.bit_count() % 2 == setting
        }


def check_bell_benchmark():
    # Supplied local observables, each a linear combination of Z and the LR3 bit flip X.
    # On (|00> + |11>)/sqrt(2), E(ZZ)=E(XX)=1 and E(ZX)=E(XZ)=0.
    state = (1, 0, 0, 1)
    z = ((1, 0), (0, -1))
    x = ((0, 1), (1, 0))
    b = (((1, 1), (1, -1)), ((1, -1), (-1, -1)))
    # Entries of B are divided by sqrt(2). Compute the remaining factors exactly.
    numerators = []
    for a in (z, x):
        for matrix in b:
            numerators.append(Fraction(sum(
                state[2 * i + j] * a[i][k] * matrix[j][l] * state[2 * k + l]
                for i in range(2) for j in range(2) for k in range(2) for l in range(2)
            ), 2))
    assert numerators == [1, 1, 1, -1]
    assert sum(numerators[:3]) - numerators[3] == 4
    print("Supplied two-setting Bell benchmark: S=4/sqrt(2).")


def main():
    cases = ((0, 1), (2, 46), (3, 272), (4, 1360), (5, 6784), (6, 30048))
    for pairs, (budget, count) in enumerate(cases):
        audit_region(pairs, budget, count)
    check_leak_after_deadline()
    check_two_readers()
    check_bell_benchmark()


if __name__ == "__main__":
    main()
