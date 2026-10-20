# EHF-HODGE-C2 — Explicit Marker-Potential Theorem

Date: 2026-10-20 (Australia/Brisbane)

**Status: PROVED within the stated MICRO model.**
This analytic proof is independent of the C1 component-classification
conjecture. It has not been formally verified in a proof assistant or
independently reviewed; no novelty claim is made.

## 1. Model and theorem

Fix n>=5. A state is a labelled binary word on an oriented n-cycle
containing no cyclic 010 or 101 pattern. A move reverses the length-three
window (i,i+1,i+2), swapping its endpoints; retain non-self moves with
valid target.

Let m be the number of 1 values and D the number of domain walls,
equivalently runs for a nonconstant state. Both are fixed on a move
component. On a directed edge w -> v=tau_i(w), put

`j(w,v)=2(w_i-w_(i+2)),`

`kappa(w,v)=+1 if w_i=w_(i+1), and -1 otherwise.`

A positive kappa is a right shift of a length-two run.
Define

`E_1=m-D,` `E_0=n-m-D,` `E=E_0+E_1=n-2D.`

**Theorem.** There is an explicitly defined integer-valued state
function F such that every admissible edge satisfies

`F(v)-F(w)=E j(w,v)-2(n-2m)kappa(w,v).`

Consequently every closed graph path gamma satisfies

`E sum_gamma j=2(n-2m) sum_gamma kappa.`

In the square complex of HODGE-02, j and kappa are closed integer
cochains. Therefore this gives the stronger integral relation

`E[j]=2(n-2m)[kappa] in H^1(C;Z)`

on every moving component C. In particular it proves the formerly
conjectural C2 relation over Q.

The edge identity is already an identity on the move graph. It does
not depend on a face-rank calculation or a one-dimensional H1 assumption.

## 2. Run-shift lemma

Every nonconstant valid state has alternating runs of length at least 2.
Every admissible non-self move shifts an entire length-two run one
position right or left. A right shift requires the following opposite-bit
run to have length at least 3.

For completeness, a non-self reversal has the form aa b -> b aa or
its reverse, with a != b. If the aa were part of a longer a-run,
the introduced b would be a forbidden singleton. If the donor b-run
had length 2, the remaining b would be a singleton. Conversely,
a length-two a-run and a donor b-run of length at least 3 give a valid
right shift. The left case is the inverse.

The number of runs is unchanged and the bits are only permuted,
so D and m are invariant.

## 3. Excess markers and their cyclic order

For every run, discard its first two positions when traversing the
oriented ring. Mark every remaining bit, recording its position and
its bit value. These are bookkeeping markers, not additional state
variables or physical particles.

A run of length r contributes r-2 markers. There are D/2 runs of
each bit value, giving exactly E_0 zero markers and E_1 one markers.

For a constant word, set F=0 separately; such words have no moves.
For a nonconstant state with no markers, also set F=0. These are
all-length-two frozen states. The construction below covers all
other nonconstant states, including frozen ones.

### Marker motion under one right shift

Suppose a length-two b-run occupies s,s+1 and moves right. The donor
opposite-bit run starts at s+2 and has length at least 3.

Before the move, s,s+1 are the discarded b pair and s+2,s+3 are the
discarded donor pair. The first donor marker is at s+4.
After the move:

- The preceding opposite-bit run gains a last site at s, adding a marker.
- The donor's start shifts to s+3, so its discarded pair becomes
  s+3,s+4; the old marker at s+4 disappears.
- All other markers are unchanged.

Thus exactly one marker of colour 1-b moves from s+4 to s, a signed
displacement -4 along the oriented lift. The four preceding positions
contain no other marker, so no marker is passed.

When D=2, the preceding and following opposite-bit run are the same
cyclic run. Comparing the old and new discarded pairs gives exactly
the same marker replacement. This avoids treating the two appearances
as distinct runs.

A left shift is the inverse marker displacement +4. Since n>=5,
the length-four arc is shorter than the ring, including at the n=5
boundary case.

It follows that the cyclic word of marker colours is invariant under
every move. Markers can move, but their cyclic order never changes.

## 4. A potential independent of cyclic labelling

List the marker positions in increasing root coordinates:

`0<=p_0<p_1<...<p_(E-1)<n,`

with colours c_a in {0,1}. Assign weights

`omega(1)=E_0,` `omega(0)=-E_1.`

Their total weight is zero:

`sum_a omega(c_a)=E_1 E_0-E_0 E_1=0.`

Choose the lexicographically least cyclic rotation of the colour word,
using 0<1. If cut a yields this canonical word, unwrap the positions
starting there:

