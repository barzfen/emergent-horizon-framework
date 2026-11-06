# How the distant tails change the nine-point matching equations

The matched ordering test found opposite outcomes when orbit 16
was exchanged for orbit 17. Their representatives, 139682475
and 139687425, have the same two-neighbour window around 9 after
the exchanged label pairs are identified.

The KK expansion shuffles the prefix before 9 with the reversed
suffix after 9, preserving each list's internal order. In orbit 16
both labels from (4,5) precede label 2 in the reversed suffix.
In orbit 17 exactly one does. Swapping labels within either pair
does not change the count. Thus the two orbit columns have disjoint
shuffle support. The exact exterior supports have 24 rows each
in both +− and −−.

To connect this difference to the two matched cuts, take the
following linear functionals on coefficients of the signed orbit
columns. In +−, impose that the folded rank-8 image belongs to the
folded rank-9 span. In −−, impose that the union lift has zero
folded image, including zero exterior coordinates. On those
respective solution spaces, the script derives these identities:

| Sector | Target functional | Orbit-coefficient expression |
| --- | --- | --- |
| +− | A coordinate nonzero on the shared residue line | c₂ + c₁₆ |
| −− | A coordinate nonzero on the exterior gluing class | −c₁ − c₃ + 2c₁₄ − c₁₇ |

The script verifies each identity on every original signed orbit
column after including the listed constraint-row combination.
Deleting the orbits on the right forces the target to zero.
For each matched surviving cut, the script separately finds a
feasible coefficient vector with nonzero target. The coefficients
and coordinates depend on the reference chart and normalization.

Run `PYTHONPATH=.. python3 tail_shuffle_trace.py` from followups
with standard-library Python. The output gives the exact row
combinations and support checks. This explains the two matched
examples. A geometry-only rule for which shuffle supports can
combine to give either exception remains open.

See the [exact trace](tail-shuffle-results.json).

The [support test](support-sector-test.md) checks whether occupied shuffle rows alone recover the exceptional sectors.
