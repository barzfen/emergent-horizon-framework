# EHF-CBB-CROSS-49 — A route recorder made of reversals

**Date** 2026-11-13 (Australia/Brisbane)  
**Status** Exact cycle construction, supplied coherent control, and a sharp classical comparison.

## An eight-state carrier and recorder

Use the 21-vertex preparation from [CROSS-48](CROSS-48-reversal-interference.md). Keep the two carrier reversals P and Q at sign-window starts 2 and 17, and use the already legal reversal R at start 6 for the recorder. The three four-sign windows are disjoint. Each of the eight subsets of moves gives a distinct indexed labelled tour. All twelve undirected cube edges are legal LR3 reversals. Write a basis state as pqr, where each bit reports whether its reversal has acted an odd number of times. The p and r bits are readable by comparing their respective windows with their initial patterns.

Supply a conditional recorder operation W. If the P window shows p=1, apply R. Otherwise leave the tour alone. The P window sits immediately beside the recorder window, and the conditional rule reads only the P window. The operation can be undone by applying the same rule again before the carrier changes. Its selection rule is supplied, while its state change is an existing cycle reversal. Splitting any edge from 10 through 16 preserves all eight states and their reversal edges in the corresponding grown cycle, with Q shifted one slot. Splitting edges 6 through 9 disables R at the resulting preparation.

## Record and unwrite with the supplied coherent lift

Use the signed flips from CROSS-48 and extend them by R flipping r with sign (-1)^(p+q). The three signed flips are involutions and anticommute, as do the three position-vector lifts checked in the verifier. Define W on basis states by this signed R when p=1 and the identity otherwise. W is an involution because R preserves its control bit. Use the same coherent carrier pulse U=(P+Q)/sqrt(2) for preparation and recombination and the same squared-amplitude readout. The observable arrival event is pq=11 with either recorder value.

Starting at 000, the first pulse gives (010+100)/sqrt(2). Writing the record gives (010-101)/sqrt(2). The latter has Schmidt rank two across carrier and recorder in the supplied tensor-product model. The mixture of the two branches has the same basis probabilities and different behaviour under coherent unwrite and recombination. The construction supplies the tensor-product amplitude model and the pulse. It does not infer either from the bare reversal graph.

| Protocol between the two pulses | Arrival probability |
|---|---:|
| Leave the recorder alone | 0 |
| Write and retain the route | 1/2 |
| Write, then unwrite before recombination | 0 |

After retaining the record the full joint distribution is uniform on 000, 001, 110 and 111. Applying W after recombination leaves the carrier arrival probability at 1/2. If the recorder starts in (0+1)/sqrt(2) or (0-1)/sqrt(2), a single intermediate W gives arrival probabilities 1 and 0, respectively, despite identical initial cycle-basis probabilities. Here 0 and 1 in the recorder superpositions denote its two cycle configurations. These are supplied coherent preparations. The restored cancellation follows reversible removal of the record before recombination, consistent with the path-distinguishability calculation in [Ferrari and Braunecker, 2010](https://www.st-andrews.ac.uk/~bhb/Papers/mach_zehnder.pdf).

## Classical comparison with the recorder included

Independent fair classical choices of P or Q at the two pulses give carrier arrival probability 1/2 with zero, one or two applications of W. With one write and recorder initially zero, this classical walk even reproduces the entire four-outcome joint distribution.

A stronger test compares the full plain and tagged joint tables. Fix fair first moves, and let the second stage use **one common stochastic kernel on the full current indexed cycle**, including the recorder, in both protocols. There is no separate run-setting flag or hidden apparatus memory in this control. The plain arm distribution is uniform on 010 and 100. The tagged arm distribution is uniform on 010 and 101. The shared arm 010 therefore enters the very same kernel in both runs.

Let x, y and z be the probabilities of returning to 000 from 100, 010 and 101. The plain output probability at 000 is A=(x+y)/2 and the tagged one is B=(y+z)/2, so B >= A-1/2. The coherent targets A=1 and B=1/4 violate that inequality. If both joint distributions have total variation error at most e, then A >= 1-e and B <= 1/4+e. Thus e >= 1/8. The bound is tight with legal second moves. On the untagged P arm always repeat P, on the Q arm repeat Q with probability 3/4, and on the tagged P arm choose fairly. The resulting plain distribution has masses 7/8 at 000 and 1/8 at 110. The tagged distribution assigns masses 3/8, 1/4, 1/8 and 1/4 to 000, 001, 110 and 111. Each has total variation distance 1/8 from its target.

If a classical controller carries an extra flag distinguishing the protocols, it can reproduce both targets exactly. It repeats the first move in the plain run and chooses independently in the tagged run. The branch of the first move is already readable from the current cycle. This identifies the missing classical variable for that simulation and the scope of the obstruction. A comparison against arbitrary apparatus memory or a derivation of coherent probabilities from admissibility remains open.

## Reproduce

Run `python3 research/cbb-binary/cross49_route_recorder.py` from the repository root. It checks the labelled cubes, the Clifford signs, the coherent arithmetic, the classical joint outcomes and tight total variation witness. AI assistance was used for construction, verification and writing.
