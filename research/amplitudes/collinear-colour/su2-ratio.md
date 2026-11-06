# Exact SU(2) finite collinear colour ratio

Compute the first finite term of the tree MHV amplitude for a
positive-helicity gluon pair along the exchange-symmetric equal-split
path. The angle spinors lie in a common real chart. The exact
momentum-conserving samples use complexified kinematics.

The symmetric pair of adjoints has a trace channel of dimension 1
and a symmetric traceless channel of dimension 5. The interaction
T1 dot T2 has eigenvalues −2 and +1 there, obtained from
(C_pair−2 C_A)/2 with C_A=2 and C_pair=0 or 6. The dimension times
squared eigenvalue law gives 1 times 4 versus 5 times 1, or 4:5.
The antisymmetric triplet carries the leading pole.

We sum the full SU(2) colour chains with the exact Parke–Taylor
Laurent coefficients. The script tests the pair exchange symmetry
of the finite term and antisymmetry of the pole, then directly
projects the finite tensor onto its trace. Subtracting the trace
norm from the total gives the symmetric traceless norm. For three
samples each at five, six, and seven gluons the squared-norm shares
are exactly 4/9 and 5/9. The chain generator is also checked against
the existing five-gluon structure-constant implementation.

Run `python3 su2_ratio.py > su2-ratio-results.json` with standard-library Python.
This is a pure Yang–Mills check of the finite coefficient. A physical
electroweak test would need its own treatment of masses, mixing and
external polarization states.

See the [exact results](su2-ratio-results.json) and the [SU(N) Casimir law](su-n-casimir-law.md).
