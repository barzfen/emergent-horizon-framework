# EHF-HC-GROW-08 — Cross-Channel Loop and Coupling Geometry Audit

**Branch:** EHF-HC-GROW  
**Inputs:** EHF-HC Foundation v1.0; GROW-01 through GROW-07  
**Status:** Exact local overlap/coupling theorems + finite-exact coloured-loop census  
**Decision role:** Final structural gate before opening a physics-bridge branch.

---

# 1. Question

GROW-07 showed that the fixed support graphs:

\[
G_{n,\ell}=(HC_n,LR_\ell)
\]

can have genuinely different internal geometry.

GROW-08 asks:

> **How do distinct reversal-support channels couple when more than one support colour is allowed in a loop?**

The principal targets were:

- mixed-support squares;
- shortest mixed loops;
- commutators;
- intrinsic-sector parity of closed loops;
- possible quotient holonomy;
- whether LR3 plays a distinctive role between LR2 and LR4.

The answer is structurally rich, but more precise than a generic “holonomy” story.

The main coupling mechanism is:

\[
\boxed{
\text{relative interval overlap geometry}.
}
\]

---

# 2. Support-coloured nearest-shell graph

At fixed \(n\), colour every 2-opt edge by its intrinsic reversal support:

\[
\ell.
\]

The result is a support-coloured graph:

\[
\boxed{
\mathcal G_n
=
\bigcup_{\ell=2}^{\lfloor n/2\rfloor}
G_{n,\ell}.
}
\]

All colours still lie in the same raw shell:

\[
d_E=2.
\]

Thus mixed loops compare different internal channels at identical raw HC distance.

---

# 3. Pair-overlap trichotomy

Take two supports:

\[
2\le\ell<k\le\left\lfloor\frac n2\right\rfloor.
\]

Let:

\[
I
\]

be a cyclic interval of length \(\ell\), and:

\[
J
\]

a cyclic interval of length \(k\).

There are exactly three geometric relations.

## Disjoint

\[
I\cap J=\varnothing.
\]

## Nested

\[
I\subset J.
\]

Because \(\ell<k\), the reverse containment cannot occur.

## Partial overlap

\[
I\cap J\neq\varnothing,
\qquad
I\nsubseteq J.
\]

This trichotomy completely controls the shortest two-channel closure.

---

# 4. Exact placement counts

Fix the small interval \(I\) and vary the cyclic start position of \(J\).

The number of nested positions is:

\[
\boxed{
k-\ell+1.
}
\]

The number of disjoint positions is:

\[
\boxed{
n-k-\ell+1.
}
\]

The number of partial-overlap positions is:

\[
\boxed{
2(\ell-1).
}
\]

These sum to:

\[
(k-\ell+1)+(n-k-\ell+1)+2(\ell-1)=n.
\]

Therefore the count of laminar positions — nested or disjoint — is:

\[
\boxed{
n-2\ell+2.
}
\]

A notable consequence is that the number of partial-overlap placements depends on the **smaller support only**.

---

# 5. Disjoint channels give commuting squares

Let:

\[
R_I,\ R_J
\]

be the positional interval reversals.

If:

\[
I\cap J=\varnothing,
\]

then they commute:

\[
\boxed{
R_IR_J=R_JR_I.
}
\]

Hence:

\[
\boxed{
R_IR_JR_IR_J=e.
}
\]

This gives a simple alternating mixed-support square in the HC quotient.

This is the genuinely commuting part of the cross-channel geometry.

---

# 6. Nested channels give conjugation squares

If:

\[
I\subset J,
\]

then reversal by \(J\) transports the smaller interval to another contiguous interval of the same length:

\[
J(I).
\]

Therefore:

\[
\boxed{
R_JR_IR_J
=
R_{J(I)}.
}
\]

Consequently:

\[
\boxed{
R_I R_J R_{J(I)} R_J=e.
}
\]

This is a mixed four-cycle, but not a commuting square unless:

\[
J(I)=I.
\]

It is better described as a **conjugation/transport square**.

Thus nested channel coupling is flat in state space while carrying nontrivial generator-frame transport.

---

# 7. Exact nested transport law

Write the small interval's offset inside the large interval as:

\[
a,
\qquad
0\le a\le k-\ell.
\]

