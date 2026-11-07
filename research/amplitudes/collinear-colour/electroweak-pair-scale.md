# Raise the pair mass relative to the weak scale

The [hard-energy scan](electroweak-scale.md) kept the pair and weak
masses fixed and found a persistent transverse shift over the
tested range. Here we increase the pair mass by factors of two
and four at fixed hard energy and fixed W mass. We also test the
same mass ratios at fixed Q/M=200. The latter path holds the
massless kinematics fixed in dimensionless units and isolates
the change in mW/M from a change in Q/M.

Both paths use the two original beam tilts, the complete
transverse helicity sum, and sin²(theta)=0.23. Each massive
point is compared with its own massless calculation at the same
Q/M and matched geometry. The fraction is formed after summing
squared amplitudes, with no flux or phase-space weighting.

| mW/M | Planar shift, fixed Q | Tilted shift, fixed Q | Planar shift, Q/M=200 | Tilted shift, Q/M=200 |
| ---: | ---: | ---: | ---: | ---: |
| 0.300 | −0.000969 | +0.001288 | −0.000969 | +0.001288 |
| 0.150 | −0.000148 | +0.000268 | −0.000151 | +0.000270 |
| 0.075 | −0.0000304 | +0.0000619 | −0.0000338 | +0.0000650 |

The shift shrinks on both paths. At fixed Q/M, halving mW/M
from 0.15 to 0.075 reduces the shift to 22% of its previous
magnitude in the planar case and 24% in the tilted case.
This is close to quadratic suppression over that interval.
The scan does not establish an asymptotic power law.

To reproduce the points with NumPy, use the following arguments
after `python3 electroweak_helicities.py`, for each tilt 0 and 20.
Pass the resulting JSON files for each path separately to
`python3 electroweak_scale.py`.

| Path | Pair mass in code units | mW/M |
| --- | ---: | ---: |
| Common baseline | 0.06 | 0.30 |
| Fixed Q and mW | 0.12 | 0.15 |
| Fixed Q and mW | 0.24 | 0.075 |
| Fixed Q/M | 0.06 | 0.15 |
| Fixed Q/M | 0.06 | 0.075 |

The [saved results](electroweak-pair-scale-results.json) include
the helicity-group breakdowns for both paths.
