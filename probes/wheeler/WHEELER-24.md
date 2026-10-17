# WHEELER-24 — Confinement / Gap-Opening Audit

**Status: NEGATIVE for intrinsic gap opening under the tested EHF mechanisms**

## Question

WHEELER-23 found that the mobile `D=2` excitation has a diffusive internal spectral gap

`lambda_1(n) = 4 sin^2(pi/n) ~ 4 pi^2 / n^2`,

which collapses as `n -> infinity`.

Can an existing EHF mechanism open a nonzero thermodynamic dynamical gap without inserting a mass term or explicit pinning by hand?

Mechanisms considered:

- interaction between the two boundaries;
- growth constraints;
- observer-relative admissibility;
- Hamilton-history closure;
- state-graph curvature / sector structure.

## Center-of-mass obstruction

Let the two boundaries of the `D=2` excitation have positions `x_1,x_2` on the cycle. Introduce relative and center-of-mass coordinates schematically as

`r = x_2 - x_1`,

`X = x_1 + x_2 (mod n)`.

An interaction potential depending only on their separation,

`V = V(r)`,

can confine `r`, but it leaves translation of the whole composite unchanged:

`X -> X + constant`.

Therefore the pair may become a bound object while its center of mass remains free to execute a random walk around the cycle.

That free translation alone produces the same cycle Laplacian low mode,

`lambda_1(n) = 4 sin^2(pi/n) ~ 4 pi^2/n^2`.

So **binding is not the same as gap opening**.

## Boundary interaction

A boundary-boundary attraction can reduce the available relative-coordinate states and create a localized composite in separation space.

But unless the rule breaks translation covariance or induces long-range/nonlocal connectivity in the center-of-mass coordinate, the composite still has `n` translated copies. The first translational mode therefore collapses as `n^-2`.

Verdict: **FAIL for opening the thermodynamic dynamical gap by itself.**

## Growth

The current MICRO growth rule preserves `D` and expands the available cycle size. It does not select a preferred absolute location for the excitation.

Thus growth increases the number of translated realizations rather than removing the translational soft mode.

Verdict: **FAIL for gap opening; if anything, larger n exposes the asymptotic collapse more clearly.**

## Observer-relative admissibility

An observer can define a preferred location, slicing, or relational frame. Relative to that observer, the excitation may appear pinned.

However, this is not an intrinsic gap of the closed system unless the observer is part of the dynamical state and the combined observer-system rules themselves remove the global translation mode.

Verdict: **CONDITIONAL only; observer pinning cannot be counted as intrinsic without a full observer-covariant construction.**

## Hamilton-history closure

Closure quantizes global crossing and winding data, but ordinary cyclic closure remains translation symmetric. Moving a closed-history excitation around the cycle does not change its topological sector.

Therefore closure protects sector labels but does not by itself penalize center-of-mass translation.

Verdict: **FAIL for gap opening by itself.**

## State-graph geometry

A genuine size-independent spectral gap could arise if the excitation graph stopped behaving like a one-dimensional cycle and instead acquired expansion-like connectivity, strong curvature, or another mechanism that changes the large-scale graph family.

This is a real mathematical possibility, but it is not currently derived from the existing MICRO/Wheeler move set.

To keep translation symmetry while obtaining a constant spectral gap would require qualitatively different kinetic connectivity than nearest-neighbour motion on a growing ring.

Verdict: **OPEN in principle, not presently realized by the tested EHF primitives.**

## Main conclusion

The current route fails for a simple structural reason:

`local binding can gap relative motion, but an unpinned translation-covariant composite retains a gapless center-of-mass mode.`

Hence the existing EHF mechanisms tested here do not turn the WHEELER-23 diffusive mode into a positive thermodynamic spectral gap.

## Verdict

- **PASS:** identified the precise obstruction to gap opening.
- **NEGATIVE:** pair interaction alone does not remove the `n^-2` mode.
- **NEGATIVE:** current growth does not remove it.
- **NEGATIVE:** Hamilton closure does not remove it.
- **CONDITIONAL:** observer-relative pinning only works if the observer is included dynamically.
- **OPEN:** a different state-graph geometry with expansion-like connectivity could in principle produce a finite gap, but this has not been derived.

## Consequence for the mass-gap programme

The present MICRO/Wheeler boundary model should not be treated as a candidate Yang-Mills mass-gap mechanism. It provides:

- quantized boundary content;
- a finite static excitation cost;
- conserved/growth-stable domain-wall sectors;
- exact diffusive kinetic scaling;

but not a nonzero thermodynamic dynamical gap.

The next useful step should be to stop trying to rescue the same one-dimensional mobile-pair mechanism and instead test whether an independently motivated EHF state graph can generate expander-like or dimension-changing kinetic geometry while retaining locality in the underlying primitive rules.
