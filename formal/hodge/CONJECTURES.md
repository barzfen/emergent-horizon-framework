# EHF MICRO component conjecture and transport theorem

Updated: 2026-10-20 (Australia/Brisbane), HODGE-04

**C1 remains CONJECTURE. C2 is now PROVED within the specified model.**
No novelty claim is made. C2 has an explicit analytic proof and exact
implementation checks; it has not been independently reviewed or
formally verified in a proof assistant.

## Definition lock

For each integer n>=5:

- Vertices are rooted, labelled binary words on the oriented n-cycle with
  no cyclic 010 or 101 pattern.
- An edge is a non-self length-three reversal whose result is valid.
  Duplicate neighbours are identified.
- Attach one square for each distinct four-state commuting relation of
  moves with disjoint swapped endpoint sets, provided both orders are valid.
  Deduplicate square boundaries under cyclic rotation and reversal.
- No other faces or higher cells are attached. Call the complex X_n.
- A moving component C is a connected component containing at least one edge.

This is the precise complex of [HODGE-02](../../probes/hodge/HODGE-02.md).
HODGE-03 proves its endpoint-square rule equals the window-disjoint rule
for all n>=5.

On a directed edge w -> tau_i(w), define the closed integer cochains

`j = 2(w_i-w_(i+2)),`
`kappa = +1 if w_i=w_(i+1), and -1 otherwise.`

The latter counts signed displacement of a 01 run boundary.
Both reverse sign on edge reversal and have integral loop periods
divisible by n. They represent classes in H^1(C;Z), and over Q.

The component has fixed number m of 1 values and fixed number D of runs
(domain walls). For a moving component, E=n-2D>0.

## EHF-HODGE-C1 — Single rational homology direction

**Status: CONJECTURE.**

For every n>=5 and every moving component C of X_n,

`dim_Q H_1(C;Q)=1,`

and the boundary-winding period map

`[gamma] -> (1/n) sum_gamma kappa`

is nonzero. Equivalently, it is an isomorphism of one-dimensional rational
vector spaces H_1(C;Q) -> Q.

**This does not assert:** H_1(C;Z)=Z; absence of torsion; a primitive
integral winding generator; fundamental group Z; or homotopy equivalence
to a circle.

A finite counterexample is any moving component with rational beta1
different from 1 or with zero kappa period on every loop.

[HODGE-03](../../probes/hodge/HODGE-03.md) exhaustively checks 200 moving
components across n=5,...,18, all satisfying C1. This finite evidence
is not an all-size classification.

## EHF-HODGE-C2 — Binary/boundary period theorem

**Status: PROVED in HODGE-04.** The C2 identifier is retained for
continuity with the original conjecture.

For every n>=5 and every moving component C of X_n,

`(n-2D)[j] = 2(n-2m)[kappa] in H^1(C;Z).`

In particular the originally conjectured equality over Q holds.
Equivalently, for every closed graph path gamma in C,

`(n-2D) sum_gamma j = 2(n-2m) sum_gamma kappa.`

The [explicit marker-potential theorem](TRANSPORT-POTENTIAL.md) proves
the stronger edge identity

`F(v)-F(w)=(n-2D)j(w,v)-2(n-2m)kappa(w,v)`

for an integer-valued state function F. Its construction uses the
invariant cyclic order of excess-bit markers and does not assume C1.

### Corollaries

On balanced moving components (m=n/2), j=d(F/E) is exact over Q.
Thus binary transport misses their topology for a proved structural
reason, not because the graph has no cycles.

Whenever the boundary period is nonzero,

`sum j / sum kappa = 2(n-2m)/(n-2D).`

The boundary winding K=(sum kappa)/n must be divisible by

`(n-2D)/gcd(n-2D,2(n-2m)).`

This is necessary; it is not an assertion that every permitted multiple
occurs. For example, some n=11 components have image 3Z, consistent
with this constraint.

The exact edge identity also determines weighted transport on open paths
from the endpoint values of F.

## Evidence and remaining work

- HODGE-03 supplies exact finite H1 and period checks for C1 and the
  then-conjectural C2.
- [HODGE-04](../../probes/hodge/HODGE-04.md) supplies the all-size C2
  proof and independent exact verification on 15,112 states and
  16,190 edges through n=18.
- C1 remains open. HODGE-05 should audit whether the conserved cyclic
  marker word, together with root-phase data, classifies components.
- Compare with existing constrained-dynamics/state-complex literature
  before claiming originality.
- No smooth projective variety, rational (p,p) identification or
  algebraic cycle map has been derived. The Clay bridge and its parity
  restriction remain as assessed in LITERATURE-01.
