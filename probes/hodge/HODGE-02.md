# EHF-HODGE-02 — MICRO Commuting Faces and Transport Cohomology

Date: 2026-10-20 (Australia/Brisbane)

**Status: PROVED elementary all-size statements for the specified construction;
COMPUTATIONAL exact topology for n=5,...,12; numerical Hodge projections.
No Clay Hodge bridge or novelty claim.**

## Purpose and provenance

HODGE-01 distinguished observer-matrix holonomy from scalar first cohomology.
This audit asks whether an existing EHF move rule supports independently
motivated cells and a scalar comparison observable.

Base commit: `c45a8ee7e433db92c451c2cf4f904aca3620fd62`.

This probe changes the base object explicitly: vertices here are MICRO
**microstates**, not RECUR observer anchors. The rule is independently
reimplemented from [the Wheeler audit](../../code/wheeler/review_audit.py).
It does not identify the MICRO cohomology with RECUR matrix holonomy.

## Model

Fix a rooted, labelled, oriented ring with n>=5 positions indexed modulo n.
A state is a binary word w with no cyclic 010 or 101 pattern; equivalently
every run in a nonconstant word has length at least 2.

The move at i reverses the length-three window (i,i+1,i+2), equivalently
swaps bits at i and i+2. Retain it only if the result is valid and different.
Use the undirected simple graph of distinct resulting neighbours.
For n>=5 a non-self edge identifies its move label uniquely.
The n=4 duplicate-event case is deliberately excluded.

The number of 1 values and domain-wall count are constant along the audited
moves. Rotation-related words remain distinct vertices. No rotation quotient
or growth is built into this fixed-size complex.

Coefficients are Q for exact ranks and real-valued Euclidean cochains for
the numerical Hodge projection. This is ordinary additive cohomology,
not a (p,q) decomposition.

## Rule-based square faces

For moves i,j with disjoint endpoint sets {i,i+2} and {j,j+2},
the coordinate transpositions commute as maps on binary words.
Retain a square only if:
1. both first moves are admissible;
2. both second moves are admissible and end at the same state;
3. all four vertices are distinct.

Attach one oriented 2-cell per distinct square boundary, deduplicating
cyclic rotations and reversal. These cells encode exchanges of independent
commuting moves. Treating the two orders as equivalent histories is an
explicit modelling choice motivated by their exact commutation; it is not
forced uniquely by the original graph.

Two versions are compared:
- **Window-disjoint:** the full length-three windows are disjoint.
- **Endpoint-disjoint:** the swapped endpoint sets are disjoint; windows may overlap.

A third sensitivity control adds all graph triangles to endpoint squares.
There are no such triangles in this finite scan, so this control adds no faces.
Equality of the two square sets in this scan is not asserted for all n.
No cubes or higher cells are attached. Nothing here proves a manifold
structure, homotopy equivalence to a circle, absence of torsion, or a
complex algebraic variety.

## Intrinsic scalar comparison observable

For the directed move w -> tau_i(w), define

`j_i(w) = 2 (w_i - w_(i+2)).`

This is the signed displacement of the binary 1 value along the oriented
two-step arc i -> i+2. It is +2 or -2 on every non-self move.
It depends on the ring orientation, but not on a chosen starting vertex.
Reversing the move negates j.

This is combinatorial transport. No physical particles, time units,
energies or currents are inferred.

### Proposition 1: closedness on commuting squares

A move with disjoint endpoints does not change the bits used in the other's
j value. For the square based at w,

`j_i(w)+j_j(tau_i w)-j_i(tau_j w)-j_j(w)=0.`

Thus d1 j=0 for either square rule, for every n>=5.
This is an elementary proof from the stated support condition.

### Proposition 2: integer loop winding

Let M(w)=sum(k*w_k), using labels k=0,...,n-1.
For every edge,

`j(w,v) - (M(v)-M(w)) is an integer multiple of n.`

Away from the label seam the two terms agree; crossing it changes the
labelled position difference by a multiple of n.
Around any closed graph path, the M differences telescope, so

`sum_loop j = n * integer.`

Since j is closed on the attached squares, this defines a homomorphism
from integral first homology to Z by dividing its periods by n.
It need not be injective.

The ring seam is a coordinate choice used in the proof; the period is
unchanged by cyclic relabelling and changes sign on orientation reversal.
Bit complement also changes its sign.

### Proposition 3: nontrivial first cohomology for every n>=5

Take the word with exactly two adjacent 1 values and all other bits 0.
Move that length-two block one site forward by reversing 110 to 011.
Every state is valid. After n moves the block returns to its starting
position; every edge has j=+2. Hence this loop has period 2n.

An exact cochain df has zero period on every loop, so j is closed but not
exact in either commuting-square complex. Consequently H^1 is nonzero.

More specifically, valid states with exactly two 1 values are precisely
the n placements of the adjacent block. Their move component is C_n:
only its one-site forward/backward shifts are admissible.
There are no square faces entirely in that component.
Bit complement supplies a second C_n component with n-2 ones.
For n>=5 the two sectors are distinct; therefore total beta1 >= 2.

These are direct all-size consequences of this construction. They do
not require extrapolation from a numerical spectrum and are not claimed
as new results in the wider literature.

## Exact finite topology

The audit exhausts all binary words and moves for each n=5,...,12.
It checks every retained face has zero boundary and computes face-boundary
rank over Q using sparse integer elimination with gcd reduction.
No floating-point rank threshold enters the Betti numbers.

If c is the number of graph components,

`beta1 = E - V + c - rank_Q(d1).`

