# EHF-OPW3-AUDIT-06 — Corrected version

This version fixes three issues in the original Audit-06 script:

1. **Equitable-refinement termination**
   The original loop stopped only when the numeric colour vector was unchanged.
   A stable partition can retain the same cells while canonical colour IDs are
   permuted, causing a nonterminating loop. The corrected code stops when a
   refinement produces no additional cells.

2. **One-cell quotient spectra**
   A quotient with one cell has no nontrivial spectral gap. It is now marked as
   ineligible for slow-gap visibility instead of assigning a false gap of zero.

3. **Isolated singleton chambers**
   A zero-degree singleton quotient is represented as the canonical absorbing
   one-state Markov chain, with transition probability 1 to itself.

Signature-closure equality is now recorded as a scientific outcome rather than
treated as an implementation requirement under `--strict`.

Validated command:

```bash
python3 scripts/ehf_opw3_audit_06_packet_closure_spectral_action.py   --base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py   --ns 5,7,9   --graphs OPW3,OPW23   --out-dir runs/ehf_opw3_audit_06   --strict
```

The corrected full validation completed in approximately four seconds.
