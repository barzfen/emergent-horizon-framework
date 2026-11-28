# EHF-AMP-FOUND-02H  
## Sixteen-Orbital Hand-Proof Compression

**Status:** exact finite-group proof-compression probe  
**Transition:** reflection-aware \(8\to7\) factorisation  
**Reference pair:** \(\{2,3,4\}\leftrightarrow\{5,6,7\}\)

---

## 1. Purpose

02G derived the exact \(36\times36\) reference-channel operator directly from
the KK shuffle identity. That closes the mathematical derivation, but a
36-state matrix is still too large for a readable proof.

02H compresses the exact result in two stages:

\[
36\times36
\quad\longrightarrow\quad
16\text{ stabiliser orbitals}
\quad\longrightarrow\quad
9\text{ Fourier blocks of size at most }4.
\]

The objective is a conventional theorem-proof presentation rather than
another numerical probe.

---

## 2. The 36-state support is \(S_3\times S_3\)

For the reference partition

\[
A=\{2,3,4\},\qquad B=\{5,6,7\},
\]

every supported seven-point state has the form

\[
(1,a_1,b_1,a_2,b_2,a_3,b_3),
\]

where \((a_1,a_2,a_3)\) is a permutation of \(A\) and
\((b_1,b_2,b_3)\) is a permutation of \(B\).

Therefore

\[
X\cong S_3\times S_3,
\qquad
|X|=3!\,3!=36.
\]

The subgroup \(S_3\times S_3\) acts regularly by relabelling within the two
blocks.

Exact covariance implies that the channel operator is convolution:

\[
K[x,y]=f(x^{-1}y)
\]

for a unique rational kernel

\[
f\in\mathbb Q[S_3\times S_3].
\]

---

## 3. Sixteen stabiliser orbitals

The block-exchange involution extends the regular subgroup to

\[
H=(S_3\times S_3)\rtimes C_2.
\]

The unordered pairs of support states split into exactly 16 \(H\)-orbitals.
Because \(K\) is \(H\)-invariant and symmetric, one exact coefficient is
required per orbital.

The coefficient set is

\[
-\frac{11}{60},\quad
-\frac7{60},\quad
-\frac1{20},\quad
\frac1{60},\quad
\frac1{12},\quad
\frac3{20},\quad
\frac5{12}.
\]

The output `sixteen_orbital_kernel_table.csv` is therefore a complete compact
description of the \(36\times36\) matrix.

---

## 4. Convolution proof of the polynomial

For kernels \(f,h\) on \(G=S_3\times S_3\), define

\[
(f*h)(g)=\sum_{u\in G}f(u)h(u^{-1}g).
\]

Matrix multiplication of the corresponding convolution operators is exactly
group convolution.

02H computes

\[
\delta_e,\quad f,\quad f^{*2},\quad\ldots,\quad f^{*5}
\]

and records them on the 16 orbitals. Their first exact dependence gives

\[
\boxed{
x(x-1)
\left(x-\frac65\right)
\left(x-\frac85\right)
\left(x-\frac95\right).
}
\]

Thus the minimal polynomial can be checked from a 16-row Krylov table rather
than 1296 matrix entries.

---

## 5. Fourier proof on \(S_3\times S_3\)

The irreducible representations of \(S_3\) are

\[
\mathbf1,\qquad \mathrm{sgn},\qquad \mathrm{std},
\]

with dimensions

\[
1,\qquad1,\qquad2.
\]

Hence \(S_3\times S_3\) has nine product irreducibles. The convolution
operator reduces to nine exact Fourier blocks:

\[
\widehat f(\rho\otimes\sigma)
=
\sum_{(g,h)\in S_3\times S_3}
f(g,h)\,\rho(g)\otimes\sigma(h).
\]

The largest block is only \(4\times4\).

The expected nonzero blocks are:

\[
\widehat f(\mathbf1\otimes\mathrm{sgn})=[1],
\]

\[
\widehat f(\mathrm{sgn}\otimes\mathbf1)=[1],
\]

