# Leptonic decay acceptance on the photon-beam patch

The [stable-boson polarization sum](electroweak-photon-longitudinal.md)
gave a same-sign diagnostic of 0.1958. Test how it changes under
simple cuts on the particles produced in W and Z decays.

## Matched calculation

Use the same production patch, tree amplitudes, ordered channels,
and flat production measure. Decay every W to a charged lepton
and neutrino, and every Z to a charged-lepton pair. Use massless
decay leptons and the spin-correlated on-shell narrow-width
approximation. Treat each boson's decay as a tagged channel.
Prompt photons remain in the event.

For each W or Z, integrate a normalized three-by-three decay
matrix. An uncut decay gives the identity. Each accepted event
requires every charged lepton and prompt photon to satisfy
`|eta| < 2.5` and `pT > {0.25, 0.50, 1.00} mW`, with both
quantities defined relative to the incoming photon axis in the
centre-of-mass frame. Neutrinos have no cuts. Since these cuts
factor by parent, the product of the integrated matrices can
be contracted with the full production spin tensor. The W
matrix uses the charged lepton as the decay axis, with opposite
spin projections for W+ and W−. The Z matrix uses the negative
lepton and the squared left- and right-handed lepton couplings.

At fixed rest-frame polar angle the boosted lepton energy is
fixed and its beam-parallel momentum is affine in a shifted
azimuthal cosine. The cuts therefore select an interval of that
cosine. Integrate azimuth analytically using Fourier moments
through order two, then integrate the rest-frame polar cosine
by Gauss–Legendre quadrature. Both beam-photon helicities are
summed explicitly. The production spin sum uses the full decay
matrices, including off-diagonal helicity terms. As controls,
repeat it with diagonal matrices, with isotropic decays, and
with the production tensor restricted to transverse states.

The normalized matrices condition on the chosen decay modes.
The diagnostic remains `R++ / [3(R++ + R00)]` and the
weights exclude branching fractions. The cut results describe
a truth-tagged acceptance test. A fiducial yield would additionally
need branching fractions, physical phase-space and luminosity
weights, and a reconstruction prescription for close leptons
and photons. These cuts do not use isolation, event-wide missing
momentum, or reconstructed parent masses.

For examples of the spin-correlated pole approximation in
leptonic vector-boson production, see
[Denner and Pelliccioli](https://arxiv.org/abs/2006.14867).

## Results

| Minimum object pT / mW | Full polarization sum | Transverse production | Same-sign acceptance | ZZ acceptance |
| ---: | ---: | ---: | ---: | ---: |
| No cuts | 0.195803 | 0.206317 | 100% | 100% |
| 0.25 | 0.195783 | 0.206432 | 76.1% | 73.7% |
| 0.50 | 0.198252 | 0.209519 | 65.5% | 59.8% |
| 1.00 | 0.203482 | 0.215645 | 48.4% | 38.8% |

The loose selection leaves the full diagnostic near 0.196.
The hardest cut raises it to 0.2035. The same-sign channel
requires four charged leptons and the ZZ channel requires six.
At the hardest cut, the same-sign channel keeps 48.4% of its
uncut weight and ZZ keeps 38.8%. All channels lose weight, with
different efficiencies.

The transverse-only result remains above the full polarization
sum at all tested thresholds. Replacing the decay matrices
with their diagonal parts changes the full diagnostic by at
most 0.00017 on the finest grid. Replacing them with isotropic
decays changes it by at most 0.00085. Most of the change under
the hardest cut is therefore captured by channel-dependent
acceptance even in the isotropic control.

Moving from production order three to four changes the full
cut results by up to 0.00076. Moving from decay polar order
512 to 1024 at fixed production order four changes them by
up to 0.00004. The shift at the hardest cut exceeds both grid
changes. The loose-cut difference from the uncut result varies
on the production grid scale.

## Reproduction and checks

Run `OPENBLAS_NUM_THREADS=1 python3 electroweak_photon_decays.py 3 4 --decay-orders 128 512 1024`
with NumPy. The [saved output](electroweak-photon-decays-results.json)
includes the accepted channel weights and efficiencies for the
two production grids and three decay orders. The script checks
the normalization of the decay kernels, the azimuth moments in
limiting cases, and the spin contraction against a direct
amplitude product. The uncut output divided by two agrees
channel by channel with the earlier half-helicity production
sums on both production grids.

The [visible-particle tagging test](electroweak-photon-reconstruction.md)
adds a separation requirement and classifies events without parent
labels, separating channel losses from wrong assignments.
