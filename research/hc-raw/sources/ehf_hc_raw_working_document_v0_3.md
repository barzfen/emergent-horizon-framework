# EHF-HC-RAW — Raw Hamilton-Cycle Comparison Space
## Working Document

**Programme:** Emergent Horizon Framework  
**Branch:** Foundational rebuild / raw Hamilton-cycle substrate  
**Version:** v0.2  
**Date:** 24 August 2026  
**Status:** Living research document  

---

# 1. Purpose

This document begins the reconstruction of the Hamilton-cycle layer from scratch.

The aim is to isolate what is already true of the raw Hamilton-cycle state space **before** adding:

- LR3;
- LR2;
- 2-opt dynamics;
- parity or \(\Pi\) sectors;
- OPW restrictions;
- Johnson reductions;
- growth \(n\to n+1\);
- probabilities or amplitudes;
- spectral operators;
- curvature;
- physical interpretation.

The guiding separation is:

\[
\boxed{\text{raw state object} \neq \text{chosen admissible move rule} \neq \text{physical dynamics}.}
\]

Earlier EHF/RAF documents often began from Hamilton cycles and immediately added a move rule. The present rebuild inserts a new layer underneath those constructions:

\[
\boxed{HC_n\text{ alone}.}
\]

The central question is:

> **What structural facts follow from the raw class of undirected cyclic orderings itself, without choosing how one state may transform into another?**

---

# 2. Dependency lock

The present hierarchy is provisionally:

```text
EHF admissible-comparison foundation
    ↓
distinguishable labels V_n
    ↓
raw undirected cyclic comparison states HC_n
    ├── candidate same-layer rule: LR3
    ├── alternative same-layer rule: 2-opt
    └── candidate cross-layer rule: all-slot insertion HC_n -> HC_{n+1}
            ↓
    derived sectors / quotients / OPW / Johnson / spectra / amplitudes / etc.
```

This changes the wording of some earlier working documents.

The raw Hamilton-cycle object is not LR3. LR3 is a candidate admissibility rule acting **on** the raw object.

Similarly, Core C is not the raw object. Core C studies the raw states after equipping them with 2-opt adjacency.

---

# 3. Raw object without assuming a physical complete graph

Let

\[
V_n=\{0,1,\ldots,n-1\}
\]

be a set of \(n\) distinguishable labels.

At the foundational level the labels are not assumed to be:

- points in physical space;
- particles;
- events;
- spatial sites;
- physical objects of any particular kind.

They are placeholders for distinguishable relational sites in the finite mathematical laboratory.

A raw Hamilton-cycle state can be defined directly as an **undirected cyclic ordering** of all labels.

The common phrase “Hamilton cycle on \(K_n\)” is equivalent combinatorial bookkeeping, but the complete graph \(K_n\) need not be interpreted as a physically fundamental all-to-all comparison graph.

This distinction is important because the foundation should not silently assume complete physical comparability before admissibility has been specified.

---

# 4. Presentation space and dihedral quotient

A linear presentation of a cyclic ordering is

\[
(v_0,v_1,\ldots,v_{n-1}).
\]

The same undirected cycle has:

- \(n\) possible starting positions;
- two orientations.

Thus there are \(2n\) presentations of the same labelled undirected cycle.

The intrinsic raw state is the equivalence class under the dihedral action:

\[
HC_n = \{\text{linear orderings of }V_n\}/D_n.
\]

Computationally, one convenient chart is:

1. rotate label \(0\) into position \(0\);
2. compare the two anchored orientations;
3. retain the lexicographically smaller orientation.

This chart is a representation convention, not additional structure in the cycle.

For distinct labels and \(n\ge3\), every orbit has size \(2n\). Therefore:

\[
\boxed{|HC_n|=\frac{n!}{2n}=\frac{(n-1)!}{2}.}
\]

This is an elementary exact count.

---

# 5. A raw cycle as a closed local relation

For a state \(C\in HC_n\), define its undirected edge set

\[
E(C)=\{\{v_i,v_{i+1}\}:i\in\mathbb Z_n\}.
\]

Then:

\[
|E(C)|=n.
\]

Every label occurs in exactly two selected pair-relations:

\[
\deg_C(v)=2\qquad\forall v\in V_n.
\]

The relation is connected and closed.

Thus a Hamilton cycle supplies a particularly simple finite form of constrained local relation:

\[
\boxed{
\text{all labels participate, every label has two local partners, and the relation closes into one component.}
}
\]

This does **not** establish that degree two, cyclicity, or Hamilton cycles are physically fundamental. It states why the object is a useful first comparison laboratory.

Important open questions remain:

- Why degree exactly two?
- Why connectedness?
- Why one cycle rather than a path, tree, matching, or union of cycles?
- Which later EHF structures genuinely depend on cyclicity?

These questions must remain visible rather than being hidden inside the definition.

---

# 6. What has not yet been supplied

The raw set \(HC_n\) alone does **not** specify a dynamics between its states.

At this stage there is no declaration that two distinct cycles are neighbours in a state-transition graph.

In particular, we have not yet supplied:

\[
\mathrm{LR3},\quad
\mathrm{LR2},\quad
\mathrm{2opt},\quad
\Pi,\quad
\text{OPW},\quad
\text{Johnson adjacency}.
\]

Nor have we supplied:

\[
P(C\to C'),\quad A(C\to C'),\quad E(C),\quad S[C],
\]

or any other physical weighting.

The raw object therefore cleanly separates:

\[
\boxed{\text{configuration structure from transition admissibility}.}
\]

---

# 7. Raw comparison between two cycle states

Even without a dynamical move rule, two states can be compared structurally.

For \(C,D\in HC_n\), define the edge overlap

\[
o(C,D)=|E(C)\cap E(D)|.
\]

Since both states contain exactly \(n\) edges, define the raw edge-symmetric-difference distance

