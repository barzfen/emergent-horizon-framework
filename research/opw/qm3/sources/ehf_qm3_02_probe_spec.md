# EHF-QM3-02
## Degenerate Slow-Multiplet Chart-Orbit Resolution

### Motivation

QM3-01 found one chart-critical chamber at each tested target size:

\[
n=7:\quad C_{18},
\]

\[
n=9:\quad C_{68}.
\]

In those chambers the lowest nontrivial normalized-Laplacian eigenvalue is
degenerate, and not every completed growth chart contains the complete
eigenspace.

The intrinsic spectral projector remains well defined, but the chart family
selects different directions inside the degenerate multiplet.

### Restricted chart projectors

Let

\[
E_{\rm slow}
\]

be the complete lowest nontrivial eigenspace with orthonormal basis
\(B_{\rm slow}\), and let \(Q_\chi\) be the completed quotient projector for
growth chart \(\chi\).

Define

\[
R_\chi
=
B_{\rm slow}^{\mathsf T}
Q_\chi
B_{\rm slow}.
\]

When \(Q_\chi\) is invariant under the normalized Laplacian, \(R_\chi\) is an
orthogonal projector onto the slow directions visible in chart \(\chi\).

### Fusion-frame analysis

The chart-selected slow subspaces form a finite fusion frame with frame
operator

\[
F=\sum_\chi R_\chi.
\]

The probe records:

- visible slow rank in every chart;
- distinct chart-selected subspaces;
- union and intersection rank;
- principal angles and projector overlaps;
- eigenvalues of \(F\);
- lower and upper frame bounds;
- frame condition number;
- whether
  \[
  F=\alpha I
  \]
  on the slow multiplet.

If \(F=\alpha I\), the chart family is a tight fusion frame and samples the
degenerate eigenspace isotropically. If \(F\) is merely positive definite, the
chart family still spans the full multiplet but with preferred directions.

### Critical-chamber input

QM3-02 is deliberately targeted. It reads the chart-critical chamber IDs from
the completed QM3-01 summary rather than repeating the full all-chamber
projector census.

### Outputs

- `critical_multiplet_summary.csv`
- `chart_slow_capture_ledger.csv`
- `chart_subspace_orbits.csv`
- `chart_subspace_pair_geometry.csv`
- `run_summary.json`

### Run

```bash
python3 scripts/ehf_qm3_02_degenerate_slow_multiplet_chart_orbit.py \
  --base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --chart-script scripts/ehf_opw3_audit_09_growth_descriptor_chart_covariance.py \
  --qm3-01-summary runs/ehf_qm3_01/run_summary.json \
  --target-ns 7,9 \
  --out-dir runs/ehf_qm3_02 \
  --strict
```

### Interpretation discipline

A degenerate structural eigenspace is not automatically a physical internal
multiplet. Chart-orbit geometry does not by itself establish spin, gauge
symmetry, charge, particle species, or a physical Hamiltonian.
