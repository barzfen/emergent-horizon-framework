# Rotating the opening plane relative to the recoil plane

This extends the [six-gluon Dalitz-patch and beam-orientation average](shape-average.md). Hold the outgoing recoil plane fixed and rotate the equal-energy daughter pair around the parent axis. Test relative plane angles of 0, 45, 90 and 135 degrees. The opening plane is unoriented, so the angle is modulo 180 degrees.

The hard energy patch is x = 2 E_P/Q in [0.46,0.54], y = 2 E_4/Q in [0.625,17/24]. The beam patch remains defined relative to the recoil plane, with polar angle 65–115 degrees from the parent and azimuth 45–90 degrees from the recoil plane. It is held fixed as the daughters rotate. The soft direction is integrated in the 20–40 degree annulus around the parent. The angular weight cos(2 phi) uses azimuth measured from the rotated opening plane.

At each opening rho = m_pair/Q, sum all hard helicities and colours and weight by the hard tree matrix element squared. Extract the coefficient of rho² in the ratio of the angular moment to the soft radiation intensity, both integrated over the same patch. Positive coefficients mean that opening the pair gives its own plane more relative weight in the radiation pattern. The four-angle average sums the weighted intensities and moments at each rho before taking their ratio. It is a discrete average over four orientations.

The method uses the leading-soft current and the same Berends–Giele hard-amplitude calculation as the [six-gluon helicity study](six-soft.md). The code checks momentum conservation, null momenta and convergence between two small-opening extrapolations. The results are for this restricted phase-space patch and four orientations. They do not give an inclusive jet prediction.

Run `OPENBLAS_NUM_THREADS=2 python3 plane_scan.py` with NumPy. The script prints intermediate grid results followed by the JSON summary.

The coefficients are +50.75, +45.79, +50.27 and +54.72 in angle order. The four-angle weighted average is +50.50. Refining the aligned and perpendicular grids gives +50.88 and +50.27. See the [saved scan](plane-scan-results.json).
