# WHEELER-56 — Maximum-Caliber / Least-Bias Measure Audit

> **Review correction — 18 October 2026:** Maximum entropy is an additional measure principle on a specified reference event set. Event primacy alone does not imply equal rates. Finite-horizon uniformity here is conditional on a fixed initial state (or conditional on each initial state with a fixed preparation law). See [ERRATA-01](ERRATA-01.md).

## Question
Can the uniform admissible-event growth measure used in WHEELER-52 be derived from a least-bias principle rather than inserted by hand?

## Setup
Work in the zero-cost cyclic binary growth model at fixed sector `D=2k`.

For a microstate `w` of length `n`, WHEELER-36 gives the exact number of admissible growth events

\[
A(n,D)=n+D.
\]

Crucially, this depends only on `(n,D)`, not on the detailed run arrangement of `w`.

An event means a specific admissible insertion opportunity (slot + inserted bit), not merely the resulting target word. Distinct insertion events may lead to the same target microstate.

## 1. Local maximum-entropy derivation
Let the admissible outgoing events from state `w` have probabilities `p_1,...,p_A`, with

\[
\sum_{i=1}^A p_i=1,
\qquad p_i\ge0.
\]

Maximize the event entropy

\[
H_w=-\sum_{i=1}^A p_i\log p_i
\]

subject only to normalization and admissibility.

By the standard Lagrange-multiplier calculation,

\[
p_i=\frac1A=\frac1{n+D}
\]

for every admissible event.

Thus, if the primitive sample space is the set of admissible growth events and no additional event property is constrained, the least-biased local measure is exactly the uniform event measure used in WHEELER-52.

## 2. Global event-history maximum caliber
Now consider event-labelled histories of fixed horizon `L`.

Because growth preserves `D`, after `j` growth steps the layer is `(n+j,D)`, and every state in that layer has

\[
A_j=n+D+j
\]

admissible outgoing events.

Therefore the number of event-labelled continuations of length `L` from any initial microstate in the same `(n,D)` layer is

\[
N_L(n,D)=\prod_{j=0}^{L-1}(n+D+j).
\]

More importantly, after choosing any admissible first event, the number of remaining event-labelled continuations is

\[
N_{L-1}(n+1,D)=\prod_{j=1}^{L-1}(n+D+j),
\]

which is the same for every first event.

Hence a maximum-caliber distribution that is uniform over all admissible event-labelled histories of horizon `L` induces

\[
P(e_1\mid w)=\frac1{n+D}
\]

for every admissible first event.

By the same argument recursively, every step is conditionally uniform over currently admissible events.

### Result
Local maximum entropy and global maximum caliber agree exactly in this model:

\[
\boxed{P(e\mid w)=\frac1{n+D}}.
\]

The agreement is not generic for arbitrary branching processes; here it follows from the exact layer-regularity theorem `A(n,D)=n+D`.

## 3. Consequence for the entropy theorem
The least-bias event measure is precisely the measure for which WHEELER-52 proved the full microstate growth kernel is column-substochastic.

Therefore

\[
pK\prec p
\]

(after zero-padding for the enlarged target space), and hence

\[
\boxed{H(pK)\ge H(p)}
\]

for every microscopic input distribution.

So within the event-labelled primitive description, the chain is

\[
\text{admissibility only}
\Rightarrow
\text{maximum event entropy / caliber}
\Rightarrow
\text{uniform event growth}
\Rightarrow
\text{majorization}
\Rightarrow
\text{Shannon entropy nondecrease}.
\]

## 4. Important primitive-sample-space caveat
The derivation depends on what is treated as primitive.

Distinct insertion events can produce the same target state. For example, from `00111` (`n=5,D=2`), the admissible insertion events have multiplicities among distinct target words such as

- `000111`: 3 events,
- `100111`: 1 event,
- `001111`: 3 events.

Uniformity over **events** therefore induces target-state probabilities `3/7, 1/7, 3/7`.

Uniformity over **distinct target states** would instead assign `1/3,1/3,1/3`.

These are different least-bias measures because they use different primitive sample spaces.

This matters for EHF foundations. If the primitive data are admissible transformations/comparisons/events, then event-labelled maximum caliber is the natural construction. If only resultant states are regarded as primitive, the measure-selection problem changes.

## 5. Additional constraints produce nonuniform measures
Maximum entropy does not imply uniformity once extra expectation constraints are imposed.

If event features `F_a(e)` are constrained, maximizing entropy yields the usual exponential-family form

\[
P(e\mid w)\propto
\exp\!\left[-\sum_a \lambda_a F_a(e)\right].
\]

Run-length weighting from WHEELER-53 is of this general type if run geometry is admitted as a constrained/relevant feature. Such measures can violate the WHEELER-52 entropy monotonicity theorem.

Thus least bias selects uniform event growth only when admissibility and normalization are the only constraints.

## Verdict
**PASS, conditional on primitive event space and admissibility-only constraints.**

1. Local maximum entropy exactly selects equal probability for all admissible growth events.
2. Because every state in a fixed `(n,D)` layer has the same number `n+D` of admissible events, fixed-horizon global maximum caliber over event-labelled histories selects the same local rule.
3. This recovers the uniform measure required by WHEELER-52 without separately postulating equal probabilities.
4. The result is not measure-free: it depends on taking admissible insertion events, rather than distinct target states, as the primitive alternatives.
5. Additional constrained event features naturally generate nonuniform Gibbs/exponential-family measures and can destroy entropy monotonicity.

## Status
- **PROVED:** local admissibility-only maximum entropy gives uniform admissible-event probabilities.
- **PROVED:** fixed-horizon global maximum caliber on event-labelled histories gives the same rule because `A(n,D)=n+D` is layer-regular.
- **PROVED:** this measure inherits the WHEELER-52 microstate majorization/Shannon-entropy theorem.
- **FOUNDATIONAL CHOICE:** event-labelled histories versus state-only histories are different primitive sample spaces.
- **OPEN:** derive, rather than assume, why admissible transformations/events should be the primitive sample space of EHF.
- **OPEN:** test whether analogous layer-regular maximum-caliber selection survives in Core C and other EHF substrates.

## Next probe
**WHEELER-57 — Primitive Event vs State Measure / Quotient-Consistency Audit**

Test whether event-uniform and state-uniform measures can be distinguished by a consistency principle under quotienting/coarse-graining, and whether one behaves naturally under composition and growth. This directly targets the remaining foundational ambiguity exposed here.
