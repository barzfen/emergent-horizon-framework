# EHF-REV-05 — A tagged connection as local memory

5 November 2026 (Australia/Brisbane). Research direction by Barry Fensom, with implementation and analysis assisted by ChatGPT.

Giving a locally marked connection a preference for forward continuation increases first-cycle returns to blocked LR4 targets from 4.15 to 17.67 per million trials in the six-slide test. The marker leaves more graphs open at the cutoff. Roughly 87% of changed cycles reached by the tagged controller have a different Pi.

## Controller and observer

Start at the REV-04 witness cycle (0,1,2,3,4,5,6,7,8), with bit 1 on vertices 1,2,3,4. Use the same reversible triangle slides, degree limit and same-bit neighbour requirement as [REV-04](../local-reconnect-04/README.md). The selected seed has two incident LR4 edges in the retained carrier whose endpoints lie outside its short-move component. These two immediate neighbours are the blocked targets counted here.

Each eligible directed slide has a weight. At a graph and marker state, the next slide is sampled with probability equal to its weight divided by the sum of all eligible weights. This is the event order of a model with competing rates and serialized whole slides. The probe counts slides and assigns no duration to the two separate edge edits inside a slide.

- **Equal weights.** All eligible moves have weight one.
- **Branch repair.** A move that takes one connection from a degree-three vertex to a degree-one vertex has weight four. The rest have weight one.
- **Tagged connection.** The first slide marks the edge it adds. The marker stores the fixed pivot, its current attachment and its previous attachment. A slide that keeps this pivot and moves the marked connection somewhere other than its immediately previous attachment has weight four. All other slides, including a reversal of the previous marked slide, have weight one. A slide through the other pivot that removes the marked edge clears the marker. Other edges can move while the marker stays in place. There is one marker, initialized only on the first slide.

The tagged policy uses local endpoint and attachment data for its preference. The one-shot initialization, serialized execution and choice of weight four are supplied. An external observer scores the first Hamiltonian cycle after leaving the seed, stopping the accounting at six slides. The observer computes Pi using the same canonical chart as REV-04. The controller has no destination, Pi test or cycle detector. The six-slide cutoff matches the minimum length of the LR4 paths found in REV-04.

## Outcomes

| First return within six slides | Equal weights | Branch repair | Tagged connection |
|---|---:|---:|---:|
| Original cycle | 9.3444% | 26.1474% | 7.9479% |
| Different Pi | 11.9097% | 33.7691% | 9.3214% |
| Other cycle with same Pi | 1.6571% | 4.6627% | 1.4012% |
| Either blocked target, per million trials | 4.1545 | 7.4235 | 17.6714 |
| Still open | 77.0884% | 35.4201% | 81.3277% |

The original cycle and the two blocked targets have separate rows. No probability mass stalled. Among changed cycles that closed within the window, the same-Pi fraction was approximately 12.2% under equal weights and 13.1% with the tag. The unconditional decrease in different-Pi returns coincides with fewer completed cycles overall.

Probability propagation retains both graph and marker state. An independent history enumeration found 12 paths to the two blocked targets that first return at six slides, four of them to the particular REV-04 witness target. Reweighting these paths with rational arithmetic gives exact blocked-target probabilities of 1327/319410000, 1013/136458000 and 21407/1211392000 respectively. These agree with the floating-point propagation.

The comparison covers one seed, one preference strength and a finite time window measured in moves. It measures the selection bias of the supplied controller. Longer-run rates and general Pi preservation remain open.

## Reproduction

Run with Python 3 and the REV-02 results and REV-04 slide implementation at their repository paths.

    python probe.py
    python verify.py

[probe.py](probe.py) writes [results.json](results.json), with cumulative first-cycle probabilities and input hashes. [verify.py](verify.py) enumerates the successful histories using the same slide legality implementation and separately calculates their exact probabilities. Its output is [independent-checks.json](independent-checks.json).
