# EHF-CBB-CROSS-63 — Growth estimates from tracked E. coli lineages

[Series guide](GROWTH-CLOCKS-AND-BELL.md) · [CROSS-62 ring estimator](CROSS-62-blind-growth.md) · [Verifier](cross63_ecoli_lineage.js)

**Date** 2026-11-17 (Australia/Brisbane)

**Status** Exploratory reanalysis of six existing microscopy recordings.

## Test the choice of daughter against observed growth

In the ring model of [CROSS-62](CROSS-62-blind-growth.md), the two daughter slots have the same sign after a split. Following a fixed daughter therefore has the same hit-count law as choosing one at random. This pilot asks how a fixed biological rule, following the daughter that inherits the parent's older pole, changes the estimate on recorded bacterial families.

Use the six public `CellDf_wAge.csv` tables associated with Nakatani et al. (2022). The recordings cover three glucose-control and three glucose-deficient cultures. The study tracked cells in hourly fluorescence images. Its pole-age algorithm used the positions and relationships of cells in their family trees. The pilot uses these inferred age labels. [Article and methods](https://doi.org/10.1038/s41598-022-22189-x) · [Pinned data and analysis code](https://github.com/funalab/pyCellLineage/tree/60008ee698e23f6400bd62fb1a60579188e09377) · [Pole-age assignment code](https://github.com/funalab/pyCellLineage/blob/60008ee698e23f6400bd62fb1a60579188e09377/LIAnalysis/cellular_ageTracking.py)

## Choose the same cutoff for every path

Use frames 8–12, inclusive, as the main window, with exploratory checks that move the entire window one frame earlier or later. Each cell recorded at the start is a candidate root. Trace both daughter links at every division and the single continuation link when a cell persists to the next frame. Require reciprocal parent links, consecutive frames, and cell identities consistent with either continuation or division. Check the cutoff count by tracing backward from the endpoint frame and by checking that each included tree has one more leaf than splits.

For the pole comparison, require a known pole age at the root. At every division within a retained tree, require the recorded ages to identify exactly one daughter of age one and one daughter whose age is the parent's plus one. This rule restricts the comparison to internally consistent age assignments. All retained families reach the same endpoint frame through their recorded branches. The reference is the tracked descendant count of those roots in the endpoint frame.

A lineage that sees $H$ divisions estimates $2^H$ descendants from its single starting cell. Sum those estimates for all retained roots. Compare always following the older pole, always following the newer pole, and choosing either daughter with equal probability. In the random control a terminal leaf at depth $h$ is reached with probability $2^{-h}$, so the exact conditional mean is the number of tracked leaves. This is the established branching-tree identity applied by Genthon and Lacoste to lineage-based growth inference. [Genthon and Lacoste, equation 4](https://pmc.ncbi.nlm.nih.gov/articles/PMC7367869/#Sec3)

## Results

| Frames | Candidate roots | Retained roots | Tracked descendant count | Random-choice mean | Always older | Always newer |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 7–11 | 96 | 40 | 75 | 75 | 74 | 76 |
| **8–12** | **129** | **54** | **93** | **93** | **97** | **89** |
| 9–13 | 150 | 67 | 116 | 116 | 122 | 110 |

In the main window, 75 of 129 candidate roots were excluded by the pole-age requirements. All candidate roots passed the track-completeness checks for that window. Of the 54 retained trees, 31 contained at least one division and six had different depths across their terminal leaves. Following the older pole overestimated five of those trees and underestimated one. At the pooled level, the older-pole estimate was $97/54=1.796$ descendants per starting cell, compared with $93/54=1.722$ observed, an overestimate of 4.3%. Under independent fair choices for each retained tree, the exact pooled total has standard deviation $\sqrt{6}$, and the probability of a total at least as high as 97 is $7/64$. That probability describes resampling on these recorded trees.

| Recording, frames 8–12 | Retained roots | Tracked descendants | Always older | Always newer |
| --- | ---: | ---: | ---: | ---: |
| Glucose-deficient 1 | 8 | 21 | 22 | 20 |
| Glucose-deficient 2 | 18 | 28 | 28 | 28 |
| Glucose-deficient 3 | 2 | 3 | 3 | 3 |
| Glucose-control 1 | 4 | 7 | 7 | 7 |
| Glucose-control 2 | 12 | 20 | 22 | 18 |
| Glucose-control 3 | 10 | 14 | 15 | 13 |

For a concrete example, the glucose-deficient sample 1 root `uID=63` at frame 8 has three descendants at frame 12. The fixed older-pole path follows two divisions and estimates four. The newer-pole path follows one division and estimates two. A fair tracker reaches the depth-one branch with probability one-half and the two depth-two endpoints with probability one-quarter each. Its mean is three.

The sign of the pooled older-pole error changes across the overlapping windows. These are descriptive results for retained families, with pole ages inferred by the source analysis. The cutoff counts use the published tracks, and the audit checks those tracks in both directions. An independent image-level count or a broader comparison across colonies would address separate measurement and sampling questions.

## Reproduce

From the repository root run `node research/cbb-binary/cross63_ecoli_lineage.js` with a Node version that supplies `fetch`. The verifier retrieves the six CSVs at the pinned public commit. It prints the inclusion counts, estimates by recording, pooled fair-choice distributions, and per-root details.
