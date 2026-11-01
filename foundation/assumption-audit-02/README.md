# EHF assumption audit 02: minimum requirements for a record

Date: 1 November 2026. Status: standard finite-state results, self-contained proofs and exact computational checks. No novelty or physical-origin claim.

Research question posed by Barry Fensom; development, code and exposition assisted by ChatGPT. Follow-up to [Audit 01](../assumption-audit-01/README.md), which distinguished structural roles from persistent records.

## 1. What is supplied, and what is measured?

We assume a finite classical state space S; an initially encoded bit B with equal prior probabilities; conditional state distributions mu_0 and mu_1; and update rules independent of B except through the encoded state. We explicitly supply an observation map g, an observation time t, and a decoder. These are model inputs, not an emergent observer or clock.

For row-stochastic update matrix K and a fixed observation map g, the two observation laws are nu_b(t)=g_*(mu_b K^t). Define accessible distinguishability by total variation:

\[
D_g(t)=\frac12\sum_y|\nu_0(t,y)-\nu_1(t,y)|.
\]

With one observation, equal priors, known model and known t, the best possible classification success is (1+D_g(t))/2. **Proof:** at each y choose whichever conditional probability is larger; summing half their maximum gives the expression. D=0 means chance performance, D=1 perfect recovery. Unequal priors, limited decoders and noisy detectors change the operational question.

For this audit a record meets a chosen retention requirement when its specified readout stays above a stated success threshold over the required interval. We use 75% as an illustrative threshold, not a privileged definition of memory. This is a retained initial encoding, not yet a mechanism that acquires an external signal.

## 2. Exact preservation, hiding and loss

**Proposition A: data processing.** For any common stochastic update K,

\[
D(\mu_0K,\mu_1K)\leq D(\mu_0,\mu_1).
\]

**Proof:** write delta=mu_0-mu_1 and use

\[
\frac12\sum_y\left|\sum_x\delta(x)K(x,y)\right|
\leq\frac12\sum_x|\delta(x)|\sum_yK(x,y)=D(\mu_0,\mu_1).
\]

An observation map is another stochastic map, so D_g(t)<=D_full(t). A deterministic bijection preserves full-state D exactly by permuting its summands.

Consequences:

- If two full conditional state laws become identical, subsequent common updates cannot separate them. Recovery would need extra information correlated with B, or access to a larger state than this model retained.
- Equal **observed** laws at one time do not imply equal full laws. A hidden distinction may become observable later. D_g(t) need not decrease even though D_full(t) does.
- Noninvertibility alone does not erase every encoding. The map (a,b)->(a,0) discards b but preserves an encoded a forever.

**Explicit controls.** Encode B as (B,0) and observe only the first bit. Under reversible swap (a,b)->(b,a), full distinguishability remains 1, but first-bit distinguishability alternates 1,0,1,0. Under (a,b)->(0,a), the distinction transfers to the second bit at step 1 and disappears from the entire four-state model at step 2. Under (a,b)->(0,b), it disappears at step 1. A physical implementation could transfer information to an unmodelled environment: these maps are not thermodynamic erasure claims.

No measurement history is supplied to these endpoint observers. Providing a stored history enlarges their available state and requires its own retention mechanism. We do not count the original t=0 reading as evidence of a dynamically generated memory.

## 3. Preserved information need not be a fixed autonomous record

Let F:S->S be deterministic and let r:S->{0,1} be a fixed readout. Call r an invariant readout if r(F(x))=r(x) for every x. This deliberately strong requirement uses no elapsed-time-dependent decoding and imposes invariance throughout S.

Construct the undirected graph whose edges join x to F(x), ignoring self-loops. If it has c connected components:

**Proposition B.** There are exactly 2^c invariant binary readouts, including the two constant readouts. Two encoded states can be separated by such a readout if and only if they belong to different components.

**Proof:** the invariance equation makes the readout equal at both ends of every edge, hence constant on each component. Conversely, assigning any bit independently to each component satisfies the equation. For deterministic finite dynamics, each component has one attractor cycle. Its component label is conserved, but an internal device able to read that label is not supplied by this theorem.

**Counterexample to a common shortcut:** the cyclic permutation 0->1->2->3->0 is fully reversible and retains every initial-state distinction at each known time. Yet it has only one component and no nonconstant invariant readout. Recovering a chosen initial bit from its state can require knowledge of the step count. Merely preserving distinctions does not produce an accessible, unchanged record. Adding a clock or extra record changes S and must be accounted for.

This criterion concerns globally invariant readouts for deterministic F. Approximate records, restricted observation maps, finite horizons, stochastic dynamics and restricted sets of reachable states require their own criteria; the component count is not a universal theorem about all forms of memory.

## 4. Noise and protection: an exact benchmark

For p=1/10, each physical bit flips independently at each discrete step. Compare (i) one bit, (ii) three bits initially encoded as 000/111 with majority decoding only at the final time, and (iii) the same three bits with ideal majority restoration after every noise step. This is a standard classical repetition-code benchmark, not a proposed EHF mechanism; see the source acknowledgement below.

Set a_t=(1-2p)^t. Exact distinguishabilities are:

\[
D_1(t)=a_t,\qquad D_{3,\mathrm{passive}}(t)=\frac{3a_t-a_t^3}{2}.
\]

