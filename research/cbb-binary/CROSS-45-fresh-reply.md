# EHF-CBB-CROSS-45 — Certifying a fresh reply after a reset

**Date** 2026-11-13 (Australia/Brisbane)  
**Status** Exact finite enumeration with explicit witnesses and receiver-disabled controls.

## Setting

Use the indexed 21-vertex seed and the joint LR3/insertion graph from [CROSS-43](CROSS-43-local-history.md) and [CROSS-44](CROSS-44-cycle-record.md). Allow up to two proper insertions at zero-based edge indices 6 or greater, at any point in the history. The receiver is the LR3 event at sign-window start 2. The readout uses the ring size and its prepared orientation and indexing.

The previous readout recognized an exterior word at start 7 as written or cleared. The test here asks whether a transition between those readings certifies a receiver event **since the preceding phase reading**, even when the preceding reading occurred after earlier receiver activity.

## An exterior-only false reset

On each explicit written state in CROSS-44, reverse at start 4. The exterior reading becomes the cleared pattern, but the receiver has not performed the second reset move at start 2. Reversing at start 4 again recreates the written pattern without a fresh reply. In the halfway state and the genuinely cleared state, every sign outside receiver positions 2 through 5 agrees. An exterior-only snapshot cannot distinguish those two states.

The genuine reset includes starts 4 and 2 in order. At the halfway point, sign 2 is plus. At the genuine reset it is minus.

## Add one sign to the reader

Use the same exterior words as in CROSS-44 and add the current sign at position 2:

| Vertices | Cleared exterior word | Receiver sign | Written exterior word | Receiver sign |
|---|---|---|---|---|
| 21 | `--+-` | `-` | `+-+-` | `+` |
| 22 | `--+-++++` | `-` | `+-+-++++` | `+` |
| 23 | `--+-+++++++` | `-` | `+-+-+++++++` | `+` |

Other readings are left unclassified. A tick is a cleared reading followed by a written reading. A new tick needs another cleared reading. The phase itself is stored in signs of the cycle. The observer supplies the readout and tracks phase changes.

Across all 130,056 reachable sign words in the full joint graph, the cleared predicate selects 4, 4 and 3 states at sizes 21, 22 and 23. The written predicate selects 4, 4 and 3. For each direction, start a multi-source search from **all** states matching the source predicate. Delete every receiver move at start 2 and allow all other reversals and all remaining growth. Neither search reaches the opposite predicate at any size. Thus any observed transition between the two phases contains at least one receiver event after the initial reading. This certifies an intervening event, with no bound on how many intervening receiver events occurred.

Of the four individual signs in the receiver window, either position 2 or position 3 suffices for this test with the existing exterior words. Positions 4 and 5 fail. The predicates in the table use position 2.

## Growth inside the write and reset

From the explicit cleared 21-vertex state, apply LR3 at start 2, split edge 14, split edge 17 of the child, and apply LR3 at start 4. The endpoint is the written 23-vertex witness. The opposite phase transition also permits both insertions in flight. From the written 21-vertex state, apply LR3 at start 4, split those same two edges in order, then apply LR3 at start 2 to reach the cleared 23-vertex witness.

At fixed size, the explicit cleared and written states are joined by the two-move paths from CROSS-44 in both directions. This establishes repeatability along chosen histories and soundness across arbitrary allowed histories in the bounded model. It leaves scheduling, continued ticking under all growth choices, readout at larger sizes, and an exterior-only reader open.

## Reproduction

Run `python3 research/cbb-binary/cross45_fresh_reply.py` from the repository root. It reuses the joint graph from CROSS-43, checks the concrete false reset and in-flight growth witnesses, and audits both directions for all four one-sign readouts and the exterior-only control. AI assistance was used for search, implementation and interpretation.
