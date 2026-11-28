#!/usr/bin/env python3
from itertools import permutations
from collections import Counter, defaultdict
import math

def canonicalize(c):
    c=tuple(c); i=c.index(0); a=c[i:]+c[:i]
    r=(a[0],)+tuple(reversed(a[1:]))
    return min(a,r)

def reverse_block(c,s,l):
    a=list(c); n=len(a)
    p=[(s+j)%n for j in range(l)]
    v=[a[x] for x in p][::-1]
    for x,y in zip(p,v): a[x]=y
    return tuple(a)

def bipartition(c):
    return frozenset((frozenset(c[0::2]),frozenset(c[1::2])))

def sector(c):
    A,B=tuple(bipartition(c)); side=A if 0 in A else B
    return frozenset(x for x in side if x!=0)

def jdist(S,T): return len(S-T)
def fsize(m): return math.factorial(m-1)*math.factorial(m)//2
def weight(m,r): return (math.factorial(r)*math.factorial(m-r))**2
def jval(m,r): return math.comb(m-1,r)*math.comb(m,r)

def fiber(m):
    A=tuple(range(m)); B=tuple(range(m,2*m)); out=set()
    for pa in permutations(A[1:]):
        for pb in permutations(B):
            q=[0]
            for j in range(m):
                q.append(pb[j])
                if j<m-1:q.append(pa[j])
            out.add(canonicalize(tuple(q)))
    return out

def neighbors(c):
    n=len(c); m=n//2; out=set()
    for l in range(2,m+1):
        for s in range(n):
            out.add(canonicalize(reverse_block(c,s,l)))
    out.discard(c); return out

for m in range(3,6):
    F=fiber(m); S=frozenset(range(1,m)); counts=Counter()
    for c in F:
        for d in neighbors(c):
            T=sector(d)
            if T!=S: counts[T]+=1
    assert len(F)==fsize(m)
    for r in range(1,m):
        vals=[v for T,v in counts.items() if jdist(S,T)==r]
        assert len(vals)==jval(m,r)
        assert min(vals)==max(vals)==weight(m,r)
    print("m",m,"PASS")

print("EHF_HC_RAW_08B_INTRINSIC_BIPARTITION_JOHNSON_QUOTIENT_PASS")
