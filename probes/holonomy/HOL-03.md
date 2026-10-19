# EHF-HOL-03 — Growth-Refined Connection Audit

**Status: COMPLETE — exact inherited holonomy exists under a block-renormalized growth connection, but not under the native enlarged connection.**

## Question

HOL-02 found no canonical shrinking-loop scale at fixed size. EHF does contain ordered growth. Can an observer loop at size `n` be embedded into larger observer spaces so that its connection and holonomy are inherited coherently?

This audit reconstructs the relevant RECUR-11 through RECUR-13 results.

## Native growth maps

For Hamilton cycles, growth `n -> n+1` inserts a new label uniformly into an old edge. For an old observer, an old neighbour pair remains unchanged with weight `(n-2)/n`, or one neighbour becomes the new label with weight `1/n` for each endpoint.

For perfect matchings, growth `n -> n+2` adds two labels. An old observer's partner remains unchanged with weight `(n-1)/(n+1)`, or becomes either new label with weight `1/(n+1)`.

After normalization, the resulting rectangular maps

`U_a : V_a^(n) -> V_a^(N)`

are isometries in the audited models. They provide an explicit ancestry/refinement map.

## Native connection test

Let `W_ab^(n)` be the old polar observer transport and `W_ab^(N)` the native enlarged transport. Exact edge naturality would require

`U_b W_ab^(n) = W_ab^(N) U_a`.

For a loop `H_n`, exact inheritance would require

`U_a H_n = H_N U_a`.

RECUR-11 found that both identities fail globally, although the defects are low rank and have large kernels. Hamilton connection and loop defect ranks follow `n-2` and `2n-5` in the audited family; for perfect matchings they are `1` and `2`.

Thus native growth gives sectorial inheritance, not exact inheritance of the complete connection. Relative defects and angle increments decrease over the tested sizes, but that is not by itself an exact limit theorem.

## Growth memory

When the completed larger ensemble restores full permutation symmetry, growth-relative observer types merge into one orbit and share the new-size spectrum. RECUR-12 retained an old/new distinction through a scalar weight. This preserved growth-relative spectral classes, but no tested scalar weight restored exact inter-size naturality.

## Exact block refinement

RECUR-13 gives an exact construction. Let

`P_a = U_a U_a^T`

project onto the embedded-old observer sector. Define

`A_ab = U_b W_ab^(n) U_a^T`

on that sector and

`B_ab = polar[(I-P_b) W_ab^(N) (I-P_a)]`

on the new orthogonal complement. Set

`W_hat_ab = A_ab + B_ab`.

Then

`W_hat_ab U_a = U_b W_ab^(n)`

and the corresponding adjoint identity holds. Around any observer loop,

`H_hat_gamma U_a = U_a H_gamma^(n)`.

Every old loop eigenvector is therefore embedded with exactly the same eigenvalue. This is an exact growth-refined holonomy lineage.

The construction was tested for Hamilton growth `5 -> 6` through `12 -> 13` and matching growth `6 -> 8` through `14 -> 16`, with numerical identity defects below about `9e-14`.

## Fixed profile

For the inherited complete-family rotation,

`cos(theta_n) = [3q^2-4]/q^3`, `q=n-2`,

and hence

`q [pi/2-theta_n] -> 3`.

Exact block transport preserves the old angle without drift on the embedded sector. This is a fixed-profile result for that inherited sector, not a universal curvature density.

## Classification

The audit separates:

1. native growth — canonical ancestry, but no exact full inheritance;
2. scalar growth memory — spectral history can persist, but exact naturality is not restored;
3. matrix block refinement — exact inheritance exists on the embedded sector.

**HOL-03 passes as an exact recursive-refinement existence result, but not as a canonical continuum-limit result.**

Growth supplies a genuine map between successive observer structures. However, exact inheritance requires a deliberate matrix-valued renormalization of admissible comparison rather than following automatically from the native enlarged ensemble.

## Curvature boundary

This does not produce a shrinking area. Exact inheritance actually keeps the inherited nontrivial holonomy fixed under refinement. The block lineage is therefore closer to recursive reuse or renormalization than to subdivision of a geometric loop.

Any local-curvature programme should now distinguish the inherited sector from the genuinely new complement sector.

## Selection problem

The exact block construction is an existence theorem, not a uniqueness theorem. It is not established that the complement polar factor is uniquely preferred, that the renormalized connection comes from a unique positive local comparison kernel, or that a microscopic rule selects the matrix correction.

## Next probe

**HOL-04 — Complement-Sector / Refinement-Defect Audit.**

Study what growth adds rather than forcing the inherited sector to become infinitesimal. Measure the native-versus-exact connection correction and the new orthogonal complement across growth, and test whether a normalized defect or complement holonomy has a controlled vanishing or fixed-profile limit.
