# EHF-QM3-01
## OPW3 Hilbert Lift and Intrinsic Slow-Sector Projectors

### Purpose

Begin the LR3-only quantum-mechanics bridge without importing the older OPW23
quantum interpretation.

For each connected OPW3 chamber \(C\), define the finite Hilbert space

\[
\mathcal H_C=\mathbb C^{|C|}
\]

with the canonical cycle-state basis.

The symmetric normalized Laplacian

\[
L_{\rm norm}=I-D^{-1/2}AD^{-1/2}
\]

is used as a canonical self-adjoint structural operator. This does not yet
select it as a physical Hamiltonian.

### Intrinsic spectral projectors

Construct:

\[
P_0
\]

onto the stationary direction and

\[
P_{\rm slow}
\]

onto the complete lowest nontrivial eigenspace, including multiplicity.

Verify:

- Hermiticity;
- idempotence;
- \(P_0P_{\rm slow}=0\);
- \([L_{\rm norm},P_{\rm slow}]=0\).

### Reference-chart hierarchy

Using the reference growth chart, construct exact degree-weighted quotient
projectors:

\[
Q_{\rm packet}
\subseteq
Q_{\rm parent}
\subseteq
Q_{\rm full},
\]

where:

- \(Q_{\rm packet}\) uses current LR3 identity;
- \(Q_{\rm parent}\) adds parent LR3 identity;
- \(Q_{\rm full}\) adds the chart-relative insertion descriptor.

This yields orthogonal finite layers:

\[
P_0,
\]

\[
Q_{\rm packet}-P_0,
\]

\[
Q_{\rm parent}-Q_{\rm packet},
\]

\[
Q_{\rm full}-Q_{\rm parent},
\]

\[
I-Q_{\rm full}.
\]

The probe records how much of the lowest eigenspace lies in each layer.

### Chart-common completed space

For every growth chart \(\chi\), construct the completed quotient subspace

\[
\mathcal Q_\chi.
\]

For every chamber, first test whether every chart completion contains the
complete lowest eigenspace.  When at least one chart misses part of a
degenerate lowest eigenspace, compute explicitly:

\[
\mathcal Q_{\cap}
=
\bigcap_\chi \mathcal Q_\chi,
\]

and

\[
\mathcal Q_{\cup}
=
\operatorname{span}_\chi\mathcal Q_\chi.
\]

The expensive intersection/union calculation is therefore targeted only at
chart-critical chambers.  When all chart completions contain the slow space,
its inclusion in the intersection follows directly.

Questions:

1. Does every \(\mathcal Q_\chi\) contain the complete lowest eigenspace?
2. Does the chart-common intersection contain it?
3. Is
   \[
   \mathcal Q_{\cap}
   =
   \operatorname{span}
   (\text{stationary},\text{lowest eigenspace})?
   \]
4. How much additional chart-invariant structure remains in the intersection?
5. How large is the chart union relative to the microscopic Hilbert space?

### Outputs

- `hilbert_chamber_summary.csv`
- `reference_projector_layers.csv`
- `chart_common_subspace_summary.csv`
- `run_summary.json`

### Run

```bash
python3 scripts/ehf_qm3_01_hilbert_lift_intrinsic_projectors.py \
  --base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --chart-script scripts/ehf_opw3_audit_09_growth_descriptor_chart_covariance.py \
  --target-ns 7,9 \
  --out-dir runs/ehf_qm3_01 \
  --strict
```

### Interpretation discipline

This probe establishes exact finite Hilbert spaces and orthogonal projectors.
It does not yet establish:

- a physical Hamiltonian;
- physical time evolution;
- the Born rule;
- physical particles or masses;
- a continuum or Lorentz limit.
