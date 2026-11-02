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


---

# 54. EHF-HC-RAW-04B — LR3 Location in Raw Pair Geometry

## 54.1 Scope

The rule audited here is the **raw, unfiltered LR3 rule**:

\[
\mathrm{LR3}=\text{circular reversal of three consecutive cycle labels}.
\]

No \(\Pi\)-preserving filter is imposed. OPW3 is downstream.

The question is:

> Is LR3 intrinsically visible inside the raw Hamilton-cycle comparison structure, or is it an unrelated move rule imposed from outside?

---

## 55. Every local reversal lies in the nearest raw shell

Let \(C\in HC_n\), and reverse a proper consecutive block of \(\ell\) vertices.

Only the two boundary edges of the block change. The \(\ell-1\) internal edges remain as unordered edges. Therefore

\[
|E(C)\cap E(D)|=n-2,
\]

and hence

\[
\boxed{d_E(C,D)=2.}
\]

RAW-02 proved that \(d_E=2\) is the nearest possible distance between distinct Hamilton cycles.

Thus every nontrivial local block reversal is a nearest-neighbour raw comparison.

---

## 56. Exact decomposition of the 2-opt shell

Reversing a block of \(\ell\) vertices or the complementary block of \(n-\ell\) vertices gives the same undirected 2-opt neighbour. Use the effective support

\[
2\le \ell\le\left\lfloor\frac n2\right\rfloor.
\]

For any state \(C\),

\[
\boxed{
N_{2\mathrm{opt}}(C)
=
\bigsqcup_{\ell=2}^{\lfloor n/2\rfloor}N_\ell(C).
}
\]

The exact class degree is

\[
|N_\ell(C)|
=
\begin{cases}
n,&\ell<n/2,\\[1mm]
n/2,&n\text{ even and }\ell=n/2.
\end{cases}
\]

Therefore

\[
\sum_\ell |N_\ell(C)|
=
\frac{n(n-3)}2,
\]

the exact 2-opt degree.

RAW-04B certified this decomposition from a reference state for every

\[
5\le n\le20.
\]

---

## 57. Reversal support is intrinsic pair data

For a 2-opt pair \((C,D)\), the common-edge graph

\[
E(C)\cap E(D)
\]

is the disjoint union of two paths.

For effective reversal length \(\ell\), those paths contain

\[
\boxed{\ell\quad\text{and}\quad n-\ell}
\]

vertices.

Therefore

\[
\boxed{
\ell
=
\min\{\text{vertex sizes of the two common-edge path components}\}.
}
\]

So the support length is recoverable from the pair itself. It is not fundamentally a slot index or coordinate choice.

The \(D_n\)-orbital audit further showed, throughout \(5\le n\le20\),

\[
\boxed{
\text{one effective reversal length }\ell
=
\text{one nearest-shell }D_n\text{ orbital}.
}
\]

Hence the number of nearest-shell orbitals is

\[
\boxed{
\left\lfloor\frac n2\right\rfloor-1.
}
\]

---

## 58. LR3 inside the raw pair geometry

For \(n\ge6\),

\[
\boxed{
\mathrm{LR3}
=
\{(C,D):d_E(C,D)=2,\ 
\text{common-path sizes}=\{3,n-3\}\}.
}
\]

Thus LR3 is exactly one canonical raw orbital of the nearest shell.

For \(n=5\), length 3 is complementary to length 2, so as undirected edge sets

\[
\mathrm{LR3}=\mathrm{LR2}.
\]

For \(n=6\), \(\ell=3=n/2\), giving degree

\[
3.
\]

For \(n\ge7\), raw LR3 has degree

\[
\boxed{n}.
\]

---

## 59. Intrinsic bipartition of an even Hamilton cycle

When \(n\) is even, every Hamilton cycle is an even cycle graph and therefore has a unique graph bipartition up to interchange:

\[
\Pi_{\mathrm{intr}}(C)=\{A_C,B_C\}.
\]

No anchor or orientation is needed.

This is important: the even-side parity object can be defined directly from the cycle graph rather than from a chosen canonical presentation.

Odd cycles do not possess such a graph bipartition.

---

## 60. Exact reversal-parity law

Under a length-\(\ell\) block reversal, an internal offset \(j\) maps to

\[
\ell-1-j.
\]

Position parity changes by

\[
\ell-1\pmod2.
\]

Therefore, for even \(n\),

\[
\boxed{
\Pi_{\mathrm{intr}}(D)=\Pi_{\mathrm{intr}}(C)
\iff
\ell\text{ is odd}.
}
\]

RAW-04B checked this for every reversal-support class through even \(n=20\).

Hence the nearest shell splits intrinsically into

\[
\text{odd-support reversals: bipartition preserving},
\]

and

\[
\text{even-support reversals: bipartition changing}.
\]

---

## 61. Structural characterization of LR3

Among nontrivial local reversal classes,

\[
\ell=2
\]

has the smallest support but changes the intrinsic bipartition of an even cycle.

The next class,

\[
\ell=3,
\]

preserves it.

Therefore:

\[
\boxed{
\mathrm{LR3}
=
\text{the unique smallest-support nontrivial nearest-shell reversal
that preserves the intrinsic bipartition of every even }HC_n.
}
\]

This is a substantially stronger justification than simply declaring length-3 reversal to be the rule.

The qualification is equally important:

> Raw \(HC_n\) does not, by itself, logically require bipartition preservation to be the admissibility criterion.

Thus LR3 is not arbitrary coordinate data, but its selection still embodies an additional structural principle:

\[
\boxed{\text{minimal bipartition-preserving locality}.}
\]

That principle is now a candidate to be stress-tested rather than silently assumed.

---

## 62. Fresh raw-LR3 component census

RAW-04B rebuilt the **unfiltered** LR3 graph from scratch.

| \(n\) | states | LR3 degree | components | component size | result |
|---:|---:|---:|---:|---:|---|
| 5 | 12 | 5 | 1 | 12 | connected |
| 6 | 60 | 3 | 10 | 6 | intrinsic bipartition fibres |
| 7 | 360 | 7 | 1 | 360 | connected |
| 8 | 2520 | 8 | 35 | 72 | intrinsic bipartition fibres |
| 9 | 20160 | 9 | 1 | 20160 | connected |

For even \(n=6,8\), connected components coincide exactly with intrinsic unordered cycle bipartitions.

The number of such bipartitions is

\[
\frac12\binom{n}{n/2},
\]

giving

\[
10
\]

at \(n=6\) and

\[
35
\]

at \(n=8\).

For odd \(n=5,7,9\), raw LR3 is connected in the complete audited graphs.

Thus a uniform rule already produces the parity contrast:

\[
\boxed{
\text{uniform LR3}
\longrightarrow
\begin{cases}
\text{even }n:\text{ intrinsic bipartition sectors},\\
\text{odd }n:\text{ no bipartition obstruction; connected in audited cases}.
\end{cases}
}
\]

Odd connectedness remains a finite result until proved for all odd \(n\).

---

## 63. Relation to the historical \(\Pi\) language

For even \(n\), the old position-parity label can be replaced conceptually by the anchor-free graph invariant

\[
\Pi_{\mathrm{intr}}(C).
\]

This cleans up the foundation: even parity is not being manufactured by the canonical representation.

For odd \(n\), there is no intrinsic graph bipartition. Any position-parity label requires additional chart/canonicalization structure and should not be described as the same object.

This distinction provides a direct structural reason for the different odd/even response to the same LR3 rule.

---

## 64. Relation to Core C

RAW-02 established

\[
\text{2-opt}=\text{complete nearest }d_E=2\text{ shell}.
\]

RAW-04B refines this as

\[
\boxed{
\text{2-opt}
=
LR_2\sqcup LR_3\sqcup\cdots\sqcup LR_{\lfloor n/2\rfloor}.
}
\]

For even \(n\), its bipartition-preserving part is

\[
\boxed{
\text{2-opt}_{\mathrm{pres}}
=
\bigsqcup_{\substack{3\le\ell\le n/2\\\ell\text{ odd}}}LR_\ell.
}
\]

Therefore:

- at \(n=6\), the preserving 2-opt fibre is exactly LR3;
- at \(n=8\), it is again exactly LR3;
- from \(n=10\) onward, additional classes such as LR5 preserve the same bipartition.

This explains why the small-\(n\) Core C fibres and LR3 structures can coincide while the two constructions are not generally identical.

---

## 65. Answer to the RAW-04B question

The answer is neither “LR3 is arbitrary” nor “raw HC logically forces LR3.”

Raw \(HC_n\) itself supplies:

1. the nearest-shell class \(d_E=2\);
2. a canonical decomposition of that shell into reversal-support orbitals \(LR_\ell\);
3. an intrinsic pair invariant recovering \(\ell\);
4. an intrinsic bipartition for every even Hamilton cycle.

If the admissibility criterion is

> choose the smallest nontrivial nearest-shell local reversal that preserves the intrinsic even-cycle bipartition,

then LR3 is uniquely selected.

