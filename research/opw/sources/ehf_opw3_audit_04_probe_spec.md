# EHF-OPW3-AUDIT-04  
## Canonical Growth Retraction and LR3 Edge-Channel Decomposition

### Purpose

Rebuild the odd growth map

\[
n\longrightarrow n+2
\]

using only the locked Audit-01 state convention, then determine what survives
when the legacy OPW23 growth results are restricted to foundational OPW3.

This probe does **not** identify one insertion step with one Planck time.

### Growth map

For a canonical source cycle on labels \(0,\ldots,n-1\):

1. insert label \(n\) after gap \(g_1\in\{0,\ldots,n-1\}\);
2. insert label \(n+1\) after gap
   \(g_2\in\{0,\ldots,n\}\) of the intermediate ordering;
3. canonicalize.

There are

\[
D_{\mathrm{all}}(n)=n(n+1)
\]

descriptors per source. Deleting the two newest labels defines the inverse
ancestor map.

### Signature-growth audit

For OPW3, LR2 and OPW23 independently:

- discover the fixed active core and variable active features;
- encode the variable features as a bit word;
- compare source and child codes under every insertion;
- record the exact Hamming distribution;
- find descriptors that preserve the code for **every** source state.

The historical core-descriptor candidate in this gap convention is

\[
\mathcal D_{\mathrm{core}}(n)
=
\{3,\ldots,n-4\}\times\{3,\ldots,n-3\},
\]

with size

\[
(n-6)(n-5).
\]

The probe tests rather than assumes whether this is also the universal OPW3
packet-preserving channel.

### LR3 edge-channel decomposition

Collapse each target OPW3 edge by deleting the newest labels at both ends.
Every target edge is classified as:

1. **vertical:** both endpoints have the same source ancestor;
2. **faithful:** the two ancestors form an OPW3 source edge;
3. **cross-chamber:** the ancestors lie in different source OPW3 chambers;
4. **same-chamber nonedge:** ancestors lie in one source chamber but are not
   adjacent.

At the exactly tested steps, the probe audits the candidate formulas:

\[
\text{vertical edges per source}=3n-5,
\]

\[
\text{faithful child edges per source edge}=(n-1)(n-2),
\]

\[
E_{\mathrm{cross}}
=
|V_n|\frac{(n-2)(9n-13)}{3}.
\]

These are finite-\(n\) audited laws, not yet all-\(n\) theorems.

### Component ancestry

For all insertion and for the universally OPW3-preserving descriptors, record
the target chambers reached by every source chamber.

At \(7\to9\), test whether the legacy two-branch ladder survives under OPW3:

\[
s\longmapsto 9s+108,\qquad 9s+144.
\]

### Outputs

- `growth_bijection_summary.csv`
- `signature_growth_summary.csv`
- `descriptor_preservation_ledger.csv`
- `opw3_edge_channel_summary.csv`
- `component_ancestry.csv`
- `run_summary.json`

### Run

```bash
python3 scripts/ehf_opw3_audit_04_growth_retraction_edge_channels.py \
  --base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --source-ns 5,7 \
  --out-dir runs/ehf_opw3_audit_04 \
  --strict
```

### Interpretation discipline

A pass establishes a canonical combinatorial retraction and exact finite growth
laws. It does not establish physical time, cosmological expansion, unitary
evolution, or particle propagation.
