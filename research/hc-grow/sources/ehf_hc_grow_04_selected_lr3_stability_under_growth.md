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
