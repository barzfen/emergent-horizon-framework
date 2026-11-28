"""Check whether the original exterior matching class survives each cut."""
import json

from mixed_orbits import rank
from ordering_holdout import load
from probe import cut, cuts, words
from union_cancellation_rule import setup


def main():
    left,right,union = map(set,(cuts[8],cuts[9],cut((2,2,4),words)))
    results = load('common-cut-verification.json')
    equations = setup(left,right,union,[{'representative':w}
                      for w in results['orbit_representatives']])
    classes = []
    for case in results['cases']:
        ids = case['removed']
        survives = rank(equations[i][0] for i in ids)==rank(equations[i][1] for i in ids)
        assert not survives or case['exact'][1] > 0
        classes.append(dict(kind=case['kind'],position=case.get('position'),removed=ids,
                            original_class_survives=survives,exact=case['exact']))
    print(json.dumps(classes,indent=2))


if __name__ == '__main__':
    main()
