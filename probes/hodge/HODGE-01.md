# EHF-HODGE-01 — Discrete Hodge Fit and Algebraic-Geometric Bridge Audit

Date: 2026-10-20 (Australia/Brisbane)

**Status: COMPUTATIONAL reference run; discrete Hodge track justified.
Bridge to the Clay Hodge conjecture unestablished.**

## Question

Can Hodge theory clarify EHF comparisons without confusing:
(a) additive exactness, (b) topology of a chosen base complex,
(c) matrix holonomy, and (d) algebraic cycle classes?

## Provenance and reconstruction

Base: holonomy commit `299313458f68b780e48b575a340f2f2284416ebe`.
Read [RECUR-BACKGROUND](../holonomy/RECUR-BACKGROUND.md) for prior definitions.

For each n=5,6,7,8, enumerate all undirected Hamilton cycles of the complete
graph K_n by fixing root 0 and taking one orientation. There are (n-1)!/2 cycles.
At anchor a, observer O_a records the unordered pair of neighbours of a.
It has binomial(n-1,2) states. Use the uniform microstate prior and Euclidean
inner products on the observer coordinates.

Construct the conditional reconstruction matrix L_ab with columns indexed by
source O_a and rows by destination O_b from integer joint counts divided by
source-fibre counts. This is the column-vector convention.
For an SVD L_ab=U Sigma V^T, retain singular values above 1e-9 and set
W_ab=U_r V_r^T. Compose H_abc=W_ca W_bc W_ab.

These matrices are freshly enumerated, not loaded from earlier reported spectra.
The SVD and eigenvalues are numerical, not exact symbolic certificates.

## Scalar cochain definitions

For a chosen finite oriented complex let
d0:C^0 -> C^1 assign (d0 f)(a,b)=f(b)-f(a).
For an oriented triangle a<b<c, let
(d1 x)(a,b,c)=x(a,b)+x(b,c)-x(a,c).

With standard Euclidean inner products:

`d1 d0=0,`
`Delta1=d0 d0^T+d1^T d1,`
`C^1=im(d0) direct_sum im(d1^T) direct_sum ker(Delta1).`

The summands are orthogonal. Harmonic cochains satisfy both d0^T h=0 and d1 h=0.
Their dimension is beta1 over R. Rational incidence ranks give the same
Betti number here. This is established finite-dimensional Hodge theory.

In particular, the RECUR-04 quantity delta_P(u,v)=r_P(u)-r_P(v) is a
vector-valued exact difference, coordinate by coordinate. It sums to zero
around every loop. Applying a Hodge decomposition cannot create a hidden
harmonic obstruction in such exact data. The code checks representative
scalar gradients as an implementation control; it does not reconstruct
the RECUR-04 transition-count vectors.

## Face-choice controls

Use observer anchors as vertices and all unordered pairs as edges.
Compare:
- G_n, the complete graph regarded as a one-dimensional complex;
- T_n, the same graph with every triangle attached as a 2-simplex,
  and no cells above dimension 2.

All triangles are an explicit diagnostic choice. A joint observer distribution
exists for each triple, but this does not require its transports to compose
consistently and does not canonically select a cell interpretation.

For G_n, beta1=E-V+1=binomial(n-1,2).

For T_n, beta1=0: every graph cycle decomposes into triangle boundaries.
For example, boundaries of triangles (0,i,j) form a basis of the cycle space.
Thus rank(d1)=E-V+1. These are standard all-n facts; the script additionally
checks rational ranks exactly for n=4,...,8 using Fraction elimination.

| n | beta1(G_n) | beta1(T_n) |
|---|---:|---:|
| 4 | 3 | 0 |
| 5 | 6 | 0 |
| 6 | 10 | 0 |
| 7 | 15 | 0 |
| 8 | 21 | 0 |

Zero beta1 does not mean all higher topology vanishes. T_n is only a
2-skeleton; no claim of a manifold, complex variety or contractibility is made.

On the single triangle with edges (01,02,12), set x=(1,-1,1).
Without a face, x is harmonic with squared norm 3.
With its triangle attached, the same x is entirely in im(d1^T),
with curl energy 3 and harmonic energy 0.
This illustrates dependence on cells; it is not an EHF discovery.

