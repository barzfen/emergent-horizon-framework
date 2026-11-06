"""Freeze a local ordering predictor and test it on previously unscanned cuts."""
from collections import Counter
from itertools import combinations
import json
import random

from probe import cut, cuts, words
from support_reduction import audit


def load(path):
    with open(path) as stream:
        return json.load(stream)


def feature(orbit, radius):
    word = orbit['representative']
    j = word.index(9)
    symbols = tuple('A' if x in (4,5) else 'B' if x in (6,7) else str(x)
                    for x in word[max(0,j-radius):j+radius+1])
    return orbit['branch'], j+1, symbols


def prediction_plan(orbits, pair_hits, triple_hits, quadruple_hits):
    rng = random.Random(905)
    plan = {}
    training = {}
    for name, size, hits, excluded in (
        ('+-',2,pair_hits,[*pair_hits,*triple_hits]),
        ('--',4,quadruple_hits,quadruple_hits),
    ):
        features = [feature(o, 1) for o in orbits]
        def key(ids):
            return tuple(sorted(features[i] for i in ids))
        positive_keys = {key(ids) for ids in hits}
        positive_training = {tuple(p) for p in hits}
        false_positives = sum(ids not in positive_training and key(ids) in positive_keys
                              for ids in combinations(range(36),size))
        training[name] = dict(positive_patterns=len(positive_keys),
                              false_positives=false_positives)
        # Choose larger, mixed-position cuts. Exclude any cut containing
        # an already known conflict, so rediscovering it cannot score a hit.
        buckets = {True: [], False: []}
        for _ in range(10_000):
            if min(map(len,buckets.values())) == 12:
                break
            ids = tuple(sorted(rng.sample(range(18), 4 if size==2 else 5)))
            if len({orbits[i]['position'] for i in ids}) < 2:
                continue
            if any(set(p)<=set(ids) for p in excluded):
                continue
            predicted = any(key(p) in positive_keys for p in combinations(ids,size))
            if ids not in buckets[predicted] and len(buckets[predicted])<12:
                buckets[predicted].append(ids)
        assert all(len(group) == 12 for group in buckets.values())
        plan[name] = [dict(orbits=ids,predicted_removed=p)
                      for p,group in buckets.items() for ids in group]
    return dict(training=training, holdouts=plan)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    mixed = load('mixed-orbits-results.json')
    orbits = mixed['orbits']
    if not args.verify:
        shared = load('shared-residue-rule-results.json')
        union = load('union-cancellation-rule-results.json')
        result = prediction_plan(orbits,mixed['extinguishing_pairs']['+-'],
                                 shared['minimal_conflicting_triples'],
                                 union['first_conflicts'])
    else:
        plan = load('ordering-predictions.json')
        left, right, union = map(set, (cuts[8], cuts[9], cut((2,2,4), words)))
        for name, cases in plan['holdouts'].items():
            metric = 'extra_shared' if name=='+-' else 'extra_union_cancel'
            for case in cases:
                removed = {tuple(w) for i in case['orbits'] for w in orbits[i]['members']}
                rows = audit(dict(left=left-removed,right=right,union=union-removed),False)
                case['observed_removed'] = not rows[name][metric]
            plan.setdefault('confusion', {})[name] = dict(Counter(
                ('predicted_removed' if c['predicted_removed'] else 'predicted_survives')
                + ('_removed' if c['observed_removed'] else '_survives') for c in cases))
        result = plan
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
