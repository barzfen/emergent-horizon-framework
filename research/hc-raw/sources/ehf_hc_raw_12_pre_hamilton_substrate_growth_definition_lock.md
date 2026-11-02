# EHF-HC-RAW-12 — Pre-Hamilton Substrate Growth Definition Lock
 EHF-HC-RAW-12 — Pre-Hamilton Substrate Growth Definition Lock

## 319.1 Purpose

RAW-11 exposed a genuine foundational fork.

The historical Johnson observable

\[
h(S)=\sum_{i\in S}i
\]

can be interpreted as a first-appearance-rank observable only if the framework carries enough cross-layer structure to distinguish the successive arrivals:

\[
1,2,3,\ldots.
\]

A Hamilton-cycle tower beginning at \(HC_3\) is insufficient because its three seed labels remain \(S_3\)-symmetric.

RAW-12 therefore asks:

> **What is the smallest graded substrate structure that supports unique first-appearance rank while adding no premature Hamilton-cycle, move, metric, probability, or physical structure?**

The preferred conditional definition is a singleton atom filtration beginning at \(V_1\).

The crucial qualification is:

\[
\boxed{
\text{the filtration is additional primitive growth data, not a theorem of static HC geometry}.
}
\]

---

# 320. Static foundation versus graded growth enrichment

To avoid retrofitting chronology into a static object, separate two layers.

## Static HC foundation

At a fixed size \(n\), one may begin with a finite set of distinguishable labels:

\[
V_n,
\qquad
|V_n|=n.
\]

Hamilton-cycle states are then defined when \(n\ge3\).

Nothing in a single static \(V_n\) or \(HC_n\) determines:

- which atom appeared first;
- a total order of atoms;
- a growth arrow;
- a time coordinate.

## CBB graded growth enrichment

For the growth programme, add the coherent tower:

\[
\boxed{
V_1
\overset{\iota_1}{\hookrightarrow}
V_2
\overset{\iota_2}{\hookrightarrow}
V_3
\hookrightarrow\cdots
}
\]

subject to:

\[
\boxed{|V_n|=n}
\]

and:

\[
\boxed{
|V_{n+1}\setminus\iota_n(V_n)|=1.
}
\]

Up to tower isomorphism one may identify every \(\iota_n\) with literal inclusion and write:

\[
V_1\subset V_2\subset\cdots.
\]

This is the **pre-Hamilton substrate growth data**.

---

# 321. What exists below \(n=3\)

For:

\[
n=1,2,
\]

RAW-12 introduces only:

1. the finite atom set \(V_n\);
2. atom identity/equality;
3. the inclusion into the next substrate layer.

It does **not** introduce:

- a Hamilton-cycle state;
- an LR move;
- 2-opt adjacency;
- an edge-overlap metric;
- a Johnson sector;
- probabilities;
- amplitudes;
- energy;
- physical time;
- a complete graph of physical pairwise comparability.

Thus the pre-Hamilton layers are deliberately sparse.

The inclusion:

\[
V_n\hookrightarrow V_{n+1}
\]

means only that earlier atoms persist into the next graded set.

---

# 322. No primitive \(K_n\) is required

The HC state sector should continue to be defined directly as undirected cyclic orderings modulo the dihedral action:

\[
HC(V_n)
=
\{\text{cyclic orderings of }V_n\}/D_n.
\]

Equivalent language using Hamilton cycles of the bookkeeping graph \(K_n\) is allowed, but the complete graph is not added as physical or substrate comparison data.

Thus the graded atom tower does not change the earlier RAW distinction:

\[
\boxed{
\text{label set}
\ne
\text{complete physical comparability graph}.
}
\]

---

# 323. Hamilton-cycle onset threshold

For ordinary simple undirected cycles, the HC state sector first exists at:

\[
\boxed{n=3}.
\]

RAW-12 locks:

\[
\boxed{
HC_n=\varnothing
\quad
(n<3)
}
\]

as a bookkeeping convention, while conceptually saying:

> the Hamilton-cycle state sector is instantiated only for \(n\ge3\).

For:

\[
n\ge3,
\]

\[
\boxed{
|HC_n|
=
\frac{(n-1)!}{2}.
}
\]

Hence:

\[
|HC_3|=1.
\]

No artificial one-cycle or two-cycle is introduced merely to make the growth formula begin earlier.

