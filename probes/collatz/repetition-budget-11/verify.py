"""Exact finite checks for the repetition congruence and word construction."""

from itertools import islice, product


def affine(word, q):
    a, b, m = 1, 0, 1
    for bit in word:
        if bit:
            a, b = 3 * a, 3 * b + q * m
        m *= 2
    return a, b, m


def parities(p, q, steps):
    bits = []
    for _ in range(steps):
        odd = p % 2
        bits.append(odd)
        p = (3 * p + q) // 2 if odd else p // 2
    return tuple(bits)


def check_congruences():
    cases = 0
    for q in (1, 3, 5):
        for d in range(1, 7):
            for word in product((0, 1), repeat=d):
                a, b, m = affine(word, q)
                for repeats in range(1, 4):
                    modulus = m**repeats
                    residue = -b * pow(a - m, -1, modulus) % modulus
                    expected = word * repeats
                    for lift in (-1, 0, 1):
                        assert parities(residue + lift * modulus, q, len(expected)) == expected
                    assert parities(residue + 1, q, len(expected)) != expected
                    cases += 1
    return cases


def all_words():
    length = 1
    while True:
        yield from product((0, 1), repeat=length)
        length += 1


def check_construction():
    word = (1, 1, 1, 0)
    targets = tuple(islice(all_words(), 10))
    for j, target in enumerate(targets):
        length, odds = len(target), sum(target)
        cover = (1,) * (2 * length) + target + (1,) * (length - odds) + (0,) * odds
        switch = (1, 1, 1, 0) if j % 2 else (1, 1, 0, 1)
        new_word = word * 2 + cover + switch
        assert new_word[:2 * len(word)] == word * 2
        assert 4 * sum(new_word) == 3 * len(new_word)
        word = new_word

    a, m = 1, 1
    for bit in word:
        a *= 3 if bit else 1
        m *= 2
        assert a >= m
    return len(word)


if __name__ == "__main__":
    print(f"Verified {check_congruences()} word/denominator/repetition combinations.")
    print(f"Verified a {check_construction()}-bit prefix of the fast-growth family.")
