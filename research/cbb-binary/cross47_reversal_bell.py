"""Verify isolated and overlapping LR3 interventions in a two-reader CHSH test."""

from collections import Counter, deque
from fractions import Fraction
from itertools import product

from cross41_growth_and_return import LR3, read, rewrite
from cross46_local_clock import INITIAL, PHASES, STARTS, observe, updates


SETTINGS = tuple(product(range(2), repeat=2))
REFLECT_COLOURS = str.maketrans("+-", "-+")


def support(size, starts, read_index):
    positions = {(start + offset) % size for start in starts for offset in range(4)}
    return positions | {read_index % size}


def attempt(signs, start):
    start %= len(signs)
    replacement = LR3.get(read(signs, start, 4))
    return signs if replacement is None else rewrite(signs, start, replacement)


def value(signs, index):
    return 1 if signs[index] == "+" else -1


def trial(signs, starts, reads, a_first=True):
    a_start, b_start = starts
    a_read, b_read = reads
    if a_first:
        after_a = attempt(signs, a_start)
        final = attempt(after_a, b_start)
        return (value(after_a, a_read), value(final, b_read)), final
    after_b = attempt(signs, b_start)
    final = attempt(after_b, a_start)
    return (value(final, a_read), value(after_b, b_read)), final


def statistics(ensemble, a_starts, b_starts, reads, a_first=True):
    counts = []
    for x, y in SETTINGS:
        starts = a_starts[x], b_starts[y]
        counts.append(Counter(trial(s, starts, reads, a_first)[0] for s in ensemble))
    correlations = [
        Fraction(sum(a * b * count for (a, b), count in joint.items()), len(ensemble))
        for joint in counts
    ]
    score = abs(sum(correlations[:3]) - correlations[3])
    return counts, correlations, score


def unbiased(joints):
    return all(
        sum(pair[side] * count for pair, count in joint.items()) == 0
        for joint in joints for side in (0, 1)
    )


def preparations(cap):
    seen = {INITIAL}
    pending = deque(seen)
    while pending:
        signs = pending.popleft()
        for _, target in updates(signs, cap):
            if target not in seen:
                seen.add(target)
                pending.append(target)
    return seen


def check_isolated():
    states = preparations(24)
    counts = Counter(map(len, states))
    assert counts == {21: 6, 22: 144, 23: 1134, 24: 4560}
    expected = (Fraction(2, 3), Fraction(5, 18), Fraction(104, 567), Fraction(43, 380))
    for size, expected_score in zip(range(21, 25), expected):
        ensemble = [signs for signs in states if len(signs) == size]
        a_starts = (2, 4)
        b_starts = (size - 6, size - 4)
        reads = (4, size - 4)
        assert support(size, a_starts, reads[0]).isdisjoint(support(size, b_starts, reads[1]))
        for signs in ensemble:
            for x, y in SETTINGS:
                a_start, b_start = a_starts[x], b_starts[y]
                joint = trial(signs, (a_start, b_start), reads)
                assert joint == trial(signs, (a_start, b_start), reads, a_first=False)
                assert joint[0] == (
                    value(attempt(signs, a_start), reads[0]),
                    value(attempt(signs, b_start), reads[1]),
                )
        _, _, score = statistics(ensemble, a_starts, b_starts, reads)
        assert score == expected_score
        print(f"Isolated, {size} vertices, {counts[size]} preparations: S={score}")

    phase_four = INITIAL
    for start in STARTS[:4]:
        phase_four = attempt(phase_four, start)
    assert observe(phase_four) == PHASES[4]
    joints, correlations, score = statistics([INITIAL, phase_four], (2, 4), (15, 17), (2, 19))
    assert unbiased(joints)
    assert correlations == [-1, 1, 1, -1] and score == 2
    print("Isolated two-phase control: unbiased marginals, S=2.")


def check_overlap():
    reflected = INITIAL.translate(REFLECT_COLOURS)
    a_starts, b_starts, reads = (2, 6), (0, 8), (2, 8)
    for signs in (INITIAL, reflected):
        assert all(attempt(signs, start) != signs for start in a_starts)
        assert attempt(signs, 8) == signs
        after_x0 = attempt(signs, 2)
        after_x1 = attempt(signs, 6)
        assert attempt(after_x0, 8) == after_x0
        assert attempt(after_x1, 8) != after_x1
        # In the x=1 branch, B's choice of window flips its recorded sign.
        assert value(attempt(after_x1, 0), 8) != value(attempt(after_x1, 8), 8)
        assert value(attempt(after_x0, 0), 8) != value(attempt(after_x1, 0), 8)
        for x, y in SETTINGS:
            pair, final = trial(signs, (a_starts[x], b_starts[y]), reads)
            mirror_pair, mirror_final = trial(signs.translate(REFLECT_COLOURS), (a_starts[x], b_starts[y]), reads)
            assert mirror_pair == tuple(-output for output in pair)
            assert mirror_final == final.translate(REFLECT_COLOURS)

    ensemble = [INITIAL, reflected]
    joints, correlations, score = statistics(ensemble, a_starts, b_starts, reads)
    assert unbiased(joints)
    assert correlations == [-1, -1, -1, 1] and score == 4
    reversed_joints, reversed_correlations, reversed_score = statistics(
        ensemble, a_starts, b_starts, reads, a_first=False
    )
    assert unbiased(reversed_joints)
    assert reversed_correlations == [-1, -1, 1, 1] and reversed_score == 2
    print("Overlap control: unbiased marginals in both orders, S=4 for A first and S=2 for B first.")


if __name__ == "__main__":
    check_isolated()
    check_overlap()
