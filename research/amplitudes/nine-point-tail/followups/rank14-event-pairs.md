# EHF-AMP-HOL-BRIDGE-03 — Can ordering events predict the rank-14 two-word repair?

**Date:** 2026-11-13 (Australia/Brisbane)  
**Status:** exact finite audit and an *exploratory, retrospectively fitted* ordering-template predictor. Not a new amplitude identity, an all-multiplicity law, or a demonstrated Hamiltonian-holonomy-to-amplitudes functor.  
**Research direction:** Barry Fensom; experiment and write-up assisted by ChatGPT.

## Research question

In our nine-point tail theorem, six source support cuts transmit a 14-dimensional subspace of the 15-dimensional eight-point KK relation kernel. The maximal cut A=(4,5,8) has a known minimal two-word repair using two zero-collision-residue nine-point orderings. Can a combinatorial ordering/event rule **identify** the repairing pairs without running the full Kleiss–Kuijf system afresh for every proposed pair?

## Exact two-word criterion (linear-algebra lemma)

Let S be the allowed source support, Q the nine-point KK coordinate map, D the signed collision-residue map and I=D(ker(Q|_S)) its transmitted image. Write W=span(Q(S)) and let qbar_u, qbar_v be the classes of Q(u),Q(v) in the quotient image space modulo W.

For added excluded words u,v with D(u)=D(v)=0:

- A new relation supported on S∪{u,v} can occur only when qbar_u and qbar_v are linearly dependent, or one is zero.
- Given a dependency α qbar_u+β qbar_v=0, choose a source combination s∈span(S) with Q(s)=-αQ(u)-βQ(v). Its residue D(s) modulo I is independent of the choice of s.
- The pair repairs the missing rank **if and only if** some such dependency has nonzero residue class in the target quotient by I. At rank 14 the target quotient is one-dimensional, tested by the already established dual functional L.

This is elementary quotient linear algebra, not a new theorem. The implementation first eliminates Q(S), groups excluded columns with proportional nonzero quotients, and evaluates their residual image classes. It does **not** repeat the full 432-column elimination for all 10,296 pairs. All 53 identified positive repairs were then independently checked by direct exact-rational KK/residue-image rank recomputation; 18 predicted negatives were also directly checked.

## Full six-fibre exact results

All source parity fibres have 576 nine-point words, all six cut images have rank 14, and all excluded words have zero collision residue. No single excluded word repairs any of the six cuts.

| A | Original cut words | Excluded words | Excluded pairs | Two-word repairs | Projectively dependent quotient pairs |
|---|---:|---:|---:|---:|---:|
| (2,5,7) | 324 | 252 | 31,626 | **0** | 135 |
| (2,5,8) | 360 | 216 | 23,220 | **4** | 76 |
| (3,5,7) | 360 | 216 | 23,220 | **0** | 522 |
| (3,5,8) | 396 | 180 | 16,110 | **11** | 108 |
| (4,5,7) | 396 | 180 | 16,110 | **18** | 108 |
| (4,5,8) | 432 | 144 | 10,296 | **20** | 176 |

**Important implication:** a one-dimensional missing target relation does **not** imply a two-word repair exists. The two cuts with zero repairs require **at least three added words**. Their exact minimum repair size has not been determined.

## An event/ordering-template candidate selector

Fitted **after inspecting the exact 20 successes at A=(4,5,8)**, so this is exploratory rather than an independent derivation.

Let A=(a,5,c), and let B={b1<b2<b3<b4} be its complement. Consider the following two eight-word templates, with independent binary choices of the order within each displayed two-label block:

- T3: (1, B_hi[first], 9, B_hi[second], A_lo[first], B_lo[first], c, B_lo[second], A_lo[second]).
- T5: (1, B_hi[first], A_lo[first], B_hi[second], 9, B_lo[first], c, B_lo[second], A_lo[second]).

Here A_lo={a,5}, B_lo={b1,b2}, and B_hi={b3,b4}.

On T3, connect two words precisely when the relative label permutation flips **an odd number** of the A_lo and B_hi pairs (the B_lo flip may be either). On T5, connect two words if one is obtained from the other by swapping only A_lo. This produces **20 candidate pairs** in every rank-14 fibre, without using a new KK calculation to generate them.

This is a label-swap / cyclic-ordering template, **not demonstrated to be a purely local LR2/LR3 reversal controller**; some candidate pairs differ by two label swaps.

