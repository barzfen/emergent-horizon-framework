# EHF-CBB-CROSS-44 — A reply written into the cycle

**Date** 2026-11-13 (Australia/Brisbane)  
**Status** Exact finite enumeration and explicit write, growth and reset witnesses.

## Setting

Start from the indexed 21-vertex sign word in [CROSS-43](CROSS-43-local-history.md). The allowed operations are length-three reversals (LR3) and at most two proper insertions at zero-based edge indices 6 or greater. Insertion can occur at any point in the history. The control disables the LR3 receiver event at window start 2, whose sign support is positions 2 through 5.

At a given size, a sign word provides evidence of a reply when it is reachable from the prepared seed and absent from the corresponding control. A snapshot of a subset of positions provides evidence only if the same reading is absent from the control at that size. The observer is supplied the size and a fixed orientation and indexing of the prepared cycle. This audit concerns the signs, with no extra observer memory or vertex identity used as a record.

## Writing and clearing a reply

Apply LR3 at starts `6,4,2,8,6,4,13,15,17`. Read the record from sign index 7. After writing it, split edge 14 and then edge 17 in the resulting child, with no intermediate reversals. The resulting record is readable at all three stages:

| Vertices | Written pattern | Cleared pattern |
|---|---|---|
| 21 | `+-+-` | `--+-` |
| 22 | `+-+-++++` | `--+-++++` |
| 23 | `+-+-+++++++` | `--+-+++++++` |

Each written pattern is absent from the full receiver-disabled graph at its size, including every allowed interleaving of insertions and reversals. Each witness state can be cleared using LR3 at starts `4,2`. The resulting whole sign word is reachable in the receiver-disabled model from the original preparation. Reversing those two moves, at starts `2,4`, rewrites the same record. These paths give a repeatable write-and-clear operation at each tested size. The reset itself involves the receiver, and the admissibility relation supplies no schedule that forces the cycle to run.

The pattern is stored in the cycle, though the readout width and the successful growth path were selected from the finite model. The table certifies the occurrence of a receiver action somewhere on the history from the seed. It is not a general guarantee that every pair of locally observed cleared and written patterns certifies a new action between them.

## What arbitrary insertion can hide

Enumerating the reachable sign graphs gives:

| Vertices | Receiver enabled | Receiver disabled |
|---|---:|---:|
| 21 | 229 | 201 |
| 22 | 8,554 | 6,568 |
| 23 | 121,273 | 90,931 |

All 28 full sign words that certify a reply at size 21 remain outside the control after **every** allowed single insertion. For 27 of the 28, this holds after **every** pair of insertions with no reversals between them.

However, every one of the 28 words has at least one allowed insertion whose entire exterior reading, at positions 6 through the end and then positions 0 and 1, matches a receiver-free history at size 22. Any detector using only a snapshot outside the four-sign receiver window has the same ambiguity on those matched pairs, even when it knows the size. The sign word still differs inside the receiver window.

For the written state above, splitting edge 6 gives the word `+++-+-+++-+-+++-+-+--+`. The receiver-free history at starts `6,4,8,6`, then insertion at edge 7, then starts `14,16,18`, gives `++-++-+++-+-+++-+-+--+`. The two words agree everywhere outside the receiver window. The full-word evidence in the first history is retained, but an exterior snapshot cannot distinguish the pair.

## Scope and reproduction

The result gives a stored, resettable reply along an explicit path through growth and an obstruction to universal exterior snapshot readout. It does not establish an autonomous clock, survival under arbitrary intervening reversals, or a growth-robust history detector. A useful follow-up is a readout that follows the record as it changes through insertion and tests for a new receiver action between reset and write.

Run `python3 research/cbb-binary/cross44_cycle_record.py` from the repository root. The verifier reuses the indexed joint-graph search in CROSS-43, exhausts both controls and replays the explicit histories. AI assistance was used for search, derivation and verification.
