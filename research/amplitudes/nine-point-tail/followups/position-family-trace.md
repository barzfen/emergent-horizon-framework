# Where the additional position-3 cancellations came from

Work in the reference chart and the minus-minus symmetry sector.
For each deletion of a whole common position family, let K be
the modified union's orientation-cancelling active space, J the
modified sum of the separately active branches, and J0 the original
sum. The exceptional space is K/(K intersect J).

Because J is contained in J0, the map from this quotient to the
original exceptional quotient sends a class to its original class.
Its kernel is (K intersect J0)/(K intersect J). Directions in this
kernel were already expressible as sums of original branch vectors.
They become exceptional when the deletion removes that ability.
The image measures how much of the original exceptional space survives.

| Position removed | Modified union cancellations | Still split in modified branches | Original class survives | Become exceptional |
| --- | ---: | ---: | ---: | ---: |
| 3 | 5 | 2 | 1 | 2 |
| 5 | 4 | 3 | 1 | 0 |
| 7 | 4 | 3 | 0 | 1 |

In position 3, the chosen two additional vectors have 64 and 88
nonzero active coordinates. The script verifies a decomposition of
each into two original branch lifts and a separate lift in the
modified union. Both additional classes are independent modulo the
modified branch sum. Position 7 uses the same mechanism but loses
the original class, as the replacement trace previously showed.

Run `PYTHONPATH=.. python3 position_family_trace.py > position-family-trace-results.json`
from followups with standard-library Python. The exact output includes
the vectors and their lifts. The scope is the three tested position
families in the reference chart and the minus-minus sector.

See the [exact vectors and lifts](position-family-trace-results.json).
