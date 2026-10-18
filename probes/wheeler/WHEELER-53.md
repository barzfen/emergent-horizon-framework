# WHEELER-53 — Weighted Growth / Entropy-Robustness Audit

## Question

Does the microscopic entropy-nondecrease result of WHEELER-52 survive when admissible growth events are not equally weighted?

## Baseline from WHEELER-52

For fixed cyclic boundary count `D`, every zero-cost source word of length `n` has exactly `n + D` admissible insertions. Under uniform weighting, every microscopic event therefore has probability `1/(n+D)`.

For any target word `v` of length `n+1`, at most `n+1` incoming microscopic events can produce it. Hence

\[
\sum_w K_{n,D}(w,v) \le \frac{n+1}{n+D}.
\]

For nontrivial cyclic binary sectors, `D >= 2`, so every column sum is strictly below 1. The uniform growth kernel is row-stochastic and column-substochastic; after zero-padding across the changing state-space dimension, this implies majorization and Shannon entropy nondecrease for every input distribution.

The question here is whether this is robust to nonuniform event weights.

## General weighted kernel

Let each admissible microscopic insertion event `e` from source state `w` carry positive weight `r(e)`. Normalize separately at each source:

\[
K(w,v)=\frac{\sum_{e:w\to v} r(e)}{Z(w)},
\qquad
Z(w)=\sum_{e\text{ admissible from }w}r(e).
\]

The uniform proof no longer goes through automatically because the denominator now depends on the source state and the incoming mass to one target can be amplified relative to others.

A simple sufficient bound follows if all event weights satisfy

\[
r_{\min}\le r(e)\le r_{\max}.
\]

Relative to the uniform event probability,

\[
K(w,v)\le \frac{r_{\max}}{r_{\min}}\frac{N_{w\to v}}{n+D},
\]

where `N_{w->v}` counts admissible insertion events from `w` that produce `v`. Summing over predecessors gives

\[
\sum_w K(w,v)
\le
R\frac{n+1}{n+D},
\qquad
R=\frac{r_{\max}}{r_{\min}}.
\]

Therefore a sufficient condition for the WHEELER-52 column-substochastic proof to survive is

\[
R\le \frac{n+D}{n+1}.
\]

This is only sufficient, not necessary. In particular, some structured biases remain column-substochastic well outside this bound.

## Natural local stress test: resulting-run-length bias

Use the local weighting rule

\[
r(e)=q^{L(e)},
\]

where `L(e)` is the length of the run containing the newly inserted bit in the resulting target word.

Interpretation:

- `q = 1`: uniform admissible-event growth;
- `q < 1`: shorter resulting runs are favored;
- `q > 1`: longer resulting runs are favored.

This rule is local in the resulting run structure and does not explicitly target any chosen global state.

## Computational audit

The exact zero-cost cyclic state spaces and weighted microscopic transition matrices were enumerated directly for small `n` and fixed `D`.

The run-length weighting can violate column-substochasticity. Examples include:

- `n=5, D=2, q=0.2`: maximum column sum approximately `1.31578947`;
- `n=6, D=2, q=0.5`: maximum column sum approximately `1.08088235`;
- `n=11, D=4, q=0.5`: maximum column sum approximately `1.22222222`.

Thus nonuniform local weighting can invalidate the majorization proof.

## Actual Shannon-entropy decrease

Failure of the column-sum condition alone would not prove entropy decrease, so the audit also searched input distributions directly.

At

\[
n=5,\qquad D=2,\qquad q=0.05,
\]

there is already a two-state input distribution supported on

- `11100`, and
- `11000`

(up to the chosen cyclic labeling convention)

for which one weighted microscopic growth step decreases Shannon entropy.

A numerically optimized two-state mixture places approximately probability `0.345` on `11000` and `0.655` on `11100` (equivalent cyclic representatives may be used). The entropy change is approximately

\[
\Delta H = H(pK)-H(p) \approx -0.0127\ \text{nats}.
\]

For stronger short-run bias the violation becomes larger; for example at `q=0.01` the best two-state search found an entropy decrease of roughly `0.209` nats.

Therefore the microscopic Shannon monotonicity of WHEELER-52 is not universal under arbitrary positive local growth weights.

## Structured biases that did not immediately break the theorem

Some restricted weighting families were also checked computationally and did not produce column-sum violations in the tested range, including:

- constant bias by inserted symbol only (`0` versus `1`), and
- constant bias between insertion at a run boundary versus insertion inside a same-symbol edge.

This does not constitute a theorem for those families; it only shows that nonuniformity by itself is not sufficient to destroy entropy monotonicity.

## Verdict

**NEGATIVE for full robustness.**

WHEELER-52 is a genuine theorem for uniformly weighted admissible growth events, but microscopic entropy nondecrease is not forced by admissibility and growth alone.

A local run-length-dependent weighting can produce

\[
H(pK)<H(p).
\]

Hence the entropy law depends on additional structure in the growth measure.

The correct refined statement is

\[
\boxed{\text{admissibility + growth + suitable measure} \Rightarrow \text{entropy monotonicity}}
\]

rather than

\[
\text{admissibility + growth alone} \Rightarrow \text{entropy monotonicity}.
\]

## What remains open

1. Characterize the largest class of weighted local growth rules whose kernels remain column-substochastic.
2. Determine whether symbol-only bias preserves column-substochasticity analytically for all `n,D`.
3. Determine whether boundary/interior local weighting preserves it analytically.
4. Identify an intrinsic EHF principle, if any, that selects the uniform or another entropy-monotone growth measure rather than imposing it by hand.
5. Test whether detailed-balance-like or reversibility constraints single out a protected weighting class.

## Status

- **PROVED:** uniform event weighting implies the WHEELER-52 column-substochastic bound.
- **PROVED:** bounded weight ratio gives the stated sufficient robustness condition.
- **COMPUTATIONAL:** local run-length bias violates column-substochasticity in explicit small sectors.
- **COMPUTATIONAL COUNTEREXAMPLE:** Shannon entropy can decrease under the weighted microscopic growth channel.
- **OPEN:** full classification of entropy-monotone weighted growth rules.
