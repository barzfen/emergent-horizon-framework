"""Check LR3 recombination squares and a supplied coherent interference control."""

from collections import Counter
from itertools import combinations, product

from cross41_growth_and_return import LR3, read, rewrite, split_edge
from cross46_local_clock import INITIAL
from cross47_reversal_bell import preparations


def successors(signs):
    for start in range(len(signs)):
        window = read(signs, start, 4)
        if window in LR3:
            yield start, rewrite(signs, start, LR3[window])


def support(start, size):
    return {(start + offset) % size for offset in range(4)}


def check_squares():
    counts = Counter()
    for signs in preparations(24):
        size = len(signs)
        for (first, left), (second, right) in combinations(successors(signs), 2):
            left_exits = tuple(successors(left))
            right_exits = tuple(successors(right))
            for (after_left, left_target), (after_right, right_target) in product(
                left_exits, right_exits
            ):
                if left_target != right_target or left_target == signs:
                    continue
                assert (after_left, after_right) == (second, first)
                assert support(first, size).isdisjoint(support(second, size))
                counts[size] += 1
    assert counts == {21: 24, 22: 1215, 23: 7608, 24: 29776}
    print("Two-step route pairs at sizes 21–24:", dict(sorted(counts.items())))


def swapped_positions(start, size):
    return (start + 1) % size, (start + 3) % size


def labelled_path(size, starts):
    labels = list(range(size))
    for start in starts:
        a, b = swapped_positions(start, size)
        labels[a], labels[b] = labels[b], labels[a]
    return labels


def clifford_product(left, right):
    result = Counter()
    for a, b in product(left, right):
        swaps = sum(1 for i in a for j in b if i > j)
        result[tuple(sorted(set(a) ^ set(b)))] += left[a] * right[b] * (-1) ** swaps
    return {blade: coefficient for blade, coefficient in result.items() if coefficient}


def check_witness(signs, first, second):
    left, right = dict(successors(signs))[first], dict(successors(signs))[second]
    end = dict(successors(left))[second]
    assert end == dict(successors(right))[first]
    assert len({signs, left, right, end}) == 4
    assert labelled_path(len(signs), (first, second)) == labelled_path(len(signs), (second, first))

    a, b = swapped_positions(first, len(signs))
    c, d = swapped_positions(second, len(signs))
    p, q = {(a,): 1, (b,): -1}, {(c,): 1, (d,): -1}
    pq, qp = clifford_product(p, q), clifford_product(q, p)
    assert pq and pq == {blade: -coefficient for blade, coefficient in qp.items()}
    assert clifford_product(qp, qp) == {(): -4}


def pulse(vector):
    # Numerator of the supplied normalized pulse (P+Q)/sqrt(2).
    result = [0] * 4
    for basis, amplitude in enumerate(vector):
        result[basis ^ 2] += amplitude
        result[basis ^ 1] += (-1 if basis & 2 else 1) * amplitude
    return tuple(result)


def check_readouts():
    basis = [tuple(int(i == j) for i in range(4)) for j in range(4)]
    for left, right in product(range(4), repeat=2):
        assert sum(a * b for a, b in zip(pulse(basis[left]), pulse(basis[right]))) == 2 * (left == right)
    arms = pulse(basis[0])
    assert arms == (0, 1, 1, 0)
    assert pulse(arms) == (2, 0, 0, 0)
    assert pulse((0, 1, -1, 0)) == (0, 0, 0, 2)
    # Each orthogonal route tag retains one arm. Add probabilities, with no cross term.
    assert pulse(basis[1])[3] ** 2 + pulse(basis[2])[3] ** 2 == 2
    # In the classical square, two of four equally likely two-move sequences arrive.
    assert sum((first ^ second) == 3 for first, second in product((1, 2), repeat=2)) == 2


if __name__ == "__main__":
    check_squares()
    check_witness(INITIAL, 2, 17)
    for slot in range(6, 17):
        check_witness(split_edge(INITIAL, slot), 2, 18)
    check_readouts()
    print("Labelled square, Clifford sign and all 11 between-window insertions verified.")
    print("Arrival probability: classical 1/2, coherent 0, phase flipped 1, tagged 1/2.")
