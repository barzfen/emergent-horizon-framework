# EHF-AMP-FOUND-03G  
## Parameterised Shuffle–Antisymmetriser Template Extraction

**Status:** exact group-ring proof compression  
**Input:** exact KK shuffle maps and the fixed-anchor \(9\to8\) deletion map  
**Symmetry:** \(G\cong C_2^3\)

---

## 1. Purpose

03F proved all fifteen minimum-support signed-orbit relations directly in the
standard \(720\)-dimensional eight-point KK basis.

That is an exact derivation, but its proof certificate still checks hundreds
of coordinate cancellations separately.

03G asks whether the KK shuffle map and the \(C_2^3\) character
antisymmetrisers can be combined into a small **parameterised universal
operator**.

The target statement is:

> The complete \(720\)-coordinate proof factors through exactly \(21\)
> primitive rows over the group ring \(\mathbb Z[C_2^3]\).

---

## 2. Group-ring variables

Let

\[
G=
\langle
g_1=(2\,3),\
g_2=(5\,6),\
g_3=(7\,8)
\rangle
\cong C_2^3.
\]

Introduce commuting variables

\[
x_1,x_2,x_3,
\qquad
x_i^2=1.
\]

For

\[
h=(h_1,h_2,h_3)\in C_2^3,
\]

write

\[
x^h=x_1^{h_1}x_2^{h_2}x_3^{h_3}.
\]

The coefficient ring is

\[
\mathbb Z[C_2^3]
\cong
\mathbb Z[x_1,x_2,x_3]/(x_1^2-1,x_2^2-1,x_3^2-1).
\]

---

## 3. Universal shuffle–antisymmetriser row

The \(72\) target orderings split into ten \(G\)-orbits. Let

\[
w_1,\ldots,w_{10}
\]

be the canonical minimum representatives.

For a standard KK basis coordinate

\[
\sigma\in S_{\{2,\ldots,7\}},
\]

define

\[
\boxed{
P_{\sigma j}(x)
=
\sum_{h\in G}
Q_8[\sigma,h\cdot w_j]\,x^h.
}
\]

The universal row is

\[
P_\sigma(x)
=
\bigl(
P_{\sigma1}(x),\ldots,P_{\sigma,10}(x)
\bigr)
\in
\mathbb Z[C_2^3]^{10}.
\]

This formula combines:

- the exact KK shuffle coefficients in \(Q_8\);
- the full \(C_2^3\) orbit of each target representative;
- all eight sign-character projections at once.

---

## 4. Character evaluation

For a sign character

\[
\chi=(\chi_1,\chi_2,\chi_3),
\qquad
\chi_i\in\{\pm1\},
\]

evaluate

\[
x_i=\chi_i.
\]

Then

\[
P_{\sigma j}(\chi)
=
\sum_{h\in G}
\chi(h)\,
Q_8[\sigma,h\cdot w_j].
\]

This is the KK coefficient of the **raw** signed orbit sum.

Let

\[
s_{\chi j}
\]

be the exact integer by which the raw orbit sum differs from the primitive
signed-orbit atom:

\[
\sum_{h\in G}\chi(h)e_{h\cdot w_j}
=
s_{\chi j}\,\Omega_\chi(w_j).
\]

Therefore the primitive character-reduced matrix is

\[
\boxed{
M_\chi[\sigma,j]
=
\frac{P_{\sigma j}(\chi)}{s_{\chi j}}.
}
\]

This gives a single parameterised formula for all eight matrices

\[
M_\chi=Q_8A_\chi^{\mathsf T}.
\]

---

## 5. Monomial equivalence of universal rows

Two nonzero universal rows are declared equivalent when