\[
d_E(C,D)
=\frac12|E(C)\triangle E(D)|
=n-o(C,D).
\]

This is a state-comparison statistic, not yet a transition distance.

A later move rule may select one or more layers of this raw comparison structure. For example, 2-opt neighbours have overlap \(n-2\), but that is a later admissibility choice rather than part of the definition of \(HC_n\).

---

# 8. EHF-HC-RAW-01
## Definition Lock, Dihedral Quotient, Incidence Neutrality, and Raw Overlap Census

### 8.1 Purpose

The first probe asks what exact symmetry and incidence structure is already present in \(HC_n\).

No LR3, LR2, 2-opt, sector map, growth rule, stochastic kernel, or physical interpretation is used.

### 8.2 Script

```text
ehf_hc_raw_01_definition_lock_incidence_overlap_census.py
```

### 8.3 Reference command

```bash
python3 ehf_hc_raw_01_definition_lock_incidence_overlap_census.py \
  --n-min 4 \
  --n-max 10 \
  --out-dir runs/ehf_hc_raw_01 \
  --strict
```

### 8.4 Strict checks

For each \(n\), the probe checks:

1. exact state count \((n-1)!/2\);
2. agreement of anchored canonicalisation with direct dihedral canonicalisation;
3. exactly \(n\) edges and degree two at every label;
4. uniform incidence of every unordered label pair;
5. exact adjacent-edge-pair incidence;
6. exact disjoint-edge-pair incidence;
7. several instances of the forced-linear-forest count;
8. exact first two moments of raw edge overlap;
9. impossibility of overlap \(n-1\) for distinct cycles;
10. source-independence of the overlap distribution for several deterministic source states.

---

# 9. HC-RAW-01 result

The strict audit passes for

\[
\boxed{n=4,5,6,7,8,9,10.}
\]

Verdict:

```text
EHF_HC_RAW_01_DEFINITION_INCIDENCE_OVERLAP_PASS
```

Summary:

| \(n\) | \(|HC_n|\) | fixed-edge incidence | adjacent pair | disjoint pair | mean overlap | overlap variance |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 3 | 2 | 1 | 2 | 2.666666667 | 0.888888889 |
| 5 | 12 | 6 | 2 | 4 | 2.500000000 | 1.250000000 |
| 6 | 60 | 24 | 6 | 12 | 2.400000000 | 1.440000000 |
| 7 | 360 | 120 | 24 | 48 | 2.333333333 | 1.555555556 |
| 8 | 2520 | 720 | 120 | 240 | 2.285714286 | 1.632653061 |
| 9 | 20160 | 5040 | 720 | 1440 | 2.250000000 | 1.687500000 |
| 10 | 181440 | 40320 | 5040 | 10080 | 2.222222222 | 1.728395062 |

---

# 10. Exact incidence neutrality

Fix an unordered label pair

\[
e=\{a,b\}.
\]

The number of undirected Hamilton cycles containing \(e\) is

\[
\boxed{N(e)=(n-2)!.}
\]

One way to see this is to contract \(a-b\) into one oriented block. There are two internal orientations of the block and \((n-2)!/2\) undirected cycles on the resulting \(n-1\) objects, giving \((n-2)!\).

Equivalently, because there are \(|HC_n|\) states, each containing \(n\) edges, total edge incidences are

\[
n|HC_n|=n\frac{(n-1)!}{2}.
\]

There are \(\binom n2\) possible unordered pairs. Relabelling symmetry forces equal incidence, so

\[
\frac{n(n-1)!/2}{\binom n2}=(n-2)!.
\]

Therefore, for a uniformly selected raw state,

\[
\boxed{
\Pr(e\in E(C))
=\frac{(n-2)!}{(n-1)!/2}
=\frac{2}{n-1}.
}
\]

This is the first exact neutrality law of the raw substrate:

> **No unordered pair of labels is privileged by the raw Hamilton-cycle ensemble.**

The statement concerns label symmetry. It does not imply that all multi-edge patterns occur equally often.

---

# 11. Relational correlations already exist before dynamics

Neutrality of individual labels and edges does **not** make the raw object structureless.

Fix two required edges.

## 11.1 Adjacent required edges

For

\[
\{a,b\},\qquad\{b,c\},
\]

which form a path of length two, the number of cycles containing both is

\[
\boxed{N_{\rm adjacent}=(n-3)!.}
\]

## 11.2 Disjoint required edges

For disjoint edges

\[
\{a,b\},\qquad\{c,d\},
\]

the number of cycles containing both is

\[
\boxed{N_{\rm disjoint}=2(n-3)!.}
\]

Therefore:

\[
\boxed{N_{\rm disjoint}=2N_{\rm adjacent}.}
\]

This is important conceptually.

The raw ensemble is label-neutral, but it distinguishes **relational incidence type**.

The system does not care which labels are used, yet it does care whether two proposed relations meet at a common label.

That is genuine structure before any between-state dynamics is chosen.

---

# 12. Forced linear-forest counting law

The pair-incidence laws are instances of a more general counting principle.

Let \(F\) be a fixed set of \(k\) required edges forming a linear forest with \(c\) nontrivial path components. For the ordinary contraction regime \(n-k\ge3\), contract each path component into one block.

Each path component has two internal orientations. The contraction leaves

\[
n-k
\]

objects.

Hence the number of Hamilton cycles containing \(F\) is

\[
2^c\frac{(n-k-1)!}{2},
\]

so

\[
\boxed{
N(F)=2^{c-1}(n-k-1)!.
}
\]

HC-RAW-01 checks representative cases including:

- one forced edge;
- two adjacent forced edges;
- two disjoint forced edges;
- a three-edge path;
- a two-edge path plus one disjoint edge;
- a three-edge matching;
- a triangle as an impossible control.

The finite checks pass through \(n=10\).

A proper theorem statement should handle the small contracted boundary cases separately and state explicitly that forced proper cycles are impossible inside a larger Hamilton cycle.

