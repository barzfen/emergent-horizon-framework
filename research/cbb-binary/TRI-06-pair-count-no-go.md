# EHF-CBB-TRI-06 — Pair-transition invariants and a no-go result for balanced three-colour cycles

Date: 2026-11-10. Status: analytic theorem plus exhaustive n=15 verification. This probe does not yet classify all connected components.

## Setup
A proper cyclic three-colour word has no equal adjacent colours. Balanced n=3m means m occurrences of each A,B,C. Legal LR3 swaps the endpoints of a three-position segment, provided the resulting word remains proper. We work with cyclic colour bracelets (rotation and reversal identified).

## Theorem 1: unordered edge-pair counts are conserved
For each unordered distinct pair X,Y, let N_XY count cyclic edges joining those colours. Every nontrivial properness-preserving LR3 move has the local form XYXZX <-> XZXYX for three distinct colours. Both sides have exactly two XY edges and two XZ edges in the four-edge local window; all other edges are unchanged. Hence N_AB, N_BC, N_CA are invariant.

## Theorem 2: balance forces these counts
For proper cyclic words, each colour A has two incident edges per occurrence:
N_AB + N_AC = 2 n_A.
Likewise N_AB + N_BC=2 n_B and N_AC + N_BC=2 n_C.
Solving:
N_AB=n_A+n_B-n_C;
N_BC=n_B+n_C-n_A;
N_CA=n_C+n_A-n_B.
In the balanced case n_A=n_B=n_C=m, all three counts equal m. Thus these invariants provide *no distinction whatsoever* between balanced admissible cycles, despite being conserved.

## Theorem 3: directed transition counts are determined by balance and winding
Let D_XY count oriented cyclic transitions X->Y. The net directed flux at each colour is zero on a closed cycle, implying
D_AB-D_BA = D_BC-D_CB = D_CA-D_AC =: J.
With the orientation convention A->B->C->A positive, the winding number W=(sum of +/-1 steps)/3 equals J. Hence
D_AB=D_BC=D_CA=(m+W)/2,
D_BA=D_CB=D_AC=(m-W)/2
in the balanced case. Reversal changes W to -W, so on undirected bracelets the entire directed-transition multiset up to reversal is fixed by |W|. Thus directed pair counts cannot refine the winding classification.

## Exact n=15 check
For n=15, m=5, enumerate 5196 proper balanced linear words, 174 dihedral bracelets and 56 LR3 bracelet components (as in TRI-05). Every bracelet has unordered edge counts (5,5,5). The 174 bracelets have |W| distribution 152 at 1, 21 at 3, 1 at 5. For each fixed |W|, all directed edge-count vectors agree up to reversal. Nevertheless the |W|=1 set has many disconnected mobile components. Therefore even all six directed pair-transition counts fail to classify these sectors.

## Reproducibility
Run TRI-05 enumeration, then for each bracelet representative w compute:
```python
from collections import Counter
n=len(w)
d=Counter(w[i]+w[(i+1)%n] for i in range(n))
assert d['AB']+d['BA']==n//3
assert d['BC']+d['CB']==n//3
assert d['CA']+d['AC']==n//3
J=d['AB']-d['BA']
assert J==d['BC']-d['CB']==d['CA']-d['AC']
```
The assertion is exact for any balanced proper cyclic three-colour word with length divisible by three.

## Interpretation and next
The local move conserves pair-edge counts, but fixed colour multiplicities already determine them. This is a useful *no-go* result: pairwise adjacency statistics and directed colour-transition counts cannot explain fragmentation beyond winding in the balanced model. Candidate next descriptors must be sensitive to higher-order cyclic ordering, such as arrangements of five-letter active motifs or sign-run structure. These candidates must be tested for conservation; no new invariant is claimed here. This is discrete combinatorics, not SU(3) physics.
