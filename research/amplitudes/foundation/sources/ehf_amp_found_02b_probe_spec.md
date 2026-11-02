# EHF-AMP-FOUND-02B — Minimal Nontrivial Growth Sections

**Status:** executable probe specification  
**Primary transition:** \(7\to8\)  
**Layer:** move-independent Hamilton-cycle ordering / Parke–Taylor relation layer  
**Dependencies:** EHF-AMP-FOUND-01 reproducibility machinery and reflection-aware EHF-AMP-FOUND-02A v0.3

## 1. Motivation

EHF-AMP-FOUND-02A established, across independent kinematic seeds, that:

1. the reflection-aware delete-8 residue of eight-point chamber-local relations contains the complete nonzero seven-point chamber-local relation sector;
2. the seven-point local relation sector has total dimension \(38\);
3. unchanged-coefficient insertion succeeds for none of the \(20\) genuine parent/branch cases;
4. the exceptional fifteenth relation in the \(n=8\) fibre
   \[
   E=\{1,4,5,6\},\qquad O=\{2,3,7,8\}
   \]
   has a nonzero, relation-valid seven-point residue but is not a naive insertion lift.

Thus the state-level section
\[
D_8 I_7^\pm=\operatorname{id}
\]
does not lift directly to the relation layer, while an abstract relation-level right inverse must exist.

The purpose of 02B is to construct that right inverse explicitly and measure how nonlocal or nontrivial it must be.

## 2. Fixed spaces

Let
\[
\mathcal R_7^{\mathrm{loc}}
 = \bigoplus_{F\in\Pi_1(7)} R_7(F),
\]
where zero-dimensional fibre spaces are included formally but omitted from nonvacuous counts. The reproduced total dimension is
\[
\dim\mathcal R_7^{\mathrm{loc}}=38.
\]

Let
\[
\mathcal R_8^{\mathrm{loc}}
 = \bigoplus_{G\in\Pi_1(8)} R_8(G).
\]
Each of the \(35\) eight-point fibres has relation dimension \(15\), so
\[
\dim\mathcal R_8^{\mathrm{loc}}=525.
\]

Let
\[
D_8:\mathbb R^{X_8}\to\mathbb R^{X_7}
\]
be the reflection-aware signed delete-8 map. It is nonzero only when label 8 is adjacent to anchor 1. Its sign is the product of:

- the collinear side sign, \(+\) after the anchor and \(-\) before it;
- the Parke–Taylor reflection character introduced if the reduced seven-point ordering must be reversed during canonicalisation.

Restricting to the local eight-point relation sector gives
\[
A=D_8 B_8,
\]
where the columns of \(B_8\) are an orthonormal ambient basis of \(\mathcal R_8^{\mathrm{loc}}\).

The target basis \(B_7\) is an orthonormal ambient basis of \(\mathcal R_7^{\mathrm{loc}}\).

## 3. Main construction

The primary section is the rank-truncated Moore–Penrose solution
\[
C=A^+B_7,
\qquad
L=B_8C.
\]

The probe tests
\[
D_8L=B_7.
\]

If the reconstruction residual is below tolerance, \(L\) is an explicit constant linear right inverse on the complete chamber-local seven-point sector.

### Interpretation guardrail

The Moore–Penrose section is canonical only after choosing the ordinary Euclidean inner product on ordering coefficients. Exact reconstruction proves existence of an algebraic section. It does **not** prove that this dense minimum-norm section is the physical growth law, nor that the Euclidean metric is preferred by EHF.

## 4. Questions

### Q1. Exact algebraic section

Does the minimum-norm section satisfy
\[
\|D_8L-B_7\|_{\mathrm{rel}}<10^{-7}?
\]

Controls:

- a positive residue-span vector must project with residual near zero;
- a constructed vector in the orthogonal complement must retain residual near one;
- the lifted columns must remain valid eight-point Parke–Taylor relations at fresh kinematics;
- the reconstructed columns must remain valid seven-point relations.

### Q2. Image rank and ambiguity

Measure
\[
\operatorname{rank}(D_8|_{\mathcal R_8^{\mathrm{loc}}})
\]
and the kernel dimension
\[
525-\operatorname{rank}(D_8|_{\mathcal R_8^{\mathrm{loc}}}).
\]

