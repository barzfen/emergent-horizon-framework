# EHF-OPW3-AUDIT-09
## Growth-Descriptor Chart Covariance

### Purpose

Audit-08 found that the exact \(n-2\to n\) insertion descriptor recovers every
residual hidden slow mode at \(n=7,9\). The descriptor was defined in one
canonical chart. Before it is treated as meaningful relational information, we
must determine whether the completed structure survives changes of chart.

### Growth charts

For source size \(m=n-2\), a chart consists of:

1. an anchor \(a\in\{0,\ldots,m-1\}\);
2. an anchored orientation policy:
   - lexicographic minimum;
   - lexicographic maximum;
3. an insertion order:
   - \(m\) then \(m+1\);
   - \(m+1\) then \(m\).

Hence there are

\[
4m
\]

growth charts:

- 20 charts for \(5\to7\);
- 28 charts for \(7\to9\).

The anchor is always an old/source label, so it survives insertion and deletion.

### Tests

#### 1. Exact chart growth bijection

Every chart must generate every target state exactly once from a source state
and a chart-relative descriptor.

#### 2. Parent invariance

The undirected \(n-2\) ancestor must be identical in all charts.

#### 3. Descriptor transition law

Raw descriptor values need not be invariant. For each chart relative to the
reference chart, the probe measures whether the descriptor transition is:

- descriptor-only functional;
- functional after conditioning on the source dihedral chart transition;
- functional after conditioning on both source and target dihedral chart
  transitions.

The fully conditioned transition must be deterministic.

#### 4. LR3 packet-closure covariance

For every OPW3 chamber, compare the exact LR3-signature equitable partition
under every anchor/orientation chart with the reference partition.

#### 5. Residual-completion covariance

On the canonical residual chambers, compare:

\[
\text{current LR3 signature},
\]

\[
\text{current + parent LR3 signature},
\]

\[
\text{current + insertion descriptor},
\]

\[
\text{current + parent signature + descriptor}.
\]

For each chart and candidate, record:

- exact final partition;
- compression;
- quotient gap;
- equality with the reference-chart partition;
- projection of the complete lowest nontrivial eigenspace into the quotient
  subspace.

The eigenspace test is stronger than merely reproducing the lowest eigenvalue.

### Scientific outcomes

Possible outcomes include:

- **partition invariant:** the completed quotient is intrinsic;
- **partition chart-dependent but eigenspace invariant:** charts provide
  different coordinate resolutions of the same slow sector;
- **slow completion chart-dependent:** the descriptor is not suitable as an
  observable, and the residual microscopic sector should be retained;
- **deterministic transition law:** chart descriptors form a legitimate
  coordinate atlas even when raw values differ.

These outcomes are reported rather than imposed by strict mode.

### Outputs

- `chart_summary.csv`
- `signature_closure_covariance.csv`
- `residual_completion_chart_covariance.csv`
- `run_summary.json`

### Run

```bash
python3 scripts/ehf_opw3_audit_09_growth_descriptor_chart_covariance.py \
  --base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --target-ns 7,9 \
  --out-dir runs/ehf_opw3_audit_09 \
  --strict
```

### Interpretation discipline

A chart-relative descriptor remains coordinate data unless the completed
partition or completed slow subspace is chart-covariant. No physical
observable, quantum number or particle identity is assumed.
