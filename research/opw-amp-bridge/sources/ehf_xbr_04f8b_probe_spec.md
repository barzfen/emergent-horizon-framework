# EHF-XBR-04F8B: Residual Commutant Algebra Classification

## 1. Purpose

EHF-XBR-04F8 resolved 46 of 48 XBR-04F7 central-isotypic sectors and certified 136 of 138 terminal blocks as rational irreducible. The only unresolved residue is a matched pair of 12-dimensional blocks in

\[
A=(6,7,8),
\]

in sectors 5 and 6.

Each unresolved block \(V\) satisfies

\[
\dim V=12,
\qquad
\dim_{\mathbb Q}\operatorname{End}_G(V)=4,
\qquad
\dim_{\mathbb Q}Z(\operatorname{End}_G(V))=1.
\]

EHF-XBR-04F8B asks:

> Is each four-dimensional central commutant the split algebra \(M_2(\mathbb Q)\), so that \(V\) is two copies of a six-dimensional irreducible module, or is it a quaternion division algebra, so that \(V\) is rational irreducible but not absolutely irreducible?

The probe performs a complete algebra classification. It does not repeat the F8 bounded search for singular elements.

---

## 2. Target objects

For each unresolved terminal block, reconstruct

\[
C_V=\operatorname{End}_{\mathbb Q[G]}(V).
\]

The expected F8 schema is

\[
\dim C_V=4,
\qquad
Z(C_V)=\mathbb Q.
\]

Every four-dimensional central simple algebra over \(\mathbb Q\) is a quaternion algebra. F8B therefore constructs an exact presentation

\[
C_V\cong(a,b)_{\mathbb Q}
\]

with basis \(1,i,j,k\) satisfying

\[
i^2=a,\qquad j^2=b,\qquad ij=-ji=k.
\]

The presentation itself is checked exactly from the commutant multiplication table.

---

## 3. Reduced trace and quaternion presentation

Let \(L_x\) denote left multiplication by \(x\) on the four-dimensional algebra \(C_V\). Since \(C_V\) has degree two,

\[
\operatorname{trd}(x)=\frac12\operatorname{tr}(L_x).
\]

The pure-quaternion subspace is

\[
C_V^0=\ker(\operatorname{trd}),
\qquad
\dim C_V^0=3.
\]

The probe chooses exact pure elements \(i,j\) such that

\[
i^2=a\in\mathbb Q^\times,
\qquad
j^2=b\in\mathbb Q^\times,
\qquad
ij+ji=0.
\]

It verifies that \(1,i,j,ij\) are linearly independent and span the complete commutant.

---

## 4. Complete local classification

The parameters \(a,b\) are reduced to rational squareclasses. The probe evaluates the Hilbert symbol

\[
(a,b)_v
\]

at:

- the real place;
- \(p=2\);
- every odd prime dividing the squareclasses of \(a\) or \(b\).

No other place can ramify.

Hilbert reciprocity is checked:

\[
\prod_v(a,b)_v=1.
\]

The exact classification is:

\[
\operatorname{Ram}(C_V)=\varnothing
\quad\Longleftrightarrow\quad
C_V\cong M_2(\mathbb Q),
\]

while a nonempty ramification set certifies that \(C_V\) is a quaternion division algebra.

This is a complete classification, not a bounded coefficient search.

---

## 5. Split-algebra certificate

Each 18-dimensional source sector already contains:

- the unresolved 12-dimensional block \(V\);
- one certified absolutely irreducible six-dimensional sibling \(W\).

In the split case F8B computes

\[
\operatorname{Hom}_G(W,V)
\]

exactly. A full-rank map

\[
T:W\hookrightarrow V
\]

supplies a six-dimensional invariant image.

The probe then solves inside \(C_V\) for an equivariant projection \(P\) with

\[
P^2=P,
\qquad
\operatorname{rank}P=6,
\qquad
P\rho_V(g)=\rho_V(g)P.
\]

This certifies

\[
V=\operatorname{im}P\oplus\ker P.
\]

Both children must have:

\[
\dim=6,
\qquad
\dim\operatorname{End}_G=1,
\qquad
\langle\chi,\chi\rangle=1.
\]

Full-rank exact intertwiners and complete class characters must identify both children with the certified sibling \(W\). The source sector is then reconstructed as

\[
U\cong W^{\oplus3}.
\]

---

