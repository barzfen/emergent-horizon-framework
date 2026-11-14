"""Compare LR3 adjacency and negative-Laplacian pulses with the same basis probabilities."""

from collections import defaultdict
from cmath import exp
from itertools import product
from math import cos, isclose, pi, sin, sqrt

from cross53_local_phase import labelled_attempt, preparation
from cross54_local_bell import observed, transport
from cross55_symmetric_hopping import TOLERANCE


def pulse(state, start, angle, diagonal):
    output = defaultdict(complex)
    for branch, amplitude in state.items():
        target = labelled_attempt(branch, start)
        if target == branch:
            output[branch] += amplitude
        else:
            weighted = exp(-1j * diagonal * angle) * amplitude
            output[branch] += cos(angle) * weighted
            output[target] -= 1j * sin(angle) * weighted
    return {branch: value for branch, value in output.items() if abs(value) > TOLERANCE}


def prepare(pairs, angle, diagonal, inverse):
    branches, _ = preparation(pairs)
    route = transport(pairs)
    state = {branches[0]: 1}
    for start in route:
        state = pulse(state, start, pi / 2, diagonal)
    state = pulse(state, 12 + 2 * pairs, angle, diagonal)
    state = pulse(state, 9 + 2 * pairs, pi / 2, diagonal)
    for start in reversed(route):
        state = pulse(state, start, -pi / 2 if inverse else pi / 2, diagonal)
    return branches, state


def readout(branches, state, pairs, diagonal):
    a, b = 6, 12 + 2 * pairs
    scores = []
    for x, y in product((0, pi / 4), (pi / 8, -pi / 8)):
        measured = pulse(pulse(state, a, x, diagonal), b, y, diagonal)
        reverse = pulse(pulse(state, b, y, diagonal), a, x, diagonal)
        assert all(abs(measured.get(key, 0) - reverse.get(key, 0)) < TOLERANCE
                   for key in measured.keys() | reverse.keys())
        assert measured.keys() <= set(branches)
        assert isclose(sum(abs(v) ** 2 for v in measured.values()), 1, abs_tol=TOLERANCE)
        scores.append(sum(abs(v) ** 2 * observed(a, branch, branches[0]) * observed(b, branch, branches[0])
                          for branch, v in measured.items()))
    return scores


def reference_return(branches, state, pairs):
    # Reverse the successful preparation under the adjacency convention.
    # A common reference analyzer converts the relative phase to a basis probability.
    route = transport(pairs)
    for start in route:
        state = pulse(state, start, pi / 2, 0)
    state = pulse(state, 9 + 2 * pairs, -pi / 2, 0)
    state = pulse(state, 12 + 2 * pairs, -pi / 4, 0)
    for start in reversed(route):
        state = pulse(state, start, -pi / 2, 0)
    return abs(state.get(branches[0], 0)) ** 2


def verify(pairs, angle, diagonal, inverse):
    branches, state = prepare(pairs, angle, diagonal, inverse)
    expected = {branches[0]: cos(angle), branches[3]: -exp(-1j * diagonal * pi / 2) * sin(angle)}
    scale = state[branches[0]] / cos(angle)
    assert abs(abs(scale) - 1) < TOLERANCE
    assert state.keys() <= expected.keys()
    assert all(abs(state.get(branch, 0) - scale * value) < TOLERANCE for branch, value in expected.items())
    actual = readout(branches, state, pairs, diagonal)
    term = sin(2 * angle) * cos(pi * diagonal / 2)
    target = [1 / sqrt(2), 1 / sqrt(2), term / sqrt(2), -term / sqrt(2)]
    assert all(isclose(a, b, abs_tol=TOLERANCE) for a, b in zip(actual, target))
    if angle == pi / 4:
        assert isclose(reference_return(branches, state, pairs),
                       (1 + cos(pi * diagonal / 2)) / 2, abs_tol=TOLERANCE)


def check_relay_echo(pairs):
    branches, _ = preparation(pairs)
    route = transport(pairs)
    relay = 9 + 2 * pairs
    mixer = 12 + 2 * pairs
    state = {branches[0]: 1}
    for start in route:
        state = pulse(state, start, pi / 2, 0)
    before_relay = pulse(state, mixer, pi / 4, 0)
    for diagonal in (0, -1, 1, 2):
        after = pulse(pulse(before_relay, relay, pi / 2, diagonal), relay, pi / 2, diagonal)
        assert {k: round(abs(v) ** 2, 12) for k, v in after.items()} == {
            k: round(abs(v) ** 2, 12) for k, v in before_relay.items()
        }
        after = pulse(after, mixer, -pi / 4, 0)
        for start in reversed(route):
            after = pulse(after, start, -pi / 2, 0)
        assert isclose(abs(after.get(branches[0], 0)) ** 2,
                       (1 - cos(pi * diagonal)) / 2, abs_tol=TOLERANCE)


def check_basis_pulses():
    branches, _ = preparation(3)
    words = list(branches)
    branch = branches[0]
    for start in transport(3):
        branch = labelled_attempt(branch, start)
        words.append(branch)
    words.append(labelled_attempt(branch, 18))
    for word, start, angle in product(words, range(34), (pi / 24, pi / 4, pi / 2)):
        original = pulse({word: 1}, start, angle, 0)
        alternate = pulse({word: 1}, start, angle, -1)
        assert original.keys() == alternate.keys()
        assert all(isclose(abs(original[key]) ** 2, abs(alternate[key]) ** 2, abs_tol=TOLERANCE)
                   for key in original)


def main():
    check_basis_pulses()
    for pairs in range(21):
        for diagonal, inverse in product((0, -1, 1, 0.5, 2), (True, False)):
            verify(pairs, pi / 4, diagonal, inverse)
        check_relay_echo(pairs)
    for angle, diagonal in product((0, pi / 24, pi / 12, pi / 6), (0, -1, 0.5)):
        verify(3, angle, diagonal, True)
    print("Both return schedules and the common phase analyzer checked on 21 labelled cycles.")
    print("Fixed CHSH: adjacency = 2 sqrt(2), negative Laplacian = sqrt(2).")
    print("Two positive relay pulses give an exact zero-versus-one return in the reference echo.")


if __name__ == "__main__":
    main()
