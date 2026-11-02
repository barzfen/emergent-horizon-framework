# EHF-AMP-FOUND-03I  
## KK-Endpoint Covariance and Two-Chart Normalizer Closure

**Status:** exact coordinate-covariance and atlas-closure theorem  
**Input:** exact eight-point KK shuffle maps and the 03G/03H group-ring construction  
**Residual symmetry:** \(\tau=(5\,7)(6\,8)\)

---

## 1. Motivation

03H proved that the nontrivial residual normalizer element

\[
\tau=(5\,7)(6\,8)
\]

acts on

\[
G=\langle(2\,3),(5\,6),(7\,8)\rangle\cong C_2^3
\]

by

\[
x_1\mapsto x_1,
\qquad
x_2\leftrightarrow x_3.
\]

It does not preserve the 21-template catalogue built in the standard KK chart
with endpoint \(8\): only eight classes remain inside and thirteen leave,
producing a 34-class residual closure.

The natural explanation is that \(\tau\) changes the fixed KK endpoint:

\[
\tau(8)=6.
\]

03I tests whether the thirteen external classes are precisely the missing
classes of the endpoint-6 KK chart.

---

## 2. Endpoint-dependent KK bases

For an endpoint

\[
e\in\{2,\ldots,8\},
\]

define the exact KK basis

\[
\mathcal B_e
=
\{\operatorname{PT}(1,\sigma,e):
\sigma\in S_{\{2,\ldots,8\}\setminus\{e\}}\}.
\]

Let

\[
Q^{(e)}:\mathbb Q^{72}\longrightarrow\mathbb Q^{720}
\]

be the exact KK coordinate matrix of the reference target fibre in this
basis.

03I constructs independently:

\[
Q^{(8)}
\qquad\text{and}\qquad
Q^{(6)}.
\]

---

## 3. Exact coordinate covariance

Let \(P_\tau\) be the target-state permutation induced by relabelling with
\(\tau\) followed by canonicalisation. Because the multiplicity is even,
canonical reversal contributes no sign.

Let \(R_\tau\) be the KK-row permutation

\[
(1,\sigma,8)
\longmapsto
(1,\tau(\sigma),6).
\]

The primary exact identity is

\[
\boxed{
Q^{(6)}P_\tau=R_\tau Q^{(8)}.
}
\]

Consequences include:

\[
\dim\ker Q^{(8)}=
\dim\ker Q^{(6)}=15,
\]

\[
\ker Q^{(8)}=
\ker Q^{(6)},
\]

and

\[
P_\tau(\ker Q^{(8)})=
\ker Q^{(6)}.
\]

---

## 4. Universal-row covariance

Using the same ten target-state orbit representatives \(w_j\), define in each
endpoint chart

\[
P^{(e)}_{\sigma j}(x)
=
\sum_{h\in C_2^3}
Q^{(e)}[\sigma,h\cdot w_j]x^h.
\]

The residual action simultaneously:

- permutes the ten target-state orbits;
- exchanges \(x_2\) and \(x_3\);
- relabels endpoint-8 KK rows into endpoint-6 rows.

03I verifies the raw polynomial identity

\[
\boxed{
\tau\!\left(P^{(8)}_\sigma(x)\right)
=
P^{(6)}_{\tau(\sigma)}(x)
}
\]

for all \(720\) KK coordinates.

---

## 5. Two independent 21-template catalogues

Each endpoint chart is reduced independently by the 03G equivalence:

\[
P'(x)=m x^hP(x),
\qquad
m\in\mathbb Z\setminus\{0\},
\quad h\in C_2^3.
\]

The expected census in both charts is

\[
21\text{ primitive classes},
\]

with multiplicity distribution

\[
16^{\times3},
\qquad
8^{\times6},
\qquad
4^{\times12}.
\]

No endpoint-6 catalogue is imported from a previous run; it is reconstructed
directly from \(Q^{(6)}\).

---

