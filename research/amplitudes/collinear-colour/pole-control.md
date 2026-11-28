# Leading parent-pole control for the soft angular contrast

This probe follows the [outgoing-shape](shape-average.md) and [opening-plane](plane-scan.md)
scans in the collinear-colour study.
It compares tree-level six-hard-gluon SU(3) amplitudes with a control that
retains only the leading collinear hard amplitude. All three calculations
use the same momenta and leading-soft radiation current at each opening.

Let rho = m_pair/Q. For the angular contrast C = <R cos(2 phi)>/<R>,
report the coefficient of rho squared, where phi is measured from the
daughter opening plane and the soft direction lies in the 20–40 degree annulus.

| Relative opening-plane angle | Full | Frozen pole, full weights | Frozen pole and weights |
| --- | ---: | ---: | ---: |
| 0 degrees | 50.8844 | 52.4701 | 52.3727 |
| 90 degrees | 50.2738 | 52.3865 | 52.3143 |

The first-to-second change isolates the effect of changing hard colour
correlations at fixed event weights. Restoring the full correlations
lowers the coefficient by 1.59 and 2.11, respectively. The second-to-third
comparison isolates the effect of reweighting events with the full hard
rate, which raises the frozen-pole result by 0.10 and 0.07 on the finer
grid. The net finite hard effect is a reduction of 1.49 and 2.04.
The large positive contrast survives when both hard inputs are frozen.
The unnormalized moments in [the saved results](pole-control-results.json) show that the degree of
agreement depends on the observable.

These are numerical results on a restricted hard patch with equal-energy
daughters. The two tested orientations and the coarse-to-fine comparison
do not establish a general angular or phase-space law. The residual
includes finite hard-amplitude effects collectively and does not isolate
the planar 1:2:3 colour law.

## Reproduction

Run `OPENBLAS_NUM_THREADS=2 python3 pole_control.py` with Python and NumPy.
The run uses 2-by-2 shape quadrature, coarse and fine beam quadratures
(2-by-2 and 3-by-3), and soft angular grids with 32 and 48 subdivisions
per axis. The opening scan uses rho = 0.008, 0.004, 0.002, 0.001.
The frozen input is the extrapolated even part of rho times the hard
amplitude under signed opening reversal. The code checks the leading
colour antisymmetry, colour conservation and extrapolation stability.
