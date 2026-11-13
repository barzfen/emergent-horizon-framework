# EHF-CBB-CROSS-43 — A local history can certify reception during one insertion

**Date** 2026-11-13 (Australia/Brisbane)  
**Status** Exact finite reachability checks and explicit matched histories.

## Setting

Use the indexed 21-vertex seed from [CROSS-41](CROSS-41-growth-and-return.md). Permit arbitrary interleaving of cyclic LR3 reversals and proper insertions at zero-based edge indices 6 or greater. This keeps the receiver's four-sign support, positions 2 through 5, outside the insertion sites. The control deletes the LR3 event at window start 2 at every size. There is no rate or scheduling rule.

## The final cycle can lose the record

Use the shared history comprising LR3 at starts `20,1,3,18,16,20,1,18,20`, insertion at edge 8, then LR3 at `5,3,1,8,6,4,10,8,12,10,15,13,17,19,21`. This reaches the old ten-sign acknowledgement from [CROSS-42](CROSS-42-resettable-return.md) without a receiver event. Compare two histories:

- Prepend two LR3 moves at start 6.
- Append two LR3 moves at start 2, the receiver.

Each pair is legal and undoes itself, including the permutation of distinct vertex labels. Both histories have 26 reversals and one insertion, with identical initial and final indexed labelled tours, vertex colours and total event counts. One has zero receiver events and the other has two. The example establishes that a final acknowledgement state can be ambiguous even when its full labelled cycle is supplied. It does not show that every final state is ambiguous.

## Two adjacent signs retain a record of the sequence

Read the signs at positions 6 and 7, just outside the receiver's reversal support. Start on the first reading below. Record each change in the pair and ignore events that leave it unchanged. Recognize this exact sequence, with no other local reading between consecutive entries:

```text
-+  →  +-  →  -+  →  --  →  ++  →  --  →  -+  →  +-
```

The observer uses local change history. It receives neither the ring size, the event count nor a label naming the receiver. The search specifies this pattern after inspecting the finite model; the observer's memory is supplied.

Allow at most one insertion from the original seed. There are 8,783 reachable indexed sign words across the two sizes. Of those, 3,299 start with the required local reading. Exhaustive search over pairs of a sign word and the number of matched observations finds no history completing the trace from any of those 3,299 starting words when the receiver event is disabled. The shorter prefix obtained by removing the last reading can be reproduced in the control.

With the receiver enabled, the verifier replays a 13-event history that realizes the full trace. The insertion is at event four, after the detector starts and before the final reading. The witness uses two receiver events. Replaying the inverse reversals is a valid operation at fixed size, but no reset or periodic ticking claim is made for the joint graph with irreversible growth.

## A second insertion can mimic the trace

From the original seed, perform LR3 at starts `6,6`, insert at edge 7, perform LR3 at starts `14,12,10,8,5,5`, insert at edge 7 again, then perform LR3 at starts `9,6`. This produces the complete eight-reading trace with zero receiver events. The detector certifies reception in the one-insertion model, with no guarantee for repeated growth.

## Reproduction

Run `python3 research/cbb-binary/cross43_local_history.py` from the repository root. It verifies the labelled histories, checks the trace against all reachable ready states in the one-insertion control and reproduces the failure with two insertions. AI assistance was used for search, implementation and interpretation.
