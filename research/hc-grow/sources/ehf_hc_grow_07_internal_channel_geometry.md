# EHF-HC-GROW-07 — Reversal-Support Intrinsic Channel Geometry Audit

**Branch:** EHF-HC-GROW  
**Inputs:** EHF-HC Foundation v1.0; GROW-01 through GROW-06  
**Status:** Exact fixed-layer channel definition + exact small/medium HC geometry + finite-exact positional-group classification  
**Decision role:** Determine whether GROW-08 cross-channel geometry is warranted.

---

# 1. Question

GROW-05 and GROW-06 showed that many support-channel laws are universal:

\[
LR_{\ell-1}\to LR_\ell\to LR_{\ell+1},
\]

generic class density:

\[
2/(N-3),
\]

renewal exponent:

\[
\ell,
\]

lineage exponent:

\[
\ell+1.
\]

That raised the possibility that different support values were merely different labels on otherwise equivalent internal graph geometries.

GROW-07 tests that possibility directly.

For each fixed layer and support define:

\[
\boxed{
G_{n,\ell}
=
(HC_n,LR_\ell).
}
\]

This is the single-channel graph whose vertices are HC states and whose edges are exactly support-\(\ell\) reversals.

The central question is:

\[
\boxed{
G_{n,2},G_{n,3},G_{n,4},\ldots
\text{ — genuinely different geometries, or one universal geometry?}
}
\]

The answer is:

\[
\boxed{
\textbf{genuinely different geometries occur.}
}
\]

---

# 2. Exact universal facts

Every \(G_{n,\ell}\) is vertex-transitive under simultaneous relabelling of atom labels.

Its degree is:

\[
\boxed{
\deg G_{n,\ell}=n
}
\]

for generic support:

\[
\ell<n/2,
\]

and:

\[
\boxed{
\deg G_{n,n/2}=n/2
}
\]

for the even half-cycle class.

All channels lie in the same raw comparison shell:

\[
\boxed{
d_E=2.
}
\]

Therefore any channel-specific internal geometry is invisible to raw overlap distance alone.

---

# 3. Positional generator subgroup

Fix a reference cyclic ordering.

Let:

\[
r_{s,\ell}
\]

be the permutation of cyclic positions induced by reversing the length-\(\ell\) block beginning at position \(s\).

Define:

\[
\boxed{
H_{n,\ell}
=
\langle
r_{s,\ell}:s\in\mathbb Z_n
\rangle
\le S_n.
}
\]

The HC state space is a dihedral quotient.

For the component containing the reference state:

\[
\boxed{
|C_{n,\ell}|
=
\frac{
|H_{n,\ell}|
}{
|H_{n,\ell}\cap D_n|
}.
}
\]

Hence:

\[
\boxed{
\#\operatorname{Comp}(G_{n,\ell})
=
|HC_n|
\frac{
|H_{n,\ell}\cap D_n|
}{
|H_{n,\ell}|
}.
}
\]

This gives a computationally cheap exact component census without enumerating all HC states.

---

# 4. Reversal permutation parity

A length-\(\ell\) reversal has permutation sign:

\[
\boxed{
(-1)^{\ell(\ell-1)/2}.
}
\]

Thus:

\[
\ell\equiv2,3\pmod4
\]

gives an odd positional permutation, while:

\[
\ell\equiv0,1\pmod4
\]

gives an even positional permutation.

This mod-4 distinction turns out to matter for internal channel connectivity.

---

# 5. Finite-exact positional-group classification

The subgroup family was computed exactly for every available support over:

\[
5\le n\le16.
\]

The observed classification is:

## Outside the even-\(n\), odd-support case

When either \(n\) is odd or \(\ell\) is even:

\[
H_{n,\ell}
=
\begin{cases}
S_n,&\ell\equiv2,3\pmod4,\\
A_n,&\ell\equiv0,1\pmod4.
\end{cases}
\]

## Even \(n=2m\), odd \(\ell\)

Odd support preserves the parity classes of cyclic positions.

The observed group is:

\[
H_{2m,\ell}
=
S_m\times S_m
\]

for:

\[
\ell\equiv3\pmod4,
\]

and:

