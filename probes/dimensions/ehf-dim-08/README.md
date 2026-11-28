# EHF-DIM-08 — Permutahedral product geometry at n=9

**Date:** 2026-11-19. **Status:** Executed exhaustive enumeration at n=7 and n=9, including an all-edge Cayley-graph isomorphism for the largest chambers.

## Main result

At n=7, the largest 36-state OPW3 chamber is Cay(S3, adjacent transpositions) □ Cay(S3, adjacent transpositions), or C6 □ C6. At n=9, the largest 576-state chamber is Cay(S4, adjacent transpositions) □ Cay(S4, adjacent transpositions), a Cartesian product of two 24-vertex permutahedron graphs. This is verified for **every vertex and adjacency**, not just graph invariants.

## Census

| Quantity | n=7 | n=9 |
|---|---:|---:|
| Canonical undirected Hamiltonian cycles | 360 | 20,160 |
| OPW3 edges | 600 | 53,760 |
| OPW23 edges | 840 | 67,200 |
| Connected chambers | 19 | 69 |
| Largest chamber states | 36 | 576 |
| Largest OPW3 degree | 4 | 6 |
| Largest OPW3 diameter | 6 | 12 |

At n=9, the component-size distribution is: 36:1, 72:2, 108:3, 144:5, 180:5, 216:7, 252:7, 288:8, 324:7, 360:7, 396:5, 432:5, 468:3, 504:2, 540:1, 576:1. The 69 OPW23 components have the same partition as OPW3.

## Generator audit

Take the canonical n=9 root (0,1,5,2,6,3,7,4,8), with nonzero even labels E={5,6,7,8} and odd labels O={1,2,3,4}. Independently relabel E and O by S4. This action is free and transitive on the largest chamber (24×24=576 states). Its six LR3 neighbours correspond exactly to (s1,e),(s2,e),(s3,e),(e,s1),(e,s2),(e,s3), where si are adjacent transpositions of four positions. Exhaustive checking of all 576 adjacency lists confirms the Cayley product.

## Interpretation and limits

This provides a structural finite-graph reconstruction from elementary admissible reversals at two sizes. It does **not** establish emergent physical space or an asymptotic metric dimension. The S4 permutahedron has a 3D polytope realization; the Cartesian product of two has a natural 6D polytope realization. Those dimensions are distinct from spectral dimension, effective diffusion dimension, and symmetry representation dimensions.

The general odd-n formula for the maximally alternating chamber, (m!)² states with m=(n−1)/2, degree 2(m−1), diameter m(m−1), is **suggested but not yet proven**. Most other chambers are irregular, so do not extrapolate the product structure to all chambers.

## Next

Prove the general maximally alternating chamber theorem directly from the LR3 rule. Classify the irregular chambers. Measure scale-dependent diffusion and volume growth with finite-size controls. Keep the SU-decomposition question separate unless an explicit representation-theoretic map is constructed.
