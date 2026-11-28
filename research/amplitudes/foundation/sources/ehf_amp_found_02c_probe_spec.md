# EHF-AMP-FOUND-02C
## Branch-Reversal Equivariance and Full Residue-Image Sections

**Status:** executable probe specification  
**Programme:** EHF amplitude foundations  
**Primary transition:** \(7\to8\)  
**Dependencies:** reflection-aware EHF-AMP-FOUND-02A v0.3 and EHF-AMP-FOUND-02B

---

## 1. Motivation

EHF-AMP-FOUND-02B established, at two independent kinematic seeds, that the reflection-aware delete-8 map

\[
D_8:\mathcal R^{\mathrm{loc}}_8\longrightarrow \mathbb R^{X_7}
\]

has rank \(110\) on the \(525\)-dimensional direct sum of eight-point fibre-local Parke–Taylor relation spaces. The complete \(38\)-dimensional seven-point fibre-local sector lies inside that image and therefore admits an exact linear section.

Two unresolved issues remain.

1. The canonical chart showed a complete branch asymmetry: the minus-side residue alone reconstructed the local target sector, while the plus-side residue did not.
2. The section in 02B was defined only on the \(38\)-dimensional fibre-local target sector, even though the complete residue image has dimension \(110\). The exceptional AMP-18 missing direction residues into the remaining nonlocal part.

02C addresses both issues.

---

## 2. Exact chart observation

Canonical cycles are represented with anchor \(1\) first and

\[
c_1<c_{n-1}.
\]

For an eight-point canonical cycle, the newly inserted maximum label \(8\) cannot occupy the position immediately after the anchor: that would require

\[
8<c_7,
\]

which is impossible. Therefore, in the standard representative chart, every anchor-adjacent occurrence of label \(8\) appears on the opposite side of the anchor.

Consequently, the observed one-sided asymmetry may be entirely a chart convention. The opposite representative chart, obtained by reversing every canonical cycle, should exchange the two branch labels.

This is not assumed. The script reconstructs the opposite-chart residue operators directly and tests the conjugation law.

---

## 3. Branch-reversal equivariance

Let \(D_+\) and \(D_-\) denote deletion of label \(8\) when it lies immediately after or immediately before anchor \(1\), including the collinear side sign and the Parke–Taylor reflection character.

Let

\[
J_n=(-1)^n I
\]

be the coefficient-coordinate transition between standard and reversed representative charts. The probe tests

\[
D^{\mathrm{opp}}_+
=
J_7D^{\mathrm{std}}_-J_8^{-1},
\]

\[
D^{\mathrm{opp}}_-
=
J_7D^{\mathrm{std}}_+J_8^{-1},
\]

and

\[
D^{\mathrm{opp}}
=
J_7D^{\mathrm{std}}J_8^{-1}.
\]

It also repeats the one-sided section test in the opposite chart.

### Interpretation criterion

If the exact operator identities hold and the successful one-sided section swaps from minus to plus, then the prior plus/minus asymmetry is a **canonical-chart orientation effect**, not an invariant chirality.

---

## 4. Full residue-image section

Let

\[
A=D_8B_8,
\]

where \(B_8\) is an orthonormal basis of the \(525\)-dimensional direct sum of eight-point fibre-local relations.

The complete residue image is

\[
\mathcal I_7=\operatorname{im}A,
\qquad
\dim\mathcal I_7=110
\]

according to 02B.

02C constructs an orthonormal basis \(Q_{\mathcal I}\) of this image and the rank-truncated Moore–Penrose section

\[
L_{\mathcal I}
=
B_8A^+Q_{\mathcal I}.
\]

The defining test is

\[
D_8L_{\mathcal I}=Q_{\mathcal I}.
\]

Fresh Parke–Taylor evaluations validate both source and target vectors.

---

## 5. Local/nonlocal decomposition

The seven-point fibre-local sector is

\[
\mathcal R^{\mathrm{loc}}_7
=
\bigoplus_F R_7(F),
\qquad
\dim\mathcal R^{\mathrm{loc}}_7=38.
\]

Because this sector lies inside \(\mathcal I_7\), the probe constructs the orthogonal complement inside the residue image:

\[
\mathcal I^{\mathrm{nonlocal}}_7
=
\mathcal I_7
\ominus
\mathcal R^{\mathrm{loc}}_7.
\]

The expected dimension is

\[
110-38=72.
\]

