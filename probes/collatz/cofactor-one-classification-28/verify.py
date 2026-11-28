from fractions import Fraction
from math import gcd


P = 1193652440098
Q = 753110839881
PRELIMINARY_LIMIT = 10**11
FINAL_LIMIT = 30


def log_interval(a, terms=64):
    """Bound log(a) with a rational series and a geometric tail bound."""
    z = Fraction(a - 1, a + 1)
    lower = 2 * sum(z ** (2 * j + 1) / (2 * j + 1) for j in range(terms))
    tail = 2 * z ** (2 * terms + 1) / ((2 * terms + 1) * (1 - z * z))
    return lower, lower + tail


def valuation(n, prime):
    exponent = 0
    while n % prime == 0:
        n //= prime
        exponent += 1
    return exponent


def step(n):
    return (3 * n + 1) // 2 if n % 2 else n // 2


def verify_bounds():
    low2, high2 = log_interval(2)
    low3, high3 = log_interval(3)
    assert Fraction(1, 2) < low2 < high2 < 1
    assert 1 < low3 < high3 < Fraction(6, 5)
    # Upper bounds for the two-log Matveev coefficient.
    assert 2**9 < 23**2
    assert Fraction(14, 10) * 30**5 * 23 * Fraction(6, 5) < 10**9
    # exp(30) > (5/2)^30 > 4 * PRELIMINARY_LIMIT.
    assert 5**30 > 4 * PRELIMINARY_LIMIT * 2**30
    assert PRELIMINARY_LIMIT > 31 * 10**9 + 30

    ratio = Fraction(P, Q)
    error = Fraction(1, Q**2)
    assert ratio - error < low3 / high2 < high3 / low2 < ratio + error
    assert gcd(P, Q) == 1 and Q > 2 * PRELIMINARY_LIMIT
    assert 3 ** (FINAL_LIMIT + 1) > 16 * Q * (FINAL_LIMIT + 1)


def classify():
    cases = []
    for q in range(1, FINAL_LIMIT + 1):
        peak = 3**q - 1
        e = valuation(peak, 2)
        assert e == (1 if q % 2 else 2 + valuation(q, 2))
        destination = peak >> e
        shifted = destination + 1
        r = valuation(shifted, 2)
        odd_part = shifted >> r
        b = valuation(odd_part, 3)
        if odd_part != 3**b:
            continue

        starts = []
        for length in range(1, q + 1):
            start = 2**length * 3 ** (q - length) - 1
            state = start
            for _ in range(length):
                assert state % 2 == 1
                state = step(state)
            assert state == peak
            for _ in range(e):
                assert state % 2 == 0
                state = step(state)
            assert state == destination and state % 2 == 1
            starts.append(start)
        cases.append((q, e, r, b, destination, sorted(starts)))
    return cases


if __name__ == "__main__":
    verify_bounds()
    cases = classify()
    assert cases == [
        (1, 1, 1, 0, 1, [1]),
        (2, 3, 1, 0, 1, [3, 5]),
        (4, 4, 1, 1, 5, [15, 23, 35, 53]),
    ]
    for case in cases:
        print(case)
