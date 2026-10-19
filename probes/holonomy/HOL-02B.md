# EHF-HOL-02B — Intrinsic Loop-Scale Search

**Status: COMPLETE — NO CANONICAL SHRINKING LOOP SCALE IN THE CURRENT FIXED-n RECUR OBSERVER GEOMETRY.**

## Question

Does the existing RECUR observer construction already contain a canonical, non-geometric notion of loop size that can shrink to zero and support a local-curvature limit?

This audit does not invent a distance or area. It searches only quantities already present in the RECUR construction.

## Existing ingredients

For the one-port Hamilton-cycle observer `O_a`, the observer state records the unordered pair of neighbours of anchor `a`. For two distinct anchors `a,b`, RECUR defines a conditional reconstruction kernel `K_ab`; its polar partial isometry `W_ab` gives the loss-separated comparison map. A three-anchor loop has

\[
\mathcal H_{abc}=W_{ca}W_{bc}W_{ab}.
\]

The earlier RECUR audits also established that automorphisms of the substrate act on observer triples and preserve the nonzero loop spectrum within each automorphism orbit.

## Candidate 1 — graph distance between observers

In the complete-graph Hamilton and perfect-matching controls, observers are indexed by vertices of `K_n`. Every distinct pair of anchors is adjacent, so

\[
d(a,b)=1
\]

for all `a != b`.

Every nondegenerate observer triangle therefore has the same edge-distance pattern `(1,1,1)`. Graph distance supplies no hierarchy of smaller versus larger loops.

Sparse substrates introduce different graph distances, but RECUR-09 showed that holonomy then depends strongly on the orbit type of the entire observer triple, not on degree irregularity alone. Distance is therefore not presently a canonical scalar loop area.

## Candidate 2 — observer-fibre size

In the complete Hamilton model every one-port observer has the same fibre size by label symmetry. Fibre size changes with global system size `n`, but does not distinguish one three-observer loop from another at fixed `n`.

Moreover HOL-02A already showed that increasing `n` does not make the fixed observer triangle approach identity: its rotation approaches `pi/2`. Thus inverse fibre size cannot by itself be interpreted as a shrinking-loop area.

## Candidate 3 — pairwise conditional overlap / transport strength

The singular spectrum of every pair transport in the complete symmetric model is

\[
1^{[2]},\qquad
\left(\frac1{n-3}\right)^{[2(n-3)]},\qquad
0^{[\binom{n-1}{2}-2(n-2)]}.
\]

This provides an intrinsic measure of recoverability/loss, but label symmetry again makes it identical for every distinct observer pair at fixed `n`.

As `n` grows, the nontrivial singular value tends to zero while the loop rotation tends to 90 degrees. Therefore increasing pairwise information loss is not a small-loop parameter for the residual holonomy.

## Candidate 4 — direct-versus-indirect reconstruction defect

RECUR-05 measured

\[
\|K_{ac}-K_{ab}K_{bc}\|_F.
\]

For complete symmetric substrates this scalar is the same for every anchor triangle at fixed `n`. It decreases only mildly over the audited sizes while the loss-separated rotation grows toward 90 degrees.

The defect is useful as a path-dependence diagnostic, but it is not currently an area-like parameter whose vanishing forces `H -> I`.

## Candidate 5 — automorphism-orbit type

RECUR-09/10 gives the strongest intrinsic classifier of loop type. Under substrate automorphisms, observer triples split into orbits, and the nonzero holonomy spectrum is constant within each orbit for the audited nondegenerate controls.

This is structurally important: the natural discrete analogue of a local loop *type* is an observer-triple orbit, not an arbitrary coordinate triangle.

But an orbit label is categorical, not a scale. There is no canonical ordering

\[
\mathcal O_1 > \mathcal O_2 > \cdots \to 0
\]

that would define shrinking loops.

## Candidate 6 — normalized holonomy defect itself

One could define

\[
A(\gamma)=\|\mathcal H_\gamma-I\|
\]

and then trivially make `H-I` scale with `A`. This is rejected as circular: the proposed loop size would be defined by the quantity whose curvature density we are trying to measure.

The same objection applies to defining area directly from the rotation angle.

## Result

The fixed-`n` RECUR observer geometry currently supplies:

- canonical observer states;
- canonical conditional comparison after a reconstruction measure is chosen;
- loss-separated polar transport;
- closed-loop holonomy;
- gauge-covariant spectral invariants;
- automorphism-orbit classification of loop types.

It does **not** currently supply a canonical scalar loop size with a sequence tending to zero.

Therefore:

> **HOL-02B verdict: the existing fixed-level observer connection has discrete holonomy, but no intrinsic shrinking-loop structure has yet been identified. A local curvature density in the continuum sense is therefore undefined, not zero.**

This is stronger and safer than assigning an arbitrary area to observer triangles.

## Important distinction

Failure to define a continuum curvature density does not remove the discrete holonomy result. A discrete connection can have meaningful loop invariants without being a discretization of a smooth manifold.

The current mathematical object is best described as a **discrete observer connection with orbit-classified holonomy**.

## Where a genuine scale may enter

The most natural pre-existing EHF source of scale is not fixed-`n` observer separation but **growth**. EHF already contains maps between levels `n -> n+1`, and later RECUR work studies inherited sectors across growth. That supplies an ordered refinement variable without inventing Euclidean distance.

The next audit should therefore ask whether growth induces a compatible hierarchy of observer loops and whether coarse loops can be refined into descendant loops whose comparison transport approaches a controlled limit.

## Next probe

**EHF-HOL-03 — Growth-Refined Connection Audit**

Required questions:

1. Is there a canonical ancestry/refinement map from observer states or recoverable sectors at level `n` to level `n+1`?
2. Does it intertwine the within-level comparison connection?
3. Can an observer loop at level `n` be refined into a canonical family of descendant loops at higher levels?
4. Does the holonomy of those descendants converge, remain finite, or diverge after comparison on the inherited sector?
5. Can any refinement parameter be justified intrinsically as resolution rather than declared to be geometric length?

No spacetime or gravity interpretation is licensed by HOL-02B.