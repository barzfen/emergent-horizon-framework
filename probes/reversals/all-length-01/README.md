# EHF-REV-01: all-length reversal admissibility audit

4 November 2026. Research direction: Barry Fensom; implementation and analysis assisted by ChatGPT.

**Outcome:** MICRO's no-isolation constraint does not select LR2/LR3. At nine vertices an admitted LR4 changes the domain-wall count even with Pi preserved. With no Pi restriction, the all-length graph is connected whenever states exist; an elementary constructive proof below extends this beyond the enumerated sizes. This is a combinatorial result, with no external novelty claim or physical interpretation established.

## Definitions and controls

States are undirected Hamiltonian cycles on distinct labels 0,...,n-1 modulo rotation and reflection. For computation, anchor label 0 and choose the smaller orientation. Each vertex carries a fixed bit; bits travel with labels and never flip. MICRO admits a cycle when every vertex has a neighbour of its own bit, equivalently every monochromatic run has length at least two.

For odd n, Pi is the set of labels in even-numbered positions of that canonical representative, recorded as a bit mask. It is chart-dependent and imposed as a separate edge condition when specified. It is not inferred from MICRO.

| Model | Reversal lengths attempted | Endpoint conditions |
|---|---|---|
| OPW3 | 3 | MICRO and unchanged Pi |
| OPW23 | 2, 3 | MICRO and unchanged Pi |
| all_Pi | 2 through n-2 | MICRO and unchanged Pi |
| all_MICRO | 2 through n-2 | MICRO only |

This separates the effect of admitting longer moves from the effect of dropping Pi. No rates, clocks, amplitudes, energy, growth or writer are included. We use simple undirected graphs: repeated events producing the same state pair count as one edge. Length-1 and length-(n-1) reversals are identities on undirected cycles; full reversal also represents the same cycle. Reversing a segment and reversing its complement give the same undirected target, so lengths l and n-l duplicate edges. Event multiplicities would matter for a stochastic process and are not evaluated as transition probabilities here.

## Exhaustive finite results

All canonical cycles at n=5,7,9 and all fixed colourings modulo global bit complement were tested: 16+64+256=336 assignments, including three constant cases and 21 empty minority-one cases. There are 312 nonconstant nonempty cases. Label identity matters for Pi-restricted counts; the following are specified representatives, not universal population-only counts.

| n | Bit-1 labels | Valid states | OPW3 components | OPW23 components | all_Pi components | all_MICRO components |
|---:|---|---:|---:|---:|---:|---:|
| 7 | {1,2,3} | 72 | 27 | 15 | 15 | 1 |
| 9 | {1,2,3} | 2,160 | 390 | 111 | 57 | 1 |
| 9 | {1,2,3,4} | 2,880 | 492 | 216 | 36 | 1 |

At n=5 and n=7, the all_Pi and OPW23 edge sets coincide: complementary segments leave no new independent lengths beyond 2 and 3. At n=9, length 4 adds a genuinely new reversal class. In every nonempty tested colouring, all_MICRO is connected. Thus the no-isolation condition alone preserves neither the original Pi sectors nor the finer MICRO–OPW fragmentation.

For n=9, ones={1,2,3,4}, all_Pi has 7,200 edges, including 864 that change the domain-wall count. All_MICRO has 21,600 edges, including 2,880 wall-changing edges. OPW3 and OPW23 have no wall-changing edges in any enumerated case.

### A Pi-preserving LR4 witness

Take bit-1 labels {1,2,3,4} and

- C = (0,1,2,3,4,5,6,7,8), cyclic word 011110000;
- D = (0,1,2,7,6,5,4,3,8), cyclic word 011000110.

Reverse the four cyclic slots starting at slot 8 in C, then canonicalize, to obtain D. Equivalently reverse the complementary five slots starting at slot 3. Both endpoints satisfy MICRO. Both have Pi={0,2,4,6,8}. The wall count changes from 2 to 4. Therefore no universal domain-wall conservation follows from MICRO plus Pi once this longer reversal is admitted.

## Exact local admissibility lemma

