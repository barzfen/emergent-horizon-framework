# WHEELER-32 — Record Composition / Markov-Naturality Audit

## Question
Does EHF history/record composition force the semigroup law used in WHEELER-31, or can internal time retain memory?

## Setup
Let H_t denote an admissible history segment of internal duration t. History concatenation is associative whenever endpoints match:

(H_t ∘ H_s) ∘ H_u = H_t ∘ (H_s ∘ H_u).

Let R_t denote the observer-accessible present record at internal time t. We ask whether future event statistics depend only on R_t or also on hidden details of the earlier history.

## Result 1 — Associative history composition is not enough
Associativity of concatenation only says that admissible history segments can be composed consistently. It does not imply a factorization of survival/no-event probabilities of the form

S(t+s) = S(t) S(s).

Therefore the semigroup law used in WHEELER-31 is not derivable from path composition alone.

## Result 2 — The missing condition is record sufficiency
Suppose the present record R_t is sufficient in the sense that, conditional on R_t, future admissible-event statistics are independent of the detailed pre-t history. Then

P(future | full past) = P(future | R_t).

This is the Markov property with the observer record as state.

Under time-homogeneity, the corresponding transition kernels satisfy

K_{t+s} = K_t K_s,

and the no-event survival function satisfies

S(t+s) = S(t) S(s).

Continuity then gives exponential waiting times and the additive-rate result of WHEELER-31.

## Result 3 — EHF presently permits non-Markov clocks
Existing EHF work contains memory-like observables, observer records, growth history and hidden lift/history labels. None of these are presently proved to be fully encoded by the instantaneous coarse observer record.

Therefore two histories can in principle arrive at the same visible record while retaining different hidden future hazards. In that case the correct effective dynamics can have a memory kernel rather than a semigroup generator.

Schematically,

dp/dt = ∫_0^t K(t-s) p(s) ds,

rather than dp/dt = L p(t).

Thus non-Markov internal time remains admissible.

## Important refinement
A non-Markov coarse description can often be made Markov by enlarging the state to include enough memory variables. Therefore the meaningful question is not whether coarse observer data are Markov, but whether the full EHF state tuple is sufficient.

This suggests a hierarchy:

1. microscopic/full-state dynamics may be Markov;
2. observer-projected dynamics may be non-Markov because information is hidden;
3. restoring the omitted record/memory variables may recover a semigroup.

## Consequence for the gap argument
The WHEELER-28 to WHEELER-31 finite-gap chain is valid if the state used by the generator is sufficient and time-homogeneous. It is not forced by history concatenation alone.

Therefore the present status is:

- Associative history composition: PASS.
- Semigroup from composition alone: FAIL.
- Semigroup from sufficient present state plus time-homogeneity: PASS.
- Full EHF state proved sufficient: UNRESOLVED.
- Non-Markov observer-level dynamics: ALLOWED.

## Next probe
WHEELER-33 — State-Sufficiency / Markov-Lift Audit.

Take the established EHF state tuple and ask whether it can be defined so that all future admissibility and growth rules depend only on the present full state. If yes, Markovianity can be recovered at the substrate level while memory emerges only after observer coarse-graining.
