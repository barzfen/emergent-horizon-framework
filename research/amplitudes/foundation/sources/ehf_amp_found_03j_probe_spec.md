# EHF-AMP-FOUND-03J  
## Full Normalizer Endpoint Atlas and Cocycle Consistency

**Status:** exact full-normalizer covariance audit  
**Input:** exact eight-point KK maps and the fixed-anchor target fibre  
**Symmetry:**

\[
G=\langle(2\,3),(5\,6),(7\,8)\rangle\cong C_2^3,
\]

inside the reference-fibre stabilizer

\[
S_3\times S_4.
\]

---

## 1. Purpose

03I proved exact endpoint covariance for one residual normalizer element,

\[
\tau=(5\,7)(6\,8),
\qquad
8\mapsto6.
\]

It showed that the endpoint-8 and endpoint-6 template catalogues form a
covariant two-chart atlas with 34 total classes.

03J closes the endpoint-covariance problem for the complete normalizer

\[
N=N_{S_3\times S_4}(G),
\qquad |N|=16,
\qquad N/G\cong C_2.
\]

The probe tests every normalizer element, every endpoint in its orbit, and
every transition composition.

---

## 2. Four endpoint charts

For

\[
e\in\{5,6,7,8\},
\]

define the exact KK basis

\[
\mathcal B_e=
\{\operatorname{PT}(1,\sigma,e):
\sigma\in S_{\{2,\ldots,8\}\setminus\{e\}}\}.
\]

Let

\[
Q^{(e)}:\mathbb Q^{72}\longrightarrow\mathbb Q^{720}
\]

be the exact KK-coordinate matrix of the reference target fibre in chart
\(e\).

The expected kernel dimensions are

\[
\dim\ker Q^{(e)}=15
\]

for all four endpoints, with all four kernels equal as subspaces of the
72-dimensional target coefficient space.

---

## 3. Full normalizer covariance

For each

\[
n\in N
\]

and source endpoint \(e\), let:

- \(P_n\) relabel and canonicalise the 72 target states;
- \(R_{n,e}\) relabel the 720 KK basis rows from endpoint \(e\) to endpoint
  \(n(e)\).

The central identity is

\[
\boxed{
Q^{(n(e))}P_n=R_{n,e}Q^{(e)}.
}
\]

There are

\[
16\times4=64
\]

such exact coordinate identities.

The corresponding relation-space covariance is

\[
\boxed{
P_n\ker Q^{(e)}=\ker Q^{(n(e))}.
}
\]

---

## 4. Exact transition cocycle

For \(m,n\in N\), with composition \(mn=m\circ n\), the state and KK-row
transition maps should satisfy

\[
\boxed{
P_{mn}=P_mP_n,
}
\]

and

\[
\boxed{
R_{mn,e}=R_{m,n(e)}R_{n,e}.
}
\]

The script audits all

\[
16^2\times4=1024
\]

endpoint-labelled composition diagrams.

It also verifies the same composition law for:

- raw universal group-ring rows;
- canonical template classes after primitive monomial normalisation.

---

## 5. Universal group-ring covariance

Using the fixed \(G\)-orbit coordinates, let

\[
P^{(e)}_\sigma(x)
\]

be the universal group-ring row in endpoint chart \(e\).

For every normalizer element and every KK coordinate,

\[
\boxed{
n\!\left(P^{(e)}_\sigma(x)\right)
=
P^{(n(e))}_{n(\sigma)}(x).
}
\]

Thus the universal template construction is covariant throughout the full
normalizer endpoint orbit.

---

## 6. Two endpoint-chart classes

The four independently reconstructed 21-template catalogues satisfy

\[
\boxed{
\mathcal T_7=\mathcal T_8,
\qquad
\mathcal T_5=\mathcal T_6.
}
\]

Hence there are exactly two distinct endpoint chart classes:

\[
C_{78}=\{7,8\},
\qquad
C_{56}=\{5,6\}.
\]

Each catalogue has multiplicity distribution

\[
16^{\times3},\qquad8^{\times6},\qquad4^{\times12}.
\]

The two chart classes have

\[
|\mathcal T_{78}\cap\mathcal T_{56}|=8,
\]

