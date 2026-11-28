"""Estimate the infinite-growth Bayes accuracy for the two Julstce rings."""

import argparse
from math import lgamma, log, sqrt

import numpy as np

from probe import run_lengths


RINGS = ("1100110011111000", "0011110011100110")
IDENTITY = np.arange(6)
REFLECTION = np.array([0, 5, 4, 3, 2, 1])
PERMUTATIONS = [
    np.roll(order, shift)
    for order in (IDENTITY, REFLECTION)
    for shift in (0, 2, 4)
]


def orbit_density(points, exponents):
    # The Dirichlet normalizing constant is common to all six permutations.
    log_normalizer = lgamma(int(exponents.sum()) + 6) - sum(
        lgamma(int(length) + 1) for length in exponents
    )
    orbit_exponents = np.stack([exponents[order] for order in PERMUTATIONS], axis=1)
    return np.exp(np.log(points) @ orbit_exponents + log_normalizer).mean(axis=1)


def estimate(sample_count, seed):
    initial_a, initial_b = (np.array(run_lengths(ring)) for ring in RINGS)
    assert tuple(initial_a) == (2, 2, 2, 5, 3, 2)
    assert tuple(initial_b) == (2, 3, 2, 2, 3, 4)
    rng = np.random.default_rng(seed)
    total = 0.0
    for start in range(0, sample_count, 50_000):
        batch_size = min(50_000, sample_count - start)
        from_a = rng.random(batch_size) < 0.5
        count_a = int(from_a.sum())
        points = np.concatenate((
            rng.dirichlet(initial_a + 1, size=count_a),
            rng.dirichlet(initial_b + 1, size=batch_size - count_a),
        ))
        density_a = orbit_density(points, initial_a)
        density_b = orbit_density(points, initial_b)
        total += (np.maximum(density_a, density_b) / (density_a + density_b)).sum()
    accuracy = total / sample_count
    radius = 0.5 * sqrt(log(40) / (2 * sample_count))
    return accuracy, radius


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=1_000_000)
    parser.add_argument("--seed", type=int, default=515)
    args = parser.parse_args()
    if args.samples < 1:
        parser.error("--samples must be positive")
    accuracy, radius = estimate(args.samples, args.seed)
    print(f"Estimate: {accuracy:.6%}")
    print(f"95% Hoeffding interval: [{accuracy - radius:.6%}, {accuracy + radius:.6%}]")


if __name__ == "__main__":
    main()
