# EHF-HODGE-C1 — Marker-Gap Classification and Fundamental Group

Date: 2026-10-21 (Australia/Brisbane)

**Status: PROVED within the specified MICRO square complex.**
This is a written analytic argument, supported by bounded exact checks.
Independent proof review, proof-assistant verification and broader novelty
assessment remain open.

## 1. Statement

Use the labelled binary n-cycle, n>=5, with no cyclic 010 or 101.
Edges are admissible non-self length-three reversals. Attach precisely
the independent commuting squares defined in HODGE-02. No higher cells
are attached. Call the square complex X_n.

Consider only a moving component. Mark the bits after the first two
positions of each run, as in the C2 proof. Write:

- D: number of runs/domain walls;
- E=n-2D>0: number of markers;
- chi: lexicographically least cyclic rotation of the marker-colour word;
- l: primitive period length of chi, so l divides E;
- T: number of cyclic colour changes in chi;
- H=(D-T)/2: slack;
- d=gcd(4,l);
- rho: position, modulo d, of a marker at which the colour word is chi.

H is a gap/slack parameter, not a homology group.

**Classification theorem.** For moving states, H>0, rho is well-defined,
and two states at the same n are connected exactly when their triples

`(D,chi,rho)`

agree. For each realizable moving necklace chi there are exactly d
components, one for each rho in Z/dZ.

**Fundamental-group theorem.** Every moving component C satisfies

`pi_1(C) is isomorphic to Z,`
`H_1(C;Z) is isomorphic to Z.`

The image of the boundary-winding homomorphism

`K(gamma)=(1/n)sum_gamma kappa`

is exactly

`(l/d) Z.`

This proves C1, including its nonzero rational winding assertion, and
strengthens it to an integral first-homology statement.

**Component size.** Every one of the d components belonging to chi has

`n*l/(E*d) * binomial(H+E-1,E-1)`

vertices.

Frozen states are separate singleton components. Their empty or
zero-slack marker descriptions must not be used to merge them.

## 2. Marker gaps reconstruct the state

The run-shift lemma and no-passing marker rule are proved in
[TRANSPORT-POTENTIAL.md](TRANSPORT-POTENTIAL.md).
A move shifts exactly one marker by +/-4.

Take two consecutive markers with colours c_a,c_(a+1).
Their clockwise distance has the form

`g_a=b_a+4h_a,`
`b_a=1+2*[c_a differs from c_(a+1)],`
`h_a>=0.`

To see this directly, after the first marker every unmarked intervening
run has length 2. Equal-colour markers have a base distance 1; inserting
an opposite-colour run and the next same-colour discarded pair adds 4.
Different-colour markers require the next run's first two bits, giving
base distance 3; additional pairs of empty runs again add 4.

More constructively, between a marker of colour c and its successor,
insert h_a copies of the four-bit block

`(1-c),(1-c),c,c.`

If the successor colour differs, append two more bits 1-c.
Then place the successor marker. This fills all g_a-1 intermediate
positions and reconstructs the original word uniquely.

Summing gaps gives

`n=E+2T+4 sum_a h_a,`

and hence

`sum_a h_a=H=(D-T)/2.`

This also proves the converse reconstruction from a colour word,
nonnegative gaps h and a first-marker position, subject to the displayed
length relation. Each reconstructed run has at least two bits and its
excess markers are exactly those prescribed.

T is even because a cyclic binary word returns to its starting colour.
Also D is even. If E>0, H=0 means every original run has markers,
so all runs have length at least 3 and the state is frozen.
H>0 means there is an empty length-two run as well as excess bits,
and the run-shift rule supplies a move.
The marker-free and constant cases are frozen separately.

## 3. Exact gap moves

Label markers in their cyclic order. Marker a can move +4 exactly when
h_a>0. It transfers one unit of slack from gap a to gap a-1.
It can move -4 exactly when h_(a-1)>0, with the reverse transfer.

For example, if h_a>0, the four sites after marker a begin with the
unmarked block (1-c),(1-c),c,c. Moving the opposite-colour length-two
run one site left sends the marker to its position +4.
The source run contains the marker and therefore has length at least 3,
so the move is admissible. The reverse case is analogous.
If h_a=0, moving +4 would pass the next marker and is not admissible.

