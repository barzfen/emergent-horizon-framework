#!/usr/bin/env python3
"""Independent exact-rational rank check for EHF-AMP-HOL-BRIDGE-05.

Implements its own KK shuffle, signed deletion and Gaussian elimination.
The primary script must first have generated rank14-lr3-threshold-results.json.
No third-party dependencies.
"""
from fractions import Fraction as F
from itertools import permutations
from functools import lru_cache
from pathlib import Path
import json

@lru_cache(None)
def shuffle(a,b):
    if not a:return (b,)
    if not b:return (a,)
    return tuple((a[0],)+s for s in shuffle(a[1:],b))+tuple((b[0],)+s for s in shuffle(a,b[1:]))

def KK(w):
    j=w.index(9);a=w[1:j];b=w[j+1:]
    return {p:F((-1)**len(b)) for p in shuffle(a,b[::-1])}

def canonical(w):
    return min(w,(w[0],)+w[:0:-1])

def full(A):
    B=tuple(x for x in range(2,9) if x not in A)
    for even in permutations(B):
        for odd in permutations((*A,9)):
            yield (1,)+tuple(x for pair in zip(even,odd) for x in pair)

def target(A):
    B=tuple(x for x in range(2,9) if x not in A)
    out=[]
    for u in permutations(A):
        for v in permutations(B):
            w=[1]
            for k in range(4):
                w.append(v[k])
                if k<3:w.append(u[k])
            if w[1]<w[-1]:out.append(tuple(w))
    return sorted(out)

def axpy(v,c,u):
    for k,x in u.items():
        y=v.get(k,0)+c*x
        if y:v[k]=y
        else:v.pop(k,None)

def residue(w,ids):
    if w[-1]==9:return {ids[canonical(w[:-1])]:F(1)}
    if w[1]==9:return {ids[canonical(w[:1]+w[2:])]:F(-1)}
    return {}

def image_rank(words,ids):
    qbase={};dbase={};image={}
    for w in words:
        q=KK(w);d=residue(w,ids)
        while q:
            p=min(q);c=q[p]
            if p not in qbase:
                qbase[p]={k:v/c for k,v in q.items()}
                dbase[p]={k:v/c for k,v in d.items()}
                break
            axpy(q,-c,qbase[p]);axpy(d,-c,dbase[p])
        if q:continue
        while d:
            p=min(d);c=d[p]
            if p not in image:
                image[p]={k:v/c for k,v in d.items()}
                break
            axpy(d,-c,image[p])
    return len(image)

def main():
    data=json.loads(Path(__file__).with_name('rank14-lr3-threshold-results.json').read_text())
    for r in data['rows']:
        A=tuple(r['A'])
        S=tuple(w for w in full(A) if w[1]<w[-1])
        pair=tuple(tuple(int(x) for x in text) for text in r['canonical_lr3_pair'])
        ids={w:i for i,w in enumerate(target(A))}
        before=image_rank(S,ids);after=image_rank(S+pair,ids)
        assert (before,after)==(14,r['rank_after_pair']),(A,before,after)
        assert all(w not in S and not residue(w,ids) for w in pair)
        print('Independent rank',A,before,'->',after,flush=True)
    # Regenerate the seed relations by the primary elimination, then
    # independently verify their KK zero sum and their nonzero residues.
    from rank14_lr3_threshold_probe import certificate,POSITIVE_SEEDS
    for A in POSITIVE_SEEDS:
        c=certificate(A);ids={w:i for i,w in enumerate(target(A))}
        q={};d={}
        for w,coef in c.items():
            axpy(q,coef,KK(w));axpy(d,coef,residue(w,ids))
        assert not q and d
        print('Independent seed relation',A,'terms',len(c),
              'nonzero residue coordinates',len(d),flush=True)
    print('ALL INDEPENDENT EXACT-RATIONAL CHECKS PASSED')

if __name__=='__main__':
    main()
