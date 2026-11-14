# EHF-CBB-CROSS-46 — A local clock with protected growth and a Bell control

**Date** 2026-11-13 (Australia/Brisbane)  
**Status** Exact local rule, finite growth census, and a classical two-reader benchmark.

## A six-reversal clock

Use the cleared 21-vertex witness of [CROSS-45](CROSS-45-fresh-reply.md). Read its six-sign core at indices 2 through 7 and the four-sign tail at the end of the indexed cycle. Across the cyclic seam the two regions are separated by just signs 0 and 1, so one 12-sign neighbourhood covers the rule. Use the existing LR3 reversal at the start specified by the current reading:

| Core | Tail | Start |
|---|---|---:|
| `-++-+-` | `+--+` | 2 |
| `+--++-` | `+--+` | 4 |
| `+-+--+` | `+--+` | n-4 |
| `+-+--+` | `-++-` | 4 |
| `+--++-` | `-++-` | 2 |
| `-++-+-` | `-++-` | n-4 |

Each selected LR3 is legal and produces the next row, cyclically. The tail stores one bit in the cycle's signs. It distinguishes the two visits to the halfway core state, allowing a single-valued choice of the next reversal from the current word. The first two moves write the core reply. The remaining four switch the tail, clear the core reply, and restore the tail. One full period uses six selected LR3 moves. A rule using only the three core states would have to select two different successors at the same halfway word to traverse the original two-move write and its two-move inverse.

The rule is a supplied orientation of selected LR3 moves on a prepared patch. The readout uses the chosen seam and orientation, and the admissibility relation alone allows undoing a legal reversal immediately. No phase counter or external list of step numbers is used when evaluating the new rule.

## Growth and background reversals

Permit any other LR3 whose four-sign support is disjoint from the readout. Permit proper insertions at edges 8 through n-5, using the insertion convention of CROSS-43. This protects the readout and leaves all other eligible disjoint reversals active. Each such insertion preserves the six core signs and the last four signs, although it can change the tail's index. Each disjoint reversal also preserves the two words. Thus there is always exactly one selected clock move after any allowed interleaving, for any number of insertions satisfying this restriction. This follows from the table and support condition, independently of the finite census.

| Vertices | Reachable states under the supplied rule |
|---|---:|
| 21 | 6 |
| 22 | 144 |
| 23 | 1,134 |
| 24 | 4,560 |

The census checks the next phase and unique clock move at every reachable state, up to three insertions. The previously selected pair of growth operations, at edge 14 and then edge 17, remains possible in every phase. With the original growth slots of CROSS-43, a single insertion can erase the phase reading. The unrestricted-slot one-insertion census includes 36 states with no selected clock move. In particular, edge 6 of the initial phase gives such a state.

The clock cycles whenever its selected local update keeps occurring. Infinite alternating background reversals can starve it even after one allowed insertion. Progress under a global interleaving therefore needs a fairness assumption or a physical rate rule. The combinatorial period is not a derived proper-time metric.

## Two-reader classical control

As a baseline for an entanglement test, choose phase 0 or phase 3 with equal probability before selecting settings. Freeze the cycle for readout. Reader A chooses one of the first two core signs and reader B chooses one of the first two tail signs. Settings are independent of the prepared phase. Both output plus or minus one and neither setting changes the cycle. Marginals are unbiased, and for settings `00, 01, 10, 11` the four correlations are exactly `-1, +1, +1, -1`. In the convention `S = |E00 + E01 + E10 - E11|`, this gives `S=2`.

Given the prepared phase, all four local answers are fixed. For each preparation, `A0(B0+B1)+A1(B0-B1)` is plus or minus two. Averaging keeps `S<=2` for any mixture with setting independence. The two regions share a classical preparation and can have perfect correlation or anticorrelation. A Bell-violating extension would need independently selected local interventions whose outcomes cannot be reduced to such a shared-state model under the Bell assumptions. The clock ports are nearby on the ring, and the frozen readout is a classical benchmark, with no claim of physical spacelike separation or of derived quantum dynamics. See [Brunner et al., Bell nonlocality, 2014](https://arxiv.org/abs/1303.2849), review PDF sections II.C and II.D and figure 4, for the local bound and quantum maximum.

## Reproduction

Run `python3 research/cbb-binary/cross46_local_clock.py` from the repository root. The verifier checks the phase table, exhausts the bounded growth graphs, constructs the starvation example and computes the exact two-reader correlations. AI assistance was used in construction, verification and writing.
