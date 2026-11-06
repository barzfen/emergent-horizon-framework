"""Separate old exterior classes from cancellations that become exceptional."""
import json

from branches import kernel
from mixed_orbits import rank
from probe import combine, cut, cuts, words
from reconstruct import add_basis, rref
from shuffle_doubles import columns
from support_reduction import exterior, fold


def lift_images(source, constraint):
    block = columns(source)
    reps = list(block)
    matrix = list(block.values())
    coeffs = list(kernel(map(constraint, matrix)))
    return ([combine(matrix,c) for c in coeffs],
            [{reps[j]:v for j,v in c.items()} for c in coeffs])


def intersection(a,b):
    return rref(combine(a,{j:v for j,v in c.items() if j<len(a)})
                for c in kernel(a+b))


def witnesses(images, lifts, target):
    index = len(images)
    coeff = next(c for c in kernel(images+[target]) if index in c)
    fit = {j:-v/coeff[index] for j,v in coeff.items() if j!=index}
    assert combine(images,fit)==target
    return combine(lifts,fit)


def encoded(row):
    return [[k,str(v)] for k,v in sorted(row.items())]


def main():
    left,right,union = map(set,(cuts[8],cuts[9],cut((2,2,4),words)))
    common = left & right
    old_left,left_lifts = lift_images(left,exterior)
    old_right,right_lifts = lift_images(right,exterior)
    old_joined = rref(old_left+old_right)
    results = {}
    for position in (3,5,7):
        removed = {w for w in common if w[-1]!=9 and w.index(9)+1==position}
        assert len(removed)==48
        a,b = [rref(lift_images(s-removed,exterior)[0]) for s in (left,right)]
        joined = rref(a+b)
        union_cancel, union_lifts = lift_images(union-removed,fold)
        cancel = rref(union_cancel)
        separate_cancel = rref(combine(joined,c) for c in kernel(map(fold,joined)))
        old_split = intersection(cancel,old_joined)
        assert len(rref(separate_cancel+old_split))==len(old_split)
        assert len(rref(old_split+cancel))==len(cancel)
        basis = {}
        for row in separate_cancel:
            add_basis(row,basis)
        additional = [row for row in old_split if add_basis(row,basis)]
        inherited = [row for row in cancel if add_basis(row,basis)]
        assert len(basis)==len(cancel)
        assert len(inherited)<=1
        records = []
        for row in additional:
            split = witnesses(old_left+old_right,
                              [{(0,w):c for w,c in v.items()} for v in left_lifts]
                              + [{(1,w):c for w,c in v.items()} for v in right_lifts],row)
            assert not fold(row)
            assert rank(joined+[row])>len(joined)
            records.append(dict(vector=encoded(row),original_branch_split=encoded(split),
                                modified_union_lift=encoded(witnesses(union_cancel,union_lifts,row))))
        results[position] = dict(modified_union_cancel_rank=len(cancel),
                                 modified_joined_cancel_rank=len(separate_cancel),
                                 old_split_cancel_rank=len(old_split),
                                 additional=len(additional),inherited=len(inherited),
                                 new_vectors=records,
                                 inherited_vectors=[encoded(row) for row in inherited])
    assert [(r['inherited'],r['additional']) for r in results.values()]==[(1,2),(1,0),(0,1)]
    print(json.dumps(results,indent=2))


if __name__ == '__main__':
    main()
