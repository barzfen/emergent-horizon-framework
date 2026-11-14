# EHF-CBB-CROSS-41 — Growth can break a local return signal

**Date** 2026-11-13 (Australia/Brisbane)  
**Status** Exact finite enumeration for the 21-vertex seed and two one-vertex refinements.

## Setup

Use the position-indexed sign word `S_2=(++(-+)^2-)^3` and the LR3 sign rewrites from [CROSS-39](CROSS-39-equal-pair-ancestry.md). The receiver is the LR3 window at zero-based start 2, as in [CROSS-40](CROSS-40-signal-and-oscillator.md). Read return patterns in a short window beginning at position 6 on the source side. These are prepared ports in the indexed cycle. A reflection or rotation can carry the ports along with the preparation. No dynamics for the ports are assumed.

Grow once by inserting the unique third colour between the two colours on edge 6 or on edge 7. In signs this replaces `+` by `--` or `-` by `++`, because the two new increments sum to the original increment modulo three. Deletion recovers the parent colour word. The receiver window has the same indices after either insertion. The children are proper three-colour words. The balance constraint is relaxed for these one-vertex children since 22 is not divisible by three.

Compare LR3-only reachability after the insertion. No additional growth, scheduling rule, or LR4 move is included. All distances are minimum counts of accepted reversals, measured from each prepared starting word after any growth.

## Exact results

The control disables the receiver reversal at start 2, retaining every other LR3 event. An acknowledgement that is reachable in the full graph and absent in the control requires at least one receiver event along every path that displays it. This test detects a dependency on a designated action. It does not track an individual carrier or assume all possible histories eventually return a signal.

| Preparation | Full reachable states | Control reachable states | First receiver eligibility | First original readout in full graph | First original readout in control |
|---|---:|---:|---:|---:|---:|
| Parent | 229 | 201 | 2 | 6 | Unreachable |
| Split edge 6 | 56 | 56 | Unreachable | Unreachable | Unreachable |
| Split edge 7 | 924 | 564 | 11 | 6 | 6 |

The original readout is the five-sign word `-+-+-` at start 6. In the parent the shortest path to it uses starts `6,4,2,8,6,4`. At the second move the receiver becomes eligible, and it acts at the third move. The source-side readout at the third move is still `-+-++`. The final readout therefore follows the response on this witness, and it cannot be produced in the control.

After splitting edge 7, starts `21,1,3,6,8,10` produce the old readout after six moves with the receiver still ineligible. The same readout can now give a false acknowledgement. A different four-sign readout `-+++` at start 6 first occurs at depth 31 in this child and is absent from its control. In the parent, that four-sign readout appears after three moves in both graphs. These examples show that a short window can certify a receiver event in one preparation and lose that meaning under a single insertion.

## Consequence for the clock question

These results distinguish growth count from the change growth makes to reachable histories. The two children have the same number of vertices, but one insertion disconnects this receiver from the prepared state in the LR3 graph and the other delays it.

The parent has a finite acknowledgement benchmark, and the delayed child has a different one. Neither result constructs a resettable clock with one repeatable readout preserved across growth. A subsequent test needs a local record or a port construction with the same operational meaning before and after growth.

## Reproduction

Run `python3 research/cbb-binary/cross41_growth_and_return.py` from the repository root. Breadth-first search exhausts each full and receiver-clamped sign component and checks the local witnesses. It reuses the colour-derived LR3 table and cyclic rewrites from CROSS-39. Counts are of indexed sign states, not of labelled Hamiltonian cycles. AI assistance was used in derivation, implementation and verification.
