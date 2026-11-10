# EHF-CBB-TRI-08 — Sign-run audit and unresolved sector classification

Date: 2026-11-10. Status: independently executed n=15 sign-graph enumeration; negative test, no claimed complete invariant.

## Model
Proper cyclic balanced three-colour words with n=15, five occurrences of each colour. Encode oriented edges by + for A->B->C->A and - for the reverse. A colour-changing LR3 induces +--+ <-> -++- on four consecutive signs. Sign bracelets identify rotations and reverse-complement, not ordinary reflection. Only sign words reconstructing balanced colour cycles are retained.

## Computation
Enumerate all proper balanced colour words (5196), map to canonical sign bracelets (60), and connect them by the exact four-symbol rewrite when the destination is in the admissible balanced set. The graph has 20 connected components:
size 1: 10 components
size 2: 1
size 3: 3
size 5: 4
size 8: 1
size 11: 1.
This independently reproduces TRI-07.

By absolute winding and component size:
|W|=1: seven singletons, two 3-class, four 5-class, one 8-class, one 11-class.
|W|=3: two singletons, one 2-class, one 3-class.
|W|=5: one singleton.
Thus mobile components share winding.

## Negative result: sign-run count is not conserved
Define R(s)=sum_i 1{s_i != s_(i+1)}, cyclically. Evaluate every legal sign-rewrite edge: some edges change R. Hence neither R nor the number of equal-sign adjacent pairs (n-R) is a sector invariant. This rules out the simplest run-count classification. The ordered run-length sequence may still contain useful information, but it cannot be presumed invariant.

## Reproduction
```python
from itertools import combinations
from collections import Counter
n=15;m=5
words=[]
for aa in combinations(range(n),m):
    rem=[i for i in range(n) if i not in aa]
    for bb in combinations(rem,m):
        w=['C']*n
        for i in aa:w[i]='A'
        for i in bb:w[i]='B'
        if all(w[i]!=w[(i+1)%n] for i in range(n)):
            words.append(''.join(w))
def signs(w):
    return ''.join('+' if ('ABC'.index(w[(i+1)%n])-'ABC'.index(w[i]))%3==1 else '-' for i in range(n))
def canon(s):
    t=s[::-1].translate(str.maketrans('+-','-+'))
    return min(v[i:]+v[:i] for v in (s,t) for i in range(n))
states=sorted({canon(signs(w)) for w in words})
ids={s:i for i,s in enumerate(states)}
adj=[set() for _ in states]
for a,s in enumerate(states):
    for i in range(n):
        if ''.join(s[(i+j)%n] for j in range(4)) not in ('+--+','-++-'):continue
        v=list(s)
        for j in range(4):
            k=(i+j)%n;v[k]='+' if v[k]=='-' else '-'
        q=canon(''.join(v))
        if q in ids:adj[a].add(ids[q])
seen=set();comps=[]
for a in range(len(states)):
    if a in seen:continue
    todo=[a];seen.add(a);comp=[]
    while todo:
        u=todo.pop();comp.append(u)
        for v in adj[u]:
            if v not in seen:seen.add(v);todo.append(v)
    comps.append(comp)
assert len(states)==60
assert Counter(map(len,comps))==Counter({1:10,2:1,3:3,5:4,8:1,11:1})
def runs(s):return sum(s[i]!=s[(i+1)%n] for i in range(n))
assert any(runs(states[a])!=runs(states[b]) for a,ns in enumerate(adj) for b in ns)
```

## Next
Seek a higher-order invariant or constructive normal form for the rewrite. Separate properties of a sign state from properties of its full connected component; avoid defining a supposed invariant solely by assigning a component ID. Also verify whether fixed balanced counts impose additional global constraints on the sign-rewrite system. No connection to physical QCD is established.
