# EHF-CBB-BIN-07 — Spectral audit of unrestricted LR3 mixing at n=7

Date: 2026-11-10. Status: numerical eigendecomposition of an exactly enumerated finite transition matrix. No MICRO/Pi constraints, no physics interpretation.

## Setup
The 360 undirected labelled Hamiltonian cycles on 7 vertices (modulo rotation/reversal) form the states. An LR3 move reverses three cyclically consecutive vertices. Each state has seven distinct LR3 neighbours. The symmetric adjacency matrix A is 360x360 and the uniform random-walk transition matrix is P=A/7. Direct enumeration verifies symmetric A and degree 7.

## Numerical spectrum
Distinct eigenvalues (rounded to 10 decimals), multiplicities:
- -0.7848513153 (15)
- -0.5363436726 (21)
- -0.4285714286 (35)
- -0.3014166092 (15)
- -0.2857142857 (14)
- -0.2211115871 (21)
- -0.1428571429 (35)
- 0 (20)
- 0.0862679245 (15)
- 0.1428571429 (84)
- 0.2857142857 (14)
- 0.4285714286 (35)
- 0.6145981168 (21)
- 0.7142857143 (14)
- 1 (1)

The second-largest eigenvalue *magnitude* is rho=0.7848513153478499. This implies convergence of every initial probability distribution to uniform, since all nontrivial eigenvalues have absolute value <1. In L2 relative to uniform, ||mu P^k-u||_2 <= rho^k ||mu-u||_2. The slowest mode has negative eigenvalue, so its signed amplitude alternates with each move.

The entropy and mutual-information observations of BIN-06 concern a *coarse-grained output channel*, not the raw slowest eigenmode. A spectral L2 bound controls the approach of intermediate distributions to stationarity, but is not an equality for the observed mutual information. Near equilibrium, relative entropy and mutual information often have leading terms quadratic in deviations, motivating rho^(2k) asymptotics only if the slowest mode couples to the specific input/output channel. Do not assert that the observed mutual information decays exactly as rho^(2k) without checking the projection.

## Reproduction
Run the following Python with numpy:

```python
import itertools
import numpy as np

def canon(p):
    p=list(p)
    i=p.index(0)
    p=p[i:]+p[:i]
    return min(tuple(p),tuple([p[0]]+p[:0:-1]))

def cycles(n):
    return sorted({canon((0,)+p) for p in itertools.permutations(range(1,n))})

def lr3(c):
    n=len(c)
    out=set()
    for i in range(n):
        a=list(c)
        idx=[(i+j)%n for j in range(3)]
        vals=[a[j] for j in idx][::-1]
        for j,v in zip(idx,vals):
            a[j]=v
        d=canon(a)
        if d!=c:out.add(d)
    return out

states=cycles(7)
index={c:i for i,c in enumerate(states)}
A=np.zeros((len(states),len(states)),dtype=float)
for c in states:
    for d in lr3(c):
        A[index[c],index[d]]=1
assert np.all(A==A.T)
assert np.all(A.sum(axis=1)==7)
ev=np.linalg.eigvalsh(A/7)
print('spectral radius off stationarity:',max(abs(ev[:-1])))
from collections import Counter
print(Counter(np.round(ev,10)))
```

## Next
Compare exact I(X;Y_k) from BIN-06 with spectral decomposition of the insertion/output channel. Identify which eigenmodes couple to the coarse-grained observable and test the asymptotic decay rate; then repeat under MICRO/Pi constraints and nonuniform controller rates.
