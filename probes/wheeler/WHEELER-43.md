# WHEELER-43 — Resource-Scaling / Cost-Exponent Audit

> **Review correction — 18 October 2026:** The Beta-law Chernoff information concerns an **infinite-growth limiting observation**. Cost-normalized optima are conditional proxy calculations. In particular, dividing that information by work for one growth event does not define a finite-budget experiment. A common Core-C/MICRO state space and generator are also required before combining their event counts as one endogenous model. See [ERRATA-01](ERRATA-01.md).

## Question

Generalize the WHEELER-42 preparation-cost model from linear cost to

\[
C_{\rm prep}(n_0) \propto n_0^\alpha
\]

and determine how the optimal preparation changes with the exponent \(\alpha\) for discrimination between hidden sectors \(D=2\) and \(D=4\).

The observer uses the asymptotic growth-fraction statistic from the Pólya-urn representation. For shared-feasible preparations, the best composition remains at the boundary

\[
N_{1,0}=4
\]

or symmetrically \(N_{1,0}=n_0-4\).

For the boundary preparation \((n_0,4)\),

\[
D=2:\quad p_\infty\sim \mathrm{Beta}(5,n_0-3),
\]

\[
D=4:\quad p_\infty\sim \mathrm{Beta}(6,n_0-2).
\]

Let \(C_{\rm Ch}(n_0)\) denote the Chernoff information between these two Beta laws. The resource-efficiency objective is

\[
\eta_\alpha(n_0)=\frac{C_{\rm Ch}(n_0)}{n_0^\alpha}.
\]

## Asymptotic structure

WHEELER-41 established that

\[
C_{\rm Ch}(n_0)\to C_\infty\approx 0.02497
\]

as \(n_0\to\infty\). Therefore:

- if \(\alpha=0\), resource cost does not increase with size and larger preparations approach the finite information ceiling;
- if \(\alpha>0\), \(\eta_\alpha(n_0)\to0\), so a finite optimal preparation must occur;
- if \(\alpha<0\), the assumed cost decreases with system size, so the objective is driven toward arbitrarily large preparations and the cost model is physically unusual.

Thus the threshold is

\[
\boxed{\alpha_c=0}.
\]

Any strictly positive size penalty is enough to convert the infinite-size optimum into a finite-size optimum.

## Numerical audit

The Chernoff information was evaluated for integer \(n_0\ge 8\) along the optimal boundary composition and \(\eta_\alpha\) was maximized numerically.

Representative results:

| \(\alpha\) | optimal \(n_0\) | \(C_{\rm Ch}(n_0)\) | \(\eta_\alpha\) |
|---:|---:|---:|---:|
| 0 | grows without finite maximizer | approaches 0.02497 | approaches 0.02497 |
| 0.05 | 307 | 0.02376 | 0.01785 |
| 0.10 | 157 | 0.02264 | 0.01366 |
| 0.25 | 66 | 0.01965 | 0.006895 |
| 0.50 | 36 | 0.01577 | 0.002628 |
| 0.75 | 26 | 0.01286 | 0.001117 |
| 1.00 | 21 | 0.01063 | 0.0005062 |
| 1.25 | 18 | 0.008903 | 0.0002401 |
| 1.50 | 16 | 0.007545 | 0.0001179 |
| 2.00 | 8 | 0.002265 | 0.00003539 |

The optimum moves monotonically toward smaller preparations as the resource penalty steepens.

## Interpretation

The important structural distinction is between raw distinguishability and resource-efficient distinguishability.

Raw discrimination improves with preparation size but saturates at a finite ceiling. Therefore even a very weak positive size cost eventually dominates the marginal information gain. The observer-design problem acquires a finite preferred scale for every \(\alpha>0\).

This gives a simple example of an emergent operational scale without inserting a preferred \(n_0\) directly into the microscopic rule. The preferred scale is not universal: it arises from the interaction between the substrate's saturating information law and the observer's resource-cost law.

This should not be interpreted as a physical length scale or mass scale. It is an operational optimum in this explicitly defined statistical toy model.

## Verdict

- **PROVED from asymptotic structure:** if \(C_{\rm Ch}(n_0)\to C_\infty>0\), then every \(\alpha>0\) gives \(\eta_\alpha(n_0)\to0\), hence the large-size optimum is removed.
- **COMPUTATIONAL:** optimal finite \(n_0\) values listed above for representative \(\alpha\).
- **PASS:** critical cost exponent \(\alpha_c=0\).
- **PASS:** increasing resource exponent shifts the optimum toward smaller preparations.
- **CAUTION:** the preferred scale is observer/resource-model dependent, not yet a substrate-intrinsic physical scale.

## Next probe

WHEELER-44 should ask whether an intrinsic resource law can be derived from EHF itself rather than supplied externally. Candidate costs include comparison count \(d_n\sim n^2/2\), growth-site count \(n\), internal event-time cost, or a combined preparation-plus-observation cost. If one of these is forced by the framework, the resulting optimal scale would be substantially more meaningful than an arbitrarily chosen \(n^\alpha\) penalty.
