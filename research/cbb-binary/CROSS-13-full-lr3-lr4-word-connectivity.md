# EHF-CBB-CROSS-13 — Full LR3+LR4 connectivity, balanced three-colour words

Date: 2026-11-10. Status: executed exhaustive computation, not yet general theorem.

## Question
Does the transition graph on all balanced, proper, position-indexed cyclic three-colour words of length n=3m become connected when both LR3 and LR4 are permitted? Each colour occurs exactly m times. Reversals operate on consecutive cyclic positions, and a resulting word is retained only if every cyclic adjacent pair has distinct colours.

## Results
| m | n | words | LR3+LR4 connected components | largest component |
| 2 | 6 | 24 | 1 | 24 |
| 3 | 9 | 132 | 1 | 132 |
| 4 | 12 | 804 | 1 | 804 |
| 5 | 15 | 5196 | 1 | 5196 |
| 6 | 18 | 34872 | 1 | 34872 |

These are full position-indexed word graphs, not winding quotient graphs, rotation/reflection bracelets, or labelled-vertex Hamiltonian cycle graphs. Thus the finite result should not be conflated with the labelled-cycle parity result in CROSS-07. Exhaustive enumeration establishes connectedness for m=2..6, not arbitrary m.

## Reproducible executable Python 3
```python
from collections import Counter
for m in range(2,7):
    n=3*m
    words=[]
    def rec(w,c):
        if len(w)==n:
            if w[-1]!=w[0]:words.append(tuple(w))
            return
        for x in range(3):
            if c[x]<m and (not w or w[-1]!=x):
                c[x]+=1;w.append(x);rec(w,c);w.pop();c[x]-=1
    rec([],[0]*3)
    S=set(words);seen=set();sizes=[]
    for w in words:
        if w in seen:continue
        stack=[w];seen.add(w);z=0
        while stack:
            u=stack.pop();z+=1
            for k in (3,4):
                for i in range(n):
                    ix=[(i+j)%n for j in range(k)]
                    v=list(u)
                    for j,t in zip(ix,reversed([u[j] for j in ix])):v[j]=t
                    v=tuple(v)
                    if v in S and v not in seen:
                        seen.add(v);stack.append(v)
        sizes.append(z)
    print(m,n,len(words),len(sizes),max(sizes),Counter(sizes))
```

## The conjecture
For every integer m>=2, the LR3+LR4 transition graph on balanced proper cyclic three-colour words of length 3m is connected.

## Proof strategy
Seek a terminating normalization procedure taking an arbitrary balanced proper word to a canonical block word such as (ABC)^m, using only legal LR3/LR4 moves. CROSS-12 already constructs a ladder of representatives C_p=(ABC)^p(ACB)^(m-p), connected by LR4, but that only proves connectivity of winding levels; it does not show every word reaches some C_p. The missing lemma is a within-level normalization or an alternate global descent algorithm. A computer search for a monotone potential could suggest one, but a proof must show no local minima.

## Interpretation
Two simple local reversal rules suffice for full reachability in five tested finite word systems, including 34,872 states at n=18. This is combinatorial reconfiguration evidence, not a physics result, not a Lie-group identification, and not a derivation of the conjectured 1:2:3 ratio.
