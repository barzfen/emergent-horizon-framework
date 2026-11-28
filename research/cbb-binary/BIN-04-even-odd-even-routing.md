# EHF-CBB-BIN-04 — Even–odd–even sector routing

Date: 2026-11-10. Status: exact finite enumeration for n=4..8, unrestricted LR3. Not a theorem for all orders and not a physics result.

## Definitions
Use undirected labelled Hamiltonian cycles on {0,...,n-1}, modulo rotation and reversal. Canonicalize by rotating 0 to first position and choosing the lexicographically smaller direction. LR3 reverses any three consecutive vertices (cyclic indices); discard moves returning the same canonical cycle. Connected components are computed by graph search. All-slot insertion adds the new largest label at each of the n cycle edges. This is **unrestricted** LR3: no MICRO or Pi preservation constraints.

## Exact results
| n | cycles | LR3 components | uniform component size |
|---|---:|---:|---:|
| 4 | 3 | 3 | 1 |
| 5 | 12 | 1 | 12 |
| 6 | 60 | 10 | 6 |
| 7 | 360 | 1 | 360 |
| 8 | 2520 | 35 | 72 |

| transition | source components | destination components | insertion edges | component-pair counts |
|---|---:|---:|---:|---|
| 4->5 | 3 | 1 | 12 | each of 3 source components contributes 4 |
| 5->6 | 1 | 10 | 60 | each of 10 destination components receives 6 |
| 6->7 | 10 | 1 | 360 | each of 10 source components contributes 36 |
| 7->8 | 1 | 35 | 2520 | each of 35 destination components receives 72 |

## Finite-order consequence
At 6->7->8, from any starting n=6 LR3 component, one can insert to n=7, move by unrestricted LR3 within the single connected n=7 component, and insert into any prescribed n=8 component (because every n=8 cycle has a deletion parent at n=7). Thus every source n=6 sector can reach every target n=8 sector through growth and odd-order LR3 mixing. This is an **existence of paths**, not a probability claim and not evidence of persistent asymmetry. If no LR3 is allowed at the intermediate order, additional reachability tests are needed.

## Interpretation
Even-order sector separation and odd-order sector connectivity alternate in these examples. The construction is symmetric under vertex relabelling (with the distinguished birth label for insertion). No nontrivial binary invariant, history memory, chirality or physical symmetry breaking has been demonstrated. Uniform counts of insertion incidences do not establish uniform dynamics without an explicit transition kernel.

## Reproducibility
Reuse the exact canonical-cycle and LR3 code in BIN-03. For each source cycle C, generate n children by inserting n as a new vertex after each cyclic position, canonicalize, and count ordered pairs (component_id(C),component_id(child)). Verify sums n*|H_n|=|H_{n+1}| and destination uniqueness under deletion. Results above are obtained by this deterministic enumeration.

## Next
Define and compare three protocols: (A) pure two-step all-slot insertion, (B) insertion + one or bounded LR3 moves at odd n, (C) insertion + full odd-order LR3 reachability. For each, calculate sector-to-sector support and, only after specifying sampling rates, transition probabilities. Separately retrieve the exact Pi and MICRO constrained variants and avoid conflating their components with the unrestricted baseline.
