# EHF-DIM-04 — Why the slow symmetry sectors survive

Date: 2026-11-19. Status: computed finite n=7 sector audit; mechanism not yet generalized.

## Setup

Same 36-state n=7 chamber as DIM-03, with A3 for LR3 and A2 for additional LR2 edges, A23=A3+A2. The S3×S3 action commutes with both operators. Its central character projectors define nine isotypic sectors, t=trivial, s=sign, d=standard.

## Computed results

| Sector | A3 eigenvalues | A2 eigenvalues | A23 eigenvalues |
|---|---|---|---|
| tt | 4 | 2 | 6 |
| ts | 0 | -2 | -2 |
| st | 0 | -2 | -2 |
| ss | -4 | 2 | -2 |
| td | 1,1,3,3 | -1,-1,1,1 | 1,1,3,3 |
| dt | 1,1,3,3 | -1,-1,1,1 | 1,1,3,3 |
| sd | -3,-3,-1,-1 | -1,-1,1,1 | -2-sqrt(3) (twice), -2+sqrt(3) (twice) |
| ds | -3,-3,-1,-1 | -1,-1,1,1 | -2-sqrt(3) (twice), -2+sqrt(3) (twice) |
| dd | -2 (4), 0 (8), 2 (4) | -2 (4), -1 (4), 1 (4), 2 (4) | (-1-sqrt(21))/2 (4), 0 (4), 1 (4), (-1+sqrt(21))/2 (4) |

The td/dt characteristic polynomial is (lambda-1)^2(lambda-3)^2 for both A3 and A23. This is a finite, exact-algebraic identity of the enumerated operators, verified numerically to high precision. It can be independently certified using integer/rational character projectors and characteristic polynomial arithmetic.

The LR2 operator does NOT annihilate the A3 eigenvalue-3 eigenspace. The compression of A2 to that 2D eigenspace is -1/2 times identity, and A2 couples it to the other two dimensions (coupling Frobenius norm sqrt(3/2)). Thus the eigenvalues persist while the eigenvectors rotate.

The global commutator has Frobenius norm ||[A3,A2]||_F=12: the operators do not share a general eigenbasis.

## Mechanistic interpretation

The symmetry projectors enforce **sector invariance**, but symmetry alone does not enforce the **same eigenvalues** under rule changes. The td/dt characteristic-polynomial invariance is an additional special property of these two adjacency operators. It is not a general theorem of admissible comparison or SU(3) emergence.

## Next falsification probes

1. Derive the td/dt 2x2 multiplicity-space matrices from explicit Cayley generators and prove their trace and determinant invariance.
2. Vary LR2 weights continuously, A(w)=A3+w A2, to test whether spectral equality occurs only at w=0 and w=1.
3. Check other n=7 chambers and n=9, with size-matched symmetry-preserving controls.
4. Keep representation dimension and graph-geometric dimension separate.
