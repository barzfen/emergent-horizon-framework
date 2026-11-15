# Three-colour cycle growth, clocks and Bell tests

This guide follows the EHF research series CROSS-39 through CROSS-58. It links every probe and its verifier, then indexes the earlier work that led to the series. [Repository home](../../README.md) · [CBB binary growth notes](README.md) · [Earlier QM bridge probes](../../probes/qm-bridge/README.md)

## Start here

The model is a ring of individually labelled vertices, each carrying one of three colours. Neighbours must have different colours. A growth step inserts a new label into a gap and gives it the third colour. A length-three reversal (LR3) reverses three consecutive vertices where the resulting ring is still properly coloured. The main series tracks the colour-changing moves. For example, the middle three vertices of **A B A C A** can be reversed to give **A C A B A**. A length-four reversal is LR4. The terms “clock”, “signal” and “receiver” identify configurations and operations of this model.

Four notes give the shortest route through the series.

1. [CROSS-39](CROSS-39-equal-pair-ancestry.md) proves an exact move count for a constrained family and corrects an earlier invariant claim.
2. [CROSS-46](CROSS-46-local-clock.md) builds a six-reversal clock with a supplied local update rule. Growth must stay outside the clock's readout windows, and scheduling affects whether it keeps running.
3. [CROSS-54](CROSS-54-local-bell.md) prepares a Bell pair using legal local moves and a supplied coherent rotation before either measurement setting is chosen. Read [CROSS-47](CROSS-47-reversal-bell.md) for the classical comparison and the overlapping-reader control.
4. [CROSS-58](CROSS-58-growth-reference.md) shows why growth and basis readout alone leave a phase ambiguity. [CROSS-56](CROSS-56-diagonal-phase.md) gives a concrete echo that separates two generators with identical single-pulse reversal probabilities.

The combinatorial results concern reachable cycles and the histories between them. The classical controls supply rules for choosing or observing moves. The coherent controls additionally supply amplitudes, their evolution and squared-amplitude probabilities. CHSH compares the correlations between two readers who each have two measurement settings. Its classical local bound is $2$. The supplied coherent model reaches $2\sqrt{2}$. A physical clock, coherent dynamics and the Born rule remain open as reconstructions from admissible comparisons.

## Complete series

### Reversals, signals and clocks

| Note | What to look for | Reproduce |
| --- | --- | --- |
| [CROSS-39](CROSS-39-equal-pair-ancestry.md) | Proves the exact escape depth and corrects the triple-freeness claim. | [Python](cross39_equal_pair_ancestry.py) |
| [CROSS-40](CROSS-40-signal-and-oscillator.md) | Builds a propagating marker and receiver, and shows why an uncoupled oscillator does not time the signal. | [Python](cross40_signal_and_oscillator.py) |
| [CROSS-41](CROSS-41-growth-and-return.md) | Shows that one insertion can block or delay a return and can mimic a local acknowledgement. | [Python](cross41_growth_and_return.py) |
| [CROSS-42](CROSS-42-resettable-return.md) | Builds a resettable detector and exhibits a false acknowledgement when growth happens between readings. | [Python](cross42_resettable_return.py) |
| [CROSS-43](CROSS-43-local-history.md) | Certifies a receiver action from two signs through one insertion. Two insertions can mimic the full trace. | [Python](cross43_local_history.py) |
| [CROSS-44](CROSS-44-cycle-record.md) | Writes and clears a reply in the cycle. Growth can hide the record from every exterior sign at once. | [Python](cross44_cycle_record.py) |
| [CROSS-45](CROSS-45-fresh-reply.md) | Adds a receiver sign to distinguish a fresh reply from an incomplete reset. | [Python](cross45_fresh_reply.py) |
| [CROSS-46](CROSS-46-local-clock.md) | Constructs a six-reversal clock with protected growth and checks where the clock stalls. | [Python](cross46_local_clock.py) |

### Interference, apparatus memory and setting isolation

