# EHF-AMP-HOL-BRIDGE-01 — Orientation, nine-point tails and the planar 1:2:3 law

**Date:** 2026-11-13 (AEST). **Status:** cross-programme comparison and falsifiable test plan; no new calculation or claimed correspondence between EHF reversal holonomy and QCD.

## Distinct mathematical structures

1. **Hamiltonian event orientation (HOL-06).** A reversible Z2 orientation lift over a multigraph of labelled LR2/LR3 reversal events. In the MICRO-only family, oriented deletion commutes with reversal actions; in OPW23, the canonical Pi support restriction can break admissibility after deletion.
2. **Nine-point Parke–Taylor tail.** Signed, support-restricted KK-relation maps from nine to eight orderings. Existing exact orientation-cut audit: full oriented source transmits the complete 15-dimensional target relation kernel in all 35 fibres; the representative support cut gives ranks 0,2,8,9,14,15. The 144 active source orderings fold in 72 pairs onto target orderings. The corresponding orientation-difference kernel is *not automatically* the orientation holonomy class of a reversal path.
3. **Collinear SU(3) 1:2:3 law.** On the equal-split tree-MHV real-projective-spinor locus, squared norms in singlet, symmetric octet and 27 channels are in ratio 1:2:3. The mathematical weights arise from d_R [(C_R−2C_A)/2]^2: 9:18:27. Generic real Lorentzian kinematics away from the real-spinor locus breaks this ratio. Exchanging the collinear gluons gives a separate Z2 selection rule classifying odd/even powers of the signed opening parameter as pair-colour antisymmetric/symmetric; it does not determine the three norm magnitudes.

## Highest-priority test: signed deletion versus involution

Build explicit signed linear operators on the actual ordered-word coefficient spaces:

- Source nine-point reversal \`J_9\` and target eight-point reversal \`J_8\`. Parke–Taylor denominator reflection has sign (−1)^n; include the differential and collision-residue sign convention separately.
- Signed deletion/collision residue \`D_9\`.
- Test \`D_9 J_9 = ± J_8 D_9\` under consistent choices of bases and charts. Do not assert a sign before computing. If neither identity holds, record counterexamples.
- Check whether the representative support cut is invariant under \`J_9\`. If not, compute its \`J_9\`-closure and recompute the ranks of lifted KK relations. Distinguish physical residue vanishing from the ability of zero-residue source orderings to cancel KK coordinates.
- Decompose retained relation and cancellation spaces by the relevant symmetry actions. The previously observed +− and −− exceptional sectors are characters of the *label swaps* (4 5) and (6 7); they are not automatically the Hamiltonian reversal sign character.
- A positive result must predict a nontrivial rank or exceptional dual functional from the equivariant map without inserting the desired dimensions. A negative result is that orientation is bookkeeping while support and shuffle constraints determine the ranks.

## Collinear comparison and rigorous null test

Bose exchange \`t -> −t\` sorts collinear expansion coefficients by colour-index symmetry. That is a defensible *shared method* with signed orientation transport: retain the involution and test whether projections respect it.

However, the Hamiltonian orientation cover alone supplies neither the SU(3) representation projectors nor the Hermitian norm and Casimir eigenvalues needed for 1:2:3. **Null test:** change to noncoplanar real Lorentzian kinematics, which retains ordering/exchange combinatorics but changes the norm ratio. Thus an explanation based on orientation alone is ruled out.

## Existing source evidence

- [Nine-point theorem, reconstruction and rank law](nine-point-tail/README.md)
- [Full oriented versus support-cut audit](nine-point-tail/followups/orientation.md)
- [Boundary signs and paired orientations](nine-point-tail/followups/boundary.md)
- [Label-swap character sectors](nine-point-tail/followups/shuffle-sectors.md)
- [Exceptional branch certificates](nine-point-tail/followups/branches.md)
- [Planar 1:2:3 theorem](collinear-colour/planar-theorem.md)
- [SU(N) dimension × Casimir law](collinear-colour/su-n-casimir-law.md)
- [Real-momentum counterexample](collinear-colour/lorentzian-counterexample.md)
- [Exchange-parity colour selection](collinear-colour/channel-orders.md)
- [Event-labelled Hamiltonian orientation](../../probes/reversals/event-groupoid-14/README.md)

**Recommendation:** run the signed-residue equivariance and support-closure test before proposing any correspondence of amplitude rank classes with Hamiltonian cocycle classes. This note records research motivation and a falsifiable comparison, not a new theorem.

## Follow-up: signed test completed (EHF-AMP-HOL-BRIDGE-02)

The [signed orientation audit](nine-point-tail/followups/signed-orientation-bridge.md) has now been run. It finds `D_9 R_9 = - R_8 D_9`, or `D_9 J_9 = J_8 D_9` with signed Parke–Taylor reflections, on all 40,320 anchored source words. Yet appending reflected copies of each allowed word **never enlarges any of the 35 restricted residue images**, whereas restoring the full original 576-word parity fibre gives rank 15 everywhere. Thus the rank law is not explained by simply restoring an orientation sheet. The real restriction concerns the available same-parity source words and their KK cancellation relations.

## Follow-up: two-word event selectors checked (EHF-AMP-HOL-BRIDGE-03)

The [six-fibre two-word audit](nine-point-tail/followups/rank14-event-pairs.md) computes all rank-restoring excluded-word pairs in the six rank-14 cuts, with counts 0,4,0,11,18,20. A combinatorial template learned from the maximal cut captures all 53 successes, but gives 67 false positives on six cuts; two fibres require at least three added words. This is a candidate selector, not a derived Hamiltonian event law or a prediction of the amplitude ranks without KK algebra.

## Follow-up: support complexity classified (EHF-AMP-HOL-BRIDGE-04)

The [minimal-triple repair audit](nine-point-tail/followups/rank14-minimal-triples.md) closes the two remaining rank-14 cases: both (2,5,7) and (3,5,7) have **minimum repair support 3**, with exact three-word witnesses and no smaller repairs. Across the six rank-14 cuts, minimum support is 3,2,3,2,2,2, despite identical one-dimensional target defects. This is a concrete finite reconstruction-distance effect, **not** a derivation of SU(3)'s planar 1:2:3 law.
