# EHF-DIM-06 — Exact quadratic algebra in slow symmetry sectors

**Date:** 2026-11-19. **Status:** Exact integer-matrix verification at n=7, largest 36-state chamber.

## Result

Let A3 be the LR3 adjacency matrix, A2 the LR2-only adjacency matrix, and P either central character projector for the td or dt sector of the natural S3×S3 relabelling action. Define X=A3−2I and Y=A2. The verifier computes integer numerator Q=18P and establishes exactly:

- (X²−I)Q = 0
- (Y²−I)Q = 0
- (XY+YX+I)Q = 0

The central projector P commutes with X and Y, so these are identities of the restricted operators. No floating-point eigenvalue fitting is used. Hence (X+wY)²=(1−w+w²)I on each sector. Because the trace of X+wY is zero in each four-dimensional sector, its eigenvalues are ±sqrt(1−w+w²) with multiplicity two each. Thus weighted adjacency eigenvalues are 2±sqrt(1−w+w²), each repeated twice.

## Minimal algebraic representation

The two generators satisfy X²=Y²=I and XY+YX=−I. One concrete real 2×2 representation is:

```
X = [[ 1, 0], [ 0,-1]]
Y = [[-1/2, sqrt(3)/2], [sqrt(3)/2, 1/2]]
```

The two unit coefficient vectors in the Pauli-matrix representation have dot product −1/2 (an angle of 120°). This is an **algebraic analogy**, not a demonstrated physical spin system. The relations imply (XY)²+(XY)+I=0, so XY has order 3. Together with X²=Y²=I, this gives the two-reflection presentation of S3 on each irreducible 2D block. A direct Cayley-generator derivation remains separate.

## Scope

- Relations hold **after projection** onto td or dt, not necessarily on the full graph.
- This verifies the identities directly from enumerated reversal operators using exact integer arithmetic, not yet from an abstract presentation of reversal moves.
- Representation dimension is not spatial dimension; no SU(3) or physical spin follows.

Run `python3 probes/dimensions/ehf-dim-06/probe.py` (NumPy).
