# EHF-AMP-FOUND-03C  
## Exact Tail-Filtration Subspace Lattice at \(9\to8\)

**Status:** exact explanatory theorem probe  
**Chart:** fixed anchor \(1\), standard canonical representative  
**Transition:** reflection-aware delete-\(9\)

---

## 1. Purpose

03B proved the exact rank formula

\[
r_{\{a<b<c\}}
=
r(b,c)
\in\{0,2,8,9,14,15\}.
\]

That formula says what the ranks are, but not what the six numbers represent.

03C tests a stronger statement:

> After transporting every target fibre to one common reference fibre, the
> 35 transmitted relation images are not 35 unrelated subspaces. They collapse
> exactly to six fixed subspaces of dimensions \(0,2,8,9,14,15\), arranged in
> a small lattice selected by the ordered right-tail occupancy of \(A\).

This is intended to explain why the smallest label \(a\) is invisible.

---

## 2. Exact transmitted image

For

\[
A=\{a<b<c\}\subset\{2,\ldots,8\},
\]

let

\[
Q_A
\]

be the exact integer nine-point KK coordinate matrix and let

\[
D_A
\]

be the exact signed delete-\(9\) map.

The source-local relation space and transmitted image are

\[
R_A^{(9)}=\ker_{\mathbb Q}Q_A,
\qquad
I_A=D_A(R_A^{(9)}).
\]

03C constructs \(I_A\) directly over \(\mathbb Q\). It uses no numerical
relation basis or rational reconstruction.

---

## 3. Canonical common-target transport

Every eight-point target local relation space has dimension \(15\), but its
coordinates belong to a different parity fibre.

Choose the reference subset

\[
A_0=\{2,3,4\}.
\]

For each \(A\), define the ordered-block relabelling

\[
\operatorname{sort}(A)\longmapsto(2,3,4),
\]

\[
\operatorname{sort}(A^c)\longmapsto(5,6,7,8).
\]

At \(n=8\), reversal has Parke--Taylor character \(+1\), so canonicalisation
introduces no sign ambiguity. This gives an exact coordinate isomorphism

\[
T_A:R_A^{(8)}\longrightarrow R_{A_0}^{(8)}.
\]

Define the transported image

\[
\widetilde I_A=T_A(I_A)
\subset R_{A_0}^{(8)}.
\]

---

## 4. Six exact target subspaces

The target theorem is

\[
\widetilde I_A=
\begin{cases}
V_0, & b\le4,\ c\le5,\\
V_2, & b\le4,\ c=6,\\
V_8, & b=5,\ c=6,\\
V_9, & b\le4,\ c\ge7,\\
V_{14}, & b=5,\ c\ge7,\\
V_{15}, & b\ge6,
\end{cases}
\]

where

\[
\dim V_d=d.
\]

Thus the rank law is the dimension shadow of an exact subspace law.

At fixed \(b,c\), changing \(a\):

- changes the source fibre size;
- can change the source relation dimension substantially;
- changes the source residue kernel;

but leaves the transported target image exactly unchanged.

This is the precise sense in which the smallest label contributes only
source-side redundancy.

---

## 5. Tail-filtration interpretation

The six classes can be written as occupancy conditions on the ordered tail:

\[
\{5,6,7,8\}\supset\{6,7,8\}\supset\{7,8\}.
\]

The activated target subspace is:

| Tail condition | Subspace | Dimension |
|---|---:|---:|
| no selected label at or above \(6\) | \(V_0\) | \(0\) |
| selected \(6\), but not \(5\) | \(V_2\) | \(2\) |
| selected pair \(\{5,6\}\) | \(V_8\) | \(8\) |
| selected one of \(\{7,8\}\), but not \(5\) | \(V_9\) | \(9\) |
| selected \(5\) and one of \(\{7,8\}\) | \(V_{14}\) | \(14\) |
| selected at least two of \(\{6,7,8\}\) | \(V_{15}\) | \(15\) |

This is Schubert-like: an ordered flag of label tails controls a filtration
of the target relation space. 03C does not claim a general Schubert theorem,
but it establishes the finite exact structure.

---

## 6. Exact subspace lattice

The six observed spaces satisfy

\[
V_0=0,
\]

\[
V_2\subset V_8,
\qquad
V_2\subset V_9,
\]

\[
\dim(V_8\cap V_9)=3,
\]

\[
\boxed{
V_{14}=V_8+V_9,
}
\]

and

\[
\boxed{
V_{15}=R_{A_0}^{(8)}.
}
\]

Furthermore,

