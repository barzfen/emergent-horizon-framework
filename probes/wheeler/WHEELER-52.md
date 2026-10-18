# WHEELER-52 — Microstate-Channel / Majorization Audit

## Question

Does the entropy-nondecrease result from WHEELER-51 survive before observer coarse-graining? In other words, is the full zero-cost microstate growth channel itself entropy-nondecreasing?

## Setup

Let `S_{n,D}` be the zero-cost cyclic binary words of length `n` with boundary count `D`, where zero cost means no cyclic `010` or `101` substring.

For a source microstate `w in S_{n,D}`, growth inserts one bit in one cyclic slot subject to zero-cost admissibility. WHEELER-36 established that every source in a fixed `D` sector has exactly

`n + D`

admissible insertion events.

Define the microscopic growth kernel by choosing uniformly among these admissible events:

`K_{n,D}(w,v) = (# admissible insertion events from w producing v)/(n+D)`.

Rows therefore sum to 1.

## Incoming-event bound

Fix a target microstate `v in S_{n+1,D}`.

Any incoming insertion event that produces `v` identifies which one of the `n+1` positions in `v` was the newly inserted symbol. Once that inserted position is specified, deleting it determines the predecessor word and the corresponding insertion event. Hence the number of incoming microscopic events is at most

`n+1`.

Therefore for every target column,

`sum_w K_{n,D}(w,v) <= (n+1)/(n+D)`.

For a nonzero cyclic binary boundary count, `D` is even and therefore `D >= 2`. Hence

`sum_w K_{n,D}(w,v) <= (n+1)/(n+2) < 1`.

For `D=0`, the sector consists of the all-zero and all-one words. Each source has `n` admissible insertion slots, all reproducing the same corresponding target, so the relevant column sum is exactly 1.

Thus, in every sector, the microstate growth kernel is row-stochastic and column-substochastic.

## Majorization consequence

A rectangular row-stochastic matrix whose column sums are all at most 1 can be completed, after zero-padding the input distribution, to a doubly stochastic square matrix. Therefore the output probability vector is majorized by the zero-padded input vector.

Hence for every input distribution `p` on `S_{n,D}`,

`H(p K_{n,D}) >= H(p)`.

So Shannon entropy is nondecreasing under the full microscopic growth channel.

This is stronger than WHEELER-51: the monotonicity does not require the observer projection to `(N1,D)`.

## Relative entropy

For any two distributions `p` and `q` propagated through the same microscopic channel, standard data processing gives

`D_KL(p K || q K) <= D_KL(p || q)`.

This contraction is generic to stochastic maps and should not be presented as uniquely EHF-specific.

## Computational audit

A brute-force enumeration was run for all zero-cost sectors through `n=14`.

Checks performed:

1. every source had exactly `n+D` admissible insertion events;
2. every target column sum was `<= 1`;
3. random input distributions were propagated through every sector, with no Shannon-entropy decrease observed.

No violations occurred.

Representative maximum column sums:

- `n=13, D=2`: `0.866666...`
- `n=14, D=2`: `0.875`
- `n=14, D=4`: `0.777777...`
- `D=0`: exactly `1`

The computational audit supports the analytic proof but is not needed for it.

## Result

**PROVED (within the zero-cost equal-event growth model):** the full microscopic growth channel is column-substochastic, and therefore Shannon entropy is nondecreasing for every input microstate distribution.

Equivalently,

`microscopic growth => majorization toward greater mixing`.

This means the entropy increase found in WHEELER-50 and WHEELER-51 is not merely an artifact of observer coarse-graining.

## Important limitation

This still does not establish thermodynamic entropy, temperature, heat flow, or a physical second law. The result is an exact information-theoretic property of this specific growth channel.

The equal weighting of admissible insertion events is part of the model assumption. Reweighting growth events can destroy column-substochasticity and must be tested separately.

## Next probe

**WHEELER-53 — Weighted Growth / Entropy-Robustness Audit**

Perturb the equal-event rule by assigning local weights to admissible insertions and determine the necessary and sufficient conditions under which column-substochasticity, majorization, and entropy nondecrease survive.
