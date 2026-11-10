# EHF-CBB-CROSS-01 — Two-colour and three-colour LR3 comparison

Date: 2026-11-10. Status: analytic proposition and small exhaustive checks. This is a discrete mathematical comparison, not a gauge-theory identification.

## Common family
Take a proper cyclic q-colour word c_i in Z/qZ: c_i != c_(i+1). Define edge comparison d_i=c_(i+1)-c_i mod q, nonzero, with sum d_i=0 mod q. A starting colour and the d_i reconstruct the oriented word. LR3 reverses three consecutive positions (swaps c_i,c_(i+2)), provided properness survives.

## Exact threshold
For q=2, every proper cyclic word alternates, and c_i=c_(i+2). Thus every LR3 operation is colour-trivial. Proper odd cycles do not exist. For q=3, proper words can support nontrivial LR3: ABACA <-> ACABA is the exact five-position local pattern. This proves a genuine difference in *colour-pattern dynamics*, not a theorem about all labelled Hamiltonian cycles (same-colour endpoint swaps can still rearrange labels).

## q=3 transition alphabet
For q=3, nonzero differences are +1,-1, and a nontrivial LR3 corresponds to +--+ <-> -++-. For q=2 the only nonzero difference is 1, so no analogous colour-changing move exists. For q>=4 there are q-1 nonzero transition types; richer behaviour requires separate analysis.

## Reproducible unbalanced q-colour n=6 audit
Enumerate all q^6 words, retain proper cyclic words, and construct unique undirected colour-word LR3 edges for distinct words. Counts:
q=2: 2 proper linear words, 0 nontrivial LR3 edges.
q=3: 66 proper linear words, 36 nontrivial LR3 edges.
q=4: 732 proper linear words, 720 nontrivial LR3 edges.
These counts are for labelled positions with colour names fixed, not bracelets or balanced words. They provide a simple controlled comparison.

```python
from itertools import product
for q in (2,3,4):
    n=6
    words=[a for a in product(range(q),repeat=n)
           if all(a[i]!=a[(i+1)%n] for i in range(n))]
    edges=set()
    for a in words:
        for i in range(n):
            b=list(a);j=(i+2)%n
            b[i],b[j]=b[j],b[i]
            b=tuple(b)
            if b!=a and all(b[k]!=b[(k+1)%n] for k in range(n)):
                edges.add(tuple(sorted((a,b))))
    print(q,len(words),len(edges))
```

## Interpretation
The colour number q and the comparison alphabet size q-1 are distinct. The q=3 model has a two-symbol *edge relation* encoding but is not equivalent to the original binary vertex-colour model. This may provide a useful general EHF hierarchy. U(1), SU(2), SU(3) are continuous Lie groups and cannot be inferred from these finite colour systems. To investigate group-like structure, test actual composition, inverses, commutators, and representations of admissible move operators rather than matching colour counts to group names.

## Next
Compare q=2,3,4 under fixed n and a common admissibility rule; compute reachability and whether legal moves commute when disjoint or overlapping. Distinguish structural constraints from symmetry quotient artefacts.
