# When SU(3) colour channels first appear in the collinear expansion

We study tree-level MHV amplitudes with negative helicities on 2 and 3 and an equal-split collinear path for the positive-helicity legs 1 and n. The parameter is t. We use real rational angle spinors and a momentum-conserving analytic path. The results concern the coefficients of the full colour amplitude at each order, resolved into irreducible representations of the pair. Channel weights are squared norms of individual coefficient vectors.

| Coefficient | Channels seen in the exact probes |
| --- | --- |
| t⁻¹ | Antisymmetric octet |
| t⁰ | Singlet, symmetric octet, 27 |
| t¹ | Antisymmetric octet and the combined decuplet sector |
| t² | Singlet, symmetric octet, 27 |
| t³ | Antisymmetric octet and the combined decuplet sector |

The leading octet is the standard collinear splitting channel. Bose symmetry gives a general selection rule for this path: exchanging the equal-helicity legs sends t to −t, so odd powers are colour antisymmetric and even powers are colour symmetric. The representation decomposition and projectors follow [Keppeler and Sjödahl](https://arxiv.org/abs/1207.0609). Symmetry allows the decuplet pair in odd orders, and the computed t¹ coefficient shows it actually enters at the first odd order after the pole. The computation resolves the combined sector and does not separately project the two conjugate irreducible representations.

The five-point 1:2:3 ratio of symmetric-channel weights at t⁰ survives two six-point tests and one seven-point test. The t² coefficient does not obey that ratio, even at five points. The ratio is a candidate relation for the first finite MHV coefficient along the specified path, and is proved at arbitrary multiplicity on the real-spinor locus in the [later theorem](planar-theorem.md).

## An exact helicity control

In an MHV amplitude, moving both negative helicities from the spectators 2 and 3 onto the collinear pair multiplies every colour-ordered term by the same factor ⟨1 n⟩⁴/⟨2 3⟩⁴. Along this path ⟨1 n⟩ is linear in t. The entire colour expansion therefore shifts by four powers of t for that helicity choice. The leading octet moves from t⁻¹ to t³, the three symmetric channels from t⁰ to t⁴, and the first combined decuplet contribution from t¹ to t⁵ in the examples with nonzero coefficients. This is a numerator identity for the two MHV helicity assignments and is independent of the colour decomposition.

## Reproduction and scope

Run `python3 orders.py > channel-orders-results.json` with standard-library Python. The code expands the Parke–Taylor denominators in exact rational arithmetic, constructs the full colour tensor by sparse chains of SU(3) structure constants, and checks exchange parity on each colour assignment. For five points it compares the pole and finite partial-amplitude coefficients to the earlier implementation. The decuplet sector is the orthogonal remainder of the antisymmetric pair after subtracting the antisymmetric octet. The output records fractions of each separate coefficient norm. It does not calculate cross sections or establish a correspondence to numerical ordering cuts.
