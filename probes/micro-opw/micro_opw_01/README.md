# EHF MICRO–OPW 01: no-isolation constraints change the role of LR2

Date: 2 November 2026. Research direction: Barry Fensom. Implementation and analysis assisted by ChatGPT.

**Status:** exhaustive finite graph enumeration, elementary deductions, and independent witness checks. No physical or novelty claim. This tests an explicitly chosen combination of two existing EHF models; it does not derive their rules.

## Main finding

MICRO can be imposed on OPW without eliminating all motion. More significantly, OPW3 and OPW23 no longer always have the same connected components after the MICRO restriction. Added LR2 transitions reconnect some regions separated under constrained LR3. This does not connect different original Pi chambers.

For the representative assignment where vertices 1,2,3 have bit 1 and every other vertex has bit 0:

| Vertices | MICRO-valid cycles | MICRO–OPW3 components | MICRO–OPW23 components | Largest component: 3 / 23 | Isolated states: 3 / 23 |
|---:|---:|---:|---:|---:|---:|
| 7 | 72 | 27 | 15 | 4 / 8 | 0 / 0 |
| 9 | 2,160 | 390 | 111 | 24 / 72 | 0 / 0 |

Thus the separation is not merely a consequence of freezing all states. Component counts above are over all surviving original chambers for the specified assignment, not inside one chamber. Identity of the coloured vertex labels matters in the fixed OPW chart; these numbers are not universal at a given population count.

## Exact definition

1. States are undirected Hamilton cycles on labelled vertices 0,...,n-1, modulo rotation and reflection. Anchor 0 and choose the lexicographically smaller orientation.
2. Pi is the unordered even/odd-position label partition of the canonical cycle. For odd n the larger, even-position set uniquely determines that pair.
3. Attach a fixed binary type to each labelled vertex. Types travel with vertices during rearrangement; they do not flip.
4. A state is MICRO-admissible if each vertex has at least one cycle neighbour of its own type. Equivalently, its cyclic binary word contains no 010 or 101, including wrap-around triples.
5. Retain the OPW edge only if both endpoints are MICRO-admissible. OPW3 uses circular length-3 reversals; OPW23 permits lengths 2 and 3. Pi must be preserved after canonicalization.

This is a hard D=0 induced-state restriction, not the directional rule D(next)<=D(current) on states with positive defect cost. No bit flips, growth, clock, energy, switching schedule, writer or rates are included. The new vertex types are not the existing active-slot packet bits. The canonical OPW chart is held fixed; arbitrary relabellings are not silently identified as symmetries.

## Exhaustive scope

Every canonical cycle at n=5,7,9 was enumerated, and every nonconstant binary vertex assignment was tested modulo global bit complement. Fixing bit(0)=0 selects exactly one member of each complement pair; this does not assume arbitrary vertex permutations preserve OPW. Counts are 15+63+255=333 assignments. Of those, 21 have a single vertex of the minority type and consequently no admissible cycle. The other 312 have surviving states.

| n | Minority count | Assignments tested | Surviving cycles per assignment | Assignments where LR2 reconnects LR3 components |
|---:|---:|---:|---:|---:|
| 5 | 1 | 5 | 0 | 0 |
| 5 | 2 | 10 | 6 | 0 |
| 7 | 1 | 7 | 0 | 0 |
| 7 | 2 | 21 | 120 | 0 |
| 7 | 3 | 35 | 72 | 35 |
| 9 | 1 | 9 | 0 | 0 |
| 9 | 2 | 36 | 5,040 | 0 |
| 9 | 3 | 84 | 2,160 | 84 |
| 9 | 4 | 126 | 2,880 | 126 |

The raw OPW census reproduced the retained baseline exactly: n=5 has 12 states, 8 edges in either model and 5 chambers; n=7 has 360 states, 600/840 edges and 19 chambers; n=9 has 20,160 states, 53,760/67,200 edges and 69 chambers. Both baseline partitions agree as sets, not just in component count.

All-single-type assignments would reproduce the original OPW graphs, since MICRO is then satisfied everywhere; they are not included in the 333 nonconstant cases.

