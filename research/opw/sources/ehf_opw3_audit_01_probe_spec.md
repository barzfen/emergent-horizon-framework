# EHF-OPW3-AUDIT-01
## Definition Lock and Matched Structural Census

### Purpose

Rebuild the Odd Preserve World from the foundational LR3 rule without importing
legacy OPW23 conclusions. The probe compares:

- **OPW3:** Pi-preserving circular length-3 reversals;
- **LR2:** Pi-preserving circular length-2 reversals as an ablation;
- **OPW23:** the legacy/enriched union of LR2 and LR3 preserve edges.

This is a foundation audit, not a QM probe.

### Locked conventions

For odd \(n\):

1. States are undirected Hamilton cycles on \(K_n\), modulo rotation and reflection.
2. Internally labels are \(0,\ldots,n-1\).
3. Canonicalization anchors label \(0\), compares the anchored orientation with its reversal, and keeps the lexicographically smaller representative.
4. \(\Pi(c)\) is the unordered pair of sorted label sets in zero-based even and odd positions of the canonical representative.
5. A local edge is retained only when the move preserves \(\Pi\).

### Exact outputs

For each \(n\in\{5,7,9\}\) and each graph:

- vertex and edge counts;
- component count and component-size distribution;
- degree distribution;
- exact Pi-fibre connectivity;
- active move-slot frequencies;
- active-signature distribution;
- component-level Pi purity and regularity;
- exact partition comparison among OPW3, LR2, OPW23 and Pi fibres;
- exact identity
  \[
  E_{\mathrm{OPW23}}=E_{\mathrm{OPW3}}\cup E_{\mathrm{LR2}}.
  \]

For OPW3 it also discovers, rather than assumes:

- LR3 slots active for every state;
- LR3 slots active for at least one state;
- the fixed-core/variable-boundary signature geometry;
- the exact number of LR3 active-signature patterns.

### Regression checks

The independent engine is checked against the documented OPW23 counts at
\(n=5,7,9\). These checks validate implementation consistency but do not
prejudge the OPW3 result.

### Survival questions answered

1. Does OPW3 induce the same chamber partition as OPW23?
2. Which legacy edges are genuinely LR3-derived?
3. Is LR2 merely an edge enrichment, or does it merge chambers?
4. What replaces the old four-bit LR2/LR3 active-slot grammar under LR3 alone?
5. Are the LR3 chambers connected Pi fibres at \(n=5,7,9\)?
6. Which component regularity and degree features survive?

### Not yet tested

This first probe does not test short-cycle ranks, spectra, heat-kernel scaling,
growth-lift compatibility, packet MSM/action, phase curvature, or QM constructions.
Those belong to later audits after the foundation passes.

### Run

```bash
python3 scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --ns 5,7,9 \
  --out-dir runs/ehf_opw3_audit_01 \
  --write-state-ledger \
  --strict
```

### Verdict

```text
EHF_OPW3_AUDIT_01_FOUNDATION_REBUILD_PASS
```
