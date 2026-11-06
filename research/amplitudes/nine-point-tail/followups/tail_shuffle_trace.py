"""Trace matched tail swaps to exact obstructions in shuffle coordinates."""
from collections import defaultdict
import json

from branches import kernel
from ordering_holdout import load
from probe import combine, cut, cuts, words
from reconstruct import axpy, norm, rref
from shared_residue_rule import lift_space
from shuffle_sectors import inactive_columns, orbit_columns
from support_reduction import exterior, fold
from union_cancellation_rule import quotient


def dual_trace(columns, target, kept):
    """Express a target functional using only coordinate rows on kept columns."""
    rows = defaultdict(dict)
    for j in kept:
        for key, value in columns[j].items():
            rows[key][j] = value
    basis = {}
    for key, entries in sorted(rows.items(), key=lambda item: (len(item[1]), item[0])):
        row, witness = dict(entries), {key: 1}
        while row:
            pivot = min(row)
            scale = row[pivot]
            if pivot not in basis:
                basis[pivot] = norm(row, scale), norm(witness, scale)
                break
            previous, trace = basis[pivot]
            axpy(row, -scale, previous)
            axpy(witness, -scale, trace)
    residual = {j:target[j] for j in kept if j in target}
    trace = {}
    while residual and min(residual) in basis:
        pivot = min(residual)
        scale = residual[pivot]
        row, witness = basis[pivot]
        axpy(residual, -scale, row)
        axpy(trace, scale, witness)
    if residual:
        return None
    return trace


def assess(source, signs, project, target_builder, cases, metadata):
    orbits = list(orbit_columns((w for w in source if w[-1] != 9), signs))
    columns = list(inactive_columns(source, signs))
    representatives = [min(o) for o in orbits]
    projected = list(map(project, columns))
    target = target_builder(columns, representatives)
    removed_ids, survives_ids = cases
    common = set(removed_ids) & set(survives_ids)
    pivot_id = next(iter(set(removed_ids)-common))
    replacement_id = next(iter(set(survives_ids)-common))
    j_pivot = representatives.index(tuple(metadata[pivot_id]['representative']))
    j_replacement = representatives.index(tuple(metadata[replacement_id]['representative']))
    disabled = {tuple(metadata[i]['representative']) for i in removed_ids}
    kept = [j for j,w in enumerate(representatives) if w not in disabled]
    trace = dual_trace(projected, target, kept)
    assert trace
    remainder = {j:target.get(j,0)-sum(c*projected[j].get(k,0) for k,c in trace.items())
                 for j in range(len(columns))}
    assert all(not remainder[j] for j in kept)
    assert remainder[j_pivot] and not remainder[j_replacement]
    restored = [j for j,w in enumerate(representatives)
                if w not in {tuple(metadata[i]['representative']) for i in survives_ids}]
    assert any(sum(c*target.get(restored[j],0) for j,c in dep.items())
               for dep in kernel(projected[j] for j in restored))
    return dict(removed=removed_ids, survives=survives_ids,
                restored_orbit=pivot_id, substituted_orbit=replacement_id,
                obstruction_coefficients={i:str(remainder[representatives.index(
                    tuple(metadata[i]['representative']))]) for i in removed_ids},
                trace=[(key,str(c)) for key,c in sorted(trace.items())])


def main():
    metadata = load('mixed-orbits-results.json')['orbits']
    left, right, union = map(set,(cuts[8],cuts[9],cut((2,2,4),words)))
    _, _, right_fold = lift_space(right)
    right_basis = {min(r):r for r in rref(right_fold)}

    def shared_target(columns, _):
        return shared_coordinate(columns,right_basis)

    def gluing_target(columns, representatives):
        common = list(inactive_columns(left & right,(-1,-1)))
        basis = {min(r):r for r in rref(map(exterior,common))}
        gluing = [quotient(exterior(c),basis) if w in left-right else {}
                  for w,c in zip(representatives,columns)]
        for dep in kernel(map(fold, columns)):
            if residue := combine(gluing,dep):
                key = min(residue)
                return {j:c[key] for j,c in enumerate(gluing) if key in c}
        raise AssertionError('Missing gluing class')

    def support_check(signs):
        representatives = [min(o) for o in orbit_columns(
            (w for w in left if w[-1] != 9), signs)]
        lookup = dict(zip(representatives, inactive_columns(left, signs)))
        counts = {}
        supports = []
        for i, expected in ((16, 2), (17, 1)):
            column = exterior(lookup[tuple(metadata[i]['representative'])])
            assert {sum(x in (4,5) for x in row[:row.index(2)]) for row in column} == {expected}
            counts[i] = dict(exterior_rows=len(column), swapped_A_labels_before_2=expected)
            supports.append(set(column))
        assert not supports[0] & supports[1]
        return counts

    results = {
        '+-':assess(left,(1,-1),lambda c:quotient(fold(c),right_basis),
                    shared_target,((0,2,16),(0,2,17)),metadata),
        '--':assess(union,(-1,-1),fold,gluing_target,
                    ((0,1,3,14,17),(0,1,3,14,16)),metadata),
    }
    for name, signs in (('+-',(1,-1)), ('--',(-1,-1))):
        results[name]['tail_supports'] = support_check(signs)
    print(json.dumps(results,indent=2))


def shared_coordinate(columns, basis):
    for dep in kernel(quotient(fold(c),basis) for c in columns):
        folded = combine(list(map(fold,columns)),dep)
        if folded:
            key = min(folded)
            return {j:fold(c)[key] for j,c in enumerate(columns) if key in fold(c)}
    raise AssertionError('Missing shared residue')


if __name__ == '__main__':
    main()
