# SIGN-02 — Orientation adds no predictive power for the BIN-09 insertion readout

**Status:** proved for the specified process; exhaustively checked at source
sizes 5, 7 and 9. This is not a claim about MICRO/Pi, direction-dependent
controllers or physical dynamics.

## Setup

Use the [BIN-09](../cbb-binary/BIN-09-analytic-mode-selection.md) process:
at odd size n = 2m+1, fix a marked set R of m old labels before the run
(R = {1,2,3} at n = 7). Choose each LR3 segment start uniformly and
independently, then insert a new label at a uniformly chosen edge. Score 1
if the even child's unordered parity partition puts the new label
together with exactly R, and 0 otherwise.

The unsigned baseline records the cyclic marked/unmarked word up to
rotation and reflection (a bracelet, equivalent here to the dihedral
marked-gap word). The signed refinement is the orientation lift of
[SIGN-01](SIGN-01.md): retain the orientation through each reversal
instead of reflecting to the canonical chart. This retains the sign
transport without making the choice of chart a physical observable.

## Why the unsigned baseline is sufficient

An LR3 event swaps positions i and i+2 modulo n. Rotation or reflection
merely permutes the n possible events. The binary word determines the
effect of each swap, independent of the individual labels within R or
its complement. Thus every oriented cycle over the same bracelet has
the same transition counts to each next bracelet.

Likewise, the target-sector hit probability depends only on the bracelet:
it is 1/n if R is independent on the old cycle and zero otherwise. One
way to see uniqueness is that an independent m-set on a (2m+1)-cycle has
m-1 gaps of length two and one gap of length three; insertion must split
the middle edge of that length-three gap to produce the target partition.

Write b for the bracelet map from oriented cycles, P for the oriented
transition operator, K for the unsigned quotient and g for the insertion
hit probability on bracelets. For any bracelet observable f,
P(f composed with b) = (Kf) composed with b. Induction gives the same
identity for P^k and K^k. In particular the success probability after
k future reversals is (K^k g)(b), even conditional on previously observed
orientation signs or loop history, once the current bracelet is known.
This uses the fixed uniform future rule; it does not say past signs are
uninformative if the current bracelet is hidden or if the future
controller uses those signs.

## Exact check and positive control

Enumerated every oriented labelled cycle up to rotation, all LR3 events,
and all insertion edges. The script checks both quotient transition
counts and direct insertion hits; it reproduces the BIN-09 four-class
matrix and compares integer path counts for k = 0 through 8.

| Source size | Oriented labelled cycles | Marked words up to rotation | Unsigned bracelets | Distinct mirror pairs |
| --- | ---: | ---: | ---: | ---: |
| 5 | 24 | 2 | 2 | 0 |
| 7 | 720 | 5 | 4 | 1 |
| 9 | 40,320 | 14 | 10 | 4 |

Orientation is not an empty refinement. At size 7, the two oriented
words 0001011 and 0001101 are mirrors. After one uniform LR3 event,
the probability of seeing the specific oriented word 0001011 is 3/7
from the first and 1/7 from the second. This readout explicitly requires
a maintained direction reference, and is not the original insertion
readout. The original 5/7 and 2/7 rates remain those of the unsigned
observation; orientation does not add a decay mode to it.

Run `python3 probe-marked-insertion.py` to reproduce the checks.

**Next falsifiable test:** specify a directional insertion controller
before running it. Test mirror-pair starts with a held-fixed direction
reference against a control that randomizes that reference. Look for
different target-sector probabilities from the same unsigned bracelet;
any difference would be a property of the augmented comparison
protocol, not of the original LR3 walk.