Begin with a MICRO-valid ring. Write the neighbourhood of the selected segment as

    ... p, a | b, c, ..., d, e | f, q ...

The bars are the two cut edges; symbols denote bits, and endpoint notation can overlap for a short segment. After reversal the cut edges become a-e and b-f. Internal vertices retain the same unordered neighbours. Only a, b, e, f need checking. The necessary and sufficient condition is

\[
(a=p\lor a=e)\land(e=d\lor e=a)
\land(b=c\lor b=f)\land(f=q\lor f=b).
\]

This proves that a local rule can govern reversals of many lengths. Length enters through which boundary contexts are brought together; the rule does not impose a universal short-length cutoff. It assumes the source is valid and is not a monotone defect-reduction rule on invalid states.

For LR2, exchanging unequal bits on a valid binary ring produces an isolated bit; accepted LR2 swaps therefore exchange equal-bit labels. This can change labelled structure while leaving the bit pattern unchanged.

## Connectivity theorem for MICRO-only all-length reversals

**Statement.** For n>=4 and a fixed binary assignment to distinct labels, the graph of MICRO-valid undirected cycles with every valid segment reversal allowed is connected whenever nonempty. The state set is nonempty exactly when the assignment is constant or both populations are at least two.

**Proof.** A singleton population has no possible same-type neighbour; otherwise a cycle with one block of each type is valid. A constant assignment permits every cycle, connected by adjacent transpositions.

For a nonconstant valid cycle with more than two domain walls, orient its traversal and select two distinct 0-to-1 boundary edges (a,b) and (d,e), where a,d have bit 0 and b,e have bit 1. A segment reversal reconnects these as (a,d) and (b,e). Each affected endpoint gains a same-type neighbour, so validity is preserved, and exactly two domain walls disappear. The edges are nonadjacent; both intervening arcs contain at least four vertices because every run has length at least two. Hence this is among the admitted lengths 2,...,n-2. Repeat until only one block of each colour remains.

Within those two blocks, adjacent exchanges of equal-bit labels leave the binary pattern valid and can put the labels into any prescribed order, including a common reference cycle. Every move is reversible, so every valid state connects to that reference and hence to every other state. QED.

The argument does not preserve Pi. It does not prove connectivity of all_Pi, which remains fragmented in the finite examples. Nor does connectivity provide a mixing time, memory lifetime or a complete classification of spectral observables.

## What this resolves, and what it leaves open

The proposed distinction between candidate transformations and their admissibility rule is mathematically productive. But MICRO alone admits longer channels and removes the component-based storage mechanism of the restricted models. The earlier [MICRO–OPW results](../../qm-bridge/revisit-01/sources/07_micro_opw_01_README.md) remain valid for their stated edge rules.

A next discriminating question is which explicitly justified additional principle would restrict those channels: preserving Pi, limiting support, or deriving a rate hierarchy are different assumptions. This probe does not choose one. A comparison to the [delta-Ising paper](https://arxiv.org/abs/2610.36829) concerns channel opening and closure; there is no constructed energy/spin-dynamics equivalence.

## Reproduction and verification

Run with Python 3, NumPy and SciPy:

    python probe.py
    python verify.py

[probe.py](probe.py) generates [results.json](results.json), retaining all 336 colouring records, per-length edge counts, component histograms and witnesses. It checks complement-length equivalence, trivial long reversals, graph nesting, Pi restrictions and the short-move wall invariants.

[verify.py](verify.py) imports no probe code and uses only the standard library. It represents cycles by undirected edges, applies two-edge reconnections, reconstructs cycles by neighbour traversal, and uses DFS for components. It checks all 80 colourings at n=5,7 and the n=9 representatives {1,2}, {1,2,3}, {1,2,3,4}, including every reported per-model statistic and per-length edge count. It also checks the domain-merging step wherever more than two walls occur in those cases, and independently checks the boundary lemma on every valid binary ring of lengths 4 through 10. Exact counts and source hashes are in [independent-checks.json](independent-checks.json).

The complete n=9 colouring census has one primary implementation; its three representative cases have the independent reconstruction. The general connectivity result rests on the displayed proof, not extrapolation from the census.
