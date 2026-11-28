# Raise the collision energy at fixed pair and weak-boson masses

Extend the [matched transverse helicity study](electroweak-helicities.md)
at beam tilts 0 and 20 degrees. Hold the pair mass and weak-boson
masses fixed in physical units while increasing Q by factors of
2, 4 and 8. Numerically we keep Q=12 in code units and rescale all
masses together, with mW/M=0.30, mH/mW=1.55 and sin²(theta)=0.23.
The tree-level ratios are dimensionless. Energy fractions and the
momentum construction are the same as in the matched benchmark.
Use the same complete transverse helicity and spectator sums.

Let p be a helicity group's share of the denominator and f its
own rate fraction. The total fraction is the sum of p f over the
equal- and opposite-helicity groups. For each group, the difference
between electroweak and matched massless results is exactly the
average p times the change in f plus the average f times the
change in p. The script checks this decomposition numerically.

| Q / pair mass | Planar total shift | 20-degree total shift |
| ---: | ---: | ---: |
| 25 | −0.000734 | +0.001083 |
| 50 | −0.000913 | +0.001241 |
| 100 | −0.000958 | +0.001279 |
| 200 | −0.000969 | +0.001288 |

At Q/M=200 the planar within-group and mixture terms are
−0.001190 and +0.000221. The tilted terms are +0.001105 and
+0.000183. In both geometries the opposite-helicity group supplies
the dominant within-group change. At the highest energy its own
fraction changes by −0.02932 in the planar case and +0.00310 at
20 degrees.

The shift does not fade over the sampled energies. The data are
consistent with a finite limiting shift at fixed mW/M, but the
scan does not establish that limit analytically or test the effect
of changing mW/M. This is a tree-level partonic diagnostic at two
beam tilts, with no longitudinal states or phase-space weighting.

The [saved summary](electroweak-scale-results.json) includes all group
fractions, denominator shares, and shift terms. Reproduce with NumPy:

```sh
for tilt in 0 20; do
  for pair in .48 .24 .12 .06; do
    python3 electroweak_helicities.py "$tilt" "$pair" > "scale-$tilt-$pair.json"
  done
done
python3 electroweak_scale.py scale-*.json > electroweak-scale-results.json
```

The [pair-mass scan](electroweak-pair-scale.md) changes the pair mass relative to the weak masses on two matched paths.
