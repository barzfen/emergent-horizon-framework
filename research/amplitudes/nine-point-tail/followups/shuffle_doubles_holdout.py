"""Compare the reference-fit doubling rule with exact ranks on new cuts."""
import argparse
import json
from random import Random

from ordering_holdout import load
from probe import cut, cuts, words
from shuffle_doubles import audit, columns, signature
from support_reduction import ACTIVE


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    left,right,union = map(set,(cuts[8],cuts[9],cut((2,2,4),words)))
    metadata = load('mixed-orbits-results.json')['orbits']
    selected = {tuple(k) for k in load('shuffle-doubles-results.json')['best_signature']['groups']}
    def retained(word,row):
        branch = 'common' if word in left & right else 'rank8' if word in left else 'rank9'
        return (branch,word.index(9)+1,'active' if row in ACTIVE else 'exterior') in selected

    if args.verify:
        records = load('shuffle-doubles-predictions.json')
    else:
        prior = {tuple(case['orbits']) for cases in load('ordering-predictions.json')['holdouts'].values()
                 for case in cases}
        for data in load('ordering-collision-results.json').values():
            for entry in data['2']['augmented_cuts']:
                prior.update(map(tuple,entry['cuts']))
        rng = Random(1936)
        chosen = set()
        for size in (5,6):
            sample = set()
            while len(sample)<6:
                candidate = tuple(sorted(rng.sample(range(36),size)))
                if candidate not in prior:
                    sample.add(candidate)
            chosen.update(sample)
        # Add one previously untested five-orbit extension per known obstruction.
        for core in load('union-cancellation-rule-results.json')['first_conflicts']:
            candidate = next(tuple(sorted((*core,i))) for i in range(36)
                             if i not in core and tuple(sorted((*core,i))) not in prior|chosen)
            chosen.add(candidate)
        records = [dict(deleted=ids) for ids in sorted(chosen)]
    for record in records:
        removed = {tuple(w) for i in record['deleted'] for w in metadata[i]['members']}
        groups = [columns(source-removed) for source in (left,right,union)]
        if args.verify:
            record['exact'] = signature(audit(groups,lambda w,r:True))
            record['matches'] = tuple(record['predicted']) == record['exact']
        else:
            record['predicted'] = signature(audit(groups,retained))
    print(json.dumps(records,indent=2))


if __name__ == '__main__':
    main()
