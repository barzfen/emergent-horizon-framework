# WHEELER-57 — Primitive Event vs State Measure / Quotient-Consistency Audit

> **Review correction — 18 October 2026:** The conditional symmetry theorem is retained. The claim that event primacy alone selects the more coherent measure is withdrawn. WHEELER-58 tests horizon consistency for both measures and keeps the initial preparation fixed. See [ERRATA-01](ERRATA-01.md).

## Question

WHEELER-56 showed that maximum entropy / maximum caliber gives a uniform measure over admissible growth **events**. But several distinct insertion events can lead to the same resultant microstate. Should EHF regard admissible transformations/events as primitive, or should it instead assign equal probability directly to distinct resultant states?

This audit compares the two measures and tests refinement/coarse-graining consistency.

## Setup

For a zero-cost source word `w`, let

- `E(w)` be the set of admissible insertion events;
- `T(w)` be the set of distinct resultant target words;
- `tau : E(w) -> T(w)` map each insertion event to its target state;
- `m_v = |tau^{-1}(v)|` be the event multiplicity of target `v`.

Within a fixed `(n,D)` sector,

`|E(w)| = n + D`.

Two candidate least-bias measures are:

### Event-uniform

`P_E(e|w) = 1 / |E(w)|`.

The induced target-state law is the push-forward

`P_E(v|w) = m_v / |E(w)|`.

### State-uniform

`P_S(v|w) = 1 / |T(w)|`.

If this is lifted back to events by treating events leading to the same target symmetrically,

`P_S(e|w) = 1 / (|T(w)| m_tau(e))`.

Therefore event probabilities are unequal whenever target multiplicities are unequal.

## Exact concrete example

Take

`w = 00111`.

It is zero-cost with

- `n = 5`;
- `D = 2`;
- hence `|E(w)| = n + D = 7`.

Enumerating admissible insertion events gives three distinct targets with multiplicities

`(3,3,1)`.

Therefore event-uniform growth gives target probabilities

`(3/7, 3/7, 1/7)`.

State-uniform growth instead gives

`(1/3, 1/3, 1/3)`.

Thus the two principles are genuinely inequivalent.

## Refinement / quotient consistency

Suppose the fine-grained primitive sample space is the event set `E(w)` and target states are a quotient under the equivalence relation

`e ~ e' iff tau(e) = tau(e')`.

Probability consistency under quotienting requires

`P(v|w) = sum_{e:tau(e)=v} P(e|w)`.

If primitive admissible events are equivalent absent further structure, maximum entropy gives equal event probabilities. The quotient law is then uniquely

`P(v|w) = m_v / |E(w)|`.

This law is invariant under merely forgetting event labels: coarse probabilities are obtained by addition, as ordinary probability theory requires.

By contrast, imposing equal probability directly on quotient states and then refining back to events does not recover event symmetry when multiplicities differ. For the `(3,3,1)` example, the lifted per-event probabilities are

`1/9, 1/9, ...` for events in the multiplicity-3 fibers and `1/3` for the single event in the multiplicity-1 fiber.

So state-uniformity treats otherwise equivalent primitive events differently solely because of how many other events share their target.

This is not a mathematical contradiction. It is a different choice of primitive reference measure.

## General theorem

Let `E` be a finite primitive event set and `tau:E->T` any quotient map. Assume:

1. primitive events carry no distinguishing information beyond admissibility;
2. the probability measure is invariant under permutations of primitive events;
3. coarse target probabilities are obtained by push-forward under `tau`.

Then necessarily

`P(e)=1/|E|`

and

`P(v)=|tau^{-1}(v)|/|E|`.

Therefore a uniform distribution over target states is compatible with primitive-event symmetry **iff** all target multiplicities are equal.

## History consistency

The distinction also persists over histories.

WHEELER-56 proved that every state in a fixed `(n,D)` layer has exactly `n+D` admissible insertion events, so all event-labelled histories of a fixed length have equal weight under maximum caliber.

Quotienting those histories by forgetting event labels produces path probabilities proportional to the number of primitive event histories realizing each coarse state-history.

Assigning equal weight directly to distinct coarse state histories generally disagrees with that push-forward whenever multiplicities differ.

Thus event-uniform maximum caliber is projectively consistent from fine histories to coarse histories; state-uniform maximum entropy defines a different theory unless coarse states are declared primitive from the outset.

## EHF interpretation

EHF's stated foundational choice is that **admissible comparison/transformation is primitive data**. This choice alone does not imply event symmetry or equal rates. If one additionally adopts admissibility-only maximum entropy, equivalently full permutation symmetry of the admissible event alternatives, the event-labelled measure is:

`admissible primitive events + full event symmetry / admissibility-only maximum entropy -> equal event weight -> push-forward to state probabilities`.

The multiplicity factor is not an arbitrary bias. It counts how many distinct admissible primitive transformations realize the same resulting state.

If instead resultant states were chosen as primitive, state-uniformity would be valid, but an additional rule would then be required to recover probabilities for distinct transformations leading to the same state.

## Verdict

**PASS — conditional foundational selection.**

- PROVED: event-uniform and state-uniform measures differ whenever target multiplicities are unequal.
- PROVED: primitive-event symmetry plus quotient push-forward uniquely gives multiplicity-weighted target probabilities.
- PROVED: state-uniformity is compatible with primitive-event symmetry only when all target multiplicities are equal.
- PROVED: event-history maximum caliber is projectively consistent under forgetting event labels.
- FOUNDATIONAL/CONDITIONAL: the event-uniform measure follows after adding full event symmetry or admissibility-only maximum entropy. State-uniform dynamics is also coherent, but does not respect that stronger event symmetry when multiplicities differ.
- NOT CLAIMED: probability theory itself does not force events rather than states to be primitive; that is a framework-level choice.

## Consequence for WHEELER-52–56

The entropy theorem can now be stated more cleanly:

`primitive admissible transformations + admissibility-only reference-measure assumption`

`-> least-bias / maximum caliber on events`

`-> uniform event measure`

`-> multiplicity-weighted target-state measure`

`-> column-substochastic microstate growth kernel`

`-> majorization`

`-> Shannon entropy nondecrease`.

This resolves the probability assignment only after the reference event space and its full symmetry/maximum-entropy assumption are fixed. Primitive event ontology alone does not remove the measure choice. WHEELER-58 additionally shows that both event-uniform and state-uniform dynamics are horizon-consistent in the specified rooted-word model.

## Next probe

**WHEELER-58 — Projective Measure / Multi-Step Consistency Audit**

Test whether the family of finite-horizon event-history measures forms a fully projectively consistent stochastic process across all horizons, and whether the same construction survives quotienting to observer macrostates. This would turn the least-bias rule from a sequence of finite-horizon choices into a single coherent path-space measure.
