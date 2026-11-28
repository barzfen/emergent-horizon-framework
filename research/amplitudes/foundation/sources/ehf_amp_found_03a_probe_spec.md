# EHF-AMP-FOUND-03A  
## Odd-to-Even Diagonal Channel Census at \(9\to8\)

**Status:** numerical rank census with exact combinatorial incidence  
**Chart:** fixed anchor \(1\), standard canonical representative  
**Transition:** reflection-aware deletion of label \(9\)

---

## 1. Purpose

The exact \(8\to7\) theorem established ten complement-pair channels:

\[
20\text{ active source fibres}
\longrightarrow
10\text{ glued rank-11 channels}.
\]

The next question is whether the adjacent odd-to-even transition has a
different channel architecture.

For the standard anchor-\(1\) chart at \(n=9\), the candidate structure is

\[
35\text{ active source fibres}
\longrightarrow
35\text{ diagonal target channels}.
\]

03A tests that statement and measures the complete channel-rank profile.

---

## 2. Active source fibres

Let

\[
U=\{2,3,4,5,6,7,8\}.
\]

For every \(A\in\binom U3\), define the \(n=9\) source fibre

\[
F_A^{(9)}:
\qquad
E=\{1,9\}\cup A,
\qquad
O=U\setminus A.
\]

There are

\[
\binom73=35
\]

such fibres.

In the standard canonical chart, label \(9\) is the greatest label. The
condition selecting the canonical reflection representative prevents it from
appearing immediately after the anchor. Therefore all anchor-adjacent
delete-\(9\) states occur on the “before-anchor” side.

Each source fibre has exactly \(144\) delete-\(9\)-active states.

---

## 3. Exact diagonal map

Deleting \(9\) from \(F_A^{(9)}\) gives the unique target fibre

\[
F_A^{(8)}:
\qquad
E=\{1\}\cup A,
\qquad
O=U\setminus A.
\]

Thus the proposed combinatorial law is

\[
A\longmapsto A.
\]

03A verifies exactly:

1. one target fibre per active source fibre;
2. preservation of the subset label \(A\);
3. a bijection between the 35 sources and 35 targets;
4. \(144\) active source states per channel;
5. two source preimages for every one of the \(72\) target states;
6. a minus-only standard chart.

The one-sided branch is a canonical-chart orientation effect, not physical
chirality.

---

## 4. Relation-space map

Let

\[
R_A^{(9)}
\subseteq
\mathbb R^{|F_A^{(9)}|}
\]

be the local nine-point Parke--Taylor relation space and let

\[
R_A^{(8)}
\subseteq
\mathbb R^{72}
\]

be the \(15\)-dimensional target relation space.

The exact signed incidence matrix is

\[
D_A:
\mathbb R^{|F_A^{(9)}|}
\longrightarrow
\mathbb R^{72}.
\]

For a validated source basis \(N_A^{(9)}\), define the residue image

\[
I_A=D_AN_A^{(9)}.
\]

The channel rank is

\[
r_A=\operatorname{rank}I_A.
\]

03A checks independently that

\[
I_A\subseteq R_A^{(8)}
\]

using both:

- fresh Parke--Taylor evaluations;
- numerical subspace containment in the independently constructed target
  local basis.

---

## 5. Global direct-sum law

Distinct \(A\)-channels occupy disjoint target fibres. Hence their target
supports do not overlap.

Once target-local containment is established,

\[
\operatorname{rank}
\left(
\bigoplus_A I_A
\right)
=
\sum_A r_A.
\]

The known aggregate targets from the earlier growth--factorisation audit are

\[
\sum_A r_A=363
\]

and

\[
\#\{A:r_A=15\}=13.
\]

03A recomputes these values channel by channel rather than treating them as
global black-box outputs.

The complete target local sector has dimension

\[
35\cdot15=525,
\]

so the expected fixed-chart deficit is

\[
525-363=162.
\]

