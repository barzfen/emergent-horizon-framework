# EHF-XBR-02 Result Note
## Common Growth Groupoid and Dual-Functor Compatibility

**Status:** independently validated in the construction environment  
**Script version:** `ehf_xbr_02_v2_2026-07-25`

## Verdict

```text
EHF_XBR_02_COMMON_GROUPOID_DUAL_FUNCTOR_COMPATIBILITY_PASS
```

All 25 strict checks passed.

## Fixed-anchor obstruction

The naive attempt to let all 72 AMP chart relabellings act on the single
globally anchor-0 OPW presentation fails.

Only the reference chart

\[
(1,9)
\]

preserves both the fixed-chart OPW3 graph and its \(\Pi\)-fibres:

\[
1/72.
\]

This is not a failure of the atlas principle. It shows that the global
anchor-0 canonical representative is chart data.

For odd \(n\), relabelling and then returning to the global representative can
reverse the anchored ordering, which changes the even/odd position split.

## Common pullback groupoid

For every AMP chart

\[
C=(a,d),
\qquad a\ne d,
\]

define

\[
\rho_C(a)=1,
\qquad
\rho_C(d)=9,
\]

with the remaining labels sent increasingly to \(2,\ldots,8\).

The common arrows are

\[
\pi_{D\leftarrow C}
=
\rho_D^{-1}\rho_C.
\]

The exact base contains

\[
72
\]

objects and

\[
5184
\]

ordered arrows.

The reconstructed arrows agree exactly with the AMP 03L transition ledger.

## OPW dynamics lift

Define the chart-\(C\) OPW representative of a reference cycle \(c\) by

\[
c_C=\rho_C^{-1}(c),
\]

and chart canonicalisation by

\[
\operatorname{can}_C(x)
=
\rho_C^{-1}
\operatorname{can}_{\mathrm{ref}}
\bigl(\rho_C(x)\bigr).
\]

In every chart:

\[
|V|=20160,
\qquad
|E|=53760.
\]

All 72 charts satisfy:

- exact state bijection;
- exact pullback orientation;
- exact \(\Pi\)-covariance;
- exact LR3 move covariance;
- exact OPW3 graph covariance;
- exact representative transport under every common arrow.

Thus OPW dynamics defines an exact chart-relative lift over the common
groupoid.

## AMP relation lift

The imported AMP 03L certificate establishes over the same arrows:

- source-state covariance;
- target-state covariance;
- KK-row covariance;
- fibre covariance;
- deletion covariance;
- transmitted-image covariance;
- exact chart cocycles;
- the common six-space filtration
  \[
  V_0,V_2,V_8,V_9,V_{14},V_{15}.
  \]

Thus the amplitude relation system is a second exact lift over the same base.

## Middle-block growth naturality

The reference middle-block correspondence contains

\[
720
\]

parent-child incidences.

For every common arrow,

\[
\pi_{D\leftarrow C}(D_C)=D_D.
\]

All

\[
5184
\]

naturality checks pass.

## Exact scientific statement

> After adopting the same pullback chart convention, OPW3 dynamics and AMP
> relation transport are distinct exact functorial lifts over one finite
> 72-chart relabelling groupoid, and their shared middle-block growth
> correspondence is natural under every chart arrow.

## Claim boundary

This result does not construct:

- a natural transformation from AMP relation spaces to OPW slow eigenspaces;
- an isomorphism or equivalence of the two functors;
- categorical duality;
- a physical gauge bundle;
- a derivation of amplitudes from OPW dynamics.

“Dual functor” means two coordinated lifts over one base.
