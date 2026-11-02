# EHF-HC-GROW Working Document v0.1

# EHF-HC-GROW-01 — Reversal-Support Propagation Law and Multi-Layer Survival Audit

**Branch:** EHF-HC-GROW  
**Input foundation:** EHF-HC Foundation v1.0  
**Status:** Exact structural growth theorem package with finite HC certification  
**Primary result:** Closed-form one-step and multi-layer propagation laws for reversal-support relations.

---

# 1. Question

The motivating question was intentionally informal:

> **What is the ratio between growth \(n\to n+1\) and propagation of an LR3 move?**

The audit shows that there is not one unique notion of “propagation.”

At least two structurally distinct questions are natural:

1. **Target-class ancestry:**  
   Given an \(LR3\) relation at size \(n+1\), did it descend from an \(LR3\) relation at size \(n\), or was it newly generated from \(LR2\)?

2. **Forward branching:**  
   Given a fixed \(LR3\) relation at size \(n\), how many child relations at size \(n+1\) remain \(LR3\), and how many become higher-support \(LR4\)?

These have different exact ratios.

The audit also derives multi-layer laws for both same-support survival and the full support-lowering cascade.

---

# 2. Structural setup

Let:

\[
N=n+1
\]

be the target size.

Let:

\[
LR_\ell^{(N)}
\]

be the canonical reversal-support-\(\ell\) relation at size \(N\).

For a non-half-cycle support class, RAW-07 established:

\[
\boxed{
LR_\ell^{(N)}
\longrightarrow
LR_\ell^{(N-1)}
\cup
LR_{\ell-1}^{(N-1)}
}
\]

under deletion of the newest atom.

The exact target-edge counts are:

\[
|E_{N,\ell}|=\frac{N!}{4},
\]

\[
|E_{N,\ell\to\ell}|
=
\frac{(N-\ell)(N-1)!}{4},
\]

\[
|E_{N,\ell\to\ell-1}|
=
\frac{\ell(N-1)!}{4}.
\]

These are structural counts.

Normalized ratios become probabilities only after an explicit uniform sampling convention is supplied.

---

# 3. Theorem A — one-step target-class ancestry

For a non-half-cycle target relation:

\[
LR_\ell^{(N)},
\]

the fraction of target edges whose deletion remains in the same support class is:

\[
\boxed{
p_{\ell\to\ell}(N)
=
\frac{N-\ell}{N}.
}
\]

The fraction whose deletion lowers support is:

\[
\boxed{
p_{\ell\to\ell-1}(N)
=
\frac{\ell}{N}.
}
\]

Therefore:

\[
\boxed{
p_{\ell\to\ell}:p_{\ell\to\ell-1}
=
(N-\ell):\ell.
}
\]

This is the cleanest general answer to the original “ratio” question when propagation means **ancestral persistence of the target support class**.

---

# 4. First-appearance boundary

A canonical support class \(LR_\ell\) first exists at:

\[
\boxed{
N=2\ell.
}
\]

At that size it is the half-cycle class.

The half-cycle boundary obeys:

\[
\boxed{
LR_\ell^{(2\ell)}
\longrightarrow
LR_{\ell-1}^{(2\ell-1)}
}
\]

with no same-support parent channel.

Thus:

\[
\boxed{
p_{\ell\to\ell}(2\ell)=0,
\qquad
p_{\ell\to\ell-1}(2\ell)=1.
}
\]

So every reversal-support species is **born from the immediately lower support channel**.

This is a general onset law.

---

# 5. LR3 onset

For:

\[
\ell=3,
\]

the first allowed layer is:

\[
\boxed{N=6}.
\]

At \(N=6\), LR3 is the half-cycle class.

Therefore:

\[
\boxed{
LR3_6
\to
LR2_5
}
\]

for every LR3 edge.

So:

\[
\boxed{
\text{LR3 first appears entirely as a growth lift of LR2.}
}
\]

There is no parent LR3 class at \(n=5\).

This is a stronger and cleaner statement than merely saying LR3 “leaks” to LR2 under deletion.

---

# 6. LR3 target-class propagation law

For target:

\[
N=n+1\ge7,
\]

Theorem A gives:

\[
\boxed{
p_{\rm inherited}^{LR3}(n)
=
\frac{n-2}{n+1}.
}
\]

The newly generated fraction from LR2 is:

\[
\boxed{
p_{\rm generated}^{LR3}(n)
=
\frac{3}{n+1}.
}
\]

Hence:

\[
\boxed{
\text{inherited LR3}:\text{generated from LR2}
=
(n-2):3.
}
\]

This is probably the most direct mathematical formulation of the original question.

Examples:

| growth | inherited LR3 fraction | generated-from-LR2 fraction | ratio |
|---|---:|---:|---:|
| \(5\to6\) | \(0\) | \(1\) | \(0:1\) |
| \(6\to7\) | \(4/7\) | \(3/7\) | \(4:3\) |
| \(7\to8\) | \(5/8\) | \(3/8\) | \(5:3\) |
| \(8\to9\) | \(2/3\) | \(1/3\) | \(6:3\) |
| \(9\to10\) | \(7/10\) | \(3/10\) | \(7:3\) |
| \(11\to12\) | \(3/4\) | \(1/4\) | \(9:3\) |

Locally:

\[
\boxed{
p_{\rm inherited}^{LR3}(n)\to1
}
\]

as:

\[
n\to\infty.
\]

At the same time:

