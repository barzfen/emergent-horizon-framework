# WHEELER-55 — Natural-Measure Selection / Symmetry-and-Growth-Consistency Audit

## Question
Can EHF-style structural principles select the growth measure, rather than leaving it as an arbitrary modelling choice?

We test the following candidate principles:

1. cyclic relabelling covariance;
2. complement symmetry under 0↔1;
3. all-slot structural equivalence;
4. size/growth consistency;
5. local event-rate assignment;
6. factorization/additivity for independent disjoint subsystems.

The target is to determine whether these principles uniquely force uniform weights over admissible growth events, or at least restrict the measure to the entropy-safe class identified in WHEELER-52 through WHEELER-54.

---

## Setup

Let `w` be a zero-cost cyclic binary word and let `e` denote an admissible one-bit insertion event.

Assign each admissible event a positive raw rate

\[
r_w(e)>0.
\]

The normalized one-step growth kernel is

\[
K(w\to e(w))
=
\frac{r_w(e)}{Z(w)},
\qquad
Z(w)=\sum_{e'\in A(w)}r_w(e').
\]

Uniform growth corresponds to

\[
r_w(e)=r
\]

for every admissible event.

WHEELER-52 proved entropy monotonicity for this uniform case. WHEELER-54 proved a larger protected family in which insertion-0 events have arbitrary constant rate `a>0` and insertion-1 events arbitrary constant rate `b>0`.

The present question is whether natural EHF structural principles force one of these forms.

---

## 1. Cyclic relabelling covariance

Let `rho` be a cyclic relabelling/rotation of the word. Covariance requires

\[
r_{\rho w}(\rho e)=r_w(e).
\]

This removes dependence on absolute slot labels.

However it does **not** remove dependence on local configuration type. A rate may still depend on whether the insertion occurs:

- in the interior of a run;
- adjacent to a run boundary;
- in a specific bounded local pattern;
- as a function of some local invariant.

Therefore cyclic covariance alone does not imply uniformity.

**Verdict:** insufficient.

---

## 2. Complement symmetry

Let `C` exchange 0 and 1. Complement symmetry requires

\[
r_{Cw}(Ce)=r_w(e).
\]

This rules out a pure symbol asymmetry `a != b` if 0 and 1 are physically indistinguishable labels.

Thus the WHEELER-54 two-rate family collapses from `(a,b)` to

\[
a=b
\]

under exact complement symmetry.

But complement symmetry still allows geometry-dependent rates, e.g. different rates for run-interior and run-edge insertions.

**Verdict:** removes symbol bias, but does not force uniformity.

---

## 3. Explicit nonuniform counterfamily satisfying the weak principles

Define two positive constants

\[
r_{\rm int}>0,
\qquad
r_{\rm edge}>0.
\]

For every admissible insertion event, assign:

- `r_int` if the insertion lies in the interior of a same-symbol run;
- `r_edge` if the insertion is adjacent to a run boundary.

This rule is:

1. invariant under cyclic relabelling;
2. invariant under 0↔1 complement;
3. local;
4. independent of total system size `n`;
5. compatible with assigning event rates independently on disjoint subsystems;
6. compatible with a continuous-time local-hazard interpretation.

Yet it is nonuniform whenever

\[
r_{\rm int}\ne r_{\rm edge}.
\]

Therefore the combination

\[
\text{relabel covariance}
+
\text{complement symmetry}
+
\text{locality}
+
\text{factorization}
\]

does **not** uniquely determine the uniform measure.

This is an explicit structural counterexample, not merely a degree-of-freedom argument.

---

## 4. Growth consistency

A useful consistency requirement is that the intrinsic rate assigned to an event type does not depend explicitly on global size `n`:

\[
r_{n+1}(\text{same local event type})
=
r_n(\text{same local event type}).
\]

This eliminates arbitrary global factors such as `n^alpha` attached to individual local events.

However it still permits any fixed local rule

\[
r_w(e)=F(\text{bounded neighbourhood of }e),
\]

with the same function `F` at all sizes.

Thus growth consistency removes some artificial measure choices, but still does not force uniformity.

**Verdict:** insufficient.

---

## 5. Subsystem factorization/additivity

For two independent disjoint subsystems `A` and `B`, locality and independent hazards naturally imply

\[
R_{A\sqcup B}=R_A+R_B,
\]

with individual local event rates inherited unchanged from each subsystem.

This is the same event-rate additivity logic used in WHEELER-30 and WHEELER-31.

