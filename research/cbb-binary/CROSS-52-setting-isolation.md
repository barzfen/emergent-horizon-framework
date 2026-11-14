# EHF-CBB-CROSS-52 — Growth delays a setting leak to the recombiner

**Date** 2026-11-14 (Australia/Brisbane)  
**Status** Exact finite isolation lengths and explicit leak histories for a specified local intervention model.

## What is isolated

Use the first 22-vertex four-window preparation from [CROSS-50](CROSS-50-cycle-apparatus.md), obtained by inserting at edge 11. Carrier windows P and Q start at 2 and 18, the recorder R at 6, and the apparatus M at 12. The two trials start on the same idle recorder branch, with r=0. The only initial difference is that one trial has flipped M. All colours and vertex labels are otherwise carried through the legal reversal.

Treat the recombiner input as the signs in P, Q and R and the vertex labels at both ends of those sign edges. The input also has the common size and indexing. It has no direct access to M, to event success outside its observed region, or to a separate setting or timing flag. During the wait, the two trials receive the same sequence of indexed LR3 attempts. An ineligible attempt leaves the tour alone and counts as an attempt. The rule is local because eligibility reads the same four signs that a successful attempt flips. Growth is used in the preparation and then paused during the attempts.

## Grow buffers on both sides

A proper insertion replaces a sign s by two copies of its complement. Splitting the second of these new signs produces a three-sign alternating word in place of s. Repeat this two-insertion operation at original edge 16, then at original edge 10, k times at each location. This adds 4k vertices and lengthens both routes around the ring from M to the recombiner. The closest sign in the recombiner is then 3+2k sign positions away from the initial M difference.

The verifier checks that every grown preparation retains the full 16-state labelled reversal cube, as well as the opposite coherent outcomes of [CROSS-51](CROSS-51-recorder-phase.md) under that probe's supplied amplitudes, control, and readout. This is an algebraic check of the grown carrier. It does not implement the coherent pulse or the controlled setting choice as signals confined by the same local schedule.

## Shortest setting leak

Search pairs of sign words together with the relative permutation of vertex labels. This state determines both the next paired transition and whether the readouts differ. For each row the verifier exhausts all shorter common attempt sequences and replays the listed witness using explicit vertex labels.

| Vertices | First distinguishable attempt | Shortest witness, by window start |
|---|---:|---|
| 22 | 1 | 9 |
| 26 | 3 | 8, 11, 8 |
| 30 | 4 | 10, 13, 10, 8 |
| 34 | 5 | 12, 15, 12, 10, 8 |
| 38 | 6 | 14, 17, 14, 12, 10, 8 |
| 42 | 7 | 16, 19, 16, 14, 12, 10, 8 |

In the 34-vertex witness, both trials initially make the start-12 move. The start-15 move then fires only in the M-written trial. Later eligibility differences carry the change toward the recorder. The fifth attempt changes recorder signs 8 and 9 in just one trial. The isolation lengths count attempted updates, including those that do not fire, and make no claim about physical time.

The finite result applies to any common, setting-independent random mixture of these attempt sequences. It also applies to selecting the next attempt from a common rule that sees only the still-identical observed readout and shared random choices. For a deterministic upper bound at larger separations, a new sign difference can appear only inside an attempted support already meeting a difference. It can advance at most three positions per attempt. This gives a general lower bound of the ceiling of the sign separation divided by three for sign-only leakage. The exact finite results also check labels. No formula for the exact shortest leak at arbitrary k is claimed.

## Consequence for the phase test

Within the certified attempt window the observed idle-branch laws are identical, so their total variation distance d is zero. Even granting the classical model arbitrary setting access on the active branch, the common-readout error bound in CROSS-51 is then 1/4. The explicit fifth attempt in the 34-vertex case shows why separation and a time window are both needed.

The bound uses a specified local input and schedule. A device reading the entire tour sees M immediately. A setting-dependent update schedule, globally visible outcomes of attempts, or direct access to a separate flag can also bypass the certified isolation. To make an operational interference test, the coherent preparation and common recombination would need to run with the same access and timing constraints. This probe supplies a finite carrier-level isolation test and a counterexample after its deadline.

Run `python3 research/cbb-binary/cross52_setting_isolation.py` from the repository root. AI assistance was used in construction, search, and verification.
