# EHF-DIM-05 — Weighted LR2 interpolation

**Date:** 2026-11-19. **Status:** Executed n=7 numerical projection and derived exact characteristic polynomial from trace invariants.

## Question
Do the identical td/dt spectra of OPW3 and OPW23 persist for intermediate LR2 weights?

Define A(w)=A3+w A2, where A2=A23-A3. The n=7 36-state chamber and S3×S3 projectors are exactly as in DIM-03 and DIM-04.

## Results
For both td=(trivial,standard) and dt=(standard,trivial), the isotypic sector is four-dimensional and each distinct eigenvalue has multiplicity two. Numerically computed sector traces:

- tr(A3)=8
- tr(A2)=0
- tr(A3 A2)=-2
- tr(A2²)=4
- tr(A3²)=20

These give tr(A(w))=8 and tr(A(w)²)=20-4w+4w². Because the sector consists of two equivalent copies of a two-dimensional multiplicity-space operator, its two distinct eigenvalues sum to 4 and have sum of squares 10-2w+2w². Their product is 3+w-w².

Hence, on either sector,

`chi_w(lambda) = [lambda² - 4lambda + 3 + w - w²]²`

and

`lambda_±(w) = 2 ± sqrt(1 - w + w²)`, each repeated twice.

The radicand is strictly positive for all real w, so there is no eigenvalue crossing within the sector. It is invariant under w -> 1-w.

| w | lower eigenvalue | upper eigenvalue |
|---:|---:|---:|
| 0 | 1 | 3 |
| 0.25 | 1.098612181 | 2.901387819 |
| 0.5 | 1.133974596 | 2.866025404 |
| 0.75 | 1.098612181 | 2.901387819 |
| 1 | 1 | 3 |
| 1.5 | 0.677124345 | 3.322875655 |
| 2 | 0.267949192 | 3.732050808 |

Thus **isospectrality at w=0 and w=1 is an endpoint coincidence explained by a quadratic symmetry**, not invariance throughout the interpolation. The symmetry *sector labels* remain preserved for all w, but their eigenvalues vary.

## Interpretation
This separates structural sector preservation (forced by the common S3×S3 action) from numerical eigenvalue protection (not forced). It does not imply SU(3), physical space, or a universal dimension law.

## Next
1. Derive the 2×2 multiplicity-space operators directly from Cayley generators, replacing numerical projector trace checks with symbolic integer arithmetic.
2. Test whether w↔1-w is induced by a similarity transformation within the sector, or is merely an equality of characteristic polynomials.
3. Compare other n=7 chambers and n=9 before extrapolation.

Run `python3 probes/dimensions/ehf-dim-05/probe.py` (NumPy).
