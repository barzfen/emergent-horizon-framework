# EHF-HOL-05 / GROW-LIFT-05 — Orientation holonomy under admissible Hamiltonian reversals

**Date:** 2026-11-13 (Australia/Brisbane).  
**Status:** exact, exhaustive finite graph/cocycle computation for n=7 and n=9, with independent direct-swap verification. **No general EHF theorem, physics claim or literature novelty claim.**  
**Research direction:** Barry Fensom; formalization and code assisted by ChatGPT.

## Question

Can EHF's **actual** MICRO+Pi admissible Hamiltonian transformations induce a reciprocal, non-potential transport invariant, rather than a memory bit deliberately appended to a controller? If so, is it persistent under the existing vertex-deletion growth projection?

## Specified carrier

- Distinct vertices `0,...,n-1` with fixed colour-1 label set `R={1,2,3}`; all others have colour 0.
- MICRO: no isolated bit in the cyclic binary word. With this assignment, the three marked vertices form one consecutive block.
- Hamiltonian states are undirected cycles modulo cyclic rotation and reflection. Canonical representation starts at 0 and uses the lexicographically smaller orientation.
- `Pi(C)` is the set of labels at even positions in the canonical representative.
- OPW3 edges: nontrivial length-three cyclic segment reversals preserving MICRO and Pi; OPW23 adds length-two reversals. Distinct *events* are checked before identifying simple graph edges.
- Calculation over `F_2`, which is appropriate for a two-valued orientation reversal.

## Natural reciprocal orientation voltage

For every directed allowed reversal `C -> D`, retain the orientation from the canonical source `C` while performing the reversal. Rotate to start at 0 **without reflecting**. Set `alpha(C,D)=0` if this oriented output is already the canonical target `D`; otherwise set `alpha(C,D)=1` when its reflection is `D`.

For n=7,9, exhaustive enumeration finds **exactly one LR2/LR3 reversal event per directed edge** of the relevant graph, so the voltage is unambiguous. Reciprocal edges have the same `F_2` voltage (the inverse equals itself). This defines the canonical orientation-double-cover class of the move graph, up to gauge changes from different local choices of canonical orientation. It is **not an artificially selected edge label**.

**Important n=5 caveat:** in the OPW23 simple-edge graph the LR2 and LR3 descriptions of the same edge produce opposite orientation voltages. Hence the voltage is NOT well defined on that n=5 simple graph without retaining the event label or using a multigraph. Do not extrapolate this construction to n=5 without that correction.

For a closed move path `P`, `Omega(P)=sum_{e in P} alpha(e) (mod 2)` records whether the underlying oriented cycle returns reversed.

## Exact finite results

| Carrier | States V | Edges E | Components c | Bare graph H1 = E-V+c | After filling **every simple square** | After additionally filling **every simple hexagon** | Components with nonzero natural orientation voltage |
|---|---:|---:|---:|---:|---:|---:|---:|
| OPW3 n=7 | 72 | 54 | 27 | 9 | 0 | 0 | **0** |
| OPW23 n=7 | 72 | 84 | 15 | 27 | 3 | 3 | **3** |
| OPW3 n=9 | 2,160 | 3,000 | 390 | 1,230 | 30 | 0 | **0** |
| OPW23 n=9 | 2,160 | 4,080 | 111 | 2,031 | 81 | 51 | **9** |

All cohomology dimensions are over `F_2`. These 2-dimensional cell structures are **defined by the stated fillings**; they are not claimed to be the uniquely correct homotopy presentation for EHF. Squares include commuting-reversal candidates; some six-cycles instantiate Coxeter braid relations, but filling every six-cycle is a deliberately strong benchmark.

### Natural voltage witnesses and controls

