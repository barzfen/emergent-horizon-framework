"""Predict deletions from the affine lift space of the shared residue."""
from itertools import combinations
import json

from branches import kernel
from mixed_orbits import rank
from probe import combine, cuts
from reconstruct import rref
from shuffle_sectors import inactive_columns, orbit_columns
from support_reduction import exterior, fold


def lift_space(source):
    signs = (1, -1)
    orbits = list(orbit_columns((w for w in source if w[-1] != 9), signs))
    columns = list(inactive_columns(source, signs))
    lifts = list(kernel(map(exterior, columns)))
    return orbits, lifts, [fold(combine(columns, lift)) for lift in lifts]


def main():
    data = json.load(open('mixed-orbits-results.json'))
    ids = {tuple(row['representative']): i for i, row in enumerate(data['orbits'])}
    left, right = (lift_space(cuts[branch]) for branch in (8, 9))
    split = len(left[1])
    assert rank(left[2]) + rank(right[2]) - rank(left[2]+right[2]) == 1
    for relation in kernel(left[2]+right[2]):
        coeff = {i: c for i, c in relation.items() if i < split}
        if combine(left[2], coeff):
            targets = (coeff, {i-split: -c for i,c in relation.items() if i >= split})
            break
    else:
        raise AssertionError('Missing shared residue')

    equations = {}
    for branch, (orbits, lifts, folded), target in zip((8,9), (left,right), targets):
        base = combine(lifts, target)
        freedom = [combine(lifts, c) for c in kernel(folded)]
        for j, orbit in enumerate(orbits):
            if min(orbit) in ids:
                orbit_id = ids[min(orbit)]
                equations[orbit_id] = (branch, {k:v[j] for k,v in enumerate(freedom) if j in v},
                                       -base.get(j,0))

    def conflicts(deleted):
        rows, augmented = [], []
        for i in deleted:
            branch, coeff, rhs = equations[i]
            row = {(branch, k): v for k,v in coeff.items()}
            rows.append(row)
            augmented.append({**row, (0,0):rhs} if rhs else row)
        return rank(augmented) > rank(rows)

    assert not any(conflicts((i,)) for i in ids.values())
    pairs = {p for p in combinations(range(len(ids)),2) if conflicts(p)}
    assert pairs == {tuple(p) for p in data['extinguishing_pairs']['+-']}
    triples = [t for t in combinations(range(18),3)
               if not any(p in pairs for p in combinations(t,2)) and conflicts(t)]
    controls = [t for t in combinations(range(18),3) if not conflicts(t)][:6]
    for t in triples + controls:
        removed = {tuple(w) for i in t for w in data['orbits'][i]['members']}
        modified = lift_space(set(cuts[8])-removed)[2]
        assert rank(modified) + rank(right[2]) - rank(modified+right[2]) == int(t in controls)
    print(json.dumps(dict(conflicting_pairs=sorted(pairs), minimal_conflicting_triples=triples,
                          surviving_controls=controls), indent=2))


if __name__ == '__main__':
    main()
