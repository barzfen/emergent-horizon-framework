# EHF-HOL-01 — Closed-Comparison Holonomy Audit

**Status: COMPLETE — HOL-01C achieved in the pre-existing RECUR observer connection.**

## Question

Do already-existing EHF comparison structures generate nontrivial path dependence when a transportable local datum is carried around a closed admissible history, without inserting curvature, gravity, spacetime or a gauge field by hand?

## Scientific requirement

A cycle in state space is not enough. The transported datum and comparison rule must already be motivated by the EHF construction. If they have to be invented solely to produce a loop defect, the candidate fails this audit.

## Candidate sequence

### HOL-01A — cyclic-residue dynamics

The WHEELER-09 residue chain has canonical state transitions but no independent nontrivial local fibre. Fixed site frames transport trivially; the state itself returns by definition; tracking a marked residue unit would add structure not present in the model.

Result: **TRIVIAL / UNDEFINED for nontrivial transport.** See [HOL-01A.md](HOL-01A.md).

### HOL-01B — Wheeler rotation quotient

The WHEELER-59 quotient has rooted orientation information, but that root is exactly the redundancy removed by the rotation quotient. Symmetric states also make a unique canonicalizing rotation unavailable without a tie-breaking convention.

Result: **REPRESENTATION-DEPENDENT, not intrinsic.** See [HOL-01B.md](HOL-01B.md).

### HOL-01C — RECUR observer connection

The earlier RECUR programme already supplied the missing structure. One-anchor port observers are dynamically motivated effective descriptions, and uniform conditional reconstruction defines observer-to-observer transport

\[
K_{ab}(B\mid A)=
\frac{|\{H:\pi_a(H)=A,\ \pi_b(H)=B\}|}
{|\{H:\pi_a(H)=A\}|}.
\]

The raw loop is path dependent but lossy. RECUR-06 therefore uses the polar partial isometry `W_ab` of the conditional transport and forms

\[
\mathcal H_{abc}=W_{ca}W_{bc}W_{ab}.
\]

After attenuation and kernel directions are separated, a nonidentity norm-preserving sector remains. For the complete symmetric Hamilton-cycle model its spectrum is

\[
\{1,(-1)^{[n-3]},e^{i\theta_n},e^{-i\theta_n}\},
\]

with

\[
\cos\theta_n=\frac{3(n-2)^2-4}{(n-2)^3}.
\]

Orientation reversal inverts the loop on this sector. Local orthogonal basis changes conjugate the loop and leave its spectrum and angle invariant. RECUR-08 derives the rotation through the observer-overlap association structure and reproduces the same angle in a perfect-matching substrate with the same relevant reflection block.

Result: **HOL-01C / INTRINSIC MATHEMATICAL HOLONOMY for the stated observer connection.**

The full prior construction and its limitations are reconstructed in [RECUR-BACKGROUND.md](RECUR-BACKGROUND.md); the integration verdict is in [HOL-01C.md](HOL-01C.md).

## What HOL-01 establishes

EHF contains at least one explicit discrete observer connection whose closed transport has a residual, orientation-sensitive, basis-covariant nonidentity action after simple information-loss factors are separated.

This is stronger than finding a cycle, a canonicalization defect or a lossy stochastic loop.

## What HOL-01 does not establish

It does not establish spacetime curvature, gravity, a Levi-Civita connection, Lorentzian geometry, Einstein dynamics, quantum phase or physical observer dynamics. The reconstruction measure and observer metric remain part of the construction, and exact unitarity/angle are not universal under arbitrary changes to them.

## Next audit

Proceed to [HOL-02.md](HOL-02.md): determine whether the observer connection admits an intrinsic small-loop notion and a controlled local-curvature-like scaling limit. The first large-`n` gate is already negative for the naive fixed-triangle interpretation: `theta_n -> pi/2`, not zero.