Schematically:

\[
\boxed{
\text{raw HC structure}
+
\text{minimal bipartition-preserving locality}
\Longrightarrow
LR3.
}
\]

This is the strongest current structural justification for LR3.

It remains a candidate selection principle, not a claim that nature must use LR3.

---

## 66. Certification ledger

### Exact elementary results

1. Every proper local reversal changes exactly two cycle edges.
2. Every nontrivial local reversal lies at \(d_E=2\).
3. Effective support obeys \(\ell\sim n-\ell\).
4. The nearest shell decomposes over \(2\le\ell\le\lfloor n/2\rfloor\).
5. A length-\(\ell\) pair has common-path vertex sizes \(\{\ell,n-\ell\}\).
6. For even \(n\), bipartition is preserved iff \(\ell\) is odd.
7. LR3 is the smallest nontrivial bipartition-preserving reversal class.

### Computational certification

For reference states through

\[
n=20,
\]

all reversal classes:

- partition the complete 2-opt shell;
- have the exact degree formula;
- form one \(D_n\) orbital each;
- are exactly recovered by common-path sizes;
- satisfy the bipartition parity law.

Complete raw-LR3 graphs were audited for

\[
n=5,6,7,8,9.
\]

All **409 strict checks passed**.

### Not yet established

1. all-odd-\(n\) LR3 connectedness;
2. all-even-\(n\) connectivity inside every bipartition fibre;
3. uniqueness of minimal bipartition-preserving locality among all plausible admissibility principles;
4. any physical meaning of the bipartition;
5. any physical necessity of LR3.

---

## 67. Recommended next probe

### EHF-HC-RAW-05A — LR3 Connectivity Theorem Search

Target:

\[
\text{odd }n:\qquad G_n^{LR3}\text{ connected},
\]

\[
\text{even }n:\qquad
\operatorname{Comp}(G_n^{LR3})
=
\text{intrinsic bipartition fibres}.
\]

The finite data now makes this the cleanest next theorem target. A constructive proof would tell us exactly what LR3 generates before OPW, Johnson reduction, spectral analysis, or growth are reintroduced.


---

# 68. EHF-HC-RAW-05A — LR3 Connectivity Theorem

## 68.1 Status

**Result:** exact theorem.

The previous raw audits established computationally that:

\[
n=5,7,9
\]

give connected raw-LR3 graphs, while

\[
n=6,8
\]

split exactly into intrinsic bipartition fibres.

RAW-05A converts this finite pattern into an all-\(n\) proof.

The proof is independent of OPW, \(\Pi\)-filtering, Johnson reduction, growth, spectra, amplitudes, or physical interpretation.

---

# 69. LR3 is a distance-two position transposition

Represent a labelled Hamilton cycle temporarily by a cyclic presentation

\[
(c_0,c_1,\ldots,c_{n-1}),
\]

with position indices in

\[
\mathbb Z_n.
\]

A circular length-3 reversal beginning at position \(i\) sends

\[
(c_i,c_{i+1},c_{i+2})
\longmapsto
(c_{i+2},c_{i+1},c_i).
\]

Therefore it does exactly one thing to the labels occupying the cyclic positions:

\[
\boxed{
\tau_i=(i,\ i+2).
}
\]

The middle label remains fixed.

Thus raw LR3 is generated by the position transpositions

\[
\mathcal T_n
=
\{(i,\ i+2):i\in\mathbb Z_n\}.
\]

This is the key simplification.

The move acts on labels through the geometry of the **position generator graph**

\[
P_n=(\mathbb Z_n,\{\{i,i+2\}:i\in\mathbb Z_n\}).
\]

---

# 70. The position generator graph

The graph \(P_n\) connects positions differing by \(2\pmod n\).

Its connected components are the orbits of addition by \(2\) on \(\mathbb Z_n\).

Therefore:

\[
\boxed{
\#\operatorname{Comp}(P_n)=\gcd(n,2).
}
\]

Hence:

### Odd \(n\)

If \(n\) is odd,

\[
\gcd(n,2)=1,
\]

so

\[
P_n\cong C_n
\]

is connected.

### Even \(n=2m\)

If \(n\) is even,

\[
\gcd(n,2)=2.
\]

The two components are exactly the even and odd position classes:

\[
\{0,2,\ldots,2m-2\},
\]

and

\[
\{1,3,\ldots,2m-1\}.
\]

Each component is an \(m\)-cycle.

---

# 71. Generator lemma

We use the standard elementary fact:

> **Lemma.** Let \(G\) be a connected graph on a finite vertex set \(X\). The transpositions associated with the edges of \(G\) generate the full symmetric group \(S_X\).

A constructive proof is immediate from a spanning tree: edge transpositions along paths allow arbitrary transpositions of vertices, and transpositions generate the symmetric group.

For a graph with connected components

\[
X_1,\ldots,X_k,
\]

the edge transpositions generate

\[
S_{X_1}\times\cdots\times S_{X_k}.
\]

Applying this to \(P_n\) gives the complete LR3 generator group.

---

# 72. Odd-\(n\) connectivity theorem

## Theorem 72.1

For every odd

\[
n\ge5,
\]

the raw LR3 graph on undirected Hamilton cycles \(HC_n\) is connected.

### Proof

For odd \(n\), the position generator graph \(P_n\) is connected.

Therefore the LR3 generators

\[
(i,\ i+2)
\]

generate the full position permutation group

\[
S_n.
\]

Starting from any cyclic labelling, arbitrary permutations of the labels among the \(n\) cyclic positions can therefore be produced by a sequence of LR3 moves.

In particular, any labelled cyclic ordering can be transformed into any other labelled cyclic ordering.

Passing to the quotient by cyclic rotation and reflection cannot split a connected orbit.

Hence the quotient state space \(HC_n\) is connected under raw LR3.

\[
\boxed{
n\text{ odd},\ n\ge5
\quad\Longrightarrow\quad
G_n^{LR3}\text{ connected}.
}
\]

\(\square\)

---

# 73. Even-\(n\) component theorem

Let

\[
n=2m\ge6.
\]

## Theorem 73.1

The connected components of the raw LR3 graph on \(HC_{2m}\) are exactly the intrinsic unordered bipartition fibres.

### Proof

For even \(n\), \(P_n\) has two connected components: even positions and odd positions.

The LR3 edge transpositions therefore generate

\[
S_m\times S_m,
\]

acting independently on the two position classes.

Hence LR3 can arbitrarily permute labels within each parity class but can never move a label from one parity class to the other.

Thus the unordered pair of label sets occupying alternating positions,

\[
\Pi_{\mathrm{intr}}(C)=\{A_C,B_C\},
\]

is invariant.

Conversely, suppose two Hamilton cycles have the same intrinsic unordered bipartition.

Choose cyclic presentations so that the same member of the unordered bipartition occupies the even positions in both presentations. This is always possible because a one-step cyclic rotation interchanges the two position classes.

The even-position labels can then be transformed arbitrarily using the first \(S_m\) factor, and the odd-position labels arbitrarily using the second.

Therefore the two presentations are connected by LR3 moves.

After quotienting by rotation and reflection, the two Hamilton-cycle states remain connected.

Hence two states are LR3-connected if and only if they have the same intrinsic unordered bipartition:

\[
\boxed{
C\sim_{LR3}D
\iff
\Pi_{\mathrm{intr}}(C)=\Pi_{\mathrm{intr}}(D).
}
\]

\(\square\)

---

# 74. Exact component count and size

For \(n=2m\), an intrinsic bipartition is an unordered split of the \(2m\) labels into two \(m\)-element sets.

Therefore the number of LR3 components is exactly

\[
\boxed{
N_{\mathrm{comp}}(2m)
=
\frac12\binom{2m}{m}.
}
\]

The total number of undirected Hamilton cycles is

\[
|HC_{2m}|=\frac{(2m-1)!}{2}.
\]

All bipartition fibres have equal size by label symmetry. Therefore

\[
|F_m|
=
\frac{|HC_{2m}|}
{\frac12\binom{2m}{m}}.
\]

Simplifying,

\[
|F_m|
=
\frac{(2m-1)!}{\binom{2m}{m}}
=
\frac{m!^2}{2m}
=
\boxed{
\frac{(m-1)!m!}{2}.
}
\]

Thus:

\[
\boxed{
n=2m:
\qquad
\#\text{components}
=
\frac12\binom{2m}{m},
\qquad
\text{component size}
=
\frac{(m-1)!m!}{2}.
}
\]

This is exactly the fibre-size formula that had appeared historically in Core C, now derived directly from raw LR3 connectivity.

---

# 75. Unified theorem

The preceding results can be stated compactly.

## Raw LR3 Connectivity Theorem

Let \(HC_n\) be the set of undirected cyclic orderings of \(n\) distinct labels, modulo rotation and reflection, and let raw LR3 adjacency be generated by circular reversal of three consecutive labels.

For every \(n\ge5\):

