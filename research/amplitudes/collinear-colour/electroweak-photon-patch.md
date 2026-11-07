# Does the photon enhancement survive averaging over a scattering region?

Use the [fixed photon initial state](electroweak-photon-initial.md)
and sum the transverse helicities. Hold the hard energy at 12,
the pair energy at 3, and the pair invariant mass at 0.48 in
code units. For the electroweak calculation use mW/M=0.30,
mH/mW=1.55 and sin²(theta)=0.23. Use the matched massless geometry
for the isospin decomposition from the [incoming colour rotation](su2-incoming-rotation.md).

Vary the beam polar angle to the pair direction from 60 to
75 degrees, its azimuth from the recoil plane from 0 to 25 degrees,
the daughter opening-plane rotation from −20 to 20 degrees, and
one recoil energy from 3.92 to 4.08. The other recoil energy
is fixed by conservation. Each point and species assignment
has on-shell momenta. Use a normalized flat measure in the
cosine of the polar angle, the two azimuthal angles, and the
varied recoil energy. This is a restricted kinematic slice,
without production, decay, or beam-luminosity weighting.

Integrate the same-sign and all four ordered neutral weights
separately before forming the fraction. For the massless controls,
integrate the isospin interference separately and also compute
the theoretical aligned colour average. The massive calculation
uses one member of each global helicity-reversal pair. The common
factor of two cancels in the ratio. The script checks reversal,
batching, an independent massless contraction and photon Ward
identities at a sample point in the patch.

| Nodes per coordinate | Massless photons | Massless without interference | Aligned colour average | Massive photons |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 0.207543 | 0.095070 | 0.114835 | 0.209082 |
| 3 | 0.204949 | 0.094420 | 0.114251 | 0.206159 |
| 4 | 0.204974 | 0.094430 | 0.114287 | 0.206317 |
| 5 | 0.205021 | 0.094438 | 0.114292 | — |

At all 625 nodes of the finest massless grid the interference
raises the same-sign weight and lowers the neutral weight.
This establishes the sign on the sampled grid, rather than
at every point of the continuous patch. The difference between
the massive and massless fractions is about 0.0013 on the
four-nodes-per-coordinate grid. Grid refinement changes this small shift by
about 0.00013 from three to four nodes per coordinate.
The massless interference effect is much larger than this
shift. The interference decomposition applies to massless SU(2).

Run `python3 electroweak_photon_patch.py 4` with NumPy.
Use orders 2 and 3 for the coarser checks, and
`python3 electroweak_photon_patch.py 5 --massless` for the
finest massless check. The script emits the node data.
See the [saved integrated results](electroweak-photon-patch-results.json).
