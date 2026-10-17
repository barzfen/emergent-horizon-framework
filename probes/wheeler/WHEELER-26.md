# WHEELER-26 — Core-C Spectral Law / n=12 Validation Audit

**Status: STRONG PARTIAL PASS; exact candidate eigenvalue derived at n=12, full n=12 gap certification not yet completed**

## Correction to WHEELER-25

WHEELER-25 misinterpreted the archived Core-C spectral quantities. The prior audits were:

- `n=8`: degree `d=20`, Laplacian gap `lambda_gap=7`, second adjacency eigenvalue `mu_2=13`, gap multiplicity `20`;
- `n=10`: degree `d=35`, Laplacian gap `lambda_gap=9`, second adjacency eigenvalue `mu_2=26`, gap multiplicity `35`.

Thus the observed law is not `mu_2=n-1`. It is

`lambda_gap = n-1`

and therefore

`mu_2 = d-(n-1)`.

This also means the normalized Laplacian gap is

`(n-1)/d = 2(n-1)/[n(n-3)] ~ 2/n`,

which tends to zero. Core C is therefore **not** an expander family under the standard normalized-gap criterion. The apparent expander-like conclusion in WHEELER-25 is withdrawn.

## Reconstructing Core C

The archived vertex counts identify Core C as the graph whose vertices are undirected Hamilton cycles of `K_n`, modulo rotation and reversal.

Hence

`|V_n| = (n-1)!/2`.

Two states are adjacent when one is obtained from the other by a 2-opt move: choose two nonadjacent edges of the Hamilton cycle and reconnect, equivalently reverse the intervening cyclic segment.

The number of available 2-opt moves is

`d_n = n(n-3)/2`.

This matches the archived values `d_8=20` and `d_10=35`.

At `n=12`:

- `|V_12| = 11!/2 = 19,958,400`;
- `d_12 = 12*9/2 = 54`.

A full sparse diagonalization over almost twenty million vertices is not a sensible direct audit here, so the symmetry of the graph was used instead.

## Exact edge-incidence eigenvalue

For each edge `e` of `K_n`, define

`f_e(C)=1` if Hamilton cycle `C` contains `e`, and `0` otherwise.

For a fixed cycle `C`:

- if `e` is in `C`, exactly `n-3` 2-opt moves remove `e`, so `d-(n-3)` neighboring cycles retain it;
- if `e` is not in `C`, exactly two 2-opt moves introduce `e`.

Therefore

`A f_e = 2 + [d-(n-1)] f_e`.

After subtracting the constant component, each centered edge-incidence function is an adjacency eigenfunction with eigenvalue

`mu_edge = d-(n-1)`.

Thus at `n=12` there is an **exact** adjacency eigenvalue

`mu_edge = 54-11 = 43`,

corresponding to Laplacian eigenvalue

`lambda_edge = 54-43 = 11`.

So the predicted `n=12` value `11` is not merely a numerical extrapolation: `11` is provably in the Laplacian spectrum.

The remaining question is whether it is the **smallest nonzero** Laplacian eigenvalue, equivalently whether any adjacency eigenvalue lies strictly between `43` and `54`.

## Independent exact reconstruction at smaller n

The Core-C graph was explicitly generated and sparse adjacency spectra computed for `n=5..9`.

| n | |V| | d | second adjacency eigenvalue | Laplacian gap |
|---:|---:|---:|---:|---:|
| 5 | 12 | 5 | 1 | 4 |
| 6 | 60 | 9 | 4 | 5 |
| 7 | 360 | 14 | 8 | 6 |
| 8 | 2,520 | 20 | 13 | 7 |
| 9 | 20,160 | 27 | 19 | 8 |

The archived `n=10` audit continues the sequence:

- `d=35`;
- second adjacency eigenvalue `26`;
- Laplacian gap `9`.

Hence every explicitly/full-audited case `n=5..10` obeys

`lambda_gap(n)=n-1`.

The associated second-adjacency law is

`mu_2(n)=n(n-3)/2-(n-1)`.

## n=12 verdict

At `n=12` we have rigorously established:

1. degree `d_12=54`;
2. an exact adjacency eigenvalue `43`;
3. therefore an exact Laplacian eigenvalue `11`;
4. the same eigenvalue mechanism explains the full-audit gap for every tested `n=5..10`.

What has **not** yet been proved in this probe is that no other representation sector at `n=12` produces a Laplacian eigenvalue below `11`.

Accordingly, the correct status is:

- **PASS:** `d_12=54` exactly;
- **PASS:** `lambda=11` occurs exactly in the n=12 Laplacian spectrum;
- **STRONG COMPUTATIONAL/STRUCTURAL EVIDENCE:** this is the actual spectral gap, based on full audits for every n=5..10 and the same edge-incidence eigenspace mechanism;
- **NOT YET PROVED:** `lambda_gap(12)=11` as the global first nonzero eigenvalue.

## Scaling consequence

If the full-gap law continues,

`lambda_gap=n-1`,

then the unnormalized gap grows linearly, but the random-walk/normalized gap is

`gamma_n=(n-1)/d_n=2(n-1)/[n(n-3)] ~ 2/n -> 0`.

So Core C avoids the `n^-2` diffusive collapse seen in the WHEELER boundary cycle, but it still does **not** form a constant-normalized-gap expander family.

This is nevertheless a different kinetic universality class:

- boundary cycle: normalized/unnormalized gap scales like `n^-2` at fixed degree;
- Core C: unnormalized gap grows as `n`, while normalized gap falls only as `n^-1` because degree grows as `n^2`.

## Next probe

**WHEELER-27 — Core-C Representation / Exact Gap Proof Audit**

Use the `S_n` symmetry of the Hamilton-cycle/2-opt graph to decompose the adjacency operator into representation sectors. The target is to prove or falsify

`lambda_gap(n)=n-1`

for all relevant `n`, rather than attempting a 19.96-million-vertex diagonalization at n=12.

A proof would convert the current empirical law into a genuine theorem about the Core-C kinetic geometry. A counterexample sector with eigenvalue below `n-1` would terminate the conjecture.
