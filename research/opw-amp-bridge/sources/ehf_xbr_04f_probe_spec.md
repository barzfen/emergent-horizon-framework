# EHF-XBR-04F — Invisible-Complement Spectrum and Symmetry Audit


**Programme:** Emergent Horizon Framework  
**Branch:** OPW3 / Amplitude Cross-Bridge  
**Status:** Exact finite probe specification  
**Date:** 27 July 2026


## 1. Motivation


EHF-XBR-04C certified an exact rational OPW3-invariant sector


\[
\mathcal K_A\subseteq \mathbb Q^{C_A}
\]


for every AMP channel. EHF-XBR-04D then certified the exact orthogonal reducing decomposition


\[
\mathbb Q^{C_A}=\mathcal K_A\oplus\mathcal K_A^\perp.
\]


EHF-XBR-04E resolved the arithmetic-coordinate issue: the large rational coefficients seen in deterministic Krylov coordinates are not intrinsic fractional OPW3 couplings.


The next question is structural rather than arithmetic:


> What spectrum and exact symmetry structure live in the AMP-invisible reducing complement \(\mathcal K_A^\perp\)?


XBR-04F answers this for a representative panel using exact characteristic polynomials, exact irreducible factorisation, exact spectral-overlap tests and exact label-induced symmetry representations.


## 2. Exact objects


For a selected channel \(A\), let


\[
M_A=\operatorname{Adj}(C_A)
\]


be the integer OPW3 chamber adjacency matrix. Let \(V_A\) be the XBR-04C basis of the visible sector and let \(W_A\) be the XBR-04D integer basis of


\[
\mathcal K_A^\perp=\ker_{\mathbb Q}(V_A).
\]


XBR-04D certifies


\[
W_A M_A=R_A^\perp W_A
\]


for an exact rational matrix \(R_A^\perp\), together with Gram self-adjointness.


Because \(M_A\) is symmetric and \(\mathcal K_A\) is invariant, both \(\mathcal K_A\) and \(\mathcal K_A^\perp\) are reducing subspaces. Therefore


\[
\chi_{C_A}(x)=\chi_A^{\mathrm{vis}}(x)\,\chi_A^\perp(x).
\]


## 3. Spectrum audit


For each selected channel, compute exactly:


1. the chamber characteristic polynomial \(\chi_{C_A}(x)\);
2. the invisible characteristic polynomial
   \[
   \chi_A^\perp(x)=\det(xI-R_A^\perp);
   \]
3. the invisible minimal polynomial \(\mu_A^\perp(x)\);
4. the visible characteristic polynomial by exact quotient
   \[
   \chi_A^{\mathrm{vis}}(x)=\chi_{C_A}(x)/\chi_A^\perp(x);
   \]
5. the irreducible factorisation over \(\mathbb Q\)
   \[
   \chi_A^\perp(x)=\prod_i f_i(x)^{m_i};
   \]
6. the exponent of every invisible factor \(f_i\) in \(\chi_A^{\mathrm{vis}}\).


This separates:


- **invisible-only spectral support**, whose irreducible factor does not occur visibly;
- **shared spectral support**, whose eigenvalue orbit occurs in both reducing sectors.


The audit records:


- factor degrees and multiplicities;
- zero-eigenvalue multiplicity;
- distinct-root count over the algebraic closure;
- maximum algebraic multiplicity;
- simple-spectrum status;
- exact sign symmetry under \(\lambda\mapsto-\lambda\);
- Newton trace moments \(\operatorname{tr}((R_A^\perp)^k)\);
- the semisimple spectral-commutant dimension
  \[
  \sum_i \deg(f_i)m_i^2.
  \]


Since the complement action is Gram self-adjoint, its minimal polynomial must be square-free. The probe checks that


\[
\mu_A^\perp(x)=\prod_i f_i(x).
\]


## 4. Symmetry audit


The AMP channels are indexed by three-subsets


\[
A\subset\{2,3,4,5,6,7,8\},
\]


