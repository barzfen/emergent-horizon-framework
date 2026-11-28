# EHF Observer Compatibility Audit 08

28 October 2026 · Barry Fensom research collaboration

## Question and outcome

Within the closed odd-gap dimer family, does retaining legal-move activity remove the need to know arrangement? No. For two excess gap units we obtain a complete all-size classification: the minimal activity-retaining predictive state is their cyclic separation. Its refinement depth is unbounded. Beyond that family, finite probes still find mergers of different geometric shapes.

These are mathematical results about the specified stochastic binary-ring model. No physical identification or novelty claim is made.

## Model and scope

Take r >= 2 one-dimers `11`, with cyclic zero gaps g_i = 3 + 2h_i, h_i >= 0, and total H = sum h_i. Then n = 5r + 2H, k = 2r, and B = 2r. Audit 06 proved this family closed under admissible nontrivial length-four reversals. Each move transfers one h-unit to an adjacent gap. With p occupied coordinates, there are d = 2p legal start events. Choose these events uniformly, including multiplicities. H = 0 is frozen.

We quotient rotations and reflections, without exchanging colours. Within each fixed (r,H), refine the observer p (equivalently d); n,k,B are constant. Refinement splits states when their probabilities to current classes differ. The terminal partition is the coarsest strongly lumpable partition retaining this observer, not a claim about every notion of predictive equivalence.

## Theorem: complete H = 2 classification

Let m = floor(r/2). There are exactly m+1 geometric states:

- D_0: both units occupy the same gap, so p=1 and d=2.
- D_j, 1 <= j <= m: units occupy two gaps at minimum cyclic distance j, so p=2 and d=4.

The exact legal-event kernel is a path:

* D_0 -> D_1 with probability 1.
* For 1 <= j < m, D_j -> D_(j-1) and D_(j+1), each with probability 1/2.
* If r is even, D_m -> D_(m-1) with probability 1.
* If r is odd, D_m -> D_(m-1) and D_m, each with probability 1/2.

This includes r=2 and r=3; multiplicity matters at r=2 because the two directions reach the same neighbour.

**Proof of dynamics.** When both units coincide, either direction creates an adjacent pair. When distinct, each occupied coordinate supplies two events. Away from the far endpoint, two events shorten separation and two lengthen it. At the antipodal endpoint of an even cycle all four events shorten separation. For odd cycles two events exchange which arc is shorter, leaving minimum separation unchanged, and two shorten it. These exhaust all events by the odd-gap transport theorem.

**Proof of minimality and depth.** Initially D_0 is distinguished by p=1, while D_1,...,D_m share p=2. For m>=2, only D_1 in the latter class can reach D_0 in one step. Each subsequent refinement separates exactly the next distance state: the remaining farther states have no transition to any already separated state, while the nearest remaining one does. At round m-1 every state is separate. Thus the exact depth is floor(r/2)-1, with depth zero when m=1. No coarser partition retaining activity is strongly lumpable.

Consequently, there is no size-independent bound on refinement rounds even after activity is retained. A single integer distance still gives a simple exact coordinate: unbounded refinement depth does not imply no simple rule exists.

For attempted-position sampling A, Audit 07 gives A = (1-d/n)I + (d/n)K. Because each refinement class retains d, exactly the same partitions and depth apply to A. Transition probabilities remain different.

## Concrete witness

For r=8, H=2, n=44, k=16, B=16, compare separation 3 with separation 4. Both have four legal moves and the same gap-length multiset: two gaps of length 5 and six of length 3. Nevertheless, under K the probability of p=1 after three steps is 1/8 from separation 3, and zero from separation 4. These states first separate in refinement round 3. Under A the corresponding probabilities are 1/10648 and zero, because all three required moves have directional probability 2/44.

This witness shows that activity and even the complete unordered gap-length list do not determine future activity. Cyclic arrangement matters.

## Computation and remaining exceptions

Exact rational refinement was run for every r=2,...,9 and H=0,...,7 (64 sectors), plus H=2 at r=10,...,40 (31 sectors). Total: 95 sectors and 2,241 geometric states. H=2 matches the theorem for all 39 tested r values, reaching n=204 and depth 19. This is a targeted family computation, not a census of all binary rings up to length 204.

An independent verifier constructed the actual binary rings and reversed indexed windows. It checked all 14,598 legal start events, compared their complete target multiplicities, checked orbit coverage against the stars-and-bars count, and verified every exact refinement step and terminal stability. It also independently checked the H=2 path probabilities.

Only four sectors in this finite rectangle retain non-geometric mergers:

| r | H | Ring length | Geometric states | Predictive classes | Depth |
|---|---|---|---|---|---|
| 4 | 4 | 28 | 8 | 7 | 1 |
| 5 | 5 | 35 | 16 | 13 | 1 |
| 6 | 6 | 42 | 50 | 35 | 2 |
| 7 | 7 | 49 | 133 | 85 | 3 |

For example, at (r,H)=(4,4), h=(0,0,2,2) and h=(0,1,0,3) are not related by rotation/reflection, yet belong to the same terminal activity-retaining class. They even have different unordered gap lengths. In fact their entire next-geometric-state distributions coincide: both move to (0,1,1,2) with probability 1/2 and (0,0,1,3) with probability 1/2, using canonical rotation/reflection representatives. Their current activity also agrees, proving their future activity laws agree. The exact certificate confirms the coarsest partition.

The fact that all four exceptions have H=r is a finite observation, not a theorem that exceptions occur only there. This is the next structural question worth investigating. No complete classification for arbitrary r,H has been proved here.

## Reproduction

Run `python3 probe.py`, followed by `python3 verify.py`. Both use only the Python standard library. `draw.py` additionally uses matplotlib. `certificates.json` records all states, transition multiplicities and refinement histories. `results.json` gives the census; `validation.json` reports independent checks. Audits 06 and 07 supply the prior general transport and time-change theorems referenced above. This audit has not been published to GitHub.
