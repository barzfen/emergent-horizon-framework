# EHF-CBB-CROSS-09 — General LRk winding-change identity

Date: 2026-11-10. Analytic identity and exact n=9 balanced enumeration.

## Model
Proper cyclic three-colour word w, colours A,B,C in oriented cyclic order. Define sigma(x,y)=+1 for A->B, B->C, C->A and -1 for opposite (only for distinct colours). W(w)=1/3 sum over cyclic edges sigma. For undirected bracelets, only |W| is well-defined, but calculations use oriented representatives.

## Exact identity
Consider a contiguous k-vertex segment with immediate outside neighbours:
L,a_1,a_2,...,a_k,R.
Let S=sum_{j=1}^{k-1} sigma(a_j,a_{j+1}). Reversing a_1,...,a_k reverses every internal oriented edge, changing its contribution from S to -S, and replaces boundary edges L->a_1 and a_k->R by L->a_k and a_1->R. Hence, whenever the reversal remains proper,
3 Delta W = sigma(L,a_k)+sigma(a_1,R)-sigma(L,a_1)-sigma(a_k,R)-2 S.
This holds for any k for which the two outside neighbours are distinct positions; in a cyclic word take 2<=k<=n-2. Closure ensures Delta W is an integer.

## Exact n=9 audit
Enumerate all 132 balanced proper linear words (three each A,B,C). For every word and cyclic start index, reverse k consecutive positions, retain proper nonidentity results. Directed move-instance distributions by signed Delta W:

k=2: DeltaW -2:216, +2:216; total 432
k=3: DeltaW 0:108; total 108
k=4: DeltaW -2:324, +2:324; total 648
k=5: DeltaW -4:54, 0:324, +4:54; total 432
k=6: DeltaW -2:270, +2:270; total 540
k=7: DeltaW -4:54, 0:216, +4:54; total 324.

These are directed instances, not unique edges or quotient transitions. In particular LR3 conserves signed W, LR4 changes signed W by +/-2 on all 648 nonidentity proper instances, but only 108 of these change |W| (CROSS-08). LR5 and LR7 sometimes conserve W and sometimes change it by +/-4.

## Reproduction
```python
from itertools import combinations
from collections import Counter
n=9
words=[]
for aa in combinations(range(n),3):
    rem=[i for i in range(n) if i not in aa]
    for bb in combinations(rem,3):
        w=[2]*n
        for i in aa:w[i]=0
        for i in bb:w[i]=1
        if all(w[i]!=w[(i+1)%n] for i in range(n)):
            words.append(tuple(w))
def W(w):
    n=len(w)
    return sum(1 if (w[(i+1)%n]-w[i])%3==1 else -1 for i in range(n))//3
for k in range(2,8):
    c=Counter()
    for w in words:
        for i in range(n):
            ix=[(i+j)%n for j in range(k)]
            v=list(w)
            for j,t in zip(ix,[w[x] for x in ix][::-1]):v[j]=t
            if tuple(v)==w or any(v[t]==v[(t+1)%n] for t in range(n)):continue
            c[W(v)-W(w)]+=1
    print(k,dict(sorted(c.items())))
```

## Interpretation
The local formula is a general theorem for this three-colour winding observable and properness rule. It shows precisely how internal comparison reversal and boundary reconnection compete. Finite n=9 distributions are examples, not universal probabilities. No evidence for a universal 1:2:3 law follows from these counts. Next test whether the observed congruence classes of DeltaW versus reversal-length parity admit a general proof, and whether there is a structural conservation law for combinations of LRk.
