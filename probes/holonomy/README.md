# EHF Holonomy Branch

This branch investigates whether nontrivial loop holonomy can arise from EHF's existing primitive structure of admissible comparison and transformation, and whether that structure admits a controlled local-curvature-like scaling limit.

## Start here

A reader should not need the original ChatGPT conversations to follow this branch.

1. [RECUR-BACKGROUND.md](RECUR-BACKGROUND.md) reconstructs the prior observer/recursion results needed by the holonomy work.
2. [HOL-01.md](HOL-01.md) states the original closed-comparison audit and its scientific criteria.
3. [HOL-01A.md](HOL-01A.md) records the negative canonical-transport gate on the cyclic-residue candidate.
4. [HOL-01B.md](HOL-01B.md) records the representation-dependent Wheeler rotation-quotient candidate.
5. [HOL-01C.md](HOL-01C.md) integrates the pre-existing RECUR observer connection and establishes the positive mathematical holonomy classification.
6. [HOL-02.md](HOL-02.md) shows that a fixed observer triangle approaches a 90-degree rather than identity rotation as size grows.
7. [HOL-02B.md](HOL-02B.md) audits existing RECUR quantities for an intrinsic shrinking-loop scale and finds none at fixed size.
8. [HOL-03.md](HOL-03.md) reconstructs the RECUR growth-transport results and establishes an exact block-renormalized holonomy lineage across growth, while showing that the native enlarged connection is not exactly functorial.
9. [`code/holonomy/recur_holonomy_formula.py`](../../code/holonomy/recur_holonomy_formula.py) reproduces the exact rotation-factor numerics using only the Python standard library.

## Current mathematical picture

The Wheeler candidates do not supply intrinsic holonomy under the strict HOL-01 criteria. The RECUR observer construction does: after attenuation and kernel loss are separated, a nonidentity orientation-sensitive norm-preserving loop sector remains. In the complete symmetric models,

\[
\cos\theta_n=\frac{3(n-2)^2-4}{(n-2)^3}.
\]

The same rotation occurs in a perfect-matching control with the same relevant observer-overlap reflection structure. Symmetry breaking generally splits the common angle into orbit-dependent classes.

HOL-02 establishes that this is not automatically a smooth-curvature limit: a fixed observer triangle tends to a 90-degree rotation and no existing fixed-level quantity supplies a canonical shrinking-loop area.

HOL-03 adds a different structure. The existing combinatorial growth maps embed old observer spaces isometrically into larger ones. The native enlarged connection fails exact full inheritance but differs only on a thin growth-sensitive sector in the audited families. A matrix-valued old/new block connection can be constructed that exactly intertwines the inherited sector and carries every old loop eigenvalue unchanged into the enlarged system. This is an exact recursive-refinement existence result, not yet a uniquely selected connection or a continuum geometry.

## Research discipline

The programme keeps three levels separate:

1. **Mathematical result** — properties proved or measured in an EHF construction.
2. **Geometric analogy** — comparison with established notions such as parallel transport, holonomy, curvature and renormalization.
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

Across growth, an isometric observer embedding `U_a` permits a sharper naturality question. For a renormalized enlarged connection `W_hat`, exact inheritance means

\[
W_{ab}^{\rm hat}U_a=U_bW_{ab}^{(n)},
\]

and therefore for any loop

\[
H_{\gamma}^{\rm hat}U_a=U_aH_{\gamma}^{(n)}.
\]

HOL-03 establishes that such a block connection exists in the audited complete-family controls, while the native enlarged connection does not satisfy the identity globally.

## Current frontier

The inherited sector is not the place to look for a vanishing local holonomy: exact refinement preserves it. The next mathematically motivated object is the **growth-added complement and the native-versus-exact refinement defect**.

HOL-04 should ask whether the correction needed to reconcile native growth with exact inheritance has a controlled normalized limit, and whether the new complement develops its own stable or vanishing holonomy structure. This uses an obstruction already present in the mathematics rather than inventing geometric length or area.
