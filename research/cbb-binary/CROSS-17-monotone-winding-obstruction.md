# EHF-CBB-CROSS-17 — Obstruction to monotone winding normalization

Date: 2026-11-10. Status: executed exhaustive small-state audit and explicit witness; general LR3+LR4 connectivity still open.

## Question
Can every balanced proper three-colour position-indexed cyclic word of length n=3m reach maximum winding W=m by a path of legal LR3 and LR4 reversals along which W never decreases?

## Definitions
Each of A,B,C occurs m times. Adjacent colours differ, including across the cyclic boundary. W=(number of forward ABC transitions minus reverse transitions)/3. LR3 preserves signed W, LR4 changes it by exactly +/-2. Max winding states are the three phase rotations of (ABC)^m.

## Negative answer, already at n=9
Start s=ABABCACBC, W=1. Exhaustive exploration of its LR3-only component finds no state with a legal LR4 move increasing W to 3. Therefore every path from s to any W=3 state must first decrease winding to -1.

An explicit shortest path using only LR4 moves is:
1. ABABCACBC, W=+1
2. ACBABACBC, W=-1 (LR4 start index 1)
3. ABCABACBC, W=+1 (LR4 start index 0)
4. ABCABCABC, W=+3 (LR4 start index 4)

All words are balanced and proper. This is a three-move witness showing that a winding decrease may be necessary even though the full graph is connected.

## Audit counts
For each m=2..6, enumerate all balanced proper position-indexed words. Count nonmaximal states with no direct LR4 increase; separately partition by LR3 components and count nonmaximal LR3 components with no LR4-increasing exit:

| n | words | no direct LR4 increase | LR3 components | LR3 components with no increasing LR4 exit |
| 6 | 24 | 0 | 24 | 0 |
| 9 | 132 | 36 | 78 | 9 |
| 12 | 804 | 120 | 342 | 48 |
| 15 | 5196 | 720 | 1656 | 150 |
| 18 | 34872 | 3654 | 8610 | 531 |

The component counts use *position-indexed colour words*, not rotation/reversal quotients and not labelled-vertex cycles. The last column counts components strictly below maximum winding; maximum-winding components are excluded by design.

## Reproducible Python
```python
from collections import Counter
for m in range(2,7):
    n=3*m;words=[]
    def rec(w,c):
        if len(w)==n:
            if w[-1]!=w[0]:words.append(tuple(w))
            return
        for x in range(3):
            if c[x]<m and (not w or w[-1]!=x):
                c[x]+=1;w.append(x);rec(w,c);w.pop();c[x]-=1
    rec([],[0]*3)
    S=set(words)
    def W(w):
        return sum(1 if (w[(i+1)%n]-w[i])%3==1 else -1 for i in range(n))//3
    def neighbors(w,k):
        for i in range(n):
            ix=[(i+j)%n for j in range(k)]
            v=list(w)
            for a,b in zip(ix,reversed([w[t] for t in ix])):v[a]=b
            v=tuple(v)
            if v!=w and v in S:yield v
    no_direct={w for w in words if W(w)<m and not any(W(v)>W(w) for v in neighbors(w,4))}
    seen=set();traps=0;numcomps=0
    for w in words:
        if w in seen:continue
        numcomps+=1;stack=[w];seen.add(w);up=False
        while stack:
            u=stack.pop()
            if W(u)<m and any(W(v)>W(u) for v in neighbors(u,4)):up=True
            for v in neighbors(u,3):
                if v not in seen:seen.add(v);stack.append(v)
        if W(w)<m and not up:traps+=1
    print(n,len(words),len(no_direct),numcomps,traps)
```

## Interpretation
A proof of general LR3+LR4 connectivity cannot rely solely on monotonically increasing W, even when arbitrarily many LR3 moves at constant W are allowed. Temporary decreases are necessary in some instances. This is an obstruction to a *proof strategy*, not a counterexample to the connectivity conjecture.

## Next
Find a global normalization potential incorporating local defects and winding, or establish a bounded detour lemma allowing W decreases followed by a net gain. Test a canonical block-reduction strategy and distinguish genuine sector invariants from artificial local minima. No 1:2:3 law is implied by these counts.
