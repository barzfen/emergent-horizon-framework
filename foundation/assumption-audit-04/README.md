# EHF assumption audit 04: writing a record into cycle structure

Date: 1 November 2026. Status: an explicit structural-writing example; exhaustive finite move checks; a scoped preservation/writeability obstruction; numerical retention calculations. No novelty or physical-origin claim.

Research direction: Barry Fensom. Development, code and exposition assisted by ChatGPT. Follows [Audit 03](../assumption-audit-03/README.md). Cycle conventions and admissible local moves follow [RW-001](../../research/related-work/2026-10-30-kazazi-reconfiguration/README.md).

## Result and assumptions

A boundary event can write a readable distinction into the Hamiltonian-triad arrangement, with no appended register bit. The chosen structural change is one allowed adjacent swap. But coupling the event to that move is an additional law; it does not follow from admissibility alone. Under the tested symmetric background rearrangements, the distinction eventually disappears.

The example is a controlled **one-event writing and storage benchmark**. The rule is also checked as a valid coupled probe/network transition rule. Retention numbers below disable further writing after the selected event and freeze the network during the final one-hop readout. They do not simulate an autonomous repeatedly writing observer or a simultaneous noisy readout. These protocol restrictions must not be omitted.

## 1. Carrier and admissible move

Use three labelled Hamiltonian cycles on vertices {0,1,2,3,4}, with no edge shared by all three. Tours are considered modulo rotation/reflection, while cycle labels remain distinct. Repeated tours are allowed when the edge constraint permits them. There are 12 individual tours and **516 admissible ordered triads**.

An LR2 move swaps two adjacent vertices on one cyclic tour, leaving the other tours unchanged, and is accepted only if the resulting triad is admissible. Distinct outcomes are separate move neighbors; multiple descriptions of the same outcome are not extra rate channels. Every accepted move has an accepted reverse.

Take the inherited triad A as a blank carrier and the following new triad B as its written carrier. B here is a new witness, not RW-003's matched triad C.

| Cycle | Blank A | Written B |
| --- | --- | --- |
| 0 | 0,1,2,3,4 | 0,1,3,2,4 |
| 1 | 0,1,2,3,4 | 0,1,2,3,4 |
| 2 | 0,2,4,1,3 | 0,2,4,1,3 |

Swap adjacent vertices 2 and 3 in cycle 0. This removes its edges {1,2},{3,4} and adds {1,3},{2,4}. Both triads satisfy the no-triple-used-edge rule. Their shared herald edge {0,2} still belongs only to cycle 2.

No new vertex, bit or extra cycle was introduced. The state used as a carrier is the existing ordered triad. Its blank initialization as A is still supplied.

## 2. Event-to-reconfiguration law

Retain the classical probe (v,k), with spatial rate 1/2 to each neighbor in its current cycle and switching rate kappa/2 to each other cycle at the same vertex. On a spatial crossing 2->0, apply the following structural operation W:

1. Require {0,2} to belong uniquely to cycle 2.
2. Swap vertex names 2 and 3 within cycle 0 only, provided this is an LR2 neighbor, the resulting triad is admissible and cycle 0 still does not use {0,2}.
3. Otherwise leave the triad unchanged.

These conditions ensure W is an involution: W(W(s))=s. They hold for A and B, so W(A)=B and W(B)=A. The rule acts on 16 of the 516 states, forming eight paired structural switches; it is the identity elsewhere. An event thus writes the selected distinction, but another event can undo it. This is a toggle, not a monotone 'ever' latch.

Starting from network A and probe state (2,2), an actual herald has the coupled transition

\[
(A,2,2)\longrightarrow(B,0,2)
\]

at rate 1/2. That transition writes the structural change while retaining a valid probe edge in the destination network. There is no preselected stored bit and no external update at the instant of the crossing. The event coupling itself remains imposed.

The joint carrier/probe model has 516*15=**7,740 states**. The code checks all **15,480 spatial transitions** under this coupling; 16 change the network. Every destination is admissible and the traversed edge exists in the destination cycle. Cycle switches and background LR2 moves can be added without extending the state space. The finite-time storage tests below evolve only the network after one selected event; no joint-process retention claim is inferred from the transition checks.

The rule selects named boundary vertices, a named cycle and a particular reversal. Its admissibility checks may inspect global triad data. 'Local' here means a short combinatorial reversal, not a derived spatially local physical interaction. Merely allowing this move does not explain why a crossing should cause it.

## 3. Boundary readout: structural access versus one observation

Let c12(s) be the number of cycles using boundary edge {1,2}. It equals 2 for A and 1 for B. Thus a reader granted exact access to this local multiplicity can distinguish the carriers perfectly immediately after writing. It need not identify individual cycle names for this readout. We do not assume that such an exact structural query is physically free.

A weaker, specified experiment uses only a single position outcome: prepare a probe at boundary vertex 1 with its cycle chosen uniformly, make exactly one spatial hop in a network held fixed during readout, and ask whether it arrives at vertex 2. Its click probability is c12/6. Therefore:

| Carrier | One-hop click probability |
| --- | ---: |
| Blank A | 1/3 |
| Written B | 1/6 |

One such outcome gives optimal equal-prior classification success **7/12 = 58.33%**, not perfect reading. This experiment supplies a position preparation, uniform cycle preparation and a resolved spatial hop; it omits cycle switching during that hop. It is an explicit access protocol rather than a derived internal reader. Repeated observations of one fluctuating carrier cannot automatically be treated as independent samples of a fixed state.