\[
\boxed{
p_{\rm generated}^{LR3}(n)\sim\frac3n.
}
\]

---

# 7. Exact LR3 lift multiplicities

The global target-class split has a corresponding fibre law.

For a generic parent LR3 edge:

\[
n\ge7,
\]

the number of faithful LR3 child lifts at size:

\[
N=n+1
\]

is:

\[
\boxed{
N-3=n-2.
}
\]

For every parent LR2 edge, the number of child LR3 lifts is exactly:

\[
\boxed{3}.
\]

Thus growth creates:

\[
\boxed{
3
}
\]

new LR3 lifts per parent LR2 edge independently of \(n\).

Meanwhile the inherited LR3 multiplicity grows linearly:

\[
\boxed{
n-2.
}
\]

This produces the same target-class ratio:

\[
\boxed{
(n-2):3
}
\]

after the appropriate edge-count normalization.

---

# 8. The \(n=6\) half-cycle fibre anomaly is structural, not a failure

At parent size:

\[
n=6,
\]

LR3 is a half-cycle relation.

The number of parent LR3 edges is half the generic \(n!/4\) count.

Consequently each parent LR3 edge has:

\[
\boxed{8}
\]

faithful LR3 lifts into size \(7\), not merely:

\[
7-3=4.
\]

This doubled fibre precisely compensates for the half-size parent relation class.

The global target LR3 ancestry fraction at size \(7\) remains:

\[
\frac47.
\]

So the global propagation law is smooth even though the per-parent fibre multiplicity changes at the boundary.

---

# 9. Theorem B — forward branching of a fixed parent support relation

There is a second natural propagation question.

Start with a fixed parent relation:

\[
LR_\ell^{(n)}.
\]

Ask for **all 2-opt child relation lifts** at:

\[
N=n+1.
\]

For a generic parent:

\[
n>2\ell,
\]

the child relations split as:

\[
\boxed{
N-\ell
}
\]

faithful:

\[
LR_\ell
\]

lifts, and:

\[
\boxed{
\ell+1
}
\]

raised-support:

\[
LR_{\ell+1}
\]

lifts.

Therefore:

\[
\boxed{
(N-\ell)+(\ell+1)=N+1=n+2.
}
\]

So every generic parent reversal relation has exactly:

\[
\boxed{
n+2
}
\]

2-opt relation lifts in the next layer.

---

# 10. Half-cycle parent boundary

If the parent itself is the half-cycle:

\[
n=2\ell,
\]

then:

\[
LR_{\ell+1}
\]

does not yet exist at target:

\[
N=2\ell+1.
\]

The faithful LR\(_\ell\) fibre doubles.

Thus:

\[
\boxed{
2(N-\ell)
=
2(\ell+1)
=
N+1
}
\]

faithful child relations are obtained.

The total:

\[
\boxed{N+1}
\]

law remains unchanged.

So Theorem B has a uniform total-lift law across the half-cycle boundary.

---

# 11. LR3 forward branching

For a fixed parent LR3 edge:

## Boundary step

At:

\[
6\to7,
\]

\[
\boxed{
8\ LR3
+
0\ LR4.
}
\]

Thus every 2-opt child relation above a half-cycle LR3 parent remains LR3.

## Generic steps

For:

\[
n\ge7,
\]

\[
\boxed{
(n-2)\ LR3
+
4\ LR4
=
n+2
}
\]

child relation lifts.

Therefore:

\[
\boxed{
LR3:LR4
=
(n-2):4.
}
\]

The faithful share among **all relation descendants of a fixed parent LR3 edge** is:

\[
\boxed{
\frac{n-2}{n+2}
}
\]

for:

\[
n\ge7.
\]

This is different from the target-class ancestry fraction:

\[
\frac{n-2}{n+1}.
\]

The denominators differ because the two questions condition on different ensembles.

---

# 12. Why the constants 3 and 4 differ

The constant:

\[
\boxed{3}
\]

belongs to the downward ancestry channel:

\[
LR3_{\rm target}
\to
LR2_{\rm parent}.
\]

It is the support size of LR3.

The constant:

\[
\boxed{4}
\]

belongs to the upward branching channel:

\[
LR3_{\rm parent}
\to
LR4_{\rm child}.
\]

It is the support size of the raised class.

Thus:

\[
\boxed{
3=\text{lower-channel generation multiplicity},
}
\]

while:

\[
\boxed{
4=\text{higher-support branching multiplicity}.
}
\]

These are structurally distinct effects.

---

# 13. Theorem C — multi-layer all-faithful target-class survival

Fix support:

\[
\ell.
\]

Take a top relation:

\[
LR_\ell^{(N)}
\]

and repeatedly delete the newest atom until bottom size:

\[
n,
\]

with:

\[
n\ge2\ell.
\]

The fraction of top LR\(_\ell\) edges that remain in LR\(_\ell\) at **every** deletion step is:

\[
\boxed{
S_\ell(n,N)
=
\prod_{M=n+1}^{N}
\frac{M-\ell}{M}.
}
\]

This telescopes:

\[
\boxed{
S_\ell(n,N)
=
\frac{(n)_\ell}{(N)_\ell},
}
\]

where:

\[
(x)_\ell
=
x(x-1)\cdots(x-\ell+1)
\]

is the falling factorial.

---

# 14. Large-\(N\) support exponent

For fixed bottom \(n\):

\[
\boxed{
S_\ell(n,N)
\sim
(n)_\ell N^{-\ell}.
}
\]

