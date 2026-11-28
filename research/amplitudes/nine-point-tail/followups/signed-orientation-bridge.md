# EHF-AMP-HOL-BRIDGE-02 — Signed reflection versus the nine-point tail cut

**Date:** 2026-11-13 (AEST)  
**Status:** exact computational audit (40,320 anchored nine-point words, all 35 parity fibres) and elementary sign/linear-dependence proof. **No new scattering-amplitude identity or demonstrated EHF-holonomy-to-QCD functor.**

## Research question

Does the natural reversible-orientation structure of EHF Hamiltonian transformations explain the six transmitted ranks 0,2,8,9,14,15 of the nine-point Parke–Taylor tail? In particular, does the rank defect come merely from discarding reflected source orderings?

## Operators and conventions

Let the cyclic word be anchored at label 1, with 2,...,9 freely permuted. Let R_n reverse the sequence after the anchor. Let D_9 be the **signed**, oriented coefficient of the collision z9−z1:

- If the nine-point word ends in 9, deleting 9 carries coefficient +1.
- If the nine-point word begins 1,9,..., deleting 9 carries coefficient −1.
- Otherwise its collision residue is 0.

At eight points, reflection of the Parke–Taylor factor has sign +1; at nine points, reflection has sign −1. Define the signed operators J_9=−R_9 and J_8=+R_8. The anchored eight-point target retains orientation until the last quotient step.

## Result 1 — the signed residue square commutes exactly

For **every one of the 8! = 40,320 anchored nine-point words**, the exact audit checks

    D_9 R_9 = − R_8 D_9
    D_9 J_9 = J_8 D_9.

It also independently checks the nine-point Kleiss–Kuijf expansion columns:

    KK_9(R_9 w) = − KK_9(w).

These are direct consequences of the reflection sign and the local collision residue, not new amplitude identities. All 40,320 cases passed.

## Result 2 — reflection closure does NOT restore missing ranks

For each 3-element block A⊂{2,...,8}, let B be its four-element complement. The **full parity fibre** F_A consists of 576 anchored oriented nine-point words with labels B in positions 2,4,6,8 and A∪{9} in positions 3,5,7,9. The **representative cut** S_A retains words in F_A satisfying second label < last label.

Reflection of a word in F_A swaps the two position classes, so **R_9(F_A) is disjoint from F_A**. It does not generate the omitted words of the same parity fibre.

Moreover, for each retained cut word w, adding R_9(w) contributes the **negative of its KK column and the negative of its folded residue column**. Therefore the joint (KK,residue) column span is unchanged, so the image of the KK relation kernel under residue cannot increase.

This is a general linear-algebra proof; the exact audit also independently recomputes the relevant ranks for all 35 fibres:

| Cut rank | Number of fibres | Rank after adding all reflected copies | Rank for full parity fibre |
|---:|---:|---:|---:|
| 0 | 4 | 0 | 15 |
| 2 | 3 | 2 | 15 |
| 8 | 3 | 8 | 15 |
| 9 | 6 | 9 | 15 |
| 14 | 6 | 14 | 15 |
| 15 | 13 | 15 | 15 |

Examples:

| Block A | Source cut size | Cut rank | Cut + reflections rank | Full parity rank |
|---|---:|---:|---:|---:|
| {2,3,4} | 144 | 0 | 0 | 15 |
| {4,5,8} | 432 | 14 | 14 | 15 |
| {6,7,8} | 576 | 15 | 15 | 15 |

**Interpretation:** the missing rank is not simply an omitted orientation sheet. It arises because the support cut excludes distinct nine-point orderings that supply *new KK-cancellation routes*, even though excluded words can have zero residue individually.

## Result 3 — the rank-14 dual obstruction is repaired by two zero-residue words

For A={4,5,8} add the previously exhibited excluded words

    u = (1,6,4,7,9,2,8,3,5)
    v = (1,6,5,7,9,2,8,3,4)

to the 432-word cut. Both have zero individual collision residue.

| Added words | Nine-point source KK rank | Number of source relations | Eight-point residue image rank |
|---|---:|---:|---:|
| neither | 375 | 57 | 14 |
| u only | 376 | 57 | 14 |
| v only | 376 | 57 | 14 |
| **both** | 376 | 58 | **15** |

These are independent exact-rational computations reproducing [the already established two-word repair](rank14.md). Adding all 432 reversed cut words instead leaves the residue rank 14, merely adding linearly dependent signed columns.

## Consequence for Hamiltonian holonomy

The new HOL-06 **orientation transport** and the nine-point residue **reflection sign** are compatible with the idea of retaining oriented objects and correct event signs, but they are **not the same invariant**. The event-groupoid orientation double cover does not currently predict the 0/2/8/9/14/15 rank profile. Neither does it explain the (+,−) and (−,−) label-swap symmetry sectors, which originate from distinct permutations acting on the KK relation-support system.

A useful next target is a **support-aware oriented event category**, in which a transformation may change the allowed word support. Construct a specific map from those event labels to KK columns and collision-residue vectors, then determine whether the two-word repair (or the shared rank-14 dual functional) follows from a short closed event relation. Without such a map, calling the cancellation 'holonomy' is only analogy.

## Reproduction

Run the standard-library Python program:

    python3 signed_orientation_bridge.py

The script uses no saved EHF matrices, independently evaluates every anchored word for the signed reflection and KK identity, computes all 35 cut and reflection-closure residue-image ranks plus all 35 full-fibre ranks by exact rational elimination, and reproduces the two-word repair. It writes [signed-orientation-bridge-results.json](signed-orientation-bridge-results.json) beside the script.

## Sources within EHF

- [Nine-point theorem and independent reconstruction](../README.md)
- [Full oriented parity fibre versus representative cut](orientation.md)
- [Two-sided collision-boundary sign convention](boundary.md)
- [Rank-14 dual and minimal two-word repair](rank14.md)
- [Sector-selection and shuffle constraints](shuffle-sectors.md)
- [HOL-06 event-labelled orientation transport](../../../../probes/reversals/event-groupoid-14/README.md)
- [Initial cross-programme hypothesis](../../ordering-orientation-bridge-01.md)

**Bottom line:** signs commute; support restrictions break the ability to lift relations; adding reflected duplicates is not the same as restoring the missing same-parity orderings. That is a concrete negative result for the simplest Hamiltonian-holonomy explanation, and it narrows the next test.
