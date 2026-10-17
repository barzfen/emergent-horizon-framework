# WHEELER-28 — Rate Normalization / Continuum-Limit Audit

**Status: PASS for rate-scaling criterion; physical gap remains normalization-dependent**

## Setup

For Core C on undirected Hamilton cycles of K_n under one 2-opt comparison,

- degree: d_n = n(n-3)/2;
- combinatorial Laplacian gap: lambda_n = n-1.

Let R_n denote the total comparison-event rate available from one state. If that total rate is shared uniformly across the d_n admissible comparisons, each edge has rate R_n/d_n. The continuous-time generator is then proportional to the normalized graph Laplacian, so the physical relaxation gap is

Delta_n = R_n * (n-1)/d_n
        = R_n * 2(n-1)/(n(n-3)).

Hence asymptotically

Delta_n ~ 2 R_n / n.

## Three normalizations

### 1. Fixed rate per admissible comparison

If every admissible comparison fires at fixed rate r, then R_n = r d_n ~ r n^2/2. Therefore

Delta_n = r(n-1) ~ r n.

The gap grows rather than closes.

### 2. Fixed total rate per state / one random comparison per step

If R_n = R is independent of n, then

Delta_n ~ 2R/n -> 0.

Equivalently, for the discrete-time simple random walk the spectral gap is

gamma_n = (n-1)/d_n = 2(n-1)/(n(n-3)) ~ 2/n.

So the same Core-C geometry is asymptotically gapless when one comparison event is one unit of time.

### 3. Growth or observer time

If one unit of internal/growth time allows R_n comparison events on average, then the critical scaling is

R_n ~ c n.

Specifically:

- R_n = o(n): Delta_n -> 0;
- R_n ~ c n: Delta_n -> 2c, a finite nonzero limit;
- R_n = omega(n): Delta_n diverges.

Thus a finite continuum relaxation gap requires the number of effective comparisons available per growth-time unit to scale linearly with n.

## Interpretation

The graph spectrum alone does not determine a physical mass or relaxation gap. One must also specify the measure/rate on admissible comparisons — effectively the dynamical clock.

This connects directly to the EHF time problem. If growth is treated as an internal clock, then the relevant question is not merely how many admissible comparisons exist, but how comparison activity scales between successive growth events.

The result can be summarized as

state-graph geometry + comparison-rate measure -> effective continuum kinetics.

This is a stronger formulation than using the unnormalized graph Laplacian by itself.

## Verdict

- **PASS:** exact normalization law derived.
- **PASS:** critical scaling R_n ~ n identified.
- **NEGATIVE:** Core-C graph geometry alone does not establish a physical nonzero asymptotic gap.
- **OPEN:** derive R_n from EHF primitives rather than choose it by hand.

## Next probe

**WHEELER-29 — Growth-Clock / Comparison-Rate Derivation Audit**

Test whether existing EHF growth rules naturally imply a scaling law for the number of admissible comparisons between growth events. The key target is whether R_n is sublinear, linear, or superlinear in n. A natural derivation of R_n ~ n would be especially significant because it would convert the exact Core-C graph gap into a finite nonzero gap in growth-time units without arbitrary normalization.