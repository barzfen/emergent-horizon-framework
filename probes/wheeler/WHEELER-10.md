# EHF-WHEELER-10 — Robustness of Threefold Selection

**Status: PARTIAL PASS / NOT UNIVERSAL**

## Goal

Stress-test the `m=3` preference found in WHEELER-09 by varying the cost metric and local transfer dynamics without introducing any explicit `m=3` tuning.

The admissible family remains `Z_m` with `m>=3`, because WHEELER-08 excludes `m=2` when a neutral class plus a distinct conjugate pair are required.

## A. Repair-cost robustness

Use cyclic distance from the neutral class,

`d_m(r) = min(r, m-r)`,

and a generic monotone cost

`c_m(r) = d_m(r)^p`,

with no `m`-dependent parameters.

For the uniform local ensemble, define

`C_p(m) = (1/m) sum_r c_m(r)`.

Representative values:

### Linear cost, `p=1`

- `C(3)=0.6667`
- `C(4)=1.0000`
- `C(5)=1.2000`
- `C(6)=1.5000`
- `C(7)=1.7143`
- `C(8)=2.0000`

### Quadratic cost, `p=2`

- `C(3)=0.6667`
- `C(4)=1.5000`
- `C(5)=2.0000`
- `C(6)=3.1667`
- `C(7)=4.0000`
- `C(8)=5.5000`

### Sublinear cost, `p=1/2`

- `C(3)=0.6667`
- `C(4)=0.8536`
- `C(5)=0.9657`
- `C(6)=1.0934`
- `C(7)=1.1846`
- `C(8)=1.2866`

Thus `m=3` remains the cheapest admissible member across broad monotone local cost families.

## B. Spectral robustness

For symmetric nearest-neighbour transfer on `Z_m`, the basic cycle generator has eigenvalues

`lambda_j = 2 - 2 cos(2 pi j/m)`.

In the pair-transfer normalization used in WHEELER-09 this gives

`gap(m) = 8 sin^2(pi/m)`.

Hence among connected `m>=3` sectors the unit-transfer gap decreases monotonically with `m`, so `m=3` mixes fastest.

This survives any rescaling of the common generator by an `m`-independent constant.

## C. Failure / limitation

The preference is not universal under arbitrary move sets.

For a step-`k` transfer, connectivity depends on `gcd(k,m)`. If `gcd(k,m)>1`, the state space splits into disconnected residue classes. Even when `gcd(k,m)=1`, the spectral ranking depends on the effective generator induced by the chosen move set.

Therefore the threefold preference is robust for a broad class of simple local, connected, monotone dynamics, but not for every conceivable admissibility rule.

## Interpretation

WHEELER-10 strengthens the statement from WHEELER-09:

`minimal conjugate-supporting structure + broad monotone local costs + simple connected local transfer -> m=3 favored`.

But it does **not** establish a universal theorem that all reasonable EHF dynamics select `m=3`.

The strongest retained claim is that `m=3` is a robust economical attractor within a natural family of untuned local models.

## Next question

A stronger test would be to derive the local move class itself from existing EHF primitives (reversal, growth, observer equivalence, Hamilton-history structure) rather than choosing a generic `Z_m` transfer rule externally. If that derivation again leads to the connected unit-transfer class and preserves the `m=3` preference, the result would become materially stronger.