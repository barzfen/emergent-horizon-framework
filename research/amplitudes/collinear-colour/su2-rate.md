# Isolating the finite SU(2) ratio with squared amplitudes

Use the pure SU(2) tree MHV amplitude on the same equal-split path
with real angle spinors and complexified momentum-conserving kinematics.
The two daughters have the same helicity. Sum spectator colours
in a complete adjoint basis, keeping spectator momenta and helicities
fixed. The daughter directions are ordered.

Let R++ and R00 denote the squared amplitudes with the pair fixed
to W+ W+ and W3 W3, respectively. Both project onto exchange-symmetric
pair states. The leading collinear pole is antisymmetric, so neither
rate receives the squared pole or its interference. The symmetric
amplitude is even in the signed opening and starts with the finite
coefficient.

By SU(2) invariance, let S0 and S2 be the total weights of the singlet
and spin-2 channels of the symmetric amplitude. Then R++ = S2/5
and R00 = S0/3 + 2 S2/15. Consequently S0+S2 = 3(R++ + R00).
These identities hold at each sampled finite opening. The finite
term gives R++/R00 = 1/2, or R++/[3(R++ + R00)] = 1/9 in the
limit. The analogous ratio to the full squared amplitude tends
to zero because that denominator contains the antisymmetric pole.

The script evaluates the unexpanded amplitude at four rational
openings, at five, six, and seven gluons. It verifies the projection
identity exactly using rational arithmetic and checks convergence
towards the finite result. JSON values are displayed as decimals.

In the massless basis rotation with a decoupled hypercharge direction,
R00 equals the sum over the ordered ZZ, Z gamma, gamma Z, and gamma
gamma pair weights at matched kinematics. In this calculation each
neutral external label merely multiplies the W3 amplitude by its
overlap, and the squared overlaps sum to one. This is a partonic
coefficient diagnostic. It does not include finite electroweak masses,
physical production and decay, or an observable event selection.

Run `python3 su2_rate.py > su2-rate-results.json` with standard-library Python.

See the [saved results](su2-rate-results.json).

The [real-momentum check](su2-real-rate.md) compares the planar benchmark with beam tilt and helicity sums.
