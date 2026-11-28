"""Compare support-only matching with exact ranks in the reference chart."""
from fractions import Fraction
from itertools import product
import json

from mixed_orbits import rank
from probe import cut, cuts, words
from shuffle_sectors import inactive_columns
from support_reduction import exterior, fold


def matching(columns):
    """Maximum matching from columns to their nonzero rows."""
    owner = {}

    def augment(j, seen):
        for row in columns[j]:
            if row in seen:
                continue
            seen.add(row)
            if row not in owner or augment(owner[row], seen):
                owner[row] = j
                return True
        return False

    return sum(augment(j, set()) for j in range(len(columns)))


def joined_constraints(left, right):
    # Independent exterior equations for each branch, with one summed
    # active output. Its rank minus the exterior rank is the joined
    # active image rank, with or without orientation folding.
    output = []
    for branch, columns in enumerate((left,right)):
        for column in columns:
            outside = exterior(column)
            output.append({**{(branch+1,k):v for k,v in outside.items()},
                           **{(0,k):v for k,v in column.items() if k not in outside}})
    return output


def run(a, b, union, ranker):
    outside = [ranker(list(map(exterior, c))) for c in (a,b,union)]
    # Keep fold's exterior rows separate from active rows in joined space.
    joined = joined_constraints(a,b)
    folded_joined = []
    for column in joined:
        active = {k:v for (i,k),v in column.items() if i==0}
        folded_joined.append({**{(i,k):v for (i,k),v in column.items() if i},
                              **{(0,k):v for k,v in fold(active).items()}})
    active = [ranker(c)-e for c,e in zip((a,b,union),outside)]
    folded = [ranker(list(map(fold,c)))-e for c,e in zip((a,b,union),outside)]
    j = ranker(joined)-sum(outside[:2])
    f = ranker(folded_joined)-sum(outside[:2])
    return dict(exterior=outside, active=active, transmitted=folded,
                joined_active=j, joined_transmitted=f,
                extra_shared=folded[0]+folded[1]-f-(active[0]+active[1]-j),
                extra_union_cancel=active[2]-j-(folded[2]-f))


def main():
    sources = [cuts[8],cuts[9],cut((2,2,4),words)]
    data = {}
    for signs in product((1,-1), repeat=2):
        name = ''.join('+' if s==1 else '-' for s in signs)
        columns = [list(inactive_columns(source,signs)) for source in sources]
        def transform(convert):
            return [[{k:convert(v) for k,v in c.items()} for c in group]
                    for group in columns]

        data[name] = dict(exact=run(*columns,rank),
                          support_matching=run(*columns,matching),
                          magnitude_only=run(*transform(abs),rank),
                          sign_only=run(*transform(lambda v: Fraction(1 if v>0 else -1)),rank))
    assert [(r['exact']['extra_shared'],r['exact']['extra_union_cancel'])
            for r in data.values()] == [(0,0),(1,0),(0,0),(0,1)]
    print(json.dumps(data,indent=2))


if __name__ == '__main__':
    main()