Conjugation by the large reversal sends:

\[
\boxed{
a
\longmapsto
a'
=
k-\ell-a.
}
\]

This transport is an involution:

\[
a''=a.
\]

A centered nested placement is fixed precisely when:

\[
\boxed{
2a=k-\ell.
}
\]

Therefore:

- if \(k-\ell\) is even, there is one centered fixed nested placement;
- if \(k-\ell\) is odd, nested placements are paired with no fixed point.

This is an exact channel-frame transport law.

---

# 8. Partial overlap is the genuinely order-sensitive regime

If \(I\) partially overlaps \(J\), conjugation by \(R_J\) sends the support of \(R_I\) to a non-contiguous positional set.

Therefore:

\[
R_JR_IR_J
\]

is not another single \(LR_\ell\) interval generator.

The alternating four-step closure leaves the single-\(\ell\) generator family.

This is the first genuinely non-flat local coupling regime.

Define the local commutator:

\[
\boxed{
\Omega_{\ell,k}
=
[R_I,R_J]
=
R_IR_JR_IR_J.
}
\]

Since the reversals are involutions:

\[
\Omega_{\ell,k}=(R_IR_J)^2.
\]

For partial overlap:

\[
\boxed{
\Omega_{\ell,k}\neq e.
}
\]

Its cycle type and order depend on:

- \(\ell\);
- \(k\);
- overlap depth.

So cross-channel coupling has an exact algebraic fingerprint beyond the support-parity label.

---

# 9. Partial-overlap coupling fingerprints

Let:

\[
r
\in
\{1,\ldots,\ell-1\}
\]

be the overlap depth at one boundary.

Examples:

## LR2 / LR3

For \(r=1\):

\[
\boxed{
\Omega_{2,3}
\text{ is a 3-cycle},
\qquad
\operatorname{ord}\Omega=3.
}
\]

## LR3 / LR4

For both:

\[
r=1,2,
\]

the commutator is again a 3-cycle of order \(3\).

## LR4 / LR5

The coupling differentiates overlap depth:

\[
r=1:
\quad
(3),
\quad
\operatorname{ord}=3,
\]

\[
r=2:
\quad
(3,3),
\quad
\operatorname{ord}=3,
\]

\[
r=3:
\quad
(2,2),
\quad
\operatorname{ord}=2.
\]

## LR5 / LR6

The deepest partial overlap gives:

\[
r=4:
\quad
\boxed{
(5),
\qquad
\operatorname{ord}=5.
}
\]

Thus higher support does not merely increase a scalar “coupling strength.”

It creates richer local commutator algebra.

The full exact finite table is supplied with the audit.

---

# 10. Mixed-square census

For a generic pair:

\[
\ell<k<n/2,
\]

each reference HC state lies on exactly:

\[
\boxed{
n(n-2\ell+2)
}
\]

distinct alternating \(LR_\ell/LR_k\) squares.

The count depends on the smaller support \(\ell\), but not on \(k\).

This is explained by the placement trichotomy:

\[
n
\left[
(k-\ell+1)+(n-k-\ell+1)
\right]
=
n(n-2\ell+2).
\]

The two contributions are:

\[
\boxed{
n(k-\ell+1)
}
\]

nested transport squares, and:

\[
\boxed{
n(n-k-\ell+1)
}
\]

disjoint commuting squares.

So equal total square counts can hide different mixtures of commuting and transport geometry.

---

# 11. Half-cycle boundary

When the larger support is:

\[
k=n/2,
\]

one HC half-cycle edge has two positional reversal representatives.

As a result, the number of distinct quotient squares is:

\[
\boxed{
\frac12 n(n-2\ell+2).
}
\]

The generator-labelled lift census contains an additional family closing to reflections in:

\[
D_n.
\]

Across the audited range these reflection-closing words occur in the same number as the identity-lift words.

This should **not** be interpreted as generic physical holonomy.

It is tied to the doubled positional representation of the half-cycle quotient edge.

---

# 12. Generic square holonomy result

For every non-half-cycle pair audited through:

\[
n=12,
\]

all simple alternating mixed four-cycles lifted to:

\[
\boxed{
\text{positional identity}.
}
\]

No nontrivial rotation or reflection holonomy was found.

