# Nine-point support reduction and modified-cut test

The nine-point shuffle-sector audit identified two extra directions.
The +− sector has an extra shared folded residue. The −− sector has
an extra cancellation available only after the branch supports are united.

Each inactive signed orbit contributes one KK shuffle column per sector.
To lift an active coefficient vector, every exterior row must vanish.
A row with one nonzero entry forces its variable to zero. A row with two
entries a and b forces the two variables into the ratio −a/b. Following
these ratios gives bundles controlled by one variable each. A bundle
vanishes if it contains a forced zero or has an inconsistent ratio around
a cycle. Substituting the surviving bundles leaves a smaller exact
linear problem. Higher-degree exterior rows and the orientation fold
still require linear algebra.

The original union uses 72 orbit variables per sector. The reduction
leaves 51, 60, 59 and 63 in ++, +−, −+ and −− respectively. The
remaining equations recover both exceptional sectors.

## Modified cut

The test removes the lexicographically first inactive symmetry orbit
exclusive to the rank-9 branch, also removing it from the union. Its
first word is (1,6,4,2,5,3,9,7,8). The reduced method predicted the
modified ranks before the unreduced calculation was run.

| Cut | Original active rank | Modified active rank | Transmitted rank in both |
| --- | ---: | ---: | ---: |
| Rank-8 branch | 19 | 19 | 8 |
| Rank-9 branch | 29 | 25 | 9 |
| Union | 47 | 43 | 14 |

Both exceptional directions survive. The scan then removes each of
the 36 branch-exclusive inactive symmetry orbits individually, 18 from
each branch. Every deletion preserves all three transmitted ranks
and both exceptional dimensions. Since these deletions only shrink
the source supports, equal transmitted ranks also imply equal
transmitted subspaces. Neither exception needs one indispensable
branch-exclusive orbit in this test. The scan does not rule out a
small support for any particular witness or explain sector selection
from geometry alone.

## Reproduce

From the followups directory, run the following with standard-library Python.

```sh
PYTHONPATH=.. python3 support_reduction.py
PYTHONPATH=.. python3 support_reduction.py --verify
PYTHONPATH=.. python3 support_reduction.py --scan
PYTHONPATH=.. python3 support_reduction.py --scan --verify
```

The verification path uses the same exact shuffle construction and
omits the bundle reduction. The reduction is an exact preconditioner
for the lift equations. This test measures variables removed and
does not benchmark runtime.

Saved output is available for the [prediction](support-reduction-prediction.json), [unreduced verification](support-reduction-verification.json), [orbit scan](support-reduction-orbit-scan.json), and [unreduced scan](support-reduction-orbit-verification.json).
