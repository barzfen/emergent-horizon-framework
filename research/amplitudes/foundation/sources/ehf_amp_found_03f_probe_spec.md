# EHF-AMP-FOUND-03F  
## Direct KK-Shuffle Derivation of the Signed-Orbit Normal Forms

**Status:** exact independent derivation probe  
**Target:** reconstruct 03E directly from KK shuffle matrices  
**Symmetry:** \(G\cong C_2^3\)

---

## 1. Purpose

03E proved that the fifteen quotient-character directions of the exact
\(9\to8\) tail-filtration lattice have minimum-support signed-orbit normal
forms.

However, 03E reached those directions through the seven filtration-adapted
seeds produced by 03D.

03F removes that dependency.

It asks:

> Can the complete signed-orbit normal form be reconstructed directly from
> exact Kleiss-Kuijf shuffle matrices and exact \(9\to8\) source residue maps,
> without reading any 03C, 03D, or 03E output file?

---

## 2. Direct character-reduced KK matrices

Let \(Q_8\) be the exact KK coordinate matrix of the reference target fibre

\[
A_0=\{2,3,4\}.
\]

For each joint character

\[
\chi\in\{\pm1\}^3
\]

of

\[
G=\langle(2\,3),(5\,6),(7\,8)\rangle\cong C_2^3,
\]

let \(A_\chi\) be the matrix whose rows are the primitive signed-orbit atoms

\[
\Omega_\chi(w)
=
\operatorname{prim}
\left(
\sum_{g\in G}\chi(g)e_{\operatorname{can}(g\cdot w)}
\right).
\]

Define the exact character-reduced shuffle matrix

\[
\boxed{
M_\chi=Q_8A_\chi^{\mathsf T}.
}
\]

A signed-orbit coefficient row \(c\) is a target Parke-Taylor relation exactly
when

\[
\boxed{
M_\chi c^{\mathsf T}=0.
}
\]

Thus the full character-pure target relation space is

\[
\ker_{\mathbb Q}M_\chi.
\]

---

## 3. Exact target kernel dimensions

The direct reduced matrices must reproduce the exact character multiplicities
of the fifteen-dimensional target relation space:

\[
\begin{array}{c|rrrrrrrr}
\chi & +++ & ++- & +-+ & +-- & -++ & -+- & --+ & ---\\
\hline
\dim\ker M_\chi & 0 & 1 & 1 & 3 & 1 & 3 & 3 & 3
\end{array}
\]

These nullities are obtained directly from exact KK shuffle expansions.

---

## 4. Independent reconstruction of the tail lattice

03F uses one exact nine-point source representative for each tail class:

\[
\begin{array}{c|c}
\text{subspace} & A\\
\hline
V_0 & \{2,3,4\}\\
V_2 & \{2,3,6\}\\
V_8 & \{2,5,6\}\\
V_9 & \{2,3,7\}\\
V_{14} & \{2,5,7\}\\
V_{15} & \{2,6,7\}
\end{array}
\]

For each representative it constructs:

1. the exact nine-point KK matrix \(Q_A\);
2. the exact source relation space \(\ker Q_A\);
3. the exact signed delete-\(9\) image;
4. the canonical ordered-block transport to \(A_0\).

It then verifies directly:

\[
\dim(V_0,V_2,V_3,V_8,V_9,V_{14},V_{15})
=(0,2,3,8,9,14,15),
\]

\[
V_3=V_8\cap V_9,
\qquad
V_{14}=V_8+V_9,
\qquad
V_{15}=\ker Q_8.
\]

No stored subspace basis from 03C is read.

---

## 5. Direct derivation of the minimum-support directions

Inside each character atom coordinate space, 03F forms the lower and upper
lattice nodes directly and exhausts all coordinate-support subsets.

For every quotient character, it:

1. verifies that the upper space lies in \(\ker M_\chi\);
2. determines the exact quotient multiplicity;
3. finds the minimum-support quotient basis;
4. verifies the expected support profile;
5. proves
   \[
   M_\chi c^{\mathsf T}=0
   \]
   for every selected direction;
6. records every nonzero contribution to every active KK coordinate and checks
   exact zero net coefficient.

The target profiles are:

\[
\begin{array}{c|c|c}
\text{layer} & \chi & \text{minimum atom supports}\\
\hline
L_2 & +-+ & 5\\
L_2 & --- & 6\\
L_3 & +-- & 6\\
L_8 & -++ & 3\\
L_8 & -+- & 5\\
L_8 & --+ & 4,5\\
L_8 & --- & 4\\
L_9 & ++- & 5\\
L_9 & +-- & 4,5\\
L_9 & -+- & 8\\
L_9 & --+ & 8\\
L_9 & --- & 6\\
L_{15} & -+- & 5
\end{array}
\]

The direction count must be \(15\), and the total atom count must be \(79\).

---

## 6. Meaning of a successful result

A successful run proves:

> The signed-orbit normal forms are not artefacts of the seven 03D seed
> relations. They are exact kernel vectors of finite character-reduced KK
> shuffle matrices. The complete tail lattice and all fifteen minimum-support
> quotient-character directions can be reconstructed independently from the
> exact KK and deletion maps.

This is a direct exact matrix derivation from the KK shuffle identity.

---

## 7. What remains open

03F still does not provide a short handwritten analytic identity. It proves
vanishing through exact finite matrices and coordinate-level cancellation.

The remaining problem is to replace the kernel computation by a compact
parameterised formula such as:

- a shuffle-antisymmetriser identity;
- a group-algebra projector relation;
- a determinantal or Plucker-type identity;
- a flag-module construction valid at general multiplicity.

---

## 8. Run command

```bash
caffeinate -i python3 scripts/ehf_amp_found_03f_direct_kk_shuffle_signed_orbit_derivation.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --rank-script scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --normal-form-script scripts/ehf_amp_found_03e_exact_signed_orbit_normal_form.py \
  --out-dir runs/ehf_amp_found_03f \
  --strict
```

The 03E script is imported only as an exact utility library for orbit atoms,
row-space operations, and exhaustive support search. No 03E output file is
used.

---

## 9. Principal outputs

```text
summary.json
verdict.json
run.log
direct_kk_shuffle_certificate.json
character_reduced_kk_summary.csv
character_reduced_kk_sparse_entries.csv
direct_quotient_character_derivation.csv
direct_signed_orbit_normal_form.csv
direct_signed_orbit_atom_coefficients.csv
direct_signed_orbit_expanded_coefficients.csv
kk_coordinate_cancellation_certificate.csv
direct_kk_shuffle_derivation.md
```

The target terminal result is:

```text
Prior 03C/03D/03E outputs used:       False
Direct Q8 relation dimension:         15
Character KK nullities exact:         True
Tail lattice reconstructed directly:  True
Quotient-character directions:        15
All minimum support profiles:         True
All KK coordinate cancellations:      True
Total minimum signed-orbit atoms:      79
Verdict: EHF_AMP_FOUND_03F_DIRECT_KK_SHUFFLE_SIGNED_ORBIT_DERIVATION_PROVED
strict checks:                        PASS
```