\[
\boxed{
\operatorname{Comp}(G_n^{LR3})
=
\begin{cases}
\{HC_n\}, & n\text{ odd},\\[2mm]
\{\text{intrinsic unordered cycle-bipartition fibres}\}, & n\text{ even}.
\end{cases}
}
\]

For even \(n=2m\),

\[
\boxed{
\#\operatorname{Comp}(G_{2m}^{LR3})
=
\frac12\binom{2m}{m}
}
\]

and every component has

\[
\boxed{
\frac{(m-1)!m!}{2}
}
\]

states.

The proof is purely combinatorial.

---

# 76. Computational certification

RAW-05A retained exhaustive computation as an independent implementation check rather than as proof.

Complete raw-LR3 graphs were rebuilt for:

\[
n=5,6,7,8,9.
\]

Results:

| \(n\) | states | components found | theorem prediction | component size |
|---:|---:|---:|---:|---:|
| 5 | 12 | 1 | 1 | 12 |
| 6 | 60 | 10 | 10 | 6 |
| 7 | 360 | 1 | 1 | 360 |
| 8 | 2520 | 35 | 35 | 72 |
| 9 | 20160 | 1 | 1 | 20160 |

For \(n=6,8\), component membership was independently checked against intrinsic graph bipartitions and agreed exactly.

The algebraic prediction ledger was also generated through

\[
n=30.
\]

All **69 strict certification checks passed**.

---

# 77. Why the theorem matters for the EHF rebuild

This result removes a major ambiguity from the old programme.

The odd/even split is not a fitted phenomenon and does not require two different underlying objects.

It follows from three elementary ingredients:

\[
\boxed{
\text{cyclic positions}
+
\text{uniform LR3}
+
\gcd(n,2).
}
\]

More explicitly:

\[
LR3
\equiv
(i,i+2),
\]

so the relevant arithmetic is simply whether stepping by \(2\) generates one orbit or two on

\[
\mathbb Z_n.
\]

Thus:

\[
\boxed{
\text{odd/even sectorization is a theorem of the same local rule}.
}
\]

No parity-dependent rule is inserted.

---

# 78. A cleaner interpretation of even parity

Historically, even-side sectors were often introduced using a canonical position-parity label.

RAW-05A shows that this can be stated without chart dependence.

For even \(n\), the preserved object is exactly the intrinsic graph bipartition of the cycle.

Thus the clean foundation is:

\[
\boxed{
\text{even LR3 sectors}
=
\text{cycle bipartition fibres}.
}
\]

Canonical even/odd positions are merely coordinates for this intrinsic bipartition.

This strengthens the representation/gauge discipline of the rebuilt framework.

---

# 79. What the theorem says about odd OPW

A crucial distinction must now be maintained.

For odd \(n\), the **raw LR3 graph is connected for every \(n\ge5\)**.

Therefore any nontrivial odd chamber decomposition cannot be an intrinsic connected-component decomposition of raw LR3 itself.

Historical OPW3 instead restricts LR3 edges by an additional preserved \(\Pi\)-type criterion.

Thus:

\[
\boxed{
\text{raw odd LR3 connectivity}
\neq
\text{odd OPW3 chamber structure}.
}
\]

The odd preserve-world is an additional admissibility restriction imposed on the connected raw LR3 substrate.

This is not a defect. It simply places the objects at the correct logical levels.

The rebuilt hierarchy should therefore distinguish:

\[
HC_n
\]

from

\[
G_n^{LR3}
\]

from

\[
G_n^{OPW3}.
\]

---

# 80. Relation to Core C

Core C had reported for even \(n=2m\):

\[
\#\text{sectors}
=
\binom{2m-1}{m-1}
\]

under an anchored parity-sector convention, with fibre size

\[
\frac{(m-1)!m!}{2}.
\]

The raw intrinsic bipartition count is

\[
\frac12\binom{2m}{m}.
\]

These are equal:

\[
\frac12\binom{2m}{m}
=
\binom{2m-1}{m-1}.
\]

Indeed,

\[
\frac12\frac{(2m)!}{m!m!}
=
\frac{(2m-1)!}{(m-1)!m!}.
\]

Thus the historical anchored sector count is exactly the intrinsic unordered bipartition count in different coordinates.

This reconciles a previously presentation-dependent formula with an anchor-free object.

---

# 81. Relation to the Johnson vertex set

Choose an anchor label \(a\) in an even cycle.

Each intrinsic unordered bipartition contains exactly one side containing \(a\).

Represent the bipartition by the complementary side, or equivalently by the non-anchor labels on the anchor side.

This produces a fixed-size subset of the remaining \(2m-1\) labels.

Hence the familiar Johnson-labelled sector set is naturally a **coordinate chart on the intrinsic bipartition space**.

This does not yet say that LR3 component adjacency is Johnson adjacency.

It says only that the sector labels themselves arise canonically from the intrinsic even-cycle bipartitions once an anchor chart is selected.

The distinction between:

\[
\text{Johnson vertex set}
\]

and

\[
\text{Johnson adjacency}
\]

must remain explicit.

---

# 82. Updated foundational chain

The rebuilt raw chain is now:

\[
\boxed{
HC_n
}
\]

\[
\downarrow
\]

raw overlap/coherent comparison structure,

\[
\downarrow
\]

nearest shell \(d_E=2\),

\[
\downarrow
\]

reversal-support orbitals \(LR_\ell\),

\[
\downarrow
\]

minimal bipartition-preserving locality,

\[
\downarrow
\]

\[
\boxed{
LR3
}
\]

with the exact theorem:

\[
\boxed{
\begin{array}{ll}
n\text{ odd}:&\text{one LR3 component},\\[1mm]
n\text{ even}:&\text{components = intrinsic bipartitions}.
\end{array}
}
\]

Only after this layer should OPW restrictions, Johnson transport, growth, spectra, and physical bridges be introduced.

---

# 83. Theorem status ledger

## Proved

1. A length-3 reversal is the position transposition \((i,i+2)\).
2. The LR3 position generator graph has \(\gcd(n,2)\) components.
3. Edge transpositions of a connected graph generate the symmetric group.
4. Raw LR3 is connected for all odd \(n\ge5\).
5. For all even \(n\ge6\), raw LR3 components are exactly intrinsic bipartition fibres.
6. For \(n=2m\), the component count is
   \[
   \frac12\binom{2m}{m}.
   \]
7. The component size is
   \[
   \frac{(m-1)!m!}{2}.
   \]
8. The historical anchored sector count equals the intrinsic bipartition count.

## Computationally certified

1. Complete graphs for \(n=5,\ldots,9\).
2. Exact bipartition/component equality for \(n=6,8\).
3. Algebraic prediction ledger through \(n=30\).
4. 69/69 strict checks passed.

## Still open

1. Whether minimal bipartition-preserving locality is the uniquely best admissibility-selection principle.
2. Why an odd-side OPW restriction should be introduced, if it should.
3. How growth interacts with the now-intrinsic even bipartition theorem.
4. Which reversal classes beyond LR3 are useful controls or enriched models.
5. Whether there is a universal characterization of LR3 not privileging the even side.

---

# 84. Recommended next step

The theorem means the next most important issue is no longer LR3 connectivity.

The sharp foundational question is now:

> **Why should the framework choose LR3 rather than another relabelling-covariant nearest-shell rule or union of raw orbitals?**

A natural next audit is:

### EHF-HC-RAW-05B — Minimality and Uniqueness Stress Test

Compare LR3 against all simple reversal-support alternatives under explicit criteria:

1. nearest-shell locality;
2. relabelling covariance;
3. presentation independence;
4. minimal support;
5. even intrinsic-bipartition preservation;
6. nontrivial odd mixing;
7. same rule at every \(n\).

The goal should be to determine which parts uniquely select LR3 and which are assumptions we have chosen.


---

# 85. EHF-HC-RAW-05B — Minimality and Uniqueness Stress Test

## 85.1 Purpose

RAW-04B and RAW-05A established that LR3 is an intrinsic nearest-shell orbital and that it generates the exact odd/even connectivity theorem.

The remaining foundational question is sharper:

> **Does raw Hamilton-cycle structure actually select LR3, or have we simply chosen one reasonable rule among many?**

RAW-05B treats this as a stress test rather than a confirmation exercise.

The candidate class is restricted to the simplest raw nearest-shell rules already justified by RAW-04B:

\[
\boxed{
\text{unions of effective reversal-support orbitals }LR_\ell,
\qquad
2\le\ell\le\lfloor n/2\rfloor.
}
\]

Every such orbital is:

- nearest-shell;
- relabelling-covariant;
- presentation-independent;
- intrinsically identifiable by common-edge path sizes.

Thus these properties alone cannot distinguish LR3.

---

# 86. Criteria ledger

The stress test uses the following criteria.

### C1 — nearest-shell locality

Every admitted move must satisfy

\[
d_E(C,D)=2.
\]

All \(LR_\ell\) orbitals pass.

### C2 — relabelling covariance

The rule must be defined invariantly under \(S_n\) relabelling.

