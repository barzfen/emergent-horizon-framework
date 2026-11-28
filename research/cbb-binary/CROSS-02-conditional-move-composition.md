# EHF-CBB-CROSS-02 — Composition and noncommutativity of conditional LR3 moves

Date: 2026-11-10. Status: exhaustive six-position comparison for q=2,3,4; no continuous-group identification.

## Definition
A state is a proper cyclic word c of length n=6 over q named colours: c_i != c_(i+1) for every cyclic i. T_i swaps entries i and i+2 (indices modulo 6) only when this changes the colour word and leaves it proper. T_i is a partial operation, not an everywhere-defined group action.

For every starting state s and unordered pair i<j, retain the pair if both T_i(s),T_j(s) exist. Then test both compositions T_j(T_i(s)) and T_i(T_j(s)), classifying whether both exist and agree, both exist and disagree, only one exists, or neither exists.

## Exhaustive results
| q | proper states | undirected nontrivial edges | initially legal move pairs | both legal same | both legal different | neither legal | only one legal |
| 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| 3 | 66 | 36 | 36 | 0 | 0 | 36 | 0 |
| 4 | 732 | 720 | 1584 | 864 | 144 | 576 | 0 |

The q=4 result proves there exist pairs of admissible transformations whose order changes the outcome.

## Explicit witness
At q=4, s=(0,1,0,2,0,3), use T_1 and T_3 (zero-based positions). Both initial moves are legal:
T_1(s)=(0,2,0,1,0,3)
T_3(s)=(0,1,0,3,0,2)
Both second moves are also legal, but:
T_3(T_1(s))=(0,2,0,3,0,1)
T_1(T_3(s))=(0,3,0,1,0,2).
These are different, and all intermediate states satisfy cyclic separation.

## Reproducible code
```python
from itertools import product
for q in (2,3,4):
    n=6
    states={a for a in product(range(q),repeat=n)
            if all(a[i]!=a[(i+1)%n] for i in range(n))}
    def move(a,i):
        b=list(a);j=(i+2)%n
        b[i],b[j]=b[j],b[i]
        b=tuple(b)
        return b if b in states and b!=a else None
    edges=set()
    counts={'same':0,'different':0,'neither':0,'one':0}
    forks=0
    for a in states:
        for i in range(n):
            b=move(a,i)
            if b is not None:edges.add(tuple(sorted((a,b))))
        for i in range(n):
            for j in range(i+1,n):
                b=move(a,i);c=move(a,j)
                if b is None or c is None:continue
                forks+=1
                d=move(b,j);e=move(c,i)
                if d is not None and e is not None:
                    counts['same' if d==e else 'different']+=1
                elif d is None and e is None:
                    counts['neither']+=1
                else:counts['one']+=1
    print(q,len(states),len(edges),forks,counts)
```

## Interpretation and caveats
These operations are conditional partial permutations of proper words, not a Lie group. On the unrestricted full word space, swaps of overlapping positions can fail to commute; the novelty here is verifying both orders remain within the admissible state space. A difference between q=3 and q=4 for n=6 is not yet a general threshold theorem across all lengths or admissibility choices. The current q=3 result means no pair of initially legal distinct moves has two legal completions in this particular finite experiment, not that all q=3 transformations commute in a global algebra.

## Next
Check n=8,9,12 for q=3 and q=4 with computationally efficient enumeration, and derive the local necessary/sufficient condition for an admissible noncommuting pair. Investigate partial-action structures (inverse semigroups or groupoids) only after verifying the relevant closure and composition definitions.
