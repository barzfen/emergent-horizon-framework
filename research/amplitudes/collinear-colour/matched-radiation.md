# Matched hard-colour and soft-radiation test

This uses the same six-hard-gluon MHV event family and helicity as the
[hard pair-correlation test](pair-dipole.md).
The beam tilts by 0°, 10°, or 20° while the outgoing momenta at each
opening stay fixed. Both hard tensors use the same leading-soft current
at the exact finite-opening momenta. The soft angular region is the
20°–40° annulus around the parent direction. The observable is
C = mean(R cos(2 phi))/mean(R), where phi is measured from the opening plane.

Write tA = E + O with E even and O odd in the signed opening t, and
L = E(0). The full-minus-frozen difference separates into the squared
finite term (O,O), interference (2E,O), and the even remainder
(E+L,E-L). For each bilinear, subtract its hard norm bilinear times
the frozen normalized colour correlator and divide by the full hard
norm. These subtractions account for hard normalization and preserve
colour conservation separately for each row. To obtain the normalized
contrast difference, contract each row with the second angular-moment
kernel minus the frozen contrast times the zeroth-moment kernel, then
divide by the full zeroth moment. This gives an exact additive
decomposition at each sampled opening. Grouping individual emitters
within each row provides diagnostics in this eikonal representation.

The direct daughter-pair kernel carries a factor p1·p2 proportional
to t². The change of the hard daughter-pair correlator is itself
order t². With the angular region kept away from the hard directions,
the direct product is therefore order t⁴. A change in the t² contrast
can enter through correlations involving spectators. The individual
channel shares of the hard finite amplitude do not determine those
correlations or the interference. The test keeps the full colour
tensors and does not independently vary their channel shares.

Run `OPENBLAS_NUM_THREADS=2 python3 matched_radiation.py > matched-radiation-results.json`
with Python and NumPy. Results are coefficients in the opening t of
`six_soft.event`, with t approximately twice the pair mass divided by
the hard energy. The angular integration uses midpoint grids in cosine
of the polar angle and in azimuth, with n and 4n subdivisions respectively.
The script compares successive opening extrapolations and checks exact
reconstruction of the contrast difference at finite opening. The test
uses one hard geometry and helicity assignment at tree level and leading
soft order.

## Results

The [saved output](matched-radiation-results.json) includes all three angular grids and the full interference breakdown.

Coefficients of t² in the normalized contrast, using the finest grid.

| Beam tilt | Full | Frozen | Full minus frozen | Pole–finite interference |
| ---: | ---: | ---: | ---: | ---: |
| 0° | 12.95019 | 10.12390 | +2.82629 | +2.90950 |
| 10° | 12.88648 | 10.32344 | +2.56304 | +2.65368 |
| 20° | 12.72584 | 10.85672 | +1.86912 | +1.96047 |

The full-minus-frozen effect is positive in this setup and shrinks by
34% from 0° to 20°, while the hard pair-correlation coefficient grows
from 10.71903 to 13.46292. The contrast residual is predominantly
interference between the leading pole and the finite amplitude in
daughter–spectator correlations. The squared finite term contributes
−0.161, −0.140 and −0.090 at the three angles. The direct pair contribution
extrapolates to zero at this order. The residuals change by less than
0.00002 when the angular grid is refined from n=64 to n=128.
