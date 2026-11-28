"""Finite joint-window examples for COLLATZ-13."""

from math import log2
from random import Random


def residues(bits, starts, length, q):
    result = []
    modulus = 1 << length
    for i in range(starts):
        a, b = 1, 0
        for j, bit in enumerate(bits[i:i + length]):
            if bit:
                a, b = 3 * a, 3 * b + q * (1 << j)
        p = -b * pow(a, -1, modulus) % modulus
        result.append(p - modulus if 2 * p >= modulus else p)
    return result


def step(p, q):
    return (3 * p + q) // 2 if p % 2 else p // 2


def longest_fit(values, cutoff):
    longest = current = 0
    for value in values:
        current = current + 1 if abs(value) <= cutoff else 0
        longest = max(longest, current)
    return longest


def main():
    n, d = 1600, 320
    cutoff = 1 << 312
    rng = Random(7)
    bits = bytes([1] * 16 + [int(rng.randrange(4) != 0) for _ in range(n + d - 17)])
    a, modulus = 1, 1
    for bit in bits:
        a *= 3 if bit else 1
        modulus *= 2
        assert a >= modulus

    for q in (1, 3, 5):
        assert 1 << d > 5 * cutoff + q
        values = residues(bits, n, d, q)
        individual = sum(abs(value) <= cutoff for value in values)
        longest = longest_fit(values, cutoff)
        assert 0 < individual < n and longest < n // 25
        print(f"q={q}: {individual}/{n} windows fit; longest fitting run = {longest}")

    for p, q in ((27, 1), (-11, 3)):
        orbit = [p]
        for _ in range(48 + 24 - 2):
            orbit.append(step(orbit[-1], q))
        height = max(map(abs, orbit[:48]))
        assert (1 << 24) > 5 * height + q
        decoded = residues(bytes(p % 2 for p in orbit), 48, 24, q)
        assert decoded == orbit[:48]
        assert all(step(x, q) == y for x, y in zip(decoded, decoded[1:]))
    print("Both known orbit controls stitch exactly.")

    chi = 0.75 * log2(3) - 1
    h = 2 - 0.75 * log2(3)
    gamma, eta, tau = 0.2, 0.195, 0.04
    assert chi < eta < gamma
    assert max(0, eta - chi * tau) < h * (gamma + tau)
    print(f"Full-pass seed-change scale factor: {(1 + gamma) / (eta - chi):.6f}")


if __name__ == "__main__":
    main()
