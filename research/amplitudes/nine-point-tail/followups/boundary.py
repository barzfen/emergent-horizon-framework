"""Resolve the two orientation-cancellation quotients by exact symmetry."""
import json

from branches import kernel
from probe import active_part, branch, candidates, combine, cut, cuts, residue, words
from reconstruct import axpy, rref

SWAPS = ((4, 5), (6, 7))


def relabel(word, pair):
    a, b = pair
    return tuple(b if x == a else a if x == b else x for x in word)


def act(row, pair):
    return {relabel(w, pair): c for w, c in row.items()}


def null_fold(rows):
    return [combine(rows, coeffs) for coeffs in kernel(residue(r) for r in rows)]


def rank(rows):
    return len(rref(rows))


def project(row, signs):
    row = dict(row)
    for pair, sign in zip(SWAPS, signs):
        axpy(row, sign, act(row, pair))
    return row


def main():
    cuts[14] = cut((2, 2, 4), words)
    for source in cuts.values():
        for pair in SWAPS:
            assert {relabel(w, pair) for w in source} == set(source)

    left, right, union = (branch(d, True)[0] for d in (8, 9, 14))
    joined = rref(left + right)
    assert rank(joined + union) == rank(union) == 47
    local = rref(null_fold(left) + null_fold(right))
    middle = null_fold(joined)
    top = null_fold(union)
    assert [rank(rows) for rows in (local, middle, top)] == [31, 32, 33]

    _, lift8, lift9 = next(candidates(False))
    shared = active_part(lift8)
    axpy(shared, -1, active_part(lift9))
    assert not residue(shared) and rank(local + [shared]) == 32
    shared = project(shared, (1, -1))
    assert rank(local + [shared]) == 32
    assert rank(middle + [shared]) == 32

    mixed = next(row for row in top if rank(middle + [row]) == 33)
    mixed = project(mixed, (-1, -1))
    assert rank(top + [mixed]) == 33
    assert rank(local + [shared, mixed]) == 33

    def certify(row, signs):
        assert not residue(row)
        for pair, sign in zip(SWAPS, signs):
            assert act(row, pair) == {w: sign * c for w, c in row.items()}
        return [[w, str(c)] for w, c in sorted(row.items())]

    print(json.dumps({
        "active_image_ranks": [rank(left), rank(right), rank(joined), rank(union)],
        "cancellation_ranks": [rank(local), rank(middle), rank(top)],
        "character_generators": {
            "+-": certify(shared, (1, -1)),
            "--": certify(mixed, (-1, -1)),
        },
    }, indent=2))


if __name__ == "__main__":
    main()
