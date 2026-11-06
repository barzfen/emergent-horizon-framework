# How many ordering orbits protect each exception?

The [position-family tests](sector-selection.md) showed that deleting one
whole family can remove one exception while leaving the other. Each of
the three sensitive families contains six symmetry orbits of four words.
This check tests all 63 nonempty subsets of orbits in each family using
unreduced exact shuffle equations in the affected symmetry sector.

| Branch | Position of 9 | Exception | Fewest orbits removed | Subsets of that size that remove it |
| --- | ---: | --- | ---: | ---: |
| Rank-8 | 5 | `+−` shared residue | 3 | 1 of 20 |
| Rank-8 | 7 | `+−` shared residue | 4 | 4 of 15 |
| Rank-9 | 3 | `−−` union cancellation | 6 | 1 of 1 |

In the rank-9 position-3 family, keeping any one of its six orbits is
sufficient for the `−−` exception to survive when all other orderings
outside the family remain available. The two rank-8 families show
selective dependence on combinations of orbits. These thresholds are
within individual families in the reference chart. They do not establish
minimum deletions across mixed families or derive the symmetry signs
from ordering geometry.

From this directory, run `PYTHONPATH=.. python3 sector_threshold.py`.
The [saved results](sector-threshold-results.json) record orbit
members and all subsets that remove each exception.
