# WHEELER-47 — Filter Realizability / Internal Classification-Cost Audit

> **Review correction — 18 October 2026:** Constant-time counter operations assume a word-RAM model or amortized binary increment. Worst-case bit-operation cost and physical access to a global size statistic are separate questions. Exact metadata access is an architecture assumption. See [ERRATA-01](ERRATA-01.md).

## Question

Can an internal EHF observer distinguish a growth event from a fixed-size comparison event cheaply enough for the selective-filter architecture of WHEELER-46 to be realizable?

## Event classes

Use the existing EHF event families:

- Growth: all-slot insertion, with system size change `n -> n+1`.
- Comparison: Core-C 2-opt / substring-reversal move, with fixed size `n -> n`.

Thus the two event classes differ in cardinality change.

## Case A — Observer retains transition size metadata

Suppose the observer record contains the size before and after the event, or equivalently the size increment

`Delta n = n_{t+1} - n_t`.

Then

- growth iff `Delta n = +1`;
- comparison iff `Delta n = 0`.

Classification is exact and requires only a bounded-size statistic. If `n_t` is already part of the observer state, the per-event classification rule is O(1).

### Verdict

PASS: exact O(1) growth/comparison classification is realizable for observers retaining size-change metadata.

## Case B — Observer receives explicit generator/event metadata

If the substrate transition record includes which admissible generator fired, then the event family is already tagged. Classification is O(1) by construction.

This is stronger than needed, but it shows that WHEELER-46's upstream-filter architecture is consistent with an event-record formulation of EHF.

### Caveat

Treating the generator label as primitive observer-accessible data may be too strong for some EHF formulations. It should not be assumed unless the observer record explicitly includes it.

## Case C — Observer sees before/after full configurations but no size metadata

If full configurations are represented with directly readable cardinality, counting their sizes yields the same classifier. Depending on representation, maintaining size incrementally is O(1), while recomputing size from a raw representation can be O(n).

Therefore complexity depends on representation and observer memory:

- retained running size: O(1);
- recount raw state each event: O(n).

This is an observer-architecture effect rather than a substrate ambiguity.

## Case D — Coarse observer omits size and sees only projected state

If the observer projection discards `n`, exact classification need not be possible. A growth event and a fixed-size comparison event can map to the same coarse visible transition.

Hence selective access is not guaranteed for arbitrary coarse observers.

This parallels WHEELER-34/35: whether a macro-observer has a closed predictive description depends on which sufficient statistics its record retains.

## Case E — Post-state only

If the observer sees only the post-event macrostate and has no retained pre-event record, event type is generally non-identifiable: the same post-state may be reachable by different histories/event classes.

Therefore exact event classification requires some transition information, not merely the current state.

## Main structural result

The WHEELER-46 filter is realizable with bounded classification cost provided the observer record contains a transition-size statistic:

`Delta n in {0,+1}`.

So the relevant distinction is not simply 'smart observer versus naive observer', but whether the observer architecture preserves the event metadata needed for cheap classification.

In particular,

`local/retained transition metadata -> O(1) classifier`,

whereas

`coarse state-only observation -> possible ambiguity`,

and

`raw reconstruction without retained metadata -> potentially O(n)`.

## Relation to observer state

This suggests a minimal observer record augmentation

`O_t -> (O_t, n_t)`

or, at the transition level,

`R_t -> (R_t, Delta n_t)`.

The additional memory burden is logarithmic in system size if `n` is stored explicitly (`O(log n)` bits), while the per-event update is constant-time.

Thus a small persistent observer memory can replace repeated O(n) reconstruction.

## Interpretation

The result is not that EHF observers automatically possess perfect upstream filters. Rather:

1. the substrate event families are structurally distinguishable;
2. the distinguishing statistic can be very cheap;
3. realizability depends on whether the observer record retains that statistic.

This gives a concrete mechanism by which observer memory can trade against processing work.

## Verdict

- **PASS**: growth/comparison event type is exactly distinguishable by `Delta n`.
- **PASS**: with retained size metadata, per-event classification can be O(1).
- **PASS**: only O(log n) persistent bits are needed to store size explicitly.
- **NEGATIVE**: arbitrary coarse/post-state-only observers are not guaranteed to classify event type.
- **OPEN**: derive from EHF observer primitives whether `n` or `Delta n` must be available to an internal observer rather than chosen by architecture.

## Next probe

WHEELER-48 — Observer-Memory / Processing Tradeoff Audit

Quantify the tradeoff between storing a small sufficient statistic such as `n_t` and paying repeated reconstruction cost. Test whether an optimal internal observer architecture emerges from memory cost + processing cost rather than being stipulated.
