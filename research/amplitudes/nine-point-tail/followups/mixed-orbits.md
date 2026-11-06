# Two-orbit deletions across ordering families

The [within-family study](sector-threshold.md) found minimum deletions
of three, four and six orbits in its three sensitive families. Here we
test every pair of distinct branch-exclusive symmetry orbits, allowing
different positions of label 9 and different branches. There are 36
orbits and 630 pairs.

The exact scan first builds the space of coefficient vectors satisfying
the exterior equations in each original cut. A deletion imposes zero
coefficients for the removed orbit variables in this space. Taking the
kernel of those extra constraints gives precisely the lift space of the
smaller cut. The script rebuilds the modified shuffle columns for all
extinguishing pairs and one fixed control pair and checks equality of
the resulting active spaces in the affected sector.

Ten pairs remove the `+−` shared residue. All ten lie in the rank-8
branch and mix positions of label 9. Five mix positions 3 and 7, three
mix 3 and 5, and two mix 5 and 7. Exact checks in all sectors on these
ten cuts retain the `−−` exception and the 14-dimensional transmitted
union. The transmitted union is a subspace of the original one, so
equal dimension certifies equality.

Every pair preserves the `−−` exception. Together with the
[single-orbit scan](support-reduction.md), the exact minimum among
branch-exclusive orbit deletions is two for `+−`. For `−−`, the
minimum lies between three and six inclusive. The upper bound comes
from removing the rank-9 position-3 family.

Run `PYTHONPATH=.. python3 mixed_orbits.py` from this directory.
The [saved results](mixed-orbits-results.json) give the members of
each orbit and the exact list of extinguishing pairs.
