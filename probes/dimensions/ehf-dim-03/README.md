# EHF-DIM-03 — Slow collective modes and microscopic symmetry sectors

**Date:** 2026-11-19. **Status:** Executed finite n=7 calculation; no general emergence claim.

## Question
Do slowest nonconstant random-walk modes select particular irreducible symmetry sectors, and is selection robust under OPW3 (LR3) versus OPW23 (LR2+LR3)?

## Method
Reconstruct canonical 36-state n=7 chamber and the S3×S3 action permuting three nonzero labels in each parity class. Project adjacency matrices onto nine isotypic sectors using central character projectors. Here t=trivial 1D, s=sign 1D, d=standard 2D representation of S3. The simple walk is A/k; lazy walk is (I+A/k)/2.

## Executed results
| Quantity | OPW3 | OPW23 |
|---|---:|---:|
| Chamber states | 36 | 36 |
| Degree | 4 | 6 |
| Leading nonconstant adjacency eigenvalue | 3 | 3 |
| Leading nonconstant sectors | td, dt | td, dt |
| Multiplicity of eigenvalue 3 | 4 | 4 |
| Simple-walk eigenvalue | 0.75 | 0.50 |
| Lazy-walk second eigenvalue | 0.875 | 0.75 |
| Simple-walk spectral gap | 0.25 | 0.50 |

In both graphs, each of td and dt has adjacency eigenvalues [1,1,3,3], a stronger coincidence than simply preserving the leading sector labels. Other sectors change. The leading nonconstant modes are four-dimensional collectively (two in each sector), but these are state-function modes, **not physical directions or spatial dimensions**.

## Limits and next steps
The n=7 chamber is small and highly symmetric. OPW3 is bipartite, making raw even-time return comparisons potentially misleading. OPW23 contains OPW3 edges, so models are related rather than independent. No asymptotic dimension, physical geometry, SU(3), or 1:2:3 norm law follows.

Next: test other chambers and n=9; compare with symmetry-preserving and symmetry-breaking nulls; seek a combinatorial explanation for eigenvalue 3; distinguish representation dimension from graph metric dimension.

See [DIM-02](../ehf-dim-02/README.md) for the complete S3×S3 projectors and sector spectra. The companion DIM-03 verifier is reproducible with NumPy.
