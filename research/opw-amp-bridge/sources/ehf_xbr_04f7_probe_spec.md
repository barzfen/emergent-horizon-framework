# EHF-XBR-04F7: Kernel Module Decomposition and Support-Orbit Audit

## 1. Purpose

EHF-XBR-04F6 established that the 11 singular proper OPW3 chamber kernels are exact, globally structured, and only partially explained by visible label symmetry. In particular:

- the total chamber-kernel dimension is 216;
- no chamber kernel is entirely constant on label-automorphism orbits;
- four chambers have a nonzero symmetry-fixed kernel sector;
- two chambers admit an involution acting as \(-I\) on the entire kernel;
- ordinary degree-colour refinement explains little of the observed nullity.

EHF-XBR-04F7 asks the next structural question:

> How do the exact chamber kernels decompose as rational modules for their label-induced automorphism groups, and how are those module sectors distributed across coordinate and automorphism-orbit support?

The probe consumes the exact sparse kernel bases written by XBR-04F6. It does **not** recompute chamber nullspaces.

---

## 2. Mathematical object

For a singular chamber \(A\), let

\[
K_A=\ker(\mathcal A_A)\subseteq \mathbb Q^{C_A},
\]

where \(\mathcal A_A\) is the chamber adjacency matrix and \(C_A\) is the chamber state set.

Let \(G_A\) be the exact label-induced chamber automorphism group found in XBR-04F6. The coordinate permutation action preserves \(K_A\), giving an exact rational representation

\[
\rho_A:G_A\longrightarrow \mathrm{GL}(K_A).
\]

For each conjugacy class \(\mathcal C\subseteq G_A\), define the class-sum operator

\[
Z_{\mathcal C}=\sum_{g\in\mathcal C}\rho_A(g).
\]

The operators \(Z_{\mathcal C}\) lie in the centre of the image of \(\mathbb Q[G_A]\) and commute exactly.

---

## 3. Exact rational central-isotypic decomposition

The probe computes the common rational primary decomposition of all class-sum operators:

\[
K_A=U_{A,1}\oplus\cdots\oplus U_{A,r_A}.
\]

Each \(U_{A,i}\) is an exact \(G_A\)-invariant rational subspace on which every class sum has a single irreducible primary factor over \(\mathbb Q\). These are the rational **central-isotypic sectors** detected by the centre of \(\mathbb Q[G_A]\).

### Claim boundary

A central-isotypic sector is not automatically a rational irreducible module. A sector may still contain:

- repeated copies of a simple module;
- a Galois packet of complex constituents;
- nontrivial Schur-index structure.

The probe therefore records the exact character norm

\[
\langle\chi_U,\chi_U\rangle
=\frac{1}{|G_A|}\sum_{g\in G_A}\chi_U(g)^2.
\]

If this norm equals 1, the sector is certified absolutely irreducible. If it is greater than 1, the sector remains an exact central-isotypic module but is not labelled irreducible without a further decomposition certificate.

---

## 4. Exact representation and character checks

For every singular chamber, the probe:

1. reads the XBR-04F6 primitive integer kernel basis;
2. verifies its dense-row SHA-256 against `kernel_channel_ledger.csv`;
3. reconstructs the same chamber and label-automorphism group;
4. reconstructs every exact kernel representation matrix;
5. verifies the representation homomorphism on generators against every group element;
6. verifies that character traces are constant on conjugacy classes;
7. verifies that all class sums commute with the group generators;
8. verifies that the central sectors form an exact direct sum equal to the full kernel;
9. verifies every sector is group-invariant;
10. verifies every sector basis vector remains in the exact chamber adjacency kernel.

The representation uses the standard column convention. XBR-04F6 stores row-basis images; the script transposes the reconstructed row action so that

\[
\rho(gh)=\rho(g)\rho(h).
\]

---

## 5. Support-orbit audit

For each central-isotypic sector \(U\subseteq K_A\), the probe computes a deterministic primitive integer row basis in chamber coordinates and audits both basis-dependent and basis-independent support data.

### 5.1 Basis-independent coordinate data

- active coordinate count;
- forced-zero coordinate count;
- full-coordinate-support flag;
- number and size of projective coordinate-evaluation classes.

A coordinate is active when some vector in \(U\) is nonzero there. The active set of a group-invariant subspace must be a union of automorphism orbits; this is checked exactly.

Projective coordinate classes identify coordinate evaluation functionals that are equal up to a nonzero rational scalar. Their count is invariant under a change of basis within \(U\).

### 5.2 Automorphism-orbit data

For every chamber-state orbit \(O\), the probe records:

\[
\operatorname{rank}(U\to\mathbb Q^O),
\]

which is the rank of restriction to the orbit;

\[
\dim\{u\in U:u|_O=0\},
\]

which is the dimension vanishing on the orbit; and

\[
\dim\{u\in U:\operatorname{supp}(u)\subseteq O\},
\]

which is the dimension of vectors supported entirely inside the orbit.

This distinguishes:

- sectors visible on every orbit;
- sectors whose information is concentrated on selected orbits;
- sectors containing genuinely orbit-local vectors;
- sectors that are forced to remain multi-orbit/global.

### 5.3 Basis-dependent diagnostics

