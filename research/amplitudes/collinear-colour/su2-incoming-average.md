# Average the incoming colour direction while retaining alignment

Follow the [fixed photon initial-state test](electroweak-photon-initial.md)
using the same massless SU(2) momenta, helicities and two outgoing
pair projections. Hold the outgoing charged and neutral projectors
fixed. Vary only the incoming colour ensemble. A fixed W3 W3 state
gives the massless photon fraction, since the incoming projection
factors cancel in the ratio.

For a real unit adjoint vector n, the aligned incoming state is
n tensor n. Averaging over a common uniformly distributed n gives
the density P0/3 + 2 P2/15, where Pj projects the incoming pair
onto total isospin j. The spin-1 sector is absent. This follows
from the fourth sphere moment
(delta_ij delta_kl + delta_ik delta_jl + delta_il delta_jk)/15.
Averaging two directions independently gives I/9, the normalized
complete incoming-species sum. Average squared amplitudes before
forming the ratio in each case.

| Tilt | Q/M | Fixed W3 W3 | Aligned average | Independent average |
| ---: | ---: | ---: | ---: | ---: |
| 0° | 25 | 0.225996 | 0.118125 | 0.112603 |
| 0° | 200 | 0.226241 | 0.118212 | 0.112467 |
| 20° | 25 | 0.172577 | 0.110118 | 0.119665 |
| 20° | 200 | 0.172868 | 0.110070 | 0.119469 |

The table sums all transverse helicities. The common-direction
average removes most of the fixed-direction enhancement even
though the incoming colours remain aligned. The independently
averaged and aligned ensembles still have distinct weights in
the three incoming isospin sectors. Those weights produce a
smaller difference in the fraction. These are massless SU(2)
diagnostics, with a theoretical average over incoming adjoint
states and fixed outgoing projectors.

The script cross-checks the aligned average against a weighted
sum over Cartesian axes and cube corners and the independent
average against the direct trace. Run
`python3 su2_incoming_average.py > su2-incoming-average-results.json`
with NumPy. The [saved output](su2-incoming-average-results.json)
also includes fixed MHV helicities and the equal-daughter sum.

The [incoming rotation test](su2-incoming-rotation.md) resolves the angular sweep and its isospin interference.
