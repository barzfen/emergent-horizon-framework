# EHF-GROW-LIFT-03 — The Pi barrier and a MICRO-only macrostep rescue

**Date:** 2026-11-13 (Australia/Brisbane).  
**Status:** exact finite computations and independently checked finite obstructions at n=7 and n=9; selected existence construction. Neither a new physics result nor a general all-n theorem.  
**Research direction:** Barry Fensom; experiments and writing assisted by ChatGPT.

## Question

GROW-LIFT-02 found a selected OPW23 controller at size 7 with three four-step orbits that could not be lifted to 9 by a **single** allowed OPW23 move. Would multiple LR2/LR3 microsteps rescue it? If not, which assumption must be relaxed?

## Carrier and admissibility

- Undirected Hamiltonian cycles on distinct labels `0,...,n-1`, modulo rotation and reflection, canonically rooted at 0. Odd sizes n=5,7,9.
- Fixed bit 1 on labels `R={1,2,3}`; all other vertices have bit 0. MICRO = every vertex has at least one same-colour cyclic neighbour. With three marked labels, the marked vertices form a contiguous block.
- `Pi(C)` = labels at positions `0,2,4,...` in the canonical orientation. OPW23 microstep = LR2 or LR3 reversal preserving MICRO and Pi at *each* step. The relaxed MICRO-only graph preserves MICRO but allows Pi to change.
- A macrostep consists of 1 or more microsteps. Projection `pi: X9 -> X7` deletes labels 8 and 7; every size-7 state has exactly 30 MICRO-valid descendants.
- The base controller `F7` is **the selected twist** from GROW-LIFT-02, with 30 length-2 orbits and three length-4 orbits. There are six LR2 directed arcs that differ from the canonical marked-triple flip.

The new graph computations independently reconstruct the full n=9 carrier (2,160 states), its Pi-preserving OPW23 graph (4,080 edges, 111 components), and the MICRO-only LR2/LR3 graph (connected).

## Result A — reachable endpoints for each exceptional directed arc

For **both directions of all six extra LR2 cross-fiber edges** (12 directed arcs total), the 30 size-9 source descendants have exactly the same distance distribution to the required 30 target descendants.

| Nine-vertex rule | Distance 1 | Distance 2 | No path | Reachable total |
|---|---:|---:|---:|---:|
| MICRO + Pi at each LR2/LR3 move | 20 | 7 | 3 | 27 |
| MICRO only at each move | 28 | 2 | 0 | 30 |

All distances are shortest-path distances in the full corresponding 2,160-state graph. Under Pi-preserving OPW23, the three unreachable source descendants are in connected components containing no required target state. This is not merely a search-depth limit.

## Result B — bijection bounds are stricter than reachability

A compatible deterministic permutation requires a **perfect matching** between each 30-element source and target fiber.

For each of the 12 directed exceptional transitions:

| Restriction | Maximum matched of 30 |
|---|---:|
| OPW23, one microstep | 20 |
| OPW23, up to two microsteps | 22 |
| OPW23, any number of microsteps | **23** |
| MICRO-only, up to two microsteps | **30** |

The 23 upper bound is exact: decompose the 2,160-state Pi graph into connected components `K`; then the maximum number of source-to-target bijective pairings reachable by arbitrary paths is
`sum_K min(|source_fiber ∩ K|, |target_fiber ∩ K|)=23`.
The length-2 matching bound was checked by exact assignment, not inferred from the 27 reachable sources.

**Even if intermediate microsteps may violate Pi but endpoints must preserve Pi**, the upper bound is 26, independent of path length. The multiset of Pi labels on source and target fibers differs, giving
`sum_sigma min(count_source(sigma),count_target(sigma))=26`.
Thus *at least four* of 30 matched transitions must change Pi at their endpoints in any full bijection, regardless of internal path length.

## Result C — exact cost of relaxing Pi

Using exact minimum-cost assignment between the two 30-element fibers, where the cost is one for an endpoint Pi change and paths are bounded in length, the following minima are attained **for all twelve directed exceptional arcs**:

| Maximum MICRO-only microsteps | Perfect matching? | Minimum endpoint Pi changes among 30 |
|---:|:---:|---:|
| 1 | No (at most 28) | — |
| 2 | Yes | **8** |
| 3 | Yes | **5** |
| 4 | Yes | **4** |

