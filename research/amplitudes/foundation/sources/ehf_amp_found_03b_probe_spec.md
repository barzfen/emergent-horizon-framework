# EHF-AMP-FOUND-03B  
## Exact Two-Rightmost-Label Rank Law at \(9\to8\)

**Status:** direct exact KK rank theorem  
**Chart:** fixed anchor \(1\), standard canonical reflection representative  
**Transition:** reflection-aware delete-\(9\) factorisation

---

## 1. Purpose

03A proved the exact diagonal fibre map

\[
F_A^{(9)}\longrightarrow F_A^{(8)}
\]

and numerically measured the channel ranks

\[
0^{\times4},\quad
2^{\times3},\quad
8^{\times3},\quad
9^{\times6},\quad
14^{\times6},\quad
15^{\times13}.
\]

Inspection of the complete ledger suggested a sharper law. If

\[
A=\{a<b<c\}\subset\{2,\ldots,8\},
\]

then the rank appears to depend only on \(b,c\), not on \(a\).

03B proves that statement exactly over \(\mathbb Q\).

---

## 2. Exact rank identity

Let

\[
Q_A:
\mathbb Q^{|F_A^{(9)}|}
\longrightarrow
\mathbb Q^{5040}
\]

be the exact integer Kleiss--Kuijf coordinate matrix of the source fibre.
Then

\[
R_A^{(9)}=\ker Q_A
\]

is its exact local Parke--Taylor relation space.

Let

\[
D_A:
\mathbb Q^{|F_A^{(9)}|}
\longrightarrow
\mathbb Q^{72}
\]

be the exact signed delete-\(9\) incidence map.

The transmitted rank is

\[
r_A=\dim D_A(\ker Q_A).
\]

Using rank--nullity,

\[
\begin{aligned}
r_A
&=
\dim\ker Q_A
-
\dim(\ker Q_A\cap\ker D_A)\\
&=
\left(|F_A^{(9)}|-\operatorname{rank}Q_A\right)
-
\left(|F_A^{(9)}|-\operatorname{rank}
\begin{bmatrix}
Q_A\\D_A
\end{bmatrix}\right).
\end{aligned}
\]

Therefore

\[
\boxed{
r_A
=
\operatorname{rank}_{\mathbb Q}
\begin{bmatrix}
Q_A\\D_A
\end{bmatrix}
-
\operatorname{rank}_{\mathbb Q}Q_A.
}
\]

This avoids constructing a numerical or symbolic nullspace basis.

---

## 3. Exact matrix construction

For \(n=9\), the KK basis has dimension

\[
(9-2)!=5040.
\]

For every source ordering \((1,\alpha,9,\beta)\), its exact column in \(Q_A\)
is obtained from

\[
\operatorname{PT}(1,\alpha,9,\beta)
=
(-1)^{|\beta|}
\sum_{\sigma\in\alpha\shuffle\beta^{\mathrm T}}
\operatorname{PT}(1,\sigma,9).
\]

Thus \(Q_A\) is a sparse integer matrix of shape

\[
5040\times |F_A^{(9)}|.
\]

The stacked matrix has shape

\[
5112\times |F_A^{(9)}|.
\]

All ranks are computed exactly over \(\mathbb Q\) using SymPy
`DomainMatrix`. The probe uses no:

- random kinematics;
- numerical SVD;
- cached relation bases;
- seed;
- rational reconstruction.

---

## 4. Exact rank law

For

\[
A=\{a<b<c\},
\]

the exact transmitted rank is

\[
\boxed{
r_A=
\begin{cases}
0, & b\le4,\ c\le5,\\[2mm]
2, & b\le4,\ c=6,\\[2mm]
9, & b\le4,\ c\ge7,\\[2mm]
8, & b=5,\ c=6,\\[2mm]
14, & b=5,\ c\ge7,\\[2mm]
15, & b\ge6.
\end{cases}
}
\]

The smallest selected label \(a\) does not appear.

