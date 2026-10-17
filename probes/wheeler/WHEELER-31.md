# WHEELER-31 — Internal-Time Generator / Additivity Audit

## Question
Can the additive local-rate rule used in WHEELER-30 be derived from composition principles rather than imposed as a clock convention?

## Setup
Let `S_A(t)` denote the probability that no admissible elementary event occurs in subsystem A during an internal-time interval of length t.

Assume:

1. **Time-homogeneous composition**: splitting an interval does not change the prediction,
   `S_A(t+s)=S_A(t) S_A(s)`.
2. **Continuity** at t=0, with `S_A(0)=1`.
3. **Independence for disjoint subsystems**: if A and B share no active local support and do not constrain each other during the interval,
   `S_{A⊔B}(t)=S_A(t) S_B(t)`.
4. **Locality**: the elementary rate attached to a local opportunity does not depend on remote system size or labels.
5. **Relabelling symmetry**: equivalent growth sites carry the same elementary rate.

These assumptions concern operational event records; no background spacetime is required.

## Derivation
The functional equation

`S_A(t+s)=S_A(t)S_A(s)`

plus continuity implies

`S_A(t)=exp(-R_A t)`

for some nonnegative rate `R_A`.

For disjoint independent A and B,

`exp[-R_{A⊔B} t] = S_{A⊔B}(t) = S_A(t)S_B(t) = exp[-(R_A+R_B)t]`,

hence

`R_{A⊔B}=R_A+R_B`.

Therefore the infinitesimal generator is additive on independent disjoint event supports.

For n equivalent elementary growth sites with local rate r,

`R_n = Σ_i r_i = n r`.

This recovers the WHEELER-30 rate law without independently postulating total-rate additivity.

## Consequence for Core C
Using

`d_n = n(n-3)/2`

and the exact combinatorial Laplacian gap

`λ_n = n-1`,

the rate-normalized continuous-time gap is

`Δ_n = R_n λ_n / d_n`.

With `R_n = n r`,

`Δ_n = 2 r (n-1)/(n-3)`,

so

`lim_{n→∞} Δ_n = 2r > 0`.

The only free parameter r is an overall time-unit scale.

## What has and has not been derived

### Derived, conditional on the stated axioms
- Exponential no-event law from time-homogeneous composition and continuity.
- Additivity of rates for independent disjoint subsystems.
- `R_n = n r` for n equivalent local growth opportunities.
- A finite limiting Core-C rate-normalized gap `2r`.

### Not derived
- That EHF internal time must be Markov/time-homogeneous.
- That all admissible local opportunities are statistically independent when disjoint.
- That history-dependent or cooperative clocks are impossible.
- Any identification of the finite relaxation gap with a physical particle mass or the Yang–Mills mass gap.

## Verdict
**PARTIAL PASS / CONDITIONAL DERIVATION.**

The additive-rate rule is not an arbitrary normalization if EHF internal time satisfies operational time-homogeneity, continuity, and independence of disjoint local events. Under those assumptions, additivity follows mathematically and WHEELER-30's linear total rate is forced up to one global clock constant.

The next unresolved issue is whether the semigroup/Markov property itself can be derived from EHF observer-record and history-composition primitives rather than assumed.

## Suggested next probe
**WHEELER-32 — Record Composition / Markov-Naturality Audit**

Test whether consistent observer records and concatenation of admissible histories force a time-homogeneous semigroup, or whether EHF naturally permits memory kernels/history-dependent clocks.