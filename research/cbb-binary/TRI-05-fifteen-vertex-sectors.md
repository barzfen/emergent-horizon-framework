# EHF-CBB-TRI-05 — Balanced three-colour separation sectors at n=15

Date: 2026-11-10. Status: executed exhaustive colour-word and dihedral-bracelet enumeration.

## Model
Fifteen cyclic positions, exactly five A, five B and five C. Neighbours must have different colours. LR3 swaps positions i and i+2 if the result remains proper. Colour names are fixed; rotations and reflections are quotiented.

## Results
5196 valid linear words, 174 bracelets, 56 connected components in the bracelet LR3 graph.

Component-size multiplicities:
- size 1: 28 components
- size 2: 3 components
- size 3: 9 components
- size 5: 12 components
- size 8: 3 components
- size 29: 1 component
Sum: 28+6+27+60+24+29=174.

Winding absolute value |W| = |sum cyclic +/-1 colour steps|/3:
- |W|=1: 152 bracelets
- |W|=3: 21 bracelets
- |W|=5: 1 bracelet.

Components by (|W|, size):
(1,1):21; (1,3):6; (1,5):12; (1,8):3; (1,29):1;
(3,1):6; (3,2):3; (3,3):3;
(5,1):1.

Legal colour-changing LR3 move count distribution across canonical bracelet representatives: 0:28, 1:54, 2:54, 3:32, 5:6. All 28 singleton components have zero colour-changing legal moves. There are 28 mobile components (size>1). Many mobile components share |W|=1, proving that winding plus merely frozen/non-frozen status does not classify sectors.

One representative of the unique 29-class component: ABABABCACACBCBC; its |W|=1. All component-size statistics refer to colour-bracelet quotient, not individually labelled cycles.

## Reproduction
```python
from itertools import combinations
from collections import Counter
n=15;m=5
words=[]
for aa in combinations(range(n),m):
    aset=set(aa); rem=[i for i in range(n) if i not in aset]
    for bb in combinations(rem,m):
        w=['C']*n
        for i in aa:w[i]='A'
        for i in bb:w[i]='B'
        if all(w[i]!=w[(i+1)%n] for i in range(n)):
            words.append(''.join(w))
def canon(w):
    return min(v[i:]+v[:i] for v in (w,w[::-1]) for i in range(n))
classes=sorted(set(map(canon,words)))
idx={w:i for i,w in enumerate(classes)}
adj=[set() for _ in classes]
legal=[]
for a,w in enumerate(classes):
    count=0
    for i in range(n):
        j=(i+2)%n
        if w[i]==w[j]:continue
        v=list(w);v[i],v[j]=v[j],v[i]
        if all(v[k]!=v[(k+1)%n] for k in range(n)):
            count+=1
            adj[a].add(idx[canon(''.join(v))])
    legal.append(count)
seen=set();sizes=[]
for i in range(len(classes)):
    if i in seen:continue
    todo=[i];seen.add(i);size=0
    while todo:
        u=todo.pop();size+=1
        for v in adj[u]:
            if v not in seen:seen.add(v);todo.append(v)
    sizes.append(size)
assert len(words)==5196
assert len(classes)==174
assert Counter(sizes)==Counter({1:28,2:3,3:9,5:12,8:3,29:1})
assert Counter(legal)==Counter({0:28,1:54,2:54,3:32,5:6})
```

## Interpretation and next
At n=15 the largest mobile bracelet component has 29 classes, versus 4 at n=9 and 3 at n=12. This is not a proof of a phase transition or a physical analogy. The existence of 28 mobile components with shared winding values indicates additional sector structure beyond winding and local arrest. Next: test whether ordered arrangements of local defects or conserved pairwise colour-order data distinguish these components, and examine how component sizes evolve at n=18 with efficient dynamic enumeration.
