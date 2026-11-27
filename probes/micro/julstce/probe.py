"""Exact detector-order decoding under uniform MICRO growth."""

from collections import Counter
from fractions import Fraction
from itertools import groupby
from math import comb, prod

SEED = "0011110011111000"
STEPS = (0, 1, 2, 4, 8, 16, 32)


def valid(ring):
    return all(bit in (ring[i - 1], ring[(i + 1) % len(ring)])
               for i, bit in enumerate(ring))


def detector(ring, start):
    size = len(ring)
    reading = ring[start - 1] != ring[(start + 4) % size]
    slots = [(start + offset) % size for offset in range(4)]
    after = list(ring)
    for left, right in zip(slots, reversed(slots)):
        after[left] = ring[right]
    after = "".join(after)
    return (after if reading and valid(after) else ring), reading


def run_lengths(ring):
    start = next(i for i, bit in enumerate(ring) if bit == "0" and ring[i - 1] == "1")
    return tuple(len(list(run)) for _, run in groupby(ring[start:] + ring[:start]))


def shape(runs):
    # Index 0 starts a zero run. Rotation and reflection must preserve colour.
    reflected = runs[:1] + runs[:0:-1]
    return min(word[i:] + word[:i]
               for word in (runs, reflected) for i in range(0, len(runs), 2))


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def distribution(initial, steps):
    weights = tuple(length + 1 for length in initial)
    factors = [[comb(weight + added - 1, added) for added in range(steps + 1)]
               for weight in weights]
    histogram = Counter()
    for increments in compositions(steps, len(initial)):
        final = tuple(length + added for length, added in zip(initial, increments))
        count = prod(factor[added] for factor, added in zip(factors, increments))
        histogram[shape(final)] += count
    normalizer = comb(sum(weights) + steps - 1, steps)
    assert sum(histogram.values()) == normalizer
    return histogram, normalizer


def direct_distribution(ring, steps):
    """Independent check by constructing every insertion child."""
    states = Counter({ring: 1})
    for _ in range(steps):
        children = Counter()
        for word, count in states.items():
            for edge in range(1, len(word) + 1):
                for bit in "01":
                    child = word[:edge] + bit + word[edge:]
                    if valid(child):
                        children[child] += count
        states = children
    histogram = Counter()
    for word, count in states.items():
        histogram[shape(run_lengths(word))] += count
    return histogram, sum(states.values())


def chance_of_same_one_run(runs):
    weights = [length + 1 for length in runs[1::2]]
    total = sum(weights)
    return Fraction(sum(weight * (weight + 1) for weight in weights),
                    total * (total + 1))


def main():
    assert valid(SEED)
    after_a, a_first = detector(SEED, 0)
    after_b, b_first = detector(SEED, 11)
    ab, b_second = detector(after_a, 11)
    ba, a_second = detector(after_b, 0)
    assert a_first and a_second and b_first and b_second
    assert (ab, ba) == ("1100110011111000", "0011110011100110")
    ab_runs, ba_runs = run_lengths(ab), run_lengths(ba)
    assert len(ab_runs) == len(ba_runs) == 6
    assert sum(ab_runs[1::2]) == sum(ba_runs[1::2]) == 9
    assert chance_of_same_one_run(ab_runs) - chance_of_same_one_run(ba_runs) == Fraction(1, 39)

    for word, runs in ((ab, ab_runs), (ba, ba_runs)):
        for steps in range(4):
            direct, paths = direct_distribution(word, steps)
            urn, normalizer = distribution(runs, steps)
            assert direct.keys() == urn.keys()
            assert all(direct[key] * normalizer == urn[key] * paths for key in urn)

    print("steps | optimal success | success using only longest 1-run")
    previous_success = Fraction(1)
    for steps in STEPS:
        left, normalizer = distribution(ab_runs, steps)
        right, right_normalizer = distribution(ba_runs, steps)
        assert normalizer == right_normalizer
        overlap = sum(min(left[key], right[key]) for key in left.keys() & right.keys())
        success = 1 - Fraction(overlap, 2 * normalizer)
        assert Fraction(1, 2) + Fraction(1, 78) <= success <= previous_success
        previous_success = success

        maxima = [Counter(), Counter()]
        for histogram, marginal in zip((left, right), maxima):
            for runs, count in histogram.items():
                marginal[max(runs[1::2])] += count
        max_overlap = sum(min(maxima[0][key], maxima[1][key])
                          for key in maxima[0].keys() & maxima[1].keys())
        max_success = 1 - Fraction(max_overlap, 2 * normalizer)
        if steps == 1:
            assert sum(count for key, count in maxima[0].items() if key >= 6) == 6
            assert sum(count for key, count in maxima[1].items() if key >= 6) == 0
        print(f"{steps:5} | {float(success):15.6%} | {float(max_success):.6%}"
              f"   (exact: {success}, {max_success})")


if __name__ == "__main__":
    main()
