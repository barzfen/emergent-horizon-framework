# The SU(2) 4:5 ratio in the charged and neutral basis

Rotate the first finite, symmetric pair tensor of the pure SU(2)
tree MHV amplitude into the charged basis. Trace over all spectator
colours at fixed kinematics and helicities. The normalized reduced
pair density commutes with SU(2). Its symmetric support is the
singlet plus spin 2, each with multiplicity one. If the spin-2 weight
is p5, its five magnetic components each have weight p5/5.

The ordered ++ state is the unique highest-weight component of spin 2,
so p5 is five times the normalized ++ diagonal. The singlet is the
remaining weight. All nine exact samples at five, six, and seven
gluons give the ++ diagonal 1/9 and hence the weights 4/9 and 5/9.
The direct Cartesian trace projection independently gives 4/9.

| Ordered pair | Normalized diagonal per ordering |
| --- | ---: |
| ++ or -- | 1/9 |
| +- or -+ | 1/6 |
| +0, 0+, -0 or 0- | 1/18 |
| 00 | 2/9 |

This reconstruction uses the diagonal entries and SU(2) invariance.
For a general pair density without that invariance, the neutral
singlet projection also involves off-diagonal elements.

For the neutral rotation only, extend the amplitude by a decoupled B
direction. Use W3 = cos(theta) Z + sin(theta) gamma. Every neutral
leg contributes its corresponding overlap to the amplitude. For
example the ordered Z gamma diagonal is (2/9) cos²(theta) sin²(theta).
Summing the rotated diagonals recovers the same total, and the
same-sign charged diagonal is unchanged. The script verifies this
at four exact illustrative values of sin²(theta).

These are weights of a finite amplitude coefficient on the real
angle-spinor path using complexified momentum-conserving kinematics.
This basis check omits electroweak mass and interaction effects.

Run with standard-library Python.

```sh
python3 su2_basis.py > su2-basis-results.json
```

See the [exact results](su2-basis-results.json).
