# Relational Atlas Framework

## Odd Preserve-World Chamber and Boundary Dynamics

## Naming Convention

This document uses **Relational Atlas Framework (RAF)** for the mathematical and combinatorial layer of the work.

RAF refers to:

- admissible comparison,
- local-move state spaces,
- quotient and chamber structure,
- active-slot signatures,
- Boolean packet dynamics,
- coarse Markov-state models,
- and emergent transport or metric structure derived from finite combinatorics.

**Emergent Horizon Framework (EHF)** refers to the broader interpretive hypothesis that RAF-type structures may eventually help explain emergent geometry, gravitational consistency, horizon-like behavior, or other physical phenomena.

This document is primarily a RAF document. Its mathematical and computational claims do not require EHF to be physically correct.

---

# 1. Status

This document summarizes the current odd preserve-world results for canonical Hamiltonian cycles under local circular reversals of lengths 2 and 3.

The odd preserve-world theory is not yet as closed as the even Johnson transport theory. However, it now has several strong exact and near-exact structures:

- exact component decomposition at \(n=5,7,9\),
- exact chamber data at \(n=9\),
- distinguished regular Cayley-action chambers,
- a toroidal \(C_6\square C_6\) chamber,
- slot-signature stratification of irregular chambers,
- an exact Boolean 4-cube of global active-slot patterns at \(n=7,9\),
- sampled support for the same Boolean grammar at \(n=11,13,15\),
- a finite Boolean transition rule at \(n=9\),
- robust distributed Boolean packets,
- a reversible 16-state packet MSM,
- an effective four-spin Ising/Glauber-like boundary model for \(n\ge 9\),
- a stable staggered slow mode,
- Gray-code-compatible traversal of the boundary packet cube,
- and metric-scaling evidence that the raw move graph is pre-geometric rather than physical 3D space.

The clean current position is:

> Odd preserve-world dynamics produces a structured chamber landscape with a stable four-bit boundary grammar.  
> The exact chamber theory is strongest at \(n=9\).  
> The boundary grammar appears stable across larger odd \(n\), but several claims remain theorem candidates rather than completed proofs.

---

# 2. Core Construction

## 2.1 State space

For fixed \(n\), states are canonical Hamiltonian cycles on \(K_n\), modulo rotation and reflection.

A cycle is represented as

\[
(c_0,c_1,\dots,c_{n-1}),
\]

with labels in \(\{1,2,\dots,n\}\).

Canonicalization:

1. rotate so that label \(1\) is first,
2. identify a cycle with its reversal,
3. keep the lexicographically smaller representative.

The number of canonical Hamilton cycles is

\[
\frac{(n-1)!}{2}.
\]

For \(n=9\), this gives

\[
\frac{8!}{2}=20160.
\]

## 2.2 Local moves

Local moves are circular segment reversals of length 2 or 3.

A move is specified by a slot

\[
(s,L),
\]

where

\[
s\in\{0,1,\dots,n-1\},\qquad L\in\{2,3\}.
\]

The circular segment of length \(L\) beginning at slot \(s\) is reversed, and the resulting cycle is canonicalized.

## 2.3 Odd preserve-world filter

For odd \(n\), define the parity-position label \(\Pi(c)\) by splitting the cycle into even and odd positions using zero-based indexing:

\[
\text{even positions}: c_0,c_2,c_4,\dots
\]

\[
\text{odd positions}: c_1,c_3,c_5,\dots
\]

The label \(\Pi(c)\) is the unordered pair of the sorted even-position and odd-position vertex sets.

A local move edge is kept only when

