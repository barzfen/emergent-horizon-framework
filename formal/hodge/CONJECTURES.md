# EHF MICRO square-complex working conjectures

Date: 2026-10-20 (Australia/Brisbane)

**Status: CONJECTURE. Exact finite support for n=5,...,18; no all-size proof
and no claim of novelty in the mathematical literature.**

## Definition lock

For each integer n>=5:

- Vertices are rooted, labelled binary words on the oriented n-cycle with
  no cyclic 010 or 101 pattern.
- An edge is a non-self length-three reversal whose result is valid.
  Duplicate neighbours are identified.
- Attach one square for each distinct four-state commuting relation of
  moves with disjoint swapped endpoint sets, provided both orders are valid.
  Deduplicate square boundaries under cyclic rotation and reversal.
- No other faces or higher cells are attached. Call the complex X_n.
- A moving component C is a connected component containing at least one edge.

This is the precise complex of [HODGE-02](../../probes/hodge/HODGE-02.md).
HODGE-03 proves its endpoint-square rule equals the window-disjoint rule
for all n>=5.

On a directed edge w -> tau_i(w), define the closed cochains

`j = 2(w_i-w_(i+2)),`
`kappa = +1 if w_i=w_(i+1), and -1 otherwise.`

The latter counts signed displacement of a 01 run boundary.
Both reverse sign on edge reversal and have integral loop periods
divisible by n. They represent classes in H^1(C;Q).

The component has fixed number m of 1 values and fixed number D of runs
(domain walls). For a moving component, E=n-2D>0.

## EHF-HODGE-C1 — Single rational homology direction

For every n>=5 and every moving component C of X_n,

`dim_Q H_1(C;Q)=1,`

and the boundary-winding period map

`[gamma] -> (1/n) sum_gamma kappa`

is nonzero. Equivalently, it is an isomorphism of one-dimensional rational
vector spaces H_1(C;Q) -> Q.

**This does not assert:** H_1(C;Z)=Z; absence of torsion; a primitive
integral winding generator; fundamental group Z; or homotopy equivalence
to a circle.

A finite counterexample is any moving component with rational beta1
different from 1 or with zero kappa period on every loop.

## EHF-HODGE-C2 — Binary/boundary period relation

For every n>=5 and every moving component C of X_n,

`(n-2D)[j] = 2(n-2m)[kappa] in H^1(C;Q).`

Equivalently, for every closed graph path gamma in C,

`(n-2D) sum_gamma j = 2(n-2m) sum_gamma kappa.`

The equivalence uses the graph period criterion for exact cochains.
This is a separate claim from C1.

If true, C2 explains why balanced components (m=n/2) have zero binary
period even when boundary winding is nonzero. It also gives the ratio

`sum j / sum kappa = 2(n-2m)/(n-2D)`

whenever the denominator period is nonzero.

A finite counterexample is a fundamental graph cycle violating the
integer equality. Fundamental cycles suffice because they span the
graph cycle space.

## Evidence

[HODGE-03](../../probes/hodge/HODGE-03.md) exhaustively audits 200 moving
components across n=5,...,18. Every one satisfies C1 and C2.
All ranks, face checks and periods are exact. Earlier sizes are retained
as consistency controls. This is evidence, not proof by induction.

The boundary-winding image need not equal Z integrally. For example,
some n=11 components have image 3Z. This does not contradict C1 over Q.

## What must happen before stronger claims

- Derive an all-size classification from the run-coordinate dynamics,
  or find a counterexample.
- For C2, construct a state potential for
  (n-2D)j-2(n-2m)kappa, or supply another all-size argument.
- Compare the exact model with existing reconfiguration/state-complex
  and constrained transport literature before claiming originality.
- Keep the Clay Hodge conjecture separate: no smooth projective variety,
  rational (p,p) identification, or algebraic cycle map has been derived.
