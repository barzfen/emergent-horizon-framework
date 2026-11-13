#!/usr/bin/env python3
"""EHF-AMP-HOL-BRIDGE-02: signed reflection vs nine-point tail residue.

Exact rational arithmetic, standard library only, no existing result files.
This reimplements the tail rank test independently of reconstruct.py.
Run: python3 signed_orientation_bridge.py
"""
from itertools import permutations, combinations
from functools import lru_cache
from collections import Counter
from fractions import Fraction
from pathlib import Path
import json

@lru_cache(None)
def shuffle(a,b):
    if not a:return (b,)
    if not b:return (a,)
    return tuple((a[0],)+s for s in shuffle(a[1:],b))+tuple((b[0],)+s for s in shuffle(a,b[1:]))

def reflect(w):return w[:1]+w[:0:-1]
def canon(w):return min(w,reflect(w))

@lru_cache(None)
def KK(w):
    i=w.index(9);a=w[1:i];b=w[i+1:]
    return {s:(-1)**len(b) for s in shuffle(a,b[::-1])}

def D(w):
    if w[-1]==9:return 1,w[:-1]
    if w[1]==9:return -1,w[:1]+w[2:]
    return 0,None

def source(A):
    left=tuple(x for x in range(2,9) if x not in A)
    right=tuple(A)+(9,)
    return tuple((1,)+tuple(x for p in zip(l,r) for x in p)
                 for l in permutations(left) for r in permutations(right))

def target(A):
    left=tuple(x for x in range(2,9) if x not in A)
    out=[]
    for r in permutations(A):
        for l in permutations(left):
            t=[]
            for i in range(4):
                t.append(l[i])
                if i<3:t.append(r[i])
            w=(1,)+tuple(t)
            if w[1]<w[-1]:out.append(w)
    return sorted(out)

def axpy(v,c,u):
    for k,x in u.items():
        y=v.get(k,0)+c*x
        if y:v[k]=y
        else:v.pop(k,None)

def ranks(words,tidx):
    """Eliminate KK columns while carrying residue; rank of residue(Ker KK)."""
    pivots={};im={};kerrank=0
    for w in words:
        q={k:Fraction(x) for k,x in KK(w).items()}
        sign,t=D(w)
        d={tidx[canon(t)]:Fraction(sign)} if sign else {}
        while q:
            p=min(q);c=q[p]
            if p not in pivots:
                pivots[p]=({k:v/c for k,v in q.items()},{k:v/c for k,v in d.items()})
                break
            a,b=pivots[p];axpy(q,-c,a);axpy(d,-c,b)
        if q:continue
        kerrank+=1
        while d:
            p=min(d);c=d[p]
            if p not in im:
                im[p]={k:v/c for k,v in d.items()};break
            axpy(d,-c,im[p])
    return (len(pivots),kerrank,len(im))

def expected(A):
    a,b,c=A
    if b<=4:return 0 if c<=5 else (2 if c==6 else 9)
    if b==5:return 8 if c==6 else 14
    return 15

def main():
    # D R9 = -R8 D (unsigned), so D(-R9)=(+R8)D (signed).
    for p in permutations(range(2,10)):
        w=(1,)+p;r=reflect(w)
        s,t=D(w);sr,tr=D(r)
        assert sr==-s and (s==0 or tr==reflect(t))
        qw=KK(w);qr=KK(r)
        assert len(qw)==len(qr) and all(qr.get(k)==-v for k,v in qw.items())
    records=[]
    for A in combinations(range(2,9),3):
        full=source(A)
        cut=tuple(w for w in full if w[1]<w[-1])
        mirrored=tuple(reflect(w) for w in cut)
        tidx={w:i for i,w in enumerate(target(A))}
        assert len(full)==576 and len(set(full)&set(mirrored))==0
        assert sum(w[-1]==9 for w in full)==sum(w[-1]==9 for w in cut)==144
        c=ranks(cut,tidx);m=ranks(cut+mirrored,tidx);f=ranks(full,tidx)
        assert c[2]==m[2]==expected(A)
        assert f[2]==15
        records.append({'A':list(A),'cut_size':len(cut),
             'cut_rank':c[2],'cut_and_reflections_rank':m[2],
             'full_parity_rank':f[2],
             'cut_KK_rank':c[0],'cut_relation_dim':c[1]})
    A=(4,5,8);full=source(A);cut=tuple(w for w in full if w[1]<w[-1])
    tidx={w:i for i,w in enumerate(target(A))}
    u=(1,6,4,7,9,2,8,3,5)
    v=(1,6,5,7,9,2,8,3,4)
    assert u in full and v in full and u not in cut and v not in cut
    assert D(u)[0]==D(v)[0]==0
    repair={name:ranks(words,tidx)[2] for name,words in
      [('cut',cut),('plus_u',cut+(u,)),('plus_v',cut+(v,)),
       ('plus_both',cut+(u,v))]}
    assert repair=={'cut':14,'plus_u':14,'plus_v':14,'plus_both':15}
    out={'status':'PASS','signed_residue_reflection_checks':40320,
         'cut_rank_counts':dict(Counter(x['cut_rank'] for x in records)),
         'all_35_reflection_closures_leave_ranks_unchanged':True,
         'all_35_full_parity_ranks':15,
         'rank14_two_word_repair':repair,'fibres':records,
         'scope':'signed PT reflection and KK-residue image in anchor-1 delete-9 chart; no Hamiltonian-path-to-amplitude functor claimed'}
    Path(__file__).with_name('signed-orientation-bridge-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS: 40320 signed orderings, 35 cut and reflection-closure ranks, 35 full-parity ranks')
    print('rank profile:',out['cut_rank_counts'])
    print('rank-14 repair:',repair)

if __name__=='__main__':main()
