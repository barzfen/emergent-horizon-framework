# Quadratic departure from the planar collinear colour ratio

This follows the [real-spinor colour-ratio proof](planar-theorem.md). Keep the same first finite tree-level MHV amplitude coefficient on the equal-split collinear path. Now vary the hard kinematics with a separate parameter t that tilts the incoming beams out of the plane. The collinear expansion parameter has already been taken to zero in the coefficient being studied.

## Exact identity and local expansion

Write V for the finite symmetric-pair colour tensor, in a real colour basis. Let P_R be the orthogonal projector onto channel R and p_R be its planar share. Define the real quadratic form Q_R(U) = ||P_R U||² − p_R ||U||² on real tensors. The planar proof gives the polynomial identity with the bilinear extension Q_R(V) = 0, also for complex spinor data in the chart.

Writing V = X + iY gives Q_R(X) = Q_R(Y) by taking its real part. The Hermitian share s_R thus satisfies the exact relation

```text
s_R − p_R = 2 Q_R(Y) / (||X||² + ||Y||²).
```

At a regular planar point with V(0) real up to a phase, choose the phase so V(0) is real. If V is nonzero there, the shift is O(t²), with coefficient

```text
2 [||P_R Im V′(0)||² − p_R ||Im V′(0)||²] / ||V(0)||².
```

No second derivative is needed. For the mirror-symmetric beam tilt below the shares are even in t, so the remainder after the quadratic term is O(t⁴). This formula constrains the order of onset. Its sign still depends on the imaginary tangent.

## Six-gluon calculation

Use the real Lorentzian two-to-three hard event from the earlier counterexample. In coordinates (E,x,y,z), the outgoing spatial momenta lie in the xz plane. Rotate the incoming unit beam direction from (a,0,b) to ((1−t²)a,2t,(1−t²)b)/(1+t²). The physical tilt angle is 2 arctan(t), so the quadratic coefficients per radian squared are one quarter of those reported in t.

For the original beam direction (5/13,0,12/13), the exact coefficient of t² in the 27-dimensional share is 1435201/611044, approximately 2.349. The singlet and symmetric octet coefficients are both negative. The code checks the expansion at t = 1/1000 with a separate exact complex calculation, and verifies that the mirrored tilt has the same fractions.

In all nine tests, covering seven directions for the original triangle and two additional outgoing triangles, the 27 channel gained share at quadratic order while the singlet and symmetric octet lost share. The sign theorem below extends the six-gluon 27 result beyond these samples.

Run `python3 tilt.py > tilt-results.json`. The derivative is evaluated by rational first-order spinor arithmetic and exact colour projection. The coefficients are shares of the squared finite amplitude tensor, and the calculation does not predict a measured scattering rate.

## Six-gluon sign theorem

For a regular real-projective six-gluon point, the quadratic change of the 27 share is strictly positive for every first-order imaginary deformation that moves the hard projective shape off the real locus. It is zero if the imaginary deformation can be removed to first order by a change of projective chart. This result concerns the quadratic coefficient and assumes a nonzero finite tensor at the starting point.

Send the parent to infinity and the first two sorted spectator points to 0 and 1. The other two spectators then have coordinates x=1+a and y=1+a+b, with a,b>0 at the real starting point. These are all four spectator points. The normalization can be imposed holomorphically along the deformation. Its spinor transformations and any removed helicity numerator multiply the full tensor by a common scalar and cancel out of the shares. Thus only the imaginary derivatives of x and y are needed.

Let Δ be the product of the six spectator differences and let p_w be the stripped finite ordering coefficient times Δ. Each p_w is a degree-four polynomial in the spectator coordinates. Form the constant quadratic form Q on ordering coefficients by taking half of the total colour Gram form and subtracting the singlet and symmetric octet Gram forms. On symmetric pair tensors this is the 27 norm minus half the total norm. The planar norm theorem implies pᵀQp=0, and differentiation gives pᵀQ dp=0. Therefore differentiating Δ contributes nothing to the sign, which is the sign of the quadratic form on derivatives of p.

The sign certificate computes the two-by-two matrix M_ij=(∂_i p)ᵀQ(∂_j p), for i,j=x,y, up to a positive constant. It uses SU(3) structure constants and the singlet and symmetric octet projectors to construct Q with bounded integer arithmetic. It then expands M11 and det M in a,b. All 22 nonzero coefficients of M11 and all 46 of det M are strictly positive. Thus M is positive definite throughout a,b>0, proving the sign by Sylvester's criterion. This does not rely on the beam samples.

Run `python3 verify_sign.py > sign-results.json` with NumPy installed. The output lists each polynomial as triples of exponents of a and b and the integer coefficient. This proof covers the first departure at six gluons. The sign at larger multiplicity and at finite departures is a separate question.
