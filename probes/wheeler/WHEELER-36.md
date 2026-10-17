# WHEELER-36 — Minimal Sufficient Observer State

## Question
For the zero-cost MICRO growth process, is the observer state `(N1,D)` sufficient for Markov closure for all n, and is it minimal?

## Setup
A zero-cost cyclic binary word has no `010` or `101`, equivalently every cyclic run has length at least 2.

Let:
- `n` = word length,
- `N1` = number of 1s,
- `N0=n-N1`,
- `D` = cyclic domain-wall count.

Growth inserts one bit into one cyclic edge, retaining zero cost.

For `D>0`, the cycle has exactly `D/2` zero-runs and `D/2` one-runs.

## Exact growth counts
A zero insertion is admissible either:
1. on a `00` internal edge of a zero-run, or
2. on either side of a 0/1 boundary.

The number of `00` edges is

`N0 - D/2`.

There are `D` boundary edges, and inserting 0 at any boundary extends the adjacent zero-run without producing an isolated bit.

Therefore

`q(N1 -> N1) = N0 - D/2 + D = n - N1 + D/2`.

Likewise, the number of admissible 1 insertions is

`q(N1 -> N1+1) = N1 - D/2 + D = N1 + D/2`.

Under zero-cost insertion, `D` is preserved exactly, so the only observable targets from `(n,N1,D)` are

`(n+1,N1,D)` and `(n+1,N1+1,D)`

with the rates/counts above.

For `D=0`, the two homogeneous cycles are special boundary cases:
- all-zero: only zero insertion is admissible, count `n`;
- all-one: only one insertion is admissible, count `n`.

## Result 1 — All-n lumpability
The aggregate growth counts depend only on `(n,N1,D)`, not on detailed run lengths or their cyclic order.

Hence the projection to `(N1,D)` (with growth layer n known from the process) is strongly lumpable for every n.

This upgrades WHEELER-35 from finite-range computation to an exact combinatorial result.

## Result 2 — Minimality must be stated relative to the observable
`(N1,D)` is not globally minimal in an absolute sense.

If an observer retains only `D`, then because growth preserves `D`, the projected D-process is trivially closed. For `D>0`, total admissible growth count is

`(n-N1+D/2) + (N1+D/2) = n + D`,

which is independent of `N1`.

So `D` alone is a sufficient macrostate for predicting D-only dynamics.

The correct minimality question is instead:

> Starting from an observer that insists on retaining N1, what additional hidden variable is minimally required to restore Markov closure?

The exact rates are

`q0 = n-N1 + D/2`,
`q1 = N1 + D/2`.

At fixed `(n,N1)`, both depend injectively on `D`. Therefore if two hidden states with the same `(n,N1)` have different D, their visible transition rates differ. No coarser statistic that identifies different D values can reproduce the exact N1 transition kernel for all states.

Thus, for the N1-observer,

`D` is the minimal exact hidden augmentation (up to one-to-one recoding of D).

## Interpretation
This gives a concrete sufficient-statistic hierarchy:

full cyclic word -> `(N1,D)` -> `N1`.

- Full word is Markov-complete for the microscopic growth rule.
- `(N1,D)` remains Markov because the partition is lumpable.
- `N1` alone is generally non-Markov because hidden D changes its future hazards.

So emergent memory is precisely the information lost when D is discarded.

## Verdict
- **PROVED:** `(N1,D)` is lumpable for zero-cost growth for all n.
- **PROVED:** exact transition counts are `n-N1+D/2` and `N1+D/2` for D>0, with homogeneous D=0 boundary cases handled separately.
- **CORRECTION:** `(N1,D)` is not absolutely minimal.
- **PROVED:** relative to preserving N1 as the visible variable, D is the minimal exact hidden augmentation, up to bijective recoding.

## Next probe
WHEELER-37 — Observer-Memory Kernel / Hidden-D Reconstruction Audit.

Goal: derive the effective non-Markov N1 dynamics after integrating out D, and determine whether the observer's memory can be represented by a finite hidden-state filter or an explicit memory kernel.