# EHF-HOL-02 — Local-Curvature / Large-n Scaling Gate

**Status: FIRST ANALYTIC GATE COMPLETE — fixed observer triangles do not become infinitesimal-flat as `n -> infinity`.**

## Question

HOL-01C establishes a nontrivial observer holonomy in the RECUR connection. Does increasing system size make the elementary three-observer loop approach the identity in a way analogous to an infinitesimal continuum connection?

This is deliberately narrower than asking whether EHF produces gravity.

## Input from HOL-01C / RECUR

For the complete symmetric Hamilton-cycle observer model, the norm-preserving loop sector contains

\[
R(\theta_n),
\]

with

\[
\cos\theta_n=
\frac{3(n-2)^2-4}{(n-2)^3}.
\]

Let `q=n-2`. Then

\[
\cos\theta_n=\frac3q-\frac4{q^3}.
\]

## Large-n limit

As `n -> infinity`,

\[
\cos\theta_n\to0,
\]

so

\[
\boxed{\theta_n\to\frac\pi2}.
\]

The residual rotation therefore approaches 90 degrees rather than zero.

Expanding about `pi/2`,

\[
\theta_n
=\frac\pi2-\arcsin\!\left(\frac3q-\frac4{q^3}\right)
=\frac\pi2-\frac3q-\frac1{2q^3}+O(q^{-5}).
\]

Thus the deviation from 90 degrees shrinks approximately as `3/(n-2)`, but the holonomy itself does **not** approach the identity.

## Immediate consequence

If a fixed three-observer triangle is declared to be an elementary loop at every `n`, simply taking `n` large does not yield the usual infinitesimal-flat behaviour

\[
\mathcal H\to I.
\]

Therefore the naive identification

> larger `n` = smaller physical loop = continuum curvature

fails this first gate.

That is useful: it prevents us from manufacturing a continuum interpretation from system size alone.

## Why this does not kill a curvature programme

In differential geometry, local curvature is inferred from holonomy only after specifying what counts as a shrinking loop and how its enclosed area scales. The RECUR construction currently has observer triples and their overlap structure, but no intrinsic continuum area measure.

A continuum-like limit could still exist if EHF supplies a sequence of loops `gamma_n` whose intrinsic size tends to zero while

\[
\mathcal H(\gamma_n)=I+F A_n+o(A_n)
\]

for an internally defined loop scale `A_n -> 0`. HOL-02 has not yet identified such a sequence.

## Candidate intrinsic loop scales

Future tests may use only quantities already defined by the discrete model, for example:

- observer-fibre overlap or information distance;
- graph/comparison distance between observer descriptions;
- a normalized defect derived from the transport matrices;
- automorphism-orbit data of observer triples;
- growth-level changes if the connection is extended across `n -> n+1`.

A geometric area must not be inserted merely to imitate general relativity.

## Curvature criterion for the next stage

For a proposed intrinsic scale `A(gamma)`, require all of the following before using the word curvature in the stronger local sense:

1. a family of loops with `A(gamma) -> 0`;
2. loop transport approaches identity on the recoverable sector;
3. `(H-I)/A` has a finite nonzero limit or controlled discrete analogue;
4. the limit is covariant under local observer basis changes;
5. different decompositions of comparable small loops obey a consistent composition law;
6. the result is not solely a polar-factor artefact or a consequence of information loss.

## Result

**HOL-02A: NEGATIVE for the naive fixed-triangle large-`n` limit.**

The existing exact formula gives a strong nonvanishing asymptotic holonomy:

\[
\theta_n\to90^\circ.
\]

This is mathematically interesting but is not the scaling expected if the same observer triangle were supposed to represent a shrinking approximately flat continuum loop.

## Next probe

**HOL-02B — Intrinsic Loop-Scale Search.**

Search the existing RECUR observer data for a canonical notion of separation/overlap that can order loops by intrinsic size. Only if such a scale exists should we test a curvature-density limit.

The companion script `code/holonomy/recur_holonomy_formula.py` reproduces the rotation formula numerically and displays its approach to `pi/2`.
