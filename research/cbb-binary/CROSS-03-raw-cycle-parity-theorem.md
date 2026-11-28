# EHF-CBB-CROSS-03 — Raw Hamiltonian cycles as the colour-neutral baseline

Date: 2026-11-10. Status: analytic classification with exact exhaustive checks n=4,...,8.

## Clarifying q=0 and q=1
The uncoloured model is the set of undirected Hamiltonian cycles on n distinctly labelled vertices. A constant one-colour assignment is mathematically equivalent to this model **only if colour does not impose a separation constraint**. Under proper-colouring separation c_i != c_(i+1), q=1 has no states (for n>=3). A 'zero-colour' description means colour is absent, not a proper q=0 colouring.

## LR3
Write a labelled cycle as a cyclic sequence (v_0,...,v_(n-1)), modulo rotation and reversal. An LR3 move reverses three consecutive entries, equivalently swaps v_i and v_(i+2) with indices modulo n. No additional admissibility filter applies in the raw baseline.

## Theorem: exact raw-cycle LR3 connectivity
For n>=3:
- If n is odd, all undirected labelled Hamiltonian cycles lie in one LR3 connected component.
- If n=2m is even (m>=2), the LR3 components are indexed exactly by the unordered bipartition {E,O} of vertex labels into the m labels at even cyclic positions and the m at odd cyclic positions. The number of components is (1/2) * binomial(2m,m). Each component contains (m!)^2/(2m) = (m!)^2/n undirected labelled cycles.

Proof: Consider the graph on n positions with edges {i,i+2} mod n. Each LR3 swaps the labels at the endpoints of one such edge. Transpositions along the edges of a connected graph generate the full symmetric group on its vertices. For odd n, the step-two position graph is connected, hence all linear cyclic orders are mutually reachable, so also all undirected Hamiltonian cycles. For even n, the step-two graph has exactly two connected components, the even and odd position classes; the generated permutation group is S_m x S_m. Thus the ordered alternating-label partition is preserved at fixed origin. Rotation by one exchanges the two classes, so on unoriented unrooted cycles only the unordered bipartition is well-defined. Conversely, for a fixed bipartition any two cyclic orders with those alternating label sets are connected after suitable rotation. The total number of undirected labelled Hamiltonian cycles is (n-1)!/2. Dividing by the number of components gives ((n-1)!/2)/(binomial(n,m)/2) = (m!)^2/n cycles per component. This also works for n=4.

## Exhaustive audit
n=4: 3 cycles, 3 components of size 1
n=5: 12 cycles, 1 component of size 12
n=6: 60 cycles, 10 components of size 6
n=7: 360 cycles, 1 component of size 360
n=8: 2520 cycles, 35 components of size 72.

## Reproduction
```python
from itertools import permutations
from collections import Counter
for n in range(4,9):
    states={tuple([0]+list(p)) for p in permutations(range(1,n)) if p[0]<p[-1]}
    def canon(a):
        b=a[a.index(0):]+a[:a.index(0)]
        return min(b,(b[0],)+b[:0:-1])
    adj={a:set() for a in states}
    for a in states:
        for i in range(n):
            b=list(a);b[i],b[(i+2)%n]=b[(i+2)%n],b[i]
            adj[a].add(canon(tuple(b)))
    seen=set();sizes=[]
    for a in states:
        if a in seen:continue
        todo=[a];seen.add(a);size=0
        while todo:
            u=todo.pop();size+=1
            for v in adj[u]:
                if v not in seen:seen.add(v);todo.append(v)
        sizes.append(size)
    print(n,len(states),Counter(sizes))
```

## Comparison hierarchy
Colour-neutral raw cycles and constant-colour cycles without a separation constraint are equivalent. Adding q distinguishable labels may (i) refine observations only, (ii) constrain admissible states, or (iii) constrain admissible moves. These are distinct operations and must not be conflated. With the same proper-colouring rule, q=1 is empty; q=2 forces alternating colours (even n only), and q=3 supports the five-letter XYXZX <-> XZXYX colour-changing LR3 pattern. The raw even-n parity partition predates any colour restrictions; some later 'colour-sector' obstructions may descend from this underlying invariant. In contrast, at odd n raw LR3 is connected, so any fragmentation under additional constraints is induced by those constraints.

## Interpretation
This is a theorem about a particular LR3 move generator on labelled cycles. It is not a physical symmetry or a claim of novelty in the literature. The next clean test should track each restricted colour-sector component relative to the raw-cycle components, keeping vertex labels and fixed vertex colours distinct from the colour-word quotient.