`(p_a,...,p_(E-1),p_0+n,...,p_(a-1)+n).`

Define F(w) as the sum of each unwrapped position times the weight of
its colour.

### Common-translation independence

Adding the same real or integer number to all unwrapped positions
changes the sum by that number times the total weight, hence by zero.
In particular a common n-shift has no effect. The ring seam is not
an extra datum in F.

### Independence among repeated canonical cuts

Suppose cuts a and b give the same canonical colour word.
The interval between them consists of whole periods of that word.
Every period has the same colour proportions as the full word,
so the weights of that interval sum to zero.

Changing cuts adds n to the positions of precisely such an interval,
up to a common translation. Its effect on F is n times a zero sum.

More explicitly, if the shift between cuts is d, put g=gcd(E,d).
Equality of the rotations makes the word a repetition of a block
of length g. The prefix of length d contains d/g copies; each
block's total weight is g/E times the full zero weight. Thus the
prefix weight vanishes.

Therefore F is a single-valued integer function of the state, even
when the colour word has rotational symmetry.

The specific lexicographic convention is only a choice of constant:
choosing a different representative for each invariant cyclic colour
word changes F by a componentwise constant. It does not change dF.

## 5. Edge identity

Track the marker identities in their preserved cyclic order during
a move. Choose a marker at which the colour sequence is canonical,
and use that marker as the cut before and after the move. No passing
ensures this remains a permissible canonical cut.

Choose unwrapped positions continuously along the marker motion.
Every unchanged marker keeps its position; the moved marker changes
by -4 for a right shift. These lifts differ from the numerical
definition at most by the canonical-cut transformations already
proved harmless.

For a right shift:

| Shifted run | Moved marker | Weight | Change in F |
|---|---|---:|---:|
| b=1 | 0 | -E_1 | +4E_1 |
| b=0 | 1 | E_0 | -4E_0 |

Here kappa=+1 and j is +2 for b=1, -2 for b=0.
Since n-2m=E_0-E_1,

- For b=1, E j-2(n-2m)kappa
  =2(E_0+E_1)-2(E_0-E_1)=4E_1.
- For b=0, the same expression is
  -2(E_0+E_1)-2(E_0-E_1)=-4E_0.

These are exactly the two changes in F. Left shifts follow by
reversing the edge. This proves the theorem for every n>=5.

No component enumeration, homology-rank conjecture, continuum limit,
or imported algebraic-geometric result is used.

## 6. Consequences

### Loop-period identity

Sum the edge identity along any closed path. The F differences
telescope. This proves C2 independently of C1.

### Balanced components

If m=n/2 and the component is moving, E>0. Then

`j=d(F/E).`

Binary transport is an exact rational cochain on every balanced
moving component, whether or not its topology has one first-homology
direction. Its vanishing periods do not require trivial topology.

### Fixed-size open paths

For any path from w to v in a component, the same summation gives

`E sum_path j-2(n-2m)sum_path kappa=F(v)-F(w).`

The weighted discrepancy is determined entirely by the endpoints.

### Necessary divisibility of boundary winding

Earlier work proves the integer winding numbers

`J=(1/n)sum_gamma j,` `K=(1/n)sum_gamma kappa.`

For a moving component E>0, C2 gives

`E J=2(n-2m)K.`

Therefore every boundary winding K is divisible by

`E/gcd(E,2(n-2m)).`

For example, n=11,m=5,D=4 gives E=3 and coefficient 2, so K must
be a multiple of 3. This explains a restriction seen in HODGE-03.
It does not prove that every permitted multiple occurs.

### Harmonic representatives

For any fixed positive cochain inner products on the stated square
complex, projection to the harmonic summand kills dF. Hence the same
linear relation holds between the harmonic projections of j and kappa.
The exact cochain identity precedes and is independent of the metric.

## 7. Scope and remaining questions

This proves the period relation inside the specified MICRO model.
It does not prove C1, classify every component, determine integral
torsion or homotopy type, establish growth compatibility, or connect
EHF to the Clay Hodge conjecture.

The invariant cyclic marker word is a new structural tool for this
branch. Whether it completely classifies components is not asserted.
A future classification must also handle root phase and realizability.

No claim is made that the marker construction or resulting identity
is original in the broader constrained-dynamics literature.

## 8. Reproduction and status

[HODGE-04 report](../../probes/hodge/HODGE-04.md)
and [standard-library audit code](../../code/hodge/hodge_04_audit.py).

The independent implementation checks every admissible edge through
n=18, including seam crossings and repeated canonical colour patterns.
Those checks verify the implementation and catch boundary cases;
the all-size conclusion rests on Sections 2–5 above.
