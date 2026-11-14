# EHF-CBB-CROSS-48 — Two reversal paths and an interference control

**Date** 2026-11-13 (Australia/Brisbane)  
**Status** Exact path census, Clifford lift calculation and supplied coherent control.

## Two paths to the same labelled cycle

Use the prepared 21-vertex cycle of [CROSS-46](CROSS-46-local-clock.md). At fixed size permit the original indexed LR3 rule when testing paths. Let P reverse at sign-window start 2 and Q at start 17. Each operation swaps the vertices in the second and fourth positions relative to its sign-window start, at start+1 and start+3. The sign supports are disjoint. The paths P then Q and Q then P are both legal, have distinct intermediate words and agree at the endpoint even when every vertex label is retained.

The witness survives insertion at any of the eleven intervening edges, from 6 through 16 in the original indexing. The tail operation shifts to start 18 in each child. This test inserts before either reversal and compares the two paths within the grown square.

From each of the 5,844 prepared words through three insertions in CROSS-47, enumerate pairs of legal two-reversal paths with different first steps and a common endpoint distinct from the source. Subsequent moves use all LR3 starts. Count each unordered route pair once per source.

| Vertices | Route pairs |
|---|---:|
| 21 | 24 |
| 22 | 1,215 |
| 23 | 7,608 |
| 24 | 29,776 |

All 38,623 pairs swap the order of two moves with disjoint sign supports. In fact, LR3 flips precisely its four-sign support. Two paths with the same source and endpoint have equal symmetric differences of their supports. For a cyclic ring of odd size, the length-four window masks over the binary field have only the relation summing all masks to zero. For the even sizes here the kernel is 4-periodic with even parity across four consecutive positions, so any nonzero relation has weight at least 10. In either case there is no relation involving at most four distinct windows. This follows by subtracting adjacent coordinates of a vanishing sum of masks to obtain c_i=c_(i-4) for the coefficients c_i. Thus the two routes use the same pair of windows in opposite orders. Distinct LR3 windows that overlap cannot both be eligible and remain eligible after one flips. Any overlap makes the first flip change a nonempty proper subset of the signs in the second window. The second window can then match neither its original eligible pattern nor the full complement, the only other eligible pattern. This accounts for the census.

## Where a relative minus can come from

The unlifted permutations for P and Q commute. In the Euclidean Clifford algebra, the lift of the transposition of positions a and b is the unit vector (e_a-e_b)/sqrt(2), using the twisted reflection action of the Pin group. The vectors for disjoint transpositions are orthogonal. Their Clifford products anticommute, so the two lifted paths differ by the central element -1. The lifted square loop has sign -1. Reversing the sign convention of either lift changes both path amplitudes by the same factor and preserves their relative sign.

This is an application of the standard Clifford/Pin double cover, with orthonormal position vectors supplied. See [Gallier, Clifford Algebras, Clifford Groups, and a Generalization of the Quaternions](https://www.cis.upenn.edu/~cis6100/clifford.pdf), sections 1.6–1.8. The sign is forced once this lift is chosen. Bare LR3 also admits the unsigned action and a classical lifted model that carries the sign as a hidden bit. The graph itself selects neither a lift nor an amplitude rule.

## Recombination control

Use a four-state basis (00, 01, 10, 11), where the bits record whether P and Q have acted modulo two. Represent the two moves by signed flips:

- P flips the first bit.
- Q flips the second bit and multiplies the amplitude by -1 when the first bit is 1.

The flips are self-adjoint involutions, with PQ=-QP. This realizes the relative sign on this square. Supply a coherent pulse U=(P+Q)/sqrt(2), and read squared amplitudes. U is unitary because P^2=Q^2=I and the cross terms cancel. U creates two arms from 00, and a second U recombines them. The two contributions to 11 have amplitudes of magnitude 1/2 and opposite signs. A sign flip on one arm between pulses redirects the entire output to 11. With a retained orthogonal route label, the two probabilities add without a cross term.

| Two-pulse protocol | Probability of final cycle 11 |
|---|---:|
| Classical, choose P or Q independently and uniformly on each pulse | 1/2 |
| Supplied coherent pulses | 0 |
| Coherent pulses with a sign flip on one arm | 1 |
| Coherent pulses with distinguishable route records | 1/2 |

The comparison uses a specified classical walk with the same single-pulse transition probabilities. An arbitrary classical controller that remembers the first choice could alter its second choice. A route label is an extra degree of freedom in the coherent control. Its effect follows the usual path-distinguishability calculation. See [Ferrari and Braunecker, Entanglement, which-way measurements, and a quantum erasure](https://www.st-andrews.ac.uk/~bhb/Papers/mach_zehnder.pdf), section II.

## Open step

The reversal square and the lift give a definite interference benchmark on the EHF carrier. The calculation supplies coherent addition of moves, an arm sign flip and the quadratic readout. A decisive follow-up would represent a preparation or recombination interaction and show what it predicts when all apparatus states and histories are included in the classical comparison. The two paths here concern a single carrier. The experiment does not establish bipartite entanglement.

Run `python3 research/cbb-binary/cross48_reversal_interference.py` from the repository root. The verifier enumerates the paths, lifts an explicit labelled square at all eleven tested insertion positions, and checks the normalized pulse via exact integer numerators. AI assistance was used for search, verification and writing.
