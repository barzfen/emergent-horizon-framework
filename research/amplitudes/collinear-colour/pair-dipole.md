# First finite hard-pair colour correlation at six gluons

This checks a consequence of the [planar 1:2:3 law](planar-theorem.md) directly in the hard amplitude. Use a tree-level six-gluon MHV amplitude with negative helicities on the two incoming legs in the all-outgoing convention. The outgoing pair has equal energies and equal helicities. The recoil follows the exactly conserved path in `six_soft.event`. The beam tilts out of the outgoing plane while all outgoing momenta at each opening stay fixed.

Write the hard amplitude as A = L/t + B + O(t) and the pair dipole as D = T1·T2. The leading tensor L has eigenvalue −3/2, and B is symmetric under pair exchange. In the normalized expectation of D + 3/2, all interference terms with L vanish because (D + 3/2)L = 0. The coefficient of t² is therefore

    (||B||²/||L||²) (−1.5 p_singlet + 2.5 p_27).

Here p denotes the squared-norm shares of B. The symmetric octet carries zero weight in this shifted moment. The planar shares (1/6, 1/3, 1/2) make the factor in parentheses exactly one. This separates changes in the relative channel shares from changes in the total finite norm.

The script extracts L and B by reversing the signed opening and verifies exchange symmetry in the ordering basis. It computes the full-amplitude coefficient separately by applying the shifted dipole to the unseparated amplitude at four openings and extrapolating. The finite-tensor singlet share comes from a direct trace projection. The remaining shares are reconstructed from the norm and the dipole expectation using the distinct symmetric-sector eigenvalues. Thus the coefficient check is a test of the opening expansion, with shared colour algebra between the two routes.

Run `OPENBLAS_NUM_THREADS=2 python3 pair_dipole.py > results.json` with Python and NumPy. The package uses the opening t defined by `six_soft.event`, which at leading order is twice m_pair/Q. This is a hard partonic colour correlation for one recoil geometry and one helicity assignment. It does not evaluate the colour-summed soft angular contrast or define a colour-tagged measurement.

## Results

The [saved output](pair-dipole-results.json) includes the signed tilt check and the opening extrapolation. This hard-amplitude test follows the [leading parent-pole radiation control](pole-control.md).

| Beam tilt | Singlet share | Symmetric octet share | 27 share | Full shift coefficient | At planar shares, same norm |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0° | 0.16667 | 0.33333 | 0.50000 | 10.71903 | 10.71903 |
| 2° | 0.16628 | 0.33300 | 0.50071 | 10.74797 | 10.72264 |
| 5° | 0.16428 | 0.33127 | 0.50444 | 10.89940 | 10.74167 |
| 10° | 0.15735 | 0.32520 | 0.51745 | 11.43317 | 10.81036 |
| 20° | 0.13254 | 0.30256 | 0.56490 | 13.46292 | 11.09487 |
| 35° | 0.08386 | 0.25239 | 0.66374 | 18.28215 | 11.92139 |
| 60° | 0.02846 | 0.17419 | 0.79735 | 27.51842 | 14.10712 |

The two departures from the planar shares reinforce one another in this scan.
The singlet has negative weight and loses share. The 27 has positive weight
and gains share. At 20°, redistribution alone raises the coefficient by
21.34% relative to planar shares at the same finite-to-pole norm ratio.

The exact quadratic channel curvatures for this geometry in the
[near-planar results](tilt-results.json)
give a dipole curvature of 7115165/3666264 = 1.940713 per radian squared,
after converting the old tilt parameter u via theta = 2 arctan(u).
The finite 2° estimate is 1.938708. The negative 2° run agrees with
positive 2° within numerical precision.
