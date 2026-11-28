#!/usr/bin/env python3
"""
EHF-HC-RAW-09A — Johnson A1 Selection Audit

Exact result:
For odd->even completion HC_{2m-1}->HC_{2m}, let x=2m-1 be the newest label
and pi_x delete x.  For every target LR2 edge (C,D),

  pi_x(C) != pi_x(D)  iff  d_J^x(Pi(C),Pi(D)) = 1,
  pi_x(C) == pi_x(D)  iff  d_J^x(Pi(C),Pi(D)) = m-1.

Thus the new-site anchor separates the intrinsic delta=1 shell:
A1 is the growth-horizontal branch and A_{m-1} is the vertical insertion-slot branch.

Without the growth structure, A1 is not anchor invariant.
For an intrinsic delta=1 sector pair, A1 is seen from 2m-2 anchors and
A_{m-1} from the two exchanged labels.
"""
from itertools import permutations
import math

def canonicalize(c):
    c=tuple(c); i=c.index(0); a=c[i:]+c[:i]
    r=(a[0],)+tuple(reversed(a[1:]))
    return min(a,r)

def cycles(n):
    for p in permutations(range(1,n)):
        if p[0] < p[-1]:
            yield (0,)+p

def rev2(c,s):
    a=list(c); n=len(a); i=s%n; j=(s+1)%n
    a[i],a[j]=a[j],a[i]
    return canonicalize(a)

def delete(c,x):
    return canonicalize(tuple(v for v in c if v!=x))

def bipartition(c):
    return frozenset((frozenset(c[0::2]),frozenset(c[1::2])))

def side(P,a):
    A,B=tuple(P)
    return A if a in A else B

def jdist(P,Q,a):
    S=side(P,a)-{a}; T=side(Q,a)-{a}
    return len(S-T)

def certify(m):
    N=2*m; x=N-1
    cs=list(cycles(N)); ix={c:i for i,c in enumerate(cs)}
    E=set()
    for i,c in enumerate(cs):
        for s in range(N):
            d=rev2(c,s); j=ix[d]
            if i!=j:
                E.add(tuple(sorted((i,j))))
    faithful=vertical=0
    for a,b in E:
        c,d=cs[a],cs[b]
        same=delete(c,x)==delete(d,x)
        r=jdist(bipartition(c),bipartition(d),x)
        if same:
            vertical+=1
            assert r==m-1
        else:
            faithful+=1
            assert r==1
    total=math.factorial(N)//4
    vf=math.factorial(N-1)//2
    assert len(E)==total
    assert vertical==vf
    assert faithful==total-vf
    assert faithful==(m-1)*vertical
    print("m",m,"PASS",{"faithful":faithful,"vertical":vertical})

for m in (3,4):
    certify(m)

print("EHF_HC_RAW_09A_JOHNSON_A1_SELECTION_AUDIT_PASS")
