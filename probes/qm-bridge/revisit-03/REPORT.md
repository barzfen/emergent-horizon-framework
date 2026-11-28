# EHF QM bridge revisit 03 — making orientation operational

4 November 2026 · Barry Fensom research collaboration

**Evidence status: COMPUTATIONAL + ANALYTIC ARGUMENTS / CLASSICAL CONTROL.**

## Result

The orientation histories from Revisit 02 can be distinguished by a represented ordered pair of adjacent markers, under an explicit co-transport rule and local readout protocol. The added markers supply a directional reference that the original undirected carrier did not contain. Their roles and dynamics are assumptions, not consequences of MICRO or admissibility alone.

For the two retained five-move histories, an ideal frozen-carrier port reader distinguishes them with certainty after matching their unordered marker-position preparations. A live first-port reader, with carrier moves still active, achieves equal-prior optimal classification success 0.6830468891 after 12 benchmark ticks. A separately specified marker-gated coupling changes carrier motion and gives 0.7028698275 under its own 12-tick process. These are exact finite probability calculations, not measured performances or optimized protocols.

Every result is described by an ordinary finite classical process. No quantum amplitudes, Born rule or unitary evolution is used or derived.

## 1. Unchanged carrier and new degrees of freedom

Retain Revisit 02's labelled Hamilton-cycle states, canonical chart, fixed type-1 vertices {1,2,3}, Pi preservation, hard cyclic no-isolation, and indexed circular LR2/LR3 events. Full definitions remain in the preceding report and are executable in its probe.py. The new script records the SHA-256 of that dependency.

Add two distinguishable marker roles, previous and current, at adjacent labelled vertices (u,v). There are 2n possible ordered marker pairs per carrier. This is real extra structure in the toy model. Calling a pair ordered does not establish how it could arise autonomously or how a physical detector would recognize the roles.