with labels \(1\) and \(9\) distinguished. The natural candidate setwise stabiliser is


\[
G_A^{\mathrm{cand}}
=
S_A\times S_{\{2,\ldots,8\}\setminus A},
\]


of order


\[
3!\,4!=144.
\]


The probe enumerates all 144 label permutations and tests exactly whether each:


1. maps the AMP fibre/chamber to itself;
2. induces a permutation of chamber states;
3. preserves every OPW3 chamber edge.


The accepted permutations form the exact label-induced OPW3 chamber automorphism subgroup


\[
G_A^{\mathrm{OPW3}}\le G_A^{\mathrm{cand}}.
\]


The script verifies identity, inverses and closure, then extracts an exact generating set.


For every certified group generator, and for every group element when the invisible dimension is small, the probe reconstructs the induced action \(S_g^\perp\) on the invisible complement:


\[
g(W_A)=S_g^\perp W_A.
\]


It certifies


\[
(S_g^\perp)^{\operatorname{ord}(g)}=I
\]


and


\[
S_g^\perp R_A^\perp=R_A^\perp S_g^\perp.
\]


The symmetry ledger records traces, fixed-space dimensions, anti-fixed dimensions for involutions, trivial-action tests, representation kernel size and image order where the full representation is enumerated.


## 5. Representative panel


The default panel is:


| Channel | Chamber | Visible | Invisible | Role |
|---|---:|---:|---:|---|
| \((4,6,7)\) | 432 | 430 | 2 | Minimal nontrivial proper complement |
| \((4,6,8)\) | 468 | 459 | 9 | Low-codimension confirmation |
| \((3,6,7)\) | 396 | 386 | 10 | Second low-codimension confirmation |
| \((2,3,6)\) | 216 | 54 | 162 | Broad invisible sector |


For invisible dimension at most 16, the full symmetry representation is enumerated. For the 162-dimensional complement, an exact generating-set representation certifies the full group action while avoiding unnecessary repeated coordinate reconstruction.


## 6. Strict falsifiers


A selected channel fails if any of the following occurs:


1. its XBR-04C or XBR-04D source certificate is not strict-pass;
2. the reconstructed visible or invisible basis hash disagrees with its source certificate;
3. the invisible rank differs from chamber codimension;
4. the invisible restricted action is not exact or not Gram self-adjoint;
5. \(\chi_A^\perp\) does not divide \(\chi_{C_A}\) exactly;
6. factor reconstruction fails;
7. the minimal polynomial is not square-free or differs from the product of distinct characteristic factors;
8. the accepted label automorphisms fail the group axioms;
9. the extracted generators do not generate the accepted group;
10. an induced complement representation is inexact, has the wrong finite order or fails to commute with adjacency.


No nontrivial symmetry, simple spectrum, sign symmetry or spectral separation is assumed. Those are measured outcomes, not pass conditions.


## 7. Outputs


The probe emits:


- `run_summary.json`;
- `spectrum_ledger.csv`;
- `factor_ledger.csv`;
- `symmetry_ledger.csv`;
- `symmetry_generator_ledger.csv`;
- per-channel `certificate.json` files;
- optional exact rational symmetry matrices in compressed coordinate format.


The selected-panel pass verdict is


```text
EHF_XBR_04F_SELECTED_INVISIBLE_COMPLEMENT_SPECTRUM_SYMMETRY_PASS
```


A complete 35-channel pass verdict is


```text
EHF_XBR_04F_INVISIBLE_COMPLEMENT_SPECTRUM_SYMMETRY_AUDIT_PASS
```


## 8. Claim boundary


XBR-04F is an exact finite spectral and representation-theoretic audit of OPW3 chamber adjacency. It does not identify adjacency with a physical Hamiltonian. It does not identify an eigenvalue with an energy, a multiplicity with a particle family, an invisible sector with dark matter or an exact graph automorphism with a fundamental physical symmetry.


Any physical interpretation requires a separate, explicit bridge with independent tests.