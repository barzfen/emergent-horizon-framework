# EHF-HC-RAW-14 — Primitive Data / Redundancy / Dependency-Minimality Audit
 EHF-HC-RAW-14 — Primitive Data / Redundancy / Dependency-Minimality Audit

## 363.1 Purpose

RAW-01 through RAW-13 established a large amount of exact structure.

That success creates a danger:

> once many useful objects exist, it becomes easy to forget which ones were actually assumed and which ones were derived.

RAW-14 therefore treats the rebuilt framework as a dependency problem.

For each object it asks:

1. Is it primitive data?
2. Is it a state-space ansatz?
3. Is it a modelling choice?
4. Is it derived?
5. Is it merely a coordinate/chart?
6. Is it an optional transport or metric convention?
7. What fails if it is removed?

The goal is not to minimize the number of words in the foundation.

The goal is to eliminate **logical redundancy and circular dependence**.

---

# 364. There is no single universal primitive package

The first conclusion is methodological.

Different questions require different amounts of structure.

A static fixed-\(n\) HC theorem does not require growth history.

A graded growth theorem does not require unique birth ranks.

Johnson \(A_1\) does not require probabilities.

Ollivier shell curvature requires substantially more analytical structure than raw HC geometry.

Therefore RAW-14 replaces the idea of one monolithic foundation with a nested family of dependency packages.

---

# 365. Static structural core

The static fixed-layer package requires only:

### Primitive/ansatz S1 — finite atoms

A finite set:

\[
V_n.
\]

### Primitive/ansatz S2 — Hamilton-cycle state construction

For:

\[
n\ge3,
\]

take:

\[
\boxed{
HC(V_n)
=
\{\text{undirected cyclic orderings of }V_n\}/D_n.
}
\]

From this pair alone one derives:

- cycle edge incidence;
- raw overlap;
- edge symmetric-difference distance;
- the nearest nontrivial shell;
- all reversal-support classes;
- the structural LR3 class;
- intrinsic even bipartitions;
- the intrinsic even sector space.

Thus the static structural core is:

\[
\boxed{
\text{finite atoms}
+
\text{HC cyclic-state ansatz}.
}
\]

No growth history is required.

---

# 366. Edge incidence is not primitive

Given a cyclic state:

\[
C=(c_0,\ldots,c_{n-1}),
\]

its unordered edge set is:

\[
\boxed{
E(C)
=
\{
\{c_i,c_{i+1}\}
:
i\in\mathbb Z_n
\}.
}
\]

Therefore:

\[
E(C)
\]

contains no additional information beyond the HC state.

It should remain derived.

---

# 367. Raw overlap and raw distance are not primitive

Once:

\[
E(C)
\]

and:

\[
E(D)
\]

are known,

\[
o(C,D)
=
|E(C)\cap E(D)|
\]

and:

\[
d_E(C,D)
=
\frac12|E(C)\triangle E(D)|
=
n-o(C,D)
\]

are exact derived observables.

Thus neither overlap nor distance should appear in the primitive data.

They are canonical comparisons built from state incidence.

---

# 368. \(K_n\) remains unnecessary

The bookkeeping phrase:

> Hamilton cycles of \(K_n\)

is mathematically equivalent to the cyclic-order definition.

But RAW-14 confirms that no primitive complete graph is needed.

The foundation does not require:

\[
\boxed{
K_n
}
\]

as substrate geometry.

This protects the distinction:

\[
\text{all possible bookkeeping edges}
\ne
\text{all physically admissible pairwise comparisons}.
\]

---

# 369. 2-opt is derived

RAW-02 established:

\[
\boxed{
d_E(C,D)=2
}
\]

as the nearest possible nonzero raw HC distance.

This shell is exactly the usual 2-opt shell.

Therefore:

\[
\boxed{
2opt
=
\text{nearest nontrivial raw comparison shell}.
}
\]

No separate 2-opt primitive is necessary.

---

# 370. Reversal-support labels are derived pair geometry

RAW-04B showed that a nearest-shell reversal pair has common-path vertex sizes:

\[
\{\ell,n-\ell\}.
\]

Hence the support parameter:

\[
\ell
\]

is intrinsically recoverable from the pair.

Therefore the structural relations:

\[
LR_\ell
\]

need not be inserted as primitive labels.

They are a classification of raw nearest-shell pairs.

In particular:

\[
\boxed{
LR3
}
\]

exists as a structural relation whether or not the framework chooses it as a dynamics/admissibility rule.

This distinction is crucial.

---

# 371. Structural LR3 versus selected LR3

RAW-14 separates:

### Structural LR3

