# EHF-CBB-BIN — Binary relational encoding of all-slot Hamiltonian growth

Status: **research proposal; no equivalence theorem or physical interpretation established** (2026-11-10).

## Motivation
Investigate whether binary relational descriptions can encode the original Combinatorial Big Bang (CBB) growth rule rather than merely augmenting it. Original CBB grows labelled, undirected Hamiltonian cycles by inserting the new labelled vertex into **every** edge slot. The aim is to compare symmetry, odd/even order, and local reversal reachability without imposing strict alternating vertex colours (which would exclude odd cycles).

## Baseline definitions
For n >= 3, let H_n be undirected Hamiltonian cycles on [n], modulo cyclic rotation and reversal. |H_n|=(n-1)!/2. For each C in H_n and each of its n edges e, let I_e(C) insert vertex n+1 into e. The n insertions over all C cover H_{n+1} exactly once: deleting vertex n+1 is the inverse.

For a fixed oriented listing of a cycle C=(v_0,...,v_{n-1}), consider vertex bits s_i in F_2 and edge differences b_i=s_i+s_{i+1} (mod 2), including the closing edge. Necessarily sum_i b_i=0 (mod 2). Conversely, every even-parity edge-bit assignment admits vertex potentials, unique up to a global bit flip. Thus each uncoloured C has 2^(n-1) such assignments. This is an **extension**, not a bijective encoding of bare CBB cycles.

When edge e of bit b is split by insertion, its replacement bits (x,y) must satisfy x+y=b (mod 2). There are two refinements, corresponding to the two possible bits of the inserted vertex relative to a fixed endpoint. Deleting the new vertex combines the two incident bits by XOR. The binary-extended growth projects onto all-slot CBB growth, but has twice as many transitions per parent slot.

## Parity and symmetry cautions
If all edges require b=1, closure is possible iff n is even. For odd n, at least one b=0 is necessary, but odd Hamiltonian cycles themselves remain valid in uncoloured CBB. A cycle's abstract dihedral symmetry must be distinguished from symmetry of the labelled ambient graph, its binary decoration, and its growth history. Symmetric rules can produce asymmetric individual outcomes without an asymmetric ensemble.

## Research probes
- **BIN-01 — Representation:** Specify a canonical/gauge-invariant binary observable derived solely from the original cycle or prove no proposed candidate is faithful. Count fibres, automorphisms, and counterexamples at small n.
- **BIN-02 — Growth:** Prove the projection commutes with all-slot insertion, enumerate all binary lifts, and test whether any canonical section commutes with insertion.
- **BIN-03 — Reversals:** Define LR3 precisely from the repository's reversal conventions before testing. Compare reversal connected components and parity-sector invariants under the proposed encoding; do not assume XOR closure explains LR3 sectors.
- **BIN-04 — Symmetry/memory:** Compare n even -> n+1 odd -> n+2 even under matched rules. Distinguish trajectory asymmetry, ensemble asymmetry, and history-dependent observables.

## Reproducibility and success criteria
Enumerate n=3..8 first, using canonical undirected cycles; independently verify cycle counts and unique deletion parent. For binary extensions verify parity closure, fibre count, insertion/deletion consistency, and symmetry covariance. Report exact counts, test code, seeds if sampling, failures, and smallest counterexamples. Only call the two systems *equivalent* after specifying a bijection or a justified quotient and showing it intertwines the chosen growth and LR3 operations.

## Physical scope
The binary XOR formulation is elementary graph cohomology / discrete potentials; it is not by itself new physics. Any analogies to chirality, symmetry breaking, time reversal, or gauge structure remain hypotheses requiring independent mathematical and physical evidence.

## Related repository work
Review existing CBB/all-slot growth, LR3/reversal, OPW and MICRO definitions before making cross-branch claims. Preserve original conventions and cite exact files in subsequent probes.