---

# 324. Substrate growth and HC-state growth are different structures

The atom tower exists for:

\[
n=1,2,3,\ldots.
\]

The HC state-growth map exists only for:

\[
n\ge3.
\]

Let:

\[
x_{n+1}
\]

be the unique new atom:

\[
x_{n+1}
\in
V_{n+1}\setminus V_n.
\]

For:

\[
C\in HC_n
\]

and:

\[
e=\{u,v\}\in E(C),
\]

define:

\[
\Gamma_n(C,e)
\]

by replacing the cycle edge:

\[
\{u,v\}
\]

with:

\[
\{u,x_{n+1}\},
\qquad
\{x_{n+1},v\}.
\]

Then:

\[
\boxed{
\Gamma_n:
\{(C,e):C\in HC_n,\ e\in E(C)\}
\overset{\sim}{\longrightarrow}
HC_{n+1}
}
\]

is a bijection for:

\[
n\ge3.
\]

Deleting \(x_{n+1}\) gives its exact inverse.

So:

\[
\boxed{
\text{atom growth begins at }1,
\qquad
\text{HC all-slot growth begins at }3.
}
\]

There is no all-slot parent for the unique \(HC_3\) state.

---

# 325. Exact all-slot count

Every:

\[
C\in HC_n
\]

has exactly:

\[
n
\]

cycle edges.

Therefore the source of \(\Gamma_n\) has size:

\[
n|HC_n|.
\]

Since:

\[
|HC_n|
=
\frac{(n-1)!}{2},
\]

\[
n|HC_n|
=
\frac{n!}{2}
=
|HC_{n+1}|.
\]

Thus:

\[
\boxed{
n|HC_n|
=
|HC_{n+1}|
}
\]

for every:

\[
n\ge3.
\]

RAW-12 exhaustively re-certified:

\[
3\to4,
\ 4\to5,
\ 5\to6,
\ 6\to7,
\ 7\to8
\]

with:

- complete coverage;
- zero duplicate children;
- exact deletion inverse.

---

# 326. First-appearance stage

For a finite terminal layer \(V_N\), define:

\[
\boxed{
\beta_N(v)
=
\min\{n:v\in V_n\}.
}
\]

Because exactly one atom is added at each stage beginning with:

\[
|V_1|=1,
\]

\[
\beta_N
\]

is a bijection:

\[
\boxed{
\beta_N:V_N\overset{\sim}{\longrightarrow}\{1,\ldots,N\}.
}
\]

Thus every atom has a unique first-appearance stage.

This is the exact structure required by the historical birth-rank coordinate.

---

# 327. Tower isomorphism covariance

Let:

\[
\mathcal V=(V_n,\iota_n)
\]

and:

\[
\mathcal V'=(V_n',\iota_n')
\]

be two singleton towers.

A tower isomorphism is a compatible family of bijections:

\[
\phi_n:V_n\to V_n'
\]

satisfying:

\[
\phi_{n+1}\circ\iota_n
=
\iota_n'\circ\phi_n.
\]

Then:

\[
\boxed{
\beta'(\phi(v))
=
\beta(v).
}
\]

So first-appearance stage is structural data of the graded tower, not of literal symbol names.

---

# 328. Canonical standard tower chart

Define the standard tower:

\[
[1]\subset[2]\subset[3]\subset\cdots,
\]

where:

\[
[n]=\{1,\ldots,n\}.
\]

For every \(V_1\)-seeded singleton tower there is a unique tower isomorphism:

\[
\boxed{
\beta_n:V_n\to[n]
}
\]

sending the atom first appearing at stage \(j\) to:

\[
j.
\]

Therefore, **after the graded tower has been declared**, notation such as:

\[
V_n=[n]
\]

is no longer merely an arbitrary computational labelling.

It is the canonical coordinate chart adapted to first appearance.

This gives a precise repaired interpretation of the historical numerical labels.

---

# 329. Anti-retrofitting theorem: filtration equals total order

The previous result has an important converse.

Fix a terminal \(N\)-element set \(V\).

A maximal singleton filtration:

\[
V_1\subset V_2\subset\cdots\subset V_N=V,
\qquad
|V_n|=n,
\]

is equivalent to a linear order on \(V\).

### From filtration to order

Set:

\[
v_i
=
V_i\setminus V_{i-1},
\]

