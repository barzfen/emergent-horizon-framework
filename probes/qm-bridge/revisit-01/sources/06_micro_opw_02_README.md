# EHF MICRO–OPW 02: a local reader for a constrained component distinction

Date: 2 November 2026. Research direction: Barry Fensom. Implementation and analysis assisted by ChatGPT.

**Status:** exact enumeration and rational probability calculations for one retained seven-vertex example, with an independent edge-set verification. No physical-observer or novelty claim. No random trials were conducted.

## Result

The two MICRO–OPW3 components joined by the retained LR2 witness can be distinguished through the bit types of the two neighbours of one specified vertex. The distinction is invariant throughout each component, so it survives every allowed LR3 path there. Full-cycle access and neighbour identities are unnecessary for this particular readout. Access to the specified reference vertex remains necessary for the stated protocol.

## Unchanged input and scope

Use the fixed assignment bit=1 on vertices {1,2,3}, bit=0 on {0,4,5,6}. Cycles are undirected Hamilton cycles on seven labelled vertices, modulo rotation/reflection with canonical anchor 0. Allowed structural moves are circular LR3 reversals preserving Pi and the hard cyclic MICRO no-isolation condition. No bit flips, growth or LR2 leakage is included during storage/readout. See the enclosed MICRO–OPW 01 report for the original full census.

Retain the original witness without searching for a replacement:

    A = (0,1,2,3,4,5,6)
    B = (0,5,4,3,2,1,6)

They have the same Pi even-position set {0,2,4,6}, are joined by the LR2 swap of adjacent vertices 6 and 0 in A, and belong to different MICRO–OPW3 components. The A component has four states and the B component two. They are inside the same six-state MICRO–OPW23 component. All six states have available LR3 moves. The allowed state spaces, vertex types and Pi definition are imposed assumptions.

## Complete state audit

| Component | Canonical cycle | Neighbours of vertex 0 | Number of type-1 neighbours of 0 |
|---|---|---|---:|
| A | 0,1,2,3,4,5,6 | 1,6 | 1 |
| A | 0,1,2,3,6,5,4 | 1,4 | 1 |
| A | 0,3,2,1,4,5,6 | 3,6 | 1 |
| A | 0,3,2,1,6,5,4 | 3,4 | 1 |
| B | 0,5,4,1,2,3,6 | 5,6 | 0 |
| B | 0,5,4,3,2,1,6 | 5,6 | 0 |

Thus a fixed readout r(c)=number of type-1 neighbours of vertex 0 separates these components with certainty under ideal simultaneous local access. It is constant on each component, not only different in the initial A/B cycles. This conclusion needs neither an equilibrium distribution nor a clock nor a chosen structural transition rate. It is not a theorem that this readout is globally conserved across all 72 valid states or under LR2/growth/noise.

## Comparison of readers

Equal-prior success below concerns distinguishing the two component hypotheses. Where specified, states are uniform within their respective components; uniformity is the stationary law for a symmetric equal-per-edge continuous-time structural walk, not for every possible walk.

| Reader | Success | Qualification |
|---|---:|---|
| Binary necklace, ignoring starting point and orientation | 50% | Same pattern for every state |
| Histogram of local type-1 neighbour counts, without vertex identities | 50% | Same histogram for every state |
| Presence of just edge {0,1} | 75% | Uniform-within-component assumption; fluctuates inside A |
| Complete neighbour-label set at vertex 0 | 100% | Ideal local access; pointwise separation |
| Number of type-1 neighbours at vertex 0 | 100% | Ideal local access; pointwise separation; no neighbour identities needed |

Both components have the same unanchored binary necklace: one run of four zeros and one run of three ones. Their unanchored local count histogram is also identical: two vertices see zero type-1 neighbours, four see one, and one sees two. Consequently, sampling an unidentified uniformly random vertex and reading this count cannot distinguish the components. An anchor-relative local observation is stronger access than an unanchored bit pattern. Canonicalization choosing label 0 does not itself construct a physical port or an observer able to find it.

## A weaker operational reader: one spatial hop

