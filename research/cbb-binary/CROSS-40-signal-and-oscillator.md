# EHF-CBB-CROSS-40 — Propagating markers, a receiver and local oscillators

**Date** 2026-11-13 (Australia/Brisbane)  
**Status** Exact constructions and a scheduling obstruction for LR3-only dynamics.

## Construction

Use the proper three-colour cycles and LR3 sign rules from [CROSS-39](CROSS-39-equal-pair-ancestry.md). Write `S_t=(++(-+)^t-)^3` for its seed sign word. A sign is the oriented colour difference modulo three. LR3 flips the four signs of `-++-` or `+--+`.

A separate length-18 balanced cyclic sign word gives an elementary oscillator:

```text
+++++-++++++--++++
+++++-+++++-++-+++
```

The only nontrivial LR3 window in either cyclic phase starts at sign index 11. The two phases map to each other by that reversal, so a return consists of two local moves. Both words reconstruct to proper cycles with six vertices of each colour and contain an LR4-eligible window. Restricting the move set to LR3 is part of this experiment.

Concatenate `S_t` and two copies of the first oscillator phase to make one cyclic sign word of length `6t+45`. Each block has zero net colour increment modulo three and balanced colour counts, so the joined cycle is also proper and balanced. The oscillators are prepared by choosing their initial patterns. The indexed windows identify regions in the prepared history; no extra vertex colour or clock variable enters the rules.

## A propagating front and a local receiver

The legal LR3 path at sign starts `2t+2,2t,...,4` remains available in the joined word, since all its windows are within the original `S_t` block. Each move creates the next equal-sign pair two positions to the left, saturating the CROSS-39 bound of two positions per ancestry link. That is a bound in LR3 events along the lineage. The probe makes no claim about shortest arrival among arbitrary histories in the joined word.

The receiver at sign-window start 2 is initially ineligible. Along this path it stays ineligible until the final front move at start 4 creates `-++-` there. The receiver can then perform its own LR3 and produce an equal-sign triple at sign positions 0 through 2. A second receiver LR3 restores the state immediately before the receiver fired. The eligibility and the first response are local properties of the colour word. This construction uses the chosen initial preparation and specified event path. Oscillator LR4 opportunities elsewhere make global LR4 activation unsuitable as a signal-arrival test here.

## Same endpoints and total number of moves, different local ticks

The signal windows and the two oscillator windows have disjoint sign supports. Each event reads and writes only its window, so the oscillator operations commute with the signal operations. In particular, for any integer `r >= 0` consider these histories from the same initial word:

- Perform `2r` LR3 moves on oscillator A and then the `t` signal moves.
- Perform `2r` LR3 moves on oscillator B and then the same `t` signal moves.

They finish at the identical sign word after the same `t+2r` moves, but oscillator A completes `r` returns in the first history and zero in the second. Applying the same receiver response to both histories preserves the equality and adds one move. The equality also holds for the full labelled tour if we start from the same labelling, since each pair of LR3 reversals at an oscillator is the identity permutation and the signal and receiver actions are identical. A single oscillator phase supplies local state information. Counting its completed returns requires an event record or a register.

There is a second ambiguity. Sliding oscillator operations past all signal operations gives the identical endpoint with identical local event sequences. If disjoint commuting events are treated as independent, the order used to decide which oscillator ticks happened before reception is undetermined by those local sequences. A physical clock construction would need a coupling or another internal record that relates those events, and a rule that constrains clock progress. The LR3 admissibility relation allows the illustrated schedules.

## Scope and reproduction

The same fixed-size cycle can support a propagating marker, a locally triggered response, and a repeatable local oscillator. The oscillator construction gives no invariant proper-time assignment to the front. Growth, clocks coupled to the front, and robustness when LR4 is allowed remain open.

Run `python3 research/cbb-binary/cross40_signal_and_oscillator.py` from the repository root. It reuses the colour-derived reversal tables from CROSS-39 and checks receiver activation and matched histories for `t=1..100`. The disjoint-support and oscillator-return arguments establish the matched histories for all `t>=1` and `r>=0`. AI assistance was used in derivation, implementation and verification.
