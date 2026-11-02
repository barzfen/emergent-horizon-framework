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


---

# EHF-HC-GROW-03A — Branching Operator Intertwining with Intrinsic Parity Sectors

**Branch:** EHF-HC-GROW  
**Inputs:** EHF-HC Foundation v1.0, GROW-01, GROW-02  
**Status:** Exact structural parity-intertwining theorem package  
**Primary result:** The support branching operator has an exact parity-even/parity-odd decomposition, but intrinsic parity is not an autonomous two-state coarse process.

---

# 1. Question

GROW-02 showed that the reversal-support branching operator is universal across support channels and does not spectrally single out LR3.

The natural next question is therefore:

> **How does that universal support-branching operator interact with the one structure that does distinguish LR3 — intrinsic even-layer bipartition preservation?**

For an even Hamilton cycle, the exact reversal parity law is:

\[
\Pi_{\rm intr}(D)=\Pi_{\rm intr}(C)
\iff
\ell\text{ is odd}.
\]

So define the support-parity tag

\[
\boxed{
\sigma(\ell)
=
\begin{cases}
+1,&\ell\text{ odd},\\
-1,&\ell\text{ even}.
\end{cases}
}
\]

On an even layer:

\[
\boxed{
\sigma=+1
\iff
\text{intrinsic bipartition preserving},
}
\]

while:

\[
\boxed{
\sigma=-1
\iff
\text{intrinsic bipartition changing}.
}
\]

The audit asks whether this parity tag intertwines cleanly with growth.

---

# 2. One-step support branching

From GROW-02, for parent size \(n\) and generic support \(\ell\):

\[
P_n(\ell,\ell)
=
\frac{n+1-\ell}{n+2},
\]

\[
P_n(\ell,\ell+1)
=
\frac{\ell+1}{n+2}.
\]

The same-support branch keeps support parity.

The raised-support branch flips it.

Therefore the branching operator already has an exact \(\mathbb Z_2\)-grading.

---

# 3. Parity operator

Let:

\[
J_n
\]

be the diagonal sign operator on support space:

\[
\boxed{
J_n e_\ell
=
\sigma(\ell)e_\ell.
}
\]

Write:

\[
\boxed{
P_n=S_n+R_n,
}
\]

where:

- \(S_n\) contains same-support entries;
- \(R_n\) contains support-raising entries.

Then:

\[
\boxed{
J_nS_nJ_{n+1}=+S_n,
}
\]

while:

\[
\boxed{
J_nR_nJ_{n+1}=-R_n.
}
\]

Hence:

\[
\boxed{
S_n
=
\frac12
\left(
P_n+J_nP_nJ_{n+1}
\right),
}
\]

and:

\[
\boxed{
R_n
=
\frac12
\left(
P_n-J_nP_nJ_{n+1}
\right).
}
\]

Thus the branching operator decomposes exactly into:

\[
\boxed{
\text{parity-even same-support propagation}
}
\]

plus:

\[
\boxed{
\text{parity-odd support-raising propagation}.
}
\]

This is the cleanest algebraic intertwining result.

---

# 4. Half-cycle boundary

At a half-cycle parent:

\[
n=2\ell,
\]

the unfolded Pólya branches are exchanged by support complement and fold back to the same canonical support.

Therefore the canonical row has:

\[
\boxed{
R_n=0,
\qquad
S_n=P_n.
}
\]

So the parity decomposition remains valid after folding.

The boundary anomaly is again a quotient effect rather than a failure of the parity grading.

---

# 5. Why two growth steps are the natural intrinsic-sector interval

Intrinsic bipartition sectors exist on even HC layers.

A one-step move:

\[
2m\to2m+1
\]

leaves the even-layer sector category.

A second step:

\[
2m+1\to2m+2
\]

returns to an even layer.

Therefore define the even-to-even branching operator:

\[
\boxed{
K_n
=
P_nP_{n+1},
\qquad
n\text{ even}.
}
\]

This is the natural object for asking whether the intrinsic bipartition-preserving/changing tag propagates across growth.

---

# 6. Exact two-step parity law

Take even parent size \(n\) and support \(\ell\).

Define:

\[
\boxed{
a=\ell+1,
}
\]

\[
\boxed{
b=n+1-\ell.
}
\]

Then:

\[
a+b=n+2.
\]

Over two Pólya growth steps, the sector tag flips precisely when exactly one support-raising event occurs.

The exact census fraction is therefore:

\[
\boxed{
q_{n,\ell}
=
\frac{
2ab
}{
(n+2)(n+3)
}.
}
\]

Substituting \(a,b\):

\[
\boxed{
q_{n,\ell}
=
\frac{
2(\ell+1)(n+1-\ell)
}{
(n+2)(n+3)
}.
}
\]

This is the exact even-to-even intrinsic sector-toggle fraction.

The same-tag fraction is:

\[
\boxed{
1-q_{n,\ell}.
}
\]

---

# 7. Exact parity attenuation

The difference between same-tag and flipped-tag fractions is:

\[
\eta_{n,\ell}
=
1-2q_{n,\ell}.
\]

Algebra gives:

\[
\boxed{
\eta_{n,\ell}
=
\frac{
(n-2\ell)^2+n+2
}{
(n+2)(n+3)
}.
}
\]

This is strictly positive:

\[
\boxed{
\eta_{n,\ell}>0.
}
\]

Therefore growth never reverses the **mean sign** of the parent intrinsic-sector tag.

It may strongly attenuate it, but it does not invert it.

---

# 8. Intertwining identity for the parity observable

Let:

\[
\sigma_n(\ell)=(-1)^{\ell+1}.
\]

Then:

\[
\boxed{
(K_n\sigma_{n+2})(\ell)
=
\eta_{n,\ell}\sigma_n(\ell).
}
\]

So the parity observable does intertwine with the two-step branching operator.

But the factor:

\[
\eta_{n,\ell}
\]

depends on support.

Therefore parity is **not** a scalar eigenfunction of the full support operator.

Instead it is multiplied by a support-dependent attenuation field.

---

# 9. No exact two-state parity closure

One might hope to compress the support process to just two states:

\[
\{\text{odd support},\text{even support}\}.
\]

That would require every odd support to have the same parity-toggle rate and every even support to have the same toggle rate.

But:

\[
q_{n,\ell}
=
\frac{
2(\ell+1)(n+1-\ell)
}{
(n+2)(n+3)
}
\]

depends explicitly on \(\ell\).

Therefore:

\[
\boxed{
\text{support parity is not strongly lumpable}.
}
\]

The finite audit shows:

- \(n=4\): trivially lumpable because only one support exists;
- \(n=6\): trivially lumpable because each parity class contains one support;
- \(n=8\): first genuine failure.

At \(n=8\):

\[
q_{8,2}=\frac{21}{55},
\]

while:

\[
q_{8,4}=\frac{5}{11}.
\]

Both parent supports are even, but their sector-toggle rates differ.

Thus no exact autonomous two-state parity chain exists.

---

# 10. Consequence for LR3

This result sharpens the status of LR3.

Odd support as a whole is the bipartition-preserving family.

LR3 is the smallest nontrivial member of that family.

But the branching operator does not collapse all odd supports into one exact propagation species.

Therefore:

\[
\boxed{
\text{LR3's distinction cannot be reduced to parity alone}.
}
\]

Parity explains why LR3 belongs to the preserving class.

Strict locality/minimality is still required to distinguish it from larger odd supports such as LR5, LR7, and so on.

This is exactly consistent with Foundation v1.0.

---

# 11. General half-cycle onset law

A support species \(LR_\ell\) first appears at:

\[
n=2\ell.
\]

At that even parent boundary:

\[
a=b=\ell+1.
\]

The two-step sector-toggle fraction becomes:

\[
\boxed{
q_{2\ell,\ell}
=
\frac{\ell+1}{2\ell+3}.
}
\]

The attenuation is:

\[
\boxed{
\eta_{2\ell,\ell}
=
\frac{1}{2\ell+3}.
}
\]

Thus a support species is born into a regime of nearly maximal sector-tag mixing.

For large \(\ell\):

\[
q_{2\ell,\ell}\to\frac12,
\]

and:

\[
\eta_{2\ell,\ell}\to0.
\]

This is a general support-onset theorem.

---

# 12. LR3 onset

For LR3:

\[
\ell=3,
\qquad
n=6.
\]

Therefore:

\[
\boxed{
q_{6,3}
=
\frac49.
}
\]

So over:

\[
6\to7\to8,
\]

the LR3 intrinsic sector tag is preserved with fraction:

\[
\boxed{
\frac59,
}
\]

and toggled with fraction:

\[
\boxed{
\frac49.
}
\]

Its attenuation is only:

\[
\boxed{
\eta_{6,3}
=
\frac19.
}
\]

Thus LR3 is **only weakly sector-tag persistent at its onset**.

That is an interesting complement to GROW-01:

- LR3 first appears at \(n=6\);
- all \(LR3_6\) ancestry comes from LR2;
- over the next even-to-even growth interval its preserving/changing tag is almost evenly mixed.

---

# 13. LR3 exact parity-propagation law

For even:

\[
n\ge6,
\]

set:

\[
\ell=3.
\]

Then:

\[
\boxed{
q_3(n)
=
\frac{
8(n-2)
}{
(n+2)(n+3)
}.
}
\]

This is the exact fraction of LR3 descendant relation lifts whose target even-layer intrinsic-sector tag is opposite to the parent LR3 tag.

Since LR3 has:

\[
\sigma=+1,
\]

the preserving fraction is:

\[
\boxed{
1-
\frac{
8(n-2)
}{
(n+2)(n+3)
}.
}
\]

The attenuation is:

\[
\boxed{
\eta_3(n)
=
1-
\frac{
16(n-2)
}{
(n+2)(n+3)
}.
}
\]

---

# 14. Large-\(n\) LR3 regime

For fixed support:

\[
\ell=3,
\]

\[
q_3(n)
\sim
\frac8n.
\]

Hence:

\[
\boxed{
q_3(n)\to0.
}
\]

And:

\[
\boxed{
\eta_3(n)\to1.
}
\]

So LR3 becomes increasingly stable with respect to the intrinsic sector tag over local even-to-even growth intervals.

This parallels GROW-01's one-step support persistence:

\[
\frac{n-2}{n+1}\to1.
\]

Large layers locally preserve both:

- LR3 support identity;
- LR3's intrinsic parity-sector tag.

---

# 15. Fixed-support general asymptotic

For any fixed \(\ell\):

\[
q_{n,\ell}
=
\frac{
2(\ell+1)(n+1-\ell)
}{
(n+2)(n+3)
}
\]

gives:

\[
\boxed{
q_{n,\ell}
\sim
\frac{2(\ell+1)}{n}.
}
\]

Therefore:

\[
\boxed{
\eta_{n,\ell}\to1.
}
\]

Every fixed finite support becomes locally sector-tag stable at large \(n\).

LR3 is not unique in this asymptotic behavior.

---

# 16. Extensive-support scaling

A different limit occurs when support grows proportionally with system size.

Let:

\[
\frac{\ell}{n}\to x,
\qquad
0\le x\le\frac12.
\]

Then:

\[
\boxed{
q_{n,\ell}
\to
2x(1-x).
}
\]

And:

\[
\boxed{
\eta_{n,\ell}
\to
(1-2x)^2.
}
\]

Thus near-half-cycle support:

\[
x\approx\frac12
\]

remains strongly sector-mixing even at large \(n\).

Low/local support:

\[
x\approx0
\]

becomes sector-stable.

This gives the parity branch a clear local-versus-extensive support distinction.

---

# 17. Two-step channel decomposition

The two-step operator can be separated into parity-preserving and parity-flipping path classes.

Write:

\[
P_t=S_t+R_t.
\]

Then:

\[
K_n
=
P_nP_{n+1}
\]

expands as:

\[
\boxed{
K_n^{(+)}
=
S_nS_{n+1}
+
R_nR_{n+1},
}
\]

and:

\[
\boxed{
K_n^{(-)}
=
S_nR_{n+1}
+
R_nS_{n+1}.
}
\]

The \(+\) part contains zero or two support raises.

The \(-\) part contains exactly one support raise.

Thus:

\[
\boxed{
K_n
=
K_n^{(+)}
+
K_n^{(-)}.
}
\]

At even endpoints, these are exactly the intrinsic sector-tag preserving and toggling pieces.

This is the two-step parity-sector intertwining decomposition.

---

# 18. Relation to the Pólya representation

In the unfolded Pólya variables:

\[
a=\ell+1,
\qquad
b=n+1-\ell,
\]

the two-step increment count \(s\) has beta-binomial weights.

For two steps:

\[
s\in\{0,1,2\}.
\]

Parity is preserved when:

\[
s=0\text{ or }2,
\]

and flipped when:

\[
s=1.
\]

The beta-binomial one-increment weight is precisely:

\[
\boxed{
\Pr(s=1)
=
\frac{2ab}{(a+b)(a+b+1)}.
}
\]

Therefore the intrinsic parity-intertwining theorem is an exact folded consequence of the Pólya operator.

No additional parity dynamics was inserted.

---

# 19. Actual HC-sector enumeration

The formula-level operator audit was independently checked against explicit Hamilton-cycle relation fibres.

Two even-to-even intervals were enumerated:

\[
4\to6,
\]

and:

\[
6\to8.
\]

The intrinsic bipartitions of the actual parent and target HC pairs were computed directly.

For every audited relation:

\[
\boxed{
\Pi_{\rm intr}(C)=\Pi_{\rm intr}(D)
\iff
\ell\text{ odd}.
}
\]

The per-parent descendant distributions matched the exact two-step support operator.

---

# 20. Explicit \(4\to6\) result

At parent:

\[
n=4,
\]

only:

\[
LR2
\]

exists.

Each parent LR2 relation has:

\[
42
\]

two-step descendant relation lifts.

Their support distribution is:

\[
\boxed{
LR2:\frac47,
\qquad
LR3:\frac37.
}
\]

Thus:

- same intrinsic sector tag:
  \[
  \boxed{24}
  \]
  descendants;
- flipped intrinsic sector tag:
  \[
  \boxed{18}
  \]
  descendants.

The normalized flip fraction is:

\[
\boxed{
\frac37.
}
\]

---

# 21. Explicit \(6\to8\) result from LR2

Each parent:

\[
LR2_6
\]

relation has:

\[
72
\]

two-step descendant relation lifts.

The exact support distribution is:

\[
\boxed{
LR2:\frac{5}{12},
}
\]

\[
\boxed{
LR3:\frac{5}{12},
}
\]

\[
\boxed{
LR4:\frac16.
}
\]

Since parent LR2 is bipartition-changing:

- LR2 and LR4 descendants retain the changing tag;
- LR3 descendants flip to the preserving tag.

Thus:

\[
\boxed{
42
}
\]

descendants retain the parent sector tag, while:

\[
\boxed{
30
}
\]

toggle it.

So:

\[
q_{6,2}
=
\frac{30}{72}
=
\boxed{
\frac5{12}.
}
\]

---

# 22. Explicit \(6\to8\) result from LR3

Each parent:

\[
LR3_6
\]

relation has:

\[
72
\]

two-step descendant relation lifts.

The exact distribution is:

\[
\boxed{
LR3:\frac59,
}
\]

\[
\boxed{
LR4:\frac49.
}
\]

Because LR3 preserves the intrinsic bipartition and LR4 changes it:

- \(40\) descendants preserve the parent sector tag;
- \(32\) descendants toggle it.

Hence:

\[
\boxed{
q_{6,3}
=
\frac49.
}
\]

This directly verifies the LR3 onset formula on the actual HC sector geometry.

---

# 23. What the audit says about LR3

The result is neither “LR3 is uniquely protected by parity” nor “parity is irrelevant.”

The exact status is:

1. **Odd support is the intrinsic bipartition-preserving class.**
2. **LR3 is the smallest nontrivial member of that class.**
3. **Growth mixes odd and even support through the raised-support branch.**
4. **The mixing is support-dependent.**
5. **Parity alone is not an autonomous coarse variable.**
6. **LR3 becomes locally parity-stable at large \(n\), but so does every fixed finite support.**
7. **Therefore the unique preference for LR3 still requires the separate strict-locality/minimality criterion.**

This is a clean compatibility result rather than a new LR3-selection mechanism.

---

# 24. Why this matters for the EHF dependency structure

Foundation v1.0 separated:

\[
\text{structural support geometry}
\]

from:

\[
\text{LR3 move selection}.
\]

GROW-03A confirms that this separation is necessary.

The branching operator contains an exact intrinsic parity grading, but that grading selects:

\[
\boxed{
\text{all odd supports},
}
\]

not:

\[
\boxed{
LR3\text{ alone}.
}
\]

Thus the current dependency chain remains:

\[
\text{raw HC}
\to
\text{support geometry}
\to
\text{odd/even parity class},
\]

followed, only with the additional locality/minimality principle, by:

\[
\boxed{
LR3.
}
\]

No circularity is introduced by the growth branch.

---

# 25. Certification

The audit contains:

### Formula/operator checks

\[
359/359
\]

passed.

These cover:

- one-step parity decomposition;
- exact even-to-even toggle law;
- attenuation identity;
- parity-lumpability status;
- LR3 formula;
- general onset law.

### Explicit HC-sector enumeration

\[
3/3
\]

relation-family checks passed.

Combined:

\[
\boxed{
362/362
}
\]

strict checks passed.

---

# 26. Main verdict

The reversal-support branching operator intertwines with intrinsic parity sectors in an exact but non-closed way.

The one-step operator has a \(\mathbb Z_2\) decomposition:

\[
\boxed{
P_n
=
P_n^{\rm even}
+
P_n^{\rm odd},
}
\]

where:

- same support is parity-even;
- raised support is parity-odd.

Across the natural even-to-even interval:

\[
\boxed{
K_n=P_nP_{n+1},
}
\]

the intrinsic sector-toggle fraction is:

\[
\boxed{
q_{n,\ell}
=
\frac{
2(\ell+1)(n+1-\ell)
}{
(n+2)(n+3)
}.
}
\]

The parity observable obeys:

\[
\boxed{
K_n\sigma
=
\eta_{n,\ell}\sigma,
}
\]

with support-dependent attenuation:

\[
\boxed{
\eta_{n,\ell}
=
\frac{
(n-2\ell)^2+n+2
}{
(n+2)(n+3)
}.
}
\]

Because \(\eta\) depends on \(\ell\), intrinsic parity is not an exact two-state Markov/lumped channel.

For LR3:

\[
\boxed{
q_3(n)
=
\frac{
8(n-2)
}{
(n+2)(n+3)
},
}
\]

so LR3 is nearly maximally sector-mixed at its \(n=6\) onset but becomes locally sector-stable as \(n\) grows.

This strengthens the existing interpretation:

\[
\boxed{
\text{parity identifies the odd-support family; locality/minimality identifies LR3 within it.}
}
\]

---

# 27. Recommended next probe

The cleanest continuation is:

## EHF-HC-GROW-04 — Selected-LR3 Stability Under Growth

Now explicitly add the optional LR3 move-selection package and quantify:

1. how much selected LR3 structure is inherited;
2. how much selected LR3 is newly supplied from the unselected LR2 channel;
3. how much of a selected LR3 parent branches into unselected LR4;
4. whether repeated growth admits an exact selected/unselected balance law;
5. whether any normalized LR3 retention observable survives large growth.

This would be the first GROW probe to study the consequences of **choosing LR3**, rather than the universal support geometry itself.


---

# EHF-HC-GROW-04 — Selected-LR3 Stability Under Growth

**Branch:** EHF-HC-GROW  
**Inputs:** EHF-HC Foundation v1.0, GROW-01, GROW-02, GROW-03A  
**Additional assumption:** LR3 is selected as the admissible same-layer move relation  
**Status:** Exact selected-channel balance and renewal theorem package  
**Primary result:** Selected LR3 is a stable layerwise relation class but not a growth-closed lineage; it is continuously renewed from LR2 while feeding LR4.

---

# 1. Purpose

The earlier GROW probes deliberately studied the universal reversal-support geometry without selecting LR3.

GROW-04 now turns on the optional modelling choice:

\[
\boxed{
\text{selected same-layer relation}=LR3.
}
\]

The question is:

> **Once LR3 is selected, how stable is that selected relation under graded growth?**

There are several non-equivalent notions of stability:

1. **closure:** does selected LR3 grow only into selected LR3?
2. **autonomy:** does target LR3 come only from selected LR3 parents?
3. **stock persistence:** what fraction of target LR3 is inherited rather than newly generated?
4. **lineage persistence:** how much of an old selected LR3 lineage remains selected after many layers?
5. **population renewal:** how old is a typical LR3 relation in the target class?
6. **relative density:** how large is selected LR3 compared with the full 2-opt shell?

The audit answers all six.

---

# 2. Selection projector

Let:

\[
Q_n
\]

denote the projector from the support-relation space at size \(n\) onto the selected support class:

\[
LR3.
\]

Let:

\[
B_n
\]

be the raw support branching operator from GROW-02.

If LR3 were growth-closed, one would have:

\[
(I-Q_{n+1})B_nQ_n=0.
\]

If LR3 were autonomously generated, one would have:

\[
Q_{n+1}B_n(I-Q_n)=0.
\]

Neither is true.

For generic parent:

\[
n\ge7,
\]

the exact cross-block coefficients are:

\[
\boxed{
Q_{n+1}B_nQ_n:
\quad
LR3\to LR3
\text{ with multiplicity }n-2,
}
\]

\[
\boxed{
Q_{n+1}B_n(I-Q_n):
\quad
LR2\to LR3
\text{ with multiplicity }3,
}
\]

and:

\[
\boxed{
(I-Q_{n+1})B_nQ_n:
\quad
LR3\to LR4
\text{ with multiplicity }4.
}
\]

Thus:

\[
\boxed{
Q_{n+1}B_n(I-Q_n)\neq0,
}
\]

and:

\[
\boxed{
(I-Q_{n+1})B_nQ_n\neq0.
}
\]

Selected LR3 is therefore an **open support channel**.

---

# 3. Boundary sequence

The first three layers require explicit treatment.

## \(5\to6\)

LR3 does not exist at size \(5\).

At size \(6\):

\[
\boxed{
LR3_6
}
\]

is the half-cycle class.

Every selected LR3 edge is generated from LR2:

\[
\boxed{
LR2_5\to LR3_6
}
\]

with multiplicity:

\[
\boxed{3}
\]

per LR2 parent edge.

Thus selected LR3 is born entirely from an unselected lower-support channel.

## \(6\to7\)

Each half-cycle LR3 parent has:

\[
\boxed{8}
\]

faithful LR3 child lifts.

LR4 does not yet exist.

So:

\[
\boxed{
LR3_6\to LR3_7
}
\]

is forward-closed at this one exceptional boundary step.

But target \(LR3_7\) still also receives new LR3 from LR2.

## \(7\to8\)

The generic open-channel structure begins:

\[
\boxed{
LR2\overset{3}{\longrightarrow}LR3
}
\]

and:

\[
\boxed{
LR3
\overset{5}{\longrightarrow}
LR3,
\qquad
LR3
\overset{4}{\longrightarrow}
LR4.
}
\]

At \(N=8\), LR4 itself first appears, so every LR4 edge at that layer is generated from LR3.

---

# 4. Exact selected stock counts

Let:

\[
E_\ell(n)
=
|E(LR_\ell^{(n)})|.
\]

For generic support:

\[
E_\ell(n)=\frac{n!}{4}.
\]

For a half-cycle support:

\[
E_{n/2}(n)=\frac{n!}{8}.
\]

Thus:

\[
E_3(6)=\frac{6!}{8}=90,
\]

while:

\[
\boxed{
E_3(n)=\frac{n!}{4}
\qquad
(n\ge7).
}
\]

So the selected relation-edge stock grows factorially in absolute size.

That absolute growth should not be confused with hereditary stability.

---

# 5. Exact target-stock balance

Let the target size be:

\[
N=n+1.
\]

For:

\[
N\ge8,
\]

the selected LR3 target stock satisfies:

\[
\boxed{
E_3(N)
=
(N-3)E_3(N-1)
+
3E_2(N-1).
}
\]

The first term is inherited selected LR3.

The second term is newly generated selected LR3 supplied by the unselected LR2 channel.

Since for generic parent size:

\[
E_2(N-1)=E_3(N-1)=\frac{(N-1)!}{4},
\]

the recursion becomes:

\[
\boxed{
E_3(N)
=
N\,E_3(N-1).
}
\]

This exactly matches:

\[
E_3(N)=\frac{N!}{4}.
\]

Thus the selected class is maintained by a mixture of inheritance and renewal.

---

# 6. Selected target-stock composition

For every target:

\[
N\ge7,
\]

the exact census fraction inherited from LR3 is:

\[
\boxed{
f_{\rm inherited}(N)
=
\frac{N-3}{N}.
}
\]

The newly supplied fraction from LR2 is:

\[
\boxed{
f_{\rm new}(N)
=
\frac3N.
}
\]

At onset:

\[
N=6,
\]

\[
\boxed{
f_{\rm new}(6)=1.
}
\]

Therefore local renewal becomes small:

\[
\boxed{
f_{\rm new}(N)\sim\frac3N.
}
\]

At large \(N\), almost every target LR3 edge has an LR3 parent one layer below.

That does **not** imply old LR3 ancestry dominates over long growth intervals.

---

# 7. Forward leakage from selected LR3

For generic parent:

\[
n\ge7,
\]

each selected LR3 edge produces:

\[
\boxed{
n-2
}
\]

selected LR3 children and:

\[
\boxed{
4
}
\]

unselected LR4 children.

Among all \(n+2\) relation lifts of one selected LR3 parent, the selected retention fraction is:

\[
\boxed{
r_3(n)
=
\frac{n-2}{n+2}.
}
\]

The selected-to-unselected leakage fraction is:

\[
\boxed{
\ell_3(n)
=
\frac4{n+2}.
}
\]

Thus:

\[
r_3(n)\to1
\]

locally, while:

\[
\ell_3(n)\sim\frac4n.
\]

Again, local near-closure emerges at large \(n\), but exact closure never occurs in the generic regime.

---

# 8. Exact cross-support census flux ratio

For:

\[
n\ge7,
\]

generic class sizes satisfy:

\[
E_2(n)=E_3(n)=\frac{n!}{4}.
\]

Therefore the number of new selected LR3 edges generated from LR2 is:

\[
\boxed{
G_{2\to3}(n)
=
3E_2(n).
}
\]

The number of unselected LR4 descendants generated from selected LR3 is:

\[
\boxed{
G_{3\to4}(n)
=
4E_3(n).
}
\]

Hence:

\[
\boxed{
G_{2\to3}:G_{3\to4}
=
3:4.
}
\]

This is an exact generic cross-support generation ratio.

It should not be interpreted as a conserved physical current.

It is a finite relation-census statement.

---

# 9. Selection is layerwise, not hereditary

The operator result has a direct modelling consequence.

If the model states:

> at every layer, LR3 is the selected admissible same-layer move,

then the selection criterion must be applied **at each layer**.

Raw growth does not carry the selected subspace into itself.

Some selected LR3 descendants leave selection through:

\[
LR3\to LR4.
\]

Some target selected LR3 relations enter selection from:

\[
LR2\to LR3.
\]

Thus:

\[
\boxed{
\text{LR3 selection is a layerwise classification on top of growth, not a growth-invariant subfunctor.}
}
\]

This is the central structural verdict of GROW-04.

---

# 10. Renewal question

A target LR3 edge may have an LR3 parent, whose parent may also be LR3, and so on.

Eventually, tracing backward, its support drops to LR2.

Define:

\[
\boxed{
G
=
\text{the layer at which the lineage most recently entered LR3 from LR2}.
}
\]

This gives an exact renewal-cohort decomposition of the selected class.

---

# 11. Onset cohort

LR3 first appears at:

\[
G=6.
\]

The fraction of LR3 edges at target size \(N\) belonging to this original onset cohort is:

\[
\boxed{
\Pr_{\rm census}(G=6)
=
\frac{120}{
N(N-1)(N-2)
}.
}
\]

Equivalently:

\[
\boxed{
\Pr_{\rm census}(G=6)
=
\frac{(6)_3}{(N)_3}.
}
\]

This is exactly the GROW-01 all-faithful ancestry fraction from \(N\) back to \(6\).

Thus the original LR3 population becomes a vanishing fraction of the later selected class:

\[
\boxed{
\Pr(G=6)\sim120\,N^{-3}.
}
\]

---

# 12. General generation cohort

For:

\[
7\le g\le N,
\]

the exact target-stock fraction whose LR3 ancestry most recently entered from LR2 at layer \(g\) is:

\[
\boxed{
\Pr_{\rm census}(G=g)
=
\frac{
3(g-1)(g-2)
}{
N(N-1)(N-2)
}.
}
\]

The special \(g=6\) boundary cohort has twice the naive continuation of this generic expression because \(LR3_6\) is a half-cycle class.

The complete cohort weights sum exactly to:

\[
\boxed{1}.
\]

So the selected target class has an exact renewal decomposition by generation layer.

---

# 13. Cumulative renewal law

For:

\[
6\le m\le N,
\]

the fraction of target LR3 stock whose selected ancestry already existed by layer \(m\) is:

\[
\boxed{
\Pr_{\rm census}(G\le m)
=
\frac{
m(m-1)(m-2)
}{
N(N-1)(N-2)
}.
}
\]

Therefore the fraction renewed from LR2 **after** layer \(m\) is:

\[
\boxed{
\Pr_{\rm census}(G>m)
=
1-
\frac{
(m)_3
}{
(N)_3
}.
}
\]

This is an exact turnover law.

---

# 14. Local renewal versus cumulative turnover

The immediately new fraction at target \(N\) is only:

\[
\frac3N.
\]

But cumulative renewal over a macroscopic fraction of the growth history is much larger.

Let:

\[
m\sim\alpha N.
\]

Then:

\[
\boxed{
\Pr(G\le\alpha N)
\to
\alpha^3.
}
\]

Therefore:

\[
\boxed{
\Pr(G>\alpha N)
\to
1-\alpha^3.
}
\]

For example, after the halfway layer:

\[
\alpha=\frac12,
\]

so:

\[
\boxed{
\Pr(G>N/2)
\to
1-\frac18
=
\frac78.
}
\]

Thus asymptotically:

\[
\boxed{
87.5\%
}
\]

of the selected LR3 target stock was generated from LR2 after the halfway point of the growth history.

This is compatible with the small one-step renewal fraction because many small renewal contributions accumulate.

---

# 15. Limiting generation-layer distribution

Scale the generation layer by the target size:

\[
X_N=\frac GN.
\]

The cumulative law gives:

\[
\boxed{
\Pr(X_N\le x)\to x^3
\qquad
0\le x\le1.
}
\]

Thus the limiting density is:

\[
\boxed{
f(x)=3x^2.
}
\]

Under uniform target-edge sampling, this is a:

\[
\boxed{
\operatorname{Beta}(3,1)
}
\]

generation-time distribution.

The beta language is stochastic shorthand for the normalized census limit.

---

# 16. Exact mean generation layer

The cohort law gives:

\[
\boxed{
\mathbb E_{\rm census}[G]
=
\frac{3(N+1)}4
+
\frac{90}{
N(N-1)(N-2)
}.
}
\]

Hence:

\[
\boxed{
\frac{\mathbb E[G]}N\to\frac34.
}
\]

The mean selected ancestry age is:

\[
N-\mathbb E[G].
\]

Therefore:

\[
\boxed{
N-\mathbb E[G]
\sim
\frac N4.
}
\]

So a typical selected LR3 relation at a large layer does not trace faithfully back to the origin of LR3.

Its most recent LR2-to-LR3 renewal occurs, on average, around three-quarters of the way through the growth history.

---

# 17. Population ancestry persistence

Fix a reference layer:

\[
n\ge6.
\]

The fraction of target LR3 edges at size \(N\) whose ancestry remains LR3 continuously all the way back to \(n\) is:

\[
\boxed{
A_3(n,N)
=
\frac{
n(n-1)(n-2)
}{
N(N-1)(N-2)
}.
}
\]

For fixed \(n\):

\[
\boxed{
A_3(n,N)\sim \text{const}\cdot N^{-3}.
}
\]

Thus the old selected population loses representation inside the later selected stock as a cubic power.

---

# 18. Individual selected-lineage persistence

Now condition instead on one fixed selected LR3 parent edge at size \(n\).

Among all of its 2-opt relation descendants at size \(N\), the fraction remaining on a completely faithful selected LR3 lineage is the GROW-01 forward fidelity:

For generic:

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

At the half-cycle onset parent:

\[
n=6,
\]

the first-step doubled fibre gives an additional factor:

\[
2
\]

for:

\[
N>6.
\]

For fixed \(n\):

\[
\boxed{
F_3(n,N)\sim \text{const}\cdot N^{-4}.
}
\]

So individual selected lineages are even less persistent than old selected population cohorts.

---

# 19. Stable class versus unstable lineage

Three exact scaling laws should be kept separate.

## Selected class density within full 2-opt

For:

\[
N\ge7,
\]

\[
\boxed{
\frac{
|E(LR3_N)|
}{
|E(2opt_N)|
}
=
\frac{2}{N-3}.
}
\]

Thus:

\[
\boxed{
\sim\frac2N.
}
\]

At \(N=6\), the half-cycle value is:

\[
\boxed{\frac13}.
\]

## Old selected ancestry within selected LR3

For fixed reference \(n\):

\[
\boxed{
A_3(n,N)\sim N^{-3}.
}
\]

## One fixed selected lineage among all descendants

\[
\boxed{
F_3(n,N)\sim N^{-4}.
}
\]

Therefore:

\[
\boxed{
\text{class density}\sim N^{-1},
\quad
\text{old selected ancestry}\sim N^{-3},
\quad
\text{fixed lineage fidelity}\sim N^{-4}.
}
\]

This hierarchy is one of the clearest outcomes of the audit.

---

# 20. Absolute abundance versus relative density

Although the LR3 fraction of the full 2-opt shell decays as:

\[
N^{-1},
\]

its absolute edge count is:

\[
\boxed{
|E(LR3_N)|
=
\frac{N!}{4}
}
\]

for:

\[
N\ge7.
\]

Thus selected LR3 becomes:

- enormously larger in absolute count;
- smaller as a proportion of the full nearest-shell relation space.

There is no contradiction.

“Stable” therefore needs an explicitly stated normalization.

---

# 21. Exact selection-density law

The full 2-opt edge count is:

\[
\boxed{
|E(2opt_N)|
=
\frac{
N!(N-3)
}{8}.
}
\]

For generic LR3:

\[
|E(LR3_N)|=\frac{N!}{4}.
\]

Therefore:

\[
\boxed{
\rho_3(N)
=
\frac{2}{N-3}
}
\]

for:

\[
N\ge7.
\]

So selecting only LR3 retains an \(O(N^{-1})\) fraction of the raw nearest-shell edge set at large \(N\).

At the degree level the same result holds:

\[
\deg(LR3)=N,
\]

while:

\[
\deg(2opt)=\frac{N(N-3)}2,
\]

giving:

\[
\frac{\deg(LR3)}{\deg(2opt)}
=
\frac2{N-3}.
\]

---

# 22. Exact local open-channel balance

For generic parent \(n\ge7\), the selected support channel can be summarized:

\[
\boxed{
LR2
\overset{3}{\longrightarrow}
\boxed{LR3}
\overset{4}{\longrightarrow}
LR4
}
\]

while selected self-inheritance contributes:

\[
\boxed{
LR3
\overset{n-2}{\longrightarrow}
LR3.
}
\]

This is the simplest exact selected-channel diagram.

The coefficients \(3\) and \(4\) are support-generated constants.

The self-inheritance coefficient grows linearly with layer size.

Hence selected LR3 becomes increasingly locally self-reproducing, but never structurally isolated.

---

# 23. Why this does not create a physical dynamics

The audit has introduced the modelling label:

\[
\text{selected}=LR3.
\]

It has **not** introduced:

- a physical time step;
- a probability of actual evolution;
- a particle propagation law;
- an energy cost;
- a causal velocity.

The coefficients are relation-lift multiplicities and normalized census fractions.

A physical or stochastic dynamics would require an additional rule specifying how relation lifts are sampled or realized.

---

# 24. Explicit HC enumeration

The selected-channel equations were independently checked on actual Hamilton-cycle relation sets.

## \(5\to6\)

Parent:

\[
|E(LR2_5)|=30.
\]

Each LR2 edge has exactly:

\[
3
\]

LR3 lifts.

Therefore:

\[
\boxed{
90
}
\]

target LR3 edges are generated.

This is the entire:

\[
LR3_6
\]

class.

## \(6\to7\)

Parent:

\[
|E(LR3_6)|=90.
\]

Each has:

\[
8
\]

faithful LR3 lifts:

\[
720.
\]

Parent:

\[
|E(LR2_6)|=180.
\]

Each has:

\[
3
\]

new LR3 lifts:

\[
540.
\]

Total:

\[
\boxed{
720+540=1260
=
|E(LR3_7)|.
}
\]

## \(7\to8\)

Parent LR3 edges:

\[
1260.
\]

Faithful selected lifts:

\[
5\times1260=6300.
\]

Parent LR2 edges:

\[
1260.
\]

New selected LR3 lifts:

\[
3\times1260=3780.
\]

Thus:

\[
\boxed{
6300+3780=10080
=
|E(LR3_8)|.
}
\]

The same parent LR3 class generates:

\[
4\times1260
=
\boxed{
5040
}
\]

LR4 target edges.

Since LR4 first appears at \(N=8\), this is the entire LR4 class.

Every enumerated fibre had exactly the predicted multiplicity.

---

# 25. Main structural interpretation

The selected LR3 relation has two different kinds of stability.

## Layerwise class stability

At every sufficiently large layer there is a large, well-defined LR3 relation class.

Most target LR3 edges have LR3 parents one layer below:

\[
\frac{N-3}{N}\to1.
\]

Most descendants of a selected LR3 parent remain LR3 one layer above:

\[
\frac{n-2}{n+2}\to1.
\]

So LR3 is locally stable under large-\(n\) growth.

## Genealogical instability

Over many layers:

- old LR3 cohorts become negligible as \(N^{-3}\);
- fixed LR3 lineages become negligible as \(N^{-4}\);
- the selected class is continually replenished from LR2.

Thus:

\[
\boxed{
\text{selected LR3 is locally persistent but globally renewal-dominated.}
}
\]

This is the most concise statement of GROW-04.

---

# 26. Consequence for the selected-move model

If LR3 is adopted as the admissible same-layer move, then the rule:

\[
\boxed{
\text{“at layer }n,\text{ admissible relation}=LR3_n”}
\]

must be understood as a **fresh structural classification at each layer**.

It is not equivalent to:

> take the selected relations at one layer and propagate only their descendants.

The latter would progressively lose the LR2-generated part of the selected class and would incorrectly retain only one genealogy.

Thus the selection principle acts on the current layer geometry, not on ancestry labels.

This distinction could matter substantially in any later attempt to interpret LR3 as a physical admissibility rule.

---

# 27. Certification

GROW-04 contains three independent check groups.

### Selected-stock / cohort formula checks

\[
100/100
\]

passed.

### Explicit HC relation enumeration

\[
3/3
\]

passed.

### Selection-density / cumulative-renewal checks

\[
665/665
\]

passed.

Combined:

\[
\boxed{
768/768
}
\]

strict checks passed.

---

# 28. GROW-04 verdict

Once LR3 is selected, it forms an exact **open branching channel**:

\[
\boxed{
LR2
\longrightarrow
\boxed{LR3}
\longrightarrow
LR4.
}
\]

For generic growth:

\[
\boxed{
LR2\to LR3
\text{ multiplicity}=3,
}
\]

\[
\boxed{
LR3\to LR3
\text{ multiplicity}=n-2,
}
\]

\[
\boxed{
LR3\to LR4
\text{ multiplicity}=4.
}
\]

Target selected LR3 is locally dominated by inheritance:

\[
\boxed{
\frac{N-3}{N},
}
\]

but the complete selected population has an exact renewal law:

\[
\boxed{
\Pr(G>m)
=
1-\frac{(m)_3}{(N)_3}.
}
\]

Hence asymptotically:

\[
\boxed{
G/N
\text{ has census density }3x^2.
}
\]

The selected class is therefore:

\[
\boxed{
\text{locally persistent, continuously renewed, and genealogically non-conserved}.
}
\]

Selecting LR3 does not create a growth-invariant subspace.

It defines a layerwise admissibility criterion on the universal support-growth geometry.

---

# 29. Recommended next probe

Two continuations are now especially clean.

## EHF-HC-GROW-05 — General Selected-Support Renewal Theorem

Replace \(3\) by arbitrary selected support \(\ell\).

Expected targets:

- inflow \(LR_{\ell-1}\to LR_\ell\) coefficient \(\ell\);
- outflow \(LR_\ell\to LR_{\ell+1}\) coefficient \(\ell+1\);
- exact cohort law;
- ancestry exponent \(N^{-\ell}\);
- lineage exponent \(N^{-(\ell+1)}\);
- class-density scaling;
- onset boundary.

This would show exactly which parts of GROW-04 are genuinely LR3-specific.

## EHF-HC-GROW-05A — LR3 Selection with Sector/Fibre Geometry

Keep LR3 selected and lift the open-channel balance from support counts back to:

- intrinsic bipartition fibres;
- horizontal/vertical LR2 channels;
- Johnson \(A_1\);
- selected LR3 component geometry.

This would test whether renewal from LR2 has a nontrivial distribution across the emergent Johnson sector structure.


---

# EHF-HC-GROW-05 — General Selected-Support Renewal Theorem

**Branch:** EHF-HC-GROW  
**Inputs:** EHF-HC Foundation v1.0, GROW-01 through GROW-04  
**Status:** Exact general selected-support theorem package  
**Primary result:** The LR3 renewal laws are the \(\ell=3\) member of a universal fixed-support hierarchy, with one important base exception at \(LR2\).

---

# 1. Purpose

GROW-04 found that selected LR3 is:

- locally persistent;
- continually renewed from LR2;
- open toward LR4;
- genealogically non-conserved.

GROW-05 asks whether this is specifically an LR3 phenomenon or the \(\ell=3\) case of a general selected-support law.

Fix:

\[
\boxed{
LR_\ell
}
\]

as the selected same-layer support relation.

The answer is mostly universal.

---

# 2. Universal support onset

The support class:

\[
LR_\ell
\]

first exists at:

\[
\boxed{
N=2\ell.
}
\]

At this onset it is the half-cycle class.

Every target \(LR_\ell\) relation is generated from the lower support channel.

For:

\[
\ell\ge3,
\]

the lower source is the ordinary relation:

\[
LR_{\ell-1}.
\]

Each such parent edge generates exactly:

\[
\boxed{\ell}
\]

new \(LR_\ell\) target edges.

Thus:

\[
\boxed{
LR_{\ell-1}
\overset{\ell}{\longrightarrow}
LR_\ell
}
\]

is the generic support-onset mechanism.

---

# 3. The LR2 base exception

For:

\[
\ell=2,
\]

the formal lower relation is:

\[
LR_1=id.
\]

But identity is a diagonal/vertex relation, not an ordinary edge class.

Therefore the per-parent inflow law is different.

At parent size \(n=N-1\), each identity state produces:

\[
\boxed{n}
\]

new LR2 target edges.

For example:

\[
HC_3
\to
LR2_4
\]

has:

\[
1\times3=3
\]

generated LR2 edges.

At:

\[
4\to5,
\]

each of the three parent identity states contributes four new LR2 target edges.

The **normalized renewal law still obeys the same \(\ell=2\) formulas**.

What fails is only the naive statement that the lower per-parent multiplicity is always \(\ell\).

Therefore LR2 is the base channel of the hierarchy rather than an ordinary interior channel.

---

# 4. Why LR3 retains one genuine structural distinction

For:

\[
\ell=3,
\]

the lower source is:

\[
LR2,
\]

and the upper branch is:

\[
LR4.
\]

Both are ordinary nontrivial reversal-edge relations.

Hence LR3 is the **first support class sitting between ordinary relation-edge channels on both sides**:

\[
\boxed{
LR2
\longrightarrow
LR3
\longrightarrow
LR4.
}
\]

This does not make LR3 physically special by itself.

But it is a genuine structural distinction that survives the generalization.

---

# 5. Generic selected-support open channel

For selected:

\[
LR_\ell,
\qquad
\ell\ge3,
\]

the generic branching structure is:

\[
\boxed{
LR_{\ell-1}
\overset{\ell}{\longrightarrow}
\boxed{LR_\ell}
\overset{\ell+1}{\longrightarrow}
LR_{\ell+1}.
}
\]

For parent size:

\[
n>2\ell,
\]

the selected self-inheritance multiplicity is:

\[
\boxed{
n+1-\ell.
}
\]

Thus the full generic local channel is:

\[
\boxed{
LR_{\ell-1}
\overset{\ell}{\longrightarrow}
LR_\ell
\overset{n+1-\ell}{\longrightarrow}
LR_\ell
}
\]

together with:

\[
\boxed{
LR_\ell
\overset{\ell+1}{\longrightarrow}
LR_{\ell+1}.
}
\]

The lower inflow and upper outflow multiplicities are support-controlled constants.

The self-inheritance multiplicity grows linearly with layer size.

---

# 6. Half-cycle post-onset fibre

At onset parent:

\[
n=2\ell,
\]

\(LR_\ell\) is a half-cycle class.

On the next growth step, its faithful fibre doubles.

The faithful multiplicity is:

\[
\boxed{
2(\ell+1).
}
\]

The upper class \(LR_{\ell+1}\) is not yet available.

So the first post-onset step is exceptionally forward-closed.

After that, the generic open-channel law applies.

---

# 7. Exact target-stock composition

Let target size be:

\[
N>2\ell.
\]

Then the fraction of selected \(LR_\ell\) target edges inherited from selected \(LR_\ell\) parents is:

\[
\boxed{
f_{\rm inherited}(N,\ell)
=
\frac{N-\ell}{N}.
}
\]

The newly generated fraction from the lower channel is:

\[
\boxed{
f_{\rm new}(N,\ell)
=
\frac{\ell}{N}.
}
\]

At onset:

\[
N=2\ell,
\]

the new fraction is:

\[
\boxed{1}.
\]

Thus every fixed support becomes locally inheritance-dominated:

\[
\boxed{
f_{\rm new}(N,\ell)\sim\frac{\ell}{N}.
}
\]

LR3's \(3/N\) law is exactly the \(\ell=3\) instance.

---

# 8. Generic gross cross-support flux ratio

Once the upper class exists and the neighboring relation classes are generic, the generated-stock inflow and outflow satisfy:

\[
\boxed{
G_{\ell-1\to\ell}
:
G_{\ell\to\ell+1}
=
\ell:(\ell+1).
}
\]

For LR3 this gives:

\[
3:4.
\]

For LR4:

\[
4:5.
\]

For LR5:

\[
5:6.
\]

Even for LR2, where the lower source is identity rather than an edge class, the **gross generated-stock ratio** becomes:

\[
2:3
\]

once LR3 exists.

So the flux-ratio hierarchy survives the LR2 base anomaly.

---

# 9. Selected-class edge counts

For fixed support \(\ell\):

At onset:

\[
N=2\ell,
\]

\[
\boxed{
|E(LR_\ell^{(N)})|
=
\frac{N!}{8}.
}
\]

After onset:

\[
N>2\ell,
\]

\[
\boxed{
|E(LR_\ell^{(N)})|
=
\frac{N!}{4}.
}
\]

Thus all fixed generic support classes have the same edge count at the same layer.

The support label does not change generic class cardinality.

It changes growth history and parity behavior.

---

# 10. Universal class-density law

The full 2-opt shell contains:

\[
\boxed{
|E(2opt_N)|
=
\frac{N!(N-3)}8.
}
\]

Therefore, for every fixed generic support:

\[
N>2\ell,
\]

\[
\boxed{
\frac{|E(LR_\ell)|}{|E(2opt)|}
=
\frac{2}{N-3}.
}
\]

This is independent of \(\ell\).

At onset:

\[
N=2\ell,
\]

the half-cycle factor gives:

\[
\boxed{
\frac{|E(LR_\ell)|}{|E(2opt)|}
=
\frac{1}{N-3}.
}
\]

Hence support classes are not distinguished by generic raw nearest-shell density.

---

# 11. Renewal generation layer

For a selected target:

\[
LR_\ell^{(N)},
\]

define:

\[
\boxed{
G_\ell
=
\text{the layer where its ancestry most recently entered }LR_\ell
\text{ from the lower channel}.
}
\]

At the onset cohort:

\[
G_\ell=2\ell.
\]

For later cohorts:

\[
G_\ell=g>2\ell.
\]

This gives an exact selected-population renewal decomposition.

---

# 12. Onset cohort weight

The fraction of target selected stock whose selected ancestry reaches continuously back to the original onset layer is:

\[
\boxed{
\Pr_{\rm census}(G_\ell=2\ell)
=
\frac{
(2\ell)_\ell
}{
(N)_\ell
}.
}
\]

Here:

\[
(x)_r
=
x(x-1)\cdots(x-r+1).
\]

Thus the original support population decays inside the later selected stock as:

\[
\boxed{
N^{-\ell}.
}
\]

For LR3:

\[
(6)_3=120,
\]

recovering GROW-04.

---

# 13. General renewal cohort law

For:

\[
2\ell<g\le N,
\]

the exact target-stock cohort weight is:

\[
\boxed{
\Pr_{\rm census}(G_\ell=g)
=
\frac{
\ell\,(g-1)_{\ell-1}
}{
(N)_\ell
}.
}
\]

The proof is the product of:

1. the fraction:

\[
\frac{\ell}{g}
\]

newly entering the selected class at layer \(g\);

2. the all-faithful selected ancestry fraction from \(g\) to \(N\):

\[
\frac{(g)_\ell}{(N)_\ell}.
\]

Multiplying:

\[
\frac{\ell}{g}
\frac{(g)_\ell}{(N)_\ell}
=
\frac{\ell(g-1)_{\ell-1}}{(N)_\ell}.
\]

---

# 14. Exact cumulative renewal theorem

The falling-factorial identity:

\[
(g)_\ell-(g-1)_\ell
=
\ell(g-1)_{\ell-1}
\]

makes the cohort law telescope.

For every threshold:

\[
2\ell\le m\le N,
\]

\[
\boxed{
\Pr_{\rm census}(G_\ell\le m)
=
\frac{
(m)_\ell
}{
(N)_\ell
}.
}
\]

Therefore:

\[
\boxed{
\Pr_{\rm census}(G_\ell>m)
=
1-
\frac{
(m)_\ell
}{
(N)_\ell
}.
}
\]

This is the general selected-support renewal theorem.

---

# 15. Macroscopic renewal limit

Let:

\[
m\sim xN.
\]

Then:

\[
\boxed{
\Pr(G_\ell/N\le x)
\to
x^\ell.
}
\]

Hence the limiting census density is:

\[
\boxed{
f_\ell(x)
=
\ell x^{\ell-1},
\qquad
0\le x\le1.
}
\]

Under uniform target-edge sampling this is:

\[
\boxed{
\operatorname{Beta}(\ell,1).
}
\]

The beta terminology belongs to the normalized sampling interpretation; the finite cohort weights are exact combinatorial counts.

---

# 16. Exact mean generation layer

The exact mean is:

\[
\boxed{
\mathbb E_{\rm census}[G_\ell]
=
\frac{
\ell(N+1)
}{
\ell+1
}
+
\frac{
\ell(2\ell)_\ell
}{
(\ell+1)(N)_\ell
}.
}
\]

Therefore:

\[
\boxed{
\frac{\mathbb E[G_\ell]}{N}
\to
\frac{\ell}{\ell+1}.
}
\]

The mean selected ancestry age satisfies:

\[
\boxed{
\frac{
N-\mathbb E[G_\ell]
}{
N
}
\to
\frac{1}{\ell+1}.
}
\]

So higher-support selected classes are typically younger relative to the total growth history.

---

# 17. Channel-age hierarchy

Asymptotically:

\[
LR2:
\quad
\mathbb E[G]/N\to\frac23,
\]

\[
LR3:
\quad
\mathbb E[G]/N\to\frac34,
\]

\[
LR4:
\quad
\mathbb E[G]/N\to\frac45,
\]

\[
LR5:
\quad
\mathbb E[G]/N\to\frac56.
\]

Equivalently, mean ancestry ages scale as:

\[
LR2:\frac N3,
\]

\[
LR3:\frac N4,
\]

\[
LR4:\frac N5,
\]

\[
LR5:\frac N6.
\]

Thus support size controls an exact renewal-age hierarchy.

---

# 18. Long-range selected-stock ancestry

Fix reference layer:

\[
n\ge2\ell.
\]

The fraction of target selected \(LR_\ell\) stock at \(N\) whose selected ancestry remains faithful all the way back to \(n\) is:

\[
\boxed{
A_\ell(n,N)
=
\frac{
(n)_\ell
}{
(N)_\ell
}.
}
\]

For fixed \(n\):

\[
\boxed{
A_\ell(n,N)
\sim
\text{const}\cdot N^{-\ell}.
}
\]

So the support label is exactly the old-population ancestry exponent.

For LR3 this is:

\[
N^{-3}.
\]

---

# 19. Fixed selected-lineage fidelity

Now start from one fixed selected \(LR_\ell\) parent relation.

For generic reference:

\[
n>2\ell,
\]

the fraction of all 2-opt descendants at \(N\) remaining on a fully faithful selected-support lineage is:

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

If the reference layer is the half-cycle onset:

\[
n=2\ell,
\]

there is an additional factor \(2\) for \(N>n\), coming from the doubled first faithful fibre.

For fixed \(n\):

\[
\boxed{
F_\ell(n,N)
\sim
\text{const}\cdot N^{-(\ell+1)}.
}
\]

Thus:

\[
\boxed{
\text{lineage exponent}
=
\text{support}+1.
}
\]

---

# 20. Universal three-exponent picture

For any fixed selected support \(LR_\ell\):

### Class density within full 2-opt

\[
\boxed{
\sim N^{-1}.
}
\]

### Old selected-stock ancestry

\[
\boxed{
\sim N^{-\ell}.
}
\]

### One fixed selected lineage among all descendants

\[
\boxed{
\sim N^{-(\ell+1)}.
}
\]

Only the last two exponents depend on support.

The generic class density does not.

This cleanly separates:

- abundance in the current layer;
- age of the selected population;
- heredity of an individual selected lineage.

---

# 21. Intrinsic parity remains an independent channel label

On even layers:

\[
\boxed{
\ell\text{ odd}
\iff
\text{intrinsic bipartition preserving},
}
\]

\[
\boxed{
\ell\text{ even}
\iff
\text{intrinsic bipartition changing}.
}
\]

Therefore every channel carries at least two exact structural attributes:

1. support scale \(\ell\);
2. parity tag \((-1)^{\ell+1}\).

The renewal hierarchy does not erase that \(\mathbb Z_2\) distinction.

---

# 22. What is genuinely LR3-specific now?

GROW-05 removes several apparent LR3 specialities.

The following are **not LR3-specific**:

- continual lower-channel renewal;
- upper-channel leakage;
- power-law ancestry;
- power-law lineage fidelity;
- beta-type generation distribution;
- decreasing mean ancestry age;
- generic \(2/(N-3)\) full-shell density.

They all belong to the general \(LR_\ell\) hierarchy.

But LR3 still has genuine structural distinctions:

1. It is the smallest nontrivial **odd** support.
2. Therefore it is the most local nontrivial reversal preserving the intrinsic even bipartition.
3. It is the first support with an ordinary nontrivial relation-edge reservoir on both sides:
   \[
   LR2\to LR3\to LR4.
   \]
4. Its onset occurs at the first even size where a nontrivial odd support exists:
   \[
   N=6.
   \]

These are cleaner reasons to continue treating LR3 separately when appropriate.

---

# 23. Physics-facing interpretation status

The support label now behaves like a mathematically exact **channel index**.

Each channel \(LR_\ell\) has:

- onset \(2\ell\);
- support size \(\ell\);
- parity;
- lower inflow;
- self-inheritance;
- upper outflow;
- renewal-age law;
- ancestry exponent;
- lineage exponent.

This resembles the formal structure of a coupled hierarchy of channels or internal excitation sectors.

But nothing here identifies:

\[
\ell
\]

with:

- energy;
- mass;
- spin;
- charge;
- particle type;
- physical length;
- interaction range.

Those identifications would require a separate bridge.

The appropriate current language is:

\[
\boxed{
LR_\ell
=
\text{reversal-support growth channel}.
}
\]

---

# 24. Explicit HC certification

The general formulas were independently checked against exact HC relation sets for:

\[
LR2,\ LR3,\ LR4.
\]

Audited cases included:

\[
(4,2),\ (5,2),\ (6,2),
\]

\[
(6,3),\ (7,3),\ (8,3),
\]

\[
(8,4),\ (9,4).
\]

Every target-stock inheritance/generation count matched.

The fibre multiplicities reproduced:

- LR2 identity-source boundary;
- half-cycle doubled faithful fibres;
- generic lower-channel coefficients;
- generic upper-channel coefficients.

Exact enumeration:

\[
\boxed{
8/8
}
\]

relation-family checks passed.

---

# 25. Certification

Formula and theorem identities were audited over support values:

\[
2\le\ell\le8
\]

and broad layer ranges.

Formula checks:

\[
\boxed{
3098/3098.
}
\]

Explicit HC enumeration:

\[
\boxed{
8/8.
}
\]

Combined:

\[
\boxed{
3106/3106
}
\]

strict checks passed.

---

# 26. Main verdict

The selected-support hierarchy obeys an exact universal renewal law.

For fixed \(LR_\ell\):

\[
\boxed{
\Pr(G_\ell\le m)
=
\frac{(m)_\ell}{(N)_\ell}.
}
\]

Therefore:

\[
\boxed{
G_\ell/N
\Rightarrow
x^\ell
}
\]

in cumulative form, with density:

\[
\boxed{
\ell x^{\ell-1}.
}
\]

The mean selected ancestry age is asymptotically:

\[
\boxed{
\frac{N}{\ell+1}.
}
\]

Old selected-stock ancestry scales as:

\[
\boxed{
N^{-\ell},
}
\]

and fixed selected-lineage fidelity as:

\[
\boxed{
N^{-(\ell+1)}.
}
\]

Thus GROW-04's LR3 laws are indeed the \(\ell=3\) member of a universal support-channel hierarchy.

The important exception is the bottom of the hierarchy:

\[
\boxed{
LR2
}
\]

is sourced from the identity/diagonal relation rather than an ordinary LR edge class.

Consequently:

\[
\boxed{
LR3
}
\]

is the first selected support sitting inside a genuine two-sided chain of nontrivial reversal-edge channels.

---

# 27. Recommended next step

At this point I would **not** immediately continue with another abstract theorem.

We now have enough exact invariants to build:

## EHF-HC-GROW-06 — Reversal-Support Channel Atlas

For each \(LR_\ell\), tabulate:

- onset;
- parity;
- raw distance;
- class degree/density;
- lower source type;
- inflow coefficient;
- self-inheritance;
- upper outflow;
- renewal CDF;
- mean ancestry age;
- ancestry exponent;
- lineage exponent;
- sector behavior;
- Johnson image where defined.

That atlas would let us inspect the hierarchy as a whole before deciding whether any part resembles a known physical channel structure.

It is the appropriate bridge between theorem accumulation and interpretation.