The exact pair relation:

\[
LR3\subset HC_n\times HC_n.
\]

This is derived from raw HC pair geometry.

### Selected LR3

The modelling assertion:

> LR3 is the preferred or admissible same-layer move rule.

This is **not** derived from raw HC alone.

RAW-05B proved the no-go result:

\[
\boxed{
\text{nearest-shell covariance alone does not uniquely select LR3}.
}
\]

Therefore selecting LR3 requires an additional modelling choice.

---

# 372. Two legitimate LR3 packages

There are two logically clean ways to handle selection.

## Direct package

Declare:

\[
\boxed{
LR3
}
\]

to be the chosen admissible move relation.

This is the logically shortest package.

## Principle-based package

Within the audited nearest-shell reversal-orbital candidate class, impose:

- preservation of intrinsic even bipartition;
- strict reversal locality / inclusion minimality.

Then the selected rule is:

\[
\boxed{LR3}.
\]

This package contains more assumptions but gives an explanatory reason for the choice.

Do not include both packages and then count both as necessary primitives.

They are alternatives.

---

# 373. The graded structural core is leaner than RAW-12's full tower

For the coherent HC growth programme, the required growth data are:

\[
\boxed{
V_3
\subset
V_4
\subset
V_5
\subset\cdots
}
\]

with one persistent new atom added per stage.

Call this the **HC\(_3\)-seeded singleton tower**.

Together with the HC state-space ansatz, it is sufficient to derive:

- newest-atom deletion;
- all-slot insertion;
- exact growth bijection;
- reversal-support filtration;
- intrinsic even sectors;
- newest-site Johnson charts;
- horizontal/vertical LR2 classification;
- ordinary Johnson \(A_1\).

Thus:

\[
\boxed{
\text{HC growth}
+
\text{Johnson }A_1
}
\]

do not require:

\[
V_1
\quad\text{or}\quad
V_2.
\]

This is one of the main minimization results of RAW-14.

---

# 374. All-slot growth is not primitive

Given:

1. a persistent singleton tower;
2. a target newest atom:
   \[
   x_{n+1};
   \]
3. the HC cyclic-state definition;

deleting \(x_{n+1}\) from an \((n+1)\)-cycle is canonical.

Its inverse consists exactly of inserting \(x_{n+1}\) into one parent cycle edge.

Therefore the all-slot relation:

\[
HC_n\times\{\text{cycle edges}\}
\cong
HC_{n+1}
\]

is derived.

The phrase:

> all-slot growth principle

may remain useful conceptually, but the actual map does not need to be independently primitive once the tower and HC state construction are fixed.

---

# 375. Support filtration is derived

Once:

- reversal-support classes;
- newest-site deletion;

exist, RAW-07's law:

\[
LR_\ell^{(N)}
\to
LR_\ell^{(N-1)}
\cup
LR_{\ell-1}^{(N-1)}
\]

is a theorem.

No separate filtration primitive is required.

The filtration is a property of deletion acting on structural reversal classes.

---

# 376. Intrinsic sectors are derived

For even:

\[
n=2m,
\]

the graph underlying each HC state is an even cycle and therefore has a unique bipartition up to block swap.

Thus:

\[
\Pi_{\rm intr}(C)
\]

is derived.

The sector space:

\[
\mathcal B_m
\]

is likewise derived.

No parity label or sector identifier needs to be primitive.

---

# 377. Johnson vertex space is derived

RAW-08B showed:

\[
\mathcal B_m
\]

is the intrinsic unordered equal-bipartition space.

A distinguished newest site gives a canonical chart into a fixed-size subset space.

Therefore the Johnson vertex set is:

\[
\boxed{
\text{derived from intrinsic sectors + growth anchor}.
}
\]

It should not be inserted as a primitive target graph.

This is important for the queued graph-emergence branch.

---

# 378. Johnson \(A_1\) is derived

RAW-09A established:

\[
\boxed{
A_1
=
\text{sector image of horizontal/parent-changing target }LR2.
}
\]

Since structural:

\[
LR2
\]

already exists inside the raw nearest shell, and horizontal status is defined by newest-site deletion,

\[
A_1
\]

requires no independent adjacency axiom.

Therefore:

\[
\boxed{
\text{Johnson }A_1
}
\]

is derived from:

- HC pair geometry;
- one-site growth structure;
- intrinsic sectors.

It does not require LR3 to be selected as the dynamics.

---

# 379. LR3 selection is not required for Johnson emergence

This point deserves explicit separation.

The chain:

\[
HC
\to
\text{sectors}
\to
LR2_{\rm horizontal}
\to
A_1
\]

