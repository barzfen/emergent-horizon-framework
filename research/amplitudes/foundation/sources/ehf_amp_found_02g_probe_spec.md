# EHF-AMP-FOUND-02G  
## Direct Exact KK Derivation of the Reference Channel Matrix

**Status:** exact symbolic/combinatorial probe  
**Transition:** reflection-aware \(8\to7\) factorisation  
**Reference complement pair:** \(\{2,3,4\}\leftrightarrow\{5,6,7\}\)

---

## 1. Why 02G is needed

02F produced an exact rational certificate for the complement-pair channel operator, but the rational matrix was obtained by reconstructing floating-point output.

02G removes that final dependency.

It constructs the source relation spaces, Euclidean relation projectors, signed deletion maps, and channel Gram operators directly over \(\mathbb Q\).

The scientific question is:

> Can the denominator \(60\), the seven rational matrix-entry values, and the spectrum
> \[
> 1,\frac65,\frac85,\frac95
> \]
> be derived without numerical SVD, random kinematics, or rational reconstruction?

---

## 2. Exact input theorem

The construction uses the standard Kleiss--Kuijf shuffle identity for Parke--Taylor factors:

\[
\operatorname{PT}(1,\alpha,n,\beta)
=
(-1)^{|\beta|}
\sum_{\sigma\in\alpha\shuffle\beta^{\mathrm T}}
\operatorname{PT}(1,\sigma,n).
\]

The \((n-2)!\) orderings

\[
\operatorname{PT}(1,\sigma,n),
\qquad
\sigma\in S_{\{2,\ldots,n-1\}},
\]

form the KK basis.

For \(n=8\), this basis has dimension

\[
6!=720.
\]

No kinematic evaluation is needed to determine the exact fibre-local relation spaces.

---

## 3. Exact local relation spaces

For an \(n=8\) fibre \(F\) with 72 canonical cycles, define the sparse integer coordinate matrix

\[
Q_F\in\mathbb Z^{720\times72}
\]

whose \(c\)-th column is the KK-shuffle expansion of \(\operatorname{PT}(c)\).

Then

\[
R_F=\ker_{\mathbb Q} Q_F.
\]

02G computes this kernel exactly. For every active fibre the expected result is

\[
\operatorname{rank}_{\mathbb Q}Q_F=57,
\qquad
\dim R_F=15.
\]

SymPy returns an integer kernel basis

\[
N_F\in\mathbb Z^{72\times15}.
\]

The Euclidean orthogonal projector onto the exact relation space is therefore

\[
P_F
=
N_F(N_F^{\mathsf T}N_F)^{-1}N_F^{\mathsf T}
\in\mathbb Q^{72\times72}.
\]

This projector is basis-independent.

---

## 4. Exact signed deletion

Let

\[
D_F:\mathbb Q^{72}\to\mathbb Q^{360}
\]

be the reflection-aware delete-8 incidence map.

Every nonzero entry of \(D_F\) is \(+1\) or \(-1\). The sign is the product of:

1. the anchor-side collinear sign;
2. the seven-point Parke--Taylor reflection character introduced when the reduced ordering is canonicalised.

For a complementary active pair \(F,\phi(F)\), define

\[
K_{F,\phi(F)}
=
D_FP_FD_F^{\mathsf T}
+
D_{\phi(F)}P_{\phi(F)}D_{\phi(F)}^{\mathsf T}.
\]

This is the channel operator derived directly over \(\mathbb Q\).

---

## 5. Reference matrix target

For the reference pair

\[
\{2,3,4\}\leftrightarrow\{5,6,7\},
\]

02G should derive:

\[
\operatorname{supp}K=36,
\qquad
\operatorname{rank}K=11,
\qquad
\dim\ker K=25.
\]

The only nonzero rational entry values should be

\[
-\frac{11}{60},
\quad
-\frac7{60},
\quad
-\frac1{20},
\quad
\frac1{60},
\quad
\frac1{12},
\quad
\frac3{20},
\quad
\frac5{12}.
\]

Thus the denominator LCM \(60\) is obtained directly from the exact relation projectors and signed incidence map.

---

## 6. Exact polynomial derivation

The script finds the first exact dependence among

\[
I,K,K^2,\ldots
\]

without supplying candidate roots.

The target minimal polynomial is

