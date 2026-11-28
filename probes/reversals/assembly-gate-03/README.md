# EHF-REV-03: interrupted assembly gate and the clock audit

5 November 2026 (Australia/Brisbane). Research direction: Barry Fensom; implementation and analysis assisted by ChatGPT.

**Result:** an explicitly added finite-state gate generates a length-dependent completion probability. It gives a smooth suppression hierarchy, not a special LR2/LR3 band. Its effective Markov rates are exact in an idle-time trace, while the cycle-only process in real time retains hidden gate memory. The gate still performs an atomic reversal at completion, so this is not a fully local implementation of a longer reversal.

## What is added to the existing construction

Reuse the independently checked 96-state MICRO/Pi component from [REV-02](../rare-channel-02/README.md). It has 48 support-2 edges, 112 support-3 edges and 88 support-4 edges. Support is the smaller of the two complementary segment lengths. The carrier and its endpoint legality are supplied inputs, not derived by this gate.

For each directed distinct-edge channel c->d, attach k=l-1 progress states, where l is its minimal support. One controller is either idle at c or attempting one channel. From idle, each outgoing channel launches at rate a. While busy, the controller advances to the next vertex of a selected contiguous arc at rate u, or aborts back to idle c at rate delta. After k advances it commits the reversal and becomes idle at d.

The construction has 96 idle states, 496 directed attempt channels and 1,168 total states. The stored channel records give source, target, arc start, progress length and auxiliary-state offset. Every scan step follows an existing edge of the frozen source cycle.

The cycle itself stays c throughout an attempt. There are no partial permutations. An abort resets the auxiliary gate; completion changes c to d atomically. Initiation, uniform local rates, interruption, directed progress, exclusive controller access, endpoint eligibility and the final commit are new assumptions. This probe does not model their physical origin, thermodynamic cost, or a local realization of the atomic commit.

## A structural obstruction before any rate calculation

Of the 88 support-4 edges, **76 connect different LR2/LR3 components**. A sequence consisting entirely of MICRO-valid, Pi-preserving LR2/LR3 transitions stays inside its original component. Therefore none of those 76 transitions can be implemented solely as such a sequence.

This is an elementary graph obstruction. A proposed microscopic implementation must change some assumption or enlarge the state space. The present model enlarges it with progress states and supplies a new final transition; it does not evade the obstruction using the old moves alone.

## Exact single-attempt calculation

Let

\[
p=\frac{u}{u+\delta}.
\]

Success requires k=l-1 advances before the first abort. Hence

\[
s_l=p^{l-1},\qquad
b_l=\frac{1-p^{l-1}}{\delta}\quad(\delta>0),
\]

where b_l is the mean busy duration of an attempt. When delta=0, every attempt succeeds and b_l=(l-1)/u.

| u | delta | Support-2 success | Support-3 success | Support-4 success |
|---:|---:|---:|---:|---:|
| 1 | 0 | 1 | 1 | 1 |
| 1 | 1 | 1/2 | 1/4 | 1/8 |
| 1 | 9 | 1/10 | 1/100 | 1/1,000 |

No per-length success factor was entered directly; it follows from the added uniform advance/abort rule and the assumed number of progress steps. However, that number of steps and those rules are modelling inputs. Longer moves still have positive completion probability whenever u>0 and delta is finite.

### No automatic LR2/LR3 plateau

The trace rates satisfy

\[
\frac{q_3}{q_2}=\frac{q_4}{q_3}=p.
\]

If LR2 and LR3 have exactly equal rates in this uniform gate, p=1 and LR4 has that same rate. Suppressing LR4 also suppresses LR3 relative to LR2. Thus this mechanism does not reproduce REV-02's equal short-edge rates with a separate LR4 penalty without another assumption.

## Two clocks give different descriptions

### Idle-time trace

Delete every busy interval from the clock. Failed attempts return to c without consuming idle time. The exact trace process on idle cycle states is Markov with distinct-edge rate

\[
q_{cd}^{\mathrm{trace}}=a s_l.
\]

The code independently computes this by eliminating all progress states using the stochastic complement of the full generator. These rates are symmetric and their stationary distribution is uniform on the 96 idle states.

### Real time

