# EHF-DIM-09 — A general permutahedral-product chamber theorem

**Date:** 2026-11-19. **Status:** General combinatorial proof for a specially ordered parity chamber; exhaustive family-level verification at n=5,7,9,11.

## Theorem (ordered-label chamber)

Let m≥2, n=2m+1, O={1,...,m}, E={m+1,...,2m}. Represent undirected Hamiltonian cycles by their lexicographically least orientation with 0 anchored first. Define Pi(c) as the set of entries at even zero-based positions, and retain an LR3 move precisely when Pi is unchanged.

Let F_m be the cycles with representatives

`c=(0,o1,e1,o2,e2,...,om,em)`,

where (o1,...,om) permutes O and (e1,...,em) permutes E.

Then:

1. F_m has (m!)² distinct cycles.
2. Every admissible LR3 move from a member of F_m remains in F_m, and exactly the 2(m−1) moves with zero-based starting positions k=1,...,n−3 are admissible.
3. These moves swap consecutive o-entries or consecutive e-entries.
4. Consequently the connected component induced by F_m is exactly
   `Cay(S_m,{s_1,...,s_{m−1}}) □ Cay(S_m,{s_1,...,s_{m−1}})`,
   where s_i=(i,i+1). It is connected and is a full connected component, not merely an induced subgraph.
5. The component is 2(m−1)-regular and has diameter m(m−1). Its vertices are the vertices of a Cartesian product of two (m−1)-dimensional permutahedra.

## Proof

**Unique canonical representatives.** Every cycle in F_m begins with 0, has its next label in O and its last label in E. Because every O label is less than every E label, the displayed orientation is lexicographically smaller than its reversal. Distinct ordered pairs of permutations give distinct canonical cycles. This proves (1).

**Interior reversals.** An LR3 reversal starting at k=1,...,n−3 swaps positions k and k+2 and fixes the middle position. Those endpoints lie in the same parity class, never include 0, and are consecutive within the o-list (for odd k) or e-list (for even k). The new cycle remains in F_m, so Pi={0}∪E remains fixed. These are exactly the adjacent-transposition moves claimed.

**Boundary reversals.** The remaining LR3 starts are k=0,n−2,n−1. For k=n−1, swapping the last and second positions changes which of O/E occupies an even slot; 0 stays anchored and Pi changes. For k=0 or k=n−2, the swap moves 0 away from position zero. Rotating to reanchor 0 causes the cyclic parity cut to cross an odd-length boundary, and at least one label changes its membership in Pi; reversing orientation during canonicalization cannot restore the original Pi because O and E are disjoint and m≥2. Thus these three moves are inadmissible. The verifier enumerates every possible permutation of O and E at m=2,3,4,5 to guard against boundary-case mistakes.

**Graph product.** The admissible moves are exactly independent adjacent transpositions of the two permutations. Adjacent transpositions generate S_m, proving connectivity and the Cartesian Cayley-product isomorphism. The longest adjacent-swap distance is the inversion number m(m−1)/2 for each factor; Cartesian-product distances add, giving diameter m(m−1). This proves (2)–(5).

## Checks

A standard-library verifier enumerates all (m!)² family states and all n LR3 windows at each state, checking canonical orientation, exact admissible-neighbour set, and closure.

| n | m | states | degree | diameter (theorem) | tested |
|---:|---:|---:|---:|---:|---|
| 5 | 2 | 4 | 2 | 2 | yes |
| 7 | 3 | 36 | 4 | 6 | yes |
| 9 | 4 | 576 | 6 | 12 | yes |
| 11 | 5 | 14,400 | 8 | 20 | yes |

## Caveat — important

This theorem is **for the ordered-label chamber under the chosen canonical-orientation and Pi convention**. The parity set Pi, defined from a lexicographically canonical representative, is not invariant under arbitrary label permutations. The product structure is not proven for all EHF chambers or for a label-independent admissibility primitive. It does not imply a physical space dimension, a scaling limit, or a construction of SU(3).

Next: formulate a label-equivariant version using oriented cycles with a marked parity cut, and examine whether the product survives; classify irregular chambers and test dimension scaling.