For efficiency, face boundaries are restricted to non-tree edges of a
spanning forest. This restriction is injective on the graph cycle space,
so it preserves their rank.

| n | V | E | Graph beta1 | Square faces | Square beta1 | Moving components |
|---|---:|---:|---:|---:|---:|---:|
| 5 | 12 | 10 | 2 | 0 | 2 | 2 |
| 6 | 20 | 12 | 2 | 0 | 2 | 2 |
| 7 | 30 | 14 | 2 | 0 | 2 | 2 |
| 8 | 46 | 16 | 2 | 0 | 2 | 2 |
| 9 | 74 | 36 | 4 | 0 | 4 | 4 |
| 10 | 122 | 80 | 16 | 10 | 6 | 6 |
| 11 | 200 | 154 | 28 | 22 | 6 | 6 |
| 12 | 324 | 264 | 52 | 36 | 16 | 16 |

Both square rules yield the same face sets and ranks over this range.
Every moving component has beta1=1 in the endpoint-square audit.
This is an **EMPIRICAL PATTERN (finite exhaustive scan)**, not an all-n
classification or a conjecture promoted to fact.

## A useful negative: transport does not detect every cycle

The exact fundamental-loop periods give the image of the winding
homomorphism as g Z; g=0 means that all periods vanish on that component.

- Through n=9, moving components have g=2.
- At n=10, some have g=0 despite beta1=1.
- At n=12, g can be 0, 1 or 2 depending on component.

For example, at n=10 there are moving components with 15 vertices and
20 edges. Square relations leave beta1=1, but this j has zero period
on every loop of such a component.
Thus j is exact there and its harmonic projection vanishes, although
the complex still has a nonzero harmonic space for other observables.

At n=12, a retained period -12 witness has one unit of signed winding;
the adjacent-pair loop instead has period 24.
The result file stores an explicit shortest-in-absolute-period witness
among the chosen fundamental cycles. It is not claimed to be a shortest
graph loop or a minimal generator of the whole homology group.

This falsifies any claim that net signed binary transport is a complete
observable for first cohomology.

## Euclidean Hodge check and symmetry

Because d1 j=0, the Euclidean decomposition is j=d0 f+h:
the curl summand is zero. Least squares is solved independently on
each connected component after fixing one vertex potential.

The code verifies d0^T h=0 and d1 h=0 numerically to 1e-8,
and retains gradient/harmonic energies and residuals.
These are numerical checks; integer loop periods certify non-exactness.

Rotation, reflection and bit complement are checked as graph
automorphisms preserving both square sets at every audited size.
Rotation preserves j and the other two symmetries negate it.
Betti numbers do not depend on this choice of sign.
Harmonic representatives and their norms refer to the stated Euclidean
inner product; no prior-independent metric has been derived.

## Growth gate: an admissible vertex insertion is insufficient

Test the fixed insertion G(w)=(w_0,w_0,w_1,...,w_(n-1)).
It is an allowed all-slot growth event duplicating the root bit and
always preserves validity.

It is not a graph map. In the scan n=5,...,11, the numbers of old edges
whose image endpoints are nonadjacent are respectively

`6, 6, 6, 6, 12, 24, 42.`

An all-size obstruction is immediate. The adjacent pair states

`w=0^(n-2)11,`
`v=1 0^(n-2)1`

are neighbours. Their root bits differ, so G(w) has two 1 values and
G(v) has three. A fixed-size reversal preserves the number of 1 values,
so these images cannot be neighbours at size n+1.

This particular insertion therefore supplies no induced cellular map
or cochain pullback on the one-step move complexes.
The result does not exclude a path-valued growth map, a correspondence,
a subdivision, or a different construction; those would require their
own definitions and compatibility proofs.
No growth-stability claim is made.

## Evidence summary

- **PROVED within this model:** square closedness of j, integer periods,
  explicit 2n winding loop, beta1>=2 for all n>=5, and failure of the
  tested fixed-root growth map.
- **COMPUTATIONAL, exact finite:** states, moves, square boundaries, Q ranks,
  per-component Betti numbers, integral periods and symmetry checks.
- **COMPUTATIONAL, numerical:** Euclidean Hodge projections.
- **EMPIRICAL PATTERN:** each moving component has beta1=1 through n=12.
- **FALSIFIED:** net signed transport detects every surviving first-homology
  class; automatic one-step growth compatibility.
- **UNESTABLISHED:** all-size component classification, canonical choice
  among justified cells, compatible growth functor, Hodge structures or
  algebraic cycle maps relevant to the Clay problem.

## Reproduce

```sh
python -m pip install -r code/hodge/requirements.txt
OPENBLAS_NUM_THREADS=1 python code/hodge/hodge_02_audit.py --output data/hodge/hodge-02-results.json
```

The environment variable only limits numerical-library threading.
[Code](../../code/hodge/hodge_02_audit.py).
[Results](../../data/hodge/hodge-02-results.json).

The default range is n=5,...,12. The script accepts --max-n up to 14,
but sizes above 12 are not part of this report's retained run.
The script imports no prior EHF code and uses only NumPy beyond the
Python standard library.

## Next: HODGE-03 — classify the missed cycles

Describe the moving components in run coordinates, then identify the
cycles with zero net j and ask whether a second rule-based observable
detects them. Audit the finite beta1=1 pattern before formulating an
all-size claim. Homology rank one alone does not establish circle
homotopy type.

Growth-compatible maps and the algebraic-geometric bridge remain
separate gates. This result is discrete topology of a specified EHF
model, not progress on algebraicity of rational (p,p) classes.