A large kernel means lower-point relation data do not select a unique eight-point ancestor.

### Q3. Branch-only sections

Split
\[
D_8=D_8^+ + D_8^-.
\]

Test independently whether
\[
D_8^+L^+=B_7
\]
or
\[
D_8^-L^-=B_7
\]
can be solved. This determines whether both anchor sides are necessary at relation level.

The script also resolves, parent fibre by parent fibre:

- a section using the full residue of the direct \(+\) child alone;
- a section using the full residue of the direct \(-\) child alone;
- a matching-branch section using only \(D_8^+\) on the \(+\) child;
- a matching-branch section using only \(D_8^-\) on the \(-\) child.

This distinguishes “one child fibre is enough” from “one side of the residue is enough.”

### Q4. Fibre locality

For each nonzero seven-point parent fibre \(F\), test whether its full local relation space can be lifted using:

1. only its two direct anchor-growth child fibres;
2. only child fibres whose delete-8 residue reaches \(F\);
3. one child fibre alone;
4. the unrestricted global source sector.

The minimum-norm section is decomposed into child-fibre blocks. Squared Frobenius weights measure how much each child fibre contributes to each parent relation space.

### Q5. Optional sparse block section

With `--run-greedy`, perform a block-greedy search for a small collection of child fibres whose residue span contains each parent sector and the complete \(38\)-dimensional target.

These block counts are **upper bounds**, not proofs of minimum cardinality.

### Q6. Exceptional fifteenth direction

Reconstruct the one-dimensional AMP-18 gap direction \(v_*\) in the exceptional eight-point fibre and let
\[
y_*=D_8v_*.
\]

The probe compares:

1. the unrestricted global minimum-norm lift of \(y_*\);
2. the minimum-norm lift restricted to the exceptional fibre itself;
3. the original \(v_*\).

Key test:

\[
v_*\stackrel{?}{=}
\operatorname*{argmin}_{v\in R_8(G_*),\,D_8v=y_*}\|v\|.
\]

If true, the exceptional relation is the unique Moore–Penrose representative of its residue **within its own fibre**, despite the four-dimensional local residue kernel.

## 5. Output files

- `summary.json` — main ranks, residuals, branch verdicts and guarded interpretation;
- `run.log` — complete terminal record;
- `relation_basis_summary.csv` — basis dimensions and fresh validation residuals;
- `residue_singular_spectrum.csv` — complete singular spectrum of \(D_8|_{\mathcal R_8^{\mathrm{loc}}}\);
- `parent_section_summary.csv` — direct-child, incident-child, one-child and branch-resolved results per nonzero parent fibre;
- `section_block_weights.csv` — minimum-norm section weight from every child fibre into every nonzero parent fibre;
- `greedy_block_trace.csv` — optional sparse-block search trace;
- `exceptional_section_audit.json` — detailed exceptional-direction comparison;
- `section_operator_data.npz` — machine-readable section coordinates, ambient lift, target basis and singular spectra.

## 6. Primary verdicts

### Exact section supported

Require all of:

- target containment residual below \(10^{-7}\);
- section reconstruction residual below \(10^{-7}\);
- fresh eight-point and seven-point PT residuals below \(10^{-7}\);
- positive control near zero and negative control near one.

### Natural/local section candidate

Stronger evidence requires exact sections using direct or incident child fibres, preferably one child fibre, with stable results across independent kinematic seeds.

### No naturality claim yet

Even if exact, a Moore–Penrose section alone is only an algebraic existence result. A serious growth law should additionally exhibit one or more of:

- sparse support;
- fibre locality;
- branch covariance;
- flip equivariance;
- sibling compatibility;
- a closed coefficient formula;
- stability across multiplicities.

## 7. Recommended run

```bash
caffeinate -i python3 scripts/ehf_amp_found_02b_minimal_nontrivial_growth_sections.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --base-run-dir runs/ehf_amp_found_01_amp18_20 \
  --out-dir runs/ehf_amp_found_02b_seed11 \
  --seed 11
```

After the primary run is audited, repeat with `--seed 29`. Run the optional slower block-sparse audit separately by adding `--run-greedy`.
