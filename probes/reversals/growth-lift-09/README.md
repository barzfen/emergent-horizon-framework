# EHF-GROW-LIFT-01 — Does Hamiltonian growth lift or split reversal dynamics?

**Date:** 2026-11-13 (Australia/Brisbane). **Status:** exact finite enumeration and elementary structural explanation. **No novel theorem or physics interpretation claimed.**

## Research question
EHF-WIEF-02 showed a precise dichotomy for powers-of-two modular orbits: under a compatible refinement, a base cycle can elongate or lift to several separate cycles. Does vertex insertion in EHF Hamiltonian systems produce a comparable, well-defined lifting phenomenon?

**Answer in this probe:** RAW LR3 component counts alternate dramatically under growth, but the natural deletion projection does *not* preserve LR3 edges. Hence this is **component fragmentation/reconnection, not yet cycle lifting in the graph-covering sense**. The same obstruction persists in a MICRO+Pi OPW test.

## Exact definitions

- RAW states at size `n`: undirected Hamiltonian cycles on distinct fixed labels `0,...,n-1`, modulo rotation and reflection. Canonical traversal starts at 0 and selects the lexicographically smaller orientation. There are `(n-1)!/2` states.
- Growth: insert new label `n` into any of the `n` cycle edges; deleting it and reconnecting its two neighbours is the **unique** inverse parent map `π`. Each RAW parent has exactly `n` distinct children.
- LR3: reverse three consecutive cyclic positions (swap its endpoints), then canonicalize. LR2 is the corresponding adjacent exchange. Treat legal reversals as undirected, unweighted **state graph edges**, not as deterministic trajectories.
- MICRO: each vertex must have a cyclic neighbour of its own fixed bit. We explicitly state the marked-label set `R` (labels in `R` carry bit 1).
- OPW3/OPW23 for odd sizes: retain only MICRO-valid states, plus LR3 or LR2/LR3 moves that preserve canonical `Pi = {c[0],c[2],c[4],...}`, respectively. In the OPW comparisons we use `R={1,2,3}` and delete two newest labels, `n+1` then `n`, to compare odd sizes `n -> n+2`.

## RAW exact enumeration

| size n | states | LR3 edges | LR3 components | equal component size |
|---:|---:|---:|---:|---:|
| 5 | 12 | 30 | 1 | 12 |
| 6 | 60 | 90 | 10 | 6 |
| 7 | 360 | 1260 | 1 | 360 |
| 8 | 2520 | 10080 | 35 | 72 |
| 9 | 20160 | 90720 | 1 | 20160 |

These reproduce [EHF-CBB-CROSS-03](../../../research/cbb-binary/CROSS-03-raw-cycle-parity-theorem.md): LR3 swaps entries separated by two positions. For odd `n`, the step-two position graph is connected, so LR3 acts transitively. For even `n=2m`, the two alternating position classes are preserved; components are indexed by unordered equal bipartitions of vertex labels, giving `(1/2) binom(2m,m)` components.

**Interpretation caution:** these are counts of connected components of a **graph of Hamiltonian-cycle states**, not counts of Hamiltonian cycles in a single modular-doubling permutation.

## The crucial cross-scale obstruction

Deleting the new vertex from an LR3 move in a size-`n+1` child yields:

- LR3 in the parent if the deleted vertex lies outside the reversed three-slot segment;
- LR2 in the parent if the deleted vertex lies in the segment.

These are checked exhaustively over all simple LR3 edges in the following RAW sizes:

| Growth | Child LR3 edges projecting to LR3 | Projecting to LR2-only | Both LR2 and LR3 in parent |
|---|---:|---:|---:|
| 5→6 | 0 | 0 | 90 |
| 6→7 | 720 | 540 | 0 |
| 7→8 | 6300 | 3780 | 0 |
| 8→9 | 60480 | 30240 | 0 |

At parent size 5 the LR2/LR3 edge sets coincide because of complementary reversal segments.

An explicit witness for `6 -> 7`:
- child `(0,1,2,3,4,5,6) -> (0,1,2,3,6,5,4)` is an LR3 edge;
- deleting label 6 gives `(0,1,2,3,4,5) -> (0,1,2,3,5,4)`, an **LR2-only** edge, not LR3.