is structural.

It exists whether or not:

\[
LR3
\]

has been selected as the admissible same-layer rule.

The separate relation:

\[
LR3
\overset{\text{deletion}}{\longrightarrow}
LR2
\]

explains how the selected LR3 layer exposes the lower-support channel under growth.

But Johnson \(A_1\) itself does not logically depend on that selection.

Thus:

\[
\boxed{
\text{Johnson emergence}
\ne
\text{LR3-selection theorem}.
}
\]

They are related branches of the same substrate, not one axiom chain.

---

# 380. Pre-Hamilton \(V_1,V_2\) are optional rank refinement

RAW-12 introduced:

\[
V_1\subset V_2\subset V_3\subset\cdots
\]

to reconstruct unique historical birth ranks.

RAW-14 shows precisely what that extension is needed for.

Removing:

\[
V_1,V_2
\]

does **not** destroy:

- static HC geometry;
- LR support;
- LR3;
- all-slot HC growth from \(3\to4\) onward;
- support filtration;
- intrinsic sectors;
- Johnson vertex emergence;
- Johnson \(A_1\).

It destroys only the unique resolution of the three HC\(_3\) seed atoms and therefore the exact historical weight system:

\[
1,2,3,4,\ldots.
\]

Thus:

\[
\boxed{
V_1,V_2
}
\]

belong in a **rank-refined growth extension**, not in the logically minimal HC-growth core.

---

# 381. Unique birth rank is an extension output

If the singleton tower is extended to:

\[
V_1,
\]

then:

\[
\beta(v)
=
\min\{n:v\in V_n\}
\]

is injective.

Hence:

\[
\boxed{
\beta:V_N\to[N].
}
\]

But \(\beta\) should remain derived.

It is not separate primitive data.

The primitive content is the rank-refined tower itself.

---

# 382. Cardinality grading is partly redundant

If one declares:

\[
|V_1|=1
\]

and every inclusion adds exactly one new atom:

\[
|V_{n+1}\setminus V_n|=1,
\]

then induction gives:

\[
\boxed{
|V_n|=n.
}
\]

Therefore it is unnecessary to list both:

- singleton increment;
- \(|V_n|=n\);

as logically independent axioms.

One may use \(|V_n|=n\) as notation/normalization of the stage index, but it should not be counted twice in the primitive ledger.

---

# 383. Numeric labels are coordinate charts

At a fixed static layer, notation:

\[
V_n=[n]
\]

is merely a convenient chart.

In the rank-refined tower, first appearance gives a canonical chart:

\[
\beta:V_n\to[n].
\]

Thus literal numbers are never independent primitive atom properties.

They are either:

- arbitrary static coordinates;
- derived growth coordinates.

---

# 384. Uniform Johnson probabilities are optional

The structural graph:

\[
J(2k-1,k)
\]

does not determine a unique stochastic process merely because it is regular.

The historical transport branch chooses:

\[
\boxed{
P(S,T)
=
\frac1{k(k-1)}
}
\]

for every:

\[
A_1\text{ neighbour }T.
\]

This is a natural neutrality convention, but it remains an analytical choice.

Removing it leaves:

- the Johnson graph;
- its adjacency algebra;
- spectra;
- structural sector relations;

fully intact.

It removes only results whose definitions use a random walk expectation.

---

# 385. Uniform shell averaging is optional

RAW-10A and RAW-10D proved that:

\[
h
\]

is not strongly lumpable.

Therefore the shell kernel:

