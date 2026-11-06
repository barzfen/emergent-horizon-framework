# An orbit-deletion rule for the nine-point shared residue

The folded images in the +− sector share exactly one direction. Fix a
nonzero residue on this line. In each branch the lifts of that fixed
residue form an affine space: one particular lift plus all lifts that
give zero folded image. Deleting an orbit sets its coefficient to zero
and gives one equation on the free parameters of that affine space.
The residue survives exactly when both branches can satisfy their
deletion equations. For two individually feasible deletions in the
same branch, the equations conflict exactly when their nonzero left
sides are proportional but their right sides disagree after the same
normalization. Different branches have independent lift parameters.

Using zero-based orbit IDs in [the mixed-orbit results](mixed-orbits-results.json), all ten
conflicting pairs take one orbit from each side of one of these rows:

| One side | Other side |
| --- | --- |
| 0, 6 | 7, 13 |
| 2, 4 | 14, 15, 16 |

The rule also predicts 22 rank-8 triples that conflict even though
every pair within them is feasible. Fresh shuffle calculations confirm
all 22 and six surviving controls. This rule is derived from the
shuffle equations in the reference chart. A rule reading the symmetry
signs directly from ordering geometry remains open, as does an analogous
deletion rule for the −− exception.

Run this command from the followups directory with standard-library Python.

`PYTHONPATH=.. python3 shared_residue_rule.py`.

See the [saved results](shared-residue-rule-results.json).
