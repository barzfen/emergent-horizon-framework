"""Finite illustration of the two tests in COLLATZ-07."""

from fractions import Fraction
from random import Random


def branch(length, seed):
    baseline = []
    multiplier = 1
    modulus = 1
    for _ in range(length + 12):
        modulus *= 2
        bit = int(multiplier < modulus)
        multiplier *= 3 if bit else 1
        baseline.append(bit)

    marked = set()
    for exponent in range(4, length.bit_length()):
        start = 1 << exponent
        if start >= length:
            break
        zeros = [i for i in range(start, start + 12) if baseline[i] == 0]
        assert len(zeros) >= 4
        marked.update(zeros[:4])

    rng = Random(seed)
    bits = baseline.copy()
    for i, bit in enumerate(baseline[:length]):
        if bit == 0:
            assert baseline[i + 1] == 1
            if i in marked:
                bits[i] = 1
            elif rng.getrandbits(1):
                bits[i], bits[i + 1] = 1, 0
    return bytes(bits[:length])


def residue(word):
    multiplier, offset, modulus = 1, 0, 1
    for bit in word:
        if bit:
            multiplier, offset = 3 * multiplier, 3 * offset + modulus
        modulus *= 2
    return -offset * pow(multiplier, -1, modulus) % modulus


def recover_parities(n, q, steps):
    word = bytearray()
    for _ in range(steps):
        odd = n % 2
        word.append(odd)
        n = (3 * n + q) // 2 if odd else n // 2
    return bytes(word)


def main():
    m = 10
    starts, short, long = 1 << m, 6 * m, 30 * m
    bits = branch(starts + long - 1, seed=7)
    assert len({bits[i:i + short] for i in range(starts)}) == starts

    cumulative = Fraction(1)
    peak = cumulative
    for bit in bits:
        cumulative *= Fraction(3, 2) if bit else Fraction(1, 2)
        assert cumulative >= 1
        peak = max(peak, cumulative)

    modulus = 1 << long
    windows = [bits[i:i + long] for i in range(starts)]
    residues = [residue(word) for word in windows]
    assert len(set(residues)) == starts
    print(f"{starts} distinct windows at both lengths {short} and {long}")
    for q in (1, 3, 5):
        bound = peak * (10**9 + Fraction(q * starts, 3))
        for word, r in zip(windows, residues):
            r = q * r % modulus
            assert recover_parities(r, q, long) == word
            assert min(r, modulus - r) > bound
        print(f"All {starts} length-{long} residues exceed the orbit-height bound for q={q}")


if __name__ == "__main__":
    main()
