# Wheeler review corrections — 18 October 2026

Based on [REVIEW-01](../../research/wheeler/REVIEW-01.md), which audited snapshot `106783d120bf5895cdcd67c8086ab382feebfb8c`.

This record governs the current interpretation of the affected earlier reports. Historical reasoning is preserved in Git; correction notices identify claims requiring stronger assumptions. WHEELER-49 has been replaced by its corrected argument.

| Reports | Correction | What survives |
|---|---|---|
| 11–12 | A concrete construction is still needed to derive the asserted unit boundary current from reversal | Algebra of the assumed transfer rule |
| 25 | Expander conclusion already withdrawn in 26; now flagged at the point of use | Corrected Core-C gap in 26–28 |
| 29–31 | Growth hazard R_G is not comparison hazard R_C without a specified coupling | Linear growth hazard under local-clock assumptions; conditional fixed-layer gap |
| 32 | Exponential holding times need a suitable pure-jump model, not merely any Markov semigroup | Pure-jump conditional argument |
| 34–37 | Failure of strong lumpability is not failure of Markov behaviour for every preparation | Exact criterion; W37's fixed-preparation endpoint sufficiency |
| 37 | Timed likelihood must include exponential density rate factors, which cancel the embedded-chain denominator | Endpoint plus elapsed-time posterior compression |
| 40–46 | Infinite-trajectory information and one-event costs cannot establish a finite-budget optimum; Core-C/MICRO competition needs a common model | Proxy optimizations and conditional event-count calculations |
| 47–48 | Counter complexity needs an explicit computational/access model | Conditional memory/processing tradeoff |
| 49 | Register capacity is not erased entropy; capacity-based lower bound withdrawn | Conditional Landauer entropy accounting |
| 53 | Correct example: P(11000)≈0.655492, P(11100)≈0.344508 | Entropy-decrease counterexample |
| 56–57 | Event primacy alone does not force equal rates; maximum entropy/event symmetry is additional | Conditional uniform-event theorem and push-forward |

## Reproducibility

- [Review code](../../code/wheeler/review_audit.py)
- [Review output](../../data/wheeler/review-01-results.json)
- [WHEELER-58 exact checks](../../code/wheeler/projective_audit.py)
- [WHEELER-58 output](../../data/wheeler/wheeler-58-results.json)

The tests support the explicit MICRO combinatorics and entropy claims within their stated conventions. They are not certification of all experiments described in every report.

## Current continuation

[WHEELER-58](WHEELER-58.md) constructs a consistent event-history process, proves consistency of compatible observer projections, and shows that state-uniform dynamics also passes the horizon-consistency test. This strengthens process construction while ruling out consistency alone as unique measure selection.
