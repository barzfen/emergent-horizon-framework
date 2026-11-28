#!/usr/bin/env python3
"""Finite audit of antiprimes in the EHF Hamiltonian-cycle counts.

Requires Python 3, standard library only.
The universal theorem depends on Bertrand's postulate and a valuation
inequality, both proved in ANTIPRIME-CYCLE-COUNTS.md. This program merely
checks finite cases and the constructive witness pattern through k=1000.
"""
from math import factorial


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def next_prime(k):
    q = k + 1
    while not is_prime(q):
        q += 1
    return q


def valuation_factorial(k, p):
    total = 0
    while k:
        k //= p
        total += k
    return total


def divisor_count(n):
    assert n >= 1
    count = 1
    p = 2
    while p * p <= n:
        exponent = 0
        while n % p == 0:
            n //= p
            exponent += 1
        if exponent:
            count *= exponent + 1
        p += 1
    return count * (2 if n > 1 else 1)


def record_divisor_sieve(limit):
    divisor_counts = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for m in range(d, limit + 1, d):
            divisor_counts[m] += 1
    records, best = set(), 0
    for m in range(1, limit + 1):
        if divisor_counts[m] > best:
            records.add(m)
            best = divisor_counts[m]
    return records


def main():
    records = record_divisor_sieve(20160)
    hits = []
    for n in range(3, 10):
        count = factorial(n - 1) // 2
        is_record = count in records
        if is_record:
            hits.append(count)
        print(f"n={n:2}: H(n)={count:>8,}, divisors={divisor_count(count):3}, "
              f"highly_composite={is_record}")
    assert hits == [1, 12, 60, 360, 2520, 20160]

    assert 166320 < 181440
    assert divisor_count(166320) == 160
    assert divisor_count(181440) == 140
    print("n=10: 166,320 < 181,440 has 160 > 140 divisors")

    for k in range(10, 1001):
        N = factorial(k) // 2
        q = next_prime(k)
        m = q.bit_length()  # q < 2**m, with m minimal
        a = valuation_factorial(k, 2) - 1
        assert k < q < 2 * k
        assert a >= 2 * m - 1
        assert N % (2 ** m) == 0
        rival = (N // (2 ** m)) * q
        assert rival < N
        if k <= 13:
            assert divisor_count(rival) >= divisor_count(N)
            print(f"n={k+1:2}: H={N:,}, rival={rival:,}; "
                  f"divisors {divisor_count(N)} <= {divisor_count(rival)}")
    print("PASS: constructive inequality spot-checked for k=10..1000")


if __name__ == "__main__":
    main()