Retain the duration of scans and aborted attempts. Observe idle c and all gates launched from c as the same visible cycle c until commit. This projection is not strongly lumpable: an idle state has no immediate visible-cycle jump, whereas the final progress state has a completion transition at rate u. The same observed cycle can therefore have different immediate futures depending on hidden progress.

Define

\[
H_c=1+a\sum_{d\sim c}b_{l(c,d)}.
\]

The stationary visible-cycle distribution in real time is exactly

\[
\pi_c^{\mathrm{visible}}=\frac{H_c}{\sum_z H_z}.
\]

It is generally not uniform, because attempt occupancy varies across cycles. The stationary fraction of time the controller is idle is 96/sum(H). Thus the symmetric trace generator is not an exact real-time replacement obtained by simply forgetting the controller.

For u=delta=a=1:

- idle-time trace probability of two domain walls: 13/24, approximately 0.54167;
- stationary real-time visible probability of two walls: approximately 0.60408;
- stationary idle fraction: approximately 0.20601.

These changes are residence-time effects of the supplied controller, not a newly selected physical equilibrium measure. As a approaches zero at fixed u and delta, the busy fraction tends to zero and the real-time distribution approaches the uniform trace distribution.

## First-exit audit

Start uniformly over the 52 idle two-wall states; this is an initialization assumption, not a represented writing protocol. Exit occurs at the first committed change to a four-wall state. Scanning still counts as the source cycle.

| u | delta | a | Mean first-exit idle time | Mean first-exit real time |
|---:|---:|---:|---:|---:|
| 1 | 0 | 1 | 2.24105 | 30.30649 |
| 1 | 1 | 1 | 17.04701 | 91.39109 |
| 1 | 9 | 1 | 1,990.38949 | 3,261.17166 |
| 1 | 1 | 0.001 | 17,047.01247 | 17,121.35655 |

The two clocks agree relatively well only when busy periods occupy little time. Times are model units; the rows vary explicit controller parameters and do not constitute a physical lifetime prediction.

If K is the killed positive trace generator on the two-wall idle states, the exact backward equations are

\[
K h^{\mathrm{idle}}=\mathbf 1,
\qquad K h^{\mathrm{real}}=H.
\]

The full 1,168-state real-time first-exit solve agrees with this separately derived recurrence. An exact rational check at u=delta=a=1 gives mean real first-exit time

\[
\frac{3781703095533}{41379342355}\approx91.39109.
\]

## Reproduction and independent checks

Requires Python 3, NumPy and SciPy; the retained [REV-02 results](../rare-channel-02/results.json) must remain at their relative path.

    python probe.py
    python verify.py

[probe.py](probe.py) reconstructs support classes from reversals on the retained carrier and builds the expanded generator. It checks generator row sums, stationary residuals, exact-formula stationary occupancy, numerical elimination to the idle-time generator, killed-generator residuals and the two first-exit recurrences. [results.json](results.json) retains all 496 arc/gate records, all twelve parameter settings, outputs and source hashes.

[verify.py](verify.py) imports no probe code. It checks every scan's adjacency and final target by two-edge reconnection; independently reconstructs the short-component obstruction; solves the single-gate success and duration equations exactly in rational arithmetic for 36 cases; and checks stationary occupancy and first-exit recurrences for all twelve parameter settings. It also solves one whole-carrier real-time recurrence exactly over the rationals. [independent-checks.json](independent-checks.json) records the results and hashes.

The parent carrier has the independent reconstruction described in REV-02. This probe reuses that carrier, rather than claiming another exhaustive audit of all colourings. Expanded-generator dynamics are numerical except for the explicitly identified rational calculations. No external novelty audit was conducted.

## Consequence for the programme

A uniform interrupted gate can turn support size into a probability hierarchy. It does not derive the gate from HC/MICRO, select LR3, or locally realize a forbidden short-component crossing. It also shows why the controller and its clock cannot be omitted without changing the model.

The next implementation question is whether auxiliary local states and reversible or otherwise accounted-for transitions can realize an actual longer rearrangement, with endpoint legality and intermediate admissibility specified. The graph obstruction and the clock audit are conditions such a proposal must satisfy; another assigned suppression factor would not answer them.