## 6. Division-algebra certificate

If the ramification set is nonempty, then \(C_V\) is a division algebra. Semisimplicity then certifies that \(V\) is rational irreducible.

In this branch the expected conclusion is:

\[
\dim_{\mathbb Q}V=12,
\qquad
\operatorname{End}_G(V)\text{ quaternion division},
\]

so \(V\) is rational irreducible but not absolutely irreducible.

Strict PASS permits this outcome only when:

- the exact quaternion presentation is valid;
- the ramification set is nonempty;
- Hilbert reciprocity holds;
- no full-rank sibling embedding exists.

---

## 7. Census correction

The post-F8B terminal count depends on the classification.

If both 12-dimensional blocks are quaternionic irreducibles, the final census is

\[
138/138
\]

certified terminal blocks.

If both split as \(6+6\), each original terminal block is replaced by two primitive children. The final census is therefore

\[
140/140,
\]

not \(138/138\).

F8B computes the final census from the certified outcome rather than hard-coding either number.

---

## 8. Inputs

Required XBR-04F8 outputs:

- `run_summary.json` with `strict_pass=true`;
- `commutant_sector_ledger.csv`;
- `primitive_module_ledger.csv`;
- sparse primitive bases for the unresolved blocks and their six-dimensional siblings.

The F8 run must therefore have used:

```text
--write-primitive-bases sparse
```

Required XBR-04F7 outputs:

- `run_summary.json`;
- `kernel_module_channel_ledger.csv`;
- `kernel_module_sector_ledger.csv`;
- sparse sector bases.

Required source scripts:

- XBR-04F8;
- XBR-04F7;
- XBR-04F;
- the OPW3 base construction;
- the AMP base construction;
- the AMP rank/key helper.

---

## 9. Self-test

```bash
python3 scripts/ehf_xbr_04f8b_residual_commutant_algebra_classification.py \
  --self-test
```

Expected:

```text
EHF-XBR-04F8B self-test PASS
```

The self-test certifies:

1. classification of \(M_2(\mathbb Q)\) as split;
2. classification of Hamilton’s algebra \((-1,-1)_{\mathbb Q}\) as division, ramified exactly at \(2\) and infinity;
3. Hilbert reciprocity in both examples;
4. exact Hom-space and idempotent-projection machinery.

---

## 10. Production command

From the `OPW3` directory:

```bash
python3 scripts/ehf_xbr_04f8b_residual_commutant_algebra_classification.py \
  --xbr04f8-dir runs/ehf_xbr_04f8 \
  --xbr04f8-script scripts/ehf_xbr_04f8_commutant_multiplicity_primitive_module_splitting_audit.py \
  --xbr04f7-dir runs/ehf_xbr_04f7_v4 \
  --xbr04f7-script scripts/ehf_xbr_04f7_kernel_module_decomposition_support_orbit_audit.py \
  --xbr04f-script scripts/ehf_xbr_04f_invisible_complement_spectrum_symmetry_audit.py \
  --opw-base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --amp-base-script ../AMP/scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --amp-rank-script ../AMP/scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --target-subset 6,7,8 \
  --target-sectors 5,6 \
  --write-resolved-bases sparse \
  --out-dir runs/ehf_xbr_04f8b \
  --strict
```

---

## 11. Outputs

Root outputs:

- `residual_commutant_classification_ledger.csv`;
- `quaternion_multiplication_ledger.csv`;
- `local_invariant_ledger.csv`;
- `resolved_primitive_module_ledger.csv`;
- `resolved_class_character_ledger.csv`;
- `residual_commutant_report.md`;
- `run_summary.json`.

Split-case primitive bases:

```text
channels/A_6_7_8/sector_XX/resolved_YYY.basis.coordinate.json.gz
```

Expected integrity verdict:

```text
EHF_XBR_04F8B_RESIDUAL_COMMUTANT_ALGEBRA_CLASSIFICATION_PASS
```

The verdict certifies the exact algebra classification and the complete outcome-specific module certificate. It does not presuppose that the split case must occur.

---

## 12. Claim boundary

This is an exact finite arithmetic and representation-theoretic audit. It does not identify:

- OPW3 adjacency with a physical Hamiltonian;
- a rational module with a particle or field;
- quaternion ramification with a physical charge or coupling;
- multiplicity with particle generation or species count.

Any later physical interpretation requires a separate bridge argument.
