# EHF-AMP-FOUND-02A
## Growth–Factorisation Compatibility — corrected multi-parent formulation

**Status:** executable probe specification, v0.2  
**Layer:** move-independent Hamilton-cycle ordering / Parke–Taylor relation layer  
**Foundational move dependency:** none

## Correction prompted by the first 7→8 run

The first script assumed that deleting the new maximum label from one child fibre always lands in one parent fibre. That is true for the tested even→odd transitions, but false for odd→even growth.

At 7→8, a fixed n=8 child fibre can residue into two distinct n=7 parent fibres. This is the reverse-side form of the previously observed parity-alternating growth rule: the two anchor-growth branches split at odd→even transitions.

Therefore the fibre-local map

\[
D_m\vert_{R_m(G)}:R_m(G)\to R_n(F)
\]

is not always defined for one parent fibre \(F\). The correct map is initially global:

\[
D_m\vert_{R_m(G)}:R_m(G)\to \mathbb R^{X_n},
\]

with support possibly spread across several parent fibres.

## Corrected tests

### Q0. State-level section

Unchanged. Anchor-side insertion and matching deletion are exact inverses on individual orderings.

### Q1. Unchanged-coefficient lift

Unchanged. Test whether the oriented insertion of a parent local relation is itself a child local relation.

### Q2. Global residue validity

For each child fibre, construct the full signed max-label residue in the complete parent ordering space. Record:

- number of parent fibres reached;
- raw global residue rank;
- fresh global Parke–Taylor residual;
- residue kernel dimension.

Local blocks are retained only as diagnostics. When a residue scatters, the blocks need not be relations separately.

### Q3. Relation-valid residue span

Aggregate all global residue images. If their raw span is not entirely relational, intersect that span with the global parent Parke–Taylor relation space using fresh evaluations and a rank-truncated nullspace calculation.

Only this relation-valid subspace may be used for inheritance claims.

### Q4. Local inheritance after global gluing

Embed each parent local relation space in the complete parent ordering space and calculate

\[
R_n(F)\cap \mathcal I_{m\to n}^{\mathrm{valid}},
\]

where \(\mathcal I_{m\to n}^{\mathrm{valid}}\) is the relation-valid global residue span.

This allows components in other parent fibres to cancel before a fibre-local relation is reconstructed. It avoids the same conceptual error as projecting re-anchored residues fibre by fibre before gluing.

### Q5. Channel-new child directions

Use the kernel of the complete global residue map on each child relation space. “Channel-new” remains channel-relative, not an absolute birth claim.

## Exceptional n=8 direction

The exceptional AMP-18 direction is now tested against the complete global 8→7 max-label residue, which may have components in more than one n=7 parent fibre. Its individual parent-fibre blocks are reported, but the kernel verdict is based on the full global residue.

## Numerical safeguards

- rank-truncated SVD throughout;
- fresh Parke–Taylor validation;
- automatic filtering of a raw residue span to its genuine relation-valid subspace if needed;
- no wide-matrix QR membership test;
- no assumption of one child fibre mapping to one parent fibre;
- local inheritance tested only after global gluing.