For LR2 or LR3, reversing a window swaps its two endpoint vertex labels a,b. Define the marker interaction by applying that same label transposition to both marker positions:

    (c,u,v) -> (c', sigma(u), sigma(v)), sigma=(a b).

The markers remain adjacent in c'. The rule is reversible at the level of each event and matches Revisit 02's transported orientation. The marker update is a supplied co-transport interaction; the original carrier rules do not require markers to follow it. Equal reverse event support does not imply equal accepted-event probabilities or thermodynamic detailed balance.

On a fixed carrier, define forward circulation (u,v)->(v,w), where w is v's other neighbour. Backward circulation is its inverse. Both retain the marker-defined direction around the ring.

## 2. Fixed-clock joint process and backreaction control

Each benchmark tick has these alternatives:

- Probability 1/2: propose a uniformly selected legal indexed LR2/LR3 carrier event and co-transport markers.
- Probability 1/4: circulate the marker pair forward by one edge.
- Probability 1/4: circulate backward by one edge.

A carrier without legal events remains unchanged on its structural proposal. This is a chosen dimensionless clock, not physical time.

The primary coupling is passive with respect to the carrier: markers respond to its moves but do not change its transition probabilities. To test an explicit backreaction, a secondary model accepts a proposed structural event only if at least one marker occupies one of the two labels being exchanged. Otherwise the whole joint state stays unchanged. Rejected proposals still count as ticks. Spatial marker probabilities are unchanged.

This gate depends on marker positions but not marker roles. It is a chosen local kinetic restriction. At every checked carrier state some choices of marker location give different carrier transition laws. This shows the backreaction has been represented; it is not derived from an action, energy, detector design or physical experiment.

## 3. Forgetting marker roles: an exact limitation

Let R exchange previous and current marker roles, (c,u,v)->(c,v,u). Structural co-transport commutes with R. The two spatial circulation moves are exchanged by R and have equal probabilities. The secondary gate depends only on {u,v}, so it also respects R.

Therefore each joint kernel commutes with R. Identifying R-related states gives a strongly lumpable process on (c,{u,v}). Two preparations with identical distributions after this identification have identical future laws for every observation and protocol that retain only this reduced state.

Proof: for any R-orbit target C, the transition sum into C from x equals that from Rx, since R permutes C and conjugates the kernel. Iterate the equality for the reduced process. An adaptive reader restricted to these reduced observations and role-symmetric controls gains no information about the discarded roles.

This is a precise conditional statement. It does not cover a detector allowed to distinguish marker roles: that detector accesses the additional information by construction.

## 4. Retained history witness and matched preparations

Reuse the exact two five-move oriented histories already saved by Revisit 02, starting at (0,1,2,3,5,4,7,6,8). Copy its verification.json unchanged as input_witness.json and record its hash. Start the ordered markers at (0,1) and apply the stated endpoint transpositions along each retained history. The selected histories are controlled preparations, not claims of on-demand autonomous path selection. The schedules are retained in results.json.

Both end on the same undirected carrier:

    (0,3,2,1,8,6,7,4,5).

The first history leaves markers at (0,3), directed along the canonical tour. The second leaves markers at (8,1), directed oppositely. These positions differ, so reading their locations directly would confound direction with position.

To remove that confound, uniformly mix each preparation over its nine direction-preserving circulation positions. Each mixture has probability 1/9 on every unordered carrier edge. Consequently their complete (carrier, unordered marker pair) distributions are identical: total variation distance is exactly zero. Ordered roles remain different. This uniform mixing is an explicit preparation, not a spontaneous equilibration theorem.

## 5. Frozen-carrier local port reader

A supplied reference port can recognize vertex 0. For this control only, freeze carrier moves and circulate the ordered pair forward until its tail is at port 0. Read the type at the adjacent marker head. At most n-1 circulation moves are needed.

The port's two neighbours in the retained endpoint are 3 (type 1) and 5 (type 0). Thus the first history outputs 1 and the second outputs 0, for every initial marker position in the uniformized mixture. Their binary output laws have TV=1 and ideal equal-prior classification success 1.

The readout uses a local adjacent type once at the port, but reaching and recognizing that port, respecting marker roles, directed circulation and the frozen-carrier stage are supplied capabilities. It is not a measurement apparatus derived from the unmarked cycle. A port whose two neighbour types agree cannot distinguish the directions by this particular one-bit readout.

In the representative colouring census, port 0 has unequal neighbour types in 36 of 72 n=7 carriers and 720 of 2,160 n=9 carriers. These are availability counts, not ensemble-averaged detector successes or a universal orientation-reader theorem.

## 6. Live reader: no carrier freeze before detection

Start from the same matched position mixtures on the same retained endpoint. Evolve either fixed-clock joint model above. At time zero and after every tick, a detector checks whether the marker tail is at port 0. On the first such visit it records the current head's bit type. The carrier continues moving before this event. Probability mass is stopped computationally after recording solely to calculate this first-arrival law.

A horizon T defines three outputs: 0, 1, or no detection yet (timeout). Retain the timeout in the data; do not condition on successful detection. The detector does not use the precise arrival time beyond whether it met the horizon. A supplied monitor and stopping rule remain assumptions. No robust persistent storage or autonomous reset mechanism is established.

Exact rational forward propagation gives:

| Model | Horizon | Equal-prior optimal success | Timeout, first preparation | Timeout, second preparation |
| --- | ---: | ---: | ---: | ---: |
| Passive carrier coupling | 0 | 0.5555555556 | 0.8888888889 | 0.8888888889 |
| Passive carrier coupling | 5 | 0.6369920428 | 0.6716798664 | 0.6716798664 |
| Passive carrier coupling | 12 | 0.6830468891 | 0.5062936983 | 0.5062936983 |
| Marker-gated backreaction | 0 | 0.5555555556 | 0.8888888889 | 0.8888888889 |
| Marker-gated backreaction | 5 | 0.6428238715 | 0.6670225781 | 0.6881284462 |
| Marker-gated backreaction | 12 | 0.7028698275 | 0.5105118938 | 0.5421920072 |

Success is (1+TV)/2 for the full three-outcome laws with equal priors. In the gated case, a timeout itself carries information. The displayed decimals summarize exact fractions in results.json. No parameter search, Monte Carlo sampling or comparison of optimized detector designs was done.

The different gated success is specific to its changed transition law and chosen preparation. It is not evidence that backreaction generically improves reading or supplies quantum behaviour.

## 7. Finite verification scope

| n | Carrier states | Ordered-marker joint states | Structural marker/event checks | States with marker-position-dependent gated carrier law |
| ---: | ---: | ---: | ---: | ---: |
| 7 | 72 | 1,008 | 2,352 | 72 |
| 9 | 2,160 | 38,880 | 146,880 | 2,160 |

All admissible carriers for this fixed colouring are covered, including components unrelated to the retained witness. For every joint state, both role-forgetting kernels were checked exactly. Structural checks verify adjacency preservation, the transported orientation sign and inverse event support. The joint-state counts describe the full specified state space, not connected-component or reachability counts from one preparation.

The independent verifier does not import either probe. It enumerates carriers separately, checks MICRO using undirected edge sets, and transports marker slots during actual reversals rather than applying the main implementation's label permutation rule. It reproduces the finite counts, both role-forgetting kernels, the retained schedules, and all 13 saved live-reader horizons in both coupling models using exact rational arithmetic. All assertions passed. Both implementations were generated in the same AI-assisted workflow; this is independent implementation, not independent human peer review.

## 8. Research conclusion

The original undirected carrier's hidden orientation becomes readable once a directional relational reference is added and coupled in a specified way. Merely retaining signed history weights had not supplied that reference. Role-blind observers remain unable to read it, even under the chosen marker-position backreaction.

This is a classical operational-access result. The marker pair already distinguishes the relevant histories in the complete state. No preparations identical in the full joint state develop different probabilities under the same process, and no positive occupancy is replaced by a squared signed difference. The probe closes a bookkeeping-to-readout gap for a deliberately enlarged model; it does not close the classical-to-quantum gap.

A useful next decision is whether to pursue this as a classical record/reference branch or audit a different mechanism for effective quantum amplitudes. More marker-rate sweeps alone would not derive QM. Any attempt to obtain complex phase, coherent recombination, a Born rule or Bell correlations must specify further structure and the relevant classical control.

## Reproduction and provenance

From the repository root:

    python3 probes/qm-bridge/revisit-03/probe.py
    python3 probes/qm-bridge/revisit-03/verify.py

Only Python's standard library is required. Keep Revisit 02 as a sibling directory. Input_witness.json is the frozen prior certificate; results.json records dependency and input hashes, the physical-marker schedules, finite counts and exact detector laws. Verification.json records the separate implementation's checks.

Research direction: Barry Fensom. Implementation, analysis and exposition assisted by ChatGPT. No novelty claim, physical experiment or researcher endorsement is asserted. No researcher was contacted.
