# WHEELER-15 — Lift Protection / Growth-Topology Audit

**Status: PARTIAL PASS — history-level protection exists; local lift protection fails**

## Question

Given a microscopic integer current `c` and the observer quotient

`r = c mod 3`, with `c = r + 3k`, can the lift index `k` become a genuinely protected quantity under existing EHF structures such as growth, topology, or observer memory?

The failure criterion is strict: if ordinary admissible moves can change `k` while all previously established conserved quantities remain intact, then `k` is not a physical sector label.

## Local-state audit

For a local site or boundary, write

`c_i = r_i + 3 k_i`.

The previously derived elementary reversal acts as a nearest-neighbour integer transfer

`(c_i,c_{i+1}) -> (c_i+1,c_{i+1}-1)`.

After reduction mod 3 this becomes the familiar residue transfer. Because of carry/wrap events, the individual lift indices can change even though the total microscopic current is conserved. Example:

`(c_i,c_{i+1}) = (2,0) -> (3,-1)`

so

`(r_i,r_{i+1}) = (2,0) -> (0,2)`

while

`(k_i,k_{i+1}) = (0,0) -> (1,-1)`.

Thus individual `k_i` values are not protected by the local reversal dynamics.

A neutral growth move that shifts lift by multiples of three,

`c_i -> c_i + 3a`,

preserves the same residue `r_i` but changes `k_i -> k_i + a`. Therefore local growth history can distinguish lifts, but unless the history itself is retained as part of the physical state, the lift is not protected.

## Observer-memory audit

An observer that stores the full path can distinguish two states with the same current residue but different growth/reversal histories. This is a valid record distinction, but it is not a state-topological invariant: erasing or coarse-graining the record removes the distinction.

Therefore observer memory yields **history distinguishability**, not automatic physical superselection.

## History-level topological lift

A stronger result appears when the quotient is treated as a covering map. The integer current is the lift of the cyclic observer variable:

`Z -> Z_3`.

Once an initial lift is fixed, a path in the quotient has a unique lifted path. For a closed observer-level history, the lifted endpoint need not equal its starting point; instead it can differ by a deck transformation:

`c_end = c_start + 3w`,

with integer `w`.

The integer `w` is a history-level winding/lift index. It is invariant under homotopies that do not cross a topological singularity or change the global sector.

This is the same structural mechanism already encountered in WHEELER-03: local folds/rearrangements can change apparent multiplicity while a global winding number remains fixed.

Hence:

- **local lift index `k_i`: NOT protected**;
- **stored growth history: distinguishable but record-dependent**;
- **global lifted-history winding `w`: topologically protected within a fixed homotopy sector**.

## Consequence for fractional-charge splitting

The result does not rescue the desired local `+2/3` versus `-1/3` species split. Those are different integer lifts of the same residue, but ordinary local dynamics can move between local lifts unless an additional independent obstruction is supplied.

What *is* naturally protected is a global history-level integer associated with how the trajectory winds through the quotient/covering structure.

Therefore EHF currently supports

`same local residue + different global history topology`

but not yet

`same local residue + two protected local particle species`.

## Verdict

**PARTIAL PASS.** The lift idea has genuine topological content at the level of complete histories, but the local lift index required to distinguish quark-like fractional species is not protected by the existing reversal/growth rules.

## Next probe

**WHEELER-16 — Global-to-Local Defect Audit**

Question: can a protected global lifted-history winding force a localized defect, endpoint, boundary class, or excitation whose local observer signature inherits a stable lift distinction? If no localization mechanism exists, this branch should stop short of particle-species claims.