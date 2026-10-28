# Exact Odd-to-Even Tail Filtration of Parke-Taylor Fibre Relations at Nine Points

## A computer-assisted exact theorem with full anchor-deletion covariance

**Barry Fensom**  
Emergent Horizon Framework research note  
**Draft v1.5 - 17 July 2026**

---

## Abstract

We study reflection-aware deletion of label \(9\) from fibre-local Parke-Taylor relation spaces carried by canonical Hamilton-cycle orderings. In the fixed anchor-\(1\) chart, the \(35\) active nine-point parity-position fibres are indexed by triples
\[
A=\{a<b<c\}\subset\{2,\ldots,8\}
\]
and map diagonally to the correspondingly indexed eight-point fibres.

For each source fibre, let \(Q_A\) be its exact Kleiss-Kuijf coordinate matrix and \(D_A\) the exact signed delete-\(9\) incidence map. The transmitted rank is
\[
r_A
=
\operatorname{rank}_{\mathbb Q}
\begin{bmatrix}
Q_A\\D_A
\end{bmatrix}
-
\operatorname{rank}_{\mathbb Q}Q_A.
\]
Exact computation over \(\mathbb Q\) proves that \(r_A\) depends only on the two largest elements \(b,c\), not on \(a\), and takes the six values
\[
0,\ 2,\ 8,\ 9,\ 14,\ 15.
\]

After transporting all target fibres to the reference fibre \(A_0=\{2,3,4\}\), the \(35\) transmitted images collapse to six fixed subspaces
\[
V_0,\ V_2,\ V_8,\ V_9,\ V_{14},\ V_{15}
\]
of the \(15\)-dimensional target relation space. They form the exact lattice
\[
V_2\subset V_8,V_9,
\qquad
\dim(V_8\cap V_9)=3,
\qquad
V_{14}=V_8+V_9,
\qquad
V_{15}=R^{(8)}.
\]
The common subgroup
\[
G=\langle(2\,3),(5\,6),(7\,8)\rangle\cong C_2^3
\]
preserves the lattice.

The lattice has a minimal seven-seed **filtration-adapted** presentation under \(G\): the five successive quotient layers require \(1,1,2,2,1\) orbit seeds. Separating the joint sign characters gives fifteen character-pure quotient directions. Each admits an exact minimum-support expression in primitive signed-orbit atoms
\[
\Omega_\chi(w)
=
\operatorname{prim}
\left(
\sum_{g\in G}\chi(g)e_{\operatorname{can}(g\cdot w)}
\right),
\]
with a total of \(79\) atom occurrences under the direction-by-direction character-pure normal-form convention.

The signed-orbit relations are independently recovered as exact kernels of the direct eight-point KK-shuffle matrices
\[
M_\chi=Q_8A_\chi^{\mathsf T}.
\]
Introducing group-ring variables \(x_i^2=1\), the full \(720\)-coordinate proof factors through \(144\) nonzero universal rows and exactly \(21\) primitive templates over \(\mathbb Z[C_2^3]\), with multiplicities
\[
16^{\times3},\qquad8^{\times6},\qquad4^{\times12}.
\]
Character evaluation of the \(21\)-row operator reproduces the complete direct KK row spaces and kernels.

Every nonzero orbit-polynomial block in the 21-template catalogue factors exactly as a signed monomial translate of a subgroup sum,
\[
p(x)=\varepsilon x^a\sum_{h\in H}x^h
=\varepsilon x^a\prod_{v\in B}(1+x^v),
\qquad H\leq\mathbb F_2^3.
\]
The 54 nonzero blocks have subgroup-rank distribution
\[
0^{\times29},\qquad1^{\times19},\qquad2^{\times5},\qquad3^{\times1},
\]
and the factorisation yields the exact character-selection law \(p(\chi)=0\) unless \(\chi\) is trivial on \(H\).

The residual normalizer has
\[
N/G\cong C_2.
\]
Its nontrivial element sends the endpoint-8 KK chart to endpoint 6. Exact endpoint covariance proves that the apparent fixed-chart nonclosure is resolved by a two-chart atlas: the endpoint catalogues each contain 21 classes, overlap in 8, and have a 34-class union in 18 residual orbits. Extending to the complete order-16 normalizer and all endpoints \(e\in\{5,6,7,8\}\) yields exactly two chart classes,
\[
\mathcal T_7=\mathcal T_8,
\qquad
\mathcal T_5=\mathcal T_6,
\]
and exact cocycle consistency for state maps, KK-row maps, universal group-ring rows, and canonical template classes. The action on the 34-class atlas factors through \(N/G\cong C_2\).



The fixed anchor and deleted leg are subsequently removed as structural restrictions. For every ordered anchor-deletion pair
\[
(a,d),\qquad a\ne d,
\]
the canonical chart normalisation sends \(a\mapsto1\) and \(d\mapsto9\). All \(72\) charts and \(2520\) chart-relative fibre channels reduce to the same six target subspaces. The exact source, target, KK-row, fibre-label, deletion, and relation-image maps are covariant, and all \(72^3=373248\) ordered chart triples satisfy the transition cocycle. Thus anchor \(1\) and deleted label \(9\) are reference coordinates rather than preferred structural data.

The result gives a finite exact explanation of the six-level \(9\to8\) rank law as an ordered-tail filtration of a common target relation module, together with constructive and symmetry-separated presentations. It is conditional only on the standard Kleiss-Kuijf shuffle identity and independence of the KK basis. No claim of physical dynamics, phenomenological utility, or literature novelty is made.

---

## 1. Scope and claim status

This note isolates one exact result in the combinatorial amplitude layer of the Emergent Horizon Framework programme. It concerns:

1. canonical cyclic orderings modulo reflection;
2. parity-position fibres;
3. Parke–Taylor factors and their Kleiss–Kuijf relations;
4. reflection-aware deletion in all ordered anchor-deletion charts;
5. exact finite-dimensional linear algebra over \(\mathbb Q\);
6. a finite permutation-group action on the resulting target relation spaces;
7. exact anchor, deleted-leg, and chart-transition covariance.

The result is a **computer-assisted exact theorem**. It does not rely on floating-point rank decisions, numerical singular-value decomposition, random kinematics, cached numerical relation bases, or rational reconstruction.

Its assumptions are:

- the standard Kleiss–Kuijf shuffle identity;
- independence of the \((n-2)!\) KK basis orderings.

A literature and novelty audit remains pending. The note therefore makes no novelty claim relative to the established amplitudes literature.

---

## 2. Canonical orderings and parity-position fibres

Let
\[
\mathcal C_n
=
\left\{
(1,c_2,\ldots,c_n):
(c_2,\ldots,c_n)\in S_{n-1},\ c_2<c_n
\right\}.
\]
The label \(1\) is anchored, and \(c_2<c_n\) selects one representative from each reversal pair.

For an ordering
\[
c=(c_1,\ldots,c_n)\in\mathcal C_n,
\]
define its odd- and even-position label sets by
\[
E(c)=\{c_1,c_3,c_5,\ldots\},
\qquad
O(c)=\{c_2,c_4,c_6,\ldots\}.
\]

At \(n=9\), let
\[
U=\{2,3,4,5,6,7,8\}.
\]
For every
\[
A\in\binom U3,
\]
define the active source fibre
\[
F_A^{(9)}
=
\left\{
c\in\mathcal C_9:
E(c)=\{1,9\}\cup A,\ 
O(c)=U\setminus A
\right\}.
\]

