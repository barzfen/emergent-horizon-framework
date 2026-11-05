"""Exact certificates for the two branches of the nine-point tail lattice."""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
import json

from audit import image, oriented_source
from certificate import A, B, DUAL, TARGET_WORDS, transported
from reconstruct import add_basis, axpy, can, fibre, kk, norm, rref


def kernel(columns):
    pivots = {}
    for j, column in enumerate(columns):
        col = dict(column)
        lift = {j: Fraction(1)}
        while col:
            p = min(col)
            scale = col[p]
            if p not in pivots:
                pivots[p] = norm(col, scale), norm(lift, scale)
                break
            q, c = pivots[p]
            axpy(col, -scale, q)
            axpy(lift, -scale, c)
        if not col:
            yield lift


def evaluate(row, vector):
    return sum(c * vector.get(j, 0) for j, c in row.items())


def cut(counts, words):
    return [w for w in words if w[-1] == 9 or B.index(w[1]) < counts[A.index(w[-1])]]


def select_certificates(source, target, relations, shared, count):
    target_idx = {w: j for j, w in enumerate(target)}
    active = defaultdict(list)
    constraints = defaultdict(list)
    next_constraint = 0
    for j, w in enumerate(source):
        if w[-1] == 9:
            active[target_idx[can(w[:-1])]].append(j)
        else:
            constraints[j].append((next_constraint, 1))
            next_constraint += 1
    for pair in active.values():
        a, b = pair
        constraints[a].append((next_constraint, 1))
        constraints[b].append((next_constraint, -1))
        next_constraint += 1

    rows = defaultdict(dict)
    for j, w in enumerate(source):
        for key, coefficient in kk(w).items():
            rows[key][j] = coefficient

    def constrained_column(row):
        out = {}
        for j, c in row.items():
            for i, sign in constraints[j]:
                axpy(out, sign * c, {i: 1})
        return out

    keys = sorted(rows)
    columns = [constrained_column(rows[key]) for key in keys]
    candidates = []
    for weights in kernel(columns):
        values = {}
        for k, c in weights.items():
            axpy(values, c, rows[keys[k]])
        functional = {j: values[pair[0]] for j, pair in active.items() if pair[0] in values}
        restriction = {j: v for j, r in enumerate(relations) if (v := evaluate(functional, r))}
        if restriction:
            dual = {keys[k]: c for k, c in weights.items()}
            candidates.append((functional, dual, restriction))

    pivots = {}
    assert add_basis({j: evaluate(shared, r) for j, r in enumerate(relations)
                      if evaluate(shared, r)}, pivots)
    selected = []
    for functional, dual, restriction in sorted(candidates, key=lambda c: (len(c[1]), len(c[0]))):
        if add_basis(restriction, pivots):
            selected.append((functional, dual))
    assert len(selected) == count
    return selected


def main():
    words = sorted(oriented_source(A, B))
    target = fibre(A, 8)
    target_idx = {w: j for j, w in enumerate(target)}
    relations = list(kernel(kk(w) for w in target))
    assert len(relations) == 15
    shared = {target_idx[w]: 1 for w in TARGET_WORDS}
    counts = {2: (1, 1, 2), 8: (2, 2, 2), 9: (1, 1, 4), 14: (2, 2, 4)}
    cuts = {d: cut(c, words) for d, c in counts.items()}
    assert set(cuts[8]) | set(cuts[9]) == set(cuts[14])
    assert set(cuts[8]) & set(cuts[9]) == set(cuts[2])
    results = {d: image(source, target) for d, source in cuts.items()}
    images = {d: result[1] for d, result in results.items()}
    assert all(len(rows) == d for d, rows in images.items())
    assert rref(images[8] + images[9]) == images[14]
    source_ranks = {d: result[0] for d, result in results.items()}
    mixed_source_dimension = source_ranks[8] + source_ranks[9] - source_ranks[14] - source_ranks[2]
    extra_common_residue_dimension = 8 + 9 - 14 - 2
    assert mixed_source_dimension == extra_common_residue_dimension == 1

    def verify(source, functional, dual):
        for w in source:
            value = evaluate(dual, kk(w))
            expected = functional.get(target_idx[can(w[:-1])], 0) if w[-1] == 9 else 0
            assert value == expected

    records = {}
    for d, extra in ((8, 6), (9, 5)):
        selected = [(shared, DUAL)] + select_certificates(cuts[d], target, relations, shared, extra)
        records[d] = []
        other = 9 if d == 8 else 8
        for i, (functional, dual) in enumerate(selected):
            verify(cuts[d], functional, dual)
            assert all(not evaluate(functional, r) for r in images[d])
            assert bool(i) == any(evaluate(functional, r) for r in images[other])
            excluded = [(w, evaluate(dual, kk(w))) for w in words if w not in set(cuts[d])]
            assert all(w[-1] != 9 for w, c in excluded if c)
            records[d].append({
                "shared": i == 0,
                "target_functional": [[target[j], str(c)] for j, c in sorted(functional.items())],
                "kk_dual": [[w, str(c)] for w, c in sorted(dual.items())],
                "nonzero_excluded_words": [[w, str(c)] for w, c in excluded if c],
                "nonzero_words_in_other_cut": [w for w, c in excluded if c and w in set(cuts[other])],
            })
        obstruction_rows = [{j: v for j, r in enumerate(relations) if (v := evaluate(f, r))}
                            for f, _ in selected]
        assert len(rref(obstruction_rows)) == 15 - d

    verified = Counter()
    for block in combinations(range(2, 9), 3):
        local_source = fibre(block, 9)
        local_target = fibre(block, 8)
        _, rows = image(local_source, local_target)
        d = len(rows)
        if d not in cuts:
            continue
        assert set(transported(block, w) for w in local_source) <= set(cuts[d])
        moved = [{target_idx[can(transported(block, local_target[j]))]: c
                  for j, c in row.items()} for row in rows]
        assert rref(moved) == images[d]
        verified[d] += 1
    assert verified == {2: 3, 8: 3, 9: 6, 14: 6}
    print(json.dumps({
        "cut_counts": counts,
        "source_sizes": {d: len(source) for d, source in cuts.items()},
        "source_kk_ranks": source_ranks,
        "mixed_source_quotient_dimension": mixed_source_dimension,
        "extra_common_residue_dimension": extra_common_residue_dimension,
        "verified_fibres": verified,
        "certificates": records,
    }, indent=2))


if __name__ == "__main__":
    main()