Thus the support value itself controls the power-law exponent of all-faithful target-class ancestry.

This is a combinatorial survival exponent.

It should not automatically be interpreted as a physical scaling dimension.

---

# 15. LR3 multi-layer survival law

For:

\[
\ell=3,
\]

\[
\boxed{
S_3(n,N)
=
\frac{
n(n-1)(n-2)
}{
N(N-1)(N-2)
}.
}
\]

Hence:

\[
\boxed{
S_3(n,N)
\sim
n(n-1)(n-2)N^{-3}
}
\]

for fixed \(n\) and large \(N\).

So two statements coexist:

### One-step locality

\[
\frac{N-3}{N}\to1.
\]

An LR3 relation at a large target layer is increasingly likely, in the edge-census sense, to have an LR3 parent one layer down.

### Long-range ancestry

Demanding faithful LR3 ancestry across many layers gives:

\[
\boxed{
N^{-3}
}
\]

decay.

There is no contradiction.

Near-perfect local persistence can accumulate into small long-range all-faithful ancestry.

---

# 16. LR3 survival back to its first layer

LR3 first appears at:

\[
n=6.
\]

Therefore the fraction of LR3 edges at size \(N\) whose deletion ancestry stays LR3 all the way back to the onset layer is:

\[
\boxed{
S_3(6,N)
=
\frac{6\cdot5\cdot4}
{N(N-1)(N-2)}
=
\frac{120}
{N(N-1)(N-2)}.
}
\]

Examples:

\[
S_3(6,6)=1,
\]

\[
S_3(6,7)=\frac47,
\]

\[
S_3(6,8)=\frac5{14},
\]

\[
S_3(6,10)=\frac16.
\]

Thus most large-\(N\) LR3 edges do **not** have a completely faithful LR3 ancestry all the way to \(N=6\), even though their immediate parent is increasingly likely to be LR3.

---

# 17. Theorem D — full multi-layer support-lowering census

Let:

\[
r=N-n
\]

newest atoms be deleted.

For a top:

\[
LR_\ell^{(N)}
\]

relation, suppose exactly:

\[
s
\]

of the deleted atoms lie on its original \(\ell\)-support.

Then the exact edge-census fraction is:

\[
\boxed{
P_{\ell,N,r}(s)
=
\frac{
\binom{\ell}{s}
\binom{N-\ell}{r-s}
}{
\binom Nr
}.
}
\]

For:

\[
n\ge2\ell,
\]

there is no complement-folding ambiguity.

The formal residual support is:

\[
\boxed{
\ell-s.
}
\]

Residual support:

\[
0\text{ or }1
\]

is the identity relation.

Thus the full multi-layer support distribution is hypergeometric.

---

# 18. LR3 three-channel cascade

For top LR3, only three effective bottom relation types remain:

\[
LR3,\quad LR2,\quad id.
\]

Let:

\[
r=N-n.
\]

Then:

\[
\boxed{
P(LR3)
=
\frac{
\binom{N-3}{r}
}{
\binom Nr
}.
}
\]

Also:

\[
\boxed{
P(LR2)
=
\frac{
3\binom{N-3}{r-1}
}{
\binom Nr
}.
}
\]

And:

\[
\boxed{
P(id)
=
\frac{
3\binom{N-3}{r-2}
+
\binom{N-3}{r-3}
}{
\binom Nr
}.
}
\]

These sum exactly to:

\[
\boxed{1}.
\]

This gives the complete finite support fate of a top LR3 relation after repeated deletion down to any:

\[
n\ge6.
\]

---

# 19. Theorem E — multi-layer forward fidelity among all descendants

There is also a forward analogue.

Start from a fixed parent:

\[
LR_\ell^{(n)}
\]

in the generic regime:

\[
n>2\ell.
\]

At each growth step, compare faithful same-support lifts with **all 2-opt relation lifts**.

The all-faithful share after growing to \(N\) is:

\[
\boxed{
F_\ell(n,N)
=
\prod_{M=n+1}^{N}
\frac{M-\ell}{M+1}.
}
\]

This telescopes to:

\[
\boxed{
F_\ell(n,N)
=
\frac{
(n+1)_{\ell+1}
}{
(N+1)_{\ell+1}
}.
}
\]

For fixed bottom \(n\):

\[
\boxed{
F_\ell(n,N)
\sim
\text{const}\cdot N^{-(\ell+1)}.
}
\]

If the bottom relation is the half-cycle:

\[
n=2\ell,
\]

the first growth step has no raised-support branch and the closed form is doubled for:

\[
N>n.
\]

---

# 20. LR3 forward multi-layer fidelity

For generic bottom:

\[
n\ge7,
\]

\[
\boxed{
F_3(n,N)
=
\frac{
(n+1)n(n-1)(n-2)
}{
(N+1)N(N-1)(N-2)
}.
}
\]

Thus:

\[
\boxed{
F_3(n,N)\sim\text{const}\cdot N^{-4}.
}
\]

For onset bottom:

\[
n=6,
\]

multiply the generic closed form by:

\[
2
\]

for:

\[
N>6.
\]

The difference between:

\[
N^{-3}
\]

and:

\[
N^{-4}
\]

is not contradictory.

They normalize against different ensembles:

- \(N^{-3}\): condition on the **top relation still being LR3**;
- \(N^{-4}\): count faithful LR3 descendants against **all 2-opt descendant support channels** of the original LR3 parent.

---

# 21. A compact propagation dictionary

For growth:

\[
n\to n+1,
\]

