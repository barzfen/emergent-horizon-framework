# A planar 1:2:3 theorem for the first finite SU(3) collinear coefficient

## Statement

Consider a tree MHV gluon amplitude with two positive-helicity legs approaching collinearity along an exchange-symmetric equal-split path. Assume the limiting hard angle spinors, including the parent direction, admit real projective representatives and that there are no other collinear degeneracies. At any multiplicity, the squared colour norms of the first finite coefficient in the pair singlet, symmetric octet and 27 are proportional to 1:2:3. The statement is an equality of norms and applies even if the common weight vanishes. Its fractions are defined where the finite coefficient is nonzero. Coplanar real Lorentzian hard momenta are an instance of the real-spinor hypothesis.

Use the tree-level [Del Duca–Dixon–Maltoni decomposition](https://arxiv.org/abs/hep-ph/9910563) and the [orthogonal SU(3) colour projectors](https://arxiv.org/abs/1207.0609). Overall coupling, helicity numerator, and spinor normalisations common to all terms are immaterial for the ratio.

## Finite coefficient in a real chart

Let the pair angle spinors be P+tR and P−tR to first order, with the spectator momenta even in t. For an ordering with hard neighbours i and k at the two ends of the spectator word, the finite coefficient equals the lower-point Parke–Taylor expression with parent spinor P multiplied by ⟨i k⟩/(2⟨P i⟩⟨P k⟩). This follows by expanding the two end brackets and using Schouten. Changes beginning at order t² cannot affect this coefficient of a simple pole.

Send P to (0,1) and rescale the remaining angle spinors to (1,z_i). All z_i are real under the hypothesis, and the omitted factors are common to the full tensor. If m is the number of spectators, the stripped finite colour tensor is

```text
V_m(z) = sum over spectator permutations w of
         C(w) (z_last − z_first) / product over adjacent (i,j) in w of (z_j − z_i).
```

Here C(w) is the chain of structure constants with the two collinear legs at the endpoints. Reversing the pair endpoints together with the spectator word gives the colour sign (−1)^m. Reversing just the spectator word in the scalar coefficient gives the same sign. Therefore V_m is symmetric on the two pair indices. Write N_R for the sum of squares of the entries of its projection onto pair representation R, in an orthonormal real colour basis.

## Starting case

For m = 2 the ratio of differences in each summand is 1. The two chains add to the symmetric projection of twice the colour operator T₁·T₂, up to an overall sign convention. This can be read directly from the two structure constants in a chain. The operator eigenvalue on R is (C_R−2C_A)/2, since (T₁+T₂)² = T₁²+T₂²+2T₁·T₂. With C_A = 3, the symmetric representations have Casimirs 0, 3 and 8, and dimensions 1, 8 and 27. Their squared norms are thus in the proportions

```text
1 × (−3)² : 8 × (−3/2)² : 27 × 1² = 9 : 18 : 27.
```

This starting identity is algebraic in the spinors. It requires no nondegenerate four-gluon real Lorentzian hard event.

## Induction on the number of spectators

Consider either difference D_m = N_8s−2N_1 or D_m = N_27−3N_1.

1. Each entry of V_m can have only a simple pole on a spectator collision z_a=z_b. Only orderings where a and b are consecutive contribute. Pair the two orders of a and b. The pole signs are opposite, so their colour chains subtract to a commutator. By the Lie algebra relation, the residue is V_(m−1) with a and b replaced by one spectator and its colour contracted with f^{a b c}, up to a common sign.
2. The pair projector acts on the other two indices and commutes with this spectator contraction. On summing spectator colours, f^{a b c} f^{a b d} = C_A δ^{c d}. Thus the potential double-pole coefficient of D_m is C_A times the corresponding D_(m−1), which vanishes by induction.
3. The colour-summed D_m is invariant under interchanging z_a and z_b because this simply relabels summed spectator colours. With their midpoint and all other variables fixed, it is even in z_b−z_a. Hence there is no simple pole either.
4. The spectator differences are the only possible denominator factors. With each pole removed, D_m is a polynomial. Yet it is homogeneous of degree −2(m−2), which is negative for m>2. Therefore D_m vanishes identically.

This proves both norm identities at every multiplicity. The pole argument also proves the two quadratic identities as **complex bilinear** identities by algebraic continuation. For complex angle data the physical colour norm is Hermitian and involves conjugation. It can violate the ratio, as the noncoplanar six-gluon counterexample shows.

## Reproduce the algebra checks

Run `python3 verify.py > planar-theorem-results.json`. It verifies the base and the next two multiplicities by exact colour contraction and checks the collision residue directly for two spectator pairs. These checks supplement the proof. The theorem concerns the finite amplitude coefficient on the specified path, with no assertion about a full scattering rate or literature novelty.