Therefore the generic shortest mixed squares are algebraically flat.

The meaningful nontrivial information is instead:

- commuting versus conjugation transport;
- failure of closure under partial overlap;
- nontrivial commutator fingerprints.

This is an important negative result because it prevents us from over-interpreting the loop geometry.

---

# 13. Large-\(n\) overlap scaling

For fixed supports \(\ell,k\):

\[
p_{\rm partial}
=
\frac{2(\ell-1)}n
\to0.
\]

Also:

\[
p_{\rm nested}
=
\frac{k-\ell+1}{n}
\to0,
\]

while:

\[
p_{\rm disjoint}\to1.
\]

Thus uniformly random placements of fixed finite supports become almost surely disjoint and commuting at large \(n\).

But if supports scale extensively:

\[
\frac{\ell}{n}\to x,
\qquad
\frac{k}{n}\to y,
\qquad
0<x<y\le\frac12,
\]

then:

\[
\boxed{
p_{\rm nested}\to y-x,
}
\]

\[
\boxed{
p_{\rm disjoint}\to1-x-y,
}
\]

\[
\boxed{
p_{\rm partial}\to2x.
}
\]

So extensive support channels retain a finite order-sensitive coupling fraction.

This mirrors the local-versus-extensive distinction found earlier in the parity branch.

---

# 14. Closed-loop parity law on even HC layers

On an even HC layer:

- odd support preserves the intrinsic bipartition;
- even support changes it.

Therefore every closed support-coloured loop must contain an even number of even-support edges.

If a loop has colour sequence:

\[
\ell_1,\ldots,\ell_r,
\]

then:

\[
\boxed{
\#\{j:\ell_j\text{ even}\}
\equiv0\pmod2.
}
\]

Equivalently, the product of the support-parity tags around a closed loop is:

\[
\boxed{+1}.
\]

This is an exact \(\mathbb Z_2\) loop constraint.

It is structural sector bookkeeping, not a physical gauge charge.

---

# 15. Mixed triangles

The audit exhaustively scanned generator-labelled mixed triangles for:

\[
5\le n\le10
\]

over every available support sequence containing at least two colours.

No simple mixed triangle was found:

\[
\boxed{
0.
}
\]

Combined with the single-channel triangle audit of GROW-07, this strongly suggests a broader triangle-free property of the full 2-opt graph.

However an all-\(n\) proof is not claimed in GROW-08.

---

# 16. First genuine LR2/LR3/LR4 closure

The three channels:

\[
LR2,\ LR3,\ LR4
\]

first coexist as effective canonical channels at:

\[
n=8.
\]

There is an exact positional identity:

\[
\boxed{
R_{0,2}
R_{1,2}
R_{2,2}
R_{0,3}
R_{0,4}
=
e.
}
\]

In support colours:

\[
\boxed{
(2,2,2,3,4).
}
\]

For:

\[
8\le n\le12,
\]

this word gives a simple five-cycle in the HC quotient.

---

# 17. No shorter three-colour 2/3/4 loop in the audited range

For:

\[
8\le n\le12,
\]

the exhaustive audit found:

- no simple mixed triangle;
- no simple four-cycle using all three support colours:
  \[
  2,3,4.
  \]

But the five-cycle above exists.

Therefore:

\[
\boxed{
\text{the finite-certified shortest genuine }LR2/LR3/LR4
\text{ loop has length }5.
}
\]

This is the first support-coloured pentagon in the hierarchy.

---

# 18. Universal recursive channel polygon

The pentagon is the first nontrivial member of a general positional identity.

Let:

\[
s_i=R_{i,2}
\]

be adjacent transpositions, and let:

\[
R_m=R_{0,m}.
\]

Then:

\[
\boxed{
s_0s_1\cdots s_{m-1}R_mR_{m+1}
=
e.
}
\]

The support-colour sequence is:

\[
\boxed{
\underbrace{2,2,\ldots,2}_{m\text{ times}},
m,m+1.
}
\]

Its length is:

\[
\boxed{
m+2.
}
\]

The raw positional identity is exact.

Simple HC quotient loops were certified for:

\[
2\le m\le8
\]

at the first layers where the highest channel is effective.

---

# 19. Why LR3 is special in the recursive loop hierarchy

For:

\[
m=2,
\]