All reversal-support orbitals pass.

### C3 — presentation independence

The rule must be recoverable from the pair \((C,D)\), not from a chosen anchor or slot.

RAW-04B showed that \(\ell\) is recovered from the two common-edge path sizes.

All \(LR_\ell\) pass.

### C4 — uniform nontriviality from \(n=6\)

The same rule family should already act nontrivially at the first nondegenerate even layer \(n=6\).

This excludes rules such as LR5-only.

### C5 — preservation of intrinsic even-cycle bipartition

For every even \(n\), admitted moves must preserve

\[
\Pi_{\rm intr}(C).
\]

RAW-04B proved

\[
LR_\ell\text{ preserves }\Pi_{\rm intr}
\iff
\ell\text{ is odd}.
\]

### C6 — odd mixing

The rule should not freeze the odd layers into artificial sectors.

RAW-05A proved LR3 is connected for every odd \(n\ge5\).

LR2 is also connected, since its position generators are adjacent transpositions.

Any rule containing LR3 is therefore connected on odd layers.

### C7 — strict locality / inclusion minimality

Among rules satisfying C1–C6, admit no larger support class than necessary and no redundant orbital union.

This is the criterion that distinguishes LR3 from preserving enrichments such as

\[
LR3\cup LR5
\]

or the union of all odd-support reversals.

---

# 87. Negative result: covariance and locality alone do not select LR3

The following rules are all intrinsic, relabelling-covariant nearest-shell rules:

\[
LR2,
\]

\[
LR3,
\]

\[
LR2\cup LR3,
\]

\[
\text{full 2-opt},
\]

\[
\bigcup_{\ell\text{ odd}}LR_\ell,
\]

and many other orbital unions.

Therefore:

\[
\boxed{
\text{raw HC + nearest-shell covariance does not uniquely select LR3}.
}
\]

This is an important negative result.

Any foundational statement claiming that LR3 follows from raw HC alone would be too strong.

---

# 88. LR2 is the decisive control

LR2 is strictly more local in support size than LR3.

A length-2 reversal is simply the adjacent position transposition

\[
(i,i+1).
\]

These generators form the edge transpositions of the ordinary cycle on positions and therefore generate \(S_n\).

Hence raw LR2 is connected for every \(n\).

It satisfies:

- nearest-shell locality;
- relabelling covariance;
- presentation independence;
- uniformity across \(n\);
- strong mixing.

But at even \(n\), LR2 changes the intrinsic bipartition.

Thus:

\[
\boxed{
\text{if even-bipartition preservation is not required, LR3 is not the minimal rule}.
}
\]

In fact, LR2 is simpler by support size.

This identifies the preservation principle as a genuine assumption rather than a theorem of raw HC.

---

# 89. Exact preservation classification

For even \(n\), an orbital union

\[
R_U=\bigcup_{\ell\in U}LR_\ell
\]

preserves every intrinsic bipartition if and only if

\[
\boxed{
U\subseteq\{3,5,7,\ldots\}.
}
\]

So preserving rules are exactly the nonempty unions of odd-support reversal orbitals.

Let

\[
q_n
=
\#\{\ell:
3\le\ell\le n/2,\ \ell\text{ odd}\}.
\]

Then the number of nonempty preserving orbital unions is

\[
\boxed{
2^{q_n}-1.
}
\]

Examples:

| \(n\) | preserving orbitals | preserving nonempty unions |
|---:|---:|---:|
| 6 | 1 | 1 |
| 8 | 1 | 1 |
| 10 | 2 | 3 |
| 12 | 2 | 3 |
| 14 | 3 | 7 |
| 16 | 3 | 7 |

Thus preservation alone ceases to select a unique rule from \(n=10\) onward.

---

# 90. Why \(n=6\) is structurally useful

At \(n=6\), the available effective reversal classes are

\[
LR2,\ LR3.
\]

Only LR3 preserves the intrinsic bipartition.

Therefore any **uniform rule family that is already nontrivial at \(n=6\) and preserves even bipartitions must include LR3**.

Higher odd supports cannot replace it because they do not yet exist at that layer.

This is stronger than a large-\(n\) minimality argument.

The smallest nondegenerate even layer itself forces LR3 to be present once preservation is demanded.

---

# 91. Conditional uniqueness theorem

## Theorem 91.1 — LR3 conditional minimality

Consider rule families formed from unions of raw nearest-shell reversal-support orbitals and require:

1. relabelling covariance;
2. presentation independence;
3. nontrivial action from \(n=6\);
4. preservation of every intrinsic even-cycle bipartition;
5. odd-layer connectivity/mixing;
6. inclusion minimality, equivalently no unnecessary higher-support orbital.

Then the unique rule family is

\[
\boxed{LR3}.
\]

### Proof

By even-bipartition preservation, every admitted support must be odd.

At \(n=6\), the only available nontrivial odd support is

\[
\ell=3.
\]

Therefore any uniform nontrivial preserving family must contain LR3.

RAW-05A proves LR3 alone already gives odd connectivity and the full even bipartition fibres.

Hence any additional admitted support \(5,7,\ldots\) is unnecessary for criteria 1–5.

Inclusion minimality removes all such enrichments.

Therefore the unique minimal rule is

\[
LR3.
\]

\(\square\)

Equivalent strict-locality statement:

\[
\boxed{
LR3
=
\arg\min_R
\{\text{largest admitted reversal support}\}
}
\]

among nontrivial uniform bipartition-preserving orbital-union rules.

---

# 92. Named-rule stress table

| rule | nearest/covariant/intrinsic | nontrivial from \(n=6\) | preserves even bipartition | odd mixing | strict minimality | verdict |
|---|---|---|---|---|---|---|
| LR2 | yes | yes | **no** | yes | no | simpler control, fails preservation |
| LR3 | yes | yes | **yes** | **yes** | **yes** | selected |
| LR2 \(\cup\) LR3 | yes | yes | **no** | yes | no | LR2 crosses sectors |
| full 2-opt | yes | yes | **no** | yes | no | canonical but too permissive |
| all odd supports | yes | yes | yes | yes | **no** | preserving enrichment |
| LR5 only | yes | **no** | yes | not needed | no | absent at \(n=6,8\) |
| LR3 \(\cup\) LR5 | yes | yes | yes | yes | **no** | strict enrichment of LR3 |

The table exposes precisely which criterion rejects each alternative.

---

# 93. Full 2-opt as a useful counterexample

Full 2-opt remains mathematically canonical because RAW-02 identified it with the complete nearest shell.

But it contains both even- and odd-support reversal orbitals.

Therefore at even \(n\) it contains moves that cross the intrinsic bipartition fibres.

So there are now two distinct canonical constructions:

\[
\boxed{
\text{full nearest-shell comparison}=2\text{-opt}
}
\]

and

\[
\boxed{
\text{minimal sector-preserving local comparison}=LR3.
}
\]

Neither should be described as replacing the other.

They answer different structural questions.

---

# 94. All-odd support as the strongest preserving competitor

Define

\[
R_{\rm odd}
=
\bigcup_{\substack{\ell\ge3\\\ell\text{ odd}}}LR_\ell.
\]

This rule is:

- nearest-shell;
- intrinsic;
- relabelling-covariant;
- bipartition-preserving at every even \(n\);
- connected on odd layers because it contains LR3.

Thus it passes every structural criterion except strict locality/minimality.

For \(n=6,8\),

\[
R_{\rm odd}=LR3.
\]

From \(n=10\) onward it becomes a genuine enrichment.

Therefore the difference between LR3 and all-odd support cannot be justified by preservation or mixing.

It is justified only by the decision to choose the **minimal sufficient** local rule.

This should be stated explicitly in the foundational document.

---

# 95. The \(n=5\) degeneracy

At \(n=5\),

\[
LR3=LR2
\]

as undirected Hamilton-cycle edge sets because a length-3 reversed block is complementary to a length-2 block.

Therefore \(n=5\) is a degenerate small layer for distinguishing the two rules.

The uniqueness argument properly begins at

\[
n=6,
\]

the first layer where LR2 and LR3 are distinct and where an intrinsic even bipartition exists.

The exhaustive control suite explicitly handles this degeneracy.

---

# 96. Exhaustive control census

Complete graphs were rebuilt for

\[
n=5,6,7,8,9
\]

under:

- LR2;
- LR3;
- LR2 \(\cup\) LR3;
- full 2-opt;
- all odd-support reversals.

The controls confirm:

1. LR2 is connected throughout the audited range;
2. LR3 reproduces the RAW-05A theorem;
3. full 2-opt is connected throughout;
4. all-odd support preserves the exact even bipartition fibres;
5. at the small audited sizes the all-odd rule coincides with LR3 because no higher odd support is yet available.

The analytic orbital-union census extends through even

\[
n=30.
\]

All **50 strict checks passed** after explicitly handling the \(n=5\) LR2/LR3 degeneracy.

---

# 97. What is now genuinely derived, and what remains chosen

RAW-05B gives a clean separation.