\[
\dim(V_{15}/V_{14})=1.
\]

Let

\[
V_3=V_8\cap V_9.
\]

Then

\[
V_2\subset V_3,
\qquad
\dim(V_3/V_2)=1.
\]

The target-space architecture is therefore:

```text
                 V15  (15)
                  |
                 V14  (14)
                /   \
             V8       V9
               \     /
                 V3  (3)
                  |
                 V2  (2)
                  |
                 V0  (0)
```

The dimensions \(0,2,8,9,14,15\) are no longer isolated rank outputs; they
are dimensions of nodes in this exact lattice.

---

## 7. Stabiliser enlargement

The reference target fibre has relabelling stabiliser

\[
S_3\times S_4,
\]

acting on the selected labels \(\{2,3,4\}\) and complementary labels
\(\{5,6,7,8\}\).

The expected exact stabiliser orders of the six subspaces are

\[
\begin{array}{c|c|l}
\text{subspace} & \text{order} & \text{description}\\
\hline
V_0 & 144 & S_3\times S_4\\
V_2 & 8 & C_2^3\\
V_8 & 24 & S_3\times C_2\times C_2\\
V_9 & 48 & C_2\times S_4\\
V_{14} & 8 & C_2^3\\
V_{15} & 144 & S_3\times S_4
\end{array}
\]

The common subgroup preserving the complete nontrivial lattice is

\[
G=
\langle
(2\,3),(5\,6),(7\,8)
\rangle
\cong C_2^3.
\]

---

## 8. Exact \(C_2^3\) character decomposition

Let the three signs record the eigenvalues under

\[
g_1=(2\,3),
\qquad
g_2=(5\,6),
\qquad
g_3=(7\,8).
\]

The full \(15\)-dimensional target relation space has exact joint-character
multiplicities

\[
\begin{array}{c|rrrrrrrr}
\chi & +++ & ++- & +-+ & +-- & -++ & -+- & --+ & ---\\
\hline
R_{15} & 0 & 1 & 1 & 3 & 1 & 3 & 3 & 3
\end{array}
\]

The six spaces decompose as follows:

\[
\begin{array}{c|rrrrrrrr}
 & +++ & ++- & +-+ & +-- & -++ & -+- & --+ & ---\\
\hline
V_2  &0&0&1&0&0&0&0&1\\
V_8  &0&0&1&1&1&1&2&2\\
V_9  &0&1&1&3&0&1&1&2\\
V_{14}&0&1&1&3&1&2&3&3\\
V_{15}&0&1&1&3&1&3&3&3
\end{array}
\]

The unobserved intersection node

\[
V_3=V_8\cap V_9
\]

has character content

\[
V_3:
\qquad
+-+,\quad +--,\quad ---,
\]

one dimension in each.

This decomposition pinpoints the exact target direction missing from
\(V_{14}\): one line in the \((-+-)\) character sector.

---

## 9. Explanation obtained

After a successful run, the two-rightmost-label law can be stated as:

> The ordered tail of \(A\) selects one node of a fixed exact subspace lattice
> inside the common 15-dimensional eight-point target relation space. The
> smallest element \(a\) changes only source-side relation redundancy; it does
> not change the transported target image.

This is stronger than saying merely that the rank is independent of \(a\).

---

## 10. Claim boundary

03C is an exact finite-dimensional explanation. It does not yet:

- derive the six subspaces from a short closed-form KK identity;
- prove that the ordered-tail filtration is anchor-independent;
- identify a universal representation for general odd-to-even \(n\);
- assign physical meaning to the filtration.

A subsequent theorem programme could seek a general flag/Schubert formulation.

---

## 11. Run command

```bash
caffeinate -i python3 scripts/ehf_amp_found_03c_exact_tail_filtration_lattice.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --rank-script scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --out-dir runs/ehf_amp_found_03c \
  --strict
```

---

## 12. Principal outputs

```text
summary.json
verdict.json
run.log
exact_tail_filtration_certificate.json
exact_transported_channel_images.csv
six_tail_filtration_subspaces.csv
pairwise_subspace_lattice.csv
target_subspace_stabilizers.csv
c2cubed_character_decomposition.csv
exact_subspace_rref_bases.json
```

The target terminal result is:

```text
All 35 exact ranks recovered:         True
Six fixed tail subspaces:             True
Exact lattice certificate:            True
Exact stabilizer orders:              True
Exact C2^3 character certificate:     True
Verdict: EHF_AMP_FOUND_03C_EXACT_TAIL_FILTRATION_SUBSPACE_LAW_PROVED
strict checks:                        PASS
```