\[
\Pi(c')=\Pi(c).
\]

The resulting graph is the odd preserve-world graph.

---

# 3. Exact Component Data for Small Odd n

## 3.1 \(n=5\)

The \(n=5\) preserve-world has:

\[
\text{states}=12,
\qquad
\text{edges}=8,
\qquad
\text{components}=5.
\]

Component sizes:

\[
[4,3,2,2,1].
\]

Degree histogram:

\[
\{0:1,1:6,2:5\}.
\]

This is the minimal nontrivial odd preserve-world seed.

## 3.2 \(n=7\)

The \(n=7\) preserve-world has:

\[
\text{states}=360,
\qquad
\text{edges}=840,
\qquad
\text{components}=19.
\]

Component sizes:

\[
[36,32,28,28,24,24,24,20,20,20,16,16,16,12,12,12,8,8,4].
\]

Degree histogram:

\[
\{2:4,3:32,4:120,5:128,6:76\}.
\]

The largest component is a 36-state regular chamber of degree 6.

## 3.3 \(n=9\)

The \(n=9\) preserve-world has:

\[
\text{states}=20160,
\qquad
\text{edges}=67200,
\qquad
\text{components}=69.
\]

The component-size histogram is:

\[
\begin{aligned}
&576^1,
540^1,
504^2,
468^3,
432^5,
396^5,
360^7,
324^7,\\
&288^8,
252^7,
216^7,
180^5,
144^5,
108^3,
72^2,
36^1.
\end{aligned}
\]

Thus all \(n=9\) component sizes are multiples of 36.

The distinguished regular chamber ladder is:

\[
576 \rightarrow 144 \rightarrow 36.
\]

More precisely:

- one 576-state regular chamber,
- two regular outer 144-state chambers within a five-chamber 144-sector,
- one 36-state torus chamber.

---

# 4. Distinguished Regular Chambers at n=9

## 4.1 The 36-state torus chamber

The unique 36-state regular chamber has:

\[
\text{vertices}=36,
\qquad
\text{edges}=72,
\qquad
\text{degree}=4.
\]

Graph invariants:

- connected,
- bipartite,
- diameter 6,
- radius 6,
- girth 4,
- shell profile \([1,4,8,10,8,4,1]\).

It is exactly isomorphic to

\[
C_6\square C_6.
\]

This is the toroidal endpoint chamber of the \(n=9\) regular ladder.

## 4.2 The 576-state master chamber

The 576-state regular chamber has:

\[
\text{vertices}=576,
\qquad
\text{edges}=2304,
\qquad
\text{degree}=8.
\]

The preserving local slot moves generate a regular group action of order 576:

- orbit size 576,
- stabilizer size 1,
- transitive action,
- regular action.

The group diagnostics match \(S_4\times S_4\):

\[
\{1:1,2:99,3:80,4:156,6:144,12:96\}.
\]

Current careful statement:

> The 576-state chamber admits an exact regular local-slot action of order 576 with diagnostics consistent with \(S_4\times S_4\).

A formal group-isomorphism certificate remains a desirable next step.

## 4.3 The corrected 144-state sector

Earlier language sometimes referred to “the two 144-state chambers.” The corrected statement is:

> There are five 144-state chambers total. Among them, two are regular outer 144-state chambers.

The five chambers form a mirror-stratified taxonomy:

\[
A\;--\;B\;--\;C\;--\;B'\;--\;A'.
\]

Abstract graph species:

\[
A\cong A',
\qquad
B\cong B',
\qquad
C\text{ is a singleton species}.
\]

For the main \(L\le3\) odd preserve-world model, their invariants are:

| chamber | edges | degree histogram | diameter | Fiedler value |
|---:|---:|---|---:|---:|
| A | 432 | \(\{6:144\}\) | 5 | 1.26794919 |
| B | 384 | \(\{4:12,5:80,6:44,7:8\}\) | 7 | 0.55195754 |
| C | 384 | \(\{4:16,5:64,6:64\}\) | 7 | 1.00000000 |
| B' | 384 | \(\{4:12,5:80,6:44,7:8\}\) | 7 | 0.55195754 |
| A' | 432 | \(\{6:144\}\) | 5 | 1.26794919 |

The outer pair \(A,A'\) are the two regular 144-state chambers emphasized in earlier notes.

Each regular outer 144-state chamber admits a regular local-slot action of order 144, with diagnostics consistent with \(S_3\times S_4\):

\[
\{1:1,2:39,3:26,4:24,6:42,12:12\}.
\]

The affine vertex inversion

\[
v\mapsto -v \pmod 9
\]

maps the five 144-state chambers as:

\[
A\leftrightarrow A',
\qquad
B\leftrightarrow B',
\qquad
C\leftrightarrow C.
\]

Caution:

> Paired chambers are abstract graph twins, but not necessarily identical as labelled admissibility systems.

---

# 5. Irregular Chambers and Slot-Signature Stratification

Not all chambers are regular or locally homogeneous.

A representative irregular component is the 360-state component with:

\[
\text{vertices}=360,
\qquad
\text{edges}=1200,
\]

and degree histogram

\[
\{5:16,6:152,7:128,8:64\}.
\]

For this component:

- graph degree equals admissible slot count,
- spectral layout shows coherent lobed structure,
- lobes correlate strongly with local admissibility structure,
- exact slot-signature classes occupy coherent spectral regions.

This motivates the term:

> local move-survival stratification.

## 5.1 Signature quotient of the 360-state component

Quotienting the 360-state component by exact slot-signature class gives:

\[
\text{original vertices}=360,
\qquad
\text{original edges}=1200,
\qquad
\text{signature classes}=15,
\qquad
\text{quotient edges}=56.
\]

Important quotient-class sizes include:

\[
64,
52,52,
32,32,32,32,
12,12,12,12,
4,4,4,4.
\]

The largest class has:

\[
\text{size}=64,
\qquad
\text{average degree}=8,
\qquad
\text{intra-class edges}=116.
\]

Interpretation:

> The irregular chamber has a high-mobility core, paired intermediate classes, transition classes, and small low-degree boundary classes.

## 5.2 All-component signature quotient scan

Across all 69 connected components at \(n=9\), exact slot-signature quotienting gives:

\[
69\text{ connected components}\rightarrow 42\text{ quotient-skeleton families}.
\]

Multiplicity summary:

- 27 quotient families occur with multiplicity 2,
- 15 quotient families occur with multiplicity 1.

Regular chambers collapse to one signature class:

- 576 chamber \(\rightarrow\) one class,
- regular 144 chamber family \(\rightarrow\) one class, multiplicity 2,
- 36 chamber \(\rightarrow\) one class.

Thus:

> Regular chambers are locally homogeneous. Irregular chambers are locally stratified.

---

# 6. Reversal Symmetry

Define label reversal

\[
\sigma_R=(1,9,8,7,6,5,4,3,2),
\]

so that

\[
1\mapsto 1,
\qquad
2\leftrightarrow 9,
\qquad
3\leftrightarrow 8,
\qquad
4\leftrightarrow 7,
\qquad
5\leftrightarrow 6.
\]

On canonical cycles, \(\sigma_R\) is applied labelwise and then canonicalized.

For the 360-state irregular component, \(\sigma_R\):

- maps the component to itself,
- preserves edges,
- has 12 fixed points,
- has 174 two-cycles,
- gives cycle-length histogram \(\{1:12,2:174\}\).

The automorphism group of this component is:

\[
\operatorname{Aut}(G)\cong \mathbb Z/2,
\]

with the nontrivial automorphism induced by \(\sigma_R\).

At the full \(n=9\) component level, \(\sigma_R\) fixes 15 components and pairs the remaining 54 into 27 component-pairs. This matches the quotient-family multiplicity structure:

\[
15\text{ singleton families}+27\text{ multiplicity-2 families}.
\]

---

# 7. Boolean Active-Slot Grammar

The strongest general odd-side structure currently known is the Boolean active-slot grammar.

For odd \(n\ge7\), define:

\[
\mathrm{CORE}_n=\{(s,3):2\le s\le n-4\},
\]

and

\[
\mathrm{OPTIONAL}_n=\{(0,2),(1,3),(n-3,3),(n-1,2)\}.
\]

The conjectured active-slot law is:

\[
\mathrm{ACTIVE}(c)=\mathrm{CORE}_n\cup S(c),
\]

where

\[
S(c)\subseteq \mathrm{OPTIONAL}_n.
\]

Thus the global active-slot pattern space is a Boolean 4-cube:

\[
\{0,1\}^4.
\]

## 7.1 Exact n=9 result

At \(n=9\):

\[
\mathrm{CORE}_9=\{(2,3),(3,3),(4,3),(5,3)\},
\]

\[
\mathrm{OPTIONAL}_9=\{(0,2),(1,3),(6,3),(8,2)\}.
\]

The exact global result is:

\[
20160\text{ states}\rightarrow 16\text{ global active-slot patterns}.
\]

Every pattern is exactly

\[
\mathrm{CORE}_9\cup S,
\qquad
S\subseteq \mathrm{OPTIONAL}_9.
\]

The slot-count histogram is binomial:

\[
\{4:1,5:4,6:6,7:4,8:1\}.
\]

Using bit order

\[
(0,2),(1,3),(6,3),(8,2),
\]

\(\sigma_R\) acts as bit reversal:

\[
(b_0,b_1,b_2,b_3)\mapsto (b_3,b_2,b_1,b_0).
\]

## 7.2 Evidence across odd n

| n | method | cycles tested | core size | optional size | observed patterns | violations | all patterns observed |
|---:|---|---:|---:|---:|---:|---:|:---:|
| 7 | exact | 360 | 2 | 4 | 16 | 0 | yes |
| 9 | exact | 20160 | 4 | 4 | 16 | 0 | yes |
| 11 | sampled | 50000 | 6 | 4 | 16 | 0 | yes |
| 13 | sampled | 50000 | 8 | 4 | 16 | 0 | yes |
| 15 | sampled | 50000 | 10 | 4 | 16 | 0 | yes |

The sampled cases strongly support the general law:

> odd preserve-world active grammar = growing fixed interior core + four boundary optional switches.

The Boolean dimension remains 4 as \(n\) grows.

---

# 8. Slot-Level Law and Optional Marginal

The global Boolean grammar is supported by slot-level diagnostics.

For odd \(n\ge7\), local slots split into three roles:

1. **CORE slots**: always active,
2. **OPTIONAL slots**: conditionally active,
3. **FORBIDDEN slots**: never active.

Exact results:

- at \(n=7\), all CORE/OPTIONAL/FORBIDDEN classifications are verified exactly,
- at \(n=9\), all CORE/OPTIONAL/FORBIDDEN classifications are verified exactly.

For \(n=7\) and \(n=9\), each optional slot is active in exactly

\[
\frac{2}{3}
\]

of all canonical Hamilton cycles.

Sampled results at \(n=11,13,15\) give optional-slot activity fractions very close to \(2/3\).

This supports three theorem candidates:

## Theorem candidate A: active-slot Boolean grammar

For odd \(n\ge7\):

\[
\mathrm{ACTIVE}(c)=\mathrm{CORE}_n\cup S(c),
\qquad
S(c)\subseteq\mathrm{OPTIONAL}_n.
\]

## Theorem candidate B: slot-role law

For odd \(n\ge7\):

- CORE slots are always active,
- OPTIONAL slots are conditional,
- FORBIDDEN slots are never active.

## Theorem candidate C: optional marginal law

For odd \(n\ge7\), each optional slot is active in exactly \(2/3\) of all canonical Hamilton cycles.

The \(2/3\) law is exact computationally for \(n=7,9\) and strongly supported by sampling for \(n=11,13,15\).

---

# 8.1 Exact Boolean Packet Counting Theory

The first bridge result is that the odd Boolean packet populations have an exact finite boundary-counting model.

Write a canonical Hamilton cycle as:

```text
c = (1, a1, a2, ..., a_{n-1})
```

with the canonical orientation condition:

```text
a1 < a_{n-1}
```

For odd n >= 7, the four optional active-slot bits can be expressed as boundary inequality predicates:

```text
b0 = 1 iff a1 < a2
b1 = 1 iff a3 < a_{n-1}
b2 = 1 iff a1 < a_{n-3}
b3 = 1 iff a_{n-2} < a_{n-1}
```

Thus the Boolean packet of a cycle is controlled by the relative order of six boundary variables:

```text
a1, a2, a3, a_{n-3}, a_{n-2}, a_{n-1}
```

This gives an exact packet-counting rule.

Let L_b be the number of relative orderings of these six boundary variables satisfying:

```text
canonical condition: a1 < a_{n-1}
packet condition:    optional bit pattern = b
```

Then for every odd n >= 7, the predicted number of canonical Hamilton cycles in packet b is:

```text
N_n(b) = ((n-1)! / 720) * L_b
```

because the relative order of the six selected boundary entries is uniformly distributed among 6! = 720 possibilities, and the canonical condition selects exactly half of them.

The exact boundary linear-extension counts are:

| bits | L_b |
|---|---:|
| 1111 | 76 |
| 1010 | 40 |
| 0101 | 40 |
| 1110 | 32 |
| 1101 | 32 |
| 1011 | 32 |
| 0111 | 32 |
| 1100 | 10 |
| 1001 | 10 |
| 0110 | 10 |
| 0011 | 10 |
| 1000 | 8 |
| 0100 | 8 |
| 0010 | 8 |
| 0001 | 8 |
| 0000 | 4 |

These counts sum to 360, matching the number of relative orderings satisfying the canonical condition.

For n=7, the multiplier is:

```text
(n-1)! / 720 = 6! / 720 = 1
```

so the packet populations are exactly L_b.

For n=9, the multiplier is:

```text
8! / 720 = 56
```

which gives the observed exact n=9 packet populations:

```text
1111: 76 * 56 = 4256
1010: 40 * 56 = 2240
0101: 40 * 56 = 2240
1110,1101,1011,0111: 32 * 56 = 1792 each
1100,1001,0110,0011: 10 * 56 = 560 each
1000,0100,0010,0001: 8 * 56 = 448 each
0000: 4 * 56 = 224
```

This exactly matches the n=9 Boolean packet table.

## 8.2 Boundary Generating Polynomial

The packet-counting data can be encoded by a four-variable boundary polynomial:

```text
Z(t0,t1,t2,t3) = sum_b L_b * t0^b0 * t1^b1 * t2^b2 * t3^b3
```

Explicitly:

```text
Z = 4
  + 8 * (t0 + t1 + t2 + t3)
  + 10 * (t0*t1 + t1*t2 + t2*t3 + t0*t3)
  + 40 * (t0*t2 + t1*t3)
  + 32 * (t0*t1*t2 + t0*t1*t3 + t0*t2*t3 + t1*t2*t3)
  + 76 * t0*t1*t2*t3
```

Then:

```text
N_n(b) = ((n-1)! / 720) * [coefficient of t^b in Z]
```

This is the first exact odd-side analogue of the even Johnson generating-function layer.

It is not yet a transition-counting theory. It counts packet populations, not packet-to-packet edge fluxes. But it gives the correct starting point for an exact odd packet transport theory.

## 8.3 Exact Packet Moments

The boundary polynomial gives exact packet moments. With respect to the uniform canonical-cycle distribution:

```text
E[b_i] = 2/3 for each optional bit
```

This proves the optional 2/3 marginal law, provided the boundary-inequality predicates are established.

Pair moments are:

```text
E[b0*b2] = 1/2
E[b1*b3] = 1/2
all other E[bi*bj] = 5/12
```

Triple moments are:

```text
E[bi*bj*bk] = 3/10 for every triple
```

and the all-active probability is:

```text
P(1111) = 19/90
```

The Hamming-weight distribution is:

```text
|b| = 0:  4/360  = 1/90
|b| = 1: 32/360  = 4/45
|b| = 2: 120/360 = 1/3
|b| = 3: 128/360 = 16/45
|b| = 4: 76/360  = 19/90
```

Thus:

```text
E[|b|] = 8/3
```

This gives the odd Boolean packet layer its first exact moment theory.

## 8.4 Bridge to the Johnson Counting Layer

The even Johnson document has an exact subset-count generating function for shell counts and moment identities.

The odd preserve-world now has an exact finite boundary-counting polynomial for Boolean packet populations and packet moments.

The analogy is:

```text
even side:
  subset generating function -> shell counts -> h,q moments -> transport

odd side:
  boundary order polynomial -> packet counts -> bit moments -> packet MSM target
```

The remaining task is to extend the odd packet-counting theory from population counts to transition counts:

```text
N_n(b)                      packet populations
E_n(b -> b')                packet edge counts
T_n(b,b')                   packet transition matrix
stationary pi_n(b)          edge-volume stationary distribution
```

If these can be derived from a finite boundary-order enumeration analogous to Z(t0,t1,t2,t3), then the odd preserve-world will have a genuine exact packet transport theory parallel to the even Johnson shell transport theory.

## 8.5 Exact Packet Transition Kernel for Odd n >= 9

The packet-counting theory extends to packet-to-packet transition counts.

Let:

```text
b in {0,1}^4
L_b = boundary packet population coefficient
F_n = (n-1)! / 720
C_n = (n-1)! / 7!
```

Then:

```text
N_n(b) = F_n * L_b
```

and the directed packet edge-volume is:

```text
V_n(b) = N_n(b) * (n - 5 + |b|)
```

because every state in packet b has:

```text
n - 5 always-active core slots
+
|b| active optional boundary slots.
```

The total directed edge-volume is therefore:

```text
V_n(total) = F_n * [360*(n-5) + 960]
           = F_n * 120*(3n - 7)
```

so the exact stationary mass of packet b under the edge-step packet MSM is:

```text
pi_n(b) = L_b * (n - 5 + |b|) / [120*(3n - 7)]
```

This formula exactly reproduces the n=9 stationary packet masses. For example:

```text
pi_9(1111) = 76 * 8 / 2400 = 0.253333...
pi_9(1010) = 40 * 6 / 2400 = 0.1
pi_9(0000) = 4 * 4 / 2400 = 0.006666...
```

## 8.6 Boundary Kernel Plus Interior Diagonal Term

For odd n >= 9, the packet transition matrix has a simple decomposition.

Let M_n(b,b') be the directed packet transition count from packet b to packet b'. Then:

```text
M_n(b,b') = C_n * H_n(b,b')
```

where:

```text
H_n(b,b') = H_9(b,b') + (n - 9) * 7 * L_b * delta_{b,b'}
```

Here:

- H_9 is the fixed n=9 boundary transition kernel,
- delta is the Kronecker delta,
- the extra term comes from the additional interior length-3 core slots present for n > 9,
- those extra interior core slots do not change the Boolean boundary packet.

Thus the odd packet transport theory has the form:

```text
fixed boundary transition kernel
+
n-dependent self-retention from interior core moves.
```

This explains why the Hamming-layer structure of off-diagonal packet transitions stabilizes across n >= 9, while self-retention increases with n.

## 8.7 Fixed Boundary Kernel H_9

Using packet order:

```text
1111, 1010, 0101, 1110, 1101, 1011, 0111, 1100,
1001, 0110, 0011, 1000, 0100, 0010, 0001, 0000
```

H_9 = M_9 / 8 is:

| from \ to | 1111 | 1010 | 0101 | 1110 | 1101 | 1011 | 0111 | 1100 | 1001 | 0110 | 0011 | 1000 | 0100 | 0010 | 0001 | 0000 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1111 | 2800 | 130 | 130 | 237 | 325 | 325 | 237 | 13 | 26 | 0 | 13 | 10 | 0 | 0 | 10 | 0 |
| 1010 | 130 | 1100 | 0 | 165 | 10 | 165 | 0 | 5 | 5 | 0 | 0 | 60 | 0 | 40 | 0 | 0 |
| 0101 | 130 | 0 | 1100 | 0 | 165 | 10 | 165 | 0 | 5 | 0 | 5 | 0 | 40 | 0 | 60 | 0 |
| 1110 | 237 | 165 | 0 | 878 | 13 | 100 | 0 | 65 | 26 | 65 | 0 | 5 | 14 | 0 | 0 | 0 |
| 1101 | 325 | 10 | 165 | 13 | 790 | 26 | 100 | 52 | 52 | 0 | 26 | 4 | 0 | 0 | 5 | 0 |
| 1011 | 325 | 165 | 10 | 100 | 26 | 790 | 13 | 26 | 52 | 0 | 52 | 5 | 0 | 0 | 4 | 0 |
| 0111 | 237 | 0 | 165 | 0 | 100 | 13 | 878 | 0 | 26 | 65 | 65 | 0 | 0 | 14 | 5 | 0 |
| 1100 | 13 | 5 | 0 | 65 | 52 | 26 | 0 | 182 | 16 | 0 | 0 | 28 | 33 | 0 | 0 | 0 |
| 1001 | 26 | 5 | 5 | 26 | 52 | 52 | 26 | 16 | 140 | 0 | 16 | 28 | 0 | 0 | 28 | 0 |
| 0110 | 0 | 0 | 0 | 65 | 0 | 0 | 65 | 0 | 0 | 224 | 0 | 0 | 33 | 33 | 0 | 0 |
| 0011 | 13 | 0 | 5 | 0 | 26 | 52 | 65 | 0 | 16 | 0 | 182 | 0 | 0 | 33 | 28 | 0 |
| 1000 | 10 | 60 | 0 | 5 | 4 | 5 | 0 | 28 | 28 | 0 | 0 | 124 | 0 | 0 | 0 | 16 |
| 0100 | 0 | 0 | 40 | 14 | 0 | 0 | 0 | 33 | 0 | 33 | 0 | 0 | 144 | 0 | 0 | 16 |
| 0010 | 0 | 40 | 0 | 0 | 0 | 0 | 14 | 0 | 0 | 33 | 33 | 0 | 0 | 144 | 0 | 16 |
| 0001 | 10 | 0 | 60 | 0 | 5 | 4 | 5 | 0 | 28 | 0 | 28 | 0 | 0 | 0 | 124 | 16 |
| 0000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 16 | 16 | 16 | 16 | 48 |

This kernel is symmetric, as expected for an undirected underlying graph represented as directed edge-volume counts.

Its off-diagonal Hamming transition totals are:

```text
Hamming distance 1: 5520
Hamming distance 2: 1344
Hamming distance 3: 288
Hamming distance 4: 0
```

So the off-diagonal Hamming fractions are exactly:

```text
distance 1: 5520 / 7152 = 0.7718120805...
distance 2: 1344 / 7152 = 0.1879194631...
distance 3:  288 / 7152 = 0.0402684564...
distance 4:    0
```

These are precisely the stable fractions observed for n=9, n=11, and n=13.

## 8.8 Exact Packet Transition Matrix

Combining the preceding formulas gives the exact packet MSM for odd n >= 9:

```text
T_n(b,b') = M_n(b,b') / V_n(b)
```

with:

```text
M_n(b,b') = C_n * [H_9(b,b') + (n - 9)*7*L_b*delta_{b,b'}]
```

and:

```text
V_n(b) = F_n * L_b * (n - 5 + |b|)
```

Equivalently, since F_n = 7*C_n:

```text
T_n(b,b') = [H_9(b,b') + (n - 9)*7*L_b*delta_{b,b'}]
            /
            [7*L_b*(n - 5 + |b|)]
```

This is the first closed odd-side packet transport law.

It is not a Fokker-Planck drift/diffusion theory like the even Johnson shell law. It is instead an exact finite-state packet transport theory on a 16-state Boolean boundary quotient.

## 8.9 Bridge Result

The even Johnson side has:

```text
subset generating function -> shell moments -> exact drift/diffusion
```

The odd preserve-world side now has:

```text
boundary order polynomial -> packet moments -> exact 16-state packet MSM
```

This substantially closes the bridge between the documents.

The two theories remain different reductions, but both now have exact counting-to-transport structure.

## 8.10 Audit Result for the Exact Packet Transport Law

The exact audit script `52_odd_packet_transport_exact_audit.py` was run with:

```bash
python3 52_odd_packet_transport_exact_audit.py \
  --exact-ns 7,9 \
  --sample-ns 11,13,15 \
  --samples 50000 \
  --seed 12345 \
  --out-dir runs/odd_packet_transport_exact_audit \
  --write-csv
```

The audit produced a strong confirmation of the odd packet transport bridge.

### Exact n=7 audit

For n=7:

```text
states_seen:                 360
states_expected:             360
states_count_pass:           True
population_pass:             True
bit_predicate_violations:    0
active_grammar_violations:   0
directed_transition_total:   1,680
undirected_edge_equivalent:  840
packet_volume_pass:          True
stationary_max_abs_diff:     0
transition_matrix_symmetric: True
offdiag_hamming_totals:      {1:288, 2:432, 3:0, 4:0}
```

Interpretation:

```text
n=7 exactly confirms the boundary bit predicates, packet population formula,
active-slot grammar, packet volumes, and stationary packet masses.
```

The n=7 transition structure is exceptional and is not governed by the n>=9 fixed H9 kernel. This matches the earlier observation that n=7 is a small-size exceptional case.

### Exact n=9 audit

For n=9:

```text
states_seen:                 20,160
states_expected:             20,160
states_count_pass:           True
population_pass:             True
bit_predicate_violations:    0
active_grammar_violations:   0
directed_transition_total:   134,400
undirected_edge_equivalent:  67,200
packet_volume_pass:          True
stationary_max_abs_diff:     0
transition_matrix_symmetric: True
offdiag_hamming_totals:      {1:44160, 2:10752, 3:2304, 4:0}
transition_formula_pass:     True
transition_formula_diff:     0
Tn_max_abs_diff:             0
derived_H9_matches_fixed:    True
```

Interpretation:

```text
n=9 exactly confirms the full packet transport law.
```

The raw Hamilton-cycle move graph reproduces:

```text
1. the packet population formula,
2. the boundary predicate formula,
3. the active-slot grammar,
4. the packet stationary formula,
5. the fixed H9 boundary kernel,
6. the exact n=9 packet transition matrix,
7. the exact T_n formula at n=9.
```

This is the strongest current evidence that the odd preserve-world has a genuine exact counting-to-transport structure.

### Sampled n=11, n=13, n=15 audits

The sampled larger-n runs used 50,000 sampled canonical cycles each.

All sampled larger-n runs had:

```text
bit_predicate_violations:   0
active_grammar_violations:  0
Hamming-4 offdiag totals:   0
```

The observed transition matrices are not symmetric because the runs used sampled states, not closed exact graphs. Therefore full count differences such as `transition_formula_diff` are not meaningful for sampled runs. The meaningful comparison is the row-normalized transition matrix error `Tn_max_abs_diff`.

The sample errors were:

```text
n=11: Tn_max_abs_diff = 0.00713168
n=13: Tn_max_abs_diff = 0.0114869
n=15: Tn_max_abs_diff = 0.00452704
```

Stationary packet mass deviations were small:

```text
n=11: stationary_max_abs_diff = 0.00235144
n=13: stationary_max_abs_diff = 0.00312971
n=15: stationary_max_abs_diff = 0.00175193
```

Off-diagonal Hamming totals remained stable:

```text
n=11: {1:109524, 2:26544, 3:5661, 4:0}
n=13: {1:110157, 2:26507, 3:5750, 4:0}
n=15: {1:109003, 2:26609, 3:5691, 4:0}
```

These support the n>=9 stable packet-transport regime predicted by the exact formula.

### Audit conclusion

The audit confirms:

```text
Exact n=7:
  packet counts, packet moments, active grammar, and stationary volumes pass.

Exact n=9:
  full packet counting-to-transport law passes with zero error.

Sampled n=11,13,15:
  boundary predicates and active grammar have zero violations;
  transition matrices are close to the predicted n>=9 law;
  Hamming-4 transitions remain absent;
  sampled deviations are consistent with finite sampling noise.
```

The odd preserve-world therefore now has a verified finite counting-to-transport bridge:

```text
boundary order polynomial
-> exact packet populations
-> exact packet moments
-> exact stationary packet masses
-> fixed H9 boundary kernel
-> n>=9 packet MSM formula
```

This materially strengthens RAF because the odd side is no longer merely a chamber catalogue. It now has an exact packet transport law parallel in role to the even Johnson shell transport law.

---

# 9. Boolean Transition Grammar at n=9

The 16 Boolean active-slot patterns form an exact Boolean 4-cube as states, but the transition graph between patterns contains more than ordinary cube edges.

The \(n=9\) Boolean pattern transition graph has:

\[
\text{pattern nodes}=16,
\qquad
\text{transition edges}=64.
\]

Hamming-layer structure:

| Hamming distance | possible | present | missing |
|---:|---:|---:|---:|
| 1 | 32 | 32 | 0 |
| 2 | 48 | 24 | 24 |
| 3 | 32 | 8 | 24 |
| 4 | 8 | 0 | 8 |

Thus:

- all Hamming-1 cube edges are present,
- half of Hamming-2 edges are present,
- one quarter of Hamming-3 edges are present,
- no antipodal Hamming-4 edges are present.

## 9.1 XOR-mask rule

For source bitword \(b\) and target bitword \(b'\), define

\[
m=b\oplus b'.
\]

The masks split into three classes.

Complete masks:

\[
0001,
0010,
0100,
1000.
\]

These are present from every source bitword.

Always-forbidden masks:

\[
1001,
1011,
1101,
1111.
\]

These all toggle both endpoint length-2 optional bits. This is a perfect one-way obstruction.

Partial masks:

\[
0011,
0101,
0110,
1010,
1100,
0111,
1110.
\]

These are governed by source-bit preconditions.

## 9.2 Exact Boolean precondition table

With bit convention

\[
b_0=(0,2),\quad b_1=(1,3),\quad b_2=(6,3),\quad b_3=(8,2),
\]

transition existence is determined by the source bits and XOR mask.

Complete single-bit masks:

\[
1000,0100,0010,0001\rightarrow \mathrm{TRUE}.
\]

Always-forbidden masks:

\[
1001,1101,1011,1111\rightarrow \mathrm{FALSE}.
\]

Partial masks:

\[
1100\rightarrow b_3,
\]

\[
0011\rightarrow b_0,
\]

\[
1110\rightarrow b_3,
\]

\[
0111\rightarrow b_0,
\]

\[
0110\rightarrow b_3\lor b_0,
\]

\[
1010\rightarrow b_3\lor(\neg b_0\land b_1\land\neg b_2)\lor(b_0\land b_1\land b_2),
\]

\[
0101\rightarrow b_0\lor(\neg b_1\land b_2\land\neg b_3)\lor(b_1\land b_2\land b_3).
\]

This table is exactly compatible with \(\sigma_R\) bit reversal.

Current compact statement:

> The \(n=9\) global admissibility grammar is an explicit finite Boolean rule system over source bits and XOR masks.

---

# 10. Boolean Packets

A Boolean packet is the set of cycles with a fixed optional active-slot bit pattern:

\[
P_b=\{c:\operatorname{optional\_pattern}(c)=b\},
\qquad
b\in\{0,1\}^4.
\]

At \(n=9\), there are 16 Boolean packets.

A packet is not a compact object in visual space. It is a distributed region in Hamilton-cycle state space.

## 10.1 Retention measure

For packet \(P\), define:

\[
\operatorname{retention}(P)=\frac{2E_{\mathrm{internal}}(P)}{2E_{\mathrm{internal}}(P)+E_{\mathrm{escape}}(P)}.
\]

This is the probability that a random local edge-step from inside \(P\) remains inside \(P\).

## 10.2 n=9 retention hierarchy

Strongest high-retention packets:

| packet | bits | states | retention | stationary mass | \(\sigma_R\) partner |
|---|---|---:|---:|---:|---|
| P00 | 1111 | 4256 | 0.657895 | 0.253333 | P00 |
| P01 | 1010 | 2240 | 0.654762 | 0.100000 | P02 |
| P02 | 0101 | 2240 | 0.654762 | 0.100000 | P01 |

Weakest / leaky packets include:

| packet | bits | states | retention | stationary mass | \(\sigma_R\) partner |
|---|---|---:|---:|---:|---|
| P08 | 1001 | 560 | 0.333333 | 0.025000 | P08 |
| P15 | 0000 | 224 | 0.428571 | 0.006667 | P15 |

A first taxonomy is:

- high-retention robust distributed packets: P00, P01, P02,
- medium-retention mixed packets: P03, P04, P05, P06, P09, P12, P13,
- low-retention leaky/transition packets: P07, P08, P10, P11, P14, P15.

The retention audit establishes:

> Boolean packets have measurable internal coherence, escape rates, stationary mass, and symmetry-respecting transition structure.

---

# 11. Boolean Packet MSM

The 16 Boolean packets define a coarse Markov State Model (MSM) with a 16-by-16 row-stochastic transition matrix.

For \(n=9\), numerical checks give:

- row-stochastic error: \(2.22\times10^{-16}\),
- stationary distribution consistency error: \(6.07\times10^{-16}\),
- \(\sigma_R\) commutator: exactly zero.

Thus the packet dynamics is exactly \(\sigma_R\)-equivariant at the quotient level.

## 11.1 Dominant eigenmodes

The leading nontrivial eigenvalue is:

\[
\lambda_2=0.788861561,
\qquad
\tau_2=4.216484.
\]

This mode is \(\sigma_R\)-odd and is strongly supported on symmetry-paired packet structures, especially P01/P02 and P11/P14.

The important refinement is:

> Robust packet structure is not only about individual retention. Slow modes may live in packet pairs or clusters.

---

# 12. Effective 4-Spin Ising/Glauber-Like Boundary MSM

The Boolean packet MSM was audited as a possible effective four-bit boundary spin system.

The audit supports the following statement for \(n=9\):

> The \(n=9\) Boolean packet quotient is a reversible, \(\sigma_R\)-equivariant 16-state MSM. Its stationary distribution is almost perfectly captured by a symmetric four-spin Ising-like boundary Hamiltonian. Its transition dynamics is Glauber-dominated, with most off-diagonal flux carried by single-bit flips. Its slowest relaxation mode is the staggered boundary observable \(b_0-b_1+b_2-b_3\).

## 12.1 Reversibility

Detailed balance holds to numerical precision:

\[
\pi_iT_{ij}=\pi_jT_{ji}.
\]

This justifies defining an effective stationary energy

\[
E(b)=-\log \pi(b).
\]

## 12.2 Hamming transition flux

For \(n=9\), off-diagonal stationary transition flux by Hamming distance is:

| Hamming distance | stationary-flux fraction |
|---:|---:|
| 1 | 0.771812 |
| 2 | 0.187919 |
| 3 | 0.040268 |
| 4 | 0.000000 |

Thus the dynamics is Glauber-dominated but not pure Glauber dynamics.

Correct phrase:

> Glauber-dominated four-bit boundary dynamics with multi-bit corrections.

## 12.3 Ising-like stationary energy

Boolean Fourier decomposition of \(E(b)
\) shows that one-body and two-body terms dominate. The ratio of higher-order terms to one/two-body terms is approximately:

\[
0.020650.
\]

A square-symmetric Ising-like fit gives:

\[
R^2=0.999331.
\]

Fitted structure:

\[
E(b)\approx c+h\sum_i s_i+J_{\mathrm{edge}}(s_0s_1+s_1s_2+s_2s_3+s_0s_3)+J_{\mathrm{diag}}(s_0s_2+s_1s_3),
\]

with coefficients approximately:

\[
h=-0.442695,
\qquad
J_{\mathrm{edge}}=0.111157,
\qquad
J_{\mathrm{diag}}=-0.235416.
\]

This is not an exact pairwise Ising model, but the pairwise square-symmetric approximation is extremely strong.

---

# 13. Boundary 3+1 Signature Probe

The four Boolean boundary bits do not currently support the claim that one raw bit acts as time.

Raw-bit diagnostics are pair-degenerate and do not identify a unique time-like coordinate.

However, collective-mode diagnostics reveal a strong exceptional mode:

\[
M_{\mathrm{stag}}=s_0-s_1+s_2-s_3,
\]

or equivalently

\[
b_0-b_1+b_2-b_3.
\]

For \(n=9\), this staggered mode:

- has the highest collective diagnostic score,
- has the longest autocorrelation time,
- aligns with the slowest non-stationary MSM mode,
- is \(\sigma_R\)-odd.

The cautious conclusion is:

> The data do not support one raw boundary coordinate acting as time. Instead, \(n=9\), \(n=11\), and \(n=13\) support a tentative mode-level 1+3 dynamical signature, with the staggered \(\sigma_R\)-odd collective mode as the exceptional slow direction.

This is a mathematical dynamical signature, not a physical spacetime claim.

---

# 14. Scaling of the Boundary MSM Across n

The effective boundary MSM structure appears exceptional at \(n=7\), but stable from \(n=9\) onward.

## 14.1 Hamming flux comparison

| n | Hamming-1 flux | Hamming-2 flux | Hamming-3 flux | Hamming-4 flux |
|---:|---:|---:|---:|---:|
| 7 | 0.400000 | 0.600000 | 0.000000 | 0.000000 |
| 9 | 0.771812 | 0.187919 | 0.040268 | 0.000000 |
| 11 | 0.773427 | 0.186880 | 0.039693 | 0.000000 |
| 13 | 0.772188 | 0.187644 | 0.040168 | 0.000000 |

The \(n=9,11,13\) rows are nearly identical.

## 14.2 Ising parameter stability

| n | field | cycle edge | diagonal | \(R^2\) |
|---:|---:|---:|---:|---:|
| 9 | -0.442695 | +0.111157 | -0.235416 | 0.999331 |
| 11 | -0.413116 | +0.104025 | -0.242836 | 0.999036 |
| 13 | -0.412024 | +0.108289 | -0.239370 | 0.999371 |

## 14.3 Slow-mode stability

| n | slowest mode observable | correlation |
|---:|---|---:|
| 9 | \(b_0-b_1+b_2-b_3\) | 0.981803 |
| 11 | \(b_0-b_1+b_2-b_3\) | 0.981131 |
| 13 | \(b_0-b_1+b_2-b_3\) | 0.981503 |

Current scaling conclusion:

> For odd preserve-worlds with \(n\ge9\), the Boolean boundary packet quotient appears to enter a stable effective four-spin boundary MSM regime.

---

# 15. Gray-Code-Compatible Boundary History

The Hamming-1 support graph on the 16 Boolean packets is the full four-dimensional Boolean cube \(Q_4\) for \(n=9,11,13\).

It has:

\[
|V|=16,
\qquad
|E|=32,
\qquad
\text{degree}=4.
\]

Therefore it admits Hamiltonian cycles corresponding to cyclic Gray codes.

The standard reflected four-bit Gray cycle is transition-compatible for \(n=9,11,13\):

\[
0000\to0001\to0011\to0010\to0110\to0111\to0101\to0100
\]

\[
\to1100\to1101\to1111\to1110\to1010\to1011\to1001\to1000\to0000.
\]

Cautious statement:

> For \(n=9,11,13\), the emergent four-bit boundary packet system supports cyclic Gray-code traversals using only single-bit admissible packet transitions.

Statement to avoid:

> This proves time is a Gray code.

Better phrase:

> Gray-code-compatible cyclic boundary history.

---

# 16. Transfer Probes

Several transfer probes show that the diagnostic pipeline distinguishes structural regimes rather than forcing all systems into the same pattern.

## 16.1 Distinguishable permutation/lattice-gas preserve-world

A related distinguishable-particle permutation model at \(n=6\) with local length-3 reversals produced:

\[
720\text{ states}\rightarrow 20\text{ components of size }36.
\]

Every component is:

- 4-regular,
- 72 edges,
- generated by four length-3 reversal slots,
- regular action of order 36,
- diagnostics matching \(S_3\times S_3\),
- graph-isomorphic to \(C_6\square C_6\).

This shows that the 36-state torus chamber is not isolated to the Hamilton-cycle \(n=9\) preserve-world.

Cautious transfer result:

> The toroidal \(C_6\square C_6\) chamber recurs across related local-reversal preserve-world constructions.

## 16.2 Binary / exclusion lattice-gas reversal dynamics

Binary strings of fixed Hamming weight produce a different regime.

For \(n=8,k=4\), line, length-3 reversals:

- 70 states,
- 5 components,
- proper local subgraph of \(J(8,4)\),
- one 36-state component that is not \(C_6\square C_6\),
- no full Boolean cube of active signatures.

For \(n=10,k=5\), ring, lengths \(2,3\):

- 252 states,
- connected,
- proper local subgraph of \(J(10,5)\),
- 126 active-signature classes,
- every class has size 2,
- every class is exactly a particle-hole complement pair.

Thus the binary/exclusion model produces:

> local Johnson-subgraph dynamics + particle-hole complement quotient.

This is structurally distinct from both the Hamilton-cycle Boolean boundary grammar and the permutation torus decomposition.

---

# 17. Quantum-Walk Fingerprints

Continuous-time quantum walks were used as spectral/interference diagnostics of chamber geometry.

The walk is

\[
\psi(t)=e^{-itA}\psi(0),
\]

where \(A\) is the adjacency matrix of a selected component.

This is not a claim that the graph is a physical quantum system. It is a diagnostic of graph structure.

## 17.1 Summary table

| component | vertices | regular | distinct rounded eigenvalues | mean return | mean IPR | best transfer |
|---|---:|---|---:|---:|---:|---:|
| Hamilton \(n=9\) torus | 36 | yes | 9 | 0.1500416851 | 0.2125075172 | 0.5624400167 |
| Permutation \(n=6\) torus | 36 | yes | 9 | 0.1500416851 | 0.2125075172 | 0.5624400167 |
| Hamilton \(n=9\) regular 144 | 144 | yes | 31 | 0.0405359582 | 0.0686398642 | 0.6200419902 |
| Hamilton \(n=9\) irregular 360 | 360 | no | 349 | 0.0264957779 | 0.0188220044 | 0.0710495720 |

The two torus chambers have identical quantum-walk fingerprints.

Regular chambers show:

- structured spectra,
- stronger spectral degeneracy,
- stronger coherent-transfer signals.

Irregular chambers show:

- near-generic spectra,
- weaker coherent transfer,
- lower mean IPR,
- more dispersive behavior.

Thus:

> local admissibility construction \(\rightarrow\) emergent chamber graph \(\rightarrow\) spectrum \(\rightarrow\) quantum-walk fingerprint.

---

# 18. Raw Move Metric and Pre-Geometric Scaling

Treating one admissible circular reversal as one elementary move-length defines a raw graph metric.

This is a useful metric probe, but it should not be identified directly with physical space.

## 18.1 Exact and sampled metric behavior

Reliable results so far:

- \(n=7\): compact chamber regime,
- \(n=9\): largest chamber shows a short 3D-ish interior growth regime,
- \(n=11\): corrected frontier BFS rises into an approximate 4D range before saturation,
- \(n=13\): corrected frontier BFS rises into a roughly 5D--6D local growth regime depending on move set.

For \(L\le3\), peak local effective dimension grows approximately linearly with \(n\).

Best empirical law so far:

\[
D_{\mathrm{peak}}\approx 0.63n-2.5.
\]

Excluding the small \(n=7\) baseline gives approximately:

\[
D_{\mathrm{peak}}\approx 0.65n-2.8.
\]

## 18.2 Consequence

Rejected naive claim:

> one circular reversal = Planck length, therefore the raw admissible-move graph is physical 3D space.

Supported cautious claim:

> one circular reversal defines primitive microscopic adjacency. The raw admissible-move graph behaves like a growing pre-geometric configuration space. Physical-looking low-dimensional geometry, if present, must emerge through quotienting, coarse-graining, packet projection, slow-mode selection, or observable-level comparison collapse.

This is methodologically important because it prevents overclaiming from the \(n=9\) 3D-ish metric signal.

---

# 19. Growth Embedding Audit

The growth embedding audit tested the proposed odd expansion map:

```text
n -> n + 2
```

by inserting two new labels into canonical Hamilton cycles and measuring whether the four-bit boundary packet is preserved.

The key distinction is between:

```text
core insertion:
  insert both new labels into the target interior/core region

boundary insertion:
  insert at least one new label into a boundary-sensitive region

all insertion:
  all possible insertion positions
```

## 19.1 Exact 7 -> 9 result

For the exact growth step n=7 -> n=9, the core insertion rule gave:

```text
source cycles:                 360
total insertions:              720
unique target cycles:          720
bit preserve rate:             1
hamming change hist:           {0:720}
active count delta hist:       {2:720}
zone hist:                     {core-core:720}
target multiplicity hist:      {1:720}
```

Thus every core insertion preserves the Boolean boundary packet exactly, and every insertion increases active slot count by 2.

The all-insertion rule covered the full n=9 target space:

```text
total insertions:              20160
unique target cycles:          20160
bit preserve rate:             0.281448412698
```

Boundary insertion produced:

```text
total insertions:              19440
unique target cycles:          19440
bit preserve rate:             0.254835390947
```

Therefore packet preservation is special to core insertion, not generic insertion.

## 19.2 Exact 9 -> 11 result

For the exact source enumeration n=9 -> n=11, the core insertion rule again gave:

```text
source cycles:                 20160
total insertions:              241920
unique target cycles:          241920
bit preserve rate:             1
hamming change hist:           {0:241920}
active count delta hist:       {2:241920}
zone hist:                     {core-core:241920}
target multiplicity hist:      {1:241920}
```

Again, every core insertion preserves the Boolean boundary packet exactly and increases active slot count by 2.

The all-insertion rule covered the full n=11 target space:

```text
total insertions:              1814400
unique target cycles:          1814400
bit preserve rate:             0.379320987654
```

Boundary insertion produced:

```text
total insertions:              1572480
unique target cycles:          1572480
bit preserve rate:             0.283831908832
```

Thus the same pattern repeats: core insertion gives exact packet preservation, while boundary insertion frequently changes packet identity.

## 19.3 Interpretation

The growth audit supports the combinatorial expansion picture:

```text
odd n increases
-> new vertices can be inserted into the interior/core
-> the four-bit boundary packet is preserved
-> active core size increases by 2
-> boundary grammar remains stable
```

The exact results for both 7 -> 9 and 9 -> 11 show:

```text
core insertion:
  bit preservation rate = 1
  Hamming change = 0 always
  active count delta = +2 always
```

This gives a precise RAF version of the expansion analogy:

> Odd n-growth can be defined as interior/core expansion that preserves boundary packet identity.

The result does not imply physical cosmological expansion. It gives a mathematical growth embedding between odd preserve-world state spaces.

## 19.4 Important extra observation

The all-insertion rule is bijective onto the full target canonical cycle space in the tested cases:

```text
7 -> 9 all insertion:
  total insertions = 20160
  unique target cycles = 20160

9 -> 11 all insertion:
  total insertions = 1814400
  unique target cycles = 1814400
```

This means every target cycle at n+2 has a unique ancestor under the tested all-insertion deletion map.

So the growth map has two layers:

```text
all insertion:
  covers the whole larger universe exactly once

core insertion:
  selects the packet-preserving expansion channel
```

This is a strong structural result. It suggests that n-growth can be studied as a canonical expansion/deletion relation between odd Hamilton-cycle universes, with core insertion defining the packet-preserving subchannel.

## 19.5 Component Ancestry Under Core Growth

The component ancestry audit tested whether packet-preserving core growth also preserves deeper chamber/component identity.

The audit used exact components for n=7 and n=9:

```text
n=7:
  cycles = 360
  components = 19
  edges = 840
  size histogram = {36:1, 32:1, 28:2, 24:3, 20:3, 16:3, 12:3, 8:2, 4:1}

n=9:
  cycles = 20160
  components = 69
  edges = 67200
  size histogram = {576:1, 540:1, 504:2, 468:3, 432:5, 396:5, 360:7, 324:7, 288:8, 252:7, 216:7, 180:5, 144:5, 108:3, 72:2, 36:1}
```

For the core insertion rule:

```text
descriptors/source:                 2
total insertions:                   720
bit preserve rate:                  1
hamming hist:                       {0:720}
active delta hist:                  {2:720}
target components reached:          38 / 69
source comps with single target:    0
source comps with multiple targets: 19
max target comps from one source:   2
```

Thus core growth does not preserve a single component. Instead, every n=7 component splits into exactly two n=9 components.

The split is highly structured. The weighted source-size to target-size map is:

```text
4  -> 144, 180
8  -> 180, 216
12 -> 216, 252
16 -> 252, 288
20 -> 288, 324
24 -> 324, 360
28 -> 360, 396
32 -> 396, 432
36 -> 432, 468
```

with multiplicities:

```text
24->324: 72, 24->360: 72
20->288: 60, 20->324: 60
28->360: 56, 28->396: 56
16->252: 48, 16->288: 48
12->216: 36, 12->252: 36
32->396: 32, 32->432: 32
36->432: 36, 36->468: 36
8->180:  16, 8->216:  16
4->144:   4, 4->180:   4
```

This suggests an exact size-ladder rule:

```text
source component size s
-> target component sizes 9s + 108 and 9s + 144
```

because:

```text
4  -> 144,180   = 9*4  + 108, 9*4  + 144
8  -> 180,216   = 9*8  + 108, 9*8  + 144
12 -> 216,252   = 9*12 + 108, 9*12 + 144
...
36 -> 432,468   = 9*36 + 108, 9*36 + 144
```

Equivalently, after dividing by 36 where possible, the target sizes advance by one step along the n=9 chamber-size ladder.

For all insertion and boundary insertion, the ancestry spreads broadly:

```text
all insertion:
  target components reached = 69 / 69
  max target comps from one source = 67

boundary insertion:
  target components reached = 69 / 69
  max target comps from one source = 67
```

Therefore the ancestry result is:

```text
core insertion:
  packet-preserving
  each source component splits into exactly two target components
  target component sizes follow a simple affine two-branch ladder

boundary/all insertion:
  packet-disrupting
  component ancestry spreads across almost the whole target component system
```

This is stronger than mere packet preservation. Core growth preserves boundary packet identity and induces a structured two-branch chamber ancestry law.

## 19.6 Exact Size-Ladder Audit

Probe 55 tested the two-branch size-ladder law directly.

The exact n=7 -> n=9 core-growth audit produced:

```text
source_count:                    360
source mode:                     components
descriptors/source:              2
total insertions:                720
unique target count:             720
target multiplicity check:       all unique
bit preserve rate:               1
hamming hist:                    {0:720}
active delta hist:               {2:720}
target components reached:       38 / 69
all sources exactly two targets: True
max targets from one source:     2
affine ladder applicable:        True
affine ladder success:           True
affine ladder formula:           s -> 9*s + 108 and 9*s + 144
```

Thus the n=7 -> n=9 core-growth ladder is not merely visual or heuristic. It is an exact audited component-ancestry law:

```text
source component size s
-> target component sizes 9s + 108 and 9s + 144
```

The mixed n=7 -> n=9 and n=9 -> n=11 run confirmed again that n=9 -> n=11 core growth preserves packet identity exactly:

```text
source_count:                    20160
descriptors/source:              12
total insertions:                241920
unique target count:             241920
target multiplicity check:       all unique
bit preserve rate:               1
hamming hist:                    {0:241920}
active delta hist:               {2:241920}
```

The exact n=11 target-component run was then performed for n=9 -> n=11. It produced:

```text
n=9:
  cycles = 20160
  components = 69
  edges = 67200

n=11:
  cycles = 1814400
  components = 251
  edges = 7862400
```

The n=11 component-size histogram is organized in multiples of 576:

```text
576:1, 1152:2, 1728:3, 2304:5, 2880:7, 3456:9,
4032:11, 4608:14, 5184:16, 5760:18, 6336:19,
6912:20, 7488:20, 8064:19, 8640:18, 9216:16,
9792:14, 10368:11, 10944:9, 11520:7, 12096:5,
12672:3, 13248:2, 13824:1, 14400:1
```

For n=9 -> n=11 core growth:

```text
source_count:                    20160
descriptors/source:              12
total insertions:                241920
unique target count:             241920
target multiplicity check:       all unique
bit preserve rate:               1
hamming hist:                    {0:241920}
active delta hist:               {2:241920}
target components reached:       248 / 251
all sources exactly two targets: False
max targets from one source:     42
affine ladder applicable:        False
```

Thus the simple two-branch affine size ladder is exact for n=7 -> n=9, but it does not generalize unchanged to n=9 -> n=11.

The corrected status is:

```text
Core growth packet preservation:
  confirmed exactly for 7 -> 9 and 9 -> 11

Core growth unique target embedding:
  confirmed exactly for 7 -> 9 and 9 -> 11

Core growth component two-branch ancestry:
  confirmed exactly for 7 -> 9
  false for 9 -> 11

Core growth affine two-branch size ladder:
  confirmed exactly for 7 -> 9
  false for 9 -> 11
```

This weakens the simple ladder conjecture but strengthens the broader expansion picture. The robust law is not two-branch chamber ancestry. The robust law is:

```text
core growth
-> preserves boundary packet identity
-> inserts new interior degrees of freedom uniquely
-> increases active count by +2
-> maps into a highly structured but increasingly branching component ancestry system
```

At n=9 -> n=11, almost every n=11 component is reached by core descendants:

```text
target components reached = 248 / 251
```

so core growth is no longer a narrow two-branch channel at component level. It becomes a broad packet-preserving expansion channel across the larger chamber system.

## 19.7 Branching Structure of n=9 -> n=11 Core Growth

Probe 56 analyzed the exact n=9 -> n=11 core-growth branching matrix from Probe 55.

The global result was:

```text
source components:         69
target components reached: 248 / 251
target coverage:           0.988048
bit preserve rate:         1.0
hamming hist:              {0:241920}
active delta hist:         {2:241920}
```

The branch-count histogram was:

```text
{42:53, 40:9, 33:6, 26:1}
```

Thus most n=9 source components reach exactly 42 n=11 target components under core growth.

The source-size branch summary was:

```text
s=36:  branches=26,    target sizes 1152..8064
s=72:  branches=33,    target sizes 576..8640
s=108: branches=33..40,target sizes 576..9216
s=144: branches=33..42,target sizes 576..9792
s=180: branches=40..42,target sizes 576..10368
s=216: branches=40..42,target sizes 1152..10944
s=252: branches=40..42,target sizes 1728..11520
s=288: branches=42,    target sizes 2304..12096
s=324: branches=42,    target sizes 2880..12672
s=360: branches=42,    target sizes 3456..13248
s=396: branches=42,    target sizes 4032..13824
s=432: branches=42,    target sizes 4608..14400
s=468: branches=42,    target sizes 5184..14400
s=504: branches=42,    target sizes 5760..14400
s=540: branches=42,    target sizes 6336..14400
s=576: branches=42,    target sizes 6912..14400
```

The branching is therefore not random. It has a saturation profile:

```text
small/source-boundary components:
  fewer reachable target components

large/interior source components:
  saturated branch count of 42
```

The affine residual diagnostic showed that no simple one-line affine law replaces the n=7 -> n=9 two-branch ladder:

```text
A=9:  B_support=265
A=20: B_support=84
A=24: B_support=50
A=25: B_support=265
A=36: B_support=132
```

Among tested slopes, A=24 gave the smallest residual support, suggesting that the n=9 -> n=11 branching may be organized by multiple bands around a slope-24 size relation rather than a two-branch affine law.

The corrected growth picture is now:

```text
7 -> 9:
  exact packet-preserving core growth
  exact two-target component branching
  exact affine two-branch size ladder

9 -> 11:
  exact packet-preserving core growth
  exact unique target embedding
  broad component branching
  branch-count saturation at 42 for most source components
  no simple global affine two-branch size law
```

This suggests a transition from small-scale chamber splitting to large-scale packet-preserving expansion across a broad chamber ensemble.

## 19.8 Small-n Emergence Atlas

Probe 57 generated a small-n RAF emergence atlas for the Hamilton-cycle admissibility programme.

The safe run used:

```bash
python3 57_odd_small_n_emergence_atlas.py \
  --n-max 11 \
  --graph-up-to 9 \
  --growth-source-up-to 9 \
  --out-dir runs/odd_small_n_emergence_atlas \
  --write-csv
```

The computed small-n ladder was:

```text
n=3:
  raw vertices = 1
  raw edges = 0
  raw components = 1
  interpretation = first Hamilton closure, but unique modulo rotation/reflection

n=4:
  raw vertices = 3
  raw edges = 3
  raw components = 1
  degree hist = {2:3}
  interpretation = first nontrivial Hamilton-cycle comparison graph

n=5:
  raw vertices = 12
  raw edges = 30
  raw components = 1
  raw degree hist = {5:12}

  preserve-world vertices = 12
  preserve-world edges = 8
  preserve-world components = 5
  component size hist = {4:1, 3:1, 2:2, 1:1}
  degree hist = {2:5, 1:6, 0:1}
  interpretation = first small odd preserve-world, still exceptional

n=6:
  raw vertices = 60
  raw edges = 270
  raw components = 1
  raw degree hist = {9:60}

n=7:
  raw vertices = 360
  raw edges = 2520
  raw components = 1
  raw degree hist = {14:360}

  preserve-world vertices = 360
  preserve-world edges = 840
  preserve-world components = 19
  component size hist = {36:1, 32:1, 28:2, 24:3, 20:3, 16:3, 12:3, 8:2, 4:1}
  degree hist = {6:76, 5:128, 4:120, 3:32, 2:4}
  boundary grammar violations = 0
  active grammar violations = 0
  packet formula pass = True
  interpretation = first stable odd four-bit boundary grammar

n=8:
  raw vertices = 2520
  raw edges = 20160
  raw components = 1
  raw degree hist = {16:2520}

n=9:
  raw vertices = 20160
  raw edges = 181440
  raw components = 1
  raw degree hist = {18:20160}

  preserve-world vertices = 20160
  preserve-world edges = 67200
  preserve-world components = 69
  component size hist = {576:1, 540:1, 504:2, 468:3, 432:5, 396:5, 360:7, 324:7, 288:8, 252:7, 216:7, 180:5, 144:5, 108:3, 72:2, 36:1}
  degree hist = {8:4256, 7:7168, 6:6720, 5:1792, 4:224}
  boundary grammar violations = 0
  active grammar violations = 0
  packet formula pass = True
  interpretation = mature odd packet transport kernel regime
```

The core-growth checks in the atlas were:

```text
7 -> 9:
  descriptors/source = 2
  total insertions = 720
  unique targets = 720
  bit preserve rate = 1.0
  hamming hist = {0:720}
  branch count hist = {2:19}

9 -> 11:
  descriptors/source = 12
  total insertions = 241920
  unique targets = 241920
  bit preserve rate = 1.0
  hamming hist = {0:241920}
  branch count hist = not computed in safe run
```

This gives the first clean internal “small-n emergence ladder”:

```text
no distinction
-> first distinction
-> first relation
-> first Hamilton closure
-> first nontrivial comparison graph
-> first small odd preserve-world
-> first stable boundary grammar
-> mature packet transport
-> broad chamber ensemble and core-growth expansion
```

The result supports the configuration-space interpretation:

> The raw Hamilton-cycle systems should not be read directly as physical space. They are better treated as pre-geometric comparison/configuration spaces from which lower-dimensional quotient or coarse-grained effective graphs may later emerge.

This is the safest current bridge toward Big-Bang-style thinking. The small-n sequence gives a staged emergence structure, while the physical cosmology comparison remains a later and separate test.

## 19.9 Large-n Retraction / Insertion “Magic Trick” Audit

Probe 58 tested the large-n insertion/deletion retraction idea:

```text
Omega_{n+2}
-> delete newest labels n+1,n+2
-> recover an Omega_n source cycle
-> classify whether the deleted labels were core/core or boundary-touching
-> compare the source and target four-bit boundary packets
```

The theoretical descriptor counts are:

```text
D_all(n)  = n(n+1)
D_core(n) = (n-5)(n-6)
```

so the core fraction is:

```text
f_core(n) = (n-5)(n-6) / (n(n+1))
```

and the non-core fraction is:

```text
1 - f_core(n) = (12n - 30) / (n(n+1)) ~ 12/n
```

The exact runs gave:

```text
n=7 -> 9:
  target_seen:              20160
  D_all:                    56
  D_core:                   2
  theory core_fraction:      0.0357142857143
  observed core_fraction:    0.0357142857143
  overall packet preserve:   0.281448412698
  core packet preserve:      1
  noncore packet preserve:   0.254835390947
  hamming_hist:              {0:5674, 1:8052, 2:4892, 3:1324, 4:218}
  deletion uniform fibre:    True, fibre_size_hist={56:360}

n=9 -> 11:
  target_seen:              1814400
  D_all:                    90
  D_core:                   12
  theory core_fraction:      0.133333333333
  observed core_fraction:    0.133333333333
  overall packet preserve:   0.379320987654
  core packet preserve:      1
  noncore packet preserve:   0.283831908832
  hamming_hist:              {0:688240, 1:668192, 2:355936, 3:88032, 4:14000}
  deletion uniform fibre:    True, fibre_size_hist={90:20160}
```

The sampled large-n runs gave:

```text
n=11 -> 13:
  theory core_fraction:     0.227272727273
  observed core_fraction:   0.22826
  overall packet preserve:  0.4556
  core packet preserve:     1
  noncore packet preserve:  0.294581076528

n=13 -> 15:
  theory core_fraction:     0.307692307692
  observed core_fraction:   0.307
  overall packet preserve:  0.52172
  core packet preserve:     1
  noncore packet preserve:  0.309841269841

n=15 -> 17:
  theory core_fraction:     0.375
  observed core_fraction:   0.37062
  overall packet preserve:  0.57032
  core packet preserve:     1
  noncore packet preserve:  0.31729638692

n=21 -> 23:
  theory core_fraction:     0.519480519481
  observed core_fraction:   0.5229
  overall packet preserve:  0.67776
  core packet preserve:     1
  noncore packet preserve:  0.324586040662

n=51 -> 53:
  theory core_fraction:     0.780542986425
  observed core_fraction:   0.78218
  overall packet preserve:  0.85582
  core packet preserve:     1
  noncore packet preserve:  0.338077311542

n=101 -> 103:
  theory core_fraction:     0.885264997088
  observed core_fraction:   0.8856
  overall packet preserve:  0.92684
  core packet preserve:     1
  noncore packet preserve:  0.36048951049
```

The core preservation law survived every exact and sampled test:

```text
core packet preserve = 1
```

The large-n pattern is therefore:

```text
n increases
-> probability newest labels lie in the core increases
-> core deletion/reinsertion preserves the boundary packet exactly
-> non-core/boundary disturbance is suppressed approximately like O(1/n)
-> overall packet preservation tends toward 1
```

The sampled n=101 -> 103 case already has:

```text
core fraction ≈ 0.8856
overall packet preserve ≈ 0.92684
```

This supports the retraction/renormalisation interpretation:

> At packet level, large odd preserve-worlds can be reduced by deleting the newest core labels, computing the smaller boundary packet, and reinserting the deleted labels. The error channel is boundary-touching insertion, whose frequency decreases roughly like 12/n before accounting for the fact that some boundary-touching insertions also preserve the packet.

Important caution:

```text
This is a packet-level reduction theorem candidate.
It is not a full component/chamber reduction, because component ancestry becomes broad by n=9 -> n=11.
```

So the strongest current statement is:

```text
Large-n Odd Preserve-World admits an asymptotically exact packet-level retraction:
large n boundary behaviour = smaller-n boundary packet + mostly invisible core insertion/deletion + O(1/n) boundary disturbance.
```

---

# 20. Theorem-Style Results Currently Supported

## Result 1: n=9 odd preserve-world decomposition

The \(n=9\) odd preserve-world graph has:

\[
20160\text{ vertices},
\qquad
67200\text{ edges},
\qquad
69\text{ connected components}.
\]

## Result 2: regular and toroidal chambers

Among the \(n=9\) components are:

- a 576-state regular chamber with local-slot action diagnostics consistent with \(S_4\times S_4\),
- two regular outer 144-state chambers with local-slot action diagnostics consistent with \(S_3\times S_4\),
- a 36-state chamber isomorphic to \(C_6\square C_6\).

## Result 3: corrected 144-sector taxonomy

The \(n=9\) 144-state sector contains five chambers arranged as:

\[
A\;--\;B\;--\;C\;--\;B'\;--\;A'.
\]

The outer pair \(A,A'\) are regular. The intermediate pair \(B,B'\) are mixed-degree abstract graph twins. The central chamber \(C\) is a mixed-degree singleton.

## Result 4: signature quotient families

Exact slot-signature quotienting reduces the 69 connected components to 42 quotient-skeleton families:

\[
15\text{ singleton families}+27\text{ multiplicity-2 families}.
\]

## Result 5: Boolean active-slot grammar

At \(n=7\) and \(n=9\), the active-slot pattern space is exactly a Boolean 4-cube:

\[
\mathrm{ACTIVE}(c)=\mathrm{CORE}_n\cup S(c),
\qquad
S(c)\subseteq\mathrm{OPTIONAL}_n.
\]

Sampled evidence supports the same law at \(n=11,13,15\).

## Result 6: Boolean transition rule at n=9

The \(n=9\) Boolean transition graph has all 32 Hamming-1 edges, 24 of 48 Hamming-2 edges, 8 of 32 Hamming-3 edges, and no Hamming-4 edges. Transition existence is governed by an exact Boolean precondition table over source bits and XOR masks.

## Result 7: stable boundary MSM regime for n≥9

For \(n=9,11,13\), the Boolean boundary packet quotient appears to enter a stable effective four-spin boundary MSM regime with:

- Hamming-1 dominated transitions,
- no Hamming-4 transitions,
- strongly pairwise Ising-like stationary energy,
- stable square-symmetric Ising parameters,
- slowest mode aligned with \(b_0-b_1+b_2-b_3\).

---

# 21. Open Problems

Immediate proof targets:

1. Prove the odd Boolean active-slot grammar for all odd \(n\ge7\).
2. Prove the CORE/OPTIONAL/FORBIDDEN slot-role law.
3. Prove the optional \(2/3\) marginal law.
4. Derive the \(n=9\) Boolean transition precondition table directly from the local reversal rule.
5. Prove or explain the 36-divisibility of \(n=9\) component sizes.
6. Prove or explain the 4-divisibility of exact slot-signature class sizes.
7. Produce formal group-isomorphism certificates for the 576 and regular 144 chambers.
8. Determine whether the 144-sector \(A/B/C/B'/A'\) taxonomy generalizes.
9. Determine whether the boundary Ising/Glauber-like MSM persists at \(n=15\) and beyond.
10. Fit limiting Ising parameters as \(n\to\infty\).
11. Compute committors between staggered packet regions.
12. Compare MSM slow modes with quantum-walk localization.
13. Search for \(\sigma_R\)-compatible cyclic Gray codes.
14. Characterize the raw move metric as a pre-geometric configuration metric.
15. Identify the quotient or observable layer, if any, that produces stable low-dimensional geometry.

---

# 22. Conservative Interpretation Without EHF Language

A conservative graph-theory formulation is:

> We study graphs whose vertices are canonical Hamiltonian cycles on \(K_n\), with edges generated by local circular segment reversals of lengths 2 and 3, filtered in the odd case by preservation of a parity-position invariant. At \(n=9\), the resulting graph has 20160 vertices, 67200 edges, and 69 connected components. Its chamber structure includes regular Cayley-action chambers, a toroidal \(C_6\square C_6\) chamber, mixed-degree irregular chambers stratified by local move-survival signatures, and an exact Boolean 4-cube of global active-slot patterns. Coarse-graining by Boolean packets gives a reversible 16-state Markov model with Ising-like stationary structure and a stable staggered slow mode for \(n\ge9\).

---

# 23. Relationship to the Johnson Transport Core

The odd preserve-world and the even Johnson transport core are related, but they are not the same reduction.

Both begin from the RAF programme:

```text
Hamilton-cycle local admissibility
-> reduced comparison structure
-> coarse observables
-> effective dynamics
```

However, they currently use different quotient/coarse-graining maps.

## 22.1 Even Johnson reduction

In the even case, parity-sector reduction and subset encoding lead to the Johnson-type state space:

```text
Omega_k = k-subsets of [2k-1]
```

with single-swap Johnson adjacency:

```text
S -> S' where |S cap S'| = k - 1
```

The natural coarse observables are shell moments such as:

```text
h(S) = sum of labels in S
q(S) = sum of squared labels in S
```

This gives an exact low-moment transport theory: exact drift, exact state diffusion, exact shell diffusion through the conditional moment E[q | h], and exact generating-function counting.

## 22.2 Odd folded Johnson-type reduction

The Johnson-style emergence is not strictly limited to even n. At the sector-configuration level, odd n has a natural complement-folded Johnson-type parent:

```text
k-subsets of [2k], modulo S ~ complement(S)
```

This folded subset geometry is a different reduction from the odd preserve-world chamber graph studied in this document.

Thus the careful statement is:

> Even n gives the clean unfolded Johnson transport benchmark. Odd n admits folded Johnson-type subset reductions, but the odd preserve-world chamber/Boolean analysis is not yet proved to be equivalent to a folded Johnson transport theory.

## 22.3 Odd Boolean boundary reduction

The odd preserve-world document studies a different coarse-graining: active local-slot signatures.

For odd n >= 7, the active slots appear to have the form:

```text
ACTIVE(c) = CORE_n union S(c), where S(c) is a subset of OPTIONAL_n
```

where OPTIONAL_n has four elements.

Therefore the packet labels form a Boolean 4-cube:

```text
S(c) in 2^OPTIONAL_n, equivalent to {0,1}^4
```

This can be viewed as a subset model on a four-element boundary set, but it is not a fixed-weight Johnson graph.

Its Hamming-weight layers are Johnson-like layers, but the full Boolean packet dynamics includes transitions between layers and conditional multi-bit transitions. Therefore the correct current description is:

> The odd Boolean grammar is a boundary Boolean-cube coarse-graining with Johnson-like layers, not a Johnson shell transport theory.

## 22.4 Coarse observable comparison

The even Johnson transport core uses scalar shell observables:

```text
h(S), q(S)
```

The odd preserve-world uses a boundary packet observable:

```text
b(c) = (b0,b1,b2,b3) in {0,1}^4
```

These are different coarse-grainings of Hamilton-cycle admissibility.

The closest odd-side analogues of even-side shell observables are not yet settled, but candidates include:

```text
|b| = b0 + b1 + b2 + b3
E(b) = -log pi(b)
staggered mode = b0 - b1 + b2 - b3
```

Thus the relationship is not:

```text
odd Boolean grammar = Johnson shell theory
```

The relationship is instead:

```text
even side: fixed-weight subset quotient -> exact shell transport
odd side: boundary active-slot quotient -> Boolean packet MSM
```

Both are RAF coarse-grainings of Hamilton-cycle admissibility, but they expose different effective variables.

## 22.5 Bridge question

The main bridge problem is:

> Can the odd Boolean packet dynamics be given an exact counting, generating-function, or moment-closure theory analogous to the even Johnson shell drift/diffusion theory?

A second bridge problem is:

> Can the even Johnson transport core be enriched with chamber, packet, or boundary-signature structure analogous to the odd preserve-world?

Until those problems are solved, the documents should present the even and odd theories as complementary RAF reductions rather than as the same object.

---

# 24. Relationship to the Emergent Horizon Framework

The odd preserve-world results are relevant to EHF only after the mathematical structure is stated on its own.

The RAF result is:

\[
\text{local Hamilton-cycle admissibility}
\rightarrow
\text{chambers}
\rightarrow
\text{slot signatures}
\rightarrow
\text{Boolean boundary packets}
\rightarrow
\text{coarse MSM}
\rightarrow
\text{effective boundary spin dynamics}.
\]

This strengthens the mathematical foundation available to EHF because it shows that local admissible comparison can produce:

- chamber worlds,
- residual symmetries,
- boundary/interior decomposition,
- robust distributed packets,
- reversible coarse dynamics,
- Ising-like stationary structure,
- slow collective modes,
- and Gray-code-compatible boundary histories.

However, these results do not prove a physical theory.

They do not yet identify:

- what the Hamilton-cycle states physically represent,
- whether the Boolean boundary bits correspond to physical degrees of freedom,
- whether the staggered slow mode corresponds to any physical time-like structure,
- whether the raw or quotient metric corresponds to physical space,
- or whether nature realizes this preserve-world construction.

The correct current status is:

> RAF has found a rich odd preserve-world chamber and boundary dynamics.  
> EHF may use this as a candidate mathematical substrate for emergent-geometry interpretation.  
> The physical interpretation remains separate, tentative, and unproven.

The strongest EHF-compatible but cautious emergence chain is:

\[
\text{Hamilton-cycle microstates}
\rightarrow
\Pi\text{-preserving local admissibility}
\rightarrow
\text{Boolean boundary active-slot packets}
\rightarrow
\text{reversible 16-state MSM}
\rightarrow
\text{effective 4-spin Ising-like boundary Hamiltonian}
\rightarrow
\text{slow staggered collective mode}.
\]

This should be treated as a mathematical emergence chain, not as a claim that spacetime has been derived.

---

# 25. Summary

The odd preserve-world side of RAF now has a coherent structure:

- exact small-n component decompositions,
- a fully enumerated \(n=9\) chamber landscape,
- regular Cayley-action chambers,
- a toroidal \(C_6\square C_6\) endpoint chamber,
- corrected five-chamber 144-sector taxonomy,
- irregular chambers stratified by local move-survival signatures,
- exact slot-signature quotient families,
- exact Boolean 4-cube active-slot grammar at \(n=7,9\),
- sampled Boolean grammar support at \(n=11,13,15\),
- exact \(n=9\) Boolean transition rules,
- robust distributed Boolean packets,
- a reversible packet MSM,
- an effective Ising/Glauber-like boundary dynamics for \(n\ge9\),
- a stable staggered slow mode,
- Gray-code-compatible boundary traversal,
- and metric-scaling evidence that raw move distance is pre-geometric.

The odd preserve-world is therefore no longer just an exploratory anomaly. It is an organized RAF sector with exact finite data, stable boundary grammar, and several clear theorem candidates.

Its next stage should be proof, compression, and generalization.

