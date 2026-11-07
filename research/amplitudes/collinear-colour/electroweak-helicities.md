# Matched electroweak rate after summing transverse helicities

Use the [matched electroweak geometry](electroweak-rate.md) at pair
mass divided by hard energy 0.04, W mass divided by pair mass 0.30,
and beam tilts of 0 and 20 degrees. Compare the massless limit, the
equal-mass custodial model, and the broken theory with sin²(theta)
equal to 0.23. All points use the same hard energy, pair invariant
mass, energy fractions and matched transverse helicity choices.
Reconstruct the on-shell momenta for each species and mass as in
the fixed-helicity scan.

Sum the channel weights before forming the ratio. The global helicity
reverse has the same squared weights. In the real gauge basis the
six-vector diagrams have an even number of imaginary three-vector
vertices. Conjugation reverses helicities and swaps the charged
external state. Charge conjugation then gives back the same rate
under the full spectator sum. The script also checks this equality
directly for the original fixed-helicity choice at both tilts.
Longitudinal states are excluded.

| Tilt | Transverse helicities included | Massless | Custodial | Electroweak |
| ---: | --- | ---: | ---: | ---: |
| 0° | Equal daughters | 0.111215 | 0.111380 | 0.111363 |
| 0° | Opposite daughters | 0.146135 | 0.125254 | 0.122416 |
| 0° | All transverse | 0.112603 | 0.112002 | 0.111870 |
| 20° | Equal daughters | 0.130071 | 0.129839 | 0.129832 |
| 20° | Opposite daughters | 0.101545 | 0.104531 | 0.104492 |
| 20° | All transverse | 0.119665 | 0.120769 | 0.120748 |

The equal-daughter sum retains the sign pattern of the fixed MHV
calculation. The all-transverse sum reverses it at both tilts.
Most of the all-transverse shift is already present in the custodial
model at these two points. The opposite-daughter subset can show
a much larger mass dependence. These are two fixed kinematic points
at tree level, with complete spectator-species sums and no
phase-space or flux weights.

Run `python3 electroweak_helicities.py 0` or
`python3 electroweak_helicities.py 20` with NumPy.
See the [planar](ew-helicity-planar.json) and [tilted](ew-helicity-tilted.json)
results for the per-helicity weights and additional groupings.