| Note | What to look for | Reproduce |
| --- | --- | --- |
| [CROSS-47](CROSS-47-reversal-bell.md) | Compares disjoint and overlapping interventions and identifies the influence behind the apparent Bell violation. | [Python](cross47_reversal_bell.py) |
| [CROSS-48](CROSS-48-reversal-interference.md) | Finds two legal paths to the same labelled cycle and compares classical counting with supplied signed amplitudes. | [Python](cross48_reversal_interference.py) |
| [CROSS-49](CROSS-49-route-recorder.md) | Stores and removes a route record with a third reversal, with a bound for a common classical recombiner. | [Python](cross49_route_recorder.py) |
| [CROSS-50](CROSS-50-cycle-apparatus.md) | Uses a fourth reversal for classical apparatus memory and reproduces the tested coherent joint tables. | [Python](cross50_cycle_apparatus.py) |
| [CROSS-51](CROSS-51-recorder-phase.md) | Uses matched reversal loops to prepare opposite recorder phases in the supplied lift and quantifies the classical memory needed. | [Python](cross51_recorder_phase.py) |
| [CROSS-52](CROSS-52-setting-isolation.md) | Buffers both sides of the setting region and measures the shortest leak into the local readout. | [Python](cross52_setting_isolation.py) |

### Local Bell readout, growth and phase

| Note | What to look for | Reproduce |
| --- | --- | --- |
| [CROSS-53](CROSS-53-local-phase.md) | Tests unchanged local reduced states and distinguishes joint parity from a two-setting Bell test. | [Python](cross53_local_phase.py) |
| [CROSS-54](CROSS-54-local-bell.md) | Prepares and measures a Bell pair on separated windows with a supplied coherent rotation. | [Python](cross54_local_bell.py) |
| [CROSS-55](CROSS-55-symmetric-hopping.md) | Uses symmetric hopping on the same graph and matches each isolated pulse to a stochastic control. | [Python](cross55_symmetric_hopping.py) |
| [CROSS-56](CROSS-56-diagonal-phase.md) | Distinguishes two generators with identical single-pulse probabilities using a phase-sensitive echo. | [Python](cross56_diagonal_phase.py) |
| [CROSS-57](CROSS-57-growth-phase.md) | Counts the exact survival slots and quantifies how a uniform growth lift leaks outside its reference subspace. | [Python](cross57_growth_phase.py) |
| [CROSS-58](CROSS-58-growth-reference.md) | Proves a phase equivalence and shows that the grown children of one proper three-colour cycle cannot supply a stationary reference under all windows. | [Python](cross58_growth_reference.py) |

### What the later probes resolve

The shared-phase and disjoint-reversal controls obey the classical CHSH bound. Overlapping readers can show an apparent violation because one action affects the other. The which-route results can also be reproduced by a classical cycle once a fourth reversal stores information about the protocol. [CROSS-47](CROSS-47-reversal-bell.md) · [CROSS-50](CROSS-50-cycle-apparatus.md)

A remote setting cannot change an isolated reader's marginal under the supplied local quantum model. A shared classical bit reproduces the tested parity correlations. The separate two-setting Bell circuit uses incompatible local measurements after a shared coherent preparation. [CROSS-53](CROSS-53-local-phase.md) · [CROSS-54](CROSS-54-local-bell.md) · [CROSS-55](CROSS-55-symmetric-hopping.md)

An equal-phase stationary reference selects the negative Laplacian within the tested family. Uniform coherent growth over all slots does not make the grow-then-pulse and pulse-then-grow operations interchangeable on all states. Opposite diagonal choices can produce identical basis probabilities when the growth phase convention is changed with them. Can a family of parent cycles provide a stationary reference across growth? [CROSS-57](CROSS-57-growth-phase.md) · [CROSS-58](CROSS-58-growth-reference.md)

## Run the verifiers

Run from the repository root with Python 3. The scripts use the standard library. Python 3.12.14 ran all 20 verifiers for this consolidation. The scripts include exact combinatorial and arithmetic checks, as well as numerical checks of the supplied coherent models. These runs did not externally review the proofs or rerun the older embedded scripts listed below.

```sh
for script in research/cbb-binary/cross[0-9]*.py; do
    python3 "$script" || exit
done
```

Each note includes its own reproduction command and states the relevant bounds, controls and assumptions. Keep the scripts in this directory because several import earlier verifiers. For research provenance and licensing, see [CONTRIBUTING.md](../../CONTRIBUTING.md), [CITATION.cff](../../CITATION.cff) and [LICENSE.md](../../LICENSE.md).

## Earlier probes

