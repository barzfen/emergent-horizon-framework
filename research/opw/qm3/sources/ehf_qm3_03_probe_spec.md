# EHF-QM3-03
## Chart-Average Multiplet Split and Growth-Symmetry Audit

### Motivation

QM3-02 found an exact two-level chart orbit in each critical chamber.

At \(n=7\):

- 8 charts see the full two-dimensional slow multiplet;
- 12 charts see one common one-dimensional subspace.

At \(n=9\):

- 16 charts see the full four-dimensional slow multiplet;
- 12 charts see one common two-dimensional subspace.

Hence the fusion operators have the exact forms

\[
F_7=8I+12P_{\rm common},
\]

\[
F_9=16I+12P_{\rm common}.
\]

The normalized chart averages have eigenvalues

\[
1,\quad \frac25
\]

at \(n=7\), and

\[
1,\quad\frac47
\]

at \(n=9\).

This produces a canonical chart-family split

\[
E_{\rm slow}
=
E_{\rm common}
\oplus
E_{\rm sensitive}.
\]

The next question is whether that split is respected by genuine relabelling
symmetries or is only an artefact of the chosen chart ensemble.

### Anchor audit

For each old-label anchor, test whether all four combinations of:

- orientation policy;
- insertion order

have the same slow capture rank.

This determines whether the observed orbit is genuinely anchor-controlled.

### Relabelling stabilizers

The anchored preserve label \(\Pi\) is not equivariant under arbitrary
permutations of labels, particularly permutations involving label \(0\).
Therefore the probe does not infer a stabilizer from the displayed
\(\Pi=A\mid B\) sets.

Instead it tests every single label transposition and retains exactly those
that map the entire critical OPW3 chamber to itself.

From those exact chamber-preserving transpositions it defines:

#### Old-label stabilizer

All chamber-preserving transpositions of two old/source labels.

#### Growth-set stabilizer

All chamber-preserving transpositions that preserve the old/new label sets:
old-old swaps together with the newest-newest swap when available.

#### Chamber transposition stabilizer

Every chamber-preserving single transposition, including old/new mixing if it
occurs.

For each retained generator:

1. verify it acts as a graph automorphism;
2. restrict its permutation action to the complete slow eigenspace;
3. test whether it preserves
   \[
   E_{\rm common}\oplus E_{\rm sensitive};
   \]
4. record cross-sector mixing.

For each generated action, record:

- split invariance;
- fixed-subspace dimension;
- commutant dimension of the slow representation.

### Scientific outcomes

- If the split is preserved by ordered-growth symmetry but not the full
  preserve stabilizer, it is intrinsic to the growth-decorated structure but
  not to the target chamber alone.
- If it is preserved by the full stabilizer, it is an intrinsic symmetry
  decomposition of the chamber slow multiplet.
- If it is preserved by neither, it is only a chart-ensemble decomposition and
  the complete \(P_{\rm slow}\) should remain the sole intrinsic object.

### Outputs

- `critical_chart_average_split.csv`
- `anchor_capture_summary.csv`
- `symmetry_generator_actions.csv`
- `symmetry_group_summary.csv`
- `run_summary.json`

### Run

```bash
python3 scripts/ehf_qm3_03_chart_average_growth_symmetry.py \
  --base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --chart-script scripts/ehf_opw3_audit_09_growth_descriptor_chart_covariance.py \
  --qm3-02-summary runs/ehf_qm3_02/run_summary.json \
  --target-ns 7,9 \
  --out-dir runs/ehf_qm3_03 \
  --strict
```

### Interpretation discipline

No physical spin, gauge representation, charge, chirality or particle identity
is inferred from the finite common/sensitive decomposition.
