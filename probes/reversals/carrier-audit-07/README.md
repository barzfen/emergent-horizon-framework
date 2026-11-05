# EHF-REV-07 — First returns across the 96-ring carrier

5 November 2026 (Australia/Brisbane). Research direction by Barry Fensom, with implementation and analysis assisted by ChatGPT.

The local seam-order controller admits a six-slide first-return route for 48 of the 76 LR4 transitions that cross short-move components. For the other 28, the probability within that window is exactly zero. Across the 96 starting rings, 68 can reach at least one of their blocked LR4 neighbours within six slides.

## What counts as success

Use the 96 completed rings from [REV-02](../rare-channel-02/README.md), with its fixed MICRO bits and common Pi. A blocked target is an immediate LR4 neighbour lying in a different component of the LR2/LR3 graph. For each of the 76 pairs, initialize the [REV-06](../pi-closure-06/README.md) tagged controller at each endpoint in turn. A trial scores a target only if it is the first completed ring after leaving the start, within six slides. The observer scores closure externally.

The controller retains REV-06's weight four for continuing the marked connection. It also requires compatible parity tags at each join. A slide that touches vertex 0 and leaves it with two unlike-tag neighbours must leave the larger neighbour with an even tag. The anchor, tags, serialized slides and six-slide horizon are supplied as in REV-06. Each seed starts with the marker unset.

## Route census and probability

| Allowed slides | Blocked pairs with a first-return route | Directed targets with a route |
|---|---:|---:|
| REV-04 triangle-slide legality | 76 of 76 | 152 of 152 |
| Require compatible joins | 56 of 76 | 112 of 152 |
| Also require seam order | 48 of 76 | 96 of 152 |

All three route sets are symmetric under exchanging the endpoints. For the first-return census, grow a ball of radius three from each endpoint, using open graphs only after leaving the seed. An intersection gives a path with at most six slides and only open interior states. This uses reversibility of the slide rules between admissible graph states. Endpoint compatibility is an invariant on the second and third graphs. The seam condition is also an invariant on the third graph, so reversing a slide restores a state satisfying the same checks.

The probabilities use exact rational arithmetic and keep the connection marker in the state. At each of six steps, distribute mass across legal slides in proportion to the REV-06 weights. On completing a cycle, absorb its mass at that endpoint. This forward propagation agrees with the separate route census for all 152 directions.

- The 96 positive target probabilities range from **24.11 to 881.83 per million**, measured per directed target and per trial from its source.
- A uniform draw from all 96 seed rings gives **276.98 blocked returns per million trials**, summing over the blocked targets incident to the sampled seed. Eighty-four seeds have blocked neighbours and 68 can reach one within six slides.
- All 48 reachable pairs have different probabilities in their two directions under the initialized controller. Reversible slide legality gives symmetric reachability, while the marker and choice weights govern how likely each route is.
- Between 12.83% and 43.04% of trials remain open at six slides, depending on the seed. Every completed return in this run lies in the retained carrier.

The zero probabilities are specific to first return within six slides under these rules. Longer paths and other carriers remain open.

## Reproduction

Run with Python 3 and keep REV-02, REV-04, REV-05 and REV-06 at their repository paths.

    python probe.py

[probe.py](probe.py) verifies exact probability conservation for every seed, checks each completed return against the Pi certificate, and reproduces the REV-06 witness probability of 317/677376. [results.json](results.json) records the route verdicts and rational probabilities for every direction, plus the per-seed totals. The numeric seed and target indices refer to the state list in [REV-02 results](../rare-channel-02/results.json).