---

# 13. Raw overlap distribution

For a fixed source state \(C\), define

\[
M_n(r)
=
|\{D\in HC_n:o(C,D)=r\}|.
\]

Relabelling transitivity of \(HC_n\) implies that this distribution does not depend on the choice of \(C\).

The probe also checks this directly against several source states at every audited \(n\).

Exact enumerated distributions are:

### \(n=4\)

\[
M_4(2)=2,\qquad M_4(4)=1.
\]

### \(n=5\)

\[
M_5(0)=1,
\quad M_5(2)=5,
\quad M_5(3)=5,
\quad M_5(5)=1.
\]

### \(n=6\)

\[
(M_6(0),M_6(1),M_6(2),M_6(3),M_6(4),M_6(6))
=(3,12,15,20,9,1).
\]

### \(n=7\)

\[
(M_7(0),M_7(1),M_7(2),M_7(3),M_7(4),M_7(5),M_7(7))
=(23,70,112,91,49,14,1).
\]

### \(n=8\)

\[
(M_8(0),\ldots,M_8(6),M_8(8))
=(177,544,740,640,302,96,20,1).
\]

### \(n=9\)

\[
(M_9(0),\ldots,M_9(7),M_9(9))
=(1553,4500,6003,4725,2439,747,165,27,1).
\]

### \(n=10\)

\[
(M_{10}(0),\ldots,M_{10}(8),M_{10}(10))
=
(14963,41740,53585,41420,20810,7076,1550,260,35,1).
\]

Observed finite support law:

- \(n=4\): overlaps \(2,4\);
- \(n=5\): overlaps \(0,2,3,5\);
- every audited \(n\ge6\): all overlaps
  \[
  0,1,\ldots,n-2,n
  \]
  occur;
- overlap \(n-1\) never occurs.

The all-\(n\ge6\) support statement is currently an audited finite pattern, not yet promoted here to a general theorem.

---

# 14. Exact first moment of raw overlap

Let

\[
X=o(C,D)
\]

where \(C\) is fixed and \(D\) is uniform on \(HC_n\).

The reference cycle has \(n\) edges. Each one occurs in \(D\) with probability

\[
p=\frac{2}{n-1}.
\]

Therefore

\[
\boxed{
\mathbb E[X]
=n\frac{2}{n-1}
=\frac{2n}{n-1}.
}
\]

Thus:

\[
\mathbb E[X]\to2
\qquad(n\to\infty).
\]

Two uniformly related raw cycle states share only about two edges on average at large \(n\), even though each state itself contains \(n\) local relations.

This is a combinatorial statement only. No dynamical or physical interpretation is assigned.

---

# 15. Exact second moment and variance

Among pairs of distinct edges of a fixed reference cycle:

- exactly \(n\) unordered pairs are adjacent along the cycle;
- exactly
  \[
  \binom n2-n=\frac{n(n-3)}2
  \]
  are disjoint.

The joint inclusion probabilities are:

\[
p_{\rm adjacent}
=\frac{(n-3)!}{(n-1)!/2}
=\frac{2}{(n-1)(n-2)},
\]

and

\[
p_{\rm disjoint}
=\frac{2(n-3)!}{(n-1)!/2}
=\frac{4}{(n-1)(n-2)}.
\]

Therefore

\[
\mathbb E\binom X2
=
np_{\rm adjacent}
+
\frac{n(n-3)}2p_{\rm disjoint}
=\frac{2n}{n-1}.
\]

Hence

\[
\mathbb E[X(X-1)]
=\frac{4n}{n-1},
\]

and

\[
\mathbb E[X^2]
=\frac{6n}{n-1}.
\]

Thus

\[
\boxed{
\operatorname{Var}(X)
=\frac{2n(n-3)}{(n-1)^2}.
}
\]

The probe reproduces this exactly to floating-point roundoff for every audited \(n\).

As \(n\to\infty\):

\[
\operatorname{Var}(X)\to2.
\]

This makes a Poisson-like large-\(n\) overlap law with mean near 2 an obvious future asymptotic question, but no Poisson limit is claimed here.

---

# 16. Why overlap \(n-1\) is impossible

Suppose two undirected Hamilton cycles shared \(n-1\) of their \(n\) edges.

The shared edge set would be a spanning path obtained by deleting one edge from either cycle. The two endpoints of that path each require one additional incident edge to restore degree two and close the cycle.

There is only one unordered edge joining those two endpoints.

Therefore both cycles must contain the same final edge and are identical.

Hence:

\[
\boxed{
C\ne D\quad\Longrightarrow\quad o(C,D)\ne n-1.
}
\]

The nearest possible distinct raw overlap is therefore \(n-2\), the layer later selected by 2-opt adjacency.

---

# 17. Raw symmetric-difference distance

Because

\[
d_E(C,D)=n-o(C,D),
\]

the exact mean raw distance from a fixed state to a uniform raw state is

\[
\mathbb E[d_E]
=n-\frac{2n}{n-1}
=\boxed{\frac{n(n-3)}{n-1}}.
\]

Its variance is the same as overlap variance:

\[
\boxed{
\operatorname{Var}(d_E)
=\frac{2n(n-3)}{(n-1)^2}.
}
\]

Again, this is a comparison metric on edge sets, not a chosen transition metric.

---

# 18. Representation redundancy and the pre-gauge question

The raw Hamilton-cycle construction provides a simple finite example of the distinction between representation and intrinsic structure.

A cycle can be presented using different:

- starting labels;
- orientations;
- anchored coordinate conventions.

The intrinsic edge relation is unchanged.

Thus the first layer already has the pattern:

\[
\boxed{
\text{many descriptions}
\to
\text{declared equivalence}
\to
\text{one intrinsic comparison state}.
}
\]

This should not yet be called physical gauge theory.

However, it is a clean example of the more primitive question now being developed in EHF:

> Which distinctions are representational, and which survive admissible structural comparison?