\[
|\mathcal T_{78}\setminus\mathcal T_{56}|
=
|\mathcal T_{56}\setminus\mathcal T_{78}|
=13,
\]

and

\[
\boxed{
|\mathcal T_{78}\cup\mathcal T_{56}|=34.
}
\]

No normalizer element generates a template outside this 34-class atlas.

---

## 7. Quotient action on the atlas

The action on canonical template classes factors through

\[
N/G\cong C_2.
\]

The theorem target is:

1. every element of \(G\) acts trivially on the 34 canonical classes;
2. every element of the nontrivial coset induces the same involution;
3. the 34 classes decompose into
   
   \[
   \boxed{2\text{ fixed classes}+16\text{ two-cycles}},
   \]
   
   giving
   
   \[
   \boxed{18\text{ quotient orbits}}.
   \]

The endpoint orbit of 8 under \(N\) is uniform:

\[
5^{\times4},\quad6^{\times4},\quad7^{\times4},\quad8^{\times4}.
\]

Elements of \(G\) keep endpoint 8 inside \(C_{78}\); elements of the other
coset send it into \(C_{56}\).

---

## 8. Exact theorem targeted

A successful run proves:

> For every element of the order-16 normalizer and every endpoint in
> \(\{5,6,7,8\}\), the exact KK coordinate systems are covariant, their
> transition maps satisfy strict cocycle consistency, and their universal
> template catalogues form a closed 34-class atlas. The canonical class
> action factors through \(N/G\cong C_2\), producing two endpoint-chart
> classes and 18 residual atlas orbits.

---

## 9. Claim boundary

03J is restricted to:

- the fixed anchor-1 chart;
- the reference target fibre \(A=\{2,3,4\}\);
- the normalizer orbit of endpoints \(\{5,6,7,8\}\);
- the eight-point KK relation space arising in the fixed-anchor \(9\to8\)
  theorem.

It does not yet prove:

- anchor covariance;
- endpoint-atlas covariance outside this normalizer orbit;
- a general \(n\)-point cocycle theorem;
- physical or phenomenological significance.

---

## 10. Run command

```bash
caffeinate -i python3 scripts/ehf_amp_found_03j_full_normalizer_endpoint_atlas_cocycle.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --normal-form-script scripts/ehf_amp_found_03e_exact_signed_orbit_normal_form.py \
  --template-script scripts/ehf_amp_found_03g_parameterised_shuffle_antisymmetriser_templates.py \
  --normalizer-script scripts/ehf_amp_found_03h_group_ring_factor_normalizer_audit.py \
  --endpoint-script scripts/ehf_amp_found_03i_kk_endpoint_covariance_normalizer_closure.py \
  --out-dir runs/ehf_amp_found_03j \
  --strict
```

No saved output files from 03G, 03H or 03I are required.

---

## 11. Principal outputs

```text
summary.json
verdict.json
run.log
exact_full_normalizer_endpoint_atlas_certificate.json
endpoint_chart_summary.csv
normalizer_element_ledger.csv
normalizer_endpoint_covariance.csv
normalizer_template_transitions.csv
normalizer_transition_cocycle_audit.csv
full_normalizer_template_atlas.csv
normalizer_quotient_orbits.csv
exact_full_normalizer_endpoint_atlas_audit.md
```

The target terminal result is:

```text
Full normalizer endpoint covariance
  target-fibre stabilizer order:      144
  G order:                            8
  normalizer order:                   16
  all 64 coordinate identities:       True
  all 64 kernel covariances:          True
  all 64 universal covariances:       True
  all 64 catalogue bijections:        True

Endpoint-chart atlas
  T7 = T8:                            True
  T5 = T6:                            True
  chart overlap:                      8
  full normalizer closure:            34
  quotient atlas orbits:              18
  orbit-size distribution:           {1: 2, 2: 16}

Cocycle consistency
  state transitions:                  True
  KK row transitions:                 True
  raw group-ring action:              True
  canonical template classes:         True
  action factors through N/G ~= C2:   True

Verdict:
EHF_AMP_FOUND_03J_EXACT_FULL_NORMALIZER_ENDPOINT_ATLAS_AND_COCYCLE_PROVED

strict checks: PASS
```
