# EHF-CBB-BIN-10 — Odd-order marked-gap quotient: n=5,7,9

Date: 2026-11-10. Status: exhaustive finite enumeration and exact quotient-matrix algebra. No physics inference.

## General construction
For n=2m+1, fix a set R of m marked vertex labels in an undirected labelled Hamiltonian cycle C. Record the m positive gaps between consecutive marked vertices around C. Identify gap words under cyclic rotation and reversal (dihedral equivalence). An LR3 move swaps the endpoints of three consecutive vertices. The resulting multiset of gap-word transitions depends only on the dihedral gap word: the marked/unmarked cyclic binary necklace determines the effect of every position swap, and the label identities within marked/unmarked classes do not matter. Consequently the gap-word partition is equitable for unrestricted LR3 at every odd n (indeed the argument applies to arbitrary n and fixed |R|). This is an exact general reduction, not merely a numerical pattern.

For n=2m+1, the n+1 even-order LR3 sector containing the newly inserted vertex is determined by a marked m-subset R of old vertices. Insertion reaches it iff R is an independent m-set in C; there are n such sets on an odd n-cycle, and exactly one insertion slot for each. The observation column is therefore T(C,R)=1/n for the independent gap pattern (2,...,2,3), and 0 otherwise.

## Exhaustive tests
| n | labelled undirected cycles | dihedral gap classes | equitable? |
|---|---:|---:|---|
| 5 | 12 | 2 | yes |
| 7 | 360 | 4 | yes |
| 9 | 20160 | 10 | yes |

At n=9, sorting gap lengths instead of retaining their dihedral cyclic order gives only six classes and is **not** equitable; an explicit counterexample occurs for sorted gaps (1,1,2,5). Dihedral gap words fix the problem.

## Exact quotient spectra
The integer LR3 neighbour-count matrix M has row sum n. Its characteristic polynomial:
- n=5: (x-5)(x-1).
- n=7: (x-7)(x-5)(x-2)(x-1).
- n=9: (x-9)(x-5)(x-4)(x^2-10x+17)(x^2-6x-3)(x^3-10x^2+27x-15).

The independent-set observation at n=5 excites eigenvalues 5 and 1. At n=7 it excites 7,5,2 (not 1), as established in BIN-09. At n=9 its minimal annihilating polynomial under M is
(x-9)(x-4)(x^2-10x+17)(x^2-6x-3)(x^3-10x^2+27x-15).
Thus **all quotient eigenvalues except 5** occur in the n=9 observation. In particular the special two-decay-mode simplification at n=7 does not persist unchanged to n=9. The n=9 observation has eight nonstationary eigenvalues (counting algebraic roots), compared with two at n=7. This describes the n=9 observation map before composing with a preceding growth channel; additional source-side cancellations remain possible.

## Reproduction sketch
Generate canonical cycles (rotate smallest label to first, choose lexicographically smaller traversal). For each cycle classify the fixed marked set R by its positive cyclic gap word, canonicalized under rotations and reversal. Generate all n LR3 endpoint swaps and count target gap classes. Assert row-count vector is constant across all cycles in each class. Construct exact integer M, factor its characteristic polynomial in sympy. Let e be the indicator of the unique independent pattern (2,...,2,3). Compute the first linear dependence of e,Me,M^2e,... over rationals to obtain the observation's minimal polynomial.

## Interpretation
The **general principle** is a reduction to marked-gap necklaces and an independent-set observation. The **special 5/7 and 2/7 mode selection** is a low-order coincidence/special case, not a universal two-mode law. The number of quotient classes grows, and additional observable modes emerge. The earlier 1:2:3 collinear-colour law has not been checked for equivalence; avoid conflating the results.

## Next
Prove explicit formulae for the number of dihedral gap classes via binary bracelets with fixed density, and derive the LR3 quotient operator algebraically for general m. Analyze the composed growth–mixing–sector channel at n=9 (8->9->10) to identify which n=9 modes survive source projection; this is computationally larger than the quotient itself.
