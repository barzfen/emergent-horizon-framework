# Matched massive and massless SU(2) rates

This control uses the custodial SU(2) Higgs model with zero hypercharge
coupling. All three vectors have the same mass and there is one Higgs
with mass 1.55 times the vector mass. The coupling is normalized to
g = 1. The recursion uses the unitary-gauge vector propagator and all
vector and Higgs tree vertices from the gauge and Higgs Lagrangian.
See [Dai, Melnikov and Caola](https://arxiv.org/abs/1201.1523) for
the underlying broken SU(2) amplitude construction.

In each comparison the massive and massless runs have the same hard
energy Q, pair invariant mass, cluster energy fractions, beam tilt
and transverse helicities. The pair has equal daughter energies.
The momenta are reconstructed on shell for each mass, with the same
pair and recoil planes. Opening angles and recoil angles follow from
those constraints and can change with mass. The incoming beams are
back-to-back in the centre-of-mass frame. The same complete spectator
species sum is used in both runs.

The six-vector massless tensor agrees with the existing massless
recursion up to common normalization at all six reference points.
A four-vector all-neutral transverse test agrees with the analytic
Higgs exchange in the three channels. The six-vector rate calculation
checks the custodial projection identity for both masses.

| Tilt | Pair mass / Q | Massless fraction | Massive fraction at m / pair mass = 0.30 | Shift |
| ---: | ---: | ---: | ---: | ---: |
| 0° | 0.02 | 0.111169 | 0.111209 | +0.000040 |
| 0° | 0.08 | 0.112024 | 0.112772 | +0.000748 |
| 20° | 0.02 | 0.130042 | 0.129978 | −0.000064 |
| 20° | 0.08 | 0.132020 | 0.130865 | −0.001155 |

The sign differs between the two geometries throughout this scan.
The model retains custodial symmetry. Physical Z–photon mixing and
unequal vector masses are outside this control.

Run `python3 su2_mass_control.py > su2-mass-results.json` with NumPy.
The [saved scan](su2-mass-results.json) contains all 18 comparisons.
