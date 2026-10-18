# WHEELER-44 — Intrinsic Resource Law Audit

> **Review correction — 18 October 2026:** The Beta-law Chernoff information concerns an **infinite-growth limiting observation**. Cost-normalized optima are conditional proxy calculations. In particular, dividing that information by work for one growth event does not define a finite-budget experiment. A common Core-C/MICRO state space and generator are also required before combining their event counts as one endogenous model. See [ERRATA-01](ERRATA-01.md).

## Question
Can the resource cost used in WHEELER-42/43 be derived from already-existing EHF structures rather than imposed as an external power law?

We keep the same discrimination problem between hidden sectors D=2 and D=4 and use the edge preparation family N1,0=4 (or its bit-flipped equivalent N1,0=n0-4), which was optimal per run in WHEELER-41.

For this family:

- D=2 gives p_infinity ~ Beta(5, n0-3)
- D=4 gives p_infinity ~ Beta(6, n0-2)

Let C_Ch(n) be the Chernoff information between these two laws. As found previously, C_Ch(n) increases with n and tends to the finite ceiling C_infinity ≈ 0.02497.

## EHF-native candidate counts
Two size-dependent quantities already exist independently in EHF:

1. Growth opportunities

   G_n = n

   from the all-slot insertion rule.

2. Core-C comparison opportunities

   d_n = n(n-3)/2

   from the degree of the Core-C / 2-opt Hamilton-cycle comparison graph.

A third natural count is their sum,

   B_n = G_n + d_n.

These are structural opportunity counts. They are not automatically identical to physical, computational, energetic, or observational cost.

## Audit A — current-layer growth-site exposure
Define resource efficiency

   eta_G(n) = C_Ch(n) / G_n = C_Ch(n)/n.

The optimum is

   n = 21,

with

   C_Ch ≈ 0.01063077,
   eta_G ≈ 5.0623e-4.

This exactly reproduces WHEELER-42's linear-cost optimum, but now the linear scaling has an EHF-native candidate interpretation: paying once per available growth site at the prepared layer.

Verdict: CONDITIONAL PASS. The scaling n is native, but the statement that each available growth site contributes one unit of preparation/observation cost is still an operational assumption.

## Audit B — current-layer comparison exposure
Define

   eta_C(n) = C_Ch(n) / d_n.

The optimum over the shared feasible family n >= 8 is

   n = 8.

At n=8,

   C_Ch ≈ 0.00226481,
   d_8 = 20,
   eta_C ≈ 1.1324e-4.

Because d_n grows quadratically while C_Ch(n) saturates, larger preparations rapidly lose efficiency.

Verdict: CONDITIONAL PASS. Core-C supplies a native quadratic opportunity count, but interpreting every admissible comparison as paid resource is again protocol-dependent.

## Audit C — combined current local-event exposure
Use

   B_n = n + n(n-3)/2.

Then

   eta_B(n) = C_Ch(n) / B_n.

The optimum is again

   n = 8,

with

   B_8 = 28,
   eta_B ≈ 8.0886e-5.

The quadratic comparison count dominates asymptotically.

## Audit D — cumulative exposure along growth
An actual preparation from a smaller layer may incur cost at every intermediate layer, not merely at the final layer.

Using n=8 as the first layer at which both D=2 and D=4 edge preparations are feasible, define

   G_cum(n) = sum_{k=8}^n k,

   C_cum(n) = sum_{k=8}^n k(k-3)/2.

For efficiencies C_Ch/G_cum, C_Ch/C_cum, and C_Ch/(G_cum+C_cum), the optimum is the smallest feasible layer,

   n = 8.

Thus cumulative opportunity exposure penalizes enlargement even more strongly than current-layer exposure.

## Main result
EHF does contain natural size-dependent structural counts, but they do not define a unique scalar resource law by themselves.

The same substrate supplies at least the following distinct candidate scalings:

- growth-site count: O(n),
- comparison-opportunity count: O(n^2),
- cumulative growth-site exposure: O(n^2),
- cumulative comparison exposure: O(n^3).

Each is mathematically natural under a different operational interpretation.

Therefore:

   EHF primitives -> natural resource-count families

but not yet

   EHF primitives -> unique observer/preparation cost.

The preferred operational scale consequently remains protocol-dependent:

- growth-site exposure selects n≈21,
- comparison or cumulative exposure selects the smallest shared feasible system n=8.

## Interpretation
This is an important negative constraint.

A preferred experimental or observer scale should not be called intrinsic to the substrate merely because it can be computed from an EHF-native count. One must first derive which opportunities are actually consumed, weighted, or timed by the observer/preparation protocol.

The distinction is:

   structural opportunity count != resource cost

unless an additional operational law connects them.

## Verdict
- PASS: EHF already supplies native O(n) and O(n^2) structural opportunity counts.
- PASS: using G_n=n as current-layer site exposure reproduces the finite optimum n=21 without an arbitrary power-law exponent.
- PASS: using Core-C comparison exposure selects n=8.
- NEGATIVE: the substrate counts do not uniquely determine one resource law.
- NEGATIVE: no observer-independent preferred scale has yet been derived.
- OPEN: derive a resource measure from an explicit internal observer/preparation dynamics rather than choosing which opportunity count is charged.

## Next logical probe
WHEELER-45 — Internal Observer Budget / Endogenous Cost Audit.

Specify an observer as part of the substrate with a finite event budget and explicit access to growth/comparison events. Derive the effective resource measure from what that observer must actually process, then test whether a preferred scale survives without externally selecting the cost functional.
