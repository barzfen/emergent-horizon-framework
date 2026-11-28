# EHF-OPW3-AUDIT-06
## Exact Packet-Closure Equivalence, Spectral Completeness, and Action Census

### Purpose

Audit-05 found that LR3-, LR2-, and joint-signature seeded equitable refinements
have nearly identical cell counts. Equal counts do not prove equal partitions.
This probe tests exact cell equality and asks whether the resulting exact
LR3-native quotient contains each chamber's true slowest diffusion mode.

### Tests

For every OPW3 and OPW23 chamber at \(n=5,7,9\):

1. Compute the stable equitable closures seeded by:
   - no labels;
   - LR3 active signatures;
   - LR2 active signatures;
   - joint LR3×LR2 signatures.
2. Test exact equality of the three signature-seeded partitions.
3. Verify that the signature closure refines the purely structural closure.
4. Build the exact reversible random-walk quotient from the LR3-seeded closure.
5. Compare:
   \[
   \lambda_1^{\rm full}
   \quad\text{and}\quad
   \lambda_1^{\rm quotient}.
   \]
   Since quotient modes form an invariant subspace,
   \[
   \lambda_1^{\rm quotient}\ge \lambda_1^{\rm full}.
   \]
   Equality means the slowest chamber mode is visible to the exact packet
   quotient.
6. Record the stochastic action census:
   \[
   A_{ab}=-\log P_{ab},
   \]
   entropy rate, stationary entropy, support size, and action range.

### Outputs

- `closure_equivalence_summary.csv`
- `quotient_action_spectral_summary.csv`
- `quotient_spectrum_ledger.csv`
- `run_summary.json`

### Run

```bash
python3 scripts/ehf_opw3_audit_06_packet_closure_spectral_action.py \
  --base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --ns 5,7,9 \
  --graphs OPW3,OPW23 \
  --out-dir runs/ehf_opw3_audit_06 \
  --strict
```

### Interpretation discipline

The exact quotient is a finite reversible stochastic system. Its transition
costs are not quantum phases or physical energies. Failure to see the slowest
mode means the chosen packet variables are spectrally incomplete, not that a
physical degree of freedom has been lost.