\[
\boxed{
m_K(x)=
x(x-1)
\left(x-\frac65\right)
\left(x-\frac85\right)
\left(x-\frac95\right).
}
\]

The exact spectral-projector multiplicities should be

\[
25,\ 2,\ 4,\ 4,\ 1.
\]

Hence the supported characteristic polynomial is

\[
x^{25}
(x-1)^2
\left(x-\frac65\right)^4
\left(x-\frac85\right)^4
\left(x-\frac95\right).
\]

---

## 7. Exact symmetry and Schur certificate

The \(72\)-element complement-pair stabiliser

\[
H\cong(S_3\times S_3)\rtimes C_2
\]

acts by signed permutations on the 36 supported seven-point states.

02G verifies exactly that

\[
R_hKR_h^{\mathsf T}=K
\qquad
(h\in H).
\]

For the four nonzero projectors, it computes exact characters

\[
\chi_\lambda(h)=\operatorname{tr}(P_\lambda R_h).
\]

The required exact identities are

\[
\langle\chi_\lambda,\chi_\lambda\rangle_H=1
\]

and

\[
\langle\chi_\lambda,\chi_\mu\rangle_H=0
\quad(\lambda\neq\mu).
\]

This proves that the four blocks are pairwise inequivalent irreducible \(H\)-modules of dimensions

\[
2,\ 4,\ 4,\ 1.
\]

The exact Schur scalars are then

\[
1,\quad\frac65,\quad\frac85,\quad\frac95.
\]

---

## 8. Compact orbital description

A 36-by-36 matrix is too large for a useful handwritten proof.

02G therefore partitions unordered pairs of support states into stabiliser orbitals. The reference matrix is constant on each orbital.

The expected count is

\[
16
\]

unordered-pair orbitals using only the seven rational matrix values above.

This gives a compact next-stage proof object: a 16-row orbital coefficient table rather than 1296 matrix entries.

---

## 9. Ten-channel theorem audit

All twenty active fibres are paired by complementation of a three-subset of

\[
\{2,3,4,5,6,7\}.
\]

02G constructs every pair operator independently over \(\mathbb Q\) and checks:

\[
10/10\text{ have rank }11,
\]

\[
10/10\text{ satisfy the same minimal polynomial},
\]

\[
10/10\text{ have multiplicities }25,2,4,4,1,
\]

and

\[
10/10\text{ are exactly transported from the reference operator by signed }S_6.
\]

---

## 10. Claim boundary after success

A successful 02G run supports:

> Assuming the standard KK shuffle identity and KK-basis independence, the reflection-aware \(8\to7\) complement-pair channel operator is derived directly over \(\mathbb Q\). Its denominator \(60\), seven matrix-entry values, rank \(11\), exact minimal polynomial, irreducible stabiliser blocks, and Schur scalars require no numerical relation reconstruction.

This is substantially stronger than 02F.

The remaining task is no longer computational exactness. It is exposition:

> Convert the sparse KK-kernel/projector calculation into a concise handwritten proof, preferably using the 16 stabiliser orbitals.

---

## 11. Run command

```bash
caffeinate -i python3 scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --symmetry-script scripts/ehf_amp_found_02e_complement_pair_symmetry_certificate.py \
  --out-dir runs/ehf_amp_found_02g
```

No 02D or 02F operator file is used.

SymPy is required.

---

## 12. Principal outputs

```text
summary.json
run.log
direct_exact_certificate.json
exact_kk_relation_basis_summary.csv
exact_pair_channel_audit.csv
exact_channel_transport_audit.csv
reference_support_states.csv
exact_reference_channel_matrix.csv
exact_reference_entry_histogram.csv
exact_reference_stabilizer_orbitals.csv
exact_schur_blocks.csv
exact_stabilizer_characters.csv
exact_character_inner_products.csv
```

The terminal target is:

```text
Exact KK identity validation:        True
Numerical relation reconstruction:   not used
Rational operator reconstruction:    not used
Exact local relation rank/nullity:   57/15
Exact reference support/rank:        36/11
Exact denominator LCM:               60
Minimal polynomial:                  x*(x - 1)*(5*x - 9)*(5*x - 8)*(5*x - 6)/125
Exact multiplicities:                [25, 2, 4, 4, 1]
Four exact irreducible Schur blocks: True
All ten exact and S6-conjugate:      True
Direct exact certificate:            True
```
