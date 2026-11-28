"""Compare completed flip pairs under constant and switched insertion bias."""

from collections import defaultdict
from fractions import Fraction
from math import exp, isclose, log, prod, sqrt

from cross57_growth_phase import refine
from cross59_growth_ratios import equilibrium_plus, initial_colours


def protocols(steps):
    middle = steps // 2
    return {
        "uniform": [(1, 1)] * steps,
        "fixed": [(2, 1)] * steps,
        "switched": [(2, 1)] * middle + [(1, 2)] * (steps - middle),
    }


def finite_masses(n, plus_count, initial_plus, weights, cap=4):
    """Aggregate a marked port by bulk plus count and number of observed flips."""
    states = {(plus_count, 0): 1}
    for size, (u, v) in enumerate(weights, n):
        following = defaultdict(int)
        for (count, flips), mass in states.items():
            port_plus = initial_plus == (flips % 2 == 0)
            per_weight = mass / (u * count + v * (size - count))
            if flips + 1 < cap:
                next_count, port_weight = (count - 1, u) if port_plus else (count + 2, v)
                following[next_count, flips + 1] += per_weight * port_weight
            background_plus = count - port_plus
            background_minus = size - count - (not port_plus)
            if background_plus:
                following[count - 1, flips] += per_weight * u * background_plus
            if background_minus:
                following[count + 2, flips] += per_weight * v * background_minus
        states = following
    masses = [0] * cap
    for (_, flips), mass in states.items():
        masses[flips] += mass
    return masses + [1 - sum(masses)]


def explicit_masses(colours, weights, cap=4):
    """Follow both ports on actual labelled cycles and read their colour signs."""
    distributions = [[Fraction(0)] * (cap + 1) for _ in range(2)]
    histories = 0

    def visit(tour, types, flips, depth, mass):
        nonlocal histories
        if depth == len(weights):
            for distribution, count in zip(distributions, flips):
                distribution[min(count, cap)] += mass
            histories += 1
            return
        u, v = weights[depth]
        edges = list(zip(tour, tour[1:] + tour[:1]))
        signs = [(types[b] - types[a]) % 3 for a, b in edges]
        edge_weights = [u if sign == 1 else v for sign in signs]
        total = sum(edge_weights)
        for slot, (source, _) in enumerate(edges):
            child, child_types = refine(tour, types, slot)
            following = list(flips)
            if source in (0, 1):
                successor = child[(child.index(source) + 1) % len(child)]
                new_sign = (child_types[successor] - child_types[source]) % 3
                assert new_sign == 3 - signs[slot]
                following[source] += 1
            visit(child, child_types, following, depth + 1, mass * Fraction(edge_weights[slot], total))

    visit(tuple(range(len(colours))), colours, [0, 0], 0, Fraction(1))
    return distributions, histories


def exposure_for_growth(q, u, v, growth):
    """Invert the total size of the deterministic two-sign growth system."""
    spread = sqrt((u + v)**2 + 12 * u * v)
    increasing = (-(u + v) + spread) / 2
    decreasing = (-(u + v) - spread) / 2
    growth_rate = u * q + v * (1 - q)
    coefficient = (growth_rate - decreasing) / spread
    lower, upper = 0.0, log(growth) / min(u, v)
    for _ in range(60):
        middle = (lower + upper) / 2
        size = coefficient * exp(increasing * middle) + (1 - coefficient) * exp(decreasing * middle)
        if size < growth:
            lower = middle
        else:
            upper = middle
    return (lower + upper) / 2


def phase_masses(masses, initial_plus, u, v, exposure):
    """Apply the alternating-rate process with a Poisson number of proposals."""
    proposal_rate = max(u, v)
    proposal_mean = proposal_rate * exposure
    factor = exp(-proposal_mean)
    result = [factor * mass for mass in masses]
    for proposals in range(1, 65):
        following = [0.0] * len(masses)
        following[-1] = masses[-1]
        for flips, mass in enumerate(masses[:-1]):
            port_plus = initial_plus == (flips % 2 == 0)
            hit = (u if port_plus else v) / proposal_rate
            following[flips] += mass * (1 - hit)
            following[flips + 1] += mass * hit
        masses = following
        factor *= proposal_mean / proposals
        for flips, mass in enumerate(masses):
            result[flips] += factor * mass
    assert isclose(sum(result), 1, abs_tol=1e-13, rel_tol=0)
    return result


def tick_masses(flip_masses):
    return [sum(flip_masses[:2]), sum(flip_masses[2:4]), flip_masses[4]]


def switched_gaps(a, b):
    """The constant and linear coefficients of the tail-gap series at weights (2, 1)."""
    first_a, first_b = exp(-a) - exp(-2 * a), exp(-b) - exp(-2 * b)
    second_a = 2 * (a * (exp(-a) + exp(-2 * a)) - 2 * first_a)
    second_b = 2 * (b * (exp(-b) + exp(-2 * b)) - 2 * first_b)
    return 3 * first_a * first_b, 3 * (second_a * first_b + first_a * second_b)


def verify_finite():
    checked = 0
    for n, count in ((6, 3), (7, 2), (8, 4)):
        colours = initial_colours(n, count, 1)
        for weights in protocols(4).values():
            explicit, histories = explicit_masses(colours, weights)
            exact_weights = [(Fraction(u), Fraction(v)) for u, v in weights]
            finite = [finite_masses(n, count, sign, exact_weights) for sign in (True, False)]
            assert explicit == finite and histories == prod(range(n, n + 4))
            checked += histories
    print(f"Both ports matched exact counts over {checked:,} labelled insertion histories.")


def verify_limits():
    q = equilibrium_plus(2, 1)
    a = exposure_for_growth(q, 2, 1, 1.5)
    b = exposure_for_growth(q, 1, 2, 4 / 3)
    print(f"Switched exposures: {a:.9f}, {b:.9f}.")
    phases = {
        "uniform": [(1, 1, log(2))],
        "fixed": [(2, 1, exposure_for_growth(q, 2, 1, 2))],
        "switched": [(2, 1, a), (1, 2, b)],
    }
    for protocol, schedule in phases.items():
        limit = []
        for sign in (True, False):
            masses = [1, 0, 0, 0, 0]
            for u, v, exposure in schedule:
                masses = phase_masses(masses, sign, u, v, exposure)
            limit.append(tick_masses(masses))
        gaps = (limit[1][0] - limit[0][0], limit[0][2] - limit[1][2])
        predicted = switched_gaps(a, b) if protocol == "switched" else (0, 0)
        assert all(isclose(gap, expected, abs_tol=1e-13, rel_tol=0) for gap, expected in zip(gaps, predicted))
        print(f"{protocol}        starts + / −")
        for n in (50, 200, 800):
            counts = (k for k in range(2, n - 1) if (2 * k - n) % 3 == 0)
            count = min(counts, key=lambda k: abs(k - n * q))
            values = [tick_masses(finite_masses(n, count, sign, protocols(n)[protocol])) for sign in (True, False)]
            print(f"  {n:5d}, >=1 tick: {1 - values[0][0]:.8f} / {1 - values[1][0]:.8f}")
        print(f"  limit, >=1 tick: {1 - limit[0][0]:.8f} / {1 - limit[1][0]:.8f}")
        print(f"  limit, >=2 ticks: {limit[0][2]:.8f} / {limit[1][2]:.8f}")
        for finite, reference in zip(values, limit):
            assert all(abs(value - target) < 0.002 for value, target in zip(finite, reference))


if __name__ == "__main__":
    verify_finite()
    verify_limits()