\[
H_{2m,\ell}
=
(S_m\times S_m)\cap A_{2m}
\]

for:

\[
\ell\equiv1\pmod4.
\]

These identities matched exact group orders in every audited case through \(n=16\).

**Status:** finite-exact classification over the audited range.  
An all-\(n\) proof is not yet claimed here.

---

# 6. Component pattern from the group census

The same audit gives a striking component classification.

## Odd \(n\)

For odd-generator support classes, all audited graphs are connected.

For even-generator supports:

- if:
  \[
  n\equiv1\pmod4,
  \]
  there are two components;
- if:
  \[
  n\equiv3\pmod4,
  \]
  the graph is connected.

Example:

\[
G_{9,4}
\]

has exactly two components of size:

\[
10080.
\]

## Even \(n\), even support

All audited even-support channel graphs are connected.

## Even \(n=2m\), odd support

The intrinsic bipartition sectors control the components.

For:

\[
\ell\equiv3\pmod4,
\]

the number of components equals exactly:

\[
\boxed{
\frac12\binom{2m}{m}.
}
\]

This recovers the exact LR3 theorem and is also observed for \(LR7\).

For:

\[
\ell\equiv1\pmod4,
\]

the audited pattern is subtler:

- when \(m\) is even, component count equals the intrinsic-sector count;
- when \(m\) is odd, each intrinsic sector splits into two components.

Example:

\[
n=10,\quad LR5:
\]

intrinsic sectors:

\[
126,
\]

channel components:

\[
252.
\]

But:

\[
n=12,\quad LR5:
\]

both counts are:

\[
462.
\]

This is already a qualitative distinction between odd preserving channels.

---

# 7. Exact odd-\(n\) LR2/LR3 isomorphism

There is one exact cross-channel equivalence.

For odd \(n\), multiplication of cyclic positions by \(2\):

\[
\phi(i)=2i\pmod n
\]

is invertible.

It normalizes the dihedral subgroup:

\[
D_n.
\]

An LR2 block reversal is simply the transposition:

\[
(i,i+1).
\]

Conjugation by \(\phi\) maps this to:

\[
(2i,2i+2),
\]

which is exactly an LR3 endpoint transposition.

Therefore:

\[
\boxed{
G_{n,2}\cong G_{n,3}
\qquad
(n\text{ odd}).
}
\]

This is an exact theorem, not merely a finite spectral coincidence.

It explains the identical LR2/LR3 data at:

\[
n=7,9.
\]

---

# 8. Consequence of the odd-\(n\) isomorphism

LR3 is not geometrically distinct from LR2 on odd layers.

Its strong distinction appears on even layers, where:

- multiplication by \(2\) is no longer invertible mod \(n\);
- the intrinsic bipartition exists;
- LR3 becomes sector-preserving;
- LR2 remains sector-changing and connected.

Thus:

\[
\boxed{
\text{the LR2/LR3 geometric split is fundamentally an even-layer phenomenon.}
}
\]

This reinforces the role of intrinsic parity sectors in the HC programme.

---

# 9. Explicit small-layer geometry

Exact HC graphs were constructed through:

\[
n=9.
\]

Selected larger preserving-channel components were also constructed at:

\[
n=10,12.
\]

The audit measured:

- component count;
- component size;
- bipartiteness;
- triangle count;
- four-cycles through a reference vertex;
- extremal adjacency eigenvalues;
- normalized largest-component spectral gap.

---

# 10. LR3 onset geometry at \(n=6\)

At:

\[
n=6,
\]

the LR3 graph has:

\[
10
\]

components.

Each component has:

\[
6
\]

vertices and degree:

\[
3.
\]

Each component is bipartite.

A simple 3-regular bipartite graph on six vertices must be:

\[
\boxed{
K_{3,3}.
}
\]

Therefore:

\[
\boxed{
G_{6,3}
=
10K_{3,3}.
}
\]

Its component spectrum is:

\[
\boxed{
\{3,0,0,0,0,-3\}.
}
\]

This is an exact finite onset geometry.

It should not yet be assigned a physical meaning.

---

# 11. \(n=8\): three visibly different channels

At:

\[
n=8,
\]

the three available supports already look qualitatively different.

## LR2