The lower bound four at unrestricted path length follows without computation from the Pi-histogram mismatch above. Four steps attain it.

## Result D — an explicit compatible n=9 macrostep permutation

Use the GROW-LIFT-02 twisted permutation `F7`, and define the larger `F9` as follows:

1. Over each ordinary marked-triple LR3 arc of `F7`, choose the same marked-triple LR3 reversal of every size-9 descendant.
2. Over each of the six exceptional directed LR2 arcs of `F7`, use an exact minimum-cost **perfect matching** between the 30-element source and target descendant fibers, with each selected pair joined by at most two MICRO-only LR2/LR3 moves. The optimization minimizes the number of changed endpoint Pi classifications.

This is an everywhere-defined **bijective** `F9` on all 2,160 states and `pi F9 = F7 pi`. Exact orbit count:

| Orbit length | n=7 count | n=9 count |
|---:|---:|---:|
| 2 | 30 | **900** |
| 4 | 3 | **90** |

Every macrostep is realized by one or two MICRO-admissible LR2/LR3 microsteps. Exactly **48 of the 2,160 selected n=9 macrosteps change Pi at their endpoints** (6 exceptional directed arcs × 8 optimal changes). All other macrosteps preserve Pi.

Example path that repairs a previously blocked direct lift:

```
(0,6,3,2,1,5,4,7,8)
  -> (0,6,3,2,1,5,7,4,8)
  -> (0,7,5,1,2,3,6,4,8)
```

The first and last states project, respectively, to
`(0,4,5,1,2,3,6)` and `(0,4,6,3,2,1,5)`: an exceptional seven-vertex LR2 arc.

### Interpretation and limitations

- **Negative result for OPW23:** no number of Pi-preserving LR2/LR3 microsteps can lift these particular exceptional transitions as bijections of all their n=9 descendants.
- **Positive result for MICRO-only macrosteps:** relaxing Pi permits a compatible selected permutation and preserves the earlier four-step orbits at n=9.
- **Essential caveat:** the n=9 controller uses a globally optimized fiber matching. The individual microsteps are local reversals, but the *selection policy is not demonstrated to be local, autonomous, equivariant under arbitrary relabelling, or consistent for n>=11*. Pi is a chosen canonical-label chart, not a demonstrated physical charge.
- The n=9 orbit counts do **not** show further orbit elongation from 4 to 8; they show persistence of the previously constructed four-step loops.
- These are finite combinatorial findings, not evidence for quantum mechanics, gravity, or Collatz.

This distinguishes **stepwise conservation**, **endpoint conservation**, and **compatibility of deterministic dynamics under growth**. They are mathematically different conditions and give strictly different obstructions here.

## Reproducibility

- [probe.py](probe.py) — standard-library exact graph enumeration, breadth-first search, integer Hungarian assignment, and explicit compatible permutation.
- [verify.py](verify.py) — independently generates LR2/LR3 edges by direct slot swapping and checks graph components, exact distance counts, assignment bounds via SciPy, and a three-state witness.
- [results.json](results.json) — retained exact output, including all 12 directed arcs.

Run `python3 probe.py`; optional independent verifier requires SciPy: `python3 verify.py`.

## Context and future question

- [GROW-LIFT-02](../growth-lift-10/README.md) gives the marked-triple involution, the selected n=7 four-step twists, and the one-step n=9 obstruction.
- [GROW-LIFT-01](../growth-lift-09/README.md) documents noncommutativity of arbitrary reversal and insertion.
- [WIEF-02](../../../research/wieferich/EHF-WIEF-02/README.md) is a separate number-theoretic orbit-lifting control.
- Gross and Tucker, [*Generating all graph coverings by permutation voltage assignments*](https://www.sciencedirect.com/science/article/pii/0012365X77901315) (1977), is background for the standard fiber/monodromy language, **not** a claim that the entire EHF reversal graph is a graph cover.

**Next test:** replace the globally optimized matching by a genuinely local controller and ask whether an analogous two-step compatible rule exists across multiple growth levels. Alternatively, identify the smallest state augmentation (a seam/phase memory) that makes Pi preservation meaningful without blocking all descendants.
