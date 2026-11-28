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


---

# 142. EHF-HC-RAW-08B — Intrinsic Bipartition / Johnson Quotient Reconstruction

## 142.1 Purpose

Earlier EHF/RAF work used an even-sector map into a Johnson-type subset space.

The raw rebuild now permits that construction to be derived in the correct order:

\[
HC_{2m}
\longrightarrow
\text{intrinsic cycle bipartitions}
\longrightarrow
\text{anchor chart}
\longrightarrow
\text{Johnson subset coordinates}.
\]

RAW-08B asks four questions.

1. What is the intrinsic even-sector space before choosing an anchor?
2. Why does a Johnson vertex set appear after anchoring?
3. Which raw reversal classes induce which sector relations?
4. Which parts of the historical weighted Johnson quotient are intrinsic, and which depend on the anchor chart?

No physical interpretation is used.

---

# 143. Intrinsic even-sector space

Let

\[
V=\{0,1,\ldots,2m-1\}.
\]

Every Hamilton cycle

\[
C\in HC_{2m}
\]

is an even cycle graph and has a unique graph bipartition up to interchange:

\[
\Pi(C)=\{A_C,A_C^c\},
\qquad
|A_C|=|A_C^c|=m.
\]

Define the intrinsic sector space

\[
\boxed{
\mathcal B_m
=
\left\{
\{A,A^c\}:
A\subset V,\ |A|=m
\right\}.
}
\]

Since \(A\) and \(A^c\) define the same sector,

\[
\boxed{
|\mathcal B_m|
=
\frac12\binom{2m}{m}.
}
\]

Using

\[
\frac12\binom{2m}{m}
=
\binom{2m-1}{m-1},
\]

this reproduces the historical even-sector count without using canonical-position parity as the definition.

---

# 144. Anchor chart and Johnson vertex set

Choose one anchor label

\[
a\in V.
\]

For each intrinsic bipartition

\[
P=\{A,A^c\},
\]

exactly one block contains \(a\).

Call that block \(A_a(P)\).

Remove the anchor:

\[
\boxed{
\chi_a(P)=A_a(P)\setminus\{a\}.
}
\]

Then

\[
|\chi_a(P)|=m-1,
\]

and

\[
\chi_a(P)\subset V\setminus\{a\},
\qquad
|V\setminus\{a\}|=2m-1.
\]

Therefore:

\[
\boxed{
\chi_a:
\mathcal B_m
\overset{\sim}{\longrightarrow}
\binom{V\setminus\{a\}}{m-1}.
}
\]

This is a bijection.

Thus the Johnson-type **vertex set** does not need to be postulated.

It is an anchor chart on the intrinsic equal-bipartition space.

By taking complements inside the \(2m-1\) non-anchor labels,

\[
\binom{[2m-1]}{m-1}
\cong
\binom{[2m-1]}{m},
\]

so this is equivalent to the \(m\)-subset convention used in the historical exact Johnson transport notes.

---

# 145. Sector fibre size

Fix an intrinsic bipartition

\[
P=\{A,A^c\}.
\]

A Hamilton cycle has sector \(P\) exactly when it alternates between the two \(m\)-element blocks.

Anchor one label and count oriented alternating cyclic presentations.

There are:

\[
(m-1)!
\]

orders for the remaining labels on the anchor side and

\[
m!
\]

orders for the opposite side.

Reflection identifies the two orientations.

Hence every intrinsic sector contains exactly

\[
\boxed{
f_m
=
\frac{(m-1)!m!}{2}
}
\]

Hamilton cycles.

The state-space factorization is therefore

\[
\boxed{
|HC_{2m}|
=
|\mathcal B_m|\,f_m.
}
\]

Indeed,

\[
\frac12\binom{2m}{m}
\frac{(m-1)!m!}{2}
=
\frac{(2m-1)!}{2}.
\]

This is now an anchor-free derivation of the historical fibre-size law.

---

# 146. Johnson distance is a chart coordinate, not the intrinsic distance

Let

\[
P,Q\in\mathcal B_m.
\]

Choose the anchor chart and write

\[
S=\chi_a(P),
\qquad
T=\chi_a(Q).
\]

Their Johnson distance is

\[
\boxed{
r=d_J(S,T)=|S\setminus T|.
}
\]

Because both anchor-containing blocks contain \(a\), this is also

\[
r=|A_a(P)\setminus A_a(Q)|.
\]

But the intrinsic bipartitions are unordered.

We may compare \(A_a(P)\) either with \(A_a(Q)\) or with its complementary block.

Therefore the anchor-free distance is

\[
\boxed{
\delta(P,Q)
=
\min(r,m-r).
}
\]

Its range is

\[
0\le\delta\le\left\lfloor\frac m2\right\rfloor.
\]

Thus the anchor chart **unfolds** one intrinsic distance shell into the two Johnson shells

\[
\boxed{
r=s
\quad\text{and}\quad
r=m-s,
}
\]

except at the midpoint \(m=2s\), where the two coincide.

This is the first major correction to the informal phrase “the intrinsic sector space is a Johnson graph.”

The **vertex set** is Johnson-charted.

The fully anchor-free pair geometry is more symmetric.

---

# 147. Intrinsic shell valencies

Fix one intrinsic sector \(P\).

For

\[
1\le s<\frac m2,
\]

an intrinsic sector at distance \(s\) is obtained by choosing:

- \(s\) labels from one block;
- \(s\) labels from the other block;

and exchanging them.

Hence:

\[
\boxed{
\nu_s
=
\binom ms^2,
\qquad
2s<m.
}
\]

If

\[
m=2s,
\]

the exchange and its complementary exchange describe the same unordered bipartition, so:

\[
\boxed{
\nu_{m/2}
=
\frac12\binom{m}{m/2}^2.
}
\]

These valencies sum to

\[
|\mathcal B_m|-1.
\]

In the anchor chart, the same intrinsic shell splits into Johnson shell counts

\[
N_s
=
\binom{m-1}{s}\binom ms
\]

and

\[
N_{m-s}
=
\binom{m-1}{s-1}\binom ms.
\]

Pascal's identity gives:

\[
N_s+N_{m-s}
=
\binom ms^2
=
\nu_s.
\]

So the folding is exact.

---

# 148. Raw reversal support and intrinsic sector distance

RAW-04B proved:

\[
LR_\ell\text{ preserves the intrinsic bipartition}
\iff
\ell\text{ is odd}.
\]

Now let

\[
\ell=2s
\]

be even.

A reversal of \(2s\) consecutive labels contains exactly:

\[
s
\]

labels from each side of the original bipartition.

All \(2s\) labels switch bipartition class after reversal.

Therefore:

\[
\boxed{
LR_{2s}
\text{ moves between intrinsic sectors at distance }s.
}
\]

Thus the sector action of the raw reversal filtration is:

\[
\boxed{
LR_{2s+1}:\quad\delta=0,
}
\]

\[
\boxed{
LR_{2s}:\quad\delta=s.
}
\]

This is anchor-free.

---

# 149. How one intrinsic reversal shell appears in a Johnson chart

For an \(LR_{2s}\) move, whether the anchor lies inside the reversed path determines the chart distance.

### Anchor outside the reversed path

The anchor-containing block changes by exactly \(s\) labels:

\[
r=s.
\]

### Anchor inside the reversed path

The child block containing the anchor is the complementary representative of the changed bipartition, giving

\[
r=m-s.
\]

Hence:

\[
\boxed{
LR_{2s}
\quad\longleftrightarrow\quad
A_s\cup A_{m-s}
}
\]

in an anchor-based Johnson association scheme.

At the midpoint

\[
m=2s,
\]

this is a single shell.

This immediately shows:

\[
\boxed{
LR2
\text{ does not quotient intrinsically to }A_1\text{ alone}.
}
\]

Rather,

\[
\boxed{
LR2
\quad\longleftrightarrow\quad
A_1\cup A_{m-1}.
}
\]

A pure Johnson \(A_1\) rule therefore requires an additional chart-sensitive selection.

---

# 150. Exact sector-pair edge weight

Fix two sectors \(P,Q\) whose anchor-chart Johnson distance is \(r\).

Let the anchor-containing blocks be \(A\) and \(B\).

Define:

\[
X=A\setminus B,
\qquad
Y=B\setminus A.
\]

Then:

\[
|X|=|Y|=r.
\]

A 2-opt edge between the two sectors has two common-edge paths whose vertex sets are:

\[
X\cup Y
\]

and its complement.

Both are balanced with respect to the source bipartition.

The first path contains \(r+r\) vertices.

The number of undirected alternating Hamilton paths on those vertices with opposite-type endpoints is:

\[
(r!)^2.
\]

The complementary path contributes:

\[
((m-r)!)^2.
\]

For each pair of such paths, the two possible cross-connections are exactly the two Hamilton cycles forming one 2-opt edge.

Therefore the number of raw 2-opt edges between the two fixed sector fibres is:

\[
\boxed{
w_r(m)
=
\left(r!(m-r)!\right)^2.
}
\]

This is now a direct anchor-free/common-path proof of the historical weight law.

The symmetry is immediate:

\[
\boxed{
w_r(m)=w_{m-r}(m).
}
\]

The two chart shells are the same intrinsic distance shell.

---

# 151. The historical weighted Johnson formula is recovered

Let

\[
A_r
\]

denote the distance-\(r\) matrix of the Johnson scheme on

\[
\binom{[2m-1]}{m-1}.
\]

Define the fibre-aggregated cross-sector edge-count matrix

\[
Q_m(P,Q)
=
\#\{
\text{2-opt edges between fibres }P,Q
\}.
\]

Then:

\[
\boxed{
Q_m
=
\sum_{r=1}^{m-1}
\left(r!(m-r)!\right)^2 A_r.
}
\]

Thus RAW-08B independently recovers the exact Core C weighted Johnson formula.

An important terminology correction is required.

This matrix is a:

\[
\boxed{
\text{fibre-aggregated sector edge-count operator}.
}
\]

The sector partition is not an ordinary equitable partition with integer per-state intersection numbers: for example,

\[
w_r/f_m
\]

need not be an integer.

So “weighted quotient” is acceptable as shorthand, but it should not be confused with an equitable graph quotient.

---

# 152. Exact quotient of a single reversal class

The reconstruction is sharper than the full 2-opt formula.

For odd support:

\[
\boxed{
LR_{2s+1}
}
\]

has no off-diagonal sector action because it preserves each intrinsic bipartition.

For even support:

\[
\boxed{
LR_{2s}
}
\]

contributes only to the chart shells

\[
s
\]

and

\[
m-s.
\]

Therefore, for \(2s<m\),

\[
\boxed{
Q_m^{(LR_{2s})}
=
w_s(m)
\left(A_s+A_{m-s}\right).
}
\]

At the midpoint

\[
m=2s,
\]

\[
\boxed{
Q_m^{(LR_m)}
=
w_{m/2}(m)A_{m/2}.
}
\]

Full 2-opt is the sum over all even supports plus sector-internal odd-support edges.

This gives an exact raw-HC origin for every distance shell in the historical weighted operator.

---

# 153. Degree split

The full 2-opt degree on \(HC_{2m}\) is:

\[
\boxed{
d_{\rm 2opt}
=
m(2m-3).
}
\]

Summing the odd-support reversal classes gives the sector-preserving degree:

\[
\boxed{
d_{\rm preserve}
=
m(m-2).
}
\]

Summing the even-support classes gives the sector-changing degree:

\[
\boxed{
d_{\rm change}
=
m(m-1).
}
\]

Hence:

\[
d_{\rm preserve}+d_{\rm change}
=
m(2m-3).
\]

There is a potentially misleading numerical coincidence:

\[
\boxed{
d_{\rm change}
=
m(m-1)
=
\deg J(2m-1,m-1).
}
\]

This equality of degrees does **not** mean the cross-sector 2-opt process is Johnson single-swap adjacency.

The raw cross-sector operator has support on every Johnson distance:

\[
r=1,\ldots,m-1.
\]

This distinction is now explicit.

---

# 154. Johnson shell counts and weighted row sum

The number of anchor-chart sectors at Johnson distance \(r\) is:

\[
\boxed{
N_r
=
\binom{m-1}{r}\binom mr.
}
\]

Multiplying by the pair weight gives:

\[
N_rw_r
=
\binom{m-1}{r}\binom mr
\left(r!(m-r)!\right)^2.
\]

This simplifies exactly to:

\[
\boxed{
N_rw_r
=
(m-1)!m!(m-r).
}
\]

Summing:

\[
\sum_{r=1}^{m-1}N_rw_r
=
\frac{(m-1)!m!}{2}m(m-1).
\]

Therefore:

\[
\boxed{
\sum_rN_rw_r
=
f_m\,d_{\rm change}.
}
\]

This is the exact fibre edge-volume identity.

---

# 155. New intrinsic shell equalization law

The anchor-free description produces an unexpectedly simple result.

For an intrinsic distance shell

\[
1\le s<\frac m2,
\]

the number of sectors is

\[
\nu_s=\binom ms^2,
\]

and each sector pair carries

\[
w_s=(s!(m-s)!)^2
\]

raw cross edges.

Therefore the total number of cross edges from one fixed fibre into the entire intrinsic shell is:

\[
\nu_sw_s
=
\binom ms^2
(s!(m-s)!)^2.
\]

Everything cancels:

\[
\boxed{
\nu_sw_s
=
(m!)^2.
}
\]

This is **independent of \(s\)**.

At the midpoint \(m=2s\), unordered complement identification halves the number of sectors:

\[
\boxed{
\nu_{m/2}w_{m/2}
=
\frac{(m!)^2}{2}.
}
\]

Thus, apart from the self-complement midpoint factor, every intrinsic bipartition-distance shell carries the same aggregate raw 2-opt edge count.

This was not required by the historical Johnson formula; it becomes obvious only after refolding the anchor chart back to intrinsic unordered bipartitions.

---

# 156. Normalized intrinsic shell distribution

If one:

1. chooses a source Hamilton cycle uniformly inside a fixed sector;
2. chooses uniformly among its sector-changing 2-opt edges;

then the induced sector kernel has pair probability proportional to \(w_s\).

Aggregating by intrinsic distance:

### Odd \(m\)

There are

\[
\frac{m-1}{2}
\]

nonzero intrinsic shells, and every shell has exactly equal aggregate weight.

Hence:

\[
\boxed{
P(\delta=s)
=
\frac{2}{m-1}
}
\]

for every

\[
s=1,\ldots,\frac{m-1}{2}.
\]

### Even \(m\)

For

\[
s<m/2,
\]

\[
\boxed{
P(\delta=s)
=
\frac{2}{m-1}.
}
\]

For the midpoint:

\[
\boxed{
P(\delta=m/2)
=
\frac{1}{m-1}.
}
\]

These are induced finite counting probabilities under a declared uniform edge-selection rule, not physical probabilities.

---

# 157. Exhaustive certification

RAW-08B exhaustively generated complete source fibres for:

\[
m=3,4,5,
\]

corresponding to:

\[
n=6,8,10.
\]

For every source cycle, every full 2-opt neighbour was generated and classified by target intrinsic sector and anchor-chart Johnson distance.

The exact sector-pair weights were recovered.

## \(m=3\)

\[
f_3=6.
\]

Weights:

\[
r=1:\quad4,
\]

\[
r=2:\quad4.
\]

## \(m=4\)

\[
f_4=72.
\]

Weights:

\[
r=1:\quad36,
\]

\[
r=2:\quad16,
\]

\[
r=3:\quad36.
\]

## \(m=5\)

\[
f_5=1440.
\]

Weights:

\[
r=1:\quad576,
\]

\[
r=2:\quad144,
\]

\[
r=3:\quad144,
\]

\[
r=4:\quad576.
\]

Every target sector in a fixed Johnson shell had exactly the predicted pair weight.

The analytic identity ledger was checked through:

\[
m=12.
\]

All:

\[
\boxed{220/220}
\]

strict checks passed.

---

# 158. Reconciliation with historical Core C

The old Core C document reported:

\[
w_r(m)=\left(r!(m-r)!\right)^2
\]

and

\[
Q_m
=
\sum_{r=1}^{m-1}w_rA_r.
\]

RAW-08B confirms these formulas independently from the intrinsic bipartition construction.

The conceptual improvement is the dependency chain:

\[
\boxed{
\text{even Hamilton cycle}
\to
\text{intrinsic unordered bipartition}
\to
\text{anchor chart}
\to
\text{Johnson coordinates}
\to
\text{weighted sector operator}.
}
\]

The Johnson coordinates are not the primitive sector object.

They are a chart on it.

---

# 159. Reconciliation with the standalone Johnson transport core

The historical Johnson transport model uses ordinary single-swap adjacency:

\[
A_1.
\]

RAW-08B shows that this adjacency is **not** the direct anchor-free quotient of:

- raw LR3;
- raw LR2;
- full raw 2-opt.

Specifically:

\[
LR3
\]

is sector-internal,

\[
LR2
\]

charts to

\[
A_1+A_{m-1},
\]

and full 2-opt charts to

\[
\sum_{r=1}^{m-1}w_rA_r.
\]

Therefore the precise bridge to the standalone Johnson walk remains:

\[
\boxed{
\text{an additional reduction/selection is required to isolate }A_1.
}
\]

For example, after choosing an anchor, the \(r=1\) half of LR2 may be selected.

But that selection is chart-relative because the anchor-free nearest sector shell contains both:

\[
r=1
\]

and

\[
r=m-1.
\]

This is a crucial distinction for the rebuilt EHF hierarchy.

---

# 160. Current status of “Johnson emergence”

The strongest safe statement is now:

> **The intrinsic even Hamilton-cycle sector space is the space of unordered equal bipartitions. Choosing an anchor gives a canonical subset chart isomorphic to the Johnson vertex set. Full 2-opt induces a fibre-aggregated operator lying in the Johnson association algebra, with exact weights \(w_r=(r!(m-r)!)^2\). Ordinary Johnson single-swap adjacency is a further chart-level selection, not the full intrinsic quotient.**

Thus:

\[
\boxed{
\text{Johnson vertex geometry: derived as a chart}
}
\]

and

\[
\boxed{
\text{weighted Johnson association operator: derived from full 2-opt}
}
\]

but

\[
\boxed{
\text{plain Johnson }A_1\text{ dynamics: not yet derived intrinsically}.
}
\]

This resolves an ambiguity that persisted across the earlier Core A/Core C documents.

---

# 161. Result ledger

## Exact/proved

1. Intrinsic sectors are unordered equal bipartitions.
2. Their number is
   \[
   \frac12\binom{2m}{m}.
   \]
3. An anchor gives a bijection with
   \[
   \binom{[2m-1]}{m-1}.
   \]
4. Each sector fibre has
   \[
   \frac{(m-1)!m!}{2}
   \]
   cycles.
5. Anchor Johnson distance \(r\) folds to intrinsic distance
   \[
   \min(r,m-r).
   \]
6. \(LR_{2s}\) changes sector by intrinsic distance \(s\).
7. \(LR_{2s+1}\) is sector-internal.
8. Sector-pair edge weight is
   \[
   (r!(m-r)!)^2.
   \]
9. Full 2-opt gives the weighted Johnson association-algebra operator.
10. LR2 charts to \(A_1+A_{m-1}\), not \(A_1\) alone.
11. Sector-changing degree is
    \[
    m(m-1).
    \]
12. Intrinsic shell aggregate edge count is constant:
    \[
    (m!)^2
    \]
    except for the midpoint half-factor.

## Computationally certified

1. Complete source-fibre enumeration for
   \[
   n=6,8,10.
   \]
2. Exact pair weights for every target sector.
3. Analytic identities through
   \[
   m=12.
   \]
4. 220/220 strict checks.

## Corrected historical statement

Do not say:

> the full raw Hamilton-cycle quotient is the Johnson graph.

Prefer:

> the intrinsic sector space admits a Johnson subset chart, while full 2-opt induces a weighted operator in the Johnson association algebra.

---

# 162. Immediate next questions

RAW-08B leaves two especially sharp targets.

### EHF-HC-RAW-09A — Johnson \(A_1\) Selection Audit

Determine whether ordinary single-swap Johnson adjacency can be selected by a natural additional structure that is:

- growth-compatible;
- chart-covariant across anchor changes;
- not simply hard-coded as \(r=1\).

This directly tests the historical exact Johnson transport bridge.

### EHF-HC-RAW-09B — Intrinsic Equipartition Quotient Spectrum

Work directly on the anchor-free distance classes

\[
\delta=0,\ldots,\lfloor m/2\rfloor
\]

and diagonalize the intrinsic full-2-opt sector operator.

This may explain the historical paired Johnson eigenvalues from the underlying \(r\leftrightarrow m-r\) folding symmetry.

The recommended next step is **RAW-09A** if the priority is to justify the historical Johnson single-swap transport model, and **RAW-09B** if the priority is to understand the new intrinsic quotient mathematics first.


---

# 163. EHF-HC-RAW-09A — Johnson \(A_1\) Selection Audit

## 163.1 Question

RAW-08B established two facts that appeared to be in tension.

First, an anchor chart identifies the intrinsic even-sector space with a Johnson vertex set.

Second, the intrinsic nearest sector shell

\[
\delta=1
\]

unfolds in any fixed anchor chart as

\[
\boxed{
A_1\cup A_{m-1}.
}
\]

Therefore plain Johnson single-swap adjacency

\[
A_1
\]

is not, by itself, the full anchor-free nearest-sector relation.

RAW-09A asks:

> Is there an independently motivated structure that separates \(A_1\) from \(A_{m-1}\) without simply hard-coding “choose \(r=1\)”?

The answer is:

\[
\boxed{\textbf{yes, once the cross-layer growth structure is included}.}
\]

---

# 164. No-go result for an isolated even layer

Consider two intrinsic bipartition sectors

\[
P,Q\in\mathcal B_m
\]

with intrinsic distance

\[
\delta(P,Q)=1.
\]

Choose representatives

\[
P=\{A,A^c\},
\]

and

\[
Q=\{B,B^c\}
\]

such that

\[
B=(A\setminus\{u\})\cup\{v\},
\]

with

\[
u\in A,
\qquad
v\in A^c.
\]

The two labels

\[
u,v
\]

are precisely the exchanged labels.

Now choose an anchor \(a\).

### Anchor not exchanged

If

\[
a\notin\{u,v\},
\]

then the anchor lies either in

\[
A\cap B
\]

or in

\[
A^c\cap B^c.
\]

The anchor-containing blocks differ by one label, so:

\[
\boxed{
d_J^{(a)}(P,Q)=1.
}
\]

There are:

\[
\boxed{2m-2}
\]

such anchors.

### Anchor is exchanged

If

\[
a=u
\]

or

\[
a=v,
\]

the anchor-containing representative of one sector is compared with the complementary representative of the other.

The Johnson chart therefore gives:

\[
\boxed{
d_J^{(a)}(P,Q)=m-1.
}
\]

There are exactly:

\[
\boxed{2}
\]

such anchors.

Hence an intrinsic \(\delta=1\) pair has the all-anchor histogram:

\[
\boxed{
\{1:2m-2,\quad m-1:2\}.
}
\]

Therefore:

\[
\boxed{
A_1\text{ alone is not invariant under change of anchor}.
}
\]

The anchor-free relation is:

\[
\boxed{
A_1\cup A_{m-1}.
}
\]

This proves that an isolated even Hamilton-cycle layer cannot intrinsically select \(A_1\) without extra structure.

---

# 165. General anchor-folding law

More generally, let:

\[
\delta(P,Q)=s,
\qquad
1\le s<\frac m2.
\]

Choose representatives with:

\[
|A\setminus B|=|B\setminus A|=s.
\]

Then:

\[
|A\cap B|=m-s,
\]

and likewise:

\[
|A^c\cap B^c|=m-s.
\]

An anchor in one of these two common parts gives chart distance:

\[
s.
\]

There are:

\[
2(m-s)
\]

such anchors.

An anchor in the symmetric difference gives chart distance:

\[
m-s.
\]

There are:

\[
2s
\]

such anchors.

Thus:

\[
\boxed{
d_J^{(a)}(P,Q)
=
\begin{cases}
s,&2(m-s)\text{ anchors},\\
m-s,&2s\text{ anchors}.
\end{cases}
}
\]

At the midpoint

\[
m=2s,
\]

the two values coincide.

This is the exact all-anchor form of the Johnson-shell folding discovered in RAW-08B.

---

# 166. Growth supplies a distinguished anchor

Now consider one-site completion:

\[
HC_{2m-1}
\longrightarrow
HC_{2m}.
\]

Let:

\[
x=2m-1
\]

be the newly inserted label.

The deletion map

\[
\pi_x:HC_{2m}\to HC_{2m-1}
\]

removes \(x\).

Unlike an arbitrary anchor chosen merely to coordinatize one isolated layer, \(x\) is distinguished by the cross-layer structure itself:

