# Testing local ordering rules for the nine-point exceptions

The conjecture tested here is that the branch, position of label 9,
and the labels immediately around it suffice to predict which
deletions remove the +− shared residue or the −− union cancellation.
Represent the swapped pairs (4,5) and (6,7) by A and B, and keep the
other labels. These features are invariant within each symmetry orbit.
All cuts remove whole orbits and keep the active words fixed.

The predictor learns the multisets of local features from the ten
known +− pairs and the four known −− quadruples. It predicts removal
when a cut contains one of those multisets. Its training features
already conflate removing and surviving cases. The purpose of the
holdout is to test whether those patterns still have predictive value
on larger cuts.

Freeze 24 mixed-position cuts for each sector, half predicted to
remove the exception. The +− holdout deletes four orbits and excludes
every cut containing a known conflicting pair or triple. The −−
holdout deletes five orbits and excludes cuts containing known
conflicting quadruples. A fixed seed selects the cuts before fresh
shuffle ranks are evaluated. All 48 holdouts preserve the relevant
exception, including the 24 predicted to remove it. These are
balanced challenge sets, not estimates of accuracy on random cuts.

## Matched counterexamples

Expanding the feature to two neighbours on each side still gives
different outcomes for identical feature multisets. Orbit IDs below
are zero-based and refer to mixed-orbits-results.json.

| Sector | Removes exception | Preserves exception |
| --- | --- | --- |
| +− | 0, 2, 16 | 0, 2, 17 |
| −− | 0, 1, 3, 14, 17 | 0, 1, 3, 14, 16 |

In both rows the only change is exchanging orbit 16 for orbit 17.
Their representatives are 139682475 and 139687425. Both look like
1, 3, 9, B, 8 in the two-neighbour window. Their remaining tails
differ. Three augmentations per sector preserve the feature equality
and the opposite outcomes. This rules out any deterministic classifier
using only the multiset of the tested window features, even with
a different decision rule. It leaves open rules using information
farther along the orderings or relations between the orderings.

## Reproduce

Run from followups with standard-library Python.

```sh
PYTHONPATH=.. python3 ordering_holdout.py > ordering-predictions.json
PYTHONPATH=.. python3 ordering_holdout.py --verify > ordering-verification.json
PYTHONPATH=.. python3 ordering_collisions.py > ordering-collision-results.json
```

See the [frozen predictions](ordering-predictions.json), [exact holdout verification](ordering-verification.json), and [matched counterexamples](ordering-collision-results.json).
