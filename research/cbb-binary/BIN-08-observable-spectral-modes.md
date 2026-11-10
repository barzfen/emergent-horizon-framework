# EHF-CBB-BIN-08 — Observable spectral modes of memory

Date: 2026-11-10. Status: exhaustive finite-state construction and numerical spectral projection with exact rational eigenvalues identified; no physical interpretation.

## Question
Which eigenmodes of the n=7 unrestricted LR3 random walk actually affect the channel from an initial n=6 cycle to a final n=8 LR3 sector?

## Matrices
Let S be the 60x360 row-stochastic matrix for uniform insertion 6->7, P the 360x360 symmetric transition matrix for uniform LR3 at n=7 (each state has 7 distinct neighbours), and T the 360x35 row-stochastic matrix for insertion 7->8 followed by the destination n=8 LR3-component label. Define Q_k=S P^k T. The stationary-output matrix U has every entry 1/35.

## Finding
Numerical eigendecomposition of P reveals that the only nonstationary eigenspaces contributing to Q_k are lambda=5/7 (multiplicity 14 in P) and lambda=2/7 (multiplicity 14 in P). In particular the largest-magnitude nonstationary eigenvalue, -0.7848513153478499, is completely invisible to this input-output channel (projected Frobenius norm about 3e-16).

Let E_5,E_2 be orthogonal spectral projectors of P for eigenvalues 5/7 and 2/7, and define D_5=S E_5 T, D_2=S E_2 T. Then, numerically to floating-point precision,
Q_k=U+(5/7)^k D_5+(2/7)^k D_2.
Maximum absolute entrywise reconstruction residual at k=0: 1.98e-16. This is a numerical verification of an exact-looking finite-matrix identity; a symbolic/group-theoretic proof of the vanishing of all other projections remains a worthwhile follow-up.

Squared Frobenius norms: ||D_5||_F^2 = 2.17687074829932, ||D_2||_F^2=0.19047619047619035; inner product ~0.

## Information-theoretic consequence
With X uniform over 60 starting cycles, Y_k the output n=8 sector, Y_k is uniform over 35 sectors for all k. Therefore I(X;Y_k) = (1/60) sum_{x,y} Q_k(x,y) log2(35 Q_k(x,y)). For large k, Taylor expansion around Q_k=1/35 gives
I(X;Y_k) ~ [35/(120 ln 2)] ||D_5||_F^2 (25/49)^k
~ 0.915996851358 (25/49)^k bits.
Thus asymptotic per-step mutual-information ratio is 25/49 ~= 0.51020408, rather than the generic full-chain squared spectral radius ~= 0.61599. The secondary mode contributes to transient behaviour.

Selected exact-enumeration I(X;Y_k), bits:
k=0: 0.904097737229
k=1: 0.419029352503
k=2: 0.213064569951
k=4: 0.057080731561
k=6: 0.015335202487
k=10: 0.001077373753
k=15: 0.00003773031466.

## Reproducible Python
Requires numpy. Enumerates canonical undirected cycles and builds the complete matrices.

```python
import itertools, numpy as np

def canon(p):
    p=list(p); i=p.index(0); p=p[i:]+p[:i]
    return min(tuple(p),tuple([p[0]]+p[:0:-1]))

def cycles(n):
    return sorted({canon((0,)+p) for p in itertools.permutations(range(1,n))})

def lr3(c):
    n=len(c); out=set()
    for i in range(n):
        a=list(c); idx=[(i+j)%n for j in range(3)]
        vals=[a[j] for j in idx][::-1]
        for j,v in zip(idx,vals): a[j]=v
        d=canon(a)
        if d!=c: out.add(d)
    return out

def insert(c,new):
    for i in range(len(c)):
        a=list(c); a.insert(i+1,new)
        yield canon(a)

def components(states):
    ids={}; groups=[]
    for s in states:
        if s in ids: continue
        idx=len(groups); stack=[s]; ids[s]=idx; group=[]
        while stack:
            a=stack.pop(); group.append(a)
            for b in lr3(a):
                if b not in ids: ids[b]=idx; stack.append(b)
        groups.append(group)
    return ids,groups

c6,c7,c8=[cycles(n) for n in (6,7,8)]
i7={c:i for i,c in enumerate(c7)}
id8,g8=components(c8)
S=np.zeros((60,360)); P=np.zeros((360,360)); T=np.zeros((360,35))
for i,c in enumerate(c6):
    for d in insert(c,6): S[i,i7[d]]+=1/6
for i,c in enumerate(c7):
    for d in lr3(c): P[i,i7[d]]+=1/7
    for d in insert(c,7): T[i,id8[d]]+=1/7
assert len(g8)==35 and all(len(g)==72 for g in g8)
assert np.allclose(P,P.T) and np.allclose(P.sum(axis=1),1)
w,V=np.linalg.eigh(P)
def projected(lam):
    ids=np.where(np.abs(w-lam)<1e-8)[0]
    return (S@V[:,ids])@(V[:,ids].T@T)
D5,D2=projected(5/7),projected(2/7)
U=np.full((60,35),1/35)
assert np.max(np.abs(S@T-U-D5-D2))<1e-12
for k in (0,1,2,4,6,10,15):
    Q=S@np.linalg.matrix_power(P,k)@T
    assert np.max(np.abs(Q-U-(5/7)**k*D5-(2/7)**k*D2))<1e-12
    mi=np.sum(Q*np.log2(35*np.maximum(Q,1e-300)))/60
    print(k,mi)
print('asymptotic coefficient',35*np.sum(D5**2)/(120*np.log(2)))
```

## Limits and next probe
The exact rational mode selection is a strong finite-matrix pattern, not yet an analytic derivation. Identify why insertion and sector projection annihilate other irreducible modes; test at 4->5->6 and 8->9->10 where computational costs rise. Repeat with MICRO and Pi admissibility and nonuniform controller rules. Do not infer physical thermalization, irreversible information destruction, or a new universal law.
