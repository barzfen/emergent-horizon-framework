# EHF-GROW-LIFT-04 — One-bit memory, growth compatibility and reciprocal holonomy

**Date:** 2026-11-13 (Australia/Brisbane).  
**Status:** exact finite enumeration at n=5,7,9, independent verification, and an elementary construction; **not a new physical law, not a solution of the earlier OPW23 twist problem, and not a novelty claim**.  
**Research direction:** Barry Fensom; computation and write-up assisted by ChatGPT.

## Question

Can one memory bit replace the globally optimized lift in [GROW-LIFT-03](../growth-lift-11/README.md), yielding genuine local dynamics compatible with inserting new Hamiltonian vertices? What distinguishes a *time-directed* cocycle from reversible transport on the undirected reversal graph?

## Exact carrier and rules

- States are undirected Hamiltonian cycles on fixed labels 0,...,n-1 modulo rotation and reflection, anchored at 0 with lexicographically smaller orientation.
- Marked vertices are R={1,2,3}; all other vertices have colour 0. MICRO requires every vertex to have a neighbour of its own colour, so for n≥5 the marked vertices form a contiguous block. State count: |X_n|=3(n-3)!.
- The geometric operation R_n reverses the **marked block of length 3**, swapping its two endpoint labels. It is a legal MICRO- and Pi-preserving LR3 involution. Here Pi(C) means the labels at even slots in the *canonical* cycle representation.
- Two-level growth projection pi_{n+2,n} deletes the two newest unmarked labels in reverse birth order.
- To define a **stable reference orientation**, orient the cycle rooted at label 0 so that label 4 is encountered before label 1. This survives deletion of all later labels. Set a(C)=1 when the first marked label in this reference orientation is numerically smaller than the last; otherwise a(C)=0. **Labels 0 and 4 and the fixed birth order are supplied reference structure; this is not a colour-only, unanchored local observable.**

## Constructed time-directed skew product

Adjoin a memory bit b∈F_2 and define

    F_n(C,b) = (R_n C, b XOR a(C)).

Because a(R_n C)=1-a(C),

    F_n^2(C,b) = (C,b XOR 1),
    F_n^4(C,b) = (C,b).

Thus every augmented orbit has length four, even though every underlying Hamiltonian configuration still has period two. The phase is stable under growth, a(pi C)=a(C), so pi_aug F_{n+2}=F_n pi_aug *exactly* for the levels tested, with an elementary argument for all n≥5.

### Exhaustive enumeration

| n | MICRO states | augmented states | R_n two-step orbits | F_n four-step orbits | OPW3 LR3 edges | OPW3 components | graph cycle rank |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | 6 | 12 | 3 | 3 | 3 | 3 | 0 |
| 7 | 72 | 144 | 36 | 36 | 54 | 27 | **9** |
| 9 | 2,160 | 4,320 | 1,080 | 1,080 | 3,000 | 390 | 1,230 |

All moves are the original marked-triple LR3; only the additional memory update is new. Pi of the underlying Hamiltonian cycle is preserved by R_n.

### Why choosing a chart matters

A naive bit defined as "the first marked endpoint is smaller than the last in the canonical 0-rooted, lexicographically oriented cycle" is **not** compatible with deletion:

| Projection | Canonical-endpoint phase unchanged | Stable 0,4,1-anchored phase unchanged |
|---|---:|---:|
| 7→5 | 42/72 | **72/72** |
| 9→7 | 1,512/2,160 | **2,160/2,160** |

The mismatches arise because canonical orientation can flip when an inserted unmarked vertex is removed. The additional persistent reference labels fix this but explicitly break relabelling symmetry.

## Crucial distinction: time cocycle versus reciprocal graph connection

For ordinary *graph voltage* or *reversible edge transport* with group F_2, the value A(C,D) on an oriented edge must obey

    A(D,C)=A(C,D)  (inverse = itself in F_2).

An immediate backtrack C→D→C therefore has **zero** net voltage. Our artificial time-directed skew product instead has a(C) XOR a(R C)=1. The *second forward dynamical step* is **not** the inverse transport of the first step. Consequently the time cocycle is legitimate as a cocycle over a time-ordered dynamical evolution, but it is **not a reciprocal voltage assignment on the underlying undirected single LR3 edge**.

This matters: attaching memory can produce longer augmented periods by rule design; that is not automatically emergent geometric holonomy.

## A genuinely graph-reversible comparison at n=7

The n=7 MICRO+Pi OPW3 move graph has **18 isolated K2 components and nine C4 components** (72 vertices; 54 edges; 27 connected components). Therefore the 1-dimensional graph cohomology over F_2 has dimension

    b1 = E-V+C = 54-72+27 = 9.

Each square is built from **commuting, independent marked-block and zero-block LR3 reversals**. A reciprocal F_2 voltage assignment can give nonzero circulation on a square by marking one undirected square edge. This is a valid graph-covering voltage example, but it is selected, not forced by the local EHF rules.

If these nine commuting squares are declared *filled relations* (zero holonomy across a commuting diagram), they form independent two-dimensional faces and

    dim H^1 (filled complex; F_2) = 9 - 9 = 0.

Thus on the n=7 carrier a **nonzero flat cocycle invariant is not forced** by MICRO+Pi; the answer depends on whether commuting squares are regarded as relations. This is a clean negative control for premature claims of Hamiltonian cocycle novelty.

## Does one bit fix GROW-LIFT-03?

**No—not with the old constraints and no change in underlying Hamiltonian transitions.**

GROW-LIFT-03 established a 7→9 mismatch between the Pi-class histograms of exceptional source and target 30-state fibers: at least **four of 30** matched transitions must change the *underlying endpoint Pi label set*. Merely duplicating every state with an auxiliary bit cannot turn a forbidden Pi-changing transition into a Pi-preserving one. The deficit becomes **eight among 60** decorated source states, if both bit values are included symmetrically.

The present F_n uses the older marked-triple involution as its geometric evolution, not the exceptional selected F7 with four-step geometric cycles. Its four-step period is in (cycle, memory), not in the Hamiltonian configuration alone.

## Reproduction and next falsifiable test

- [probe.py](probe.py): enumerates all three carriers; exact compatibility, phase-failure statistics, graph component census, and augmented orbit periods. Standard-library Python.
- [verify.py](verify.py): independent direct position-swap graph audit and square-face test.
- [results.json](results.json): exact result snapshot.

Next: seek a genuinely local, growth-compatible **geometric** controller that uses a bit to choose between different admissible reversals, rather than merely updating a passive register. Specify locality (which marked/anchor-relative sites are visible), relabelling-equivariance, allowable Pi defects, and whether two-step macro moves can modify the Hamiltonian cycle. Only after these are fixed can we test whether a bit is sufficient or prove a no-go theorem.

## Established mathematical context

- Graph voltage assignments require opposite edge orientations to carry inverse group elements; see [Voltage Graph, MathWorld](https://mathworld.wolfram.com/VoltageGraph.html).
- General graph covering/monodromy notions: [Graph Cover, MathWorld](https://mathworld.wolfram.com/GraphCover.html).
- Prior exact EHF probes: [GROW-LIFT-02](../growth-lift-10/README.md), [GROW-LIFT-03](../growth-lift-11/README.md), [CBB CROSS-03](../../../research/cbb-binary/CROSS-03-raw-cycle-parity-theorem.md).
