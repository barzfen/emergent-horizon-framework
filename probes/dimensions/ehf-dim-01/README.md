# EHF-DIM-01 — Graph-distance and return-probability audit

**Date:** 2026-11-19 (Australia/Brisbane)  
**Status:** Reproduced exact n=7 graph-distance results; spectral dimension **not established**.

## Goal
Test whether effective geometry changes when reversal rules change, holding the microscopic state space and parity-preserving chamber fixed. This is distinct from the dimensions of irreducible symmetry representations in [REV-03](../../reversals/ehf-rev-03/README.md).

## Model and controls
Canonical undirected Hamiltonian cycles of K7; parity label Pi fixed; OPW3 admits circular LR3 and OPW23 admits LR2 or LR3. Enumerate the same largest 36-state chamber for both graphs, following the [OPW3 definition](../../../research/source-documents/opw3-v0.6.md). Count graph balls B(r) including the root, averaged over roots (in these chambers counts are root-independent). Define simple random-walk transition P=D^{-1}A and mean return probability tr(P^t)/36.

## Exact finite results

| Quantity | OPW3 | OPW23 |
|---|---:|---:|
| Full graph states | 360 | 360 |
| Full graph edges | 600 | 840 |
| Full graph components | 19 | 19 |
| Largest chamber states | 36 | 36 |
| Chamber degree | 4 | 6 |
| Chamber diameter | 6 | 3 |
| B(0) | 1 | 1 |
| B(1) | 5 | 7 |
| B(2) | 13 | 27 |
| B(3) | 23 | 36 |
| B(4) | 31 | 36 |
| B(5) | 35 | 36 |
| B(6) | 36 | 36 |

Mean return probabilities (numerically evaluated from the real symmetric random-walk spectrum):

| t | OPW3 | OPW23 |
|---|---:|---:|
| 2 | 0.250000 | 0.166667 |
| 4 | 0.140625 | 0.066358 |
| 6 | 0.098633 | 0.039995 |
| 8 | 0.078674 | 0.031887 |
| 10 | 0.068287 | 0.029211 |
| 12 | 0.062649 | 0.028290 |

OPW3's graph is bipartite, so even-time returns tend toward 2/36 rather than 1/36; OPW23 is nonbipartite and tends to 1/36. Therefore a naive log-slope fit to these finite-size returns can be misleading. For a meaningful spectral-dimension analysis, first remove periodicity (e.g., lazy walk), account for finite stationary return, and identify a scale window away from both microscopic and saturation regimes.

## Interpretation
**Positive:** admissible reversal rules change the graph metric and diffusion behaviour on identical states.  
**Not established:** an asymptotic dimension, dimensional flow, physical spatial dimension, or a relation between 1/2/4 representation dimensions and geometric dimension. The 36-state chamber is too small for robust scaling fits.

## Next
1. Audit multiple chamber sizes at n=7 and n=9, not only the largest.
2. Calculate scale-dependent volume-growth slopes and lazy-walk spectral slopes, with confidence/fit-window sensitivity.
3. Compare with degree-matched randomized graphs and standard lattices of similar size; avoid fitting a dimension after observing the data.
4. Preserve the representation-theoretic question independently: whether a natural coarse-graining maps symmetry sectors to graph-geometric modes.

Run `python3 probes/dimensions/ehf-dim-01/probe.py` (requires numpy).
