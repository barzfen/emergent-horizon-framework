#!/usr/bin/env python3
"""Independent direct-rank check of minimal triple witnesses (stdlib Python)."""
from itertools import combinations
from signed_orientation_bridge import source, target, D, canon, ranks
from rank14_event_pairs import oracle

CASES={
    (2,5,7):('162374985','162894735','169473285'),
    (3,5,7):('145678923','163894725','165894723'),
}

def main():
    for A,strings in CASES.items():
        words=tuple(tuple(map(int,w)) for w in strings)
        out=oracle(A)
        assert len(out['repair_pairs'])==0
        assert not out['one_word_repairs']
        cut=out['cut'];excluded=set(out['excluded']);idx=out['idx']
        assert set(words)<=excluded
        assert all(D(w)[0]==0 for w in words)
        assert ranks(cut,idx)[2]==14
        for k in (1,2,3):
            for subset in combinations(words,k):
                actual=ranks(cut+subset,idx)[2]
                assert actual==(15 if k==3 else 14),(A,subset,actual)
        print(A,'PASS: no one/pair repairs anywhere and explicit triple rank 15')
    print('INDEPENDENT EXACT RANK CHECKS PASSED')

if __name__=='__main__':main()
