# WHEELER-23 — Dynamical Spectral Gap / Boundary-Hamiltonian Audit

**Status: NEGATIVE for a positive thermodynamic dynamical gap; exact diffusive closing in the simplest mobile boundary sector**

## Question

WHEELER-22 established a static excitation-cost gap for the unified boundary field. The stronger question here is whether the actual admissible local dynamics has a nonzero spectral gap as system size grows.

Use the existing MICRO zero-cost dynamics:

- binary cyclic words;
- forbidden local patterns `010` and `101`;
- zero-cost states only;
- local move: reverse a cyclic length-3 segment;
- retain only moves that remain inside the zero-cost set.

Treat the move graph Laplacian `L = D - A` as the kinetic generator and inspect the lowest nonzero eigenvalue in the simplest non-vacuum sector `D=2`.

## D=2 mobile sector

A `D=2` zero-cost configuration consists of one contiguous 1-block and one contiguous 0-block, each of length at least 2. Under the admissible length-3 reversal, the mobile degree of freedom is the position of the boundary pair around the cycle.

The largest mobile connected component has exactly `n` states and is isomorphic to the cycle graph `C_n`.

Exact numerical checks for `n=4..14` give:

| n | mobile-component size | lambda_1 |
|---:|---:|---:|
| 4 | 4 | 2.0000000000 |
| 5 | 5 | 1.3819660113 |
| 6 | 6 | 1.0000000000 |
| 7 | 7 | 0.7530203963 |
| 8 | 8 | 0.5857864376 |
| 9 | 9 | 0.4679111138 |
| 10 | 10 | 0.3819660113 |
| 11 | 11 | 0.3174929343 |
| 12 | 12 | 0.2679491924 |
| 13 | 13 | 0.2290879487 |
| 14 | 14 | 0.1980622642 |

These values match the exact cycle-graph formula

`lambda_1(n) = 2 - 2 cos(2 pi / n) = 4 sin^2(pi / n)`.

Hence

`lambda_1(n) ~ 4 pi^2 / n^2`.

The kinetic relaxation time therefore scales diffusively:

`tau ~ n^2 / (4 pi^2)`.

## Relation to the static boundary gap

WHEELER-22 gave a static boundary-energy gap

`Delta E = 2`

for `E = D`, and more generally a positive first closed-cycle excitation cost for any positive additive local boundary energy.

That static gap survives growth because the minimum nonzero domain-wall count remains two.

But the dynamical move-graph gap is different:

- static excitation cost: finite;
- kinetic Laplacian gap: closes as `n^-2`.

Thus the model is energetically gapped but dynamically diffusive.

## Global graph caveat

The full zero-cost move graph is disconnected and therefore has multiple exact zero eigenvalues. The quoted `lambda_1` is the first nonzero eigenvalue within a mobile connected component of the `D=2` sector. This is the appropriate quantity for internal relaxation, but it is not a global unique ground-state spectral gap.

## Verdict

- **PASS:** the admissible local dynamics yields a clean exact spectral law in the simplest boundary sector.
- **NEGATIVE:** there is no positive thermodynamic kinetic gap; `lambda_1 -> 0`.
- **PASS:** the closing is exactly diffusive, `lambda_1 ~ 4 pi^2 / n^2`.
- **IMPORTANT DISTINCTION:** a finite combinatorial excitation-energy gap does not imply a finite dynamical spectral gap.
- **NOT YANG-MILLS:** this result is a discrete constrained-dynamics benchmark only.

## Interpretation

This is a useful failure for the EHF mass-gap programme. A model with quantized finite-energy defects can still possess arbitrarily slow collective motion of those defects as the system grows. To obtain a true positive dynamical gap, EHF would need some mechanism beyond unrestricted translational diffusion of the lowest excitation—e.g. confinement, pinning, curvature of the state graph, nonlocal coupling, or a different kinetic operator derived from the framework.

## Next probe

A productive next step is **WHEELER-24 — Confinement / Gap-Opening Audit**: determine what minimal EHF-native modification of the dynamics, if any, can prevent the `D=2` boundary pair from behaving as a freely diffusing mode, while preserving locality and the previously derived conservation structure. The test must reject mechanisms that merely insert a mass term by hand.
