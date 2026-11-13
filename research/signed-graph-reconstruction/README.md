# Signed-graph reconstruction and reversal sectors

**Status:** [SIGN-01](SIGN-01.md) completed: orientation signs do not distinguish the unmarked unrestricted LR3 parity sectors. [SIGN-02](SIGN-02.md) proves that orientation does not improve prediction of the original marked insertion readout once the unsigned gap class is known. Switching-deck reconstruction remains open for this research thread.  
**Scope:** Combinatorial reconstruction, not a physical model.

Admissible comparison is the chosen primitive data of the framework. EHF studies what can be reconstructed from an admissible-comparison relation. Here the question is whether a sector distinction is recoverable from admissible reversal events and their induced orientation transport, without supplying the sector labels.

## Source and existing EHF baseline

Matteo Cavaleri, Alfredo Donno and Stefano Spessato, [Switching reconstruction of signed graphs: net-degree and balance](https://arxiv.org/abs/2611.13901v1), arXiv preprint v1, submitted 10 November 2026. Abstract and selected passages consulted; proofs not independently checked. The paper asks when a signed graph is determined up to isomorphism by the multiset of unlabeled signed graphs obtained by flipping the incident edge signs at each vertex in turn. It proves reconstruction under specified net-degree or balance hypotheses, not for arbitrary signed graphs.

[EHF-HOL-05](../../probes/reversals/orientation-holonomy-13/README.md) already derives signs from orientation transport on MICRO+Pi reversal events. In the tested odd sizes, OPW3 has trivial orientation holonomy, while some OPW23 components have nontrivial holonomy. That nontriviality disappears on the tested growth-projectable restriction. At size 5, distinct reversal events can share endpoints but give opposite signs, so a simple edge graph can lose essential data.

## First probe — blinded sector separation

1. Specify the two sector definitions, their source and the carrier on which they are observed. Reserve the sector labels for scoring; do not use them to choose signs, moves, loop lengths or filters. Use the smallest documented odd and even instances of the same construction if both exist. If no comparable even instance exists, record that limitation.
2. Retain reversal events and derive their signs using the existing orientation-lift rule where applicable. Verify reciprocal signs and preserve parallel events. Explicitly state any extra data needed beyond the bare comparison graph. In particular, changing an orientation chart for a **fixed** carrier is not the same as changing the canonical convention used to define Pi; that may change which edges are admitted.
3. Multiply signs along closed walks. Changing the orientation chart at a state flips the signs at its incident edge ends, so the closed-walk product is unchanged. Check chart changes and consistent relabellings of the carrier, including its marked data. Start with the balanced/unbalanced status of each connected component; a spanning forest and the fundamental cycles of the remaining events suffice to check it. Keep a negative loop as a witness, or retain a vertex-sign potential as a certificate of balance.
4. Reveal the labels and compare against an unsigned baseline (component sizes and adjacency). Report whether the sign test adds separation, collides across sectors, or is inapplicable. If it adds separation, repeat on the growth-projectable graph wherever a compatible projection is defined. Finite separation is not a general theorem and would not explain the 5/7 and 2/7 decay eigenvalues identified in BIN-09.

## Separate follow-up — reconstruction from switched views

Sector separation is not reconstruction. On small **simple** signed carriers for which the event signs descend unambiguously, form the source paper's switching deck with multiplicities. Keep the unsigned carrier fixed for an initial exhaustive search over signings. Canonicalize each card up to signed-graph isomorphism and look for non-isomorphic signings with identical decks; do not identify switching equivalence with signed-graph isomorphism. Log which source hypotheses hold, the search bounds and any collision witnesses. An event-multigraph extension requires a separate definition and is outside the source theorem as used here.

**Potential contribution back:** Nothing ready to share. First produce and independently verify a finite witness or an explicit limitation of the comparison.