There are
\[
\binom73=35
\]
such fibres.

The corresponding eight-point target fibre is
\[
F_A^{(8)}
=
\left\{
d\in\mathcal C_8:
E(d)=\{1\}\cup A,\ 
O(d)=U\setminus A
\right\}.
\]

Each target fibre has \(72\) canonical orderings and a \(15\)-dimensional local KK relation space.

---

## 3. Exact diagonal incidence at \(9\to8\)

The reflection-aware delete-\(9\) map acts only when \(9\) is adjacent to the anchor \(1\).

In the standard canonical chart, the maximal label \(9\) cannot occupy the position immediately after \(1\), because the representative condition \(c_2<c_9\) would fail. Thus every active delete-\(9\) state lies on the before-anchor branch.

For every \(A\):

- exactly \(144\) source states are delete-\(9\)-active;
- each of the \(72\) target states has exactly two source preimages;
- deletion preserves the fibre label:
  \[
  F_A^{(9)}\longrightarrow F_A^{(8)};
  \]
- the \(35\) active source fibres reach \(35\) distinct target fibres.

Hence the fixed-anchor combinatorial map is exactly diagonal:
\[
\boxed{
A\longmapsto A.
}
\]

The one-sided branch is a feature of the chosen canonical chart, not an invariant chirality statement.

---

## 4. Exact local relation spaces

For a cyclic ordering \(c=(c_1,\ldots,c_n)\), write
\[
\operatorname{PT}(c)
=
\frac{1}{
\langle c_1c_2\rangle
\langle c_2c_3\rangle
\cdots
\langle c_nc_1\rangle
}.
\]

The reflection identity is
\[
\operatorname{PT}(c^{\mathrm{rev}})
=
(-1)^n\operatorname{PT}(c).
\]

For an ordering written as \((1,\alpha,n,\beta)\), the Kleiss–Kuijf identity is
\[
\operatorname{PT}(1,\alpha,n,\beta)
=
(-1)^{|\beta|}
\sum_{\sigma\in\alpha\shuffle\beta^{\mathrm T}}
\operatorname{PT}(1,\sigma,n).
\]

At \(n=9\), the KK basis has dimension
\[
(9-2)!=5040.
\]

For each active source fibre, let
\[
Q_A:
\mathbb Q^{|F_A^{(9)}|}
\longrightarrow
\mathbb Q^{5040}
\]
be the exact sparse integer matrix whose columns are the KK shuffle expansions of the source orderings.

The exact source-local relation space is
\[
R_A^{(9)}=\ker_{\mathbb Q}Q_A.
\]

Let
\[
D_A:
\mathbb Q^{|F_A^{(9)}|}
\longrightarrow
\mathbb Q^{72}
\]
be the exact signed delete-\(9\) incidence matrix. The transmitted relation image is
\[
I_A=D_A(R_A^{(9)}).
\]

---

## 5. Exact rank identity

### Lemma 5.1

For every active source fibre,
\[
\boxed{
\dim I_A
=
\operatorname{rank}_{\mathbb Q}
\begin{bmatrix}
Q_A\\D_A
\end{bmatrix}
-
\operatorname{rank}_{\mathbb Q}Q_A.
}
\]

### Proof

By rank–nullity,
\[
\dim D_A(\ker Q_A)
=
\dim\ker Q_A
-
\dim(\ker Q_A\cap\ker D_A).
\]
Now
\[
\ker Q_A\cap\ker D_A
=
\ker
\begin{bmatrix}
Q_A\\D_A
\end{bmatrix}.
\]
Therefore
\[
\begin{aligned}
\dim I_A
&=
\left(
|F_A^{(9)}|-\operatorname{rank}Q_A
\right)
-
\left(
|F_A^{(9)}|
-
\operatorname{rank}
\begin{bmatrix}
Q_A\\D_A
\end{bmatrix}
\right)\\
&=
\operatorname{rank}
\begin{bmatrix}
Q_A\\D_A
\end{bmatrix}
-
\operatorname{rank}Q_A.
\end{aligned}
\]
All ranks are over \(\mathbb Q\). \(\square\)

This identity avoids constructing a floating-point or symbolic nullspace basis merely to determine the transmitted rank.

---

## 6. Exact two-rightmost-label rank law

Write
\[
A=\{a<b<c\}.
\]

### Theorem 6.1 — exact rank law

The transmitted rank
\[
r_A=\dim I_A
\]
depends only on \(b,c\) and is independent of \(a\). Explicitly,
\[
\boxed{
r_A=
\begin{cases}
0, & b\le4,\ c\le5,\\[2mm]
2, & b\le4,\ c=6,\\[2mm]
9, & b\le4,\ c\ge7,\\[2mm]
8, & b=5,\ c=6,\\[2mm]
14, & b=5,\ c\ge7,\\[2mm]
15, & b\ge6.
\end{cases}
}
\]

### Exact multiplicities

The six classes contain:

\[
\begin{array}{c|c|c}
\text{condition} & r_A & \text{channel count}\\
\hline
b\le4,\ c\le5 & 0 & 4\\
b\le4,\ c=6 & 2 & 3\\
b=5,\ c=6 & 8 & 3\\
b\le4,\ c\ge7 & 9 & 6\\
b=5,\ c\ge7 & 14 & 6\\
b\ge6 & 15 & 13
\end{array}
\]

Consequently,
\[
0^{\times4},\quad
2^{\times3},\quad
8^{\times3},\quad
9^{\times6},\quad
14^{\times6},\quad
15^{\times13}.
\]

The total transmitted rank is
\[
4(0)+3(2)+3(8)+6(9)+6(14)+13(15)=363.
\]

The complete target-local sector has dimension
\[
35\cdot15=525,
\]
so the total missing dimension is
\[
525-363=162.
\]

Exactly thirteen target fibres are recovered completely.

---

## 7. Gap-coordinate formulation

Define the gap composition
\[
(g_0,g_1,g_2,g_3)
=
(a-2,\ b-a-1,\ c-b-1,\ 8-c).
\]

Then
\[
g_0+g_1=b-3,
\qquad
g_3=8-c.
\]

The rank law is equivalently
\[
\boxed{
r_A=r(g_0+g_1,g_3).
}
\]

It is independent of the internal split
\[
g_0+g_1
\]
between \(g_0\) and \(g_1\). This is the first indication that the smallest selected label contributes only source-side redundancy.

---

## 8. Canonical transport to a common target relation space

The six ranks become structurally meaningful only after comparing the transmitted images themselves.

Choose the reference subset
\[
A_0=\{2,3,4\}.
\]

For each
\[
A=\{a<b<c\},
\]
define the order-preserving block relabelling
\[
\operatorname{sort}(A)\longmapsto(2,3,4),
\]
and
\[
\operatorname{sort}(A^c)\longmapsto(5,6,7,8).
\]

Because the target multiplicity is even,
\[
\operatorname{PT}(d^{\mathrm{rev}})
=
\operatorname{PT}(d)
\qquad(n=8),
\]
so canonicalisation introduces no reflection sign.

This gives an exact coordinate isomorphism
\[
T_A:R_A^{(8)}
\longrightarrow
R_{A_0}^{(8)}.
\]

Define the transported image
\[
\widetilde I_A=T_A(I_A).
\]

---

## 9. Six fixed transmitted subspaces

### Theorem 9.1 — exact tail-filtration subspace law

