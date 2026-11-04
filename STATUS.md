# EHF Status

Last consolidated: 2026-10-19 (Australia/Brisbane)

## Programme status

EHF is an exploratory constrained-combinatorial research programme, not an established theory of physics.

## Strongest current themes

### 1. Admissible transformations and histories
**Status: FOUNDATIONAL / ACTIVE**

The recurring EHF primitive is not a particle, field, geometry, or spacetime. It is a constrained space of distinguishable configurations together with admissible comparisons and transformations. Histories through this structure are treated as potentially more fundamental than object identity at a single state.

### 2. Spectral structure and transport
**Status: COMPUTATIONAL + ANALYTIC TARGET**

Several EHF graph families have shown structured spectra and nontrivial gap behaviour. This is currently one of the most physics-relevant directions because spectral gaps connect naturally to relaxation, transport, mixing, and effective continuum behaviour.

### 3. Growth and changing state spaces
**Status: ACTIVE / PARTLY SPECULATIVE**

EHF permits state-space enlargement rather than assuming a permanently fixed number of degrees of freedom. The important open question is whether growth can be forced intrinsically by admissibility rather than inserted as an external rule.

### 4. Internal observers, records, and time
**Status: ACTIVE / CONJECTURAL**

EHF investigates whether observers and clocks can be defined internally through persistent records and ordered histories, without assuming an external time coordinate.

### 5. Hamilton-history / Wheeler probes
**Status: REVIEWED IN PART; WHEELER-63 BOUNDED EXTENSION COMPLETE**

The strongest current results concern the explicitly defined zero-cost MICRO growth process: exact insertion counts, observer macro kernels, conditional entropy monotonicity, and consistent probability measures on histories. An independent reconstruction reproduced state/component counts and growth checks through n=14; the review does not certify every earlier experiment.

WHEELER-58 proves horizon consistency for a fixed preparation and compatible observer projections. In the rooted/labelled representation, nonhomogeneous states have exactly D+1 distinct successors. Both event-uniform and state-uniform maximum-entropy history constructions are consistent, so consistency alone does not select a probability measure.

WHEELER-59 proves rotation lumpability for event-uniform growth and exhibits root dependence of rooted state-uniform growth. Rotation invariance still does not select a unique kernel. Ordinary quotient majorization is falsified by an exact n=12 counterexample; entropy monotonicity survives with orbit-size reference weights. WHEELER-60 falsifies universal ordinary class Shannon monotonicity with an exact two-source preparation at n=204: entropy falls by 0.0586400757 bits, with an integer sign certificate. The inherited orbit-weighted entropy increases. WHEELER-61 then gives a single-seed unconditioned counterexample: `(2,100,2,100)` loses 0.0136737948 bits from event 2 to 3, certified by rational logarithm bounds. An exact symmetry correction explains the change. WHEELER-62 proves strict entropy increase for the minimal seed `(2,2,2,2)` at every event, using an exact periodicity bound and an ordered-run entropy-production estimate. Its leading entropy growth is `3 log₂ t + O(1)`. This is a preparation-specific theorem, not a reversal of the other-seed counterexample.

The Core-C graph gap is n−1 for the specified Hamilton-cycle/2-opt graph; its normalized gap tends to zero. A growth-site clock does not automatically set the comparison rate. The earlier universal counter-reset heat bound is withdrawn because memory capacity is not erased entropy. Finite-resource inference optima remain conditional proxy calculations where infinite-history information was paired with one-event cost.

See [WHEELER-62](probes/wheeler/WHEELER-62.md), [WHEELER-61](probes/wheeler/WHEELER-61.md), [WHEELER-60](probes/wheeler/WHEELER-60.md), [WHEELER-59](probes/wheeler/WHEELER-59.md), [WHEELER-58](probes/wheeler/WHEELER-58.md), [ERRATA-01](probes/wheeler/ERRATA-01.md), [REVIEW-01](research/wheeler/REVIEW-01.md), and [reproducible checks](code/wheeler/README.md).

[WHEELER-63](probes/wheeler/WHEELER-63.md) records the full stabilizer correction and positive finite scans for minimal seeds with D=6,8,10. These are not all-time proofs. [Working paper v0.1](research/wheeler/paper-v0.1/README.md) is prepared for review. External proof review and comparison against Nakata’s full classification remain pending. Clock-coupling and finite-resource repairs are separate tasks.

## Evidence hierarchy

EHF claims must carry one of these tags:

- PROVED
- COMPUTATIONAL
- EMPIRICAL PATTERN
- CONJECTURE
- SPECULATIVE
- FALSIFIED / NEGATIVE

## Near-term criterion for meaningful progress

The next major milestone is to derive at least one recognizable effective law from microscopic EHF rules without putting that law in by hand. Candidate targets include diffusion, conservation laws, internal-clock dynamics, effective metric structure, or controlled unitary/quantum-walk-like evolution.

## QM bridge update — 2026-11-04

**Status: COMPUTATIONAL + ANALYTIC ARGUMENTS / NEGATIVE CONTROL.**

[Revisit 01](probes/qm-bridge/revisit-01/README.md) rebuilds a locally readable six-state carrier and distinguishes stochastic evolution from an explicitly supplied coherent control. [Revisit 02](probes/qm-bridge/revisit-02/README.md) constructs orientation transport from actual LR2/LR3 histories: 3 of 15 representative n=7 components and 9 of 111 representative n=9 components contain negative closed walks. The original six-state component is flat. A parity argument excludes equal-length opposite-sign paths at n=7; the n=9 seed exhibits them after five moves. A separate oriented-tour verifier reproduces the finite counts and exact rational probabilities.

The signed evolution is exactly the orientation difference of a nonnegative classical lifted process. Its squared norm is not conserved. This supplies reproducible transport structure and controls; physical phase access, coherent recombination, a derived Born rule and physical QM remain unestablished. No general-size classification or external novelty review is claimed.


## QM bridge operational-access update — 2026-11-04

**Status: COMPUTATIONAL + ANALYTIC ARGUMENTS / CLASSICAL CONTROL.**

[Revisit 03](probes/qm-bridge/revisit-03/README.md) represents a directional reference by ordered adjacent markers and transports them with actual carrier endpoint swaps. The matched unordered preparations are identical; a role-sensitive port reader distinguishes them. A live first-port reader retains timeouts and reaches exact finite classification success 0.6830468891 at 12 ticks, or 0.7028698275 for the specified marker-position-gated control. All 1,008 n=7 and 38,880 n=9 ordered-marker states receive role-forgetting kernel checks; an independent slot-based implementation reproduces the finite counts and live-reader laws.

This is a conditional classical access result: markers, their co-transport, the named port and detector are supplied. The unmarked carrier has not generated an intrinsic readable phase, and no quantum probability rule or unitary dynamics is derived. Rate sweeps alone would not close that gap.
