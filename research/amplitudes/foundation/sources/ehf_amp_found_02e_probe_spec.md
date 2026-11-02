# EHF-AMP-FOUND-02E
## Complement-Pair Symmetry Decomposition and Proof Certificate

**Status:** computational symmetry certificate and analytic proof scaffold  
**Depends on:** EHF-AMP-FOUND-02D full `operator_data.npz` output  
**Primary transition:** reflection-aware \(8\to7\) factorisation  
**Date:** 2026-07-13

---

## 1. Purpose

EHF-AMP-FOUND-02D found that the rank-110 residue image decomposes into ten complementary rank-11 channels and that each channel has the numerically exact squared spectrum

\[
1^{\times2},
\qquad
\left(\frac65\right)^{\times4},
\qquad
\left(\frac85\right)^{\times4},
\qquad
\left(\frac95\right)^{\times1}.
\]

The twenty active eight-point fibres are indexed by the three-subsets of

\[
\{2,3,4,5,6,7\},
\]

and complementation identifies them in ten unordered pairs.

02E tests whether the observed \(2+4+4+1\) spectral multiplicities arise from the finite symmetry of a reference complement-pair channel.

The target proof architecture is

\[
\mathcal C
\cong
V_2\oplus V_4^{(a)}\oplus V_4^{(b)}\oplus V_1,
\]

with

\[
K|_{\mathcal C}
=
1P_2+rac65P_{4a}+rac85P_{4b}+rac95P_1.
\]

The script provides a computational certificate for this architecture. It does not replace an analytic derivation of the Parke--Taylor relation projector or the four rational eigenvalues.

---

## 2. Exact finite group acting on the channels

Fix anchor label 1. Permutations of labels \(2,\ldots,7\) form the group

\[
S_6,
\qquad |S_6|=720.
\]

The action on canonical seven-point ordering coordinates includes the odd-multiplicity Parke--Taylor reflection character:

\[
\operatorname{PT}(\alpha^{\mathrm{rev}})=-\operatorname{PT}(\alpha).
\]

The ten channels are the complement-pair orbits

\[
\{S,S^c\},
\qquad
S\in\binom{[6]}3.
\]

The action should be transitive. For the reference pair

\[
\{\{2,3,4\},\{5,6,7\}\},
\]

the stabilizer should be

\[
H\cong(S_3\times S_3)\rtimes C_2,
\qquad |H|=72.
\]

---

## 3. Tests

### 3.1 Signed \(S_6\) channel covariance

For every \(g\in S_6\) and every channel \(\mathcal C_j\), test

\[
J_7(g)\mathcal C_j=\mathcal C_{g\cdot j}.
\]

Pass conditions:

- group order 720;
- reference orbit size 10;
- reference stabilizer size 72;
- maximum channel-covariance residual below tolerance.

### 3.2 Stabilizer representation

Restrict the signed action to the reference channel:

\[
\rho(h)=Q^{\mathsf T}J_7(h)Q,
\qquad h\in H.
\]

Test:

- channel invariance;
- orthogonality of \(\rho(h)\);
- character inner product
  \[
  \langle\chi,\chi\rangle_H
  =\frac1{|H|}\sum_{h\in H}|\chi(h)|^2;
  \]
- dimension of the commutant
  \[
  \operatorname{End}_H(\mathcal C).
  \]

The multiplicity-free four-block candidate predicts

\[
\langle\chi,\chi\rangle_H=4,
\qquad
\dim\operatorname{End}_H(\mathcal C)=4.
\]

### 3.3 Stabilizer equivariance of the channel operator

For the reference channel operator \(K_{\mathcal C}\), test

\[
\rho(h)K_{\mathcal C}=K_{\mathcal C}\rho(h)
\qquad
\forall h\in H.
\]

If the channel representation is multiplicity-free, Schur's lemma then forces \(K_{\mathcal C}\) to act as a scalar on each irreducible block.

### 3.4 Spectral projectors and irreducibility

Construct the exact-candidate Lagrange projectors

