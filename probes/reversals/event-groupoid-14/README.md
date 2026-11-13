# EHF-HOL-06 / EVENT-01 — Event-labelled orientation transport and growth

**Date:** 2026-11-13 (Australia/Brisbane)  
**Status:** exact finite enumeration on sizes 5, 7, 9, independently verified; all-size elementary proposition for the stated MICRO-only LR2 model. This is standard orientation-double-cover / voltage-graph mathematics applied to a specified EHF carrier, **not a novel general theorem, physical claim, or proof about Collatz**.  
**Research direction:** Barry Fensom; formalisation, computation and report assisted by ChatGPT.

## Question and decisive distinction

Does retaining *which reversal event occurred*, rather than identifying all events between the same two unoriented Hamiltonian states, repair orientation holonomy under vertex deletion?

**Answer:** yes, for the full MICRO-only event-labelled category; partially, but not at 9->7, for the more restricted MICRO+Pi OPW23 category. The event labels are essential already at five vertices.

## Definitions

- Hamiltonian states: undirected Hamiltonian cycles through distinct fixed labels \`0,...,n-1\`, modulo rotation and reversal. Canonical representative starts at 0 and uses the lexicographically smaller orientation.
- Marked labels \`R={1,2,3}\` have binary colour 1; all other labels colour 0. MICRO: every vertex has a same-colour cyclic neighbour. For this assignment, marked vertices form one consecutive run, and the \`n-3\` zeros form another. The carrier exists for n>=5.
- A reversal **event** is the cyclically contiguous *ordered list of vertex labels* \`b=(v_1,...,v_k)\` of length \`k=2 or 3\` being reversed. Its output on an **oriented** cyclic order is specified without reflecting the cycle. The inverse event reverses the same vertex set in reverse order.
- MICRO-only permits LR2/LR3 events whose endpoints satisfy MICRO. OPW23 additionally requires the **canonical** \`Pi\` sets of endpoints to be equal, with \`Pi(C)={C_0,C_2,...}\`.
- Growth projection \`pi_{n+2,n}\` deletes the two newest zero labels \`n+1\` then \`n\` and reconnects their neighbours. Orientation is retained. We also use one-vertex deletions for the all-size proposition.

The underlying event-labelled graph may have *parallel edges*. Path concatenation and reversing events define its path groupoid. Deleting a vertex may send an LR2/LR3 event to an identity event: this is allowed in the target path groupoid.

## Exact event-deletion identity

Let \`e_b\` reverse the cyclicly consecutive block \`b\` of size 2 or 3. Let \`b'\` be the subsequence of \`b\` remaining after deletion. Then, **as oriented cyclic orders**,

\`pi(e_b(C)) = e_(b')(pi(C))\`.

If \`|b'| <= 1\`, the projected event is an identity. The proof is elementary: removing elements from a cyclic block preserves the order of its remaining contiguous subsequence, and reversal commutes with restriction to that subsequence. The inverse event projects to the inverse event. Composition of paths therefore commutes with projection.

This algebraic statement holds for any labelled cyclic order, without imposing Pi. In the chosen R={1,2,3} MICRO carrier, deletion of the newest zero vertex also **preserves admissible states** whenever at least two zeros remain. Thus it yields a full event/path-groupoid functor on the MICRO-only family.

For OPW23 it can fail because the projected endpoints may not preserve the smaller system's canonical Pi. That is a restriction failure, not a failure of the event-deletion identity.

## Natural reciprocal orientation voltage

Lift each unoriented state C to its two rooted **oriented** representatives. Starting with the canonical orientation of source C, apply the actual event and rotate back to vertex 0 *without reflecting*. Let \`alpha(e)=0\` if this equals the canonical target, and \`alpha(e)=1\` if it equals the reflected target.

The inverse event has the same voltage in F2, hence a backtrack gives zero. For a closed event path P, \`Omega(P)=sum alpha(e) mod 2\` reports whether the lifted oriented path ends on the opposite sheet. Different choices of canonical orientation change alpha by a coboundary and leave Omega invariant.

With \`gamma(C)=1\` iff the **oriented deletion** of canonical child C is reflected relative to the canonical parent chart, exhaustive tests confirm

\`alpha_(n+2)(e) = alpha_n(pi(e)) + gamma(source) + gamma(target)  (mod 2)\`.

The formula allows projected identity events, assigned zero voltage.

## Five-vertex event ambiguity is essential

At n=5, OPW23 has **six unoriented states, three simple graph edges, and twelve directed reversal events**. Each directed pair has **two distinct events**, an LR2 and an LR3, with **opposite orientation voltages**. A simple-edge voltage is therefore not even well-defined.

For example, with C=(0,1,2,3,4) and D=(0,3,2,1,4):

1. LR2 on block (4,0) sends C to D, orientation voltage 1.
2. LR3 on block (3,2,1) sends D to C, orientation voltage 0.

Their composite is a closed **two-event** loop with Omega=1. Using the exact inverse of the first event instead would cancel its voltage. This resolves why the event multigraph has nontrivial holonomy while the n=5 simple graph (a matching) has graph cycle rank zero.

## Exact numerical census

| Model | n | States | Simple undirected edges | Directed events | Graph components | Components with nonzero natural orientation holonomy |
|---|---:|---:|---:|---:|---:|---:|
| MICRO+Pi OPW23 | 5 | 6 | 3 | 12 | 3 | 3 |
| MICRO+Pi OPW23 | 7 | 72 | 84 | 168 | 15 | 3 |
| MICRO+Pi OPW23 | 9 | 2,160 | 4,080 | 8,160 | 111 | 9 |
| MICRO-only LR2/LR3 | 5 | 6 | 9 | 36 | 1 | 1 |
| MICRO-only LR2/LR3 | 7 | 72 | 288 | 576 | 1 | 1 |
| MICRO-only LR2/LR3 | 9 | 2,160 | 12,960 | 25,920 | 1 | 1 |

At n=5, there are two events per **ordered** pair in both models. At n=7,9 every admitted ordered pair in these models has one event; events are still retained rather than identified by policy.

### Projection census, directed events

| Projection | Model | Total events | Map to legal parent reversal | Collapse to parent identity | Forbidden by parent Pi |
|---|---|---:|---:|---:|---:|
| 7 -> 5 | OPW23 | 168 | 84 | 84 | **0** |
| 9 -> 7 | OPW23 | 8,160 | 3,216 | 2,304 | **2,640** |
| 7 -> 5 | MICRO-only | 576 | 324 | 252 | **0** |
| 9 -> 7 | MICRO-only | 25,920 | 17,712 | 8,208 | **0** |

This distinguishes **exact projection of event operations** from **closure of a restricted admissible event family**.

The OPW23 result at 9 -> 7 reproduces the earlier count of 1,320 *unoriented edges* failing projection compatibility (2,640 directed events). The additional event labels do not remove this Pi obstruction.

The explicit ten-event orientation-reversing OPW23 witness at n=9 projects to a valid MICRO-only closed event path at n=7 but contains **three** projected moves forbidden by seven-vertex Pi. Its orientation transport remains nonzero because oriented deletion preserves the final orientation reversal.

## General proposition: the MICRO-only orientation class survives all n>=5

**Proposition.** With fixed marked labels R={1,2,3}, at every n>=5 the oriented MICRO-only LR2 event graph is connected; consequently its orientation-double-cover class on the unoriented event graph is nontrivial. Newest-zero-vertex deletion maps this class compatibly down to each smaller valid carrier.

**Proof.** Orient a cycle and start its written cyclic word at the unique 0-to-1 colour boundary. The oriented state consists of a permutation of the three marked labels, followed by a permutation of the q=n-3 zero labels. There are \`3! q!\` such states. Adjacent swaps within the marked run and within the zero run are permitted LR2 events: they preserve both runs and MICRO. These adjacent transpositions generate \`S_3 x S_q\`, so the **oriented** event graph is connected. The reflection of any oriented cycle is a different oriented state (all labels are distinct), and therefore a path connects a cycle to its reflected orientation. Its image in the unoriented event graph is a closed path with orientation voltage 1. All these operations remain valid under deletion of newest zero labels provided at least two zeros remain; the oriented event projection identity proves compatibility of their voltage classes. QED.

This is a finite-combinatorial application of standard covering-space/signed-graph facts, not evidence of a physical gauge field or independent emergent memory. In particular, the nonzero class is inherited from identifying opposite orientations, and the use of distinguished vertex labels and birth order is supplied structure.

## Reproducibility and independent verification

- [probe.py](probe.py) exhaustively enumerates both event models at n=5,7,9; tests inverse events, oriented deletion, reciprocal Z2 voltage and gauge-correct compatibility for every directed event in each of the six carriers; constructs explicit orientation-reversing paths.
- [verify.py](verify.py) independently checks all event counts, the oriented block action, the projection identity, the canonical orientation phase of every recorded witness, and its nonzero return. It does **not** import the primary probe.
- [results.json](results.json) is the retained exact numerical snapshot, including witnesses and projected-event categories.

The primary program uses only Python standard library and writes results.json:
\`python3 probe.py && python3 verify.py\`.

**Scope note:** these event and graph projections are **not graph covering maps between growth levels**; fibers can have many elements and edges can collapse to identity. The **orientation double cover at a fixed level** is a genuine two-sheeted covering of the event multigraph.

## Next discriminating experiment

Return to OPW3/OPW23 with **Pi treated as a specified chart-dependent rule rather than a fundamental charge**. Seek a growth-compatible *intrinsic* constraint that retains some of the useful OPW fragmentation while allowing a nontrivial event-labelled class to persist. One candidate is a locally transported seam marker with an explicitly defined update; another is to ask which subsets of LR2 events maintain a compatible path category without requiring canonical Pi equality. Any added marker must be counted as an input, not inferred from the carrier.

## Background

- [Voltage graph definitions, inverse edge rule, and derived coverings (MathWorld)](https://mathworld.wolfram.com/VoltageGraph.html)
- [EHF-HOL-05](../orientation-holonomy-13/README.md), natural orientation holonomy in stricter OPW systems.
- [EHF-GROW-LIFT-03](../growth-lift-11/README.md), Pi obstruction to geometry-compatible controller lift.
- [EHF-CBB-BIN-02](../../../research/cbb-binary/BIN-02-history-audit.md), fixed-birth-order deletion history.
