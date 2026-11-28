# EHF-OPW3-AUDIT-02  
## Square-Complex and Active-Signature Projection Survival

## Purpose

Determine whether LR3 alone supplies the non-generic cycle and coarse-sector
structure required for a rebuilt QM bridge.

Audit 01 proved, for the tested values \(n=5,7,9\), that OPW3 alone generates
exactly the same realised \(\Pi\)-fibre chamber partition as legacy OPW23. That
does **not** imply that the internal cycle geometry, phase support, spectra, or
packet dynamics survive. Audit 02 addresses the first of those missing layers.

## Inputs

The probe imports the independently rebuilt Audit-01 engine and constructs:

- **OPW3:** \(\Pi\)-preserving circular LR3 edges;
- **LR2:** \(\Pi\)-preserving LR2 edges as an ablation;
- **OPW23:** their legacy union.

No old QM conclusions are imported.

## Exact square-complex audit

For each connected component and graph, the script computes:

- triangle count;
- all simple 4-cycles, including chorded 4-cycles;
- induced-square count;
- graph cycle-space dimension
  \[
  \beta_1=|E|-|V|+1;
  \]
- rank of the oriented square-boundary span over \(\mathbb F_2\) and
  \(\mathbb F_3\);
- residual square-homology dimension
  \[
  h_1^{\square}(p)=\beta_1-
  \operatorname{rank}_{\mathbb F_p}\langle\partial(\text{squares})\rangle.
  \]

A nonzero residual means that attaching a 2-cell to every graph square does not
kill every cycle. Such residual directions are natural candidates for later
holonomy/phase audits, but are not yet physical gauge degrees of freedom.

## Active-signature audit

For LR3 and LR2 separately, the script discovers:

- fixed active slots;
- variable active slots;
- realised boundary-bit patterns.

It then constructs the joint LR3×LR2 active-signature coordinate and checks:

- whether all \(4\times4=16\) combinations occur;
- whether the joint signature maps deterministically and injectively to the
  OPW23 active signature;
- whether the four-state and sixteen-state partitions are equitable for the
  adjacency dynamics;
- whether they are exactly lumpable for the random-walk dynamics;
- the same tests component by component.

These are tests of an **active-signature packet candidate**. They do not assume
that this candidate equals the mature packet map used in the old OPW23 QM work.

## Main questions

1. Does OPW3 possess abundant square geometry without LR2?
2. Do OPW3 squares generate the full cycle space, or leave residual holonomy
   directions?
3. Does LR2 create square geometry of its own, or only mixed LR2/LR3 squares?
4. Is the legacy 16-state active grammar exactly the Cartesian product of a
   four-state LR3 grammar and a four-state LR2 decoration?
5. Is either the four-state or sixteen-state partition an exact dynamical
   quotient?
6. Does characteristic two behave differently from odd characteristic?

## Run

```bash
python3 scripts/ehf_opw3_audit_02_square_complex_packet_projection.py \
  --base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --ns 5,7,9 \
  --square-rank-fields 2,3 \
  --out-dir runs/ehf_opw3_audit_02 \
  --strict
```

## Outputs

- `square_graph_summary.csv`
- `square_component_summary.csv`
- `active_signature_geometry.csv`
- `active_signature_crosswalk.csv`
- `signature_partition_dynamics.csv`
- `run_summary.json`

## Interpretation discipline

- A strict pass validates implementation consistency only.
- Square-span residuals are algebraic cycle directions, not automatically
  physical phases.
- Failure of exact lumpability does not make a coarse packet model useless; it
  means any reduced Markov model is approximate, conditional, or requires more
  state variables.
- Differences between \(\mathbb F_2\) and odd characteristic flag arithmetic
  structure requiring a later integral audit.
