# Soft radiation in a region that follows the shrinking gluon pair

This continues the [matched six-gluon radiation test](matched-radiation.md)
using the same tree MHV assignment, recoil, leading-soft current and frozen
hard pole. The soft limit is taken first. At each opening t, a direction
is proportional to (1, a y, a z), where a = 2t/(1−t²). The daughters have
scaled coordinates (0, ±1). Use uniform area in the scaled (y,z) disk
of radius 1.8, excluding disks of radius 0.35 around both daughters.
A radius of 0.50 tests sensitivity to the cut. The harmonic is
(z²−y²)/(z²+y²).

At small t, the two daughter denominators are each of order t²
and their mutual numerator is of order t². The resulting direct pair
kernel scales as 1/t². Thus a hard pair-correlation shift of order t²
gives an order-one change in the unscaled mean radiation, or an order-t²
relative correction to its leading 1/t² behaviour. The angular
contrast difference also starts at order t².

## Results

| Beam tilt | Contrast correction | Direct pair contribution | Pole–finite interference |
| ---: | ---: | ---: | ---: |
| 0° | +0.93465 | +0.06273 | +0.80918 |
| 10° | +0.87339 | +0.06691 | +0.73957 |
| 20° | +0.70720 | +0.07879 | +0.54961 |

The direct contribution is grouped by emitter pair. The interference
column is grouped by hard-amplitude bilinear. The [saved output](tracking-radiation-results.json) gives
the full cross-tabulation. With the wider exclusion, the direct share
of the contrast correction ranges from 9% to 14%, and interference
still dominates.

| Beam tilt | Mean radiation difference | Direct pair | Daughter–spectator |
| ---: | ---: | ---: | ---: |
| 0° | −6.298 | −20.152 | +13.854 |
| 10° | −5.692 | −21.495 | +15.803 |
| 20° | −4.036 | −25.311 | +21.275 |

These are constant-order differences in the unscaled mean. The direct
pair term is large but mostly offset by the daughter–spectator terms.
As a cross-check, dividing the direct mean by the patch average of the
limiting ordered-pair kernel, −4/[(y²+(z−1)²)(y²+(z+1)²)], recovers
the hard-pair coefficients 10.71903, 11.43317 and 13.46292.

Run `OPENBLAS_NUM_THREADS=2 python3 tracking_radiation.py > tracking-radiation-results.json`
with Python and NumPy. The 192 and 384 grids agree on the contrast
difference to 0.00011 for the main cut. Emitter groups are diagnostics
within the eikonal representation, while the full contrast and mean
include all groups. The calculation covers one event family and one
helicity assignment. It is a partonic test with a soft limit taken
before the angular scaling.
