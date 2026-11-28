# EHF-CBB-TRI-09 — Greedy normal-form obstruction

Date: 2026-11-10. Exact finite counterexample, not a general classification theorem.

## Model
Use balanced proper three-colour cyclic words of length 15 (five each A,B,C). Encode directed adjacent colour differences by signs + and -. The only nontrivial colour-changing LR3 rewrite is `+--+ <-> -++-`. Identify sign words under cyclic rotation and reverse-complement, and retain sign words reconstructing balanced colour words. There are 60 sign bracelets and 20 connected components.

## Tested normal form
Represent each sign bracelet by its lexicographically least rotation or reverse-complement rotation, using Python string order ('+' precedes '-'). Orient every nontrivial rewrite edge from the lexicographically greater canonical representative toward the lesser. Call a state a local minimum if it has no strictly smaller neighbour.

Exhaustive computation gives:
- 13 connected components with one local minimum;
- 5 connected components with two local minima;
- 2 connected components with three local minima.

The largest component has 11 sign bracelets and three local minima:
`++++--+-+++-+--`,
`+++--+++--+++--`,
`+++-+-+++-+--+-`.

Thus naive strictly decreasing rewriting is **not confluent** under this ordering: distinct local minima in the same undirected connected component cannot reach each other by strictly decreasing steps. This refutes this particular greedy normal-form proposal, **not** the existence of some other structural normal form.

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
        if ''.join(s[(i+j)%n] for j in range(4)) not in ('+--+','-++-'):
            continue
        v=list(s)
        for j in range(4):
            k=(i+j)%n
            v[k]='+' if v[k]=='-' else '-'
        q=canon(''.join(v))
        if q in ids:adj[a].add(ids[q])
seen=set();components=[]
for a in range(len(states)):
    if a in seen:continue
    todo=[a];seen.add(a);comp=[]
    while todo:
        u=todo.pop();comp.append(u)
        for v in adj[u]:
            if v not in seen:seen.add(v);todo.append(v)
    components.append(comp)
assert len(states)==60 and len(components)==20
mins=lambda comp:[i for i in comp if all(states[j]>=states[i] for j in adj[i])]
assert Counter(len(mins(c)) for c in components)==Counter({1:13,2:5,3:2})
assert len(mins(max(components,key=len)))==3
```

## Next
Seek a structural invariant of the sign-domain-wall ordering or a completed rewrite orientation; validate any candidate on every legal edge and against the multiple mobile components of equal winding. Component minimum found by exhaustive traversal is an algorithmic canonical label, not an explanatory theorem. No QCD claim.
