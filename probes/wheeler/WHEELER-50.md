# WHEELER-50 — Internal Irreversibility / EHF Entropy Candidate Audit

## Question

Can EHF define a native entropy or information-loss quantity from its own observer coarse-graining and growth structure, without importing thermodynamic temperature or Landauer's principle?

## Setup

Use the zero-cost cyclic binary MICRO/Wheeler model.

- State: cyclic binary word `w` of length `n`.
- Zero-cost admissibility: no cyclic occurrence of `010` or `101`.
- Observable statistics:
  - `N1(w)=m`, the number of 1s.
  - `D(w)=2k`, the cyclic domain-wall count.
- Observer map:

  `pi(w)=(N1(w),D(w))`.

For `D=2k>0`, every zero-cost state has exactly `k` one-runs and `k` zero-runs, and every run has length at least 2.

## Candidate entropy

Define the observer-fiber multiplicity

`Omega_pi(y)=|pi^{-1}(y)|`

and the corresponding combinatorial observer entropy

`S_pi(y)=log Omega_pi(y)`.

This quantity uses only the EHF state space and observer partition. It is not a thermodynamic entropy claim.

## Exact fiber-count theorem

Let `m=N1` and `D=2k>0`. The number of labelled cyclic zero-cost binary words with macrostate `(n,m,2k)` is

`Omega(n,m,2k) = (n/k) * C(m-k-1,k-1) * C(n-m-k-1,k-1)`

provided

`m >= 2k` and `n-m >= 2k`.

Otherwise the fiber is empty.

### Derivation

A zero-cost state with `D=2k` consists of:

- `k` one-runs whose lengths are positive integers >=2 summing to `m`;
- `k` zero-runs whose lengths are positive integers >=2 summing to `n-m`.

The number of ordered compositions of `m` into `k` parts >=2 is

`C(m-k-1,k-1)`.

Similarly, the number of ordered zero-run compositions is

`C(n-m-k-1,k-1)`.

For a labelled cyclic word, there are `n` choices of absolute origin, while choosing a distinguished one-run start overcounts each word by the `k` one-run starts. Hence the prefactor `n/k`.

The formula was brute-force checked for every zero-cost state through `n=14`; no mismatches were found.

## Growth monotonicity theorem

Zero-cost growth preserves `D` and either

1. inserts `0`: `(n,m,2k) -> (n+1,m,2k)`, or
2. inserts `1`: `(n,m,2k) -> (n+1,m+1,2k)`.

For a 1-insertion,

`Omega(n+1,m+1,2k) / Omega(n,m,2k)`

`= ((n+1)/n) * ((m-k)/(m-2k+1))`.

Since `m>=2k`, both factors are positive and the ratio is strictly greater than 1.

For a 0-insertion,

`Omega(n+1,m,2k) / Omega(n,m,2k)`

`= ((n+1)/n) * (((n-m)-k)/((n-m)-2k+1))`,

which is also strictly greater than 1 because `n-m>=2k`.

Therefore

`Omega_{t+1} > Omega_t`

for every nontrivial zero-cost growth step with `D>0`, and hence

`S_pi(t+1) > S_pi(t)`.

### Result

**PROVED (conditional on the stated model and observer map):**

`S_pi = log |pi^{-1}(N1,D)|`

is a strict growth-monotone along every zero-cost growth history with `D>0`.

## Observer forgetting and information loss

Suppose an observer has a finer record `Y` and later replaces it by a deterministic coarsening `Z=f(Y)`. Then distinct `Y` records can merge into the same `Z` record. In finite state counting terms, the compatible microstate set cannot become smaller solely because information was discarded.

At the probabilistic level, if `X` is the substrate microstate, the hidden-state uncertainty satisfies the standard information inequality

`H(X|Z) >= H(X|Y)`

for deterministic forgetting `Z=f(Y)`.

Thus EHF supplies a native notion of **observer-relative information loss** through many-to-one record maps, independent of thermodynamic interpretation.

## What this does and does not establish

### Established

1. A natural internal combinatorial entropy can be defined from observer fibers.
2. For the `(N1,D)` observer in the zero-cost growth model, its exact fiber multiplicity is known analytically.
3. This entropy is strictly monotone under every allowed growth step with `D>0`.
4. Additional observer forgetting increases or preserves hidden-state uncertainty.

### Not established

1. This is not yet thermodynamic entropy.
2. No temperature, heat, energy, or second law of physics has been derived.
3. The monotonicity is observer-partition dependent; a different observer map can have different fiber behavior.
4. The entropy counts compatible microstates, not necessarily the observer's actual nonuniform posterior. A Shannon-posterior entropy requires a probability measure.
5. `D=0` is degenerate: the only zero-cost states are uniform words, so the fiber structure is trivial.

## Interpretation

The strongest defensible statement is:

> EHF admits an internally defined, observer-relative combinatorial entropy whose increase can be proved from growth alone in a concrete model.

This is stronger than importing Landauer after the fact, but weaker than deriving thermodynamics.

The result suggests a possible hierarchy:

`substrate multiplicity -> observer coarse-graining -> combinatorial entropy -> probabilistic entropy -> thermodynamic interpretation`

Only the first two arrows are established here.

## Verdict

- **PASS / PROVED:** exact `(N1,D)` fiber-count formula.
- **PASS / PROVED:** strict monotonicity of `log Omega` under zero-cost growth for `D>0`.
- **PASS:** many-to-one observer forgetting supplies a native information-loss quantity.
- **NEGATIVE:** this does not yet constitute a derivation of thermodynamic entropy.
- **OPEN:** determine whether a probability measure naturally induced by EHF dynamics gives a Shannon entropy with a comparable monotonicity law.

## Next probe

**WHEELER-51 — Dynamic Measure / Shannon-Entropy Audit**

Derive the actual probability distribution over microstates generated by equal local growth rates and test whether observer posterior entropy, relative entropy, or another measure-theoretic quantity is monotone without assuming a uniform distribution over observer fibers.
