# EHF-AMP-FOUND-02A — Orientation and Vacuity Audit

Date: 2026-07-13

## Status

Two defects were identified in the v0.2 implementation.

### 1. Vacuous lift successes were counted as genuine

At the 7→8 transition, nine of the nineteen n=7 fibres have zero-dimensional local relation spaces. Each contributes two empty branch lifts. Empty matrices automatically return zero Parke–Taylor and containment residuals, so the reported 18/38 “successes” were exactly 18 vacuous cases.

Correct reporting must separate:

- genuine parent branches with relation dimension > 0;
- vacuous branches with relation dimension = 0.

The previous 18/38 headline is retired.

### 2. Reflection character was discarded during canonicalization

Canonical Hamilton-cycle representatives identify an ordering with its reversal. Parke–Taylor factors obey

PT(reverse(alpha)) = (-1)^n PT(alpha).

Therefore canonicalization must return both the canonical representative and the reflection character. The v0.2 code retained only the representative.

This affects:

- insertion lifts, where the child multiplicity determines the reflection character;
- deletion/residue maps, where canonicalization of the reduced parent ordering contributes the parent reflection character.

The omission is especially consequential for 8→7 deletion because the target multiplicity 7 is odd. It may explain the parity-localized failure in which the raw 7→8 residue span had a large Parke–Taylor residual before filtering.

## Consequences

The following v0.2 conclusions are not secure and must be recomputed:

- the 110 raw versus 40 relation-valid rank at 7→8;
- the 9/19 parent-inheritance count at 7→8;
- the exceptional relation’s delete-8 Parke–Taylor residual;
- the 0/15 inherited intersection for the exceptional fibre;
- the verdict RESIDUE_VISIBLE_NOT_NAIVELY_INHERITED.

The exact state-level insertion/deletion section remains valid.

The AMP-18 14/15 exceptional rank result is unaffected because it belongs to the separately reproduced n=9→8 calculation.

## Corrected implementation

Version 0.3:

- carries the Parke–Taylor reflection character through every canonicalization;
- separates collinear side sign from target canonicalization sign;
- excludes zero-dimensional parent relation spaces from lift success counts;
- reports genuine, failed and vacuous cases separately;
- requires a residue to pass the Parke–Taylor test before calling it relation-valid.

## Interpretation guardrail

The state-dependent factor

<1a> / (<1M><Ma>)

shows why unchanged-coefficient insertion is not expected to preserve relations. It rules out the naive diagonal copy lift except under a slot-graded decomposition. By itself it does not prove that every possible constant-coefficient map with nonlocal mixing is impossible.
