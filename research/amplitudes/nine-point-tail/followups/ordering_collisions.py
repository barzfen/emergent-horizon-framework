"""Test whether extending the local window removes the feature collisions."""
from itertools import combinations
import json

from ordering_holdout import feature, load
from probe import cut, cuts, words
from support_reduction import audit


def main():
    mixed = load('mixed-orbits-results.json')
    orbits = mixed['orbits']
    union_hits = load('union-cancellation-rule-results.json')['first_conflicts']
    sources = dict(left=set(cuts[8]), right=set(cuts[9]), union=set(cut((2,2,4),words)))
    result = {}
    for name, hits in (('+-',mixed['extinguishing_pairs']['+-']), ('--',union_hits)):
        metric = 'extra_shared' if name=='+-' else 'extra_union_cancel'
        positive = {tuple(p) for p in hits}
        sizes = len(hits[0])
        profiles = {}
        for radius in (1,2):
            def key(ids):
                return tuple(sorted(feature(orbits[i],radius) for i in ids))
            patterns = {key(p):p for p in sorted(positive)}
            collisions = [p for p in combinations(range(36),sizes)
                          if p not in positive and key(p) in patterns]
            negative = collisions[0]
            match = patterns[key(negative)]
            profiles[radius] = dict(collisions=len(collisions), removed=match, survives=negative)
            if radius == 2:
                new_cuts = []
                available = sorted(set(range(18))-set(match)-set(negative))
                for added in available[:3]:
                    pair = [tuple(sorted((*base,added))) for base in (match,negative)]
                    assert key(pair[0]) == key(pair[1])
                    outcomes = []
                    for ids in pair:
                        removed = {tuple(w) for i in ids for w in orbits[i]['members']}
                        rows = audit({k:s-removed for k,s in sources.items()},False)
                        outcomes.append(not rows[name][metric])
                    new_cuts.append(dict(cuts=pair, removed=outcomes))
                profiles[radius]['augmented_cuts'] = new_cuts
        result[name] = profiles
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
