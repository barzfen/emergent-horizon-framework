# EHF-QM3-04
## Exact Product-Symmetric Slow-Representation Classification

### Motivation

QM3-03 found that the chart-induced common/sensitive decomposition is
preserved by every chamber-preserving label transposition.

The largest transposition stabilizers are visibly organised on two disjoint
label supports:

- at \(n=7\), two supports of size \(2\);
- at \(n=9\), two supports of size \(3\).

The commutant of the complete slow representation has dimension \(2\) in both
cases, consistent with a multiplicity-free sum of two inequivalent real
irreducible blocks.

### Group generation

Generate the exact finite label-permutation group from all chamber-preserving
transpositions.

Discover the connected supports of the transposition graph and test

\[
|G|
=
\prod_i |S_{m_i}|
=
\prod_i m_i!.
\]

The expected finite groups are candidates only until exact closure verifies
their orders and actions.

### Candidate representation

For two supports \(A\) and \(B\), let

\[
\mathrm{Std}_A
\]

and

\[
\mathrm{Std}_B
\]

be the zero-sum standard representations of \(S_A\) and \(S_B\).

Test the exact character identity

\[
E_{\rm slow}
\cong
(\mathrm{Std}_A\otimes\mathbf 1_B)
\oplus
(\mathbf 1_A\otimes\mathrm{Std}_B).
\]

This predicts dimensions

\[
(|A|-1)+(|B|-1),
\]

giving:

\[
1+1
\]

for \(S_2\times S_2\), and

\[
2+2
\]

for \(S_3\times S_3\).

The standard character is

\[
\chi_{\rm Std}(g)
=
\#\operatorname{Fix}(g)-1.
\]

### Irreducibility and inequivalence

For the common and sensitive blocks, compute:

- real commutant dimension;
- cross-intertwiner dimension.

A block commutant dimension of \(1\) establishes absolute irreducibility over
\(\mathbb R\). A zero cross-intertwiner dimension establishes inequivalence of
the two blocks.

### Character projectors

Reconstruct each block projector from the finite-group character formula:

\[
P_\rho
=
\frac{d_\rho}{|G|}
\sum_{g\in G}
\chi_\rho(g)\,U_g.
\]

Compare these symmetry projectors with the chart-fusion common and sensitive
projectors.

### Outputs

- `product_group_classification.csv`
- `representation_character_table.csv`
- `representation_block_summary.csv`
- `run_summary.json`

### Run

```bash
python3 scripts/ehf_qm3_04_product_symmetric_representation.py \
  --base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --chart-script scripts/ehf_opw3_audit_09_growth_descriptor_chart_covariance.py \
  --qm3-02-summary runs/ehf_qm3_02/run_summary.json \
  --target-ns 7,9 \
  --out-dir runs/ehf_qm3_04 \
  --strict
```

### Interpretation discipline

A finite product-symmetric representation is not automatically a gauge group,
spin representation, charge sector or particle classification. Such a physical
interpretation would require additional dynamics, scaling, transport and
phenomenological evidence.
