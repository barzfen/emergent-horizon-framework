# Seven-gluon sign of the departure from the planar colour ratio

**The six-gluon sign persists at seven gluons.** For the first
finite tree-level MHV coefficient on the exchange-symmetric,
equal-split collinear path, the planar 27 share is one half.
At every regular real-projective seven-gluon starting point with
a nonzero finite tensor, a genuine imaginary projective tangent
raises that share at quadratic order. A tangent removable by a
projective change of chart has zero quadratic coefficient.

This follows the [six-gluon sign proof](near-planar-sign.md) and
uses the same [planar norm identity](planar-theorem.md).
The sign concerns the first finite amplitude coefficient in the
collinear expansion. It is a local statement about a deformation
of the hard kinematics.

## Exact certificate

Send the parent spinor to infinity. Sort the five real spectator
coordinates and send the first two to zero and one. Write the
coordinates as `(0, 1, 1+a, 1+a+b, 1+a+b+c)`, with
`a,b,c>0`. The three independent imaginary tangents are the
changes in the last three coordinates in this normalized chart.
Sorting is a relabelling of the summed spectator colours and
orderings.

For each spectator ordering, clear the common Vandermonde
denominator in the stripped finite coefficient. The resulting
polynomial is the signed product of the endpoint difference and
the six pairwise differences complementary to the four edges of
the ordering path. The sign compensates for the path edges whose
orientation is opposite to the coordinate order. Overall scalar
factors cancel from the colour share.

In the 120-ordering basis, form the real colour Gram combination
`Q = G27 − Gtotal/2`, up to a common positive scale. Spectator
permutation symmetry lets the code obtain every entry by
permuting a single reference overlap row. For the vector of
polynomials `p`, the planar identity is `pᵀQp=0`. Its derivative
gives `pᵀQ dp=0`, so differentiating the common denominator
does not affect the sign. The code checks both identities as
integer polynomials.

Let `Mij = (∂i p)ᵀ Q (∂j p)`, with derivatives taken in the last
three spectator coordinates. For an imaginary tangent `v`, the
sign of the quadratic share shift is the sign of `vᵀ M v`.
In the positive gaps `a,b,c`, the exact expansion gives

| Leading principal minor | Nonzero coefficients | Positive coefficients |
| --- | ---: | ---: |
| First diagonal entry | 296 | 296 |
| Upper-left two-by-two determinant | 1,907 | 1,907 |
| Full determinant | 4,727 | 4,727 |

Each minor is strictly positive throughout the sorted chart.
Sylvester's criterion makes `M` positive definite there, which
proves the sign for every nonzero tangent in the chart.

## Checks and reproduction

The numerical search sampled 10,000 positive gap configurations.
Its smallest normalized eigenvalue was about −1.9e−11 at a
strongly clustered point, within the scan's 1e−9 tolerance. The
exact positivity certificate settles the sign even there.

As checks, the six-gluon calculation reproduces the published
first-minor and determinant coefficients term for term.
For the seven-gluon point `(0,1,2,4,7)` and imaginary direction
`(0,0,1,−2,3)`, a separate exact contraction in explicit colour
indices agrees with the Gram form and gives the quadratic share
coefficient `29389072/30383991`, about 0.9673.

Run `python3 verify_seven_sign.py --samples 10000` with NumPy.
The [saved output](near-planar-seven-results.json) gives the
reference Gram row, scan summary and minor coefficient counts.
Use `--coefficients` to emit the complete minor polynomials
as exponent tuples and integer coefficients. Use `--gluons 6`
to recover the earlier leading minors.

The sign at eight or more gluons and the behaviour at finite
tilt remain open.