the following quantities now have exact meanings.

## Target LR3 ancestry fidelity

\[
\boxed{
\frac{n-2}{n+1}.
}
\]

## Target LR3 newly generated fraction

\[
\boxed{
\frac3{n+1}.
}
\]

## Target LR3 inherited:generated ratio

\[
\boxed{
(n-2):3.
}
\]

## Faithful child LR3 lifts per generic parent LR3

\[
\boxed{
n-2.
}
\]

## New child LR3 lifts per parent LR2

\[
\boxed{
3.
}
\]

## Raised LR4 lifts per generic parent LR3

\[
\boxed{
4.
}
\]

## Total 2-opt child lifts per parent LR3

\[
\boxed{
n+2.
}
\]

## Forward same-support share for generic parent LR3

\[
\boxed{
\frac{n-2}{n+2}.
}
\]

These are related but not interchangeable.

---

# 22. General support dictionary

For general support \(\ell\):

## Target-class one-step fidelity

\[
\boxed{
\frac{N-\ell}{N}.
}
\]

## Target-class lowering fraction

\[
\boxed{
\frac{\ell}{N}.
}
\]

## Target inherited:generated ratio

\[
\boxed{
(N-\ell):\ell.
}
\]

## Generic faithful lifts per parent LR\(_\ell\)

\[
\boxed{
N-\ell.
}
\]

## Raised LR\(_{\ell+1}\) lifts per parent LR\(_\ell\)

\[
\boxed{
\ell+1.
}
\]

## Total relation lifts

\[
\boxed{
N+1.
}
\]

## Multi-layer target-conditioned faithful survival

\[
\boxed{
\frac{(n)_\ell}{(N)_\ell}.
}
\]

## Generic forward all-descendant fidelity

\[
\boxed{
\frac{(n+1)_{\ell+1}}{(N+1)_{\ell+1}}.
}
\]

---

# 23. Interpretation

The support filtration now has a precise growth interpretation.

A fixed support species has two competing effects.

### Local persistence increases with size

For fixed \(\ell\):

\[
\frac{N-\ell}{N}
\to1.
\]

Large layers overwhelmingly preserve support over one deletion.

### New lower-channel-generated relations remain present

The number of LR\(_\ell\) lifts generated per LR\(_{\ell-1}\) parent relation is exactly:

\[
\boxed{\ell}.
\]

This does not grow with \(N\).

### Existing relations also branch upward in support

A generic LR\(_\ell\) parent produces:

\[
\boxed{\ell+1}
\]

LR\(_{\ell+1}\) descendants per growth step.

So support propagation is not merely survival versus death.

It is a graded branching process over reversal-support channels.

---

# 24. Structural significance for LR3

LR3 has a particularly simple story:

1. It first becomes available at \(N=6\).
2. At birth, it is entirely generated from LR2.
3. At later layers, each target LR3 class contains:
   - an inherited LR3 part growing like \(N-3\);
   - a newly generated LR2 ancestry part of fixed multiplicity \(3\).
4. A fixed LR3 parent also produces four LR4 descendants once LR4 becomes available.
5. Long-range all-faithful LR3 ancestry decays as \(N^{-3}\) under target-class conditioning.
6. Forward same-support fidelity among all descendant support channels decays as \(N^{-4}\).

This is a purely combinatorial propagation law.

No physical propagation speed, field, particle, or causal process has yet been identified.

---

# 25. Important probability caution

The ratios:

\[
\frac{N-\ell}{N},
\qquad
\frac{\ell}{N}
\]

are exact fractions of relation edges in the finite census.

Likewise the multi-layer hypergeometric laws are exact counting fractions.

They may be read as probabilities only under an explicit convention such as:

- uniformly sample a top LR\(_\ell\) edge;
- uniformly choose the deletion set;
- uniformly choose among relation descendants.

No such stochastic convention belongs to the structural theorem itself.

---

# 26. Half-cycle caution

The generic support formulas must not be used blindly at:

\[
N=2\ell.
\]

At that boundary:

- \(LR_\ell\) is a half-cycle class;
- the relation edge count is:
  \[
  N!/8
  \]
  rather than:
  \[
  N!/4;
  \]
- same-support deletion disappears;
- per-parent faithful fibres may double at the next layer.

The audit handles this explicitly.

---

# 27. Finite HC certification

The exact relation-level formulas were independently enumerated on Hamilton-cycle state spaces through target size:

\[
N=8.
\]

The checked target classes were:

\[
(N,\ell)
=
(5,2),
(6,2),
(6,3),
(7,2),
(7,3),
(8,2),
(8,3),
(8,4).
\]

All exact target-to-parent split counts matched.

Important examples:

## \(N=6,\ell=3\)

\[
90
\]

LR3 target edges, all mapping to LR2.

Each parent LR2 edge has exactly:

\[
3
\]

LR3 lifts.

## \(N=7,\ell=3\)

\[
1260
\]

LR3 target edges split into:

\[
720
\]

faithful LR3 ancestry edges and:

\[
540
\]

LR2-generated edges.

Thus:

\[
720:540=4:3.
\]

Each half-cycle parent LR3 edge has:

\[
8
\]

faithful lifts.

Each parent LR2 edge has:

\[
3
\]

new LR3 lifts.

## \(N=8,\ell=3\)

\[
10080
\]

LR3 target edges split into:

\[
6300
\]

faithful LR3 ancestry edges and:

\[
3780
\]

LR2-generated edges.

