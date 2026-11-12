#!/usr/bin/env python3
"""EHF-WIEF-02: orbit decomposition of x -> 2*x mod p**k.

All arithmetic is exact. Large prime-cube cases use modular-order
formulas instead of materialising billions of vertices.
"""
from collections import Counter

PRIMES = (3, 5, 7, 11, 1093, 3511)


def prime_factors(n):
    out = []
    d = 2
    while d*d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out.append(n)
    return out


def order_mod_prime(p):
    d = p - 1
    for q in prime_factors(d):
        while d % q == 0 and pow(2, d // q, p) == 1:
            d //= q
    return d


def order_mod_prime_power(p, k):
    d = order_mod_prime(p)
    for r in range(2, k+1):
        if pow(2, d, p**r) != 1:
            d *= p
    return d


def analytic_counts(p, k):
    per_layer = {}
    for j in range(k):
        r = k-j
        length = order_mod_prime_power(p, r)
        count = ((p-1) * p**(r-1)) // length
        per_layer[j] = (length, count)
    return per_layer


def brute_cycle_counts(modulus, p):
    """Independently enumerate all orbits; -1 is the valuation of zero."""
    seen = bytearray(modulus)
    results = Counter()
    for first in range(modulus):
        if seen[first]:
            continue
        x = first
        length = 0
        while not seen[x]:
            seen[x] = 1
            x = (2*x) % modulus
            length += 1
        assert x == first, (first, x, modulus)
        if first == 0:
            val = -1
        else:
            val = 0
            v = first
            while v % p == 0:
                v //= p
                val += 1
        results[val, length] += 1
    return results


def verify(p, k):
    expected = Counter({(-1, 1): 1})
    for valuation, (length, count) in analytic_counts(p, k).items():
        expected[valuation, length] += count
    observed = brute_cycle_counts(p**k, p)
    assert expected == observed, (p, k, expected, observed)
    assert sum(length*count for (_, length), count in observed.items()) == p**k
    return sum(observed.values())


if __name__ == "__main__":
    for p in PRIMES:
        ds = [order_mod_prime_power(p, k) for k in (1, 2, 3)]
        unit = [(p-1)*p**(k-1)//ds[k-1] for k in (1, 2, 3)]
        full = [1+sum((p-1)*p**(r-1)//ds[r-1] for r in range(1, k+1))
                for k in (1, 2, 3)]
        print(f"p={p:<4} orders={ds} unit_cycles={unit} full_cycles={full}")
        for k in ((1, 2, 3) if p < 20 else (1, 2)):
            count = verify(p, k)
            print(f"  verified all {p**k:,} states modulo p^{k}: {count:,} cycles")
