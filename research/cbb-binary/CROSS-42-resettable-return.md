# EHF-CBB-CROSS-42 — A resettable return detector and its growth limit

**Date** 2026-11-13 (Australia/Brisbane)  
**Status** Exact finite result for indexed LR3 sign graphs. One explicit failure when growth intervenes during a tick.

## Local detector

Retain the receiver at zero-based sign-window start 2 and the proper insertion rule from [CROSS-41](CROSS-41-growth-and-return.md). Read ten consecutive signs from position 5. The detector arms on any of these ready words:

```text
+-++-+-+-+
+++++-+-+-
+---+-+-+-
```

It records one acknowledgement when it next sees `++--+-+++-`, then waits for a ready word before arming again. The ready words are the initial readings of the parent and the two children in CROSS-41. The acknowledgement was selected by comparing finite reachable sets. The detector's one-bit phase is an added observer record. The LR3 graph provides paths between its readings and leaves the choice and timing of moves open.

## Soundness and repeatability at fixed size

For the 21-vertex parent and each of the 15 single insertions at edges 6 through 20, enumerate the full LR3 component from the prepared seed. Within each full component, remove every receiver event at start 2. In all 16 preparations, no resulting connected component contains both a ready word and the acknowledgement. Thus from any reachable ready state, every fixed-size path to the acknowledgement contains a receiver event. Since the graph is reversible, the same condition applies to paths from acknowledgement back to readiness. This checks repeated local rearming even when the entire word differs from the initial seed.

| Preparation | Earliest acknowledgement | Earliest acknowledgement followed by a ready word |
|---|---:|---:|
| Original cycle | 6 | 12 |
| Split edge 6 | Unreachable | Unreachable |
| Split edge 7 | 21 | 30 |

Counts are minimum numbers of accepted LR3 reversals from the prepared seed, with the ready reading at depth zero. Reversing any witness path from a seed to acknowledgement returns to that seed. Repeating that pair of paths gives arbitrarily many certified ticks in the original and edge-7 preparations. Some other single-insertion preparations lack a ready word or a reachable acknowledgement. The soundness check covers those preparations without claiming that they all tick.

## Insertion during a tick defeats the detector

Arm on the original seed. Apply LR3 at starts `20,1,3,18,16,20,1,18,20`. Split edge 8 of the resulting word using the proper insertion. Apply LR3 at starts `5,3,1,8,6,4,10,8,12,10,15,13`. The final word displays the acknowledgement. Neither list contains the receiver event.

The detector can be used in multiple prepared sizes when growth takes place before arming. A growth event between its readings can create a false tick. A clock robust to that kind of growth needs an observable or causal record that stays sound in the joint graph of insertions and reversals. No physical proper time is inferred here.

## Reproduction

Run `python3 research/cbb-binary/cross42_resettable_return.py` from the repository root. The script reuses the LR3 exploration and growth operations from CROSS-41 and checks the clamped components, minimum counts and explicit counterexample. AI assistance was used for the finite search, derivation and verification.
