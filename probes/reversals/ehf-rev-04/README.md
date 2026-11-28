# EHF-REV-04 — Exact adjacency spectrum and symmetry-sector audit

**Date:** 2026-11-19 (Australia/Brisbane)  
**Status:** Independent finite calculation (n=7, largest OPW3 chamber); SU(3) norm-law comparison negative for the tested natural grouping.

## Method

Use [REV-03](../ehf-rev-03/README.md) definitions: 360 canonical undirected Hamiltonian cycles on K7, preserve Pi (even-position label set) and use circular LR3. Construct the 36-vertex, 4-regular chamber. Form its real symmetric adjacency matrix A. Independently permute the three nonzero labels in each of the two parity classes; this S3×S3 action commutes with A and acts regularly.

Compute eigenvalues of A; then use the central character projectors for the nine irreducible complex representations of S3×S3. For an irrep rho of dimension d, P_rho=(d/36) sum_g chi_rho(g) R(g) (characters are real here). Numerically diagonalize the symmetric projected restrictions; all displayed eigenvalues are integers to floating precision.

## Results

Full spectrum, eigenvalue: multiplicity:

- -4:1; -3:4; -2:4; -1:4; 0:10; +1:4; +2:4; +3:4; +4:1.

Central projector sectors (t=trivial, s=sign, d=2D standard S3 representation):

| sector | isotypic dimension | adjacency eigenvalues (with multiplicities) |
|---|---:|---|
| tt | 1 | 4 |
| ts | 1 | 0 |
| st | 1 | 0 |
| ss | 1 | -4 |
| td | 4 | 1,1,3,3 |
| dt | 4 | 1,1,3,3 |
| sd | 4 | -3,-3,-1,-1 |
| ds | 4 | -3,-3,-1,-1 |
| dd | 16 | -2×4, 0×8, 2×4 |

The nine isotypic dimensions group by irrep dimension as 4 (four 1D types), 16 (four 2D types), 16 (one 4D type), hence 1:4:4, **not** 1:2:3. This is only a chosen mathematically natural grouping; no unique three-sector physical decomposition has been derived. The irrep dimensions 1,2,4 are not the SU(3) 1,8,27 irreps, and their dimensions are not projected amplitude norms.

## Interpretation and next tests

- The chamber has an integral adjacency spectrum and a regular S3×S3 action. This is a finite graph-theoretic fact, not evidence of particle masses or SU(3).
- The simplest three-family dimension comparison does not give 1:2:3.
- Compare the n=7 OPW23 adjacency spectrum on the same chamber; examine which spectral structure survives LR2 shortcuts.
- Check n=9, and null models, before attributing special significance to integrality.
- If comparing amplitude squared norms, specify a non-fitted amplitude vector and inner product **before** calculating the three projections.

The companion standalone verifier below regenerates these results from canonical cycle enumeration and character projectors.