| Fibre | True repairs | Candidates | True positives | False positives | False negatives |
|---|---:|---:|---:|---:|---:|
| (2,5,7) | 0 | 20 | 0 | 20 | 0 |
| (2,5,8) | 4 | 20 | 4 | 16 | 0 |
| (3,5,7) | 0 | 20 | 0 | 20 | 0 |
| (3,5,8) | 11 | 20 | 11 | 9 | 0 |
| (4,5,7) | 18 | 20 | 18 | 2 | 0 |
| (4,5,8) | 20 | 20 | 20 | 0 | 0 |
| **Total** | **53** | **120** | **53** | **67** | **0** |

The five smaller fibres are **transported structural holdouts**, not independent physical experiments. A perfectly recalled set is **not** a sufficient rule or a proof of an all-multiplicity mechanism.

### Controls and specificity

In the maximal reference fibre, permitting *any* single label swap within A or B generates **432** excluded pairs but catches only **12** of the 20 repairs: 12 true positives, 420 false positives and eight misses. Allowing odd-character swaps in the larger (4,5),(2,3),(6,7) label-swap group selects 288 pairs, covering all 20 but with 268 false positives. The tighter T3/T5 position templates eliminate those false positives **only in the fibre where they were fitted**.

All observed repair sets become nested under the stated order-preserving block transport and the partial order in the two varying block coordinates. This is consistent with the previously proved support-inclusion monotonicity, not independent evidence of physical conservation.

## Can precomputed relation certificates avoid repeated KK elimination?

For each of the 20 successes in the maximal fibre, the probe stores **one** exact KK source-relation certificate constructed by elimination. Transport that certificate by the order-preserving relabeling to a smaller fibre and ask, *without calculating new KK ranks*, whether all of its non-pair supporting words survive the smaller cut.

If yes, the transported relation is a **rigorous sufficient certificate** for a repair. This gives these transported counts:

| A | Actual repairs | Repairs certified by one fixed reference certificate per pair |
|---|---:|---:|
| (2,5,7) | 0 | 0 |
| (2,5,8) | 4 | 0 |
| (3,5,7) | 0 | 0 |
| (3,5,8) | 11 | 0 |
| (4,5,7) | 18 | **18** |
| (4,5,8) | 20 | **20** |

No false positive can occur for an actually verified transported relation. However these chosen certificates have large nonminimal support (40–170 words) and are far from necessary. The zero counts at A=(2,5,8) and (3,5,8) do **not** mean no transported/sparser certificates exist.

## Relation to EHF

A *zero-residue* ordering can still be indispensable because it enables a source relation that transmits a nonzero target relation. Thus the **space of admissible comparisons**, not merely the direct output of each individual ordering, controls what can be reconstructed after reduction.

This is a useful rigorous analogue of support-sensitive projection in EHF Hamiltonian growth, but it is **not** proof that a Hamiltonian reversal cocycle determines the Parke–Taylor rank-14 obstruction. The template uses labelled permutation characters and specified positions, not a new intrinsic Hamiltonian groupoid functor.

## Reproduction

Run from this folder:

    python3 rank14_event_pairs.py

Requires only Python 3 standard library and the existing [signed_orientation_bridge.py](signed_orientation_bridge.py) for exact KK/shuffle and residue definitions. The script:

1. Computes every two-word repair by quotient elimination for all six rank-14 fibres;
2. Verifies all 53 successes and 18 negatives by *separate full* rank calculations;
3. Tests the reference-fitted candidate templates on all five other fibres;
4. Builds 20 reference certificates and verifies which ones transport without new KK elimination;
5. Writes [rank14-event-pairs-results.json](rank14-event-pairs-results.json) with all 20 maximal-fibre repairing pairs.

## Next falsifiable step

Derive a **minimal-support** or intrinsic event relation predicting the correct subset of the 20 candidates for the other five fibres. An honest success requires *zero false positives* on newly chosen cuts without using their KK matrix as the selector. Another useful target is an exact lower bound and construction for the repair size at (2,5,7) and (3,5,7), where every pair fails.

## Related research

- [Nine-point tail theorem and independent reconstruction](../README.md)
- [Rank-14 dual and minimal maximal-fibre repair](rank14.md)
- [Signed reflection and residue audit](signed-orientation-bridge.md)
- [Order-dependent symmetry-sector cancellations](shuffle-sectors.md)
- [Local ordering features that already failed](ordering-geometry.md)
- [Orientation-event groupoid comparison](../../../../probes/reversals/event-groupoid-14/README.md)