## Derived from raw HC

The following are not discretionary:

- the raw nearest shell;
- its reversal-support orbital decomposition;
- the intrinsic support label \(\ell\);
- the intrinsic bipartition of even cycles;
- the parity law
  \[
  \ell\text{ odd}\iff\text{bipartition preserved};
  \]
- LR3 connectivity/component theorem.

## Chosen structural principle

The following is an EHF modelling choice:

> **Preserve the intrinsic even-cycle bipartition while using the minimal sufficient local reversal rule.**

Given that choice, LR3 follows uniquely within the tested natural candidate class.

This is the precise status.

---

# 98. Recommended foundational language

Avoid:

> LR3 is forced by Hamilton cycles.

That is too strong.

Prefer:

> **Within the natural nearest-shell reversal orbitals of raw Hamilton-cycle space, LR3 is the unique minimal rule that is nontrivial from the first nondegenerate even layer, preserves the intrinsic bipartition of every even cycle, and still mixes every odd layer.**

Or more compactly:

\[
\boxed{
\text{LR3 is selected by minimal bipartition-preserving locality.}
}
\]

The phrase “selected by” is preferable to “fundamental” or “forced.”

---

# 99. Consequence for the working foundation

The rebuilt hierarchy can now distinguish the primitive mathematical object from the selected admissibility rule:

\[
\boxed{HC_n}
\]

is the raw state space.

\[
\boxed{d_E=2}
\]

is its intrinsic nearest comparison shell.

\[
\boxed{LR_\ell}
\]

are the canonical reversal-support orbitals inside that shell.

Then EHF imposes the structural selection principle:

\[
\boxed{\text{minimal bipartition-preserving locality}}
\]

which selects

\[
\boxed{LR3}.
\]

This is a substantially more disciplined statement than beginning with

\[
(HC_n,LR3)
\]

without explaining why LR3 is present.

---

# 100. Open issue exposed by RAW-05B

The main unresolved question has shifted.

It is no longer:

> Why length 3?

That now has a conditional answer.

The deeper question is:

> **Why should preservation of the intrinsic even-cycle bipartition be privileged as an admissibility constraint at all?**

Possible answers must not be invented after the fact.

The bipartition may prove to be important because it supports later exact quotient geometry, growth covariance, or other structures. But those are downstream tests.

The correct current status is:

\[
\boxed{
\text{bipartition preservation is a motivated but still chosen structural criterion}.
}
\]

That criterion should now be tested independently rather than silently baked into the foundation.

---

# 101. Result ledger

## Proved / exact

1. Every preserving reversal-support orbital has odd support.
2. Every preserving orbital union contains only odd supports.
3. LR3 is the unique smallest-support preserving orbital.
4. Any preserving uniform family nontrivial at \(n=6\) must contain LR3.
5. LR3 alone already supplies the required odd mixing and even fibre connectivity.
6. Hence LR3 is the unique inclusion-minimal rule under the declared criteria.

## Computationally certified

1. Named control rules through \(n=5,\ldots,9\).
2. Exhaustive orbital-union census where tractable.
3. Analytic union counts through even \(n=30\).
4. 50/50 strict checks pass.

## Falsified stronger claim

\[
\boxed{
\text{raw HC alone uniquely determines LR3}
}
\]

is **not supported**.

## Current conditional claim

\[
\boxed{
\text{raw HC}
+
\text{bipartition preservation}
+
\text{strict locality}
\Longrightarrow
LR3.
}
\]

---

# 102. Recommended next research step

RAW-05B exposes the next foundational audit:

### EHF-HC-RAW-06 — Bipartition Principle Stress Test

Question:

> Is intrinsic even-cycle bipartition preservation independently distinguished by the raw/growth mathematics, or is it merely a convenient criterion chosen because LR3 preserves it?

Possible tests:

1. compare preserving and non-preserving nearest-shell rules under \(n\to n+1\) completion;
2. test whether preserving rules uniquely support clean quotient/growth covariance;
3. compare spectral and coherent-configuration behaviour without importing later physics;
4. test whether the Johnson-labelled quotient arises specifically from preserved bipartitions or from broader nearest-shell structure.

This should be done before treating bipartition preservation as part of the permanent EHF definition lock.


---

# 103. EHF-HC-RAW-06 — Bipartition Principle Stress Test

## 103.1 Question

RAW-05B gave a conditional selection theorem:

\[
\text{raw HC}
+
\text{even-bipartition preservation}
+
\text{strict locality}
\Longrightarrow
LR3.
\]

But this left a potentially circular concern:

> Are we privileging the even bipartition only because LR3 happens to preserve it?

RAW-06 tests the bipartition principle against a second structure already motivated independently in the programme:

\[
\boxed{\text{all-slot }n\to n+1\text{ completion}.}
\]

The audit deliberately avoids physical interpretation. It asks only how the raw state space, the intrinsic even bipartitions, and alternative nearest-shell rules interact under exact one-site completion.

Controls:

- LR2;
- LR3;
- full 2-opt;
- LR4 as a non-preserving but growth-generative control.

---

# 104. Re-certified all-slot completion

For every \(C\in HC_n\), insert the new label \(n\) into each of the \(n\) cycle edges.

Deletion of the new label gives the inverse map.

Hence:

\[
\boxed{
HC_n\times\{\text{cycle edges}\}
\cong
HC_{n+1}.
}
\]

Equivalently,

\[
|HC_{n+1}|=n|HC_n|.
\]

RAW-06 rebuilt this independently for

\[
5\to6,\quad6\to7,\quad7\to8,\quad8\to9
\]

with:

- coverage \(=1\);
- duplicates \(=0\);
- deletion inverse \(=1\).

Thus the growth layer used in this stress test does not depend on cached CBB data.

---

# 105. Odd-to-even growth creates a regular bipartition incidence structure

Let

\[
n=2m-1
\]

be odd and insert the new label to obtain a child in \(HC_{2m}\).

Every child has an intrinsic unordered bipartition.

## Proposition 105.1

For a fixed odd parent \(C\), its \(n\) insertion edges produce children in \(n\) **distinct** even bipartition sectors.

### Reason

Take the bipartition of a child and delete the new label.

In the resulting odd parent cycle, the two former neighbours of the new label now form the unique edge whose endpoints lie in the same restricted colour class.

Therefore the insertion edge is recoverable from the child bipartition.

Two different insertion edges cannot produce the same bipartition.

Hence:

\[
\boxed{
\text{one odd parent}
\longrightarrow
n\text{ distinct even sectors}.
}
\]

This is exact and does not use LR3.

---

# 106. Regular incidence theorem

The odd-parent/even-sector incidence is biregular.

At \(n=2m-1\):

- each odd parent is incident to exactly
  \[
  2m-1
  \]
  target bipartition sectors;
- the number of target sectors is
  \[
  \frac12\binom{2m}{m};
  \]
- each target sector is incident to exactly
  \[
  \frac{(m-1)!m!}{2}
  \]
  distinct odd parents.

The right degree equals the even LR3 fibre size from RAW-05A.

Fresh census:

### \(5\to6\)

\[
12\text{ parents},
\qquad
10\text{ sectors},
\]

with

\[
5\text{ sectors per parent},
\qquad
6\text{ parents per sector}.
\]

### \(7\to8\)

\[
360\text{ parents},
\qquad
35\text{ sectors},
\]

with

\[
7\text{ sectors per parent},
\qquad
72\text{ parents per sector}.
\]

Thus the even bipartition structure is not an arbitrary label added after LR3.

It is an exact structure created by minimal one-site completion from the odd layer.

This gives the bipartition principle an independent structural motivation.

---

# 107. Even-to-odd growth removes the bipartition but retains it as parent data

For even source size \(2m\), the parent possesses an intrinsic bipartition.

After insertion, the target has odd size \(2m+1\) and therefore no graph bipartition.

Deletion of the new site recovers the unique even parent and hence its bipartition.

Thus the graded sequence naturally alternates:

\[
\boxed{
\text{odd layer: no intrinsic bipartition}
\quad\longrightarrow\quad
\text{even layer: bipartition created}
\quad\longrightarrow\quad
\text{odd layer: bipartition no longer intrinsic}.
}
\]

No parity-dependent rule is required to produce this alternation.

---

# 108. Growth-projection lemma for reversal support

Let

\[
\pi:HC_{n+1}\to HC_n
\]

delete the newest label.

Consider a target \(LR_\ell\) edge.

There are two cases.

### New label outside the reversed block

Deletion leaves the same \(\ell\)-block reversal between the parents:

\[
LR_\ell^{(n+1)}
\longrightarrow
LR_\ell^{(n)}.
\]

This is a faithful lift of old comparability.

### New label inside the reversed block

After deletion, the remaining old labels in that block form an \((\ell-1)\)-block reversal:

\[
LR_\ell^{(n+1)}
\longrightarrow
LR_{\ell-1}^{(n)}.
\]

With the convention

\[
LR_1=\mathrm{id},
\]

the projection law is:

\[
\boxed{
\pi\times\pi
\left(LR_\ell^{(n+1)}\right)
\subseteq
LR_\ell^{(n)}
\cup
LR_{\ell-1}^{(n)}.
}
\]

This is a structural support-filtration law induced by deletion.

---

# 109. LR2 under growth: new-site motion collapses to identity

Set \(\ell=2\).

The projection law becomes

\[
LR2^{(n+1)}
\longrightarrow
LR2^{(n)}
\cup
\mathrm{id}.
\]

Thus target LR2 moves involving the new label become **vertical edges** between children of the same parent.

There are no new cross-parent comparison types.

Fresh audits through \(8\to9\) give:

\[
\boxed{
\text{LR2 cross-parent novelty}=0.
}
\]

For \(n\to n+1\):

\[
\text{vertical fraction}
=
\frac{2}{n+1},
\]

and

\[
\text{faithful fraction}
=
\frac{n-1}{n+1}.
\]

Every source LR2 edge lifts, with uniform multiplicity.

So LR2 is strongly growth-compatible, but in a conservative sense:

> it copies old comparison and adds pure insertion-slot motion.

---

# 110. LR3 under growth: new-site motion becomes LR2 parent comparability

Set \(\ell=3\).

Then:

\[
\boxed{
LR3^{(n+1)}
\longrightarrow
LR3^{(n)}
\cup
LR2^{(n)}.
}
\]

If the new label lies outside the reversed triple, the edge is a faithful LR3 lift.

If the new label lies inside the triple, deletion produces an LR2 pair of parents.

Therefore LR3 completion creates comparison relations that were **not** source LR3 edges.

For \(n\ge6\):

\[
\boxed{
\text{cross fraction}
=
\frac{3}{n+1},
}
\]

\[
\boxed{
\text{faithful fraction}
=
\frac{n-2}{n+1},
}
\]

and

\[
\boxed{
\text{vertical fraction}=0.
}
\]

The complete fresh counts include:

### \(6\to7\)

\[
720\text{ faithful},
\qquad
540\text{ cross}.
\]

### \(7\to8\)

\[
6300\text{ faithful},
\qquad
3780\text{ cross}.
\]

### \(8\to9\)

\[
60480\text{ faithful},
\qquad
30240\text{ cross}.
\]

Every cross-parent pair was certified to be exactly LR2:

\[
\boxed{
\text{LR3 growth novelty}
=
\text{projected LR2 parent channels}.
}
\]

This gives a clean structural explanation for why LR2 repeatedly appears as a natural enrichment or diagnostic around LR3 without being part of the foundational same-layer rule.

---

# 111. Sector meaning of LR3 cross channels

When the source layer is even, RAW-05A says LR3 source edges stay within one intrinsic bipartition fibre.

RAW-06 finds something stronger about the target odd layer.

For

\[
6\to7
\]

all \(540\) LR3 cross-parent edges project to parents in **different** even bipartition sectors.

For

\[
8\to9
\]

all \(30240\) cross-parent edges do likewise.

There are:

\[
0
\]

cross edges whose parents share the same source bipartition.

Thus:

\[
\boxed{
\text{even LR3 preserves sectors internally,}
}
\]

while

\[
\boxed{
\text{completion to the odd layer creates cross-sector coupling.}
}
\]

This is the precise finite mechanism behind the qualitative phrase:

> growth preserves old local comparability while creating new local comparability.

---

# 112. Odd-to-even LR3 lifts respect the newly created sectors

At an odd source layer, each source LR3 edge has several faithful lifts to the even target.

RAW-06 finds that those faithful lifts lie in distinct target bipartition sectors.

### \(5\to6\)

Each source LR3 edge has:

\[
3
\]

faithful lifts in

\[
3
\]

distinct even sectors.

### \(7\to8\)

Each source LR3 edge has:

\[
5
\]

faithful lifts in

\[
5
\]

distinct even sectors.

So the old odd-layer comparability is replicated across multiple newly created even sectors rather than being concentrated in a preferred sector.

This is another neutrality property of the growth/bipartition interaction.

---

# 113. Full 2-opt control

Full 2-opt contains all nearest-shell reversal supports.

Under deletion, a support drop

\[
LR_\ell\to LR_{\ell-1}
\]

remains inside full 2-opt, except

\[
LR2\to\mathrm{id}.
\]

Therefore full 2-opt is projection-closed up to vertical identity motion.

RAW-06 finds:

\[
\boxed{
\text{full 2-opt cross-parent novelty}=0
}
\]

for every audited transition.

It has vertical edges and faithful edges only.

Thus the complete nearest shell is extremely compatible with growth, but precisely because it already contains the lower-support relations that LR3 growth creates as novel.

This distinguishes two structural philosophies:

\[
\text{full 2-opt}
=
\text{closure under all nearest-shell comparison},
\]

versus

\[
\text{LR3}
=
\text{minimal rule whose growth exposes a lower-support comparison channel}.
\]

---

# 114. LR4 control: growth generativity is independent of bipartition preservation

To ensure that LR3's growth novelty is not merely another way of restating bipartition preservation, RAW-06 tested LR4 at

\[
8\to9.
\]

LR4 is even-support and therefore **does not** preserve the source even bipartition.

Nevertheless:

\[
50400\text{ target edges are faithful},
\]

and

\[
40320\text{ are cross-parent edges},
\]

with

\[
0\text{ vertical edges}.
\]

Every cross-parent pair is exactly LR3:

\[
\boxed{
LR4^{(9)}
\to
LR4^{(8)}
\cup
LR3^{(8)}.
}
\]

Moreover, those LR3 cross parents remain in the same even bipartition sector.

Thus:

\[
\boxed{
\text{growth generativity}\not\Rightarrow
\text{bipartition preservation}.
}
\]

The two criteria are genuinely independent.

---

# 115. The independent-selector picture

RAW-06 therefore gives two different reasons to reject LR2.

## Selector A — even structural preservation

Odd-to-even completion creates an exact intrinsic bipartition incidence structure.

If the same-layer rule is required to preserve that structure while it exists, LR2 fails and LR3 passes.

## Selector B — growth generativity

If completion is required not merely to add vertical slot motion but to create genuinely new parent comparability, LR2 again fails and LR3 passes.

LR4 proves the selectors are not equivalent:

- LR4 passes growth generativity;
- LR4 fails bipartition preservation.

Higher odd supports such as LR5 can pass both, but they are less local.

Therefore the first reversal support satisfying both independent selectors is:

\[
\boxed{\ell=3.}
\]

---

# 116. Strengthened conditional selection principle

RAW-05B used:

\[
\text{minimal bipartition-preserving locality}.
\]

RAW-06 supports a stronger formulation:

> **Choose the smallest intrinsic nearest-shell reversal rule that preserves the structural bipartition created on even layers and, under one-site completion, both lifts old comparison and creates genuinely new nonvertical parent comparability.**

Within the reversal-support family this selects:

\[
\boxed{LR3}.
\]

Schematically:

\[
\boxed{
\text{raw HC}
+
\text{all-slot completion}
+
\text{even-structure preservation}
+
\text{growth generativity}
+
\text{minimality}
\Longrightarrow
LR3.
}
\]

This remains a **conditional selection theorem**.

The framework still chooses the desiderata.

What has improved is that the desiderata are now independently motivated and testable rather than reverse-engineered from LR3.

---

# 117. Bipartition-principle verdict

The bipartition principle survives RAW-06, with an important qualification.

### Supported

The bipartition is independently distinguished because:

1. it is intrinsic to every even Hamilton cycle;
2. odd-to-even all-slot completion creates it in an exact biregular incidence structure;
3. no slot, anchor, or label is privileged;
4. LR3 preserves it exactly on even layers;
5. the same rule becomes connected on odd layers where no such intrinsic structure exists.

### Not supported

Growth does **not** force us to demand its preservation.

Non-preserving rules such as LR4 can also have clean and generative growth behaviour.

Therefore:

\[
\boxed{
\text{bipartition preservation is structurally motivated, not logically compulsory}.
}
\]

That is the correct current foundational status.

---

# 118. Fresh certification ledger

All-slot completion was re-audited at:

\[
5\to6,\ 6\to7,\ 7\to8,\ 8\to9.
\]

Rule-growth projection was exhaustively audited for:

- LR2;
- LR3;
- full 2-opt;

across all four transitions, plus LR4 at \(8\to9\).

The odd-to-even sector incidence was exhaustively audited at:

\[
5\to6,\qquad7\to8.
\]

The audit certified:

- exact completion coverage and inverse;
- exact regular bipartition incidence;
- source-edge lift rate \(1\) for every tested rule;
- uniform faithful lift multiplicity;
- zero LR2 cross-parent novelty;
- zero full-2-opt cross-parent novelty;
- zero LR3 vertical motion;
- LR3 cross channels exactly equal LR2 parent pairs;
- even-source LR3 cross channels connect different bipartition sectors only;
- LR4 cross channels exactly equal LR3 parent pairs.

All:

