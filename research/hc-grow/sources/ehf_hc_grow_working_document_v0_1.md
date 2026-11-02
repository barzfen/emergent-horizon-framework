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