But factorization constrains how rates combine across subsystems; it does not require all local event types within one subsystem to have the same rate.

A local type-dependent rule such as `(r_int,r_edge)` factorizes perfectly well.

**Verdict:** insufficient.

---

## 6. Strong all-slot equivalence

There are two distinct meanings of "all-slot equivalence".

### Weak form

All slot labels are arbitrary, but local structure may distinguish event types.

This is just relabelling covariance and does not imply uniformity.

### Strong form

The primitive substrate supplies no event attribute beyond:

1. the fact that the insertion is admissible;
2. the identity of the local slot as a temporary label with no physical content.

Equivalently, the raw rate is required to be a function only of admissibility:

\[
r_w(e)=F(\mathbf 1_{\rm admissible}(e)).
\]

On the admissible set this reduces to a constant:

\[
r_w(e)=r.
\]

Therefore the strong no-extra-structure version of all-slot equivalence **does** force uniform admissible-event rates.

This is a theorem, but it is conditional on adopting a stronger primitive-data axiom than ordinary symmetry.

---

## 7. Natural-measure selection theorem (conditional)

### Theorem
Suppose admissible growth-event rates satisfy:

1. positivity;
2. size-independent local rate assignment;
3. cyclic relabelling covariance;
4. complement symmetry;
5. disjoint-subsystem rate additivity;
6. **admissibility-only dependence**: no local geometric feature other than admissibility is available to the rate law.

Then there exists a constant `r>0` such that

\[
r_w(e)=r
\]

for every admissible event in every state.

Hence the normalized growth kernel is exactly the uniform admissible-event measure used in WHEELER-52.

### Proof sketch
By admissibility-only dependence, every admissible event belongs to the same primitive rate class. Positivity assigns that class some rate `r>0`. Size consistency makes `r` independent of `n`; relabelling/complement symmetry prevent hidden label dependence; subsystem additivity preserves the same local rate under composition. Therefore all admissible events have equal raw rate.

---

## 8. Important logical status

The crucial point is that **uniformity is not derived from symmetry alone**.

It follows only if EHF adopts the stronger statement:

> admissibility is the only primitive event property relevant to the growth rate.

This is close in spirit to the framework preference that admissible comparison is primitive data, but it is still an additional measure principle unless it can itself be derived.

So the honest hierarchy is:

- relabelling covariance alone: insufficient;
- complement symmetry added: insufficient;
- local size-consistent rates: insufficient;
- subsystem additivity: insufficient;
- all of the above plus admissibility-only dependence: uniform measure forced.

---

## 9. Relation to entropy monotonicity

If the strong admissibility-only principle is accepted, then WHEELER-52 immediately applies:

\[
\text{uniform admissible-event growth}
\Rightarrow
\text{column-substochastic microstate channel}
\Rightarrow
pK\prec p
\Rightarrow
H(pK)\ge H(p).
\]

Thus an EHF-native entropy law can be obtained from a compact structural package.

But without the admissibility-only principle, local geometry-dependent measures remain allowed, and WHEELER-53 showed that some such measures can make entropy decrease.

---

## Verdict

**PASS / NEGATIVE-THEN-CONDITIONAL-POSITIVE**

1. The obvious natural symmetries and factorization principles do **not** uniquely select the uniform growth measure.
2. An explicit nonuniform local counterfamily survives those weak principles.
3. Uniformity is forced if one adds the stronger `admissibility-only rate` axiom.
4. Therefore the entropy theorem is not yet completely measure-free: one remaining foundational choice is whether local geometry is allowed to influence growth rates.

---

## Status

- **PROVED:** cyclic/complement symmetry + locality + subsystem additivity do not force uniformity; explicit `(r_int,r_edge)` counterfamily.
- **PROVED:** admissibility-only rate dependence forces uniform admissible-event growth.
- **PROVED conditional consequence:** under that principle, WHEELER-52 microscopic entropy monotonicity follows.
- **OPEN:** derive admissibility-only dependence from a deeper EHF principle rather than assume it.
- **OPEN:** determine whether the wider local rate class allowed by weak symmetry is entirely entropy-safe under additional constraints such as bounded-radius covariance.

---

## Proposed next probe

**WHEELER-56 — Maximum-Caliber / Least-Bias Measure Audit**

Rather than postulating admissibility-only dependence directly, ask whether the uniform admissible-event measure is selected by an internal least-bias principle: among all growth measures compatible with the known EHF constraints, maximize path entropy (or local event entropy). Then test whether that reproduces uniform growth without introducing thermodynamic assumptions.