Thus deletion is **not a graph morphism from the size-7 LR3 graph to the size-6 LR3 graph**. This invalidates interpreting the raw even/odd component pattern as a strict Wieferich-style lift. A graph covering would impose even stronger compatibility, including local correspondence of incident edges; see Gross and Tucker, *Generating all graph coverings by permutation voltage assignments*, Discrete Mathematics 18 (1977), 273–283.

## MICRO insertion/deletion need not be closed

With fixed marked labels `R={1,2,3,4}`:
- `7 -> 8`: 72 MICRO-valid parent states, 432 MICRO-valid child states; **144 valid children delete to invalid parents**.
- `8 -> 9`: 432 parent states, 2880 child states; **576 valid children delete to invalid parents**.

Witness at size 8: `(0,1,2,5,6,3,4,7)` satisfies MICRO with bits `R={1,2,3,4}`, but deleting 7 gives `(0,1,2,5,6,3,4)`, where a zero-bit vertex is isolated. Thus a naive parent map need not even map the *admissible child state space* into the parent state space.

## OPW3 and OPW23 exact cross-scale test

Use fixed bit-1 labels `R={1,2,3}`, MICRO on both sides, canonical Pi preservation for moves, and deletion of the two newest labels for odd-size comparisons.

| Growth | Model | Parent components | Child components | Child edges | Project to same parent | Project to allowed edge | Project to forbidden parent edge |
|---|---|---:|---:|---:|---:|---:|---:|
| 5→7 | OPW3 | 3 | 27 | 54 | 18 | 36 | 0 |
| 5→7 | OPW23 | 3 | 15 | 84 | 42 | 42 | 0 |
| 7→9 | OPW3 | 27 | 390 | 3000 | 576 | 1296 | **1128** |
| 7→9 | OPW23 | 15 | 111 | 4080 | 1152 | 1608 | **1320** |

In these particular OPW tests **every child state has a MICRO-valid parent**. Nevertheless a substantial subset of size-9 legal edges projects to forbidden size-7 moves, even with fixed bits and Pi checked on each side.

Common OPW3/OPW23 witness:
- size-9 legal edge `(0,1,2,3,4,5,6,7,8) -> (0,1,2,3,4,7,6,5,8)`;
- delete labels 8 and 7 to get size-7 states `(0,1,2,3,4,5,6) -> (0,1,2,3,4,6,5)`.
The parent transition is LR2 but changes canonical Pi and is therefore forbidden in both models.

## Validation

Reproduce with standard-library Python:
- [probe.py](probe.py) — RAW edges, insertion fibers, MICRO fixed-`R={1,2,3}` and projected edge categories; writes `results.json`.
- [opw_audit.py](opw_audit.py) — odd-size MICRO+Pi OPW3/OPW23 projection census; writes `opw-results.json`.
- [verify.py](verify.py) — independent LR3 edge generator via endpoint swaps, all-size census, MICRO nonclosure counts, and OPW projection assertions.

Run `python probe.py`, `python opw_audit.py`, `python verify.py` from this directory. The independent LR3 generator and the OPW cross-check assertions passed.

## Next experiment — growth-compatible moves

To make a Wieferich-type cycle-lift comparison mathematically legitimate, construct a family of admissible state spaces `X_n`, parent maps `π_n : X_{n+1} -> X_n`, and **deterministic** moves `F_n` or consistently labelled move generators such that `π_n F_{n+1}=F_n π_n` (or a specified edge-lift property). Then study the **fiber return permutation** above each closed base orbit. Possible outcomes include lengthening, splitting, and nonexistence of a compatible lift.

Do not equate component counts with orbit lengths. Do not infer a novel effect, a physical interpretation, or a Collatz implication from the finite examples.

## Related EHF work

- [Wieferich orbit lifting](../../../research/wieferich/EHF-WIEF-02/README.md)
- [RAW LR3 parity theorem](../../../research/cbb-binary/CROSS-03-raw-cycle-parity-theorem.md)
- [MICRO and Pi restrictions](../all-length-01/README.md)
- [Unique insertion history under fixed label order](../../../research/cbb-binary/BIN-02-history-audit.md)