- connected;
- degree \(8\);
- \(2520\) vertices;
- non-bipartite;
- \(20\) four-cycles through a reference vertex;
- normalized component gap approximately:
  \[
  0.188255.
  \]

## LR3

- \(35\) components;
- \(72\) vertices per component;
- degree \(8\);
- non-bipartite;
- \(20\) four-cycles through a reference vertex;
- normalized component gap:
  \[
  \boxed{1/2}.
  \]

## LR4

- connected;
- half-cycle degree \(4\);
- no four-cycle through the reference vertex;
- normalized component gap approximately:
  \[
  0.137628.
  \]

So a common raw distance:

\[
d_E=2
\]

does not imply common internal graph geometry.

---

# 12. \(n=9\): LR2/LR3 equivalence and LR4 splitting

At:

\[
n=9,
\]

the exact odd-\(n\) theorem gives:

\[
G_{9,2}\cong G_{9,3}.
\]

Both are:

- connected;
- degree \(9\);
- bipartite;
- have \(27\) reference four-cycles;
- have identical adjacency spectra.

Meanwhile:

\[
G_{9,4}
\]

has:

- two components;
- \(10080\) vertices per component;
- degree \(9\);
- non-bipartite;
- only \(9\) reference four-cycles;
- a different spectral gap.

This cleanly separates support geometry from raw class abundance.

---

# 13. \(n=10\): two preserving odd channels

At:

\[
n=10,
\]

both LR3 and LR5 preserve the intrinsic bipartition.

But their component structures differ.

## LR3

- intrinsic sector components:
  \[
  126;
  \]
- component size:
  \[
  1440;
  \]
- degree:
  \[
  10;
  \]
- bipartite;
- \(35\) four-cycles through the reference vertex;
- normalized component gap:
  \[
  \approx0.276393.
  \]

## LR5

- components:
  \[
  252;
  \]
- each intrinsic sector splits into two;
- component size:
  \[
  720;
  \]
- half-cycle degree:
  \[
  5;
  \]
- bipartite;
- zero four-cycles through the reference vertex;
- normalized gap:
  \[
  0.2.
  \]

Thus parity preservation alone does not determine internal channel geometry.

---

# 14. Decisive comparison: \(n=12\), LR3 versus LR5

The cleanest GROW-07 comparison occurs at:

\[
n=12.
\]

Both:

\[
LR3
\]

and:

\[
LR5
\]

have all of the following in common:

- odd support;
- intrinsic bipartition preserving;
- degree:
  \[
  12;
  \]
- component count:
  \[
  462;
  \]
- component size:
  \[
  43200.
  \]

So parity, degree, component count and component size have all been controlled.

Yet the graphs are still different.

## LR3

Reference four-cycles:

\[
\boxed{54}.
\]

Top nontrivial adjacency eigenvalue:

\[
10
\]

in the numerical exact-adjacency audit.

Normalized gap:

\[
\boxed{
1/6\approx0.166667.
}
\]

## LR5

Reference four-cycles:

\[
\boxed{18}.
\]

Top nontrivial adjacency eigenvalue numerically:

\[
\approx9.464101615.
\]

Normalized gap:

\[
\approx0.211324865.
\]

Therefore:

\[
\boxed{
G_{12,3}\not\cong G_{12,5}.
}
\]

The differing exact local square count alone proves non-isomorphism.

This is the decisive answer to the GROW-07 question.

---

# 15. Internal geometry survives universal normalization

GROW-05 showed that LR3 and LR5 obey the same *form* of:

- renewal law;
- generic class density;
- support-channel inflow/outflow law.

GROW-07 shows that after those universal properties are stripped away, their fixed-layer graphs still retain different:

- component refinements;
- short-loop structure;
- spectra;
- mixing gaps.

Therefore:

\[
\boxed{
\ell
\text{ is not merely a renewal exponent or channel position.}
}
\]

It labels genuinely different internal HC geometries.

---

# 16. Triangle audit

No triangles were found in any explicitly enumerated channel graph through:

\[
n=10
\]

in the audited set, nor through the reference neighborhood for the \(n=12\) LR3/LR5 components.

This is a finite-exact observation.

An all-\(n,\ell\) triangle-free theorem is **not** claimed here.

