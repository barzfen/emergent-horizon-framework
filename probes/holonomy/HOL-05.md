# EHF-HOL-05 — Renormalized Refinement Generator Audit

**Status: MIXED / NEGATIVE FOR THE PROPOSED q^2 FULL-OPERATOR GENERATOR; POSITIVE FOR A FIRST-ORDER q-SCALED NATIVE REFINEMENT DEFECT.**

## Question

HOL-04 found two different asymptotic facts:

1. the distinguished holonomy angle changes by only `Delta theta_q = O(q^-2)`, with `q^2 Delta theta_q -> 3`;
2. the native growth-intertwining obstruction occupies a vanishing fraction of observer space.

This suggested testing an operator analogue of the scalar angular derivative. The naive proposal was schematically

`G_q = q^2 [H_(N) U - U H_n]`,

where `U` is the native isometric growth embedding and `H_n`, `H_N` are native three-observer loop operators.

The point of this audit is to test that proposal rather than assume the scalar `q^-2` law controls the full matrix difference.

## Existing ingredients

The audit uses only existing RECUR definitions:

- the exact-form polar observer transports from RECUR-08;
- the normalized isometric Hamilton-cycle and perfect-matching growth maps from RECUR-11;
- the same old-observer triangle `(0,1,2)`;
- the Frobenius and singular-value defect diagnostics already used in RECUR-11/13.

For Hamilton cycles, growth is `n -> n+1`. For perfect matchings, growth is `n -> n+2`.

Define the native loop refinement defect

`D_n = H_N U - U H_n`.

This is rectangular but canonical once the existing native growth embedding and native loop operators are fixed.

## Numerical audit

The matrices were reconstructed directly from the existing RECUR-08 and RECUR-11 code and evaluated beyond the original finite sweep.

### Hamilton cycles

Representative Frobenius norms:

| old n | q=n-2 | ||D_n||_F | q ||D_n||_F | q^2 ||D_n||_F |
|---:|---:|---:|---:|---:|
| 5 | 3 | 1.340626 | 4.021878 | 12.065635 |
| 8 | 6 | 0.493274 | 2.959643 | 17.757855 |
| 12 | 10 | 0.282834 | 2.828340 | 28.283399 |
| 17 | 15 | 0.184378 | 2.765668 | 41.485014 |

The defect tends downward, but the `q^2` rescaling grows rather than stabilizes. The `q` rescaling is the plausible finite normalization.

At `n=12`, the largest singular values of `q D_n` are approximately

`2.2106, 1.4775, 0.4302, 0.3032, ...`.

At `n=17` they are approximately

`2.1463, 1.4581, 0.3130, 0.2506, ...`.

The rank grows (`5,7,9,...` in this tested sequence), so convergence of the full rectangular operator requires a precise inductive-limit topology and cannot be claimed merely from bounded Frobenius norms.

### Perfect matchings

Representative values:

| old n | q=n-2 | ||D_n||_F | q ||D_n||_F | q^2 ||D_n||_F |
|---:|---:|---:|---:|---:|
| 6 | 4 | 0.817630 | 3.270519 | 13.082077 |
| 10 | 8 | 0.383732 | 3.069853 | 24.558827 |
| 14 | 12 | 0.248729 | 2.984749 | 35.816983 |
| 22 | 20 | 0.145822 | 2.916446 | 58.328917 |

Again `q^2 D_n` is not the natural full-operator scaling. The defect is consistent with `O(1/q)` in Frobenius norm over the audited range.

Unlike Hamilton cycles, the perfect-matching defect has rank `2` throughout this sweep. At `n=22`, the two non-negligible singular values of `qD_n` are approximately `2.89384` and `0.36239`.

## Main result

The scalar rotation angle and the full native refinement defect live on different asymptotic scales.

For the distinguished rotation pair,

`Delta theta_q = O(q^-2)`

and

`q^2 Delta theta_q -> 3`.

But for the complete native loop-intertwining defect,

`||D_n||_F = O(q^-1)`

is the scaling supported by the finite data, while

`q^2 ||D_n||_F`

grows approximately linearly.

Therefore the originally proposed full generator

`q^2 (H_N U - U H_n)`

**fails the first boundedness gate in Frobenius norm** and is rejected as the natural full-space refinement generator.

This is an important separation: the `3/q^2` angular drift describes a distinguished spectral sector, not the leading change of the whole observer loop operator.

## Candidate first-order defect

The data instead motivate

`J_n = q (H_N U - U H_n)`.

Its Frobenius norm remains bounded and appears to approach a finite nonzero scale in both controls over the tested range. This makes `J_n` a better candidate for a first-order native growth defect.

However, bounded norm is not operator convergence. The observer spaces change dimension, and in the Hamilton family the defect rank itself grows. A claim of a limiting operator requires an explicit common inductive-limit space or a canonical decomposition into stable representation sectors.

HOL-05 therefore does **not** claim that `J_n` already converges to a unique generator.

## Relation to exact block refinement

RECUR-13 constructs a renormalized enlarged connection whose inherited sector satisfies exact naturality. For that deliberately corrected connection, the inherited-loop defect is identically zero:

`H_hat U - U H_n = 0`.

So a nonzero refinement generator cannot come from the exactly inherited old sector itself. It must describe either:

- the difference between native and exactly natural growth;
- the growth-added complement;
- or a sector-specific change such as the distinguished rotation pair before exact block correction.

This reinforces the HOL-04 conclusion that the local candidate quantity is the **refinement obstruction**, not the persistent inherited holonomy.

## Theorem-status boundary

**Established directly from existing exact matrix constructions plus finite numerical evaluation**

- the native defect `D_n = H_N U - U H_n` is well defined in both audited controls;
- `q^2 ||D_n||_F` does not stabilize over the tested ranges and grows strongly;
- `q ||D_n||_F` remains bounded and slowly varying over the same ranges;
- the distinguished angular drift has a different `q^-2` scaling;
- the exact RECUR-13 block connection has zero inherited-sector defect by construction.

**Supported by finite-size trend, not yet proved analytically**

- `||D_n||_F = O(1/q)`;
- convergence of `q ||D_n||_F` to a finite constant;
- convergence of individual singular-value branches of `qD_n`.

**Not established**

- convergence of `qD_n` as an operator;
- a unique inductive-limit observer Hilbert space;
- a universal generator shared by HC, PM, or arbitrary substrates;
- identification of this refinement defect with geometric curvature, a Hamiltonian, or a physical field.

## Interpretation

HOL-05 reveals a two-scale structure:

`distinguished spectral drift ~ q^-2`

while

`full native refinement defect ~ q^-1`.

That is more informative than a single continuum exponent. The observer system contains a leading first-order rearrangement of a thin/growth-sensitive sector, while its distinguished nontrivial rotation changes only at second order.

## Next probe

**HOL-06 — Representation-Sector Generator Audit.**

Use the symmetry decomposition already present in RECUR-08 to put successive observer spaces into canonical trivial/standard/residual sectors. Project `D_n` into those sectors and determine analytically which blocks carry the `1/q` term and which carry the `1/q^2` angular drift. This avoids comparing growing matrices entry-by-entry and may turn the bounded `qD_n` observation into a finite-dimensional sectorwise limit theorem.
