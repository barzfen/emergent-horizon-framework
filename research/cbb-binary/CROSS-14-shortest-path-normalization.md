# EHF-CBB-CROSS-14 — Shortest-path normalization audit

Date: 2026-11-10. Status: executed BFS, finite constructive certificates, conjectural scaling.

## Problem
For balanced proper cyclic three-colour position-indexed words of length n=3m, use LR3 and LR4 reversals of cyclic contiguous positions to reach the fixed target T=(ABC)^m. Unlike rotation-quotient words, position-indexed words distinguish rotations of T.

## Exact BFS results
| n | reachable states | max distance to T | states at max distance |
| 6 | 24 | 4 | 2 |
| 9 | 132 | 6 | 2 |
| 12 | 804 | 8 | 2 |
| 15 | 5196 | 10 | 2 |
| 18 | 34872 | 12 | 2 |

All balanced proper states at these lengths are reached. For n=9 the two farthest words are BCABCABCA and CABCABCAB, the two nontrivial position shifts of T. This warns that the maximum is **eccentricity of a fixed position-indexed target**, not the diameter of a rotation-quotient graph and not an intrinsic lower bound on normalization modulo rotation.

## Hypothesis
For m>=2, eccentricity of T in the position-indexed LR3+LR4 graph is 2m. This is supported by m=2..6 only. It is independent of the stronger conjecture that the graph is connected for every m.

## Algorithm
Breadth-first search from T gives a shortest legal path to T for every reachable state. Store parent pointers and reversal (k,start) to reconstruct normalization certificates. The algorithm is finite but exponential in n; BFS at tested n is not a uniform constructive proof of arbitrary-n connectivity.

## Reproduction
```python
from collections import deque,Counter
for m in range(2,7):
    n=3*m
    T=(0,1,2)*m
    q=deque([T])
    distance={T:0}
    parent={T:None}
    while q:
        u=q.popleft()
        for k in (3,4):
            for i in range(n):
                ix=[(i+j)%n for j in range(k)]
                v=list(u)
                for j,x in zip(ix,reversed([u[t] for t in ix])):v[j]=x
                v=tuple(v)
                if v in distance or any(v[t]==v[(t+1)%n] for t in range(n)):continue
                distance[v]=distance[u]+1
                parent[v]=(u,k,i)
                q.append(v)
    hist=Counter(distance.values())
    farthest=[''.join('ABC'[x] for x in w) for w,d in distance.items() if d==max(distance.values())]
    print(n,len(distance),max(distance.values()),hist[max(distance.values())],farthest)
    # Given any w in parent, repeatedly apply parent[w] to obtain
    # a legal shortest path to T.
```

## Next
Find a local, terminating normalization potential that works for every m. Investigate why nontrivial rotations of the target appear maximally distant, and test whether this persists. Avoid confusing fixed-position target eccentricity with graph diameter. Seek a proof or counterexample to the 2m bound, and a separate general proof of LR3+LR4 connectivity.
