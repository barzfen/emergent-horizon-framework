# EHF-CBB-CROSS-07 — Nine-vertex LR3+LR4 connectivity and parity explanation

Date: 2026-11-10. Status: independently executed exhaustive enumeration and analytic parity obstruction.

## Model
n=9 labelled vertices 0,...,8, undirected Hamiltonian cycles modulo rotation and reversal. Each vertex v has fixed colour c(v)=v mod q. For q=3, colour class sizes (3,3,3); for q=4, sizes (3,2,2,2). Admissibility: adjacent vertices have distinct colours. LRk reverses k consecutive cyclic positions and is permitted if resulting cycle remains proper. Count connected components of the labelled-cycle transition graph.

## Executed results
Unrestricted raw labelled undirected Hamiltonian cycles: (9-1)!/2 = 20160.

| q | proper labelled cycles | LR3 components | LR4 components | LR3+LR4 components |
| 3 | 1584 | 235 | 2 (792 each) | 1 (1584) |
| 4 | 3696 | 127 | 2 (1848 each) | 1 (3696) |

LR3 component-size distributions:
q=3: 72 singleton, 162 size-4, 1 size-864.
q=4: 72 size-2, 48 size-4, 6 size-8, 1 size-3312.
These agree with earlier q=3 TRI-02 and independently verify LR3+LR4 connectivity at n=9.

## Parity theorem for n=9
Fix a representation of an undirected Hamiltonian cycle as the vertex order starting at label 0, choosing either traversal direction. For n=9, changing traversal direction reverses the remaining 8 labels, which is an even permutation (4 transpositions). Therefore the parity of the resulting 9-label ordering is well-defined on undirected cycles. Alternatively, rotation by one of a 9-cycle is even, and reversal of the 9 positions has 4 transpositions, also even.

An LR4 reversal exchanges two disjoint position pairs, hence is an even permutation and preserves parity. An LR3 reversal swaps one position pair, hence is odd and flips parity. Thus LR4 cannot cross the even/odd permutation parity classes, while LR3 can. The enumeration establishes each parity class is LR4-connected for the specific q=3 and q=4 colour assignments above, and that the combined LR3+LR4 graph is connected.

For n=7, reflection of the remaining 6 positions is odd (3 transpositions), so parity of a cycle's chosen orientation is not a well-defined invariant of an undirected cycle; do not generalize the n=9 parity statement without checking n mod 4. For odd n, parity is orientation-independent exactly when n=1 mod 4.

## Reproducible code
```python
from itertools import permutations
from collections import Counter
n=9
states=[(0,)+p for p in permutations(range(1,n)) if p[0]<p[-1]]
assert len(states)==20160
def canon(a):
    j=a.index(0)
    b=a[j:]+a[:j]
    return min(b,(b[0],)+b[:0:-1])
for q in (3,4):
    colors=tuple(i%q for i in range(n))
    allowed={s for s in states if all(colors[s[i]]!=colors[s[(i+1)%n]] for i in range(n))}
    adj={k:{s:set() for s in allowed} for k in (3,4)}
    for s in allowed:
        for k in (3,4):
            for i in range(n):
                b=list(s);ix=[(i+j)%n for j in range(k)]
                for a,v in zip(ix,[s[t] for t in ix][::-1]):b[a]=v
                t=canon(tuple(b))
                if t in allowed and t!=s:adj[k][s].add(t)
    def components(ks):
        seen=set();sizes=[]
        for s in allowed:
            if s in seen:continue
            todo=[s];seen.add(s);size=0
            while todo:
                u=todo.pop();size+=1
                for k in ks:
                    for v in adj[k][u]:
                        if v not in seen:seen.add(v);todo.append(v)
            sizes.append(size)
        return Counter(sizes)
    print(q,len(allowed),components((3,)),components((4,)),components((3,4)))
```

## Interpretation
Parity is an inherited combinatorial obstruction from the reversal generator, not a novel physical conservation law. Adding LR3 removes that parity obstruction, and exhaustive enumeration proves there is no further disconnection in these finite instances. This does not yet prove general connectivity for arbitrary n, colour multiplicities or admissibility rules.

## Next
Test n=10 or develop constructive LR3+LR4 connectivity proof with precise hypotheses. For n=9, distinguish this labelled-cycle parity invariant from colour-word winding, which applies to LR3 alone and need not survive LR4. Investigate whether the LR3+LR4 union destroys winding-sector barriers by explicit witness transitions.