Thus:

\[
6300:3780=5:3.
\]

Each generic parent LR3 edge has:

\[
5
\]

faithful LR3 lifts.

Each LR2 parent edge again has:

\[
3.
\]

---

# 28. Certification summary

The audit contains three independent certification layers.

### Closed-form identity checks

\[
675/675
\]

passed.

### Explicit HC relation enumeration

\[
8/8
\]

passed.

### Forward branching / multi-layer fidelity checks

\[
260/260
\]

passed.

Combined:

\[
\boxed{
943/943
}
\]

strict checks passed.

---

# 29. The answer to the original informal question

If “propagation of LR3 from \(n\) to \(n+1\)” means:

> What fraction of target LR3 relations are inherited from LR3 rather than generated from LR2?

then the answer is:

\[
\boxed{
\frac{n-2}{n+1}
}
\]

versus:

\[
\boxed{
\frac3{n+1},
}
\]

with ratio:

\[
\boxed{
(n-2):3.
}
\]

If instead it means:

> What happens to a fixed LR3 relation when the layer grows?

then, for:

\[
n\ge7,
\]

the answer is:

\[
\boxed{
(n-2)\ LR3
+
4\ LR4
}
\]

out of:

\[
\boxed{
n+2
}
\]

relation lifts.

Both are exact, but they answer different propagation questions.

---

# 30. Recommended next questions

GROW-01 opens several mathematically clean directions.

## GROW-02 — Reversal-Support Branching Operator

Construct the full support-channel growth operator whose one-step fibres are:

\[
LR_\ell
\to
LR_\ell
\oplus
LR_{\ell+1}.
\]

Study its finite matrix form, spectra, normalized limits, and boundary folding.

## GROW-03 — Propagation Generating Function

Encode the full multi-layer support distribution and descendant multiplicities in a generating function.

## GROW-04 — Selected-LR3 Stability Under Growth

If LR3 is chosen as the admissible same-layer move, quantify exactly how much of the selected move relation is:

- inherited;
- newly generated from LR2;
- lost into unselected LR4 branching.

This would connect the structural GROW branch back to the optional LR3 move-model package without confusing structural propagation with dynamics.


---

# EHF-HC-GROW-02 — Reversal-Support Branching Operator

**Branch:** EHF-HC-GROW  
**Input:** EHF-HC Foundation v1.0 + GROW-01  
**Status:** Exact operator identification with finite exact certification  
**Primary result:** The reversal-support branching operator is the colour-swap quotient of an exact two-colour Pólya urn.

---

# 1. Purpose

GROW-01 established exact one-step and multi-layer support-propagation laws.

GROW-02 packages those laws into an operator and asks:

1. What is the exact one-step support branching matrix?
2. Can the half-cycle boundary be represented without an ad hoc exception?
3. Is there a useful spectral description despite the support space changing with \(n\)?
4. Is there an exact multi-step kernel?
5. Does LR3 have a special operator eigenmode?

The answer to the final question is negative:

\[
\boxed{
\text{LR3 is not spectrally singled out by the support-branching operator itself.}
}
\]

Its wider significance comes from separate HC parity/locality results.

---

# 2. Canonical support spaces

At parent size \(n\), the effective reversal supports are

\[
\boxed{
\mathcal L_n
=
\left\{
2,3,\ldots,\left\lfloor\frac n2\right\rfloor
\right\}.
}
\]

For each parent relation \(LR_\ell^{(n)}\), GROW-01 counted all 2-opt child relation lifts at target

\[
N=n+1.
\]

This defines a raw multiplicity operator

\[
\boxed{
B_n:
\mathbb R^{\mathcal L_n}
\to
\mathbb R^{\mathcal L_{n+1}}.
}
\]

Rows are parent support classes and columns are child support classes.

---

# 3. Exact raw branching operator

For a generic parent support

\[
\ell<\frac n2,
\]

the only child supports are

\[
\ell
\quad\text{and}\quad
\ell+1.
\]

Their exact multiplicities are

\[
\boxed{
B_n(\ell,\ell)=n+1-\ell
}
\]

and

\[
\boxed{
B_n(\ell,\ell+1)=\ell+1.
}
\]

Thus every generic row sums to

\[
\boxed{
n+2.
}
\]

Equivalently:

\[
\boxed{
(n+1-\ell)+(\ell+1)=n+2.
}
\]

---

# 4. Half-cycle boundary

If

\[
n=2\ell,
\]

then \(LR_\ell\) is the parent half-cycle class.

The raised support

\[
LR_{\ell+1}
\]

does not yet exist at target size \(n+1\).

Instead the two unfolded child branches fold onto the same canonical support, giving

\[
\boxed{
B_n(\ell,\ell)=n+2.
}
\]

So the half-cycle row remains normalized by the same total multiplicity.

This boundary behavior is not an unrelated correction; it is the quotient image of the unfolded operator described below.

---

# 5. Normalized branching kernel

Define

\[
\boxed{
P_n=\frac{1}{n+2}B_n.
}
\]

For generic support:

\[
\boxed{
P_n(\ell,\ell)
=
\frac{n+1-\ell}{n+2},
}
\]

\[
\boxed{
P_n(\ell,\ell+1)
=
\frac{\ell+1}{n+2}.
}
\]

At the half-cycle boundary:

\[
\boxed{
P_n(\ell,\ell)=1.
}
\]

Each row sums exactly to one.

The entries are exact normalized relation-census weights.

