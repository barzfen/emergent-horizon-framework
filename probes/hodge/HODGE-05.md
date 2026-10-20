# EHF-HODGE-05 — Component Invariant and Classification Audit

Date: 2026-10-21 (Australia/Brisbane)

**Status: PASS — written all-size classification and C1 proof within the
specified MICRO square complex; exact bounded checks through n=18.**
Independent proof review, formal verification and novelty assessment remain open.

Base commit: `94781dbf8ad03bbf7419bf3ea7c834a72c810e7b`.

## Main conclusions

[The complete argument](../../formal/hodge/COMPONENT-CLASSIFICATION.md)
gives a component classifier for every moving state:

`(D,chi,rho),`

where D is the run count, chi is the cyclic excess-marker colour word,
and rho is a canonical marker position modulo

`d=gcd(4,l),`

with l the primitive period length of chi.

The colour word alone is not sufficient. The extra modulus can be 1,
2 or 4, and is derived from the four-site marker motion rather than
chosen to fit the counts.

For each moving component C, the argument proves

`pi_1(C) ~= Z,` `H_1(C;Z) ~= Z,`

and the exact boundary-winding image is

`(l/d)Z.`

This proves C1, strengthens its first-homology assertion to integral
coefficients, and explains nonprimitive winding values seen earlier.
It does not claim that the two-dimensional complex is homotopy
equivalent to a circle.

## 1. Why the necklace alone fails

At n=10, D=4 and chi=01, the primitive period is l=2.
There are two components, distinguished by canonical marker-position parity.

| Representative | Phase modulo 2 | Vertices |
|---|---:|---:|
| 1110011000 | 1 | 10 |
| 0111001100 | 0 | 10 |

Both have the same marker necklace and aggregate bit counts.
Local moves shift a marker by 4 and cannot change this phase.

Frozen states are not grouped by this moving-state invariant.
They remain separate singleton components.

## 2. The exact gap model

Consecutive markers with colours c_a,c_(a+1) have distance

`1+2*[c_a differs from c_(a+1)]+4h_a,` `h_a>=0.`

The gaps reconstruct the entire word. Their slack total is

`H=sum h_a=(D-T)/2,`

where T is the cyclic colour-change count of chi.
Moving states have H>0.

A marker moves +4 when its following gap has positive slack, transferring
one slack unit to its preceding gap. The reverse move transfers it back.
This is an exact representation of all original moves.

After choosing marker labels and a residue r modulo 4, the unwrapped
coordinates lie in

`R_H={u in Z^E: u_0<=...<=u_(E-1)<=u_0+H}.`

Moves increment or decrement one coordinate.
Positive diamonds project to existing commuting squares.

## 3. Proof mechanism

The ordered lift is connected. Any two coordinate vectors can reach
their coordinatewise maximum by positive moves.

Any two positive paths with the same endpoints differ by commuting
diamonds. Choosing a common upper bound for all vertices in a loop
then contracts every zero-return loop.

A closed path downstairs can return upstairs with a cyclic marker-index
shift q. Preserving both the colour word and the coordinate residues
requires

`q in lcm(l,4) Z.`

These shifts form an infinite cyclic group. Each allowed return shift
is realized, and a zero shift contracts in the lift.
This proves the fundamental-group statement.

The boundary winding of a return shift is K=-q/4, yielding image
(l/d)Z. No C2 assumption is needed for this argument.

## 4. Independent exact finite checks

A pure JavaScript audit independently enumerates all states and moves.
It compares BFS components against the proposed labels and verifies:
- Marker-gap reconstruction and exact gap-move correspondence.
- Independence of the chosen canonical cut modulo d.
- Completeness of the classifier, not just constancy on components.
- The component-size formula.
- Boundary-winding images from integer spanning-tree periods.
- Positive diamonds as valid disjoint-window squares.

| n | States | Moving necklaces | Moving components | Phase moduli present |
|---|---:|---:|---:|---|
| 5 | 12 | 2 | 2 | 1 |
| 6 | 20 | 2 | 2 | 1 |
| 7 | 30 | 2 | 2 | 1 |
| 8 | 46 | 2 | 2 | 1 |
| 9 | 74 | 4 | 4 | 1 |
| 10 | 122 | 5 | 6 | 1,2 |
| 11 | 200 | 6 | 6 | 1 |
| 12 | 324 | 7 | 16 | 1,4 |
| 13 | 522 | 10 | 10 | 1 |
| 14 | 842 | 12 | 18 | 1,2 |
| 15 | 1362 | 14 | 14 | 1 |
| 16 | 2206 | 17 | 48 | 1,2,4 |
| 17 | 3572 | 22 | 22 | 1 |
| 18 | 5780 | 29 | 48 | 1,2 |

Across 15,112 states and 16,190 edges, all checks pass.
There are 200 moving components and 4,392 positive diamonds checked.

For every component, the size is exactly

`n*l/(E*d) * binomial(H+E-1,E-1).`

The component size, m, D and winding-image records agree with all 200
records retained from HODGE-03. This audit does not independently
recompute those earlier rational H1 ranks; its new tests concern the
classifier and lift, while the written proof supplies the all-size
topological conclusion.

Additional finite controls test 24 ordered-coordinate regions
(E=1,...,6 and H=1,...,4) within coordinate window 0,...,3:
11,451 comparable endpoint pairs admit the predicted monotone paths,
and 785 positive diamonds remain valid.
These controls support implementation/proof-boundary checks, not an
extrapolation to all sizes.

## 5. Execution and reproduction

The terminal execution environment was unavailable in this session.
The pure audit functions were executed in the available JavaScript
tool runtime. No Python or terminal run is claimed for HODGE-05.

The same pure functions are packaged with a Node entry point:

```sh
node code/hodge/hodge_05_audit.mjs > data/hodge/hodge-05-results.json
```

An optional positional maximum n from 5 to 22 can be supplied; the
retained run uses 18. Only sizes through 18 are claimed here.
The Node wrapper was not terminal-tested. No external packages are needed.

[Source](../../code/hodge/hodge_05_audit.mjs).
[Results](../../data/hodge/hodge-05-results.json).
The retained result adds execution notes and the comparison against
the earlier dataset; a standalone rerun reproduces the mathematical
audit fields rather than those historical annotations.

## 6. Correction to HODGE-02

The earlier report described a zero-binary-winding example at n=10
as having 15 vertices and 20 edges. That description was incorrect.

The two balanced zero-j components have 10 vertices and 10 edges.
The retained HODGE-03 data and the independent HODGE-05 enumeration
agree on this correction. The mistaken paragraph has been corrected;
no retained numerical dataset was changed.

## 7. Evidence and limits

- **PROVED within the specified model:** moving-component classification,
  component-size formula, fundamental group Z, integral first homology Z,
  and exact boundary-winding image.
- **COMPUTATIONAL, exact finite:** classifier and formula checks through
  n=18, plus bounded controls on the ordered-coordinate lemmas.
- **UNCHANGED:** C2 and its explicit potential.
- **OPEN:** independent review, formal verification, broader novelty,
  higher homology, higher-cube completion and growth compatibility.
- **UNESTABLISHED:** a bridge to the Clay Hodge conjecture.

The result is a classification theorem about this constrained move
system. It is not an identification of these components with smooth
projective varieties.

## Next: HODGE-06 — Higher-cell completion audit

Determine how adding compatible higher cubes changes the homotopy type.
The present square-only complex can have higher topology even though
its fundamental group is Z. Keep that question separate from the
already established first-homology classification.
