# Helicity sum and hard-angle test of the soft angular contrast

This extends the [colour-summed soft calculation](soft-emission.md). We retain the tree-level leading-soft approximation with a five-gluon hard amplitude. The five sample angles are between the parent and one beam at zero opening. The beam-exchange symmetry makes 65 and 115 degrees equivalent, and likewise 75 and 105 degrees. The two incoming momenta are boosted to account for recoil while the outgoing recoil leg is held fixed. At 90 degrees the path agrees with the earlier calculation.

At fixed real hard kinematics, every nonvanishing five-gluon tree helicity amplitude is MHV or its parity conjugate. Its helicity numerator is independent of the ordering. The colour vector is therefore the same up to a scalar and possibly complex conjugation. The summed-polarization leading-soft colour quadratic form is real, so the normalized radiation weight is identical across the nonvanishing hard helicities. Summing hard helicities in numerator and denominator preserves it. The script evaluates the sum explicitly. The argument does not apply to general multiplicity or to subleading soft-energy terms.

## Angular pattern

Average over the 20–40 degree annulus around the parent using solid angle. Define R as the normalized radiation weight and phi as the azimuth measured from the pair opening plane. The normalized angular moment is mean(R cos(2 phi)) / mean(R). The coefficient of t² in this ratio measures an angular shape change after accounting for the change in total intensity. It is positive at every sample angle. The table in angular-ensemble-results.json also records the coefficients of t² in the unnormalized mean and angular moment. Equal event weights are used for the reported ensemble average.

The calculation keeps all hard emitters and uses unexpanded hard amplitudes at small nonzero t. Numerical differences at several openings isolate the quadratic coefficient, and a separate angular grid checks convergence. The calculation recovers the previously derived single-direction coefficient 14/3 and the previous 90-degree hard-event angular average. The sample is a controlled partonic ensemble and does not integrate the cross section or simulate hadronization.

Run `OPENBLAS_NUM_THREADS=1 python3 angular_ensemble.py > angular-ensemble-results.json` with NumPy installed.

For the helicity amplitudes see [Dixon, Calculating Scattering Amplitudes Efficiently](https://arxiv.org/abs/hep-ph/9601359).
