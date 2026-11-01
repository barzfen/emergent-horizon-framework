# EHF assumption audit 05: reversible probe-gated structural writing

Date: 1 November 2026. Status: explicit finite classical interaction; exact rate and waiting-time checks; numerical retention and unintended-write calculations. No novelty or physical-origin claim.

Research direction: Barry Fensom. Development, implementation and exposition assisted by ChatGPT. Follows [Audit 04](../assumption-audit-04/README.md).

## Result

The probe's actual movement can enable a structural write without an external switch or an appended memory bit. The model also supports reset by the reverse crossing. But this simplest gate supplies neither durable storage nor selective response to deliberate inputs: the reverse transition can immediately erase the record, and unplanned crossings write it too.

Unlike Audit 04's storage benchmark, **the writer is never disabled during retention**. All six tested models evolve the carrier and probe together under a single time-independent rule. The gate's availability is represented by the probe's current location and cycle, not by an unmodelled on/off schedule.

The gate rule itself, its selected ports and cycle, and the suppression of other structural moves are still chosen. This constructs a constrained interaction; it does not derive that constraint from bare admissibility.

## 1. Existing carrier, represented gate

Keep the structural A/B pair from Audit 04:

| Cycle | Blank A | Written B |
| --- | --- | --- |
| 0 | 0,1,2,3,4 | 0,1,3,2,4 |
| 1 | 0,1,2,3,4 | 0,1,2,3,4 |
| 2 | 0,2,4,1,3 | 0,2,4,1,3 |

Both obey the no-triple-used-edge rule. A and B differ by the allowed adjacent swap of 2 and 3 in cycle 0. Their boundary edge {0,2} belongs uniquely to cycle 2. Their multiplicities at boundary edge {1,2} are 2 and 1 respectively, allowing an ideal structural readout to tell them apart.

The full state is (S,v,k), with S in {A,B}, five probe positions and three cycle labels: **30 joint states**. S denotes the actual triad arrangement, not a newly appended register. The two-carrier sector is closed because we permit only this selected structural involution during crossings. Other admissible LR2 moves are suppressed in the main model. This is a substantial imposed kinetic constraint, not a consequence of the no-triple-edge condition. In particular, Audit 04's full 516-state rearrangement noise is not included here.

Each probe spatial neighbor in its current network/cycle is reached at rate 1/2; each other cycle is reached at rate kappa/2. A spatial traversal of {0,2}, in **either direction**, simultaneously applies S -> the other triad. All other spatial jumps and cycle switches leave S unchanged. Thus the selected write and its reverse are

\[
(A,2,2)\mathrel{\mathop{\rightleftarrows}^{1/2}_{1/2}}(B,0,2).
\]

There is also the reverse carrier pairing (B,2,2) <-> (A,0,2). The crossed edge remains in cycle 2 after every update. Coupling both directions changes Audit 04's directed-herald rule so that every joint transition now has an equal-rate reverse. This modification is explicit; reversibility was not established for Audit 04's directed writer.

Here **reversible means Markov-chain detailed balance**: the joint generator Q is symmetric and has uniform equilibrium. It does not mean that stochastic evolution preserves all initial-state information, or that Q alone describes a complete microscopic thermodynamic system.

## 2. What is temporarily protected?

At zero leakage, the instantaneous hazard of a carrier change is

\[
\lambda(S,v,k)=\begin{cases}1/2,&k=2,\ v\in\{0,2\},\\0,&\text{otherwise.}\end{cases}
\]

The probe therefore explicitly supplies the enabling condition. While it is away from those ports in cycle 2, the structure has no allowed change. But normal motion can bring it back. A zero instantaneous hazard in one state is not a guarantee of future isolation.

Immediately after the selected write the probe is at (0,2), an enabled location. Its total next-transition rate is 1+kappa. The reverse crossing has rate 1/2, so the probability that the **very next transition** undoes the write is exactly

\[
\frac{1}{2(1+\kappa)}.
\]

At kappa=0.1,1,10 this is respectively 5/11, 1/4 and 1/22. Faster switching reduces this immediate risk, but the probe remains in a finite returning system. It does not remove later erasure. No directional bias, ratchet, externally triggered closure, probe removal or cooling operation is assumed.

## 3. Ongoing-writer retention

The **written history** is the state (B,0,2) produced by an actual crossing from (A,2,2). The **matched blank history** is (A,0,2), with the same current probe coordinates but no preceding write. Both subsequently evolve under the same Q; no writer shutdown or stopping intervention occurs. These are controlled conditional starting states, not uniformly sampled histories.

We compare the two evolving laws by total variation, either on the complete joint state or after observing only the carrier. Equal-prior best classification success is (1+D)/2, as in Audit 02.

For kappa=1, with no independent carrier leakage:

| Time after write | Ideal carrier-only classification success | Ideal full-joint-state success | Probability carrier has never yet reset |
| --- | ---: | ---: | ---: |
| 1 | 80.1898% | 92.5717% | 76.5942% |
| 3 | 73.8465% | 75.1635% | 65.8648% |
| 10 | 63.3081% | 63.3081% | 45.8464% |
| 30 | 52.5192% | 52.5192% | 16.3704% |
| 100 | 50.0074% | 50.0074% | 0.4453% |

Units are inherited inverse spatial-hop-rate units, not seconds. These are numerical probability calculations, not observed trials. Near equality between carrier and full-state success at some listed times is a numerical finding for this comparison, not a universal equality theorem.

