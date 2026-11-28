# EHF-CBB-CROSS-11 — Winding-transition graphs for LR4

Date: 2026-11-10. Status: exhaustive balanced cyclic-word enumerations n=9,12,15, plus a finite-local-pattern proof for LR4 increments.

## Model
Oriented cyclic words with three fixed colour names A,B,C, n=3m, exactly m occurrences each and unequal adjacent colours. W=(N+-N-)/3, where forward edges are A->B, B->C, C->A. LR4 reverses four consecutive cyclic positions, retaining only proper, nonidentity results. Winding-transition graph has one vertex per attainable signed W, an undirected edge if at least one admissible LR4 move connects those values. Counts below are *directed position-indexed move instances*, not unique quotient edges.

## Executed exact results
n=9: 132 words; winding multiplicities {-3:3,-1:63,1:63,3:3}; LR4 directed counts:
-3 -> -1:27; -1 -> -3:27; -1 -> 1:270; 1 -> -1:270; 1 -> 3:27; 3 -> 1:27.
The winding graph is the path -3 -- -1 -- 1 -- 3.

n=12: 804 words; winding multiplicities {-4:3,-2:156,0:486,2:156,4:3}; directed LR4 counts:
-4 -> -2:36; -2 -> -4:36; -2 -> 0:1260; 0 -> -2:1260; 0 -> 2:1260; 2 -> 0:1260; 2 -> 4:36; 4 -> 2:36.
Graph is path -4 -- -2 -- 0 -- 2 -- 4.

n=15: 5196 words; winding multiplicities {-5:3,-3:315,-1:2280,1:2280,3:315,5:3}; directed LR4 counts:
-5 -> -3:45; -3 -> -5:45; -3 -> -1:3690; -1 -> -3:3690; -1 -> 1:12690; 1 -> -1:12690; 1 -> 3:3690; 3 -> 1:3690; 3 -> 5:45; 5 -> 3:45.
Graph is path -5 -- -3 -- -1 -- 1 -- 3 -- 5.

## General LR4 local increment theorem
For any proper three-colour cyclic word, every admissible LR4 reversal has signed DeltaW = +2 or -2. The proof reduces to a finite local six-colour pattern audit: write L,a,b,c,d,R, with all five adjacent pairs unequal before reversal and L != d and a != R after. There are exactly 42 possible six-letter patterns with labelled colours; 21 give DeltaW=+2 and 21 give DeltaW=-2. In particular DeltaW=0 is impossible for LR4 (including moves that happen to be the identity on a colour word: none of the 42 locally legal patterns can yield identity on the four-letter segment). This finite local exhaustion is a rigorous computer-checkable proof, with tiny self-contained code below. A symbolic proof without finite enumeration remains desirable.

## Code to reproduce local theorem
```python
from itertools import product
from collections import Counter
c=Counter()
for w in product(range(3),repeat=6):
    if any(w[i]==w[i+1] for i in range(5)): continue
    v=(w[0],)+tuple(reversed(w[1:5]))+(w[5],)
    if v[0]==v[1] or v[4]==v[5]: continue
    def s(a,b): return 1 if (b-a)%3==1 else -1
    numer=sum(s(v[i],v[i+1])-s(w[i],w[i+1]) for i in range(5))
    assert numer%3==0
    c[numer//3]+=1
assert c==Counter({-2:21,2:21})
print(c)
```

## Code to reproduce n=9,12,15
```python
from collections import Counter,defaultdict
for n in (9,12,15):
    words=[];m=n//3
    def rec(w,c):
        if len(w)==n:
            if w[-1]!=w[0]: words.append(tuple(w))
            return
        for x in range(3):
            if c[x]<m and (not w or w[-1]!=x):
                c[x]+=1;w.append(x);rec(w,c);w.pop();c[x]-=1
    rec([],[0]*3)
    def W(w):
        return sum(1 if (w[(i+1)%n]-w[i])%3==1 else -1 for i in range(n))//3
    dist=Counter(map(W,words));trans=Counter()
    for w in words:
        a=W(w)
        for i in range(n):
            ix=[(i+j)%n for j in range(4)]
            v=list(w)
            for t,z in zip(ix,reversed([w[t] for t in ix])):v[t]=z
            if tuple(v)==w or v[(i-1)%n]==v[i] or v[(i+3)%n]==v[(i+4)%n]:continue
            trans[(a,W(v))]+=1
    assert all(abs(b-a)==2 for a,b in trans)
    print(n,len(words),sorted(dist.items()),sorted(trans.items()))
```

## Interpretation and limitations
The path-shaped winding graph is established by exhaustive tests at n=9,12,15, not yet for all balanced lengths. The general LR4 increment restriction DeltaW=+/-2 follows from a local proof independent of n. The winding-level quotient graph being connected does not imply the full LR4 configuration graph is connected: for n=9, CROSS-07 found two LR4 components on labelled cycles, explained by permutation parity. LR3 conserves W but may bridge other sector distinctions; combining LR3+LR4 connected labelled n=9 examples.

No established relation to the EHF collinear 1:2:3 amplitude ratio. Next: prove a general path theorem for balanced 3-colour words and characterize residual connectivity obstructions.
