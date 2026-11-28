# SU(3) colour channels beyond the collinear pole

This extends the SU(2) control calculation to the colour group of QCD. Use a five-gluon tree amplitude with negative helicity on 2 and 3. The positive-helicity pair 1 and 5 follows the equal-split path in color_probe.py. The calculation projects the full colour tensor onto representations of the pair, leaving all other colours summed in the squared norms. It uses the standard adjoint-pair projectors described by [Keppeler and Sjödahl](https://arxiv.org/abs/1207.0609).

| Pair representation | Share of squared pole coefficient | Share of squared finite coefficient |
| --- | ---: | ---: |
| Antisymmetric octet | 1 | 0 |
| Singlet | 0 | 1/6 |
| Symmetric octet | 0 | 1/3 |
| 27-dimensional representation | 0 | 1/2 |
| Decuplet and conjugate decuplet | 0 | 0 |

The fractions in the last column are for the squared norm of the finite amplitude coefficient on the real-angle-spinor locus described below. The squared full amplitude can also have a term at order t⁰ from interference between the pole and the order-t coefficient. The table is not a decomposition of that full t⁰ term or of a cross section.

The antisymmetric splitting colour factor gives the pole octet. Exchange of the two equal-helicity legs sends t to −t on this path. Bose symmetry therefore puts the finite coefficient entirely in the symmetric pair sector. In particular the singlet contribution has no interference with the pole in the colour sum. Two invariant contractions are independently evaluated in the trace and structure-constant decompositions, following [Del Duca, Dixon and Maltoni](https://arxiv.org/abs/hep-ph/9910563). The three rational test points all agree between these decompositions and all have nonzero singlet, symmetric-octet and 27 contributions.

## Why the symmetric fractions are fixed in this case

Choose the three spectator orders 234, 243 and 324 as representatives modulo reversal. Write (x,y,z) for the finite Parke–Taylor coefficients on these orders, with pair 1 and 5 at the endpoints. Reversing the spectator order reverses the finite coefficient. The symmetric colour tensors are thus combined with weights 2(x,y,z) when each basis tensor is defined by averaging its two pair orientations.

The projector Gram forms on the three symmetric colour tensors, with weights (x,y,z) and before that common factor of 2, are

```text
N1  = (27/4) |x - y - z|²
N8s = 27 (|x|² + |y|² + |z|²)
N27 = 4 N8s - 5 N1
```

The script verifies the Gram entries by exact colour contractions of individual tensors and pairwise sums. They are real symmetric forms and so determine the Hermitian forms as well.

Let P be the angle spinor in the collinear direction. Define u = ⟨P 2⟩⟨3 4⟩ and v = ⟨P 4⟩⟨2 3⟩. Schouten gives ⟨P 3⟩⟨2 4⟩ = u + v. Expanding the Parke–Taylor denominator on the equal-split path gives (x,y,z) proportional to ((u+v)², −v², −u²). For real u and v, or for u and v with a common complex phase, the identity

```text
[(u+v)² + v² + u²]² = 2 [(u+v)⁴ + v⁴ + u⁴]
```

gives N8s = 2 N1 and N27 = 3 N1. The ratios apply where the denominator is regular apart from the specified collinear pole and the finite vector is nonzero. No generalisation to arbitrary complex kinematics, helicities, higher multiplicity, or numerical ordering cuts is claimed.

## Reproduce

Run `python3 su3_probe.py > su3-channels-results.json`. The script uses rational arithmetic and an integer-entry Gell-Mann basis with the associated diagonal metric. The file color_probe.py supplies the momentum-conserving path and Laurent expansion used in the SU(2) calculation.
