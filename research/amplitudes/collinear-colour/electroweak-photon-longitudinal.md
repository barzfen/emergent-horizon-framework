# Longitudinal W and Z states on the photon-beam patch

The [photon-beam patch](electroweak-photon-patch.md) gave a same-sign
diagnostic of 0.2063 with transverse final states. Test whether it
survives a sum over all physical final polarizations of on-shell
W and Z bosons.

## Matched calculation

Keep the same two incoming photons, external momenta for each
species assignment, channel ordering, model parameters and
normalized flat integration measure. At each massive final leg
use two transverse states and the longitudinal vector
`(|p|/m, E p/(m |p|))`, where `p` in this expression is the
three-momentum. Each photon has two transverse states. The recursion
includes the bosonic tree diagrams with Higgs exchange.

For the selected W+ W+ pair the recoil is W− W−. For a neutral
selected pair the two ordered charged recoils are W+ W− and W− W+.
An all-neutral final state with incoming photons vanishes at
tree level. There is no tree of charged lines without charged
external endpoints.

Bin the squared amplitudes by the number of longitudinal legs in
the selected pair and in the recoil. Integrate each channel and
bin before forming `R++ / [3(R++ + R00)]`, with `R00` the sum
of the ordered ZZ, Zγ, γZ and γγ weights. Use one member of
each global helicity-reversal pair, so the unnormalized weights
in the output are half the full helicity sums. In the recursion,
complex conjugation reverses the sign of the gauge cubic vertex.
Reflecting the Cartesian W2 direction reverses the same sign and
maps conjugate charge vectors back to the original ones. The two
operations give equal squared amplitudes for reversed helicities
at the same momentum. The script checks the reversal at a
nonplanar point inside the patch.

## Results

| Nodes per coordinate | Transverse only | Pair inclusive, recoil transverse | Pair transverse, recoil inclusive | Fully inclusive |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 0.209082 | 0.203539 | 0.208115 | 0.197908 |
| 3 | 0.206159 | 0.200968 | 0.205256 | 0.195614 |
| 4 | 0.206317 | 0.201207 | 0.205405 | 0.195803 |

The fully inclusive result is 0.1958 on the finest grid, a
decrease of 0.0105 from the transverse result. The diagnostic
changes by 0.00019 from order three to order four. The inclusive
value remains well above the matched massless aligned colour
average of 0.1143.

On the finest grid, longitudinal states increase the same-sign
weight by 2.17% and the combined neutral weight by 16.57%.
The ZZ channel alone grows by 27.02% and accounts for 94.58%
of the added neutral weight. Configurations with a longitudinal
boson in both the selected pair and the recoil account for
51.33% of all the added weight. Keeping either side transverse
omits those configurations. The diagnostic therefore drops
further when both sides are included.

The aligned colour average and interference removal are controls
from the matched massless transverse calculation. They provide
a scale for the comparison. The decomposition into interference
terms has only been tested in that massless calculation.

The weights refer to a flat kinematic patch for stable external
bosons. A fiducial cross section would also require phase-space
weights, boson decays and cuts.

## Reproduction and checks

Run `OPENBLAS_NUM_THREADS=1 python3 electroweak_photon_longitudinal.py 2 3 4`
with NumPy. The [saved output](electroweak-photon-longitudinal-results.json)
records the integrated channel weights by polarization bin.
The script checks momentum conservation, the mass shells and
polarization orthonormality, then tests the photon Ward identities
and invariance of the inclusive sum under a rotation of the
massive polarization bases at a representative nonplanar point.
It reproduces the earlier transverse weights at that point. The
saved transverse weights also agree channel by channel with the
previous calculation on all three grids.

The [leptonic decay follow-up](electroweak-photon-decays.md)
keeps the production patch and applies charged-lepton and photon
acceptance cuts with spin correlations.
