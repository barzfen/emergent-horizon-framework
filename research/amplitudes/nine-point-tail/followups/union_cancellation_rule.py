"""Find deletion constraints for the original minus-minus cancellation."""
from itertools import combinations
import json
import sys

from branches import kernel
from mixed_orbits import rank
from probe import combine, cut, cuts, words
from reconstruct import axpy, rref
from shuffle_sectors import inactive_columns, orbit_columns
from support_reduction import audit, exterior, fold

SIGNS = (-1, -1)


def quotient(row, basis):
    row = dict(row)
    for pivot, vector in basis.items():
        axpy(row, -row.get(pivot, 0), vector)
    return row


def setup(left, right, union, metadata):
    orbits = list(orbit_columns((w for w in union if w[-1] != 9), SIGNS))
    columns = list(inactive_columns(union, SIGNS))
    lookup = {min(orbit): j for j, orbit in enumerate(orbits)}
    left_only = {j for j, orbit in enumerate(orbits) if min(orbit) in left-right}
    common = list(inactive_columns(left & right, SIGNS))
    basis = {min(row):row for row in rref(map(exterior, common))}
    gluing = [quotient(exterior(c), basis) if j in left_only else {}
              for j,c in enumerate(columns)]

    # The folded projection retains all exterior coordinates, so its
    # kernel consists precisely of lifts that cancel after gluing.
    cancellations = list(kernel(map(fold, columns)))
    classes = [combine(gluing, c) for c in cancellations]
    assert rank(classes) == 1
    pivot = min(next(c for c in classes if c))
    weights = {i:c[pivot] for i,c in enumerate(classes) if pivot in c}
    first = next(iter(weights))
    reference = combine(cancellations, {first:1/weights[first]})
    freedom = [combine(cancellations, v) for v in
               kernel({0: weights[i]} if i in weights else {} for i in range(len(classes)))]

    equations = []
    for orbit in metadata:
        j = lookup[tuple(orbit['representative'])]
        row = {k:c[j] for k,c in enumerate(freedom) if j in c}
        rhs = -reference.get(j, 0)
        equations.append((row, {**row, -1:rhs} if rhs else row))
    return equations


def main():
    metadata = json.load(open('mixed-orbits-results.json'))['orbits']
    left, right, union = map(set, (cuts[8], cuts[9], cut((2,2,4), words)))
    equations = setup(left, right, union, metadata)

    def conflict(ids):
        return rank(equations[i][1] for i in ids) > rank(equations[i][0] for i in ids)

    assert not any(conflict(ids) for size in (1,2) for ids in combinations(range(36), size))
    counts, hits = {}, []
    for size in range(3, int(sys.argv[1])+1):
        hits = [ids for ids in combinations(range(36),size) if conflict(ids)]
        counts[size] = len(hits)
        print(size, len(hits), file=sys.stderr, flush=True)
        if hits:
            break
    family = tuple(i for i,m in enumerate(metadata) if m['branch']==9 and m['position']==3)
    assert len(family)==6 and conflict(family)
    assert all(not conflict(ids) for ids in combinations(family,5))

    for ids in [*hits, family, family[:-1], (0,18,35)]:
        removed = {tuple(w) for i in ids for w in metadata[i]['members']}
        result = audit(dict(left=left-removed,right=right-removed,union=union-removed), False)
        assert result['--']['extra_union_cancel'] == int(not conflict(ids))
    certificates = []
    for ids in hits:
        for relation in kernel(equations[i][0] for i in ids):
            rhs = sum(c*equations[ids[j]][1].get(-1, 0) for j,c in relation.items())
            if rhs:
                certificates.append(dict(orbits=ids, weights={ids[j]:str(c) for j,c in relation.items()},
                                         nonzero_rhs=str(rhs)))
                break
        else:
            raise AssertionError('Missing inconsistency certificate')
    print(json.dumps(dict(certificates=certificates, conflicts_by_size=counts, first_conflicts=hits, position3_family=family),indent=2))


if __name__ == '__main__':
    main()
