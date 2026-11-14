"""Check one symmetric LR3 Hamiltonian across Bell preparation and readout."""

from collections import defaultdict
from itertools import product
from math import atan, cos, hypot, isclose, pi, sin, sqrt

from cross48_reversal_interference import support
from cross53_local_phase import labelled_attempt, preparation
from cross54_local_bell import observed, transport


TOLERANCE = 1e-12


def hop(state, start, angle, coherent=True):
    """On eligible pairs apply exp(-i angle X), or its measured stochastic kernel."""
    output = defaultdict(complex if coherent else float)
    for branch, weight in state.items():
        target = labelled_attempt(branch, start)
        if target == branch:
            output[branch] += weight
        elif coherent:
            output[branch] += cos(angle) * weight
            output[target] -= 1j * sin(angle) * weight
        else:
            output[branch] += cos(angle) ** 2 * weight
            output[target] += sin(angle) ** 2 * weight
    return {branch: weight for branch, weight in output.items() if abs(weight) > TOLERANCE}


def prepare(pairs, angle, coherent=True, inverse=True):
    branches, _ = preparation(pairs)
    schedule = transport(pairs)
    state = {branches[0]: 1}
    for start in schedule:
        state = hop(state, start, pi / 2, coherent)
    state = hop(state, 12 + 2 * pairs, angle, coherent)
    state = hop(state, 9 + 2 * pairs, pi / 2, coherent)
    for start in reversed(schedule):
        state = hop(state, start, -pi / 2 if inverse else pi / 2, coherent)
    return branches, state


def statistics(branches, prepared, pairs, bob_angle, coherent):
    first, second = 6, 12 + 2 * pairs
    correlations = []
    for angle_a, angle_b in product((0, pi / 4), (bob_angle, -bob_angle)):
        state = hop(hop(prepared, first, angle_a, coherent), second, angle_b, coherent)
        flipped = hop(hop(prepared, second, angle_b, coherent), first, angle_a, coherent)
        assert all(abs(state.get(branch, 0) - flipped.get(branch, 0)) < TOLERANCE
                   for branch in state.keys() | flipped.keys())
        assert state.keys() <= set(branches)
        weights = {branch: abs(value) ** 2 if coherent else value for branch, value in state.items()}
        assert isclose(sum(weights.values()), 1, abs_tol=TOLERANCE)
        correlations.append(sum(
            weight * observed(first, branch, branches[0]) * observed(second, branch, branches[0])
            for branch, weight in weights.items()
        ))
    return correlations


def verify_bell(pairs, angle):
    branches, coherent = prepare(pairs, angle)
    for branch in (branches[0], branches[3]):
        count = 0
        for start in transport(pairs):
            target = labelled_attempt(branch, start)
            count += target != branch
            branch = target
        assert count == pairs + 2
    _, classical = prepare(pairs, angle, coherent=False)
    _, forward_only = prepare(pairs, angle, inverse=False)
    assert all(isclose(probability, abs(coherent.get(branch, 0)) ** 2, abs_tol=TOLERANCE)
               for branch, probability in classical.items())
    expected = (cos(angle), 0, 0, -sin(angle))
    for state, phase in ((coherent, 1), (forward_only, (-1) ** (pairs + 2))):
        assert state.keys() <= {branches[0], branches[3]}
        assert all(abs(state.get(branch, 0) - phase * value) < TOLERANCE
                   for branch, value in zip(branches, expected))
    size = len(branches[0][0])
    assert (support(6, size) | {10}).isdisjoint(support(12 + 2 * pairs, size) | {16 + 2 * pairs})
    visibility = sin(2 * angle)
    for bob in (pi / 8, atan(visibility) / 2):
        cosine, sine = cos(2 * bob), sin(2 * bob)
        quantum = statistics(branches, coherent, pairs, bob, True)
        dephased = statistics(branches, classical, pairs, bob, False)
        for result, target in (
            (quantum, (cosine, cosine, visibility * sine, -visibility * sine)),
            (dephased, (cosine, cosine, 0, 0)),
        ):
            assert all(isclose(a, b, abs_tol=TOLERANCE) for a, b in zip(result, target))
    return sqrt(2) * (1 + visibility), 2 * hypot(1, visibility)


def main():
    angles = (0, pi / 24, pi / 12, pi / 8, pi / 6, pi / 4)
    for angle in angles:
        fixed, tuned = verify_bell(3, angle)
        print(f"Pulse {angle / pi:.6f} pi: fixed S={fixed:.9f}, retuned S={tuned:.9f}")
    for pairs in range(21):
        verify_bell(pairs, pi / 4)
    verify_bell(3, pi / 2)
    assert sqrt(2) * (1 + sin(pi / 12)) < 2
    assert sqrt(2) * (1 + sin(pi / 6)) > 2
    print("Symmetric hopping and forward-only transport checked on 22–102 vertices.")
    print("Same single-pulse probabilities. Classical fixed-setting CHSH = sqrt(2).")


if __name__ == "__main__":
    main()
