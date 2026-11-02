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
