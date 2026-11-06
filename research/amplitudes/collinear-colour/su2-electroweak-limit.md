# The SU(2) ratio and the electroweak limit

The [charged-basis check](su2-basis.md) reconstructs the two SU(2)
weights from the same-sign charged diagonal and the total, using the
full spectator-species sum. It also rotates the neutral gauge field
into the Z and photon directions with a decoupled hypercharge field.
Here we distinguish that basis change from the effects of electroweak
symmetry breaking.

## Ordered high-energy limit

At tree level, scale the hard momenta up at fixed nonzero opening and
fixed dimensionless kinematic ratios away from singular configurations.
Use transversely polarized external gauge bosons. In the leading
high-energy amplitudes, the unbroken gauge basis applies. For tree
amplitudes with only external gauge bosons, the hypercharge field has
no contribution in that unbroken basis. Matter or scalar lines would
need to form a loop in the absence of vacuum-expectation-value
vertices and external matter or scalar legs.

For an equal-split MHV path in the real angle-spinor chart, take the
collinear expansion of that limiting amplitude. This order of limits
recovers the pure SU(2) finite coefficient and hence the 4:5
reconstruction, with the complete spectator sum in the limiting
kinematics. The mass eigenstate labels at this order amount to a
basis rotation.

See [Electroweak Symmetry Restoration and Radiation Amplitude Zeros](https://arxiv.org/abs/2412.12336)
and [Chen, Han and Tweedie on massive electroweak collinear splitting](https://arxiv.org/abs/1611.00788).

## Finite-mass check with transverse Z bosons

A rotation of the pure gauge tensor gives zero for an all-neutral
tree amplitude because all neutral legs project onto the same W3
direction. In the broken theory, the Standard Model tree amplitude
for ZZ to ZZ receives Higgs exchange in all three channels.

For all four polarization vectors perpendicular to the scattering
plane, each product of polarization contractions is one. Up to a
common sign, the amplitude is

```text
(2 mZ²/v)² [1/(s−mh²) + 1/(t−mh²) + 1/(u−mh²)].
```

For example, at a centre-of-mass scattering angle of 90 degrees and
s = 4 mZ² + 2 mh², one has t = u = −mh². The bracket is
1/(4 mZ² + mh²) − 1/mh², which is nonzero for positive masses.
This is a finite-mass amplitude absent from the pure basis rotation.

See Appendix G of [Atwood, Bar-Shalom and Soni](https://arxiv.org/abs/hep-ph/9906400)
for the Standard Model Higgs-exchange amplitudes.

The example tests the pure rotation, while the finite-mass correction
to the original five-boson reconstruction remains open. A quantitative
test would vary the hard scale and the pair invariant mass independently.

The [pole-free rate test](su2-rate.md) specifies a candidate combination in the massless theory.
