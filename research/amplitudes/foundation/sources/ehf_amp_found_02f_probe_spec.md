# EHF-AMP-FOUND-02F  
## Exact Symbolic Channel Operator and Schur-Scalar Derivation

**Status:** computational exact-certificate probe  
**Input:** completed EHF-AMP-FOUND-02D operator bundles and the 02E symmetry machinery  
**Primary transition:** reflection-aware \(8\to7\) factorisation  
**Reference channel:** \(\{2,3,4\}\leftrightarrow\{5,6,7\}\)

---

## 1. Purpose

EHF-AMP-FOUND-02D found the squared singular spectrum

\[
1^{\times20},\qquad
\left(\frac65\right)^{\times40},\qquad
\left(\frac85\right)^{\times40},\qquad
\left(\frac95\right)^{\times10}.
\]

EHF-AMP-FOUND-02E then showed that the rank-\(110\) residue image decomposes into ten \(S_6\)-conjugate rank-\(11\) channels. For one channel, the stabiliser

\[
H\cong(S_3\times S_3)\rtimes C_2
\]

acts multiplicity-free with block dimensions

\[
2+4+4+1=11.
\]

02E explained **why there are four spectral values and why their multiplicities are \(2,4,4,1\) per channel**, but the four rational values themselves were still numerical observations.

02F closes that gap at the level of a computer-assisted exact certificate.

---

## 2. Core construction

Let \(A_F\) be the residue map restricted to the two complementary source fibres of the reference channel, and let

\[
K_F=A_FA_F^{\mathsf T}.
\]

The numerical operator has support on \(36\) canonical seven-point states. 02F reconstructs the supported \(36\times36\) matrix over \(\mathbb Q\), using a denominator bound of \(60\).

For the seed-11 bundle, the only nonzero rational entries are expected to be

\[
-\frac{11}{60},\quad
-\frac7{60},\quad
-\frac1{20},\quad
\frac1{60},\quad
\frac1{12},\quad
\frac3{20},\quad
\frac5{12}.
\]

The rational reconstruction is accepted only when every entry agrees with the numerical operator to the requested tolerance and the off-support norm is negligible.

---

## 3. Minimal polynomial without assumed eigenvalues

The script does **not** insert the candidate roots \(1,6/5,8/5,9/5\) by hand.

It forms the exact matrix powers

\[
I,\ K_F,\ K_F^2,\ldots
\]

and finds the first exact linear dependence. The expected result is

\[
m(x)
=
x^5-\frac{28}{5}x^4+\frac{289}{25}x^3
-\frac{1302}{125}x^2+\frac{432}{125}x,
\]

which factors as

\[
\boxed{
m(x)=
x(x-1)
\left(x-\frac65\right)
\left(x-\frac85\right)
\left(x-\frac95\right).
}
\]

This is an exact symbolic derivation from the reconstructed rational operator.

---

## 4. Exact projectors and multiplicities

For every root \(\lambda\) of \(m(x)\), 02F constructs the Lagrange spectral projector

\[
P_\lambda
=
\prod_{\mu\neq\lambda}
\frac{K_F-\mu I}{\lambda-\mu}.
\]

The script verifies exactly that

\[
P_\lambda^2=P_\lambda,
\qquad
K_FP_\lambda=\lambda P_\lambda,
\qquad
\sum_\lambda P_\lambda=I.
\]

The expected traces are

\[
\operatorname{tr}P_0=25,
\]

\[
\operatorname{tr}P_1=2,\qquad
\operatorname{tr}P_{6/5}=4,\qquad
\operatorname{tr}P_{8/5}=4,\qquad
\operatorname{tr}P_{9/5}=1.
\]

Therefore the exact supported characteristic polynomial is

\[
x^{25}
(x-1)^2
\left(x-\frac65\right)^4
\left(x-\frac85\right)^4
\left(x-\frac95\right).
\]

The nonzero rank is exactly \(11\).

---

## 5. Exact stabiliser certificate

The \(72\)-element stabiliser \(H\) acts on the \(36\) supported target states by signed permutation matrices.

02F verifies entry-by-entry over \(\mathbb Q\) that