\[
P_\lambda
=
\prod_{\mu\neq\lambda}
\frac{K_{\mathcal C}-\mu I}{\lambda-\mu},
\]

for

\[
\lambda\in\left\{1,\frac65,\frac85,\frac95\right\}.
\]

Test:

- ranks \(2,4,4,1\);
- idempotency;
- mutual orthogonality;
- sum to identity;
- commutation with the stabilizer;
- scalar action of \(K_{\mathcal C}\);
- commutant dimension 1 on every block;
- block character norm 1.

The final two tests support irreducibility of each real block under \(H\).

### 3.5 Transport to all ten channels

For one permutation carrying the reference pair to each target pair, test

\[
J_7(g)K_0J_7(g)^{-1}=K_j.
\]

This should explain why all ten channels have identical spectra without independently fitting each channel.

### 3.6 Cross-seed comparison

When both seed-11 and seed-29 `operator_data.npz` files are supplied, compare:

- the full squared spectrum;
- all ten target channel subspaces.

Raw source-coordinate residue matrices are not expected to agree entrywise because independently computed orthonormal source bases may differ.

---

## 4. Exact polynomial certificate

The script records the candidate characteristic polynomial

\[
\chi_{\mathcal C}(x)
=(x-1)^2
\left(x-\frac65\right)^4
\left(x-\frac85\right)^4
\left(x-\frac95\right),
\]

and minimal polynomial

\[
m_{\mathcal C}(x)
=(x-1)
\left(x-\frac65\right)
\left(x-\frac85\right)
\left(x-\frac95\right).
\]

These are exact candidate polynomials inferred from the 02D spectrum. The script verifies their representation-theoretic compatibility, not their analytic derivation from first principles.

---

## 5. Verdict boundary

A successful 02E run supports:

1. exact finite \(S_6\) indexing of the ten complement-pair channels;
2. a reference stabilizer of order 72;
3. a multiplicity-free four-block decomposition of dimensions \(2+4+4+1\);
4. stabilizer-equivariance of the residue channel operator;
5. irreducibility of the four numerical spectral blocks;
6. conjugacy of all ten channel operators.

It does **not** yet prove:

- a closed-form Parke--Taylor identity producing the rank-11 channel;
- an exact symbolic derivation of \(1,6/5,8/5,9/5\);
- a physical interpretation of the four blocks;
- that the Euclidean operator metric is physically selected.

---

## 6. Run command

```bash
caffeinate -i python3 scripts/ehf_amp_found_02e_complement_pair_symmetry_certificate.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --operator-data runs/ehf_amp_found_02d_seed11/operator_data.npz \
  --comparison-operator-data runs/ehf_amp_found_02d_seed29/operator_data.npz \
  --out-dir runs/ehf_amp_found_02e
```

No Parke--Taylor basis recomputation is required. The script consumes the two completed 02D operator certificates.

---

## 7. Principal outputs

```text
summary.json
run.log
group_action_audit.json
stabilizer_representation_audit.json
spectral_irrep_audit.json
channel_transport_audit.json
cross_seed_comparison.json
exact_polynomials.json
spectral_block_summary.csv
stabilizer_character_rows.csv
channel_transport_rows.csv
```

---

## 8. Internal validation result

An end-to-end run on the uploaded seed-11 and seed-29 operator bundles produced:

```text
S6 group elements:                    720
reference orbit size:                 10
reference stabilizer size:            72
max channel-covariance residual:      2.3e-15
character inner product:              4.000000000000
full commutant dimension:             4
projector ranks:                      [2, 4, 4, 1]
block commutant dimensions:           [1, 1, 1, 1]
block character norms:                [1, 1, 1, 1]
max K/stabilizer commutator error:     1.3e-15
max ten-channel conjugacy error:       1.4e-15
max cross-seed pair-subspace residual:2.1e-15
```

This validates the implementation and strongly supports the proposed symmetry decomposition. The remaining task is an analytic identification of the four irreducible \(H\)-modules and a derivation of the four rational scalars.
