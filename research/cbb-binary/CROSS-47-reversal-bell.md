# EHF-CBB-CROSS-47 — Local reversal interventions and a Bell control

**Date** 2026-11-13 (Australia/Brisbane)  
**Status** Exact finite intervention audit and a general locality argument for the tested readout model.

## Protocol

Prepare an indexed proper three-colour Hamiltonian cycle using [CROSS-46](CROSS-46-local-clock.md). Choose settings $x,y$ independently after preparation. Each setting selects the start of a length-three reversal attempt. The four-sign window determines eligibility and the update. If the reversal is ineligible, leave the word unchanged and still record an outcome. Each reader records a fixed sign immediately after its own attempt. The audit executes only the two requested attempts after preparation. This is an intervention using the original LR3 rule, independent of which update the clock would select. No run is discarded and all settings use the same preparation ensemble.

Use $S=\lvert E_{00}+E_{01}+E_{10}-E_{11}\rvert$, where $E_{xy}$ is the mean product of the two signs. The classical Bell-local bound is $S\le 2$ with setting independence. See [Brunner et al., Bell nonlocality, 2014](https://arxiv.org/abs/1303.2849), sections II and III and figure 4. The calculation is a combinatorial intervention test. A disjoint read-and-write support guarantees isolation in this protocol, and carries no claim of physical spacelike separation.

## Disjoint interventions

Reader A attempts at start 2 or 4 and reads sign 4. Reader B attempts at start $n-6$ or $n-4$ and reads sign $n-4$. Their supports, including eligibility checks and readout, are disjoint. Every setting pair was evaluated in both orders on every reachable protected-clock preparation through three insertions. The final word and both outcomes agreed across orders, and each outcome agreed with the outcome of its corresponding reader acting alone.

| Vertices | Prepared words | Exact CHSH score |
|---|---:|---:|
| 21 | 6 | $2/3$ |
| 22 | 144 | $5/18$ |
| 23 | 1,134 | $104/567$ |
| 24 | 4,560 | $43/380$ |

The preparation is uniform over the words at the stated size. A separate tight control weights clock phases 0 and 4 equally at size 21, uses the same two reversal settings per reader, and reads signs 2 and 19. It has unbiased marginals, correlations $(-1,+1,+1,-1)$, and $S=2$.

The bound for disjoint attempts is independent of the particular census. Let $\lambda$ be the prepared sign word. Each outcome is a function of only the local setting and $\lambda$, because the other attempt changes no sign used for eligibility or readout. The same functions are therefore defined for all four setting pairs on each preparation. The CHSH combination is plus or minus two pointwise, and averaging with a common preparation law gives $S\le 2$.

## Overlapping interventions

Use an equal mixture of the prepared 21-vertex phase-0 word and its colour reflection, which exchanges plus and minus throughout. The reflection is an explicitly supplied second preparation. Reader A attempts at start 2 or 6 and reads sign 2. Reader B attempts at start 0 or 8 and reads sign 8.

| Attempt order | $E_{00}$ | $E_{01}$ | $E_{10}$ | $E_{11}$ | $S$ |
|---|---:|---:|---:|---:|---:|
| A then B | -1 | -1 | -1 | +1 | 4 |
| B then A | -1 | -1 | +1 | +1 | 2 |

Every individual marginal is exactly unbiased in both orders. Colour reflection preserves reversal eligibility and flips both recorded outcomes, so averaging the two preparations hides the dependence visible at fixed preparation.

In the A-first order, B's start-8 window is ineligible initially. A's start-6 move changes the overlap at signs 8 and 9 and makes the start-8 move legal. B's own move then flips the sign at position 8. A's start-2 move leaves the start-8 reversal disabled. B's outcome at fixed preparation also depends on A's setting even when B uses the ineligible start-0 window, since A's start-6 move directly changes B's readout sign. The sequential overlap provides an explicit influence channel. A balanced marginal and a large Bell score can coexist with that channel.

## Scope

The sign model with disjoint classical interventions satisfies the Bell-local bound even when growth has correlated the preparations. The overlapping protocol is a control for hidden disturbance. The results concern these operational models. A local CHSH score does not rule out every entangled quantum preparation. A coherent preparation and incompatible measurements would require a separate model of the allowed operations and outcome probabilities.

Run `python3 research/cbb-binary/cross47_reversal_bell.py` from the repository root. The verifier computes exact rational correlations and checks each isolated trial in both orders. AI assistance was used for search, verification and writing.