Later atlas/covariance work should be treated as downstream tests of this principle rather than retroactively inserted into the raw definition.

---

# 19. What HC-RAW-01 establishes

## Definition-locked

1. Raw states are undirected cyclic orderings modulo rotation and reflection.
2. The anchor and orientation convention are computational coordinates.
3. \(|HC_n|=(n-1)!/2\).
4. Each state contains exactly \(n\) local pair relations and every label has degree two.

## Exact elementary results

1. Every fixed unordered label pair occurs in exactly \((n-2)!\) states.
2. A fixed adjacent edge pair occurs in \((n-3)!\) states.
3. A fixed disjoint edge pair occurs in \(2(n-3)!\) states.
4. Forced linear forests obey a block-contraction counting law in the ordinary contraction regime.
5. Raw edge overlap has exact mean
   \[
   \frac{2n}{n-1}.
   \]
6. Raw edge overlap has exact variance
   \[
   \frac{2n(n-3)}{(n-1)^2}.
   \]
7. Distinct cycles cannot overlap in exactly \(n-1\) edges.

## Fresh exhaustive finite audit

All strict checks pass for

\[
n=4,\ldots,10.
\]

The complete overlap histograms through \(n=10\) have been recorded.

---

# 20. What HC-RAW-01 does not establish

The probe does not show:

- that Hamilton cycles are physically fundamental;
- that degree-two cyclicity is uniquely selected by admissible comparison;
- that LR3 is the correct move rule;
- that 2-opt is the correct move rule;
- that raw edge overlap is a physical distance;
- that \(n\) is time, size of space, particle number, or cosmological scale;
- that any probability measure on physical states is uniform over \(HC_n\);
- that later parity, Johnson, OPW, amplitude, or curvature structures follow without additional rules.

---

# 21. Relationship to earlier documents

## 21.1 Core C

The cleaned Core C document already uses the same raw state count and dihedral canonicalisation, but then immediately equips \(HC_n\) with 2-opt adjacency.

The present document therefore sits logically below Core C:

```text
HC-RAW
    ↓ add 2-opt
Core C
```

## 21.2 LR3 / OPW3

The OPW3 rebuild starts from canonical Hamilton cycles and adds LR3 together with preserve labels and restrictions.

The present document sits below that branch:

```text
HC-RAW
    ↓ add LR3
raw LR3 dynamics
    ↓ impose/diagnose preserve structure
OPW3
```

## 21.3 Johnson transport

Johnson geometry is downstream of sector reduction and subset encoding. It is not part of raw \(HC_n\).

## 21.4 Growth

All-slot insertion is a cross-layer relation

\[
HC_n\to HC_{n+1}.
\]

It is not part of a single raw layer. It should therefore be studied only after the raw layer has been definition-locked.

---

# 22. Health assessment after Probe 01

The raw Hamilton-cycle layer is currently healthy in the limited sense that:

- its object definition is exact;
- the dihedral quotient is unambiguous;
- label neutrality is exact;
- nontrivial relational incidence structure appears without any between-state move rule;
- several exact formulas follow from simple counting;
- the finite enumeration agrees with those formulas through \(n=10\).

The main foundational weakness is not internal inconsistency. It is **selection**:

> Why should the first relational object be one connected degree-two cycle rather than another neutral relational class?

That question should remain open and should eventually be tested by explicit alternative substrates.

---

# 23. Next probe targets

## HC-RAW-02 — Exact Raw Overlap Distribution Law

Goal:

Derive a closed formula, recurrence, or generating function for

\[
M_n(r)=|\{D:o(C,D)=r\}|.
\]

Questions:

1. Can the full distribution be obtained by inclusion-exclusion over runs of selected reference edges?
2. Can the support law be proved for all \(n\ge6\)?
3. Does the overlap distribution have a known combinatorial name?
4. Does it converge to a Poisson-type law with mean 2?
5. What are its exact higher factorial moments?

## HC-RAW-03 — Raw Comparison Scheme / Overlap Algebra

Goal:

Determine whether relations defined by fixed overlap

\[
o(C,D)=r
\]

form an association scheme or a weaker coherent configuration.

This would identify the full natural comparison algebra **before** selecting LR3 or 2-opt.

## HC-RAW-04 — Minimal-Change Layers

Goal:

Classify all pairs with overlap \(n-2\), \(n-3\), etc., and determine which local transformations generate each raw comparison shell.

This would place 2-opt and LR3 inside the raw overlap structure rather than assuming them independently.

## HC-RAW-05 — Alternative Substrate Controls

Compare the same neutrality criteria against:

- Hamilton paths;
- perfect matchings;
- spanning trees;
- fixed-degree connected graphs;
- unions of cycles.

The purpose is to test whether Hamilton cycles are structurally distinguished or merely one convenient member of a larger class.

---

# 24. Current concise statement

The raw EHF Hamilton-cycle laboratory is presently:

\[
\boxed{
HC_n
=
\{\text{undirected cyclic orderings of }n\text{ distinguishable labels}\}/\text{dihedral presentation redundancy}.
}
\]

A state is a closed degree-two local relation using every label exactly once.

The raw ensemble is exactly label-neutral:

\[
\Pr(\{a,b\}\in E(C))=\frac{2}{n-1},
\]

but it is not structurally trivial: multi-edge incidence depends on relational pattern, and two raw states possess a nontrivial exact edge-overlap distribution.

No same-layer dynamics has yet been chosen.

This is the correct starting point for asking which additional admissibility rule, if any, should come next.

---

# 25. EHF-HC-RAW-02
## Exact Raw Overlap Distribution Law

### 25.1 Purpose

HC-RAW-01 established the exact first two moments of raw edge overlap and exhaustively enumerated the overlap distribution through \(n=10\).

HC-RAW-02 asks for the full law:

\[
M_n(r)
=
\#\{D\in HC_n:|E(C)\cap E(D)|=r\},
\]

