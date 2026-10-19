# EHF Holonomy Branch

This branch investigates whether nontrivial loop holonomy can arise from EHF's existing primitive structure of admissible comparison and transformation, and whether that structure admits a controlled local-curvature-like scaling limit.

## Start here

A reader should not need the original ChatGPT conversations to follow this branch.

1. [RECUR-BACKGROUND.md](RECUR-BACKGROUND.md) reconstructs the prior observer/recursion results needed by the holonomy work.
2. [HOL-01.md](HOL-01.md) states the original closed-comparison audit and its scientific criteria.
3. [HOL-01A.md](HOL-01A.md) records the negative canonical-transport gate on the cyclic-residue candidate.
4. [HOL-01B.md](HOL-01B.md) records the representation-dependent Wheeler rotation-quotient candidate.
5. [HOL-01C.md](HOL-01C.md) integrates the pre-existing RECUR observer connection and establishes the positive mathematical holonomy classification.
6. [HOL-02.md](HOL-02.md) begins the local-curvature/large-`n` audit and gives the first asymptotic result.
7. [`code/holonomy/recur_holonomy_formula.py`](../../code/holonomy/recur_holonomy_formula.py) reproduces the exact rotation-factor numerics using only the Python standard library.

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

HOL-02 shows that the fixed three-observer RECUR loop does not approach identity merely by taking `n` large. In fact,

\[
\theta_n\to\pi/2.
\]

So system size alone cannot be called a shrinking continuum loop. The next task is to search the existing observer structure for an intrinsic notion of loop size/separation. Only then is a curvature-density limit scientifically well posed.
