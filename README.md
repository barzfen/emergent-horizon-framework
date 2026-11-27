# Emergent Horizon Framework (EHF)

EHF is an exploratory mathematical-physics research programme. It starts with configurations and allowed changes, then asks what structure follows from the histories those changes generate. The work spans combinatorics, graph dynamics, statistical models of growth and memory, and comparisons with established physics. A result about a mathematical model carries the assumptions of that model.

## Start here

| If you want to… | Read |
| --- | --- |
| Understand what EHF assumes and how the projects fit together | [Foundations](foundation/README.md) and the [connections map](research/foundations/CONNECTIONS-01.md) |
| See what a concrete result looks like | [Julstce: reading detector order after growth](probes/micro/julstce/README.md). Two reversal orders can produce the same statistics for every sequence of added colours while leaving different traces in the final ring shape. |
| Find machine-checked mathematics | [Lean 4 verification](formal/lean/README.md), including binary edge splitting and all-slot Hamiltonian-cycle growth with unique ordered ancestry |
| See the programme assessment and open questions | [Status](STATUS.md) and [roadmap](ROADMAP.md) |

## Research index

### Growth, entropy, and records

| Topic | Entry points |
| --- | --- |
| **Hamiltonian growth and its colour extensions** | [Binary relational encoding](research/cbb-binary/README.md) introduces all-slot growth and its binary extension. [BIN, TRI and CROSS reader’s guide](research/cbb-binary/GROWTH-CLOCKS-AND-BELL.md) indexes the binary and three-colour studies of reversal reachability, winding, transport, records, clocks and Bell controls. |
| **Wheeler series: constrained growth and entropy** | [Working paper](research/wheeler/paper-v0.1/README.md) · [Probe series](probes/wheeler/README.md) · [Review](research/wheeler/REVIEW-01.md) · [Reproduction code](code/wheeler/README.md). See [WHEELER-62](probes/wheeler/WHEELER-62.md) for entropy growth from the minimal seed and [WHEELER-61](probes/wheeler/WHEELER-61.md) for an exact entropy decrease from a different seed. [WHEELER-63](probes/wheeler/WHEELER-63.md) extends the bounded checks. The [summary](research/wheeler/SUMMARY-01.md) and [errata](probes/wheeler/ERRATA-01.md) give the scope and corrections. |
| **MICRO growth and observer comparison** | [Observer compatibility audit](probes/micro/observer-compatibility-01/README.md) tests when projected observations retain a closed growth rule. [Julstce](probes/micro/julstce/README.md) gives an exact lower bound on how well the final shape can reveal detector order after growth. |
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
