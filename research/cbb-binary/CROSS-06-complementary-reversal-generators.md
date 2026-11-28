# EHF-CBB-CROSS-06 — Complementarity of LR3 and LR4

Date: 2026-11-10. Status: exhaustive labelled-cycle computation for n=6,7,8; no general connectivity theorem claimed.

## Model
Undirected Hamiltonian cycles on n labelled vertices, modulo rotation/reversal. Colours fixed on vertex identities as c(v)=v mod q. Properness requires unlike colours at every cyclic adjacency. LRk reverses k consecutive cyclic entries; a move is allowed iff the resulting cycle remains proper. Raw means no colour constraint.

## n=8 results: number of connected components
| model | states | LR2 | LR3 | LR4 | LR5 | LR3+LR4 | LR2+LR3 | LR2+LR4 | LR4+LR5 |
| raw | 2520 | 1 | 35 | 1 | 35 | 1 | 1 | 1 | 1 |
| q=2 (4,4) | 72 | 72 | 1 | 72 | 1 | 1 | 1 | 72 | 1 |
| q=3 (3,3,2) | 252 | 6 | 35 | 4 | 35 | 1 | 1 | 1 | 1 |
| q=4 (2,2,2,2) | 744 | 1 | 75 | 121 | 75 | 1 | 1 | 1 | 1 |

Notably LR3 and LR4 individually fail to connect q=3 and q=4, but their union is connected. q=2 is already connected by LR3, and raw already by LR4.

## n=6 and n=7 checks
For n=6 all nonempty models raw, q2, q3, q4 have one LR3+LR4 component (60,6,16,24 states respectively).
For n=7 raw, q3 and q4 have one LR3+LR4 component (360,48,120 states). Proper q2 cyclic states are absent for odd n.

## Exact implication and limits
This proves finite-instance generator complementarity. It does NOT prove that LR3+LR4 always connects proper q>=3 Hamiltonian cycles at arbitrary n, nor that these conditional reversals form a Lie group. Connectedness is for labelled cycles, not colour bracelets. For q2 with strict alternation, even-length reversals are inadmissible; odd-length reversals may permute vertex identities.

## Reproducible code
```python
from itertools import permutations
def audit(n,q):
    states={(0,)+p for p in permutations(range(1,n)) if p[0]<p[-1]}
    def canon(a):
        j=a.index(0);b=a[j:]+a[:j]
        return min(b,(b[0],)+b[:0:-1])
    colors=None if q is None else tuple(i%q for i in range(n))
    allowed={s for s in states if colors is None or all(colors[s[i]]!=colors[s[(i+1)%n]] for i in range(n))}
    adj={k:{s:set() for s in allowed} for k in range(2,6)}
    for s in allowed:
        for k in range(2,6):
            if k>=n:continue
            for i in range(n):
                b=list(s);ix=[(i+j)%n for j in range(k)]
                for a,v in zip(ix,[s[t] for t in ix][::-1]):b[a]=v
                t=canon(tuple(b))
                if t in allowed and t!=s:adj[k][s].add(t)
    def comp(ks):
        seen=set();sizes=[]
        for s in allowed:
            if s in seen:continue
            todo=[s];seen.add(s);z=0
            while todo:
                u=todo.pop();z+=1
                for k in ks:
                    for v in adj[k][u]:
                        if v not in seen:seen.add(v);todo.append(v)
            sizes.append(z)
        return len(sizes),max(sizes,default=0)
    return len(allowed),{str(ks):comp(ks) for ks in ((3,),(4,),(3,4),(2,3),(2,4),(4,5))}
for n in (6,7,8):
    for q in (None,2,3,4):
        print(n,q,audit(n,q))
```

## Next
Test n=9 with q=3 and q=4 to check whether LR3+LR4 still restores connectivity, and seek constructive proof or counterexample for a general generator theorem. Examine whether a finite set of local reversal lengths can connect all proper coloured cycles for q>=3, with specified colour multiplicities. Keep graph connectivity distinct from algebraic group-action claims.
