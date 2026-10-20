# EHF-HODGE-03 — Run Coordinates and Boundary Winding

Date: 2026-10-20 (Australia/Brisbane)

**Status: PROVED local structural facts; COMPUTATIONAL exact audit through
n=18; two precisely stated working conjectures remain unproved.**

## Question and scope

Why does signed binary transport miss some first-homology cycles in
HODGE-02? Can a rule-based observable detect them, and does the one-cycle
pattern survive a larger audit?

Base commit: `03e2555bc1cd224f6c2f9d769bfff6320c7c33b9`.

The model remains the rooted MICRO microstate complex defined in
[HODGE-02](HODGE-02.md). All claims refer to that model and its square
relations. They do not identify this scalar topology with the RECUR
observer connection or the Clay Hodge conjecture.

## 1. Exact run-coordinate dynamics

A nonconstant valid cyclic word consists of an even number D of alternating
runs, with lengths r_a>=2. Set x_a=r_a-2.

Every admissible non-self length-three reversal shifts a **length-two run**
one position left or right. To move it right, the following run must have
length at least 3; one site is transferred from that donor run to the
preceding run. In run lengths,

`(...,r_(a-1),2,r_(a+1),...) -> (...,r_(a-1)+1,2,r_(a+1)-1,...).`

A left shift is the inverse transfer. In excess coordinates it transfers
one unit between neighbouring same-bit runs, through an intervening run
with x_a=0.

### Proof of the local rule

For a non-self reversal the endpoint bits differ; the middle bit agrees
with one endpoint. Thus it is aa b -> b aa or its reverse.
For the result to avoid a singleton b, the aa must be the whole length-two
run, rather than the end of a longer a-run. For the donor b-run to remain
valid, its length must be at least 3. These conditions also suffice:
the donor remains length at least 2 and the receiver grows.

