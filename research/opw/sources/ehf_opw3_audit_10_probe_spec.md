# EHF-OPW3-AUDIT-10
## Exact Growth-Chart Groupoid and Descriptor Cocycle

### Purpose

Audit-09 established that every growth chart gives a bijective coordinate
description of target states:

\[
\kappa_\chi(x)
=
\bigl(
\operatorname{parent}(x),
d_\chi(x)
\bigr),
\]

with chart-invariant parent and chart-dependent descriptor.

Audit-10 promotes this finite atlas to an exact groupoid.

### Transition maps

For charts \(\chi,\psi\), define

\[
T_{\psi\leftarrow\chi}
=
\kappa_\psi\circ\kappa_\chi^{-1}.
\]

Each transition is a bijection between complete coordinate sets.

### Groupoid laws

The probe verifies:

\[
T_{\chi\leftarrow\chi}
=
\operatorname{id},
\]

\[
T_{\chi\leftarrow\psi}
=
T_{\psi\leftarrow\chi}^{-1},
\]

and

\[
T_{\omega\leftarrow\psi}
\circ
T_{\psi\leftarrow\chi}
=
T_{\omega\leftarrow\chi}.
\]

The cocycle is tested over every chart triple and every target-state coordinate
at \(5\to7\) and \(7\to9\).

### Why this matters

The result separates:

- intrinsic ancestry;
- chart-relative descriptor coordinates;
- exact chart-transition laws.

It supplies the OPW side of the proposed shared growth atlas.

It does **not** yet prove that the amplitude relation spaces and OPW spectral
spaces are functors over one formally identical groupoid. That requires a
separate cross-branch construction.

### Run

```bash
python3 scripts/ehf_opw3_audit_10_growth_chart_groupoid_cocycle.py \
  --base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --chart-script scripts/ehf_opw3_audit_09_growth_descriptor_chart_covariance.py \
  --target-ns 7,9 \
  --out-dir runs/ehf_opw3_audit_10 \
  --strict
```

### Outputs

- `run_summary.json`

### Interpretation discipline

This is an exact finite coordinate-atlas theorem. It is not a physical gauge
bundle, spacetime atlas, quantum connection, or continuum structure.
