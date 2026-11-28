# Six-gluon helicity sum of the soft angular contrast

This extends the [leading-soft collinear calculation](soft-emission.md) to six hard gluons. It includes the 20 assignments with three negative helicities (NMHV), in addition to the 30 MHV and parity-conjugate assignments. The calculation sums all hard colours and the extra soft gluon's colours and polarizations. It uses tree-level hard amplitudes and the leading eikonal current for the soft emission.

The hard parent and the two other outgoing momenta at zero opening have spatial vectors (3,0,0), (0,0,4), and (−3,0,−4). Two incoming beams have energy 6. The parent opens along the z direction while incoming momenta recoil to preserve conservation. The two zero-opening beam directions tested are (5/13,0,12/13) and (0,1,0), the latter perpendicular to the outgoing plane. The soft direction is integrated over the 20–40 degree annulus around the parent, using solid angle. The azimuth phi is measured from the opening plane.

Let R be the leading-soft radiation weight divided by the hard amplitude norm, with the sums in numerator and denominator over the same helicity sector. The normalized angular contrast is mean(R cos(2 phi)) / mean(R). The reported coefficient of t² in this ratio measures the opening-induced shape change after accounting for total intensity. The full sum is obtained by summing squared amplitudes before normalization, with no equal-sector weighting.

The full contrast coefficient is positive in both test geometries. Including NMHV lowers it in the planar example and raises it in the perpendicular example. The results are numerical for two partonic configurations. They do not integrate a cross section over hard phase space or include subleading terms in the soft energy.

## Reproduction

Run `OPENBLAS_NUM_THREADS=2 python3 six_soft.py > six-soft-results.json` with NumPy. The calculation uses colour-ordered [Berends–Giele recursion](https://arxiv.org/abs/1206.2381) and a structure-constant colour basis. It checks null momenta, momentum conservation, a polarization Ward identity, vanishing tree helicity assignments, and the MHV and anti-MHV ordering dependence against the Parke–Taylor formula. It checks the quadratic extraction with two extrapolation windows and the angular integration with two grids. The saved output also gives the unnormalized angular averages.
