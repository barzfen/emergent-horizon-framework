# EHF-QM3-05
## Critical-Chamber Product-Permutahedron Scaling Audit

### Motivation

QM3-04 proves at the two chart-critical sizes:

\[
n=7:
\qquad
G_{\rm slow}\cong S_2\times S_2,
\qquad
E_{\rm slow}\cong
(\mathbf1\otimes\mathrm{Std})
\oplus
(\mathrm{Std}\otimes\mathbf1),
\]

and

\[
n=9:
\qquad
G_{\rm slow}\cong S_3\times S_3,
\qquad
E_{\rm slow}\cong
(\mathbf1\otimes\mathrm{Std})
\oplus
(\mathrm{Std}\otimes\mathbf1).
\]

The critical states themselves reveal a stronger pattern.

Let

\[
n=2m+3,
\qquad m\ge2.
\]

Define

\[
\mathcal C_m
=
\left\{
(0,m+1,a_1,b_1,\ldots,a_m,b_m,m+2)
\right\},
\]

where

\[
(a_1,\ldots,a_m)\in S_{\{1,\ldots,m\}},
\]

and

\[
(b_1,\ldots,b_m)
\in
S_{\{m+3,\ldots,2m+2\}}.
\]

### Exact graph candidate

The candidate theorem is

\[
\operatorname{OPW3}[\mathcal C_m]
\cong
\operatorname{Perm}_m
\square
\operatorname{Perm}_m,
\]

where

\[
\operatorname{Perm}_m
=
\operatorname{Cay}
\left(
S_m,
\{s_1,\ldots,s_{m-1}\}
\right)
\]

is the adjacent-transposition permutahedron graph.

Under the proposed coordinate map:

- LR3 start \(2i\) swaps \(a_i,a_{i+1}\);
- LR3 start \(2i+1\) swaps \(b_i,b_{i+1}\).

Hence the predicted exact laws are

\[
|\mathcal C_m|=(m!)^2,
\]

\[
\deg\mathcal C_m=2(m-1),
\]

\[
|E(\mathcal C_m)|=(m!)^2(m-1).
\]

### Spectral candidate

The tested normalized gaps suggest

\[
\lambda_1(\mathcal C_m)
=
\frac{1-\cos(\pi/m)}{m-1}.
\]

The predicted multiplicity is

\[
2(m-1),
\]

with slow representation

\[
(\mathrm{Std}_A\otimes\mathbf1_B)
\oplus
(\mathbf1_A\otimes\mathrm{Std}_B).
\]

The probe verifies this numerically at the requested \(m\) values. The all-\(m\)
gap formula remains a candidate until supported by a separate proof or a
properly cited spectral theorem.

### Default scaling range

The default run tests

\[
m=2,3,4,5,
\]

corresponding to

\[
n=7,9,11,13.
\]

The directly constructed critical chamber sizes are only

\[
4,\ 36,\ 576,\ 14400,
\]

so this avoids enumerating the full OPW3 state spaces at \(n=11,13\).

### Outputs

- `critical_product_permutahedron_summary.csv`
- `run_summary.json`

### Run

```bash
python3 scripts/ehf_qm3_05_critical_product_permutahedron.py \
  --base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --ms 2,3,4,5 \
  --out-dir runs/ehf_qm3_05 \
  --strict
```

### Interpretation discipline

The exact product graph and product-symmetric representation are structural
finite combinatorics. They do not by themselves establish:

- physical spin;
- gauge symmetry;
- charge;
- particle species;
- physical mass or energy;
- a physical Hamiltonian;
- a continuum limit.
