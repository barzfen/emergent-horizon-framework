# Colour information beyond the leading collinear pole

This is a five-gluon tree-level SU(2) Yang–Mills amplitude calculation. The pair 1 and 5 has positive helicity and approaches collinearity. The negative helicities are on legs 2 and 3. The spinors follow an equal-split, momentum-conserving path with rational complexified kinematics. The reported amplitudes use a common stripped normalization.

## Two invariant colour contractions

Write the external adjoint colour indices as a1 through a5. Define A = ε(a1,a5,a2) δ(a3,a4) and S = δ(a1,a5) ε(a2,a3,a4). Contract the full amplitude with A + S or A − S. Both tensors are invariant under simultaneous adjoint rotations and have the same norm. In the first tensor component, the pair is antisymmetric and couples to a single adjoint parent. In the second it is a symmetric colour singlet. The leading gluon splitting colour factor is antisymmetric, so its contraction with S vanishes.

The calculation gives the following expansion coefficients in the path parameter t at the first point.

| Contraction | Pole coefficient multiplying 1/t | Finite coefficient |
| --- | ---: | ---: |
| A + S | 750 | −3875 |
| A − S | 750 | +3875 |

The two choices have the same nonzero pole at all three tested points, with distinct finite terms. Exchanging legs 1 and 5 sends t to −t along this path. Bose symmetry makes the A projection odd and the S projection even. The split colour factor explains the vanishing pole of S. The exact amplitude calculation establishes that its finite term is nonzero at the tested points.

The full contracted amplitudes agree between the Pauli trace and Del Duca–Dixon–Maltoni structure-constant decompositions, both for the Laurent coefficients and at finite values of t. The reported difference is a statement about invariant contractions of a perturbative amplitude. Its scope is this path and helicity sector. No cross section or correspondence to the numerical ordering cuts is inferred.

## Reproduce

Run `python3 color_probe.py` with standard-library Python. The script checks momentum conservation, evaluates the Parke–Taylor factors, and computes the pole and finite terms with exact fractions.

References for the established theory are [Del Duca, Dixon and Maltoni on colour decomposition](https://arxiv.org/abs/hep-ph/9910563), [Catani and Grazzini on collinear factorization](https://arxiv.org/abs/hep-ph/9908523) and [Stieberger and Taylor on finite collinear terms](https://arxiv.org/abs/1508.01116).
