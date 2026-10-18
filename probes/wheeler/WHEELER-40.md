# WHEELER-40 — Finite-Sample Discrimination / Sample-Complexity Audit

> **Review correction — 18 October 2026:** The Beta-law Chernoff information concerns an **infinite-growth limiting observation**. Cost-normalized optima are conditional proxy calculations. In particular, dividing that information by work for one growth event does not define a finite-budget experiment. A common Core-C/MICRO state space and generator are also required before combining their event counts as one endogenous model. See [ERRATA-01](ERRATA-01.md).

## Goal
Turn the WHEELER-39 asymptotic identifiability result into a finite-sample discrimination estimate for nearby hidden sectors.

## Concrete preparation
Use the balanced preparation

- `n0 = 8`
- `N1,0 = 4`

and compare

- `H2: D = 2`
- `H4: D = 4`.

From the WHEELER-37 Pólya-urn reduction, the limiting one-frequency for one independent preparation satisfies

`p_inf | D ~ Beta(N1,0 + D/2, n0 - N1,0 + D/2)`.

Therefore

- `D=2`: `p_inf ~ Beta(5,5)`
- `D=4`: `p_inf ~ Beta(6,6)`.

## Distinguishability
For equal priors, the optimal classifier is the likelihood-ratio test based on independent samples `p_1,...,p_m`.

The sector laws are close but distinct. The KL divergences are

- `KL(Beta(5,5) || Beta(6,6)) ≈ 0.0096653`
- `KL(Beta(6,6) || Beta(5,5)) ≈ 0.0085165`.

Hence discrimination error decreases exponentially with the number of independent preparations, but slowly.

## Approximate sample complexity
Using the Gaussian approximation to the accumulated log-likelihood ratio under the optimal equal-prior test gives approximately:

| Target correct classification | Independent preparations |
|---|---:|
| 90% | 363 |
| 95% | 599 |
| 99% | 1201 |

These are operational estimates, not rigorous guarantees.

## Conservative Chernoff bound
The Chernoff information for `Beta(5,5)` versus `Beta(6,6)` is approximately

`C ≈ 0.00226481`.

Using the standard upper bound

`P_error <= (1/2) exp(-m C)`

gives sufficient sample counts of approximately:

| Target correct classification | Conservative sufficient m |
|---|---:|
| 90% | 711 |
| 95% | 1017 |
| 99% | 1728 |

The Chernoff numbers are deliberately conservative; the Gaussian likelihood-ratio estimates are closer to expected practical performance.

## Interpretation
WHEELER-39 showed that repeated independent preparations can asymptotically identify a shared hidden `D` sector. WHEELER-40 shows that nearby sectors may nevertheless require hundreds to more than a thousand independent preparations for high-confidence discrimination.

Thus

`asymptotic identifiability != easy observability`.

The hidden sector can be mathematically identifiable while remaining operationally difficult to infer.

## Status

- Distinct sector laws: **PROVED** from the Beta-family reduction.
- KL divergences: **COMPUTATIONAL / analytic evaluation**.
- Gaussian sample counts: **APPROXIMATE**.
- Chernoff sufficient counts: **RIGOROUS BOUND conditional on the Beta-limit experiment and equal priors**.

## Next probe
A useful next audit is to optimize the initial preparation `(n0,N1,0)` or the observation channel to maximize Chernoff/KL separation between candidate `D` sectors. This would ask whether observer design can make a hidden sector operationally easy to detect rather than merely identifiable in principle.
