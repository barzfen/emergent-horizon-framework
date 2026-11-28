# EHF-CBB-BIN-05 — Is odd-order LR3 mixing necessary?

Date: 2026-11-10. Exact finite enumeration, unrestricted labelled undirected Hamiltonian cycles and LR3. Reproduced locally with Python exhaustive search. No MICRO/Pi constraints, no physics inference.

## Protocol
Start with each of 60 cycles at n=6. Insert label 6 into one of 6 slots (n=7), apply k LR3 reversals at n=7, then insert label 7 into one of 7 slots (n=8). For exact-k path counts, count each sequence of slot choices and LR3 choices with multiplicity. In this n=7 graph each cycle has 7 distinct LR3 neighbours. For a source sector, aggregate uniformly over its 6 member cycles. For <=k reachability, allow at most k reversals and ignore multiplicities.

## Critical finding: no LR3 is needed for sector-level complete support
Even at k=0, **all 350 of 10x35 source-sector/destination-sector pairs are reachable** through two pure insertions. This strengthens and corrects the interpretation of BIN-04: odd-order LR3 connectivity is sufficient for all-pair sector reachability but **not necessary**. At the individual n=6 cycle level, pure insertion reaches 23 of 35 n=8 sectors; with at most one intermediate LR3 move, it reaches all 35.

## Exact-k uniform path-count results
At k=0, every source sector has 252 paths (6 starting cycles x 6 first slots x 7 second slots), with destination-sector counts in {4,12,36}. Hence destination probabilities in {1/63,1/21,1/7} and Shannon entropy 4.618740637 bits.

At k=1, every source sector has 1764 paths; destination-sector counts in {28,36,84,180} (probabilities {1/63,1/49,1/21,5/49}), entropy 4.843387716 bits.

At k=2, every source sector has 12348 paths; destination-sector counts in {228,284,540,972}, entropy 4.972187725 bits.

Uniform destination-sector distribution would have entropy log2(35)=5.129283017 bits. The entropy increase for these protocols measures **redistribution under a specified uniform path-counting rule**, not symmetry breaking or irreversible thermodynamics.

## Important controls and caveats
- The counts above aggregate over each source LR3 component. They do not mean every individual starting cycle has all 35 target sectors at k=0.
- Counting exact-k paths uniformly is one explicit sampling protocol, not a consequence of reachability. Distinguish it from uniform choice of reachable endpoint.
- Entropy here is the Shannon entropy of **destination sector labels**, not thermodynamic entropy.
- Full relabelling symmetry, growth birth labels, and automorphism actions need separate treatment before claiming intrinsic asymmetry.
- Previous BIN-04 claim that odd-order LR3 *provides* all-pair sector reachability is true but misleading as a causal explanation: two pure growth steps already provide all-pair sector reachability.

## Next tests
1. Determine the exact combinatorial formula for the k=0 destination-sector count distribution.
2. Analyze source-cycle-conditioned distributions and whether a single LR3 step erases source-specific constraints.
3. Repeat with the repository's MICRO and Pi constraints, where reachability may change.
4. Compare unbiased random LR3 versus controller-weighted transitions, and report total variation or mutual information rather than inferring physical effects.
