# EHF-XBR-04F8: Commutant Multiplicity and Primitive Module Splitting Audit

## 1. Purpose

EHF-XBR-04F7 decomposed the 216-dimensional aggregate singular-chamber kernel into 48 exact rational central-isotypic sectors. Eighteen sectors were certified absolutely irreducible by character norm one, while 30 sectors retained nontrivial character norms and therefore could still contain multiplicity, rational field structure, or Schur-index structure.

EHF-XBR-04F8 asks:

> Which nonabsolute central-isotypic sectors are repeated copies of smaller rational modules, and which terminal sectors are genuinely rational irreducible modules with nontrivial endomorphism division algebras?

The probe consumes the exact sector bases written by XBR-04F7. It does **not** recompute chamber kernels or repeat the central-isotypic decomposition.

---

## 2. Mathematical object

For an XBR-04F7 central-isotypic sector

\[
U\subseteq K_A,
\]

with exact label-group representation

\[
\rho_U:G_A\longrightarrow \mathrm{GL}(U),
\]

define its rational commutant algebra

\[
C_U=\operatorname{End}_{\mathbb Q[G_A]}(U)
 =\{T\in\operatorname{Mat}_{\dim U}(\mathbb Q):
 T\rho_U(g)=\rho_U(g)T\ \forall g\in G_A\}.
\]

Because \(G_A\) is finite and the coefficient field has characteristic zero, \(U\) is semisimple. If

\[
U\cong W^{\oplus m}
\]

for a rational irreducible module \(W\), then

\[
C_U\cong M_m(D),
\qquad
D=\operatorname{End}_{\mathbb Q[G_A]}(W),
\]

where \(D\) is a finite-dimensional division algebra over \(\mathbb Q\).

The exact commutant dimension must equal the complex character norm already measured in XBR-04F7:

\[
\dim_{\mathbb Q} C_U
=
\langle\chi_U,\chi_U\rangle.
\]

This equality is used as a source-to-probe consistency certificate.

---

## 3. Exact commutant construction

For generator matrices \(R_1,\ldots,R_s\), an unknown matrix \(X\) belongs to the commutant exactly when

\[
XR_i-R_iX=0
\qquad (1\le i\le s).
\]

The script forms this rational linear system in the \((\dim U)^2\) entries of \(X\) and computes an exact nullspace over \(\mathbb Q\).

For scalar sectors, where every group generator acts as a scalar matrix, the script uses the exact shortcut

\[
C_U=M_{\dim U}(\mathbb Q),
\qquad
\dim C_U=(\dim U)^2,
\qquad
\dim Z(C_U)=1.
\]

This avoids explicitly constructing and centralising large matrix-unit bases such as the 121-dimensional commutants of the 11-dimensional scalar multiplicity sectors.

The centre

\[
Z(C_U)=\{Z\in C_U:ZT=TZ\ \forall T\in C_U\}
\]

is also computed exactly unless the scalar shortcut applies.

---

## 4. Certified multiplicity splitting

### 4.1 Singular commutant maps

If \(0\ne T\in C_U\) is singular, then

\[
0<\operatorname{im}T<U
\]

is a proper \(G_A\)-invariant subspace.

The script performs a deterministic bounded census of commutant elements built from:

- individual exact commutant basis elements;
- trace-free basis elements;
- small two-basis integer combinations;
- products of basis elements;
- selected three-basis sums.

The census is controlled by:

```text
--combination-bound
--candidate-limit
```

Every detected singular element is exact; no floating-point rank decision is used.

### 4.2 Exact Maschke projection

Let \(V=\operatorname{im}T\). The script solves for a projection

\[
P\in C_U
\]

subject to

\[
P|_V=I_V,
\qquad
\operatorname{im}P\subseteq V.
\]

These are linear constraints in the commutant coefficients. They imply

\[
P^2=P,
\qquad
U=\operatorname{im}P\oplus\ker P.
\]

The script verifies exactly that:

- \(P^2=P\);
- \(P\) commutes with every representation generator;
- both children are nonzero and invariant;
- their dimensions add to the parent dimension;
- their combined basis has full parent rank.

The procedure then recurses on both children.

### 4.3 Scalar multiplicity sectors

If all generator actions on a block are scalar, every rational line is invariant. The block is therefore split directly into one-dimensional rational irreducible modules. This is an exact decomposition, not a heuristic choice.

---

## 5. Primitive-module certificates

A terminal block is called **certified rational irreducible** only under one of the following exact conditions.

### 5.1 One-dimensional commutant

If

\[
\dim_{\mathbb Q}\operatorname{End}_G(V)=1,
\]

then the commutant is \(\mathbb Q\), and semisimplicity implies that \(V\) is absolutely irreducible.

### 5.2 Field commutant

Suppose the exact commutant is commutative of dimension \(d\). The script searches for an element \(T\) whose exact minimal polynomial:

- is irreducible over \(\mathbb Q\);
- has degree \(d\);
- generates a \(d\)-dimensional algebra \(\mathbb Q[T]\).

Then

\[
C_V=\mathbb Q[T]
\]