with:

\[
V_0=\varnothing.
\]

Then:

\[
v_1<v_2<\cdots<v_N.
\]

### From order to filtration

Given:

\[
v_1<v_2<\cdots<v_N,
\]

define:

\[
V_n=\{v_1,\ldots,v_n\}.
\]

The constructions are inverse.

Hence:

\[
\boxed{
\{\text{singleton filtrations on }V\}
\cong
\{\text{linear orders on }V\}.
}
\]

Both sets have size:

\[
\boxed{N!}.
\]

---

# 330. Foundational consequence of the equivalence theorem

The singleton tower does not make total order emerge from a static unordered set.

It **is** total-order information written in growth form.

Therefore the correct statement is:

\[
\boxed{
\text{birth rank is derived from graded growth data}.
}
\]

Do not say:

\[
\boxed{
\text{raw Hamilton cycles force a unique birth order}.
}
\]

They do not.

This is the principal anti-circularity safeguard in RAW-12.

---

# 331. Why the growth formulation may nevertheless be preferable

Although a singleton filtration and total order contain equivalent finite information, their roles in the framework differ.

A bare order says only:

\[
v_1<v_2<\cdots.
\]

A graded tower additionally organizes the dependency of state spaces:

\[
HC(V_3),
HC(V_4),
HC(V_5),
\ldots
\]

and identifies the new atom used by each all-slot growth map.

So for the CBB programme, the tower provides the correct **structural interface** between:

- atom persistence;
- state-space completion;
- deletion;
- reversal-support filtration;
- growth-selected Johnson charts.

The preference for tower language is organizational and modelling-based, not information-theoretic.

---

# 332. Candidate foundations audited

RAW-12 compared five possibilities.

## A. Static \(V_n\) only

Insufficient.

No cross-layer atom identity means no birth history.

## B. HC\(_3\)-seeded singleton filtration

Partially sufficient.

Later birth stages are reconstructed, but the seed retains:

\[
S_3
\]

symmetry.

## C. \(V_1\)-seeded singleton filtration

Sufficient.

Unique first-appearance rank is reconstructed.

This is the preferred **conditional** growth enrichment.

## D. Explicit total order

Also sufficient.

Mathematically equivalent to C on a finite terminal set, but less naturally integrated with HC growth maps.

## E. Literal numeric labels

Rejected as a foundational justification.

Writing:

\[
V_n=\{1,\ldots,n\}
\]

does not by itself prove that the numerals carry structural rank.

That interpretation is licensed only after C or equivalent order data is declared.

---

# 333. Exact relation to the historical Johnson coordinate

At even target layer:

\[
HC_{2k},
\]

RAW-09A uses the newest target atom:

\[
x_{2k}
\]

as the growth-relative anchor.

Removing it leaves the parent atom set:

\[
V_{2k-1}.
\]

Under the canonical tower chart:

\[
\beta:
V_{2k-1}
\overset{\sim}{\longrightarrow}
[2k-1].
\]

Therefore the historical Johnson ground set:

\[
[2k-1]
\]

is recovered exactly.

The historical observable:

\[
h(S)=\sum_{i\in S}i
\]

becomes:

\[
\boxed{
h(S)
=
\sum_{v\in S}\beta(v).
}
\]

So the old \(h\) is now a genuine first-appearance-rank sum **conditional on the \(V_1\)-seeded graded substrate**.

---

# 334. Dependency chain after RAW-12

The rebuilt even branch now has the precise chain:

\[
\boxed{
\text{graded atom tower }V_1\subset V_2\subset\cdots
}
\]

\[
\downarrow
\]

\[
\boxed{
\beta(v)=\text{first-appearance rank}
}
\]

and independently, from:

\[
n\ge3,
\]

\[
\boxed{
HC_n
}
\]

\[
\downarrow
\]

\[
\boxed{
LR3,\ \text{support filtration, all-slot state completion}
}
\]

\[
\downarrow
\]

\[
\boxed{
\text{intrinsic even bipartitions}
}
\]

\[
\downarrow
\]

\[
\boxed{
\text{newest-site growth chart}
}
\]

\[
\downarrow
\]

\[
\boxed{
J(2k-1,k)\ A_1
}
\]

while the rank tower supplies:

\[
\boxed{
h(S)=\sum\beta(v).
}
\]

