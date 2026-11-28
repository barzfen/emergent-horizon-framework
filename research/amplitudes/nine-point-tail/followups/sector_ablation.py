"""Test which symmetry exceptions survive removal of whole ordering families."""
import json
from collections import defaultdict
from itertools import product

from boundary import SWAPS, relabel
from probe import cut, cuts, words
from reconstruct import rref
from shuffle_sectors import inactive_columns
from support_reduction import audit, exterior


def overlap_audit(left, right):
    output = {}
    for signs in product((1, -1), repeat=2):
        a, b, common = (list(inactive_columns(source, signs))
                        for source in (left, right, left & right))
        rank = lambda columns: len(rref(columns))
        assert rank(a) + rank(b) - rank(a+b) == rank(common)
        pa, pb, pc = ([exterior(column) for column in rows] for rows in (a, b, common))
        name = ''.join('+' if x == 1 else '-' for x in signs)
        output[name] = dict(projected_overlap=rank(pa)+rank(pb)-rank(pa+pb),
                            projected_common=rank(pc))
    return output


def main():
    left, right, union = map(set, (cuts[8], cuts[9], cut((2, 2, 4), words)))
    base = dict(left=left, right=right, union=union)
    partitions = defaultdict(set)
    for name, branch, other in (('left', left, right), ('right', right, left)):
        for word in branch-other:
            assert word[-1] != 9
            for feature, key in (('position9', word.index(9)+1),
                                 ('terminal', min(word[-1], 4) if word[-1] in (4,5) else word[-1]),
                                 ('first_after_anchor', 6 if word[1] in (6,7) else word[1])):
                partitions[name,feature,key].add(word)

    records = []
    for (name, feature, key), removed in sorted(partitions.items()):
        assert all({relabel(w, pair) for w in removed} == removed for pair in SWAPS)
        modified = {**base, name: base[name]-removed, 'union': union-removed}
        reduced = audit(modified, True)
        full = audit(modified, False)
        for sector in reduced:
            for metric in ('extra_shared', 'extra_union_cancel'):
                assert reduced[sector][metric] == full[sector][metric]
            for branch, row in reduced[sector]['cuts'].items():
                for metric in ('active', 'transmitted'):
                    assert row[metric] == full[sector]['cuts'][branch][metric]
        records.append(dict(branch=name, feature=feature, value=key,
                            removed=sorted(removed), sectors=reduced))
    print(json.dumps(dict(exterior_overlap=overlap_audit(left, right),
                          baseline=audit(base, False), ablations=records), indent=2))


if __name__ == '__main__':
    main()
