# EHF-CBB-CROSS-16 — Bounds for phase-rotation distance

Date: 2026-11-10. Status: exact finite shortest paths, verified explicit construction, general lower bounds; no general optimality theorem.

## Definitions
Position-indexed cyclic balanced proper three-colour words of length n=3m, with moves LR3 and LR4: reverse 3 or 4 consecutive cyclic positions, retaining only proper results. T=(ABC)^m and R=(BCA)^m. These are distinct indexed words, but equivalent under cyclic rotation.

## Verified LR4-only construction
For m>=2 the following starts define 2m LR4 reversals:
[0,3] followed for j=1,...,m-1 by
(3j-2, 3j+3) if j<m-1, and (3m-5,3m-2) at j=m-1.
Each step is checked for properness; final word R. Computational verification m=2..19. A formal induction of all intermediate patterns is desirable; the finite verification by itself does not prove the construction for arbitrary m.

## Exact BFS results previously obtained (CROSS-14/15)
m=2..6: d(T,R)=2m, and both nontrivial phase rotations uniquely maximize distance to T among the respective finite state graphs. These are finite certificates, not an arbitrary-m lower bound.

## General lower bound from Hamming distance
Hamming distance H(T,R)=3m: every indexed position changes colour. One LR3 reversal exchanges endpoints and leaves the middle position unchanged, so it changes at most 2 positions. One LR4 reversal exchanges two pairs, so it changes at most 4 positions. Thus any path of t moves has H(T,R)<=4t, yielding
d(T,R) >= ceil(3m/4).
This bound is weak compared with observed 2m but rigorously applies for every m for which a path exists.

## Additional winding-based restriction
W(T)=W(R)=m, the maximum possible winding. LR3 conserves W; any proper LR4 changes W by +/-2. Therefore every path from T to R has an even number of LR4 moves (as many +2 as -2), and any path containing LR4 must contain at least two. Moreover, no LR3 move is admissible from T: the fully forward cyclic pattern ABCABC... makes every LR3 boundary fail. Hence a nontrivial path must contain at least two LR4 moves. Together:
d(T,R) >= max(2,ceil(3m/4)).
This is a valid but not sharp lower bound for m>=2. No proof that d(T,R)>=2m is claimed.

## Reproduction of the constructive path
```python
def rev(w,k,i):
    n=len(w);ix=[(i+j)%n for j in range(k)];v=list(w)
    for a,b in zip(ix,reversed([w[t] for t in ix])):v[a]=b
    return tuple(v)
def proper(w):
    return all(w[i]!=w[(i+1)%len(w)] for i in range(len(w)))
for m in range(2,20):
    w=(0,1,2)*m
    starts=[0,3]
    for j in range(1,m):
        starts.extend([3*j-2,3*j+3 if j<m-1 else 3*m-2])
    assert len(starts)==2*m
    for i in starts:
        w=rev(w,4,i)
        assert proper(w)
    assert w==(1,2,0)*m
print('Verified phase-rotation paths for m=2..19')
```

## Crucial scope distinction
These distances are artefacts of indexing in the sense that T and R are the same *unindexed cyclic word*. They can still be interesting combinatorial metrics on the indexed reconfiguration graph, but must not be interpreted as an intrinsic cycle-space obstruction. The stronger open goal remains a general connectivity/normalization theorem for all balanced proper cyclic three-colour words using LR3+LR4.

## Next
Derive an invariant/potential with per-move change <=1 and total difference 2m, or exhibit a shorter path for m>=7. Separately prove the uniform LR4 construction by induction and find a terminating normalization algorithm for arbitrary balanced proper words. No 1:2:3 ratio has been established here.