## A small exact witness

Take n=7, bit-1 vertices {1,2,3}. The cycles

    A = (0,1,2,3,4,5,6)
    B = (0,5,4,3,2,1,6)

are both MICRO-valid and have the same even-position set {0,2,4,6}. Swapping the adjacent vertices 6 and 0 in A, then canonicalizing, produces B. Both swapped vertices have bit 0.

Under MICRO–OPW3 the two cycles are in distinct components. Under MICRO–OPW23 the displayed LR2 edge joins them. The OPW3 component containing A has four states; its containing OPW23 component has six states. Other OPW23 components can be larger, as shown in the table.

The independent checker represents cycles as undirected edge sets, determines MICRO validity from the two neighbours of each vertex, and computes connected components by direct depth-first search. It independently recovers the complete n=7 and n=9 representative graphs and their counts; it does not import probe.py or use scipy's component algorithm.

## Why LR2 can matter while its bit swap looks invisible

On a no-isolation binary ring, an adjacent unequal pair has the local surroundings aa bb. Swapping the middle a and b gives a b a b and creates isolated symbols. Therefore a MICRO-valid LR2 swap must exchange equal bits. Such a swap can still exchange different labelled vertices and change the Hamiltonian cycle.

**Consequently, bit-invisible rearrangements can change reachability among labelled structures.** This is precisely what the witness demonstrates. It does not imply that all readers can detect the component distinction. With a 3/4 split at n=7 every admissible word has one run of each type, so a reader seeing only the unanchored binary necklace sees the same colour pattern in all 72 states. A labelled structural reader can distinguish A and B, for example through whether edge {0,1} is present. That is ideal structural access, not a constructed physical detector.

The census also checks that every accepted LR3/LR23 edge preserves the number of binary domain walls in these finite cases. Such invariants need careful separation from the finer labelled fragmentation; they do not alone explain every component.

## Connection to the memory audits

This supplies a candidate separation of move classes: MICRO–OPW3 can preserve a component label while a MICRO-compatible LR2 interaction changes it. It does not yet supply a memory device. Choosing LR3 during storage and enabling LR2 during writing would add a control assumption. We have not represented that control, measured a retention time, imposed a noise law, or established a boundary-readout protocol.

All moves still preserve the original Pi label. The new separation is within original OPW chambers. Adding LR2 never connects different original chambers in this audit. Under a connected finite symmetric-rate process, endpoint distinguishability within that connected component would eventually decay; no numerical lifetime follows from component counts alone.

The most specific next question is whether a represented probe interaction can enable one of these extra LR2 transitions and then depart, while accounting for return crossings and accidental activation. A precursor is to identify a readable structural distinction in a chosen constrained component. This avoids declaring conserved but inaccessible labels to be useful records.

## Reproduction and checks

Requires Python 3, NumPy and SciPy. Run from this directory:

    python probe.py
    python verify_witness.py

Outputs are results.json and independent_checks.json. The results include every assignment, component-size histograms, witnesses, dependency versions and the main script SHA-256. No stochastic sampling or fitted rates are used. The main run checks baseline counts, Pi-fibre connectivity, component refinement, domain-wall conservation and LR2 reconnection. A union-find implementation independently checks component counts for all n<=7 assignments; the edge-set checker independently verifies the complete representative n=7 and n=9 cases and the separating witness. All assertions passed.

## Sources and scope

Definitions follow the supplied EHF OPW3 Rebuild Working Document v1.6 and RAF Odd Preserve-World Chamber and Boundary Dynamics v6, plus the recovered cyclic MICRO no-isolation definition in the conversation. The MICRO–OPW composition is specified in full above rather than inherited as an already proved result. This audit uses no theorem from the delta-Ising paper. Its relevance is only a prospective comparison about transition channels; no Ising dynamics or energy was imposed here. The record-access limitations follow the questions in EHF-RW-002–005 and assumption audits 02–05.

This is a finite combinatorial result within a chosen model. It is not evidence that nature uses vertex bits, OPW, MICRO or a write/store switch. No external novelty review or publication claim is made.