the recursive polygon uses only two distinct support colours:

\[
LR2,\ LR3.
\]

For:

\[
m=3,
\]

the relation becomes:

\[
\boxed{
LR2,LR2,LR2,LR3,LR4,
}
\]

which is the **first recursive closure involving three distinct support channels**.

Thus LR3 has another exact structural distinction:

\[
\boxed{
LR3
\text{ is the middle channel of the first genuine three-colour recursive polygon.}
}
\]

This is independent of the earlier reasons LR3 was distinguished:

- smallest nontrivial odd support;
- first two-sided nontrivial interior channel.

The three facts are compatible but logically separate.

---

# 20. Is this a physical interaction?

Not yet.

The cross-channel objects found here are:

- interval-overlap relations;
- conjugation maps;
- commutators of positional involutions;
- support-coloured graph cycles.

They are exact combinatorial structures.

Nothing in GROW-08 supplies:

- an interaction amplitude;
- coupling constant;
- action;
- Hamiltonian;
- physical time;
- energy;
- field strength.

Therefore phrases such as “LR3 mediates an interaction between LR2 and LR4” would currently be too strong.

The safe statement is:

\[
\boxed{
LR3
\text{ participates in the first nontrivial three-colour channel closure.}
}
\]

---

# 21. What GROW-08 changes

Before this audit, the support ladder could be viewed only as a birth/renewal hierarchy:

\[
LR_{\ell-1}
\to
LR_\ell
\to
LR_{\ell+1}.
\]

GROW-08 adds fixed-layer coupling geometry.

Two support channels can interact locally in three qualitatively different ways:

\[
\boxed{
\text{disjoint}
\;\Rightarrow\;
\text{commutation},
}
\]

\[
\boxed{
\text{nested}
\;\Rightarrow\;
\text{conjugation transport},
}
\]

\[
\boxed{
\text{partial overlap}
\;\Rightarrow\;
\text{nontrivial commutator}.
}
\]

This is a genuine cross-channel algebra.

It is substantially stronger than merely observing different support labels.

---

# 22. GROW-08 verdict

The original question was whether distinct internal channel geometries have nontrivial coupling.

The answer is:

\[
\boxed{
\textbf{Yes.}
}
\]

But the correct structure is not generic nontrivial holonomy.

It is an exact overlap-controlled coupling algebra consisting of:

1. commuting squares;
2. nested transport squares;
3. partial-overlap commutators;
4. recursive multi-channel polygons;
5. an exact even-layer \(\mathbb Z_2\) loop constraint.

The first genuine three-colour support closure is the:

\[
\boxed{
LR2/LR3/LR4
\text{ pentagon}.
}
\]

This gives us enough internally derived structure to proceed to a physics-bridge branch without relying on superficial numerical resemblance.

---

# 23. Certification

GROW-08 contains four independent certification groups.

### Pair-regime / commutator / recursive-polygon checks

\[
\boxed{
432/432
}
\]

passed.

### Mixed-triangle and three-colour minimality checks

\[
\boxed{
131/131
}
\]

passed.

### Lifted square-holonomy checks

\[
\boxed{
30/30
}
\]

passed.

### Distinct quotient-square counts

\[
\boxed{
19/19
}
\]

passed.

Combined:

\[
\boxed{
612/612
}
\]

strict checks passed.

---

# 24. Next branch: physics bridge

The structural gate is now passed.

The next work should leave the GROW branch and begin a deliberately separate comparison programme:

\[
\boxed{
\textbf{EHF-PHYS-CHAN-01 — Coupled-Channel Analogue Census and No-Fit Bridge Test}.
}
\]

The purpose should **not** be to assign particle names to \(LR_\ell\).

Instead, compare the independently derived HC channel invariants against known physical/mathematical channel structures.

The comparison targets should include:

- coupled-channel scattering;
- partial-wave / angular-momentum channel systems;
- representation ladders;
- lattice excitation sectors;
- transfer-matrix channel decompositions;
- parity-graded systems;
- threshold-opening channel models.

A candidate bridge should be rejected unless several independent invariants match simultaneously:

1. channel adjacency;
2. binary grading;
3. threshold structure;
4. loop/commutator algebra;
5. scaling hierarchy;
6. sector action.

That is the appropriate next step.
