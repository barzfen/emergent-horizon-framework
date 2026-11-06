# Which doubled shuffle entries matter for the minus-minus exception?

The sign-only control replaces every nonzero signed orbit coefficient
by its sign. In the −− sector it creates an extra shared direction
and two extra union cancellations, whereas the exact calculation
has zero extra shared directions and one extra union cancellation.

## A doubled entry by hand

Consider the row 8234657 and the orbit of the word 124697538.
The KK expansion interleaves the prefix before 9 with the reversed
suffix after 9, leaving out the anchor 1. In the row 8234657 both
of the following interleavings occur:

| Word | Prefix | Reversed suffix |
| --- | --- | --- |
| 124697538 | 246 | 8357 |
| 125796438 | 257 | 8346 |

The second word comes from applying both swaps, (4 5) and (6 7).
In the −− character it gets sign +1, just like the original word.
Both KK signs are +1 since the suffix has length four. Neither
single swap reaches this row. The coefficient is therefore 1+1=2.
The saved output includes one two-term trace for each restoration group.

## Selective restoration and new cuts

In the reference union, group the 64 doubled entries by branch
membership, position of label 9 (counting the anchor as position 1),
and whether the row is active or exterior. This gives six groups.
Start with sign-only columns and exhaust all 64 subsets of these
groups, restoring exact magnitudes in the selected groups.

The smallest restoration by number of entries that recovers both
exception counts keeps all 28 doubles in the common cut with label 9
in position 5. It includes 12 active and 16 exterior entries. This
recovers the exception counts but changes other ranks. The smallest
restoration among these groups that recovers the full reference rank
profile keeps 48 entries. These minima are over whole groups, not
arbitrary subsets of entries.

The 28-entry rule was frozen before running the exact checks for 16
new cuts. Twelve were sampled with a fixed seed at sizes five and
six. Four were new five-orbit extensions of known obstructions.
The rule agreed on both exception counts in all 16. The −− exception
survived in 12 and was absent in four. This comparison is limited to
the −− sector and the tested cuts in the reference chart. It still
uses shuffle ranks and does not supply a rank-free selector.

## Reproduce

Run from followups with standard-library Python.

```sh
PYTHONPATH=.. python3 shuffle_doubles.py > shuffle-doubles-results.json
PYTHONPATH=.. python3 shuffle_doubles_holdout.py > shuffle-doubles-predictions.json
PYTHONPATH=.. python3 shuffle_doubles_holdout.py --verify > shuffle-doubles-verification.json
```

See the [group scan](shuffle-doubles-results.json), [frozen predictions](shuffle-doubles-predictions.json), and [exact verification](shuffle-doubles-verification.json).
