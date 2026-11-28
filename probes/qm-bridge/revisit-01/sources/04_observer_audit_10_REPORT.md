# EHF Observer Compatibility Audit 10

## Seeing the dynamics and testing the simulator

29 October 2026 · Barry Fensom research collaboration

An interactive experiment now shows actual admissible four-bit reversals on the original binary ring, alongside the corresponding gap-unit description. Its purpose is to make the established dynamics visible and test its implementation against exact probabilities. These are internal mathematical and simulation checks, not comparisons with measurements of a physical system.

## What the display represents

Each original ring has one-dimers `11` separated by zero gaps `3+2h_i`. The outer open circles are original zero bits, and the squares are original one bits. The inner numbers are the movable units h_i in cyclic gap order. This inner ordering is read from the first zero-run boundary after the fixed outer origin; it is a description of gaps, not a second physical ring or a trajectory of individually labelled particles.

At each animation step, the simulator reverses an actual window of four original bits. It rejects changes violating cyclic no-isolation, and retains multiplicities when several legal start positions lead to the same shape. Accepted windows are highlighted. The animation preserves length, counts, the odd-gap dimer family, and total gap units.

Two sampling rules are available:

- Legal-event sampling K: enumerate all admissible nontrivial starts and choose uniformly.
- Attempted-position sampling A: choose uniformly among all n starts; an invalid or trivial reversal leaves the state unchanged.

The displayed time is a count of model events or attempts. It is not calibrated to physical seconds. The run button performs 20 steps and stops; there is no automatic background simulation.

Both displayed rings use independent random choices. In the balanced experiment, equal future activity laws mean equal probability distributions, not identical activity at every step of two independently sampled paths.

## Three reproducible experiments

“Together” means all movable units occupy one gap, equivalently p=1.

| Experiment | Initial A | Initial B | Steps | Exact K probability, A | Exact K probability, B |
|---|---|---|---|---|---|
| Separation matters | (1,0,0,1,0,0,0,0) | (1,0,0,0,1,0,0,0) | 3 | 1/8 | 0 |
| Balanced symmetry | (0,0,2,2) | (0,1,0,3) | 4 | 31/288 | 31/288 |
| Same arrival time | (0,0,2,3) | (0,1,0,4) | 2 | 1/16 | 1/8 |

For attempted-position sampling the corresponding exact probabilities are:

| Experiment | Exact A probability, start A | Exact A probability, start B |
|---|---|---|
| Separation matters | 1/10648 | 0 |
| Balanced symmetry | 131/10976 | 131/10976 |
| Same arrival time | 1/900 | 1/450 |

The two clocks count different things. A much lower chance after three attempts than after three accepted moves is the expected consequence of waiting, not a disagreement between the implementations.

## Sampling results

The independent Python experiment ran 100,000 fresh trials for each starting state, experiment and sampling rule: 1,200,000 trials in total. It uses explicitly recorded deterministic pseudorandom seeds. Exact endpoint distributions are computed using rational arithmetic, independently of sampling.

Selected legal-event results:

| Experiment and start | Exact chance | Observed successes / 100,000 |
|---|---|---|
| Separation A | 12.5% | 12,468 |
| Separation B | 0% | 0 |
| Balanced A | 10.763888…% | 10,814 |
| Balanced B | 10.763888…% | 10,787 |
| Same arrival time A | 6.25% | 6,251 |
| Same arrival time B | 12.5% | 12,627 |

All counts, including every final activity category and both clocks, are in results.json. These sampled results are consistent with the exact probabilities; the proofs and exact kernel checks, rather than finite sample agreement, establish the underlying identities and impossibilities.

The interactive test button performs a separate batch of 10,000 fresh trials for each initial ring, irrespective of the current animation state. It displays the estimated chance and a 95% Wilson binomial confidence interval. Its seeds and random-number generator differ from the Python experiment, so its counts need not match the table above. Zero sampled successes alone do not prove impossibility; the exact-probability column supplies that distinction.

## Implementation checks

Browser execution was checked at desktop and narrow mobile widths, including 320 and 360 pixels, in light and dark appearance. The checks exercised the experiment selector, both sampling rules, one-step advancement, finite 20-step playback, and repeated-trial output. No browser errors or horizontal mobile overflow were observed.

The actual JavaScript original-ring reversal kernel was independently compared against Audit 09's exact certificates for all 23 geometric states across the three selected sectors, covering 106 legal start events. Every target multiplicity matched. Those checks also verified admissibility, preserved bit count and length, nonnegative integer gap units, and conserved total units for each checked transition. The JavaScript finite-horizon calculations matched all 12 rational reference probabilities to within 1e-12. The JavaScript probability display uses floating-point arithmetic; the reference calculations are exact fractions.

The independent probability calculation and Monte Carlo trials use gap-unit transfers, whose equivalence to original LR4 was proved in Audit 06 and checked in Audits 08–09. In contrast, the visible animation itself executes original four-bit reversals. This separation makes the cross-check meaningful.

## What this adds

We can now inspect local motion, compare two observationally equivalent or inequivalent starts, and test the effect of the sampling clock. The experiment confirms the implemented model reproduces its exact mathematics. It supplies no new proof of the still-open complete classification for arbitrary r,H>=4, and no empirical evidence that the model describes nature.

The next physics-oriented computational question would be whether larger-scale transport admits a simple effective description under a clearly specified clock. That requires a separate observable, initial-condition protocol and scaling test; it has not been claimed from this animation.

## Reproduction

Run `python3 test_model.py` to regenerate all exact reference distributions and the 1,200,000 seeded trials. Only the Python standard library is required. The interactive experiment is delivered in the conversation; it is not included as an HTML download in this package. visual_validation.json records its browser and kernel checks. This audit has not been published to GitHub.
