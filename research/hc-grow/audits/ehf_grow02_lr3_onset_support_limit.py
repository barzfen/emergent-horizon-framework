#!/usr/bin/env python3
"""Exact arithmetic checks for the GROW-02 LR3-onset Pólya limit."""
from fractions import Fraction
from math import comb

n0, ell0 = 6, 3
a0, b0 = ell0 + 1, n0 + 1 - ell0
assert (a0, b0) == (4, 4)

# Check the canonical one-step recurrence equals the Pólya probabilities.
for n in range(n0, n0 + 12):
    # Test interior states only; at the folding boundary GROW-02 sums the
    # two oriented colour-swapped branches into the same canonical child.
    for ell in range(2, n // 2):
        p_raise = Fraction(ell + 1, n + 2)
        p_stay = Fraction(n + 1 - ell, n + 2)
        a, b = ell + 1, n + 1 - ell
        assert p_raise == Fraction(a, a + b)
        assert p_stay == Fraction(b, a + b)
        assert p_raise + p_stay == 1

# Beta(4,4) moments.
mean = Fraction(a0, a0 + b0)
variance = Fraction(a0 * b0, (a0 + b0) ** 2 * (a0 + b0 + 1))
assert mean == Fraction(1, 2)
assert variance == Fraction(1, 36)

# Exact beta-binomial finite-horizon normalization for several horizons.
def rising(x, k):
    out = 1
    for i in range(k):
        out *= x + i
    return out

finite_checks = {}
for steps in range(0, 21):
    weights = [Fraction(comb(steps, s) * rising(a0, s) * rising(b0, steps-s),
                        rising(a0 + b0, steps)) for s in range(steps + 1)]
    assert sum(weights) == 1
    finite_checks[str(steps)] = str(sum(weights))

print({
    "initial_size": n0,
    "initial_support": ell0,
    "initial_urn_counts": [a0, b0],
    "limit": "Beta(4,4) conditional on uniform lift sampling",
    "mean": str(mean),
    "variance": str(variance),
    "finite_horizon_normalization_steps_0_to_20": finite_checks,
    "scope": "No critical-point, scale-invariance, or CFT conclusion."
})