for a fixed reference state \(C\in HC_n\).

Because relabelling acts transitively on \(HC_n\), the result is independent of the chosen reference cycle.

No LR3, LR2, 2-opt, parity filter, growth rule, stochastic kernel, or physical weighting is used in the derivation.

The result is obtained entirely from the incidence structure of subsets of the \(n\) edges of the reference cycle.

### 25.2 Script

```text
ehf_hc_raw_02_exact_overlap_distribution_law.py
```

Reference run:

```bash
python3 ehf_hc_raw_02_exact_overlap_distribution_law.py \
  --n-min 4 \
  --n-max 30 \
  --enumerate-through 10 \
  --out-dir runs/ehf_hc_raw_02 \
  --strict
```

Verdict:

```text
EHF_HC_RAW_02_EXACT_OVERLAP_DISTRIBUTION_LAW_PASS
```

Fresh exhaustive enumeration matches the exact formula for every \(n=4,\ldots,10\). Exact integer consistency checks pass for every \(n=4,\ldots,30\).

---

# 26. Circular runs of reference edges

Fix a reference cycle \(C\) and consider a proper subset

\[
F\subset E(C),
\qquad
|F|=k<n.
\]

Because \(F\) is a proper subset of a cycle, it is a linear forest: a disjoint union of path components.

Around the reference cycle, these path components are exactly the **runs** of selected edges.

Let

\[
c=c(F)
\]

be the number of selected runs.

For

\[
1\le k\le n-1,
\qquad
1\le c\le \min(k,n-k),
\]

the number of \(k\)-edge subsets of an \(n\)-cycle having exactly \(c\) runs is

\[
\boxed{
R(n,k,c)
=
\frac{n}{c}
\binom{k-1}{c-1}
\binom{n-k-1}{c-1}.
}
\]

### 26.1 Counting argument

Write the \(k\) selected edges as \(c\) positive run lengths. The number of compositions is

\[
\binom{k-1}{c-1}.
\]

Write the \(n-k\) unselected edges as \(c\) positive gap lengths between selected runs. The number of compositions is

\[
\binom{n-k-1}{c-1}.
\]

There are \(n\) choices for the labelled edge at which to start the circular description.

Each actual subset is counted once for each of its \(c\) selected runs, so divide by \(c\).

Hence

\[
R(n,k,c)
=
\frac{n}{c}
\binom{k-1}{c-1}
\binom{n-k-1}{c-1}.
\]

The probe checks exactly that

\[
\sum_c R(n,k,c)=\binom nk
\]

for every \(k=1,\ldots,n-1\) and every tested \(n\le30\).

---

# 27. Number of Hamilton cycles containing a forced run pattern

Let \(F\subset E(C)\) contain \(k<n\) edges in \(c\) path components.

Each path component may occur in either of its two orientations inside a containing undirected Hamilton cycle.

Treat each forced path as one oriented block. Together with the isolated labels not incident internally to a forced edge, the contraction leaves

\[
n-k
\]

cyclic blocks.

There are

\[
(n-k-1)!
\]

oriented cyclic orders of these blocks, and \(2^c\) internal path orientations. Global reversal identifies pairs of descriptions.

Therefore the exact number of undirected Hamilton cycles containing \(F\) is

\[
\boxed{
N(F)=2^{c-1}(n-k-1)!.
}
\]

This formula remains valid at the boundary cases \(n-k=1,2\) when understood as a count of expanded cyclic block arrangements rather than as an independent Hamilton-cycle count on the contracted block set.

For \(F=E(C)\), i.e. \(k=n\), the count is separately

\[
N(E(C))=1.
\]

---

# 28. Binomial overlap sums

Let

\[
X(D)=|E(C)\cap E(D)|.
\]

For each \(k\), define

\[
S_{n,k}
=
\sum_{D\in HC_n}\binom{X(D)}k.
\]

Equivalently, \(S_{n,k}\) counts pairs

\[
(D,F)
\]

where \(D\in HC_n\) and \(F\) is a \(k\)-edge subset of the reference cycle contained in \(D\).

Therefore:

\[
S_{n,0}=|HC_n|=\frac{(n-1)!}{2},
\]

\[
S_{n,n}=1,
\]

and for

\[
1\le k\le n-1,
\]

\[
\boxed{
S_{n,k}
=
\sum_{c=1}^{\min(k,n-k)}
R(n,k,c)\,
2^{c-1}(n-k-1)!.
}
\]

Substituting the run count gives

\[
\boxed{
S_{n,k}
=
n(n-k-1)!
\sum_{c=1}^{\min(k,n-k)}
\frac{2^{c-1}}{c}
\binom{k-1}{c-1}
\binom{n-k-1}{c-1}.
}
\]

This is an exact finite formula involving only factorials and binomial coefficients.

---

# 29. Exact overlap distribution by binomial inversion

By definition,

\[
S_{n,k}
=
\sum_{r=k}^{n}
\binom rk M_n(r).
\]

This is an upper-triangular binomial transform.

Binomial inversion therefore gives the complete overlap law:

\[
\boxed{
M_n(r)
=
\sum_{k=r}^{n}
(-1)^{k-r}
\binom kr
S_{n,k}.
}
\]

Together with the exact formula for \(S_{n,k}\), this determines every overlap multiplicity \(M_n(r)\) for every \(n\ge4\).

This is the central result of HC-RAW-02.

No state-space enumeration is required once the formula is known.

---

# 30. Exact overlap generating polynomial

The same result has a compact generating-function form.

For any target state \(D\),

\[
z^{X(D)}
=
[1+(z-1)]^{X(D)}
=
\sum_{k=0}^{X(D)}
\binom{X(D)}k(z-1)^k.
\]

Summing over \(D\in HC_n\) yields

\[
\boxed{
P_n(z)
:=
\sum_{r=0}^{n}M_n(r)z^r
=
\sum_{k=0}^{n}S_{n,k}(z-1)^k.
}
\]

