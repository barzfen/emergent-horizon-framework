# EHF-XBR-04F–04F8B Result Note

## Complete Primitive Rational Decomposition of the Invisible-Complement Kernel

**Programme:** Emergent Horizon Framework  
**Branch:** OPW3–AMP cross-branch reconstruction  
**Date:** 31 July 2026  
**Status:** Exact finite result; F-series representation-theoretic gate closed

---

## 1. Purpose

XBR-04B through XBR-04E established that AMP-generated Krylov closures are exact rational reducing modules of OPW3 adjacency, that each has an exact invisible orthogonal complement, and that rational denominators in unsaturated Krylov coordinates are coordinate-lattice effects rather than intrinsic fractional OPW3 couplings.

The XBR-04F programme then analysed the invisible complements:

\[
\text{invisible complements}
\longrightarrow
\text{exact spectral structure}
\longrightarrow
\text{label-group symmetry}
\longrightarrow
\text{rational central-isotypic sectors}
\longrightarrow
\text{primitive rational modules}.
\]

XBR-04F8 left two 12-dimensional terminal blocks unclassified. XBR-04F8B completes the programme by proving that both four-dimensional residual commutants are split matrix algebras and by constructing the missing six-dimensional module decompositions exactly.

---

## 2. XBR-04F7 and XBR-04F8 starting point

XBR-04F7 decomposed the 216-dimensional aggregate singular-chamber kernel into 48 exact rational central-isotypic sectors.

| XBR-04F7 sector class | Count |
|---|---:|
| Absolutely irreducible, certified by character norm one | 18 |
| Nonabsolute central-isotypic sectors requiring further analysis | 30 |
| Total | 48 |

XBR-04F8 constructed exact rational commutants and recursively split multiplicity blocks using equivariant idempotent projections.

Its terminal census was:

| XBR-04F8 quantity | Result |
|---|---:|
| Source central-isotypic sectors | 48 |
| Terminal blocks | 138 |
| Certified rational-irreducible terminal blocks | 136 |
| Unresolved terminal blocks | 2 |
| Fully resolved source sectors | 46/48 |

The unresolved pair occurred in

\[
A=(6,7,8),
\]

in sectors 5 and 6.

For each sector \(s\), XBR-04F8 had certified

\[
U_s=V_s\oplus W_s,
\]

where

\[
\dim U_s=18,\qquad
\dim V_s=12,\qquad
\dim W_s=6.
\]

The sibling \(W_s\) was certified absolutely irreducible, while

\[
\dim_{\mathbb Q}\operatorname{End}_G(V_s)=4,
\qquad
\dim_{\mathbb Q}Z(\operatorname{End}_G(V_s))=1.
\]

The remaining alternatives were

\[
\operatorname{End}_G(V_s)\cong M_2(\mathbb Q)
\]

or a quaternion division algebra over \(\mathbb Q\).

---

## 3. Exact XBR-04F8B construction

For each residual block \(V_s\), XBR-04F8B reconstructs

\[
C_s=\operatorname{End}_{\mathbb Q[G]}(V_s)
\]

and its exact multiplication table.

### 3.1 Quaternion presentation

Because \(C_s\) is a four-dimensional central simple algebra over \(\mathbb Q\), F8B constructs an exact quaternion presentation

\[
C_s\cong(a_s,b_s)_{\mathbb Q}.
\]

Using the reduced trace

\[
\operatorname{trd}(x)=\frac12\operatorname{tr}(L_x),
\]

the probe constructs pure elements \(i,j\) satisfying

\[
i^2=a_s,\qquad
j^2=b_s,\qquad
ij=-ji,
\]

and verifies that \(1,i,j,ij\) form a basis of the complete commutant.

### 3.2 Complete local classification

F8B evaluates the Hilbert symbols

\[
(a_s,b_s)_v
\]

at every potentially ramified finite place and at the real place. It verifies Hilbert reciprocity:

\[
\prod_v(a_s,b_s)_v=1.
\]

An empty ramification set certifies

\[
C_s\cong M_2(\mathbb Q),
\]

while a nonempty ramification set would certify a quaternion division algebra.

This is a complete algebra classification, not another bounded search for small singular commutant elements.

### 3.3 Exact module splitting

In the split case F8B computes

\[
\operatorname{Hom}_G(W_s,V_s)
\]

and constructs a full-rank embedding

\[
W_s\hookrightarrow V_s.
\]

It then solves for an exact equivariant projection

\[
P_s\in C_s
\]

with

\[
P_s^2=P_s,\qquad
\operatorname{rank}P_s=6,\qquad
P_s\rho(g)=\rho(g)P_s.
\]

The two children

\[
\operatorname{im}P_s,
\qquad
\ker P_s
\]

are checked to have one-dimensional commutants, character norm one, exact class-character agreement with \(W_s\), and full-rank exact intertwiners with \(W_s\).

---

## 4. XBR-04F8B verdict

```text
strict checks: 17/17
EHF_XBR_04F8B_RESIDUAL_COMMUTANT_ALGEBRA_CLASSIFICATION_PASS
```

The production run completed in 35.69 seconds.

