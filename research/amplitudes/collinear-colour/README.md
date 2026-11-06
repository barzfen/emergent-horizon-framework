# Colour channels in the first finite collinear coefficient

In tree-level SU(3) MHV Yang–Mills, for an exchange-symmetric equal-split collinear path and hard angle spinors admitting a common real chart, the squared colour norms of the first finite coefficient in the singlet, symmetric octet and 27 obey **1:2:3 at arbitrary multiplicity**. This includes coplanar real Lorentzian hard configurations. An exact noncoplanar real Lorentzian example disproves the corresponding unrestricted claim.

The original ratio concerns an amplitude coefficient in full SU(3) colour. The [SU(N) extension](su-n-casimir-law.md) gives the corresponding weights for other colour groups. Coplanarity here is a kinematic restriction. The theorem is separate from a leading-colour approximation and from a statement about a measured rate.

| Result | Reproduce from this directory |
| --- | --- |
| [SU(2) control](su2-control.md) | `python3 color_probe.py` |
| [SU(3) projection and five-gluon derivation](su3-channels.md) | `python3 su3_probe.py` |
| [Colour channels by order at five through seven gluons](channel-orders.md) | `python3 orders.py` |
| [Matched real Lorentzian counterexample](lorentzian-counterexample.md) | `python3 lorentzian.py` |
| [SU(3) all-multiplicity proof](planar-theorem.md) and exact checks | `python3 verify.py` |
| [SU(N) Casimir law](su-n-casimir-law.md) and exact SU(4) checks | `python3 verify_su4.py` |

Each study has a corresponding results JSON. The proof uses colour Casimirs at four points and induction on spectator-collision poles. See the [literature search](literature.md) for prior results and the scope of the novelty check. This study followed the [nine-point ordering work](../nine-point-tail/followups/README.md). A correspondence between its ordering cuts and these colour channels remains open.
