"""Trace and selectively restore doubled coefficients in the minus-minus sector."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
import json

from mixed_orbits import rank
from ordering_holdout import load
from probe import cut, cuts, words
from reconstruct import kk
from shuffle_sectors import inactive_columns, orbit_columns
from support_reduction import ACTIVE
from support_sector_test import run

SIGNS = (-1, -1)


def columns(source):
    return dict(zip((min(o) for o in orbit_columns(
        (w for w in source if w[-1] != 9), SIGNS)), inactive_columns(source,SIGNS)))


def audit(groups, select):
    def weight(word, row, value):
        return value if abs(value)==1 or select(word,row) else Fraction(1 if value>0 else -1)
    return run(*[[{row:weight(word,row,value) for row,value in col.items()}
                  for word,col in group.items()] for group in groups],rank)


def signature(result):
    return result['extra_shared'],result['extra_union_cancel']


def main():
    left,right,union = map(set,(cuts[8],cuts[9],cut((2,2,4),words)))
    groups = [columns(source) for source in (left,right,union)]

    def category(word,row):
        branch = 'common' if word in left & right else 'rank8' if word in left else 'rank9'
        return branch,word.index(9)+1,'active' if row in ACTIVE else 'exterior'

    counts = Counter(category(w,k) for w,col in groups[2].items()
                     for k,v in col.items() if abs(v)==2)
    exact = audit(groups,lambda w,k:True)
    trials = []
    for size in range(len(counts)+1):
        for subset in combinations(sorted(counts),size):
            chosen = set(subset)
            measured = audit(groups,lambda w,k:category(w,k) in chosen)
            trials.append(dict(groups=subset,restored=sum(counts[k] for k in subset),
                               signature=signature(measured),full_rank_profile_matches=measured==exact))
    successful = [r for r in trials if r['signature']==signature(exact)]
    best = min(successful,key=lambda r:r['restored'])
    full = min((r for r in trials if r['full_rank_profile_matches']),key=lambda r:r['restored'])
    examples = {}
    for orbit in orbit_columns((w for w in union if w[-1]!=9),SIGNS):
        word = min(orbit)
        for row,value in groups[2][word].items():
            label = category(word,row)
            if abs(value)!=2 or label in examples:
                continue
            terms = [(w,str(c),str(kk(w)[row])) for w,c in sorted(orbit.items()) if row in kk(w)]
            assert len(terms)==2
            assert sum(Fraction(c)*Fraction(v) for _,c,v in terms)==value
            examples[label]=dict(representative=word,row=row,coefficient=str(value),terms=terms)
    print(json.dumps(dict(counts=[[k,v] for k,v in sorted(counts.items())],
                          best_signature=best,best_full_profile=full,trials=trials,
                          examples=[[k,v] for k,v in sorted(examples.items())]),indent=2))


if __name__ == '__main__':
    main()
