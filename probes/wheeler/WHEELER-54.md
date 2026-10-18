# WHEELER-54 — Entropy-Monotone Measure Classification

## Question
Which local weighting rules preserve the column-substochastic / majorization structure found in WHEELER-52, and which do not?

## Setup
Work in a fixed zero-cost cyclic-binary sector with

- length `n`,
- boundary count `D=2k`,
- admissible growth by one-bit insertion preserving zero cost and `D`.

A weighted microscopic growth kernel is

\[
K(w,v)=\frac{r(w\to v)}{Z(w)},
\qquad
Z(w)=\sum_{e\in A(w)} r(e),
\]

where `A(w)` is the set of admissible insertion events from source microstate `w`.

Universal Shannon-entropy nondecrease follows if the kernel is row-stochastic and column-substochastic:

\[
\sum_w K(w,v)\le 1
\]

for every target microstate `v`.

This column condition is therefore the exact operational criterion used here.

---

## 1. Uniform event weights

For `r(e)=const`, WHEELER-52 proved

\[
\sum_w K(w,v)\le \frac{n+1}{n+D}\le 1,
\]

with strict inequality for every nontrivial sector `D>0`.

Status: **PROVED**.

---

## 2. Arbitrary inserted-symbol bias is protected

Let every admissible insertion of `0` have positive weight `a`, and every admissible insertion of `1` have positive weight `b`:

\[
r(e)=
\begin{cases}
a,&\text{insert }0,\\
b,&\text{insert }1.
\end{cases}
\]

No restriction is imposed on the ratio `a/b`.

For a source state with `N_0=x`, `N_1=y` and `D=2k`, WHEELER-36 gives the exact numbers of admissible insertion events:

\[
A_0=x+k,
\qquad
A_1=y+k.
\]

Hence its outgoing normalization is

\[
Z=a(x+k)+b(y+k).
\]

Consider a target state `v` of length `n+1` with `x` zeros and `y` ones. An incoming predecessor produced by deleting a zero has normalization `Z-a`; one produced by deleting a one has normalization `Z-b`.

The number of valid zero deletions is at most `x`, and the number of valid one deletions is at most `y`, so

\[
C(v)=\sum_w K(w,v)
\le
\frac{ax}{Z-a}+\frac{by}{Z-b}.
\]

It remains to prove the right-hand side is at most 1.

Multiplying by the positive denominator `(Z-a)(Z-b)`, the numerator of

\[
1-\frac{ax}{Z-a}-\frac{by}{Z-b}
\]

is

\[
a^2(k-1)(x+k)
+b^2(k-1)(y+k)
+ab\bigl[k(x+y)+2k(k-1)+1\bigr].
\]

Every term is nonnegative for `k>=1`, `a,b>0`.

Therefore

\[
\boxed{C(v)\le1}
\]

for every target, every system size, and every positive symbol-bias ratio `a/b`.

Thus the microscopic channel remains column-substochastic and

\[
\boxed{H(pK)\ge H(p)}
\]

for every input distribution.

Status: **PROVED**.

### Interpretation
The entropy theorem is not tied to exact equality of all insertion probabilities. A potentially extreme global `0`-versus-`1` preference is harmless.

What matters is whether weighting depends on finer geometry in a way that concentrates normalized incoming probability onto particular targets.

---

## 3. Local geometric weighting can break the theorem

WHEELER-53 supplied the counterexample family

\[
r(e)=q^{L(e)},
\]

where `L(e)` is the length of the target run containing the newly inserted bit.

For sufficiently small `q`, shorter resulting runs are strongly preferred.

Already at `n=5, D=2`, column sums can exceed 1, and an explicit two-state input distribution gives Shannon-entropy decrease. At `q=0.05`, the observed decrease was approximately

\[
\Delta H\approx -0.0127\text{ nats}.
\]

Status: **COMPUTATIONAL COUNTEREXAMPLE**.

Therefore