is a field. Hence it is a division algebra, and semisimplicity implies that \(V\) is rational irreducible. It need not be absolutely irreducible; its character norm equals the field degree.

### 5.3 Unresolved terminal blocks

If the bounded census finds no singular commutant element and no exact field certificate, the block is recorded as

```text
unresolved_no_singular_or_field_certificate
```

It is **not** called irreducible. Such a block may be:

- an irreducible module with a noncommutative division algebra, such as a quaternionic case;
- a multiplicity block whose singular elements were not reached by the bounded census.

Strict PASS does not require this research question to be resolved.

---

## 6. Character and reconstruction checks

For every terminal block, the probe computes exact conjugacy-class characters and checks

\[
\dim_{\mathbb Q}\operatorname{End}_G(V)
=
\langle\chi_V,\chi_V\rangle.
\]

For every source sector, it verifies exact character additivity:

\[
\chi_U=\sum_j\chi_{V_j}.
\]

It also verifies that the terminal block bases reconstruct the complete source sector as a direct sum.

A sector receives a certified multiplicity \(m\) only when:

- every terminal block is certified rational irreducible;
- all terminal blocks have the same dimension;
- all terminal blocks have the same exact character for the same literal group.

Then

\[
U\cong W^{\oplus m}
\]

is certified.

---

## 7. Primitive coordinate support

Each terminal block is converted back into an exact primitive integer basis in chamber coordinates. The probe records:

- active and forced-zero coordinate counts;
- full-coordinate-support status;
- active automorphism-orbit count;
- whether the active support is an exact union of automorphism orbits;
- whether the entire block is supported on one orbit;
- deterministic basis support ranges.

These diagnostics test whether the orbit-delocalisation found in XBR-04F7 survives after multiplicity is removed.

---

## 8. Recurring primitive module types

### Exact recurrence

For certified primitive modules acted on by the same literal label subgroup, equality of the complete conjugacy-class character certifies equality of semisimple module type. Such groups are written as

```text
exact_same_literal_group_primitive_character
```

### Coarse cross-group candidates

A weaker fingerprint uses:

- group order;
- primitive dimension;
- primitive commutant dimension;
- element-order/trace histogram.

Repeated coarse fingerprints are written as

```text
coarse_cross_group_primitive_candidate
```

These are analogies only, not certified cross-group module isomorphisms.

---

## 9. Inputs

Required XBR-04F7 directory contents:

- `run_summary.json` with `strict_pass=true`;
- `kernel_module_channel_ledger.csv`;
- `kernel_module_sector_ledger.csv`;
- `kernel_module_class_character_ledger.csv`;
- `channels/A_a_b_c/sector_XX.basis.coordinate.json.gz` for all 48 sectors.

The XBR-04F7 run must therefore have used:

```text
--write-sector-bases sparse
```

Required source scripts:

- the completed XBR-04F7 script;
- `ehf_xbr_04f_invisible_complement_spectrum_symmetry_audit.py`;
- OPW3 base construction script;
- AMP fibre base script;
- AMP rank/key script.

---

## 10. Self-test

```bash
python3 scripts/ehf_xbr_04f8_commutant_multiplicity_primitive_module_splitting_audit.py \
  --self-test
```

Expected:

```text
EHF-XBR-04F8 self-test PASS
```

The self-test verifies three exact synthetic cases:

1. a three-copy scalar module with commutant \(M_3(\mathbb Q)\);
2. the rational two-dimensional \(C_3\) module with commutant \(\mathbb Q(\zeta_3)\);
3. two copies of that module, whose commutant is \(M_2(\mathbb Q(\zeta_3))\), including an exact singular-map split and Maschke projection.

---

## 11. Production command

```bash
python3 scripts/ehf_xbr_04f8_commutant_multiplicity_primitive_module_splitting_audit.py \
  --xbr04f7-dir runs/ehf_xbr_04f7_v4 \
  --xbr04f7-script scripts/ehf_xbr_04f7_kernel_module_decomposition_support_orbit_audit.py \
  --xbr04f-script scripts/ehf_xbr_04f_invisible_complement_spectrum_symmetry_audit.py \
  --opw-base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --amp-base-script ../AMP/scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --amp-rank-script ../AMP/scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --combination-bound 2 \
  --candidate-limit 5000 \
  --write-primitive-bases sparse \
  --out-dir runs/ehf_xbr_04f8 \
  --strict
```

---

## 12. Outputs

### Root ledgers

- `commutant_sector_ledger.csv`
- `commutant_split_ledger.csv`
- `primitive_module_ledger.csv`
- `primitive_class_character_ledger.csv`
- `primitive_recurrence_ledger.csv`
- `module_splitting_report.md`
- `run_summary.json`

### Sparse primitive bases

```text
channels/A_a_b_c/sector_XX/primitive_YYY.basis.coordinate.json.gz
```

### Expected integrity verdict

```text
EHF_XBR_04F8_COMMUTANT_MULTIPLICITY_PRIMITIVE_MODULE_SPLITTING_AUDIT_PASS
```

The verdict certifies the audit and reconstruction machinery. It does not assert that every noncommutative division-algebra candidate has been classified.