\[
\boxed{
x=\text{the unique label removed by the declared deletion map}.
}
\]

Therefore the chart

\[
\chi_x
\]

is canonical **relative to the growth morphism**.

This does not restore full within-layer \(S_{2m}\) symmetry while holding the growth history fixed.

Rather, the natural symmetry is the covariance of the complete object:

\[
(HC_{2m-1},HC_{2m},\pi_x,x).
\]

Relabelling the full graded object relabels the distinguished new site as well.

---

# 167. Target LR2 has an exact horizontal/vertical split

Take a target raw LR2 edge:

\[
C\sim_{LR2}D
\]

in \(HC_{2m}\).

LR2 swaps the labels occupying two adjacent cyclic positions.

There are exactly two cases.

## Horizontal case: the new site is not swapped

If:

\[
x\notin\text{the reversed 2-block},
\]

then deleting \(x\) leaves an LR2 edge between distinct parents:

\[
\boxed{
\pi_x(C)\sim_{LR2}\pi_x(D).
}
\]

This is a faithful/horizontal lift of parent comparability.

Because the anchor \(x\) lies outside the exchanged two-label block, RAW-08B's support-to-chart rule gives:

\[
\boxed{
d_J^{(x)}(\Pi(C),\Pi(D))=1.
}
\]

## Vertical case: the new site is swapped

If:

\[
x\in\text{the reversed 2-block},
\]

then LR2 only moves the insertion position of the new site.

Deleting \(x\) gives the same parent:

\[
\boxed{
\pi_x(C)=\pi_x(D).
}
\]

This is vertical motion inside one growth fibre.

Because the anchor lies inside the exchanged block, the Johnson chart gives:

\[
\boxed{
d_J^{(x)}(\Pi(C),\Pi(D))=m-1.
}
\]

Therefore:

\[
\boxed{
\pi_x(C)\ne\pi_x(D)
\iff
d_J^{(x)}(\Pi(C),\Pi(D))=1,
}
\]

and:

\[
\boxed{
\pi_x(C)=\pi_x(D)
\iff
d_J^{(x)}(\Pi(C),\Pi(D))=m-1.
}
\]

This is the central RAW-09A selection theorem.

---

# 168. Johnson \(A_1\) is the growth-horizontal LR2 quotient

The theorem gives an exact interpretation:

\[
\boxed{
A_1
=
\text{sector image of horizontal/faithful target LR2 edges}.
}
\]

Its complementary chart shell is:

\[
\boxed{
A_{m-1}
=
\text{sector image of vertical insertion-slot LR2 edges}.
}
\]

Thus the two pieces of the intrinsic nearest sector shell have different cross-layer meanings.

Without growth:

\[
A_1\cup A_{m-1}
\]

is one intrinsic shell.

With growth:

\[
\boxed{
A_1=\text{horizontal transport},
}
\]

\[
\boxed{
A_{m-1}=\text{vertical fibre motion}.
}
\]

This is an independently motivated separator.

---

# 169. Exact global counts

The number of target \(LR2\) edges in \(HC_{2m}\) is:

\[
\boxed{
|E_{LR2}^{(2m)}|
=
\frac{(2m)!}{4}.
}
\]

RAW-07 gave the vertical count:

\[
\boxed{
E_{\rm vert}
=
\frac{(2m-1)!}{2}.
}
\]

Hence the faithful/horizontal count is:

\[
E_{\rm horiz}
=
\frac{(2m)!}{4}
-
\frac{(2m-1)!}{2},
\]

so:

\[
\boxed{
E_{\rm horiz}
=
\frac{(m-1)(2m-1)!}{2}.
}
\]

Therefore:

\[
\boxed{
E_{\rm horiz}:E_{\rm vert}
=
(m-1):1.
}
\]

This exactly matches the Johnson shell-volume ratio.

---

# 170. Sector-count derivation of the same split

The number of even sectors is:

\[
B_m=\binom{2m-1}{m-1}.
\]

For the new-site anchor chart:

\[
\deg(A_1)=m(m-1),
\]

while:

\[
\deg(A_{m-1})=m.
\]

RAW-08B gave the common sector-pair edge weight:

\[
w_1=w_{m-1}
=
((m-1)!)^2.
\]

Thus the total number of raw LR2 edges mapping to \(A_1\) is:

\[
\frac{B_m}{2}
m(m-1)
((m-1)!)^2.
\]

This simplifies to:

\[
\boxed{
\frac{(m-1)(2m-1)!}{2}
=
E_{\rm horiz}.
}
\]

Similarly:

\[
\frac{B_m}{2}
m
((m-1)!)^2
=
\boxed{
\frac{(2m-1)!}{2}
=
E_{\rm vert}.
}
\]

So the Johnson shell split and the growth horizontal/vertical split agree exactly at the global counting level.

---

# 171. Exhaustive certification at \(n=6\)

For:

\[
5\to6,
\qquad
m=3,
\]

the target has:

\[
180
\]

LR2 edges.

Deletion relative to the new label gives:

\[
120
\]

horizontal edges and:

\[
60
\]

vertical edges.

Using the new-site anchor:

\[
\boxed{
120/120\text{ horizontal edges lie in }A_1,
}
\]

and:

\[
\boxed{
60/60\text{ vertical edges lie in }A_2=A_{m-1}.
}
\]

There were:

\[
0
\]

classification mismatches.

Using an unrelated old anchor instead gives a mixture:

- horizontal edges occur in both \(A_1\) and \(A_2\);
- vertical edges occur in both \(A_1\) and \(A_2\).

So the exact separation is genuinely tied to the growth anchor.

---

# 172. Exhaustive certification at \(n=8\)

For:

\[
7\to8,
\qquad
m=4,
\]

the target has:

\[
10080
\]

LR2 edges.

The growth split is:

\[
7560
\]

horizontal and:

\[
2520
\]

vertical.

With the new-site anchor:

\[
\boxed{
7560/7560\text{ horizontal edges lie in }A_1,
}
\]

\[
\boxed{
2520/2520\text{ vertical edges lie in }A_3=A_{m-1}.
}
\]

Again:

\[
0
\]

mismatches.

With an unrelated old anchor, both horizontal and vertical classes are split across \(A_1\) and \(A_3\).

This rules out the possibility that the result is merely a generic feature of any anchor.

---

# 173. Status of the Johnson \(A_1\) bridge

RAW-08B concluded:

\[
A_1
\]

was not intrinsically selected by the isolated even-layer quotient.

RAW-09A refines that conclusion.

## Isolated-layer status

\[
\boxed{
A_1\text{ is not intrinsic}.
}
\]

The anchor-free nearest sector shell is:

\[
A_1\cup A_{m-1}.
\]

## Graded/growth status

Once the layer is regarded as the result of:

\[
HC_{2m-1}\to HC_{2m}
\]

with distinguished new label and deletion map,

\[
\boxed{
A_1\text{ is canonically selected as the horizontal LR2 sector relation}.
}
\]

Thus ordinary Johnson single-swap adjacency is not a primitive raw-HC quotient.

It is a **growth-relative effective transport relation**.

This is a substantially stronger and more disciplined bridge.

---

# 174. Connection back to LR3

The current foundational same-layer selector remains LR3, not LR2.

RAW-07 showed:

\[
\boxed{
LR3^{(N)}
\to
LR3^{(N-1)}
\cup
LR2^{(N-1)}
}
\]

under deletion.

Thus LR2 is not an unrelated extra rule inserted solely to manufacture Johnson transport.

It already appears as the exact lower-support channel exposed by LR3 growth.

RAW-09A then shows that, on an even layer equipped with its incoming growth map, the horizontal part of this lower-support LR2 geometry gives:

\[
\boxed{
A_1.
}
\]

A plausible structural chain is therefore:

\[
\boxed{
LR3
\overset{\text{growth/deletion}}{\longrightarrow}
LR2\text{ lower channel}
\overset{\text{horizontal sector quotient}}{\longrightarrow}
A_1.
}
\]

This is not yet a dynamical derivation of every historical Johnson transport assumption, but it removes the previous need to hard-code the single-swap shell arbitrarily.

---

# 175. Symmetry status

It is important not to overstate the result.

The selected \(A_1\) relation is not invariant under the full \(S_{2m}\) action if the distinguished growth label \(x\) is held fixed as external metadata.

The relevant object is the graded tuple:

\[
\boxed{
(HC_{2m-1},HC_{2m},\pi_x,x).
}
\]

Its natural symmetry consists of relabellings that act covariantly on all of:

- parent states;
- child states;
- the deletion map;
- the distinguished newest label.

Thus:

\[
\boxed{
A_1\text{ is growth-covariant, not isolated-layer invariant}.
}
\]

This distinction should remain explicit in all later EHF writing.

---

# 176. RAW-09A verdict

The audit asked whether \(A_1\) could be selected naturally without simply saying “take Johnson distance one.”

The answer is:

\[
\boxed{\textbf{yes, but only after adding the already-motivated growth structure}.}
\]

The logic is:

\[
\text{intrinsic }\delta=1
\longleftrightarrow
A_1\cup A_{m-1},
\]

then growth distinguishes:

\[
\boxed{
A_1=\text{horizontal parent-changing branch},
}
\]

\[
\boxed{
A_{m-1}=\text{vertical same-parent branch}.
}
\]

So the historical Johnson walk has a much more credible structural origin than it appeared to have after RAW-08B alone.

---

# 177. Certification ledger

## Exact/proved

1. An intrinsic \(\delta=1\) pair appears as \(A_1\) from \(2m-2\) anchors and \(A_{m-1}\) from 2 anchors.
2. Therefore \(A_1\) alone is not intrinsic to an isolated even layer.
3. The newest growth label defines a canonical anchor relative to the deletion map.
4. For target LR2:
   \[
   \pi_x(C)\ne\pi_x(D)
   \iff
   r_x=1.
   \]
5. For target LR2:
   \[
   \pi_x(C)=\pi_x(D)
   \iff
   r_x=m-1.
   \]
6. Horizontal/vertical global counts are:
   \[
   \frac{(m-1)(2m-1)!}{2},
   \qquad
   \frac{(2m-1)!}{2}.
   \]
7. Their ratio is:
   \[
   m-1:1.
   \]
8. Johnson shell edge-volume formulas give exactly the same split.

## Computationally certified

Complete target LR2 graphs at:

\[
n=6,\qquad n=8.
\]

New-site anchor classification mismatches:

\[
\boxed{0}.
\]

Old-anchor control:

\[
\boxed{\text{mixed horizontal/vertical shell assignment}}.
\]

All:

\[
\boxed{50/50}
\]

strict checks passed.

---

# 178. Updated Johnson status statement

The strongest safe statement is now:

> **The intrinsic even-sector space is the unordered equal-bipartition space. An anchor chart identifies it with a Johnson vertex set. The intrinsic nearest sector shell folds to \(A_1\cup A_{m-1}\). When the even layer is equipped with its incoming one-site growth map, the distinguished newest site selects a canonical growth chart in which \(A_1\) is exactly the horizontal/parent-changing LR2 sector relation and \(A_{m-1}\) is exactly vertical insertion-slot motion.**

This is the current clean bridge.

---

# 179. Immediate next questions

RAW-09A leaves two particularly useful next targets.

### EHF-HC-RAW-09B — Intrinsic Equipartition Quotient Spectrum

Now study the genuinely anchor-free sector operator and determine how the \(r\leftrightarrow m-r\) folding acts spectrally.

### EHF-HC-RAW-10A — Johnson Transport Recovery Audit

Take the growth-selected \(A_1\) graph and rederive the historical exact Johnson drift/diffusion formulas from this new dependency chain, checking precisely which observables require an anchor/new-site chart and which descend invariantly.

Given the rebuild goal, RAW-10A is the most direct way to reconnect the old Johnson transport mathematics without importing any of its assumptions silently.


---

# 180. EHF-HC-RAW-10A — Johnson Transport Recovery Audit

## 180.1 Purpose

RAW-09A supplied the missing bridge:

\[
HC_{2k-1}\to HC_{2k}
\]

with newest-site deletion structure selects the horizontal part of target \(LR2\), and its sector image is exactly Johnson \(A_1\).

RAW-10A therefore asks whether the historical exact Johnson transport core can be reconstructed from the rebuilt dependency chain without silently reinstating old assumptions.

Historical transport ingredients to recover:

\[
\Omega_k=\binom{[2k-1]}{k},
\]

single-swap adjacency,

\[
h(S)=\sum_{i\in S}i,
\qquad
q(S)=\sum_{i\in S}i^2,
\]

exact drift,

\[
A(h),
\]

state diffusion,

\[
B(S),
\]

shell-conditioned diffusion,

generating-function counts,

and reflection symmetry.

The answer is:

\[
\boxed{\text{the exact transport mathematics is recovered, with two dependency clarifications}.}
\]

Those clarifications are:

1. \(A_1\) is growth-relative rather than intrinsic to an isolated even layer;
2. \(h\) and \(q\) require an ordered growth-history chart.

---

# 181. Recovered state space

Let the target layer be

\[
HC_{2k}.
\]

Its incoming growth map comes from

\[
HC_{2k-1}.
\]

Let \(x\) be the newest label.

RAW-09A showed that the anchor chart defined by \(x\), followed by complementing the \((k-1)\)-subset coordinate, gives a \(k\)-subset of the \(2k-1\) parent labels.

Thus:

\[
\boxed{
\Omega_k
=
\binom{[2k-1]}{k}
}
\]

is recovered as a growth chart on the intrinsic even-sector space.

The state count is:

\[
\boxed{
|\Omega_k|
=
\binom{2k-1}{k}.
}
\]

This is exact.

---

# 182. Recovered adjacency

RAW-09A established:

\[
\boxed{
A_1
=
\text{sector image of horizontal target }LR2.
}
\]

Hence two chart states satisfy:

\[
S\sim T
\iff
|S\cap T|=k-1.
\]

Each state has:

\[
k
\]

choices of removed element and:

\[
k-1
\]

choices of inserted element.

Therefore:

\[
\boxed{
d_k=k(k-1).
}
\]

So the historical Johnson graph \(J(2k-1,k)\) is recovered.

Its status is now precise:

\[
\boxed{
\text{derived growth-relative comparison graph},
}
\]

not primitive raw HC adjacency.

---

# 183. Transport weighting is an additional convention

The graph alone does not define a stochastic process.

The historical transport core chooses:

> from each state, select uniformly among its \(k(k-1)\) Johnson neighbours.

This is a natural neutrality convention because the Johnson graph is regular and all microscopic single-swap neighbours are symmetry-equivalent.

But it is still a declared transport rule.

Therefore:

\[
\boxed{
\text{uniform }A_1\text{ walk}
}
\]

should be classified as:

\[
\boxed{
\text{chosen neutral transport convention on a derived graph}.
}
\]

It is not forced by the existence of \(A_1\).

---

# 184. Birth-rank coordinate requirement

The Johnson graph only needs a finite set of \(2k-1\) labels.

The shell observable:

\[
h(S)=\sum_{i\in S}i
\]

requires more.

It assigns numerical coordinates:

\[
1,2,\ldots,2k-1
\]

to the parent labels.

The rebuilt interpretation is:

\[
\boxed{
i=\text{birth rank in the cumulative growth history}.
}
\]

Thus \(h\) is not invariant under an arbitrary relabelling of an isolated layer.

It is an exact observable in a **growth-history chart**.

Likewise:

\[
q(S)=\sum_{i\in S}i^2
\]

is a growth-history moment observable.

This is not a defect.

It separates:

\[
\text{intrinsic sector geometry}
\]

from:

\[
\text{history-dependent coarse observables}.
\]

---

# 185. Exact shell centre and variance

For:

\[
S\in\Omega_k
\]

uniform over all \(k\)-subsets of \([2k-1]\),

\[
\boxed{
\mathbb E[h]=k^2.
}
\]

The variance is:

\[
\boxed{
\operatorname{Var}(h)
=
\frac{k^2(k-1)}{6}.
}
\]

RAW-10A re-certified both identities exactly for:

\[
k=2,\ldots,7.
\]

The shell range is:

\[
h_{\min}
=
1+\cdots+k
=
\frac{k(k+1)}2,
\]

\[
h_{\max}
=
k+(k+1)+\cdots+(2k-1)
=
\frac{k(3k-1)}2.
\]

Their midpoint is:

\[
\boxed{
h_* = k^2.
}
\]

---

# 186. Exact microscopic drift derivation

Let:

\[
S'=(S\setminus\{a\})\cup\{b\},
\]

with:

\[
a\in S,
\qquad
b\notin S.
\]

Then:

\[
\Delta h=b-a.
\]

Define:

\[
T_1=\sum_{i=1}^{2k-1}i=k(2k-1).
\]

Since the step is uniform over all:

\[
k(k-1)
\]

ordered remove/insert pairs,

\[
\mathbb E[a\mid S]
=
\frac{h}{k},
\]

and:

\[
\mathbb E[b\mid S]
=
\frac{T_1-h}{k-1}.
\]

Therefore:

\[
A(S)
=
\frac{T_1-h}{k-1}
-
\frac hk.
\]

Simplifying:

\[
\boxed{
A(S)
=
\frac{2k-1}{k(k-1)}
(k^2-h(S)).
}
\]

Thus the state drift depends on the state only through \(h\).

Consequently:

\[
\boxed{
A(h)
=
\frac{2k-1}{k(k-1)}
(k^2-h).
}
\]

This is an exact theorem, not a shell-average approximation.

---

# 187. Meaning of the exact drift closure

The result:

\[
A(S)=A(h(S))
\]

is stronger than saying only that shell-averaged drift is simple.

Every two microstates having the same \(h\) have exactly the same first increment moment.

Thus:

\[
\boxed{
h\text{ is an exact first-moment sufficient statistic for one-step drift}.
}
\]

The restoring centre is:

\[
h_*=k^2.
\]

Hence:

\[
h<k^2
\Longrightarrow
A(h)>0,
\]

\[
h>k^2
\Longrightarrow
A(h)<0.
\]

This is exact combinatorial restoring drift.

No physical force interpretation is implied.

---

# 188. Exact state-level diffusion

Define:

\[
T_2
=
\sum_{i=1}^{2k-1}i^2
=
\frac{(2k-1)(2k)(4k-1)}6.
\]

Also define:

\[
q(S)=\sum_{i\in S}i^2.
\]

For a uniform Johnson step:

\[
(\Delta h)^2
=
(b-a)^2.
\]

Summing over all ordered remove/insert pairs gives:

\[
\sum_{a\in S}
\sum_{b\notin S}
(b-a)^2
\]

\[
=
k(T_2-q)
+
(k-1)q
-
2h(T_1-h).
\]

Therefore:

\[
\boxed{
B(S)
=
\mathbb E[(\Delta h)^2\mid S]
=
\frac{
kT_2-q(S)-2T_1h(S)+2h(S)^2
}{
k(k-1)
}.
}
\]

This exactly reproduces the historical state-diffusion formula.

RAW-10A verified it on every state for:

\[
k=2,\ldots,7.
\]

---

# 189. Why \(q\) is genuinely required

Unlike drift, the second increment moment does not close on \(h\) alone.

At:

\[
k=3,
\]

for example, distinct subsets can have the same \(h\) and different \(q\).

Therefore they have different:

\[
B(S).
\]

So:

\[
\boxed{
h\text{ is sufficient for drift but not for state diffusion}.
}
\]

The first exact correction is:

\[
\boxed{q}.
\]

This confirms rather than weakens the historical low-moment interpretation.

---

# 190. Exact shell diffusion

Average over all microstates in a fixed shell:

\[
h(S)=h.
\]

Then:

\[
\boxed{
B(h)
=
\frac{
kT_2
-
\mathbb E[q\mid h]
-
2T_1h
+
2h^2
}{
k(k-1)
}.
}
\]

Thus shell diffusion is exact once:

\[
\mathbb E[q\mid h]
\]

is known.

This is a genuine conditional-moment coarse-graining.

---

# 191. Important correction: the shell partition is not strongly lumpable

Define the complete one-step shell histogram of a microstate:

\[
\Gamma_S(h')
=
\#\{S'\sim S:h(S')=h'\}.
\]

Strong lumpability with respect to \(h\) would require:

\[
\Gamma_S
=
\Gamma_T
\]

whenever:

\[
h(S)=h(T).
\]

RAW-10A tested this exhaustively.

Result:

\[
\boxed{
k=2:\text{ strongly lumpable},
}
\]

but:

\[
\boxed{
k\ge3:\text{ not strongly lumpable}
}
\]

through every audited case \(k=3,\ldots,7\).

Non-lumpable shell counts were:

\[
k=3:\ 3,
\]

\[
k=4:\ 9,
\]

\[
k=5:\ 17,
\]

\[
k=6:\ 27,
\]

\[
k=7:\ 39.
\]

Therefore the scalar process \(h_t\) obtained by merely observing an arbitrary microscopic Johnson walk is not, in general, an autonomous Markov chain.

This is an important precision correction.

---

# 192. Status of the averaged shell kernel

One can nevertheless define exactly:

\[
K(h,h')
=
\frac{
\#\{(S,S'):
h(S)=h,\ S\sim S',\ h(S')=h'\}
}{
N_h\,k(k-1)
}.
\]

This is the transition kernel obtained by averaging uniformly over the microstates in shell \(h\).

RAW-10A checked exact row normalization and detailed balance.

Because the microscopic Johnson graph is undirected:

\[
\boxed{
N_hK(h,h')
=
N_{h'}K(h',h).
}
\]

Thus the averaged shell kernel is exact and reversible.

But its correct status is:

\[
\boxed{
\text{exact conditional coarse kernel},
}
\]

not:

\[
\boxed{
\text{strongly lumped projection of every microscopic trajectory}.
}
\]

This distinction should be retained in future documents.

---

# 193. Exact subset generating function

Define:

\[
\boxed{
G_k(x,y)
=
\prod_{j=1}^{2k-1}(1+yx^j).
}
\]

Selecting the term:

\[
yx^j
\]

means including label \(j\).

Therefore:

\[
\boxed{
N_h
=
[x^hy^k]G_k(x,y).
}
\]

RAW-10A independently reconstructed the coefficients and checked them against direct subset enumeration for:

\[
k=2,\ldots,7.
\]

Every shell count matched exactly.

---

# 194. Label-refined generating function

For fixed label \(j\), define:

\[
F_{k,j}(x,y)
=
\prod_{\substack{r=1\\r\ne j}}^{2k-1}
(1+yx^r).
\]

Then the number of shell-\(h\) states containing \(j\) is:

\[
\boxed{
N_{h,j}
=
[x^{h-j}y^{k-1}]
F_{k,j}(x,y).
}
\]

RAW-10A checked the complete label-refined arrays against direct enumeration through:

\[
k=7.
\]

All coefficients matched.

---

# 195. Exact shell moment identities

The label-refined counts satisfy:

\[
\boxed{
\sum_jN_{h,j}=kN_h,
}
\]

because every shell state contains \(k\) labels.

Likewise:

\[
\boxed{
\sum_j jN_{h,j}=hN_h,
}
\]

and:

\[
\boxed{
\sum_j j^2N_{h,j}
=
N_h\mathbb E[q\mid h].
}
\]

All three identities were certified exactly through:

\[
k=7.
\]

Thus the historical hierarchy survives:

\[
\text{generating function}
\to
\text{shell counts}
\to
\text{label-refined counts}
\to
\text{conditional moments}
\to
\text{drift/diffusion}.
\]

---

# 196. Exact reflection symmetry

The birth-rank label set has the involution:

\[
j\mapsto 2k-j.
\]

For a \(k\)-subset:

\[
S\mapsto
\{2k-j:j\in S\}.
\]

Its shell height transforms as:

\[
h
\mapsto
2k^2-h.
\]

Therefore:

\[
\boxed{
N_{h,j}
=
N_{2k^2-h,\,2k-j}.
}
\]

RAW-10A verified the full refined reflection arrays through:

\[
k=7.
\]

This is an exact symmetry of the growth-history label chart.

It is not an anchor-free invariant of unlabeled HC states.

---

# 197. Dependency audit

The rebuilt transport chain is now:

### Intrinsic / raw-derived

\[
HC_{2k}
\to
\text{intrinsic equal bipartitions}.
\]

### Growth-derived

\[
\text{incoming growth map}
\to
\text{newest-site anchor}
\to
\Omega_k
\to
A_1.
\]

### History-chart derived

\[
\text{birth ranks}
\to
h,q.
\]

### Chosen transport convention

\[
\text{uniform neighbour selection on }A_1.
\]

### Exact consequences

\[
A(h),
\]

\[
B(S),
\]

\[
B(h),
\]

generating-function shell counts,

reflection laws,

and the reversible averaged shell kernel.

### Effective interpretation

continuum/Fokker--Planck language.

This dependency structure is now explicit.

---

# 198. Comparison with the historical exact Johnson transport core

The historical core's exact formulas are mathematically recovered.

However, its older emergence sentence:

\[
\text{Hamilton-cycle local admissibility}
\to
\text{parity-sector reduction}
\to
\text{subset encoding}
\to
\text{Johnson geometry}
\]

was too compressed.

The rebuilt chain is more precise:

\[
\boxed{
HC_{2k}
\to
\text{intrinsic bipartitions}
\to
\text{incoming growth chart}
\to
LR2_{\rm horizontal}
\to
A_1
\to
\text{uniform Johnson walk}.
}
\]

And the shell observables require:

\[
\boxed{
\text{cumulative birth-order chart}.
}
\]

Thus the old transport formulas survive, while their upstream dependencies have been corrected.

---

# 199. Exact versus chosen versus effective

## Exact structural results

- intrinsic even sectors;
- growth-selected Johnson vertex chart;
- growth-selected horizontal \(A_1\);
- Johnson degree;
- exact drift;
- exact state diffusion;
- exact conditional shell diffusion;
- exact generating functions;
- exact reflection;
- exact averaged shell detailed balance.

## Chosen

- equal probability for all \(A_1\) neighbours;
- use of birth-rank coordinates as the shell chart.

## Not strongly exact as an autonomous projection

- \(h_t\) alone is not generally a Markov process under arbitrary microscopic initial distributions.

## Effective

- Fokker--Planck/continuum interpretation;
- any physical meaning assigned to \(h,q\), drift, or diffusion.

---

# 200. Computational certification

Complete subset-state enumeration was performed for:

\[
k=2,3,4,5,6,7.
\]

Largest audited Johnson graph:

\[
J(13,7)
\]

with:

\[
1716
\]

states and degree:

\[
42.
\]

Every state was checked for:

- exact drift;
- exact diffusion.

Every shell was checked for:

- exact shell drift;
- exact conditional shell diffusion;
- microscopic transition-profile multiplicity;
- strong lumpability.

Complete generating-function and label-refined coefficients were checked against enumeration.

Final audit:

\[
\boxed{
319/319
}
\]

strict checks passed.

---

# 201. RAW-10A verdict

The Johnson transport core survives the raw rebuild.

The correct statement is now:

> **The historical exact Johnson drift/diffusion theory is a valid exact transport theory on a growth-derived \(A_1\) sector graph. Its shell variables \(h\) and \(q\) are exact growth-history chart observables. The microscopic drift closes exactly on \(h\), diffusion closes on \((h,q)\), and shell-conditioned transport is exact under conditional averaging. The \(h\)-partition itself is not strongly lumpable for \(k\ge3\), so the averaged shell kernel should not be described as an autonomous projection of every microscopic trajectory.**

This is stronger mathematically because the dependency chain is now explicit and the coarse-graining claim is properly bounded.

---

# 202. Immediate next questions

RAW-10A leaves three useful directions.

### EHF-HC-RAW-10B — Birth-Rank Gauge / Observable Robustness Audit

Ask how much of the exact transport survives if the growth-history ordering is changed or forgotten.

Questions:

1. Which properties of \(h\) are invariant under monotone/reversal changes of birth rank?
2. Is there an anchor-free or history-coarser observable with comparable exact drift closure?
3. How special is the linear birth-rank coordinate?

### EHF-HC-RAW-10C — Shell Non-Lumpability Structure

Classify the microscopic transition signatures inside equal-\(h\) shells and determine the minimum additional moment set required for exact Markov lumpability or finite closure.

### EHF-HC-RAW-11 — Reconnect to Growth Transport

Derive how the \(A_1\) Johnson walk itself transforms under the next growth step and connect it back to the support-filtration operators.

The most foundational next step is **RAW-10B**, because the only major coordinate assumption remaining in the even transport core is now the birth-rank shell observable.


---

# 203. EHF-HC-RAW-10B — Birth-Rank Gauge / Observable Robustness Audit

## 203.1 Purpose

RAW-10A recovered the exact historical Johnson transport theory but isolated one remaining coordinate assumption:

\[
h(S)=\sum_{i\in S}i
\]

uses the ordered labels

\[
1,2,\ldots,2k-1.
\]

Those numbers were reinterpreted as cumulative birth ranks from the growth history.

RAW-10B asks:

> **How much of the exact transport mathematics genuinely depends on the linear birth-rank coordinate?**

The answer is surprisingly strong:

\[
\boxed{
\text{the exact restoring drift is universal for every additive label-weight observable}.
}
\]

Thus linear birth rank is not selected by drift closure itself.

---

# 204. General additive observable

Let:

\[
N=2k-1.
\]

Assign an arbitrary fixed real weight:

\[
w_i
\]

to each of the \(N\) Johnson labels.

Define:

\[
\boxed{
F_w(S)=\sum_{i\in S}w_i.
}
\]

Also define:

\[
\boxed{
G_w(S)=\sum_{i\in S}w_i^2,
}
\]

and the global weight moments:

\[
W_1=\sum_{i=1}^{N}w_i,
\]

\[
W_2=\sum_{i=1}^{N}w_i^2.
\]

No ordering or monotonicity of the weights is assumed.

The historical birth-rank observable is the special case:

\[
w_i=i.
\]

---

# 205. Universal additive drift theorem

A uniform Johnson \(A_1\) step removes:

\[
a\in S
\]

and inserts:

\[
b\notin S.
\]

The additive increment is:

\[
\Delta F=w_b-w_a.
\]

Conditioned on the microstate:

\[
\mathbb E[w_a\mid S]
=
\frac{F_w(S)}{k},
\]

while:

\[
\mathbb E[w_b\mid S]
=
\frac{W_1-F_w(S)}{k-1}.
\]

Therefore:

\[
\mathbb E[\Delta F\mid S]
=
\frac{W_1-F}{k-1}
-
\frac{F}{k}.
\]

Hence:

\[
\boxed{
\mathbb E[\Delta F\mid S]
=
\frac{
kW_1-(2k-1)F_w(S)
}{
k(k-1)
}.
}
\]

Let:

\[
\bar w=\frac{W_1}{2k-1}.
\]

Then:

\[
\boxed{
\mathbb E[\Delta F\mid S]
=
-\lambda_k
\left(
F_w(S)-k\bar w
\right),
}
\]

with:

\[
\boxed{
\lambda_k
=
\frac{2k-1}{k(k-1)}.
}
\]

This restoring coefficient is **independent of the weight system**.

---

# 206. Consequence: the old drift slope is Johnson structure, not birth-rank structure

For linear birth rank:

\[
w_i=i,
\]

we have:

\[
\bar w=k,
\]

and therefore:

\[
k\bar w=k^2.
\]

The historical formula:

\[
A(h)
=
\frac{2k-1}{k(k-1)}
(k^2-h)
\]

is exactly the universal additive law specialized to linear weights.

Therefore:

\[
\boxed{
\text{the restoring coefficient }
\frac{2k-1}{k(k-1)}
\text{ comes from Johnson }A_1\text{ transport itself}.
}
\]

It does **not** provide evidence that the numerical birth-rank coordinate \(w_i=i\) is uniquely preferred.

This is an important interpretive correction.

---

# 207. Universal first eigenspace

Define the centered observable:

\[
\widetilde F_w
=
F_w-k\bar w.
\]

Let \(P\) be the transition operator of the uniform Johnson walk.

The drift theorem gives:

\[
P\widetilde F_w-\widetilde F_w
=
-\lambda_k\widetilde F_w.
\]

Hence:

\[
\boxed{
P\widetilde F_w
=
\rho_k\widetilde F_w,
}
\]

where:

\[
\boxed{
\rho_k
=
1-\lambda_k
=
1-
\frac{2k-1}{k(k-1)}.
}
\]

Thus every centered additive observable is an exact transition eigenfunction with the same eigenvalue.

Weights differing by an additive constant define the same centered observable.

The space of centered weight vectors has dimension:

\[
\boxed{
(2k-1)-1=2k-2.
}
\]

The map from centered weights to centered additive subset observables is injective.

Therefore the Johnson walk carries an exact:

\[
\boxed{
2k-2
}
\]

dimensional additive eigenfunction space with common eigenvalue \(\rho_k\).

This is the representation-theoretic reason that the restoring drift is so robust.

---

# 208. Exact correlation consequence

Because:

\[
P\widetilde F=\rho_k\widetilde F,
\]

iteration gives:

\[
\boxed{
\mathbb E[\widetilde F_t\mid S_0]
=
\rho_k^t\widetilde F(S_0).
}
\]

Under the uniform stationary distribution:

\[
\boxed{
\operatorname{Cov}(F_t,F_0)
=
\rho_k^t
\operatorname{Var}(F).
}
\]

So the one-mode relaxation factor is universal across every additive weight observable.

Only its scale and shell geometry depend on the chosen weights.

---

# 209. Universal stationary mean and variance

For a uniformly chosen \(k\)-subset of \(N=2k-1\) labels:

\[
\boxed{
\mathbb E[F_w]
=
k\bar w.
}
\]

Let the population variance of the label weights be:

\[
\sigma_w^2
=
\frac1N
\sum_i
(w_i-\bar w)^2.
\]

The finite-population variance formula gives:

\[
\operatorname{Var}(F_w)
=
\frac{
k(N-k)
}{
N-1
}
\sigma_w^2.
\]

Since:

\[
N-k=k-1
\]

and:

\[
N-1=2(k-1),
\]

this reduces to:

\[
\boxed{
\operatorname{Var}(F_w)
=
\frac{k}{2}\sigma_w^2.
}
\]

For:

\[
w_i=i,
\]

the population variance is:

\[
\frac{k(k-1)}{3},
\]

giving:

\[
\boxed{
\operatorname{Var}(h)
=
\frac{k^2(k-1)}6.
}
\]

So the old width law is not universal.

It combines:

1. the universal subset-sampling factor \(k/2\);
2. the specific population variance of the linear birth-rank weights.

---

# 210. Scaling consequence

Suppose a family of weight systems has population standard deviation:

\[
\sigma_w(k).
\]

Then:

\[
\boxed{
\sigma_F(k)
=
\sqrt{\frac{k}{2}}\,
\sigma_w(k).
}
\]

Thus the shell width scaling depends directly on the scale assigned to label history.

For linear birth rank:

\[
\sigma_w\asymp k,
\]

hence:

\[
\sigma_h\asymp k^{3/2}.
\]

For quadratic weights:

\[
w_i=i^2,
\]

one instead obtains:

\[
\sigma_w\asymp k^2,
\]

and therefore:

\[
\sigma_F\asymp k^{5/2}.
\]

So the historical \(k^{3/2}\) width is a property of the **linear birth-rank metric**, not Johnson transport alone.

---

# 211. Universal state diffusion theorem

The additive increment is:

\[
\Delta F=w_b-w_a.
\]

Hence:

\[
(\Delta F)^2
=
w_b^2+w_a^2-2w_aw_b.
\]

Summing uniformly over all remove/insert pairs gives:

\[
\boxed{
B_w(S)
=
\mathbb E[(\Delta F)^2\mid S]
=
\frac{
kW_2
-
G_w(S)
-
2W_1F_w(S)
+
2F_w(S)^2
}{
k(k-1)
}.
}
\]

Thus the historical \(h,q\) formula is also universal.

The exact two-moment pair is:

\[
\boxed{
F_w,
\qquad
G_w=\sum_{i\in S}w_i^2.
}
\]

So arbitrary additive reweighting preserves both:

- exact first-moment closure on \(F_w\);
- exact second-moment closure on \((F_w,G_w)\).

---

# 212. Affine gauge theorem

Let:

\[
w_i'=aw_i+b,
\qquad
a\ne0.
\]

Then:

\[
F_{w'}(S)
=
aF_w(S)+kb.
\]

The centered observable transforms as:

\[
\widetilde F_{w'}
=
a\widetilde F_w.
\]

Therefore:

\[
\boxed{
\Delta F_{w'}=a\Delta F_w.
}
\]

Hence:

\[
\boxed{
A_{w'}=aA_w,
}
\]

and:

\[
\boxed{
B_{w'}=a^2B_w.
}
\]

The shell partition is unchanged because:

\[
F_{w'}(S)=F_{w'}(T)
\iff
F_w(S)=F_w(T).
\]

Thus:

\[
\boxed{
w_i\mapsto aw_i+b
}
\]

is an exact gauge of the additive transport description, up to orientation when \(a<0\).

The linear birth-rank coordinate is therefore naturally only defined up to scale and origin once equal spacing is assumed.

---

# 213. Birth-rank reversal

For the historical weights:

\[
w_i=i,
\]

the rank-reversal map:

\[
i\mapsto2k-i
\]

gives:

\[
w_i'=2k-w_i.
\]

Therefore:

\[
\boxed{
h\mapsto2k^2-h.
}
\]

This is the exact reflection recovered in RAW-10A.

Mathematically it is an affine gauge with negative scale.

However, if the arrow of cumulative growth history:

\[
\text{older}\to\text{newer}
\]

is retained as structure, birth-rank reversal reverses that arrow.

Therefore it should be described as:

\[
\boxed{
\text{a mathematical reflection symmetry of the rank chart},
}
\]

not automatically as a gauge symmetry of the oriented growth history.

---

# 214. General reflection criterion

Let:

\[
N=2k-1.
\]

Under label reversal:

\[
i\mapsto N+1-i,
\]

an additive observable has a simple shell reflection if:

\[
\boxed{
w_i+w_{N+1-i}=C
}
\]

for every \(i\).

Then:

\[
F_w(RS)
=
kC-F_w(S).
\]

Thus the shell centre is:

\[
\frac{kC}{2}.
\]

Linear birth ranks satisfy:

\[
C=2k.
\]

But they are not unique.

For example, centered odd functions of rank displacement:

\[
w_i=(i-k)^3
\]

also satisfy a reflection condition.

Therefore reflection symmetry does not uniquely select linear birth rank either.

---

# 215. Arbitrary label permutations

The Johnson graph is invariant under any permutation of its \(2k-1\) labels.

If the weights are carried with those labels, a permutation gives an isomorphic weighted observable.

Hence:

\[
\boxed{
\text{permuting the weight assignment leaves the universal transport law unchanged}.
}
\]

For a permutation of the linear weight multiset:

\[
\{1,\ldots,2k-1\},
\]

the complete multiset of shell values and shell multiplicities is unchanged.

RAW-10B verified this through:

\[
k=7.
\]

But there is a logical distinction.

If:

\[
i
\]

is specifically the birth rank of a label in the full graded history, then scrambling the weight assignment changes that history coordinate.

It is an automorphism of the isolated Johnson graph, not a gauge transformation of a fixed birth-history assignment.

---

# 216. No-go theorem for an intrinsic nonconstant scalar

The automorphism group of the Johnson vertex set contains the full permutation group:

\[
S_{2k-1},
\]

which acts transitively on all \(k\)-subsets.

Therefore any scalar observable:

\[
f:\Omega_k\to\mathbb R
\]

that is invariant under every label permutation must satisfy:

\[
f(S)=f(T)
\]

for every pair of states.

Hence:

\[
\boxed{
\text{every fully relabelling-invariant scalar on the isolated Johnson layer is constant}.
}
\]

So no nonconstant shell coordinate can be extracted from the isolated Johnson graph without supplying additional structure.

This is an exact obstruction, not a failure of imagination.

A useful scalar must reference something extra, such as:

- growth history;
- a distinguished subset;
- external weights;
- another relational structure.

---

# 217. One incoming growth map is not enough to define full birth rank

RAW-09A showed that the incoming map:

\[
HC_{2k-1}\to HC_{2k}
\]

distinguishes the newest target label and therefore selects the Johnson \(A_1\) chart.

But after deleting that newest label, the:

\[
2k-1
\]

parent labels remain symmetric under the single-step growth object.

Therefore the single incoming map does **not** by itself select:

\[
1,2,\ldots,2k-1
\]

as an order on those parent labels.

To obtain birth rank, one must retain the cumulative chain:

\[
HC_2
\to
HC_3
\to
\cdots
\to
HC_{2k}.
\]

Thus:

\[
\boxed{
h\text{ requires cumulative growth history, not merely the current growth edge}.
}
\]

This sharpens the dependency statement in RAW-10A.

---

# 218. Nonlinear reweighting of birth rank

Now choose:

\[
w_i=f(i)
\]

for any fixed function \(f\).

The observable:

\[
F_f(S)=\sum_{i\in S}f(i)
\]

remains additive.

Therefore the universal drift theorem still holds:

\[
\boxed{
\mathbb E[\Delta F_f\mid S]
=
-\lambda_k
(F_f-k\bar f).
}
\]

And its state diffusion still closes on:

\[
F_f
\]

and:

\[
G_f=\sum_{i\in S}f(i)^2.
\]

Thus even strongly nonlinear birth-age metrics preserve the exact restoring slope.

Example families certified in RAW-10B include:

- quadratic:
  \[
  f(i)=i^2;
  \]
- centered cubic:
  \[
  f(i)=(i-k)^3.
  \]

Both obey the exact universal drift and diffusion formulas.

---

# 219. Nonlinear reweighting changes the coarse geometry

Although the transport identities survive, the shell partition generally does not.

At:

\[
k=5,
\]

with:

\[
|\Omega_5|=126,
\]

RAW-10B found:

| weight family | shells | non-lumpable shells |
|---|---:|---:|
| constant | 1 | 0 |
| parity | 5 | 0 |
| linear birth rank | 21 | 17 |
| affine birth rank | 21 | 17 |
| reversed birth rank | 21 | 17 |
| quadratic birth rank | 93 | 26 |
| centered cubic | 77 | 35 |
| scrambled linear | 21 | 17 |
| powers of two | 126 | 0 |

This demonstrates:

\[
\boxed{
\text{exact additive drift closure}
\ne
\text{a unique or optimal coarse-graining}.
}
\]

The weights determine how much state-space compression the scalar coordinate provides.

---

# 220. Two extreme controls

## Two-valued/parity weights

A two-valued label weighting can produce a very small shell space.

For the parity weighting tested at \(k=5\):

\[
126\text{ states}
\to
5\text{ shells},
\]

and the partition is strongly lumpable.

This occurs because the observable is essentially an intersection count with a distinguished label class, an equitable Johnson-scheme coordinate.

## Powers-of-two weights

Assign:

\[
w_i=2^{i-1}.
\]

Every subset has a unique sum.

Therefore:

\[
\boxed{
\#\text{shells}=|\Omega_k|.
}
\]

The observable contains the full microstate information.

Strong lumpability is then trivial because every shell is a singleton.

So scalar additive observables range continuously from:

\[
\text{constant/no information}
\]

to:

\[
\text{complete state encoding}.
\]

Linear birth rank sits between these extremes.

---

# 221. Additive reweighting versus post-composition

The robustness theorem applies to:

\[
F_w(S)=\sum_{i\in S}w_i.
\]

It does **not** say that an arbitrary nonlinear function:

\[
\phi(h(S))
\]

has closed drift.

At:

\[
k=3,
\]

take:

\[
S=\{1,2,5\},
\qquad
T=\{1,3,4\}.
\]

Both satisfy:

\[
h(S)=h(T)=8,
\]

but:

\[
q(S)=30,
\qquad
q(T)=26.
\]

For:

\[
\phi(h)=h^2,
\]

the one-step drift is:

\[
\mathbb E[\Delta(h^2)\mid S]
=
2hA(h)+B(S).
\]

Hence:

\[
\boxed{
\mathbb E[\Delta(h^2)\mid S]
=
\frac{103}{6},
}
\]

while:

\[
\boxed{
\mathbb E[\Delta(h^2)\mid T]
=
\frac{107}{6}.
}
\]

Thus arbitrary nonlinear post-composition does not preserve scalar closure.

The universal class is **additive label reweighting**.

---

# 222. Linear birth rank is not selected by drift, diffusion, or reflection

RAW-10B therefore falsifies several possible uniqueness arguments.

Linear weights:

\[
w_i=i
\]

are **not uniquely selected** by:

### Exact restoring drift

All additive weights have it.

### Exact two-moment diffusion closure

All additive weights have it.

### Common restoring coefficient

All additive weights share the same \(\lambda_k\).

### Reflection symmetry

Any centrally antisymmetric weight system can have it.

### Johnson covariance

Arbitrary weight permutations give isomorphic weighted observables.

Therefore none of those properties explains why the historical coordinate should be linear birth rank.

---

# 223. What does select affine birth rank?

Suppose the full cumulative growth history gives an ordered sequence:

\[
1<2<\cdots<N.
\]

Now impose the additional principle:

> **Equal displacement in birth rank should have equal coordinate displacement, independent of absolute birth time.**

Formally, require:

\[
w_{i+d}-w_i
\]

to depend only on \(d\), whenever both indices exist.

Taking:

\[
d=1
\]

gives:

\[
w_{i+1}-w_i=c
\]

independent of \(i\).

Therefore:

\[
\boxed{
w_i=ai+b.
}
\]

Conversely, every affine weight system satisfies displacement homogeneity.

Hence:

\[
\boxed{
\text{ordered birth history}
+
\text{homogeneous birth displacement}
\Longrightarrow
\text{affine birth rank}.
}
\]

After quotienting the affine gauge:

\[
w_i\mapsto aw_i+b,
\]

one may choose the convenient representative:

\[
\boxed{
w_i=i.
}
\]

This is the first clean uniqueness statement for the linear coordinate.

---

# 224. Status of homogeneous birth displacement

The principle:

\[
w_{i+d}-w_i
=
\text{function of }d\text{ only}
\]

is not forced by Johnson geometry.

It says that successive growth events are assigned equal coordinate spacing.

That is a modelling convention analogous to choosing a homogeneous coordinate on an ordered sequence.

Therefore the correct status is:

\[
\boxed{
\text{linear birth rank is selected by homogeneous history parametrization, not by transport closure}.
}
\]

This is a much more precise statement than treating the integers \(1,\ldots,2k-1\) as self-evident.

---

# 225. Gauge hierarchy

RAW-10B suggests three distinct notions that should not be conflated.

## Johnson automorphism

Arbitrary permutation of current labels:

\[
S_{2k-1}.
\]

This preserves the unweighted Johnson graph.

## Additive observable gauge

For a fixed weighted observable:

\[
w_i\mapsto aw_i+b.
\]

This preserves shell equality structure and rescales transport moments covariantly.

## Growth-history covariance

Relabel the entire cumulative growth history consistently.

This preserves birth-rank meaning but does not allow arbitrary reassignment of ranks while keeping the history fixed.

These are different symmetry statements.

---

# 226. Standardized transport universality

For any nonconstant additive observable define:

\[
Z_w
=
\frac{
F_w-k\bar w
}{
\sqrt{\operatorname{Var}(F_w)}
}.
\]

Because the restoring coefficient does not depend on \(w\):

\[
\boxed{
\mathbb E[\Delta Z_w\mid S]
=
-\lambda_k Z_w(S).
}
\]

Thus every standardized additive observable has the same exact first-moment relaxation law.

The weight system affects:

- state degeneracies;
- diffusion structure;
- higher moments;
- shell geometry;
- physical interpretation, if any.

But not the normalized restoring coefficient.

This sharply limits what can be inferred from observing the drift coefficient alone.

---

# 227. RAW-10B verdict

The audit gives a three-part answer.

## Robust

The following survive arbitrary additive label reweighting:

\[
\boxed{
\text{exact linear restoring drift}
}
\]

with universal slope,

\[
\boxed{
\text{exact two-moment state diffusion}
}
\]

and:

\[
\boxed{
\text{first-eigenspace relaxation}.
}
\]

## Not robust

The following depend strongly on the chosen weights:

- shell counts;
- shell widths;
- strong lumpability;
- reflection unless the weights satisfy an additional symmetry;
- detailed coarse geometry;
- interpretation of the scalar coordinate.

## Linear birth rank

The historical choice:

\[
w_i=i
\]

is therefore not selected by Johnson transport.

It is selected only after adding:

1. cumulative growth order;
2. homogeneous spacing of birth displacement;
3. affine gauge normalization.

The clean statement is:

\[
\boxed{
\text{full growth history}
+
\text{homogeneous history coordinate}
\Longrightarrow
h(S)=\sum i
\quad
\text{up to affine gauge}.
}
\]

---

# 228. Computational certification

RAW-10B audited:

\[
k=2,\ldots,7
\]

against nine very different weight families:

1. constant;
2. parity/two-valued;
3. linear birth rank;
4. affine birth rank;
5. reversed birth rank;
6. quadratic birth rank;
7. centered cubic;
8. scrambled linear;
9. powers of two.

For every state of every tested Johnson graph it checked:

- universal drift;
- universal diffusion;
- stationary mean;
- stationary variance;
- additive eigenfunction identity.

It additionally checked:

- affine covariance;
- reflection where applicable;
- shell-count preservation under affine maps;
- global shell multiplicity preservation under weight permutations;
- unique subset sums for powers-of-two weights.

Final result:

\[
\boxed{
336/336
}
\]

strict checks passed.

---

# 229. Foundational consequence

The even transport branch is now cleaner.

The dependencies are:

\[
HC_{2k}
\]

\[
\downarrow
\]

intrinsic bipartitions,

\[
\downarrow
\]

incoming growth selects \(A_1\),

\[
\downarrow
\]

uniform Johnson transport convention,

while independently:

\[
\text{cumulative growth history}
\]

\[
\downarrow
\]

ordered birth ranks,

\[
\downarrow
\]

homogeneous history parametrization,

\[
\downarrow
\]

affine class:

\[
w_i=ai+b,
\]

\[
\downarrow
\]

convenient gauge:

\[
w_i=i,
\]

\[
\downarrow
\]

\[
h(S)=\sum i.
\]

This separates graph emergence from observable selection.

---

# 230. Immediate next questions

RAW-10B exposes two useful directions.

### EHF-HC-RAW-10C — Exact Coarse-Closure / Minimal Moment Audit

Since linear \(h\)-shells are not strongly lumpable, determine the smallest additional invariant/moment data required to make the Johnson transport exactly Markov under coarse-graining.

Candidates include:

\[
(h,q),
\]

label-refined counts,

or a small finite hierarchy of power sums.

### EHF-HC-RAW-11 — Growth-History Observable Reconstruction

Ask whether the cumulative birth order itself can be reconstructed from the graded HC growth object without explicitly carrying historical labels.

This is the deeper question behind whether birth rank is merely bookkeeping or an observable of the graded structure.

For mathematical closure, RAW-10C is the cleaner next step.


---

# 231. EHF-HC-RAW-10C — Exact Coarse-Closure / Minimal Moment Audit

## 231.1 Purpose

RAW-10A established:

\[
h=p_1=\sum_{i\in S}i
\]

has exact one-step drift closure, while state diffusion requires:

\[
p_2=q.
\]

It also established that the \(h\)-partition is not strongly lumpable for \(k\ge3\).

RAW-10C asks the sharper question:

> **What is the smallest exact autonomous coarse description that retains the birth-rank shell information?**

Two notions of minimality are audited.

### Markov/equitable minimality

Starting from the \(h\)-partition, repeatedly refine states according to their exact neighbour counts into the current coarse classes.

The terminal partition is the coarsest equitable, hence strongly lumpable, refinement of the \(h\)-partition.

### Moment minimality

Define the power sums:

\[
p_r(S)=\sum_{i\in S}i^r.
\]

Test partitions generated by:

\[
(p_1),
\]

\[
(p_1,p_2),
\]

\[
(p_1,p_2,p_3),
\]

and so on, and ask at what order the partition becomes strongly lumpable.

---

# 232. Exact equitable-refinement procedure

Let:

\[
\mathcal P_0
\]

be the partition into equal-\(h\) shells.

Given a partition \(\mathcal P_t\), define the colour/signature of state \(S\) by:

\[
\boxed{
\Sigma_t(S)
=
\left(
[S]_{\mathcal P_t},
\left\{
\#(N(S)\cap C)
:
C\in\mathcal P_t
\right\}
\right).
}
\]

Split states whenever these signatures differ.

Iterate until stable.

This is standard equitable partition refinement.

The fixed point is the coarsest equitable partition refining the original \(h\)-shell partition.

No moment ansatz is used in this construction.

---

# 233. Main finite result: exact \(h\)-Markov closure resolves the full state

RAW-10C performed the refinement on:

\[
J(5,3),
J(7,4),
J(9,5),
J(11,6),
J(13,7),
J(15,8),
J(17,9).
\]

Equivalently:

\[
k=3,\ldots,9.
\]

The result in every case was:

\[
\boxed{
\text{coarsest equitable refinement of the }h\text{-partition}
=
\text{singleton state partition}.
}
\]

Even more strongly, the **first refinement step** already separates every state.

The exact histories are:

| \(k\) | states | initial \(h\) shells | first refined classes |
|---:|---:|---:|---:|
| 3 | 10 | 7 | 10 |
| 4 | 35 | 13 | 35 |
| 5 | 126 | 21 | 126 |
| 6 | 462 | 31 | 462 |
| 7 | 1716 | 43 | 1716 |
| 8 | 6435 | 57 | 6435 |
| 9 | 24310 | 73 | 24310 |

Thus, throughout the audited range:

\[
\boxed{
\text{exact destination-shell profile relative to }h
\text{ identifies the entire microstate}.
}
\]

---

# 234. Consequence for exact autonomous shell dynamics

This is a strong negative result.

If a coarse partition:

1. must refine the \(h\)-shells;
2. must be exactly strongly lumpable for the microscopic Johnson walk;

then, through:

\[
k=3,\ldots,9,
\]

the only possibility is:

\[
\boxed{
\text{the full microstate partition}.
}
\]

So there is no nontrivial exact Markov coarse-graining that preserves \(h\) in the audited range.

This is stronger than the RAW-10A statement that \(h\) itself is not lumpable.

The exact failure is maximal:

\[
\boxed{
\text{the first missing transition information already distinguishes all states}.
}
\]

This is currently a finite theorem/certification, not yet an all-\(k\) proof.

---

# 235. What the first refinement is measuring

For a state \(S\) with shell height \(h\), a Johnson swap:

\[
a\in S,
\qquad
b\notin S
\]

changes height by:

\[
d=b-a.
\]

Therefore the exact destination-shell signature is equivalent to the directed displacement histogram:

\[
\boxed{
M_S(d)
=
\#\{
(a,b):
a\in S,\ b\notin S,\ b-a=d
\}.
}
\]

RAW-10C's first-refinement result is therefore equivalently:

> For \(k=3,\ldots,9\), the pair
> \[
> (h(S),M_S)
> \]
> uniquely identifies the subset \(S\).

This suggests a natural all-\(k\) theorem target.

---

# 236. Power-moment hierarchy

Define:

\[
\boxed{
p_r(S)=\sum_{i\in S}i^r.
}
\]

Let:

\[
T_r=\sum_{i=1}^{2k-1}i^r.
\]

Because every \(p_r\) is an additive label-weight observable, RAW-10B immediately gives:

\[
\boxed{
\mathbb E[\Delta p_r\mid S]
=
\frac{
kT_r-(2k-1)p_r(S)
}{
k(k-1)
}.
}
\]

Thus the drift of every power moment closes exactly on that same moment.

So for the vector:

\[
(p_1,\ldots,p_r),
\]

the complete first-moment drift vector closes exactly at order \(r\).

---

# 237. Exact cross-second-moment identity

For:

\[
\Delta p_r=b^r-a^r,
\]

and:

\[
\Delta p_s=b^s-a^s,
\]

their product is:

\[
(b^r-a^r)(b^s-a^s).
\]

Summing over all:

\[
a\in S,
\qquad
b\notin S
\]

gives:

\[
\boxed{
\mathbb E[
\Delta p_r\Delta p_s
\mid S
]
=
\frac{
kT_{r+s}
-
p_{r+s}
-
T_rp_s
-
T_sp_r
+
2p_rp_s
}{
k(k-1)
}.
}
\]

This generalizes RAW-10A's \(h,q\) formula.

---

# 238. Moment-order doubling

The cross-second moment of:

\[
p_r
\]

and:

\[
p_s
\]

requires:

\[
p_{r+s}.
\]

Therefore a moment vector:

\[
(p_1,\ldots,p_r)
\]

has exact first drift closure, but its complete one-step covariance matrix generally requires moments through:

\[
\boxed{
p_{2r}.
}
\]

If those moments are added, their own covariance requires moments through:

\[
p_{4r},
\]

and so forth.

Thus:

\[
\boxed{
\text{finite low-order moment closure is natural for drift but not automatically for full second-order transport}.
}
\]

On a finite \(k\)-subset state space the hierarchy ultimately terminates algebraically once enough power sums determine the state, but that is no longer a nontrivial coarse description.

---

# 239. The \((h,q)\) status

The pair:

\[
(h,q)
=
(p_1,p_2)
\]

has an important but limited exact role.

It determines:

- exact drift of \(h\);
- exact state diffusion of \(h\);
- exact drift of \(q\).

But it does **not** generally determine the full transition law of the pair.

RAW-10C found:

\[
\boxed{
(p_1,p_2)\text{ is not strongly lumpable for every audited }k\ge4.
}
\]

At \(k=3\), it is strongly lumpable only because:

\[
(p_1,p_2)
\]

already identifies every state.

So:

\[
\boxed{
(h,q)\text{ is a moment closure, not an exact Markov coarse state}.
}
\]

This distinction should be maintained.

---

# 240. Exact \((h,q)\) failure witness

At:

\[
k=4,
\]

consider:

\[
S=\{1,4,5,6\},
\]

and:

\[
T=\{2,3,4,7\}.
\]

Both have:

\[
p_1=16,
\]

and:

\[
p_2=78.
\]

Thus:

\[
\boxed{
(h,q)(S)=(h,q)(T).
}
\]

Nevertheless their exact neighbour-count profiles into \((h,q)\)-classes differ.

Therefore:

\[
\boxed{
(h,q)\text{ is not strongly lumpable already at }k=4.
}
\]

This is an explicit finite counterexample.

---

# 241. Higher power sums

RAW-10C tested partitions generated by:

\[
(p_1,\ldots,p_r).
\]

The first strongly lumpable order found was:

| \(k\) | first strongly lumpable \(r\) |
|---:|---:|
| 3 | 2 |
| 4 | 3 |
| 5 | 3 |
| 6 | 3 |
| 7 | 4 |
| 8 | 4 |
| 9 | 5 |

In every one of these cases, the first strongly lumpable moment partition was already:

\[
\boxed{
\text{the singleton partition}.
}
\]

So no nontrivial power-moment Markov closure was found.

The low orders fail because distinct states share the same moment tuple but have different coarse transition profiles.

The high order succeeds because the moments have become sufficient to reconstruct the state itself.

---

# 242. Power sums eventually reconstruct the microstate

A \(k\)-element subset:

\[
S=\{x_1,\ldots,x_k\}
\]

is the root set of the monic polynomial:

\[
\prod_{i=1}^k(t-x_i).
\]

Newton identities recover the elementary symmetric polynomials from the first:

\[
k
\]

power sums:

\[
p_1,\ldots,p_k.
\]

Therefore:

\[
\boxed{
(p_1,\ldots,p_k)
}
\]

always determines the subset exactly.

So exact moment closure can always be obtained by carrying enough moments.

But at that point it is simply a coordinate representation of the complete microstate.

RAW-10C found that the bounded integer universe often permits state reconstruction with fewer than \(k\) moments.

---

# 243. Three levels of closure

The audit suggests separating three notions that had previously been easy to blur.

## Level I — observable drift closure

For any additive observable:

\[
F_w,
\]

\[
\mathbb E[\Delta F_w\mid S]
\]

is a function of \(F_w\) alone.

This is highly robust.

## Level II — finite moment closure

For \(h\):

\[
\mathbb E[(\Delta h)^2\mid S]
\]

requires:

\[
q.
\]

More generally cross-second moments require higher power sums.

This gives exact low-order transport moments but not an autonomous coarse process.

## Level III — exact Markov closure

The complete transition distribution must depend only on the coarse state.

For \(h\)-refining partitions, RAW-10C finds that exact Markov closure requires the entire microstate through \(k=9\).

These levels should be stated separately in future EHF work.

---

# 244. Implication for Fokker--Planck language

A drift/diffusion pair:

\[
A(h),B(h)
\]

can be exact as conditional moments even when:

\[
h_t
\]

is not an autonomous Markov process.

Therefore continuum-style Fokker--Planck language should be understood as an effective description based on conditional low-order moments, not as an exact projection theorem.

RAW-10C strengthens the caution from RAW-10A:

\[
\boxed{
\text{exact moments do not imply exact coarse Markov dynamics}.
}
\]

---

# 245. A new theorem target

The finite data strongly suggests:

### Directed-displacement reconstruction conjecture

For every:

\[
k\ge3,
\]

a state:

\[
S\in\binom{[2k-1]}k
\]

is uniquely determined by its birth-rank height:

\[
h(S)
\]

together with the directed swap-displacement histogram:

\[
M_S(d).
\]

Equivalently:

\[
\boxed{
\text{one equitable refinement of the }h\text{-partition is the singleton partition}.
}
\]

This is certified for:

\[
3\le k\le9.
\]

An all-\(k\) proof would explain why exact \(h\)-preserving Markov coarse closure fails maximally.

---

# 246. RAW-10C verdict

The question was:

> What minimal extra information must accompany \(h\) to obtain exact autonomous coarse transport?

The answer depends on what “exact” means.

### Exact first moment

Nothing additional:

\[
\boxed{h}
\]

already closes drift.

### Exact second increment moment of \(h\)

Add:

\[
\boxed{q=p_2}.
\]

### Exact finite covariance hierarchy through moment order \(r\)

Generally require moments through:

\[
\boxed{2r}.
\]

### Exact autonomous Markov process refining \(h\)

In every audited graph:

\[
\boxed{
k=3,\ldots,9,
}
\]

the coarsest exact refinement is:

\[
\boxed{
\text{the full microstate}.
}
\]

So there is no nontrivial exact \(h\)-respecting Markov compression in the tested range.

---

# 247. Certification

RAW-10C exhaustively audited:

\[
k=3,\ldots,9,
\]

up to:

\[
J(17,9)
\]

with:

\[
24310
\]

microstates and degree:

\[
72.
\]

It computed:

- exact \(h\)-shell partitions;
- coarsest equitable refinements;
- power-moment partitions;
- exact lumpability tests;
- explicit failure witnesses.

All:

\[
\boxed{
34/34
}
\]

strict certification checks passed.

---

# 248. Immediate next questions

### EHF-HC-RAW-10D — Directed-Displacement Reconstruction Theorem

Attempt to prove for all \(k\ge3\) that the exact \(h\)-destination profile uniquely identifies the Johnson microstate.

This would upgrade the strongest RAW-10C observation to theorem.

### EHF-HC-RAW-11 — Growth-History Observable Reconstruction

Return to the graded HC object and ask whether cumulative birth order can itself be reconstructed relationally rather than stored as historical metadata.

Both are mathematically clean. RAW-10D is the direct closure of the current transport thread.


---

# 249. EHF-HC-RAW-10D — Directed-Displacement Reconstruction Theorem

## 249.1 Status

**Result:** exact all-\(k\) theorem.

RAW-10C found computationally that one equitable refinement of the birth-rank shell partition already separated every Johnson microstate for:

\[
k=3,\ldots,9.
\]

The finite observation was reformulated using the directed swap-displacement histogram:

\[
M_S(d)
=
\#\{
(a,b):
a\in S,\ b\notin S,\ b-a=d
\}.
\]

RAW-10D proves a stronger statement:

\[
\boxed{
M_S
\text{ alone uniquely determines }S
}
\]

for every:

\[
S\in\binom{[2k-1]}k.
\]

The shell height:

\[
h(S)=\sum_{i\in S}i
\]

is itself recoverable from the first signed moment of \(M_S\) and is therefore redundant.

---

# 250. Why \(M_S(d)\) is the exact one-step shell profile

The growth-selected Johnson graph is:

\[
J(2k-1,k).
\]

A neighbour of:

\[
S
\]

is obtained uniquely by removing:

\[
a\in S
\]

and inserting:

\[
b\notin S.
\]

For the birth-rank observable:

\[
h(S)=\sum_{i\in S}i,
\]

the increment is:

\[
\Delta h=b-a.
\]

Hence:

\[
\boxed{
M_S(d)
=
\#\{
S'\sim S:
h(S')-h(S)=d
\}.
}
\]

Thus the RAW-10C first equitable-refinement signature is exactly the directed displacement histogram.

No information is lost in passing from the neighbour list to the destination-\(h\) histogram.

---

# 251. Signed displacement moments

Let:

\[
N=2k-1.
\]

For:

\[
r\ge1,
\]

define the signed displacement moment:

\[
\boxed{
D_r(S)
=
\sum_d d^r M_S(d).
}
\]

Equivalently:

\[
\boxed{
D_r(S)
=
\sum_{\substack{a\in S\\b\notin S}}
(b-a)^r.
}
\]

Define the subset power sums:

\[
\boxed{
p_r(S)
=
\sum_{a\in S}a^r,
}
\]

and the ambient power sums:

\[
\boxed{
T_r
=
\sum_{j=1}^{N}j^r.
}
\]

Use the conventions:

\[
p_0=k,
\qquad
T_0=N.
\]

---

# 252. Master moment identity

Expand:

\[
(b-a)^r
=
\sum_{t=0}^r
(-1)^t
\binom rt
a^t b^{r-t}.
\]

Summing over:

\[
a\in S,
\qquad
b\notin S
\]

gives:

\[
\boxed{
D_r
=
\sum_{t=0}^r
(-1)^t
\binom rt
p_t
\left(
T_{r-t}-p_{r-t}
\right).
}
\]

This identity is exact for every:

\[
r\ge1.
\]

---

# 253. Separate the new power sum \(p_r\)

The endpoint terms are:

\[
t=0:
\qquad
k(T_r-p_r),
\]

and:

\[
t=r:
\qquad
(-1)^r
p_r(N-k).
\]

Since:

\[
N=2k-1,
\]

we have:

\[
N-k=k-1.
\]

Define the already-known lower-order contribution:

\[
\boxed{
L_r
=
\sum_{t=1}^{r-1}
(-1)^t
\binom rt
p_t
(T_{r-t}-p_{r-t}).
}
\]

Then:

\[
\boxed{
D_r
=
kT_r
+
L_r
+
c_rp_r,
}
\]

where:

\[
c_r
=
-k+(-1)^r(k-1).
\]

Therefore:

\[
\boxed{
c_r
=
\begin{cases}
-(2k-1),&r\text{ odd},\\[1mm]
-1,&r\text{ even}.
\end{cases}
}
\]

Crucially:

\[
\boxed{
c_r\ne0
\quad\text{for every }r.
}
\]

---

# 254. Recursive inversion theorem

Because:

\[
L_r
\]

contains only:

\[
p_1,\ldots,p_{r-1},
\]

the master identity recursively determines each new power sum.

For odd \(r\):

\[
\boxed{
p_r
=
\frac{
kT_r+L_r-D_r
}{
2k-1
}.
}
\]

For even \(r\):

\[
\boxed{
p_r
=
kT_r+L_r-D_r.
}
\]

Therefore:

\[
\boxed{
M_S
\Longrightarrow
D_1,D_2,\ldots
\Longrightarrow
p_1,p_2,\ldots
}
\]

recursively.

No search or optimization is required.

---

# 255. The shell height is redundant

For:

\[
r=1,
\]

there is no lower-order term:

\[
L_1=0.
\]

Hence:

\[
D_1
=
kT_1
-
(2k-1)p_1.
\]

Therefore:

\[
\boxed{
p_1=h
=
\frac{
kT_1-D_1
}{
2k-1
}.
}
\]

So:

\[
\boxed{
M_S
\text{ already determines }h(S).
}
\]

The original RAW-10C candidate invariant:

\[
(h,M_S)
\]

contains redundant information.

---

# 256. The second moment recovers \(q\)

For:

\[
r=2,
\]

the lower term is:

\[
L_2
=
-2p_1(T_1-p_1).
\]

Since the coefficient of:

\[
p_2
\]

is:

\[
-1,
\]

we obtain:

\[
\boxed{
p_2
=
kT_2
-
2T_1p_1
+
2p_1^2
-
D_2.
}
\]

But:

\[
p_2=q.
\]

Thus:

\[
\boxed{
q
=
kT_2
-
2T_1h
+
2h^2
-
D_2.
}
\]

The quantity:

\[
D_2
\]

is precisely the unnormalised second increment moment:

\[
D_2
=
k(k-1)
B(S).
\]

So the exact Johnson diffusion formula from RAW-10A is the \(r=2\) case of the reconstruction recurrence.

---

# 257. Transport moments are reconstruction moments

Because:

\[
M_S(d)
\]

is the complete one-step increment histogram,

\[
\frac{D_r}{k(k-1)}
=
\mathbb E[
(\Delta h)^r
\mid S
]
\]

under the uniform Johnson neighbour rule.

Therefore the full hierarchy of one-step increment moments determines:

\[
p_1,p_2,p_3,\ldots
\]

recursively.

The earlier transport identities now have a stronger interpretation:

\[
\boxed{
\text{one-step increment statistics encode the microscopic birth-rank subset}.
}
\]

This does not mean low-order moments alone determine the state.

It means the complete moment hierarchy does.

---

# 258. Newton reconstruction

A \(k\)-element subset:

\[
S=\{s_1,\ldots,s_k\}
\]

has elementary symmetric functions:

\[
e_1,\ldots,e_k.
\]

Newton identities recursively recover them from:

\[
p_1,\ldots,p_k.
\]

Explicitly, with:

\[
e_0=1,
\]

\[
\boxed{
m e_m
=
\sum_{i=1}^m
(-1)^{i-1}
e_{m-i}p_i.
}
\]

Therefore the displacement histogram determines:

\[
e_1,\ldots,e_k.
\]

Now form:

\[
\boxed{
P_S(x)
=
x^k
-e_1x^{k-1}
+e_2x^{k-2}
-\cdots
+(-1)^ke_k.
}
\]

By construction:

\[
\boxed{
P_S(x)
=
\prod_{s\in S}(x-s).
}
\]

Hence the roots of:

\[
P_S
\]

are exactly the elements of:

\[
S.
\]

Thus:

\[
\boxed{
M_S
\Longrightarrow
S.
}
\]

---

# 259. Directed-Displacement Reconstruction Theorem

## Theorem 259.1

Let:

\[
k\ge2,
\qquad
N=2k-1,
\]

and let:

\[
S\in\binom{[N]}k.
\]

Define:

\[
M_S(d)
=
\#\{
(a,b):
a\in S,\ b\notin S,\ b-a=d
\}
\]

for all nonzero integer displacements:

\[
-(N-1)\le d\le N-1.
\]

Then the map:

\[
\boxed{
S\mapsto M_S
}
\]

is injective.

Equivalently:

\[
\boxed{
M_S=M_T
\Longrightarrow
S=T.
}
\]

### Proof

The histogram determines every signed moment:

\[
D_r.
\]

The master identity recursively determines:

\[
p_r(S)
\]

for every \(r\), because the coefficient of the new \(p_r\) is:

\[
-(2k-1)
\]

for odd \(r\) and:

\[
-1
\]

for even \(r\).

In particular the histogram determines:

\[
p_1,\ldots,p_k.
\]

Newton identities determine the elementary symmetric functions:

\[
e_1,\ldots,e_k.
\]

These determine the monic polynomial:

\[
\prod_{s\in S}(x-s).
\]

Therefore they determine its root set \(S\).

\[
\square
\]

---

# 260. Exact all-\(k\) upgrade of RAW-10C

RAW-10C certified for:

\[
k=3,\ldots,9
\]

that one equitable refinement of the \(h\)-partition is the singleton partition.

RAW-10D proves this for every:

\[
\boxed{k\ge2}.
\]

Indeed, the first refinement signature is:

\[
(h,M_S).
\]

But:

\[
M_S
\]

already determines:

\[
h.
\]

Therefore:

\[
\boxed{
\text{the first exact neighbour-shell refinement of }h
\text{ is the singleton partition for every }k\ge2.
}
\]

Hence the coarsest equitable refinement of the \(h\)-partition is also the singleton partition.

This is now theorem, not finite evidence.

---

# 261. Exact Markov-closure corollary

Consider the uniform Johnson walk on:

\[
J(2k-1,k).
\]

Let a partition:

\[
\mathcal P
\]

satisfy:

1. \(\mathcal P\) refines the equal-\(h\) shell partition;
2. \(\mathcal P\) is strongly lumpable/equitable.

The coarsest equitable refinement of the \(h\)-partition is singleton by Theorem 259.1.

Therefore:

\[
\boxed{
\mathcal P
=
\text{singleton partition}
}
\]

or is finer only trivially.

Thus:

## Corollary 261.1

For every:

\[
k\ge2,
\]

there is no nontrivial exact strongly-lumpable Markov coarse-graining that preserves the birth-rank shell observable \(h\).

This upgrades the main negative conclusion of RAW-10C to an all-\(k\) theorem.

---

# 262. Why the directed nature matters

If one discards the sign of the displacement and retains only:

\[
M_S(d)+M_S(-d),
\]

one keeps only the number of selected/unselected pairs at absolute separation \(|d|\).

That is an autocorrelation-like statistic.

The inversion proof above uses the **signed moments**:

\[
D_r
=
\sum_dd^rM_S(d).
\]

Odd moments distinguish direction.

Therefore the theorem concerns:

\[
\boxed{
\text{directed displacement data}.
}
\]

An undirected absolute-displacement reconstruction theorem is not claimed.

---

# 263. Why the \(2k-1:k\) imbalance matters

For a more general ambient set of size:

\[
N
\]

and selected subset size:

\[
s,
\]

the coefficient of a new power sum \(p_r\) in the analogous recurrence is:

\[
\boxed{
-s+(-1)^r(N-s).
}
\]

For odd \(r\), this is always:

\[
-N.
\]

For even \(r\), it becomes:

\[
N-2s.
\]

In the Johnson geometry derived here:

\[
N=2k-1,
\qquad
s=k,
\]

so:

\[
N-2s=-1.
\]

Thus the even-order coefficient is never singular.

This is a notable structural consequence of the growth-derived Johnson state size:

\[
\boxed{
\text{the selected side exceeds its complement by exactly one label}.
}
\]

The reconstruction recurrence exploits exactly that imbalance.

No claim is made here about injectivity in the balanced case:

\[
N=2s.
\]

---

# 264. Connection to RAW-10B

RAW-10B showed that every additive observable:

\[
F_w
\]

lies in the same Johnson first eigenspace and has universal restoring drift.

RAW-10D gives the complementary statement for the specific linear birth-rank observable:

\[
h=p_1.
\]

Although its first-moment dynamics are extremely simple, the **full increment distribution** is information-rich enough to reconstruct the entire microstate.

Thus:

\[
\boxed{
\text{simple drift}
\not\Rightarrow
\text{simple transition information}.
}
\]

The same microscopic process can have:

- a one-dimensional exact drift law;
- a two-moment diffusion law;
- yet a full one-step increment histogram that encodes the complete state.

This sharply separates moment simplicity from Markov coarse simplicity.

---

# 265. Information hierarchy

RAW-10A through RAW-10D now give:

### Level 1

\[
h
\]

determines exact first drift.

### Level 2

\[
(h,q)
\]

determines exact second increment moment of \(h\).

### Level \(r\)

\[
p_1,\ldots,p_r
\]

control an increasing finite hierarchy of increment moments.

### Complete one-step shell profile

\[
M_S
\]

determines all:

\[
D_r,
\]

hence all:

\[
p_r,
\]

hence the full state:

\[
S.
\]

So:

\[
\boxed{
\text{the coarse transition profile contains microscopic reconstruction information}.
}
\]

---

# 266. Computational certification

Although the proof is exact, RAW-10D independently implemented the constructive inversion.

For every state through:

\[
k=10,
\]

it performed:

1. direct construction of \(M_S\);
2. recursive recovery of:
   \[
   p_1,\ldots,p_k;
   \]
3. Newton recovery of:
   \[
   e_1,\ldots,e_k;
   \]
4. reconstruction of the root set \(S\).

Exhaustive state counts:

| \(k\) | states |
|---:|---:|
| 2 | 3 |
| 3 | 10 |
| 4 | 35 |
| 5 | 126 |
| 6 | 462 |
| 7 | 1,716 |
| 8 | 6,435 |
| 9 | 24,310 |
| 10 | 92,378 |

Every histogram was unique.

Every reconstructed state matched exactly.

All:

\[
\boxed{
45/45
}
\]

strict certification checks passed.

---

# 267. Updated closure status

The exact transport thread can now be summarized:

\[
\boxed{
\text{Johnson }A_1
}
\]

\[
\downarrow
\]

\[
\boxed{
h\text{ has exact linear restoring drift}
}
\]

\[
\downarrow
\]

\[
\boxed{
(h,q)\text{ gives exact first two }h\text{-increment moments}
}
\]

but:

\[
\boxed{
h\text{-respecting exact Markov compression does not exist nontrivially}
}
\]

because:

\[
\boxed{
\text{one complete }h\text{-increment histogram reconstructs the microstate}.
}
\]

This is now an all-\(k\) mathematical theorem.

---

# 268. What RAW-10D does not imply

The theorem does not imply:

1. that a physical system literally observes or stores \(M_S\);
2. that all coarse descriptions are impossible;
3. that approximate Markov closure is impossible;
4. that \(h\) is physically meaningful;
5. that finite-time or noisy observation reconstructs the state efficiently;
6. that undirected displacement counts are injective;
7. that the same theorem holds for arbitrary Johnson parameters.

It is an exact combinatorial observability/reconstruction theorem for:

\[
J(2k-1,k)
\]

with the directed birth-rank displacement profile.

---

# 269. Immediate next questions

The RAW-10 transport subthread is now close to a natural stopping point.

Possible next targets:

### EHF-HC-RAW-10E — Undirected / Partial Displacement Information Audit

Determine how much reconstruction survives if only:

- \(|d|\);
- low-order moments;
- truncated displacement range;
- noisy counts;

are retained.

This would quantify information loss rather than exact closure.

### EHF-HC-RAW-11 — Growth-History Observable Reconstruction

Return upstream and ask whether the cumulative birth order needed for \(h\) can itself be reconstructed from the graded HC growth object.

### EHF-GRAPH-EMERG-00

The queued parallel graph-emergence branch can begin later without changing the HC-RAW spine.

The cleanest continuation of the foundational HC chain is RAW-11; RAW-10E is an optional information-theory extension.


---

# 270. EHF-HC-RAW-10E — Johnson Shell Ollivier Curvature Reaudit

## 270.1 Why this audit was necessary

The historical technical note reported a constant adjacent-shell Ollivier curvature law for the even Johnson shell kernel:

\[
\kappa_0(h,h+1)
=
\frac{2k-3}{k(k-1)}.
\]

At the time, the upstream Johnson reduction and the status of the shell process were less clear.

The rebuilt RAW chain has since established:

1. the intrinsic even-sector space;
2. the growth-relative Johnson \(A_1\) selection;
3. the exact Johnson drift/diffusion laws;
4. non-lumpability of the \(h\)-partition;
5. the all-\(k\) directed-displacement reconstruction theorem.

Therefore RAW-10E reaudits both the formula and its interpretation.

---

# 271. Correct kernel status

Let:

\[
\Omega_k
=
\binom{[2k-1]}k
\]

with the uniform Johnson \(A_1\) walk.

Let:

\[
h(S)=\sum_{i\in S}i.
\]

For each shell \(h\), let:

\[
N_h
=
|\{S:h(S)=h\}|.
\]

Let:

\[
M(h,h')
\]

be the number of directed Johnson edges from shell \(h\) to shell \(h'\).

Define:

\[
\boxed{
K(h,h')
=
\frac{M(h,h')}{N_h\,k(k-1)}.
}
\]

This is an exact stochastic kernel obtained by:

1. choosing a microstate uniformly inside shell \(h\);
2. making one uniform Johnson step;
3. retaining only the destination shell.

However RAW-10A and RAW-10D show that the \(h\)-partition is not strongly lumpable.

Therefore the correct status is:

\[
\boxed{
K=\text{exact uniformly shell-averaged conditional kernel},
}
\]

not:

\[
\boxed{
K=\text{autonomous Markov projection of every microscopic trajectory}.
}
\]

Ollivier curvature of \(K\) remains mathematically well defined once the shell metric is declared.

---

# 272. Exact microscopic Johnson curvature

Before coarse-graining, consider the full Johnson graph:

\[
J(n,k).
\]

Its degree is:

\[
\boxed{
d=k(n-k).
}
\]

Take adjacent vertices:

\[
X=A\cup\{a\},
\qquad
Y=A\cup\{b\},
\]

where:

\[
|A|=k-1.
\]

Let:

\[
C=[n]\setminus(A\cup\{a,b\}),
\]

so:

\[
|C|=n-k-1.
\]

The common neighbours of \(X\) and \(Y\) are exactly:

### Type I

\[
A\cup\{c\},
\qquad
c\in C,
\]

giving:

\[
n-k-1
\]

vertices.

### Type II

\[
(A\setminus\{u\})\cup\{a,b\},
\qquad
u\in A,
\]

giving:

\[
k-1
\]

vertices.

Hence:

\[
\boxed{
|N(X)\cap N(Y)|=n-2.
}
\]

---

# 273. Microscopic non-lazy coupling proof

Let:

\[
\mu_X,\mu_Y
\]

be the uniform non-lazy neighbour measures.

Each common neighbour carries mass:

\[
\frac1d
\]

under both measures, so that mass may remain fixed at cost zero.

The remaining unique neighbours have the form:

\[
X_{u,c}
=
(A\setminus\{u\})\cup\{a,c\},
\]

and:

\[
Y_{u,c}
=
(A\setminus\{u\})\cup\{b,c\}.
\]

Pair:

\[
X_{u,c}
\leftrightarrow
Y_{u,c}.
\]

Each pair is a Johnson edge and therefore costs one.

Finally pair:

\[
Y\in N(X)
\]

with:

\[
X\in N(Y),
\]

also at cost one.

Thus a coupling exists whose cost is exactly the unmatched mass:

\[
1-\frac{n-2}{d}.
\]

Because distinct graph vertices have distance at least one, total variation gives the matching lower bound.

Therefore:

\[
\boxed{
W_1(\mu_X,\mu_Y)
=
1-\frac{n-2}{d}.
}
\]

Hence:

\[
\boxed{
\kappa^{\rm micro}_0
=
\frac{n-2}{k(n-k)}.
}
\]

This is an exact all-\((n,k)\) theorem.

---

# 274. Specialization to the EHF Johnson layer

For the growth-derived Johnson graph:

\[
n=2k-1.
\]

Therefore:

\[
d=k(k-1),
\]

and:

\[
\boxed{
\kappa^{\rm micro}_0
=
\frac{2k-3}{k(k-1)}.
}
\]

This is exactly the historical shell-curvature formula.

Thus the value was already present in the microscopic Johnson graph.

This forces an interpretation change:

\[
\boxed{
\text{the shell averaging does not create this Ollivier curvature value}.
}
\]

Instead, the linear shell construction reproduces or preserves the same value.

---

# 275. Exact microscopic idleness law

Introduce idleness:

\[
\alpha\in[0,1].
\]

Let:

\[
\mu_X^\alpha
=
\alpha\delta_X
+
(1-\alpha)\mu_X.
\]

Define:

\[
\boxed{
\beta=\frac{1-\alpha}{d}.
}
\]

The common-neighbour overlap is:

\[
(n-2)\beta.
\]

At each endpoint \(X,Y\), the overlap is:

\[
\min(\alpha,\beta).
\]

Therefore total overlap is:

\[
\boxed{
(n-2)\beta
+
2\min(\alpha,\beta).
}
\]

The same explicit cost-one coupling transports all unmatched mass.

Thus:

\[
\boxed{
\kappa_\alpha^{\rm micro}
=
(n-2)\beta
+
2\min(\alpha,\beta).
}
\]

The branch point is:

\[
\alpha=\beta
\iff
\boxed{
\alpha_*=\frac1{d+1}.
}
\]

Hence:

### Low-idleness branch

For:

\[
0\le\alpha\le\frac1{d+1},
\]

\[
\boxed{
\kappa_\alpha^{\rm micro}
=
\frac{(n-2)(1-\alpha)}{d}
+
2\alpha.
}
\]

### High-idleness branch

For:

\[
\alpha\ge\frac1{d+1},
\]

\[
\boxed{
\kappa_\alpha^{\rm micro}
=
\frac{n(1-\alpha)}{d}.
}
\]

For:

\[
n=2k-1,
\]

this becomes:

\[
\boxed{
\kappa_\alpha
=
(1-\alpha)\frac{2k-3}{k(k-1)}
+
2\alpha
}
\]

below the threshold, and:

\[
\boxed{
\kappa_\alpha
=
(1-\alpha)\frac{2k-1}{k(k-1)}
}
\]

above it.

This exactly matches the historical \(\alpha=0.25\) and \(\alpha=0.5\) data.

---

# 276. Exact rational shell reaudit

RAW-10E rebuilt the linear birth-rank shell kernel using exact integer transition counts and rational arithmetic.

The complete adjacent-shell sweep covered:

\[
k=3,4,\ldots,11.
\]

Results:

| \(k\) | adjacent shell pairs | exact \(\kappa_0\) |
|---:|---:|---:|
| 3 | 6 | \(1/2\) |
| 4 | 12 | \(5/12\) |
| 5 | 20 | \(7/20\) |
| 6 | 30 | \(3/10\) |
| 7 | 42 | \(11/42\) |
| 8 | 56 | \(13/56\) |
| 9 | 72 | \(5/24\) |
| 10 | 90 | \(17/90\) |
| 11 | 110 | \(19/110\) |

Every adjacent shell pair matched:

\[
\boxed{
\kappa_0^{\rm shell}
=
\frac{2k-3}{k(k-1)}
}
\]

exactly.

This removes floating-point ambiguity from the old audit.

---

# 277. One-dimensional CDF formulation

For adjacent shells:

\[
h,\ h+1,
\]

define:

\[
\mu_h=K(h,\cdot),
\]

and:

\[
\nu_h=K(h+1,\cdot).
\]

Let:

\[
F_h(x)
\]

and:

\[
F_{h+1}(x)
\]

be their cumulative distributions on the integer shell line.

Define:

\[
\boxed{
C_h(x)
=
F_h(x)-F_{h+1}(x).
}
\]

On the unit-spaced line:

\[
\boxed{
W_1(\mu_h,\nu_h)
=
\sum_x|C_h(x)|.
}
\]

RAW-10E found an exact structural pattern through every audited shell.

---

# 278. The CDF one-defect property

For every:

\[
3\le k\le11
\]

and every adjacent shell pair:

\[
\boxed{
C_h(h)=-\frac1d,
}
\]

while:

\[
\boxed{
C_h(x)\ge0
\qquad
\text{for every }x\ne h.
}
\]

Thus the cumulative-difference profile has exactly one negative defect.

This was checked in exact rational arithmetic.

The local defect itself can be proved for all \(k\).

---

# 279. All-\(k\) proof of the local defect

Write:

\[
S=\{s_1<\cdots<s_k\}.
\]

The number of unselected labels below \(s_i\) is:

\[
s_i-i.
\]

Therefore the total number of Johnson swaps that decrease \(h\) is:

\[
\sum_{i=1}^k(s_i-i).
\]

But:

\[
\sum_i s_i=h,
\]

and:

\[
\sum_i i
=
h_{\min}
=
\frac{k(k+1)}2.
\]

Hence every state in shell \(h\) has exactly:

\[
\boxed{
r=h-h_{\min}
}
\]

downward Johnson swaps.

Since the degree is:

\[
d=k(k-1),
\]

and no Johnson swap has zero \(h\)-increment:

\[
F_h(h)
=
\frac rd.
\]

For shell \(h+1\):

\[
F_{h+1}(h)
=
\frac{r+1}{d}.
\]

Therefore:

\[
\boxed{
C_h(h)
=
-\frac1d.
}
\]

This part of the one-defect property is exact for all \(k\).

The remaining all-\(k\) proof target is:

\[
\boxed{
C_h(x)\ge0
\quad
(x\ne h).
}
\]

---

# 280. Curvature from the one-defect property

The exact drift from RAW-10A is:

\[
A(h)
=
\lambda(k^2-h),
\]

where:

\[
\boxed{
\lambda
=
\frac{2k-1}{d}.
}
\]

Therefore the difference between the means of:

\[
K(h+1,\cdot)
\]

and:

\[
K(h,\cdot)
\]

is:

\[
\boxed{
\rho=1-\lambda.
}
\]

For probability measures on the integer line:

\[
\sum_x C_h(x)
=
\mathbb E_{\nu_h}[X]
-
\mathbb E_{\mu_h}[X]
=
\rho.
\]

If the CDF one-defect property holds, then:

\[
\sum_{x\ne h}C_h(x)
=
\rho+\frac1d.
\]

Hence:

\[
W_1
=
\left(\rho+\frac1d\right)
+
\frac1d
=
\boxed{
\rho+\frac2d.
}
\]

Therefore:

\[
\kappa_0
=
1-W_1
=
\lambda-\frac2d.
\]

Since:

\[
\lambda=\frac{2k-1}{d},
\]

we obtain:

\[
\boxed{
\kappa_0
=
\frac{2k-3}{d}
=
\frac{2k-3}{k(k-1)}.
}
\]

Thus the historical all-\(k\) curvature conjecture reduces to one precise sign lemma.

---

# 281. Exact shell idleness formula from the same lemma

For the lazy measures:

\[
\mu_h^\alpha
=
\alpha\delta_h
+
(1-\alpha)K(h,\cdot),
\]

\[
\nu_h^\alpha
=
\alpha\delta_{h+1}
+
(1-\alpha)K(h+1,\cdot),
\]

the CDF difference changes only at the interval:

\[
[h,h+1).
\]

There:

\[
C_h^\alpha(h)
=
\alpha-\frac{1-\alpha}{d}.
\]

Every other cumulative difference is simply multiplied by:

\[
1-\alpha.
\]

Therefore the sign changes exactly at:

\[
\boxed{
\alpha_*=\frac1{d+1}.
}
\]

Assuming the one-defect lemma, the shell curvature is:

### Low branch

\[
\boxed{
\kappa_\alpha^{\rm shell}
=
(1-\alpha)\frac{2k-3}{d}
+
2\alpha,
\qquad
\alpha\le\frac1{d+1}.
}
\]

### High branch

\[
\boxed{
\kappa_\alpha^{\rm shell}
=
(1-\alpha)\frac{2k-1}{d},
\qquad
\alpha\ge\frac1{d+1}.
}
\]

This is exactly the microscopic Johnson idleness law specialized to:

\[
n=2k-1.
\]

RAW-10E checked the piecewise formula exactly for representative \(\alpha\) values on both branches for every:

\[
k=3,\ldots,11.
\]

---

# 282. Drift-curvature difference explained

The historical note observed:

\[
\lambda_A
=
\frac{2k-1}{d},
\]

and:

\[
\kappa_0
=
\frac{2k-3}{d},
\]

so:

\[
\lambda_A-\kappa_0
=
\frac2d.
\]

RAW-10E gives a concrete combinatorial explanation.

For two adjacent microscopic Johnson states:

- there are:
  \[
  2k-3
  \]
  common neighbours;
- there are two distinguished exchanged endpoints.

At zero idleness the endpoints do not contribute overlap.

Thus:

\[
\boxed{
\kappa_0
=
\frac{\text{common neighbours}}{d}
=
\frac{2k-3}{d}.
}
\]

With sufficient idleness, endpoint overlap contributes as well, and the high-idleness branch uses the coefficient:

\[
\boxed{
\frac{2k-1}{d}
=
\lambda_A.
}
\]

So the difference:

\[
\frac2d
\]

has an exact endpoint-overlap meaning.

This is more specific than the old statement that drift and curvature merely had similar asymptotic scale.

---

# 283. Curvature is not created by shell coarse-graining

The old note emphasized the shell layer as the location where the Ricci-like behaviour appeared.

RAW-10E changes that conclusion.

The microscopic Johnson graph already satisfies:

\[
\boxed{
\kappa_0^{\rm micro}
=
\frac{2k-3}{k(k-1)}.
}
\]

The historical linear shell kernel satisfies the same value:

\[
\boxed{
\kappa_0^{\rm shell}
=
\kappa_0^{\rm micro}
}
\]

through every audited \(k\).

Likewise their idleness formulas agree.

Therefore the safer statement is:

> **The linear birth-rank shell averaging preserves or exactly reproduces the microscopic Johnson Ollivier curvature value.**

Do not say:

> positive Ollivier curvature is generated only after coarse-graining.

At least for this curvature notion, that is false.

---

# 284. Observable robustness audit

RAW-10B showed that exact restoring drift is universal for every additive label-weight observable.

RAW-10E asked whether constant adjacent-shell Ollivier curvature is equally universal.

It is not.

For:

\[
k=3,\ldots,6,
\]

the following controls were tested exactly.

## Arithmetic-progression family

The following all reproduced the historical constant law:

- linear birth rank;
- affine transforms;
- reversed rank;
- scrambled assignments of the same arithmetic-progression weight multiset.

This is expected from affine metric covariance and Johnson label-permutation symmetry.

## Nonlinear controls

Quadratic birth weights:

\[
w_i=i^2
\]

produced strongly nonconstant curvature and many negative adjacent-shell values.

At:

\[
k=5,
\]

the range was:

\[
\boxed{
-\frac{161}{20}
\le
\kappa
\le
\frac7{20}.
}
\]

Centered cubic weights also produced variable and negative curvature.

Two-valued parity weights produced positive but nonconstant curvature.

At:

\[
k=5,
\]

the two values were:

\[
\frac7{20},
\qquad
\frac9{20}.
\]

Therefore:

\[
\boxed{
\text{constant shell curvature is not universal across additive observables}.
}
\]

This sharply contrasts with the universal additive drift law.

---

# 285. Constant curvature does not uniquely select linear spacing

The previous result must not be over-interpreted.

A finite search over distinct integer weights found non-arithmetic weight systems with constant shell curvature.

For:

\[
k=3,
\]

among 70 normalized increasing weight systems:

\[
0=w_1<\cdots<w_5\le8,
\]

15 had constant adjacent-shell curvature, of which 13 were non-arithmetic.

For:

\[
k=4,
\]

among 210 systems:

\[
0=w_1<\cdots<w_7\le10,
\]

two had constant curvature, including the non-arithmetic example:

\[
\boxed{
(0,2,3,4,5,6,8).
}
\]

Therefore:

\[
\boxed{
\text{constant Ollivier shell curvature does not uniquely select affine birth rank}.
}
\]

It is a discriminating property, but not a uniqueness principle.

---

# 286. Scrambled arithmetic progressions

A further caution follows from Johnson symmetry.

Suppose the weights are the arithmetic progression:

\[
1,2,\ldots,2k-1
\]

but assigned to labels in an arbitrary permutation.

Because any label permutation is an automorphism of the Johnson graph, the resulting weighted shell process is isomorphic to the linear one.

Therefore it has the same constant curvature.

So Ollivier curvature cannot determine which label was actually older or younger in the cumulative HC growth history.

It sees the weighted Johnson geometry, not the chronology attached to that weighting.

Thus RAW-10E does not replace the growth-history reconstruction problem.

---

# 287. Relation to RAW-10D non-lumpability

RAW-10D proved:

\[
\text{one complete }h\text{-increment histogram}
\Longrightarrow
\text{full microstate}.
\]

So the conditional measures:

\[
K(h,\cdot)
\]

average distributions that are microscopically distinct enough to identify individual states before averaging.

Yet their adjacent-shell Wasserstein curvature is constant.

This is a useful example of:

\[
\boxed{
\text{simple coarse transport geometry coexisting with maximal microscopic non-lumpability}.
}
\]

Constant Ollivier curvature therefore does not imply that the coarse variable forms an exact autonomous Markov projection.

---

# 288. Current proof status of the shell theorem

The status should now be separated carefully.

## Proved exactly

1. microscopic Johnson non-lazy curvature:
   \[
   \kappa_0^{\rm micro}
   =
   \frac{n-2}{k(n-k)};
   \]
2. microscopic idleness law;
3. shell CDF defect:
   \[
   C_h(h)=-1/d;
   \]
4. curvature/idleness formula conditional on the one-defect CDF sign lemma.

## Exhaustively certified in exact rational arithmetic

For:

\[
k=3,\ldots,11,
\]

all adjacent linear birth-rank shell pairs satisfy:

\[
C_h(x)\ge0
\quad
(x\ne h),
\]

and therefore:

\[
\kappa_0^{\rm shell}
=
\frac{2k-3}{k(k-1)}.
\]

## Remaining theorem target

Prove for all \(k\):

\[
\boxed{
C_h(x)\ge0
\qquad
(x\ne h).
}
\]

This is now the single missing lemma behind the all-\(k\) shell-curvature theorem.

---

# 289. Reassessment of the historical note

The old note survives in part but needs substantial wording changes.

### Survives

- exact Johnson drift law;
- constant shell curvature numerical law;
- positive curvature;
- exact line-metric Wasserstein calculation;
- close algebraic relation between drift and curvature coefficients.

### Strengthened

- Johnson \(A_1\) now has a reconstructed HC/growth origin;
- shell curvature is verified with exact rational arithmetic;
- microscopic Johnson curvature has an exact coupling proof;
- idleness dependence now has a closed piecewise formula.

### Revised

- \(K(h,h')\) is a conditional shell-averaged kernel, not an exact strong Markov quotient;
- curvature is not generated by shell averaging—it is already present microscopically;
- the drift/curvature difference has a concrete two-endpoint explanation.

### Not supported as a general statement

- constant curvature is not universal for arbitrary additive observables;
- constant curvature does not uniquely identify linear birth rank;
- shell Ollivier curvature and odd square-loop curvature should not yet be called complementary manifestations of the same geometry.

---

# 290. RAW-10E verdict

The old curvature discovery is mathematically real.

But its best current interpretation is different.

The strongest safe statement is:

> **The growth-derived Johnson graph \(J(2k-1,k)\) has exact positive microscopic Ollivier curvature \((2k-3)/(k(k-1))\). The uniformly shell-averaged kernel associated with the linear birth-rank observable reproduces exactly the same adjacent-shell curvature through \(k=11\) in rational arithmetic. Its all-\(k\) proof reduces to a single CDF one-defect sign lemma. The shell kernel is an exact conditional coarse kernel rather than a strongly lumped Markov quotient. Constant curvature is not universal across additive observables and does not uniquely select the birth-rank coordinate.**

This is both stronger mathematically and more conservative interpretively than the historical formulation.

---

# 291. Certification ledger

RAW-10E performed:

1. exact shell-kernel reconstruction through:
   \[
   k=11;
   \]
2. exact rational adjacent-shell Wasserstein calculation;
3. CDF one-defect verification on every adjacent shell pair;
4. exact representative idleness checks on both branches;
5. microscopic Johnson curvature formula ledger through:
   \[
   n=30;
   \]
6. additive-observable stress tests through:
   \[
   k=6;
   \]
7. finite non-uniqueness searches for constant weighted-shell curvature.

Primary certification:

\[
\boxed{
278/278
}
\]

strict checks passed.

---

# 292. What should happen next

RAW-10E is a natural closure point for the rebuilt Johnson transport/curvature branch.

There are two possible continuations.

### Optional RAW-10F — CDF One-Defect Proof

Attempt the remaining all-\(k\) sign lemma:

\[
C_h(x)\ge0
\quad
(x\ne h).
\]

This is now a sharply isolated combinatorial theorem problem.

### RAW-11 — Growth-History Observable Reconstruction

Return upstream and ask whether the cumulative birth ordering required for:

\[
h(S)=\sum i
\]

can itself be reconstructed from the graded Hamilton-cycle growth object.

For the foundation rebuild, RAW-11 remains the more important next step. RAW-10F can be queued as a theorem-completion side target.


---

# 293. EHF-HC-RAW-11 — Growth-History Observable Reconstruction

## 293.1 Purpose

RAW-10A through RAW-10E clarified the status of the historical Johnson shell observable:

\[
h(S)=\sum_{i\in S}i.
\]

Its exact transport mathematics is valid, but its numerical label weights:

\[
1,2,\ldots,2k-1
\]

require more structure than a single isolated Johnson graph.

RAW-11 asks:

> **Can the cumulative birth history needed by \(h\) be reconstructed from the graded Hamilton-cycle growth object itself, rather than supplied as external metadata?**

The answer is:

\[
\boxed{
\text{first-appearance stage is reconstructible from a full growth filtration},
}
\]

but:

\[
\boxed{
\text{an HC tower beginning at }HC_3
\text{ does not intrinsically order the three seed labels}.
}
\]

Thus the exact historical rank observable is only partially reconstructed by the HC tower alone.

---

# 294. Four information levels

It is essential to distinguish four different objects.

## Level 0 — final layer only

Retain:

\[
HC_N
\]

with its full raw comparison structure.

The relabelling group:

\[
S_N
\]

acts transitively on the \(N\) labels.

Therefore no label has a distinguished birth status.

## Level 1 — one incoming growth map

Retain:

\[
HC_{N-1}
\to
HC_N
\]

with its distinguished new label \(x_N\) and deletion map:

\[
\pi_{x_N}.
\]

This distinguishes:

\[
\boxed{x_N}
\]

from the \(N-1\) old labels.

But:

\[
S_{N-1}
\]

still permutes all old labels.

Thus one incoming map reconstructs only:

\[
\boxed{\text{newest versus old}}.
\]

## Level 2 — full cumulative one-site growth filtration

Retain the nested atom sets:

\[
V_r
\subset
V_{r+1}
\subset
\cdots
\subset
V_N,
\]

with:

\[
|V_n|=n,
\]

and:

\[
|V_n\setminus V_{n-1}|=1.
\]

This reconstructs the first-appearance stage of every atom.

## Level 3 — growth maps with atom incidence forgotten

If one keeps only abstract state-to-state maps but erases the underlying atom incidence and cross-layer label identity, birth stage is not automatically available as an atom observable.

RAW-11 therefore treats the atom filtration as part of the graded growth data.

Reconstructing atoms themselves from fully abstract state maps would be a separate theorem problem.

---

# 295. First-appearance stage

For a full one-site filtration define:

\[
\boxed{
\beta(v)
=
\min\{
n:v\in V_n
\}.
}
\]

Then:

\[
\beta(v)=r
\]

for every seed atom:

\[
v\in V_r,
\]

while for:

\[
n>r,
\]

the unique atom:

\[
x_n\in V_n\setminus V_{n-1}
\]

satisfies:

\[
\boxed{
\beta(x_n)=n.
}
\]

Thus the tower reconstructs the birth-stage partition:

\[
\boxed{
V_r,
\{x_{r+1}\},
\{x_{r+2}\},
\ldots,
\{x_N\}.
}
\]

---

# 296. Filtration automorphism theorem

Consider atom permutations preserving every level:

\[
V_r,V_{r+1},\ldots,V_N.
\]

Every later singleton difference:

\[
V_n\setminus V_{n-1}
=
\{x_n\}
\]

must be fixed.

The only freedom is to permute the seed block:

\[
V_r.
\]

Therefore:

\[
\boxed{
\operatorname{Aut}_{\rm atom}
(\mathcal T_{r,N})
\cong
S_r.
}
\]

Its order is:

\[
\boxed{r!}.
\]

This remains a symmetry of the full HC growth tower because simultaneous relabelling of the seed labels preserves every Hamilton-cycle state set, local relation and growth map.

Hence the residual seed ambiguity is genuine.

---

# 297. Maximal orbit structure of birth information

The atom orbits under the full tower automorphism group are:

\[
\boxed{
V_r,
\{x_{r+1}\},
\ldots,
\{x_N\}.
}
\]

Therefore any scalar atom observable that is intrinsic to the tower must be constant on:

\[
V_r.
\]

It may assign distinct values to the later singleton birth classes.

Thus the first-appearance function:

\[
\beta
\]

is a canonical orbit-separating observable.

But if:

\[
r>1,
\]

there can be no tower-invariant injective total rank on all atoms.

---

# 298. Final-layer no-go theorem

On:

\[
HC_N
\]

alone, full relabelling symmetry acts transitively on labels.

Therefore any fully relabelling-invariant scalar:

\[
w:V_N\to\mathbb R
\]

must satisfy:

\[
\boxed{
w(v)=\text{constant}.
}
\]

So birth order cannot be reconstructed from a single layer.

This is the atom-level analogue of the RAW-10B no-go result for scalar Johnson state observables.

---

# 299. One-step no-go theorem

Now include only one incoming map:

\[
V_{N-1}
\subset
V_N.
\]

The atom orbits are:

\[
\boxed{
V_{N-1},
\qquad
\{x_N\}.
}
\]

Therefore a one-step intrinsic scalar can distinguish only two values:

\[
\boxed{
\text{old},
\qquad
\text{new}.
}
\]

It cannot reconstruct the internal chronology of:

\[
V_{N-1}.
\]

This sharpens RAW-10A's statement that the newest-site anchor selects Johnson \(A_1\): that construction needs only the newest-versus-old distinction, whereas the historical \(h\) observable requires the full cumulative history.

---

# 300. The natural Hamilton-cycle seed

The smallest ordinary Hamilton cycle is:

\[
HC_3.
\]

At:

\[
n=3,
\]

there is one undirected Hamilton-cycle state, the triangle.

Its three labels remain fully symmetric:

\[
\boxed{
S_3
}
\]

acts on them.

Therefore a natural HC-only cumulative tower:

\[
HC_3
\to
HC_4
\to
\cdots
\to
HC_N
\]

reconstructs:

\[
\boxed{
\beta(v)=3
\quad
(v\in V_3),
}
\]

and:

\[
\boxed{
\beta(x_n)=n
\quad
(n\ge4).
}
\]

But it does not distinguish which seed label should historically be called:

\[
1,\ 2,\ \text{or }3.
\]

---

# 301. Exact seed-order obstruction

Suppose the historical linear rank assigns the seed values:

\[
1,\ 2,\ 3.
\]

The HC\(_3\)-seeded tower admits the automorphism swapping the atoms historically called:

\[
1
\leftrightarrow
3.
\]

For example, at:

\[
k=3,
\]

the Johnson states:

\[
S=\{1,4,5\},
\]

and:

\[
T=\{3,4,5\}
\]

are related by this seed automorphism.

But:

\[
h(S)=10,
\]

while:

\[
h(T)=12.
\]

Hence:

\[
\boxed{
h
\text{ is not invariant under the HC}_3\text{-tower automorphism group}.
}
\]

The same obstruction persists at every larger layer.

So the exact historical rank sum:

\[
h=\sum i
\]

is not intrinsic to an HC\(_3\)-seeded tower.

---

# 302. Canonical HC-tower replacement

The exact tower-invariant additive alternative is:

\[
\boxed{
H_\beta(S)
=
\sum_{v\in S}\beta(v).
}
\]

For an HC\(_3\)-seeded tower, its weights are:

\[
\boxed{
(3,3,3,4,5,\ldots,2k-1).
}
\]

Equivalently, after subtracting the common seed stage:

\[
\boxed{
(0,0,0,1,2,\ldots,2k-4)
}
\]

up to an additive gauge.

This observable is invariant under all seed permutations:

\[
S_3.
\]

For the previous witness:

\[
H_\beta(\{1,4,5\})
=
H_\beta(\{3,4,5\})
=
12.
\]

Thus:

\[
\boxed{
H_\beta
}
\]

is reconstructible from the HC growth filtration without an arbitrary seed order.

---

# 303. Transport of the canonical stage observable

RAW-10B proved that every additive weight observable:

\[
F_w(S)=\sum_{i\in S}w_i
\]

has exact Johnson restoring drift.

Therefore:

\[
H_\beta
\]

automatically satisfies:

\[
\boxed{
\mathbb E[
\Delta H_\beta
\mid S
]
=
-\frac{2k-1}{k(k-1)}
\left(
H_\beta(S)-k\bar\beta
\right).
}
\]

So the universal restoring coefficient survives removal of the arbitrary seed ordering.

RAW-11 directly certified this through:

\[
k=3,\ldots,8.
\]

This strengthens the conclusion from RAW-10B:

\[
\boxed{
\text{the exact restoring drift does not depend on resolving the seed ambiguity}.
}
\]

---

# 304. Stationary variance of the canonical stage observable

Let:

\[
\sigma_\beta^2
\]

be the population variance of the stage weights.

RAW-10B gives:

\[
\boxed{
\operatorname{Var}(H_\beta)
=
\frac{k}{2}\sigma_\beta^2.
}
\]

RAW-11 checked this exactly through:

\[
k=8.
\]

The resulting width differs from the historical linear-rank width because the three seed labels are tied.

Thus the exact drift coefficient is robust, while shell width remains coordinate-dependent.

---

# 305. Curvature does not survive unchanged

RAW-10E showed that constant shell Ollivier curvature is not universal across additive observables.

The canonical HC\(_3\)-stage weights give a direct foundational control.

For:

\[
k=3,\ldots,8,
\]

the tied-seed observable did **not** have constant adjacent-shell curvature.

Examples:

### \(k=3\)

Curvature values range from:

\[
\frac12
\]

to:

\[
\frac56.
\]

### \(k=5\)

The two exact values are:

\[
\frac7{20},
\qquad
\frac9{20}.
\]

### \(k=8\)

The values range from:

\[
\frac{83}{360}
\]

to:

\[
\frac{15}{56}.
\]

Therefore:

\[
\boxed{
\text{the historical constant-curvature shell law requires more than the HC}_3
\text{-tower birth-stage observable}.
}
\]

In particular, it depends on resolving the seed labels into a distinct weighted rank system, or on another weight structure with the same curvature property.

---

# 306. Implication for the old curvature note

RAW-10E already showed that microscopic Johnson curvature is independent of the shell coordinate.

RAW-11 adds:

- the **linear** shell curvature law uses more history structure than an HC\(_3\)-seeded tower alone supplies;
- the canonical tied-seed history observable keeps exact restoring drift but loses constant shell curvature.

So the old shell curvature should not be called a consequence merely of:

\[
\boxed{
\text{HC growth history}.
}
\]

A more precise dependency is:

\[
\boxed{
\text{Johnson }A_1
+
\text{distinct rank weighting of parent labels}
}
\]

for the historical linear shell construction.

---

# 307. How to recover unique rank exactly

There are two clean options.

## Option A — supply an ordered seed

Add extra structure that totally orders:

\[
V_3.
\]

Then the cumulative HC tower reconstructs:

\[
1,2,3,4,\ldots,N.
\]

But the seed order is an additional primitive.

## Option B — extend the atom filtration below Hamilton-cycle formation

Introduce:

\[
V_1
\subset
V_2
\subset
V_3
\subset
V_4
\subset\cdots
\]

with exactly one atom added at each stage.

Hamilton-cycle state geometry begins only at:

\[
n=3,
\]

but the atom-growth substrate begins earlier.

Then:

\[
\boxed{
\beta(v)=1,2,\ldots,N
}
\]

is uniquely determined by first appearance.

The atom filtration automorphism group is:

\[
\boxed{
S_1=\{e\}.
}
\]

Thus unique birth rank becomes intrinsic to the **extended substrate-growth tower**.

---

# 308. Status of the pre-HC extension

Option B is mathematically clean, but its dependency must be stated honestly.

The structures:

\[
V_1,
\qquad
V_2
\]

do not yet carry ordinary Hamilton cycles.

Therefore:

\[
\boxed{
\text{unique birth rank is not derived from Hamilton-cycle geometry alone}.
}
\]

It is derived from:

\[
\boxed{
\text{a one-atom-at-a-time distinguishable-label substrate filtration}
}
\]

on which Hamilton-cycle states become available beginning at:

\[
n=3.
\]

This may fit the broader EHF foundation naturally because distinguishable labels:

\[
V_n
\]

already precede the definition of:

\[
HC_n.
\]

But it should be adopted explicitly rather than retroactively assumed.

---

# 309. Minimal extension theorem

Let the substrate contain a filtration:

\[
V_1
\subset
V_2
\subset\cdots\subset
V_N,
\]

with:

\[
|V_n|=n,
\]

and one new atom per stage.

Then:

\[
\boxed{
\beta(v)=\min\{n:v\in V_n\}
}
\]

is injective.

Since exactly one atom has each birth stage:

\[
1,\ldots,N,
\]

\[
\beta
\]

is a canonical total rank.

Therefore:

\[
\boxed{
\text{one-atom substrate filtration}
\Longrightarrow
\text{unique birth rank}.
}
\]

Hamilton-cycle geometry may then be layered on top from:

\[
n=3.
\]

This is the minimal symmetry-breaking extension required to derive the historical unique rank without an arbitrary seed order.

---

# 310. Is numerical spacing also reconstructed?

If the filtration is graded by cardinality:

\[
|V_n|=n,
\]

then first-appearance stage already carries the integer value:

\[
n.
\]

So the canonical rank coordinate is:

\[
\boxed{
w(v)=\beta(v).
}
\]

One may still apply an affine reparametrization:

\[
w\mapsto aw+b
\]

as a coordinate gauge if only relative spacing is relevant.

But unlike an arbitrary monotone reweighting, the integer stage itself is defined by the graded cardinality.

Thus the extended substrate filtration supplies more than merely a total order.

---

# 311. Tower covariance

The phrase “birth rank is intrinsic” should not mean that literal symbol names are fixed.

Let:

\[
\phi_n:V_n\to V_n'
\]

be a compatible relabelling of the entire tower.

Compatibility means:

\[
\phi_{n+1}|_{V_n}
=
\phi_n.
\]

Then:

\[
\boxed{
\beta'(\phi(v))=\beta(v).
}
\]

So birth stage is covariant under tower isomorphisms.

This is the correct notion of structural invariance.

---

# 312. Relation to RAW-09A

RAW-09A needed only the newest site:

\[
x_{2k}
\]

to define the growth-relative Johnson chart.

Therefore the derivation:

\[
LR2_{\rm horizontal}
\to
A_1
\]

does **not** require full birth rank.

This is important.

The Johnson graph is already derived with one incoming growth map.

The cumulative filtration is needed only for the historical scalar shell coordinate.

Thus:

\[
\boxed{
\text{Johnson geometry}
}
\]

and:

\[
\boxed{
\text{birth-rank shell geometry}
}
\]

have different upstream requirements.

---

# 313. Relation to RAW-10B

RAW-10B showed:

\[
\boxed{
\text{all additive weight observables share the same exact restoring coefficient}.
}
\]

RAW-11 now identifies three history-weight statuses.

### Isolated-layer arbitrary weight

External coordinate structure.

### HC\(_3\)-tower canonical weight

\[
\beta=(3,3,3,4,5,\ldots).
\]

Fully reconstructed from the HC growth tower.

### Extended \(V_1\)-tower canonical weight

\[
\beta=(1,2,3,\ldots).
\]

Fully reconstructed from the one-atom substrate-growth tower.

The historical \(h\) belongs to the third category unless an ordered HC seed is supplied.

---

# 314. Relation to admissible-comparison foundations

RAW-11 does not require the claim:

> birth time is physically fundamental.

The precise structural statement is:

> **If the EHF substrate is supplied as a graded sequence of distinguishable-label sets with one atom added at each stage, then first-appearance stage is reconstructible data of that graded structure. Hamilton-cycle comparison geometry begins at the first stage supporting such states.**

This remains a modelling choice about the graded substrate.

It is not implied by a single static Hamilton-cycle layer.

---

# 315. RAW-11 verdict

The question was whether growth history can be reconstructed rather than manually stored.

The answer has three levels.

## From a static layer

\[
\boxed{\text{NO}.}
\]

Full relabelling symmetry erases chronology.

## From one incoming growth map

\[
\boxed{\text{PARTIALLY}.}
\]

Only newest versus old is reconstructed.

## From a cumulative HC tower beginning at \(HC_3\)

\[
\boxed{\text{YES for birth stage, NO for unique seed rank}.}
\]

The canonical history observable has tied seed weights:

\[
(3,3,3,4,5,\ldots).
\]

## From a one-atom substrate tower beginning at \(V_1\)

\[
\boxed{\text{YES completely}.}
\]

The unique first-appearance ranks are:

\[
1,2,\ldots,N.
\]

Therefore the old birth-rank shell coordinate can be derived exactly, but only after the foundation includes the pre-Hamilton atom-growth filtration or an equivalent ordered seed.

---

# 316. Computational certification

RAW-11 certified:

- atom-orbit and automorphism counts for multiple:
  \[
  N
  \]
  and seed sizes;
- exact seed-order ambiguity witnesses;
- invariance of the tied-seed stage observable;
- universal Johnson drift for the canonical stage observable;
- exact stationary variance;
- changed shell curvature under the tied-seed coordinate.

The transport audit covered:

\[
k=3,\ldots,8.
\]

Final result:

\[
\boxed{
66/66
}
\]

strict checks passed.

---

# 317. Foundational decision exposed by RAW-11

The rebuild has reached a genuine modelling fork.

### Minimal HC-only foundation

Begin meaningful state geometry at:

\[
HC_3.
\]

Then accept that the intrinsic history observable is:

\[
H_\beta
\]

with an unresolved/tied three-atom seed.

### Extended graded-substrate foundation

Define distinguishable atom sets:

\[
V_1\subset V_2\subset\cdots
\]

first, and define:

\[
HC_n
\]

when:

\[
n\ge3.
\]

Then unique birth rank is reconstructed naturally.

This is not a cosmetic choice because it changes the exact shell coordinate and its Ollivier curvature.

The decision should therefore be made explicitly before downstream physical interpretation.

---

# 318. Recommended next audit

### EHF-HC-RAW-12 — Pre-Hamilton Substrate Growth Definition Lock

If the extended substrate route is adopted, define and stress-test:

1. \(V_n\) as graded distinguishable atom sets;
2. one-atom completion:
   \[
   V_n\subset V_{n+1};
   \]
3. compatible relabelling covariance;
4. emergence threshold:
   \[
   HC_n\text{ exists for }n\ge3;
   \]
5. whether any admissible-comparison structure exists before \(HC_3\), or whether those layers contain atoms only;
6. exact status of cardinality \(n\) as birth-rank coordinate;
7. how HC all-slot completion sits over the atom filtration.

Only after that definition lock should the historical unique-rank shell observable be treated as fully reconstructed.


---

# 319. EHF-HC-RAW-12 — Pre-Hamilton Substrate Growth Definition Lock

## 319.1 Purpose

RAW-11 exposed a genuine foundational fork.

The historical Johnson observable

\[
h(S)=\sum_{i\in S}i
\]

can be interpreted as a first-appearance-rank observable only if the framework carries enough cross-layer structure to distinguish the successive arrivals:

\[
1,2,3,\ldots.
\]

A Hamilton-cycle tower beginning at \(HC_3\) is insufficient because its three seed labels remain \(S_3\)-symmetric.

RAW-12 therefore asks:

> **What is the smallest graded substrate structure that supports unique first-appearance rank while adding no premature Hamilton-cycle, move, metric, probability, or physical structure?**

The preferred conditional definition is a singleton atom filtration beginning at \(V_1\).

The crucial qualification is:

\[
\boxed{
\text{the filtration is additional primitive growth data, not a theorem of static HC geometry}.
}
\]

---

# 320. Static foundation versus graded growth enrichment

To avoid retrofitting chronology into a static object, separate two layers.

## Static HC foundation

At a fixed size \(n\), one may begin with a finite set of distinguishable labels:

\[
V_n,
\qquad
|V_n|=n.
\]

Hamilton-cycle states are then defined when \(n\ge3\).

Nothing in a single static \(V_n\) or \(HC_n\) determines:

- which atom appeared first;
- a total order of atoms;
- a growth arrow;
- a time coordinate.

## CBB graded growth enrichment

For the growth programme, add the coherent tower:

\[
\boxed{
V_1
\overset{\iota_1}{\hookrightarrow}
V_2
\overset{\iota_2}{\hookrightarrow}
V_3
\hookrightarrow\cdots
}
\]

subject to:

\[
\boxed{|V_n|=n}
\]

and:

\[
\boxed{
|V_{n+1}\setminus\iota_n(V_n)|=1.
}
\]

Up to tower isomorphism one may identify every \(\iota_n\) with literal inclusion and write:

\[
V_1\subset V_2\subset\cdots.
\]

This is the **pre-Hamilton substrate growth data**.

---

# 321. What exists below \(n=3\)

For:

\[
n=1,2,
\]

RAW-12 introduces only:

1. the finite atom set \(V_n\);
2. atom identity/equality;
3. the inclusion into the next substrate layer.

It does **not** introduce:

- a Hamilton-cycle state;
- an LR move;
- 2-opt adjacency;
- an edge-overlap metric;
- a Johnson sector;
- probabilities;
- amplitudes;
- energy;
- physical time;
- a complete graph of physical pairwise comparability.

Thus the pre-Hamilton layers are deliberately sparse.

The inclusion:

\[
V_n\hookrightarrow V_{n+1}
\]

means only that earlier atoms persist into the next graded set.

---

# 322. No primitive \(K_n\) is required

The HC state sector should continue to be defined directly as undirected cyclic orderings modulo the dihedral action:

\[
HC(V_n)
=
\{\text{cyclic orderings of }V_n\}/D_n.
\]

Equivalent language using Hamilton cycles of the bookkeeping graph \(K_n\) is allowed, but the complete graph is not added as physical or substrate comparison data.

Thus the graded atom tower does not change the earlier RAW distinction:

\[
\boxed{
\text{label set}
\ne
\text{complete physical comparability graph}.
}
\]

---

# 323. Hamilton-cycle onset threshold

For ordinary simple undirected cycles, the HC state sector first exists at:

\[
\boxed{n=3}.
\]

RAW-12 locks:

\[
\boxed{
HC_n=\varnothing
\quad
(n<3)
}
\]

as a bookkeeping convention, while conceptually saying:

> the Hamilton-cycle state sector is instantiated only for \(n\ge3\).

For:

\[
n\ge3,
\]

\[
\boxed{
|HC_n|
=
\frac{(n-1)!}{2}.
}
\]

Hence:

\[
|HC_3|=1.
\]

No artificial one-cycle or two-cycle is introduced merely to make the growth formula begin earlier.

---

# 324. Substrate growth and HC-state growth are different structures

The atom tower exists for:

\[
n=1,2,3,\ldots.
\]

The HC state-growth map exists only for:

\[
n\ge3.
\]

Let:

\[
x_{n+1}
\]

be the unique new atom:

\[
x_{n+1}
\in
V_{n+1}\setminus V_n.
\]

For:

\[
C\in HC_n
\]

and:

\[
e=\{u,v\}\in E(C),
\]

define:

\[
\Gamma_n(C,e)
\]

by replacing the cycle edge:

\[
\{u,v\}
\]

with:

\[
\{u,x_{n+1}\},
\qquad
\{x_{n+1},v\}.
\]

Then:

\[
\boxed{
\Gamma_n:
\{(C,e):C\in HC_n,\ e\in E(C)\}
\overset{\sim}{\longrightarrow}
HC_{n+1}
}
\]

is a bijection for:

\[
n\ge3.
\]

Deleting \(x_{n+1}\) gives its exact inverse.

So:

\[
\boxed{
\text{atom growth begins at }1,
\qquad
\text{HC all-slot growth begins at }3.
}
\]

There is no all-slot parent for the unique \(HC_3\) state.

---

# 325. Exact all-slot count

Every:

\[
C\in HC_n
\]

has exactly:

\[
n
\]

cycle edges.

Therefore the source of \(\Gamma_n\) has size:

\[
n|HC_n|.
\]

Since:

\[
|HC_n|
=
\frac{(n-1)!}{2},
\]

\[
n|HC_n|
=
\frac{n!}{2}
=
|HC_{n+1}|.
\]

Thus:

\[
\boxed{
n|HC_n|
=
|HC_{n+1}|
}
\]

for every:

\[
n\ge3.
\]

RAW-12 exhaustively re-certified:

\[
3\to4,
\ 4\to5,
\ 5\to6,
\ 6\to7,
\ 7\to8
\]

with:

- complete coverage;
- zero duplicate children;
- exact deletion inverse.

---

# 326. First-appearance stage

For a finite terminal layer \(V_N\), define:

\[
\boxed{
\beta_N(v)
=
\min\{n:v\in V_n\}.
}
\]

Because exactly one atom is added at each stage beginning with:

\[
|V_1|=1,
\]

\[
\beta_N
\]

is a bijection:

\[
\boxed{
\beta_N:V_N\overset{\sim}{\longrightarrow}\{1,\ldots,N\}.
}
\]

Thus every atom has a unique first-appearance stage.

This is the exact structure required by the historical birth-rank coordinate.

---

# 327. Tower isomorphism covariance

Let:

\[
\mathcal V=(V_n,\iota_n)
\]

and:

\[
\mathcal V'=(V_n',\iota_n')
\]

be two singleton towers.

A tower isomorphism is a compatible family of bijections:

\[
\phi_n:V_n\to V_n'
\]

satisfying:

\[
\phi_{n+1}\circ\iota_n
=
\iota_n'\circ\phi_n.
\]

Then:

\[
\boxed{
\beta'(\phi(v))
=
\beta(v).
}
\]

So first-appearance stage is structural data of the graded tower, not of literal symbol names.

---

# 328. Canonical standard tower chart

Define the standard tower:

\[
[1]\subset[2]\subset[3]\subset\cdots,
\]

where:

\[
[n]=\{1,\ldots,n\}.
\]

For every \(V_1\)-seeded singleton tower there is a unique tower isomorphism:

\[
\boxed{
\beta_n:V_n\to[n]
}
\]

sending the atom first appearing at stage \(j\) to:

\[
j.
\]

Therefore, **after the graded tower has been declared**, notation such as:

\[
V_n=[n]
\]

is no longer merely an arbitrary computational labelling.

It is the canonical coordinate chart adapted to first appearance.

This gives a precise repaired interpretation of the historical numerical labels.

---

# 329. Anti-retrofitting theorem: filtration equals total order

The previous result has an important converse.

Fix a terminal \(N\)-element set \(V\).

A maximal singleton filtration:

\[
V_1\subset V_2\subset\cdots\subset V_N=V,
\qquad
|V_n|=n,
\]

is equivalent to a linear order on \(V\).

### From filtration to order

Set:

\[
v_i
=
V_i\setminus V_{i-1},
\]

with:

\[
V_0=\varnothing.
\]

Then:

\[
v_1<v_2<\cdots<v_N.
\]

### From order to filtration

Given:

\[
v_1<v_2<\cdots<v_N,
\]

define:

\[
V_n=\{v_1,\ldots,v_n\}.
\]

The constructions are inverse.

Hence:

\[
\boxed{
\{\text{singleton filtrations on }V\}
\cong
\{\text{linear orders on }V\}.
}
\]

Both sets have size:

\[
\boxed{N!}.
\]

---

# 330. Foundational consequence of the equivalence theorem

The singleton tower does not make total order emerge from a static unordered set.

It **is** total-order information written in growth form.

Therefore the correct statement is:

\[
\boxed{
\text{birth rank is derived from graded growth data}.
}
\]

Do not say:

\[
\boxed{
\text{raw Hamilton cycles force a unique birth order}.
}
\]

They do not.

This is the principal anti-circularity safeguard in RAW-12.

---

# 331. Why the growth formulation may nevertheless be preferable

Although a singleton filtration and total order contain equivalent finite information, their roles in the framework differ.

A bare order says only:

\[
v_1<v_2<\cdots.
\]

A graded tower additionally organizes the dependency of state spaces:

\[
HC(V_3),
HC(V_4),
HC(V_5),
\ldots
\]

and identifies the new atom used by each all-slot growth map.

So for the CBB programme, the tower provides the correct **structural interface** between:

- atom persistence;
- state-space completion;
- deletion;
- reversal-support filtration;
- growth-selected Johnson charts.

The preference for tower language is organizational and modelling-based, not information-theoretic.

---

# 332. Candidate foundations audited

RAW-12 compared five possibilities.

## A. Static \(V_n\) only

Insufficient.

No cross-layer atom identity means no birth history.

## B. HC\(_3\)-seeded singleton filtration

Partially sufficient.

Later birth stages are reconstructed, but the seed retains:

\[
S_3
\]

symmetry.

## C. \(V_1\)-seeded singleton filtration

Sufficient.

Unique first-appearance rank is reconstructed.

This is the preferred **conditional** growth enrichment.

## D. Explicit total order

Also sufficient.

Mathematically equivalent to C on a finite terminal set, but less naturally integrated with HC growth maps.

## E. Literal numeric labels

Rejected as a foundational justification.

Writing:

\[
V_n=\{1,\ldots,n\}
\]

does not by itself prove that the numerals carry structural rank.

That interpretation is licensed only after C or equivalent order data is declared.

---

# 333. Exact relation to the historical Johnson coordinate

At even target layer:

\[
HC_{2k},
\]

RAW-09A uses the newest target atom:

\[
x_{2k}
\]

as the growth-relative anchor.

Removing it leaves the parent atom set:

\[
V_{2k-1}.
\]

Under the canonical tower chart:

\[
\beta:
V_{2k-1}
\overset{\sim}{\longrightarrow}
[2k-1].
\]

Therefore the historical Johnson ground set:

\[
[2k-1]
\]

is recovered exactly.

The historical observable:

\[
h(S)=\sum_{i\in S}i
\]

becomes:

\[
\boxed{
h(S)
=
\sum_{v\in S}\beta(v).
}
\]

So the old \(h\) is now a genuine first-appearance-rank sum **conditional on the \(V_1\)-seeded graded substrate**.

---

# 334. Dependency chain after RAW-12

The rebuilt even branch now has the precise chain:

\[
\boxed{
\text{graded atom tower }V_1\subset V_2\subset\cdots
}
\]

\[
\downarrow
\]

\[
\boxed{
\beta(v)=\text{first-appearance rank}
}
\]

and independently, from:

\[
n\ge3,
\]

\[
\boxed{
HC_n
}
\]

\[
\downarrow
\]

\[
\boxed{
LR3,\ \text{support filtration, all-slot state completion}
}
\]

\[
\downarrow
\]

\[
\boxed{
\text{intrinsic even bipartitions}
}
\]

\[
\downarrow
\]

\[
\boxed{
\text{newest-site growth chart}
}
\]

\[
\downarrow
\]

\[
\boxed{
J(2k-1,k)\ A_1
}
\]

while the rank tower supplies:

\[
\boxed{
h(S)=\sum\beta(v).
}
\]

Only after these two branches meet does the historical Johnson shell transport model appear.

---

# 335. Minimal primitive content

The preferred RAW-12 growth enrichment contains only:

### Atom data

\[
V_n.
\]

### Persistence data

\[
\iota_n:V_n\hookrightarrow V_{n+1}.
\]

### Singleton growth condition

\[
|V_{n+1}\setminus\iota_n(V_n)|=1.
\]

### Cardinality grading

\[
|V_n|=n.
\]

It does not primitive-encode:

- atom adjacency;
- metric;
- cycle state before \(n=3\);
- LR move;
- sector;
- probability;
- amplitude;
- force;
- curvature;
- physical time.

This is the strict definition lock.

---

# 336. Is the grading physical time?

No such claim is made.

The index:

\[
n
\]

is a combinatorial stage/cardinality parameter.

Therefore:

\[
\boxed{
\beta(v)
}
\]

should be called:

- first-appearance stage;
- growth rank;
- birth rank as shorthand.

It should not automatically be called physical time.

Any identification with physical temporal structure would require a separate bridge.

---

# 337. Admissible-comparison status

The graded atom tower is chosen primitive data of the growth framework.

A careful statement is:

> **EHF-HC studies comparison structures built on graded finite sets of distinguishable atoms. In the CBB growth enrichment, atom persistence and one-at-a-time addition are included as primitive cross-layer data. Hamilton-cycle comparison states become available beginning at \(n=3\).**

Avoid saying:

> admissible comparison alone forces the atom tower.

That has not been shown.

Similarly, the finite-set structure does not imply all pairs of atoms are physically comparable.

---

# 338. RAW-12 verdict

The definition lock is:

\[
\boxed{
\mathcal V
=
(V_n,\iota_n)_{n\ge1},
\qquad
|V_n|=n,
\qquad
|V_{n+1}\setminus\iota_n(V_n)|=1.
}
\]

Hamilton-cycle states are instantiated for:

\[
\boxed{n\ge3}.
\]

All-slot HC growth begins at:

\[
\boxed{3\to4}.
\]

First-appearance rank:

\[
\boxed{
\beta(v)=\min\{n:v\in V_n\}
}
\]

is a canonical tower observable and, with a \(V_1\) seed, is injective.

However:

\[
\boxed{
\text{a singleton tower is equivalent to total-order data}.
}
\]

Therefore the unique birth order belongs to the chosen graded growth enrichment, not to static raw HC geometry.

This is the preferred definition because it makes the growth assumptions explicit rather than hiding them in numeric labels.

---

# 339. Computational certification

RAW-12 checked:

- HC state counts for:
  \[
  n=1,\ldots,7;
  \]
- first nonempty HC layer at:
  \[
  n=3;
  \]
- complete all-slot growth:
  \[
  3\to4,\ldots,7\to8;
  \]
- zero duplicate growth children;
- exact deletion inverse;
- singleton-filtration/linear-order count equivalence through:
  \[
  N=10;
  \]
- exact recovery of historical Johnson parent rank sets through:
  \[
  k=10.
  \]

Final result:

\[
\boxed{
59/59
}
\]

strict checks passed.

---

# 340. Recommended status in the overall framework

The clean architecture is now:

## EHF static comparison foundation

Studies:

\[
V_n,
\ HC_n,
\ \text{raw comparison geometry}
\]

at fixed \(n\).

## CBB graded growth enrichment

Adds:

\[
\boxed{
V_1\subset V_2\subset\cdots
}
\]

as chosen primitive growth data.

This produces:

- first-appearance rank;
- canonical newest-site identities;
- coherent all-slot HC completion;
- the historical rank chart needed by Johnson shell observables.

This separation prevents chronology from being silently inserted into the static HC object.

---

# 341. Immediate next question

With the substrate definition now locked, the next natural audit is:

### EHF-HC-RAW-13 — Graded HC Compatibility / Naturality Audit

Prove that every previously certified raw construction is natural with respect to the newly locked atom tower:

- dihedral HC quotient;
- raw overlap;
- reversal-support orbitals;
- LR3;
- deletion/support filtration;
- intrinsic bipartitions;
- growth-selected Johnson \(A_1\);
- first-appearance rank chart.

The purpose would be to verify that RAW-12 changes the **dependency bookkeeping** without changing or contradicting the already certified fixed-layer mathematics.


---

# 342. EHF-HC-RAW-13 — Graded HC Compatibility / Naturality Audit

## 342.1 Purpose

RAW-12 added a new foundational distinction:

- static fixed-\(n\) Hamilton-cycle comparison geometry;
- graded one-atom substrate growth.

That addition changes the symmetry bookkeeping.

At a fixed layer:

\[
HC_n
\]

still has full relabelling covariance under:

\[
S_n.
\]

But a chosen singleton tower:

\[
V_1\subset V_2\subset\cdots\subset V_N
\]

has a unique first-appearance stage for every atom and therefore has trivial atom-level self-automorphism.

RAW-13 asks whether these facts are compatible and whether all previously certified constructions commute correctly with isomorphisms of graded towers.

The answer is:

\[
\boxed{\textbf{yes}.}
\]

No contradiction was found.

The tower changes dependency and symmetry status, but not the earlier combinatorial theorems.

---

# 343. Static covariance versus tower symmetry

The following statements must be distinguished.

## Static fixed-layer covariance

For any bijection:

\[
\phi:V_n\to V_n',
\]

relabel every atom in every Hamilton-cycle state.

Then:

\[
\boxed{
HC(\phi):HC(V_n)\to HC(V_n')
}
\]

is a bijection.

Thus the static Hamilton-cycle object is fully relabelling-covariant.

If:

\[
V_n=V_n',
\]

then:

\[
S_n
\]

acts as the usual fixed-layer relabelling symmetry.

## Chosen-tower self-symmetry

For a \(V_1\)-seeded singleton filtration:

\[
V_1\subset V_2\subset\cdots\subset V_N,
\]

each atom has a unique first-appearance stage.

Any automorphism preserving every filtration level must fix every atom.

Therefore:

\[
\boxed{
\operatorname{Aut}_{\rm atom}(\mathcal V_N)=\{e\}.
}
\]

These statements are not inconsistent.

The second object carries strictly more structure than the first.

---

# 344. Tower isomorphisms

Let:

\[
\mathcal V=(V_n,\iota_n)
\]

and:

\[
\mathcal V'=(V_n',\iota_n')
\]

be singleton towers.

A tower isomorphism is a compatible family:

\[
\phi_n:V_n\to V_n'
\]

such that:

\[
\boxed{
\phi_{n+1}\circ\iota_n
=
\iota_n'\circ\phi_n.
}
\]

Equivalently, the atom born at stage \(j\) is mapped to the atom born at stage \(j\).

Naturality means that every derived HC construction commutes with these maps.

This is the correct symmetry notion once growth history is retained.

---

# 345. HC-state naturality

A Hamilton-cycle state is an undirected cyclic ordering modulo the dihedral action.

Relabelling every atom by:

\[
\phi_n
\]

does not alter:

- cyclic incidence;
- degree-two structure;
- dihedral equivalence.

Therefore:

\[
\boxed{
HC(\phi_n)
}
\]

is well defined and bijective.

RAW-13 directly checked this on complete HC state sets through:

\[
n=7
\]

under multiple nontrivial relabellings.

Thus RAW-12's canonical growth chart does not modify the raw HC state definition.

---

# 346. Raw overlap naturality

For:

\[
C,D\in HC(V_n),
\]

define:

\[
o(C,D)=|E(C)\cap E(D)|.
\]

Since a bijection maps unordered edges bijectively:

\[
E(\phi C)=\phi(E(C)),
\]

we have:

\[
\boxed{
o(\phi C,\phi D)=o(C,D).
}
\]

Hence:

\[
d_E(C,D)=n-o(C,D)
\]

is also preserved.

Likewise the common-edge graph is carried isomorphically to the relabelled common-edge graph.

Therefore its component/path-size data are natural.

This includes the intrinsic pair data used in RAW-03 and RAW-04B.

---

# 347. Reversal-support naturality

Let:

\[
D=R_{s,\ell}(C)
\]

be obtained by reversing a circular block of length:

\[
\ell.
\]

Relabelling changes only the atom names, not the cyclic positions.

Therefore:

\[
\boxed{
\phi(R_{s,\ell}(C))
=
R_{s,\ell}(\phi C).
}
\]

Hence every reversal-support relation:

\[
LR_\ell
\]

is natural.

In particular:

\[
\boxed{
C\sim_{LR3}D
\iff
\phi C\sim_{LR3}\phi D.
}
\]

The intrinsic common-path support:

\[
\{\ell,n-\ell\}
\]

is preserved as well.

Thus the entire RAW-04B/05A reversal-support classification survives unchanged.

---

# 348. Intrinsic bipartition naturality

For even:

\[
n=2m,
\]

every Hamilton cycle is bipartite.

Let:

\[
\Pi_{\rm intr}(C)
=
\{A_C,B_C\}.
\]

Relabelling gives:

\[
\boxed{
\Pi_{\rm intr}(\phi C)
=
\{\phi(A_C),\phi(B_C)\}.
}
\]

Therefore:

- the bipartition sector relation is natural;
- LR odd/even preservation status is natural;
- even LR3 components remain intrinsic bipartition fibres under every relabelling.

The sector construction does not depend on the tower chart.

---

# 349. All-slot growth naturality

Let:

\[
x_{n+1}
\]

be the new atom in:

\[
V_{n+1}\setminus V_n.
\]

For:

\[
C\in HC_n
\]

and:

\[
e\in E(C),
\]

let:

\[
\Gamma_n(C,e)
\]

insert \(x_{n+1}\) into \(e\).

For a tower isomorphism:

\[
\phi,
\]

the new atom maps to:

\[
x_{n+1}'=\phi_{n+1}(x_{n+1}),
\]

and the edge maps to:

\[
\phi_n(e).
\]

Then:

\[
\boxed{
HC(\phi_{n+1})
\big(
\Gamma_n(C,e)
\big)
=
\Gamma_n'
\big(
HC(\phi_n)(C),
\phi_n(e)
\big).
}
\]

Thus the insertion square commutes.

Symbolically:

\[
\begin{array}{ccc}
HC_n\times E(C) & \xrightarrow{\Gamma_n} & HC_{n+1}\\
\downarrow \phi_n && \downarrow \phi_{n+1}\\
HC_n'\times E(\phi C) & \xrightarrow{\Gamma_n'} & HC_{n+1}'
\end{array}
\]

commutes.

RAW-13 certified this exhaustively/sampled through target size:

\[
N=8.
\]

---

# 350. Deletion naturality

Let:

\[
\pi_{x_{n+1}}
:
HC_{n+1}\to HC_n
\]

delete the newest atom and restore its two neighbours as one edge.

Then:

\[
\boxed{
HC(\phi_n)
\circ
\pi_{x_{n+1}}
=
\pi_{x_{n+1}'}
\circ
HC(\phi_{n+1}).
}
\]

So the deletion square also commutes.

This is the exact compatibility required by:

- RAW-06 growth analysis;
- RAW-07 support filtration;
- RAW-09A horizontal/vertical LR2 classification.

---

# 351. Support-filtration naturality

Take a target reversal pair:

\[
(C,D)\in LR_\ell^{(n+1)}.
\]

Delete the newest atom:

\[
(\pi C,\pi D).
\]

RAW-07 showed that its support lies in:

\[
LR_\ell^{(n)}
\cup
LR_{\ell-1}^{(n)}
\]

with the appropriate half-cycle and identity boundary cases.

RAW-13 verifies that tower relabelling commutes with this projection.

Hence the diagram:

\[
LR_\ell^{(n+1)}
\longrightarrow
LR_\ell^{(n)}
\cup
LR_{\ell-1}^{(n)}
\]

is natural with respect to tower isomorphisms.

Therefore the reversal-support filtration is genuinely graded rather than an artifact of the canonical numeric chart.

---

# 352. First-appearance rank naturality

Let:

\[
\beta(v)
=
\min\{n:v\in V_n\}.
\]

For a tower isomorphism:

\[
\phi,
\]

compatibility of the filtration implies:

\[
\boxed{
\beta'(\phi(v))
=
\beta(v).
}
\]

Thus:

\[
\beta
\]

is a tower-natural scalar.

It is not a static-layer invariant if the tower structure is held fixed and one arbitrarily permutes terminal atom names without relabelling the tower.

This distinction resolves the apparent tension between:

- full \(S_n\) covariance of static HC geometry;
- unique birth ranks in a chosen singleton tower.

---

# 353. Newest-site Johnson chart naturality

At even target size:

\[
N=2m,
\]

let:

\[
x_N
\]

be the newest atom.

The intrinsic sector:

\[
P=\{A,A^c\}
\]

is charted by selecting the side containing \(x_N\).

Using the historical \(m\)-subset convention on the parent labels gives a subset:

\[
S(P)\subset V_{N-1},
\qquad
|S(P)|=m.
\]

Now apply a tower isomorphism:

\[
\phi.
\]

The target chart gives:

\[
S'(\phi P)
\subset V_{N-1}'.
\]

Applying the target first-appearance rank:

\[
\beta'
\]

recovers exactly the same rank subset:

\[
\boxed{
\beta'(S'(\phi P))
=
\beta(S(P)).
}
\]

Thus the Johnson chart is natural **relative to the graded tower**.

Literal atom names disappear after passing to first-appearance coordinates.

---

# 354. Horizontal LR2 selector naturality

RAW-09A classified target LR2 edges using newest-site deletion.

For:

\[
C\sim_{LR2}D,
\]

define:

### Horizontal

\[
\pi_x(C)\ne\pi_x(D).
\]

### Vertical

\[
\pi_x(C)=\pi_x(D).
\]

Since deletion commutes with tower isomorphism:

\[
\boxed{
\text{horizontal/vertical status is natural}.
}
\]

The newest-site Johnson chart then gives:

\[
\boxed{
\text{horizontal}
\iff
d_J=1,
}
\]

and:

\[
\boxed{
\text{vertical}
\iff
d_J=m-1.
}
\]

RAW-13 verified that these Johnson distances are unchanged after arbitrary tested tower relabellings and subsequent conversion back to birth-rank coordinates.

Therefore:

\[
\boxed{
LR2_{\rm horizontal}
\to
A_1
}
\]

is a natural graded construction.

---

# 355. Naturality hierarchy

The rebuilt objects now fall into three classes.

## Static-natural

Defined without growth history and covariant under arbitrary atom bijections:

- \(HC_n\);
- raw overlap;
- common-path pair geometry;
- \(LR_\ell\);
- LR3;
- intrinsic even bipartition.

## Graded-natural

Require the tower but commute with tower isomorphisms:

- newest atom;
- insertion/deletion;
- support filtration across layers;
- first-appearance rank \(\beta\).

## Graded/chart-natural

Require the tower and a derived coordinate representation:

- newest-site Johnson subset chart;
- historical rank subset \([2k-1]\);
- horizontal \(LR2\to A_1\);
- birth-rank observable \(h\).

This vocabulary should replace the looser use of “intrinsic” for all three situations.

---

# 356. No symmetry contradiction

A common possible confusion is:

> If the graded tower has trivial automorphism, have we destroyed the \(S_n\) symmetry that supported the HC theorems?

No.

The \(S_n\) action remains the covariance group of the **static fixed-layer construction**.

Adding a particular history selects one structured object from among many isomorphic towers.

The correct analogy is:

\[
\boxed{
\text{covariance of a construction}
\ne
\text{automorphism group of one structured instance}.
}
\]

All fixed-layer formulas remain independent of which tower chart is used.

---

# 357. RAW-12 does not change earlier HC counts or theorems

RAW-13 found no change to:

- \(|HC_n|=(n-1)!/2\);
- incidence neutrality;
- raw overlap;
- nearest-shell 2-opt characterization;
- reversal-support decomposition;
- LR3 parity theorem;
- even LR3 component theorem;
- all-slot state completion;
- reversal-support deletion filtration;
- intrinsic bipartition sector counts;
- weighted Johnson association operator;
- growth-selected \(A_1\).

RAW-12 therefore changes:

\[
\boxed{
\text{dependency bookkeeping and history status},
}
\]

not:

\[
\boxed{
\text{certified fixed-layer combinatorics}.
}
\]

---

# 358. Commuting dependency diagram

The current architecture can be summarized as:

\[
\begin{array}{ccccc}
V_n
&\longrightarrow&
HC_n
&\longrightarrow&
\text{raw pair geometry}\\[1mm]
\downarrow
&&
\downarrow
&&
\downarrow\\[1mm]
V_{n+1}
&\longrightarrow&
HC_{n+1}
&\longrightarrow&
\text{raw pair geometry}
\end{array}
\]

where:

- the left vertical arrow is atom inclusion;
- the middle vertical structure is all-slot completion/deletion;
- the right vertical structure is reversal-support filtration.

For even layers an additional branch is:

\[
HC_{2m}
\to
\mathcal B_m
\to
\text{newest-site Johnson chart}
\to
A_1,
\]

while independently:

\[
V_1\subset\cdots\subset V_{2m-1}
\to
\beta
\to
h.
\]

Every audited square commutes under tower isomorphism.

---

# 359. Exact status of the word “natural”

RAW-13 uses “natural” in the structural sense:

> A construction is natural if applying a compatible atom relabelling before the construction gives the same result as applying the construction first and relabelling the output.

This is essentially functorial/equivariant behaviour.

No category-theoretic machinery is required for the present proofs, though the architecture can be formalized categorically later.

Avoid reading “natural” as:

- physically necessary;
- uniquely selected by nature;
- probabilistically preferred.

It is a covariance statement.

---

# 360. Computational certification

RAW-13 used multiple deterministic and seeded-random tower isomorphisms.

It checked:

### Fixed layers

Through:

\[
n=7,
\]

for:

- HC state relabelling;
- raw overlap;
- common-path data;
- all effective reversal supports;
- LR3;
- even intrinsic bipartitions.

### Cross-layer growth

Through target:

\[
N=8,
\]

for:

- insertion commuting squares;
- deletion commuting squares;
- projected support type;
- first-appearance rank covariance.

### Even sector / Johnson bridge

For:

\[
N=4,6,8,
\]

for:

- intrinsic sector relabelling;
- newest-anchor chart covariance;
- birth-rank subset recovery;
- horizontal/vertical LR2 status;
- Johnson \(A_1/A_{m-1}\) distance preservation.

Final result:

\[
\boxed{
317/317
}
\]

strict checks passed.

---

# 361. RAW-13 verdict

The graded substrate introduced in RAW-12 is compatible with the previously certified HC-RAW structure.

The exact status is:

\[
\boxed{
\text{static HC constructions remain fully relabelling-covariant},
}
\]

while:

\[
\boxed{
\text{growth-history constructions are natural under tower isomorphisms}.
}
\]

The tower does not alter raw HC mathematics.

It supplies additional cross-layer structure that:

- selects the newest atom;
- reconstructs first-appearance rank;
- makes deletion/growth coherent;
- turns the historical Johnson rank chart into a graded coordinate.

Thus RAW-12 is a foundational enrichment rather than a revision of the earlier fixed-layer theorems.

---

# 362. Recommended next step

The foundation is now sufficiently coherent for a consolidation audit.

### EHF-HC-RAW-14 — Primitive Data / Redundancy / Dependency-Minimality Audit

Candidate questions:

1. Which objects are genuinely primitive?
2. Which are definitional conveniences?
3. Which are exact consequences?
4. Is singleton atom growth stronger than required by any downstream theorem?
5. Which historical structures can be removed without losing:
   - LR3 selection;
   - support filtration;
   - Johnson \(A_1\);
   - birth-rank transport?
6. Can the entire current foundation be represented as a dependency DAG with no circular edges?

This would be a useful final foundation check before either opening the queued graph-emergence programme or returning to downstream physics bridges.


---

# 363. EHF-HC-RAW-14 — Primitive Data / Redundancy / Dependency-Minimality Audit

## 363.1 Purpose

RAW-01 through RAW-13 established a large amount of exact structure.

That success creates a danger:

> once many useful objects exist, it becomes easy to forget which ones were actually assumed and which ones were derived.

RAW-14 therefore treats the rebuilt framework as a dependency problem.

For each object it asks:

1. Is it primitive data?
2. Is it a state-space ansatz?
3. Is it a modelling choice?
4. Is it derived?
5. Is it merely a coordinate/chart?
6. Is it an optional transport or metric convention?
7. What fails if it is removed?

The goal is not to minimize the number of words in the foundation.

The goal is to eliminate **logical redundancy and circular dependence**.

---

# 364. There is no single universal primitive package

The first conclusion is methodological.

Different questions require different amounts of structure.

A static fixed-\(n\) HC theorem does not require growth history.

A graded growth theorem does not require unique birth ranks.

Johnson \(A_1\) does not require probabilities.

Ollivier shell curvature requires substantially more analytical structure than raw HC geometry.

Therefore RAW-14 replaces the idea of one monolithic foundation with a nested family of dependency packages.

---

# 365. Static structural core

The static fixed-layer package requires only:

### Primitive/ansatz S1 — finite atoms

A finite set:

\[
V_n.
\]

### Primitive/ansatz S2 — Hamilton-cycle state construction

For:

\[
n\ge3,
\]

take:

\[
\boxed{
HC(V_n)
=
\{\text{undirected cyclic orderings of }V_n\}/D_n.
}
\]

From this pair alone one derives:

- cycle edge incidence;
- raw overlap;
- edge symmetric-difference distance;
- the nearest nontrivial shell;
- all reversal-support classes;
- the structural LR3 class;
- intrinsic even bipartitions;
- the intrinsic even sector space.

Thus the static structural core is:

\[
\boxed{
\text{finite atoms}
+
\text{HC cyclic-state ansatz}.
}
\]

No growth history is required.

---

# 366. Edge incidence is not primitive

Given a cyclic state:

\[
C=(c_0,\ldots,c_{n-1}),
\]

its unordered edge set is:

\[
\boxed{
E(C)
=
\{
\{c_i,c_{i+1}\}
:
i\in\mathbb Z_n
\}.
}
\]

Therefore:

\[
E(C)
\]

contains no additional information beyond the HC state.

It should remain derived.

---

# 367. Raw overlap and raw distance are not primitive

Once:

\[
E(C)
\]

and:

\[
E(D)
\]

are known,

\[
o(C,D)
=
|E(C)\cap E(D)|
\]

and:

\[
d_E(C,D)
=
\frac12|E(C)\triangle E(D)|
=
n-o(C,D)
\]

are exact derived observables.

Thus neither overlap nor distance should appear in the primitive data.

They are canonical comparisons built from state incidence.

---

# 368. \(K_n\) remains unnecessary

The bookkeeping phrase:

> Hamilton cycles of \(K_n\)

is mathematically equivalent to the cyclic-order definition.

But RAW-14 confirms that no primitive complete graph is needed.

The foundation does not require:

\[
\boxed{
K_n
}
\]

as substrate geometry.

This protects the distinction:

\[
\text{all possible bookkeeping edges}
\ne
\text{all physically admissible pairwise comparisons}.
\]

---

# 369. 2-opt is derived

RAW-02 established:

\[
\boxed{
d_E(C,D)=2
}
\]

as the nearest possible nonzero raw HC distance.

This shell is exactly the usual 2-opt shell.

Therefore:

\[
\boxed{
2opt
=
\text{nearest nontrivial raw comparison shell}.
}
\]

No separate 2-opt primitive is necessary.

---

# 370. Reversal-support labels are derived pair geometry

RAW-04B showed that a nearest-shell reversal pair has common-path vertex sizes:

\[
\{\ell,n-\ell\}.
\]

Hence the support parameter:

\[
\ell
\]

is intrinsically recoverable from the pair.

Therefore the structural relations:

\[
LR_\ell
\]

need not be inserted as primitive labels.

They are a classification of raw nearest-shell pairs.

In particular:

\[
\boxed{
LR3
}
\]

exists as a structural relation whether or not the framework chooses it as a dynamics/admissibility rule.

This distinction is crucial.

---

# 371. Structural LR3 versus selected LR3

RAW-14 separates:

### Structural LR3

The exact pair relation:

\[
LR3\subset HC_n\times HC_n.
\]

This is derived from raw HC pair geometry.

### Selected LR3

The modelling assertion:

> LR3 is the preferred or admissible same-layer move rule.

This is **not** derived from raw HC alone.

RAW-05B proved the no-go result:

\[
\boxed{
\text{nearest-shell covariance alone does not uniquely select LR3}.
}
\]

Therefore selecting LR3 requires an additional modelling choice.

---

# 372. Two legitimate LR3 packages

There are two logically clean ways to handle selection.

## Direct package

Declare:

\[
\boxed{
LR3
}
\]

to be the chosen admissible move relation.

This is the logically shortest package.

## Principle-based package

Within the audited nearest-shell reversal-orbital candidate class, impose:

- preservation of intrinsic even bipartition;
- strict reversal locality / inclusion minimality.

Then the selected rule is:

\[
\boxed{LR3}.
\]

This package contains more assumptions but gives an explanatory reason for the choice.

Do not include both packages and then count both as necessary primitives.

They are alternatives.

---

# 373. The graded structural core is leaner than RAW-12's full tower

For the coherent HC growth programme, the required growth data are:

\[
\boxed{
V_3
\subset
V_4
\subset
V_5
\subset\cdots
}
\]

with one persistent new atom added per stage.

Call this the **HC\(_3\)-seeded singleton tower**.

Together with the HC state-space ansatz, it is sufficient to derive:

- newest-atom deletion;
- all-slot insertion;
- exact growth bijection;
- reversal-support filtration;
- intrinsic even sectors;
- newest-site Johnson charts;
- horizontal/vertical LR2 classification;
- ordinary Johnson \(A_1\).

Thus:

\[
\boxed{
\text{HC growth}
+
\text{Johnson }A_1
}
\]

do not require:

\[
V_1
\quad\text{or}\quad
V_2.
\]

This is one of the main minimization results of RAW-14.

---

# 374. All-slot growth is not primitive

Given:

1. a persistent singleton tower;
2. a target newest atom:
   \[
   x_{n+1};
   \]
3. the HC cyclic-state definition;

deleting \(x_{n+1}\) from an \((n+1)\)-cycle is canonical.

Its inverse consists exactly of inserting \(x_{n+1}\) into one parent cycle edge.

Therefore the all-slot relation:

\[
HC_n\times\{\text{cycle edges}\}
\cong
HC_{n+1}
\]

is derived.

The phrase:

> all-slot growth principle

may remain useful conceptually, but the actual map does not need to be independently primitive once the tower and HC state construction are fixed.

---

# 375. Support filtration is derived

Once:

- reversal-support classes;
- newest-site deletion;

exist, RAW-07's law:

\[
LR_\ell^{(N)}
\to
LR_\ell^{(N-1)}
\cup
LR_{\ell-1}^{(N-1)}
\]

is a theorem.

No separate filtration primitive is required.

The filtration is a property of deletion acting on structural reversal classes.

---

# 376. Intrinsic sectors are derived

For even:

\[
n=2m,
\]

the graph underlying each HC state is an even cycle and therefore has a unique bipartition up to block swap.

Thus:

\[
\Pi_{\rm intr}(C)
\]

is derived.

The sector space:

\[
\mathcal B_m
\]

is likewise derived.

No parity label or sector identifier needs to be primitive.

---

# 377. Johnson vertex space is derived

RAW-08B showed:

\[
\mathcal B_m
\]

is the intrinsic unordered equal-bipartition space.

A distinguished newest site gives a canonical chart into a fixed-size subset space.

Therefore the Johnson vertex set is:

\[
\boxed{
\text{derived from intrinsic sectors + growth anchor}.
}
\]

It should not be inserted as a primitive target graph.

This is important for the queued graph-emergence branch.

---

# 378. Johnson \(A_1\) is derived

RAW-09A established:

\[
\boxed{
A_1
=
\text{sector image of horizontal/parent-changing target }LR2.
}
\]

Since structural:

\[
LR2
\]

already exists inside the raw nearest shell, and horizontal status is defined by newest-site deletion,

\[
A_1
\]

requires no independent adjacency axiom.

Therefore:

\[
\boxed{
\text{Johnson }A_1
}
\]

is derived from:

- HC pair geometry;
- one-site growth structure;
- intrinsic sectors.

It does not require LR3 to be selected as the dynamics.

---

# 379. LR3 selection is not required for Johnson emergence

This point deserves explicit separation.

The chain:

\[
HC
\to
\text{sectors}
\to
LR2_{\rm horizontal}
\to
A_1
\]

is structural.

It exists whether or not:

\[
LR3
\]

has been selected as the admissible same-layer rule.

The separate relation:

\[
LR3
\overset{\text{deletion}}{\longrightarrow}
LR2
\]

explains how the selected LR3 layer exposes the lower-support channel under growth.

But Johnson \(A_1\) itself does not logically depend on that selection.

Thus:

\[
\boxed{
\text{Johnson emergence}
\ne
\text{LR3-selection theorem}.
}
\]

They are related branches of the same substrate, not one axiom chain.

---

# 380. Pre-Hamilton \(V_1,V_2\) are optional rank refinement

RAW-12 introduced:

\[
V_1\subset V_2\subset V_3\subset\cdots
\]

to reconstruct unique historical birth ranks.

RAW-14 shows precisely what that extension is needed for.

Removing:

\[
V_1,V_2
\]

does **not** destroy:

- static HC geometry;
- LR support;
- LR3;
- all-slot HC growth from \(3\to4\) onward;
- support filtration;
- intrinsic sectors;
- Johnson vertex emergence;
- Johnson \(A_1\).

It destroys only the unique resolution of the three HC\(_3\) seed atoms and therefore the exact historical weight system:

\[
1,2,3,4,\ldots.
\]

Thus:

\[
\boxed{
V_1,V_2
}
\]

belong in a **rank-refined growth extension**, not in the logically minimal HC-growth core.

---

# 381. Unique birth rank is an extension output

If the singleton tower is extended to:

\[
V_1,
\]

then:

\[
\beta(v)
=
\min\{n:v\in V_n\}
\]

is injective.

Hence:

\[
\boxed{
\beta:V_N\to[N].
}
\]

But \(\beta\) should remain derived.

It is not separate primitive data.

The primitive content is the rank-refined tower itself.

---

# 382. Cardinality grading is partly redundant

If one declares:

\[
|V_1|=1
\]

and every inclusion adds exactly one new atom:

\[
|V_{n+1}\setminus V_n|=1,
\]

then induction gives:

\[
\boxed{
|V_n|=n.
}
\]

Therefore it is unnecessary to list both:

- singleton increment;
- \(|V_n|=n\);

as logically independent axioms.

One may use \(|V_n|=n\) as notation/normalization of the stage index, but it should not be counted twice in the primitive ledger.

---

# 383. Numeric labels are coordinate charts

At a fixed static layer, notation:

\[
V_n=[n]
\]

is merely a convenient chart.

In the rank-refined tower, first appearance gives a canonical chart:

\[
\beta:V_n\to[n].
\]

Thus literal numbers are never independent primitive atom properties.

They are either:

- arbitrary static coordinates;
- derived growth coordinates.

---

# 384. Uniform Johnson probabilities are optional

The structural graph:

\[
J(2k-1,k)
\]

does not determine a unique stochastic process merely because it is regular.

The historical transport branch chooses:

\[
\boxed{
P(S,T)
=
\frac1{k(k-1)}
}
\]

for every:

\[
A_1\text{ neighbour }T.
\]

This is a natural neutrality convention, but it remains an analytical choice.

Removing it leaves:

- the Johnson graph;
- its adjacency algebra;
- spectra;
- structural sector relations;

fully intact.

It removes only results whose definitions use a random walk expectation.

---

# 385. Uniform shell averaging is optional

RAW-10A and RAW-10D proved that:

\[
h
\]

is not strongly lumpable.

Therefore the shell kernel:

\[
K(h,h')
\]

requires an explicit conditional averaging prescription.

The historical choice is uniform averaging over states in shell \(h\).

This may equivalently be interpreted as conditioning the uniform stationary ensemble.

But it is not implied by strong Markov projection.

Thus:

\[
\boxed{
\text{uniform shell averaging}
}
\]

belongs to the analytical extension, not the structural foundation.

---

# 386. The shell line metric is optional

The Ollivier audit chooses:

\[
d(h,h')
=
|h-h'|.
\]

This metric is natural for the integer birth-rank coordinate, but it is still a declared metric on the coarse observable space.

Removing it does not alter:

- HC geometry;
- Johnson geometry;
- transport transition probabilities.

It removes only that particular transport-curvature calculation.

Therefore:

\[
\boxed{
\text{shell line metric}
}
\]

is an optional metric convention.

---

# 387. Minimal package table

RAW-14 identifies the following sufficient and deletion-minimal packages for the stated output bundles.

| Package | Primitive / chosen inputs | Main derived outputs |
|---|---|---|
| Static structural core | finite \(V_n\) + HC cyclic-state ansatz | overlap, 2-opt, \(LR_\ell\), structural LR3, bipartitions |
| Graded structural core | HC state ansatz + HC\(_3\)-seeded singleton tower | all-slot growth, support filtration, Johnson \(A_1\) |
| LR3 direct model | graded core + direct LR3 choice | selected LR3 model |
| LR3 principle model | graded core + audited preservation/locality principles | selected LR3 model |
| Rank-refined extension | graded core + extension to \(V_1,V_2\) | unique \(\beta\), historical \(h\) |
| Johnson transport | rank-refined extension + uniform \(A_1\) weighting | exact stochastic drift/diffusion |
| Shell-curvature extension | Johnson transport + shell averaging + line metric | historical shell Ollivier curvature |

Each package was deletion-tested against its target bundle.

---

# 388. Logical minimality versus explanatory minimality

RAW-14 exposes an important distinction.

The logically shortest way to obtain a selected move rule is:

\[
\boxed{
\text{declare LR3 selected}.
}
\]

But that does not explain why LR3 is chosen.

The principle-based route adds assumptions but provides explanatory structure:

\[
\text{even preservation}
+
\text{strict locality/minimality}
\Longrightarrow
LR3
\]

within the audited reversal-orbital candidate class.

Therefore:

\[
\boxed{
\text{logical minimality}
\ne
\text{explanatory minimality}.
}
\]

Both packages should remain available, clearly labelled.

---

# 389. The genuinely primitive choices

After removing redundancies, the HC programme contains only a few genuine modelling choices.

## Static state-space choice

Use undirected cyclic orderings modulo dihedral presentation as the comparison states.

This is not derived from finite atoms alone.

## Graded-growth choice

If studying CBB growth, retain persistent one-at-a-time atom addition.

This is not derived from static HC geometry.

## Move-selection choice

If LR3 is to be interpreted as the admissible same-layer rule, choose it directly or adopt explicit selection principles.

## Transport choice

If a stochastic Johnson model is desired, specify neighbour weighting.

## Coarse metric choice

If shell Ollivier curvature is desired, specify shell averaging and a metric.

Everything else in the current structural spine is derived from these layers.

---

# 390. What is not a primitive anymore

The following should not appear in a minimal primitive list:

- \(K_n\);
- raw overlap;
- \(d_E\);
- 2-opt;
- \(LR_\ell\) labels as external data;
- intrinsic bipartition sectors;
- all-slot insertion as an independent map;
- support filtration;
- Johnson vertex set;
- Johnson \(A_1\);
- birth rank \(\beta\);
- historical \(h\);
- restoring drift;
- Ollivier curvature.

All are derived or convention-dependent.

---

# 391. Acyclic dependency result

RAW-14 encoded the current dependency relations as a directed graph.

The AND-dependency graph is acyclic.

LR3 selection has two explicit alternative parent packages rather than a circular derivation.

Thus no current certified node depends on itself, directly or indirectly.

The rebuilt dependency structure is therefore a genuine DAG.

This is important because several historical narratives had blurred:

- Johnson geometry;
- LR3 selection;
- parity sectors;
- birth rank;

in ways that could sound circular.

The current graph separates them.

---

# 392. Lean structural DAG

The core structural DAG can be written:

\[
\boxed{
\text{finite atoms}
\to
HC_n
}
\]

then:

\[
HC_n
\to
E(C)
\to
\text{raw overlap}
\to
2opt
\to
LR_\ell,
\]

and independently:

\[
HC_{2m}
\to
\Pi_{\rm intr}
\to
\mathcal B_m.
\]

The graded branch adds:

\[
\boxed{
V_3\subset V_4\subset\cdots
}
\]

giving:

\[
\text{newest-site deletion}
\to
\text{all-slot growth},
\]

\[
LR_\ell
+
\text{deletion}
\to
\text{support filtration},
\]

and:

\[
\mathcal B_m
+
\text{newest site}
+
LR2
\to
A_1.
\]

No birth-rank assumption is present in this lean structural branch.

---

# 393. Rank-refined DAG

Only if the historical shell coordinate is desired do we extend:

\[
V_3\supset V_2\supset V_1
\]

in the reverse reading, equivalently:

\[
V_1\subset V_2\subset V_3\subset\cdots.
\]

Then:

\[
\boxed{
\text{rank-refined tower}
\to
\beta
\to
h.
}
\]

This branch meets the Johnson structural branch only at the observable layer.

Therefore the historical shell coordinate is not needed to derive the Johnson graph itself.

---

# 394. Transport DAG

The transport branch is:

\[
A_1
+
\text{uniform neighbour weighting}
\to
\text{Johnson walk}.
\]

Then:

\[
\text{Johnson walk}
+
h
\to
\text{exact drift/diffusion}.
\]

Then:

\[
\text{walk}
+
h
+
\text{uniform shell averaging}
\to
K(h,h').
\]

Finally:

\[
K
+
|h-h'|
\to
\text{shell Ollivier curvature}.
\]

Each extra step is explicitly optional.

---

# 395. RAW-14 deletion results

The deletion audit gives several high-value results.

### Remove HC state ansatz

Almost all HC-derived structure disappears.

Therefore it is genuinely essential.

### Remove HC\(_3\)-seeded tower

Static HC mathematics survives.

But:

- all-slot growth;
- support filtration;
- Johnson \(A_1\);

lose their current graded derivation.

### Remove \(V_1,V_2\) extension

All structural HC-growth and Johnson results survive.

Lost:

- unique birth rank;
- historical \(h\);
- rank-based transport/curvature branch.

### Remove LR3 direct choice

Nothing is lost if the principle-based selection package remains.

### Remove LR3 principles

Nothing is lost if the direct LR3 choice remains.

Thus those are true alternatives.

### Remove uniform \(A_1\) weighting

Structural Johnson \(A_1\) survives.

Stochastic drift and shell-curvature analysis do not.

### Remove shell averaging or line metric

Only the shell-curvature extension is lost.

---

# 396. Recommended foundation architecture

RAW-14 recommends three nested layers.

## Layer A — Static HC structural theory

Primitive/ansatz:

- finite atoms;
- HC cyclic-state construction.

Everything fixed-layer is derived from there.

## Layer B — CBB graded HC growth

Add:

- HC\(_3\)-seeded singleton persistence/growth.

This is sufficient for:

- deletion;
- all-slot completion;
- support filtration;
- Johnson emergence.

## Layer C — Rank-refined history extension

Optionally extend growth down to:

\[
V_1.
\]

This is required only for:

- unique birth rank;
- historical \(h\);
- its particular shell geometry.

Transport and metric conventions sit downstream of Layer C rather than inside the structural foundation.

---

# 397. Consequence for the book / explanatory narrative

A clean conceptual narrative is now possible without pretending every later object was present at the beginning.

One can say:

1. begin with distinguishable atoms;
2. choose cyclic comparison states;
3. derive raw pair geometry;
4. if growth is added, derive coherent deletion/completion;
5. derive sector and Johnson structures;
6. only if cumulative rank history is retained, define birth-rank observables;
7. only if stochastic weighting is chosen, discuss drift/diffusion;
8. only after a coarse metric is chosen, discuss Ollivier curvature.

This ordering mirrors the actual dependency DAG.

---

# 398. RAW-14 verdict

The current HC-RAW programme is substantially less assumption-heavy than its historical presentation suggested.

The minimal structural growth core is:

\[
\boxed{
\text{HC cyclic-state ansatz}
+
\text{HC}_3\text{-seeded singleton atom tower}.
}
\]

From this one obtains:

- raw comparison geometry;
- reversal-support classes;
- deletion/all-slot growth;
- support filtration;
- intrinsic even sectors;
- growth-selected Johnson \(A_1\).

The following are **not** required for that core:

\[
V_1,V_2,
\]

unique birth rank,

\[
h,
\]

uniform random-walk probabilities,

shell averaging,

or the shell line metric.

LR3 exists structurally, but interpreting it as the selected admissible move still requires an explicit modelling choice or a conditional selection-principle package.

This is the current dependency-minimal architecture.

---

# 399. Certification

RAW-14 encoded:

- primitive/derived node statuses;
- dependency edges;
- alternative LR3 selection packages;
- nested sufficient packages;
- package deletion tests;
- primitive deletion impacts;
- redundancy classifications.

The tightened package audit verified:

\[
\boxed{
31/31
}
\]

dependency/minimality checks.

The dependency DAG is acyclic.

---

# 400. Immediate next step

RAW-14 is a natural stopping point for the foundational HC rebuild.

Three queued directions now exist:

### RAW-10F — CDF One-Defect Proof

A theorem-completion side target.

### EHF-GRAPH-EMERG-00 — Definition Lock and Historical Recovery

A separate graph-emergence classification branch.

### Downstream bridge rebuild

Return carefully to OPW / amplituhedron / other physics-facing structures using the dependency-minimal HC core.

Before choosing among them, it would be useful to create one compact **Foundation v1.0 theorem-and-dependency document** containing only the surviving definitions, exact theorems, modelling choices, and open conjectures from RAW-01 through RAW-14.
