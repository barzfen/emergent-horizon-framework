# A real-momentum counterexample to the collinear 1:2:3 ratio

This tests the conjectured ratio of singlet, symmetric octet and 27-dimensional squared norms in the first finite coefficient of an equal-split tree MHV collinear expansion. It keeps the SU(3) colour group, the helicities and the pair projection used in the earlier probes. It changes the kinematics from real angle spinors to real Lorentzian momenta.

## Matched six-gluon configurations

Before splitting the parent, take the three outgoing spatial momenta (3,0,0), (0,4,0), and (−3,−4,0), with energies 3, 4 and 5. Split the first outgoing momentum into the positive-helicity pair. The two incoming beams each have energy 6 and opposite directions. Use negative helicities on the two incoming labels in the all-outgoing amplitude convention. Changing the beam orientation leaves the final configuration unchanged.

| Beam direction relative to the outgoing plane | Singlet | Symmetric octet | 27 |
| --- | ---: | ---: | ---: |
| In the plane | 1/6 | 1/3 | 1/2 |
| Perpendicular | 193/13358 | 933/6679 | 11299/13358 |

The tilted beam provides a third exact point in results.json. The code clears input denominators by a common energy rescaling, which cancels out of the fractions. A five-gluon control also recovers 1:2:3.

## Kinematic and colour calculation

Each hard real null momentum is checked against a Hermitian spinor outer product, with the incoming energy sign retained. The script uses Gaussian integers and rational real and imaginary parts. It sums the squared norms of both parts to obtain each Hermitian colour norm. Colour projections use the [SU(3) multiplet projectors](https://arxiv.org/abs/1207.0609).

Choose angle spinors P+tR and P−tR for the two daughters, with conjugate square spinors and equal weights. Their total differs from the hard parent momentum only at order t². The incoming total four-vector Q(t) can absorb that difference. Hold one beam null direction ℓ fixed and choose its momentum as Q(t)²ℓ/(2Q(t)·ℓ). The other beam is the remainder and is also null. This gives a real, momentum-conserving local path in which all spectator changes begin at order t², so those changes cannot affect the constant coefficient of a simple 1/t pole.

In a DDM ordering with the pair at its endpoints and adjacent hard neighbours i and k, expansion of the Parke–Taylor denominator gives the finite coefficient as the hard Parke–Taylor amplitude times ⟨i k⟩/(2⟨P i⟩⟨P k⟩), in the common stripped normalization. The hard Parke–Taylor expression uses P as its parent angle spinor. The colour tensor is assembled before computing the norms.

The earlier proof at five points used a real-phase spinor identity. Coplanar Lorentzian configurations permit real angle-spinor representatives up to phases. Real Lorentzian momenta in general need not have that property. The perpendicular-beam example disproves the extension of the ratio to general real Lorentzian kinematics, at six points. The [later theorem](planar-theorem.md) proves the arbitrary-multiplicity law on the planar locus. The fractions refer to a finite amplitude coefficient and are not fractions of a measured scattering rate.

Run `python3 lorentzian.py > lorentzian-counterexample-results.json` with standard-library Python.