The last column asks whether any reset has happened since the selected write. A carrier can reset and later return to B, so its current value alone does not certify an unbroken record. The mean time to **first** reset from (B,0,2) at kappa=1 is exactly 16965/1129, approximately 15.027 model-time units. The code solves the 15-state killed-sector waiting equations with rational arithmetic.

All six joint generators tested below are connected and symmetric. Their unique stationary law is uniform on 30 states, with half its mass on each carrier. The two initial histories therefore become indistinguishable in the long-time limit. This follows from finite symmetric-generator spectral decomposition; it is not inferred solely from the final sampled time.

Readout is ideal access to the current A/B structure, for example its boundary-link multiplicity. The full-state reader is an even stronger bound. Audit 04's one-hop detector was not simulated here, and an internal reader has not been derived. Readout is not allowed to use a noiseless stored list of earlier events.

## 4. Unintended writes and reuse

To test accidental activation, start with carrier A and a probe uniformly distributed over its 15 position/cycle states, with no commanded write and no extra mechanism distinguishing intention. Leave exactly the same gate rule active. At kappa=1 and zero leakage:

| Time | Probability the nominally idle carrier currently reads B |
| --- | ---: |
| 1 | 4.9143% |
| 3 | 11.9514% |
| 10 | 28.7545% |
| 30 | 45.9784% |

These are current wrong-carrier probabilities, not probabilities that any unintended write has ever occurred. Later toggles can undo earlier ones. There is no extra label in this model saying that one crossing is deliberate and another is incidental. The same modeled state and transition rule cannot respond differently solely because we describe their causes differently.

Reset is possible: a reverse crossing returns B to A and places the probe at (2,2). There is no absorbing reset flag or one-use latch. But the model does not choose when that reset happens or hold A safely afterward. Consequently it supplies **repeatable toggling**, not a reliable on-demand writable/resettable memory. Steering, identifying or removing a probe, distinguishing probe types, or using different driving conditions would add control assumptions.

At equilibrium and zero leakage, the four directed carrier-changing jumps each have stationary source mass 1/30 and rate 1/2. The total flip flux is exactly 1/15; the stationary mean interval between all flips is therefore 15. This average event interval is distinct from the conditional mean first reset 16965/1129 and from waiting from a uniformly sampled probe state. The latter is approximately 19.257 at kappa=1. None of these equalities asserts Poisson-distributed inter-event intervals.

## 5. Leakage sensitivity and scope

As a limited perturbation test, add an independent allowed A<->B rearrangement at rate epsilon=0.01 at every probe state. It changes the existing carrier, not an appended bit. Its reverse has the same rate. This only tests leakage through the selected structural reversal; it does not restore all other admissible triads or constitute a comprehensive noise model.

The carrier-change hazard becomes the gate hazard plus epsilon. The stationary total flip flux becomes 1/15+epsilon=23/300, with mean inter-flip interval 300/23. Both structural writing and unintended resetting remain active. Full results retain the time scans and exact first-reset costs with and without leakage, at kappa=0.1,1,10. No claim is made that increasing kappa or adding leakage monotonically improves or worsens every possible readout at every time; the stated tests have their declared scope.

## 6. Checks and reproduction

Requires Python 3.10+, NumPy and SciPy:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 foundation/assumption-audit-05/probe.py
```

For each of six parameter combinations, the standalone script verifies exact rational generator symmetry, conservation, nonnegative rates, gate hazards, write/reverse rates, stationary flip flux and connectivity of all 30 states. Exact rational linear solves establish first-reset waiting times and check their defining equations. The numerical calculations check stochastic transition matrices, a single stationary eigenmode, observation/data-processing bounds, and first-reset survival against current-carrier probabilities. Eigenmode transition matrices are independently checked by direct matrix exponentiation at time 3 to absolute tolerance 4e-13. At time zero the identity matrix is used exactly to avoid reporting roundoff as probabilities outside [0,1].

All assertions passed. The time grid is 0,0.1,1,3,10,30,100. [probe.py](probe.py) and [results.json](results.json) include the source hash, versions, exact fractions and unrounded numerical tables. No random trajectories or fitted parameters are used.

## Assessment, attribution and contribution back

This audit removes Audit 04's external writer-shutoff step and makes the enabling condition part of the probe/network dynamics. It exposes the price of that change: returning probes undo writes, and accidental crossings cannot be distinguished from selected inputs. Strong protection is still not explained; suppressing all non-gated rearrangements was itself a substantial choice.

The carrier pair and admissibility conventions come from EHF Audit 04; the inherited Hamiltonian-triad probe and directed-herald motivation come from RW-003 through RW-005. Their primary-source acknowledgements remain in those entries. Bidirectional gate coupling is an explicitly new model choice here. Detailed balance, finite-chain mixing, killed-process waiting equations and total variation are standard mathematical methods, not EHF inventions. The calculations are self-contained; NumPy and SciPy versions are recorded. No external code or paper text is reproduced, and no novelty review was performed.

**Potential contribution back:** nothing ready for novelty-based outreach. The benchmark's value is a reproducible negative result about this proposed mechanism. Further arbitrary gates would risk relocating the assumptions. A meaningful next step would identify an independently motivated distinction between a writing input and an idle perturbation, and account for any extra states, rates or resources that distinction needs. No physical observer, energy barrier, thermodynamic cost or origin of the gate law is derived here. Licences follow the repository's [licensing policy](../../LICENSE.md).