Thus the gap description gives all moves, not merely an invariant.

## 4. Ordered integer lift

Fix the canonical colour sequence c_0,...,c_(E-1).
Put B_0=0 and B_a=sum_(j<a) b_j. Fix an integer residue r modulo 4
and write unwrapped marker positions as

`p_a=r+B_a+4u_a.`

The allowed integer-coordinate region is

`R_H={u in Z^E: u_0<=u_1<=...<=u_(E-1)<=u_0+H}.`

Here h_a=u_(a+1)-u_a for a<E-1, and
h_(E-1)=H+u_0-u_(E-1).
Extend both sequences to all integer indices by

`u_(a+E)=u_a+H,`
`B_(a+E)=B_a+E+2T.`

Then p_(a+E)=p_a+n.

An elementary move changes just one u coordinate by +/-1, provided the
result stays in R_H. It projects to the exact gap move above.
Every base edge lifts uniquely after marker identities and lifts have
been chosen. Its changed bit pair identifies the reversal label uniquely
for n>=5, and that label fixes the signed +/-4 displacement even when
the two signs could agree modulo n. The removed marker identifies its
label in the non-passing ordered sequence.

### Positive diamonds project to allowed square faces

If two distinct coordinate increments are both available, their
combination is also available. Neither increment can invalidate the
other: each inequality involves differences of coordinates, and if
both one-step increments satisfy it then so does doing both.

Both corresponding markers have positive slack immediately after them.
Their clockwise gaps are at least 5, so the three-site windows beginning
at those markers are disjoint. The two original reversals therefore
give an admissible four-state commuting square of X_n.

The positive coordinate diamond is consequently a legitimate homotopy
in the stated base complex, not a newly added relation.

## 5. The ordered lift is connected and its loops contract

These facts use H>0.

### Existence of monotone paths

If u<=v coordinatewise in R_H, there is a path from u to v using only
positive unit increments without exceeding v.

Choose a coordinate needing an increment. If it is blocked by equality
with the next coordinate, that next coordinate also needs an increment,
because v is ordered. At the last coordinate a blocker is
u_(E-1)=u_0+H; validity of v then forces coordinate 0 to need an increment.

Blockers cannot continue around the entire cycle: that would force all
adjacent coordinates equal and also u_(E-1)=u_0+H, contradicting H>0.
Thus an allowed increment exists. Repeat; the remaining coordinate
difference decreases each time.

R_H is closed under coordinatewise maximum: the order inequalities
are preserved, and the maximum last coordinate is at most the maximum
first coordinate plus H. Therefore any two vertices can be connected
through their common coordinatewise maximum.

### Uniqueness of monotone paths up to diamonds

Any two positive paths with the same endpoints differ by positive
commuting diamonds.

Prove this by induction on their common number of increments.
If their first increments agree, remove that step and apply induction.
If they are distinct, both are available initially and form a diamond.
From the upper corner a positive path to the target exists by the
previous argument. Apply induction to compare each original tail
with the route through that corner.

### Arbitrary loop contraction

For the finitely many vertices in a loop, take their coordinatewise
maximum v, which still lies in R_H. Choose a positive path from each
loop vertex to v.

For an edge from u to u+e_a, its edge followed by the chosen path from
u+e_a to v is a positive path from u to v. It is diamond-equivalent to
the chosen path from u to v. The same observation handles a reversed
edge by reversing this homotopy.

Replacing each loop edge in this way makes all paths to v cancel
in succession. The loop contracts using backtracks and positive
diamonds. Every such diamond projects to an existing face of X_n.

Only simple connectivity is proved here. The square complex omits
higher cubes, so contractibility of this two-dimensional lift is
not asserted.

## 6. The phase label and completeness of classification

Let g=gcd(n,4). For a fixed labelled-marker cut, choosing its lifted
position in residue r modulo 4 is possible precisely when its ordinary
position agrees with r modulo g.

Cuts giving the same canonical colour word differ by multiples of l.
A block of l colours returns to its starting colour, so its transition
count is even. Its base gap length is therefore l modulo 4.
Changing the canonical cut shifts its position by l modulo g,
up to multiples of 4.

