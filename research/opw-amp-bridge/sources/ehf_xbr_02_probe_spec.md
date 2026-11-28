# EHF-XBR-02
## Common Growth Groupoid and Dual-Functor Compatibility

### Status

Exact finite cross-branch compatibility audit.

### Inputs

The probe consumes:

1. the OPW3 foundational graph engine;
2. a successful `EHF-AMP-FOUND-03L` run directory containing:
   - `summary.json`;
   - `anchor_deletion_transition_ledger.csv`;
   - `anchor_deletion_chart_summary.csv`;
   - `full_anchor_deletion_channel_ledger.csv`;
   - `anchor_deletion_subspace_class_summary.csv`.

The AMP relation matrices are not recomputed. Their exact covariance is taken
from the complete 03L certificate and cross-checked against its ledgers.

---

## 1. Common chart groupoid

The objects are the 72 ordered anchor--deletion charts

\[
\chi=(a,d),
\qquad a\ne d,
\qquad a,d\in\{1,\ldots,9\}.
\]

Each chart has normalization

\[
\rho_\chi(a)=1,
\qquad
\rho_\chi(d)=9,
\]

with the remaining labels mapped increasingly to \(2,\ldots,8\).

For charts \(\chi,\psi\), define

\[
\pi_{\psi\leftarrow\chi}
=
\rho_\psi^{-1}\rho_\chi.
\]

The probe verifies:

\[
\pi_{\chi\leftarrow\chi}=\mathrm{id},
\]

\[
\pi_{\chi\leftarrow\psi}
=
\pi_{\psi\leftarrow\chi}^{-1},
\]

and

\[
\pi_{\omega\leftarrow\psi}
\pi_{\psi\leftarrow\chi}
=
\pi_{\omega\leftarrow\chi}
\]

for all

\[
72^3=373248
\]

ordered chart triples.

It also verifies that every arrow is exactly the arrow recorded by AMP-03L.

---

## 2. Shared source-state functor

Both branches use the same nine-point dihedral Hamilton-cycle basis after the
label translation

\[
\ell_{\rm AMP}=\ell_{\rm OPW}+1.
\]

The common source-state functor assigns to each chart the vector space on the

\[
20160
\]

nine-point cycle classes, with chart arrows acting by label permutation.

The probe verifies exact basis equality and arrow equality.

---

## 3. OPW dynamics lift

The OPW lift assigns:

- the OPW3 adjacency operator;
- the 69 \(\Pi\)-fibres/chambers;
- their induced graph decomposition.

For every chart normalization the probe verifies:

\[
U_\chi A_{\rm OPW3}U_\chi^{-1}
=
A_{\rm OPW3},
\]

together with exact covariance of:

- \(\Pi\)-labels;
- connected components;
- the full 53760-edge graph.

Because the normalized Laplacian is a degree-normalized polynomial in
adjacency, its spectral projectors are consequently covariant as well.

---

## 4. Amplitude-relations lift

AMP-03L assigns to every chart:

- 35 source/target fibre channels;
- exact KK and deletion maps;
- one of six transported image spaces
  \[
  V_0,V_2,V_8,V_9,V_{14},V_{15}.
  \]

For every ordered chart pair and all 35 channels, XBR-02 verifies that the
common groupoid arrow maps:

- the chart subset;
- its normalized subset;
- transmitted rank;
- transported subspace class

exactly.

The exact matrix covariance and image cocycle are supplied by the successful
AMP-03L certificate.

---

## 5. Middle-block natural transformation

In the reference chart \((1,9)\), the middle-block correspondence inserts the
pair

\[
\{8,9\}.
\]

For a chart \(\chi\), define the companion inserted leg

\[
u_\chi=\rho_\chi^{-1}(8).
\]

The chart-relative growth correspondence inserts

\[
\{u_\chi,d_\chi\}
\]

at the middle block.

The probe verifies that every common arrow maps:

- the seven-label parent basis;
- all 720 parent/child incidences;
- the chart-relative middle-block pair;
- the associated one-leg-deleted target basis

naturally.

Thus the diagrams commute at the state-correspondence level.

---

## 6. Exact theorem tested

A PASS establishes:

> The AMP-03L anchor--deletion atlas and the chart-relative OPW nine-point
> atlas are two compatible lifts over one exact finite chart groupoid. The same
> arrows act on their common Hamilton-cycle source basis, intertwine the
> pullback OPW dynamics, transport AMP relation-image channels, and make the
> middle-block growth correspondence natural.

This is stronger than the XBR-01 identification of one reference-chart growth
map.

---

## 7. Claim boundary

The audit does not establish:

- invariance of one fixed globally anchored OPW3 graph under all 72 charts;
- equality of amplitude relation spaces and OPW spectral spaces;
- a canonical linear map between those two lifted spaces;
- a physical gauge bundle or connection;
- a derivation of quantum mechanics;
- continuum or phenomenological physics;
- a novelty claim.

The word *functor* is used in the finite algebraic sense: chart arrows are sent
to compatible bijective or linear transport maps satisfying composition.

---

## 8. Run

From the OPW3 project, point `--amp03l-run-dir` to the completed AMP-03L run:

```bash
python3 scripts/ehf_xbr_02_common_growth_groupoid_dual_functor.py \
  --opw-base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --amp03l-run-dir /absolute/path/to/runs/ehf_amp_found_03l \
  --out-dir runs/ehf_xbr_02 \
  --strict
```

### Outputs

- `common_chart_object_ledger.csv`
- `common_groupoid_arrow_ledger.csv`
- `amp_channel_arrow_naturality.csv`
- `run_summary.json`
