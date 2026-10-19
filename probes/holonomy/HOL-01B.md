# EHF-HOL-01B — Rotation-Quotient Frame Audit

**Status: NEGATIVE / REPRESENTATION-DEPENDENT — the WHEELER-59 rotation quotient does not yet supply intrinsic holonomy.**

## Question

Does the existing WHEELER-59 rotation quotient provide the canonical local-frame transport that HOL-01 requires?

This is the second canonical-transport gate after the WHEELER-09 cyclic-residue audit.

## Existing structure used

No new dynamics or physics are introduced. WHEELER-59 already defines

- rooted cyclic binary words `w`;
- the rotation orbit `rotations(w)`;
- a canonical representative `canonical(w) = min(rotations(w))`;
- growth transitions inherited from the exact WHEELER-58 event law;
- projection of fine histories to rotation classes.

The existing audit explicitly quotients rotations only, not reflections or bit complements, and verifies exact path-law projection for the event kernel.

## Candidate transported datum

The tempting local datum is the **root offset**: the cyclic displacement required to rotate a rooted word into its canonical representative.

For a generic asymmetric word with a unique canonical rotation, this offset is well defined. A transition `w -> v` could then appear to induce a frame change by comparing the canonicalizing offsets of `w` and `v`.

However, this does not pass the intrinsic-transport test.

## Obstruction 1 — the root is quotient redundancy

WHEELER-59 deliberately identifies all rotations of a word. Therefore the root offset is precisely the information removed by the quotient. A nonzero accumulated root shift can distinguish rooted representatives while leaving the physical/quotient state unchanged.

Consequently a loop defect measured only by root offset is representation-dependent unless some pre-existing EHF observable makes the root physically meaningful. WHEELER-59 contains no such observable.

This places raw root-offset holonomy in HOL-01B, not HOL-01C.

## Obstruction 2 — canonicalization is not a globally unique frame

For rotationally symmetric words, more than one rotation gives the same canonical representative. Thus `canonical(w)` is a unique quotient state but the **rotation taking w to canonical(w)** need not be unique.

This is not a numerical problem; it is stabilizer symmetry of the cyclic word. Any attempt to transport a unique orientation through such a state requires an additional tie-breaking convention.

A lexicographic tie break would manufacture a gauge choice, not reveal an intrinsic EHF connection.

## Obstruction 3 — growth changes the cyclic set

A WHEELER event inserts a new bit, changing length `n -> n+1`. Although the event records an insertion slot in the rooted description, WHEELER-59 projects the resulting state to a rotation orbit. There is no existing quotient-level rule that identifies every old cyclic position with a unique position in the new orbit independently of root choice.

Defining such an identification would amount to adding the connection that HOL-01 is supposed to test for.

## Exact structural check

The existing source code establishes the relevant facts:

1. `rotations(w)` generates the rotation orbit.
2. `canonical(w)` chooses the lexicographically minimal rotated word.
3. `quotient_row` projects every transition target through `canonical`.
4. `history_check` verifies that projected fine histories reproduce the coarse rotation-class history law.
5. WHEELER-59 states that the quotient is rotations only and records root-dependence diagnostics for alternative kernels.

Thus the quotient is mathematically coherent, but coherence of the quotient does not provide a canonical connection between local orientations.

## Classification

For the native WHEELER-59 structure:

- quotient-state transport around a closed quotient loop is trivial at the state level;
- rooted orientation can accumulate apparent shifts, but root is gauge-like redundancy removed by the quotient;
- symmetric states make canonical orientation nonunique;
- a unique cross-growth orientation map would require a new convention.

Therefore the candidate is classified

**HOL-01B — nontrivial orientation defects, if measured in rooted representatives, are representation-dependent and are not intrinsic holonomy.**

No claim of curvature follows.

## What this teaches us

The first two gates now distinguish three notions that must not be conflated:

- a cycle in state space;
- a quotient/gauge redundancy;
- an intrinsic transport connection.

EHF has the first two in the tested Wheeler sectors. HOL-01 requires the third.

## Next candidate

Move to an EHF sector in which the observer/comparison structure itself retains relational information across histories. The recursion/observer series is a stronger candidate than forcing a frame onto the Wheeler quotient.

The selection criterion remains strict: identify an already-defined datum attached to an observer/local description and an already-defined comparison map between neighbouring descriptions. If that pair is absent, report `UNDEFINED` again rather than inventing it.
