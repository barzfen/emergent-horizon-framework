# EHF-HOL-01C — RECUR Observer-Connection Integration Audit

**Status: PASS — intrinsic mathematical holonomy already exists in the prior RECUR branch, subject to an explicitly chosen reconstruction geometry.**

## Why this audit changed direction

HOL-01A and HOL-01B tested currently organised repository sectors and found, respectively, no canonical nontrivial transport and only representation-dependent rotational residue. Re-examining the earlier EHF recursive-closure work reveals that the required construction had already been developed in RECUR-05 through RECUR-07.

This file records that connection so the holonomy branch does not duplicate or overwrite the earlier result.

## Native observer transport from RECUR-05

For each anchor `a`, observer `O_a` retains the unordered pair of neighbours of `a` in a Hamilton cycle. For observers `a,b`, the canonical coarse transport is the uniform conditional reconstruction kernel

\[
K_{ab}(B\mid A)=
\frac{|\{H:\pi_a(H)=A,\ \pi_b(H)=B\}|}
{|\{H:\pi_a(H)=A\}|}.
\]

This is native to the observer construction: it averages over the complete source fibre rather than selecting a representative microstate.

For an observer triangle,

\[
H_{abc}=K_{ab}K_{bc}K_{ca}.
\]

RECUR-05 found nonidentity, gauge-resistant loop transport for all tested anchor triangles at `5 <= n <= 8`, but the kernels are generally rank deficient. Thus this first effect is path-dependent coarse reconstruction and can still be explained by information loss.

## Loss-curvature separation from RECUR-06

RECUR-06 transposes the conditional kernel to column form,

\[
L_{ab}=K_{ab}^{\mathsf T},
\]

and uses its polar decomposition. If

\[
L_{ab}=U\Sigma V^{\mathsf T},
\]

the canonical polar partial isometry is

\[
W_{ab}=U_rV_r^{\mathsf T},
\]

with zero singular directions omitted. The observer-loop connection is then

\[
\mathcal H_{abc}=W_{ca}W_{bc}W_{ab}.
\]

After attenuation and kernel directions are separated, a norm-preserving invariant loop sector survives and is nonidentity.

For `n >= 6`, the observed unitary-sector spectrum is

\[
\{1,(-1)^{[n-3]},e^{i\theta_n},e^{-i\theta_n}\},
\]

with

\[
\cos\theta_n=
\frac{3(n-2)^2-4}{(n-2)^3}.
\]

The rotation pair reverses to its inverse under orientation reversal. Independent orthogonal basis changes at each observer conjugate the loop operator, leaving its spectrum and rotation angle invariant.

This meets the mathematical core of HOL-01C: a nontrivial loop action survives removal of simple attenuation/kernel loss and survives local basis relabelling.

## Robustness from RECUR-07

The prior audit extended exact finite-matrix spectral certificates through `n=12` and verified the rotation-cosine formula to numerical precision over that range. Small perturbations of the prior and observer metric retain a nearby almost-unit-modulus rotation, while larger perturbations progressively destroy exact unitarity.

Therefore three claims must remain separate:

1. **Uniform-model holonomy:** strong and reproducible.
2. **Local robustness:** supported under small prior/metric perturbations.
3. **Metric/prior-free universality:** not established.

## HOL-01 classification

The RECUR construction upgrades the holonomy search beyond the Wheeler tests:

- it has an already-motivated transported observer description;
- it has canonical comparison maps once the uniform-fibre reconstruction rule and observer metric are fixed;
- closed composition is path dependent;
- the residual polar-loop action contains a nonidentity norm-preserving sector;
- orientation reversal inverts the holonomy;
- loop spectral data are invariant under independent observer basis changes.

Accordingly:

> **HOL-01C PASS: EHF already contains a mathematically nontrivial, orientation-sensitive, gauge-covariant observer holonomy in the RECUR construction.**

## Scientific boundary

This is **not** evidence that EHF has derived gravity or spacetime curvature. The observer family, conditional reconstruction rule, prior and metric are structural choices. The result is currently a discrete connection with genuine residual mathematical holonomy, not a demonstrated Levi-Civita connection or physical gauge field.

No claim should be made that the rotation angle is gravitational, quantum mechanical or physically measurable without an independent bridge.

## Consequence for the new gravity-visualisation branch

The next useful question is no longer `does EHF admit holonomy?` That question has a positive mathematical answer in RECUR.

The sharper question is:

> Can the RECUR observer connection acquire an intrinsic local curvature description and controlled continuum/large-`n` limit without importing spacetime geometry by hand?

A follow-up should therefore study small-loop/connection structure, large-`n` scaling, metric dependence, and whether a curvature-like local invariant can be defined from the existing comparison data before any GR analogy is attempted.
