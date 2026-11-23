# Formal Material

Use this directory for mathematics that has been separated from exploratory narrative.

## Machine-checked proofs

- [EHF-LEAN-02 — Complete-graph Hamiltonian-cycle insertion and unique ancestry](lean/README.md): Lean 4.36.0 proves valid all-edge-slot insertion, membership/length preservation, deletion recovery, distinct slots and unique ordered ancestry. Cycles remain rooted and oriented; dihedral quotient counting is not yet proved.

- [EHF-LEAN-01 — Binary XOR edge-splitting invariant](lean/README.md):
  Lean 4.36.0 verification of a local comparison-preservation property
  used in the binary Hamiltonian-cycle growth extension. This is not a
  global Hamiltonian-cycle growth theorem or a physics claim.

Suggested substructure:

- `definitions/`
- `lemmas/`
- `conjectures/`
- `proved-results/`

Every theorem/lemma should state assumptions explicitly and link to any computational evidence used during discovery.
