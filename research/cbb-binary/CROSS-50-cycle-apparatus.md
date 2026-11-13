# EHF-CBB-CROSS-50 — Classical apparatus memory on a grown cycle

**Date** 2026-11-13 (Australia/Brisbane)  
**Status** Explicit classical simulations, an exact distinguishability bound, and a sharp conditional information bound.

## Four disjoint reversal windows

Start with the 21-vertex preparation of [CROSS-49](CROSS-49-route-recorder.md). Insert at zero-based edge 11, 12, or 13. The two carrier moves P and Q now start at 2 and 18, and the route recorder R remains at 6. The insertion opens a fourth LR3 window M at start 12, 11, or 10, respectively. Its support is disjoint from the other three windows. Each subset of the four reversals gives a different indexed, labelled tour. Each of the 32 undirected edges of this 16-state cube is a legal LR3 event. The verifier checks all three constructions. It finds no fourth disjoint move at the other four insertion slots preserving the three-window preparation in CROSS-49.

Write pqr for the first three bits and m for the apparatus bit. The bits are readable by comparing each window with its initial word. All four start at zero. The construction supplies a controller which may read these bits, apply a legal move or no move, and use independent fair random choices. It does not select these control rules from LR3 admissibility.

## One classical recombiner for three protocols

Start with a fair choice of P or Q. A write on the P arm flips R. A write on the Q arm leaves R blank and flips M with probability 1/2. In the write-then-unwrite protocol, read the marker and undo whichever reversal actually occurred. This read-and-act erasure uses no saved writer coin, and is not asserted to be a fixed reversible map on an enlarged state space including that coin.

The second-stage recombiner uses the same rule in every protocol:

- If m=1, switch to the other carrier move.
- If r=1, choose the second carrier move fairly.
- If both records are blank, repeat the first carrier move, as determined by the current p and q.

The first two conditions never hold together on the preparations tested. After recombination, flip M whenever pqr=110. In these protocols that condition holds exactly on the reached states with m=1. This last operation is an involution on the full cube and restores m=0 on the reached outputs. The simulation matches the coherent tables even when the final apparatus bit is read.

| Protocol | Final distribution on pqr | Final m |
|---|---|---:|
| No write | 000 with probability 1 | 0 |
| Write and retain | 000, 001, 110, 111 each with probability 1/4 | 0 |
| Write, then unwrite | 000 with probability 1 | 0 |

The comparison is to the three CROSS-49 protocols with a basis-state recorder initially zero. Its separate plus/minus coherent recorder preparations are outside the simulation. During the Q arm, the route recorder remains blank in both experiments. The apparatus supplies the information that the route recorder lacks.

## How distinguishable must the apparatus states be?

Compare the no-write and retain-write trials, with equal prior probabilities. Let d be the total variation distance between their full classical apparatus distributions on the common Q arm immediately before the second stage. Include any additional state available to that stage. The visible pqr value there is 010 in both trials. Assume fair first moves and one common stochastic recombination kernel, including any cleanup. Write A and B for the probabilities of visible output 000 in the plain and tagged trials, respectively.

Let x be the probability of output 000 from the plain P arm, z the corresponding tagged P-arm probability, and y0, y1 the probabilities on the two Q arms. Then A=(x+y0)/2 and B=(z+y1)/2. A common stochastic kernel implies |y0-y1|<=d. Since x<=1 and z>=0, B>=A-1/2-d/2. If the full visible joint tables each have total variation error at most e from their targets, A>=1-e and B<=1/4+e. Therefore

    e >= max(0, 1/8 - d/4).

For any d between 0 and 1/2 this bound is tight. Encode a binary apparatus decision on the Q arm that repeats Q with probability 3/4+d/2 in the plain run and 3/4-d/2 in the tagged run. The common recombiner follows that bit on the Q arm, always repeats on the plain P arm, and chooses fairly on the tagged P arm. The two Bernoulli apparatus laws have distance d and each visible joint table has error 1/8-d/4. The exact cube simulation attains the zero-error endpoint d=1/2.

## How much setting information is needed?

In an exact fit, A=1 forces x=y0=1 and B=1/4 forces y1<=1/2. On the Q arm, even the single downstream indicator for output 000 therefore carries at least

    h2(1/4) - 1/2 = 0.311278124 bits

about the equally likely write/no-write setting. Here h2 is binary entropy. For y0=1, the least informative allowed output channel has y1=1/2. Any y1 below 1/2 is more informative because its output can be randomized into the y1=1/2 channel while keeping y0=1. By data processing the classical apparatus on that arm must carry at least as much information. See [Polyanskiy and Wu, Information Theory, chapter 3](https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/resources/mit6_441s16_chapter_3/). The M bit of the exact simulation attains the bound. Averaging this conditional requirement over the two fair arms gives 0.155639062 bits of additional apparatus information conditional on the arm. The P arm already carries setting information in the visible route bit and needs no additional apparatus record.

The cycle therefore supports an explicit classical explanation of these three tables once an apparatus reversal can carry setting information to recombination. The finite construction uses a supplied writer, recombiner and random choices. It gives neither an autonomous derivation of those rules nor a simulation of arbitrary coherent preparations. An experiment designed to exclude this explanation needs to audit the full apparatus state at recombination or independently bound the setting information carried on the shared arm.

## Reproduce

Run `python3 research/cbb-binary/cross50_cycle_apparatus.py` from the repository root. The verifier checks the labelled cubes, exact coherent and classical distributions, the common cleanup, and tight error witnesses on a rational grid. The displayed bound is analytic and holds for every d in the stated range. AI assistance was used for construction, verification and writing.