They become stochastic transition probabilities only if one adopts uniform sampling among relation lifts.

---

# 6. Why a single finite spectrum is not enough

The support-space dimension changes with \(n\).

If \(n\) is odd, then \(n+1\) is even and a new half-cycle support channel appears.

Hence

\[
P_n
\]

is rectangular.

If \(n\) is even, \(P_n\) is square.

Therefore the full graded branching family is a **non-autonomous sequence of operators**, not repeated powers of one fixed finite matrix.

A more natural spectral object appears after unfolding the support reflection.

---

# 7. Unfolded reversal-length coordinate

Canonical support identifies the two circular block lengths

\[
j
\quad\text{and}\quad
n-j.
\]

Introduce an unfolded reversal-length coordinate

\[
j.
\]

Define

\[
\boxed{
a=j+1,
}
\]

\[
\boxed{
b=n+1-j,
}
\]

so

\[
\boxed{
a+b=n+2=:T.
}
\]

Under one growth step:

\[
j\to j+1
\]

with normalized census weight

\[
\boxed{
\frac{a}{T},
}
\]

while

\[
j\to j
\]

with weight

\[
\boxed{
\frac{b}{T}.
}
\]

If the support raises, \(a\) increases by one.

If the support stays, \(b\) increases by one.

Therefore the unfolded branching rule is exactly:

\[
\boxed{
(a,b)
\to
(a+1,b)
\quad\text{or}\quad
(a,b+1)
}
\]

with weights proportional to the current counts.

This is the classical two-colour Pólya reinforcement rule.

Here it arises as exact relation-lift combinatorics.

---

# 8. Canonical support is the colour-swap quotient

Reflection

\[
j\leftrightarrow n-j
\]

corresponds exactly to

\[
\boxed{
(a,b)\leftrightarrow(b,a).
}
\]

Canonical support is

\[
\boxed{
\ell
=
\min(j,n-j)
=
\min(a,b)-1.
}
\]

So the canonical support operator is the quotient of the Pólya operator by colour exchange.

This explains the half-cycle boundary immediately.

At a half-cycle parent:

\[
a=b.
\]

After one Pólya update the two oriented states are

\[
(a+1,a)
\quad\text{and}\quad
(a,a+1).
\]

Colour exchange identifies them.

Both therefore fold back to the same canonical support.

The previously observed doubled half-cycle fibre is exactly this quotient multiplicity.

---

# 9. Operator on observables

Let \(f\) be a function of the unfolded count \(a\).

The one-step backward operator is

\[
(\mathcal P_n f)(a)
=
\frac{b}{T}f(a)
+
\frac{a}{T}f(a+1).
\]

Since

\[
b=T-a,
\]

\[
\boxed{
(\mathcal P_n f)(a)
=
f(a)
+
\frac{1}{T}
a\left[f(a+1)-f(a)\right].
}
\]

Define

\[
\boxed{
(\mathcal Gf)(a)
=
a\left[f(a+1)-f(a)\right].
}
\]

Then

\[
\boxed{
\mathcal P_n
=
I+\frac{1}{n+2}\mathcal G.
}
\]

The key point is:

\[
\boxed{
\mathcal G
\text{ is independent of }n.
}
\]

Thus the graded branching family has a fixed scaled bulk generator.

---

# 10. Exact polynomial spectrum

Define the rising factorial

\[
\boxed{
f_r(a)
=
a^{\overline r}
=
a(a+1)\cdots(a+r-1).
}
\]

The elementary difference identity gives

\[
a\left[
(a+1)^{\overline r}
-
a^{\overline r}
\right]
=
r\,a^{\overline r}.
\]

Therefore

\[
\boxed{
\mathcal G f_r
=
r f_r.
}
\]

So the polynomial spectrum of the scaled unfolded generator is

\[
\boxed{
0,1,2,3,\ldots.
}
\]

And

\[
\boxed{
\mathcal P_n f_r
=
\left(
1+\frac{r}{n+2}
\right)f_r.
}
\]

This is the natural spectral structure of the non-autonomous growth operator.

---

# 11. Exact martingales

Because

\[
\mathcal P_n f_r
=
\frac{n+2+r}{n+2}f_r,
\]

and

\[
(n+3)^{\overline r}
=
\frac{n+2+r}{n+2}
(n+2)^{\overline r},
\]

the normalized observable

\[
\boxed{
M_r(n,a)
=
\frac{
a^{\overline r}
}{
(n+2)^{\overline r}
}
}
\]

satisfies

