# RECUR Background for the EHF Holonomy Branch

This note makes the holonomy branch self-contained. It records the earlier recursive-observer results used by HOL-01C, so a reader does not need earlier chat transcripts or private working notes.

## Observer construction

The primary model uses undirected Hamilton cycles of `K_n` as microstates. Observer `O_a`, anchored at vertex `a`, retains only the unordered pair of neighbours of `a`. Its state count is

\[
d_n=\binom{n-1}{2}.
\]

Earlier RECUR audits established that this one-anchor port observer is an exact dynamically sufficient quotient for the audited full 2-opt dynamics. This motivates treating it as a reusable effective description rather than an arbitrary projection.

## RECUR-04: a useful negative result

For observer partition `P`, let `r_P(u)` be the vector of transition counts from microstate `u` into the observer blocks and define

\[
\delta_P(u,v)=r_P(u)-r_P(v).
\]

This detects hidden information, but `delta_P = d r_P`; it is an exact 1-cocycle and sums to zero around every closed loop. It therefore cannot provide nontrivial holonomy.

## RECUR-05: conditional observer transport

For anchors `a,b`, define

\[
K_{ab}(B\mid A)=
\frac{|\{H:\pi_a(H)=A,\ \pi_b(H)=B\}|}
{|\{H:\pi_a(H)=A\}|}.
\]

This reconstructs uniformly over the complete source fibre and records observer `b`; no representative microstate is selected. For three observers,

\[
H_{abc}=K_{ab}K_{bc}K_{ca}.
\]

Enumeration for `5 <= n <= 8` found nonzero direct-versus-indirect reconstruction defects and nonidentity loop transport. Under independent observer-state relabellings the loop transforms by conjugation, so trace, rank and spectrum are invariant. However, the transports are generally rank deficient, with observed rank `2(n-2)`. RECUR-05 therefore establishes path-dependent coarse reconstruction but does not by itself separate holonomy from information loss.

## RECUR-06: loss separation

Write

\[
L_{ab}=K_{ab}^{\mathsf T}=U\Sigma V^{\mathsf T}
\]

and define the polar partial isometry on nonzero support,

\[
W_{ab}=U_rV_r^{\mathsf T}.
\]

For an oriented observer triangle,

\[
\mathcal H_{abc}=W_{ca}W_{bc}W_{ab}.
\]

The single-transport singular spectrum is

\[
1^{[2]},\qquad
\left(\frac1{n-3}\right)^{[2(n-3)]},\qquad
0^{[\binom{n-1}{2}-2(n-2)]}.
\]

After attenuation and zero directions are separated, a norm-preserving nonidentity loop sector remains. For `n >= 6` its spectrum is

\[
\boxed{\{1,(-1)^{[n-3]},e^{i\theta_n},e^{-i\theta_n}\}},
\]

where

\[
\boxed{\cos\theta_n=\frac{3(n-2)^2-4}{(n-2)^3}}.
\]

Orientation reversal produces the inverse loop on the norm-preserving sector. Independent orthogonal basis changes at each observer conjugate the loop operator, leaving its spectrum and rotation angle unchanged.

## RECUR-07: robustness boundary

The spectral certificates and rotation formula were checked through `n=12`. Small changes to the microstate prior and observer metric retained a nearby almost-unit-modulus rotation, while larger changes mixed it with lossy directions. Exact angle and exact unitarity are therefore not presently metric-free or prior-free invariants.

## RECUR-08: analytic mechanism and second substrate

Put `q=n-2`. The two-anchor observer transport contains the block

\[
K_X=\frac{J_q-I_q}{q-1},
\]

whose polar factor is

\[
W_X=\frac2qJ_q-I_q.
\]

The complementary block is controlled by the Johnson association scheme `J(q,2)`. The resulting three-observer norm-preserving loop decomposes as

\[
1\oplus(-1)^{[n-3]}\oplus R(\theta_n),
\]

with characteristic rotation factor

\[
\lambda^2-2\frac{3q^2-4}{q^3}\lambda+1.
\]

This gives the cosine formula above.

The construction was also repeated on perfect matchings of `K_n`, where observer `O_a` records the partner of `a`. The same reflection block appears and the three-observer loop has the same rotation angle. The effect is therefore not unique to Hamilton cycles; it is tied to the shared overlap geometry of these symmetric local observers.

## RECUR-09/10: symmetry breaking

Sparse and irregular graph controls showed that nonidentity observer holonomy often survives symmetry breaking, while the unique common angle generally does not. Reduced symmetry produces multiple angle classes or dispersion.

An automorphism audit found that the nonzero loop spectrum is constant on each automorphism orbit of observer triples. In the nondegenerate tested ensembles, different triple orbits also had different spectra. A degenerate cycle-only control had only trivial loop spectra, so orbit structure alone is not sufficient; a nontrivial ensemble of overlapping closures is also required.

## Current theorem-status boundary

Within the stated constructions, EHF has a discrete observer connection with path-dependent closed transport and a residual orientation-sensitive norm-preserving holonomy after simple loss is separated. The complete symmetric models admit an analytic rotation formula, and related holonomy recurs in a second closure substrate.

This does **not** establish spacetime curvature, Lorentzian geometry, Einstein dynamics, the equivalence principle, quantum phase, or a metric/prior-independent universal invariant.

The next HOL question is therefore whether a local curvature-like invariant and controlled scaling limit can be extracted from this connection without importing continuum geometry by hand.
