"""Check availability of a marked LR3 after weighted three-colour insertions."""

from collections import defaultdict
from fractions import Fraction
from itertools import accumulate
from math import prod, sqrt


def tracked_probability(n, m, inner_weight, outer_weight):
    """Exact parity formula for rational weights on the four tracked slots."""
    first_total = n - 4 + 2 * (inner_weight + outer_weight)
    modes = [
        prod(Fraction(first_total + j - loss, first_total + j) for j in range(m))
        for loss in (
            2 * inner_weight,
            2 * (inner_weight + outer_weight),
            2 * (inner_weight + 2 * outer_weight),
        )
    ]
    return Fraction(modes[0] + 2 * modes[1] + modes[2], 4)


def sign_probability(n, m, plus_count, outer_sign, plus_weight, minus_weight):
    """Aggregate live histories by plus count and the two boundary signs."""
    weight = {1: plus_weight, -1: minus_weight}
    plus_change = {1: -1, -1: 2}
    states = {(plus_count, outer_sign, outer_sign): 1}
    for size in range(n, n + m):
        following = defaultdict(int)
        for (count, left, right), mass in states.items():
            total = plus_weight * count + minus_weight * (size - count)
            per_weight = mass / total
            following[count + plus_change[left], -left, right] += per_weight * weight[left]
            following[count + plus_change[right], left, -right] += per_weight * weight[right]

            # Inserting into either inner slot removes the history from the live states.
            tracked_plus = 2 * (outer_sign == -1) + (left == 1) + (right == 1)
            background_plus = count - tracked_plus
            background_minus = size - 4 - background_plus
            if background_plus:
                following[count - 1, left, right] += per_weight * background_plus * plus_weight
            if background_minus:
                following[count + 2, left, right] += per_weight * background_minus * minus_weight
        states = following
    return sum(mass for (_, left, right), mass in states.items() if left == right == outer_sign)


def equilibrium_plus(plus_weight, minus_weight):
    """Positive stationary root, in a form that also works for equal weights."""
    linear = plus_weight + 3 * minus_weight
    discriminant = linear**2 + 8 * minus_weight * (plus_weight - minus_weight)
    return 4 * minus_weight / (linear + sqrt(discriminant))


def sign_limit(x, outer_sign, plus_weight, minus_weight):
    q = equilibrium_plus(plus_weight, minus_weight)
    density = plus_weight * q + minus_weight * (1 - q)
    outer_weight = plus_weight if outer_sign == 1 else minus_weight
    inner_weight = plus_weight + minus_weight - outer_weight
    total = inner_weight + outer_weight
    boundary_return = (inner_weight + outer_weight * (1 + x)**(-total / density)) / total
    return (1 + x)**(-2 * inner_weight / density) * boundary_return**2


def initial_colours(n, plus_count, outer_sign):
    """Make a proper ring with the chosen motif on labels 0 through 4."""
    assert 2 <= plus_count <= n - 2 and (2 * plus_count - n) % 3 == 0
    signs = (outer_sign, -outer_sign, -outer_sign, outer_sign)
    signs += (1,) * (plus_count - 2) + (-1,) * (n - plus_count - 2)
    return (0,) + tuple(value % 3 for value in accumulate(signs[:-1]))


def explicit_probabilities(colours, steps, *, tracked_weights=None, sign_weights=None):
    """Enumerate all insertion histories on labels and test the reversed tour directly."""
    point_probabilities = [Fraction(0) for _ in range(steps + 1)]
    leaves = 0

    def visit(tour, types, depth, mass):
        nonlocal leaves
        start = tour.index(1)
        intact = tour[start:start + 3] == (1, 2, 3)
        if intact:
            reversed_tour = tour[:start] + (3, 2, 1) + tour[start + 3:]
            reversed_edges = zip(reversed_tour, reversed_tour[1:] + reversed_tour[:1])
            if all(types[a] != types[b] for a, b in reversed_edges):
                point_probabilities[depth] += mass
        if depth == steps:
            leaves += 1
            return

        size = len(tour)
        edges = list(zip(tour, tour[1:] + tour[:1]))
        weights = [1] * size
        if tracked_weights is not None and intact:
            inner, outer = tracked_weights
            weights[start - 1:start + 3] = (outer, inner, inner, outer)
        if sign_weights is not None:
            plus, minus = sign_weights
            weights = [plus if (types[b] - types[a]) % 3 == 1 else minus for a, b in edges]
        total = sum(weights)
        for index, ((a, b), weight) in enumerate(zip(edges, weights)):
            child = tour[:index + 1] + (size,) + tour[index + 1:]
            visit(child, types + (3 - types[a] - types[b],), depth + 1, mass * Fraction(weight, total))

    visit(tuple(range(len(colours))), colours, 0, Fraction(1))
    return point_probabilities, leaves


def verify_small_cycles():
    checked = 0
    for n, count in ((6, 3), (7, 2), (8, 4)):
        assert tracked_probability(n, 1, 1, 1) == Fraction(n - 4, n)
        for outer_sign in (1, -1):
            colours = initial_colours(n, count, outer_sign)
            for weights in ((1, 1), (1, 2), (2, 1)):
                probabilities, leaves = explicit_probabilities(colours, 4, tracked_weights=weights)
                assert probabilities == [tracked_probability(n, m, *weights) for m in range(5)]
                checked += leaves
            probabilities, leaves = explicit_probabilities(colours, 4, sign_weights=(2, 1))
            for m, probability in enumerate(probabilities):
                assert probability == sign_probability(n, m, count, outer_sign, Fraction(2), Fraction(1))
                assert probability == sign_probability(n, m, n - count, -outer_sign, Fraction(1), Fraction(2))
                assert tracked_probability(n, m, 1, 1) == sign_probability(
                    n, m, count, outer_sign, Fraction(1), Fraction(1)
                )
            checked += leaves
    print(f"Checked exact probabilities through four insertions across {checked:,} complete histories.")


def verify_scaling():
    growth_factor = Fraction(2)
    print("Doubling limits for tracked-slot weights (inner, outer):")
    for inner, outer in ((1, 1), (1, 2), (2, 1)):
        boundary_return = (1 + growth_factor**(-2 * outer)) / 2
        limit = growth_factor**(-2 * inner) * boundary_return**2
        print(f"  ({inner}, {outer})    {limit} = {float(limit):.8f}")
        assert abs(tracked_probability(800, 800, inner, outer) - limit) < Fraction(1, 1000)

    q = equilibrium_plus(2.0, 1.0)
    print("Doubling probabilities for sign weights (+, −) = (2, 1):")
    print("  initial size        + boundaries        − boundaries")
    limits = [sign_limit(1, sign, 2.0, 1.0) for sign in (1, -1)]
    for n in (50, 200, 800):
        compatible_counts = (k for k in range(2, n - 1) if (2 * k - n) % 3 == 0)
        count = min(compatible_counts, key=lambda k: abs(k - n * q))
        values = [sign_probability(n, n, count, sign, 2.0, 1.0) for sign in (1, -1)]
        print(f"  {n:12}        {values[0]:.8f}          {values[1]:.8f}")
    print(f"  {'limit':>12}        {limits[0]:.8f}          {limits[1]:.8f}")
    assert max(abs(value - limit) for value, limit in zip(values, limits)) < 0.001


if __name__ == "__main__":
    verify_small_cycles()
    verify_scaling()
