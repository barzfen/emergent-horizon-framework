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
