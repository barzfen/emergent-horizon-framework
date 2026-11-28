# EHF-CBB-CROSS-05 — Colour count versus reversal length

Date: 2026-11-10. Status: exhaustive labelled-cycle audits for n=6,7,8.

## Definitions
Hamiltonian cycles on n distinct labelled vertices, modulo cyclic rotation and reversal. Vertex colours are fixed attributes of labels. Properness means neighbouring colours differ. LRk reverses k consecutive cyclic entries; only a move to a different undirected labelled cycle satisfying properness is counted. All LR2, LR3, LR4, LR5 are tested separately. The raw case has no properness filter.

## Eight-vertex results
Colour assignment is c(v)=v mod q, with q=2,3,4, giving respective multiplicities (4,4), (3,3,2), (2,2,2,2).

| q | admissible states | LR2 components | LR3 components | LR4 components | LR5 components | combined LR2-5 components |
| raw | 2520 | 1 | 35 | 1 | 35 | 1 |
| 2 | 72 | 72 | 1 | 72 | 1 | 1 |
| 3 | 252 | 6 | 35 | 4 | 35 | 1 |
| 4 | 744 | 1 | 75 | 121 | 75 | 1 |

## Six-vertex results
| q | admissible states | LR2 components | LR3 components | LR4 components | LR5 components |
| raw | 60 | 1 | 10 | 1 | 60 |
| 2 | 6 | 6 | 1 | 6 | 6 |
| 3 | 16 | 1 | 10 | 1 | 16 |
| 4 | 24 | 1 | 10 | 1 | 24 |

At n=6 LR5 reverses all but one vertex, equivalent to global reflection of the cycle and hence is a trivial move.

## Seven-vertex results
| q | admissible states | LR2 components | LR3 components | LR4 components | LR5 components |
| raw | 360 | 1 | 1 | 1 | 1 |
| 3 (3,2,2) | 48 | 2 | 1 | 1 | 2 |
| 4 (2,2,2,1) | 120 | 1 | 1 | 1 | 1 |

There are no proper cyclic two-colour states for odd n.

## Boundary test for LRk
For proper word with local window L,a1,...,ak,R, reversing the segment preserves internal undirected adjacency, so admissibility is equivalent to L != ak and a1 != R. This holds for all k, with cyclic indexing.

## Exact consequences
1. Assigning colour labels without constraints leaves the raw LRk graph unchanged.
2. Under strict two-colour separation and even n, every proper cycle alternates. Odd-length reversal LR(2r+1) preserves the colour pattern, while even-length reversal LR(2r) breaks separation. This does not imply odd-length reversal is identity on labelled cycles.
3. A reversal length does not have a monotone relationship to connectivity: n=8, q=4 has 75 LR3 components and 121 LR4 components, while LR2 is connected.
4. Combining move lengths can connect states that individual move sets do not: n=8 q=3 has LR2 6 components, LR3 35, LR4 4, LR5 35, but union LR2-5 connected. The union includes LR2 and should not be interpreted as proof that LR3+LR4 alone suffices.

## Reproducible Python
```python
from itertools import permutations
def audit(n,colors):
    states={(0,)+p for p in permutations(range(1,n)) if p[0]<p[-1]}
    def canon(a):
        j=a.index(0);b=a[j:]+a[:j]
        return min(b,(b[0],)+b[:0:-1])
    allowed={s for s in states if colors is None or all(
        colors[s[i]]!=colors[s[(i+1)%n]] for i in range(n))}
    adj={k:{s:set() for s in allowed} for k in [2,3,4,5,'all']}
    for s in allowed:
        for k in [2,3,4,5]:
            if k>=n:continue
            for i in range(n):
                b=list(s);ix=[(i+j)%n for j in range(k)]
                for a,v in zip(ix,[s[t] for t in ix][::-1]):b[a]=v
                t=canon(tuple(b))
                if t in allowed and t!=s:
                    adj[k][s].add(t);adj['all'][s].add(t)
    def comp(g):
        seen=set();sizes=[]
        for s in allowed:
            if s in seen:continue
            todo=[s];seen.add(s);z=0
            while todo:
                u=todo.pop();z+=1
                for v in g[u]:
                    if v not in seen:seen.add(v);todo.append(v)
            sizes.append(z)
        return len(sizes)
    return len(allowed),{k:comp(g) for k,g in adj.items()}
for n in (6,7,8):
    for q in (None,2,3,4):
        colours=None if q is None else tuple(i%q for i in range(n))
        print(n,q,audit(n,colours))
```

## Next
Separate the effect of (i) adding an LRk generator and (ii) splitting colour classes under a fixed underlying labelled vertex set. Investigate LR3+LR4 *without* LR2 to see whether the two moves jointly recover connectivity. Then seek general structural criteria for connectivity, beyond finite n=8. None of these discrete results establishes a U(1), SU(2), SU(3) correspondence.