\[
R_hK_FR_h^{\mathsf T}=K_F
\qquad
\text{for every }h\in H.
\]

For each nonzero projector it then computes the exact character

\[
\chi_\lambda(h)=\operatorname{tr}(P_\lambda R_h).
\]

The decisive tests are

\[
\langle\chi_\lambda,\chi_\lambda\rangle_H=1
\]

for all four nonzero blocks, and

\[
\langle\chi_\lambda,\chi_\mu\rangle_H=0
\qquad(\lambda\neq\mu).
\]

These identities certify that the four nonzero eigenspaces are exact, pairwise inequivalent irreducible \(H\)-modules.

---

## 6. Exact Schur scalars

Since \(K_F\) commutes with \(H\) and every nonzero block is irreducible, Schur's lemma makes \(K_F\) scalar on each block.

02F evaluates each scalar exactly as

\[
\kappa_\lambda
=
\frac{\operatorname{tr}(K_FP_\lambda)}
{\operatorname{tr}(P_\lambda)}.
\]

The expected result is

\[
\boxed{
\kappa=
1,\quad\frac65,\quad\frac85,\quad\frac95
}
\]

on irreducible dimensions

\[
\boxed{
2,\quad4,\quad4,\quad1.
}
\]

This is the requested Schur-scalar derivation.

---

## 7. Ten-channel transport

The probe rationally reconstructs the supported operator for all ten complementary fibre pairs and checks exactly that every channel:

- has support size \(36\);
- has rank \(11\);
- satisfies the same minimal polynomial;
- has projector traces \(25,2,4,4,1\);
- reconstructs from the same four nonzero rational spectral values.

Together with 02E's exact signed \(S_6\) conjugacy certificate, this transports the one-channel result to the full rank-\(110\) image.

---

## 8. Cross-seed control

When a second 02D operator bundle is supplied, 02F independently rationally reconstructs the reference matrix and requires exact equality over \(\mathbb Q\).

This is stronger than merely comparing eigenvalues.

---

## 9. Claim boundary

After a successful run, the following statement is justified:

> Conditional on the denominator-\(60\) rational reconstruction of the 02D residue Gram matrix, the reference complement-pair channel has an exact rational operator with minimal polynomial
> \[
> x(x-1)(x-6/5)(x-8/5)(x-9/5).
> \]
> Its four nonzero eigenspaces are pairwise inequivalent irreducible modules of the \(72\)-element complement-pair stabiliser, of dimensions \(2,4,4,1\). The exact Schur scalars are \(1,6/5,8/5,9/5\). All ten complement-pair channels satisfy the same exact certificate.

The remaining theorem-level obligation is:

> Derive the rational \(36\times36\) reference operator directly from exact Parke--Taylor relation identities, rather than reconstructing it from floating operator data.

Thus 02F is an **exact computer-assisted certificate**, not yet a handwritten first-principles proof.

---

## 10. Run command

```bash
caffeinate -i python3 scripts/ehf_amp_found_02f_exact_symbolic_channel_operator.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --symmetry-script scripts/ehf_amp_found_02e_complement_pair_symmetry_certificate.py \
  --operator-data runs/ehf_amp_found_02d_seed11/operator_data.npz \
  --comparison-operator-data runs/ehf_amp_found_02d_seed29/operator_data.npz \
  --out-dir runs/ehf_amp_found_02f
```

SymPy is required.

---

## 11. Principal outputs

```text
summary.json
run.log
exact_symbolic_certificate.json
reference_support_states.csv
exact_reference_channel_matrix.csv
exact_entry_histogram.csv
exact_schur_blocks.csv
exact_stabilizer_characters.csv
exact_character_inner_products.csv
exact_trace_moments.csv
ten_channel_exact_audit.csv
```

The terminal summary should report:

```text
Exact rational reference matrix:     True
Minimal polynomial derived exactly:  True
Exact roots:                         ['0', '1', '6/5', '8/5', '9/5']
Exact multiplicities:                [25, 2, 4, 4, 1]
Exact stabilizer covariance:         True
Four irreducible Schur blocks:       True
All ten channels exact:              True
Cross-seed exact matrix equality:    True
Computer-assisted exact certificate: True
```
