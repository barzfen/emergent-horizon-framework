# Reversal admissibility explorations

These probes distinguish the cycle representation, state constraints, edge selection, and rates. They do not derive physical dynamics.

- [REV-01: all-length reversals](all-length-01/README.md) tests MICRO-only and Pi-preserving move rules. It includes a local admissibility lemma, a general MICRO-only connectivity proof, and an exact finite census.
- [REV-02: rare longer channels](rare-channel-02/README.md) adds an explicit symmetric rate hierarchy on one 96-state MICRO/Pi component. Rare extra moves delay loss of a domain-count signal; the hierarchy itself is supplied. Domain count is not an exactly closed Markov observable.

- [REV-03: interrupted assembly gate](assembly-gate-03/README.md) adds explicit progress/abort states. It derives a smooth completion hierarchy under the added gate rules, proves a short-move implementation obstruction, and distinguishes exact idle-time rates from the real-time cycle projection. The final reversal commit remains an added atomic operation.
- [REV-04 — Local reconnection by triangle slides](local-reconnect-04/README.md) realizes all 76 blocked LR4 transitions with reversible two-hop edits in an expanded graph state space. It compares direct schedules and checks every intermediate edit for connectivity, degree and same-bit adjacency.
- [REV-05 — A tagged connection as local memory](tagged-controller-05/README.md) compares first-cycle returns under equal weights, branch repair and forward continuation of a marked edge. An exact history sum checks the rare blocked LR4 completions.
- [REV-06 — Local Pi tags and seam order](pi-closure-06/README.md) gives a local invariant for Pi at completed odd cycles and compares closure policies on the blocked LR4 witness.

See the [foundations map](../../research/foundations/CONNECTIONS-01.md) for the connections and verification boundaries of the wider EHF programme.