For one bit, the probability of an odd number of flips is q_t=(1-a_t)/2. In the passive three-bit model the bits remain independent conditional on B; majority fails with probability 3q_t^2-2q_t^3, giving the second formula. Majority is an optimal endpoint decoder for these symmetric conditional distributions.

With perfect restoration after each noise step, the entire codeword flips logically with probability r=3p^2-2p^3=0.028 per step. Thus

\[
D_{3,\mathrm{corrected}}(t)=(1-2r)^t.
\]

The program independently builds the full 2-state and 8-state transition matrices and evolves both conditional distributions with rational arithmetic, checking these formulas at every t=0,...,30. These are exact probability calculations, not Monte Carlo estimates or physical trials.

| Observation time | One bit: success | Three bits, final majority | Three bits, restoration each step |
| --- | ---: | ---: | ---: |
| 1 | 90.00% | 97.20% | 97.20% |
| 5 | 66.38% | 73.70% | 87.48% |
| 10 | 55.37% | 58.02% | 78.10% |
| 20 | 50.58% | 50.86% | 65.79% |

The last integer steps with success >=75% are respectively **3, 4 and 12**. These are model steps under a shared noise schedule, not equal hardware, energy or computation budgets. Three bits already cost more than one; active restoration adds still more assumptions. For these fixed-size models and 0<p<1/2, all three distinguishabilities tend to zero. Correction extends finite retention but does not make this finite noisy memory permanent.

**What protection assumes:** a known encoding, distinguishable bit locations, independent bit-flip noise, simultaneous step boundaries, a perfect majority operation and a way to rewrite the three bits. No noise, resource or runtime cost is assigned to correction. No local asynchronous implementation has been constructed. The restoration rule is many-to-one and its physical implementation is outside this model. This audit does not establish protected memory from bare comparison rules.

**Change the error assumption and the conclusion changes.** If at most one physical bit flips between ideal restorations, every allowed error is corrected forever. With independent errors, two or three flips have positive probability and logical failures remain. The code checks all eight codeword/zero-or-one-flip cases. The bounded-error guarantee depends on the restriction on errors; it must not be substituted for a result under unrestricted noise.

## 5. What was actually executed?

Run Python 3.10+ with no external packages:

```sh
python3 foundation/assumption-audit-02/probe.py
```

- Every deterministic map on one through four states: **288 maps**, including 33 bijections. For each, enumerate all binary readouts and check the 2^c criterion exactly. Across 1,621 distinct encoded pairs, check the invariant-readout separation criterion, permanence of merging and preservation under bijections. Trajectories are checked through n^2 steps; the general conclusions follow from the proofs, not a finite horizon.
- **225 stochastic kernels**: every two- and three-state kernel whose row entries have denominator 2. Check data processing for all 3,267 unordered pairs of distinct denominator-2 input laws, and check all 26,028 associated binary observation cases.
- Exact full-matrix noisy evolution for all three benchmarks through step 30; compare with the closed formulas and verify majority attains full-state endpoint distinguishability in the three-bit examples.
- Explicit transfer, erasure, clock-dependent decoding and irreversible-retention controls; all bounded single-error correction cases.

All assertions passed. [Code](probe.py) and [full output](results.json) accompany this note. Finite exhaustive checks are implementation evidence within the stated ranges; the self-contained proofs establish the general mathematical statements.

## 6. What this says about EHF

An initially distinguishable pair is insufficient for an accessible persistent record. The update must retain the relevant distinction over the desired time, the permitted readout must expose it, and any robustness mechanism must work under a specified perturbation model. A static structural role from Audit 01 does not settle any of these requirements.

Conversely, global reversibility is not necessary for retaining a particular encoded bit, and global reversibility alone does not provide a fixed readout. Protected records can be conserved sectors, time-dependent encodings or actively restored encodings, with different assumptions in each case.

Next targeted EHF question: for a specified Hamiltonian-triad transition rule, can a permitted boundary event write a locally readable state that retains information under those same transitions? Start with the event and accessible record already identified in the history-heralding work, but include the recording state in the dynamics. Require it to be written by the event rather than selected initially. List any new update, noise, reset and timing assumptions. This audit has not yet built that device or derived an observer, a clock, physical space or the origin of laws.

## Sources, attribution and potential contribution back

These are standard classical probability, deterministic-dynamics and error-correction arguments. No novelty or priority claim is made; no outside code or datasets are reproduced.

- **IBM Quantum Learning, “Repetition codes,” classical encoding/decoding and binary symmetric channel sections**, [official source](https://quantum.cloud.ibm.com/learning/en/courses/foundations-of-quantum-error-correction/correcting-quantum-errors/repetition-codes), accessed 1 November 2026. Those sections were read. The 000/111 encoding, majority decoding and 3p^2-2p^3 error probability are established methods; our repeated-step calculation is an elementary application, not a new code. We use only the classical example and claim no quantum-memory result.
- **David A. Levin and Yuval Peres, with contributions by Elizabeth L. Wilmer, _Markov Chains and Mixing Times_, second edition**, [authors' book page](https://pages.uoregon.edu/dlevin/MARKOV/). Background reference for finite Markov chains and total variation. The landing page was accessed; the linked PDF timed out and was not read in this audit. The specific inequalities used here are proved explicitly above rather than represented as verified quotations from the book.

There is currently no novel result ready to return to external researchers. The useful contribution is an explicit accounting framework for our EHF probes. Any outreach or novelty claim requires further checking. Licences follow the repository's [licensing policy](../../LICENSE.md).
