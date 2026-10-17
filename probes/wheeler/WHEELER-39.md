# WHEELER-39 — Hidden-Sector Distinguishability / Many-Observer Audit

## Question

WHEELER-38 showed that a single arbitrarily long coarse trajectory need not identify the growth-stable hidden sector `D`. Does identifiability return if an observer has access to repeated independent preparations, several observers, or several observation channels?

## Setup

For a fixed preparation `(n0,N10)` and hidden sector `D`, the zero-cost growth process has the Pólya-urn transition law

\[
P(\Delta N_1=1\mid n,N_1,D)=\frac{N_1+D/2}{n+D},
\]

\[
P(\Delta N_1=0\mid n,N_1,D)=\frac{n-N_1+D/2}{n+D}.
\]

For one infinite untimed trajectory, the limiting fraction of 1s satisfies

\[
p_\infty\mid D\sim \mathrm{Beta}(\alpha_D,\beta_D),
\]

with

\[
\alpha_D=N_{1,0}+D/2,\qquad
\beta_D=n_0-N_{1,0}+D/2.
\]

Different admissible values of `D` give distinct Beta laws, although their supports overlap on `(0,1)`.

## Case A — One trajectory

Because the Beta laws overlap, observing one draw `p_\infty` cannot identify `D` exactly with probability one. This is the WHEELER-38 result.

## Case B — Repeated independent preparations with common D

Suppose the substrate can be prepared independently `m` times with the same hidden sector `D`, producing independent limiting fractions

\[
p_1,\ldots,p_m\stackrel{iid}{\sim}f_D,
\]

where `f_D` is the corresponding Beta density.

For two distinct sectors `D\neq D'`, the densities are not identical. Hence

\[
\mathrm{KL}(f_D\Vert f_{D'})>0.
\]

The log likelihood ratio is additive across preparations:

\[
\log \frac{L_m(D)}{L_m(D')}
=\sum_{j=1}^{m}\log\frac{f_D(p_j)}{f_{D'}(p_j)}.
\]

Under the true sector `D`, the strong law of large numbers gives

\[
\frac1m\log \frac{L_m(D)}{L_m(D')}
\to \mathrm{KL}(f_D\Vert f_{D'})>0.
\]

Therefore, for a finite admissible set of candidate `D` values and nonzero prior mass on the true sector, the posterior concentrates on the true `D` as the number of independent preparations tends to infinity.

### Verdict

A hidden sector that is not exactly identifiable from one infinite trajectory becomes statistically identifiable from infinitely many independent trajectories drawn from the same sector.

## Balanced preparations

If `N10=n0/2`, all sectors have the same limiting mean `1/2`, but they still have different concentration parameters and therefore different variances and higher moments. Thus repeated preparations still distinguish `D`; mean information alone is insufficient, but the full distribution is identifiable.

## Case C — Many observers watching the same trajectory

If several observers see the same coarse variable `(n,N1)` on the same underlying history, they do not obtain independent samples. Repeating the same observation channel does not multiply information about `D`.

Thus

\[
\boxed{\text{many copies of the same observation}\neq\text{many independent preparations}.}
\]

## Case D — Multiple distinct observation channels

Let observers see projections `\pi_1(X),\ldots,\pi_k(X)` of the same full substrate state. Their joint observation is equivalent to the combined map

\[
\Pi(X)=(\pi_1(X),\ldots,\pi_k(X)).
\]

`D` becomes identifiable from one history only if the joint law induced by `\Pi` separates the candidate sectors strongly enough. In particular, if `D` is measurable from the combined observable state, identifiability is immediate; if all channels discard the same `D`-sensitive information, adding observers does not help.

## Main result

There are two distinct notions:

1. **Single-history observability:** may fail permanently under a coarse projection.
2. **Ensemble identifiability:** can hold because the sector determines the distribution over histories.

For the present MICRO growth model,

\[
\boxed{\text{single trajectory: not exactly identifying}}
\]

but

\[
\boxed{\text{independent repeated preparations: asymptotically identifying}.}
\]

This is analogous to a parameter that cannot be inferred with certainty from one realization but is identifiable from an ensemble distribution.

## Status

- Distinct sector-conditioned Beta laws: **PROVED** from the exact Pólya-urn form.
- One-trajectory exact identification: **NEGATIVE** (WHEELER-38).
- Repeated independent preparations with common `D`: **PASS / asymptotically identifiable** for a finite candidate set.
- Multiple identical observers on one history: **NEGATIVE / no independent gain**.
- Multiple distinct channels: **CONDITIONAL** on whether the joint projection separates sectors.

## Interpretation discipline

This is a statistical-identifiability result for the EHF/MICRO growth model. It does not establish hidden variables in physical quantum theory, superselection sectors in nature, or experimentally inaccessible physical quantities.

## Next target

Test whether the ensemble-identifiable hidden sector has an observer-independent operational signature under finite resources: derive sample complexity and optimal discrimination error between nearby `D` sectors (WHEELER-40).