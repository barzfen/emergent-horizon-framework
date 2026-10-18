# WHEELER-42 — Information-per-Resource / Optimal Experimental Cost Audit

## Question
Does the preparation that maximizes hidden-sector distinguishability also maximize distinguishability per unit preparation cost?

We compare the same hidden sectors as WHEELER-40/41:

- D = 2
- D = 4

For a zero-cost cyclic preparation with size n0 and N1,0 = k, the infinite-growth limiting frequency obeys

- D=2: p∞ ~ Beta(k+1, n0-k+1)
- D=4: p∞ ~ Beta(k+2, n0-k+2)

Shared feasibility for D=4 requires k >= 4 and n0-k >= 4.

## Baseline cost model
Take preparation cost proportional to substrate size:

Cprep(n0) = c n0.

The overall constant c only fixes units, so optimize

η(n0,k) = C_Ch(n0,k) / n0,

where C_Ch is the Chernoff information between the two Beta laws.

## Numerical search
Search over all shared-feasible integer preparations, 8 <= n0 <= 300, and 4 <= k <= n0-4.

For every n0, the optimum remains on the extremal-composition boundary:

k = 4 or k = n0-4.

However, unlike WHEELER-41, η does not increase indefinitely with n0.

The numerical maximum occurs at

n0 = 21,
N1,0 = 4 or 17.

At this point:

C_Ch ≈ 0.01063072,
η ≈ 0.000506225 per unit n0.

Representative values along the optimal boundary k=4:

| n0 | Chernoff information | C_Ch / n0 |
|---:|---:|---:|
| 8 | 0.00226480 | 0.00028310 |
| 12 | 0.00434904 | 0.00036242 |
| 16 | 0.00754537 | 0.00047159 |
| 20 | 0.01009287 | 0.00050464 |
| 21 | 0.01063072 | **0.00050622** |
| 22 | 0.01113426 | 0.00050610 |
| 100 | ≈ 0.02138 | ≈ 0.0002138 |
| 300 | ≈ 0.02373 | ≈ 0.0000791 |

Thus larger preparations continue to increase information per run, but eventually waste resources because the gain saturates while preparation cost grows linearly.

## Interpretation
WHEELER-41 optimized information per preparation and therefore drove n0 toward large values.

WHEELER-42 shows that once preparation cost is included, the optimum becomes finite.

For the baseline linear cost model:

**Optimal preparation:**

(n0, N1,0) = (21,4) or (21,17).

The observer should use an extremal but not arbitrarily large preparation.

## Structural lesson
Optimal observability depends on three distinct ingredients:

1. the hidden-sector laws,
2. the chosen observable/projection,
3. the resource cost assigned to preparation.

Hence there is no unique “best observer experiment” without a cost model.

## Caveats
The optimum n0=21 is conditional on:

- the D=2 versus D=4 discrimination task,
- infinite-growth endpoint observation,
- Chernoff information as the discrimination metric,
- equal treatment of the two sectors,
- linear preparation cost Cprep ∝ n0.

Different cost functions can move the optimum.

## Verdict
- PASS: information-per-run and information-per-resource have different optima.
- PASS: under linear cost, the optimum is finite.
- COMPUTATIONAL: n0=21 is the optimum over the searched integer range up to n0=300.
- OPEN: derive the optimum analytically and test nonlinear cost models.
