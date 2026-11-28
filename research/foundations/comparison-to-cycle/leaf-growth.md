# What does one new leaf do to an existing cycle?

**Date** 18 November 2026, Australia/Brisbane  
**Status** Exact projection and locality theorems, sharp examples and finite verification.  
**Setup** Grow the [comparison-to-cycle model](README.md) by attaching one fresh leaf to an old site. Keep every old site identifiable between parent and child. At each site, rank incident branches by size, with their canonical rooted shape code deciding among equal sizes. Identical codes remain tied. This is one of the conventions discussed in [the branch-shape study](branch-shape-order.md).

## Restricting the history and recomputing the ranks

For either tree, each total resolution of the local ranks gives one directed successor cycle. Define deletion of the new site by linking its predecessor directly to its successor in the child's directed cycle. This leaves a directed cycle on the original sites.

**Projection law.** Deleting the leaf from the child cycle gives the same result as omitting the leaf swap from that particular schedule. To see this, let $a$ be the attachment site, $z$ the fresh leaf, and $U,V$ the old swap products before and after the leaf swap. The child product is

$$
V(a\,z)U=(V(a)\,z)\,VU,
$$

since $V$ fixes $z$. The extended old product $VU$ fixes $z$. Multiplication by $(V(a)\,z)$ splices $z$ immediately before $V(a)$ in its directed cycle. Deletion removes that splice. This proof is independent of how the schedule was chosen.

**Criterion for rebuilding a cycle by the ranking rule.** Compare the original family of permitted cycles to the family obtained by recomputing ranks on the child, running its swaps, and deleting its new site. The families coincide exactly when the status of every old pair of incident edges is preserved as earlier, tied, or later. They are disjoint exactly when some old pair is strictly reversed. Otherwise they overlap with a change in at least one family.

For the proof, the [tree swap correspondence](README.md#what-can-an-observer-reconstruct) identifies each family with the product of its permitted local total orders. Every refinement of the restricted child ranks extends to a full refinement, since the new edge at $a$ can be inserted at its ranked position. Two weak orders have a common total refinement if they have no opposite strict comparisons. In that case, sorting by the pair of old and new ranks in lexicographic order respects both. The projection law transports this local criterion to the cycle families.

## How far and how many?

At $a$, the old branches retain their sizes and shapes. At any other site $v$, only the branch pointing toward $a$ changes. If its old size is $s_v$, it grows to $s_v+1$. Therefore an old pair can change at $v$ only when another branch has size $s_v$ or $s_v+1$.

**Sharp bound.** On a parent with $n$ sites, all affected vertices lie on one path from $a$. At most

$$
\lfloor \log_2(n+1)\rfloor-1
$$

sites can have any old comparison change. This counts a new or broken tie as well as a strict reversal and applies to any fixed shape tie-break within each size.

Root the tree at $a$. An affected site $v$ has a child branch of size at least $s_v$, so $2s_v+1\le n$. Its descendant subtree therefore has more than half of the old vertices. Such heavy descendant subtrees are nested and their roots lie on one path. If another affected site lies farther along that path, its heavy subtree lies in a heavy child branch of $v$. Any heavy child of $v$ has size at least $s_v+2$: its size $t>n/2$ and $s_v+t+1\le n$ imply $t-s_v\ge2$. Thus the shape that changes comparison with the growth-facing branch belongs to a different child branch, with at least $s_v$ vertices. Those vertices and $v$ itself join the growth-facing side at the next affected site. The successive values satisfy $s_{\rm next}\ge2s_v+1$, starting from $s_v\ge1$. With $k$ affected sites this gives $s_{\rm last}\ge2^k-1$, yielding the bound.

To attain it, start at $a$ with one vertex, designated the tip. Add a new tip connected to the old one and, at this new tip, attach a copy of the entire previous tree by its copied tip. Repeat $k$ times. Each introduced tip has two equal-shaped branches, and growth at the original $a$ breaks that tie at all $k$ tips. The parent has $2^{k+1}-1$ sites. For any parent size between consecutive such sizes, append a path at the last tip to reach that size. The witnessed branch pairs keep their shapes and the bound stays the same.

**Unbounded distance.** For an integer $d\ge4$, take a hub with three arms of lengths $1$, $2$ and $2d-3$. Attach the fresh leaf to the tip of the long arm. At the site $d$ edges from that tip, the old branches both contain $d$ vertices. The tip-facing branch is a path, which has $d$ opening parentheses before its first closing one. The hub-facing branch has $d-1$ openings before its first close. Since an opening parenthesis ranks before a closing one, the tip-facing branch comes first. After growth it is larger and comes second. Both trees are asymmetric, so there are no equal branch ties to resolve. A distant strict reversal therefore occurs even when each ranking specifies a single directed cycle.

## Smallest strict reversal and finite checks

The smallest parent with any strict reversal has six sites. Use the path `a—b—v—c—d—e` and attach the new leaf at `b`. At `v` the branch toward `b` originally has size two and comes first. After growth it is a rooted fork of size three. It comes after the opposite rooted path of size three under the parenthesis-code tie-break. For a strict reversal, size $s$ versus size $s$ requires two different rooted shapes of the same size, so $s\ge3$ and $n\ge7$. Size $s$ versus size $s+1$ requires two different rooted shapes of final size $s+1$, so $s+1\ge3$ and $n\ge6$. This proves minimality.

| Cycle families after projecting the child to the parent sites | Inequivalent attachments through 14 original sites |
| --- | ---: |
| Identical | 30,452 |
| Overlap with a change | 12,667 |
| Disjoint | 10,153 |
| Total | 53,272 |

An attachment type is an orbit of the original site's position under the parent tree's automorphisms. The verifier runs the same ranking in every case, checks 1,205 actual cycle projections, and enumerates both families exactly for all 85 attachment types through seven parent sites. Explicit examples verify distant strict reversals through distance 64 and sharpness through seven affected sites. Run `python3 research/foundations/comparison-to-cycle/check_leaf_growth.py` from the repository root.

This experiment compares two snapshots of the comparison relation under the same supplied ranking, with the old sites identified. The projection law preserves an inherited schedule. The disjoint cases show exactly where applying the snapshot ranking again forces a different cycle. Whether the network can generate a usable ordering rule that respects accumulated growth history is the next question.

*AI assistance covered the mathematical derivations, finite verifier and write-up.*
