# Start here — How can a ring rearrange itself?

Imagine nine numbered beads connected in a ring. Every bead is black or white, and each must touch at least one bead of its own colour. We asked what rearrangements are possible under that rule, whether small edits can build a bigger rearrangement, and how a controller might choose those edits without being given a destination.

This guide follows eight experiments in the order we ran them. You can read the whole story on this page and open any experiment for its definitions, code and checks.

## The starting setup

A **Hamiltonian cycle** is our ring through all the numbered vertices, visiting each once before returning to the start. We keep track of which labels are connected. A **length reversal** flips the order along a consecutive stretch of the ring. LR2, LR3 and LR4 refer to stretches of two, three and four vertices.

We use two constraints in different combinations.

| Term | What it means here |
|---|---|
| **MICRO** | Every vertex must have a neighbour of its own colour. The colours stay with the labels as the ring rearranges. |
| **Pi** | Start at label 0 and head toward its smaller-numbered neighbour. Pi is the set of labels at positions 0, 2, 4 and so on. A Pi-preserving rearrangement keeps that set the same. |

For a running example, use the ring in numerical order from 0 to 8. Give labels 1, 2, 3 and 4 one colour, and the rest the other colour. Its Pi is the set {0, 2, 4, 6, 8}. It starts with two colour blocks. One legal LR4 flips the stretch 8, 0, 1, 2 across the end of the written list. It changes the ring into one that can be read as 0, 1, 2, 7, 6, 5, 4, 3, 8. The new ring has four colour blocks, and each block still has at least two vertices. Its Pi is the same.

## Follow the experiments

### 1. Find out which moves the rules allow

We began with short reversals, then allowed every reversal length. The no-isolated-colour rule by itself allowed longer moves. Even with Pi held fixed, the example above shows that a longer move can change the number of colour blocks. When Pi is dropped, the study proves that all valid cycles are connected by the allowed reversals whenever any valid cycle exists. [REV-01 · Which moves are allowed?](all-length-01/README.md)

### 2. Separate what can happen from how fast it happens

We zoomed in on one set of 96 valid rings connected by the full set of tested moves. We assigned longer moves lower rates and measured how long the starting colour-block signal persisted. Slowing those moves made the signal last longer, even though the same rings remained reachable. The rates were inputs to this experiment. [REV-02 · What happens when longer moves are rare?](rare-channel-02/README.md)

### 3. Give a longer move more chances to be interrupted

We introduced a controller that advances along a proposed reversal one step at a time. An interruption can reset it at each step, so moves requiring more steps are less likely to finish. The ring still changes in one operation at the end. We also counted time both with and without the busy intervals and found that the two clocks give different descriptions of the process. [REV-03 · Can interruptions make longer moves rarer?](assembly-gate-03/README.md)

### 4. Build the rearrangement from nearby edits

On the 96-ring set, 76 LR4 transitions cross between regions that LR2 and LR3 alone cannot connect under the original cycle rules. We allowed the graph to branch temporarily. In a **triangle slide**, two vertices that share a neighbour are joined, then one edge of the triangle is removed. The two remaining edges keep a route open. Search found six-slide paths for all 76 transitions, preserving connectivity and a same-colour neighbour at every edit. The search was given the destination. [REV-04 · Can nearby edits do the whole rearrangement?](local-reconnect-04/README.md)

### 5. Let the controller choose its slides

We gave the controller a small memory. It marks the connection created by the first slide and favours continuing to move that connection without immediately undoing the last step. From the example ring, this raised the chance of first closing at either of two blocked LR4 targets within six slides from about 4 to 18 per million. Many other closures changed Pi, and many graphs remained open. [REV-05 · What does remembering a connection change?](tagged-controller-05/README.md)

### 6. Give it a local rule for which connections fit

We gave each vertex a second tag, recording whether it started at an even or odd position. The controller uses these tags to screen proposed joins and checks the order of the neighbours at vertex 0 when relevant. On a completed odd ring there must be a seam where the alternating tags meet. These local checks put that seam in the correct place for Pi.

On the same starting ring and six-slide window, the rule raised blocked LR4 returns to about 468 per million. Every completed cycle kept Pi, as the rule guarantees. About 39% of runs were still open at the cutoff. [REV-06 · How can local checks preserve Pi?](pi-closure-06/README.md)

### 7. Try the same rule from every ring in the test set

The first controller test started from one ring. We then tried all 96 starting rings and checked both directions of all 76 blocked LR4 transitions. The original triangle slides can reach all 76 without closing another ring along the way. The local seam rule leaves 48 of those pairs reachable within six slides. The exact chances vary widely across the reachable pairs. This separates routes the rule allows but rarely chooses from routes it blocks within the test window. [REV-07 · Does the rule work across the test set?](carrier-audit-07/README.md)

### 8. Follow the open graphs until the search runs out

We removed the six-slide cutoff and searched every reachable graph. The 28 missing pairs all had longer routes, taking 10 to 30 slides at minimum. One connected region of open graphs touches all 96 completed rings. It lets any one of those rings reach any other without completing a different ring in between. The search establishes that a route exists. Its probability depends on the controller's choices along the way. [REV-08 · Where do longer paths lead?](exhaustive-returns-08/README.md)

## Where the series stands

The experiments give explicit paths from short graph edits to longer rearrangements, and one controller that preserves a supplied position constraint when a ring closes. The controller starts with an anchor and parity tags, and the experiments serialize its moves. The first two controller comparisons use one starting ring. The seventh experiment covers the 96-ring set. All three measure probabilities within six slides. The eighth experiment settles reachability on this set without a cutoff. Longer-run probabilities and other sets of rings remain open.

For the wider Emergent Horizon Framework and how this series connects to its other work, see the [foundations map](../../research/foundations/CONNECTIONS-01.md).