\[
\boxed{76/76}
\]

strict checks passed.

---

# 119. What RAW-06 changes in the historical growth language

The old phrase

> growth preserves old local comparability while creating new local comparability

can now be made precise for raw LR3.

Under deletion:

\[
\boxed{
LR3_{n+1}
\to
LR3_n\cup LR2_n.
}
\]

The faithful branch is preserved old LR3 comparison.

The cross branch is newly exposed LR2 parent comparison.

So "new comparability" is no longer only a qualitative statement.

It has an exact support-lowering mechanism.

---

# 120. New structural hierarchy

The current raw foundation can now be written:

\[
HC_n
\]

\[
\downarrow
\]

intrinsic overlap and nearest-shell comparison,

\[
\downarrow
\]

reversal-support filtration

\[
LR_2,LR_3,LR_4,\ldots,
\]

together with

\[
HC_n\times\text{edge}
\cong HC_{n+1},
\]

and deletion law

\[
LR_\ell^{(n+1)}
\to
LR_\ell^{(n)}\cup LR_{\ell-1}^{(n)}.
\]

Even layers additionally carry intrinsic bipartitions, produced regularly from odd-layer completion.

LR3 is the smallest support simultaneously satisfying:

- preservation of that even structure;
- nonvertical growth generativity;
- odd mixing;
- uniform relabelling-covariant locality.

Only after this should OPW restrictions or Johnson dynamics be introduced.

---

# 121. Immediate next question

RAW-06 makes the next issue much sharper.

The natural next probe is not another attempt to justify LR3.

It is to understand the new exact support-lowering structure:

### EHF-HC-RAW-07 — Reversal-Support Growth Filtration

Target theorem:

\[
\boxed{
\pi(LR_\ell^{(n+1)})
=
LR_\ell^{(n)}
\cup
LR_{\ell-1}^{(n)}
}
\]

with exact multiplicities, boundary/complement exceptions, and composition under repeated growth/deletion.

Questions:

1. Does repeated deletion produce a genuine filtration
   \[
   LR_\ell\to LR_{\ell-1}\to\cdots\to LR_2\to\mathrm{id}?
   \]
2. What are the exact faithful/cross multiplicities for general \(\ell,n\)?
3. Does this explain why LR2 appears naturally around LR3 and LR3 around LR4?
4. How does this filtration interact with even bipartition sectors?

This is now a raw combinatorial theorem problem, independent of physical interpretation.


---

# 122. EHF-HC-RAW-07 — Reversal-Support Growth Filtration

## 122.1 Status

**Result:** exact one-step theorem, exact repeated-deletion counting law, and exhaustive finite certification.

RAW-06 found the first support-lowering examples:

\[
LR3_{n+1}\to LR3_n\cup LR2_n,
\]

and

\[
LR4_{n+1}\to LR4_n\cup LR3_n.
\]

RAW-07 derives the general rule for arbitrary reversal support and then composes it through repeated deletion.

No physical interpretation is used.

---

# 123. Intrinsic pair description

Let

\[
(C,D)
\]

be an \(LR_\ell\) pair in \(HC_N\), where

\[
2\le \ell\le\left\lfloor\frac N2\right\rfloor.
\]

RAW-04B showed that the common-edge graph

\[
E(C)\cap E(D)
\]

is the disjoint union of two paths whose vertex sizes are

\[
\boxed{\{\ell,N-\ell\}.}
\]

This pair of path sizes is intrinsic. It is therefore the cleanest language for studying deletion.

---

# 124. One-site deletion theorem

Let

\[
\pi:HC_N\to HC_{N-1}
\]

delete the newest label.

Deleting one vertex shortens exactly one of the two common paths.

If the deleted vertex lies on the \(\ell\)-path, the path-size pair becomes

\[
\{\ell-1,N-\ell\}.
\]

If it lies on the other path, it becomes

\[
\{\ell,N-\ell-1\}.
\]

Therefore the effective reversal support can change by at most one.

## Generic case

If

\[
\ell<\frac N2,
\]

then:

\[
\boxed{
\pi(LR_\ell^{(N)})
\subseteq
LR_\ell^{(N-1)}
\cup
LR_{\ell-1}^{(N-1)}.
}
\]

For

\[
\ell=2,
\]

interpret

\[
LR_1=\mathrm{id}.
\]

Thus:

\[
LR2^{(N)}
\to
LR2^{(N-1)}
\cup
\mathrm{id}.
\]

## Half-cycle boundary

If

\[
N=2\ell,
\]

the two paths have equal size.

Deleting a vertex from either path gives

\[
\{\ell-1,\ell\}.
\]

Hence every target edge collapses to effective support

\[
\ell-1.
\]

So:

\[
\boxed{
LR_{N/2}^{(N)}
\to
LR_{N/2-1}^{(N-1)}
}
\]

with no separate stay branch.

This is the exact complement/half-cycle exception.

---

# 125. Exact number of \(LR_\ell\) edges

For

\[
2\le\ell<\frac N2,
\]

every state has \(N\) distinct \(LR_\ell\) neighbours.

Therefore:

\[
\boxed{
|E_{N,\ell}|=\frac{N!}{4}.
}
\]

At the half-cycle boundary

\[
N=2\ell,
\]

complementary reversed blocks generate the same neighbour and the degree is \(N/2\). Hence:

\[
\boxed{
|E_{N,N/2}|=\frac{N!}{8}.
}
\]

These formulas are exact.

---

# 126. Generic one-step edge split

Assume

\[
\ell<\frac N2.
\]

By relabelling symmetry, the newest label lies on the short \(\ell\)-path in the fraction

\[
\frac{\ell}{N}
\]

of all \(LR_\ell\) edges, and on the long path in fraction

\[
\frac{N-\ell}{N}.
\]

Therefore:

\[
\boxed{
E_{N,\ell\to\ell}
=
\frac{N-\ell}{N}|E_{N,\ell}|
=
\frac{(N-\ell)(N-1)!}{4},
}
\]

and

\[
\boxed{
E_{N,\ell\to\ell-1}
=
\frac{\ell}{N}|E_{N,\ell}|
=
\frac{\ell(N-1)!}{4}.
}
\]

For \(\ell=2\), the second term is the vertical/identity branch.

The fractions are therefore:

\[
\boxed{
P(\text{stay at }\ell)=\frac{N-\ell}{N},
}
\]

\[
\boxed{
P(\text{drop to }\ell-1)=\frac{\ell}{N}.
}
\]

These are counting fractions over the finite edge orbital, not physical transition probabilities.

---

# 127. Exact lift multiplicities

## Lower-support lifts

For every generic target class, each source \(LR_{\ell-1}\) edge has exactly

\[
\boxed{\ell}
\]

target \(LR_\ell\) lifts in the lower-support branch.

This follows from

\[
E_{N,\ell\to\ell-1}
=
\ell\,|E_{N-1,\ell-1}|.
\]

The law includes:

\[
LR3\to LR2:
\qquad3\text{ lifts per source LR2 edge},
\]

and

\[
LR4\to LR3:
\qquad4\text{ lifts per source LR3 edge}.
\]

At the target half-cycle boundary \(N=2\ell\), **all** target edges belong to this branch and each source \(LR_{\ell-1}\) edge still has exactly \(\ell\) lifts.

## Faithful lifts

If source support \(\ell\) is not itself a half-cycle class, each source \(LR_\ell\) edge has

\[
\boxed{N-\ell}
\]

faithful target lifts.

If the source layer \(N-1\) is even and

\[
\ell=\frac{N-1}{2},
\]

the source edge has two complementary block representatives. The faithful multiplicity doubles:

\[
\boxed{
2(N-\ell).
}
\]

Example:

\[
6\to7,\quad \ell=3:
\]

each source half-cycle LR3 edge has

\[
2(7-3)=8
\]

faithful lifts.

This exactly explains the previously exceptional-looking multiplicity \(8\).

---

# 128. LR2 vertical fibres

For \(\ell=2\), the lower branch becomes identity.

The number of vertical target LR2 edges is:

\[
\boxed{
\frac{(N-1)!}{2}.
}
\]

Since

\[
|HC_{N-1}|=\frac{(N-2)!}{2},
\]

each parent growth fibre contains exactly

\[
\boxed{N-1}
\]

vertical LR2 edges.

The \(N-1\) children of a fixed parent correspond to insertion into its \(N-1\) cycle edges, and LR2 moves the new label between adjacent insertion positions.

Thus each growth fibre carries a canonical cycle of insertion-slot motion.

This is why LR2 growth adds vertical structure rather than new parent comparability.

---

# 129. A genuine support filtration

Define:

\[
\mathcal F_1^{(N)}=\mathrm{id},
\]

and for \(q\ge2\),

\[
\boxed{
\mathcal F_q^{(N)}
=
\mathrm{id}
\cup
LR_2^{(N)}
\cup\cdots\cup
LR_q^{(N)},
}
\]

truncated at \(\lfloor N/2\rfloor\) where necessary.

The one-step theorem gives:

