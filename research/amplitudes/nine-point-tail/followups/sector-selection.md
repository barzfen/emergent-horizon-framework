# Where the two nine-point symmetry exceptions arise

This study uses the reference chart and the rank-8 and rank-9 branches
from the nine-point shuffle-sector audit. The signs record the action
of (4 5) and (6 7) respectively.

Let S8 and S9 be the inactive KK shuffle spans, E the active coordinate
space, and P the projection onto exterior coordinates, with kernel E.
The space of additional active directions available when the branches
are joined satisfies

    ((S8+S9) ∩ E) / ((S8 ∩ E)+(S9 ∩ E))
      ≅ (P S8 ∩ P S9) / P(S8 ∩ S9).

To see this, lift a shared exterior vector to each branch and subtract
the lifts. The difference lies in E. Changing the lifts changes the
difference by a sum of separately active vectors. An exterior vector
lifts to the zero quotient class precisely when it comes from a
common vector in S8 ∩ S9.

In the exact reference-chart calculation the intersection of the
inactive spans is the common cut span in every sector.

| Sector | Shared exterior rank | Exterior rank from common span | Excess |
| --- | ---: | ---: | ---: |
| ++ | 35 | 35 | 0 |
| +− | 36 | 36 | 0 |
| −+ | 36 | 36 | 0 |
| −− | 36 | 35 | 1 |

The −− direction therefore first appears in the exterior matching
step. The orientation fold kills it. The +− direction instead first
appears as an extra intersection between the folded images of the
separately active branch spaces. These are different mechanisms.

Removing the 24 branch-exclusive words in a fixed position of label 9
removes six symmetry orbits at a time. Positions count the anchor as 1.
In the table, 1 indicates that the original exceptional dimension survives.

| Branch | Position of 9 removed | +− shared residue | −− union cancellation | Union transmitted rank |
| --- | ---: | ---: | ---: | ---: |
| Rank-8 | 3 | 1 | 1 | 14 |
| Rank-8 | 5 | 0 | 1 | 14 |
| Rank-8 | 7 | 0 | 1 | 14 |
| Rank-9 | 3 | 1 | 0 | 14 |
| Rank-9 | 5 | 1 | 1 | 14 |
| Rank-9 | 7 | 1 | 1 | 14 |

All six cuts are contained in the original union and retain its
transmitted rank, so the transmitted union subspace itself is unchanged.
The rank-8 branch drops to transmitted rank 7 in the two cuts that lose
the +− exception. The rank-9 position-3 cut removes the −− exception
while preserving the transmitted ranks of both branches.

Run `PYTHONPATH=.. python3 sector_ablation.py > sector-ablation-results.json`
from followups with standard-library Python. Each ablation is checked
with and without support reduction. This is an exact reference-chart
diagnosis of the two mechanisms and their support dependence. A
rank-free rule deriving the selected signs directly from the ordering
geometry remains open.

See the [saved exact results](sector-ablation-results.json).