For the immediate mathematical prerequisites, start with the [sign encoding and rewrite rules](CROSS-21-orientation-sign-rewrite-rules.md), the [LR4 pattern catalogue](CROSS-28-frozen-automaton-scc-and-LR3-escape.md), the [escape construction](CROSS-31-explicit-LR3-escape-upper-bound.md) and the [ancestry bound](CROSS-34-LR3-causal-ancestry.md). The historical [triple-freeness claim](CROSS-35-triple-free-LR3-invariant.md) has a counterexample and replacement argument in [CROSS-39](CROSS-39-equal-pair-ancestry.md). The original text remains available with its correction at the top.

### Related EHF work

| Resource | How it connects |
| --- | --- |
| [Foundations connection map](../foundations/CONNECTIONS-01.md) | Cycle objects, growth, move selection and observables across EHF. |
| [Original working documents](../source-documents/README.md) | RAW, GROW, OPW23, OPW3 and the historical quantum bridge, with source and scope notes. |
| [Reversal probes](../../probes/reversals/README.md) | Alternative reversal rules, transport, and growth controls. |
| [QM bridge revisits 01–03](../../probes/qm-bridge/README.md) | Earlier classical and coherent controls on separate MICRO–OPW23 carriers. |

<details>
<summary>All 60 earlier CBB notes in this directory</summary>

### Binary encoding and dynamics

- [BIN-01 · Representation audit](BIN-01-representation-audit.md)
- [BIN-02 · Fixed-order growth history and binary observables](BIN-02-history-audit.md)
- [BIN-03 · Unrestricted LR3 connectivity baseline](BIN-03-lr3-connectivity.md)
- [BIN-04 · Even–odd–even sector routing](BIN-04-even-odd-even-routing.md)
- [BIN-05 · Is odd-order LR3 mixing necessary?](BIN-05-mixing-control.md)
- [BIN-06 · Mutual information and coarse-grained memory](BIN-06-mutual-information.md)
- [BIN-07 · Spectral audit of unrestricted LR3 mixing at n=7](BIN-07-spectral-audit.md)
- [BIN-08 · Observable spectral modes of memory](BIN-08-observable-spectral-modes.md)
- [BIN-09 · Analytic selection rule for the 5/7 and 2/7 observable modes](BIN-09-analytic-mode-selection.md)
- [BIN-10 · Odd-order marked-gap quotient: n=5,7,9](BIN-10-odd-order-gap-quotients.md)
- [BIN-11 · Direct binary-bracelet LR3 quotient](BIN-11-direct-bracelet-quotient.md)
- [BIN-12 · MICRO quotient survives; Pi breaks lumpability](BIN-12-micro-pi-lumpability.md)
- [BIN-13 · Minimal equitable refinement of (Pi, colour bracelet) at n=9](BIN-13-pi-equitable-refinement.md)

### Balanced three-colour probes

- [TRI-01 · Balanced three-colour LR3 quotient at n=9](TRI-01-balanced-three-colour.md)
- [TRI-02 · Three-colour separation at n=12 and labelled n=9](TRI-02-separation-sectors.md)
- [TRI-03 · Winding-number conservation under three-colour separation LR3](TRI-03-winding-conservation.md)
- [TRI-04 · Exact local LR3 selection rule and frozen colour bracelets](TRI-04-local-selection-and-arrest.md)
- [TRI-05 · Balanced three-colour separation sectors at n=15](TRI-05-fifteen-vertex-sectors.md)
- [TRI-06 · Pair-transition invariants and a no-go result for balanced three-colour cycles](TRI-06-pair-count-no-go.md)
- [TRI-07 · Exact sign-word rewriting and symmetry quotient](TRI-07-sign-word-rewrite.md)
- [TRI-08 · Sign-run audit and unresolved sector classification](TRI-08-sign-run-audit.md)
- [TRI-09 · Greedy normal-form obstruction](TRI-09-greedy-normal-form-obstruction.md)

### Colour comparisons, move selection and winding

