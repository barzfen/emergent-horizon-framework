"""Finite illustration of repetition and residue tests in COLLATZ-12."""

from math import log2
from random import Random


def numerator_residue(word):
    a, b, modulus = 1, 0, 1
    for bit in word:
        if bit:
            a, b = 3 * a, 3 * b + modulus
        modulus *= 2
    return -b * pow(a, -1, modulus) % modulus


def common_prefix(left, right):
    for i, (a, b) in enumerate(zip(left, right)):
        if a != b:
            return i
    return len(left)


def main():
    starts, length = 1280, 320
    rng = Random(7)
    bits = bytes([1] * 16 + [int(rng.randrange(4) != 0) for _ in range(starts + length - 17)])
    multiplier, modulus = 1, 1
    for bit in bits:
        multiplier *= 3 if bit else 1
        modulus *= 2
        assert multiplier >= modulus

    windows = sorted(bits[i:i + length] for i in range(starts))
    longest = max(common_prefix(a, b) for a, b in zip(windows, windows[1:]))
    assert longest < length
    print(f"{starts} distinct windows; longest common prefix = {longest} bits")

    residues = [numerator_residue(word) for word in windows]
    modulus = 1 << length
    bound = 1 << (starts // 5)
    for q in (1, 3, 5):
        scaled = [q * r % modulus for r in residues]
        closest = min(min(r, modulus - r) for r in scaled)
        assert closest > bound
        print(f"q={q}: all residue magnitudes exceed 2^{starts // 5}; minimum has {closest.bit_length()} bits")

    chi = 0.75 * log2(3) - 1
    entropy = 2 - 0.75 * log2(3)
    print(f"Growth exponent {chi:.9f}; entropy per step {entropy:.9f}")


if __name__ == "__main__":
    main()