Thus the complete raw overlap distribution is encoded by the exact polynomial \(P_n(z)\).

The coefficients in the ordinary \(z\)-basis are the overlap multiplicities.

The coefficients in the shifted \((z-1)\)-basis are the binomial-overlap sums generated by forced reference-edge patterns.

This gives a clean structural interpretation:

\[
\boxed{
\text{forced-edge incidence}
\longleftrightarrow
\text{binomial overlap moments}
\longleftrightarrow
\text{full overlap distribution}.
}
\]

---

# 31. Fresh exact distributions beyond RAW-01

RAW-02 reproduces every RAW-01 distribution through \(n=10\) and then extends the law without state enumeration.

For example:

### \(n=11\)

\[
\begin{aligned}
&M_{11}(0)=157931,\\
&M_{11}(1)=426514,\\
&M_{11}(2)=532950,\\
&M_{11}(3)=403315,\\
&M_{11}(4)=203236,\\
&M_{11}(5)=70114,\\
&M_{11}(6)=17050,\\
&M_{11}(7)=2860,\\
&M_{11}(8)=385,\\
&M_{11}(9)=44,\\
&M_{11}(10)=0,\\
&M_{11}(11)=1.
\end{aligned}
\]

The total is

\[
\sum_rM_{11}(r)=\frac{10!}{2}=1,814,400.
\]

### \(n=12\)

\[
\begin{aligned}
&M_{12}(0)=1814453,\\
&M_{12}(1)=4771008,\\
&M_{12}(2)=5829894,\\
&M_{12}(3)=4349024,\\
&M_{12}(4)=2185911,\\
&M_{12}(5)=772128,\\
&M_{12}(6)=194532,\\
&M_{12}(7)=36000,\\
&M_{12}(8)=4851,\\
&M_{12}(9)=544,\\
&M_{12}(10)=54,\\
&M_{12}(11)=0,\\
&M_{12}(12)=1.
\end{aligned}
\]

The total is

\[
\sum_rM_{12}(r)=\frac{11!}{2}=19,958,400.
\]

---

# 32. Exact corollaries

The full distribution law immediately reproduces and strengthens several RAW-01 observations.

## 32.1 Identity shell

\[
\boxed{M_n(n)=1.}
\]

Only the reference cycle shares all \(n\) edges with itself.

## 32.2 The forbidden \(n-1\) shell

\[
\boxed{M_n(n-1)=0.}
\]

Two distinct Hamilton cycles cannot differ in only one edge.

## 32.3 Nearest distinct overlap shell

\[
\boxed{
M_n(n-2)=\frac{n(n-3)}2.
}
\]

This shell is nonempty for \(n\ge4\).

Since \(n-1\) overlap is impossible, \(n-2\) is the maximum possible overlap of two distinct raw states.

Equivalently, under

\[
d_E(C,D)=n-|E(C)\cap E(D)|,
\]

the minimum nonzero distance is

\[
\boxed{d_E=2.}
\]

---

# 33. Core C is the nearest-neighbour graph of raw HC space

This is an important structural consequence of HC-RAW-02.

Two distinct Hamilton cycles with overlap \(n-2\) differ by exactly two removed edges and two replacement edges. Their symmetric difference therefore has four edges, and the change is precisely a 2-opt reconnection.

Thus:

\[
C\sim_{2\mathrm{opt}}D
\quad\Longleftrightarrow\quad
|E(C)\cap E(D)|=n-2
\quad\Longleftrightarrow\quad
 d_E(C,D)=2.
\]

Therefore the full 2-opt graph is not merely one arbitrary move graph that can be imposed on \(HC_n\).

It has an intrinsic characterization:

\[
\boxed{
G_n^{2\mathrm{opt}}
=
\text{nearest-neighbour graph of }HC_n
\text{ under raw edge-symmetric-difference distance}.
}
\]

Its degree follows immediately from the raw overlap law:

\[
\boxed{
\deg G_n^{2\mathrm{opt}}
=M_n(n-2)
=\frac{n(n-3)}2.
}
\]

This gives Core C a more principled position in the rebuilt hierarchy.

It does **not** prove that 2-opt is the physically correct admissibility rule. It shows that 2-opt is canonically selected if one asks for the smallest nontrivial change in raw edge relation.

The comparison with LR3 must therefore be made explicitly rather than treating 2-opt and LR3 as conceptually interchangeable.

---

# 34. Exact moment recovery from the full law

Let \(D\) be uniform on \(HC_n\) and

\[
X=|E(C)\cap E(D)|.
\]

The exact distribution satisfies

\[
\sum_r rM_n(r)
=
|HC_n|\frac{2n}{n-1},
\]

and

\[
\sum_r r^2M_n(r)
=
|HC_n|\frac{6n}{n-1}.
\]

Hence:

\[
\boxed{\mathbb E[X]=\frac{2n}{n-1}},
\]

\[
\boxed{\mathbb E[X^2]=\frac{6n}{n-1}},
\]

and

\[
\boxed{
\operatorname{Var}(X)
=\frac{2n(n-3)}{(n-1)^2}.
}
\]

HC-RAW-02 checks these as exact integer identities, avoiding floating-point rank or moment decisions.

---

# 35. Support pattern

Exact formula evaluation gives:

- \(n=4\): support \(\{2,4\}\);
- \(n=5\): support \(\{0,2,3,5\}\);
- for every evaluated \(n=6,\ldots,30\):
  \[
  \operatorname{supp}M_n
  =\{0,1,\ldots,n-2,n\}.
  \]

Thus the only missing overlap value in the full range \(0,\ldots,n\) is \(n-1\) for all tested \(n\ge6\).

The formula computes this exactly over the tested range, but the all-\(n\) positivity statement

\[
M_n(r)>0
\qquad
(0\le r\le n-2,\ n\ge6)
\]

