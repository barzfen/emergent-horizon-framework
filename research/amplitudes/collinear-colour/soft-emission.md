# Soft emission from the first finite collinear colour channels

This follows the [collinear-colour studies](README.md). Take the leading soft-energy limit at fixed hard kinematics first, then expand in the equal-split collinear parameter t at fixed soft direction. We resolve the colour of the two hard daughters after emission. The result is a projected partonic amplitude calculation.

## Two amplitudes contribute at the same order

Write the hard amplitude as L/t + B + O(t). The hard pole tensor L is in the antisymmetric adjoint pair channel. The finite tensor B is symmetric on the specified equal-helicity path. The tree eikonal current is the sum over hard legs of T_i times p_i·ε/(p_i·q), where q is the soft direction. See [Catani and Grazzini](https://arxiv.org/abs/hep-ph/0007142).

At t=0 the pair contributes through T₁+T₂, so the zeroth-order current J₀ preserves pair representations. Spectator terms also preserve them. At first order the pair eikonal weights shift oppositely, so J₁ is proportional to T₁−T₂. The symmetric projection of the soft amplitude has no pole in t. Its finite term is J₀ B + J₁ L. Both contributions are needed, including their interference. The Ward identity holds separately for these contributions on this path. In the first term, replacing the polarization by q invokes total colour conservation. In the second, each derivative eikonal weight vanishes under that replacement.

## The difference current reproduces the Casimir law

For a parent colour d, the leading splitting tensor is proportional to f(a,b,d). Acting with T₁^c−T₂^c, where c is the emitted gluon colour, gives a symmetric sum of two products of structure constants, up to a common phase. As a map from the parent and emitted colours (d,c) to the daughter pair (a,b), it is proportional to twice the colour dipole operator projected onto the symmetric pair. This is the same map as in the four-gluon starting case of the [SU(N) law](su-n-casimir-law.md).

For a fixed pair projection R, summing the emitted and daughter colours makes the resulting quadratic form on the parent colour proportional to the identity by adjoint invariance. Its trace is proportional to the representation dimension times the squared colour-dipole eigenvalue. This applies for any hard spectator tensor multiplying the parent. Thus the isolated difference-current contribution has the Casimir weights, including the SU(3) ratio 1:2:3. Its total colour strength before multiplying by the squared eikonal derivative is 3 C_A times the norm of the pole tensor, by (T₁−T₂)² = 4 C_A−(T₁+T₂)².

## Exact example with all emitters

Use a five-gluon hard MHV configuration with negative helicities on the two crossed incoming legs, a collinear positive pair along the x axis, and the soft direction along the y axis. The daughter opening is varied in the xz plane. Momentum conservation and the null conditions are checked through first order, which suffices for the finite term. An order-t² recoil can restore exact conservation along the path without changing that term.

| Contribution | Singlet | Symmetric octet | 27 |
| --- | ---: | ---: | ---: |
| Hard finite tensor | 1/6 | 1/3 | 1/2 |
| J₀ B alone | 27/257 | 57/257 | 173/257 |
| J₁ L alone | 1/6 | 1/3 | 1/2 |
| Full symmetric soft finite tensor | 9/284 | 12/71 | 227/284 |

The norms sum over both physical soft polarizations and all colour indices after projection. The full row includes interference. At this point the interference is negative in the singlet and symmetric octet and positive in the 27. Thus an extra soft gluon probes a combination of the hard finite colour channels and the first angular correction to emission from the hard pole. The projected calculation does not define a detector measurement of pair colour or an inclusive cross section.

Run `python3 soft_probe.py > soft-probe-results.json` with standard-library Python. The exact check includes all five hard emitters and verifies total colour conservation and the difference-current norm.

## Colour-summed radiation weight

For the same soft direction, keep the recoil needed to conserve the hard momenta through order t². Now sum over all hard colours, emitted colours, and both soft polarizations, without projecting the pair. The calculation keeps the same hard helicity assignment. Strip the soft coupling and set the soft energy to one in the eikonal weight.

If the leading-soft amplitude is A/t + D + t E + …, its colour-summed constant term is ||D||² + 2 Re⟨A,E⟩. The second term involves the hard order-t coefficient and the first two corrections to the soft current. In the example these two pieces are 1917 and 135/2 in the common stripped normalization. Their sum is 3969/2. The interference between the two symmetric contributions is already included in ||D||².

Dividing the soft norm by the hard norm at the same kinematics gives a conditional partonic radiation weight of 14 + (14/3)t² + O(t⁴). Exchanging the two equal-helicity daughters flips t and leaves the weight unchanged. The positive coefficient is specific to this soft direction and recoil path. It includes the other emitters and the pole interference. It is not a prediction for a colour-tagged cross section or a jet observable.

Run `python3 colour_sum.py > colour-sum-results.json`. The script checks the expansion against the unexpanded amplitude and eikonal current at a small rational t with exact real momentum conservation.
