# Rotate the aligned incoming colour and resolve its interference

This follows the [incoming-colour average](su2-incoming-average.md).
Hold the real massless six-vector momenta and outgoing projectors
fixed. The two incoming adjoint vectors share a real unit direction
n. Let alpha be its internal angle to W3 and x = cos²(alpha).

The contracted amplitude is quadratic in n. Summing recoil colours
makes each selected squared weight invariant under rotations around
the W3 axis, since the outgoing pair projector is invariant as a
projector under those rotations. A homogeneous quartic with that
axial invariance is a quadratic in x on the unit sphere. Thus each
weight has the form A+B x+C x², while the ratio is a quotient of
two such polynomials. Determine the coefficients at x=0, 1/2, 1.
The script checks six held-out x values at two azimuths each,
for all four kinematic points and both helicity selections.
The maximum absolute residual divided by the largest fit weight
is below 7e-16 in this run.

Decompose the aligned amplitude into the incoming isospin-0 trace
and the isospin-2 traceless part. Their squared contributions and
their interference add to the full weight in each outgoing channel.
The cross term averages to zero over the sphere since the average
of n_i n_j is delta_ij/3. The integrated full weights also match
the previous aligned average.

| Tilt | Q/M | Fixed W3 W3 | Fixed W3 W3 with cross term omitted | Aligned average |
| ---: | ---: | ---: | ---: | ---: |
| 0° | 25 | 0.225996 | 0.099659 | 0.118125 |
| 0° | 200 | 0.226241 | 0.099652 | 0.118212 |
| 20° | 25 | 0.172577 | 0.089038 | 0.110118 |
| 20° | 200 | 0.172868 | 0.089084 | 0.110070 |

The table uses all transverse helicities. At fixed W3 W3 the
interference is constructive in the same-sign weight and
destructive in the neutral weight at all four points. The
interference-omitted column is an algebraic control at that
same direction. It does not change the kinematics or represent
a collider event selection.

Run `python3 su2_incoming_rotation.py > su2-incoming-rotation-results.json`
with NumPy. The [saved output](su2-incoming-rotation-results.json)
includes the angular coefficients and each interference term.
