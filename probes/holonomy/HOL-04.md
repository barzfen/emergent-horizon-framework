# EHF-HOL-04 — Complement-Sector / Refinement-Defect Audit

**Status: COMPLETE — the growth-sensitive obstruction occupies a vanishing fraction of observer space and the native complete-family holonomy increment vanishes quadratically, while the inherited holonomy itself remains nontrivial. This supplies an intrinsic asymptotic refinement-defect scale, not yet curvature.**

## Question

HOL-03 showed that old holonomy can be inherited exactly under a block-renormalized connection, whereas the native enlarged connection fails exact naturality on a thin growth-sensitive sector. Instead of forcing the inherited holonomy to become small, HOL-04 asks whether the *change introduced by one growth step* becomes small in an intrinsic sense.

The audit uses only quantities already defined by RECUR-11 through RECUR-13.

## 1. Defect-support fraction

For Hamilton-cycle observers at old size `n`, the observer dimension is

`d_HC(n) = C(n-1,2)`.

RECUR-11 found native connection-defect rank `n-2` and loop-defect rank `2n-5`. Therefore the fractions of old observer space touched by the defects are

`f_edge_HC(n) = (n-2)/C(n-1,2) = 2/(n-1)`,

and

`f_loop_HC(n) = (2n-5)/C(n-1,2)
              = 2(2n-5)/[(n-1)(n-2)]`.

Hence

`f_edge_HC(n) -> 0` and `f_loop_HC(n) -> 0`,

with leading orders `2/n` and `4/n`.

For perfect-matching observers the old dimension is

`d_PM(n) = n-1`,

while the connection- and loop-defect ranks are `1` and `2`. Thus

`f_edge_PM(n) = 1/(n-1) -> 0`,

`f_loop_PM(n) = 2/(n-1) -> 0`.

So in both independently audited closure families, a single growth step changes a vanishing *fraction* of the old observer space even though exact native naturality fails at every finite tested size.

This is stronger than merely observing decreasing matrix norms: it follows algebraically from the finite-size rank patterns, conditional on those rank formulas continuing as established in the audited families.

## 2. Exact-block correction is also asymptotically thin

RECUR-13 found correction rank equal to the growth-added complement dimension.

For Hamilton growth `n -> n+1`, the old observer dimension is `C(n-1,2)` and the enlarged dimension is `C(n,2)`. Their difference is `n-1`, exactly the observed correction rank. Relative to the enlarged space,

`f_corr_HC(n) = (n-1)/C(n,2) = 2/n -> 0`.

For perfect-matching growth `n -> n+2`, the enlarged observer dimension is `n+1`, the old dimension is `n-1`, and the complement/correction dimension is `2`. Therefore

`f_corr_PM(n) = 2/(n+1) -> 0`.

Thus the matrix-valued repair needed for exact inheritance remains nonzero but is confined to a vanishing fraction of the enlarged observer degrees of freedom.

## 3. Holonomy increment under native growth

For the complete-family rotation let `q=n-2`. The exact RECUR formula is

`cos(theta_q) = 3/q - 4/q^3`.

For large `q`, write `theta_q = pi/2 - epsilon_q`. Since `sin(epsilon_q)=3/q-4/q^3`, expansion gives

`epsilon_q = 3/q + (1/2)/q^3 + O(q^-5)`.

Therefore

`theta_q = pi/2 - 3/q - 1/(2q^3) + O(q^-5)`.

One growth step changes the native angle by

`Delta theta_q = theta_(q+1) - theta_q
               = 3/q^2 + O(q^-3)`.

Consequently

`Delta theta_q -> 0`

and, more sharply,

`q^2 Delta theta_q -> 3`.

This is an intrinsic asymptotic refinement scale already encoded in the exact holonomy formula. The absolute loop holonomy approaches a 90-degree rotation, but the *change caused by one additional growth step* approaches zero quadratically.

That distinction resolves the apparent tension between HOL-02 and HOL-03/04:

- fixed-loop holonomy does not approach identity;
- successive native growth levels nevertheless become increasingly close in holonomy angle;
- the fraction of observer space on which native growth violates exact inheritance tends to zero.

## 4. What this does and does not establish

The combined asymptotic picture is

`persistent inherited structure + asymptotically thin refinement defect`.

That is a meaningful discrete refinement phenomenon. It does **not** yet provide a geometric area, Riemann tensor, Ricci curvature, Einstein equation, or physical gravitational field.

In particular, a vanishing defect fraction is not the same thing as a vanishing operator norm. A low-rank correction can retain finite action on the directions it touches. Likewise, `Delta theta -> 0` measures inter-size change, not small-loop holonomy.

Therefore the correct current statement is:

> EHF's audited observer connection has a nontrivial persistent holonomy sector whose native inter-size change becomes asymptotically small, while the growth-sensitive obstruction occupies a vanishing fraction of observer space.

## 5. Complement holonomy status

Under the RECUR-13 polar-complement choice, the tested new complement introduced no additional nonreal unitary rotation angle; it contributed only real `+1/-1` sectors. Thus no independent complement curvature-like phase has yet appeared in that construction.

This result is complement-choice dependent. Since uniqueness of the complement connection is not established, absence of a new phase cannot yet be promoted to a framework-level theorem.

## 6. Theorem-status boundary

### Algebraic consequences of the reported rank formulas

- Hamilton native edge-defect fraction scales as `2/(n-1)`.
- Hamilton native loop-defect fraction scales as `2(2n-5)/[(n-1)(n-2)]`.
- Perfect-matching native edge- and loop-defect fractions scale as `1/(n-1)` and `2/(n-1)`.
- RECUR-13 correction fractions scale as `2/n` for Hamilton cycles and `2/(n+1)` for perfect matchings.

### Derived analytically from the exact complete-family angle formula

- `theta_q = pi/2 - 3/q - 1/(2q^3) + O(q^-5)`.
- `Delta theta_q = 3/q^2 + O(q^-3)`.
- `q^2 Delta theta_q -> 3`.

### Established computationally in prior RECUR audits

- the finite-size rank patterns over the reported HC and PM sweeps;
- decreasing relative native defects;
- exact block inheritance to numerical precision;
- no extra nonreal unitary complement angle for the tested polar-complement choice.

### Not established

- a proof of the native rank formulas for all admissible sizes;
- vanishing operator norm of the refinement correction;
- uniqueness of the block/complement connection;
- a canonical geometric area associated with one growth step;
- a continuum manifold or physical curvature interpretation.

## Verdict

**HOL-04 PASS as an asymptotic refinement-defect result.**

The strongest new invariant is not that holonomy itself vanishes. It is that one-step *change* has a controlled scaling:

`q^2 Delta theta_q -> 3`,

while the support fraction of the growth obstruction falls as `O(1/n)` in both audited closure families.

This is the first point in the holonomy branch where EHF has an internally defined refinement parameter and a quantitatively vanishing inter-level change without assigning external geometric length.

## Next probe

**HOL-05 — Renormalized Refinement Generator Audit.**

Use the one-step difference itself to define a candidate infinitesimal growth generator. Test whether a rescaled connection/holonomy difference such as `q^2(H_(q+1)-embedded(H_q))`, restricted to the appropriate native or growth-sensitive sector, converges to a nontrivial operator rather than merely a scalar angle. Compare Hamilton-cycle and perfect-matching controls and keep inherited versus complement sectors explicit.
