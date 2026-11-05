# EHF-REV-08 — Exhaustive first returns

5 November 2026 (Australia/Brisbane). Research direction by Barry Fensom, with implementation and analysis assisted by ChatGPT.

Every pair of distinct rings in the retained 96-ring carrier has a first-return path under the seam-order rule. In particular, the 28 blocked LR4 pairs that missed the six-slide cutoff have shortest first-return paths of 10 to 30 slides. One component of open graphs touches all 96 completed rings.

## Search and scope

Start from all 96 rings in the [REV-02 carrier](../rare-channel-02/README.md). Keep the fixed MICRO bits, even/odd tags, degree bound, serialized triangle slides and local seam-order rule from [REV-06](../pi-closure-06/README.md). A first return is the first completed Hamiltonian cycle after leaving the seed. The observer detects completion externally.

The connection marker changes relative slide weights, which are always positive for eligible slides. The reachability search therefore needs only the graph. Every finite path it finds has positive probability with the marker initialized as in REV-06. The search records existence and minimum length. The marker-dependent probabilities over longer windows remain to be measured.

First enumerate the legal graph states reachable from the starting set, expanding completed and open states alike until the frontier is empty. Then run breadth-first search from each completed ring, expanding only open graphs and recording completed rings as endpoints. The first discovery of each endpoint gives its minimum slide count. Every directed slide in the enumerated state graph has a legal reverse.

As a separate reachability check, remove all completed cycles and find the connected components of the remaining graph. Each open component induces first-return routes between every pair of completed cycles adjacent to it. The resulting endpoint sets agree with the breadth-first searches.

## Results

| Minimum slides to a blocked LR4 neighbour | Pairs |
|---:|---:|
| 6 | 48 |
| 10 | 8 |
| 16 | 8 |
| 17 | 4 |
| 30 | 8 |
| **Total** | **76** |

The first six-slide row agrees exactly with [REV-07](../carrier-audit-07/README.md). All counts are unordered pairs. Reversing a path gives the same minimum distance for the reverse direction.

The census contains 6,624 graph states, including 6,528 open graphs and exactly the original 96 completed cycles. The open graph has 49 components. One touches all 96 completed cycles, and the other 48 touch between one and four. The common open component gives a first-return path between every pair of distinct completed cycles. There are 4,560 such pairs, with minimum distances from two to 35 slides.

Consequently, the six components of the original short-reversal graph are connected through first returns. In fact any ring in any of those regions can reach any ring in the others on a single excursion through open states. This is a finite reachability result for the supplied carrier and controller rules. The frequency of those paths under stochastic execution can differ considerably from their availability.

## Reproduction and checks

Run with Python 3 and keep REV-02 and REV-04 through REV-07 at their repository paths.

    python probe.py
    python verify.py

[probe.py](probe.py) exhausts the reachable states and checks the Pi certificate for every completed cycle, symmetry of slides and first-return distances, agreement between the two reachability methods, and agreement with the six-slide audit. [results.json](results.json) contains the exact minimum distances for all 4,560 pairs and the 76 blocked-pair witnesses. The endpoint indices match the [REV-02 state list](../rare-channel-02/results.json).

[verify.py](verify.py) replays the blocked-pair witnesses without calling the slide generator. It checks 3,216 single-edge edits in both directions for two-hop adjacency, connectivity, degree, same-bit neighbours, parity compatibility, anchor order at slide boundaries and first closure at the target.
