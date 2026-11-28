"""Transport label order through rooted nine-site MICRO reversals."""

from itertools import combinations, product

import numpy as np
from scipy.linalg import expm


def admissible(ring):
    return all(bit in (ring[i - 1], ring[(i + 1) % len(ring)])
               for i, bit in enumerate(ring))


def reverse(ring, start, length):
    slots = [(start + offset) % len(ring) for offset in range(length)]
    result = list(ring)
    for target, source in zip(slots, reversed(slots)):
        result[target] = ring[source]
    return tuple(result)


def parity(order):
    return (-1) ** sum(a > b for a, b in combinations(order, 2))


def colour_signs(source, transported_labels):
    return tuple(parity([label for label in transported_labels
                         if source[label] == colour]) for colour in (0, 1))


def build(words, lengths):
    indices = {word: i for i, word in enumerate(words)}
    counts = np.zeros((len(words), len(words)), dtype=int)
    zero = np.zeros_like(counts)
    one = np.zeros_like(counts)
    both = np.zeros_like(counts)
    for i, word in enumerate(words):
        for length in lengths:
            for start in range(len(word)):
                labels = reverse(tuple(range(len(word))), start, length)
                target = tuple(word[label] for label in labels)
                if target == word or not admissible(target):
                    continue
                j = indices[target]
                z, o = colour_signs(word, labels)
                assert z * o == parity(labels) * parity(word) * parity(target)
                counts[i, j] += 1
                zero[i, j] += z
                one[i, j] += o
                both[i, j] += z * o
    assert all(np.array_equal(matrix, matrix.T) for matrix in (counts, zero, one, both))
    return counts, zero, one, both


def switching_signs(matrix, overall_sign):
    """Solve H = overall_sign × D |H| D with a diagonal sign matrix D."""
    assigned = {}
    for root in range(len(matrix)):
        if root in assigned:
            continue
        assigned[root] = 1
        stack = [root]
        while stack:
            i = stack.pop()
            for j in np.flatnonzero(matrix[i]):
                candidate = assigned[i] * overall_sign * np.sign(matrix[i, j])
                if j not in assigned:
                    assigned[j] = candidate
                    stack.append(j)
                elif assigned[j] != candidate:
                    return None
    return np.array([assigned[i] for i in range(len(matrix))])


def distance(signed, control, time):
    distributions = [abs(expm(-1j * h * time)[:, 0]) ** 2
                     for h in (signed, control)]
    assert all(np.isclose(np.sum(p), 1) for p in distributions)
    return np.sum(abs(distributions[0] - distributions[1])) / 2


def main():
    words = [w for w in product((0, 1), repeat=9) if sum(w) == 4 and admissible(w)]
    idx = lambda word: words.index(tuple(map(int, word)))
    assert len(words) == 18 and idx("000001111") == 0

    counts, zero, one, both = build(words, range(2, 8))
    assert counts.sum() == 252 and np.count_nonzero(counts) == 162
    for matrix in (zero, one):
        assert np.count_nonzero((counts != 0) & (matrix == 0)) == 18
        assert all(switching_signs(matrix, s) is None for s in (1, -1))
    assert np.array_equal(both != 0, counts != 0)
    signs = switching_signs(both, -1)
    assert np.array_equal(both, -signs[:, None] * abs(both) * signs[None, :])
    reduced = np.count_nonzero(abs(both) < counts) // 2
    assert reduced > 0
    print(f"Both-colour sign reduces {reduced} link magnitudes without deleting links")

    seed = words[0]
    original_labels = tuple(range(9))
    first = reverse(original_labels, 4, 5)
    returned = reverse(first, 3, 7)
    assert tuple(seed[label] for label in first) == words[idx("000011110")]
    assert tuple(seed[label] for label in returned) == seed
    assert returned == (3, 1, 2, 0, 4, 5, 6, 7, 8)
    assert colour_signs(seed, returned) == (-1, 1)

    target = idx("000111100")
    for start, length, expected in ((3, 6, (-1, 1)), (7, 7, (1, -1))):
        labels = reverse(original_labels, start, length)
        assert tuple(seed[label] for label in labels) == words[target]
        assert colour_signs(seed, labels) == expected
    assert counts[0, target] == 2 and zero[0, target] == one[0, target] == 0

    cycle = tuple(map(idx, ("000001111", "000011110", "000111100", "001111000")))
    assert [zero[i, j] for i, j in zip(cycle, cycle[1:] + cycle[:1])] == [1, 1, 1, -1]

    print("All lengths 2–7, signed vs equal-magnitude phase-free control")
    for name, matrix in (("zeros", zero), ("ones", one), ("both", both)):
        for time in (0.5, 1.0):
            print(f"{name:5s} t={time:.1f}: TV={distance(matrix, abs(matrix), time):.10f}")
    assert np.isclose(distance(zero, abs(zero), 0.5), 0.7395004030595224)

    print("Lengths 2–4, exact switching checks")
    for (name, matrix), expected in zip(
        zip(("zeros", "ones", "both"), build(words, range(2, 5))[1:]), (1, -1, -1)
    ):
        signs = switching_signs(matrix, expected)
        assert np.array_equal(matrix, expected * signs[:, None] * abs(matrix) * signs[None, :])
        print(f"{name}: overall sign {expected:+d}")


if __name__ == "__main__":
    main()
