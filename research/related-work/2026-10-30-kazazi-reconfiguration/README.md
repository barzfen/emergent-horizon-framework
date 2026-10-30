# EHF-RW-001 — Hamiltonian reconfiguration and apparent memory

30 October 2026. **Assessment: directly relevant as a reachability audit; its path theorem does not transfer to EHF cycles or constrained triads.**

## External source and review scope

Albi Kazazi, *Connectivity of the reconfiguration graph of Hamiltonian paths*, [arXiv:2610.05068](https://arxiv.org/abs/2610.05068). Inspected full PDF: **2610.05068v1**, dated 24 September 2026 internally, submitted 4 October 2026, ten pages. Retrieved 30 October 2026 from https://arxiv.org/pdf/2610.05068. The returned PDF itself identifies v1; no claim is made to have reviewed a newer revision.

PDF SHA-256: `c7556ab2630c9f263caeab8841f0d820ae2a0f1277e5206df6cafeffbf177c45`.

The abstract and full text, including the constructive proof in sections 3–5 and the obstruction in section 7, were read. The proof's route reduces edges outside a spanning squared path, then reaches a canonical path. This audit independently implements the move and checks finite examples; it is not a formal verification of the paper's full proof or its diameter bound. The paper PDF is linked, not redistributed here.

**Paper result (attributed):** a host graph containing a spanning squared Hamiltonian path has connected path reconfiguration under backbites. **Relevant warning:** its section 7 supplies disconnected reconfiguration spaces even on hosts with high connectivity. Here a backbite adds an edge from a path endpoint to a non-neighbor along the path and removes the preceding path edge, retaining a spanning path. Path reversal represents the same state.

The introduction also points to existing cycle-switching results, including Kleer, Patel and Stroh (2020), *Switch-based Markov chains for sampling Hamiltonian cycles in dense graphs*, EJC 27(4), P4.29, and Takaoka (2018), *Complexity of Hamiltonian cycle reconfiguration*, Algorithms 11(9), 140. These are follow-up leads, not independently reviewed sources in this entry.

## EHF model under test

The recent geometry work uses three Hamiltonian cycles on a common labelled vertex set, with no undirected edge present in all three. Our present test fixes N, retains the three cycle labels, and changes one cycle at a time. It studies the proposed cycle-rearrangement dynamics, **not the previous birth-only trajectories**. These moves are explicitly defined experimental choices; this entry does not assert that every historical EHF branch used them.

A tour is represented modulo cyclic rotation and reversal, with vertex 0 placed first and the lexicographically smaller orientation selected. Vertex labels are retained. A triad is an ordered triple of these tours satisfying the no-triple-edge constraint. Cycle-label permutations are also quotiented in a separate control. Vertex relabellings are not quotiented; collapsing distinct microscopic states could erase meaningful reachability information.

| Rule | Exactly what can change |
| --- | --- |
| LR2 | Reverse two consecutive cyclic slots: adjacent swap |
| LR3 | Reverse three consecutive cyclic slots: swap first and third |
| LR23 | Either LR2 or LR3 |
| 2opt | Reverse any proper cyclic segment of length 2 through N−2 |

All tours are on K_N. There is no fixed union-edge host restriction: a rearrangement may introduce a new edge. Every accepted change preserves the Hamiltonian-cycle condition and the triad constraint. This differs from the paper's fixed-host path problem. A cyclic segment is local along the selected tour; unrestricted 2opt need not be local in union graph distance. A move is an unweighted adjacency relation here; no probability kernel or mixing time is inferred.

## Provenance of the recent construction

The definitions and motivation were checked against two prior packages:

- `EHF_Hamiltonian_Geometry_Research_01.zip`, research note dated 29 October 2026, SHA-256 `79b15fcceb156174606f1b44ab4f1473035efe8dd9864030406a3debacbb2907`. It proposes fixed-N cycle-preserving 2opt relaxation as a next test.
- `EHF_Probe_Dependent_Geometry_01.zip`, report dated 29 October 2026, SHA-256 `c0c183faa40f4c569374bce13468ed03274c78e574925c5841bd9ab0cf164751`. Its network input is a Hamiltonian triad obeying no triple-used edge; its moving probe on (vertex, cycle label) is a different state space from the triad-rearrangement space used here.

These packages were read for continuity, not claimed to be already present in this repository. The definitions above and code here are sufficient to reproduce this audit without them. No large geometry snapshots are required.

## Questions and controls

1. Does the implementation agree with the paper's positive examples? Enumerate all Hamiltonian paths on K_N and the squared path P_N² for N=4,…,8.
2. Does it detect frozen or conserved sectors? Test a clique with two degree-one attachments at N=6,…,8, and the paper's section-7 lifts A_1(H_2) and A_2(H_2), at N=8 and 10. Check preservation of the internal H_2 path on every accepted backbite.
3. What do the cycle rules alone conserve? Enumerate all individual tours for N=4,…,8.
4. Does the triad constraint create additional obstruction? Enumerate **every** admissible ordered triple for N=4,5,6, under all four rules; repeat connectivity after forgetting cycle labels.

`probe.py` uses integer edge sets, exhaustive state generation and breadth-first component search. Assertions check state counts, move validity, reversibility, and edge-set changes. No energy, Metropolis acceptance, trajectory sampling, growth or fitted dimension is used. Full component-size histograms, counts, witness representatives, Python version and probe-source hash are retained in [results.json](results.json).

## Analytic interpretation

**PROVED from the declared rules:** on an even-length single tour, LR3 preserves the unordered bipartition of vertices occupying alternating cyclic slots. It swaps positions two apart, which have the same parity. Rotation can exchange the two parts and reflection can reorder them, so the unordered partition is well defined on our cycle quotient. Any triad LR3 move preserves this partition for each selected cycle. This is a combinatorial invariant, not a derived physical charge.

For a single even tour, swaps at cyclic distance two generate all permutations within each alternating slot class. Thus the sectors are exactly these bipartitions, with `binomial(N,N/2)/2` components. For odd N the distance-two slot graph is connected; its transpositions generate every permutation, so LR3 alone connects all tours. LR2 connects single tours at every N by adjacent transpositions; LR23 and unrestricted 2opt include those moves. This analytic argument is for unconstrained single tours, not for triads.

The computational triad counts and their interpretation appear in [RESULTS.md](RESULTS.md). A difference persisting under dynamics can be an invariant or an inaccessible sector. Within a connected sector it can still reflect slow mixing. Connectivity by itself proves neither rapid equilibration nor absence of memory in an observed process.

## Reproduction and limitations

From the repository root, with Python 3 and no third-party packages:

```bash
python3 research/related-work/2026-10-30-kazazi-reconfiguration/probe.py
```

This regenerates results.json. Exact counts should agree across Python versions; the recorded version is environment metadata. There are no seeds. Each graph is finite and fully enumerated, but N≤6 triad connectivity cannot establish connectivity at arbitrary N. Adding energy barriers, extra admissibility rules or geometric locality may disconnect the state space again. Neither this paper nor these probes establish emergent particles, quantum memory, or three-dimensional geometry.

**Next test:** compare long-lived observables within one identified sector, then allow a controlled rate of LR2 moves to test sector leakage. Before a large-N relaxation experiment, specify the proposal probabilities, rejected-move treatment, target measure and mixing diagnostics. A general connectivity proof for constrained triads under LR2/2opt remains open in this audit.

## Potential contribution back

**Not ready for outreach yet.** The constrained-triad reachability counts, executable enumeration and alternating-partition explanation could support a precise follow-up question about cycle reconfiguration. Before contacting the author, check the cycle-switching literature identified in the paper and determine whether these constrained-triad observations add anything beyond known results. The path controls reproduce small instances of the author's results and should be described as reproduction, not new EHF theorems. A possible message should give Kazazi clear credit, state the changed assumptions and link the retained code and outputs. No researcher has been contacted as part of this audit.