The ambiguity subgroup in Z/gZ is generated by l. Its quotient has size
gcd(g,l). Because n=E+2T+4H, T is even, and l divides E,

`gcd(g,l)=gcd(n,4,l)=gcd(4,l)=d.`

Therefore rho is independent of the chosen canonical cut.
Moves change a marker position by 4, so rho is invariant.

Conversely, suppose a state has phase rho=r modulo d.
Change its canonical cut by a multiple of l to make its first-marker
position agree with r modulo g. Then add a multiple of n to its lift
to make it agree with r modulo 4. Its markers now give a point of
the same R_H lift with fixed r.

Thus every state with the same (D,chi,rho) is a projection of that
connected lift. All those states are connected.
Different triples cannot be connected by invariance of D, chi and rho.

Spatial translation by one site preserves chi and changes rho by one.
Hence all d phases are realized and have equal component size.

## 7. Return shifts and the fundamental group

Fix a base state and a point u of its ordered lift.
Any other lifted representation of the same state is obtained by an
index shift of its doubly infinite ordered marker sequence:

`p'_a=p_(a+q).`

The candidate q=E adds n to all physical lifts; it is retained only
when it also meets the residue condition below. Thus no separate
physical-translation parameter is needed.
The colour labels agree exactly when q is a multiple of l.

For such q the number of colour transitions across the q-block is even,
so p_(a+q)-p_a is congruent to q modulo 4.
The fixed residue r is retained exactly when q is also a multiple of 4.

Consequently the possible return shifts are

`q in L Z,` `L=lcm(l,4)=4l/d.`

These shifts act by relabelling the ordered lift; they commute with
the lifted moves. Distinct shifts give distinct points because marker
positions increase strictly along the infinite ordered sequence.

### Boundary winding measures the return shift

For a lift of a closed base path ending at shift q,

`sum_(a=0)^(E-1) (p_(a+q)-p_a)=q n.`

For q=1 this is a telescoping sum p_E-p_0=n; iteration gives every
integer q, with negative shifts handled by reversal.

Each elementary move changes the sum of lifted marker positions by
-4 kappa. Thus

`sum_gamma kappa=-q n/4,` `K(gamma)=-q/4.`

In particular, independent squares have zero K (by their local
commutation), so q is unchanged by the defining homotopies of X_n.
The return shift defines a homomorphism from pi_1(C) to LZ.

Every return shift occurs: its endpoint lies in the connected R_H,
so a lifted path to it projects to a base loop.
A loop with zero return shift is a closed loop in the ordered lift,
and contracts there by Section 5. Its projection is null-homotopic
in X_n.

The return-shift homomorphism is therefore an isomorphism

`pi_1(C) ~= L Z ~= Z.`

Abelianizing gives H_1(C;Z)~=Z.
The winding image is K(C)=(L/4)Z=(l/d)Z.
It is nonzero, proving C1.

This argument does not need every base square to be a positive
coordinate diamond. Positive diamonds contract zero-shift loops;
all base squares have zero winding and hence add no nonzero-shift
relation.

## 8. Component size

For a fixed canonical colour sequence there are n first-marker
positions and

`binomial(H+E-1,E-1)`

nonnegative gap vectors of total H.

Every unlabelled state is counted E/l times, once for each marker
cut yielding that same canonical colour sequence. Thus the total
number of states for chi is

`n*l/E * binomial(H+E-1,E-1).`

There are d equally sized components by spatial translation,
giving the stated size formula.

## 9. Limits and verification

- Frozen states remain singleton components.
- The theorem concerns the precise MICRO square complex; a different
  move set, quotient, or face relation requires a new argument.
- pi_1=Z does not assert circle homotopy type or vanishing higher homology.
  Higher cubes were not attached.
- C2 and its potential remain valid; C1 is now proved by a separate
  marker-gap argument.
- No growth functor, smooth projective variety, or Clay Hodge bridge
  has been constructed.
- Broader novelty and independent proof review remain open.

[HODGE-05](../../probes/hodge/HODGE-05.md) records exact JavaScript checks
through n=18, including classifier completeness, size and winding formulas,
gap moves and positive diamonds. The analytic argument above supplies
the all-size conclusion.
