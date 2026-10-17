# WHEELER-19 — Residual Invariant / Growth-Stability Audit

**Status: PARTIAL PASS at fixed size; NEGATIVE under growth**

## Question

WHEELER-18 found the first translation-inequivalent residual split in the MICRO zero-cost graph at `n=12`, inside the sector `(N1,D)=(6,4)`. One component contains the perfectly balanced cyclic run pattern `(3,3,3,3)` and the other contains unequal four-run patterns such as `(2,2,4,4)` and `(2,3,4,3)`.

This probe asks:

1. Is there a compact invariant that explains the split?
2. Does the phenomenon persist for larger `n`?
3. Does the label survive the existing MICRO growth step?

MICRO assumptions retained from WHEELER-17/18:

- binary cyclic words;
- forbidden patterns `010` and `101`;
- zero cost means no isolated bit, equivalently every cyclic run has length at least 2;
- local dynamics are cyclic length-3 reversals restricted here to zero-cost -> zero-cost moves;
- growth is a one-bit insertion that remains admissible/zero-cost.

## Fixed-size residual variable at n=12

Inside `(N1,D)=(6,4)`, every zero-cost configuration has four cyclic runs with total length 12. The exceptional component is represented by

`(3,3,3,3)`.

A compact statistic that separates it from all other states in this sector is the run-length variance about the mean run length 3:

`V_run = sum_j (ell_j - 3)^2`.

For the balanced class,

`V_run = 0`.

Every other state in the same `(6,4)` sector has

`V_run > 0`.

Examples:

- `(3,3,3,3)` -> `V_run=0`;
- `(2,3,4,3)` -> `V_run=2`;
- `(2,2,4,4)` -> `V_run=4`.

The balanced class is dynamically locked under the zero-cost length-3 reversal graph at `n=12`: no zero-cost reversal path leaves that translation-quotiented component.

Important caution: `V_run` is a separator for this split, not a globally conserved invariant across all MICRO components. It is better interpreted as a local order parameter that identifies the maximally equal run partition.

## Larger n

Exact enumeration was extended through `n=16`.

After quotienting cyclic translation, residual component multiplicity beyond `(N1,D)` persists and grows:

- `n=12`: `(6,4)` splits into 2 components;
- `n=13`: `(6,4)` and `(7,4)` each split into 2;
- `n=14`: `(6,4)`, `(7,4)`, `(8,4)` each split into 3;
- `n=15`: corresponding four-wall sectors split into 3 or 4 components;
- `n=16`: several four-wall sectors split into 4–6 components, and `(8,6)` also splits into 2.

Thus WHEELER-18 was not a one-off finite-size accident. Once `n` is large enough, simple observables `(N1,D)` cease to classify the zero-cost transition graph.

However, the simple balanced-run statistic does **not** classify all of these larger residual components. More detailed cyclic run-spacing information is required.

Therefore the positive scaling result is:

`residual dynamical sector structure persists and becomes richer with n`,

but there is no single discovered scalar invariant that classifies all sectors.

## Growth test

The decisive test is growth stability.

Starting from all labelled `n=12`, `(N1,D)=(6,4)` zero-cost states, one admissible bit is inserted at every possible slot and both bit values are tried, retaining only zero-cost `n=13` descendants.

Let:

- `B` = descendants of the balanced `(3,3,3,3)` component;
- `U` = descendants of the unbalanced component.

Measured sets:

- `|B| = 26` distinct zero-cost descendants;
- `|U| = 156` distinct zero-cost descendants;
- `|B ∩ U| = 26`.

Therefore

`B subset U`.

Every admissible zero-cost growth descendant of the balanced sector is also obtainable by one admissible growth step from an unbalanced sector.

So growth erases the provenance label immediately.

This is stronger than merely saying that the run variance changes: the two fixed-size dynamical sectors have overlapping—and for the balanced side completely shared—growth images.

## Verdict

- **PASS:** at fixed `n=12`, the residual split has a simple geometric order parameter: perfect equality of the four run lengths, `V_run=0`, versus unequal run partitions.
- **PASS:** residual component structure persists and becomes richer for `n=13..16`; it is not a one-size artefact.
- **NEGATIVE:** the simple run-variance statistic does not classify the larger residual structure.
- **NEGATIVE:** the `n=12` residual vacuum label is not preserved by admissible growth. All balanced-sector descendants are also descendants of the unbalanced sector.

## Interpretation

The MICRO zero-cost graph contains genuine fixed-size connectivity sectors, but the first residual label found in WHEELER-18 is not a growth-stable vacuum quantum number.

This strongly weakens its usefulness for the WHEELER topological-defect programme. The sector is dynamically meaningful at fixed size, but once growth is admitted it behaves like a finite-size organization label rather than a protected emergent charge or vacuum index.

The useful retained result is therefore narrower:

`constrained reversal dynamics can create higher-order organization sectors invisible to simple local counts, but growth can merge those sectors.`

## Suggested next probe

**WHEELER-20 — Growth Quotient / Persistent-Sector Audit**

Instead of demanding that fixed-size components survive one growth step individually, construct the directed graph whose nodes are translation-quotiented zero-cost components across successive `n`, with edges given by admissible growth. Ask whether any coarser equivalence class or persistent branch survives indefinitely across growth.

If persistent branches exist, they would be better candidates for an emergent history/vacuum label than any single fixed-size component. If the growth graph becomes broadly mixing, the MICRO branch should be considered negative for protected vacuum-sector emergence.