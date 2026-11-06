"""Trace the replacement cancellation through the original branch spaces."""
from itertools import combinations
import json

from branches import kernel
from mixed_orbits import rank
from probe import combine, cut, cuts, words
from reconstruct import rref
from shuffle_doubles import SIGNS, columns
from shuffle_sectors import orbit_columns
from support_reduction import active_images, exterior, fold
from union_cancellation_rule import setup


def main():
    left,right,union = map(set,(cuts[8],cuts[9],cut((2,2,4),words)))
    common = left & right
    orbits = [set(o) for o in orbit_columns((w for w in common if w[-1]!=9),SIGNS)
              if min(o).index(9)==6]
    assert len(orbits)==12
    removed = set.union(*orbits)
    original = [list(columns(source).values()) for source in (left,right,union)]
    altered = [list(columns(source-removed).values()) for source in (left,right,union)]
    old_a,old_b,_ = map(active_images,original)
    new_a,new_b,new_u = map(active_images,altered)
    old_joined = rref(old_a+old_b)
    new_joined = rref(new_a+new_b)
    cancellations = rref(combine(new_u,c) for c in kernel(map(fold,new_u)))
    replacement = next(v for v in cancellations if rank(new_joined+[v])>len(new_joined))
    assert rank(old_joined+[replacement])==len(old_joined)
    assert rank(old_a+[replacement])>len(old_a)
    assert rank(old_b+[replacement])>len(old_b)

    # Fit the fixed vector with two separately active lifts, allowing
    # arbitrary decomposition and arbitrary null lifts in both branches.
    left_columns,right_columns = [columns(s) for s in (left,right)]
    blocks = [left_columns,right_columns]
    lifts, images = [], []
    for branch, block in enumerate(blocks):
        representatives = list(block)
        seq = list(block.values())
        for coeff in kernel(map(exterior,seq)):
            lifts.append({(branch,representatives[i]):c for i,c in coeff.items()})
            images.append(combine(seq,coeff))
    solutions = list(kernel(images+[replacement]))
    j = len(images)
    relation = next(c for c in solutions if j in c)
    reference = combine(lifts,{i:-v/relation[j] for i,v in relation.items() if i!=j})
    freedom = [combine(lifts,c) for c in kernel(images)]

    constraints = []
    for orbit in orbits:
        equations = []
        for branch in range(2):
            key = (branch,min(orbit))
            row = {i:v[key] for i,v in enumerate(freedom) if key in v}
            rhs = -reference.get(key,0)
            equations.append((row,{**row,-1:rhs} if rhs else row))
        constraints.append(equations)

    def predicts_split(restored):
        rows = [eq for i,group in enumerate(constraints) if i not in restored for eq in group]
        return rank(a for a,b in rows)==rank(b for a,b in rows)

    predictions = []
    for size in range(len(orbits)+1):
        good = [ids for ids in combinations(range(len(orbits)),size) if predicts_split(ids)]
        predictions.append(dict(size=size,successes=good))
        if good:
            break
    assert predictions[-1]['successes']

    original_class = setup(left,right,union,[{"representative":min(o)} for o in orbits])
    checks = []
    for ids in [(),*((i,) for i in range(len(orbits))),*predictions[-1]['successes']]:
        banned = set.union(*(o for i,o in enumerate(orbits) if i not in ids))
        a,b,u = [active_images(list(columns(s-banned).values())) for s in (left,right,union)]
        joined = rref(a+b)
        observed = rank(joined+[replacement])==len(joined)
        assert observed == predicts_split(ids)
        dimension = len(u)-len(joined)-(rank(map(fold,u))-rank(map(fold,joined)))
        omitted = [original_class[i] for i in range(len(orbits)) if i not in ids]
        original_survives = rank(a for a,b in omitted)==rank(b for a,b in omitted)
        checks.append(dict(restored=ids,fixed_vector_splits=observed,
                           original_class_survives=original_survives,extra_cancellations=dimension))
    print(json.dumps(dict(orbit_representatives=[min(o) for o in orbits],
                          replacement=[[k,str(c)] for k,c in sorted(replacement.items())],
                          original_split_lift=[[b,w,str(c)] for (b,w),c in sorted(reference.items())],
                          predictions=predictions,checks=checks),indent=2))


if __name__ == '__main__':
    main()