---

## 6. Rank-profile diagnostics

The source fibres are naturally indexed by the 35 vertices of \(J(7,3)\).
03A records for every \(A\):

- its binary word in the ordered labels \(2,\ldots,8\);
- inversion count between \(A\) and \(A^c\);
- gap composition;
- number of runs;
- source fibre size;
- source relation dimension;
- residue rank;
- source residue-kernel dimension;
- target missing dimension;
- complete/partial recovery status.

The source fibre size has the exact chart formula

\[
|F_A^{(9)}|
=
36\bigl(4+\iota(A)\bigr),
\]

where

\[
\iota(A)
=
\#\{(a,b)\in A\times A^c:a>b\}.
\]

The probe tests whether the residue rank is determined by this coarse
statistic or requires finer binary-word data.

It also outputs:

- rank differences along the edges of \(J(7,3)\);
- nonedge comparisons;
- the ordered-label reflection
  \[
  A\mapsto\{10-a:a\in A\};
  \]
- feature/rank Pearson and Spearman correlations.

These are exploratory diagnostics, not theorem claims.

---

## 7. Channel classes

Each channel is assigned one of:

```text
NO_SOURCE_RELATIONS
SOURCE_LIMITED_INJECTIVE
CAPACITY_SATURATED_PARTIAL_TARGET
LOSSY_PARTIAL
TARGET_COMPLETE_INJECTIVE
TARGET_COMPLETE_WITH_SOURCE_KERNEL
```

This distinguishes failure caused by absent source relations from genuine
loss under factorisation.

---

## 8. Claim boundary

A successful 03A run supports:

> In the fixed anchor-\(1\) chart, reflection-aware \(9\to8\) factorisation
> is diagonal at the parity-fibre level. Each of the 35 active nine-point
> fibres maps into the uniquely \(A\)-labelled eight-point fibre. The
> transmitted local relation rank is nonuniform, sums to \(363\), and
> completely recovers 13 of the 35 target local spaces.

It does **not** yet establish:

- an exact symbolic formula for \(r_A\);
- an anchor-independent odd-to-even theorem;
- a universal parity-alternating law for all \(n\);
- a physical interpretation of the rank profile.

The exact combinatorial map and the numerical rank census must remain
distinguished.

---

## 9. Run command

```bash
caffeinate -i python3 scripts/ehf_amp_found_03a_odd_even_diagonal_channel_census.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --base-run-dir runs/ehf_amp_found_01_amp18_20 \
  --out-dir runs/ehf_amp_found_03a \
  --seed 11 \
  --strict
```

The script reuses the successful relation-basis cache convention:

\[
n=8:\ \text{seed }18,
\qquad
n=9:\ \text{seed }12
\]

when the master seed is \(11\).

A cache directory can be supplied directly with `--cache-dir`.

---

## 10. Structural smoke test

```bash
python3 scripts/ehf_amp_found_03a_odd_even_diagonal_channel_census.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --out-dir runs/ehf_amp_found_03a_structure_smoke \
  --structure-only
```

This performs the complete 35-channel combinatorial audit without constructing
Parke--Taylor relation bases.

---

## 11. Principal outputs

```text
summary.json
verdict.json
run.log
diagonal_structure_ledger.csv
relation_basis_summary.csv
diagonal_channel_census.csv
rank_distribution.csv
feature_group_summary.csv
feature_rank_correlations.csv
johnson_pair_rank_audit.csv
label_order_reflection_audit.csv
```

The expected terminal summary is:

```text
Fixed-anchor diagonal structure:      True
All residue images target-local:     True
All residue images PT-valid:         True
Global direct-sum rank:               363
Expected global rank:                 363
Complete target fibres:               13/35
Expected complete targets:            13
Verdict: EHF_AMP_FOUND_03A_FIXED_ANCHOR_DIAGONAL_CHANNEL_LAW_SUPPORTED
strict checks:                        PASS
```
