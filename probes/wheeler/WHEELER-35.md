# WHEELER-35 — Observer Partition / Lumpability Audit

## Goal
Test an actual EHF observer/coarse-graining map for Markov lumpability under the existing zero-cost MICRO growth rule.

## Substrate
- State: cyclic binary word `w`.
- Zero-cost admissibility: forbid cyclic occurrences of `010` and `101`.
- Growth: insert one bit `0` or `1` at any slot, retaining zero cost.
- Equal local growth rates per admissible insertion event.

## Observer map A: retain `(N1,D)`
Let
- `N1(w)` = number of ones;
- `D(w)` = cyclic domain-wall count.

For each zero-cost state through `n=12`, aggregate all admissible growth events by the next observer macrostate `(N1',D')`.

Result: no violations of strong lumpability were found for `n=4,...,12`.

Equivalently, whenever two zero-cost words share the same `(N1,D)`, their total growth rates into each possible `(N1',D')` class agree in the tested range.

This matches the structural growth law already established in WHEELER-20:
- `Delta D = 0` exactly;
- `Delta N1 in {0,1}`.

Thus `(N1,D)` behaves as a sufficient observer state for this growth process over the tested range.

Status: **COMPUTATIONAL PASS through n=12**. A general proof remains open.

## Observer map B: retain only `N1`
Now erase `D` and let the observer see only the Hamming weight `N1`.

The first strong-lumpability failure occurs at `n=8`, `N1=4`.

Two zero-cost substrate states that are observationally identical under `N1` are:

- `00001111`, with `D=2`;
- `00110011`, with `D=4`.

For `00001111`, admissible growth-event counts are:
- to `N1'=4`: 5 events;
- to `N1'=5`: 5 events.

For `00110011`, admissible growth-event counts are:
- to `N1'=4`: 6 events;
- to `N1'=5`: 6 events.

Therefore the aggregate transition hazards depend on hidden `D` even though the observer sees the same current `N1=4`.

Hence the projection `w -> N1(w)` is not lumpable.

## Interpretation
This gives a concrete EHF example of emergent observer memory from coarse-graining:

`full zero-cost word -> (N1,D)` is Markov-compatible in the tested range,
while
`full zero-cost word -> N1` is not.

So the domain-wall variable `D` acts as a hidden sufficient variable for the coarser observer. If the observer omits it, future growth statistics depend on the posterior distribution over hidden `D`, which is history-dependent.

This is stronger than an analogy to memory: the Markov failure is an exact transition-rate statement.

## Verdict
- **PASS (computational, n<=12):** `(N1,D)` projection is lumpable under zero-cost growth.
- **PASS (explicit counterexample):** `N1`-only projection is not lumpable.
- **PASS:** coarse-graining can generate observer-level memory in an explicitly defined EHF process.
- **OPEN:** prove `(N1,D)` lumpability for all `n` under the zero-cost insertion rule.

## Next probe
**WHEELER-36 — Sufficient-Statistic / Minimal Observer-State Audit**

Determine whether `(N1,D)` is minimal for Markov closure of zero-cost growth, or whether a smaller statistic than the full pair can still restore lumpability. Also seek a general proof that `(N1,D)` is lumpable for all `n`.