The abundance of four-cycles, however, is strongly support-dependent.

This makes mixed and unmixed short loops a natural next target.

---

# 17. Spectral distinctions

The spectral audit shows several qualitatively different behaviors:

- LR3 onset components at \(n=6\) have \(K_{3,3}\) spectrum;
- odd-layer LR2/LR3 spectra coincide exactly by graph isomorphism;
- even-layer LR3 sector components can have substantially larger normalized gaps than LR2;
- LR5 can have the same component size as LR3 while retaining a different gap.

Thus channel-specific slow-mode structure exists already at the purely combinatorial graph level.

This is potentially relevant to later physics bridges, but no physical relaxation time is yet defined.

---

# 18. Finite generator-group universality classes

The positional-group audit suggests four algebraic support classes controlled by:

- parity of \(n\);
- parity of \(\ell\);
- \(\ell\bmod4\).

Schematically:

\[
\boxed{
S_n,\quad
A_n,\quad
S_m\times S_m,\quad
(S_m\times S_m)\cap A_{2m}.
}
\]

This is stronger internal structure than the two-way odd/even support split.

The classification matched:

\[
\boxed{
48/48
}
\]

audited \((n,\ell)\) cases through \(n=16\).

Because the all-\(n\) group-generation proof has not yet been written, it remains a finite-exact classification rather than a theorem in Foundation v1.0.

---

# 19. What GROW-07 says about physics-like interpretation

The result improves the situation considerably.

Before GROW-07, a skeptical reading was:

> all channels obey one universal law, so perhaps \(\ell\) is merely bookkeeping.

That reading is now false.

Channels can have:

- different component topology;
- different finite algebraic generator groups;
- different short-loop counts;
- different spectral gaps;

even after matching:

- raw distance;
- parity;
- degree;
- component count;
- component size.

So a later interpretation of \(\ell\) as an **internal mode/channel label** is structurally better motivated.

Still, nothing identifies those modes with known particles or forces.

---

# 20. LR3 status after GROW-07

LR3 now has three distinct kinds of significance:

## Selection significance

It is the smallest nontrivial odd support and therefore the most local nontrivial intrinsic-bipartition-preserving reversal.

## Channel-position significance

It is the first two-sided nontrivial interior channel:

\[
LR2\to LR3\to LR4.
\]

## Geometry significance

On even layers it develops intrinsic-sector component geometry that is genuinely different from adjacent and higher support channels.

However:

\[
\boxed{
G_{n,2}\cong G_{n,3}
\quad
\text{for odd }n.
}
\]

So LR3's geometric distinction is specifically tied to the even-layer sector structure rather than being universal at every \(n\).

This is a useful restriction.

---

# 21. GROW-07 verdict

The principal question was:

\[
\text{Are reversal-support channels internally equivalent after universal growth laws are removed?}
\]

The answer is:

\[
\boxed{
\textbf{No.}
}
\]

The support label \(\ell\) indexes genuinely different channel geometries.

The decisive controlled witness is:

\[
\boxed{
n=12,\quad LR3\text{ versus }LR5,
}
\]

where both channels have:

- preserving parity;
- degree \(12\);
- \(462\) components;
- component size \(43200\);

yet have different exact local four-cycle counts:

\[
54\neq18,
\]

and different adjacency spectral gaps.

Therefore the internal geometry is not determined solely by parity, support-class abundance, or component size.

---

# 22. Is GROW-08 needed?

Yes.

GROW-07 finds genuine channel-specific internal geometry.

The next question should now be:

> **How do those distinct channel geometries couple to one another when more than one support colour is allowed in a loop?**

This is exactly the purpose of:

\[
\boxed{
\textbf{EHF-HC-GROW-08 — Cross-Channel Loop and Coupling Geometry Audit}.
}
\]

The highest-value targets are:

1. minimal mixed-support loops;
2. support-coloured square/hexagon census;
3. commutators of \(LR_\ell\) and \(LR_{\ell+1}\) moves;
4. parity of mixed loops;
5. whether mixed loops close within or change intrinsic sectors;
6. support-space holonomy;
7. whether LR3 has a distinctive bridging role between LR2 and LR4.

Only after that should the programme open a physics-bridge branch.
