# Does the doubled-entry rule survive a change to the common cut?

The previous study restored only the doubled coefficients in the
common orderings with label 9 in position 5. That reproduced the
reference −− exception counts and matched 16 cuts that removed
branch-exclusive orbits. This test freezes the rule and removes
common inactive symmetry orbits from both branches and the union.
Active orderings stay fixed. An entry removed with its orbit is
absent from both calculations.

The 63 cuts include every one of the 36 single-orbit deletions,
three whole position families, 12 pairs sampled from position 5,
and 12 sampled triples with one orbit per position family. The
samples use a fixed seed. Compare two quantities in the −− sector:
the extra shared residue dimension and the extra union cancellation
dimension. Full exact calculations are run only after saving the
predictions.

Run from followups with standard-library Python.

```sh
PYTHONPATH=.. python3 common_cut_holdout.py > common-cut-predictions.json
PYTHONPATH=.. python3 common_cut_holdout.py --verify > common-cut-verification.json
```

## Results

The rule matched 61 of 63 cuts, including all 60 single, pair and
triple deletions tested. Two complete position-family cuts fail.

| Common family removed | Predicted extra cancellations | Exact extra cancellations | Original exterior class survives |
| --- | ---: | ---: | --- |
| Position 3 | 2 | 3 | Yes |
| Position 5 | 0 | 1 | Yes |
| Position 7 | 1 | 1 | No |

In all three rows the extra shared-residue dimension in the −−
sector is zero. The position-5 cut removes all entries retained by
the rule. The full coefficients still support the original exterior
match. The position-7 cut preserves the number of extra cancellations
but removes the original class. Its cancellation comes from another
direction relative to the modified branches.

The class check uses the original folded-kernel affine equations,
including the original common exterior span. It tests whether
any representative of the original nonzero exterior class can
satisfy the new zero-coefficient constraints. Run
`PYTHONPATH=.. python3 common_cut_class.py > common-cut-class-results.json`
from followups after the exact checks.

See the [frozen predictions](common-cut-predictions.json), [exact verification](common-cut-verification.json), and [original-class checks](common-cut-class-results.json).
