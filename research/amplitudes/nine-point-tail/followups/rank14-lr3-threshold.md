# EHF-AMP-HOL-BRIDGE-05 — A canonical LR3 event and a six-fibre support threshold

**Date:** 2026-11-13 (Australia/Brisbane).  
**Status:** exact nine-point finite classification and constructive support-inclusion proof; no general all-multiplicity result, independent QCD identity, or established EHF-holonomy-to-amplitude functor.  
**Research direction:** Barry Fensom; formalisation and verification assisted by ChatGPT.

## Question

Can **cyclic ordering data** identify which rank-14 nine-point Parke–Taylor tail cuts need two excluded source words to restore the missing target direction, and which require three, *without recalculating each fibre's complete KK quotient*?

## A single canonical three-position reversal

Work with the six rank-14 three-label blocks \`A=(a,5,c)\` with \`a ∈ {2,3,4}\` and \`c ∈ {7,8}\`. Let the complementary four labels be \`B=(b1<b2<b3<b4)\`. Nine-point words are anchored at 1 and alternate B in even slots and A∪{9} in odd slots. The original representative cut retains words with second label smaller than last.

Consider the **same source-ordering pattern** in every fibre:

    u = (1,b3,9,b4,a,b1,c,b2,5)
    v = (1,b4,9,b3,a,b1,c,b2,5).

The map u↔v reverses the consecutive three-vertex segment (b3,9,b4), exactly an **LR3** reversal. Label 9 stays in the middle, so **both words have zero individual collision residue**. Both are *excluded* from the existing support cut, since b3,b4 > 5; they are proposed *new source words*, not a move allowed within the original cut.

For every one of the six fibres the exact result is:

| A | Comparison counts κ=(#B<a,#B<5,#B<c) | Original rank | Rank after adding u,v | Minimum additional words |
|---|---|---:|---:|---:|
| (2,5,7) | (0,2,3) | 14 | 14 | **3** |
| (2,5,8) | (0,2,4) | 14 | **15** | 2 |
| (3,5,7) | (1,2,3) | 14 | 14 | **3** |
| (3,5,8) | (1,2,4) | 14 | **15** | 2 |
| (4,5,7) | (2,2,3) | 14 | **15** | 2 |
| (4,5,8) | (2,2,4) | 14 | **15** | 2 |

Thus **on these six specified cuts**:

    d_L(S_A) = 2   iff   κ_1 = 2 or κ_3 = 4
             = 3   otherwise.

Equivalently, d_L=2 iff a=4 or c=8. In all four d_L=2 cases, this *particular canonical LR3 pair* works; in both d_L=3 cases it fails. This is a proved, case-bounded finite classification, **not** an unexplained equality with the planar SU(3) 1:2:3 colour law.

## A proof with only three seed fibres and support inclusion

The ordering-cut monotonicity was already established in the [orientation-cut audit](orientation.md). For fixed abstract positions in A and B, describe a cut by \`κ_i = #{b∈B:b<A_i}\`. After order-preserving relabeling within A and B, one cut support embeds into another **iff** its comparison-count vector is coordinatewise smaller. The code exhaustively checks the equivalence on all 36 ordered pairs of the six cuts. The transported KK/residue algebra is equivariant under the same relabeling.

**Two positive seed certificates.**

- At A=(2,5,8), the canonical LR3 pair \`169723845\`, \`179623845\` supports an **exact rational 138-term source KK relation** whose signed residue leaves the original rank-14 image. Its support fits every larger cut with c=8, after ordered-block relabeling.
- At A=(4,5,7), the canonical LR3 pair \`169842735\`, \`189642735\` supports an **exact rational 42-term source KK relation** whose signed residue leaves the rank-14 image. Its support also fits A=(4,5,8).

Both certificates have been reconstructed and their **entire KK sum checked to vanish** after each transport; direct rank calculations independently give 15 for all covered cases. Their term counts refer to particular Gaussian-elimination certificates, **not minimal certificate sparsity**.

**One negative seed obstruction.** At A=(3,5,7), the [previous exact exhaustive quotient audit](rank14-event-pairs.md) finds **no repairing one- or two-word subsets at all**. The smaller A=(2,5,7) support embeds into A=(3,5,7), and both images have rank 14 and the same transported missing hyperplane. If a two-word repair existed in the smaller cut, transporting it would produce an at-most-two-word repair in the larger cut (some words might already be admitted there), a contradiction.

**Three-word upper bounds.** The explicit triples already exhibited by [BRIDGE-04](rank14-minimal-triples.md) restore rank 15 in both negative fibres; the probe checks those exact ranks again. Thus the minima really are 3.

Together these establish the entire table **using two positive seed KK certificates, one exact negative seed computation, support-inclusion monotonicity and the known triple witnesses**. The six results do not require six independent KK quotient classifications.

## What the event does and does not explain

**Positive:** the same LR3 move involving the *deleted label 9* identifies a constructive repairing pair whenever the ordering-comparison boundary permits a two-word repair. This is a precise connection between an EHF-style length reversal and the structure of support-restricted KK cancellation.

**Limitations:**
- The event is outside the original admissible source cut: the two words become admissible only when deliberately added.
- We have **not derived** the two seed KK certificates from a purely local reversal law. Thus the threshold has a rigorous **support-order plus algebraic seed proof**, not a fully rank-free derivation from the bare ordering geometry.
- The threshold is certified for only six rank-14, nine-point cuts. It has no asserted validity for other rank classes, deleted labels, or multiplicities.
- Both restored directions are eight-point KK relations whose Parke–Taylor combination vanishes; this work does not produce a new measurable scattering process.
- This result does not explain the colour-Casimir 1:2:3 norm proportions.

## Reproducibility

- [rank14_lr3_threshold_probe.py](rank14_lr3_threshold_probe.py) checks the rank before/after the canonical LR3 pair for every fibre, verifies all support-poset inclusions, constructs the two rational seed relations, transports and checks them, invokes the prior exhaustive negative-case oracle, and confirms the two minimal triples. Standard library only; imports existing [rank14_event_pairs.py](rank14_event_pairs.py) and [signed_orientation_bridge.py](signed_orientation_bridge.py).
- [verify_rank14_lr3_threshold.py](verify_rank14_lr3_threshold.py) independently implements the KK shuffle, collision deletion, and rational elimination. It checks all six ranks and both seed certificates without importing the main probe.
- [rank14-lr3-threshold-results.json](rank14-lr3-threshold-results.json) retains the six-rank table, both exact seed coefficient certificates and the transported-support checks.

Execute from this directory:

    python3 rank14_lr3_threshold_probe.py
    python3 verify_rank14_lr3_threshold.py

## Next falsifiable problem

Derive the seed certificate and obstruction *without KK elimination*, perhaps using an intrinsic event-labelled shuffle relation whose exact support footprint can be read from order comparisons. Test that rule on additional support cuts and at other multiplicities. A meaningful advance would predict the **two-versus-three support distance** or a successful repair from admissible ordering data and a short structural identity, without using a fitted template or precomputed quotient ranks.

**Bottom line:** a single LR3 event predicts the entire six-fibre minimum-repair classification, and the support inclusion poset reduces the proof to three seed checks. The broader reconstruction theorem remains open.
