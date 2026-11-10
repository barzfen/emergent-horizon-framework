# EHF-CBB-BIN-06 — Mutual information and coarse-grained memory

Date: 2026-11-10. Status: exact finite-state enumeration; unrestricted LR3, no MICRO/Pi constraints. No physics claim.

## Protocol
X is uniform over all 60 undirected labelled Hamiltonian cycles at n=6. Insert vertex 6 uniformly into one of six edges, take exactly k independent uniformly selected LR3 moves at n=7 (seven distinct neighbours per state), then insert vertex 7 uniformly into one of seven edges. Y is the connected-component index of the resulting n=8 cycle under LR3 (35 components of 72 states). Also measure Z, the n=6 LR3 component of X (10 components of six states). All distributions are obtained by exhaustive integer path counts, not Monte Carlo.

## Exact numerical results (bits)
| k | H(Y) | H(Y given X) | I(X;Y) | I(Z;Y) |
|---:|---:|---:|---:|---:|
| 0 | 5.129283017 | 4.225185280 | 0.904097737 | 0.510542380 |
| 1 | 5.129283017 | 4.710253664 | 0.419029353 | 0.285895301 |
| 2 | 5.129283017 | 4.916218447 | 0.213064570 | 0.157095292 |
| 3 | 5.129283017 | 5.019236559 | 0.110046458 | 0.084592972 |
| 4 | 5.129283017 | 5.072202285 | 0.057080732 | 0.045003325 |
| 5 | 5.129283017 | 5.099671432 | 0.029611585 | 0.023736963 |
| 6 | 5.129283017 | 5.113947814 | 0.015335202 | 0.012433131 |
| 8 | 5.129283017 | 5.125200236 | 0.004082780 | 0.003355250 |
| 10 | 5.129283017 | 5.128205643 | 0.001077374 | 0.000891456 |

At each k, Y is exactly uniform across the 35 destination sectors when X is uniform across all 60 cycles, since each insertion has a unique deletion parent and the n=7 LR3 graph is 7-regular and undirected. Thus H(Y)=log2(35) for all k. Conditional on a particular starting cycle or sector, the distribution is generally nonuniform.

The earlier BIN-05 entropies 4.618740637, 4.843387716, 4.972187725 are H(Y|Z=z) for a fixed source LR3 sector z, NOT overall H(Y); due to symmetry the value is the same for each source sector. Hence I(Z;Y)=log2(35)-H(Y|Z). This corrects any ambiguous wording in BIN-05.

At k=0, each individual source cycle reaches 23 of 35 target sectors; at k>=1, each reaches all 35. Exact-k paths from each source cycle number 6*7^k*7; over 60 source cycles total 2520*7^k.

## Interpretation
Mutual information about the starting cycle or starting LR3 sector survives in the coarse-grained destination label and decreases with k in the computed range. The sequence of stochastic LR3 steps forms a Markov chain, so the data-processing inequality also ensures I(X;Y_k) cannot increase with k when the final insertion/output channel is held fixed and the intermediate n=7 chain is iterated under a stationary uniform distribution with reversible transitions; a direct general proof for this specific comparison should explicitly use reversibility/spectral properties, rather than assume the standard data-processing inequality alone compares Y_k and Y_{k+1}. This is coarse-grained information loss, not destruction of full path history, physical entropy production, or demonstrated irreversible dynamics.

## Reproducibility
Canonicalize undirected cycles by rotating label 0 to first and taking lexicographically smaller traversal direction. Enumerate all permutations of the remaining labels, quotient reversal. LR3 reverses three consecutive cyclic positions. Compute connected components at n=6 and n=8. For each n=6 cycle, use a Counter over n=7 cycles initialized with its six insertion children. Repeat k times: for each intermediate cycle and its count, add count to each distinct LR3 neighbour. For every intermediate state, insert label 7 at all seven slots and tally the resulting n=8 component. Normalize integer joint counts over 60*6*7^k*7. Compute H(Y), H(Y|X), I(X;Y), and I(Z;Y). Verify all n=7 degrees equal 7, n=8 components equal 35 of size 72, and each Y sector has exactly 72*7^k paths across all X (per k).

## Next
Derive the spectral mixing rate for the n=7 LR3 random walk and test whether coarse-grained information decay is governed by its nontrivial eigenvalues. Repeat under MICRO/Pi restrictions and controller-weighted LR3 transitions, clearly specifying the admissible state spaces.
