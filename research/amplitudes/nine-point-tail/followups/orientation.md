# Nine-point Parke–Taylor tail filtration and the orientation cut

Follow-up to Barry Fensom’s [nine-point draft v1.5](../theorem-v1.5.md) · 5 November 2026

## Exact comparison

Fix anchor 1, deleted label 9, a three-element block A of labels 2 through 8, and its four-element complement B. The full oriented source consists of the 576 words starting at 1 with labels from B at even positions and labels from A plus 9 at the remaining odd positions. At odd multiplicity, anchored reversal exchanges the two position classes on the non-anchor labels. Consequently, these 576 words represent distinct unoriented cycles within this source. The draft first chooses the representative satisfying second label < last label, then selects its parity pattern. Relative to the full oriented fibre, this imposes an actual restriction on support.

The same 144 source words contribute to the collision residue in both calculations. They all end in 9. All removed words have zero residue individually. They can still participate in relations and change which target relations lift.

| Source support | Exact residue image ranks across the 35 fibres |
| --- | --- |
| Draft’s representative cut | 0 in 4 fibres, 2 in 3, 8 in 3, 9 in 6, 14 in 6, 15 in 13 |
| Full oriented parity fibre | 15 in all 35 fibres |

The full images equal the entire eight-point local relation kernel in every fibre. For example, at A = {2,3,4} the cut keeps precisely the 144 active words, so the cut image has rank zero. The full oriented source restores the entire 15-dimensional kernel.

The audit enumerates both source supports, computes Kleiss–Kuijf coordinates, carries the deletion columns through exact rational elimination, and checks every basis row of the full image against the target KK matrix. It also checks containment of the cut image. Relabelling within the two ordered blocks is unnecessary for the comparison within each fibre. More generally, relabelling A and B between fibres while fixing 1 and 9 carries the full oriented residue diagram to itself up to the induced isomorphism. Thus one surjective full-fibre calculation already implies the other 34.

## A general monotonicity lemma

Fix abstract labels for the two blocks, with the internal order of each block fixed. Vary the interleaving of the blocks in the label order, with the deleted label still maximal. Write C for the set of pairs (b,a) with b in B, a in A and b < a. All active words survive. An inactive word survives exactly when the pair made by its second and last labels belongs to C. Thus inclusion C ⊆ C′ gives inclusion of the cut source spaces after transporting to the common labels. The KK kernel and residue image respect this inclusion. In particular, swapping adjacent labels from A,B to B,A enlarges the image or leaves it fixed. This argument applies at every odd multiplicity with the analogous parity rule.

There is also an exact description of the lifting condition. Split the source into active coordinates X and retained inactive coordinates Y. In the KK basis with endpoints 1 and 9, each active word is a distinct basis column. Let E = Q(X) and S = Q(Y), where Q is the KK coordinate map. Then the residue image is D applied to the inverse of Q restricted to X, evaluated on E ∩ S. Indeed, an active coefficient vector can occur in a relation exactly when its KK vector can be cancelled by retained inactive words. The missing target directions therefore measure restrictions on cancellation before taking the residue. The monotonicity argument gives inclusions, while the exact dimensions and coincidences among incomparable cuts still need a structural derivation.

## Boundary geometry

Use a local chart on the worldsheet moduli space with three retained marks fixed, t = z9 − z1 as collision coordinate, and order the top-form differential with dt first. All orderings share the same gauge factor from the three fixed marks. If the cyclic word ends in 9, its denominator contains z9 − z1. Taking the coefficient of dt/t removes this factor and replaces the surviving neighbour’s z9 by z1. If 9 immediately follows 1, the pole factor is z1 − z9 and the residue has the opposite sign. If 9 is away from 1 in the cyclic order, the form is regular along the generic collision. This identifies D with the coefficient map of the logarithmic residue on the divisor for the split {1,9} | {2,…,8}. The divisor has factors M̄₀,₃ and M̄₀,₈, with the node on the eight-mark factor relabelled 1.

Lam’s [*Moduli spaces in positive geometry*](https://arxiv.org/abs/2405.17332), canonical form and boundary residue sections, supplies the established geometric operation. Damgaard, Ferro, Łukowski and Moerman’s [*Kleiss–Kuijf Relations from Momentum Amplituhedron Geometry*](https://arxiv.org/abs/2103.13908) is related prior work on obtaining KK identities geometrically. Here the question is which relations on a fixed collision divisor admit lifts with prescribed ordering support. The residue formula is standard. The finite support comparison and the monotonicity lemma are the results of this follow-up. Literature novelty and a geometric interpretation of the ordered support cut remain open.

A concrete next problem is to explain the last missing direction when the image has rank 14. The existing reconstruction places the one-dimensional quotient in the (−,+,−) character for the swaps (2 3), (5 6), (7 8). Can a single shuffle or boundary functional explain why this direction fails to lift through the cut?

## Reproduce

Run `PYTHONPATH=.. python3 audit.py > orientation-results.json` from the followups directory. The parent directory’s `reconstruct.py` is the repository implementation of the KK shuffle and exact elimination helpers. The audit does not read saved matrices, certificates or ranks beyond the stated cut-rank law used as a cross-check.
