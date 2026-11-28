# Two cancellation directions at the nine-point collision boundary

This follows the explicit pair of lifts in Barry Fensom’s [nine-point tail](../README.md). We work in the common reference labels A = (4,5,8), B = (2,3,6,7). All computations are exact over the rationals.

## Local chamber interpretation

Consider the collision divisor for the split {1,9} | {2,…,8} in the real compactified moduli space of marked genus-zero curves. Fix a generic boundary point and a local affine coordinate with t = z9 − z1. A boundary cyclic order with label 1 at the node has two adjacent nine-point chambers. The inserted label 9 comes immediately before 1 in one chamber and immediately after 1 in the other, when the same boundary orientation is used. Locally the chambers meet the divisor from opposite signs of t.

The oriented source convention uses a word ending in 9 for both preimages. To put the second insertion in that form, reverse its cyclic word. Reversal multiplies the nine-point Parke–Taylor factor by −1 and the eight-point factor by +1. In a fixed differential convention with dt first, the two pole factors z9 − z1 and z1 − z9 carry opposite residue signs prior to this change of representatives. The source reversal supplies another minus sign. Consequently both active columns map to the same target coefficient with positive sign in the chosen basis. The kernel of this local map is spanned by the difference of the two preimages for each target word.

This interprets the summation map as incidence across the two sides of a boundary chamber. The standard background for this description is the real chamber and polygon construction of [Brown, Carr and Schneps](https://arxiv.org/abs/0910.0122), together with the boundary residue description in [Lam’s moduli-space notes](https://arxiv.org/abs/2405.17332). The rank statements below refer to formal coefficients of Parke–Taylor relations with the specified support cuts. The shared residue witness evaluates to zero as a rational differential form.

## Two cancellation directions

Let P and Q be the rank-8 and rank-9 branch images in the 144 active coefficients before summation. Let U be the corresponding active image for the union cut. Write K for the kernel of summation and C for (K ∩ P) + (K ∩ Q).

| Active coefficient subspace | Dimension |
| --- | ---: |
| P + Q | 46 |
| U | 47 |
| C | 31 |
| K ∩ (P + Q) | 32 |
| K ∩ U | 33 |

The adjacent quotients in C ⊂ K ∩ (P + Q) ⊂ K ∩ U are both lines. The first measures an extra shared residue obtainable separately in the two branches. Its representative is the active difference of the previously exhibited lifts, projected onto the character below. The second measures a cancellation obtainable with the union cut that lies outside the active sum of the two branches. Since the union and branch sum have the same folded image, this second line accounts for the extra active direction that vanishes after passing to the quotient by the folded branch sum.

The formal label swaps (4 5) and (6 7) preserve all source cuts used here. The exact calculation produces pure character generators:

| Cancellation class | (4 5) | (6 7) |
| --- | --- | --- |
| Difference of separate lifts | +1 | −1 |
| Available only in the union modulo the branch sum | −1 | −1 |

Thus (K ∩ U)/C splits as the sum of these two distinct characters. The signs concern permutations of formal cycle labels. The geometric local incidence describes how the coefficients cancel. The one-dimensional counts and the character assignments come from exact linear algebra with the ordering cuts. An independent geometric derivation of those counts remains open.

## Reproduce

Run `PYTHONPATH=.. python3 boundary.py > boundary-results.json`. The script reconstructs the active images, computes the nested cancellation spaces, verifies their dimensions, and checks both projected generators under the two swaps and under the residue map. It uses standard-library Python and the supplied exact reconstruction code.