The minimum, maximum, and mean support sizes of the deterministic canonical sector basis are also written. These are diagnostics only and are never treated as intrinsic localisation invariants.

---

## 6. Recurring module types

### 6.1 Exact recurrence

For two sectors acted on by the **same literal label subgroup** of \(S_9\), equality of the complete rational character vector certifies equality of their semisimple \(\mathbb Q[G]\)-module type.

The exact type fingerprint therefore contains:

- the literal group hash;
- the full character value for every canonically ordered group element.

Repeated exact fingerprints are written as

`exact_same_literal_group_character`.

### 6.2 Coarse cross-group candidates

The probe also creates a weaker group-agnostic fingerprint from:

- group order;
- element-order distribution;
- sector dimension;
- element-order/trace histogram;
- character norm.

Repeated coarse fingerprints are written as

`coarse_cross_group_candidate`.

These are candidate analogies only. They do not certify an isomorphism between modules for different groups.

---

## 7. Inputs

Required XBR-04F6 directory contents:

- `run_summary.json` with `strict_pass=true`;
- `kernel_channel_ledger.csv`;
- `channels/A_a_b_c/kernel_basis.coordinate.json.gz` for all 11 singular channels.

The XBR-04F6 run must therefore have used:

```text
--write-kernel-bases sparse
```

Required source scripts:

- `ehf_xbr_04f_invisible_complement_spectrum_symmetry_audit.py`;
- OPW3 base construction script;
- AMP fibre base script;
- AMP rank/key script.

---

## 8. Self-test

```bash
python3 scripts/ehf_xbr_04f7_kernel_module_decomposition_support_orbit_audit.py \
  --self-test
```

Expected:

```text
EHF-XBR-04F7 self-test PASS
```

The self-test uses an exact synthetic \(C_2\) module

\[
\mathbf 1\oplus\chi\oplus\chi
\]

and verifies:

- a \(1+2\) central decomposition;
- character norms 1 and 4;
- exact support-orbit bookkeeping;
- exact polynomial-matrix evaluation.

---

## 9. Production command

```bash
python3 scripts/ehf_xbr_04f7_kernel_module_decomposition_support_orbit_audit.py \
  --xbr04f6-dir runs/ehf_xbr_04f6_v7 \
  --xbr04f-script scripts/ehf_xbr_04f_invisible_complement_spectrum_symmetry_audit.py \
  --opw-base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --amp-base-script ../AMP/scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --amp-rank-script ../AMP/scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --write-sector-bases sparse \
  --out-dir runs/ehf_xbr_04f7 \
  --strict
```

---

## 10. Outputs

### Root ledgers

- `kernel_module_channel_ledger.csv`
- `kernel_module_sector_ledger.csv`
- `kernel_module_class_character_ledger.csv`
- `kernel_module_support_orbit_ledger.csv`
- `kernel_module_recurrence_ledger.csv`
- `module_report.md`
- `run_summary.json`

### Per-channel outputs

Under `channels/A_a_b_c/`:

- `certificate.json`
- `sector_00.basis.coordinate.json.gz`
- `sector_01.basis.coordinate.json.gz`
- etc., when `--write-sector-bases sparse` is selected.

---

## 11. Strict checks

The strict verdict requires:

1. the source XBR-04F6 run passed;
2. exactly 11 singular channels are loaded;
3. every source kernel-basis hash matches;
4. every reconstructed automorphism-group order matches XBR-04F6;
5. every representation-image order matches XBR-04F6;
6. every reconstructed representation is an exact homomorphism;
7. character traces are constant on conjugacy classes;
8. class sums are exactly central;
9. all central decompositions are exact direct sums;
10. every sector is group-invariant;
11. every final sector is primary-pure for every class sum;
12. all character norms are integral;
13. every sector active set is a union of automorphism orbits;
14. every written sector basis remains in the exact chamber kernel;
15. sector dimensions sum to 216.

The strict verdict validates the decomposition and audit machinery. It does **not** require:

- every sector to be absolutely irreducible;
- recurring module types to exist;
- orbit-local support to exist;
- a single module pattern to distinguish null from mixed chambers.

Expected integrity verdict:

```text
EHF_XBR_04F7_KERNEL_MODULE_DECOMPOSITION_SUPPORT_ORBIT_AUDIT_PASS
```

---

## 12. Interpretation targets

The principal questions are:

1. Do the two full-sign kernels decompose into the same recurring anti-invariant module types, or are their sign actions only superficially similar?
2. Is the 22-dimensional \((4,6,8)\) kernel an exact pair of 11-dimensional sectors, consistent with the observed fixed/anti-fixed split?
3. Do null chambers share exact or coarse module sectors absent from mixed chambers?
4. Are the large mixed kernels \((5,7,8)\) and \((6,7,8)\) built from repeated low-dimensional module types?
5. Are unexplained sectors globally supported across many automorphism orbits, or do they contain orbit-local submodules hidden by whole-kernel summaries?
6. Does a recurring module fingerprint provide a better structural invariant than the scalar chamber classifiers studied in XBR-04F3--04F6?

A positive answer to a recurrence question remains a finite \(n=9\) module theorem unless and until a general construction is proved.
