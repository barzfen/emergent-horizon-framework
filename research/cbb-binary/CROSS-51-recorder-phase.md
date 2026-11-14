# EHF-CBB-CROSS-51 — Matched reversal loops prepare opposite recorder phases

**Date** 2026-11-14 (Australia/Brisbane)  
**Status** Exact finite construction with supplied coherent dynamics and a sharp classical memory comparison.

## Prepare and reset the apparatus

Use the 16 labelled cycle configurations from [CROSS-50](CROSS-50-cycle-apparatus.md). P and Q are the two carrier moves, R is the recorder move, and M is the extra apparatus move. Each bit records whether its reversal has acted an odd number of times. In the coherent control, use the signed flips of [CROSS-49](CROSS-49-route-recorder.md) and extend them by M with sign (-1)^(p+q+r). All four lifts square to the identity and anticommute. These are supplied lifts of the available moves, as in [CROSS-48](CROSS-48-reversal-interference.md) and the standard [Clifford/Pin construction](https://www.cis.upenn.edu/~cis6100/clifford.pdf).

Start at p=q=r=m=0. Supply the pulse (R+M)/sqrt(2). Its two terms move along legal reversal edges and produce the R and M arms with equal positive amplitudes. Follow with M controlled on r=0, using its lifted sign. This sends the M arm back to the zero word and leaves the R arm alone. The two arms give the recorder state (|0>+|1>)/sqrt(2) with p=q=m=0. The pulse, control rule and amplitude interpretation are supplied. The cycle gives the moves and the readable control bit.

## Two histories with the same endpoints

While r=1, execute one of these controlled sequences, in written time order:

| Setting | Moves on the r=1 branch | Lifted phase |
|---|---|---:|
| Sham | P, P, Q, Q | +1 |
| Square | P, Q, P, Q | -1 |

On r=0, both sequences leave the state alone. The sequences each use two P moves and two Q moves when active, and return every vertex label, all four basis bits and the sign word to their original values. In the lift, the sham product is the identity and the square product is minus the identity by anticommutation. The sign is relative because the r=0 branch does not execute the loop. Applying the square on both branches gives a common minus sign and no change in probabilities. The verifier checks these facts on all 16 states of all three grown cubes.

The two prepared recorder phases have identical cycle-basis probabilities, with p=q=m=0 in both. Apply the same carrier pulse, recorder write and second carrier pulse from CROSS-49. The apparatus M remains zero. The sham ends at pqr=110 or 111 with equal probability. The square ends at 000 or 001 with equal probability. Arrival at pq=11 thus has probability one or zero. Replacing the coherent recorder state by the equal classical mixture of its two basis configurations gives arrival probability one half in either setting under the same supplied coherent readout.

## Classical comparison

For the comparison, the setting is independent of an initially fair recorder basis value. At the input to the common recombiner, the visible basis laws in both trials are uniform on p=q=m=0 and r in {0,1}, aside from any apparatus memory explicitly allowed in the control. The model has no other setting input at recombination.

First allow arbitrary setting information on the r=1 branch, where the loop runs, and let d be the total variation distance between the full recombiner-input distributions on r=0 across the two settings. With a common stochastic recombiner, the difference in its two arrival probabilities is at most (1+d)/2. Indeed, each branch has weight one half. The r=1 branch can change its arrival probability by at most one, and the r=0 branch by at most d, by contraction under the common kernel. If both output tables have error at most e in total variation, the difference must be at least 1-2e. Consequently

    e >= (1-d)/4.

This is tight for the full output distributions on the cycle cube, including m. Supply the correct setting bit on r=1 and a symmetric noisy copy with probability (1+d)/2 of being correct on r=0. The two conditional bit laws on r=0 then have distance d. Choose the first carrier move fairly. At the second move, repeat for bit one or switch for bit zero. The final carrier parity reports the guessed setting, so a single common conditional M reversal clears the apparatus bit on the reached outputs. Both output distributions have error exactly (1-d)/4. The verifier checks rational examples of the full tables.

When only the active branch can retain a setting record, d=0 and the least possible worst error is 1/4 on these targets. An exact classical fit needs d=1, meaning perfectly distinguishable setting records even on the r=0 branch, where neither controlled loop acts. A full classical flag is sufficient and can be reset at the output. This control constrains what information could be available when recombination starts. It places no restriction on arbitrary external apparatus that communicates the setting to both branches.

## Scope and reproduction

The basis-state return and the relative sign of the lifted loop are exact. Interference in the readout uses a supplied coherent pulse, signed lift and squared-amplitude rule. A choice of earlier protocol is an apparatus input and need not be forgotten simply because the labelled cycle is restored. An experiment aiming to exclude the classical flag explanation needs an independent reason that the idle branch cannot carry setting information to the common recombiner.

Run `python3 research/cbb-binary/cross51_recorder_phase.py` from the repository root. AI assistance was used in constructing and checking the probe.