Only after these two branches meet does the historical Johnson shell transport model appear.

---

# 335. Minimal primitive content

The preferred RAW-12 growth enrichment contains only:

### Atom data

\[
V_n.
\]

### Persistence data

\[
\iota_n:V_n\hookrightarrow V_{n+1}.
\]

### Singleton growth condition

\[
|V_{n+1}\setminus\iota_n(V_n)|=1.
\]

### Cardinality grading

\[
|V_n|=n.
\]

It does not primitive-encode:

- atom adjacency;
- metric;
- cycle state before \(n=3\);
- LR move;
- sector;
- probability;
- amplitude;
- force;
- curvature;
- physical time.

This is the strict definition lock.

---

# 336. Is the grading physical time?

No such claim is made.

The index:

\[
n
\]

is a combinatorial stage/cardinality parameter.

Therefore:

\[
\boxed{
\beta(v)
}
\]

should be called:

- first-appearance stage;
- growth rank;
- birth rank as shorthand.

It should not automatically be called physical time.

Any identification with physical temporal structure would require a separate bridge.

---

# 337. Admissible-comparison status

The graded atom tower is chosen primitive data of the growth framework.

A careful statement is:

> **EHF-HC studies comparison structures built on graded finite sets of distinguishable atoms. In the CBB growth enrichment, atom persistence and one-at-a-time addition are included as primitive cross-layer data. Hamilton-cycle comparison states become available beginning at \(n=3\).**

Avoid saying:

> admissible comparison alone forces the atom tower.

That has not been shown.

Similarly, the finite-set structure does not imply all pairs of atoms are physically comparable.

---

# 338. RAW-12 verdict

The definition lock is:

\[
\boxed{
\mathcal V
=
(V_n,\iota_n)_{n\ge1},
\qquad
|V_n|=n,
\qquad
|V_{n+1}\setminus\iota_n(V_n)|=1.
}
\]

Hamilton-cycle states are instantiated for:

\[
\boxed{n\ge3}.
\]

All-slot HC growth begins at:

\[
\boxed{3\to4}.
\]

First-appearance rank:

\[
\boxed{
\beta(v)=\min\{n:v\in V_n\}
}
\]

is a canonical tower observable and, with a \(V_1\) seed, is injective.

However:

\[
\boxed{
\text{a singleton tower is equivalent to total-order data}.
}
\]

Therefore the unique birth order belongs to the chosen graded growth enrichment, not to static raw HC geometry.

This is the preferred definition because it makes the growth assumptions explicit rather than hiding them in numeric labels.

---

# 339. Computational certification

RAW-12 checked:

- HC state counts for:
  \[
  n=1,\ldots,7;
  \]
- first nonempty HC layer at:
  \[
  n=3;
  \]
- complete all-slot growth:
  \[
  3\to4,\ldots,7\to8;
  \]
- zero duplicate growth children;
- exact deletion inverse;
- singleton-filtration/linear-order count equivalence through:
  \[
  N=10;
  \]
- exact recovery of historical Johnson parent rank sets through:
  \[
  k=10.
  \]

Final result:

\[
\boxed{
59/59
}
\]

strict checks passed.

---

# 340. Recommended status in the overall framework

The clean architecture is now:

## EHF static comparison foundation

Studies:

\[
V_n,
\ HC_n,
\ \text{raw comparison geometry}
\]

at fixed \(n\).

## CBB graded growth enrichment

Adds:

\[
\boxed{
V_1\subset V_2\subset\cdots
}
\]

as chosen primitive growth data.

This produces:

- first-appearance rank;
- canonical newest-site identities;
- coherent all-slot HC completion;
- the historical rank chart needed by Johnson shell observables.

This separation prevents chronology from being silently inserted into the static HC object.

---

# 341. Immediate next question

With the substrate definition now locked, the next natural audit is:

### EHF-HC-RAW-13 — Graded HC Compatibility / Naturality Audit

Prove that every previously certified raw construction is natural with respect to the newly locked atom tower:

- dihedral HC quotient;
- raw overlap;
- reversal-support orbitals;
- LR3;
- deletion/support filtration;
- intrinsic bipartitions;
- growth-selected Johnson \(A_1\);
- first-appearance rank chart.

The purpose would be to verify that RAW-12 changes the **dependency bookkeeping** without changing or contradicting the already certified fixed-layer mathematics.