The word **nonlocal** here means only that the relation is not supported inside one seven-point fibre, nor in the direct sum of fibre-local relation spaces. It does not imply physical spatial nonlocality.

The probe verifies

\[
\mathcal I_7
=
\mathcal R^{\mathrm{loc}}_7
\oplus
\mathcal I^{\mathrm{nonlocal}}_7
\]

numerically, including orthogonality, rank and Parke–Taylor validity.

---

## 6. Branch image geometry

The script computes:

- \(\dim\operatorname{im}D_+B_8\);
- \(\dim\operatorname{im}D_-B_8\);
- their intersection dimension;
- the rank of their independent sum;
- the rank of the coupled full-residue image \(\operatorname{im}(D_++D_-)B_8\);
- containment of the local and nonlocal target sectors in each branch image.

The independent sum permits separate source coefficients in the two branches. The coupled full residue uses the same source relation coefficients in both terms. These are distinct linear constructions and are reported separately.

---

## 7. Exceptional AMP-18 direction

Let \(v_*\) be the unique relation direction in the exceptional eight-point fibre

\[
E=\{1,4,5,6\},
\qquad
O=\{2,3,7,8\}
\]

that is absent from the anchor-1 AMP-18 arrival span.

Its residue is

\[
y_*=D_8v_*.
\]

02B showed that \(y_*\) is a valid global seven-point relation but lies completely outside the \(38\)-dimensional fibre-local target sector.

02C tests:

1. whether \(y_*\) lies in the full \(110\)-dimensional image;
2. whether it lies entirely in the \(72\)-dimensional nonlocal complement;
3. whether it belongs to the plus or minus branch image;
4. the global Moore–Penrose preimage of \(y_*\);
5. the support of that preimage across eight-point fibres;
6. the difference between the global minimum-norm preimage and the original \(v_*\);
7. whether that difference lies in the \(415\)-dimensional source kernel;
8. whether \(v_*\) remains the minimum-norm preimage when support is restricted to its own exceptional fibre.

A difference between the global and fibre-restricted preimages is expected and is not a contradiction. It measures the freedom to add source-kernel relations and to redistribute ancestry across fibres.

---

## 8. Numerical controls

The probe uses:

- reflection-aware canonicalisation;
- rank-truncated SVD throughout;
- positive span-membership control;
- negative orthogonal-complement control;
- fresh Parke–Taylor validation;
- singular-value spectra for full, branch and nonlocal spaces;
- explicit operator-level reversal identities;
- independent source and target relation checks.

No wide-matrix QR span-membership test is used.

---

## 9. Run command

Place the script and this specification in `scripts/`, then run:

```bash
caffeinate -i python3 scripts/ehf_amp_found_02c_branch_reversal_full_image_sections.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --section-script scripts/ehf_amp_found_02b_minimal_nontrivial_growth_sections.py \
  --base-run-dir runs/ehf_amp_found_01_amp18_20 \
  --out-dir runs/ehf_amp_found_02c_seed11 \
  --seed 11
```

The existing base cache should make the run fast.

A second-seed reproduction should use:

```bash
caffeinate -i python3 scripts/ehf_amp_found_02c_branch_reversal_full_image_sections.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --section-script scripts/ehf_amp_found_02b_minimal_nontrivial_growth_sections.py \
  --base-run-dir runs/ehf_amp_found_01_amp18_20 \
  --out-dir runs/ehf_amp_found_02c_seed29 \
  --seed 29
```

---

## 10. Principal outputs

```text
summary.json
run.log
branch_reversal_audit.json
full_image_section_audit.json
exceptional_full_image_audit.json
branch_image_summary.csv
residue_image_singular_spectrum.csv
full_image_section_block_weights.csv
exceptional_global_mp_support.csv
full_image_section_operator_data.npz
relation_basis_summary.csv
```

The three most important files for the first audit are:

```text
branch_reversal_audit.json
full_image_section_audit.json
exceptional_full_image_audit.json
```

---

## 11. Claim boundary

A successful probe would establish:

- exact reversal conjugacy of the two branch labels;
- an exact algebraic section on the full rank-110 residue image;
- a precise \(38+72\) local/nonlocal decomposition;
- a valid full-image ancestry for the exceptional relation.

It would not establish:

- a preferred physical inner product;
- a unique physical growth law;
- locality in emergent spacetime;
- particle content;
- a derivation of gauge theory.

The immediate mathematical question is whether the apparent branch directionality survives reversal of the representative chart. The immediate structural question is how the exceptional relation sits inside the complete nonlocal residue sector.
