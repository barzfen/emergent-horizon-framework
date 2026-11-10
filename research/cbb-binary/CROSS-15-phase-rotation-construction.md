# EHF-CBB-CROSS-15 — Phase rotations, LR4 construction, and normalization traps

Date: 2026-11-10. Status: exact BFS for m=2..6; explicit uniform LR4-only construction for m>=2 (verified computationally through m=19); optimality unproved for arbitrary m.

## Problem
Position-indexed balanced proper three-colour words of length n=3m, LR3 and LR4 cyclic segment reversals. Target T=(ABC)^m. Two phase rotations R1=(BCA)^m, R2=(CAB)^m are distinct as indexed words but identical to T modulo cyclic rotation.

## Exact BFS checks
| m | n | graph states | max shortest distance from T | distance(T,R1) | distance(T,R2) | count at max |
| 2 | 6 | 24 | 4 | 4 | 4 | 2 |
| 3 | 9 | 132 | 6 | 6 | 6 | 2 |
| 4 | 12 | 804 | 8 | 8 | 8 | 2 |
| 5 | 15 | 5196 | 10 | 10 | 10 | 2 |
| 6 | 18 | 34872 | 12 | 12 | 12 | 2 |

Thus both phase rotations are the unique farthest states in all five tested sizes. These are fixed-position distances, NOT distances modulo cyclic rotation. Neither an arbitrary-n diameter theorem nor arbitrary-n optimality is established.

## Uniform LR4-only phase-rotation construction
For m>=2, set w=(ABC)^m, index positions 0,...,3m-1. Apply LR4 with cyclic start indices, in this order:
- 0, 3;
- for j=1,...,m-1, append (3j-2) and then (3j+3) if j<m-1, otherwise (3m-2).

This yields exactly 2m moves. Each intermediate word is proper and balanced, and the final word is (BCA)^m. This is a uniform constructive *upper bound* d(T,R1)<=2m. It was checked for m=2..19, and the regular pattern admits a direct blockwise induction (to be written in full for formal publication).

Example m=3: start indices [0,3,1,6,4,7]. States:
ABCABCABC
ACBABCABC
ACBACBABC
ACABCBABC
ACABCBACB
ACABCABCB
BCABCABCA

A global relabelling of A,B,C sends the same construction between other cyclic phase rotations. Because reversals are involutions, it can be traversed backwards.

## Reproduction and verification
```python
from collections import deque,Counter
def rev(w,k,i):
    n=len(w); ix=[(i+t)%n for t in range(k)];v=list(w)
    for j,x in zip(ix,reversed([w[t] for t in ix])):v[j]=x
    return tuple(v)
def proper(w):
    return all(w[i]!=w[(i+1)%len(w)] for i in range(len(w)))
for m in range(2,20):
    n=3*m;w=(0,1,2)*m
    starts=[0,3]
    for j in range(1,m):
        starts.extend([3*j-2,3*j+3 if j<m-1 else 3*m-2])
    assert len(starts)==2*m
    for i in starts:
        w=rev(w,4,i)
        assert proper(w)
    assert w==(1,2,0)*m
print('Uniform LR4 construction checked m=2..19')

for m in range(2,7):
    n=3*m;T=(0,1,2)*m;Q=deque([T]);d={T:0}
    while Q:
        u=Q.popleft()
        for k in (3,4):
            for i in range(n):
                v=rev(u,k,i)
                if v not in d and proper(v):
                    d[v]=d[u]+1;Q.append(v)
    r1=(1,2,0)*m;r2=(2,0,1)*m
    mx=max(d.values())
    print(m,len(d),mx,d[r1],d[r2],sum(x==mx for x in d.values()))
```

## Naive normalization potential fails
Hamming distance to the fixed target is not a universal strictly descending potential. Counting states (excluding target) with no legal LR3/LR4 neighbour having strictly lower Hamming distance:
m=2 (n6): 0; m=3 (n9): 0; m=4 (n12): 12; m=5 (n15): 40.
Therefore a greedy algorithm minimizing simple position mismatches gets stuck by n=12, even though all these states remain connected to the target. This is an exact finite counterexample to that proposed *algorithm*, not to connectivity.

## What is proved vs conjectured
- Proven from explicit move formula once its straightforward block induction is formalized: phase rotation has an LR4-only path of length 2m; computational verification m<=19 is provided.
- Exact BFS: phase rotations uniquely maximize distance to fixed T for m=2..6.
- Open: show 2m is a lower bound for phase rotations for all m, and show every balanced proper word normalizes to T by a uniformly terminating local rule.
- No derived 1:2:3 ratio or physics claim.

## Next
Find a lower-bound potential for the phase-rotation distance that changes by at most one per move, and a normalization algorithm robust to Hamming local minima. Analyze quotient by cyclic rotations separately to remove indexing artefacts.
