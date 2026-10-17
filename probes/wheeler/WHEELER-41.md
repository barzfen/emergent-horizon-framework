# WHEELER-41 — Optimal Preparation / Observer Design Audit

## Question
Given the hidden-sector discrimination problem from WHEELER-40, can an observer choose an initial preparation `(n0, N1,0)` that makes `D=2` and `D=4` substantially easier to distinguish?

## Sector-conditioned laws
For the zero-cost growth process, an infinite growth trajectory gives a limiting 1-frequency

`p_inf | D ~ Beta(N1,0 + D/2, n0 - N1,0 + D/2)`.

For the comparison `D=2` versus `D=4`, the two laws are therefore

- `D=2`: `Beta(N1,0+1, n0-N1,0+1)`
- `D=4`: `Beta(N1,0+2, n0-N1,0+2)`

A preparation must be feasible in both sectors. Since `D=4` requires two 0-runs and two 1-runs, each of length at least 2,

`N1,0 >= 4` and `n0 - N1,0 >= 4`.

## Numerical optimization
Scanning all common-feasible preparations through `n0=100` using both KL divergence and Chernoff information gives the same qualitative optimum:

- for fixed `n0`, maximal separation occurs at the edge of feasibility,
- namely `N1,0=4` or, by 0/1 symmetry, `N1,0=n0-4`,
- and along this edge the separation increases with `n0` over the tested range.

Thus the balanced preparation used in WHEELER-40 is far from optimal.

At `n0=100, N1,0=4`:

- `KL(D=2 || D=4) ≈ 0.08891`
- `KL(D=4 || D=2) ≈ 0.08238`
- Chernoff information `C ≈ 0.02138`

For comparison, the balanced `n0=8, N1,0=4` case has Chernoff information only

`C ≈ 0.002265`.

## Large-n edge limit
Take the maximally imbalanced common-feasible sequence

`N1,0 = 4`, `n0 -> infinity`.

Then

- `D=2`: `p_inf ~ Beta(5, n0-3)`
- `D=4`: `p_inf ~ Beta(6, n0-2)`.

Under the rescaling `x = n0 p_inf`, these converge to

- `D=2`: `x => Gamma(5,1)`
- `D=4`: `x => Gamma(6,1)`.

Hence the asymptotic discrimination problem remains nontrivial and strictly separated.

The limiting KL divergences are

- `KL(Gamma(5,1) || Gamma(6,1)) ≈ 0.10332`
- `KL(Gamma(6,1) || Gamma(5,1)) ≈ 0.09668`

and the limiting Chernoff information is

`C_inf ≈ 0.02497`.

## Sample-complexity consequence
For equal priors, the standard Chernoff bound

`P_error <= (1/2) exp(-m C)`

gives the following conservative asymptotic preparation counts on the optimal edge:

- 90% correct: about 65 runs
- 95% correct: about 93 runs
- 99% correct: about 157 runs

At the practical finite choice `n0=100, N1,0=4`, the same bound gives approximately

- 90% correct: 76 runs
- 95% correct: 108 runs
- 99% correct: 184 runs.

These are dramatically smaller than the balanced-preparation WHEELER-40 bounds of 711, 1017, and 1728 runs.

## Interpretation
Observer design matters. A hidden sector that is difficult to distinguish under one preparation can become much easier to detect under another, even though the underlying sector laws are unchanged.

The useful preparation principle here is not balance but controlled asymmetry: choose the smallest minority population compatible with both candidate sectors.

This does not mean arbitrarily large `n0` is automatically operationally optimal. If preparation cost scales with system size, a different objective such as information per primitive resource may have a finite optimum.

## Verdict
- **PASS**: preparation choice can change hidden-sector distinguishability by an order of magnitude in Chernoff information.
- **COMPUTATIONAL**: for fixed `n0` up to 100, the optimum is at `N1,0=4` or `n0-4`.
- **ANALYTIC**: the large-`n0` edge family converges to `Gamma(5,1)` versus `Gamma(6,1)` with nonzero limiting KL and Chernoff separation.
- **OPEN**: prove global fixed-`n0` edge optimality for all `n0`.
- **OPEN**: optimize information per preparation cost rather than information per independent run.
