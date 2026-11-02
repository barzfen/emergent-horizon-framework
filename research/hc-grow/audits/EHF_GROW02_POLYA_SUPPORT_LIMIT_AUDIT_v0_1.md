# EHF-GROW-02-POLYA-01 — Support-Density Limit Audit

**Date:** 2026-09-29  
**Branch:** GROW / spectral-criticality conjecture check  
**Status:** Exact result conditional on the recurrence transcribed below. The original GROW-02 source file was not located in the current Library search, so source fidelity is not certified.

## Purpose

Check the proposed claim that the two-colour growth rule has a critical support density (x^*=1/2). The CFT interpretation is not tested here. This audit checks only the support process and its limiting law.

## Input recurrence

The recurrence quoted in the discussion is

\[
P_n(\ell,\ell)=\frac{n+1-\ell}{n+2},\qquad
P_n(\ell,\ell+1)=\frac{\ell+1}{n+2}.
\]

The state changes from ((n,\ell)) to size (n+1). Define urn counts

\[
a=\ell+1,\qquad b=n+1-\ell.
\]

Then (a+b=n+2). On the increase event, ((a,b)\mapsto(a+1,b)); on the stay event, ((a,b)\mapsto(a,b+1)). The transition probabilities are exactly (a/(a+b)) and (b/(a+b)). Thus the quoted recurrence is the standard linear two-colour Pólya urn.

## Exact limiting law

For initial state ((n_0,\ell_0)),

\[
a_0=\ell_0+1,\qquad b_0=n_0+1-\ell_0.
\]

After (k) growth steps, the urn fraction

\[
X_k=\frac{a_k}{a_k+b_k}=\frac{\ell_k+1}{n_0+k+2}
\]

converges almost surely and in distribution to

\[
X_\infty\sim\operatorname{Beta}(\ell_0+1,n_0+1-\ell_0).
\]

Its mean and variance are

\[
\mathbb E[X_\infty]=\frac{\ell_0+1}{n_0+2},\qquad
\operatorname{Var}(X_\infty)=
\frac{(\ell_0+1)(n_0+1-\ell_0)}{(n_0+2)^2(n_0+3)}.
\]

The finite-(k) increment count has the beta-binomial law. The accompanying Python script checks that identity exactly with rational arithmetic across the listed cases.

## Starting-state ambiguity resolved conditionally

The two initializations stated in the proposed argument do not agree:

| Interpretation | \(\ell_0\) | \((a_0,b_0)\) | Limit law | Mean |
|---|---:|---:|---|---:|
| “(a_0=3)” | 2 | \((3,n_0-1)\) | \(\mathrm{Beta}(3,n_0-1)\) | \(3/(n_0+2)\) |
| “support frozen at \(\ell=3\)” | 3 | \((4,n_0-2)\) | \(\mathrm{Beta}(4,n_0-2)\) | \(4/(n_0+2)\) |
| balanced support initialization | \(\lfloor n_0/2\rfloor\) | \((\ell_0+1,n_0+1-\ell_0)\) | corresponding Beta law | approaches (1/2) as (n_0\to\infty) |

Under either fixed-support initialization \(\ell_0=2\) or \(\ell_0=3\), the mean tends to zero as (n_0\to\infty). A half-density mean occurs when the *initial support itself scales proportionally* with size, \(\ell_0/n_0\to1/2\); it is inherited from that initial condition.

For example, at (n_0=1000), \(\ell_0=2\) gives \(\mathrm{Beta}(3,999)\) with mean \(1/334\approx0.002994\). At the same size, \(\ell_0=3\) gives \(\mathrm{Beta}(4,998)\) with mean \(2/501\approx0.003992\). A balanced start \(\ell_0=500\) gives \(\mathrm{Beta}(501,501)\) with mean (1/2).

## Verdict and claim status

- **Established, conditional on the recurrence:** exact Pólya-urn identification, Beta limiting law, mean, variance, and beta-binomial finite-step law.
- **Input ambiguity:** \(a_0=3\) corresponds to \(\ell_0=2\), whereas \(\ell_0=3\) corresponds to \(a_0=4\). The original GROW-02 source must resolve which state is intended.
- **Not established:** a distinguished critical density, a spectral scaling transition, conformal invariance, a CFT, or a quantum interpretation.
- **Disposition:** the proposed (x^*=1/2) is not a consequence of the quoted fixed-support recurrence. Park the CFT bridge until the source transition rule and the LR2 finite-size spectral scaling are independently specified and tested.

## Reproducibility

Run:

```bash
python ehf_grow02_polya_support_limit_audit.py
```

The script uses only Python's standard library and writes `ehf_grow02_polya_support_limit_results.json`. All finite-step distribution comparisons use exact fractions.

## Cumulative record of this lead

1. **Initial proposal:** the coincidence of Fock, Plancherel, and monotone spectral-flow structures might signal a 2D critical system.
2. **Status correction:** the CFT and unitarity claims were withdrawn as unsupported; the CFT link is now explicitly conjectural.
3. **First quantitative prediction:** (x^*=1/2) was proposed from the half-cycle boundary.
4. **Audit result:** under the quoted recurrence, the urn mapping is exact, but the limiting mean depends on the initial support density. The two quoted starting-state descriptions ((a_0=3) and \(\ell_0=3\)) are inconsistent with each other. For fixed \(\ell_0=2\) or 3 and growing (n_0), the limit mean tends to zero.
5. **Next admissible step:** locate and read the canonical GROW-02 source, lock ((n_0,\ell_0)), then separately define the LR2 spectral observable and its size normalization before testing for critical scaling.
