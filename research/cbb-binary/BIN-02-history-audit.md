# EHF-CBB-BIN-02 — Fixed-order growth history and binary observables

Status: exact combinatorial analysis, 2026-11-10. No computational experiment or physics claim.

## Setup
Let H_n be undirected Hamiltonian cycles on vertex labels [n], modulo cyclic rotation and reversal, n>=3. The initial H_3 contains one cycle. For k>=3, the all-slot insertion map takes (C,e), where e is an edge of C in H_k, to the cycle I_e(C) in H_{k+1} obtained by replacing e={u,v} with {u,k+1},{k+1,v}.

## Proposition: unique fixed-order insertion history
The map (C,e)->I_e(C) is a bijection between the disjoint union of all edge slots of all H_k and H_{k+1}. For any child D, remove vertex k+1 and reconnect its two neighbours to obtain the unique C; the neighbour pair determines the unique e. Iterating deletion of n,n-1,...,4 recovers the unique full insertion history of any D in H_n. Thus |H_n|=product_{k=3}^{n-1} k=(n-1)!/2.

The history is an alternative lossless *encoding* of the final labelled cycle, not an independent degree of freedom. It does not contradict BIN-01: fixed numerical labels and their introduction order provide distinguished structure, so this history representation is not equivariant under arbitrary relabelling that changes birth order.

## Binary observables: options and limitations
Any deterministic binary statistic of this unique history is a function of the final labelled cycle. For example, one can define an insertion-slot index after choosing a canonical traversal rooted at the smallest label with an orientation convention, then record its parity at each growth step. But the choice of traversal convention is additional structure; these bits are not automatically invariant under arbitrary vertex relabelling, and binary slot parities are generally not sufficient to reconstruct the full slot choices.

A lossless binary encoding is always possible using a variable-length or fixed-width code for each slot choice (k possibilities at stage k); this is information-theoretic recoding, not an intrinsic physical binary symmetry or a proof of equivalence with XOR edge decorations.

## Where genuinely extra history could enter
1. Allow non-fixed vertex birth order; the same final uncoloured or relabelled cycle may then arise by distinct sequences.
2. Interleave LR3 or other reversible reconfiguration steps; different move sequences may reach the same final cycle, so paths can carry additional information.
3. Retain external memory/controller state not determined by the final cycle.

These changes must be defined explicitly. With the original fixed-order pure insertion rule, claims of multiple distinct histories producing the same final labelled cycle are false.

## Next probe
BIN-03 should first retrieve the exact LR3 definition, then construct the augmented state-transition graph with insertion and LR3 moves. Test whether a binary path observable is invariant under path deformations, whether closed move sequences yield nontrivial parity/holonomy, and whether odd/even n changes the invariant. Distinguish state observables from path observables; provide counterexamples and exact small-n enumerations.
