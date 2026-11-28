# Two lifts of one nine-point tail residue

The rank-8 and rank-9 branches in Barry Fensom’s [nine-point tail](../README.md) both lift one additional eight-point relation modulo the common-cut image. The [side-by-side lifts](Lifts.md) give a 64-term and a 72-term nine-point relation with the same 24-term residue. Exact substitution verifies both source KK relations and the target relation. The coefficient of target word 12468753 is 2 in the witness, while that coordinate vanishes on the whole common-cut image.

Use the common block labels A = (4,5,8), B = (2,3,6,7) as in the branch audit. The three cuts have count profiles (1,1,2), (2,2,2) and (1,1,4). All three have the same active source words, which end in 9. First restrict a source relation to these 144 oriented coordinates. Then delete 9 and identify the two target orientations. Each of the 72 resulting coordinates is the sum of its two active preimage coordinates, since eight-point reflection has positive sign. Call the summation map F.

| Relation image | Common cut | Rank-8 branch | Rank-9 branch | Branch intersection |
| --- | ---: | ---: | ---: | ---: |
| Active coefficients before summation | 2 | 19 | 29 | 2 |
| Residue coefficients after summation | 2 | 8 | 9 | 3 |

Before summation, the intersection equals the common-cut active image by inclusion and equal dimension. Thus every pair of lifts of an extra shared residue must disagree in the active coordinates. In the exhibited witness the active difference consists of 24 opposite-sign pairs. The two lifts agree on all 72 pair sums.

## A quotient describing the extra direction

Write P and Q for the two active-coefficient images and K for the kernel of F. There is a natural isomorphism

```text
(F(P) ∩ F(Q)) / F(P ∩ Q)
    ≅ (K ∩ (P + Q)) / ((K ∩ P) + (K ∩ Q)).
```

To construct it, lift a shared residue to p in P and q in Q, and send it to the class of p − q. Changing either lift changes the difference by its branch kernel. Every element of K in P + Q is such a difference, and the difference can be removed by branch-kernel adjustments exactly when the residue has a common active lift.

Here the numerator on the right has dimension 46 − 14 = 32. The denominator has dimension (19 − 8) + (29 − 9) = 31 because F is injective on the two-dimensional common active image. This identifies the extra shared residue with a cancellation between the branches’ active coefficients, modulo cancellations available in either branch alone.

## Reproduce

Run `PYTHONPATH=.. python3 probe.py > shared-lifts-results.json` with standard-library Python. The script uses exact elimination, carries both lifts, and verifies the certificates against the source and target KK columns. The displayed lifts were selected by exact elimination. Their support sizes are descriptive. The identification is algebraic and leaves open a description via boundary geometry.