- OPW3: the orientation voltage is a **coboundary** on each entire n=7 and n=9 graph component. All closed paths have zero orientation holonomy, even though many graph cycles exist.
- OPW23 n=7: exactly **three 8-state components** have nontrivial orientation voltage; the shortest orientation-reversing closed path has **five** edges. Every one of the 24 simple five-cycles has nonzero orientation voltage.
- OPW23 n=9: exactly **nine components** (three of size 48, three of size 64 and three of size 72) have nontrivial orientation voltage. A shortest orientation-reversing closed path found has **ten** edges.
- The voltage is zero on **every enumerated simple square, hexagon and eight-cycle** on the four carriers. Consequently it defines a nonzero class after filling all squares and hexagons for the OPW23 cases. At n=9 even filling all simple eight-cycles leaves the natural orientation class nontrivial, since it evaluates to 1 on the explicit ten-cycle.
- The dimension 51 is **not** 51 independent naturally assigned orientation bits. Our distinguished natural voltage gives one cohomology class on each of the nine nontrivial components. Many other cohomology classes exist, but choosing their edge voltages requires extra structure.

## Exact growth-compatibility obstruction (7 -> 9)

Use the existing fixed-birth-order projection `pi: X_9 -> X_7`, deleting labels 8 then 7. An edge at n=9 is **projectable** if its endpoints project either to the same n=7 vertex or to a legal n=7 edge. Restricting to such edges makes projection a graph morphism (allowing collapsed edges).

| Child model | All n=9 edges | Projectable edges | Nonprojectable edges | Collapsed-to-vertex edges | Components of projectable subgraph | Natural orientation-voltage-nontrivial components there |
|---|---:|---:|---:|---:|---:|---:|
| OPW3 | 3,000 | 1,872 | 1,128 | 576 | 702 | **0** |
| OPW23 | 4,080 | 2,760 | **1,320** | 1,152 | 354 | **0** |

The orientation voltages on the projectable edges agree with the parent's oriented transitions **up to the canonical-orientation chart change**, and collapsed edges do not reverse the parent orientation. These are checked on every projected directed edge.

**Sharp finite observation for OPW23:** every nonprojectable edge connects different components of the projectable subgraph; therefore an orientation-reversing closed path must cross **at least two** nonprojectable edges. The quotient graph has 12 pairs of compatible components joined by forbidden edges with opposite residual orientation voltage, producing a closed path using **exactly two** nonprojectable edges. Thus the minimum is **exactly 2**.

So the natural orientation class is present in n=9 OPW23, but **vanishes after restricting to the moves compatible with the chosen 7->9 growth projection**. Neither the full OPW23 adjacency nor its nontrivial orientation class is a proven persistent object under this projection.

## Reproducibility

- [probe.py](probe.py) is a standard-library exhaustive enumeration. It constructs oriented reversal events, tests reciprocal voltage and ambiguity, enumerates short loops, computes binary boundary ranks, searches the orientation double cover for nonzero closed paths, and audits growth projection.
- [verify.py](verify.py) independently reconstructs the graphs via direct positional swaps and tests the witness paths and growth-compatible potential exactness.
- [results.json](results.json) retains the numerical results and explicit five-step and ten-step witness paths.

Run `python3 probe.py` and then `python3 verify.py` from this folder.

## Interpretation and next falsifiable experiment

**Positive:** EHF's chosen LR2/LR3 move system can produce a mathematically canonical, reciprocal orientation-cover cocycle *without* introducing a passive memory register. This is an application of standard graph covering theory to a specified EHF carrier.

**Negative:** the nontrivial class is absent from OPW3 and is not inherited via the present growth-compatible OPW23 subgraph. It may reflect the quotient identifying clockwise and anticlockwise cycles, rather than a new independent conserved quantity.

**Next:** switch from unoriented simple edges to an **event-labelled oriented reversal groupoid**, retaining information about which segment was actually reversed, and test whether there is a coherent growth map or whether the same obstruction persists. A positive result would require an explicit compatible functor and a nontrivial class under that functor; merely finding closed loops or assigning a voltage would not suffice.

## Mathematical background and attribution

- Voltage assignments and inverse edges: https://doi.org/10.1016/j.jctb.2018.01.007
- Coxeter commutation and braid relations: https://www.symmetricfunctions.com/permutations.htm
- Earlier EHF probes: [GROW-LIFT-04](../growth-lift-12/README.md), [GROW-LIFT-03](../growth-lift-11/README.md), [EHF-WIEF-02](../../../research/wieferich/EHF-WIEF-02/README.md).

**Bottom line:** A real finite orientation holonomy exists under OPW23, but **persistence under the chosen EHF growth rule remains unestablished and fails on the projection-compatible subgraph tested here**.