\[
\boxed{\text{locality alone does not guarantee entropy monotonicity}.}
\]

---

## 4. Other tested local families

Several additional two-weight local rules were scanned computationally through small zero-cost sectors and across large weight ratios, including:

- boundary versus interior insertion,
- local left-match versus non-match weighting,
- inserted-symbol weighting.

No column-substochasticity violations were found for the first two families in the tested range. Inserted-symbol weighting is now proved analytically above.

The boundary/interior and match-based families remain **COMPUTATIONAL PATTERNS**, not theorems.

---

## 5. General exact criterion

For an arbitrary positive local weighting rule, define

\[
Z(w)=\sum_{e\in A(w)}r(e).
\]

Then the weighted growth rule is universally entropy-monotone by the same majorization argument whenever

\[
\boxed{
\forall v:\quad
\sum_{(w,e):\ e(w)=v}
\frac{r(e)}{Z(w)}\le1.
}
\]

This is necessary and sufficient for **column-substochasticity** of the weighted kernel.

Column-substochasticity is a sufficient structural route to universal Shannon-entropy nondecrease for every input distribution.

This criterion is exact but not yet a satisfying local classification, because it is expressed in terms of normalized incoming mass at each target.

---

## 6. Bounded-distortion sufficient condition

WHEELER-53 also established a simple robustness bound. If every admissible event weight obeys

\[
r_{\min}\le r(e)\le r_{\max},
\]

with distortion ratio

\[
R=\frac{r_{\max}}{r_{\min}},
\]

then column-substochasticity is guaranteed whenever

\[
\boxed{
R\le\frac{n+D}{n+1}.
}
\]

This is sufficient, not necessary. The symbol-bias theorem above demonstrates how conservative the bound can be: arbitrary `a/b` is allowed in that protected family.

---

## Classification obtained so far

### Proven entropy-monotone classes
1. Uniform admissible-event weights.
2. Arbitrary positive inserted-symbol weights `a,b`.
3. Any weighting satisfying the exact normalized incoming-mass criterion.
4. Any weighting satisfying the bounded-distortion sufficient inequality.

### Proven / computed failure class
- Target-run-length weighting `q^{L(e)}` for sufficiently strong bias.

### Computationally stable but unproved classes
- boundary/interior two-weight rules,
- simple local match/non-match rules.

---

## Main conclusion

The correct refinement of WHEELER-52 is

\[
\boxed{
\text{entropy monotonicity is measure-dependent, but it possesses nontrivial protected measure classes.}
}
\]

The distinction is not simply `uniform` versus `biased`.

A better dividing line is whether the local weighting preserves sufficiently diffuse **normalized incoming mass**. Global symbol bias does; sufficiently strong target-geometry bias need not.

This is a substantially stronger and more precise statement than saying that equal weighting was required.

---

## EHF significance

EHF still does not yet derive a unique growth measure. However, the entropy law is now known to survive a meaningful family of non-uniform measures.

A possible naturality principle would need to select weights from an entropy-monotone class rather than merely assert uniformity. Candidate principles include:

- complement/relabeling covariance,
- dependence only on source-local data rather than target-global geometry,
- growth consistency across `n`,
- observer-independence,
- factorization/additivity under independent subsystems.

These principles have not yet been shown to uniquely select the uniform measure.

---

## Verdict

**PASS / PARTIAL CLASSIFICATION**

- Exact criterion: obtained.
- Nontrivial analytic protected class: obtained.
- Natural local counterexample class: retained from WHEELER-53.
- Unique EHF-selected measure: **NOT obtained**.
- Full local-rule classification: **OPEN**.

## Recommended next probe

**WHEELER-55 — Natural-Measure Selection / Symmetry-and-Growth-Consistency Audit**

Test whether relabeling covariance, binary-complement symmetry, all-slot growth consistency, and subsystem factorization force or strongly constrain the admissible weight family. The target is not to assume uniformity, but to determine whether the framework itself selects it or a small entropy-monotone class.