## Independent RECUR transport checks

| n | Hamilton microstates | Observer states | rank(L_ab) | Target cos(theta) |
|---|---:|---:|---:|---|
| 5 | 12 | 6 | 6 | 23/27 |
| 6 | 60 | 10 | 8 | 11/16 |
| 7 | 360 | 15 | 10 | 71/125 |
| 8 | 2520 | 21 | 12 | 13/27 |

For q=n-2 the reference target is cos(theta)=(3q^2-4)/q^3.
The audit checks for the corresponding nonreal unit-modulus eigenvalue in
H_012. Maximum eigenvalue residual in the recorded run is below 1.2e-15.
The reverse product equals H_012^T to numerical tolerance.
Because the W maps are contractions, a unit-modulus eigenmode preserves norm
on its orbit. The full loop can still contain lossy directions.
The full Frobenius distance from identity is retained for diagnostics,
not used alone as evidence of lossless holonomy.

The n=5 case is included as a finite control and has an extra +1 mode;
the general n>=6 multiplicity statement in the RECUR background is not
silently extended to this boundary case.

Changing G_n to T_n does not change these transport matrices.
Consequently nonidentity loop transport is present even on a base complex
whose ordinary scalar H^1 is zero. It detects path dependence that cannot
be identified with ordinary first cohomology. A curved connection can
have nontrivial holonomy around a contractible loop.

This is a distinction between structures, not a contradiction. A flat
local system on filled triangles would instead require compatible
invertible edge maps whose product around each face is identity.
The current rank-deficient partial-isometry construction does not
automatically supply one. No twisted cochain complex with d^2=0 is claimed.
No matrix logarithms or scalar eigenangle sums are used as substitute
cochains.

## Result and fit decision

- **PROVED (standard):** exact differences have zero loop sum;
  the stated complete-graph/filled-triangle beta1 formulas follow from
  elementary cycle-space algebra.
- **COMPUTATIONAL:** exact rational incidence-rank checks for n=4,...,8;
  floating-point scalar decomposition controls; independent RECUR matrix
  reconstruction and rotation checks for n=5,...,8.
- **NEGATIVE / BOUNDARY:** ordinary first cohomology alone does not encode
  the observed matrix holonomy; face choice can remove harmonic scalar
  cycles without removing matrix loop transport.
- **UNESTABLISHED:** intrinsic EHF cells, a compatible coefficient system
  for the matrix transport, and any bridge to rational (p,p) algebraic
  cycle classes on a smooth projective variety.

Proceed with a bounded discrete Hodge track. Nothing in this audit proves,
refutes, or provides a reduction of the Clay Hodge conjecture.
No new conjecture is asserted.

## Reproduction

From repository root, with Python 3.10+:

```sh
python -m pip install -r code/hodge/requirements.txt
python code/hodge/hodge_01_audit.py --output data/hodge/hodge-01-results.json
```

[Code](../../code/hodge/hodge_01_audit.py).
[Results](../../data/hodge/hodge-01-results.json).
NumPy version and tolerance are recorded in the JSON. Floating-point last
digits may vary across numerical libraries. Rational ranks, integer counts,
and rational target cosines must agree exactly.

## HODGE-02 — proposed cell and coefficient audit

Before further interpretation:

1. Choose one EHF model and distinguish its microstate complex from its
   observer-comparison complex.
2. Specify independently justified face relations, for example exact
   commuting transformation squares. Test the relations rather than
   fill loops because a preferred Betti number results.
3. Identify an intrinsically motivated scalar edge observable, or prove
   the conditions needed for a vector coefficient complex. Preserve
   noncommutative transport information.
4. Compare justified face rules and inner products. Test relabelling
   invariance and whether growth maps commute with coboundaries.
5. Retain negative results. If only standard identities or arbitrary
   completions result, pause rather than claim a new conjecture.

An algebraic-geometric bridge audit is a separate later gate; its missing
objects and requirements are listed in the [branch guide](../../research/hodge/README.md).

## Sources

- Deligne, official Clay statement:
  https://www.claymath.org/wp-content/uploads/2022/06/hodge.pdf
- Jiang, Lim, Yao and Ye, established scalar discrete Hodge methods:
  https://arxiv.org/abs/0811.1067