\[
P_{\sigma'}(x)
=
m\,x^h P_\sigma(x),
\]

where

\[
m\in\mathbb Z\setminus\{0\},
\qquad
h\in C_2^3.
\]

At a sign character,

\[
x^h\mapsto\chi(h)\in\{\pm1\},
\]

so equivalent universal rows impose the same kernel equation up to a nonzero
scalar.

03G primitive-normalises each row and chooses the lexicographically least
representative over its eight group-monomial translates.

---

## 6. Exact 21-template theorem

The target census is:

\[
720\text{ KK coordinates},
\]

of which only

\[
144
\]

give nonzero universal rows.

Those \(144\) rows collapse to exactly

\[
\boxed{21}
\]

primitive monomial-equivalence classes.

Their multiplicities are

\[
\boxed{
16^{\times3},\quad
8^{\times6},\quad
4^{\times12}.
}
\]

Equivalently,

\[
3(16)+6(8)+12(4)=144.
\]

For every KK coordinate, the script records the unique exact reconstruction

\[
P_\sigma(x)
=
m_\sigma x^{h_\sigma}T_{t(\sigma)}(x),
\]

where

\[
T_1(x),\ldots,T_{21}(x)
\]

are the primitive templates.

---

## 7. Specialised template matrix

Let

\[
T_\chi
\]

be the \(21\)-row rational matrix obtained by:

1. evaluating every group-ring polynomial at \(x_i=\chi_i\);
2. deleting the orbit columns whose signed atom vanishes;
3. dividing each surviving orbit column by \(s_{\chi j}\).

The central exact statement is

\[
\boxed{
\operatorname{rowspan}_{\mathbb Q}T_\chi
=
\operatorname{rowspan}_{\mathbb Q}M_\chi.
}
\]

Consequently,

\[
\boxed{
\ker_{\mathbb Q}T_\chi
=
\ker_{\mathbb Q}M_\chi.
}
\]

The expected ranks and nullities are:

\[
\begin{array}{c|c|c}
\chi & \operatorname{rank} & \operatorname{nullity}\\
\hline
+++ & 10 & 0\\
++- & 7 & 1\\
+-+ & 7 & 1\\
+-- & 7 & 3\\
-++ & 7 & 1\\
-+- & 7 & 3\\
--+ & 7 & 3\\
--- & 5 & 3
\end{array}
\]

---

## 8. Parameterised proof of a normal form

Let

\[
c=(c_1,\ldots,c_r)
\]

be a signed-orbit coefficient row in character \(\chi\). Its PT relation is
proved by the \(21\) equations

\[
\boxed{
\sum_j
c_j\,
\frac{T_{tj}(\chi)}{s_{\chi j}}
=
0,
\qquad
t=1,\ldots,21.
}
\]

Every one of the original \(720\) KK-coordinate equations is then automatic,
because it is a scalar/monomial specialisation of one template equation.

03G verifies these equations for all fifteen minimum-support
quotient-character directions and recovers the same total atom count

\[
79.
\]

---

## 9. Relation to 03F

### 03F

Checks

\[
M_\chi c^{\mathsf T}=0
\]

directly in all \(720\) KK coordinates.

### 03G

Factors the matrix through

\[
\mathbb Z[C_2^3]
\]

and checks only the universal template equations

\[
T_\chi c^{\mathsf T}=0.
\]

Thus 03G is a proof compression:

\[
720
\longrightarrow
144
\longrightarrow
21.
\]

The \(21\) templates are still finite data. A subsequent step may seek a
smaller combinatorial classification of those templates.

---

## 10. Claim boundary

A successful 03G run proves:

> The exact fixed-anchor \(9\to8\) signed-orbit relation theorem admits a
> \(21\)-row parameterised group-ring shuffle–antisymmetriser presentation.

It does not yet:

- reduce the \(21\) templates to one closed symbolic family;
- prove a corresponding template count for general \(n\);
- establish anchor independence;
- identify the construction with a known representation-theoretic or
  geometric filtration;
- demonstrate phenomenological utility.

---

## 11. Run command

```bash
caffeinate -i python3 scripts/ehf_amp_found_03g_parameterised_shuffle_antisymmetriser_templates.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --rank-script scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --normal-form-script scripts/ehf_amp_found_03e_exact_signed_orbit_normal_form.py \
  --derivation-script scripts/ehf_amp_found_03f_direct_kk_shuffle_signed_orbit_derivation.py \
  --out-dir runs/ehf_amp_found_03g \
  --strict
```

No output files from 03C–03F are required.

---

## 12. Principal outputs

```text
summary.json
verdict.json
run.log
exact_parameterised_shuffle_template_certificate.json
universal_shuffle_template_catalog.csv
universal_shuffle_template_polynomials.csv
kk_coordinate_to_universal_template_map.csv
character_specialised_template_summary.csv
template_derived_signed_orbit_relations.csv
template_equation_cancellation_certificate.csv
parameterised_shuffle_template_derivation.md
```

The target terminal result is:

```text
Universal group-ring template census
  KK coordinate rows:                 720
  nonzero universal rows:             144
  primitive monomial classes:         21
  multiplicity distribution:         {4: 12, 8: 6, 16: 3}

Character specialisation
  exact row-space equality:           True
  exact kernel equality:              True
  character ranks exact:              True
  character nullities exact:          True

FINAL SUMMARY
Universal rows reconstructed:         True
21-template theorem:                  True
Tail lattice reconstructed:           True
Quotient-character directions:        15
All template equations exact:         True
Total minimum signed-orbit atoms:      79
Verdict: EHF_AMP_FOUND_03G_EXACT_21_TEMPLATE_GROUP_RING_DERIVATION_PROVED
strict checks:                        PASS
```
