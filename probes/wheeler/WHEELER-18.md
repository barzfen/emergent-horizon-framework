# WHEELER-18 — Vacuum Component / Emergent Label Audit

**Status: PARTIAL PASS; first nontrivial residual component label appears at n=12**

## Question

Treat the zero-cost states of the existing MICRO rule as a graph under admissible length-3 reversals that remain at zero cost. Does connected-component membership define an emergent vacuum label that is not reducible to obvious conserved quantities or mere translation around the cycle?

MICRO rule used here:

- binary cyclic words;
- forbidden local patterns `010` and `101`;
- zero cost means neither forbidden pattern occurs;
- dynamics: reverse a length-3 segment;
- only zero-cost -> zero-cost moves are retained for the vacuum graph.

## Raw zero-cost graph

Exact enumeration gives the following numbers of zero-cost states and connected components:

| n | zero-cost states | raw components |
|---:|---:|---:|
| 4 | 6 | 3 |
| 5 | 12 | 4 |
| 6 | 20 | 10 |
| 7 | 30 | 18 |
| 8 | 46 | 32 |
| 9 | 74 | 42 |
| 10 | 122 | 58 |
| 11 | 200 | 74 |
| 12 | 324 | 112 |

Two simple quantities are constant on every connected component examined:

- Hamming weight `N1 = number of 1s`;
- domain-wall count `D = number of cyclic nearest-neighbour changes 0<->1`.

However, raw component multiplicity is misleading because many components differ only by cyclic translation of the same word around the ring.

## Translation quotient

After identifying configurations related by cyclic rotation, the component counts become:

| n | translation-quotiented components |
|---:|---:|
| 4 | 3 |
| 5 | 4 |
| 6 | 5 |
| 7 | 6 |
| 8 | 8 |
| 9 | 10 |
| 10 | 12 |
| 11 | 14 |
| 12 | 18 |

For every `n <= 11`, these translation-quotiented components are completely classified by the pair `(N1,D)`.

Thus up to `n=11`, there is no evidence for a genuinely new vacuum label beyond weight and domain-wall count once translation is treated as observer-irrelevant.

## First genuine residual split at n=12

At `n=12`, the sector

`(N1,D) = (6,4)`

splits into two disconnected translation-quotiented components.

They are distinguished by cyclic run-length structure.

One component contains run patterns equivalent to

- `(2,2,4,4)`;
- `(2,3,4,3)`;

and contains 48 labelled configurations before translation quotienting.

The other component contains the highly regular pattern

- `(3,3,3,3)`

and contains 6 labelled configurations before translation quotienting.

No zero-cost length-3 reversal path connects these two classes, even though they have identical Hamming weight and identical domain-wall count.

Therefore component membership first carries genuinely additional dynamical information at `n=12` in the tested range.

## Interpretation

This is weaker than a topological vacuum label in the field-theory sense. The split is a connectivity invariant of a discrete constrained-dynamics graph. It may reflect a higher-order run-length/spacing invariant rather than topology.

The important result is:

`zero-cost admissibility + local reversal dynamics -> disconnected vacuum sectors not always captured by simple local counts`.

But the effect does not appear at the smallest sizes; it emerges only once the configuration is large enough to support inequivalent run-spacing organizations.

## Verdict

- **PASS:** zero-cost MICRO dynamics has disconnected vacuum components.
- **NEGATIVE / caution:** most apparent multiplicity through `n=11` is explained by `(N1,D)` plus cyclic translation.
- **PARTIAL PASS:** at `n=12`, a genuinely residual component split survives translation and shares the same `(N1,D)` values.
- **UNRESOLVED:** whether this residual split is governed by a clean conserved invariant, scales to larger `n`, or can act as a robust vacuum label under growth.

## Next probe

**WHEELER-19 — Residual Invariant / Growth-Stability Audit**

Tasks:

1. Identify an explicit invariant that separates the `n=12`, `(N1,D)=(6,4)` components, preferably from cyclic run-length data or a Fourier/parity statistic.
2. Test whether the invariant predicts all zero-cost components for `n>12`.
3. Apply the EHF growth operation and determine whether the label is preserved, split, merged, or destroyed.

If the label survives growth and has a compact algebraic definition, it becomes a serious candidate for an emergent vacuum-sector variable. If growth freely mixes it, it is merely a finite-size dynamical obstruction.