- [CROSS-01 · Two-colour and three-colour LR3 comparison](CROSS-01-two-three-colour-comparison.md)
- [CROSS-02 · Composition and noncommutativity of conditional LR3 moves](CROSS-02-conditional-move-composition.md)
- [CROSS-03 · Raw Hamiltonian cycles as the colour-neutral baseline](CROSS-03-raw-cycle-parity-theorem.md)
- [CROSS-04 · Distinguishability versus admissibility in labelled Hamiltonian cycles](CROSS-04-colour-versus-admissibility.md)
- [CROSS-05 · Colour count versus reversal length](CROSS-05-colour-reversal-length-audit.md)
- [CROSS-06 · Complementarity of LR3 and LR4](CROSS-06-complementary-reversal-generators.md)
- [CROSS-07 · Nine-vertex LR3+LR4 connectivity and parity explanation](CROSS-07-nine-vertex-parity-bridge.md)
- [CROSS-08 · LR4 breaks absolute winding conservation](CROSS-08-lr4-winding-break.md)
- [CROSS-09 · General LRk winding-change identity](CROSS-09-general-winding-change.md)
- [CROSS-10 · General winding parity and n=12,15 tests](CROSS-10-winding-parity-n12-n15.md)
- [CROSS-11 · Winding-transition graphs for LR4](CROSS-11-winding-transition-graph.md)
- [CROSS-12 · General balanced three-colour LR4 winding-path theorem](CROSS-12-general-lr4-winding-path-theorem.md)
- [CROSS-13 · Full LR3+LR4 connectivity, balanced three-colour words](CROSS-13-full-lr3-lr4-word-connectivity.md)
- [CROSS-14 · Shortest-path normalization audit](CROSS-14-shortest-path-normalization.md)
- [CROSS-15 · Phase rotations, LR4 construction, and normalization traps](CROSS-15-phase-rotation-construction.md)
- [CROSS-16 · Bounds for phase-rotation distance](CROSS-16-phase-rotation-distance-bounds.md)
- [CROSS-17 · Obstruction to monotone winding normalization](CROSS-17-monotone-winding-obstruction.md)
- [CROSS-18 · Bounded winding detours](CROSS-18-bounded-winding-detours.md)
- [CROSS-19 · Nine-position trapped-component repair audit](CROSS-19-nine-position-trap-repair.md)
- [CROSS-20 · Repair length grows while winding excursion remains bounded](CROSS-20-repair-length-vs-winding-depth.md)

### Sign rewrites and LR4 escape

- [CROSS-21 · Exact orientation-sign rewrite rules](CROSS-21-orientation-sign-rewrite-rules.md)
- [CROSS-22 · Defect arrangement and upward-trapped components](CROSS-22-defect-arrangement-traps.md)
- [CROSS-23 · Gap transport and a trapped defect triple](CROSS-23-defect-gap-transport.md)
- [CROSS-24 · LR4 defect reactions and a complete gap-space repair](CROSS-24-LR4-gap-reactions.md)
- [CROSS-25 · Bounded-defect repair distances and a candidate progress rank](CROSS-25-bounded-defect-repair-distance.md)
- [CROSS-26 · LR4-only connectivity and an exceptional 15-cycle obstruction](CROSS-26-LR4-frozen-configurations.md)
- [CROSS-27 · Forbidden-pattern automaton and frozen configurations at n=21](CROSS-27-frozen-pattern-automaton.md)
- [CROSS-28 · SCC structure and LR3 escape depth of LR4-frozen cycles](CROSS-28-frozen-automaton-scc-and-LR3-escape.md)
- [CROSS-29 · LR3 escape depth grows in frozen balanced cycles](CROSS-29-growing-LR3-escape-depth.md)
- [CROSS-30 · An explicit family with linearly growing LR3 escape depth](CROSS-30-linear-frozen-family-escape-depth.md)
- [CROSS-31 · Explicit all-t LR3 escape construction and parity invariant](CROSS-31-explicit-LR3-escape-upper-bound.md)
- [CROSS-32 · Exact lower-bound checks to t=12 and three-seed sign structure](CROSS-32-escape-lower-bound-audit.md)
- [CROSS-33 · Three LR3 fronts and failure of naive ++-pair conservation](CROSS-33-three-LR3-fronts.md)
- [CROSS-34 · Causal ancestry for LR3 rewrites](CROSS-34-LR3-causal-ancestry.md)
- [CROSS-35 · Triple-free LR3 invariant and reduction to two LR4 triggers](CROSS-35-triple-free-LR3-invariant.md)
- [CROSS-36 · Single-front activation disproves the two-front collision hypothesis](CROSS-36-single-front-activation.md)
- [CROSS-37 · Failure of naive pair-gap transport potential](CROSS-37-pair-gap-potential-counterexample.md)
- [CROSS-38 · Cyclic defect dipole conservation and transport lower bounds](CROSS-38-cyclic-dipole-and-transport.md)

</details>
