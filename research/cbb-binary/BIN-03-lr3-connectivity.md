# EHF-CBB-BIN-03 — Unrestricted LR3 connectivity baseline

Date: 2026-11-10. Status: exact finite enumeration, **not** a general theorem. This baseline uses bare labelled undirected Hamiltonian cycles, **without** MICRO, Pi-preservation, or controller restrictions. The repository's `probes/reversals/README.md` defines LR3 as reversing three consecutive vertices; its MICRO and Pi variants are distinct experiments.

## Definitions and algorithm
Represent each cycle by the lexicographically smaller of the two sequences obtained by starting at vertex 0 and traversing in either direction. Enumerate all permutations of 1,...,n-1 modulo reversal. For each cycle and every cyclic start index i, reverse the order of the three consecutive vertices at positions i,i+1,i+2 modulo n. Canonicalize, discard self-loops, and form the undirected adjacency graph. BFS/DFS gives connected components. Check undirected adjacency and total cycle count (n-1)!/2.

## Exact results
| n | cycles | components | component sizes | distinct undirected LR3 edges | LR3 graph bipartite? |
|---|---:|---:|---|---:|---|
| 3 | 1 | 1 | 1 | 0 | yes |
| 4 | 3 | 3 | 1 each | 0 | yes |
| 5 | 12 | 1 | 12 | 30 | yes |
| 6 | 60 | 10 | 6 each | 90 | yes |
| 7 | 360 | 1 | 360 | 1260 | no |
| 8 | 2520 | 35 | 72 each | 10080 | no |

These results show connectivity at n=5,7 and disconnected sectors at n=6,8, but do not prove a general odd/even theorem. The n=3,4 degeneracies matter. Bipartiteness of the LR3 *transition graph* is not equivalent to odd/even n: n=7 and n=8 both fail bipartiteness.

## Reproducible Python 3 code
```python
import itertools

def canonical(p):
    p=list(p)
    i=p.index(0)
    p=p[i:]+p[:i]
    return min(tuple(p), tuple([p[0]]+p[:0:-1]))

def cycles(n):
    return sorted({canonical((0,)+p) for p in itertools.permutations(range(1,n))})

def lr3(c):
    n=len(c)
    out=set()
    for i in range(n):
        a=list(c)
        idx=[(i+j)%n for j in range(3)]
        vals=[a[j] for j in idx][::-1]
        for j,v in zip(idx,vals):
            a[j]=v
        d=canonical(a)
        if d!=c: out.add(d)
    return out

for n in range(3,9):
    states=cycles(n)
    adj={c:lr3(c) for c in states}
    assert all(c in adj[d] for c,ds in adj.items() for d in ds)
    seen=set()
    sizes=[]
    for c in states:
        if c in seen: continue
        stack=[c]
        seen.add(c)
        size=0
        while stack:
            a=stack.pop()
            size+=1
            for b in adj[a]:
                if b not in seen:
                    seen.add(b)
                    stack.append(b)
        sizes.append(size)
    print(n,len(states),len(sizes),sorted(sizes),sum(map(len,adj.values()))//2)
```

## Interpretation and next step
This establishes an LR3 reachability baseline but **does not yet establish a binary path invariant or growth–LR3 commutator**. Next: define a binary sector observable at even n, test its behaviour under insertion and LR3, and examine commuting/noncommuting growth/reversal squares. Distinguish static sector labels from parity of path length and from memory-bearing transport. Avoid claims about physical symmetry breaking.
