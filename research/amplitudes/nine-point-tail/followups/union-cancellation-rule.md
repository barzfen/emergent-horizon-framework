# Deletion rule for the nine-point minus-minus cancellation

Work in the reference chart and in the −− character. A union lift
that cancels after orientation folding lies in the kernel of the
folded shuffle map. This map also retains exterior coordinates, so
these lifts already satisfy the exterior equations.

For such a lift, take the exterior part contributed by rank-8-only
columns, modulo the exterior span of the common cut. This records
the exterior match between the branches. Assigning the common
columns to either branch changes only the representative. By the
exterior overlap quotient in the sector-selection study, a nonzero
class certifies an active direction outside the sum of the original
separately active branch spaces. The class map on cancelling lifts
has rank one in this chart.

Normalize one nonzero class to 1. The cancelling lifts with that
class form an affine space. Each deletion sets one orbit coefficient
to zero and hence imposes one linear equation on this space. If these
equations are consistent, the original exception survives. This
criterion tests survival of the original exterior class. For the
cuts that first kill it, fresh rank calculations also check that
no replacement exception occurs in the modified −− sector.

All 7,140 triples preserve the class. Exactly four of the 58,905
quadruples kill it. All four use rank-8 orbits and mix positions of label 9.
The precise orbit IDs and rational inconsistency certificates are
in the saved output. Fresh shuffle calculations confirm the −−
exception is absent on all four cuts. Thus the minimum is four
among the 36 branch-exclusive orbits. This is compatible with the
earlier six-orbit threshold when deletion is confined to the
rank-9 position-3 family.

Run `PYTHONPATH=.. python3 union_cancellation_rule.py 4` from
followups with standard-library Python. Orbit IDs are zero-based
and refer to the included mixed-orbits-results.json. The rule is
derived from the shuffle equations in the reference chart.

See the [saved exact results](union-cancellation-rule-results.json).
