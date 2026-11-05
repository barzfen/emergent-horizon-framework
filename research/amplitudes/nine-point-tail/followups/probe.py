import json
from branches import kernel, cut
from audit import oriented_source
from certificate import A, B
from reconstruct import axpy, add_basis, can, fibre, kk, rref

words = sorted(oriented_source(A,B))
target = fibre(A,8)
idx = {w:i for i,w in enumerate(target)}
cuts = {d:cut(c,words) for d,c in {2:(1,1,2),8:(2,2,2),9:(1,1,4)}.items()}

def combine(rows, coeffs):
    out={}
    for j,c in coeffs.items():axpy(out,c,rows[j])
    return out

def residue(lift):
    out={}
    for w,c in lift.items():
        if w[-1]==9:axpy(out,c,{idx[can(w[:-1])]:1})
    return out

def branch(d, active_only=False):
    source=cuts[d]
    piv={}
    imgs=[]; lifts=[]
    for rel in kernel(kk(w) for w in source):
        lift={source[j]:c for j,c in rel.items()}
        projected = {w:c for w,c in lift.items() if w[-1]==9} if active_only else residue(lift)
        if add_basis(projected,piv):
            imgs.append(projected); lifts.append(lift)
    return imgs,lifts

def candidates(active_only):
    x,a=branch(8,active_only);y,b=branch(9,active_only)
    common = {}
    for row in branch(2)[0]:
        add_basis(row, common)
    for joint in kernel(x+y):
        l=combine(a,{j:c for j,c in joint.items() if j<len(a)})
        r=combine(b,{j-len(a):-c for j,c in joint.items() if j>=len(a)})
        t=residue(l)
        assert t==residue(r)
        if add_basis(t,dict(common)):
            yield t,l,r

def active_part(lift):
    return {w: c for w, c in lift.items() if w[-1] == 9}


def main():
    dimensions = {}
    for name, active_only in (("before_fold", True), ("after_fold", False)):
        common, left, right = (branch(d, active_only)[0] for d in (2, 8, 9))
        union = len(rref(left + right))
        dimensions[name] = [len(common), len(left), len(right), union,
                            len(left) + len(right) - union]
    assert dimensions == {"before_fold": [2, 19, 29, 46, 2],
                          "after_fold": [2, 8, 9, 14, 3]}

    witness, lift8, lift9 = next(candidates(False))
    for d, lift in ((8, lift8), (9, lift9)):
        assert set(lift) <= set(cuts[d])
        check = {}
        for w, c in lift.items():
            axpy(check, c, kk(w))
        assert not check and residue(lift) == witness
    target_check = {}
    for j, c in witness.items():
        axpy(target_check, c, kk(target[j]))
    assert not target_check

    coordinate = idx[(1, 2, 4, 6, 8, 7, 5, 3)]
    assert witness[coordinate] == 2
    assert all(not row.get(coordinate) for row in branch(2)[0])

    difference = active_part(lift8)
    axpy(difference, -1, active_part(lift9))
    assert difference and not residue(difference)
    paired = {}
    for w, c in difference.items():
        paired.setdefault(idx[can(w[:-1])], []).append(c)
    assert len(paired) == 24 and all(sorted(v) == [-1, 1] for v in paired.values())

    print(json.dumps({
        "dimension_columns": ["common_cut", "branch8", "branch9", "branch_sum", "branch_intersection"],
        "dimensions": dimensions,
        "common_cut_obstruction_word": target[coordinate],
        "common_cut_obstruction_witness_value": str(witness[coordinate]),
        "target_witness": [[target[j], str(c)] for j, c in sorted(witness.items())],
        "side_by_side_lifts": [[w, str(lift8.get(w, 0)), str(lift9.get(w, 0))]
                               for w in sorted(set(lift8) | set(lift9))],
    }, indent=2))


if __name__ == "__main__":
    main()
