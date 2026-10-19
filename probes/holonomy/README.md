# EHF Holonomy Branch

This branch investigates whether nontrivial loop holonomy can arise from EHF's existing primitive structure of admissible comparison and transformation, and whether that structure admits a controlled local-curvature-like scaling limit.

## Start here

A reader should not need the original ChatGPT conversations to follow this branch.

1. [RECUR-BACKGROUND.md](RECUR-BACKGROUND.md) reconstructs the prior observer/recursion results needed by the holonomy work.
2. [HOL-01.md](HOL-01.md) states the original closed-comparison audit and its scientific criteria.
3. [HOL-01A.md](HOL-01A.md) records the negative canonical-transport gate on the cyclic-residue candidate.
4. [HOL-01B.md](HOL-01B.md) records the representation-dependent Wheeler rotation-quotient candidate.
5. [HOL-01C.md](HOL-01C.md) integrates the pre-existing RECUR observer connection and establishes the positive mathematical holonomy classification.
6. [HOL-02.md](HOL-02.md) tests the naive large-`n` continuum interpretation and shows that a fixed observer triangle approaches a 90-degree rather than identity rotation.
7. [HOL-02B.md](HOL-02B.md) audits existing RECUR quantities for an intrinsic shrinking-loop scale and finds none at fixed `n`.
8. [`code/holonomy/recur_holonomy_formula.py`](../../code/holonomy/recur_holonomy_formula.py) reproduces the exact rotation-factor numerics using only the Python standard library.

## Current result in one paragraph

The Wheeler candidates do not supply intrinsic holonomy under the strict HOL-01 criteria. The earlier RECUR observer construction does: conditional observer reconstruction is path dependent, and after attenuation/kernel loss is separated by polar decomposition, a nonidentity orientation-sensitive norm-preserving loop sector remains. In the complete symmetric models its rotation satisfies

\[
\cos\theta_n=\frac{3(n-2)^2-4}{(n-2)^3}.
\]

The same rotation occurs in a perfect-matching control with the same relevant observer-overlap reflection structure. Symmetry breaking generally splits the common angle into orbit-dependent classes. None of this establishes physical spacetime curvature.

## Research discipline

The programme keeps three levels separate:

1. **Mathematical result** — properties proved or measured in an EHF construction.
2. **Geometric analogy** — comparison with established notions such as parallel transport, holonomy, and curvature.
3. **Physical interpretation** — any possible relation to gravity or emergent spacetime. This remains speculative unless independently derived and empirically constrained.

The branch does **not** assume that EHF describes gravity, that spacetime is fundamental, or that an analogy with general relativity establishes physical equivalence.

## Core transport language

For a closed history

\[
\gamma:S_1\to S_2\to\cdots\to S_n\to S_1,
\]

a connection supplies comparison maps whose closed composition is schematically

\[
H(\gamma)=C_{n1}C_{n-1,n}\cdots C_{12}.
\]

A nonidentity `H(gamma)` is meaningful only when the transported datum and edge comparison are independently justified. A state-space cycle by itself is not holonomy.

## Current frontier

HOL-02A shows that the fixed three-observer RECUR loop does not approach identity merely by taking `n` large; instead `theta_n -> pi/2`. HOL-02B then tests graph distance, observer-fibre size, pairwise transport strength, direct-via reconstruction defect, automorphism-orbit type and holonomy-derived scales. None supplies a canonical scalar sequence of shrinking loops in the current fixed-level construction.

The mathematically justified description at this stage is therefore a **discrete observer connection with orbit-classified holonomy**, not a discretized smooth curvature field.

The next candidate source of an intrinsic refinement parameter is EHF growth itself. HOL-03 should test whether the existing `n -> n+1` ancestry/refinement maps intertwine observer transport strongly enough to define descendant loop families and a controlled refinement limit. No geometric length is to be assigned unless it is independently derived.