Equivalently, with gap coordinates

\[
(g_0,g_1,g_2,g_3)
=
(a-2,\ b-a-1,\ c-b-1,\ 8-c),
\]

the rank depends only on

\[
(g_0+g_1,\ g_3)
=
(b-3,\ 8-c).
\]

It is independent of the internal split of \(b-3\) into \(g_0\) and \(g_1\).

---

## 5. Exact multiplicities

For fixed \(b,c\), the number of allowed smallest labels is

\[
\#\{a:2\le a<b\}=b-2.
\]

Summing these counts over the six cells gives:

\[
\begin{array}{c|c|c}
\text{condition} & r_A & \text{number of channels}\\
\hline
b\le4,\ c\le5 & 0 & 4\\
b\le4,\ c=6 & 2 & 3\\
b\le4,\ c\ge7 & 9 & 6\\
b=5,\ c=6 & 8 & 3\\
b=5,\ c\ge7 & 14 & 6\\
b\ge6 & 15 & 13
\end{array}
\]

Hence

\[
0^{\times4},\quad
2^{\times3},\quad
8^{\times3},\quad
9^{\times6},\quad
14^{\times6},\quad
15^{\times13}.
\]

The global rank is exactly

\[
4(0)+3(2)+3(8)+6(9)+6(14)+13(15)=363.
\]

Exactly thirteen target fibres are recovered completely.

---

## 6. Why the result is nontrivial

The exact source relation dimension and source fibre size can vary as \(a\)
changes while \(b,c\) remain fixed, but \(r_A\) does not.

For example, every channel

\[
\{a,6,7\},
\qquad
a=2,3,4,5,
\]

has exact transmitted rank \(15\), even though the source relation dimensions
are not all equal.

Thus the rank law is not merely a reformulation of source relation-space
dimension or fibre size. The delete-\(9\) map retains a coarser right-tail
statistic of the ordered subset.

---

## 7. Relation to 03A

When the 03A ledger is supplied, 03B compares all 35 exact values against:

- the numerical source relation dimensions;
- the numerical transmitted ranks.

The required result is exact agreement in all 35 channels.

03B therefore upgrades the 03A rank census from:

> numerically stable and independently PT-validated

to:

> exact over \(\mathbb Q\), assuming the standard KK identity and KK-basis
> independence.

---

## 8. Claim boundary

A successful 03B run proves:

> In the fixed anchor-\(1\) chart at \(9\to8\), the diagonal local
> Parke--Taylor relation-transmission rank is an exact function of the two
> largest elements of \(A=\{a<b<c\}\) and is independent of \(a\).

It does not yet provide:

- a representation-theoretic explanation of the six values;
- an anchor-independent formulation;
- a theorem for general odd-to-even \(n\);
- a physical interpretation.

The next mathematical problem is to explain the six-cell law structurally,
not merely verify it.

---

## 9. Run command

```bash
caffeinate -i python3 scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --census-csv runs/ehf_amp_found_03a/diagonal_channel_census.csv \
  --out-dir runs/ehf_amp_found_03b \
  --strict
```

The computation is exact and requires no cache.

---

## 10. Principal outputs

```text
summary.json
verdict.json
run.log
exact_rank_law_certificate.json
exact_channel_rank_ledger.csv
two_rightmost_pair_table.csv
six_cell_rank_law.csv
exact_rank_distribution.csv
exact_label_reflection_audit.csv
```

The terminal target is:

```text
Exact QQ channel ranks:              True
Rank independent of smallest a:      True
Six-cell (b,c) law matches 35/35:    True
Rank distribution:                   {0: 4, 2: 3, 8: 3, 9: 6, 14: 6, 15: 13}
Global direct-sum rank:               363
Complete target fibres:               13/35
03A numerical census exact match:     True
Verdict: EHF_AMP_FOUND_03B_EXACT_TWO_RIGHTMOST_LABEL_RANK_LAW_PROVED
strict checks:                        PASS
```
