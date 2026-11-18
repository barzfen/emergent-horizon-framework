# Comparison networks and emergent cycles

Admissible comparison is the chosen primitive data of the framework. This research branch asks which comparison relations and local event rules can generate a Hamiltonian cyclic order, and what that order lets an observer reconstruct.

## Studies

| Study | Result |
| --- | --- |
| [Local swaps produce one cycle](#can-a-comparison-network-generate-a-single-cycle) | One swap per tree edge produces a single directed successor cycle. The output and the tree recover the order of intersecting swaps. |
| [Tree shape and the order of swaps](branch-shape-order.md) | A shape-based convention resolves distinguishable branches. Exact symmetries block a choice on the individual sites, while all tie choices give one output up to tree symmetry under a fixed ranking. |

## Next questions

1. Test whether changing the comparison network by growth preserves existing local orders, and identify the smallest cases where order changes or new ties appear.
2. Work out what the comparison relation can retain when the network has loops. Test whether a local rule can select merging events without already knowing global components.
3. Compare candidate rules on inequivalent rankings and on observations that identify different amounts of microscopic information.

## Can a comparison network generate a single cycle?

**Date** 18 November 2026, Australia/Brisbane  
**Status** Known transposition construction, an explicit observer recovery proof, and exact finite checks.  
**Context** Admissible comparison is the chosen primitive data of the framework. The [foundations map](../CONNECTIONS-01.md) identifies the Hamiltonian-cycle representation as a specific EHF construction. This probe asks which input data suffice to reconstruct a cyclic order.

### A tree and a local swap

Take a finite tree $T$ on $n\ge 2$ sites. Give each site a distinguishable token so that the final position of each initial token can be read. A tree edge permits its two endpoints to exchange tokens. Apply each edge swap exactly once, in any order. Write $\sigma(v)$ for the final site of the token initially at $v$. The net map $\sigma$ is a permutation. Its successor relation $v\to\sigma(v)$ is a single directed cycle.

To see this, start with the identity permutation, with one singleton cycle per vertex. At every prefix the used edges form a forest. The next tree edge connects two different components of this forest, hence two different current permutation cycles by induction. Multiplication by the next transposition joins those two cycles. Together the $n-1$ swaps leave one cycle on all $n$ sites. This is a standard fact from the study of minimal transposition factorizations. [József Dénes, 1959](https://real.mtak.hu/200901/) · [Ian Goulden and Alexander Yong, 2002, §2](https://uwaterloo.ca/math/sites/default/files/uploads/documents/gyongjcta2002.pdf).

For example, the star with hub 0 and leaves 1, 2 and 3 admits swaps $(0,1),(0,2),(0,3)$. Taken in that order they give $0\to1\to2\to3\to0$ as the final-position map. The step $1\to2$ summarizes the token's travel $1\to0\to2$ during the round. The star itself has three vertices of degree one and admits no Hamiltonian tour on its own edges. Here the single cycle belongs to the *derived successor relation*. The [EHF Hamiltonian-cycle search series](../../hamiltonian-cycle/README.md) instead tracks routes that use the supplied graph edges.

### What can an observer reconstruct?

At each vertex, supply a linear order on its incident swaps. Every such assignment on a tree can be realized by some overall schedule. Remove a leaf, realize the reduced orders inductively, and insert the leaf edge among the already ordered edges at its remaining endpoint. There are no other constraints involving that edge. Local edge orderings and their realizability more generally are studied by [Nikos Apostolakis, *A Duality for Labeled Graphs and Factorizations with Applications to Graph Embeddings and Hurwitz Enumeration*, 2024, §2](https://doi.org/10.1216/rmj.2024.54.631).

Any two schedules satisfying the same local orders give the same permutation. Indeed they are connected by exchanges of adjacent incomparable events. One can bring the first event of the target schedule to the front, then repeat on the remaining events. Any two incomparable swaps have disjoint endpoints and commute.

Conversely, given the tree and the directed cycle, all local orders can be recovered. Remove a vertex $v$. Let $B_1,\ldots,B_d$ be the components of the remaining tree, named for this proof in the order their edges at $v$ were used. At the first incident swap, the token initially at $v$ goes into $B_1$. Exactly one token enters $v$ from $B_1$ and then waits for the next incident swap, which carries it to $B_2$. This continues until a token from $B_d$ enters $v$ at the last incident swap. Every swap inside a branch stays inside that branch, and each branch has just one exchange with $v$. Thus the final directed cycle read from $v$ visits each branch as a consecutive block, in the order $B_1,\ldots,B_d$. Reading the block order gives the local incident orders. In particular, the number of distinct directed successor cycles obtainable on the fixed, individually distinguished sites of $T$ is

$$
\prod_{v\in V(T)}\deg_T(v)! .
$$

The induced order of events at a shared site survives. The interleavings of disjoint events that respect the same local orders disappear from the full directed successor readout.

### What the bare relation leaves open

The star has a symmetry that permutes its three leaves while fixing the hub. A directed successor selected deterministically from adjacency and equivariantly under relabeling would have to send the hub to a site fixed by every leaf permutation. Only the hub qualifies. An undirected spanning cyclic order would have to select an invariant two-element set of neighbours for the hub. The three interchangeable leaves supply no such set. Consequently a bare tree can determine a family of possible cycles in this model, while selecting one requires information that breaks this symmetry.

The experiment supplies persistent site identity, a swap law, and one application per edge. The tree condition guarantees that every event merges two cycles. On a triangle, applying all three swaps leaves two permutation cycles. On a general connected graph one can recover a merging construction by accepting an edge only when it joins two disconnected components of the previously accepted edges. The accepted edges span a tree and the same proof applies. This filter uses component information, and the probe leaves its local implementation open.

### Reproduction

Run `python3 research/foundations/comparison-to-cycle/check_comparison_cycles.py` from the repository root. Python's standard library suffices. The verifier checked every edge order on every labelled tree of orders 2–6. It verified 158,623 schedules on 1,441 trees, recovered the local incident orders and checked the product formula for each tree. The explicit controls cover the star, commuting disjoint swaps and the extra-edge triangle.

The physical interpretation remains open. This construction demonstrates a route from local comparison events to an effective cyclic order, and specifies what event information still has to be supplied or reconstructed. It makes no claim of mathematical priority over the edge-ordering and factorization literature.

*AI assistance covered the formulation, proof write-up and finite checks. We inspected the cited paper sections and the Dénes archive abstract.*
