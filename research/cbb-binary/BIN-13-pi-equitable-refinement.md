# EHF-CBB-BIN-13 — Minimal equitable refinement of (Pi, colour bracelet) at n=9

Date: 2026-11-10. Status: exhaustive exact finite-state enumeration. The word “minimal” is relative to the prescribed initial partition, not among all conceivable state descriptors.

## Model
Nine labelled vertices, fixed marked colour labels R={0,1,2,3}, the other five unmarked. Undirected cycles canonicalized by placing 0 first and taking the lexicographically smaller orientation. MICRO means every vertex has a cyclic neighbour of its own colour. Pi: orient cycle starting at 0 toward its smaller-numbered neighbour, then collect labels at even positions. LR3 reverses three cyclically consecutive vertices. Legal edges preserve MICRO and the source Pi set.

There are 2880 MICRO-valid undirected labelled cycles, distributed over 50 Pi sets. Legal LR3 degrees: 1440 cycles of degree 2, 720 of degree 3, 720 of degree 4. Both cycles (0,1,2,3,4,5,6,7,8) and (0,1,4,5,6,7,8,3,2) have the same bracelet and Pi, yet respectively four and three legal LR3 neighbours.

## Exact equitable refinement
Partition the 2880 states initially by the pair (Pi set, binary colour bracelet). This produces 80 blocks, but is not equitable. For each state, count legal LR3 neighbours into every current block; split each block according to its resulting count vector. This is standard colour refinement / equitable partition refinement.

Result:
- Initial blocks: 80.
- After first refinement: 100.
- After second refinement: unchanged at 100 (stable).
- Final block sizes: 50 blocks of size 24, 30 blocks of size 48, 20 blocks of size 12.
- Per Pi set, final block counts: 20 Pi sets with one block, 10 with two blocks, 20 with three blocks.

Thus the **coarsest equitable refinement of the initial (Pi, bracelet) partition** has exactly 100 blocks, a 28.8-fold reduction from 2880 MICRO-valid cycles. Equitability means every state in a block has the same legal-move counts to each target block. The result is a mathematically exact quotient of the constrained LR3 adjacency graph, although the extra refinement class has so far been defined algorithmically rather than as a simple local label/seam invariant.

## Reproduction
```python
from itertools import permutations
from collections import Counter

n=9;R=set(range(4))
def canon(p):
    p=list(p);i=p.index(0);p=p[i:]+p[:i]
    return min(tuple(p),tuple([p[0]]+p[:0:-1]))
def pi(c):
    a=list(c);i=a.index(0);a=a[i:]+a[:i]
    if a[-1]<a[1]:a=[a[0]]+a[:0:-1]
    return frozenset(a[::2])
def micro(c):
    return all(any((c[j] in R)==(c[(j+d)%n] in R)
               for d in (-1,1)) for j in range(n))
def lr(c):
    out=set()
    for i in range(n):
        a=list(c);inds=[(i+j)%n for j in range(3)]
        v=[a[j] for j in inds][::-1]
        for j,z in zip(inds,v):a[j]=z
        out.add(canon(a))
    return out
def bracelet(c):
    w=tuple(int(v in R) for v in c);r=w[::-1]
    return min([w[i:]+w[:i] for i in range(n)]
              +[r[i:]+r[:i] for i in range(n)])
def ids(keys):
    d={};out=[]
    for k in keys:
        if k not in d:d[k]=len(d)
        out.append(d[k])
    return out

states=[(0,)+p for p in permutations(range(1,n)) if p[0]<p[-1]]
valid=[c for c in states if micro(c)]
idx={c:i for i,c in enumerate(valid)}
links=[[idx[d] for d in lr(c) if d in idx and pi(d)==pi(c)]
       for c in valid]
assert len(valid)==2880
blocks=ids([(tuple(sorted(pi(c))),bracelet(c)) for c in valid])
assert len(set(blocks))==80
while True:
    nxt=ids([(blocks[i],tuple(sorted(Counter(blocks[j] for j in ns).items())))
             for i,ns in enumerate(links)])
    if len(set(nxt))==len(set(blocks)):break
    blocks=nxt
assert len(set(blocks))==100
assert Counter(Counter(blocks).values())==Counter({24:50,48:30,12:20})
```

## Markov protocols
For a reject-and-stay protocol with nine uniformly proposed LR3 positions, add 9-degree(state) self loops to the quotient diagonal. Since degree is constant in every equitable block, this is well defined. For uniform choice among legal LR3 moves, divide the quotient row by its legal degree (also block-constant). These are distinct chains with distinct stationary measures.

## Limits / next
This is the smallest equitable partition **refining the specified 80 initial blocks**, not a proof of the smallest possible physically meaningful descriptor. Find an explicit structural invariant explaining the extra 20 splits, likely related to the anchored label ordering and Pi seam. Test the construction at n=7,11, and compare mixing for the two proposal protocols. No physical claim follows.
