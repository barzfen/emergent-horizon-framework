# An explicit obstruction in the rank-14 Parke–Taylor tail

This follow-up uses the conventions of Barry Fensom’s [nine-point theorem draft v1.5](../theorem-v1.5.md). The rank-14 channels have selected block A = {a,5,c}, where a is 2, 3 or 4 and c is 7 or 8. The eight-point target kernel has dimension 15.

## The obstruction

Work first at A = {4,5,8}, with complementary block B = {2,3,6,7}. For a formal eight-point coefficient vector r let

```text
L(r) = r[1,6,5,2,8,3,4,7] + r[1,6,5,3,8,2,4,7].
```

On the target relation space, the rank-14 image is exactly the hyperplane L = 0. The same formula holds after order-preserving transport within the two blocks from each of the other five rank-14 channels to this one. On the target relation space, L transforms with signs (−,+,−) under (4 5), (2 3), (6 7), respectively. These swaps correspond to (2 3), (5 6), (7 8) in the draft’s reference fibre.

## Six KK rows certify the obstruction

Let Q be the nine-point Kleiss–Kuijf map with endpoints 1 and 9, and D the signed collision deletion of 9 at 1. Define Lambda on Q coordinates by the following six terms. Each row lists only the interior word.

| KK coordinate | Weight |
| --- | ---: |
| 7 4 8 2 3 5 6 | −1 |
| 7 4 2 8 3 5 6 | +1 |
| 7 4 3 8 2 5 6 | +1 |
| 6 5 8 2 3 4 7 | −1 |
| 6 5 2 8 3 4 7 | +1 |
| 6 5 3 8 2 4 7 | +1 |

On the cut source, Lambda Q = L D. One can check this by inverse shuffling: for each listed interior word, select any subsequence alpha and take beta to be the reverse of its complementary subsequence. The source word (1,alpha,9,beta) contributes the row weight times (−1) to the power |beta|. Keep the words with B in even positions and add repeated contributions. Of the 16 nonzero totals, four are active words, two above each of the two target words in L. The other twelve are inactive words excluded by the second-label < last-label cut. All sixteen totals are +1. Hence a permitted lift in the KK kernel must have L D = 0.

For the five smaller interleavings, order-preserving block transport sends each retained source word into the maximal cut A = {4,5,8}. The same identity follows there by restriction. Exact rank checks and the witness below show the hyperplane is attained in all six cases.

## A minimal repair in the maximal cut

Add these two excluded words to the A = {4,5,8} source:

```text
u = (1,6,4,7,9,2,8,3,5)
v = (1,6,5,7,9,2,8,3,4)
```

Both have zero collision residue. Their KK columns have identical nonzero classes modulo the span of the retained source columns. Thus Q(v) − Q(u) can be cancelled using retained words. Since Lambda Q(u) = 1 and Lambda Q(v) = 0, the resulting source relation with coefficients −1 on u and +1 on v has L D = 1. The augmented image has rank 15.

One added word cannot suffice in this fibre. If its Lambda value is zero, the dual obstruction still holds. For each of the twelve excluded words with Lambda value +1, exact reduction shows that its KK column is outside the retained span. Such a word cannot have a nonzero coefficient in a relation after adding it alone. The minimum number of added words is therefore two for this cut.

## Reproduce

Run `PYTHONPATH=.. python3 certificate.py > rank14-results.json`. The standard-library script checks the inverse-shuffle calculation against the direct KK columns, transports the identity across all six channels, verifies the character on the full target kernel, and emits a rational source lift and its eight-point witness. It verifies the lift by substitution into the original columns. The supporting audit and reconstruction modules are included. The functional uses two target coefficients and six KK rows. Their minimum possible support has not been determined. The certificate addresses this finite ordering restriction. A geometric characterization of such restrictions remains open.
