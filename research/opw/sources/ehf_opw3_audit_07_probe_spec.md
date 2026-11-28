# EHF-OPW3-AUDIT-07
## Hidden Slow-Sector Families and Minimal Completion

Audit-06 found 5 hidden eligible OPW3 chambers at \(n=7\) and 18 at \(n=9\).
The misses are highly structured: many occur in exact pairs with identical
component size, packet-cell count, full gap, quotient gap and action entropy.

This probe:

1. reconstructs the hidden lowest normalized-Laplacian eigenspace;
2. verifies orthogonality to the exact LR3 packet quotient;
3. measures packet-cell energy concentration and localization;
4. groups repeated numerical fingerprints;
5. tests exact equitable completion using:
   - LR3 square-incidence count;
   - \(n-2\) ancestor chamber;
   - ancestor LR3 signature;
   - ancestor exact packet cell;
   - square count plus ancestor packet cell;
6. diagnoses the unique known OPW23 signature-closure exception.

Run:

```bash
python3 scripts/ehf_opw3_audit_07_hidden_slow_sector_completion.py \
  --base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --ns 7,9 \
  --out-dir runs/ehf_opw3_audit_07 \
  --strict
```

Outputs:

- `hidden_slow_sector_summary.csv`
- `completion_candidate_summary.csv`
- `hidden_family_summary.csv`
- `opw23_closure_exception_summary.csv`
- `run_summary.json`

A completion is scientifically useful only when it recovers hidden modes while
retaining substantial compression. No particle or quantum interpretation is
made.
