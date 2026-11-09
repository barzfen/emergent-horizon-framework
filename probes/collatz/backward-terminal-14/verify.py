"""Exact arithmetic controls for the backward terminal test."""

from itertools import product
from random import Random


def affine(bits, q):
    a, b, m = 1, 0, 1
    for bit in bits:
        if bit:
            a, b = 3 * a, 3 * b + q * m
        m *= 2
    return a, b, m


def smallest_start(bits, q):
    a, b, m = affine(bits, q)
    residue = -b * pow(a, -1, m) % m
    return 2 + (residue - 2) % m


def step(p, q):
    return (3 * p + q) // 2 if p % 2 else p // 2


def trajectory(p, q, n):
    states = [p]
    for _ in range(n):
        states.append(step(states[-1], q))
    return states


def main():
    checked = 0
    for q in (1, 3, 5):
        for length in range(1, 9):
            for word in product((0, 1), repeat=length):
                a, b, m = affine(word, q)
                p = smallest_start(word, q)
                orbit = trajectory(p, q, length)
                assert tuple(x % 2 for x in orbit[:-1]) == word
                assert orbit[-1] * m == a * p + b
                assert orbit[-1] % a == b * pow(m, -1, a) % a
                assert smallest_start(word[:-1], q) <= p
                checked += 1

    junctions = 0
    for q in (1, 3, 5):
        for past in product((0, 1), repeat=4):
            a, b, m = affine(past, q)
            past_residue = b * pow(m, -1, a) % a
            for future in product((0, 1), repeat=4):
                c, e, modulus = affine(future, q)
                future_residue = -e * pow(c, -1, modulus) % modulus
                offset = (future_residue - past_residue) * pow(a, -1, modulus) % modulus
                y = past_residue + a * offset
                p = (m * y - b) // a
                states = trajectory(p, q, len(past + future))
                assert states[len(past)] == y
                assert tuple(x % 2 for x in states[:-1]) == past + future
                junctions += 1

    control = trajectory(27, 1, 80)
    word = tuple(p % 2 for p in control[:-1])
    assert smallest_start(word[:20], 1) == smallest_start(word, 1) == 27
    a, b, m = affine(word[:48], 1)
    assert control[48] == (27 * a + b) // m

    rng = Random(7)
    n = 1600
    word = (1,) * 16 + tuple(int(rng.randrange(4) != 0) for _ in range(n - 16))
    a, b, m = affine(word, 1)
    p = smallest_start(word, 1)
    endpoint = (a * p + b) // m
    assert endpoint > 1 << 312
    print(f"Checked {checked} finite words, {junctions} junctions, and a genuine start at 27.")
    print(f"Symbolic example at N={n}: least seed has {p.bit_length()} bits.")
    print(f"Least terminal state has {endpoint.bit_length()} bits; it exceeds 2^312.")


if __name__ == "__main__":
    main()
