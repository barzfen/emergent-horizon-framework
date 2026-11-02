# EHF-AMP-FOUND-03K
## Anchor-Change Covariance and Full Fibre-Atlas Closure

**Status:** exact all-anchor covariance theorem  
**Transition:** fixed deleted label9, all surviving anchors `1,...,8`  
**Coefficient domain:** `QQ`

---

## 1. Purpose

The exact nine-to-eight theorem was initially formulated in the anchor-1
canonical chart. Probes 03I and 03J established exact covariance under changes
of the **KK endpoint**, but retained anchor1.

03K asks the next structural question:

> Does the complete delete-9 fibre system transform covariantly when the
> anchor itself is changed to any surviving label?

The probe covers all eight surviving anchors and all 35 active fibres in each
anchor chart.

---

## 2. Anchor-relative charts

For a surviving anchor

\[
a\in\{1,2,3,4,5,6,7,8\},
\]

rotate every undirected cycle to begin at `a` and choose the lexicographically
smaller of the two orientations.

For a three-subset

\[
A\subset\{1,\ldots,8\}\setminus\{a\},
\qquad |A|=3,
\]

define the source and target fibres

\[
F_{a,A}^{(9)}:
\quad E=\{a,9\}\cup A,
\quad O=\{1,\ldots,8\}\setminus(\{a\}\cup A),
\]

and

\[
F_{a,A}^{(8)}:
\quad E=\{a\}\cup A,
\quad O=\{1,\ldots,8\}\setminus(\{a\}\cup A).
\]

Because label9 is maximal, anchor-relative reflection reduction always places
an adjacent9 immediately **before** the anchor. Consequently every active
channel remains one-sided and diagonal:

\[
F_{a,A}^{(9)}\longrightarrow F_{a,A}^{(8)}.
\]

There are 35 channels for each anchor and 280 channels in the complete atlas.

---

## 3. Canonical anchor normalisation

Define

\[
\rho_a(a)=1,
\qquad
\rho_a(9)=9,
\]

and send the remaining labels in

\[
\{1,\ldots,8\}\setminus\{a\}
\]

in increasing order to

\[
2,3,\ldots,8.
\]

The normalised subset is

\[
A_a'=\rho_a(A)\subset\{2,\ldots,8\}.
\]

This provides one deterministic comparison between every anchor chart and the
original anchor-1 chart.

---

## 4. Signed source-state transport

At nine points, reflection is odd:

\[
\operatorname{PT}(c^{\mathrm{rev}})=-\operatorname{PT}(c).
\]

Therefore anchor normalisation gives a signed state permutation

