# EHF-AMP-FOUND-03E  
## Exact Signed-Orbit Normal Form

**Status:** exact symmetry-separated proof compression  
**Input:** the seven filtration-adapted seeds from 03D  
**Symmetry:** \(G\cong C_2^3\)

---

## 1. Motivation

03D proved that seven primitive seed relations, closed under

\[
G=
\langle
(2\,3),(5\,6),(7\,8)
\rangle
\cong C_2^3,
\]

generate all five successive quotient layers of the \(15\)-dimensional
target relation lattice.

The seven relations are exact, but their explicit expansions contain between
\(16\) and \(34\) Parke--Taylor terms. They do not make the symmetry content
visually transparent.

03E factors the symmetry action out of the coefficient data.

---

## 2. Signed-orbit atoms

Let \(w\) be a canonical ordering in the reference target fibre
\(A=\{2,3,4\}\). For a joint sign character

\[
\chi=(\chi_1,\chi_2,\chi_3)\in\{\pm1\}^3,
\]

define the primitive signed-orbit atom

\[
\boxed{
\Omega_\chi(w)
=
\operatorname{prim}
\left(
\sum_{g\in G}
\chi(g)\,
e_{\operatorname{can}(g\cdot w)}
\right).
}
\]

Here:

- \(e_w\) is the coefficient vector of \(\operatorname{PT}(w)\);
- \(\chi(g)\) is the product of the appropriate three signs;
- repeated canonical states are combined;
- `prim` clears denominators, divides by the integer gcd, and fixes the first
  nonzero coefficient to be positive.

An atom is supported on one \(G\)-orbit.

The \(72\) target states split into exactly:

\[
8\text{ orbits of size }8,
\qquad
2\text{ orbits of size }4.
\]

---

## 3. Character-orbit coordinate spaces

For each character \(\chi\), the nonzero atoms from the ten state orbits form
an exact basis of the \(\chi\)-isotypic subspace of the full coefficient
space.

The atom-space dimensions are:

\[
\begin{array}{c|rrrrrrrr}
\chi & +++ & ++- & +-+ & +-- & -++ & -+- & --+ & ---\\
\hline
\dim & 10 & 8 & 8 & 10 & 8 & 10 & 10 & 8
\end{array}
\]

Every exact target relation in a fixed character sector can therefore be
written uniquely as an integer or rational combination of signed-orbit atoms.

---

## 4. Quotient-character directions

The successive layers are

\[
L_2=V_2/V_0,\qquad
L_3=V_3/V_2,
\]

\[
L_8=V_8/V_3,\qquad
L_9=V_9/V_3,
\]

\[
L_{15}=V_{15}/V_{14}.
\]

Their character multiplicities give fifteen one-dimensional directions when
multiplicity is counted:

\[
2+1+5+6+1=15.
\]

03E constructs an explicit atom-coordinate relation for every direction.

---

## 5. Exact minimum-support audit

For a relation

\[
R=\sum_j c_j\Omega_{\chi,j},
\]

define its atom support by

\[
\operatorname{supp}_\Omega(R)
=
\#\{j:c_j\ne0\}.
\]

Every character-orbit coordinate space has dimension at most ten. Therefore
minimum support can be certified exhaustively.

For each quotient character:

1. enumerate every subset of orbit-atom coordinates;
2. compute the exact subspace of the upper relation space supported inside
   that subset;
3. test its exact rank modulo the lower lattice node;
4. identify the smallest support admitting a nonzero quotient class;
5. for multiplicity two, identify the lexicographically smallest support
   profile of two independent quotient classes.

This is an exact finite search, not an LLL heuristic.

---

## 6. Expected minimum-support profile

The theorem target is:

\[
\begin{array}{c|c|c}
\text{layer} & \chi & \text{minimum atom supports}\\
\hline
L_2 & +-+ & 5\\
L_2 & --- & 6\\
L_3 & +-- & 6\\
L_8 & -++ & 3\\
L_8 & -+- & 5\\
L_8 & --+ & 4,\ 5\\
L_8 & --- & 4\\
L_9 & ++- & 5\\
L_9 & +-- & 4,\ 5\\
L_9 & -+- & 8\\
L_9 & --+ & 8\\
L_9 & --- & 6\\
L_{15} & -+- & 5
\end{array}
\]

The total number of atom occurrences is

\[
\boxed{79}.
\]

The two multiplicity-two sectors have exact minimum support profile

\[
(4,5).
\]

In particular, neither admits two independent four-atom representatives.

---

## 7. Relation to the seven 03D seeds

The 03D result and the 03E result answer different compression questions.

### 03D

\[
\boxed{
7\text{ mixed-character orbit seeds}
}
\]

is the minimum filtration-adapted seed count.

### 03E

\[
\boxed{
15\text{ character-pure quotient directions}
}
\]

are written in a unique symmetry-separated coordinate system, using a
minimum total of \(79\) atom occurrences under the direction-by-direction
minimum-support convention.

03D minimizes the number of generating seeds.  
03E exposes the irreducible sign content and minimizes orbit-atom support.

---

## 8. Why this is closer to closed form

A raw seed may contain dozens of explicit Parke--Taylor terms. A signed-orbit
atom packages up to eight related terms into the symbol

\[
\Omega_\chi(w).
\]

The resulting identities have the form

\[
c_1\Omega_\chi(w_1)
+\cdots+
c_k\Omega_\chi(w_k)=0,
\]

where

\[
3\le k\le8
\]

for the new quotient directions.

This isolates:

- the permutation symmetry in \(\Omega_\chi\);
- the actual relation data in the short integer coefficient list
  \((c_1,\ldots,c_k)\).

It is a normal form, not yet a short derivation from KK shuffle identities.

---

## 9. Claim boundary

A successful 03E run proves:

> Every exact quotient-character direction in the fixed-anchor \(9\to8\)
> tail-filtration lattice has a minimum-support expression as an integer
> combination of primitive \(C_2^3\) signed-orbit atoms.

It does not yet:

- derive the atom relations from a closed analytic shuffle formula;
- show that \(79\) is a globally minimal count under arbitrary mixing of
  quotient directions;
- establish anchor independence;
- generalise to higher multiplicity;
- demonstrate phenomenological utility.

---

## 10. Run command

```bash
caffeinate -i python3 scripts/ehf_amp_found_03e_exact_signed_orbit_normal_form.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --seed-coefficients runs/ehf_amp_found_03d/sparse_seed_coefficients.csv \
  --out-dir runs/ehf_amp_found_03e \
  --strict
```

---

## 11. Principal outputs

```text
summary.json
verdict.json
run.log
exact_signed_orbit_normal_form_certificate.json
signed_orbit_atom_catalog.csv
quotient_character_normal_form_summary.csv
signed_orbit_normal_form.csv
signed_orbit_normal_form_atom_coefficients.csv
signed_orbit_normal_form_expanded_coefficients.csv
signed_orbit_normal_form.md
```

The target terminal result is:

```text
Target state-orbit distribution:      {4: 2, 8: 8}
Tail lattice reconstructed:           True
Quotient-character directions:        15
All minimum support profiles:         True
All character quotients reconstructed:True
Total minimum signed-orbit atoms:      79
Verdict: EHF_AMP_FOUND_03E_EXACT_MINIMUM_SIGNED_ORBIT_NORMAL_FORM_PROVED
strict checks:                        PASS
```