\[
\boxed{
\mathbb E_{\rm census}
[
M_r(n+1,a')
\mid a
]
=
M_r(n,a).
}
\]

Thus every polynomial order gives an exact graded martingale under the normalized branching kernel.

For \(r=1\):

\[
\boxed{
\frac{a}{n+2}
}
\]

is the familiar Pólya fraction martingale.

---

# 12. Canonical symmetric martingales

The oriented quantity \(a/(n+2)\) is not invariant under support reflection.

To descend to canonical support, symmetrize under

\[
a\leftrightarrow b.
\]

For \(r\ge2\), define

\[
\boxed{
H_r(n,\ell)
=
\frac{
a^{\overline r}
+
b^{\overline r}
}{
(n+2)^{\overline r}
},
}
\]

where

\[
\{a,b\}
=
\{\ell+1,n+1-\ell\}.
\]

Then

\[
\boxed{
\mathbb E_{\rm census}
[
H_r(n+1,L_{n+1})
\mid L_n=\ell
]
=
H_r(n,\ell).
}
\]

So the canonical support process itself possesses an infinite symmetric martingale hierarchy.

The \(r=1\) symmetrization is trivial because

\[
a+b=n+2.
\]

The first nontrivial canonical invariant occurs at \(r=2\).

---

# 13. Exact multi-step kernel

Let the bottom layer be \(n\), top layer \(N\), and

\[
R=N-n.
\]

Start from unfolded support \(j\), with

\[
a=j+1,
\qquad
b=n+1-j,
\qquad
T=n+2.
\]

Let \(s\) be the number of support-raising updates during the \(R\) growth steps.

Then the exact descendant census fraction is

\[
\boxed{
\Pr_{\rm census}(s)
=
\binom Rs
\frac{
a^{\overline s}
b^{\overline{R-s}}
}{
T^{\overline R}
}.
}
\]

This is the beta-binomial law.

No approximation is involved.

---

# 14. Folded canonical multi-step kernel

After \(s\) unfolded support raises,

\[
j'=j+s.
\]

At top size \(N\), canonical support is

\[
\boxed{
\ell'
=
\min(j+s,N-j-s).
}
\]

Therefore the exact canonical multi-step branching kernel is obtained by summing the beta-binomial weights of all \(s\) values that fold to the same \(\ell'\).

Symbolically:

\[
\boxed{
P_{n\to N}^{\rm can}
(\ell,\ell')
=
\sum_{\substack{0\le s\le R\\
\min(\ell+s,N-\ell-s)=\ell'}}
\binom Rs
\frac{
(\ell+1)^{\overline s}
(n+1-\ell)^{\overline{R-s}}
}{
(n+2)^{\overline R}
}.
}
\]

This is the closed-form multi-step support branching operator.

---

# 15. Exact matrix-product verification

The direct product

\[
\boxed{
P_nP_{n+1}\cdots P_{N-1}
}
\]

was compared with the folded beta-binomial formula for:

- bottom sizes \(n=4,\ldots,12\);
- every available starting support;
- growth horizons up to eight layers where included by the audit range.

Every rational entry matched exactly.

Thus the Pólya identification is not merely a suggestive analogy.

It is an exact representation of the canonical branching operator.

---

# 16. Conventional finite spectrum on even steps

For even parent size

\[
n=2m,
\]

the canonical support set is

\[
2,\ldots,m,
\]

and the target support set at \(n+1\) has the same cardinality.

Therefore \(P_n\) is square.

It is upper triangular.

For

\[
2\le\ell<m,
\]

the diagonal entry is

\[
\boxed{
\lambda_\ell(n)
=
\frac{n+1-\ell}{n+2}.
}
\]

The half-cycle row contributes

\[
\boxed{
\lambda_{\rm boundary}=1.
}
\]

Hence:

\[
\boxed{
\operatorname{spec}(P_n)
=
\left\{
1
\right\}
\cup
\left\{
\frac{n+1-\ell}{n+2}:
2\le\ell<m
\right\}.
}
\]

---

# 17. Exact even-step spectral gap

The largest subunit eigenvalue occurs at the lowest support

\[
\ell=2.
\]

Thus

\[
\lambda_2
=
\frac{n-1}{n+2}.
\]

The gap to the boundary eigenvalue \(1\) is

\[
\boxed{
\gamma_n
=
1-\lambda_2
=
\frac{3}{n+2}.
}
\]

This exact \(3/(n+2)\) should not be attributed to LR3.

It comes from the lower nontrivial support boundary

\[
\ell=2.
\]

So the canonical finite-matrix spectral gap is controlled by LR2, not LR3.

---

# 18. Odd steps are rectangular

For odd parent

\[
n=2m+1,
\]

the target

\[
n+1=2m+2
\]

introduces a new half-cycle support

\[
m+1.
\]

Therefore \(P_n\) maps a smaller support space into a larger one.

An ordinary same-space eigen-spectrum is consequently not intrinsic to that step.

This is why the \(n\)-independent unfolded generator

\[
\mathcal G
\]

is the cleaner spectral object for the full graded family.

---

# 19. Large-\(n\) scaling

On polynomial mode \(r\), growth from \(n\) to \(N\) multiplies the unnormalized mode by

\[
\prod_{t=n}^{N-1}
\left(
1+\frac{r}{t+2}
\right).
\]

This product is exact:

\[
\boxed{
\prod_{t=n}^{N-1}
\left(
1+\frac{r}{t+2}
\right)
=
\frac{
(N+2)^{\overline r}
}{
(n+2)^{\overline r}
}.
}
\]

For large \(n,N\):

\[
\boxed{
\frac{
(N+2)^{\overline r}
}{
(n+2)^{\overline r}
}
\sim
\left(
\frac Nn
\right)^r.
}
\]

Thus, introducing the combinatorial scale

\[
\boxed{
\tau=\log(n+2),
}
\]

the graded operator has the asymptotic form

\[
\boxed{
\frac{d}{d\tau}
\sim
\mathcal G
}
\]

on polynomial observables.

This is an asymptotic growth-coordinate statement only.

No identification of \(\tau\) with physical time is made.

---

# 20. Relation to GROW-01 exponents

GROW-01 found target-conditioned all-faithful same-support survival

\[
S_\ell(n,N)
=
\frac{(n)_\ell}{(N)_\ell}
\sim N^{-\ell}.
\]

It also found forward same-support fidelity among all descendants scaling as

\[
N^{-(\ell+1)}.
\]

GROW-02 explains why factorial structures appear naturally: the operator itself is diagonal on rising-factorial polynomial modes in the unfolded representation.

The falling-factorial survival ratios and rising-factorial martingales are dual manifestations of the same support-growth combinatorics.

---

# 21. LR3 row

For generic parent LR3:

\[
n\ge7,
\]

the raw operator row is

\[
\boxed{
B_n(3,3)=n-2,
}
\]

\[
\boxed{
B_n(3,4)=4.
}
\]

The normalized row is

\[
\boxed{
P_n(3,3)=\frac{n-2}{n+2},
}
\]

\[
\boxed{
P_n(3,4)=\frac4{n+2}.
}
\]

At the onset half-cycle parent

\[
n=6,
\]

\[
\boxed{
P_6(3,3)=1.
}
\]

This exactly recovers GROW-01.

---

# 22. Is LR3 spectrally special?

Not in this operator.

The generic support row is

\[
\ell
\to
\ell
\quad\text{with multiplicity }n+1-\ell,
\]

\[
\ell
\to
\ell+1
\quad\text{with multiplicity }\ell+1.
\]

LR3 simply substitutes

\[
\ell=3.
\]

The unfolded generator spectrum is the universal integer hierarchy

\[
0,1,2,\ldots
\]

and contains no isolated LR3 eigenvalue.

The even-step canonical spectrum is also a monotone support sequence with no LR3 anomaly.

Therefore:

\[
\boxed{
\text{the growth-branching operator alone does not select LR3}.
}
\]

This is consistent with EHF-HC Foundation v1.0.

LR3's special role comes instead from:

- being the smallest nontrivial odd reversal support;
- preserving the intrinsic even bipartition;
- the conditional locality/minimality selection result;
- its characteristic onset at \(n=6\);
- the structural relation \(LR3\to LR3\cup LR2\) under deletion.

That distinction is useful because it prevents us from reading the desired LR3 preference back into an otherwise universal branching operator.

---

# 23. Exact Pólya interpretation

Under uniform relation-lift sampling, the unfolded branching kernel is literally the standard Pólya urn with initial counts

\[
\boxed{
a_0=j+1,
\qquad
b_0=n+1-j.
}
\]

Thus standard Pólya consequences become exact statements about the normalized relation-census operator:

- beta-binomial finite-horizon law;
- martingale colour fraction;
- beta limiting fraction under indefinite normalized branching.

The last item is a stochastic interpretation and should be stated only after the uniform-lift convention is adopted.

The underlying finite counts and beta-binomial coefficients themselves remain exact combinatorics.

---

# 24. Canonical large-growth limit under uniform-lift sampling

If the normalized kernel is interpreted stochastically, the unfolded fraction

\[
X_n
=
\frac{a_n}{n+2}
\]

is a bounded martingale.

Starting from

\[
(a_0,b_0),
\]

its limiting law is

\[
\boxed{
X_\infty
\sim
\operatorname{Beta}(a_0,b_0).
}
\]

The canonical support fraction folds colour exchange, so asymptotically it is governed by

\[
\boxed{
\min(X_\infty,1-X_\infty).
}
\]

This is not added to the structural foundation; it is a consequence of the optional uniform-lift stochastic interpretation.

---

# 25. Certification

GROW-02 performed exact rational checks of:

1. every canonical one-step row through parent \(n=20\);
2. square even-step spectra through parent \(n=30\);
3. direct matrix products against folded beta-binomial kernels;
4. unfolded generator eigenfunction identities;
5. canonical symmetric martingale identities;
6. rising-factorial generator algebra.

Final result:

\[
\boxed{
1221/1221
}
\]

strict checks passed.

---

# 26. Main verdict

The reversal-support growth system has a compact exact operator form.

The raw canonical operator is bidiagonal except at the half-cycle fold:

\[
\boxed{
B_n(\ell,\ell)=n+1-\ell,
\qquad
B_n(\ell,\ell+1)=\ell+1.
}
\]

After normalization:

\[
\boxed{
P_n=\frac{B_n}{n+2}.
}
\]

Unfolding the complement identification converts the process exactly into a two-colour Pólya reinforcement operator.

The fixed scaled generator is

\[
\boxed{
\mathcal Gf(a)
=
a[f(a+1)-f(a)],
}
\]

with exact polynomial spectrum

\[
\boxed{
0,1,2,\ldots.
}
\]

The exact multi-step kernel is beta-binomial before folding.

The canonical half-cycle anomaly is entirely explained by the colour-swap quotient.

And:

\[
\boxed{
\text{LR3 is structurally important elsewhere, but not an exceptional eigenchannel of this branching operator.}
}
\]

---

# 27. Recommended next probe

A natural continuation is:

## EHF-HC-GROW-03 — Support-Branching Entropy, Concentration, and Scaling Limit

Possible targets:

1. exact entropy of the beta-binomial descendant support distribution;
2. canonical folded distribution;
3. concentration width as \(N\) grows;
4. beta limiting law under uniform-lift sampling;
5. whether selected LR3 ancestry occupies an asymptotically distinguishable sector after folding;
6. comparison of target-conditioned \(N^{-3}\) survival with the full branching distribution.

A more structural alternative is:

## EHF-HC-GROW-03A — Branching Operator Intertwining with Parity Sectors

Ask whether the reversal-support Pólya operator intertwines nontrivially with the even intrinsic bipartition-preserving/violating split, which is where LR3's genuine structural distinction lives.