## 4. Retention under the same allowed move class

During the storage interval, permit every valid LR2 neighbor transition at rate eta/10. Ten is the maximum degree of the full move graph; the state-dependent total escape rate is between 0.6 eta and eta. Rates are per distinct neighbor, not per attempted swap. Because edge rates are symmetric, the stationary distribution is uniform, rather than degree-weighted.

Enumeration finds **1,980 undirected move edges and one connected component of size 516**. The reverse B->A is among these background moves. For eta>0, the continuous-time move chain mixes to its unique uniform stationary law. The two initial conditional laws, one at A and one at B, consequently converge to the same distribution.

Time below is u=eta*t, a dimensionless rearrangement-noise time. It is not automatically the mean-hop time of the original probe, because eta is a separately imposed rate. Zero rearrangement noise freezes either carrier; that limiting persistence is supplied by freezing, not demonstrated protection.

| u | Optimal full-triad classification success | Ideal single-link multiplicity success | One-hop position readout success |
| --- | ---: | ---: | ---: |
| 0 | 100.00% | 100.00% | 58.33% |
| 1 | 89.66% | 75.81% | 54.65% |
| 3 | 75.37% | 58.03% | 51.57% |
| 10 | 58.65% | 50.27% | 50.06% |

All entries use equal priors for the initial A/B alternatives and the corresponding optimal decoder for the stated observation. They are calculated distributions, not random trials. Full-state access is an ideal upper bound. The code also checks all three visible boundary multiplicities jointly; they help somewhat but still reveal much less than the complete triad at late times.

The loss of a particular boundary signal does not imply complete erasure: at u=3 the full-triad reader still succeeds about 75.37% of the time, while the selected one-hop reader is near chance. Conversely, indefinite global retention is impossible for this finite connected symmetric noise model, as the two full distributions eventually coincide in the limit.

The symmetric generator has a single zero eigenvalue and numerically estimated positive spectral gap **0.1417391887 eta**. The exponential decay of all nonconstant eigenmodes proves convergence; the decimal gap is a numerical result, not an exact algebraic value. These calculations concern only this five-vertex model and specified rates, not every EHF network or every noise model.

## 5. A scoped obstruction: conserved sectors cannot be written by their own conserving moves

**Proposition.** Let M be an allowed move graph, and let r be a readout unchanged along every edge of M. No event implemented solely by a finite sequence of moves in M can change r.

**Proof:** each move preserves r; induction preserves it along the whole path. Equivalently, r is constant on every connected component. To change it, a write must cross components and therefore use an operation outside this move class.

For our connected 516-state LR2 graph, the only exactly conserved readouts of this kind are constants. Fragmented move spaces can have sector labels, but a writer confined to those same sector-preserving moves cannot change the sector label. This connects the structural-record question to the earlier reachability audit without interpreting a frozen sector as a freely writable memory.

This is not a general prohibition on useful memory. Long but finite retention, different rates for deliberate writes and perturbations, energy barriers, driven correction or additional control operations can change the practical result. Each would add assumptions. Nor does connectivity alone imply rapid erasure; the rate law and bottlenecks matter.

## 6. Reproduction and checks

Requires Python 3.10+, NumPy and SciPy:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 foundation/assumption-audit-04/probe.py
```

The standalone implementation exhaustively generates all 12 tours and 516 valid triads; verifies every move and reverse; checks connectivity, the A/B witness and writer involution on every state; and validates all coupled spatial transitions. Numerical checks cover generator symmetry and conservation, one-dimensional stationary nullspace, stochastic distributions, data-processing bounds for increasingly limited readers, and monotonically decreasing full-state total variation at the sampled times. Eigenmode evolution is independently compared with direct matrix exponentiation at u=1 and 10, to absolute tolerance 3e-13.

All assertions passed. [probe.py](probe.py) and [results.json](results.json) retain the method, input witnesses, source hash, software versions and full time table. The mathematical sector argument is proved above; finite enumeration establishes the particular move graph. Float calculations establish the reported approximate retention values. Values near machine precision at late times should not be treated as exact zeros.

## Attribution and interpretation

Canonical-tour conventions and LR2 admissibility follow EHF-RW-001 and its source acknowledgement to Albi Kazazi's Hamiltonian-path reconfiguration paper. That paper's path theorem is not being applied as a theorem about our triads. The inherited blank triad and boundary-event preparation follow RW-003 through RW-005 and Audit 03. Their source acknowledgements remain in place. This program is a standalone implementation; no external paper or code is copied.

The record now occupies existing cycle structure, but the event-to-write law, initial blank arrangement, distinguished ports and labels, allowed rearrangements, perturbation rates and readout protocol remain chosen. This is an assumption reduction in the carrier description, not a derivation of all recording rules or an emergent observer. The required background mathematics—finite Markov chains, spectral decomposition, total variation, and connected-component invariants—is standard. NumPy/SciPy versions are recorded. No novelty review has been performed.

**Potential contribution back:** no novelty-based outreach is ready. The useful EHF benchmark is the explicit writable structural pair, its limited boundary readout and the exact reason sector protection alone cannot supply both writing and retention under one conserving move class. A sensible next theoretical target is an explicitly justified separation between deliberate-write and incidental-perturbation dynamics; further size sweeps alone would not supply that justification. Licences follow the repository's [licensing policy](../../LICENSE.md).
