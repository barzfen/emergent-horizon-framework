# Emergent Horizon Framework (EHF)

EHF is an exploratory mathematical-physics research programme investigating whether effective geometry, time, observers, information, and physical-law-like behaviour can emerge from constrained combinatorial histories whose primitive structure is admissible comparison and transformation.

## Research discipline

EHF distinguishes sharply between:

- **PROVED** — established analytically from stated assumptions.
- **COMPUTATIONAL** — reproduced numerically/computationally but not yet proved.
- **EMPIRICAL PATTERN** — suggestive regularity requiring stronger validation.
- **CONJECTURE** — precise claim not yet established.
- **SPECULATIVE** — conceptual possibility or analogy, not evidence.
- **FALSIFIED / NEGATIVE** — tested and not supported under the stated model.

The repository is intended to preserve both positive and negative results and to separate demonstrated mathematics from physical interpretation.

## Current priorities

1. Formalize the minimal substrate: configurations, admissibility, transformations, growth, and histories.
2. Consolidate previous EHF probes and identify which results survive audit.
3. Derive recognizable effective laws from microscopic rules rather than identifying analogies after the fact.
4. Study spectral gaps, transport, internal time/records, topology, and observer-relative descriptions.
5. Maintain explicit separation between mathematical result and proposed physical interpretation.

## Repository map

- `STATUS.md` — current assessment of the programme and strongest results.
- `ROADMAP.md` — immediate research priorities and falsification targets.
- `foundation/` — primitives and foundational definitions.
- `formal/` — definitions, lemmas, conjectures, and proved results.
- `research/` — topic-oriented research notes.
- `probes/` — individual computational and analytic probes.
- `code/` — reproducible probe code.
- `data/` — retained datasets that cannot be cheaply regenerated.
- `archive/` — superseded or speculative material retained for provenance.

## Current status

EHF is **not** an established physical theory. Its present value is as a constrained combinatorial research framework with several mathematically nontrivial results and testable emergence questions.

The standard for progress is increasingly strict: a useful EHF result should either prove a structural property, survive reproducible computation, derive an effective law, or clearly falsify a proposed mechanism.

## Latest Wheeler work

[Entropy and Symmetry in Constrained Cyclic Growth — working paper v0.1](research/wheeler/paper-v0.1/README.md) consolidates the proofs, counterexamples and literature comparison. [WHEELER-63](probes/wheeler/WHEELER-63.md) adds bounded many-domain checks. External proof review and the full Nakata comparison remain pending.

[Summary through WHEELER-62](research/wheeler/SUMMARY-01.md): strongest mathematical results, physics relevance, provisional novelty assessment and a plain-language account.

[WHEELER-62](probes/wheeler/WHEELER-62.md) proves strict ordinary rotation-class entropy increase at every growth event from the minimal seed `(2,2,2,2)`, with leading growth `3 log₂ t + O(1)`. An exact periodicity bound controls the symmetry correction. This is preparation-specific: [WHEELER-61](probes/wheeler/WHEELER-61.md) retains its certified decrease from a different deterministic seed. Rooted and orbit-weighted entropy theorems remain valid.

Read [ERRATA-01](probes/wheeler/ERRATA-01.md) before relying on earlier clock, observer-cost, erasure or measure-selection claims. The [review](research/wheeler/REVIEW-01.md) and [reproducible checks](code/wheeler/README.md) record what was and was not independently verified.

## Tail theorem and MICRO observer audit

- [Nine-point odd-to-even tail theorem, draft v1.5](research/amplitudes/nine-point-tail/README.md): original note and an independent exact reconstruction, with its verification scope stated explicitly.
- [MICRO observer compatibility audit 01](probes/micro/observer-compatibility-01/README.md): exact observer tests, analytic growth formula and a visual counterexample showing why block count can matter.

These are separate mathematical investigations; a connection between them or to physical dynamics remains unproved.


## AI-assisted literature follow-up

[Related work and reproducible follow-up probes](research/related-work/README.md) records external papers, their precise relationship to EHF, and positive or negative probe results. The first entry audits Hamiltonian reconfiguration and distinguishes inaccessible sectors from memory-like persistence.

## Licensing, citation and contributions

Original code is available under MIT; original research notes, documentation and figures use CC BY 4.0. File-specific and third-party terms take precedence. See [licensing scope](LICENSE.md), [citation metadata](CITATION.cff) and [contribution and attribution guidance](CONTRIBUTING.md). We credit the researchers whose results, methods and materials inform this work and welcome reproducible findings that we can contribute back.
