# Shuffle certificates for the two branches of the nine-point tail

This note follows Barry Fensom’s [nine-point theorem draft v1.5](../theorem-v1.5.md) and the explicit rank-14 obstruction. All ranks and certificates here use exact rational arithmetic.

Use the common reference labels A = (4,5,8), B = (2,3,6,7), with anchor 1 and deleted mark 9. For a target ordering w, write r[w] for its formal Parke–Taylor coefficient. Write L for the shared rank-14 obstruction, r[16528347] + r[16538247], with each digit specifying a label.

## Two families of liftability conditions

Restrict the following functionals to the 15-dimensional target KK kernel. Each column, together with L, is a complete independent set of equations for the corresponding image.

| Rank 8 | Rank 9 |
| --- | --- |
| r[16835247] | r[13528746] + r[13578246] |
| r[16538247] | r[13528647] + r[13568247] |
| r[16825347] | r[13864257] + r[16834257] |
| r[16834257] | r[13874256] + r[16524387] |
| r[16438257] | r[13524687] + r[13524786] |
| r[16824357] | |

The signs of the rank-9 certificates in the JSON are the negatives of the displayed equations. Each of the six extra rank-8 conditions has a certificate using two KK rows. These rows are precisely the two target orientations with the initial 1 removed, in the nine-point chart whose endpoints are 1 and 9. Each of the five extra rank-9 conditions has a six-row certificate. The shared condition also has a six-row certificate.

For example, the rank-8 equation r[16835247] = 0 is certified by the sum of KK rows 6835247 and 7425386. On the rank-8 source this sum reads exactly the coefficient sent to the target ordering 16835247. The JSON lists every row, sign, and excluded word where each dual has a nonzero evaluation. The selected rank-8 duals each detect 14 excluded words, of which 4 or 5 are allowed on the opposite branch. The selected rank-9 duals each detect 12 excluded words, of which 3 or 6 are allowed on the opposite branch. The shared dual detects no excluded word allowed on either branch. These are counts for the displayed certificates.

The verification checks the dual identity on every source column. It then checks independence on the full target kernel and confirms that each branch-specific functional is nonzero on the other image. Since the two images sum to rank 14, the line spanned by L is the complete common obstruction.

## How the source cuts combine

Describe a cut by the three counts of B labels before the three A labels in their common order, with 9 maximal. After block transport, every active word is retained. An inactive word is retained exactly when its second label lies among the permitted initial B labels for its last label.

| Image rank | Maximal representative block before transport | Counts | Source words | Source KK rank |
| --- | --- | --- | ---: | ---: |
| 2 | {3,4,6} | (1,1,2) | 288 | 286 |
| 8 | {4,5,6} | (2,2,2) | 360 | 331 |
| 9 | {3,4,8} | (1,1,4) | 360 | 331 |
| 14 | {4,5,8} | (2,2,4) | 432 | 375 |

The two branch cuts have disjoint sets of additions to the common cut. Their union is the rank-14 cut and their intersection is the rank-2 cut. For the six rank-14, six rank-9, three rank-8 and three rank-2 fibres, the verifier checks that the transported image matches its maximal representative.

Two distinct one-dimensional effects appear. At source level, the union kernel has dimension 57. The sum of the branch kernels has dimension 56, since the branch kernels both have dimension 29 and intersect in the two-dimensional common-cut kernel. There is therefore one additional source relation modulo the branch kernels. Its residue class modulo the sum of the branch images is zero, because the branch images already span the rank-14 image.

At target level, the two branch images intersect in dimension 3. The common cut has image dimension 2, so one further residue direction is attainable separately through either branch. This statement concerns the quotient by the common-cut image. It identifies a separate effect from the extra source relation just described.

## Reproduce

Run `PYTHONPATH=.. python3 branches.py > branches-results.json` with standard-library Python. The JSON contains every functional, every KK certificate, and the excluded words detected by each one. Sparsity is reported for these explicit choices. Minimal certificate support, an analytic classification beyond this finite case, and the geometric interpretation remain open.
