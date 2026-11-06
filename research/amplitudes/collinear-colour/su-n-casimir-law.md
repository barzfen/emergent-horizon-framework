# A Casimir law for the first finite collinear colour coefficient

This extends the [SU(3) planar colour-ratio proof](planar-theorem.md). The setup is a tree-level MHV gluon amplitude, an equal-helicity positive pair on an exchange-symmetric equal-split collinear path, and a common real projective chart for the hard angle spinors. We study the squared norms of projections of the first finite amplitude coefficient. Fractions apply when that coefficient is nonzero.

## Dimension times squared colour eigenvalue

In the chart with parent spinor at infinity, remove the factors common to every colour term. The finite tensor V_m for m spectators is the sum over their orderings of the adjoint colour chains, weighted by the difference between the endpoint spectator coordinates divided by the product of adjacent spectator differences. The two pair indices are symmetric. Let N_R be the squared norm after projecting them to an irreducible symmetric colour channel R and summing all colour indices.

For two spectators, the kinematic ratio in each term is 1. The colour tensor is twice the pair interaction T₁·T₂ restricted to the symmetric space, up to a common sign. In a channel of dimension d_R and Casimir C_R its squared norm is proportional to

```text
w_R = d_R [(C_R − 2 C_A)/2]².
```

For m>2, take the difference w_S N_R − w_R N_S. It has only possible spectator-collision poles of order at most two. The commutator of the two adjacent colour generators turns each collision residue of V_m into the same tensor with one fewer spectator, with the merged colour carried by a structure constant. Squaring and summing the spectator colours multiplies the lower-order norm by C_A independently of R. The double-pole coefficient of the difference therefore vanishes by induction. The difference is invariant under interchange of the colliding spectator coordinates because their colours are summed, so the simple pole vanishes as well. With no denominators left it is a polynomial, but its degree is −2(m−2). It must vanish.

Thus the base weights determine the norm ratios at arbitrary multiplicity. This argument uses the real colour norm on a real spinor chart. For general complex angle data the argument applies to the bilinear square, and physical Hermitian weights can differ.

## SU(N), N ≥ 3

The dimensions and Casimirs are from [Dokshitzer and Marchesini, equations (3.3) and (3.7)](https://arxiv.org/abs/hep-ph/0509078). Here R₊ is the continuation of the SU(3) 27, and R₋ is the additional symmetric channel present for N≥4.

| Symmetric channel | Normalized share |
| --- | ---: |
| Singlet | 4 / [3(N²−1)] |
| Symmetric adjoint | 1/3 |
| R₊ | (N+3) / [3(N+1)] |
| R₋ | (N−3) / [3(N−1)] |

In particular the symmetric adjoint has one third of the total squared finite coefficient for every N≥3 on this locus. At N=3 the last channel is absent. At N=4 the dimensions in order are 1, 15, 84 and 20, and the shares are 4/45, 15/45, 21/45 and 5/45.

## Exact SU(4) check

Run `python3 verify_su4.py > su4-results.json`. The script constructs SU(4) structure constants from matrices and obtains the four symmetric-pair projectors by polynomial interpolation of the colour operator. It verifies the eigenvalue polynomial and projector dimensions on the full symmetric pair space. It then assembles the finite five-gluon tensor and projects it at two distinct sets of real spectator coordinates. The fractions are exact. The formulas concern the first finite coefficient of the amplitude on the stated path. Literature novelty of the all-multiplicity law remains unverified.