has not yet been given a separate constructive proof in this working document.

That is an optional theorem-polish target rather than a prerequisite for the exact distribution formula itself.

---

# 36. First asymptotic clue

RAW-01 observed

\[
\mathbb E[X]\to2,
\qquad
\operatorname{Var}(X)\to2.
\]

The exact binomial-moment representation in RAW-02 makes a Poisson limit much more plausible.

For fixed \(k\), the dominant \(k\)-edge subsets of a large reference cycle are those with \(k\) disjoint runs, and their forced-cycle count contributes the leading binomial moment expected for a Poisson random variable of mean \(2\).

This suggests the next asymptotic theorem target:

\[
X_n
\overset{?}{\Longrightarrow}
\operatorname{Poisson}(2).
\]

No limit theorem is claimed in RAW-02. It should be proved separately from the exact formula rather than inferred only from matching mean and variance.

---

# 37. HC-RAW-02 result ledger

## Exact derivation

1. Circular-run count:
   \[
   R(n,k,c)=\frac nc\binom{k-1}{c-1}\binom{n-k-1}{c-1}.
   \]
2. Forced-pattern count:
   \[
   N(F)=2^{c-1}(n-k-1)!.
   \]
3. Exact binomial-overlap sum \(S_{n,k}\).
4. Exact full overlap law:
   \[
   M_n(r)=\sum_{k=r}^n(-1)^{k-r}\binom krS_{n,k}.
   \]
5. Exact overlap generating polynomial:
   \[
   P_n(z)=\sum_kS_{n,k}(z-1)^k.
   \]
6. Exact nearest distinct shell:
   \[
   M_n(n-2)=\frac{n(n-3)}2.
   \]
7. Exact identification of the raw nearest-neighbour graph with 2-opt adjacency.

## Fresh computational certification

- formula versus complete state enumeration: PASS for \(n=4,\ldots,10\);
- run-subset partition counts: PASS exactly through \(n=30\);
- distribution normalization: PASS exactly through \(n=30\);
- first and second moment identities: PASS exactly through \(n=30\);
- \(M_n(n)=1\): PASS;
- \(M_n(n-1)=0\): PASS;
- \(M_n(n-2)=n(n-3)/2\): PASS.

## Interpretation status

This is a combinatorial theorem about the raw Hamilton-cycle comparison space.

No literature-novelty claim is made here.

No physical interpretation is required.

---

# 38. Immediate questions after HC-RAW-02

The raw programme now has several natural next directions.

### A. Poisson limit

Prove or disprove

\[
X_n\Rightarrow\mathrm{Poisson}(2).
\]

### B. Raw association layers

For every raw distance shell

\[
d_E=s,
\]
construct the corresponding relation matrix and ask whether the full overlap partition forms an association scheme or a weaker coherent configuration.

This would determine whether 2-opt is merely the first member of a canonical hierarchy of raw comparison shells.

### C. Compare LR3 to raw overlap shells

Measure exactly which raw distances LR3 moves occupy.

This would answer a basic foundational question:

> Is LR3 also naturally selected by the raw comparison geometry, or does it encode an additional locality principle not present in edge-symmetric-difference distance alone?

### D. Higher forced-pattern structure

Extend from subsets of one reference cycle to joint incidence among several reference cycles and classify which quantities depend only on overlap and which depend on finer arrangement data.

### E. Canonicality of the raw metric

Study whether

\[
d_E(C,D)=\frac12|E(C)\triangle E(D)|
\]

is uniquely or naturally selected by minimal assumptions such as relabelling invariance and additivity over pair-relations.

---

# 39. Current rebuilt hierarchy after RAW-02

The present dependency picture is now sharper:

```text
admissible-comparison foundation
    ↓
raw undirected cyclic states HC_n
    ↓
raw edge-overlap / symmetric-difference comparison
    ├── nearest nontrivial shell = 2-opt graph (Core C)
    ├── other raw overlap shells
    └── separate locality question: where does LR3 sit?

HC_n
    ↓
all-slot completion HC_n -> HC_{n+1}       [later cross-layer question]
```

The important change is that 2-opt now has a derivation from raw comparison geometry:

\[
\boxed{
\text{2-opt} = \text{minimal nonzero raw edge-relation change}.
}
\]

LR3 should now be audited against that raw structure rather than silently treated as equally primitive.



---

# 40. EHF-HC-RAW-03 — Raw Comparison Scheme / Overlap Algebra Audit

## 40.1 Question

RAW-02 supplied the intrinsic raw overlap

\[
o(C,D)=|E(C)\cap E(D)|
\]

and distance

\[
d_E(C,D)=n-o(C,D).
\]

Define

\[
R_r=\{(C,D):o(C,D)=r\}.
\]

RAW-03 asks whether the \(R_r\) close as an association scheme: for fixed
\(i,j,k\), is

\[
p_{ij}^{\,k}
=
\#\{Z:o(C,Z)=i,\ o(D,Z)=j\}
\]

determined solely by \(o(C,D)=k\)?

No move rule is introduced.

## 40.2 Overlap-only result

Exhaustive result:

| n | states | overlap relations | overlap association-scheme test |
|---:|---:|---:|---|
| 4 | 3 | 2 | PASS |
| 5 | 12 | 4 | PASS |
| 6 | 60 | 6 | FAIL |
| 7 | 360 | 7 | FAIL |
| 8 | 2520 | 8 | FAIL |

Thus overlap alone is not the full comparison algebra.

## 40.3 Minimal exact failure witness

At \(n=6\), fix

\[
C=(0,1,2,3,4,5).
\]

Take

\[
D_1=(0,1,3,5,2,4),
\qquad
D_2=(0,1,4,2,5,3).
\]

Both have

\[
o(C,D_1)=o(C,D_2)=1.
\]

But

\[
\#\{Z:o(C,Z)=0,\ o(D_1,Z)=2\}=1,
\]

while

