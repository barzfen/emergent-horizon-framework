# Matched electroweak rate scan with hypercharge

Extend the [custodial control](su2-mass-control.md) to the bosonic
electroweak tree amplitude. Fix the SU(2) coupling to one, the Higgs
mass to 1.55 times the W mass, and use the tree mass relation
mZ = mW / cos(theta). Scan sin²(theta) at 0, 0.115 and 0.23, with
mW / pair mass = 0.30. The final value is an illustrative weak mixing
parameter. The calculation keeps only the stated transverse MHV
helicity assignment in the massless limit and its transverse
continuation in the massive theory. See [Denner's electroweak
Feynman rules](https://arxiv.org/abs/0709.1075).

The numerator is the same-sign squared amplitude. The denominator
is three times the sum of that weight and the four ordered neutral
weights ZZ, Z gamma, gamma Z and gamma gamma. Sum all four vector
species independently at each spectator leg, at the stated
helicities. The charged spectator states can be summed in their
degenerate Cartesian basis. Weights are squared amplitudes at
specified phase-space points, with no flux or phase-space factors.

Each massive assignment is matched to the same hard energy, pair
invariant mass, cluster energy fractions, beam tilt, recoil plane
and transverse helicities in the massless calculation. Spatial
momenta adjust to satisfy each mass shell. At zero mixing the
scan agrees with the corrected custodial calculation. The massless
fraction is invariant under the neutral rotation. For the massive
channels with a photon in the pair, replacing its polarization
by its momentum gives zero within numerical tolerance.

| Tilt | Pair mass / Q | Matched massless | Custodial massive | Massive at sin²(theta) = 0.23 |
| ---: | ---: | ---: | ---: | ---: |
| 0° | 0.02 | 0.111169 | 0.111209 | 0.111206 |
| 0° | 0.08 | 0.112024 | 0.112761 | 0.112710 |
| 20° | 0.02 | 0.130042 | 0.129988 | 0.129988 |
| 20° | 0.08 | 0.132020 | 0.131022 | 0.130926 |

The added shift from hypercharge is smaller than the custodial
mass shift at all six points for sin²(theta) = 0.23. The neutral
channels are retained separately. For example, the two mixed
neutral orderings have different weights at finite mass and
fixed helicities. This is a fixed-kinematics tree benchmark.
It does not establish the same behavior for broader helicity
selections or collider event rates.

Run `python3 electroweak_rate.py > electroweak-rate-results.json` with NumPy.
See the [full scan](electroweak-rate-results.json).
