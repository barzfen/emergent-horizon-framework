# EHF-REV-04 — Local reconnection by triangle slides

5 November 2026 (Australia/Brisbane). Research direction by Barry Fensom, with implementation and analysis assisted by ChatGPT.

All 76 LR4 transitions that cross short-move components on the retained nine-vertex carrier admit a sequence of six reversible triangle slides. Every single-edge edit preserves connectivity and a same-bit neighbour for each vertex. Intermediate graphs have maximum degree three and can branch. The carrier's Hamiltonian-cycle and Pi conditions apply at the start and finish.

## Models and scope

The input is the 96-cycle MICRO/Pi carrier from [REV-02](../rare-channel-02/README.md). It has 48 LR2 edges, 112 LR3 edges and 88 LR4 edges. Of the LR4 edges, 76 cross components of the LR2/LR3 subgraph. [REV-03](../assembly-gate-03/README.md) counted that obstruction and kept a final atomic reversal.

This probe treats adjacency in the **current** graph as the geometry for local edits. The fixed vertex bits travel with their labels. At each edit the graph must stay connected, each vertex must keep at least one same-bit neighbour, and degree must stay at most three. Pi is defined for the completed cycles. Intermediate branches and temporary edges expand the allowed graph states.

### Direct four-edit control

For each directed transition, enumerate all 24 orders of the two source-edge cuts and two target-edge joins. For a join, record the distance between its endpoints immediately before the join. Cuts in this control are tested for state admissibility, without imposing a distance bound on the remaining route. The minimum join radius is the smallest possible maximum distance over a valid schedule.

The minimum direct join radius equals the reversal's minimal support on this carrier. Both prospective joins have that distance in the initial cycle, and cuts alone cannot shorten the distance before the first join. Adding both target edges first attains the bound. The four endpoints are distinct, so degree is at most three, and every intermediate graph contains the source or the target cycle. That order can temporarily use two extra edges.

The proposed cut–join–cut–join order succeeds in both directions for 52 of the 76 blocked edges. Where it succeeds, its final join spans eight hops because the preceding graph is a connected nine-vertex path.

### Triangle slides

Given existing edges a–b and b–c, add the missing edge a–c and then cut a–b. Both edits are supported by a two-edge route. The route for the addition is a–b–c, and the route remaining after the cut is a–c–b. The intermediate triangle ensures the cut preserves connectivity. The reverse slide uses that same intermediate triangle.

Check degree and same-bit neighbours after both edits. The addition can only improve same-bit adjacency. The subsequent cut requires that a and b still have a same-bit neighbour. Each slide begins and ends with nine edges and uses one extra edge in between.

| Carrier edge class | Edges | Minimum direct join radius | Alternating schedule feasible in both directions | Minimum triangle slides |
|---|---:|---:|---:|---:|
| LR2 | 48 | 2 | Included in short total below | 2 |
| LR3 | 112 | 3 | Included in short total below | 4 |
| All short edges | 160 | 2 or 3 | 152 | 2 or 4 |
| Blocked LR4 | 76 | 4 | 52 | 6 |
| Other LR4 | 12 | 4 | 12 | 6 |

The slide distances are exact in the defined slide graph for these targets. Breadth-first search out to three slides at each endpoint covers all paths of length at most six because slides are reversible. The shortest intersection gives the minimum. This minimum concerns paired triangle slides, with the specified degree and bit constraints.

## Witness

Start at the cycle (0,1,2,3,4,5,6,7,8), with bit 1 on labels 1,2,3,4. The target is (0,1,2,7,6,5,4,3,8). Pi is the same at both endpoints. There are two binary domains at the start and four at the finish.

| Slide | Add edge | Cut edge |
|---|---|---|
| 1 | 0–7 | 7–8 |
| 2 | 1–7 | 0–7 |
| 3 | 2–7 | 1–7 |
| 4 | 1–3 | 2–3 |
| 5 | 0–3 | 1–3 |
| 6 | 3–8 | 0–3 |

This moves each connection along a chain of neighbours. At every cut, the triangle formed by the preceding join supplies an alternate route.

## Reproduction and limits

Run with Python 3 and keep the REV-02 results at their relative path.

    python probe.py
    python verify.py

[probe.py](probe.py) constructs the direct schedules and the bounded slide searches. [results.json](results.json) records every witness, direct schedule radii and the parent file hash. [verify.py](verify.py) independently replays all 248 witnesses in both directions as 4,288 single-edge edits. It checks degree, connectivity, same-bit neighbours and the two-hop routes for each edit.

The paths are existence certificates selected by a search with a specified destination. The local edits alone leave open how a controller picks the next triangle, avoids unintended completed cycles, and determines a completion rate. The finite census concerns this one carrier and permits intermediate graphs outside the original Hamiltonian-cycle state space.