There exist six fixed subspaces
\[
V_0,\ V_2,\ V_8,\ V_9,\ V_{14},\ V_{15}
\subseteq R_{A_0}^{(8)}
\]
such that
\[
\dim V_d=d
\]
and
\[
\boxed{
\widetilde I_A=
\begin{cases}
V_0, & b\le4,\ c\le5,\\
V_2, & b\le4,\ c=6,\\
V_8, & b=5,\ c=6,\\
V_9, & b\le4,\ c\ge7,\\
V_{14}, & b=5,\ c\ge7,\\
V_{15}, & b\ge6.
\end{cases}
}
\]

Thus, at fixed \(b,c\), changing \(a\) leaves not only the rank but the complete transported image subspace unchanged.

The exact rank law is therefore the dimension shadow of an exact subspace-selection law.

---

## 10. Ordered-tail interpretation

The relevant ordered tails are
\[
\{5,6,7,8\}
\supset
\{6,7,8\}
\supset
\{7,8\}.
\]

The selected elements in this tail determine the activated target subspace:

\[
\begin{array}{c|c|c}
\text{tail occupancy condition} & \text{subspace} & \dim\\
\hline
\text{no selected label at or above }6 & V_0 & 0\\
6\text{ selected, }5\text{ absent} & V_2 & 2\\
\{5,6\}\text{ selected} & V_8 & 8\\
7\text{ or }8\text{ selected, }5\text{ absent} & V_9 & 9\\
5\text{ and one of }\{7,8\}\text{ selected} & V_{14} & 14\\
\text{at least two of }\{6,7,8\}\text{ selected} & V_{15} & 15
\end{array}
\]

This is a finite flag-like or Schubert-like filtration: an ordered label tail selects a node in a fixed target-space lattice. The present theorem does not assert a general Schubert construction, but the analogy records the correct finite structure.

---

## 11. Exact subspace lattice

Define
\[
V_3=V_8\cap V_9.
\]

The exact relations among the six observed spaces are:

\[
V_0=0,
\]
\[
V_2\subset V_8,
\qquad
V_2\subset V_9,
\]
\[
\dim V_3=3,
\qquad
V_2\subset V_3,
\qquad
\dim(V_3/V_2)=1,
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

The lattice is:

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

The six transmitted ranks are therefore dimensions of exact lattice nodes rather than isolated numerical values.

---

## 12. Stabiliser structure

The reference fibre is preserved by
\[
S_{\{2,3,4\}}\times S_{\{5,6,7,8\}}
\cong S_3\times S_4,
\]
of order \(144\).

The exact stabiliser orders of the six spaces inside \(S_3\times S_4\) are:

\[
\begin{array}{c|c|l}
\text{subspace} & \text{stabiliser order} & \text{description}\\
\hline
V_0 & 144 & S_3\times S_4\\
V_2 & 8 & C_2^3\\
V_8 & 24 & S_3\times C_2\times C_2\\
V_9 & 48 & C_2\times S_4\\
V_{14} & 8 & C_2^3\\
V_{15} & 144 & S_3\times S_4
\end{array}
\]

The common subgroup preserving the entire nontrivial lattice is
\[
G
=
\langle
(2\,3),(5\,6),(7\,8)
\rangle
\cong C_2^3.
\]

---

## 13. Exact \(C_2^3\) character decomposition

Let the three signs record eigenvalues under
\[
g_1=(2\,3),
\qquad
g_2=(5\,6),
\qquad
g_3=(7\,8).
\]

The full target relation space \(V_{15}\) decomposes as:

\[
\begin{array}{c|rrrrrrrr}
\chi & +++ & ++- & +-+ & +-- & -++ & -+- & --+ & ---\\
\hline
V_{15} & 0 & 1 & 1 & 3 & 1 & 3 & 3 & 3
\end{array}
\]

The principal subspaces have multiplicities:

\[
\begin{array}{c|rrrrrrrr}
 & +++ & ++- & +-+ & +-- & -++ & -+- & --+ & ---\\
\hline
V_2    &0&0&1&0&0&0&0&1\\
V_8    &0&0&1&1&1&1&2&2\\
V_9    &0&1&1&3&0&1&1&2\\
V_{14} &0&1&1&3&1&2&3&3\\
V_{15} &0&1&1&3&1&3&3&3
\end{array}
\]

The intersection node
\[
V_3=V_8\cap V_9
\]
has character content
\[
+-+,\qquad +--,\qquad ---,
\]
one dimension in each.

The unique quotient direction
\[
V_{15}/V_{14}
\]
lies in the \((-+-)\) sector. Thus the final one-dimensional obstruction to complete recovery is identified representation-theoretically.

---

## 14. Filtration-adapted orbit generators

Let
\[
V_3=V_8\cap V_9.
\]
The independent successive quotient layers are
\[
L_2=V_2/V_0,
\qquad
L_3=V_3/V_2,
\]
\[
L_8=V_8/V_3,
\qquad
L_9=V_9/V_3,
\qquad
L_{15}=V_{15}/V_{14}.
\]
Their dimensions are
\[
2,\quad1,\quad5,\quad6,\quad1,
\]
which sum to \(15\).

Because
\[
G\cong C_2^3
\]
is abelian and all of its irreducible representations over \(\mathbb Q\) are one-dimensional sign characters, a rational \(G\)-module
\[
L=\bigoplus_\chi \mathbb Q^{m_\chi}\otimes\chi
\]
requires exactly
\[
\boxed{\max_\chi m_\chi}
\]
cyclic orbit generators. One seed contributes at most one independent direction to each copy of a fixed character, while \(\max_\chi m_\chi\) generic seeds attain the bound.

For the five layers, the exact character contents and minimum seed counts are
\[
\begin{array}{c|c|c|c}
\text{layer} & \dim & \text{nonzero character multiplicities} & \text{minimum seeds}\\
\hline
L_2 & 2 & (+-+)^1,(---)^1 & 1\\
L_3 & 1 & (+--)^1 & 1\\
L_8 & 5 & (-++)^1,(-+-)^1,(--+)^2,(---)^1 & 2\\
L_9 & 6 & (++-)^1,(+--)^2,(-+-)^1,(--+)^1,(---)^1 & 2\\
L_{15} & 1 & (-+-)^1 & 1
\end{array}
\]

Hence the exact lattice admits a filtration-adapted presentation by
\[
\boxed{1+1+2+2+1=7}
\]
primitive relation seeds and their \(G\)-orbits.

This is a minimal count **subject to respecting the five quotient layers**. It is not the absolute minimum number of unconstrained seeds needed merely to span the full module \(V_{15}\). Since the largest character multiplicity in \(V_{15}\) is \(3\), three sufficiently generic global seeds could span the full module while obscuring the filtration.

The seven-seed result is therefore a constructive presentation of the discovered lattice, not a global cyclic-generator theorem for \(V_{15}\) considered without its filtration.

---

## 15. Signed-orbit normal form

The seven filtration-adapted seeds contain between \(16\) and \(34\) explicit Parke-Taylor terms. To separate symmetry from coefficient data, define for a joint sign character
\[
\chi=(\chi_1,\chi_2,\chi_3)\in\{\pm1\}^3
\]
and a target ordering \(w\),
\[
\boxed{
\Omega_\chi(w)
=
\operatorname{prim}
\left(
\sum_{g\in G}
\chi(g)e_{\operatorname{can}(g\cdot w)}
\right).
}
\]
Here \(e_w\) is the coefficient vector of \(\operatorname{PT}(w)\), repeated canonical states are combined, and `prim` clears denominators, divides by the integer gcd, and fixes the first nonzero coefficient to be positive.

The \(72\) target orderings split into
\[
8\text{ orbits of size }8
\qquad\text{and}\qquad
2\text{ orbits of size }4.
\]
For each character, the nonzero atoms from these state orbits form a basis of the corresponding character-isotypic coefficient space.

Every one of the fifteen quotient-character directions has an exact minimum-support expression
\[
R=\sum_j c_j\Omega_\chi(w_j),
\qquad c_j\in\mathbb Z.
\]
The certified minimum atom-support profiles are
\[
\begin{array}{c|c|c}
\text{layer} & \chi & \text{minimum atom supports}\\
\hline
L_2 & +-+ & 5\\
L_2 & --- & 6\\
L_3 & +-- & 6\\
L_8 & -++ & 3\\
L_8 & -+- & 5\\
L_8 & --+ & 4,5\\
L_8 & --- & 4\\
L_9 & ++- & 5\\
L_9 & +-- & 4,5\\
L_9 & -+- & 8\\
L_9 & --+ & 8\\
L_9 & --- & 6\\
L_{15} & -+- & 5
\end{array}
\]
The two multiplicity-two sectors have the exact lexicographically minimum profile
\[
(4,5),
\]
so neither admits two independent four-atom representatives.

Across the fifteen character-pure directions, the direction-by-direction minimum-support convention uses
\[
\boxed{79}
\]
signed-orbit atom occurrences.

This number is not claimed to be a global minimum under arbitrary mixing of characters or quotient directions. Its meaning is precise: each pure quotient-character direction is individually represented with minimum atom support, and the two-dimensional character quotients use a lexicographically minimum pair of supports.

The signed-orbit form converts a long Parke-Taylor relation into
\[
\text{group action encoded in }\Omega_\chi
\quad+\quad
\text{a short integer relation among orbit atoms}.
\]
It is a symmetry-separated normal form, not yet a closed analytic derivation from a parameterised family of KK shuffle identities.

---

## 16. Direct exact KK-shuffle derivation

Let
\[
Q_8:\mathbb Q^{72}\longrightarrow\mathbb Q^{720}
\]
be the exact eight-point KK coordinate matrix of the reference target fibre, and let \(A_\chi\) be the matrix whose rows are the primitive signed-orbit atoms in character \(\chi\). Define
\[
\boxed{M_\chi=Q_8A_\chi^{\mathsf T}.}
\]
A signed-orbit coefficient row \(c\) is a Parke--Taylor relation exactly when
\[
M_\chi c^{\mathsf T}=0.
\]

An independent exact reconstruction uses only the standard KK shuffle matrices, the nine-to-eight deletion maps, and rational linear algebra. It reads no saved subspace bases or selected seeds from the preceding compression probes. It recovers
\[
\dim\ker Q_8=15,
\]
the complete tail lattice, the fifteen quotient-character directions, all minimum support profiles, and the total atom count \(79\).

The direct character ranks and nullities are
\[
\begin{array}{c|c|c}
\chi & \operatorname{rank}M_\chi & \dim\ker M_\chi\\
\hline
+++ & 10 & 0\\
++- & 7 & 1\\
+-+ & 7 & 1\\
+-- & 7 & 3\\
-++ & 7 & 1\\
-+- & 7 & 3\\
--+ & 7 & 3\\
--- & 5 & 3
\end{array}
\]
Thus the signed-orbit normal forms are intrinsic elements of the exact KK kernel, not artefacts of the seven filtration-adapted seeds or of a particular RREF basis.

---

## 17. Parameterised group-ring shuffle templates

Introduce commuting involutive variables
\[
x_1,x_2,x_3,
\qquad x_i^2=1,
\]
so that
\[
\mathbb Z[C_2^3]\cong
\mathbb Z[x_1,x_2,x_3]/(x_1^2-1,x_2^2-1,x_3^2-1).
\]
Let \(w_1,\ldots,w_{10}\) be representatives of the ten target-state orbits. For a standard eight-point KK basis coordinate \(\sigma\), define
\[
\boxed{
P_{\sigma j}(x)=
\sum_{h\in C_2^3}Q_8[\sigma,h\cdot w_j]x^h.
}
\]
This combines the exact KK shuffle coefficients and all eight character antisymmetrisers into one universal group-ring row
\[
P_\sigma(x)=\bigl(P_{\sigma1}(x),\ldots,P_{\sigma,10}(x)\bigr).
\]

Among the \(720\) KK coordinates, exactly \(144\) universal rows are nonzero. Up to an overall nonzero integer scalar and multiplication by a group monomial \(x^h\), they collapse to exactly
\[
\boxed{21}
\]
primitive templates. Their exact multiplicity distribution is
\[
\boxed{16^{\times3},\qquad8^{\times6},\qquad4^{\times12}.}
\]
Indeed,
\[
3(16)+6(8)+12(4)=144.
\]

For a sign character \(\chi=(\chi_1,\chi_2,\chi_3)\), evaluate \(x_i=\chi_i\) and divide each surviving orbit column by its exact primitive-orbit normalisation. This gives a \(21\)-row matrix \(T_\chi\) satisfying
\[
\boxed{
\operatorname{rowspan}_{\mathbb Q}T_\chi
=
\operatorname{rowspan}_{\mathbb Q}M_\chi,
}
\]
and therefore
\[
\boxed{\ker_{\mathbb Q}T_\chi=\ker_{\mathbb Q}M_\chi.}
\]
Every one of the fifteen minimum-support quotient-character relations satisfies all \(21\) specialised template equations exactly.

The direct proof compression is therefore
\[
720\longrightarrow144\longrightarrow21.
\]
This is an exact finite parameterised shuffle--antisymmetriser theorem. The list of \(21\) templates has not yet been replaced by one shorter combinatorial family.

---

## 18. Affine subgroup factors and fixed-chart normalizer obstruction

Every nonzero orbit-polynomial block in the 21 templates is an affine subgroup sum in the group ring. Explicitly,
\[
\boxed{
p(x)=\varepsilon x^a\sum_{h\in H}x^h
=\varepsilon x^a\prod_{v\in B}(1+x^v),
}
\]
where \(H\leq\mathbb F_2^3\), \(B\) is any basis of \(H\), \(a\in\mathbb F_2^3\), and \(\varepsilon\in\{\pm1\}\).

The catalogue contains 54 nonzero orbit-polynomial blocks. Their exact subgroup-rank distribution is
\[
\boxed{
0^{\times29},\qquad
1^{\times19},\qquad
2^{\times5},\qquad
3^{\times1}.
}
\]
The 21 templates have seven coarse factor-rank profiles:
\[
\begin{array}{c|c|c}
\text{profile}&\text{sorted nonzero block ranks}&\text{count}\\
\hline
F_1&(3)&1\\
F_2&(2)&3\\
F_3&(1,2)&2\\
F_4&(1,1)&6\\
F_5&(0,0,1)&2\\
F_6&(0,0,0,1)&3\\
F_7&(0,0,0,0)&4
\end{array}
\]

For a sign character \(\chi\), the factorisation gives
\[
\boxed{
p(\chi)=0\quad\text{unless}\quad\chi|_H=1,
}
\]
and, when \(\chi\) is trivial on \(H\),
\[
\boxed{
p(\chi)=\varepsilon\,\chi(a)\,|H|.
}
\]
Thus the character activation and annihilation pattern is explained exactly by the subgroup factors \(1+x^v\).

Inside the target-fibre stabilizer
\[
S_3\times S_4,
\qquad |S_3\times S_4|=144,
\]
the normalizer of
\[
G=\langle(2\,3),(5\,6),(7\,8)\rangle
\]
has order 16. Hence
\[
\boxed{N/G\cong C_2.}
\]
A representative of the nontrivial residual action is
\[
\tau=(5\,7)(6\,8),
\]
which acts on the group-ring variables by
\[
x_1\mapsto x_1,
\qquad
x_2\leftrightarrow x_3.
\]

The fixed endpoint-8 template catalogue is not closed under \(\tau\): eight classes remain inside and thirteen leave. Its residual closure contains 34 classes arranged in 18 residual orbits. This is a coordinate-chart obstruction, because \(\tau\) sends endpoint 8 to endpoint 6. It is not evidence of physical symmetry breaking.

---

## 19. Exact KK-endpoint covariance and two-chart closure

Let \(Q^{(e)}\) denote the exact eight-point KK matrix in endpoint chart \(e\). For
\[
\tau=(5\,7)(6\,8),
\qquad \tau(8)=6,
\]
there are exact state and KK-row permutation matrices \(P_\tau\) and \(R_\tau\) satisfying
\[
\boxed{
Q^{(6)}P_\tau=R_\tau Q^{(8)}.
}
\]
Consequently,
\[
\dim\ker Q^{(8)}=\dim\ker Q^{(6)}=15,
\]
\[
\ker Q^{(8)}=\ker Q^{(6)}
\]
as subspaces of the common target-state coordinate space, and
\[
\boxed{
P_\tau\bigl(\ker Q^{(8)}\bigr)=\ker Q^{(6)}.
}
\]

The raw universal group-ring rows obey
\[
\boxed{
\tau\!\left(P^{(8)}_\sigma(x)\right)
=P^{(6)}_{\tau(\sigma)}(x).
}
\]
The independently reconstructed endpoint catalogues satisfy
\[
|\mathcal T_8|=|\mathcal T_6|=21,
\]
\[
|\mathcal T_8\cap\mathcal T_6|=8,
\]
\[
|\mathcal T_8\setminus\mathcal T_6|
=|\mathcal T_6\setminus\mathcal T_8|=13,
\]
and
\[
\boxed{
|\mathcal T_8\cup\mathcal T_6|=34.
}
\]
Moreover,
\[
\boxed{
\tau(\mathcal T_8)=\mathcal T_6.
}
\]
Thus the thirteen classes that leave the endpoint-8 chart are exactly the thirteen endpoint-6-only classes. The 34-class closure is a covariant two-chart atlas rather than unexplained catalogue growth.

---

## 20. Full normalizer endpoint atlas and cocycle consistency

For every normalizer element
\[
n\in N,
\qquad |N|=16,
\]
and every endpoint
\[
e\in\{5,6,7,8\},
\]
there are exact state and KK-row maps \(P_n\) and \(R_{n,e}\) satisfying
\[
\boxed{
Q^{(n(e))}P_n=R_{n,e}Q^{(e)}.
}
\]
All 64 endpoint-labelled coordinate identities and kernel covariances hold exactly.

For every \(m,n\in N\), the transition maps satisfy the cocycle laws
\[
\boxed{P_{mn}=P_mP_n,}
\]
and
\[
\boxed{
R_{mn,e}=R_{m,n(e)}R_{n,e}.
}
\]
The same composition law holds for the raw universal group-ring rows and for the canonical primitive template classes. This audits all
\[
16^2\cdot4=1024
\]
endpoint-labelled composition diagrams.

The four endpoint catalogues reduce to exactly two chart classes:
\[
\boxed{
\mathcal T_7=\mathcal T_8,
\qquad
\mathcal T_5=\mathcal T_6.
}
\]
Each chart contains 21 templates. Their overlap is 8, and their union contains 34 classes. No element of the full normalizer generates a class outside this union.

The action on canonical template classes factors through
\[
\boxed{N/G\cong C_2.}
\]
The 34 classes decompose into
\[
\boxed{
2\text{ fixed classes}+16\text{ two-cycles},
}
\]
hence 18 quotient-atlas orbits. The endpoint atlas is therefore closed and cocycle-consistent under the complete normalizer.

---

## 21. All-anchor covariance with fixed deleted leg

Fix deleted leg 9 and let the surviving anchor be
\[
a\in\{1,\ldots,8\}.
\]
Define the canonical anchor normalisation \(\rho_a\) by
\[
\rho_a(a)=1,
\qquad
\rho_a(9)=9,
\]
with all remaining labels sent increasingly to \(2,\ldots,8\).
For every anchor-relative fibre \(A\), exact signed source transport \(P_a\), target transport \(T_a\), and KK-row relabelling \(R_a\) satisfy
\[
\boxed{
Q^{(1)}_{\rho_a(A)}P_a=R_aQ_A^{(a)},
}
\]
and
\[
\boxed{
D^{(1)}_{\rho_a(A)}P_a=T_aD_A^{(a)}.
}
\]
The source transport includes the odd-point reflection character; the even-point target transport is unsigned.

Each of the eight anchor charts contains 35 channels and 5040 active source incidences. The complete fixed-delete-9 anchor atlas therefore contains
\[
8\cdot35=280
\]
channels and
\[
8\cdot5040=40320
\]
active incidences. Every chart has the rank distribution
\[
0^{\times4},\quad2^{\times3},\quad8^{\times3},\quad9^{\times6},\quad14^{\times6},\quad15^{\times13}.
\]
After anchor normalisation and ordered-block target transport, all 280 images select the same six spaces
\[
\boxed{V_0,V_2,V_8,V_9,V_{14},V_{15}.}
\]

For anchors \(a,b\), let
\[
\pi_{b\leftarrow a}=\rho_b^{-1}\rho_a.
\]
All \(8^3=512\) ordered anchor triples obey
\[
\boxed{
\pi_{c\leftarrow b}\pi_{b\leftarrow a}=\pi_{c\leftarrow a},
}
\]
with exact induced cocycles on signed source states, target states, KK rows, fibre labels, and transmitted images.

---

## 22. Full anchor-deletion atlas

A general chart is an ordered pair
\[
(a,d),\qquad a\ne d,
\]
where \(a\) is the surviving anchor and \(d\) is the deleted leg. Define
\[
\rho_{a,d}(a)=1,
\qquad
\rho_{a,d}(d)=9,
\]
with the remaining seven labels sent increasingly to \(2,\ldots,8\). The chart orientation is the pullback of the reference \((1,9)\) orientation.

For every chart and local selected triple \(A\), the exact covariance identities are
\[
\boxed{
Q^{(1,9)}_{\rho_{a,d}(A)}P_{a,d}
=R_{a,d}Q_A^{(a,d)},
}
\]
and
\[
\boxed{
D^{(1,9)}_{\rho_{a,d}(A)}P_{a,d}
=T_{a,d}D_A^{(a,d)}.
}
\]
There are
\[
9\cdot8=72
\]
anchor-deletion charts and
\[
72\cdot35=2520
\]
chart-relative channels. The complete atlas has
\[
2520\cdot144=362880=9!
\]
active source incidences. This equality is a combinatorial census identity, not a physical interpretation.

Every chart has the same six-level rank distribution. Across the full atlas the chart-counted multiplicities are
\[
0^{\times288},\quad
2^{\times216},\quad
8^{\times216},\quad
9^{\times432},\quad
14^{\times432},\quad
15^{\times936}.
\]
After chart normalisation, all 2520 images again collapse to
\[
\boxed{V_0,V_2,V_8,V_9,V_{14},V_{15}.}
\]
The invariant form of the tail law is therefore chart-relative: after sending the anchor to 1, the deleted leg to 9, and the remaining labels to ordered coordinates, the two largest entries of the selected triple determine the transmitted subspace.

For charts \(C=(a,d)\) and \(C'=(b,e)\), define
\[
\pi_{C'\leftarrow C}=\rho_{b,e}^{-1}\rho_{a,d}.
\]
All
\[
72^3=373248
\]
ordered chart triples satisfy
\[
\boxed{
\pi_{C_3\leftarrow C_2}\pi_{C_2\leftarrow C_1}
=\pi_{C_3\leftarrow C_1}.
}
\]
The induced source-state, target-state, KK-row, fibre-label, and relation-image cocycles are exact.

---

## 23. Why the smallest label is invisible

At fixed \(b,c\), changing \(a\) can alter:

- the source fibre size;
- the exact source relation dimension;
- the dimension of the source kernel under deletion.

For example, the channels
\[
A=\{a,6,7\},
\qquad
a=2,3,4,5,
\]
all transmit the complete \(15\)-dimensional target relation space, while their exact source relation dimensions are
\[
40,\ 40,\ 59,\ 90.
\]

The source contains increasingly many relation directions, but deletion projects all of them onto the same target subspace
\[
V_{15}.
\]

Hence the smallest label changes the amount of source-side redundancy but does not activate a new target direction. The rightmost two labels determine which part of the target relation module is accessible.

---

## 24. Comparison with the even-to-odd \(8\to7\) theorem

The adjacent transitions exhibit sharply different channel architectures.

At \(8\to7\):

\[
20\text{ active fibres}
\longrightarrow
10\text{ complementary two-fibre channels},
\]
and every channel has the same rank \(11\) and the same exact spectrum
\[
1^{\times2},
\quad
(6/5)^{\times4},
\quad
(8/5)^{\times4},
\quad
(9/5)^{\times1}.
\]

At \(9\to8\):

\[
35\text{ active fibres}
\longrightarrow
35\text{ diagonal single-fibre channels},
\]
whose transported images select six nodes of a common target-space lattice.

Thus:

\[
\boxed{
8\to7:
\text{ uniform complementary gluing},
}
\]

whereas

\[
\boxed{
9\to8:
\text{ nonuniform diagonal tail filtration}.
}
\]

This finite parity contrast is exact. A general parity-alternating theorem for arbitrary multiplicity has not yet been proved.

---

## 25. Mathematical and physical significance

The immediate result is mathematical:

> Nine-to-eight factorisation organises fibre-local KK relations by an exact ordered-tail filtration of the fifteen-dimensional target relation module, covariantly across the complete anchor-deletion atlas.

Possible relevance to amplitude theory includes:

- factorisation-adapted bases for relation spaces;
- prediction of transmitted rank without constructing a full numerical nullspace;
- block-sparse organisation of symbolic residue calculations;
- a new finite permutation-module filtration to compare with standard KK, BCJ, CHY, or positive-geometry structures.

No practical gain has yet been demonstrated. The theorem currently does not:

- improve a phenomenological amplitude computation;
- calculate a cross section;
- provide a new physical observable;
- identify a gauge group or particle spectrum;
- establish a physical time evolution.

Its potential value to physicists is structural and computational, not yet phenomenological.

---

## 26. Exact theorem statement

> **Exact odd-to-even tail-filtration theorem at nine points, with full chart covariance.**  
> Assume the standard Kleiss-Kuijf shuffle identity and independence of the KK basis. In the reference anchor-1, delete-9 canonical chart, the 35 reflection-aware delete-9 channels map the nine-point fibre \(F_A^{(9)}\) diagonally into the eight-point fibre \(F_A^{(8)}\). For \(A=\{a<b<c\}\), the exact transmitted rank is a function only of \(b,c\), with values \(0,2,8,9,14,15\). After canonical ordered-block transport to the reference target fibre \(A_0=\{2,3,4\}\), all 35 images collapse to six fixed subspaces \(V_0,V_2,V_8,V_9,V_{14},V_{15}\), satisfying
> \[
> V_2\subset V_8,V_9,
> \qquad
> \dim(V_8\cap V_9)=3,
> \qquad
> V_{14}=V_8+V_9,
> \qquad
> V_{15}=R_{A_0}^{(8)}.
> \]
> The lattice is preserved by \(G=C_2^3=\langle(2\,3),(5\,6),(7\,8)\rangle\). Its five successive quotient layers have dimensions \(2,1,5,6,1\), character-theoretic minimum orbit-seed counts \(1,1,2,2,1\), and hence a minimal seven-seed filtration-adapted presentation. Separating the joint characters gives fifteen pure quotient directions, each possessing an exact minimum-support signed-orbit normal form; the complete direction-by-direction normal form uses 79 signed-orbit atom occurrences. These relations are independently the exact kernels of \(M_\chi=Q_8A_\chi^{\mathsf T}\). The complete 720-coordinate KK proof factors through 144 nonzero universal rows and exactly 21 primitive rows over \(\mathbb Z[C_2^3]\); character specialisation reproduces the exact row space and kernel of every \(M_\chi\). Every nonzero orbit-polynomial block is a signed affine subgroup sum \(\varepsilon x^a\sum_{h\in H}x^h\), giving the exact character-selection law \(p(\chi)=0\) unless \(\chi|_H=1\). The residual normalizer has \(N/G\cong C_2\). Its apparent failure to preserve one fixed KK endpoint chart is resolved by an exact full-normalizer endpoint atlas: \(\mathcal T_7=\mathcal T_8\), \(\mathcal T_5=\mathcal T_6\), the two charts overlap in 8 classes, their union contains 34 classes in 18 quotient orbits, and all state, KK-row, group-ring, and template transition maps obey exact cocycle consistency. Finally, the construction extends covariantly to all 72 ordered anchor-deletion charts: their 2520 chart-relative channels reduce to the same six subspaces, and all source, target, KK-row, fibre, deletion, relation-image, and chart-transition cocycles are exact.

---

## 27. Proof architecture

The theorem package is certified through the following exact steps:

1. Enumerate the 35 active fibres \(F_A^{(9)}\).
2. Construct the exact signed delete-9 incidence map \(D_A\).
3. Verify the exact diagonal target \(F_A^{(8)}\), with 144 active source states and two preimages per target state.
4. Construct the sparse integer KK matrix \(Q_A\).
5. Compute the exact transmitted ranks from the stacked-matrix identity.
6. Verify the six-cell two-rightmost-label law.
7. Construct \(I_A=D_A(\ker Q_A)\) over \(\mathbb Q\).
8. Transport every image to the common reference target fibre and prove the six-space collapse.
9. Compute all sums, intersections, stabilizers, and the exact \(C_2^3\) character decomposition.
10. Form the five successive quotient layers and prove the minimal seven-seed filtration-adapted presentation.
11. Construct primitive signed-orbit atoms and certify the minimum support of every quotient-character direction.
12. Reconstruct the target relation space and the complete tail lattice independently from the exact KK and deletion matrices.
13. Form \(M_\chi=Q_8A_\chi^{\mathsf T}\) and prove every normal form directly in the exact KK kernel.
14. Construct the universal group-ring rows and reduce the 144 nonzero rows to 21 primitive scalar/monomial classes.
15. Prove exact row-space and kernel equality between every specialised 21-row operator and the corresponding direct matrix \(M_\chi\).
16. Factor all 54 nonzero orbit-polynomial blocks as signed affine subgroup sums and prove the character-evaluation law.
17. Compute the normalizer of \(G\) inside \(S_3\times S_4\), obtaining \(|N|=16\) and \(N/G\cong C_2\).
18. Audit the fixed endpoint-8 catalogue under the residual involution, obtaining 8 internal classes, 13 external classes, and a 34-class closure.
19. Construct the endpoint-6 chart and prove \(Q^{(6)}P_\tau=R_\tau Q^{(8)}\), kernel covariance, raw universal-row covariance, and \(\tau(\mathcal T_8)=\mathcal T_6\).
20. Enumerate all 16 normalizer elements and all endpoints \(e\in\{5,6,7,8\}\), proving all 64 coordinate and kernel covariance identities.
21. Verify the state, KK-row, group-ring, and canonical-template cocycles across all 1024 endpoint-labelled compositions.
22. Prove that the four endpoint catalogues reduce to two chart classes with a closed 34-class union and that the canonical action factors through \(N/G\cong C_2\).
23. Construct all eight fixed-delete-9 anchor charts, prove exact KK and deletion covariance, and verify all 512 anchor-transition cocycles.
24. Construct all 72 ordered anchor-deletion charts, prove the 2520-channel six-space collapse, and verify all 373248 chart-transition cocycles.

All linear-algebraic identities are exact over \(\mathbb Q\).

---

## 28. Reproducibility

The exact theorem package is generated by probes 03A through 03J. The later exact stages are run as follows.

### 28.1 Exact rank and subspace lattice

```bash
caffeinate -i python3 scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --census-csv runs/ehf_amp_found_03a/diagonal_channel_census.csv \
  --out-dir runs/ehf_amp_found_03b \
  --strict

caffeinate -i python3 scripts/ehf_amp_found_03c_exact_tail_filtration_lattice.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --rank-script scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --out-dir runs/ehf_amp_found_03c \
  --strict
```

### 28.2 Orbit generators and signed-orbit normal forms

```bash
caffeinate -i python3 scripts/ehf_amp_found_03d_exact_quotient_orbit_generators.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --subspace-bases-json runs/ehf_amp_found_03c/exact_subspace_rref_bases.json \
  --out-dir runs/ehf_amp_found_03d \
  --strict

caffeinate -i python3 scripts/ehf_amp_found_03e_exact_signed_orbit_normal_form.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --seed-coefficients runs/ehf_amp_found_03d/sparse_seed_coefficients.csv \
  --out-dir runs/ehf_amp_found_03e \
  --strict
```

### 28.3 Direct KK and group-ring compression

```bash
caffeinate -i python3 scripts/ehf_amp_found_03f_direct_kk_shuffle_signed_orbit_derivation.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --rank-script scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --normal-form-script scripts/ehf_amp_found_03e_exact_signed_orbit_normal_form.py \
  --out-dir runs/ehf_amp_found_03f \
  --strict

caffeinate -i python3 scripts/ehf_amp_found_03g_parameterised_shuffle_antisymmetriser_templates.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --rank-script scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --normal-form-script scripts/ehf_amp_found_03e_exact_signed_orbit_normal_form.py \
  --derivation-script scripts/ehf_amp_found_03f_direct_kk_shuffle_signed_orbit_derivation.py \
  --out-dir runs/ehf_amp_found_03g \
  --strict
```

### 28.4 Factor theorem and endpoint atlas

```bash
caffeinate -i python3 scripts/ehf_amp_found_03h_group_ring_factor_normalizer_audit.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --template-catalog runs/ehf_amp_found_03g/universal_shuffle_template_catalog.csv \
  --template-polynomials runs/ehf_amp_found_03g/universal_shuffle_template_polynomials.csv \
  --out-dir runs/ehf_amp_found_03h \
  --strict

caffeinate -i python3 scripts/ehf_amp_found_03i_kk_endpoint_covariance_normalizer_closure.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --normal-form-script scripts/ehf_amp_found_03e_exact_signed_orbit_normal_form.py \
  --template-script scripts/ehf_amp_found_03g_parameterised_shuffle_antisymmetriser_templates.py \
  --normalizer-script scripts/ehf_amp_found_03h_group_ring_factor_normalizer_audit.py \
  --out-dir runs/ehf_amp_found_03i \
  --strict

caffeinate -i python3 scripts/ehf_amp_found_03j_full_normalizer_endpoint_atlas_cocycle.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --normal-form-script scripts/ehf_amp_found_03e_exact_signed_orbit_normal_form.py \
  --template-script scripts/ehf_amp_found_03g_parameterised_shuffle_antisymmetriser_templates.py \
  --normalizer-script scripts/ehf_amp_found_03h_group_ring_factor_normalizer_audit.py \
  --endpoint-script scripts/ehf_amp_found_03i_kk_endpoint_covariance_normalizer_closure.py \
  --out-dir runs/ehf_amp_found_03j \
  --strict
```



### 28.5 Anchor and deleted-leg covariance

```bash
caffeinate -i python3 scripts/ehf_amp_found_03k_anchor_change_covariance_full_fibre_atlas.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --rank-script scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --lattice-script scripts/ehf_amp_found_03c_exact_tail_filtration_lattice.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --out-dir runs/ehf_amp_found_03k \
  --strict

caffeinate -i python3 scripts/ehf_amp_found_03l_deleted_leg_covariance_full_anchor_deletion_atlas.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --rank-script scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --lattice-script scripts/ehf_amp_found_03c_exact_tail_filtration_lattice.py \
  --direct-script scripts/ehf_amp_found_02g_direct_exact_kk_channel_derivation.py \
  --anchor-script scripts/ehf_amp_found_03k_anchor_change_covariance_full_fibre_atlas.py \
  --out-dir runs/ehf_amp_found_03l \
  --strict
```

The required late-stage verdicts are:

```text
03F: direct KK-shuffle signed-orbit derivation proved
03G: exact 21-template group-ring derivation proved
03H: affine subgroup factor theorem and fixed-chart normalizer obstruction proved
03I: exact two-chart KK-endpoint covariance proved
03J: exact full-normalizer endpoint atlas and cocycle proved
03K: exact all-anchor fibre-atlas covariance proved
03L: exact full anchor-deletion atlas covariance proved
```

---

## 29. Claim boundary and next questions

The exact theorem package is restricted to:

- the nine-to-eight transition;
- the chosen parity-position fibre atlas;
- the exact relation-image construction \(D_A(\ker Q_A)\);
- the pullback chart-orientation convention;
- the stated filtration-adapted and character-pure compression conventions.

It is no longer restricted to one anchor or one deleted leg. Within its stated scope it establishes:

- the exact six-level rank and six-subspace tail-filtration law;
- constructive, character-pure, direct-KK, and group-ring presentations;
- the affine-subgroup factor theorem;
- a closed full-normalizer endpoint atlas;
- exact covariance across all eight surviving anchors for each deleted leg;
- a closed 72-chart anchor-deletion atlas with 2520 channels;
- exact cocycle consistency across all chart transitions.

It does not yet establish:

- a general odd-to-even theorem for \(11\to10\), \(13\to12\), and beyond;
- one closed combinatorial formula replacing the 21 finite templates;
- independence from the chosen ordered coordinate normalisation;
- a demonstrated speed-up in a standard amplitude workflow;
- phenomenological utility.

The completed nine-point package motivates EHF-AMP-FOUND-04A, an eleven-to-ten discovery census. That probe should work in one canonical chart, use the proven covariance to avoid redundant anchor-deletion repetitions, and test whether the transmitted rank depends on a bounded ordered tail of a selected four-subset.

---

## Appendix A. Six-cell rank law

\[
\begin{array}{c|c|c|c}
\text{class} & \text{condition} & \dim\widetilde I_A & \text{count}\\
\hline
V_0 & b\le4,\ c\le5 & 0 & 4\\
V_2 & b\le4,\ c=6 & 2 & 3\\
V_8 & b=5,\ c=6 & 8 & 3\\
V_9 & b\le4,\ c\ge7 & 9 & 6\\
V_{14} & b=5,\ c\ge7 & 14 & 6\\
V_{15} & b\ge6 & 15 & 13
\end{array}
\]

---

## Appendix B. Exact character multiplicities

\[
\begin{array}{c|rrrrrrrr}
 & +++ & ++- & +-+ & +-- & -++ & -+- & --+ & ---\\
\hline
V_2    &0&0&1&0&0&0&0&1\\
V_3    &0&0&1&1&0&0&0&1\\
V_8    &0&0&1&1&1&1&2&2\\
V_9    &0&1&1&3&0&1&1&2\\
V_{14} &0&1&1&3&1&2&3&3\\
V_{15} &0&1&1&3&1&3&3&3
\end{array}
\]

---

## Appendix C. Exact quotient layers and seed minima

\[
\begin{array}{c|c|c|c}
\text{layer} & \text{quotient} & \dim & \text{minimum orbit seeds}\\
\hline
L_2 & V_2/V_0 & 2 & 1\\
L_3 & V_3/V_2 & 1 & 1\\
L_8 & V_8/V_3 & 5 & 2\\
L_9 & V_9/V_3 & 6 & 2\\
L_{15} & V_{15}/V_{14} & 1 & 1
\end{array}
\]

The total filtration-adapted count is seven.

---

## Appendix D. Minimum signed-orbit support profiles

\[
\begin{array}{c|c|c}
\text{layer} & \chi & \text{minimum atom supports}\\
\hline
L_2 & +-+ & 5\\
L_2 & --- & 6\\
L_3 & +-- & 6\\
L_8 & -++ & 3\\
L_8 & -+- & 5\\
L_8 & --+ & 4,5\\
L_8 & --- & 4\\
L_9 & ++- & 5\\
L_9 & +-- & 4,5\\
L_9 & -+- & 8\\
L_9 & --+ & 8\\
L_9 & --- & 6\\
L_{15} & -+- & 5
\end{array}
\]

The direction-by-direction total is \(79\) atom occurrences.

---

## Appendix E. Direct KK and group-ring compression

For the eight sign characters, the exact direct KK ranks and relation nullities are
\[
\begin{array}{c|rrrrrrrr}
\chi & +++ & ++- & +-+ & +-- & -++ & -+- & --+ & ---\\
\hline
\operatorname{rank}M_\chi & 10&7&7&7&7&7&7&5\\
\dim\ker M_\chi &0&1&1&3&1&3&3&3
\end{array}
\]

The universal group-ring census is
\[
720\text{ KK rows}\longrightarrow144\text{ nonzero universal rows}\longrightarrow21\text{ primitive templates},
\]
with multiplicities
\[
16^{\times3},\qquad8^{\times6},\qquad4^{\times12}.
\]

---

## Appendix F. Affine subgroup factors

Every nonzero template block is of the form
\[
p(x)=\varepsilon x^a\sum_{h\in H}x^h,
\qquad H\leq\mathbb F_2^3.
\]
The exact block-rank census is
\[
0^{\times29},\quad1^{\times19},\quad2^{\times5},\quad3^{\times1}.
\]
The seven sorted factor-rank profiles have template counts
\[
(3):1,
\quad(2):3,
\quad(1,2):2,
\quad(1,1):6,
\quad(0,0,1):2,
\quad(0,0,0,1):3,
\quad(0,0,0,0):4.
\]

---

## Appendix G. Full normalizer endpoint atlas

The exact group orders are
\[
|S_3\times S_4|=144,
\qquad |G|=8,
\qquad |N|=16,
\qquad N/G\cong C_2.
\]
The endpoint catalogues satisfy
\[
\mathcal T_7=\mathcal T_8,
\qquad
\mathcal T_5=\mathcal T_6.
\]
For the two distinct chart classes,
\[
|\mathcal T_{78}|=|\mathcal T_{56}|=21,
\]
\[
|\mathcal T_{78}\cap\mathcal T_{56}|=8,
\]
and
\[
|\mathcal T_{78}\cup\mathcal T_{56}|=34.
\]
The quotient action has orbit-size distribution
\[
1^{\times2},\qquad2^{\times16},
\]
so the atlas contains 18 quotient orbits.

---

## Appendix H. All-anchor covariance census

With deleted leg 9 fixed, the eight anchor charts contain
\[
8\cdot35=280
\]
channels. The full chart-counted rank distribution is
\[
0^{\times32},\quad2^{\times24},\quad8^{\times24},\quad9^{\times48},\quad14^{\times48},\quad15^{\times104}.
\]
All charts reduce to the same six transported subspaces.

---

## Appendix I. Full anchor-deletion atlas

The complete atlas contains
\[
72\text{ charts},\qquad2520\text{ channels},\qquad362880\text{ active incidences}.
\]
Its chart-counted rank distribution is
\[
0^{\times288},\quad2^{\times216},\quad8^{\times216},\quad9^{\times432},\quad14^{\times432},\quad15^{\times936}.
\]
All \(72^3=373248\) chart-transition cocycles are exact.

---

## Appendix J. Machine-checkable certificates

The principal exact certificates are:

```text
runs/ehf_amp_found_03b/exact_rank_law_certificate.json
runs/ehf_amp_found_03c/exact_tail_filtration_certificate.json
runs/ehf_amp_found_03c/exact_subspace_rref_bases.json
runs/ehf_amp_found_03d/exact_orbit_generator_certificate.json
runs/ehf_amp_found_03e/exact_signed_orbit_normal_form_certificate.json
runs/ehf_amp_found_03f/direct_kk_shuffle_certificate.json
runs/ehf_amp_found_03g/exact_parameterised_shuffle_template_certificate.json
runs/ehf_amp_found_03h/exact_factor_normalizer_certificate.json
runs/ehf_amp_found_03i/exact_kk_endpoint_covariance_certificate.json
runs/ehf_amp_found_03j/exact_full_normalizer_endpoint_atlas_certificate.json
runs/ehf_amp_found_03k/exact_anchor_covariance_certificate.json
runs/ehf_amp_found_03l/exact_anchor_deletion_covariance_certificate.json
```

A conventional bibliography should be added only after the amplitudes-literature and novelty audit.
