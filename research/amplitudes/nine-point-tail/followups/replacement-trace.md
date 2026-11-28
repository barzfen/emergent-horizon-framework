# Where the position-7 replacement cancellation came from

Remove all 12 common inactive symmetry orbits with label 9 in
position 7. In the minus-minus sector, the exact calculation finds
one extra cancellation in the modified union. The original exterior
class is absent.

The script extracts a 64-coordinate representative of the replacement.
It is in the sum of the two original separately active branch spaces,
but outside either original branch individually. It lies outside the
sum of the modified separately active spaces. The output includes
a decomposition into two original branch lifts.

All original decompositions of this fixed vector form an affine
space. Keeping an orbit deleted requires its coefficient to vanish
in each branch. Solving the resulting equations for every addback
set of size at most four predicts no successful set of size zero
through three. Exactly three size-four sets work. Fresh shuffle
calculations check the fully deleted cut, all 12 single addbacks,
and the three successful size-four sets.

| Restored orbit IDs | Replacement splits again | Original class survives | Extra cancellations |
| --- | --- | --- | ---: |
| 0, 2, 3, 9 | Yes | No | 0 |
| 0, 9, 10, 11 | Yes | Yes | 1 |
| 2, 3, 10, 11 | Yes | Yes | 1 |

Orbit IDs are zero-based and refer to the position-7 representatives
in the output. Adding back only orbit 7, 10, or 11 brings back the
original class while leaving the replacement exceptional. The exact
count rises to two in each case.

Run `PYTHONPATH=.. python3 replacement_trace.py > replacement-trace-results.json`
from followups with standard-library Python. This is an exact
reference-chart calculation about the fixed replacement class under
position-7 addbacks.

The [saved results](replacement-trace-results.json) include the vector, its original decomposition, and the exact addback checks.