| Sector | Residual dimension | Commutant classification | Ramified places | Exact module result |
|---:|---:|---|---|---|
| 5 | 12 | \(M_2(\mathbb Q)\) | None | \(V_5\cong W_5^{\oplus2}\), \(U_5\cong W_5^{\oplus3}\) |
| 6 | 12 | \(M_2(\mathbb Q)\) | None | \(V_6\cong W_6^{\oplus2}\), \(U_6\cong W_6^{\oplus3}\) |

Thus both residual four-dimensional central commutants split:

\[
\operatorname{End}_G(V_5)
\cong
\operatorname{End}_G(V_6)
\cong
M_2(\mathbb Q).
\]

No quaternion division-algebra residue survives.

---

## 5. Final primitive census

Each unresolved 12-dimensional F8 block is replaced by two certified six-dimensional primitive children. Therefore two source blocks become four primitive blocks, increasing the terminal count by two:

\[
138-2+4=140.
\]

The final exact census is:

| Quantity | Final result |
|---|---:|
| XBR-04F7 source sectors | 48 |
| Fully resolved source sectors | 48/48 |
| Certified primitive terminal blocks | 140 |
| Total primitive terminal blocks | 140 |
| Unresolved terminal blocks | 0 |

Equivalently,

\[
\boxed{48/48\text{ source sectors resolved}}
\]

and

\[
\boxed{140/140\text{ primitive terminal blocks certified}.}
\]

---

## 6. Exact theorem-level conclusion

The complete F-series supports the following finite statement:

> The 216-dimensional aggregate singular-chamber invisible-complement kernel decomposes into 48 exact rational central-isotypic sectors, and every sector admits a complete decomposition into certified rational irreducible modules. All non-unit central character norms encountered in the programme are explained by ordinary representation multiplicity.

For the final pair,

\[
U_s\cong W_s^{\oplus3},
\qquad s\in\{5,6\},
\]

with

\[
\dim W_s=6,
\qquad
\operatorname{End}_G(W_s)=\mathbb Q.
\]

The conclusion is sectorwise. It does not assert that \(W_5\) and \(W_6\) are the same literal-group module unless separately certified by their exact character or an explicit intertwiner.

---

## 7. Why F8 stopped early

F8’s bounded deterministic search found neither a singular commutant element nor a field certificate inside the two 12-dimensional blocks. F8 therefore correctly left them unresolved.

F8B shows that singular rank-six idempotents do exist. The issue was search reach, not exotic rational structure. F8B reached the idempotents structurally by:

1. completely classifying the commutant as \(M_2(\mathbb Q)\);
2. using the certified six-dimensional sibling module;
3. constructing \(\operatorname{Hom}_G(W_s,V_s)\);
4. solving exactly for the equivariant projection.

This validates F8’s conservative certification policy: failure of a bounded singular-element search was not treated as irreducibility.

---

## 8. Updated cross-branch structural picture

The exact finite picture is now:

1. AMP channels select exact rational reducing modules of OPW3 adjacency.
2. Each selected module has an exact invisible orthogonal complement.
3. Every certified rational invariant sector has an invariant saturated integral lattice.
4. Large rational denominators in unsaturated Krylov coordinates are coordinate-lattice effects.
5. The invisible complements possess exact finite label-group representation structure.
6. Their 216-dimensional aggregate singular-chamber kernel decomposes into 48 rational central-isotypic sectors.
7. All 48 sectors decompose completely into certified rational irreducible modules.
8. All non-unit central character norms are accounted for by ordinary multiplicity.
9. No unresolved field-commutant or quaternion division-algebra case remains.

The XBR-04F representation-theoretic programme is therefore closed at the audited finite scale.

---

## 9. Integrity boundary

The F8B PASS certifies:

- both residual F8 bases and six-dimensional sibling bases match their recorded hashes;
- the reconstructed label-group representations are exact;
- both residual commutants have dimension four and centre \(\mathbb Q\);
- both quaternion presentations and multiplication relations are exact;
- all required Hilbert-symbol and reciprocity checks pass;
- both algebras are split as \(M_2(\mathbb Q)\);
- both rank-six equivariant projections are exact;
- all four new six-dimensional children are absolutely irreducible;
- child characters and exact intertwiners identify each pair with its certified sibling;
- both 18-dimensional source sectors reconstruct exactly;
- no unresolved terminal block remains.

---

## 10. Claim boundary

These are exact finite arithmetic and representation-theoretic statements about OPW3 chamber adjacency, AMP-generated invariant sectors, invisible complements, and finite label-group actions.

They do not:

- identify OPW3 adjacency with a physical Hamiltonian or time evolution;
- identify any module with a physical particle or field;
- assign physical meaning to module multiplicities or commutant dimensions;
- identify quaternion ramification with a physical charge or coupling;
- derive amplitudes from OPW3 dynamics;
- establish persistence of the finite representation pattern at larger \(n\).

The result supplies rigorous finite structure for later bridge work. It is not a physical interpretation by itself.

---

## 11. Programme decision

No F8C cleanup probe is required. The algebra-classification gate is closed.

The next probe should begin a deliberately chosen new question—for example, recurrence or scaling of primitive module types beyond the audited finite system, or a return to the OPW3–AMP bridge—rather than extending the F-series merely to produce another census.
