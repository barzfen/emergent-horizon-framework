# EHF MICRO–OPW 03: autonomous probe-enabled writing, with the reverse active

Date: 2 November 2026. Research direction: Barry Fensom. Implementation and exposition assisted by ChatGPT.

**Result:** the selected reversible probe coupling writes and resets the local structural record, but provides no useful separation between writing and retention times in the six tested parameter combinations. The local readout remains meaningful, but its value is no longer protected when the probe can return. This is a negative result for this specified mechanism, not an impossibility theorem for MICRO–OPW memory.

## Fixed carrier and continuously active interaction

Use the retained seven-vertex fixed colouring: vertices {1,2,3} have type 1 and {0,4,5,6} type 0. The carrier is the same six-state MICRO–OPW23 component used in MICRO–OPW 02, divided into an A component of four states and a B component of two under LR3 alone. All states obey hard cyclic no-isolation and the same Pi label.

The ideal local readout is the number of type-1 neighbours of vertex 0: one in A, zero in B. There is no appended memory bit. The carrier is the actual Hamiltonian cycle.

The joint state is (c,v): a carrier cycle and one probe position at a labelled vertex. There are 6*7=42 states. Dynamics is time-independent:

* Every valid distinct LR3 carrier neighbour is reached at rate eta, leaving probe position unchanged.
* The probe hops to each of its current cycle neighbours at rate 1/2. Total spatial-hop rate is one.
* When the probe traverses edge {0,6} in either direction, simultaneously exchange the adjacent vertex labels 0 and 6 in the carrier, provided the resulting cycle preserves Pi and MICRO. The probe finishes at the named destination vertex.
* The reverse coupled transition has exactly the same rate. There is no shutoff schedule, removal of the probe, one-way latch, feedback or absorbing storage flag.
* Optional leakage adds every valid distinct LR2 carrier transition at rate epsilon, leaving probe position unchanged.

Thus the selected write and its reverse are

    (A=(0,1,2,3,4,5,6), probe at 6)
        <---- rate 1/2 each way ---->
    (B=(0,5,4,3,2,1,6), probe at 0).

The carrier LR3 dynamics continues while the probe moves, waits and returns. The selected coupling changes the probe's future spatial graph; the probe marginal is not stipulated to remain the old fixed-cycle walk. Symmetric joint rates establish Markov detailed balance, not deterministic information preservation or a full thermodynamic microscopic account.

The gate itself remains an imposed interaction law. Distinguished vertices, fixed vertex types, initial carrier, continuous time, rates and ideal readout are supplied. Suppressing ungated LR2 changes at epsilon=0 is an explicit kinetic restriction. The model does not derive why a probe should implement this exchange or why background LR2 would be absent.

## First writing and first erasure

Write time is the mean first arrival in carrier component B from the prepared state (A identity cycle, probe at 6). It includes missed opportunities and subsequent wandering. Erasure time is the mean first exit from B following the actual displayed write, starting at (B,0). These are different conditional preparations, not identical ensembles. They are exact first-passage calculations, not a claim that the first jump must write.

| eta per LR3 edge | epsilon per LR2 edge | Mean first write | Mean first erasure | Erasure/write ratio |
|---:|---:|---:|---:|---:|
| 0.1 | 0 | 13.8044 | 6.8462 | 0.4959 |
| 1 | 0 | 13.6979 | 6.5000 | 0.4745 |
| 10 | 0 | 13.7214 | 6.3548 | 0.4631 |
| 0.1 | 0.01 | 12.4536 | 6.1372 | 0.4928 |
| 1 | 0.01 | 12.5575 | 5.8630 | 0.4669 |
| 10 | 0.01 | 12.6609 | 5.7456 | 0.4538 |

At eta=1 and epsilon=0 the exact means are 1408756/102845 for writing and 13/2 for first erasure. Units are inverse total spatial-hop-rate units, not seconds. No general optimality claim is made for these preparations or parameters.

