# EHF-RW-005 — Can a boundary history supply the preparation?

30 October 2026. Follow-up to [RW-004](../2026-10-30-detection-access/README.md).

**PROVED in the specified model:** observing an actual spatial crossing 2→0 identifies the post-crossing cycle exactly. This supplies the preparation used by RW-004 through an observed event, without an active cycle setter. **COMPUTATIONAL:** finite-time probabilities, monitoring costs and a less precise snapshot observer. The observer, recording rule, noninvasive detector and clock remain prescribed; this is not a derivation of a physical observer from EHF dynamics.

## Fixed construction and question

Use the same matched five-vertex triads A and C, boundary positions {0,1,2}, hidden positions {3,4}, and classical probe state (v,k) as RW-003/004. Each of two spatial neighbors in the current cycle has rate 1/2. Each other cycle is reached at the same vertex at rate κ/2. The network itself stays fixed.

RW-004's simpler detection protocol actively selected cycle 2 at position 0, waited t=1.7378008287493762, and detected position 2 irrespective of final cycle. Can a boundary observer obtain the same initial information from what it sees, without reading or changing the cycle label?

## Exact crossing as a herald

In both matched triads, boundary edge {0,2} belongs to cycle 2 alone. An actual jump along that edge retains the probe's cycle. Consequently,

    actual observed spatial jump 2→0  =>  post-jump state (0,2).

The conditional distribution is a point mass, independently of the prior state distribution whenever that event occurs. No stationary assumption is needed for this inference. Continuous-time spatial hops and switches are separate events; simultaneous events have probability zero. A finite confirmation delay or an unresolved intervening jump can weaken this inference.

An observer can therefore apply a simple prescribed rule:

1. Monitor the observed boundary link for an actual 2→0 crossing.
2. On that event, start a timer and record that a trial is armed.
3. After the fixed delay t, record whether position detector 2 clicks.
4. Re-arm on the first 2→0 crossing after that measurement. Ignore crossings during the observation interval.

Both the herald and the final detector concern visible boundary positions, not direct access to k. This is passive conditioning on a record, not an operation setting the cycle. It still assumes a detector that resolves a genuine edge crossing, a stable identification of boundary ports and a clock. The record is logically part of the observer protocol; an autonomous physical mechanism storing it has not been constructed.

## Signal recovered from the record

At κ=1 the heralded initial state is exactly RW-004's selected state, so the same prospective measurement probabilities follow:

| Model | Probability of position-2 click after delay t |
| --- | --- |
| A | 0.1805749007 |
| C | 0.1762057978 |

The gap is **0.4369103 percentage points**. The code also checks κ=0.1 and 10 at the same delay. These probabilities are computed, not measured by running random trajectories.

The prior 100,000-trial binomial design remains applicable if accepted trials use the non-overlapping protocol above, the model parameters are fixed and known, and observations do not alter the probe. Each accepted herald is a stopping time at which the full hidden state is the same deterministic state (0,2). The standard strong Markov property then gives the same future outcome distribution independently of the preceding history. Starting the next trial only after the previous observation prevents overlapping trial intervals. Counting all nearby heralds as independent trials would not be justified.

## Monitoring is not free

For κ>0 the finite lifted process is irreducible and symmetric, so its stationary distribution is uniform on 15 states. The only transition producing the herald is (2,2)→(0,2), with rate 1/2. Its stationary flux is therefore

    (1/15) × (1/2) = 1/30.

The mean interval between all repeated herald events is 30 mean-hop-time units. The code independently checks this by solving exact hitting-time equations for the target transition. It removes that one off-diagonal rate while retaining holding rates and solves M h=1 using fractions. Starting immediately after a herald gives h_(0,2)=30 exactly at all three tested positive switching rates. An arbitrary stationary starting time has a different mean wait; these quantities are not equated.

The observer also has an observation dead time t. If P(t) is the transition matrix from (0,2), its mean accepted-trial interval is

    t + sum_x P(t)[x,(0,2)] h_x.

