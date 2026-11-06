# Colour channels in the first finite collinear coefficient

This series follows what the first finite correction to the leading two-gluon collinear limit retains about the pair's colour. It studies the full-colour tree MHV amplitude along an exchange-symmetric equal-split path. All shares below are squared norms of projections of that amplitude coefficient.

## What we found and why it matters

**The 1:2:3 law is an exact constraint within QCD.** When two gluons are nearly parallel, the leading term describes their splitting from a parent gluon. The first finite term gives us a way to ask what colour structure appears beyond that leading description. On the planar, equal-split MHV path studied here, the singlet, symmetric octet and 27-dimensional channel carry one sixth, one third and one half of that finite term's squared norm. Those shares hold as more gluons are added. [Planar proof](planar-theorem.md)

**For physics, the law fixes how the pair's colour correlation first changes as the gluons separate.** On the planar path, the coefficient of that change follows from the squared norm of the finite term relative to the squared norm of the leading pole. In one six-gluon test, tilting the beam out of the outgoing plane made the singlet lose share and the 27 channel gain share. Both changes strengthened the correction. In a separate radiation test, most of the angular contrast was already present when the hard amplitude was frozen at its leading form and the soft radiation could still resolve the two daughter directions. How much of the hard colour shift survives in the full radiation pattern remains open. [Hard colour test](pair-dipole.md) · [Radiation control](pole-control.md)

**For calculations, the immediate use is a benchmark with a narrow shortcut.** If the total squared norm of the planar finite term is known, the law gives the three channel norms directly. The planar pair-correlation correction also follows from one norm ratio. A general soft-radiation calculation still needs colour correlations involving the other hard gluons, and an overall speedup has yet to be demonstrated.

## Main results

1. **On the real-spinor locus**, the SU(3) singlet, symmetric octet and 27-dimensional channel have weights **1:2:3** at arbitrary multiplicity. This includes coplanar real Lorentzian hard momenta. The [proof](planar-theorem.md) starts from four-gluon colour Casimirs and uses induction on spectator collisions. The [SU(N) extension](su-n-casimir-law.md) gives weights proportional to the channel dimension times the squared colour-interaction eigenvalue.
2. **Away from the real locus**, the same fractions can change. A [matched six-gluon example](lorentzian-counterexample.md) varies the beam direction while keeping the outgoing configuration fixed.
3. **Near the real locus**, the first possible change is quadratic, given by an exact formula involving the imaginary first derivative of the finite tensor. At six gluons, the [sign proof](near-planar-sign.md) shows that every nontrivial imaginary projective tangent increases the 27 share at quadratic order from its planar value of one half.

4. **With an extra soft gluon**, the first angular correction to the eikonal current reproduces the Casimir weights in isolation. Radiation from the finite hard amplitude interferes with it. The [soft-emission calculation](soft-emission.md) includes both the pair-projected result and the colour-summed radiation weight.

## Calculations and reproduction

Run the commands in this directory. Each script prints JSON that can be compared with the linked output. The six-gluon sign certificate and the angular calculations use NumPy. The other scripts use the Python standard library.

| Study | Command | Saved output |
| --- | --- | --- |
| [SU(2) colour control](su2-control.md) | `python3 color_probe.py` | [Results](su2-control-results.json) |
| [SU(3) projection and five-gluon derivation](su3-channels.md) | `python3 su3_probe.py` | [Results](su3-channels-results.json) |
| [Colour channels by order at five through seven gluons](channel-orders.md) | `python3 orders.py` | [Results](channel-orders-results.json) |
| [Matched real Lorentzian counterexample](lorentzian-counterexample.md) | `python3 lorentzian.py` | [Results](lorentzian-counterexample-results.json) |
| [SU(3) all-multiplicity proof and algebra checks](planar-theorem.md) | `python3 verify.py` | [Results](planar-theorem-results.json) |
| [SU(N) Casimir law and exact SU(4) checks](su-n-casimir-law.md) | `python3 verify_su4.py` | [Results](su4-results.json) |
| [Near-planar curvature and nine beam-tilt tests](near-planar-sign.md#six-gluon-calculation) | `python3 tilt.py` | [Results](tilt-results.json) |
| [Six-gluon sign certificate](near-planar-sign.md#six-gluon-sign-theorem) | `python3 verify_sign.py` | [Polynomial coefficients](sign-results.json) |
| [Soft emission and pair-colour interference](soft-emission.md) | `python3 soft_probe.py` | [Results](soft-probe-results.json) |
| [Colour-summed radiation weight](soft-emission.md#colour-summed-radiation-weight) | `python3 colour_sum.py` | [Results](colour-sum-results.json) |
| [Five-gluon angular and helicity checks](angular-ensemble.md) | `python3 angular_ensemble.py` | [Results](angular-ensemble-results.json) |
| [Six-gluon full helicity sum](six-soft.md) | `python3 six_soft.py` | [Results](six-soft-results.json) |
| [Matrix-element-weighted orientation average](weighted-angles.md) | `python3 weighted_angles.py` | [Results](weighted-angles-results.json) |
| [Outgoing-shape and beam average](shape-average.md) | `python3 shape_average.py` | [Results](shape-average-results.json) · [Centre control](shape-average-centre.json) |
| [Opening-plane orientation scan](plane-scan.md) | `python3 plane_scan.py` | [Results](plane-scan-results.json) |
| [Leading parent-pole control](pole-control.md) | `python3 pole_control.py` | [Results](pole-control-results.json) |
| [Six-gluon hard-pair colour correlation](pair-dipole.md) | `python3 pair_dipole.py` | [Results](pair-dipole-results.json) |

## Scope and open questions

Coplanarity is a restriction on the kinematics. These results concern the first finite amplitude coefficient at fixed colour group. The sign at higher multiplicity and the behaviour at finite tilt remain open. The [literature search](literature.md) describes related results and the limits of the novelty check for the planar ratio. The [nine-point ordering studies](../nine-point-tail/followups/README.md) motivated this work. A correspondence between their ordering cuts and the colour channels remains open.
