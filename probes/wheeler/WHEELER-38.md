# WHEELER-38 — Hidden-Sector Identifiability Audit

## Question
Given the zero-cost MICRO growth process observed only through `(n,N1)` (and optionally event times), can one infinite trajectory identify the conserved hidden sector `D` exactly?

## Embedded event chain
From WHEELER-36/37,

`P(Delta N1=1 | n,N1,D) = (N1 + D/2)/(n + D)`

`P(Delta N1=0 | n,N1,D) = (n - N1 + D/2)/(n + D)`.

For fixed initial `(n0,N10)`, this is a Polya urn with parameters

`alpha_D = N10 + D/2`,

`beta_D = n0 - N10 + D/2`.

By the standard Polya-urn/de Finetti representation, the asymptotic one-frequency `p` satisfies

`p | D ~ Beta(alpha_D,beta_D)`.

For ordinary nondegenerate sectors (`alpha_D,beta_D > 0`), different `D` values induce Beta densities that are all strictly positive on `(0,1)`. Therefore their induced measures overlap: observing one infinite symbol trajectory determines `p` almost surely but does not determine `D` almost surely. The posterior over `D` generally remains non-degenerate.

**Verdict without timing:** exact identification of `D` from one infinite trajectory fails generically.

## Event-time information
Under the local-rate model from WHEELER-29..31, total growth rate at size `n` is

`R(n,D)=r(n+D)`.

Thus the waiting time between the `k`th and `(k+1)`th growth events is exponential with rate

`lambda_k(D)=r(n0+k+D)`.

For two candidate sectors `D` and `D'`, the per-step relative rate difference is `O(1/n)`. The Fisher information in one exponential waiting time for `D` is

`I_k(D)=1/(n0+k+D)^2`,

so total timing information is bounded:

`sum_k I_k(D) < infinity`.

Equivalently, the Hellinger deficit between `Exp(lambda_k(D))` and `Exp(lambda_k(D'))` is `O(1/k^2)`, and the sum of those deficits converges. Hence the infinite product timing laws for distinct finite `D,D'` are mutually absolutely continuous rather than mutually singular.

So even an arbitrarily long single timed trajectory does not generically force the posterior onto the true `D` with probability one.

**Verdict with timing:** exact identification from one infinite trajectory still fails generically, despite timing carrying additional finite information.

## Interpretation
`D` is a persistent hidden sector, but it is not necessarily an asymptotically observable label from one coarse trajectory. The observer can improve a posterior over `D`, but different sectors remain statistically compatible with the same infinite coarse record.

This is stronger than ordinary short-memory ambiguity: it is a form of structural non-identifiability under the chosen observation map.

## What would identify D?
- Direct access to a sufficient observable containing `D` (for example `(N1,D)`).
- Multiple independent trajectories prepared with the same unknown `D`: each provides fresh finite information, so repeated preparations can identify the sector statistically under standard identifiability conditions.
- An additional observable whose distributions for different `D` become mutually singular asymptotically.

## Status
- Polya-urn reduction: PROVED from WHEELER-36 transition counts.
- Single untimed trajectory identifies `D`: NEGATIVE generically.
- Single timed trajectory identifies `D`: NEGATIVE generically under `R(n,D)=r(n+D)`.
- Multiple independent preparations: expected statistically identifiable when candidate sectors are distinct; separate audit recommended.

## Next
WHEELER-39 — Repeated-Preparation / Sector-Tomography Audit: quantify how many independent trajectories are needed to discriminate candidate `D` sectors and whether an observer can reconstruct the hidden-sector distribution.