"""Compare the ordered representative cut with the full oriented parity fibre."""
from collections import Counter
from itertools import combinations, permutations
from fractions import Fraction
import json

from reconstruct import add_basis, axpy, can, fibre, kk, rref, ranklaw


def oriented_source(block, complement):
    for even_positions in permutations(complement):
        for odd_positions in permutations((*block, 9)):
            yield (1, *(x for pair in zip(even_positions, odd_positions) for x in pair))


def image(words, target):
    positions = {word: j for j, word in enumerate(target)}
    pivots = {}
    images = {}
    for word in words:
        column = dict(kk(word))
        residue = {positions[can(word[:-1])]: Fraction(1)} if word[-1] == 9 else {}
        while column:
            pivot = min(column)
            scale = column[pivot]
            if pivot not in pivots:
                pivots[pivot] = (
                    {j: c / scale for j, c in column.items()},
                    {j: c / scale for j, c in residue.items()},
                )
                break
            q, d = pivots[pivot]
            axpy(column, -scale, q)
            axpy(residue, -scale, d)
        if not column:
            add_basis(residue, images)
    return len(pivots), rref(images.values())


def main():
    labels = set(range(2, 9))
    records = []
    for block in combinations(sorted(labels), 3):
        complement = sorted(labels.difference(block))
        source = tuple(oriented_source(block, complement))
        cut = tuple(w for w in source if w[1] < w[-1])
        target = fibre(block, 8)
        assert len(source) == 576
        assert sum(w[-1] == 9 for w in source) == sum(w[-1] == 9 for w in cut) == 144
        cut_rank, cut_image = image(cut, target)
        full_rank, full_image = image(source, target)
        target_nullity = len(target) - len(rref(kk(w) for w in target))
        assert len(cut_image) == ranklaw(block)
        assert len(full_image) == target_nullity == 15
        assert rref(full_image + cut_image) == full_image
        for row in full_image:
            check = {}
            for j, c in row.items():
                axpy(check, c, kk(target[j]))
            assert not check
        records.append(dict(block=block, cut_words=len(cut), cut_kk_rank=cut_rank,
                            cut_residue_rank=len(cut_image), full_kk_rank=full_rank,
                            full_residue_rank=len(full_image), target_nullity=target_nullity))
    print(json.dumps(dict(fibres=records,
                          cut_rank_counts=dict(Counter(r['cut_residue_rank'] for r in records)),
                          full_rank_counts=dict(Counter(r['full_residue_rank'] for r in records))),
                     indent=2))


if __name__ == '__main__':
    main()