\[
\boxed{
\pi(\mathcal F_q^{(N)})
\subseteq
\mathcal F_q^{(N-1)}.
}
\]

More sharply, an individual level obeys:

\[
\boxed{
LR_\ell
\to
LR_\ell\cup LR_{\ell-1},
}
\]

with half-cycle collapse and \(LR_1=\mathrm{id}\).

Thus the reversal supports form an exact deletion-compatible filtration.

---

# 130. Repeated deletion

Now delete a fixed set of \(k\) newest labels.

Let:

\[
M=N-k.
\]

Start from an \(LR_\ell\) pair with common path sizes

\[
\{\ell,N-\ell\}.
\]

Suppose exactly \(s\) of the \(k\) deleted labels lie on the \(\ell\)-path.

Then the remaining path sizes are:

\[
\boxed{
\{\ell-s,\ N-\ell-(k-s)\}.
}
\]

If either remaining path has size at most \(1\), the two ancestor cycles coincide.

Otherwise the ancestor pair is the effective reversal class

\[
\boxed{
LR_{\min(\ell-s,\ M-(\ell-s))}.
}
\]

Therefore repeated deletion can never increase reversal support.

---

# 131. Exact hypergeometric law

The \(LR_\ell\) edge set is one relabelling orbital.

For \(\ell<N/2\), the short path is uniquely determined. Relative to a fixed \(k\)-label deletion set, the number \(s\) of deleted labels lying on it has the exact hypergeometric counting law:

\[
\boxed{
\Pr(S=s)
=
\frac{
\binom{\ell}{s}
\binom{N-\ell}{k-s}
}{
\binom Nk
}.
}
\]

At the half-cycle boundary, the two paths are interchangeable, but the projected effective support is symmetric under

\[
s\leftrightarrow k-s,
\]

so the same aggregated formula applies.

Again, \(\Pr\) here denotes a finite counting fraction over a uniform orbital, not physical probability.

---

# 132. Exact repeated-deletion count formula

Define:

\[
\epsilon_M(r)
=
\begin{cases}
0,&r\le1\text{ or }M-r\le1,\\[1mm]
\min(r,M-r),&\text{otherwise}.
\end{cases}
\]

Here \(0\) denotes the identity relation.

Then the number of target \(LR_\ell\) edges that project after \(k\) deletions to effective level \(e\) is:

\[
\boxed{
C_{N,\ell,k}(e)
=
\frac{|E_{N,\ell}|}{\binom Nk}
\sum_{\substack{s\\
\epsilon_{N-k}(\ell-s)=e}}
\binom{\ell}{s}
\binom{N-\ell}{k-s}.
}
\]

This is an exact integer.

The full sum satisfies:

\[
\sum_e C_{N,\ell,k}(e)=|E_{N,\ell}|.
\]

RAW-07 checked the integrality and total law through:

\[
N\le20,\qquad k\le4.
\]

---

# 133. The staircase exists, but it is not deterministic

The original RAW-07 question suggested:

\[
LR_\ell
\to LR_{\ell-1}
\to\cdots\to LR_2\to\mathrm{id}.
\]

The exact answer is:

> **Yes as a filtration branch; no as a deterministic trajectory.**

If each successive deleted label lies on the currently shorter reversed path, support descends by one at every step:

\[
LR_\ell
\to
LR_{\ell-1}
\to
LR_{\ell-2}
\to\cdots.
\]

But if a deleted label lies on the other common path, the support can remain unchanged.

Hence the true structure is a branching filtration:

\[
\boxed{
\ell
\longrightarrow
\{\ell,\ell-1\}
}
\]

at each generic deletion.

Repeated deletion produces the hypergeometric mixture of all admissible branches.

---

# 134. Direct staircase count

For \(k<\ell\), the branch that descends at every deletion requires all \(k\) deleted labels to lie on the initial \(\ell\)-path.

Its counting fraction is:

\[
\boxed{
\frac{\binom{\ell}{k}}{\binom Nk}.
}
\]

Equivalently, in ordered sequential-deletion form:

\[
\boxed{
\frac{\ell}{N}
\frac{\ell-1}{N-1}
\cdots
\frac{\ell-k+1}{N-k+1}.
}
\]

This is the exact no-replacement descent branch.

---

# 135. Selected examples

## \(LR4\) at \(N=9\), delete two labels

There are:

\[
|E_{9,4}|=90720
\]

target edges.

After two deletions:

\[
\boxed{
15120\to LR2,
}
\]

\[
\boxed{
75600\to LR3.
}
\]

No \(LR4\) relation survives because the ancestor has size \(7\), where effective support \(4\) is complementary to support \(3\).

## \(LR4\) at \(N=10\), delete three labels

There are:

\[
907200
\]

target edges.

The exact ancestor distribution is:

\[
\boxed{
30240\to\mathrm{id},
}
\]

\[
\boxed{
272160\to LR2,
}
\]

\[
\boxed{
604800\to LR3.
}
\]

## \(LR5\) at \(N=12\), delete three labels

There are:

\[
119750400
\]

target edges.

The exact distribution is:

\[
5443200\to LR2,
\]

\[
38102400\to LR3,
\]

\[
76204800\to LR4.
\]

These are exact combinatorial counts.

---

# 136. Exhaustive finite certification

RAW-07 enumerated every Hamilton cycle and every \(LR_\ell\) edge for:

\[
5\le N\le9.
\]

For each available support class and up to three successive deletions, it compared the observed ancestor-support distribution with the exact hypergeometric formula.

All matches were exact.

The broader symbolic/formula ledger included:

- one-step formulas through
  \[
  N=30;
  \]
- repeated-deletion formulas through
  \[
  N=20,\quad k\le4.
  \]

All:

\[
\boxed{1250/1250}
\]

strict checks passed.

---

# 137. Structural interpretation

The reversal classes are not merely a list of unrelated local moves.

Growth/deletion organizes them into a graded hierarchy:

\[
\boxed{
\cdots
\to LR5
\to LR4
\to LR3
\to LR2
\to\mathrm{id}.
}
\]

The arrows mean **available support-lowering channels under deletion**, not that every edge follows the arrow.

The filtration explains several historical observations:

- LR2 appears naturally as the lower channel of LR3 growth;
- LR3 appears naturally as the lower channel of LR4 growth;
- full 2-opt is closed under this support lowering;
- a single fixed-support rule is generally not deletion-closed unless lower supports are included.

Thus:

\[
\boxed{
\text{full 2-opt}
=
\text{support-filtration closure of the nearest reversal classes}.
}
\]

LR3, by contrast, is deliberately a non-closed minimal slice whose growth exposes LR2 as a new channel.

---

# 138. Relation to the bipartition principle

For even layers:

\[
LR_\ell\text{ preserves intrinsic bipartition}
\iff
\ell\text{ odd}.
\]

But deletion can lower support by one, changing its parity.

Therefore support lowering naturally alternates between:

\[
\text{bipartition-preserving odd support}
\]

and

\[
\text{bipartition-changing even support}.
\]

In particular:

\[
LR3\to LR2
\]

and

\[
LR4\to LR3.
\]

This makes the preservation/non-preservation distinction part of a larger graded support structure rather than two unrelated families.

No physical parity interpretation is claimed.

---

# 139. Revised status of the growth structure

The raw graded object now contains three exact layers:

### State completion

\[
HC_{N-1}\times\{\text{insertion edge}\}
\cong
HC_N.
\]

### Pair-support filtration

\[
LR_\ell^{(N)}
\to
LR_\ell^{(N-1)}
\cup
LR_{\ell-1}^{(N-1)}.
\]

### Repeated-deletion counting

\[
C_{N,\ell,k}(e)
\]

given exactly by the hypergeometric formula.

This is substantially stronger than the earlier qualitative statement that growth is compatible with LR3.

It gives an exact finite algebra of how local comparison support changes across size.

---

# 140. What is not yet established

RAW-07 does not establish:

1. that reversal support has a physical meaning;
2. that deletion is physical time reversal;
3. that the hypergeometric counting fraction is a probability law of nature;
4. that full 2-opt should replace LR3;
5. that the support filtration alone determines an amplitude or action;
6. that growth must occur physically.

The result is an exact combinatorial growth filtration.

---

# 141. Immediate next questions

RAW-07 opens two natural directions.

### EHF-HC-RAW-08A — Growth-Filtration Algebra

Construct operators

\[
D_{\ell\to\ell},
\qquad
D_{\ell\to\ell-1}
\]

between edge modules of adjacent layers and test composition, commutation, rank, kernels, and whether the repeated hypergeometric law comes from a simple operator algebra.

### EHF-HC-RAW-08B — Intrinsic Bipartition / Johnson Quotient Reconstruction

Now that even bipartitions and their growth incidence have been derived intrinsically, rebuild the Johnson-labelled sector space from scratch and determine exactly which raw/growth relations induce Johnson adjacency versus higher association shells.

The second route reconnects directly to the historical Johnson core; the first develops the new raw theorem further.
