# WHEELER-21 — Boundary Current / Domain-Wall Unification Audit

**Status: PASS for common boundary object; NOT a particle derivation**

## Question

Are Wheeler's signed current/winding invariant and MICRO's growth-stable domain-wall count independent structures, or two observables of one underlying boundary/current object?

## Oriented boundary field

For a binary configuration define the oriented boundary variable on each edge

- `j_i = +1` for `0 -> 1`,
- `j_i = -1` for `1 -> 0`,
- `j_i = 0` when the bit does not change.

Then two natural observables are

`D = sum_i |j_i|`

and

`Q = sum_i j_i`.

Thus:

- `D` is the unsigned number of local boundaries/domain walls;
- `Q` is the signed algebraic boundary/current.

They are not separate primitives. They are respectively the L1 norm and the signed sum of the same oriented boundary field.

## Closed binary cycle

On a closed cyclic binary word, every `0 -> 1` transition is eventually matched by a `1 -> 0` transition. Therefore

`Q = 0`

identically, while

`D = 2 N_+ = 2 N_-`

can be nonzero.

Hence MICRO's persistent `D` sectors survive even when the signed algebraic current vanishes.

## Open history

For an open binary sequence with endpoints `s_start,s_end in {0,1}`,

`Q = s_end - s_start`.

So the signed boundary reduces to an endpoint imbalance, matching the structural form seen earlier in the Wheeler open-path audit.

Because every nonzero local boundary contributes `+1` or `-1`, one also has

`|Q| <= D`

and, for unit boundary steps,

`D ≡ Q (mod 2)`.

Thus `D` measures total variation while `Q` measures net oriented transport.

## Periodic/lifted Wheeler history

For a periodic observer variable with a lift to an integer cover, the same algebraic idea generalizes: the signed sum of oriented crossings is the winding/degree `w`, while the unsigned crossing number counts total crossings.

Schematically,

`Q = w`,

`D_cross = total number of crossings`,

with

`|w| <= D_cross`

and parity compatibility for unit crossings.

Therefore the earlier Wheeler winding and the MICRO wall count fit the same pattern:

- algebraic sum -> topological/net sector;
- absolute sum -> total local boundary content.

## Growth

WHEELER-20 found that admissible zero-cost MICRO growth preserves `D` exactly. In the boundary-field language, growth may relocate the support of `j_i` but cannot create or annihilate an oriented `(+1,-1)` pair while remaining zero-cost.

For a closed binary cycle, `Q=0` remains automatic. Thus growth stability of `D` is naturally interpreted as preservation of the L1 norm of the boundary field, not as conservation of a separate charge.

## Interpretation

This is a useful unification:

`oriented boundary/current j`

produces

`Q = algebraic current / winding / endpoint index`

and

`D = unsigned boundary content / total variation`.

The two quantities are related but not equivalent. In particular, many configurations can have the same `Q` and different `D`, so `D` contains excitation/content information not captured by net charge-like winding.

## Verdict

- **PASS:** Wheeler signed current and MICRO domain-wall number are two observables of one common oriented boundary object.
- **PASS:** closed-cycle cancellation `Q=0` and open-endpoint imbalance follow directly.
- **PASS:** the inequalities and parity constraints follow for unit boundary steps.
- **CAUTION:** this is standard discrete boundary/current structure, not a derivation of electric charge or particle species.
- **OPEN:** whether an EHF effective energy can depend on both `Q` and `D` in a way that yields nontrivial stable excitations and sector-dependent gaps.

## Next probe

**WHEELER-22 — Boundary Energy / Mass-Gap Audit**

Use only the derived boundary field and existing admissibility structure. Ask whether a natural local energy depending on boundary content produces:

1. an energy floor above the `D=0` vacuum;
2. sector-dependent low-lying spectra at fixed `Q` or winding;
3. a gap that persists or scales cleanly under growth.

This is the point where the Wheeler branch can reconnect to the broader EHF mass-gap programme without claiming particle identification.