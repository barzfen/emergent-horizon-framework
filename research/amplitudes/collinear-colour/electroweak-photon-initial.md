# Fixing the two incoming particles to photons

Repeat the transverse six-vector comparison with two incoming photons.
Sum the transverse helicities and keep the two recoil species sums
complete. The numerator is the same-sign charged squared amplitude.
The denominator is three times the sum of that weight and the four
ordered neutral-pair weights. The ratio uses squared amplitudes at
matched phase-space points with no flux or phase-space weighting.

For each pair mass and tilt, compare to the massless calculation
with the same incoming photons, energy fractions, planes and
helicities. The massive points use mW/M=0.30 and sin²(theta)=0.23.
The two incoming photons each project onto W3 in the massless
gauge amplitude. The script checks all massless helicity weights
against the independent SU(2) tensor with both incoming colours
fixed to W3, allowing one common normalization per point. Photon
Ward identities and global helicity reversal are checked for
the original reference helicity at each point.

| Tilt | Q/M | Massless with complete incoming species sum | Massless with two photons | Massive with two photons |
| ---: | ---: | ---: | ---: | ---: |
| 0° | 25 | 0.112603 | 0.225996 | 0.227680 |
| 0° | 200 | 0.112467 | 0.226241 | 0.226305 |
| 20° | 25 | 0.119665 | 0.172577 | 0.173917 |
| 20° | 200 | 0.119469 | 0.172868 | 0.174952 |

Fixing the incoming state changes the massless baseline much
more than the massive correction changes the photon-only result
at these points. A fixed W3 W3 incoming state does not give an
SU(2)-invariant spectator trace. Thus the argument that multiplies
the same-sign weight by five cannot be applied to this restricted
sum. The near doubling of the all-transverse planar fraction is
a numerical result of this geometry and selection.

Use `python3 electroweak_photon_initial.py 0 .48` with NumPy.
Repeat with tilt 20 and with pair mass .06 for the other points.
The [saved summary](electroweak-photon-initial-results.json)
includes separate equal and opposite daughter helicity sums.

The [incoming colour average](su2-incoming-average.md) separates the effect of selecting a fixed direction from aligning the incoming states.