Prepare a probe at vertex 0, give each of its current two cycle neighbours jump rate 1/2, and observe only whether its first spatial hop ends on bit type 1. The probe does not need to identify the destination vertex. During the waiting interval, let the cycle continue all its MICRO–OPW3 moves, at rate eta per distinct LR3 edge. Structural moves leave the probe at vertex 0 until the spatial hop. No backreaction of the probe on structural motion is imposed in this reader.

For every carrier state in A, one of the two outgoing spatial transitions goes to type 1; in B, neither does. The total spatial-hop rate is always one. Therefore, for any within-component starting state or mixture:

    P(type-1 first hop | A) = 1/2
    P(type-1 first hop | B) = 0.

These are exact probabilities with ongoing rearrangements, not results obtained by freezing the carrier. The pointwise constant exit fractions prove the assertion for all eta>=0 (and more general within-component dynamics satisfying the stated hop rule). Independent rational first-jump absorption equations (I+eta*L)h=q confirm it at eta=0,1/10,1,10 from every state in both components. Equal first-hop rates and unchanged vertex types are supplied rules.

One binary outcome gives optimal equal-prior classification success 3/4. A type-1 arrival certifies A in this ideal model, whereas a type-0 arrival is ambiguous.

For m fresh preparations at the same port with fresh random hop choices and no component-changing moves, use the rule: report A if any type-1 arrival occurs, otherwise report B. Then:

    P(error | A) = 2^(-m)
    P(error | B) = 0
    equal-prior success = 1 - 2^(-m-1).

At m=5, error under A is 1/32=3.125%, error under B is zero, and equal-prior success is 63/64=98.4375%. These are prospective design calculations, not measured trials. Re-preparing a probe at vertex 0, detecting its first jump, resetting a counter and knowing the bit type at arrival are assumptions. Correlated structural states do not invalidate this stated protocol because its conditional hop probability is the same at every state in each component; arbitrary unreset observations along one probe trajectory are not this protocol. The jump count replaces an externally chosen observation time but does not derive the detector, reset mechanism or trial counter. Reset/travel costs are not calculated.

## Bounded secondary check

For the same fixed colouring, all 27 MICRO–OPW3 components give 351 unordered component pairs. For 333 pairs, there is at least one vertex whose possible type-1-neighbour-count values in the two components are disjoint. The independent edge-set checker reproduces this count.

This is a pair-specific access census: it does not supply one universal location/readout distinguishing all components, does not say that all these pairs share Pi or have an LR2 connection, and does not alter the preselected A/B example. Eighteen pairs fail this particular perfect single-vertex-count criterion; that is not a proof of indistinguishability under other observations. The primary result is the retained A/B witness.

## What this resolves and what remains

MICRO–OPW 01 found a component distinction that LR2 could change. This audit establishes that the distinction is locally readable for the chosen pair, rather than merely a global label accessible to an omniscient reader. It also corrects a tempting weak reader: the single edge {0,1} changes within the A component, so its initial value is not itself a perfectly stable record. The two-neighbour bit count is stable throughout the component.

The result supplies a candidate carrier and readout for ideal storage under a specified move class. It has not supplied autonomous writing, a represented LR2 gate, a mechanism suppressing accidental LR2 events, noise tolerance, finite leakage lifetimes, readout backreaction, growth robustness or a physical observer. A writer restricted to LR3 still cannot change this component label; enabling LR2 can also enable erasure. The next substantive step would represent the enabling interaction and test it while keeping both writing and accidental reversal active, as required by the lessons of Assumption Audit 05.

## Reproduction and provenance

Keep enclosed micro_opw_01 and micro_opw_02 as sibling directories. Python 3, NumPy and SciPy are required by the original enumeration module; the independent checker uses only the standard library.

    python micro_opw_02/probe.py
    python micro_opw_02/verify.py

results.json contains exact fractions, complete component states, reader comparisons, tested absorption equations and input/source hashes. independent_checks.json reports the separate edge-set/vertex-neighbour reconstruction. The independent checker neither imports the main reader probe nor uses scipy's component algorithm. All assertions passed. These are exhaustive finite checks and elementary deductions, not new fundamental memory laws. No external novelty review was performed and no researcher was contacted.
