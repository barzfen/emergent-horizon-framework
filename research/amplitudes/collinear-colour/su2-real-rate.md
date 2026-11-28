# The pole-free SU(2) rate combination with real momenta

This pure tree-level Yang–Mills test uses the real six-boson event
family in six_soft.event. The two incoming momenta are crossed.
The equal-energy daughter opening is varied, and the beam is tilted
out of the outgoing plane by 0, 10 and 20 degrees. The full amplitudes
are built with the existing Berends–Giele recursion and SU(2) colour
chains. The recursion checks a Ward identity and the MHV ordering
dependence is checked against Parke–Taylor.

The same-sign and W3 W3 diagonals are evaluated at finite opening.
The script verifies that three times their sum equals the total
exchange-symmetric pair weight for each tested helicity selection.
It reports the same-sign share of that symmetric weight and the
same-sign to neutral ratio. Both quantities sum over spectator colours.

| Tilt | Fixed MHV share | Equal daughter helicities, other helicities summed | All helicities summed |
| ---: | ---: | ---: | ---: |
| 0° | 0.11111115 | 0.11095511 | 0.11246454 |
| 10° | 0.11622352 | 0.11598714 | 0.11495141 |
| 20° | 0.12991981 | 0.12956011 | 0.11946567 |

The table uses t=0.001, the smallest of the four openings.
The planar fixed-helicity result approaches 1/9. The tilt and
helicity comparisons quantify deviations that are already present
with massless bosons. In this test the helicity sums keep the same
kinematics and equal weighting of included initial helicities.
The calculation is restricted to one real hard event family and
contains no broken-electroweak mass corrections.

Run `python3 su2_real_rate.py > su2-real-rate-results.json` with NumPy.

The [matched massive control](su2-mass-control.md) turns on a common vector mass and Higgs interactions.
