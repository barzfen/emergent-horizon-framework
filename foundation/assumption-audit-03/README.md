# EHF assumption audit 03: can a boundary crossing write a record?

Date: 1 November 2026. Status: an explicitly added recording mechanism in the fixed classical Hamiltonian-triad probe; elementary proofs, exact rate checks and numerical finite-time calculations. No emergent-observer or novelty claim.

Research direction: Barry Fensom. Model development, implementation and exposition assisted by ChatGPT. Follows [Audit 02](../assumption-audit-02/README.md) and uses the two matched triads from [RW-005: history heralding](../../research/related-work/2026-10-30-history-heralding/README.md).

## 1. The actual advance, and its boundary

We now include a one-bit register in the Markov state and give an observed crossing an explicit rule for writing it. All acquisition runs start with the register blank; we do not start those runs by choosing the desired stored bit.

This constructs an operational event recorder in the toy model. The register, its two states, boundary placement, directional coupling, initialization, stability and readout are still supplied. None has been derived from the bare comparison relation or from the existing probe motion alone. The Hamiltonian cycles themselves remain fixed; they do not store the new record by rearranging.

## 2. Inherited probe and new recording rule

The state of the original probe is x=(v,k), with five positions and three cycle labels. Each spatial neighbor within the current cycle is reached at rate 1/2. At a fixed vertex, each other cycle is reached at rate kappa/2. Our time unit is the inverse total spatial-hop rate; these are not seconds.

The matched triads, with each list closed back to its beginning, are:

| Cycle | A | C |
| --- | --- | --- |
| 0 | 0,1,2,3,4 | 0,1,2,3,4 |
| 1 | 0,1,2,3,4 | 0,1,2,4,3 |
| 2 | 0,2,4,1,3 | 0,2,3,1,4 |

Every cycle visits all five vertices; no edge belongs to all three. Edge {0,2} belongs only to cycle 2 in both triads. The inherited directed herald is an actual spatial jump 2->0, which therefore has full-state source x=(2,2) and destination y=(0,2). Its rate is 1/2.

Add register m in {0,1}, anchored to the accessible boundary. On every probe jump x->y, use exactly its inherited rate and update

\[
m' = \begin{cases}1,&\text{if the jump is }2\to0,\\m,&\text{otherwise.}\end{cases}
\]

The rate does not depend on m. Register noise, when included, consists of independent transitions 0->1 and 1->0, each at rate epsilon. The full process has 30 states. We use a row-generator convention and transition matrix exp(tQ).

**Exact marginal check:** summing joint jump rates over destination register values reproduces every original probe jump rate for every joint source state. Thus the probe marginal is unchanged by this stipulated coupling. That mathematical lack of feedback is an assumption, not a demonstration that a physical detector costs nothing.

**Event-driven writing:** (2,2,0)->(0,2,1) occurs at rate 1/2; the corresponding transition ending in register 0 has rate zero. There is no external intervention at the moment of writing and no sampled-time detector in this writer. Directional detection has been encoded directly into the transition rule. Continuous-time transition rates and later externally timed readout remain assumed.

## 3. Acquisition from a blank register

For the noiseless writer, a pathwise induction proves

\[
m(t)=1\quad\Longleftrightarrow\quad
\text{at least one herald occurred since initialization.}
\]

Initially both sides are false. A herald makes both true; no other allowed transition changes either side. Hence this latch stores a correct one-bit history for arbitrarily long times **under the ideal rule that forbids register errors and resets**. That stability is built into the enlarged dynamics.

For finite-time acquisition, initialize the probe uniformly over its 15 states and m=0. We compute event occurrence independently using a killed 15-state generator T: remove the herald off-diagonal rate but keep the original diagonal. Missing probability is the probability that a herald has occurred. Therefore

\[
\Pr(m(t)=1)=1-\pi e^{tT}\mathbf1
\]

in the ideal case, where pi is the initial uniform row distribution. No Poisson assumption about repeated crossings is used. The stationary herald flux is exactly (1/15)(1/2)=1/30; event intervals are not asserted to be independent exponential variables.

For triad A, kappa=1:

| Time since blank initialization | Probability at least one herald occurred | Ideal register reads 1 |
| --- | ---: | ---: |
| 10 | 27.9451% | 27.9451% |
| 30 | 62.5338% | 62.5338% |
| 100 | 96.2020% | 96.2020% |

To check correctness with noise, the validation calculation appends a ground-truth flag h recording whether any herald occurred. This 60-state calculation does **not** grant the tested observer access to h. It independently checks false positives and false negatives. The flag is bookkeeping for the audit, not a noiseless component proposed for the device.

At epsilon=0.01, triad A and kappa=1:

| Time | False positive, conditional on no herald | False negative, conditional on at least one herald |
| --- | ---: | ---: |
| 10 | 9.0635% | 4.4257% |
| 30 | 22.5594% | 10.5669% |
| 100 | 43.2332% | 17.9022% |

These conditional errors have different denominators; neither is the unconditional error rate. The false-positive expression is exactly (1-exp(-2 epsilon t))/2 because, conditional on no herald, the register is an independent symmetric noisy bit. Repeated heralds can refresh the register and reduce false negatives. Noise rates are per model-time unit, not per-step flip probabilities from Audit 02.

## 4. Remembering 'ever' differs from remembering one earlier event

A separate retention question compares two histories at time zero:

- **Written history:** the actual herald has just taken a blank register to m=1 and left the probe at (0,2).
- **Blank history:** the register is still blank and the probe is at that same state (0,2), without that preceding herald.

These are deliberately matched current probe states. They are controlled conditional preparations, not two random samples taken from a stationary ensemble. The first register value is justified by the writing transition above; acquisition itself was tested from blank states. No resetting is performed during either subsequent evolution.

Both histories then evolve under exactly the same enlarged dynamics, with future writing still enabled. A later herald writes 1 in both histories and removes their contrast. Let tau be the time of the next herald, starting from probe state (0,2). For symmetric register noise rate epsilon, we obtain the exact formula

\[
D_{\mathrm{register}}(t)=D_{\mathrm{full}}(t)
=e^{-2\epsilon t}\Pr(\tau>t).
\]

**Proof:** write d_x(t) as the probability of joint state (x,1) in the written history minus its probability in the blank history. Probe marginals agree, so the difference at (x,0) is -d_x(t). On the herald, register resetting removes the difference; elsewhere it transports with the probe. Independent symmetric register noise contributes -2 epsilon d_x. Therefore d(t)=exp(-2 epsilon t) e_(0,2) exp(tT), with all entries nonnegative. Summing gives the formula. The sign structure also proves that observing m alone attains the full joint-state total variation for this particular pair of preparations.

The initial bit is one in both cases eventually under the ideal writer; **saturation loses the identity of the earlier history even though the 'ever since initialization' statement remains true**. At positive kappa these finite probe chains are irreducible, so the next herald occurs almost surely and the contrast tends to zero, even at epsilon=0.

For triad A, kappa=1, equal-prior classification success (1+D)/2 is:

| Time after the selected event | Ideal register | Register noise epsilon=0.01 |
| --- | ---: | ---: |
| 10 | 85.3422% | 78.9358% |
| 30 | 68.3769% | 60.0854% |
| 100 | 51.8629% | 50.2521% |

These are calculated probabilities, not trajectory trials. They concern distinguishing a past event from a matched blank history, not distinguishing network A from C. Numerical results for C are retained separately; we make no new A-versus-C detection claim.

## 5. Controls exposing the assumptions

**Remove the writer coupling.** Keep the probe motion and register, initialize m=0, permit no register noise and leave m unchanged on every hop. Then m remains 0 along every trajectory, including herald crossings. No event recording arises simply from adding an uncoupled bit. A register with other interactions might record indirectly; that broader possibility is not excluded.

**Replace the latch with a reversible toggle.** Toggle m on either direction of crossing edge {0,2}. The resulting 30-state generator is symmetric: each joint transition has a reverse transition at the same rate. The path 2->0->2 changes m as 0->1->0. The register stores crossing parity, not whether any crossing ever occurred. The latch instead gives 0->1->1. This control monitors the undirected edge rather than the directed herald, a distinction we state explicitly. It shows the difference between reversible event coupling and a monotone 'ever' latch; it is not a theorem that every persistent record must be irreversible.

**Do not hide initialization or reuse.** A blank register must be supplied at the start. The latch can store only this one 'ever' bit. Resetting it for repeated independent trials, distinguishing multiple events, storing their order, and starting a timer all need additional state or rules. No free reusable observer follows from this one-shot recorder.

## 6. Executed checks and reproducibility

Requires Python 3.10+, NumPy and SciPy:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 foundation/assumption-audit-03/probe.py
```

The standalone script includes the two triads and checks them against RW-005's result file when it is present; it records that file's hash. It does not import the earlier analysis chain. The output records software versions and its own source hash.

Checks include valid triads and unique herald membership; exact rational row sums, nonnegative jump rates and probe-marginal preservation at kappa=0.1,1,10; a numerical mean next-herald wait of 30 from the post-event state (the earlier RW-005 audit establishes that wait exactly); stochastic matrix exponentials; and independent 15-, 30- and 60-state formulations.

The time scans use **kappa=1 only**, both triads, epsilon=0 and 0.01, and times 0,1,3,10,30,100. They check the acquisition identity, the analytic conditional false-positive expression and the exact retention formula to absolute tolerance 4e-12. The uncoupled and reversible-toggle controls also pass. Computed finite-time values use floating-point matrix exponentials, not exact rational exponentiation; proofs and rate checks are identified separately. All assertions passed.

See [probe.py](probe.py) and [results.json](results.json).

## Interpretation, attribution and contribution back

The useful result is a fully specified event-writing process with a precise limit: ideal persistence of an 'ever' flag does not imply persistent distinguishability of individual histories. We can now point to the exact additions responsible for writing, stability and failure. This does not derive an observer from admissible comparison, establish thermodynamic costs or solve the original framework's foundation problem.

The inherited triads, event inference and model provenance are credited to the EHF RW-003 through RW-005 investigations and their cited sources. Finite-state Markov generators, killed-process survival, total variation and latch/toggle operations are standard tools, not claimed EHF inventions. The self-contained proofs are elementary applications. NumPy and SciPy provide numerical arrays, linear solves and matrix exponentials, with versions recorded. No external code or paper text is reproduced and no fresh literature-priority review was performed.

**Potential contribution back:** no result ready for novelty-based outreach. This is an assumption audit of our toy model. The next substantive task is to ask whether an allowed network reconfiguration can supply a writable, readable record without appending a protected bit and its special coupling. If such a mechanism needs new rules, those must remain explicit. Licences follow the repository's [licensing policy](../../LICENSE.md).
