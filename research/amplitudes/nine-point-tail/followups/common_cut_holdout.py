"""Test the frozen doubling rule after changing the common ordering cut."""
import argparse
from collections import defaultdict
from itertools import combinations
import json
from random import Random

from ordering_holdout import load
from probe import cut, cuts, words
from shuffle_doubles import SIGNS, audit, columns, signature
from shuffle_sectors import orbit_columns


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    left,right,union = map(set,(cuts[8],cuts[9],cut((2,2,4),words)))
    common = left & right
    orbits = list(orbit_columns((w for w in common if w[-1]!=9),SIGNS))
    assert len(orbits)==36
    chosen = {tuple(k) for k in load('shuffle-doubles-results.json')['best_signature']['groups']}
    assert chosen == {('common',5,'active'),('common',5,'exterior')}

    def retained(word, row):
        return word in common and word.index(9)==4

    if args.verify:
        plan = load('common-cut-predictions.json')
        assert plan['orbit_representatives'] == [list(min(o)) for o in orbits]
    else:
        groups = defaultdict(list)
        for i,o in enumerate(orbits):
            groups[min(o).index(9)+1].append(i)
        cases = [dict(kind='single',removed=[i]) for i in range(len(orbits))]
        cases.extend(dict(kind='position_family',position=p,removed=ids)
                     for p,ids in sorted(groups.items()))
        rng = Random(1937)
        pairs = list(combinations(groups[5],2))
        cases.extend(dict(kind='position5_pair',removed=ids)
                     for ids in sorted(rng.sample(pairs,12)))
        cases.extend(dict(kind='mixed_triple',removed=sorted(
            rng.choice(groups[p]) for p in sorted(groups))) for _ in range(12))
        assert len({tuple(c['removed']) for c in cases})==len(cases)
        plan = dict(orbit_representatives=[min(o) for o in orbits], cases=cases)

    for case in plan['cases']:
        removed = {w for i in case['removed'] for w in orbits[i]}
        matrices = [columns(s-removed) for s in (left,right,union)]
        if args.verify:
            result = audit(matrices,lambda w,r:True)
            case['exact'] = signature(result)
            case['matches'] = tuple(case['predicted']) == case['exact']
            case['exact_ranks'] = result
        else:
            case['predicted'] = signature(audit(matrices,retained))
    print(json.dumps(plan,indent=2))


if __name__ == '__main__':
    main()