\[
K(h,h')
\]

requires an explicit conditional averaging prescription.

The historical choice is uniform averaging over states in shell \(h\).

This may equivalently be interpreted as conditioning the uniform stationary ensemble.

But it is not implied by strong Markov projection.

Thus:

\[
\boxed{
\text{uniform shell averaging}
}
\]

belongs to the analytical extension, not the structural foundation.

---

# 386. The shell line metric is optional

The Ollivier audit chooses:

\[
d(h,h')
=
|h-h'|.
\]

This metric is natural for the integer birth-rank coordinate, but it is still a declared metric on the coarse observable space.

Removing it does not alter:

- HC geometry;
- Johnson geometry;
- transport transition probabilities.

It removes only that particular transport-curvature calculation.

Therefore:

\[
\boxed{
\text{shell line metric}
}
\]

is an optional metric convention.

---

# 387. Minimal package table

RAW-14 identifies the following sufficient and deletion-minimal packages for the stated output bundles.

| Package | Primitive / chosen inputs | Main derived outputs |
|---|---|---|
| Static structural core | finite \(V_n\) + HC cyclic-state ansatz | overlap, 2-opt, \(LR_\ell\), structural LR3, bipartitions |
| Graded structural core | HC state ansatz + HC\(_3\)-seeded singleton tower | all-slot growth, support filtration, Johnson \(A_1\) |
| LR3 direct model | graded core + direct LR3 choice | selected LR3 model |
| LR3 principle model | graded core + audited preservation/locality principles | selected LR3 model |
| Rank-refined extension | graded core + extension to \(V_1,V_2\) | unique \(\beta\), historical \(h\) |
| Johnson transport | rank-refined extension + uniform \(A_1\) weighting | exact stochastic drift/diffusion |
| Shell-curvature extension | Johnson transport + shell averaging + line metric | historical shell Ollivier curvature |

Each package was deletion-tested against its target bundle.

---

# 388. Logical minimality versus explanatory minimality

RAW-14 exposes an important distinction.

The logically shortest way to obtain a selected move rule is:

\[
\boxed{
\text{declare LR3 selected}.
}
\]

But that does not explain why LR3 is chosen.

The principle-based route adds assumptions but provides explanatory structure:

\[
\text{even preservation}
+
\text{strict locality/minimality}
\Longrightarrow
LR3
\]

within the audited reversal-orbital candidate class.

Therefore:

\[
\boxed{
\text{logical minimality}
\ne
\text{explanatory minimality}.
}
\]

Both packages should remain available, clearly labelled.

---

# 389. The genuinely primitive choices

After removing redundancies, the HC programme contains only a few genuine modelling choices.

## Static state-space choice

Use undirected cyclic orderings modulo dihedral presentation as the comparison states.

This is not derived from finite atoms alone.

## Graded-growth choice

If studying CBB growth, retain persistent one-at-a-time atom addition.

This is not derived from static HC geometry.

## Move-selection choice

If LR3 is to be interpreted as the admissible same-layer rule, choose it directly or adopt explicit selection principles.

## Transport choice

If a stochastic Johnson model is desired, specify neighbour weighting.

## Coarse metric choice

If shell Ollivier curvature is desired, specify shell averaging and a metric.

Everything else in the current structural spine is derived from these layers.

---

# 390. What is not a primitive anymore

The following should not appear in a minimal primitive list:

- \(K_n\);
- raw overlap;
- \(d_E\);
- 2-opt;
- \(LR_\ell\) labels as external data;
- intrinsic bipartition sectors;
- all-slot insertion as an independent map;
- support filtration;
- Johnson vertex set;
- Johnson \(A_1\);
- birth rank \(\beta\);
- historical \(h\);
- restoring drift;
- Ollivier curvature.

All are derived or convention-dependent.

---

# 391. Acyclic dependency result

RAW-14 encoded the current dependency relations as a directed graph.

The AND-dependency graph is acyclic.

LR3 selection has two explicit alternative parent packages rather than a circular derivation.

Thus no current certified node depends on itself, directly or indirectly.

The rebuilt dependency structure is therefore a genuine DAG.

This is important because several historical narratives had blurred:

- Johnson geometry;
- LR3 selection;
- parity sectors;
- birth rank;

in ways that could sound circular.

The current graph separates them.

---

# 392. Lean structural DAG

The core structural DAG can be written:

\[
\boxed{
\text{finite atoms}
\to
HC_n
}
\]

then:

\[
HC_n
\to
E(C)
\to
\text{raw overlap}
\to
2opt
\to
LR_\ell,
\]

and independently:

\[
HC_{2m}
\to
\Pi_{\rm intr}
\to
\mathcal B_m.
\]

The graded branch adds:

\[
\boxed{
V_3\subset V_4\subset\cdots
}
\]

giving:

\[
\text{newest-site deletion}
\to
\text{all-slot growth},
\]

\[
LR_\ell
+
\text{deletion}
\to
\text{support filtration},
\]

and:

\[
\mathcal B_m
+
\text{newest site}
+
LR2
\to
A_1.
\]

No birth-rank assumption is present in this lean structural branch.

---

# 393. Rank-refined DAG

Only if the historical shell coordinate is desired do we extend:

\[
V_3\supset V_2\supset V_1
\]

in the reverse reading, equivalently:

\[
V_1\subset V_2\subset V_3\subset\cdots.
\]

Then:

\[
\boxed{
\text{rank-refined tower}
\to
\beta
\to
h.
}
\]

This branch meets the Johnson structural branch only at the observable layer.

Therefore the historical shell coordinate is not needed to derive the Johnson graph itself.

---

# 394. Transport DAG

The transport branch is:

\[
A_1
+
\text{uniform neighbour weighting}
\to
\text{Johnson walk}.
\]

Then:

\[
\text{Johnson walk}
+
h
\to
\text{exact drift/diffusion}.
\]

Then:

\[
\text{walk}
+
h
+
\text{uniform shell averaging}
\to
K(h,h').
\]

Finally:

\[
K
+
|h-h'|
\to
\text{shell Ollivier curvature}.
\]

Each extra step is explicitly optional.

---

# 395. RAW-14 deletion results

The deletion audit gives several high-value results.

### Remove HC state ansatz

Almost all HC-derived structure disappears.

Therefore it is genuinely essential.

### Remove HC\(_3\)-seeded tower

Static HC mathematics survives.

But:

- all-slot growth;
- support filtration;
- Johnson \(A_1\);

lose their current graded derivation.

### Remove \(V_1,V_2\) extension

All structural HC-growth and Johnson results survive.

Lost:

- unique birth rank;
- historical \(h\);
- rank-based transport/curvature branch.

### Remove LR3 direct choice

Nothing is lost if the principle-based selection package remains.

### Remove LR3 principles

Nothing is lost if the direct LR3 choice remains.

Thus those are true alternatives.

### Remove uniform \(A_1\) weighting

Structural Johnson \(A_1\) survives.

Stochastic drift and shell-curvature analysis do not.

### Remove shell averaging or line metric

Only the shell-curvature extension is lost.

---

# 396. Recommended foundation architecture

RAW-14 recommends three nested layers.

## Layer A — Static HC structural theory

Primitive/ansatz:

- finite atoms;
- HC cyclic-state construction.

Everything fixed-layer is derived from there.

## Layer B — CBB graded HC growth

Add:

- HC\(_3\)-seeded singleton persistence/growth.

This is sufficient for:

- deletion;
- all-slot completion;
- support filtration;
- Johnson emergence.

## Layer C — Rank-refined history extension

Optionally extend growth down to:

\[
V_1.
\]

This is required only for:

- unique birth rank;
- historical \(h\);
- its particular shell geometry.

Transport and metric conventions sit downstream of Layer C rather than inside the structural foundation.

---

# 397. Consequence for the book / explanatory narrative

A clean conceptual narrative is now possible without pretending every later object was present at the beginning.

One can say:

1. begin with distinguishable atoms;
2. choose cyclic comparison states;
3. derive raw pair geometry;
4. if growth is added, derive coherent deletion/completion;
5. derive sector and Johnson structures;
6. only if cumulative rank history is retained, define birth-rank observables;
7. only if stochastic weighting is chosen, discuss drift/diffusion;
8. only after a coarse metric is chosen, discuss Ollivier curvature.

This ordering mirrors the actual dependency DAG.

---

# 398. RAW-14 verdict

The current HC-RAW programme is substantially less assumption-heavy than its historical presentation suggested.

The minimal structural growth core is:

\[
\boxed{
\text{HC cyclic-state ansatz}
+
\text{HC}_3\text{-seeded singleton atom tower}.
}
\]

From this one obtains:

- raw comparison geometry;
- reversal-support classes;
- deletion/all-slot growth;
- support filtration;
- intrinsic even sectors;
- growth-selected Johnson \(A_1\).

The following are **not** required for that core:

\[
V_1,V_2,
\]

unique birth rank,

\[
h,
\]

uniform random-walk probabilities,

shell averaging,

or the shell line metric.

LR3 exists structurally, but interpreting it as the selected admissible move still requires an explicit modelling choice or a conditional selection-principle package.

This is the current dependency-minimal architecture.

---

# 399. Certification

RAW-14 encoded:

- primitive/derived node statuses;
- dependency edges;
- alternative LR3 selection packages;
- nested sufficient packages;
- package deletion tests;
- primitive deletion impacts;
- redundancy classifications.

The tightened package audit verified:

\[
\boxed{
31/31
}
\]

dependency/minimality checks.

The dependency DAG is acyclic.

---

# 400. Immediate next step

RAW-14 is a natural stopping point for the foundational HC rebuild.

Three queued directions now exist:

### RAW-10F — CDF One-Defect Proof

A theorem-completion side target.

### EHF-GRAPH-EMERG-00 — Definition Lock and Historical Recovery

A separate graph-emergence classification branch.

### Downstream bridge rebuild

Return carefully to OPW / amplituhedron / other physics-facing structures using the dependency-minimal HC core.

Before choosing among them, it would be useful to create one compact **Foundation v1.0 theorem-and-dependency document** containing only the surviving definitions, exact theorems, modelling choices, and open conjectures from RAW-01 through RAW-14.