\[
\widehat f(\mathrm{sgn}\otimes\mathrm{sgn})=[9/5],
\]

\[
\widehat f(\mathrm{sgn}\otimes\mathrm{std})
\text{ has eigenvalues }0,8/5,
\]

\[
\widehat f(\mathrm{std}\otimes\mathrm{sgn})
\text{ has eigenvalues }0,8/5,
\]

\[
\widehat f(\mathrm{std}\otimes\mathrm{std})
\text{ has eigenvalues }0,0,0,6/5.
\]

The remaining three blocks vanish.

In the regular representation, a product irrep of dimension \(d\) occurs
\(d\) times. Therefore the nonzero channel multiplicities are

\[
1+1=2
\]

for eigenvalue \(1\),

\[
2+2=4
\]

for eigenvalue \(8/5\),

\[
4
\]

for eigenvalue \(6/5\), and

\[
1
\]

for eigenvalue \(9/5\).

This gives rank

\[
2+4+4+1=11
\]

and kernel dimension

\[
36-11=25.
\]

---

## 6. Recovering the \(H\)-irreducible blocks

The complement-exchange \(C_2\) pairs factor-swapped Fourier sectors:

\[
\mathbf1\otimes\mathrm{sgn}
\longleftrightarrow
\mathrm{sgn}\otimes\mathbf1,
\]

forming the two-dimensional eigenvalue-\(1\) block, and

\[
\mathrm{sgn}\otimes\mathrm{std}
\longleftrightarrow
\mathrm{std}\otimes\mathrm{sgn},
\]

forming the four-dimensional eigenvalue-\(8/5\) block.

The self-paired sectors give:

- a four-dimensional eigenvalue-\(6/5\) block from the rank-one Fourier mode
  of \(\mathrm{std}\otimes\mathrm{std}\), repeated four times in the regular
  representation;
- a one-dimensional eigenvalue-\(9/5\) block from
  \(\mathrm{sgn}\otimes\mathrm{sgn}\).

Thus

\[
\mathcal C
\cong
V_2\oplus V_4^{(8/5)}\oplus V_4^{(6/5)}\oplus V_1.
\]

---

## 7. Exact theorem obtained

A successful 02H run yields the compact theorem:

> The exact reference complement-pair residue operator is right convolution
> by a seven-valued rational kernel on \(S_3\times S_3\). The symmetric kernel
> is specified by 16 stabiliser orbitals. Its nine product-Fourier blocks have
> maximum size four and yield nonzero spectrum
> \[
> 1^{\times2},\quad
> (6/5)^{\times4},\quad
> (8/5)^{\times4},\quad
> (9/5)^{\times1}.
> \]
> The complement-exchange involution combines these Fourier sectors into
> irreducible \(H=(S_3\times S_3)\rtimes C_2\) blocks of dimensions
> \(2,4,4,1\).

This is the intended human-readable proof of the spectral mechanism.

---

## 8. Run command

```bash
caffeinate -i python3 scripts/ehf_amp_found_02h_sixteen_orbital_hand_proof.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --symmetry-script scripts/ehf_amp_found_02e_complement_pair_symmetry_certificate.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --out-dir runs/ehf_amp_found_02h
```

---

## 9. Principal outputs

```text
summary.json
run.log
hand_proof_certificate.json
hand_proof_compression.md
sixteen_orbital_kernel_table.csv
orbital_krylov_table.csv
group_convolution_kernel.csv
s3xs3_fourier_blocks.csv
induced_H_blocks.csv
```

The terminal target is:

```text
Support is exactly S3 x S3:          True
Exact convolution law:               True
Sixteen stabilizer orbitals:         True
Minimal polynomial from convolution: x*(x - 1)*(5*x - 9)*(5*x - 8)*(5*x - 6)/125
Nine exact Fourier blocks:           True
Largest Fourier block:               4 x 4
Exact Fourier spectrum:              True
Nonzero multiplicities:              {'1': 2, '6/5': 4, '8/5': 4, '9/5': 1}
Hand-proof compression certificate:  True
```