## 6. Exact two-chart theorem

Let

\[
\mathcal T_8
\]

be the endpoint-8 catalogue and

\[
\mathcal T_6
\]

the endpoint-6 catalogue.

The theorem target is

\[
\boxed{
\tau(\mathcal T_8)=\mathcal T_6
}
\]

bijectively, with KK-row multiplicities preserved.

The exact set census is

\[
|\mathcal T_8|=|\mathcal T_6|=21,
\]

\[
|\mathcal T_8\cap\mathcal T_6|=8,
\]

\[
|\mathcal T_8\setminus\mathcal T_6|=13,
\qquad
|\mathcal T_6\setminus\mathcal T_8|=13,
\]

and

\[
\boxed{
|\mathcal T_8\cup\mathcal T_6|=34.
}
\]

The union contains

\[
\boxed{18}
\]

orbits under the residual involution.

Its multiplicity distribution is

\[
4^{\times18},
\qquad
8^{\times11},
\qquad
16^{\times5},
\]

exactly matching the 03H normalizer closure.

---

## 7. Interpretation

A successful 03I run proves that the 03H result is a **fixed-chart
obstruction**, not a failure of covariance of the underlying relation system.

The correct object is a two-chart atlas:

\[
\boxed{
\mathcal T_8\cup\mathcal T_6.
}
\]

The thirteen classes that appear to leave the standard endpoint-8 catalogue
are exactly the thirteen endpoint-6-only classes.

Thus

\[
21\longrightarrow34
\]

is not arbitrary catalogue growth. It is the minimal closure obtained by
including the KK chart selected by the residual normalizer.

---

## 8. Claim boundary

03I proves covariance only for:

- the fixed anchor-1 reference target fibre;
- the endpoints \(8\) and \(6\);
- the specific residual element \(\tau=(5\,7)(6\,8)\);
- the exact finite eight-point KK system.

It does not yet prove:

- covariance among all seven possible non-anchor endpoints;
- covariance under the complete target-fibre stabilizer;
- anchor covariance;
- a general multiplicity theorem;
- physical or phenomenological significance.

---

## 9. Run command

```bash
caffeinate -i python3 scripts/ehf_amp_found_03i_kk_endpoint_covariance_normalizer_closure.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --normal-form-script scripts/ehf_amp_found_03e_exact_signed_orbit_normal_form.py \
  --template-script scripts/ehf_amp_found_03g_parameterised_shuffle_antisymmetriser_templates.py \
  --normalizer-script scripts/ehf_amp_found_03h_group_ring_factor_normalizer_audit.py \
  --out-dir runs/ehf_amp_found_03i \
  --strict
```

No saved output files from 03G or 03H are required.

---

## 10. Principal outputs

```text
summary.json
verdict.json
run.log
exact_kk_endpoint_covariance_certificate.json
kk_endpoint_row_relabelling.csv
universal_row_endpoint_covariance.csv
endpoint8_to_endpoint6_template_map.csv
endpoint_chart_intersection.csv
two_chart_template_atlas.csv
exact_kk_endpoint_covariance_audit.md
```

The target terminal result is:

```text
Residual normalizer
  target-fibre stabilizer order:      144
  normalizer order:                   16
  quotient N/G order:                 2
  tau is nontrivial residual element: True

Exact KK endpoint covariance
  Q6 P_tau = R_tau Q8:               True
  endpoint kernels equal:             True
  tau kernel covariance:              True
  raw universal row covariance:       True

Two-chart template atlas
  endpoint-8 templates:               21
  endpoint-6 templates:               21
  shared templates:                   8
  endpoint-8-only templates:          13
  endpoint-6-only templates:          13
  union size:                         34
  tau orbits in union:                18
  tau catalogue bijection:            True

Verdict: EHF_AMP_FOUND_03I_EXACT_TWO_CHART_KK_ENDPOINT_COVARIANCE_PROVED
strict checks: PASS
```
