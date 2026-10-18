# WHEELER-46 — Observer Architecture / Selective Access Audit

> **Review correction — 18 October 2026:** The Beta-law Chernoff information concerns an **infinite-growth limiting observation**. Cost-normalized optima are conditional proxy calculations. In particular, dividing that information by work for one growth event does not define a finite-budget experiment. A common Core-C/MICRO state space and generator are also required before combining their event counts as one endogenous model. See [ERRATA-01](ERRATA-01.md).

## Question

Does the linear observer-processing burden found in WHEELER-45 survive when the observer has a smarter architecture: filtering, selective attention, or preferential access to event classes?

## Native event pool

At size n the EHF structures already supply

- growth opportunities: G_n = n,
- Core-C comparison opportunities: d_n = n(n-3)/2.

With equal local event rates, blind sampling sees growth with fraction

p_grow(n) = G_n / (G_n + d_n) = 2/(n-1),

so blind expected work per encountered growth event is

W_blind(n) = (n-1)/2 = Theta(n).

## Selective observer model

Let an observer-side filter accept:

- a true growth event with sensitivity s_n,
- a comparison event with false-positive probability f_n.

Assume rejected events do not consume the observer's limited downstream processing budget. The accepted event pool therefore has rates proportional to

s_n G_n

and

f_n d_n.

The fraction of accepted events that are genuine growth events is

p_acc,grow(n)
= s_n G_n / (s_n G_n + f_n d_n)
= s_n / [s_n + f_n (n-3)/2].

Hence the expected number of accepted events processed per accepted true growth event is

W_acc(n)
= 1 / p_acc,grow(n)
= 1 + (f_n/s_n)(n-3)/2.

## Scaling regimes

Assume s_n is bounded away from zero.

1. Constant false-positive rate, f_n -> f > 0:

   W_acc(n) = Theta(n).

   Ordinary imperfect filtering does not remove the linear burden.

2. f_n ~ c/n:

   W_acc(n) -> 1 + c/(2s).

   The observer reaches O(1) downstream work per detected growth event.

3. f_n = o(1/n):

   W_acc(n) -> 1.

   Comparison contamination becomes asymptotically negligible.

4. Perfect class filter, f_n = 0 and s_n > 0:

   W_acc(n) = 1.

   The linear burden disappears completely at the downstream observer level.

Thus the critical selectivity scaling is

f_n = O(1/n).

## False negatives

False negatives by themselves are not responsible for the asymptotic linear contamination burden. If f_n = 0, reducing sensitivity only changes how many true growth events are missed; among accepted events, every event is still genuine growth. If one counts substrate events that must pass through the classifier, however, low sensitivity increases the raw-event cost by 1/s_n.

## Architecture-cost distinction

The conclusion depends on where processing cost is charged.

### A. Rejected events are filtered before the scarce observer budget

Then the relevant cost is W_acc above. Strong enough filtering can reduce Theta(n) to O(1).

### B. The observer itself must inspect every raw event in order to classify it

Then filtering does not remove the front-end burden. With sensitivity s_n, the expected number of raw events required to register one growth event is

W_raw(n)
= (G_n+d_n)/(s_n G_n)
= (n-1)/(2s_n).

For s_n = Theta(1), this remains Theta(n), independent of the false-positive rate.

Therefore selective attention only beats WHEELER-45 if selection occurs upstream of the scarce processing resource, or if the filtering mechanism itself has lower asymptotic cost.

## Consequence for the n=21 optimum

WHEELER-45 recovered an effective linear cost and therefore the same finite optimum n_0 = 21 for the D=2 versus D=4 discrimination task.

WHEELER-46 shows this optimum is architecture-dependent.

- With blind sampling or constant-quality filtering, the effective burden remains asymptotically linear and a finite optimum remains.
- With perfect or asymptotically improving upstream filtering satisfying f_n = O(1/n), the per-detected-growth downstream burden becomes O(1). Then the finite n=21 optimum is no longer forced by observer event competition; raw discrimination can again favour increasingly large preparations toward its Chernoff-information ceiling.

## Main result

The linear observer burden is robust to ordinary fixed-quality filtering, but it is not a substrate invariant.

A sharp threshold appears:

- f_n >> 1/n  => divergent downstream contamination burden,
- f_n ~ c/n  => finite nontrivial burden,
- f_n << 1/n  => asymptotically perfect selective access.

Equivalently, to overcome the O(n^2) comparison-event pool while preserving access to the O(n) growth-event pool, the filter's false-positive probability must improve at least as fast as 1/n.

## Interpretation

This is a useful negative/conditional result.

Observer limitation does not follow from event counts alone. It follows from event counts plus observer architecture and where filtering cost is paid.

The native EHF asymmetry G_n = O(n) versus d_n = O(n^2) does create a real selection-pressure problem for a finite observer, but sufficiently structured access can evade it.

## Verdict

- PASS: blind sampling gives Theta(n) burden.
- PASS: constant-quality imperfect filtering still gives Theta(n) burden.
- PASS: upstream filtering with f_n = O(1/n) reduces downstream burden to O(1).
- PASS: perfect filtering removes the downstream linear burden entirely.
- NEGATIVE: the n=21 preferred scale is not observer-architecture invariant.
- OPEN: derive whether an internal EHF observer can implement f_n = O(1/n) without paying an equal or larger front-end cost.

## Next probe

WHEELER-47 — Filter Realizability / Internal Classification-Cost Audit

Ask whether event class (growth versus comparison) can be recognized locally by an internal observer, and what state/information/work is required to do so. This determines whether the selective architecture that beats the linear burden is physically/structurally available inside the framework rather than externally granted.
