# EHF-HOL-01 — Closed-Comparison Holonomy Audit

**Status: PROPOSED / NOT YET RUN**

## Question

Do already-existing EHF admissible-comparison structures generate nontrivial path dependence when a transportable local datum is carried around a closed admissible history?

Equivalently, can a closed comparison loop have

\[
H(\gamma)\neq I
\]

without inserting curvature, gravity, spacetime, or a gauge field by hand?

## Motivation

This probe arose from comparing two visualization problems:

- observer-relative local frames in special relativity; and
- the inadequacy of the rubber-sheet/trampoline analogy for general relativity.

A more faithful geometric intuition for GR is that local inertial frames are individually ordinary but cannot, in curved spacetime, always be stitched into one global inertial frame. Parallel transport around a closed loop can exhibit nontrivial holonomy.

EHF should not import that physics as an assumption. Instead, the mathematical analogue can be tested directly because EHF already has histories, cycles, transformations, and admissible comparison as primitive structure.

## Primitive setup

Let the tested EHF sector have states \(S\), admissible directed comparisons or transformations

\[
C_{ij}:S_i\to S_j,
\]

and a transportable local datum \(q_i\) attached to a state or local frame.

For an admissible closed history

\[
\gamma=(S_1,S_2,\ldots,S_n,S_1),
\]

define the composed transport

\[
H(\gamma)=C_{n1}C_{n-1,n}\cdots C_{23}C_{12}.
\]

The action on the transported datum is

\[
q_1' = H(\gamma)q_1.
\]

A loop is **trivial** for the chosen transport if \(q_1'=q_1\) for all admissible \(q_1\). It is **nontrivial** if at least one transported datum changes.

## Critical requirement: transport must not be invented to force holonomy

The first implementation must use an already-motivated EHF object or comparison rule. Candidate transported data include, in order of preference:

1. an existing local signature or orientation already used by the selected EHF sector;
2. a canonical label/frame induced by the admissible comparison itself;
3. an existing observable whose identification between neighbouring states is already defined.

If no canonical transport rule exists, HOL-01 must report **UNDEFINED** rather than manufacture one.

## Initial substrate

Begin with a small, already-audited finite EHF state graph so exhaustive loop enumeration is feasible. Prefer a sector for which:

- states and admissible edges are already reproducible;
- automorphisms/quotients are understood;
- short cycles exist;
- the comparison maps can be defined without new physical assumptions.

The existing constrained cyclic/Wheeler work is a natural first candidate, but substrate selection is part of the audit rather than a fixed physical commitment.

## Audit procedure

### A. Define transport

Specify exactly:

- state space;
- admissible edge set;
- transported datum;
- edge transport map;
- identity criterion.

### B. Enumerate closed loops

For tractable systems enumerate simple directed cycles up to a chosen length \(L\). For larger systems sample loops reproducibly with fixed seeds.

Record loop length, orientation, start state, equivalence class under graph symmetries, and composed map \(H(\gamma)\).

### C. Null tests

Check:

1. zero-length loop gives identity;
2. immediate edge reversal gives identity when the edge maps are genuine inverses;
3. cyclic re-rooting changes only the representation expected from conjugacy, not the invariant classification;
4. relabelling equivalent states does not create apparent holonomy;
5. numerical or canonicalization artefacts do not produce false nonidentity.

### D. Measure nontriviality

At minimum report

\[
f_L=\frac{\#\{\gamma:|\gamma|=L,\ H(\gamma)\neq I\}}{\#\{\gamma:|\gamma|=L\}}.
\]

Where the transport object permits it, also measure a magnitude \(K(\gamma)\), such as permutation distance, orientation defect, matrix norm, phase, or another invariant appropriate to the native EHF object.

### E. Structural dependence

Test whether holonomy depends on:

- loop length;
- orientation reversal;
- local constraint density;
- growth depth;
- odd/even system size;
- component or symmetry sector;
- loop area analogue, if one exists intrinsically.

Do not introduce a geometric 'area' merely to imitate continuum curvature.

## Outcomes

### HOL-01A — Trivial

\[
H(\gamma)=I
\]

for all tested loops. This is a useful negative result: the tested comparison structure is globally integrable for the chosen transport.

### HOL-01B — Nontrivial but representation-dependent

Apparent holonomy disappears after quotienting labels/gauge-like redundancy. Record as an artefact or coordinate effect, not intrinsic curvature.

### HOL-01C — Intrinsic nontrivial holonomy

A loop invariant survives canonicalization and symmetry quotienting. This establishes a discrete path-dependent comparison structure.

It does **not** establish gravity.

## Relation to general relativity

Only after HOL-01C would comparison with geometric curvature be justified. Relevant later questions would include whether small-loop holonomy has a controlled local limit, whether defects compose consistently, and whether an analogue of curvature can be defined without importing continuum geometry.

Any claim of emergent gravity would require substantially more: an effective Lorentzian geometry, equivalence-principle behaviour, suitable dynamics, a continuum/large-scale limit, and quantitative contact with gravitational observations.

## Relation to the radial-history visualization discussion

The motivating visualization showed how observer-local time/spatial directions can make relativistic relations easier to see. That discussion is retained only as provenance. HOL-01 does not assume instantaneous light propagation, a Big-Bang radial embedding, or the physical correctness/novelty of that visualization.

## Pass criterion

HOL-01 passes as a mathematical probe if it produces a reproducible classification of closed comparison loops as intrinsically trivial or nontrivial under a pre-existing, explicitly justified transport rule.

The scientifically strongest result may be either positive or negative.

## Next step

Select the smallest existing EHF sector with a canonical edge transport rule, implement exhaustive short-loop enumeration, and run the null tests before interpreting any nonidentity result.
