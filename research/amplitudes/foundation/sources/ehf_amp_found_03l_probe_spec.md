# EHF-AMP-FOUND-03L  
## Deleted-Leg Covariance and the Full Anchor–Deletion Atlas

**Status:** exact all-chart covariance audit  
**Transition:** fixed multiplicity reduction from nine points to eight points  
**Charts:** all ordered anchor–deletion pairs

---

## 1. Purpose

03K proved exact covariance across all surviving anchors while the deleted leg
remained label `9`.

03L removes the final label preference. It tests every ordered pair

\[
(a,d),\qquad a\ne d,
\]

where:

- \(a\) is the surviving anchor;
- \(d\) is the deleted leg.

There are

\[
9\cdot8=72
\]

anchor–deletion charts.

The target theorem is:

> Every chart is an exact relabelled copy of the reference chart
> \((a,d)=(1,9)\), and all 2520 chart-relative fibre channels reduce to the
> same six-space tail-filtration lattice.

---

## 2. Canonical chart normalisation

For each ordered pair \((a,d)\), define

\[
\rho_{a,d}(a)=1,
\qquad
\rho_{a,d}(d)=9,
\]

and send the remaining seven labels increasingly to

\[
2,3,4,5,6,7,8.
\]

The chart orientation is defined by pullback from the reference chart:

> A chart ordering \(c\) is canonical when \(\rho_{a,d}(c)\) is canonical in
> the standard anchor-1, deleted-9 chart.

This convention is essential. A raw numerical reversal convention cannot
simultaneously privilege every possible deleted label.

---

## 3. Chart fibres

Let

\[
A\subset\{1,\ldots,9\}\setminus\{a,d\},
\qquad |A|=3.
\]

The source fibre is

\[
E=\{a,d\}\cup A,
\qquad
O=\{1,\ldots,9\}\setminus E.
\]

After deleting \(d\), the target fibre is

\[
E'=\{a\}\cup A,
\qquad
O'=\bigl(\{1,\ldots,9\}\setminus\{d\}\bigr)\setminus E'.
\]

Every chart therefore contains

\[
\binom73=35
\]

channels.

The full atlas contains

\[
72\cdot35=2520
\]

chart-relative channels.

---

## 4. Exact covariance equations

Let \(P_{a,d}\) transport source states, \(T_{a,d}\) transport target states,
and \(R_{a,d}\) relabel the KK basis.

For every chart and every local fibre \(A\), 03L tests

\[
\boxed{
Q^{(1,9)}_{\rho_{a,d}(A)}P_{a,d}
=
R_{a,d}Q^{(a,d)}_A
}
\]

and

\[
\boxed{
D^{(1,9)}_{\rho_{a,d}(A)}P_{a,d}
=
T_{a,d}D^{(a,d)}_A.
}
\]

These are verified column by column using exact integer KK shuffle
coefficients and exact signed deletion maps.

---

## 5. Expected channel census

Every chart must reproduce

\[
0^{\times4},\quad
2^{\times3},\quad
8^{\times3},\quad
9^{\times6},\quad
14^{\times6},\quad
15^{\times13}.
\]

Across all 72 charts:

\[
\boxed{
0^{\times288},\quad
2^{\times216},\quad
8^{\times216},\quad
9^{\times432},\quad
14^{\times432},\quad
15^{\times936}.
}
\]

The chart-counted transmitted-rank sum is

\[
72\cdot363=26136.
\]

Each channel has 144 active source states and two active preimages per target
state. Hence the full atlas contains

\[
2520\cdot144=362880=9!
\]

active source incidences.

---

## 6. Common six-space lattice

After chart normalisation and ordered-block target transport, every channel
must select one of

\[
V_0,V_2,V_8,V_9,V_{14},V_{15}.
\]

Thus the rank law is neither anchor-specific nor deleted-label-specific. It is
an ordered-tail law in the normalised chart coordinates.

---

## 7. Full transition groupoid

For source chart \((a,d)\) and target chart \((b,e)\), define

\[
\pi_{(b,e)\leftarrow(a,d)}
=
\rho_{b,e}^{-1}\rho_{a,d}.
\]

For every ordered chart triple, 03L tests

\[
\boxed{
\pi_{(c,f)\leftarrow(b,e)}
\pi_{(b,e)\leftarrow(a,d)}
=
\pi_{(c,f)\leftarrow(a,d)}.
}
\]

There are

\[
72^3=373248
\]

ordered chart triples.

Because all state, target, KK-row, fibre and image maps are exact pullbacks of
these label permutations, the same cocycle holds on every level of the atlas.

---

## 8. Claim boundary

A successful run proves exact full anchor–deletion covariance at the finite
transition \(9\to8\), under the specified pullback chart convention and
ordered-block target transport.

It does not prove:

- the same law for \(11\to10\) or general odd multiplicity;
- independence from every possible chart convention;
- physical dynamics or phenomenological utility;
- a novelty claim relative to the amplitudes literature.

---

## 9. Run command

```bash
caffeinate -i python3 scripts/ehf_amp_found_03l_deleted_leg_covariance_full_anchor_deletion_atlas.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --rank-script scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --lattice-script scripts/ehf_amp_found_03c_exact_tail_filtration_lattice.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --anchor-script scripts/ehf_amp_found_03k_anchor_change_covariance_full_fibre_atlas.py \
  --out-dir runs/ehf_amp_found_03l \
  --strict
```

---

## 10. Principal outputs

```text
summary.json
verdict.json
run.log
exact_anchor_deletion_covariance_certificate.json
anchor_deletion_chart_summary.csv
full_anchor_deletion_channel_ledger.csv
deleted_leg_summary.csv
anchor_summary.csv
anchor_deletion_subspace_class_summary.csv
anchor_deletion_transition_ledger.csv
anchor_deletion_cocycle_failures.csv
exact_anchor_deletion_covariance_audit.md
```

The target terminal result is:

```text
Full anchor--deletion atlas
  charts:                             72
  channels per chart:                 35
  total chart-relative channels:      2520
  active source incidences:           362880
  common transported subspaces:       6

Exact anchor--deletion covariance
  source chart bijections:            True
  target chart bijections:            True
  KK row bijections:                  True
  fibre-label bijections:             True
  KK column covariance:               True
  delete-map covariance:              True
  diagonal target fibres:             True
  two preimages per target:           True
  normalised rank law:                True
  six-space collapse:                 True

Full chart-transition cocycle
  ordered chart triples:              373248
  permutation cocycle:                True
  source-state cocycle:               True
  target-state cocycle:               True
  KK-row cocycle:                     True
  fibre/image cocycle:                True

Verdict:
EHF_AMP_FOUND_03L_EXACT_FULL_ANCHOR_DELETION_ATLAS_COVARIANCE_PROVED
strict checks: PASS
```
