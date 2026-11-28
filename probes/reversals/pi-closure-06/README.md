# EHF-REV-06 — Local Pi tags and seam order

5 November 2026 (Australia/Brisbane). Research direction by Barry Fensom, with implementation and analysis assisted by ChatGPT.

A local rule on added edges and the order of the anchor's neighbours preserves Pi at every completed cycle in the model. On the retained witness seed it raises the six-slide probability of a blocked LR4 first return from 17.67 to 467.98 per million. A stricter anchor rule leaves no successful blocked LR4 history within that window.

## Certificate

Attach an even or odd tag to each vertex from its canonical position in the source cycle. These immutable tags are separate from the MICRO bits. The canonical traversal starts at vertex 0 and takes the smaller of its two neighbours first.

Call an edge compatible if it connects unlike tags or connects two even tags with vertex 0 as an endpoint. An odd cycle with only compatible edges must have exactly one equal-tag edge. A closed walk crosses from even to odd as often as it crosses from odd to even, so the number of equal-tag edges is odd. At most two of them can occur because both must meet vertex 0. The larger neighbour at 0 must carry the even tag for the canonical traversal to place the equal-tag edge last. All other positions then alternate, recovering the assigned Pi. Conversely, a cycle with the assigned Pi meets both checks.

The code compares this certificate with the canonical position set for all 20,160 undirected cycles on the nine labels, without a MICRO filter. Exactly 360 match the seed's Pi.

## Policies

Keep the [REV-05](../tagged-controller-05/README.md) connection marker, weights, witness seed and six-slide accounting. Every policy uses [REV-04](../local-reconnect-04/README.md) slide legality. The first completed cycle is detected and scored by an external observer.

| Policy | Additional rule |
|---|---|
| Tagged baseline | The connection marker is the only weight preference. |
| Soft endpoint | Multiply the slide weight by four if the added edge is compatible. |
| Hard endpoint | Permit only compatible added edges. |
| Strict seam | Apply the hard endpoint rule and, whenever a slide touches vertex 0 and leaves it at degree two, require its smaller neighbour to be odd and its larger neighbour to be even. |
| Seam order | Apply the hard endpoint rule and, whenever a slide touches vertex 0 and leaves it with two unlike-tag neighbours, require the larger neighbour to be even. Same-tag neighbour pairs can occur temporarily. |
| Whole-cycle check | Veto any slide whose resulting graph is a completed cycle with a different Pi. This comparison uses the whole candidate graph. |

All moves are serialized. The endpoint rule reads the added edge's tags. The two seam rules additionally use vertex 0's prospective neighbourhood when that vertex participates. They require readable labels to compare its neighbours and apply at slide boundaries. The tagged seed initialization and canonical choice of anchor are supplied.

In the seam-order policy, compatibility is invariant because the seed has compatible edges, cuts remove edges, and joins add compatible edges. The anchor condition is invariant when it applies, because an edit away from the anchor cannot change its neighbourhood. At any completed cycle the certificate forces the anchor's neighbours to have unlike tags, so the seam-order policy guarantees the correct Pi without using the observer's cycle detector.

## First return within six slides

| Policy | Original cycle | Different Pi | Other same-Pi cycle | Blocked LR4 per million | Still open |
|---|---:|---:|---:|---:|---:|
| Tagged baseline | 7.9479% | 9.3214% | 1.4012% | 17.6714 | 81.3277% |
| Soft endpoint | 15.6959% | 4.8461% | 7.2361% | 127.0560 | 72.2092% |
| Hard endpoint | 31.7509% | 3.2010% | 22.5734% | 377.8367 | 42.4370% |
| Strict seam | 43.9300% | 0 | 54.2181% | 0 | 1.8519% |
| Seam order | 35.3080% | 0 | 25.2167% | 467.9823 | 39.4285% |
| Whole-cycle check | 8.5399% | 0 | 1.4583% | 19.4256 | 89.9998% |

The original cycle and the two immediate blocked LR4 neighbours are counted separately from the other same-Pi cycles. No mass stalled. For the tagged baseline, 3.1929% of all trials returned with the wrong Pi despite a compatible final join. Hard endpoint compatibility alone leaves the canonical orientation unresolved, accounting for its different-Pi returns.

The seam-order rule admits two of the 12 successful first-return histories found under unrestricted legality. Its increased probability comes from concentrating weight on admissible histories. A check imposed only on complete cycles yields a much smaller change in blocked LR4 probability over the same window. The guarantee applies to completed odd cycles under the given tags and chart. The numerical rates cover one seed and six slides and leave long-run completion and other carriers open.

## Reproduction

Use Python 3 with the REV-02, REV-04 and REV-05 files at their repository paths.

    python probe.py
    python verify.py

[probe.py](probe.py) verifies the certificate, reproduces the previous baseline and propagates all six policies. [results.json](results.json) retains cumulative outcome probabilities at each slide. [verify.py](verify.py) separately enumerates and reweights all 12 successful first-return histories with rational arithmetic using the same slide generator. [independent-checks.json](independent-checks.json) gives the exact probabilities and surviving history counts.