\[
P_a:F_{a,A}^{(9)}\longrightarrow F_{1,A_a'}^{(9)}.
\]

The sign records whether relabelling and return to the global anchor-1
canonical representative requires reversal.

At eight points the reflection character is positive, so the target transport

\[
T_a:F_{a,A}^{(8)}\longrightarrow F_{1,A_a'}^{(8)}
\]

is unsigned.

---

## 5. Exact covariance equations

Let

\[
Q_A^{(a)}
\]

be the exact KK matrix in basis

\[
\operatorname{PT}(a,\sigma,9),
\]

and let

\[
D_A^{(a)}
\]

be the exact signed delete-9 matrix.

The theorem target is

\[
\boxed{
Q_{A_a'}^{(1)}P_a=R_aQ_A^{(a)},
}
\]

and

\[
\boxed{
D_{A_a'}^{(1)}P_a=T_aD_A^{(a)}.
}
\]

Here `R_a` is the exact row relabelling of the KK basis induced by
\(\rho_a\).

03K verifies these equations column by column in exact integer arithmetic for
every source state in all 280 channels.

---

## 6. Consequences for transmitted images

The two covariance equations imply

\[
T_a\,D_A^{(a)}(\ker Q_A^{(a)})
=
D_{A_a'}^{(1)}(\ker Q_{A_a'}^{(1)}).
\]

Therefore the exact transmitted rank in anchor chart `a` is the anchor-1 rank
of the normalised triple \(A_a'\).

If

\[
A_a'=\{u<v<w\},
\]

the exact rank is

\[
r_{a,A}=
\begin{cases}
0,&v\le4,\ w\le5,\\
2,&v\le4,\ w=6,\\
9,&v\le4,\ w\ge7,\\
8,&v=5,\ w=6,\\
14,&v=5,\ w\ge7,\\
15,&v\ge6.
\end{cases}
\]

Thus the law is an **anchor-normalised two-rightmost-label law**.

---

## 7. Full atlas census

Each anchor has rank multiplicities

\[
0^{\times4},
\quad2^{\times3},
\quad8^{\times3},
\quad9^{\times6},
\quad14^{\times6},
\quad15^{\times13}.
\]

Across all eight anchors, the multiplicities are

\[
\boxed{
0^{\times32},
\quad2^{\times24},
\quad8^{\times24},
\quad9^{\times48},
\quad14^{\times48},
\quad15^{\times104}.
}
\]

The total transmitted rank counted over anchor charts is

\[
8\cdot363=2904.
\]

After anchor normalisation and ordered-block transport, all 280 images collapse
to the same six spaces

\[
\boxed{V_0,V_2,V_8,V_9,V_{14},V_{15}.}
\]

---

## 8. Anchor transition cocycle

For anchors `a,b`, define

\[
\pi_{b\leftarrow a}=\rho_b^{-1}\rho_a.
\]

For every triple of surviving anchors,

\[
\boxed{
\pi_{c\leftarrow b}\pi_{b\leftarrow a}
=
\pi_{c\leftarrow a}.
}
\]

03K checks the induced cocycle on:

1. signed nine-point source-state maps;
2. unsigned eight-point target-state maps;
3. exact KK-row relabellings;
4. the 35 fibre labels in every anchor chart;
5. the transported image assignment.

The audit contains all

\[
8^3=512
\]

anchor-labelled composition diagrams.

---

## 9. Exact theorem targeted

A successful run proves:

> With label9 fixed as the deleted leg, the complete nine-to-eight
> parity-fibre relation system is exactly covariant across all eight surviving
> anchors. The 280 anchor-relative channels form a closed cocycle-consistent
> atlas. Under canonical anchor normalisation, every channel reduces to the
> original anchor-1 theorem and all transmitted images select the same six
> target subspaces.

---

## 10. Claim boundary

03K does not yet prove:

- a chart with deleted label9 also serving as anchor;
- covariance under changing the deleted leg;
- a simultaneous all-anchor/all-deleted-leg atlas;
- a general result at multiplicity above nine;
- physical dynamics or phenomenological utility.

The theorem is exact for the stated anchor normalisations and the fixed
delete-9 transition.

---

## 11. Run command

```bash
caffeinate -i python3 scripts/ehf_amp_found_03k_anchor_change_covariance_full_fibre_atlas.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --rank-script scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --lattice-script scripts/ehf_amp_found_03c_exact_tail_filtration_lattice.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --out-dir runs/ehf_amp_found_03k \
  --strict
```

---

## 12. Principal outputs

```text
summary.json
verdict.json
run.log
exact_anchor_covariance_certificate.json
anchor_chart_summary.csv
all_anchor_channel_ledger.csv
all_anchor_subspace_class_summary.csv
anchor_transition_cocycle_audit.csv
exact_anchor_covariance_audit.md
```

The target terminal result is:

```text
Full surviving-anchor atlas
  anchors:                            8
  channels per anchor:                35
  total anchor-fibre channels:        280
  active source incidences:           40320
  rank multiplicities full atlas:     {0: 32, 2: 24, 8: 24, 9: 48, 14: 48, 15: 104}
  common transported subspaces:       6

Exact anchor covariance
  source state bijections:            True
  target state bijections:            True
  KK column covariance:               True
  delete-map covariance:              True
  diagonal target fibres:             True
  two preimages per target:           True
  anchor-normalised rank law:         True
  six-space collapse:                 True

Anchor transition cocycle
  permutation cocycle:                True
  signed source-state cocycle:        True
  target-state cocycle:               True
  KK-row cocycle:                     True
  fibre-chart cocycle:                True

Verdict:
EHF_AMP_FOUND_03K_EXACT_ALL_ANCHOR_FIBRE_ATLAS_COVARIANCE_PROVED
strict checks: PASS
```
