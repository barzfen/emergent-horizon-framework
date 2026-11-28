# EHF-HC-RAW — Raw Hamilton-Cycle Comparison Space
## Working Document

**Programme:** Emergent Horizon Framework  
**Branch:** Foundational rebuild / raw Hamilton-cycle substrate  
**Version:** v0.1  
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
=rac{2n}{n-1}.
\]

Hence

\[
\mathbb E[X(X-1)]
=rac{4n}{n-1},
\]

and

\[
\mathbb E[X^2]
=rac{6n}{n-1}.
\]

Thus

\[
\boxed{
\operatorname{Var}(X)
=rac{2n(n-3)}{(n-1)^2}.
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
