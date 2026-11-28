# Can occupied shuffle rows predict the symmetry sectors?

The [tail trace](tail-shuffle-trace.md) explains why two particular
ordering orbits reach disjoint exterior rows. This test asks if the
pattern of nonzero entries alone predicts the two exceptions.

Treat each nonzero entry as independently variable. A maximum matching
between columns and occupied rows gives the generic rank of that
support pattern. In all four sectors, each branch and the union can
match every inactive column to a distinct exterior row. Thus this
support-only calculation predicts no active images and neither
exception. The exact matrices do have active images. Their entries
are linked by signed shuffle sums, so generic independence is a poor
model for them.

We also tested two controlled changes to the signed orbit columns
before the orientation fold. One keeps the absolute values and
discards signs. The other replaces each nonzero entry by +1 or −1
while retaining its sign. Both preserve the original column supports.

| Calculation | Extra shared directions | Extra union cancellations |
| --- | --- | --- |
| Exact | One in `+−` | One in `−−` |
| Support matching | None | None |
| Magnitudes only | None | None |
| Signs only | One each in `+−` and `−−` | Two in `−−` |

These are exact reference-chart controls. They rule out generic
matching as the predictor and show that the support and signs do not
protect the result against changes of coefficient magnitudes. They
do not rule out a combinatorial rule that reconstructs the correlated
signed shuffle counts from the orderings.

Run `PYTHONPATH=.. python3 support_sector_test.py` from this directory.
See the [saved ranks](support-sector-results.json).

The [doubled-shuffle follow-up](shuffle-doubles.md) tests which coefficient magnitudes need to be restored.
