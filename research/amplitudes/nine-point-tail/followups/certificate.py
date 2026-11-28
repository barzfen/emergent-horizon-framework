"""Exact rank-14 obstruction, verified with standard-library Python."""
import json

from itertools import product

from audit import image, oriented_source
from reconstruct import add_basis, axpy, can, fibre, kk, norm, rref

A = (4, 5, 8)
B = (2, 3, 6, 7)
TARGET_WORDS = ((1, 6, 5, 2, 8, 3, 4, 7), (1, 6, 5, 3, 8, 2, 4, 7))
DUAL = {
    (7, 4, 8, 2, 3, 5, 6): -1,
    (7, 4, 2, 8, 3, 5, 6): 1,
    (7, 4, 3, 8, 2, 5, 6): 1,
    (6, 5, 8, 2, 3, 4, 7): -1,
    (6, 5, 2, 8, 3, 4, 7): 1,
    (6, 5, 3, 8, 2, 4, 7): 1,
}
PAIR = ((1, 6, 4, 7, 9, 2, 8, 3, 5), (1, 6, 5, 7, 9, 2, 8, 3, 4))


def dual(word):
    return sum(c * kk(word).get(row, 0) for row, c in DUAL.items())


def inverse_shuffle():
    """Recover source coefficients from the six rows without forward KK."""
    out = {}
    for row, weight in DUAL.items():
        for mask in product((False, True), repeat=7):
            left = tuple(x for x, take in zip(row, mask) if take)
            right = tuple(x for x, take in zip(row, mask) if not take)[::-1]
            word = (1, *left, 9, *right)
            if set(word[1::2]) == set(B):
                axpy(out, weight * (-1) ** len(right), {word: 1})
    return out


def transported(block, word):
    complement = sorted(set(range(2, 9)).difference(block))
    mapping = {1: 1, 9: 9, **dict(zip(block, A)), **dict(zip(complement, B))}
    return tuple(mapping[x] for x in word)


def evaluate(row, positions):
    return sum(row.get(p, 0) for p in positions)


def main():
    target = fibre(A, 8)
    target_idx = {w: j for j, w in enumerate(target)}
    positions = [target_idx[w] for w in TARGET_WORDS]
    source = fibre(A, 9)
    full = tuple(oriented_source(A, B))
    assert len(source) == 432
    inverse = inverse_shuffle()
    assert len(inverse) == 16
    assert inverse == {w: dual(w) for w in full if dual(w)}
    assert all(dual(w) == int(w[-1] == 9 and can(w[:-1]) in TARGET_WORDS)
               for w in source)
    excluded = [w for w in full if w[1] > w[-1]]
    visible = {w: int(dual(w)) for w in excluded if dual(w)}
    assert len(visible) == 12 and set(visible.values()) == {1}

    # A forbidden word with dual value zero cannot remove this obstruction.
    # For the other forbidden words, rule out a single addition by showing its
    # KK column is outside the span of the cut KK columns.
    pivots = {}
    for w in source:
        add_basis(kk(w), pivots)
    quotients = []
    for w in [*visible, PAIR[1]]:
        residual = dict(kk(w))
        for pivot in sorted(pivots):
            if pivot in residual:
                axpy(residual, -residual[pivot], pivots[pivot])
        assert residual
        quotients.append(residual)
    assert PAIR[0] in visible and PAIR[1] in excluded and not dual(PAIR[1])
    assert quotients[list(visible).index(PAIR[0])] == quotients[-1]

    # Recover an explicit lift for the restoring pair by carrying coefficient
    # vectors through KK elimination, stopping at the last column.
    basis = {}
    augmented = source + list(PAIR)
    for j, w in enumerate(augmented):
        col, lift = dict(kk(w)), {j: 1}
        while col:
            p = min(col)
            scale = col[p]
            if p not in basis:
                basis[p] = norm(col, scale), norm(lift, scale)
                break
            q, c = basis[p]
            axpy(col, -scale, q)
            axpy(lift, -scale, c)
    assert not col and lift[len(source)] == -1 and lift[len(source) + 1] == 1
    target_row, source_check, target_check = {}, {}, {}
    for j, coeff in lift.items():
        w = augmented[j]
        axpy(source_check, coeff, kk(w))
        if w[-1] == 9:
            axpy(target_row, coeff, {target_idx[can(w[:-1])]: 1})
    for j, coeff in target_row.items():
        axpy(target_check, coeff, kk(target[j]))
    assert not source_check and not target_check
    assert evaluate(target_row, positions) == 1

    _, full_image = image(full, target)
    assert len(full_image) == len(target) - len(rref(kk(w) for w in target)) == 15
    symmetry = []
    for a, b in ((4, 5), (2, 3), (6, 7)):
        swapped = [target_idx[can(tuple(b if x == a else a if x == b else x for x in w))]
                   for w in TARGET_WORDS]
        signs = [s for s in (-1, 1)
                 if all(evaluate(r, swapped) == s * evaluate(r, positions) for r in full_image)]
        assert len(signs) == 1
        symmetry.extend(signs)
    assert symmetry == [-1, 1, -1]

    cases = []
    for a in (2, 3, 4):
        for c in (7, 8):
            block = (a, 5, c)
            words = fibre(block, 9)
            for w in words:
                tw = transported(block, w)
                assert tw[1] < tw[-1]  # Contained in the maximal cut.
                expected = int(tw[-1] == 9 and can(tw[:-1]) in TARGET_WORDS)
                assert dual(tw) == expected
            local_target = fibre(block, 8)
            _, local_image = image(words, local_target)
            assert len(local_image) == 14
            moved = [{target_idx[can(transported(block, local_target[j]))]: v
                      for j, v in r.items()} for r in local_image]
            assert all(not evaluate(row, positions) for row in moved)
            cases.append({"block": block, "rank": len(local_image), "source_words": len(words)})

    def encode(words, coeffs):
        return [[words[j], str(c)] for j, c in sorted(coeffs.items())]

    print(json.dumps({"rank_14_fibres": cases, "target_character": symmetry,
                      "nonzero_excluded_words": list(visible), "minimum_added_words": 2,
                      "restoring_pair": PAIR, "source_lift": encode(augmented, lift),
                      "target_witness": encode(target, target_row),
                      "witness_functional_value": str(evaluate(target_row, positions))}, indent=2))


if __name__ == "__main__":
    main()
