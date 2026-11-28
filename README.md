# Emergent Horizon Framework (EHF)

EHF is an exploratory mathematical-physics research programme. It starts with configurations and allowed changes, then asks what structure follows from the histories those changes generate. The work spans combinatorics, graph dynamics, statistical models of growth and memory, and comparisons with established physics. A result about a mathematical model carries the assumptions of that model.

## Start here

| If you want to… | Read |
| --- | --- |
| Pick up the current research and see what to do next | [Research handover](HANDOVER.md) |
| Understand what EHF assumes and how the projects fit together | [Foundations](foundation/README.md) and the [connections map](research/foundations/CONNECTIONS-01.md) |
| See what a concrete result looks like | [Julstce: reading detector order after growth](probes/micro/julstce/README.md). Two reversal orders can produce the same statistics for every sequence of added colours while leaving different traces in the final ring shape. |
| Find machine-checked mathematics | [Lean 4 verification](formal/lean/README.md), including binary edge splitting and all-slot Hamiltonian-cycle growth with unique ordered ancestry |
| See the programme assessment and open questions | [Status](STATUS.md) and [roadmap](ROADMAP.md) |

## Research index

For individual notes and proofs, jump to the [full research index](#full-research-index).

### Growth, entropy, and records

| Topic | Entry points |
| --- | --- |
| **Hamiltonian growth and its colour extensions** | [Binary relational encoding](research/cbb-binary/README.md) introduces all-slot growth and its binary extension. [BIN, TRI and CROSS reader’s guide](research/cbb-binary/GROWTH-CLOCKS-AND-BELL.md) indexes the binary and three-colour studies of reversal reachability, winding, transport, records, clocks and Bell controls, through CROSS-63. |
| **Wheeler series: constrained growth and entropy** | [Working paper](research/wheeler/paper-v0.1/README.md) · [Probe series](probes/wheeler/README.md) · [Review](research/wheeler/REVIEW-01.md) · [Reproduction code](code/wheeler/README.md). See [WHEELER-62](probes/wheeler/WHEELER-62.md) for entropy growth from the minimal seed and [WHEELER-61](probes/wheeler/WHEELER-61.md) for an exact entropy decrease from a different seed. [WHEELER-63](probes/wheeler/WHEELER-63.md) extends the bounded checks. The [summary](research/wheeler/SUMMARY-01.md) and [errata](probes/wheeler/ERRATA-01.md) give the scope and corrections. |
| **MICRO growth and observer comparison** | [Observer compatibility audit](probes/micro/observer-compatibility-01/README.md) tests when projected observations retain a closed growth rule. [Julstce](probes/micro/julstce/README.md) shows how the final shape reveals detector order after growth. The [handover](HANDOVER.md#a-result-linking-wheeler-and-julstce) proves a formula for the limiting accuracy. |
| **Assumptions behind records and readout** | [Assumption audits 01–05](foundation/README.md) examine when relational roles are forced, how records form and survive, and what probe-gated writing adds. |

### Graphs, reversals, geometry, and quantum comparisons

| Topic | Entry points |
| --- | --- |
| **Hamiltonian cycles and admissible comparisons** | [HC studies](research/hamiltonian-cycle/README.md) investigate which partial routes can share a search state, with an exact attachment rule and a minimal counterexample to a degree-based comparison. |
| **Reversal rules, transport, and holonomy** | [Reversal series](probes/reversals/README.md) · [All-length MICRO connectivity](probes/reversals/all-length-01/README.md) · [Rare reversal channels](probes/reversals/rare-channel-02/README.md) · [Orientation holonomy](probes/reversals/orientation-holonomy-13/README.md) · [Reversal event groupoid](probes/reversals/event-groupoid-14/README.md). These studies distinguish the admissible moves, their orientations, and any rates assigned to them. |
| **Dimensions and geometry of reversal graphs** | [DIM-01–09](probes/dimensions) · [Graph distance and return probabilities](probes/dimensions/ehf-dim-01/README.md) · [Permutahedral-product chamber theorem](probes/dimensions/ehf-dim-09/README.md). The theorem describes a specified ordered parity chamber. Spectral and physical dimension are separate questions. |
| **Signed-graph reconstruction** | [SIGN-01–03](research/signed-graph-reconstruction/README.md) tests which sector, orientation and directional insertion information can be recovered from reversal data. |
| **Quantum comparison and classical controls** | [QM bridge revisits 01–03](probes/qm-bridge/README.md) cover coherent controls, signed orientation transport and operational readout. The tested transport statistics admit a classical explanation on oriented tours. The [CROSS guide](research/cbb-binary/GROWTH-CLOCKS-AND-BELL.md) continues with growth clocks, detector controls and Bell circuits with supplied coherent dynamics. |

### Amplitudes and number theory

| Topic | Entry points |
| --- | --- |
| **Nine-point amplitudes and ordering** | [Nine-point odd-to-even tail theorem](research/amplitudes/nine-point-tail/README.md) · [Exact follow-up checks](research/amplitudes/nine-point-tail/followups/README.md). The series studies parity fibres, support cuts, and when identities lift through prescribed cyclic orderings. |
| **Collinear colour and the 1:2:3 law** | [Collinear colour channels](research/amplitudes/collinear-colour/README.md) gives the exact planar equal-split tree-MHV result, its SU(N) extension, and the tested limits beyond the planar path. [Amplitude studies index](research/amplitudes/README.md) links the comparison with ordering and orientation. |
| **Collatz** | [Working note](research/collatz/README.md) · [Probe series](probes/collatz) · [Cofactor-one classification](probes/collatz/cofactor-one-classification-28/README.md). The probes test how parity graphs, residues and lifted relations preserve information about integer trajectories. The general conjecture remains open. |
| **Wieferich primes and modular cycle lifting** | [EHF-WIEF-02](research/wieferich/EHF-WIEF-02/README.md) uses established number theory and exact computation to compare cycle splitting with elongation under prime-power refinement. |

### Sources and reproduction

- [Source-document index](research/source-documents/README.md) preserves OPW23, OPW3, RAW, GROW, Johnson transport and curvature, historical AMP and QM notes, and PHYS-ALG materials including the Lam connection. Its checksum manifest identifies the retained snapshots.
- [Recovered Hamilton-cycle archive](research/consolidation-2026-11-02/README.md) links the RAW, GROW, OPW, AMP and XBR source packages and the [MICRO–OPW probes](probes/micro-opw/README.md). The recovery report identifies which checks ran and which certificates are missing.
- [Related work](research/related-work/README.md) links external papers to EHF definitions, follow-up probes, and limitations.
- [Research notes](research/README.md) · [Probe directories](probes) · [Formal results](formal/README.md) · [Code](code/README.md) · [Data](data/README.md) · [Archive](archive/README.md). Many individual probes carry their own verifier and instructions alongside the research note.

## Research discipline

- **PROVED** — established analytically from stated assumptions.
- **MACHINE-VERIFIED** — checked by a proof assistant within the stated formalisation.
- **COMPUTATIONAL** — established by a specified numerical or exact computation within its tested scope.
- **EMPIRICAL PATTERN** — regularity observed in examples that needs stronger validation.
- **CONJECTURE** — precise claim that remains open.
- **SPECULATIVE** — proposed mechanism or physical analogy.
- **FALSIFIED / NEGATIVE** — claim ruled out or unsupported under the stated model and test.

The current priorities are formalising the underlying configurations and moves, auditing earlier results, and deriving effective laws for growth, transport, records, time and geometry from explicit rules. EHF currently provides mathematical models and comparisons with physics. Its physical interpretations remain research questions.

## Licensing, citation, and contributions

Original code is available under MIT. Original research notes, documentation and figures use CC BY 4.0. File-specific and third-party terms take precedence. See the [licensing scope](LICENSE.md), [citation metadata](CITATION.cff) and [contribution and attribution guidance](CONTRIBUTING.md).

## Full research index

Every Markdown note, retained PDF and Lean proof file on the default branch is indexed below. The [code](code/README.md) and [data](data/README.md) guides cover supporting files.

[Project guides and foundations](#project-guides-and-foundations) · [Formal results and Lean proofs](#formal-results-and-lean-proofs) · [Hamiltonian cycles and binary/three-colour growth](#hamiltonian-cycles-and-binarythree-colour-growth) · [Wheeler growth, entropy, and reproduction](#wheeler-growth-entropy-and-reproduction) · [MICRO growth, observers, and Julstce](#micro-growth-observers-and-julstce) · [Reversal rules, winding, and holonomy](#reversal-rules-winding-and-holonomy) · [Dimensions and geometry](#dimensions-and-geometry) · [Quantum comparisons and signed graphs](#quantum-comparisons-and-signed-graphs) · [Amplitudes, ordering, and collinear colour](#amplitudes-ordering-and-collinear-colour) · [Collatz](#collatz) · [Wieferich primes and modular cycles](#wieferich-primes-and-modular-cycles) · [Source documents, related work, and archives](#source-documents-related-work-and-archives) · [Recovered sources and MICRO–OPW](#recovered-sources-and-microopw)

### Project guides and foundations

<details>
<summary>Show 15 entries</summary>

**Repository root**

- [Contribution and attribution guide](CONTRIBUTING.md)
- [Licensing scope](LICENSE.md)
- [Research roadmap](ROADMAP.md)
- [Programme status](STATUS.md)
- [Research handover](HANDOVER.md)

**`foundation/`**

- [Guide](foundation/README.md)

**`foundation/assumption-audit-01/`**

- [Guide](foundation/assumption-audit-01/README.md)

**`foundation/assumption-audit-02/`**

- [Guide](foundation/assumption-audit-02/README.md)

**`foundation/assumption-audit-03/`**

- [Guide](foundation/assumption-audit-03/README.md)

**`foundation/assumption-audit-04/`**

- [Guide](foundation/assumption-audit-04/README.md)

**`foundation/assumption-audit-05/`**

- [Guide](foundation/assumption-audit-05/README.md)

**`research/foundations/`**

- [CONNECTIONS-01](research/foundations/CONNECTIONS-01.md)

**`research/foundations/comparison-to-cycle/`**

- [Guide](research/foundations/comparison-to-cycle/README.md)
- [branch-shape-order](research/foundations/comparison-to-cycle/branch-shape-order.md)
- [leaf-growth](research/foundations/comparison-to-cycle/leaf-growth.md)

</details>

### Formal results and Lean proofs

<details>
<summary>Show 6 entries</summary>

**`formal/`**

- [Guide](formal/README.md)

**`formal/lean/`**

- [Guide](formal/lean/README.md)
- [CycleGrowth.lean](formal/lean/CycleGrowth.lean)
- [EdgeSplit.lean](formal/lean/EdgeSplit.lean)
- [UNDIRECTED-GROWTH](formal/lean/UNDIRECTED-GROWTH.md)
- [UndirectedCycles.lean](formal/lean/UndirectedCycles.lean)

</details>

### Hamiltonian cycles and binary/three-colour growth

<details>
<summary>Show 98 entries</summary>

**`research/cbb-binary/`**

- [Guide](research/cbb-binary/README.md)
- [BIN-01-representation-audit](research/cbb-binary/BIN-01-representation-audit.md)
- [BIN-02-history-audit](research/cbb-binary/BIN-02-history-audit.md)
- [BIN-03-lr3-connectivity](research/cbb-binary/BIN-03-lr3-connectivity.md)
- [BIN-04-even-odd-even-routing](research/cbb-binary/BIN-04-even-odd-even-routing.md)
- [BIN-05-mixing-control](research/cbb-binary/BIN-05-mixing-control.md)
- [BIN-06-mutual-information](research/cbb-binary/BIN-06-mutual-information.md)
- [BIN-07-spectral-audit](research/cbb-binary/BIN-07-spectral-audit.md)
- [BIN-08-observable-spectral-modes](research/cbb-binary/BIN-08-observable-spectral-modes.md)
- [BIN-09-analytic-mode-selection](research/cbb-binary/BIN-09-analytic-mode-selection.md)
- [BIN-10-odd-order-gap-quotients](research/cbb-binary/BIN-10-odd-order-gap-quotients.md)
- [BIN-11-direct-bracelet-quotient](research/cbb-binary/BIN-11-direct-bracelet-quotient.md)
- [BIN-12-micro-pi-lumpability](research/cbb-binary/BIN-12-micro-pi-lumpability.md)
- [BIN-13-pi-equitable-refinement](research/cbb-binary/BIN-13-pi-equitable-refinement.md)
- [CROSS-01-two-three-colour-comparison](research/cbb-binary/CROSS-01-two-three-colour-comparison.md)
- [CROSS-02-conditional-move-composition](research/cbb-binary/CROSS-02-conditional-move-composition.md)
- [CROSS-03-raw-cycle-parity-theorem](research/cbb-binary/CROSS-03-raw-cycle-parity-theorem.md)
- [CROSS-04-colour-versus-admissibility](research/cbb-binary/CROSS-04-colour-versus-admissibility.md)
- [CROSS-05-colour-reversal-length-audit](research/cbb-binary/CROSS-05-colour-reversal-length-audit.md)
- [CROSS-06-complementary-reversal-generators](research/cbb-binary/CROSS-06-complementary-reversal-generators.md)
- [CROSS-07-nine-vertex-parity-bridge](research/cbb-binary/CROSS-07-nine-vertex-parity-bridge.md)
- [CROSS-08-lr4-winding-break](research/cbb-binary/CROSS-08-lr4-winding-break.md)
- [CROSS-09-general-winding-change](research/cbb-binary/CROSS-09-general-winding-change.md)
- [CROSS-10-winding-parity-n12-n15](research/cbb-binary/CROSS-10-winding-parity-n12-n15.md)
- [CROSS-11-winding-transition-graph](research/cbb-binary/CROSS-11-winding-transition-graph.md)
- [CROSS-12-general-lr4-winding-path-theorem](research/cbb-binary/CROSS-12-general-lr4-winding-path-theorem.md)
- [CROSS-13-full-lr3-lr4-word-connectivity](research/cbb-binary/CROSS-13-full-lr3-lr4-word-connectivity.md)
- [CROSS-14-shortest-path-normalization](research/cbb-binary/CROSS-14-shortest-path-normalization.md)
- [CROSS-15-phase-rotation-construction](research/cbb-binary/CROSS-15-phase-rotation-construction.md)
- [CROSS-16-phase-rotation-distance-bounds](research/cbb-binary/CROSS-16-phase-rotation-distance-bounds.md)
- [CROSS-17-monotone-winding-obstruction](research/cbb-binary/CROSS-17-monotone-winding-obstruction.md)
- [CROSS-18-bounded-winding-detours](research/cbb-binary/CROSS-18-bounded-winding-detours.md)
- [CROSS-19-nine-position-trap-repair](research/cbb-binary/CROSS-19-nine-position-trap-repair.md)
- [CROSS-20-repair-length-vs-winding-depth](research/cbb-binary/CROSS-20-repair-length-vs-winding-depth.md)
- [CROSS-21-orientation-sign-rewrite-rules](research/cbb-binary/CROSS-21-orientation-sign-rewrite-rules.md)
- [CROSS-22-defect-arrangement-traps](research/cbb-binary/CROSS-22-defect-arrangement-traps.md)
- [CROSS-23-defect-gap-transport](research/cbb-binary/CROSS-23-defect-gap-transport.md)
- [CROSS-24-LR4-gap-reactions](research/cbb-binary/CROSS-24-LR4-gap-reactions.md)
- [CROSS-25-bounded-defect-repair-distance](research/cbb-binary/CROSS-25-bounded-defect-repair-distance.md)
- [CROSS-26-LR4-frozen-configurations](research/cbb-binary/CROSS-26-LR4-frozen-configurations.md)
- [CROSS-27-frozen-pattern-automaton](research/cbb-binary/CROSS-27-frozen-pattern-automaton.md)
- [CROSS-28-frozen-automaton-scc-and-LR3-escape](research/cbb-binary/CROSS-28-frozen-automaton-scc-and-LR3-escape.md)
- [CROSS-29-growing-LR3-escape-depth](research/cbb-binary/CROSS-29-growing-LR3-escape-depth.md)
- [CROSS-30-linear-frozen-family-escape-depth](research/cbb-binary/CROSS-30-linear-frozen-family-escape-depth.md)
- [CROSS-31-explicit-LR3-escape-upper-bound](research/cbb-binary/CROSS-31-explicit-LR3-escape-upper-bound.md)
- [CROSS-32-escape-lower-bound-audit](research/cbb-binary/CROSS-32-escape-lower-bound-audit.md)
- [CROSS-33-three-LR3-fronts](research/cbb-binary/CROSS-33-three-LR3-fronts.md)
- [CROSS-34-LR3-causal-ancestry](research/cbb-binary/CROSS-34-LR3-causal-ancestry.md)
- [CROSS-35-triple-free-LR3-invariant](research/cbb-binary/CROSS-35-triple-free-LR3-invariant.md)
- [CROSS-36-single-front-activation](research/cbb-binary/CROSS-36-single-front-activation.md)
- [CROSS-37-pair-gap-potential-counterexample](research/cbb-binary/CROSS-37-pair-gap-potential-counterexample.md)
- [CROSS-38-cyclic-dipole-and-transport](research/cbb-binary/CROSS-38-cyclic-dipole-and-transport.md)
- [CROSS-39-equal-pair-ancestry](research/cbb-binary/CROSS-39-equal-pair-ancestry.md)
- [CROSS-40-signal-and-oscillator](research/cbb-binary/CROSS-40-signal-and-oscillator.md)
- [CROSS-41-growth-and-return](research/cbb-binary/CROSS-41-growth-and-return.md)
- [CROSS-42-resettable-return](research/cbb-binary/CROSS-42-resettable-return.md)
- [CROSS-43-local-history](research/cbb-binary/CROSS-43-local-history.md)
- [CROSS-44-cycle-record](research/cbb-binary/CROSS-44-cycle-record.md)
- [CROSS-45-fresh-reply](research/cbb-binary/CROSS-45-fresh-reply.md)
- [CROSS-46-local-clock](research/cbb-binary/CROSS-46-local-clock.md)
- [CROSS-47-reversal-bell](research/cbb-binary/CROSS-47-reversal-bell.md)
- [CROSS-48-reversal-interference](research/cbb-binary/CROSS-48-reversal-interference.md)
- [CROSS-49-route-recorder](research/cbb-binary/CROSS-49-route-recorder.md)
- [CROSS-50-cycle-apparatus](research/cbb-binary/CROSS-50-cycle-apparatus.md)
- [CROSS-51-recorder-phase](research/cbb-binary/CROSS-51-recorder-phase.md)
- [CROSS-52-setting-isolation](research/cbb-binary/CROSS-52-setting-isolation.md)
- [CROSS-53-local-phase](research/cbb-binary/CROSS-53-local-phase.md)
- [CROSS-54-local-bell](research/cbb-binary/CROSS-54-local-bell.md)
- [CROSS-55-symmetric-hopping](research/cbb-binary/CROSS-55-symmetric-hopping.md)
- [CROSS-56-diagonal-phase](research/cbb-binary/CROSS-56-diagonal-phase.md)
- [CROSS-57-growth-phase](research/cbb-binary/CROSS-57-growth-phase.md)
- [CROSS-58-growth-reference](research/cbb-binary/CROSS-58-growth-reference.md)
- [GROWTH-CLOCKS-AND-BELL](research/cbb-binary/GROWTH-CLOCKS-AND-BELL.md)
- [TRI-01-balanced-three-colour](research/cbb-binary/TRI-01-balanced-three-colour.md)
- [TRI-02-separation-sectors](research/cbb-binary/TRI-02-separation-sectors.md)
- [TRI-03-winding-conservation](research/cbb-binary/TRI-03-winding-conservation.md)
- [TRI-04-local-selection-and-arrest](research/cbb-binary/TRI-04-local-selection-and-arrest.md)
- [TRI-05-fifteen-vertex-sectors](research/cbb-binary/TRI-05-fifteen-vertex-sectors.md)
- [TRI-06-pair-count-no-go](research/cbb-binary/TRI-06-pair-count-no-go.md)
- [TRI-07-sign-word-rewrite](research/cbb-binary/TRI-07-sign-word-rewrite.md)
- [TRI-08-sign-run-audit](research/cbb-binary/TRI-08-sign-run-audit.md)
- [TRI-09-greedy-normal-form-obstruction](research/cbb-binary/TRI-09-greedy-normal-form-obstruction.md)
- [CROSS-59-growth-ratios](research/cbb-binary/CROSS-59-growth-ratios.md)
- [CROSS-60-local-growth-clock](research/cbb-binary/CROSS-60-local-growth-clock.md)
- [CROSS-61-clock-bias](research/cbb-binary/CROSS-61-clock-bias.md)
- [CROSS-62-blind-growth](research/cbb-binary/CROSS-62-blind-growth.md)
- [CROSS-63-ecoli-lineage](research/cbb-binary/CROSS-63-ecoli-lineage.md)

**`research/hamiltonian-cycle/`**

- [Guide](research/hamiltonian-cycle/README.md)
- [HC-02](research/hamiltonian-cycle/HC-02.md)
- [HC-03](research/hamiltonian-cycle/HC-03.md)
- [HC-04](research/hamiltonian-cycle/HC-04.md)
- [HC-05](research/hamiltonian-cycle/HC-05.md)
- [HC-06](research/hamiltonian-cycle/HC-06.md)
- [HC-07](research/hamiltonian-cycle/HC-07.md)
- [HC-08](research/hamiltonian-cycle/HC-08.md)
- [ANTIPRIME-CYCLE-COUNTS](research/hamiltonian-cycle/ANTIPRIME-CYCLE-COUNTS.md)

**`research/cbb-binary/reversal-building-blocks/`**

- [Guide](research/cbb-binary/reversal-building-blocks/README.md)
- [visible-phase](research/cbb-binary/reversal-building-blocks/visible-phase.md)

</details>

### Wheeler growth, entropy, and reproduction

<details>
<summary>Show 64 entries</summary>

**`code/wheeler/`**

- [Guide](code/wheeler/README.md)

**`probes/wheeler/`**

- [Guide](probes/wheeler/README.md)
- [ERRATA-01](probes/wheeler/ERRATA-01.md)
- [WHEELER-09](probes/wheeler/WHEELER-09.md)
- [WHEELER-10](probes/wheeler/WHEELER-10.md)
- [WHEELER-11](probes/wheeler/WHEELER-11.md)
- [WHEELER-12](probes/wheeler/WHEELER-12.md)
- [WHEELER-13](probes/wheeler/WHEELER-13.md)
- [WHEELER-14](probes/wheeler/WHEELER-14.md)
- [WHEELER-15](probes/wheeler/WHEELER-15.md)
- [WHEELER-16](probes/wheeler/WHEELER-16.md)
- [WHEELER-17](probes/wheeler/WHEELER-17.md)
- [WHEELER-18](probes/wheeler/WHEELER-18.md)
- [WHEELER-19](probes/wheeler/WHEELER-19.md)
- [WHEELER-20](probes/wheeler/WHEELER-20.md)
- [WHEELER-21](probes/wheeler/WHEELER-21.md)
- [WHEELER-22](probes/wheeler/WHEELER-22.md)
- [WHEELER-23](probes/wheeler/WHEELER-23.md)
- [WHEELER-24](probes/wheeler/WHEELER-24.md)
- [WHEELER-25](probes/wheeler/WHEELER-25.md)
- [WHEELER-26](probes/wheeler/WHEELER-26.md)
- [WHEELER-27](probes/wheeler/WHEELER-27.md)
- [WHEELER-28](probes/wheeler/WHEELER-28.md)
- [WHEELER-29](probes/wheeler/WHEELER-29.md)
- [WHEELER-30](probes/wheeler/WHEELER-30.md)
- [WHEELER-31](probes/wheeler/WHEELER-31.md)
- [WHEELER-32](probes/wheeler/WHEELER-32.md)
- [WHEELER-33](probes/wheeler/WHEELER-33.md)
- [WHEELER-34](probes/wheeler/WHEELER-34.md)
- [WHEELER-35](probes/wheeler/WHEELER-35.md)
- [WHEELER-36](probes/wheeler/WHEELER-36.md)
- [WHEELER-37](probes/wheeler/WHEELER-37.md)
- [WHEELER-38](probes/wheeler/WHEELER-38.md)
- [WHEELER-39](probes/wheeler/WHEELER-39.md)
- [WHEELER-40](probes/wheeler/WHEELER-40.md)
- [WHEELER-41](probes/wheeler/WHEELER-41.md)
- [WHEELER-42](probes/wheeler/WHEELER-42.md)
- [WHEELER-43](probes/wheeler/WHEELER-43.md)
- [WHEELER-44](probes/wheeler/WHEELER-44.md)
- [WHEELER-45](probes/wheeler/WHEELER-45.md)
- [WHEELER-46](probes/wheeler/WHEELER-46.md)
- [WHEELER-47](probes/wheeler/WHEELER-47.md)
- [WHEELER-48](probes/wheeler/WHEELER-48.md)
- [WHEELER-49](probes/wheeler/WHEELER-49.md)
- [WHEELER-50](probes/wheeler/WHEELER-50.md)
- [WHEELER-51](probes/wheeler/WHEELER-51.md)
- [WHEELER-52](probes/wheeler/WHEELER-52.md)
- [WHEELER-53](probes/wheeler/WHEELER-53.md)
- [WHEELER-54](probes/wheeler/WHEELER-54.md)
- [WHEELER-55](probes/wheeler/WHEELER-55.md)
- [WHEELER-56](probes/wheeler/WHEELER-56.md)
- [WHEELER-57](probes/wheeler/WHEELER-57.md)
- [WHEELER-58](probes/wheeler/WHEELER-58.md)
- [WHEELER-59](probes/wheeler/WHEELER-59.md)
- [WHEELER-60](probes/wheeler/WHEELER-60.md)
- [WHEELER-61](probes/wheeler/WHEELER-61.md)
- [WHEELER-62](probes/wheeler/WHEELER-62.md)
- [WHEELER-63](probes/wheeler/WHEELER-63.md)

**`research/wheeler/`**

- [REVIEW-01](research/wheeler/REVIEW-01.md)
- [SUMMARY-01](research/wheeler/SUMMARY-01.md)

**`research/wheeler/paper-v0.1/`**

- [Guide](research/wheeler/paper-v0.1/README.md)
- [entropy-and-symmetry-v0.1.pdf](research/wheeler/paper-v0.1/entropy-and-symmetry-v0.1.pdf)
- [LITERATURE-COMPARISON](research/wheeler/paper-v0.1/LITERATURE-COMPARISON.md)
- [manuscript](research/wheeler/paper-v0.1/manuscript.md)

</details>

### MICRO growth, observers, and Julstce

<details>
<summary>Show 4 entries</summary>

**`probes/micro/julstce/`**

- [Guide](probes/micro/julstce/README.md)
- [Memory under four-slot reversals](probes/micro/julstce/reversals/README.md)

**`probes/micro/observer-compatibility-01/`**

- [Guide](probes/micro/observer-compatibility-01/README.md)
- [REPORT](probes/micro/observer-compatibility-01/REPORT.md)

</details>

### Reversal rules, winding, and holonomy

<details>
<summary>Show 19 entries</summary>

**`probes/reversals/`**

- [Guide](probes/reversals/README.md)

**`probes/reversals/all-length-01/`**

- [Guide](probes/reversals/all-length-01/README.md)

**`probes/reversals/assembly-gate-03/`**

- [Guide](probes/reversals/assembly-gate-03/README.md)

**`probes/reversals/carrier-audit-07/`**

- [Guide](probes/reversals/carrier-audit-07/README.md)

**`probes/reversals/ehf-rev-01/`**

- [Guide](probes/reversals/ehf-rev-01/README.md)

**`probes/reversals/ehf-rev-02/`**

- [Guide](probes/reversals/ehf-rev-02/README.md)

**`probes/reversals/ehf-rev-03/`**

- [Guide](probes/reversals/ehf-rev-03/README.md)

**`probes/reversals/ehf-rev-04/`**

- [Guide](probes/reversals/ehf-rev-04/README.md)

**`probes/reversals/event-groupoid-14/`**

- [Guide](probes/reversals/event-groupoid-14/README.md)

**`probes/reversals/exhaustive-returns-08/`**

- [Guide](probes/reversals/exhaustive-returns-08/README.md)

**`probes/reversals/growth-lift-09/`**

- [Guide](probes/reversals/growth-lift-09/README.md)

**`probes/reversals/growth-lift-10/`**

- [Guide](probes/reversals/growth-lift-10/README.md)

**`probes/reversals/growth-lift-11/`**

- [Guide](probes/reversals/growth-lift-11/README.md)

**`probes/reversals/growth-lift-12/`**

- [Guide](probes/reversals/growth-lift-12/README.md)

**`probes/reversals/local-reconnect-04/`**

- [Guide](probes/reversals/local-reconnect-04/README.md)

**`probes/reversals/orientation-holonomy-13/`**

- [Guide](probes/reversals/orientation-holonomy-13/README.md)

**`probes/reversals/pi-closure-06/`**

- [Guide](probes/reversals/pi-closure-06/README.md)

**`probes/reversals/rare-channel-02/`**

- [Guide](probes/reversals/rare-channel-02/README.md)

**`probes/reversals/tagged-controller-05/`**

- [Guide](probes/reversals/tagged-controller-05/README.md)

</details>

### Dimensions and geometry

<details>
<summary>Show 9 entries</summary>

**`probes/dimensions/ehf-dim-01/`**

- [Guide](probes/dimensions/ehf-dim-01/README.md)

**`probes/dimensions/ehf-dim-02/`**

- [Guide](probes/dimensions/ehf-dim-02/README.md)

**`probes/dimensions/ehf-dim-03/`**

- [Guide](probes/dimensions/ehf-dim-03/README.md)

**`probes/dimensions/ehf-dim-04/`**

- [Guide](probes/dimensions/ehf-dim-04/README.md)

**`probes/dimensions/ehf-dim-05/`**

- [Guide](probes/dimensions/ehf-dim-05/README.md)

**`probes/dimensions/ehf-dim-06/`**

- [Guide](probes/dimensions/ehf-dim-06/README.md)

**`probes/dimensions/ehf-dim-07/`**

- [Guide](probes/dimensions/ehf-dim-07/README.md)

**`probes/dimensions/ehf-dim-08/`**

- [Guide](probes/dimensions/ehf-dim-08/README.md)

**`probes/dimensions/ehf-dim-09/`**

- [Guide](probes/dimensions/ehf-dim-09/README.md)

</details>

### Quantum comparisons and signed graphs

<details>
<summary>Show 22 entries</summary>

**`probes/qm-bridge/`**

- [Guide](probes/qm-bridge/README.md)

**`probes/qm-bridge/revisit-01/`**

- [Guide](probes/qm-bridge/revisit-01/README.md)
- [REPORT](probes/qm-bridge/revisit-01/REPORT.md)

**`probes/qm-bridge/revisit-01/sources/`**

- [00_Emergent Horizon Framework (EHF)_ehf_qm_bridge_program_v5_qm09c_qm12_documented](probes/qm-bridge/revisit-01/sources/00_Emergent%20Horizon%20Framework%20%28EHF%29_ehf_qm_bridge_program_v5_qm09c_qm12_documented.md)
- [01_observer_audit_07_REPORT](probes/qm-bridge/revisit-01/sources/01_observer_audit_07_REPORT.md)
- [02_observer_audit_08_REPORT](probes/qm-bridge/revisit-01/sources/02_observer_audit_08_REPORT.md)
- [03_observer_audit_09_REPORT](probes/qm-bridge/revisit-01/sources/03_observer_audit_09_REPORT.md)
- [04_observer_audit_10_REPORT](probes/qm-bridge/revisit-01/sources/04_observer_audit_10_REPORT.md)
- [05_probe_access_01_REPORT](probes/qm-bridge/revisit-01/sources/05_probe_access_01_REPORT.md)
- [06_micro_opw_02_README](probes/qm-bridge/revisit-01/sources/06_micro_opw_02_README.md)
- [07_micro_opw_01_README](probes/qm-bridge/revisit-01/sources/07_micro_opw_01_README.md)
- [08_micro_opw_03_README](probes/qm-bridge/revisit-01/sources/08_micro_opw_03_README.md)

**`probes/qm-bridge/revisit-02/`**

- [Guide](probes/qm-bridge/revisit-02/README.md)
- [REPORT](probes/qm-bridge/revisit-02/REPORT.md)

**`probes/qm-bridge/revisit-03/`**

- [Guide](probes/qm-bridge/revisit-03/README.md)
- [RANDOM-GRAPHS](probes/qm-bridge/revisit-03/RANDOM-GRAPHS.md)
- [REPORT](probes/qm-bridge/revisit-03/REPORT.md)

**`research/signed-graph-reconstruction/`**

- [Guide](research/signed-graph-reconstruction/README.md)
- [SIGN-01](research/signed-graph-reconstruction/SIGN-01.md)
- [SIGN-02](research/signed-graph-reconstruction/SIGN-02.md)
- [SIGN-03](research/signed-graph-reconstruction/SIGN-03.md)

**`probes/qm-bridge/label-parity/`**

- [Guide](probes/qm-bridge/label-parity/README.md)

</details>

### Amplitudes, ordering, and collinear colour

<details>
<summary>Show 68 entries</summary>

**`research/amplitudes/`**

- [Guide](research/amplitudes/README.md)
- [ordering-orientation-bridge-01](research/amplitudes/ordering-orientation-bridge-01.md)

**`research/amplitudes/collinear-colour/`**

- [Guide](research/amplitudes/collinear-colour/README.md)
- [angular-ensemble](research/amplitudes/collinear-colour/angular-ensemble.md)
- [atlas-lost-lepton-audit](research/amplitudes/collinear-colour/atlas-lost-lepton-audit.md)
- [channel-orders](research/amplitudes/collinear-colour/channel-orders.md)
- [electroweak-helicities](research/amplitudes/collinear-colour/electroweak-helicities.md)
- [electroweak-pair-scale](research/amplitudes/collinear-colour/electroweak-pair-scale.md)
- [electroweak-photon-decays](research/amplitudes/collinear-colour/electroweak-photon-decays.md)
- [electroweak-photon-initial](research/amplitudes/collinear-colour/electroweak-photon-initial.md)
- [electroweak-photon-longitudinal](research/amplitudes/collinear-colour/electroweak-photon-longitudinal.md)
- [electroweak-photon-patch](research/amplitudes/collinear-colour/electroweak-photon-patch.md)
- [electroweak-photon-reconstruction](research/amplitudes/collinear-colour/electroweak-photon-reconstruction.md)
- [electroweak-rate](research/amplitudes/collinear-colour/electroweak-rate.md)
- [electroweak-scale](research/amplitudes/collinear-colour/electroweak-scale.md)
- [literature](research/amplitudes/collinear-colour/literature.md)
- [lorentzian-counterexample](research/amplitudes/collinear-colour/lorentzian-counterexample.md)
- [matched-radiation](research/amplitudes/collinear-colour/matched-radiation.md)
- [near-planar-seven](research/amplitudes/collinear-colour/near-planar-seven.md)
- [near-planar-sign](research/amplitudes/collinear-colour/near-planar-sign.md)
- [pair-dipole](research/amplitudes/collinear-colour/pair-dipole.md)
- [planar-theorem](research/amplitudes/collinear-colour/planar-theorem.md)
- [plane-scan](research/amplitudes/collinear-colour/plane-scan.md)
- [pole-control](research/amplitudes/collinear-colour/pole-control.md)
- [shape-average](research/amplitudes/collinear-colour/shape-average.md)
- [six-soft](research/amplitudes/collinear-colour/six-soft.md)
- [soft-emission](research/amplitudes/collinear-colour/soft-emission.md)
- [su-n-casimir-law](research/amplitudes/collinear-colour/su-n-casimir-law.md)
- [su2-basis](research/amplitudes/collinear-colour/su2-basis.md)
- [su2-control](research/amplitudes/collinear-colour/su2-control.md)
- [su2-electroweak-limit](research/amplitudes/collinear-colour/su2-electroweak-limit.md)
- [su2-incoming-average](research/amplitudes/collinear-colour/su2-incoming-average.md)
- [su2-incoming-rotation](research/amplitudes/collinear-colour/su2-incoming-rotation.md)
- [su2-mass-control](research/amplitudes/collinear-colour/su2-mass-control.md)
- [su2-rate](research/amplitudes/collinear-colour/su2-rate.md)
- [su2-ratio](research/amplitudes/collinear-colour/su2-ratio.md)
- [su2-real-rate](research/amplitudes/collinear-colour/su2-real-rate.md)
- [su3-channels](research/amplitudes/collinear-colour/su3-channels.md)
- [tracking-radiation](research/amplitudes/collinear-colour/tracking-radiation.md)
- [weighted-angles](research/amplitudes/collinear-colour/weighted-angles.md)

**`research/amplitudes/nine-point-tail/`**

- [Guide](research/amplitudes/nine-point-tail/README.md)
- [theorem-v1.5](research/amplitudes/nine-point-tail/theorem-v1.5.md)

**`research/amplitudes/nine-point-tail/followups/`**

- [Guide](research/amplitudes/nine-point-tail/followups/README.md)
- [benchmark](research/amplitudes/nine-point-tail/followups/benchmark.md)
- [boundary](research/amplitudes/nine-point-tail/followups/boundary.md)
- [branches](research/amplitudes/nine-point-tail/followups/branches.md)
- [common-cut-holdout](research/amplitudes/nine-point-tail/followups/common-cut-holdout.md)
- [Lifts](research/amplitudes/nine-point-tail/followups/Lifts.md)
- [mixed-orbits](research/amplitudes/nine-point-tail/followups/mixed-orbits.md)
- [ordering-geometry](research/amplitudes/nine-point-tail/followups/ordering-geometry.md)
- [orientation](research/amplitudes/nine-point-tail/followups/orientation.md)
- [position-family-trace](research/amplitudes/nine-point-tail/followups/position-family-trace.md)
- [rank14-event-pairs](research/amplitudes/nine-point-tail/followups/rank14-event-pairs.md)
- [rank14-lr3-threshold](research/amplitudes/nine-point-tail/followups/rank14-lr3-threshold.md)
- [rank14-minimal-triples](research/amplitudes/nine-point-tail/followups/rank14-minimal-triples.md)
- [rank14](research/amplitudes/nine-point-tail/followups/rank14.md)
- [replacement-trace](research/amplitudes/nine-point-tail/followups/replacement-trace.md)
- [sector-selection](research/amplitudes/nine-point-tail/followups/sector-selection.md)
- [sector-threshold](research/amplitudes/nine-point-tail/followups/sector-threshold.md)
- [shared-lifts](research/amplitudes/nine-point-tail/followups/shared-lifts.md)
- [shared-residue-rule](research/amplitudes/nine-point-tail/followups/shared-residue-rule.md)
- [shuffle-doubles](research/amplitudes/nine-point-tail/followups/shuffle-doubles.md)
- [shuffle-sectors](research/amplitudes/nine-point-tail/followups/shuffle-sectors.md)
- [signed-orientation-bridge](research/amplitudes/nine-point-tail/followups/signed-orientation-bridge.md)
- [support-reduction](research/amplitudes/nine-point-tail/followups/support-reduction.md)
- [support-sector-test](research/amplitudes/nine-point-tail/followups/support-sector-test.md)
- [tail-shuffle-trace](research/amplitudes/nine-point-tail/followups/tail-shuffle-trace.md)
- [union-cancellation-rule](research/amplitudes/nine-point-tail/followups/union-cancellation-rule.md)

</details>

### Collatz

<details>
<summary>Show 28 entries</summary>

**`probes/collatz/adaptive-merge-18/`**

- [Guide](probes/collatz/adaptive-merge-18/README.md)

**`probes/collatz/backward-terminal-14/`**

- [Guide](probes/collatz/backward-terminal-14/README.md)

**`probes/collatz/cofactor-avoidance-24/`**

- [Guide](probes/collatz/cofactor-avoidance-24/README.md)

**`probes/collatz/cofactor-frequency-25/`**

- [Guide](probes/collatz/cofactor-frequency-25/README.md)

**`probes/collatz/cofactor-observer-26/`**

- [Guide](probes/collatz/cofactor-observer-26/README.md)

**`probes/collatz/cofactor-one-classification-28/`**

- [Guide](probes/collatz/cofactor-one-classification-28/README.md)

**`probes/collatz/cofactor-pair-lifts-27/`**

- [Guide](probes/collatz/cofactor-pair-lifts-27/README.md)

**`probes/collatz/cofactor-returns-23/`**

- [Guide](probes/collatz/cofactor-returns-23/README.md)

**`probes/collatz/escape-tail-15/`**

- [Guide](probes/collatz/escape-tail-15/README.md)

**`probes/collatz/expanding-pieces-20/`**

- [Guide](probes/collatz/expanding-pieces-20/README.md)

**`probes/collatz/fast-residues-12/`**

- [Guide](probes/collatz/fast-residues-12/README.md)

**`probes/collatz/joint-window-13/`**

- [Guide](probes/collatz/joint-window-13/README.md)

**`probes/collatz/merge-coverage-19/`**

- [Guide](probes/collatz/merge-coverage-19/README.md)

**`probes/collatz/multiplier-band-05/`**

- [Guide](probes/collatz/multiplier-band-05/README.md)

**`probes/collatz/odd-run-join-22/`**

- [Guide](probes/collatz/odd-run-join-22/README.md)

**`probes/collatz/offset-bound-04/`**

- [Guide](probes/collatz/offset-bound-04/README.md)

**`probes/collatz/orbit-height-10/`**

- [Guide](probes/collatz/orbit-height-10/README.md)

**`probes/collatz/parity-complexity-06/`**

- [Guide](probes/collatz/parity-complexity-06/README.md)

**`probes/collatz/parity-descent-02/`**

- [Guide](probes/collatz/parity-descent-02/README.md)

**`probes/collatz/planted-orbit-21/`**

- [Guide](probes/collatz/planted-orbit-21/README.md)

**`probes/collatz/regular-growth-09/`**

- [Guide](probes/collatz/regular-growth-09/README.md)

**`probes/collatz/repetition-budget-11/`**

- [Guide](probes/collatz/repetition-budget-11/README.md)

**`probes/collatz/residue-size-07/`**

- [Guide](probes/collatz/residue-size-07/README.md)

**`probes/collatz/residue-stabilisation-08/`**

- [Guide](probes/collatz/residue-stabilisation-08/README.md)

**`probes/collatz/smaller-merge-17/`**

- [Guide](probes/collatz/smaller-merge-17/README.md)

**`probes/collatz/survival-count-16/`**

- [Guide](probes/collatz/survival-count-16/README.md)

**`probes/collatz/survivor-branches-03/`**

- [Guide](probes/collatz/survivor-branches-03/README.md)

**`research/collatz/`**

- [Guide](research/collatz/README.md)

</details>

### Wieferich primes and modular cycles

<details>
<summary>Show 1 entries</summary>

**`research/wieferich/EHF-WIEF-02/`**

- [Guide](research/wieferich/EHF-WIEF-02/README.md)

</details>

### Source documents, related work, and archives

<details>
<summary>Show 23 entries</summary>

**`archive/`**

- [Archive guide](archive/README.md)

**`code/`**

- [Code directory guide](code/README.md)

**`data/`**

- [Data directory guide](data/README.md)

**`research/`**

- [Research directory guide](research/README.md)

**`research/related-work/`**

- [Guide](research/related-work/README.md)

**`research/related-work/2026-10-30-boundary-reconstruction/`**

- [Guide](research/related-work/2026-10-30-boundary-reconstruction/README.md)

**`research/related-work/2026-10-30-cycle-aware-boundary/`**

- [Guide](research/related-work/2026-10-30-cycle-aware-boundary/README.md)

**`research/related-work/2026-10-30-detection-access/`**

- [Guide](research/related-work/2026-10-30-detection-access/README.md)

**`research/related-work/2026-10-30-history-heralding/`**

- [Guide](research/related-work/2026-10-30-history-heralding/README.md)

**`research/related-work/2026-10-30-kazazi-reconfiguration/`**

- [Guide](research/related-work/2026-10-30-kazazi-reconfiguration/README.md)
- [RESULTS](research/related-work/2026-10-30-kazazi-reconfiguration/RESULTS.md)

**`research/source-documents/`**

- [Guide](research/source-documents/README.md)
- [amp-historical.pdf](research/source-documents/amp-historical.pdf)
- [hc-grow-v0.8](research/source-documents/hc-grow-v0.8.md)
- [hc-raw-v0.19](research/source-documents/hc-raw-v0.19.md)
- [johnson-ollivier-curvature-v1](research/source-documents/johnson-ollivier-curvature-v1.md)
- [johnson-transport-original.pdf](research/source-documents/johnson-transport-original.pdf)
- [opw3-v0.6](research/source-documents/opw3-v0.6.md)
- [opw3-v1.1](research/source-documents/opw3-v1.1.md)
- [opw23-v6](research/source-documents/opw23-v6.md)
- [pancakes.pdf](research/source-documents/pancakes.pdf)
- [phys-alg-v0.65](research/source-documents/phys-alg-v0.65.md)
- [qm-bridge-historical.pdf](research/source-documents/qm-bridge-historical.pdf)

</details>

### Recovered sources and MICRO–OPW

<details>
<summary>Show 140 entries</summary>

**`probes/micro-opw/micro_opw_01/`**

- [Guide](probes/micro-opw/micro_opw_01/README.md)

**`probes/micro-opw/micro_opw_02/`**

- [Guide](probes/micro-opw/micro_opw_02/README.md)

**`probes/micro-opw/micro_opw_03/`**

- [Guide](probes/micro-opw/micro_opw_03/README.md)

**`probes/micro-opw/`**

- [Guide](probes/micro-opw/README.md)

**`research/amplitudes/foundation/`**

- [Guide](research/amplitudes/foundation/README.md)

**`research/amplitudes/foundation/sources/`**

- [ehf_amp_found_01_anchor_relative_scaffolds_v0_1](research/amplitudes/foundation/sources/ehf_amp_found_01_anchor_relative_scaffolds_v0_1.md)
- [ehf_amp_found_01_anchor_relative_scaffolds_v0_2](research/amplitudes/foundation/sources/ehf_amp_found_01_anchor_relative_scaffolds_v0_2.md)
- [ehf_amp_found_01_anchor_relative_scaffolds_v0_3](research/amplitudes/foundation/sources/ehf_amp_found_01_anchor_relative_scaffolds_v0_3.md)
- [ehf_amp_found_01_anchor_relative_scaffolds_v0_4](research/amplitudes/foundation/sources/ehf_amp_found_01_anchor_relative_scaffolds_v0_4.md)
- [ehf_amp_found_01_anchor_relative_scaffolds_v0_5](research/amplitudes/foundation/sources/ehf_amp_found_01_anchor_relative_scaffolds_v0_5.md)
- [ehf_amp_found_01_anchor_relative_scaffolds_v0_6](research/amplitudes/foundation/sources/ehf_amp_found_01_anchor_relative_scaffolds_v0_6.md)
- [ehf_amp_found_01b_claude_comparison_audit](research/amplitudes/foundation/sources/ehf_amp_found_01b_claude_comparison_audit.md)
- [ehf_amp_found_01b_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_01b_probe_spec.md)
- [ehf_amp_found_02a_orientation_and_vacuity_audit](research/amplitudes/foundation/sources/ehf_amp_found_02a_orientation_and_vacuity_audit.md)
- [ehf_amp_found_02a_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_02a_probe_spec.md)
- [ehf_amp_found_02a_probe_spec_v0_2](research/amplitudes/foundation/sources/ehf_amp_found_02a_probe_spec_v0_2.md)
- [ehf_amp_found_02b_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_02b_probe_spec.md)
- [ehf_amp_found_02c_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_02c_probe_spec.md)
- [ehf_amp_found_02d_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_02d_probe_spec.md)
- [ehf_amp_found_02e_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_02e_probe_spec.md)
- [ehf_amp_found_02f_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_02f_probe_spec.md)
- [ehf_amp_found_02g_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_02g_probe_spec.md)
- [ehf_amp_found_02h_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_02h_probe_spec.md)
- [ehf_amp_found_03a_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_03a_probe_spec.md)
- [ehf_amp_found_03b_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_03b_probe_spec.md)
- [ehf_amp_found_03c_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_03c_probe_spec.md)
- [ehf_amp_found_03d_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_03d_probe_spec.md)
- [ehf_amp_found_03e_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_03e_probe_spec.md)
- [ehf_amp_found_03f_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_03f_probe_spec.md)
- [ehf_amp_found_03g_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_03g_probe_spec.md)
- [ehf_amp_found_03h_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_03h_probe_spec.md)
- [ehf_amp_found_03i_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_03i_probe_spec.md)
- [ehf_amp_found_03j_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_03j_probe_spec.md)
- [ehf_amp_found_03k_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_03k_probe_spec.md)
- [ehf_amp_found_03l_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_03l_probe_spec.md)
- [ehf_amp_found_04a_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_04a_probe_spec.md)
- [ehf_amp_found_04a_result_audit](research/amplitudes/foundation/sources/ehf_amp_found_04a_result_audit.md)
- [ehf_amp_found_04b_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_04b_probe_spec.md)
- [ehf_amp_found_04c_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_04c_probe_spec.md)
- [ehf_amp_found_04c_t0_probe_spec](research/amplitudes/foundation/sources/ehf_amp_found_04c_t0_probe_spec.md)

**`research/consolidation-2026-11-02/`**

- [Guide](research/consolidation-2026-11-02/README.md)

**`research/hc-grow/audits/`**

- [EHF_GROW02_LR3_ONSET_SUPPORT_LIMIT_AUDIT_v0_2](research/hc-grow/audits/EHF_GROW02_LR3_ONSET_SUPPORT_LIMIT_AUDIT_v0_2.md)
- [EHF_GROW02_POLYA_SUPPORT_LIMIT_AUDIT_v0_1](research/hc-grow/audits/EHF_GROW02_POLYA_SUPPORT_LIMIT_AUDIT_v0_1.md)

**`research/hc-grow/`**

- [Guide](research/hc-grow/README.md)

**`research/hc-grow/sources/`**

- [ehf_hc_grow_01_reversal_support_propagation_multi_layer](research/hc-grow/sources/ehf_hc_grow_01_reversal_support_propagation_multi_layer.md)
- [ehf_hc_grow_02_reversal_support_branching_operator](research/hc-grow/sources/ehf_hc_grow_02_reversal_support_branching_operator.md)
- [ehf_hc_grow_03a_branching_operator_intrinsic_parity_sectors](research/hc-grow/sources/ehf_hc_grow_03a_branching_operator_intrinsic_parity_sectors.md)
- [ehf_hc_grow_04_selected_lr3_stability_under_growth](research/hc-grow/sources/ehf_hc_grow_04_selected_lr3_stability_under_growth.md)
- [ehf_hc_grow_05_general_selected_support_renewal](research/hc-grow/sources/ehf_hc_grow_05_general_selected_support_renewal.md)
- [ehf_hc_grow_06_reversal_support_channel_atlas](research/hc-grow/sources/ehf_hc_grow_06_reversal_support_channel_atlas.md)
- [ehf_hc_grow_07_internal_channel_geometry](research/hc-grow/sources/ehf_hc_grow_07_internal_channel_geometry.md)
- [ehf_hc_grow_08_cross_channel_loop_coupling_geometry](research/hc-grow/sources/ehf_hc_grow_08_cross_channel_loop_coupling_geometry.md)
- [ehf_hc_grow_working_document_v0_1](research/hc-grow/sources/ehf_hc_grow_working_document_v0_1.md)
- [ehf_hc_grow_working_document_v0_2](research/hc-grow/sources/ehf_hc_grow_working_document_v0_2.md)
- [ehf_hc_grow_working_document_v0_3](research/hc-grow/sources/ehf_hc_grow_working_document_v0_3.md)
- [ehf_hc_grow_working_document_v0_4](research/hc-grow/sources/ehf_hc_grow_working_document_v0_4.md)
- [ehf_hc_grow_working_document_v0_5](research/hc-grow/sources/ehf_hc_grow_working_document_v0_5.md)
- [ehf_hc_grow_working_document_v0_6](research/hc-grow/sources/ehf_hc_grow_working_document_v0_6.md)
- [ehf_hc_grow_working_document_v0_7](research/hc-grow/sources/ehf_hc_grow_working_document_v0_7.md)
- [ehf_hc_grow_working_document_v0_8](research/hc-grow/sources/ehf_hc_grow_working_document_v0_8.md)
- [ehf_hc_grow_working_document_v0_8__snapshot_b810be8dec](research/hc-grow/sources/ehf_hc_grow_working_document_v0_8__snapshot_b810be8dec.md)

**`research/hc-raw/`**

- [Guide](research/hc-raw/README.md)

**`research/hc-raw/sources/`**

- [ehf_hc_raw_10f_cdf_one_defect_proof_queue_v0_1](research/hc-raw/sources/ehf_hc_raw_10f_cdf_one_defect_proof_queue_v0_1.md)
- [ehf_hc_raw_12_pre_hamilton_substrate_growth_definition_lock](research/hc-raw/sources/ehf_hc_raw_12_pre_hamilton_substrate_growth_definition_lock.md)
- [ehf_hc_raw_13_graded_hc_compatibility_naturality](research/hc-raw/sources/ehf_hc_raw_13_graded_hc_compatibility_naturality.md)
- [ehf_hc_raw_14_primitive_redundancy_dependency_minimality](research/hc-raw/sources/ehf_hc_raw_14_primitive_redundancy_dependency_minimality.md)
- [ehf_hc_raw_working_document_v0_1](research/hc-raw/sources/ehf_hc_raw_working_document_v0_1.md)
- [ehf_hc_raw_working_document_v0_10](research/hc-raw/sources/ehf_hc_raw_working_document_v0_10.md)
- [ehf_hc_raw_working_document_v0_11](research/hc-raw/sources/ehf_hc_raw_working_document_v0_11.md)
- [ehf_hc_raw_working_document_v0_12](research/hc-raw/sources/ehf_hc_raw_working_document_v0_12.md)
- [ehf_hc_raw_working_document_v0_13](research/hc-raw/sources/ehf_hc_raw_working_document_v0_13.md)
- [ehf_hc_raw_working_document_v0_14](research/hc-raw/sources/ehf_hc_raw_working_document_v0_14.md)
- [ehf_hc_raw_working_document_v0_15](research/hc-raw/sources/ehf_hc_raw_working_document_v0_15.md)
- [ehf_hc_raw_working_document_v0_16](research/hc-raw/sources/ehf_hc_raw_working_document_v0_16.md)
- [ehf_hc_raw_working_document_v0_17](research/hc-raw/sources/ehf_hc_raw_working_document_v0_17.md)
- [ehf_hc_raw_working_document_v0_18](research/hc-raw/sources/ehf_hc_raw_working_document_v0_18.md)
- [ehf_hc_raw_working_document_v0_19](research/hc-raw/sources/ehf_hc_raw_working_document_v0_19.md)
- [ehf_hc_raw_working_document_v0_2](research/hc-raw/sources/ehf_hc_raw_working_document_v0_2.md)
- [ehf_hc_raw_working_document_v0_20](research/hc-raw/sources/ehf_hc_raw_working_document_v0_20.md)
- [ehf_hc_raw_working_document_v0_3](research/hc-raw/sources/ehf_hc_raw_working_document_v0_3.md)
- [ehf_hc_raw_working_document_v0_4](research/hc-raw/sources/ehf_hc_raw_working_document_v0_4.md)
- [ehf_hc_raw_working_document_v0_5](research/hc-raw/sources/ehf_hc_raw_working_document_v0_5.md)
- [ehf_hc_raw_working_document_v0_6](research/hc-raw/sources/ehf_hc_raw_working_document_v0_6.md)
- [ehf_hc_raw_working_document_v0_7](research/hc-raw/sources/ehf_hc_raw_working_document_v0_7.md)
- [ehf_hc_raw_working_document_v0_8](research/hc-raw/sources/ehf_hc_raw_working_document_v0_8.md)
- [ehf_hc_raw_working_document_v0_9](research/hc-raw/sources/ehf_hc_raw_working_document_v0_9.md)

**`research/opw-amp-bridge/`**

- [Guide](research/opw-amp-bridge/README.md)

**`research/opw-amp-bridge/sources/`**

- [ehf_xbr_01_probe_spec](research/opw-amp-bridge/sources/ehf_xbr_01_probe_spec.md)
- [ehf_xbr_02_probe_spec](research/opw-amp-bridge/sources/ehf_xbr_02_probe_spec.md)
- [ehf_xbr_02_result_note](research/opw-amp-bridge/sources/ehf_xbr_02_result_note.md)
- [ehf_xbr_03_probe_spec](research/opw-amp-bridge/sources/ehf_xbr_03_probe_spec.md)
- [ehf_xbr_03_result_note](research/opw-amp-bridge/sources/ehf_xbr_03_result_note.md)
- [ehf_xbr_04_probe_spec](research/opw-amp-bridge/sources/ehf_xbr_04_probe_spec.md)
- [ehf_xbr_04_result_note](research/opw-amp-bridge/sources/ehf_xbr_04_result_note.md)
- [ehf_xbr_04b_probe_spec](research/opw-amp-bridge/sources/ehf_xbr_04b_probe_spec.md)
- [ehf_xbr_04c_probe_spec](research/opw-amp-bridge/sources/ehf_xbr_04c_probe_spec.md)
- [ehf_xbr_04f4_probe_spec](research/opw-amp-bridge/sources/ehf_xbr_04f4_probe_spec.md)
- [ehf_xbr_04f7_probe_spec](research/opw-amp-bridge/sources/ehf_xbr_04f7_probe_spec.md)
- [ehf_xbr_04f8_probe_spec](research/opw-amp-bridge/sources/ehf_xbr_04f8_probe_spec.md)
- [ehf_xbr_04f8b_probe_spec](research/opw-amp-bridge/sources/ehf_xbr_04f8b_probe_spec.md)
- [ehf_xbr_04f_probe_spec](research/opw-amp-bridge/sources/ehf_xbr_04f_probe_spec.md)
- [ehf_xbr_04f_to_04f8_result_note](research/opw-amp-bridge/sources/ehf_xbr_04f_to_04f8_result_note.md)
- [ehf_xbr_04f_to_04f8b_result_note](research/opw-amp-bridge/sources/ehf_xbr_04f_to_04f8b_result_note.md)
- [ehf_xbr_05a_05c_null_channel_holonomy_classification_result](research/opw-amp-bridge/sources/ehf_xbr_05a_05c_null_channel_holonomy_classification_result.md)
- [ehf_xbr_05a_probe_spec](research/opw-amp-bridge/sources/ehf_xbr_05a_probe_spec.md)
- [ehf_xbr_05b_probe_spec](research/opw-amp-bridge/sources/ehf_xbr_05b_probe_spec.md)
- [ehf_xbr_05c_probe_spec](research/opw-amp-bridge/sources/ehf_xbr_05c_probe_spec.md)

**`research/opw/qm3/`**

- [Guide](research/opw/qm3/README.md)

**`research/opw/qm3/sources/`**

- [ehf_qm3_01_probe_spec](research/opw/qm3/sources/ehf_qm3_01_probe_spec.md)
- [ehf_qm3_02_probe_spec](research/opw/qm3/sources/ehf_qm3_02_probe_spec.md)
- [ehf_qm3_03_probe_spec](research/opw/qm3/sources/ehf_qm3_03_probe_spec.md)
- [ehf_qm3_04_probe_spec](research/opw/qm3/sources/ehf_qm3_04_probe_spec.md)
- [ehf_qm3_05_probe_spec](research/opw/qm3/sources/ehf_qm3_05_probe_spec.md)

**`research/opw/`**

- [Guide](research/opw/README.md)

**`research/opw/sources/`**

- [ehf_opw3_audit_01_probe_spec](research/opw/sources/ehf_opw3_audit_01_probe_spec.md)
- [ehf_opw3_audit_02_probe_spec](research/opw/sources/ehf_opw3_audit_02_probe_spec.md)
- [ehf_opw3_audit_03_probe_spec](research/opw/sources/ehf_opw3_audit_03_probe_spec.md)
- [ehf_opw3_audit_04_probe_spec](research/opw/sources/ehf_opw3_audit_04_probe_spec.md)
- [ehf_opw3_audit_05_probe_spec](research/opw/sources/ehf_opw3_audit_05_probe_spec.md)
- [ehf_opw3_audit_06_fix_note](research/opw/sources/ehf_opw3_audit_06_fix_note.md)
- [ehf_opw3_audit_06_probe_spec](research/opw/sources/ehf_opw3_audit_06_probe_spec.md)
- [ehf_opw3_audit_07_probe_spec](research/opw/sources/ehf_opw3_audit_07_probe_spec.md)
- [ehf_opw3_audit_08_probe_spec](research/opw/sources/ehf_opw3_audit_08_probe_spec.md)
- [ehf_opw3_audit_09_probe_spec](research/opw/sources/ehf_opw3_audit_09_probe_spec.md)
- [ehf_opw3_audit_10_probe_spec](research/opw/sources/ehf_opw3_audit_10_probe_spec.md)
- [ehf_opw3_rebuild_working_document_v0_1](research/opw/sources/ehf_opw3_rebuild_working_document_v0_1.md)
- [ehf_opw3_rebuild_working_document_v0_2](research/opw/sources/ehf_opw3_rebuild_working_document_v0_2.md)
- [ehf_opw3_rebuild_working_document_v0_3](research/opw/sources/ehf_opw3_rebuild_working_document_v0_3.md)
- [ehf_opw3_rebuild_working_document_v0_4](research/opw/sources/ehf_opw3_rebuild_working_document_v0_4.md)
- [ehf_opw3_rebuild_working_document_v0_5](research/opw/sources/ehf_opw3_rebuild_working_document_v0_5.md)
- [ehf_opw3_rebuild_working_document_v0_6](research/opw/sources/ehf_opw3_rebuild_working_document_v0_6.md)
- [ehf_opw3_rebuild_working_document_v0_7](research/opw/sources/ehf_opw3_rebuild_working_document_v0_7.md)
- [ehf_opw3_rebuild_working_document_v0_8](research/opw/sources/ehf_opw3_rebuild_working_document_v0_8.md)
- [ehf_opw3_rebuild_working_document_v0_9](research/opw/sources/ehf_opw3_rebuild_working_document_v0_9.md)
- [ehf_opw3_rebuild_working_document_v1_1](research/opw/sources/ehf_opw3_rebuild_working_document_v1_1.md)
- [ehf_opw3_rebuild_working_document_v1_2](research/opw/sources/ehf_opw3_rebuild_working_document_v1_2.md)
- [ehf_opw3_rebuild_working_document_v1_4](research/opw/sources/ehf_opw3_rebuild_working_document_v1_4.md)
- [ehf_opw3_rebuild_working_document_v1_5](research/opw/sources/ehf_opw3_rebuild_working_document_v1_5.md)
- [ehf_opw3_rebuild_working_document_v1_6](research/opw/sources/ehf_opw3_rebuild_working_document_v1_6.md)
- [raf_odd_preserve_world_chamber_and_boundary_dynamics_v6](research/opw/sources/raf_odd_preserve_world_chamber_and_boundary_dynamics_v6.md)

</details>
