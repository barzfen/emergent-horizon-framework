# EHF-CBB-BIN-09 — Analytic selection rule for the 5/7 and 2/7 observable modes

Date: 2026-11-10. Status: exact combinatorial derivation for unrestricted LR3 at n=7. The four-class transition counts were independently checked against all 360 labelled undirected 7-cycles; the matrix calculation is exact. No physics interpretation.

## Claim
For the channel Q_k = S P^k T defined in BIN-08, the only nonstationary modes are 5/7 and 2/7. In fact this is stronger: the n=7-to-n=8-sector observation matrix T *itself* has no components in other nonstationary eigenspaces of P. The cancellation does not depend on S.

## Why the n=8 sectors are 4+4 partitions
At even n, LR3 reverses a length-three segment, swapping the two endpoint vertices (positions differing by two), so it preserves the unordered bipartition of vertices by even/odd positions. At n=8, the moves generate all permutations within each parity class; the undirected cycle forgets which class is named even. There are binomial(8,4)/2=35 components, one for each unordered 4+4 partition. (The equality of each 72-state component with one partition can also be checked by exact enumeration.)

Fix one output sector. Specify it by the three old vertices R in the four-vertex parity class containing the newly inserted vertex 7. For a given 7-cycle C, inserting 7 into an edge reaches this sector iff R is a maximum independent set of size 3 on C. There are exactly seven maximum independent triples of C; each corresponds to exactly one insertion edge. Therefore T(C,R)=1/7 if R is an independent triple in C, otherwise 0.

## Four possible marked-gap patterns
Mark the three vertices of R around C. Their positive cyclic gap lengths sum to seven. Up to cyclic permutation and reversal, the possible sorted triples are
A=(1,1,5), B=(1,2,4), C=(1,3,3), D=(2,2,3).
Only D is independent.

An LR3 move swaps the two endpoints of three consecutive vertices. For each marked-gap type, direct local counting of the seven possible endpoint swaps gives the number of moves to each type:

| from / to | A | B | C | D | total |
|---|---:|---:|---:|---:|---:|
| A | 3 | 2 | 2 | 0 | 7 |
| B | 1 | 4 | 1 | 1 | 7 |
| C | 2 | 2 | 3 | 0 | 7 |
| D | 0 | 2 | 0 | 5 | 7 |

This is an *equitable partition* of the 360-state LR3 graph for every fixed marked triple R. Exhaustive check: all 360 cycles obey these four row-counts (72,144,72,72 cycles in the four types for fixed R).

Let M be the 4x4 integer matrix in the table, K=M/7, and e_D=(0,0,0,1)^T. The observation function is f_R=e_D/7 on the four classes. Exact linear algebra gives eigenvalues of M: 7,5,2,1. The eigenvalue 1 does not appear in the observation because
(M-5I)(M-2I)e_D = 2 * 1,
where 1 is the all-ones vector. Since M 1=7*1, the observation decomposes into only eigenvalues 7,5,2. The constant part of e_D is (1/5)*1 because 72/360=1/5. Consequently the constant part of T(C,R) is (1/7)*(1/5)=1/35.

Hence for the full 360x35 matrix T,
(P-I)(P-(5/7)I)(P-(2/7)I) T = 0
and more strongly
(P-(5/7)I)(P-(2/7)I)(T-J)=0,
where J is the constant matrix with entries 1/35. The latter is an exact identity, with no floating-point assumptions. Therefore for any initial insertion matrix S with S*1=1,
Q_k=S P^k T=J+(5/7)^k D_5+(2/7)^k D_2,
where D_5=S E_{5/7} T and D_2=S E_{2/7} T. This proves the two-mode selection rule of BIN-08 and explains why the slower negative full-chain eigenmode is invisible.

## Independent exact verification
The four row counts were checked by generating every labelled undirected 7-cycle, classifying the gaps of a fixed triple R, applying each of seven LR3 moves, and confirming the same target-type counts for all cycles in a type. Exact symbolic check:
```python
import sympy as sp
M=sp.Matrix([[3,2,2,0],[1,4,1,1],[2,2,3,0],[0,2,0,5]])
e=sp.Matrix([0,0,0,1]); one=sp.ones(4,1)
assert M.eigenvals()=={7:1,5:1,2:1,1:1}
assert (M-5*sp.eye(4))*(M-2*sp.eye(4))*e==2*one
```

## Interpretation and limits
The observable's low-dimensional spectral support is due to its dependence on a fixed triple's **four cyclic gap types**, and the way LR3 endpoint swaps move among those types. This is a selection rule imposed by the observation map, not a new universal law. The 1:2:3 law from other EHF colour/collinearity work is an interesting comparison to investigate separately; no identity has been established between that law and this 7,5,2 eigenvalue structure. No inference about physical particles, entropy, or symmetry breaking follows.

## Next
Derive explicit closed-form D_5 and D_2 entries using the four-type quotient; test whether analogous equitable partitions and observable modes persist for odd orders 5,9 and constrained MICRO/Pi systems. Compare the source 1:2:3 law's precise definitions before asserting a connection.
