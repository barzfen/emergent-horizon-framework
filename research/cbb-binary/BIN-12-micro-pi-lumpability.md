# EHF-CBB-BIN-12 — MICRO quotient survives; Pi breaks lumpability

Date: 2026-11-10. Status: exact finite combinatorial argument and enumerated counterexample.

## Definitions
Unrestricted LR3 reverses three consecutive cyclic vertices. MICRO: every vertex has at least one cyclic neighbour of its own fixed binary colour. Pi: rotate cycle to start at label 0, choose traversal towards its smaller-labelled neighbour, and take labels at positions 0,2,4,... . A move is Pi-preserving if its Pi set equals that of the source. Canonical undirected cycle representations choose the lexicographically smaller traversal after placing 0 first.

## Theorem: MICRO restriction respects binary-bracelet lumping
Fix the marked colour set R. MICRO is a predicate of the cyclic binary word alone: no position may be isolated between two opposite-coloured neighbours. Thus MICRO is constant on each bracelet class. Unrestricted LR3 acts on binary words by swapping positions i and i+2, and the number of moves between bracelet classes is representative-independent. Restricting to MICRO-valid target bracelets retains this equitability, with disallowed transitions deleted. The resulting count matrix can be substochastic if forbidden proposals are discarded; if invalid proposals cause a stay-put step, add rejected counts to the diagonal, yielding a stochastic reversible chain. If one instead chooses uniformly among legal moves, normalize each row by its legal degree; this is a different Markov protocol and has degree-weighted stationary distribution, not necessarily the orbit-size distribution. Specify the protocol before comparing spectral results.

## Count of MICRO-valid bracelets, with m=(n-1)/2 marked positions
n=7: 1 of 4
n=9: 2 of 10
n=11: 3 of 26
n=13: 6 of 76
These are computed by binary word enumeration and testing the no-isolated-bit condition.

## Pi counterexample at n=9
Fix marked labels R={0,1,2,3}. Let
C1=(0,1,2,3,4,5,6,7,8)
C2=(0,1,4,5,6,7,8,3,2).
Both are canonical undirected cycles, have bracelet 000001111, satisfy MICRO, and have identical Pi={0,2,4,6,8} under the anchored orientation rule. Enumerating all nine distinct LR3 proposals and requiring both MICRO and Pi preservation gives **four** legal moves from C1 and **three** from C2. All legal moves remain in bracelet 000001111. Hence even the proposed augmented state (bracelet, Pi set) is not an equitable partition for the joint MICRO+Pi-constrained LR3 dynamics.

This is a direct counterexample to inferring exact quotient dynamics from the bracelet and Pi set alone. It does not rule out a finer finite-state quotient with additional orientation, seam, or local label data.

## Reproducible counterexample
```python
def canon(p):
    p=list(p);i=p.index(0);p=p[i:]+p[:i]
    return min(tuple(p),tuple([p[0]]+p[:0:-1]))
def lr3(c):
    n=len(c);out=set()
    for i in range(n):
        a=list(c); ix=[(i+j)%n for j in range(3)]
        v=[a[j] for j in ix][::-1]
        for j,z in zip(ix,v):a[j]=z
        out.add(canon(a))
    return out
def pi(c):
    a=list(c);i=a.index(0);a=a[i:]+a[:i]
    if a[-1]<a[1]:a=[a[0]]+a[:0:-1]
    return frozenset(a[::2])
def micro(c,R):
    n=len(c)
    return all((c[(i-1)%n] in R)==(c[i] in R)
               or (c[(i+1)%n] in R)==(c[i] in R)
               for i in range(n))
R={0,1,2,3}
C1=(0,1,2,3,4,5,6,7,8)
C2=(0,1,4,5,6,7,8,3,2)
assert pi(C1)==pi(C2)==frozenset({0,2,4,6,8})
assert micro(C1,R) and micro(C2,R)
def legal(c):
    return {d for d in lr3(c) if micro(d,R) and pi(d)==pi(c)}
assert len(legal(C1))==4
assert len(legal(C2))==3
```

## Interpretation
MICRO is invariant under colour-pattern equivalence; Pi is sensitive to label order and anchor orientation. Therefore a colour-pattern-only observable is a sufficient state for the MICRO-only projected Markov dynamics but not for the joint MICRO+Pi model. Next: determine a minimal augmented local descriptor (including the Pi seam/anchor) that yields an equitable quotient, or prove that specific proposed descriptors remain insufficient. Do not infer any physical law.