Immediately after the write, the reverse spatial crossing has rate 1/2. At zero leakage the postwrite total transition rate is 1+eta, giving probability 1/[2(1+eta)] that the very next event is the reverse write. At eta=1 this is 1/4. Faster LR3 motion lowers that immediate next-event fraction but does not improve the mean erasure time in this tested zero-leakage set. A structural move can precede the reversal without eliminating later return access.

## Local retention with no writer shutoff

Compare the written history (B, probe at 0), produced by the actual write, with the matched blank history (identity A, probe at 0). Both continue under the same joint rule. Equal-prior optimal classification from the current local readout is (1+TV)/2, where TV is the difference between the two current B probabilities.

At eta=1, epsilon=0:

| Time | Local classification success | Probability no first erasure yet, given written history | Idle carrier currently B |
|---:|---:|---:|---:|
| 1 | 76.2741% | 67.3655% | 5.0168% |
| 3 | 66.2342% | 43.7944% | 10.8007% |
| 10 | 56.6814% | 20.8823% | 22.1584% |
| 30 | 50.8387% | 4.0179% | 31.7660% |
| 100 | 50.0009% | 0.0137% | 33.3317% |

The idle test starts uniformly over the four A carrier states and seven probe positions. No commanded input is provided; the same interaction remains active. Current B occupancy is not the probability that any accidental write has ever happened, since subsequent erasure can undo it. Likewise, current B occupancy in the written history is not first-erasure survival. A reset followed by a rewrite does not restore an unbroken record of the original event.

The 42-state generator is connected and symmetric for all six tested models. Its stationary law is uniform, with B mass 14/42=1/3. Consequently the two complete joint-state distributions converge to the same law, and all endpoint readouts eventually lose the initial-history distinction. This is a finite-chain conclusion, not an inference from near-chance decimal values alone. The imbalance between four A and two B carrier states is retained explicitly; equilibrium does not give B mass 1/2.

At zero leakage the stationary A-to-B flux is exactly 1/21; with leakage it is 1/21+epsilon/3. This is an event flux, not a Poisson waiting-time assertion. Full-carrier and full-joint distinguishability are also recorded in results.json; a locally unreadable distinction need not already be globally erased.

## What was learned

MICRO–OPW 02's local record survives every LR3-only path in the two selected components. This audit shows that using a returning probe to open the connecting LR2 transition also opens erasure and incidental activation. Structural sector protection has not removed the control problem exposed by Assumption Audit 05.

The mechanism supports repeatable structural transitions and an accessible local carrier value. It does not supply reliable on-demand memory, autonomous recognition of deliberate inputs, a stable write/store distinction or a noise barrier. The label 'deliberate' cannot change a transition when the modelled state is otherwise identical.

**Stopping decision:** retain this as a reproducible negative benchmark and pause this particular reversible gate. More rate sweeps alone would not explain protection. Further work should have an independently specified new ingredient or question, such as a represented interaction with a genuine reason to distinguish writing from background perturbations. This result does not justify silently removing the reverse edge or declaring a protected storage interval by fiat.

## Reproduction and verification

Keep enclosed micro_opw_01, micro_opw_02 and micro_opw_03 as sibling directories. Requires Python 3, NumPy and SciPy.

    python micro_opw_03/probe.py
    python micro_opw_03/verify.py

The main code constructs rates with fractions and checks symmetry, conservation, nonnegative off-diagonal entries, full connectivity, the local record value, exact reverse rates, stationary flux and exact first-passage residual equations. Spectral propagation is checked against direct matrix exponentials; killed generators independently compute first-erasure survival. Observation bounds and stochastic normalization are checked at every retained time.

The independent verifier rebuilds the carrier from undirected edge sets, independently filters the cyclic MICRO condition, identifies the coupled swap from circular LR2 slots, constructs the joint generator, and compares first-passage means and every recorded local/idle probability using floating linear solves and matrix exponentials. All six models passed. No Monte Carlo trajectories were run. Source and reader-input hashes are retained.

This audit uses the original MICRO/OPW definitions and the stored witness from the previous two probes. It uses no theorem from the delta-Ising paper and makes no physical interpretation or novelty claim. No researcher was contacted.
