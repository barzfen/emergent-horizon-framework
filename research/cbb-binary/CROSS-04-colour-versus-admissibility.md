# EHF-CBB-CROSS-04 — Distinguishability versus admissibility in labelled Hamiltonian cycles

Date: 2026-11-10. Status: exact n=6 and n=7 enumerations, with n=9 comparison to TRI-02.

## Protocol
Use labelled undirected Hamiltonian cycles on fixed vertex set {0,...,n-1}, represented modulo rotation and reversal. LR3 swaps the entries at cyclic positions i and i+2. Vertex colours are fixed attributes of vertex labels, not reassignable word symbols. Compare:
(1) raw cycles;
(2) colour assigned but no separation filter;
(3) colour assigned and cyclic neighbours required to differ.
When restricted, the LR3 graph is the induced subgraph of the raw graph on proper cycles; no additional non-LR3 moves are allowed.

## n=6 exact results
Raw: 60 cycles; 10 LR3 components, each of size 6.
One colour, no separation: same 60 cycles and 10 components.
One colour, separation: zero states.
Two colours with label assignment (0,1,0,1,0,1): 6 proper cycles, 1 component of size 6.
Three colours with assignment (0,0,1,1,2,2): 16 proper cycles, 10 components: six components of size 2 and four singleton components.
Four colours with assignment (0,1,2,3,0,1): 24 proper cycles, 10 components: two components of size 6, four of size 2, four singleton components.
In this n=6 sample, each surviving restricted component is contained in a distinct raw parity sector: none of the raw LR3 sectors is further disconnected by the separation filter. Counts depend on colour multiplicities and n, not merely q.

## n=7 check
Raw: 360 undirected labelled cycles, one component.
Three colours assigned (0,0,0,1,1,2,2): 48 proper cycles, one component.
Four colours assigned (0,0,1,1,2,2,3): 120 proper cycles, one component.
Thus a properness constraint need not fragment the raw odd-length component at every size.

## Contrast n=9
TRI-02 previously found 1584 proper labelled Hamiltonian cycles for three colour classes of size 3 each, with 235 LR3 connected components (72 singletons, 162 components of size 4, one component of size 864). Since n=9 is odd, unrestricted raw LR3 is connected. Therefore the n=9 fragmentation is induced by the separation admissibility filter, not inherited from raw parity sectors.

## Proof-level distinctions
- Assigning colours without imposing a rule changes observation/metadata, not the raw state graph or its LR3 connectivity.
- Imposing separation deletes states and all incident edges; the remaining graph is induced and cannot connect different raw components, but it can delete raw components or split one into many.
- q=1 with separation has no proper cycles for n>=3. q=1 without separation is equivalent to raw cycles.
- Colour-word bracelet quotients can identify distinct labelled cycles, so their connectivity counts must never be substituted for labelled-cycle counts.

## Reproducible n=6 code
```python
from itertools import permutations
from collections import Counter
n=6
states={(0,)+p for p in permutations(range(1,n)) if p[0]<p[-1]}
def canon(a):
    j=a.index(0);b=a[j:]+a[:j]
    return min(b,(b[0],)+b[:0:-1])
adj={s:set() for s in states}
for s in states:
    for i in range(n):
        b=list(s);b[i],b[(i+2)%n]=b[(i+2)%n],b[i]
        adj[s].add(canon(tuple(b)))
def components(allowed):
    allowed=set(allowed);seen=set();sizes=[]
    for s in allowed:
        if s in seen:continue
        stack=[s];seen.add(s);size=0
        while stack:
            u=stack.pop();size+=1
            for v in adj[u]&allowed:
                if v not in seen:seen.add(v);stack.append(v)
        sizes.append(size)
    return Counter(sizes)
print('raw',len(states),components(states))
for colors in ((0,0,0,0,0,0),(0,1,0,1,0,1),
               (0,0,1,1,2,2),(0,1,2,3,0,1)):
    allowed=[s for s in states if all(colors[s[i]]!=colors[s[(i+1)%n]]
                                     for i in range(n))]
    print(colors,len(allowed),components(allowed))
```

## Interpretation and next
The hierarchy is not a monotone increase of reachable configurations with colour count, especially when multiplicities differ. Distinguish the 'colour observation' layer from 'admissibility restriction' layer. Next examine a controlled sequence of refinements of one fixed vertex partition, keeping n and the underlying labelled graph fixed, and determine when refining colours relaxes separation and merges or expands sectors. In the proper-colouring model, splitting one colour class into distinct classes can only add admissible cycles; the restricted graphs are nested. This nesting gives a possible exact monotonicity theorem, unlike comparing arbitrary assignments with different multiplicities. No U(1)/SU(q) identification is claimed.
