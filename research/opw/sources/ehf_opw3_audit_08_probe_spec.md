# EHF-OPW3-AUDIT-08
## Residual Hidden-Sector Completion by LR3 Edge Labels and Growth History

Audit-07 leaves two unresolved \(n=7\) chambers and four unresolved \(n=9\)
chambers after adjoining the \(n-2\) ancestor LR3 signature.

This targeted probe tests whether they are recovered by:

- the exact insertion descriptor;
- parent signature plus descriptor;
- two-level signature, packet, or descriptor history;
- oriented LR3 square-incidence profiles;
- edge-labelled LR3 colour refinement.

The edge-labelled refinement retains the identity of the LR3 move slot on each
edge rather than treating every adjacency as identical. It is therefore a
native discrete completion, not an externally supplied physical label.

Run:

```bash
python3 scripts/ehf_opw3_audit_08_residual_completion.py \
  --base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --ns 7,9 \
  --out-dir runs/ehf_opw3_audit_08 \
  --strict
```

Output:

- `residual_completion_summary.csv`
- `run_summary.json`

A successful candidate must reproduce the full chamber gap while retaining
nontrivial compression. No quantum or particle interpretation follows directly.