\[
\#\{Z:o(C,Z)=0,\ o(D_2,Z)=2\}=0.
\]

Therefore \(p_{0,2}^{\,1}\) is not determined by overlap alone.

## 40.4 Common-edge run structure is also insufficient

At \(n=6\), the two distinct intersection-profile classes inside overlap \(1\)
both have the same common-edge run partition \((1)\).  Thus even overlap plus
the circular run lengths of common edges does not determine the intrinsic pair
type.  The reconnection pattern of the noncommon edges matters.

## 40.5 Canonical relabelling-covariant refinement

\(S_n\) acts transitively on \(HC_n\) by relabelling.  The stabilizer of the
reference undirected cycle is \(D_n\).  Hence simultaneous-relabeling ordered
pair types are indexed by

\[
\boxed{D_n\backslash S_n/D_n}.
\]

These are the orbitals of the transitive \(S_n\)-action.  By the standard
group-action construction they form a homogeneous Schurian coherent
configuration.

Thus raw \(HC_n\) has a canonical coherent comparison structure before any
LR3, 2-opt, growth, sector, or physics rule is chosen.

## 40.6 Orbital census

| n | states | orbital classes |
|---:|---:|---:|
| 4 | 3 | 2 |
| 5 | 12 | 4 |
| 6 | 60 | 12 |
| 7 | 360 | 39 |
| 8 | 2520 | 202 |

Refinement by overlap:

\[
n=6:\quad (1,2,3,3,2,1)
\]

over overlaps \(0,1,2,3,4,6\);

\[
n=7:\quad (5,6,12,8,5,2,1)
\]

over overlaps \(0,1,2,3,4,5,7\);

\[
n=8:\quad (19,40,57,48,26,8,3,1)
\]

over overlaps \(0,1,2,3,4,5,6,8\).

## 40.7 First intersection-profile refinement recovers every orbital through n=8

Define the full overlap-intersection profile

\[
\Phi_{C,D}(i,j)
=
\#\{Z:o(C,Z)=i,\ o(D,Z)=j\}.
\]

Exhaustively for every state at \(n=4,5,6,7,8\),

\[
\boxed{
\Phi_{C_0,D_1}=\Phi_{C_0,D_2}
\iff
(C_0,D_1),(C_0,D_2)
\text{ are in the same }S_n\text{ orbital}.
}
\]

| n | profile classes | orbital classes | bijection |
|---:|---:|---:|---|
| 4 | 2 | 2 | yes |
| 5 | 4 | 4 | yes |
| 6 | 12 | 12 | yes |
| 7 | 39 | 39 | yes |
| 8 | 202 | 202 | yes |

This is a finite computational theorem through \(n=8\), not yet an all-\(n\)
proof.

## 40.8 The coherent configuration is not symmetric from n=6

Transpose reverses the ordered pair \((C,D)\mapsto(D,C)\).

| n | orbitals | self-transpose | transpose pairs |
|---:|---:|---:|---:|
| 4 | 2 | 2 | 0 |
| 5 | 4 | 4 | 0 |
| 6 | 12 | 8 | 2 |
| 7 | 39 | 17 | 11 |
| 8 | 202 | 52 | 75 |

So undirected cycle states do not imply that every ordered pair type is
self-transpose.

## 40.9 Simply symmetrizing transpose pairs still fails

At \(n=6\), 12 directed orbitals merge to 10 transpose-symmetrized classes,
but 2 of those classes still have nonconstant intersection profiles.

At \(n=7\), 39 orbitals merge to 28 symmetric classes, and 11 still fail.

Therefore the directional orbital data is part of the closure structure, not
just removable presentation noise.

## 40.10 Revised raw hierarchy

\[
\boxed{
HC_n
\rightarrow
\text{coarse overlap}
\rightarrow
\text{intersection-profile refinement}
\rightarrow
D_n\backslash S_n/D_n
\rightarrow
\text{Schurian coherent configuration}.
}
\]

RAW-02 remains valid:

\[
\text{nearest nontrivial overlap shell}=\text{2-opt}.
\]

But RAW-03 shows that the full raw comparison geometry is finer than the
overlap hierarchy.

## 40.11 Foundational significance

Before any dynamics is chosen, raw Hamilton cycles already admit progressively
finer invariant comparisons:

\[
C=D,
\]

\[
o(C,D),
\]

\[
\Phi_{C,D},
\]

and finally the full simultaneous-relabeling pair type

\[
D_ngD_n.
\]

This is a concrete example of admissible comparison as a rule-governed,
non-mystical structural notion: different comparison questions resolve
different distinctions.

## 40.12 Result ledger

Exact/group-theoretic:

1. \(S_n\) acts transitively on \(HC_n\).
2. the reference-cycle stabilizer is \(D_n\);
3. ordered pair types are \(D_n\backslash S_n/D_n\);
4. the orbitals form a Schurian homogeneous coherent configuration.

Exhaustive finite certification:

1. overlap-only association test through \(n=8\);
2. exact failure from \(n=6\) onward in the audited range;
3. full profile/orbital bijection through \(n=8\);
4. complete transpose census through \(n=8\);
5. transpose-symmetrized fusion failure at \(n=6,7\).

Open:

1. prove or disprove that the first overlap-intersection refinement always
   equals the orbital partition;
2. derive a formula for \(|D_n\backslash S_n/D_n|\);
3. find direct combinatorial labels for orbital classes;
4. derive the coherent adjacency algebra;
5. locate LR3 inside the raw orbital structure.

## 40.13 Recommended next probes

**RAW-04A — Double-Coset / Orbital Enumeration Law**

Derive \(|D_n\backslash S_n/D_n|\) analytically.

**RAW-04B — LR3 Location in Raw Pair Geometry**

Determine the raw overlap, distance, and orbital classes occupied by LR3.

For reconnecting the raw foundation to the existing EHF programme, RAW-04B
is the more informative next step.