A complete coordinate chart must retain the ring phase (one run's start)
and a bit label, as well as cyclic run lengths. For D=2, the preceding and
following donor/receiver are the same opposite-bit run: its total length
does not change, but the two-bit run moves around the labelled ring.
A run-length vector alone would erase this motion.

### Frozen-state criterion

A nonconstant state is moving exactly when some run has length 2 and
some run has length greater than 2. In a mixed cyclic list there is a
length-two run next to a longer donor, yielding a move.
If all runs are length 2, there is no donor; if all are longer, there is
no mobile length-two run. Constant states are frozen separately.

For fixed m ones and D runs, the two bit species have excesses

`E_1=m-D,` `E_0=n-m-D,` `E=E_0+E_1=n-2D.`

In every moving component E>0.

The code independently predicts each state's neighbours from run lengths,
without calling the old validity-based move generator for its prediction.
It matches all 15,112 states across sizes 5,...,18.

## 2. The two square rules coincide for all sizes

HODGE-02 observed equality of window-disjoint and endpoint-disjoint
squares through n=12. We can now justify this for every n>=5.

Two length-three windows whose endpoint pairs are disjoint can overlap
only at relative offsets +1 or -1. Up to reversal, consider swaps of
positions (0,2) and (1,3). Non-self moves require the four bits to be

`(a,b,1-a,1-b).`

For each choice of a,b, and external bits e,f, test the original word,
each single swap, and the double swap on the six-bit interval
(e,a,b,1-a,1-b,f). There are only 16 external/local assignments in total.
In every case at least one corner contains a forbidden singleton.
The exact local certificate records:

| Four internal bits | External choices | Choices with all four corners valid |
|---|---:|---:|
| 0011 | 4 | 0 |
| 0110 | 4 | 0 |
| 1001 | 4 | 0 |
| 1100 | 4 | 0 |

For n=5 the two external positions coincide, which only restricts the
tested assignments further. Thus no admissible four-state square has
overlapping windows. Every retained endpoint-square is window-disjoint;
the reverse inclusion is immediate.

This is a finite local proof valid for all n>=5, not an extrapolation from
the larger topology scan.

## 3. Boundary displacement detects what binary displacement can miss

Retain the old cochain

`j(w,tau_i w)=2(w_i-w_(i+2)).`

Define a second one:

`kappa(w,tau_i w)=+1 if w_i=w_(i+1), and -1 otherwise.`

It counts a right/left shift of the moved length-two run, independently
of whether the run consists of 0 or 1 values.

| Elementary shift | j | kappa |
|---|---:|---:|
| Length-two 1-run moves right | +2 | +1 |
| Length-two 0-run moves right | -2 | +1 |
| Reverse either move | Negate the corresponding value | -1 |

Therefore binary transport can cancel while boundary motion accumulates.

### All-size closedness

Kappa reverses sign under edge reversal. On every retained square the
windows are disjoint, so one move does not alter the other's local kappa
value. Its square circulation is zero: d1 kappa=0.

### All-size integer boundary winding

Let P_01(w) be the sum of the labels of edges carrying a 0-to-1 transition.
Each elementary run shift moves exactly one such boundary one site in
the corresponding direction. Therefore

`kappa(w,v) - (P_01(v)-P_01(w)) is a multiple of n.`

On a closed path the P_01 terms telescope, so sum kappa is an integer
multiple of n. The integer sum kappa/n is independent of the ring seam.
Rotation preserves kappa, reflection negates it, and bit complement
preserves it (while negating j). These symmetries are checked on all
scanned edges.

Kappa defines a class in ordinary H^1, using the stated square relations.
It is not a Hodge (p,p) class or a quantum phase.

## 4. Exact exhaustive audit

The code audits every valid state, edge, and commuting square for each
n=5,...,18. It computes per-component face-boundary rank over Q using
the integer elimination routine from HODGE-02, then computes all fundamental
graph-cycle periods of both cochains.

| n | States | Edges | Moving components | Total square beta1 | Components missed by j |
|---|---:|---:|---:|---:|---:|
| 5 | 12 | 10 | 2 | 2 | 0 |
| 6 | 20 | 12 | 2 | 2 | 0 |
| 7 | 30 | 14 | 2 | 2 | 0 |
| 8 | 46 | 16 | 2 | 2 | 0 |
| 9 | 74 | 36 | 4 | 4 | 0 |
| 10 | 122 | 80 | 6 | 6 | 2 |
| 11 | 200 | 154 | 6 | 6 | 0 |
| 12 | 324 | 264 | 16 | 16 | 4 |
| 13 | 522 | 442 | 10 | 10 | 0 |
| 14 | 842 | 756 | 18 | 18 | 4 |
| 15 | 1362 | 1320 | 14 | 14 | 0 |
| 16 | 2206 | 2304 | 48 | 48 | 10 |
| 17 | 3572 | 3978 | 22 | 22 | 0 |
| 18 | 5780 | 6804 | 48 | 48 | 10 |

Across 200 moving components:
- Every component has beta1_Q=1.
- Kappa has a nonzero period on every component.
- J misses 30 components; kappa detects all 30.
- On every component, the periods obey the finite identity below.

Because a scanned component has one-dimensional rational H_1, a nonzero
period map detects its entire rational first-homology direction.
This does not detect integral torsion or classify the fundamental group.
Kappa/n is not always a primitive integral coordinate: some n=11
components have winding image 3Z.

### Explicit missed cycle

At n=10, the retained witness starts at 0110011100, with run lengths
(2,2,3,3), m=5 ones and D=4 runs. It returns after ten moves:

`sum j=0,` `sum kappa=-10.`

Thus binary winding is zero while boundary winding is -1.
The full word-by-word loop is retained in the JSON.

## 5. A quantitative period pattern

Every scanned moving component satisfies

`(n-2D) sum_gamma j = 2(n-2m) sum_gamma kappa`

on every fundamental graph cycle, hence on every loop in that finite graph.

Equivalently, for a nonzero boundary period,

`sum j / sum kappa = 2(n-2m)/(n-2D).`

This is checked with exact integers and rational numbers, including zero
period cycles. It is not inferred from a floating-point regression.
For m=n/2 the factor vanishes; this quantitatively explains all the
scanned components missed by signed binary transport.

An all-size proof is still absent. In particular, the run-coordinate
rewrite alone does not prove that this weighted cochain difference is
exact for every n.

## 6. Working conjectures, precisely stated

[CONJECTURES.md](../../formal/hodge/CONJECTURES.md) locks two separate claims:

- **EHF-HODGE-C1:** every moving component has one rational first-homology
  direction, detected by boundary winding.
- **EHF-HODGE-C2:** the binary/boundary cohomology classes satisfy
  (n-2D)[j]=2(n-2m)[kappa].

Both quantify over every n>=5 and use the exact complex of this audit.
Both have finite support through n=18; neither is proved here.
We have formulated EHF working conjectures, not established that they
are new to mathematics.

C1 does not claim that every component is homotopy equivalent to a circle.
C2 does not follow from beta1=1 without an additional coefficient argument.

## 7. Literature comparison and novelty boundary

Abrams and Ghrist's *State complexes for metamorphic robots*
(arXiv:cs/0307004, 2003) explicitly builds square cells for commuting local
moves and higher cubes for compatible independent moves. The construction
of a complex from a move graph is therefore established mathematics,
not an EHF invention.

Our MICRO complex retains only its stated square relations. Applying
general results about full state complexes requires matching their
legality/support definitions and higher cells. In particular, no CAT(0)
or nonpositive-curvature theorem is imported here.

The paper's distinction between the support needed to determine legality
and the sites actually changed is relevant to a future comparison.
Checking four corners of a square is not itself an all-dimensional
compatibility proof.

A preliminary targeted literature search did not establish an existing
classification for this exact MICRO model. That is not evidence of
originality. A complete comparison with reconfiguration and constrained
transport models remains necessary.

Primary source consulted:
https://arxiv.org/abs/cs/0307004
Full text:
https://arxiv.org/pdf/cs/0307004

## 8. Evidence ledger

**PROVED within this model:**
- Run-coordinate move characterization and frozen-state criterion.
- Equality of endpoint/window square rules.
- Closedness of kappa and integral boundary winding.
- The existing adjacent-pair family supplies nonzero boundary periods
  for every n>=5, as a special family rather than every moving component.

**COMPUTATIONAL, exact finite:**
- Full scans through n=18; all 200 moving components satisfy C1 and C2.
- The second observable detects all 30 components missed by j.
- Run-neighbour predictions and cochain symmetry checks pass.

**CONJECTURE:**
- C1 and C2 for arbitrary sizes.

**UNESTABLISHED:**
- Novelty, all-size component classification, integral torsion,
  homotopy type, compatible growth, and a Clay Hodge bridge.

## 9. Reproduce and next step

```sh
python -m pip install -r code/hodge/requirements.txt
OPENBLAS_NUM_THREADS=1 python code/hodge/hodge_03_audit.py --output data/hodge/hodge-03-results.json
```

[Code](../../code/hodge/hodge_03_audit.py).
[Results](../../data/hodge/hodge-03-results.json).
The script imports hodge_02_audit.py from the same directory.
It retains counterexamples if C1 or C2 fails at a requested larger size;
it does not assume those conjectures in computing ranks or periods.
Default --max-n is 18. All topology and period checks in HODGE-03 are
exact; no new floating-point Hodge projection is used.

**HODGE-04 — Period-identity proof audit.**
Seek an explicit state potential F_C satisfying

`dF_C=(n-2D)j-2(n-2m)kappa.`

Constructing that potential analytically, or finding an all-size
alternative, would prove C2 independently of C1. Investigate how cyclic
run order and the retained root phase constrain possible components;
do not replace the missing proof with a larger finite scan.