At κ=1 this is approximately **32.2082** under A and **32.1942** under C. Collecting 100,000 accepted outcomes from a stationary start takes approximately **3.22 million model-time units** on average. These are not seconds. They exclude costs of constructing the observer, powering or reading a clock, and physical measurement errors. There is no free external reset, but there is a real waiting cost.

## What if the observer sees only sampled positions?

An actual edge crossing is stronger information than seeing position 2 at time −δ and position 0 at time 0. With coarse snapshots the probe may have taken other routes or switched between observations. We test the weaker record

    X(−δ)=2, X(0)=0,

at stationarity, without reading any cycle label. Its posterior at position 0 is

    q_k = [sum_j P(δ)[(0,k),(2,j)]] / [sum_(l,j) P(δ)[(0,l),(2,j)]].

We then compute the probability of X(t)=2 from this posterior, at the same future delay t. For κ=1:

| Past snapshot separation δ | Probability of the two-snapshot record | Cycle-2 posterior under A | Cycle-2 posterior under C | Conditional future-probability gap (percentage points) |
| --- | --- | --- | --- | --- |
| 0.01 | 0.000331676 | 0.990075 | 0.990071 | 0.430420 |
| 0.1 | 0.00317572 | 0.907198 | 0.906840 | 0.377311 |
| 1 | 0.0222768 | 0.492065 | 0.482865 | 0.135338 |
| 3 | 0.0367672 | 0.348673 | 0.343475 | 0.0277415 |
| 10 | 0.0399943 | 0.333352 | 0.333336 | 0.0000646607 |

Short-separated snapshots approach the pure heralded preparation but their record is rare: its probability behaves as δ/30 at small δ. Widely separated snapshots lose the useful cycle information. The table compares a stationary sampled record, not a guarantee that a detector resolves individual jumps.

### A position-history distinction

For this pair, at the tested rates, boundary position distributions and two-time position transition probabilities agree, as established by RW-003's complete position-transfer checks. In particular the two-snapshot record probabilities above agree between models. Nevertheless,

    Pr[X(−δ)=2, X(0)=0, X(t)=2]

differs. At κ=1 and δ=1 the absolute joint-probability difference is approximately **3.01491×10^−5**. The code checks this independently by both conditioning on the posterior and multiplying transition matrices with position projections.

Thus boundary position histories reveal information that these two-time boundary statistics omit. This is a standard consequence of observing only part of a Markov state: projected position histories can retain information about hidden labels. It is not a new fundamental memory law. No claim is made that overlapping snapshot windows are independent; RW-004's binomial counts cannot simply be applied to those windows without treating correlations and record-acquisition costs.

## Reproduction, validation and attribution

Requires Python 3, NumPy and SciPy. From the repository root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 research/related-work/2026-10-30-history-heralding/probe.py
```

[probe.py](probe.py) imports the retained generators and inputs through RW-004. [results.json](results.json) records the source/dependency/input hashes, triads, exact event-entry probabilities and flux, interval calculations, all snapshot posteriors and three-time joint probabilities. There are no random seeds, fitted parameters or Monte Carlo trials. Checks include exact rational waiting-time equations, independent numerical linear solves, stochastic transition matrices, agreement with RW-004's probabilities and two independent forms of the three-time probability.

The inherited mathematical and physical motivation retains the source credits in RW-002 through RW-004, including Dörfler and Bullo, Pasterski, Pate and Raclariu, and Hoeffding for the earlier sampling bound. Event conditioning, hidden-state filtering and the strong Markov property are standard tools, not EHF inventions. The present work is a model-specific reconstruction and access audit developed with AI assistance; no additional external literature review was performed.

**Potential contribution back:** this extends the matched benchmark with an explicit history-based preparation rule and its monitoring cost. Any outreach should first check the relevant hidden Markov, boundary-observability and event-triggered sampling literature. No novelty claim or researcher contact is warranted yet.

## Assessment

The cycle-specific access need not be a direct cycle setter: an observable boundary crossing can supply it exactly, and finite position histories supply it approximately. This is progress in operationally specifying an observer. It leaves the existence of a physical recording device, timer, noninvasive detector, stable boundary and probe dynamics as assumptions. Deriving those structures from admissible comparison and transformations remains a separate EHF task.
