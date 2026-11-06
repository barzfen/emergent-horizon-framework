"""Exhaustively test two-orbit deletions across all branch-exclusive orbits."""
from itertools import combinations
import json

from branches import kernel
from probe import combine, cut, cuts, words
from reconstruct import add_basis, rref
from shuffle_sectors import inactive_columns, orbit_columns
from support_reduction import exterior, fold


def rank(rows):
    basis = {}
    for row in rows:
        add_basis(row, basis)
    return len(basis)


def prepare(source, signs, orbit_ids):
    orbits = list(orbit_columns((w for w in source if w[-1] != 9), signs))
    columns = list(inactive_columns(source, signs))
    assert len(orbits) == len(columns)
    lookup = {orbit_ids[min(orbit)]: i for i, orbit in enumerate(orbits)
              if min(orbit) in orbit_ids}
    lifts = list(kernel(map(exterior, columns)))
    images = [combine(columns, lift) for lift in lifts]
    return lookup, lifts, images


def restrict(prepared, deleted):
    lookup, lifts, images = prepared
    banned = [lookup[i] for i in deleted if i in lookup]
    if not banned:
        return rref(images)
    constraints = [{k: lift.get(j, 0) for k, j in enumerate(banned)
                    if j in lift} for lift in lifts]
    return rref(combine(images, c) for c in kernel(constraints))


def signature(left, right, union):
    joined = rref(left + right)
    l, r, j, u = (rank(map(fold, a)) for a in (left, right, joined, union))
    return (l+r-j - (len(left)+len(right)-len(joined)),
            len(union)-len(joined) - (u-j))


def main():
    left, right, union = map(set, (cuts[8], cuts[9], cut((2, 2, 4), words)))
    sources = (left, right, union)
    metadata = []
    for branch, source, other in ((8, left, right), (9, right, left)):
        for orbit in orbit_columns((w for w in source-other if w[-1] != 9), (1,1)):
            metadata.append(dict(branch=branch, position=min(orbit).index(9)+1,
                                 representative=min(orbit), members=sorted(orbit)))
    assert len(metadata) == 36
    orbit_ids = {m['representative']: i for i, m in enumerate(metadata)}
    report = {}
    for name, signs, metric in (('+-',(1,-1),0), ('--',(-1,-1),1)):
        prepared = [prepare(s, signs, orbit_ids) for s in sources]
        hits = []
        for deleted in combinations(range(len(metadata)), 2):
            result = signature(*(restrict(p, deleted) for p in prepared))
            assert result[metric] in (0,1)
            if not result[metric]:
                hits.append(deleted)
        # Verify both a fixed pair and every extinguishing pair using fresh
        # shuffle columns for the modified cuts.
        for deleted in [(0,35), *hits]:
            removed = {w for i in deleted for w in metadata[i]['members']}
            fresh = []
            for source in sources:
                columns = list(inactive_columns(source-removed, signs))
                fresh.append(rref(combine(columns, c) for c in kernel(map(exterior, columns))))
            assert fresh == [restrict(p, deleted) for p in prepared]
        report[name] = hits
    print(json.dumps(dict(orbits=metadata, pairs_tested=630,
                          extinguishing_pairs=report), indent=2))


if __name__ == '__main__':
    main()
