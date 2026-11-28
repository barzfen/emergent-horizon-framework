"""Find minimum orbit deletions within the three sensitive position families."""
from itertools import combinations
import json

from probe import cut, cuts, words
from reconstruct import rref
from shuffle_sectors import inactive_columns, orbit_columns
from support_reduction import active_images, fold


def signature(left, right, union):
    rank = lambda columns: len(rref(columns))
    joined = rref(left + right)
    l, r, j, u = [rank(map(fold, rows)) for rows in (left, right, joined, union)]
    return (l+r-j - (len(left)+len(right)-len(joined)),
            len(union)-len(joined) - (u-j))


def main():
    left, right, union = map(set, (cuts[8], cuts[9], cut((2, 2, 4), words)))
    cases = []
    for branch, position, signs, metric in ((8,5,(1,-1),0), (8,7,(1,-1),0),
                                             (9,3,(-1,-1),1)):
        target, other = (left, right) if branch == 8 else (right, left)
        family = (w for w in target-other if w.index(9)+1 == position)
        orbits = [set(orbit) for orbit in orbit_columns(family, (1,1))]
        assert len(orbits) == 6
        other_active = active_images(list(inactive_columns(other, signs)))
        levels = []
        for count in range(1, len(orbits)+1):
            hits = []
            for ids in combinations(range(len(orbits)), count):
                removed = set.union(*(orbits[i] for i in ids))
                altered = active_images(list(inactive_columns(target-removed, signs)))
                joined = active_images(list(inactive_columns(union-removed, signs)))
                images = (altered, other_active) if branch == 8 else (other_active, altered)
                result = signature(*images, joined)
                assert result[metric] in (0,1)
                if not result[metric]:
                    hits.append(ids)
            levels.append(dict(deletions=count, extinguishing_subsets=hits))
        cases.append(dict(branch=branch, position=position,
                          orbits=[sorted(orbit) for orbit in orbits], levels=levels))
    print(json.dumps(cases, indent=2))


if __name__ == '__main__':
    main()
