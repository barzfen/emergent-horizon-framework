# EHF Observer Compatibility Audit 09

## Exchange symmetry and the three-gap theorem

29 October 2026 · Barry Fensom research collaboration

**Outcome.** We prove why balanced odd-gap families have hidden mergers, and prove that non-geometric mergers exist at every balanced size r=H>=4. We also obtain a complete classification whenever there are at most three gaps or at most three movable units. The stronger assertion that the exchange symmetry explains every merger at arbitrary r,H remains a conjecture. It matches every case tested here.

These are exact results about a specified stochastic combinatorial model. No novelty claim, physical interpretation, or identification with the substrate of reality is asserted.

## 1. Definitions

The original admissible binary ring contains r>=2 one-dimers `11`, separated by zero gaps

    g_i = 3 + 2h_i,   h_i >= 0,   H = sum_i h_i.

Its length is n=5r+2H, with k=2r ones and B=2r monochromatic runs. Audit 06 proved that this family is closed under admissible nontrivial length-four reversals. Each legal event transfers one unit from a positive h_i to one of its two cyclic neighbours. There are d(h)=2p(h) legal start events, where p(h) is the number of positive coordinates. Both directions count separately, including when r=2 and they reach the same neighbour.

The principal kernel K chooses uniformly among legal events, retaining multiplicity. H=0 is frozen. We identify rotations and reflections, but do not initially identify any further shapes. At fixed r,H, the observer is p, equivalently d; n,k,B are constant. “Predictive classes” here means the coarsest strongly lumpable partition refining this observer. This is not a claim that strong lumpability is equivalent to every alternative notion of stochastic observational equivalence.

## 2. Encoding theorem: gaps become separators

Encode h by the cyclic word

    E(h) = 0 1^(h_0) 0 1^(h_1) ... 0 1^(h_(r-1)).

Here **0 denotes a separator and 1 denotes one movable gap unit**. These are auxiliary symbols, not the bits of the original ring. The encoded word has length r+H, with r zeros and H ones.

This is a bijection between geometric h-shapes and binary words with these counts modulo rotation/reflection. To invert it, choose any zero and count successive runs of ones between zeros. Choosing another zero rotates h; reflecting the encoded ring reverses the cyclic order of h, up to rotation. These are exactly the geometric identifications already allowed.

**Move correspondence.** Transfer of a unit to the next gap is exactly a swap of the adjacent `10` at the intervening separator. Transfer to the previous gap is a swap of the adjacent `01`. Each positive h_i has two such boundary edges. Thus legal events correspond one-to-one to swaps of unlike neighbouring symbols in E(h). The correspondence preserves event multiplicities, including transitions that return to the same geometric shape.

Therefore K is exactly the kernel that chooses uniformly among unlike adjacent pairs in this auxiliary binary ring and swaps the pair.

## 3. The exchange theorem

For r,H>=2 define T by exchanging every 0 and 1 in E(h), then decoding back into gap coordinates. It maps the (r,H) family bijectively to the (H,r) family.

The map has three exact properties:

1. T is an involution on geometric shapes: T(T(h))=h.
2. It preserves p. In a cyclic binary word containing both symbols, the number of one-runs equals the number of zero-runs. Both equal half the number of unlike neighbouring pairs.
3. It conjugates the complete legal-event kernel:

    K_(r,H)(h,g) = K_(H,r)(T(h),T(g)).

**Proof.** Symbol exchange commutes with every indexed adjacent swap and preserves the set of unlike adjacent pairs. Hence it gives a bijection of legal events, with the same normalization 2p. Decoding and geometric quotienting preserve the resulting transition multiplicities. This proves all three properties.

### Balanced consequence

When H=r, T stays inside the same fixed family. Its orbits {h,T(h)} form an activity-preserving strongly lumpable partition. Explicitly, for every T-orbit C,

    sum_(g in C) K(h,g) = sum_(g in C) K(T(h),g).

Thus no refinement starting from p can separate h from T(h): by induction, T-related states have the same label at every round. They have identical laws for every finite sequence of future activity observations.

This symmetry also preserves the original attempted-position kernel A=(1-d/n)I+(d/n)K within a balanced family, since n and d agree. Away from balance, T still conjugates K, but generally changes the original ring length from 5r+2H to 5H+2r, so the original attempted-position probabilities need not agree.

### Why balance matters—and the precise limit of this proof

For H!=r, this particular exchange changes the number of separators and units. It therefore maps to a different family, not another state of the same fixed (n,k,B) sector. This proves that the exchange mechanism creates within-family partners only at balance. **It does not prove that every possible merger must come from this mechanism.** A general necessity proof is still missing.

This is also different from flipping the bits of the original physical-model ring. At balance the original ring has n=7r and k=2r, so its zero and one populations are not equal.

## 4. Nontrivial mergers at every balanced size

For every r>=4, consider the two r-coordinate vectors

    a = (0 repeated r-2 times, 2, r-2),
    b = (0 repeated r-3 times, 1, 0, r-1).

Both have total H=r and activity p=2. The code of a is

    0^(r-1) 11 0 1^(r-2).

Its symbol complement, decoded cyclically, is b up to rotation/reflection. Therefore T(a)=b. But max(a)=r-2 and max(b)=r-1, so they cannot be rotations or reflections of one another. They are distinct geometric shapes with identical future activity laws. This proves the existence of a non-geometric merger for every r=H>=4.

At r=H=2 and r=H=3, there is no nontrivial exchange pair: the two and three geometric states, respectively, are already distinguished by p. The three-gap proof below also covers the latter case.

**Smallest example:**

| Quantity | a | b |
|---|---|---|
| Gap units h | (0,0,2,2) | (0,1,0,3) |
| Original zero-gap lengths | (3,3,7,7) | (3,5,3,9) |
| Original ring length | 28 | 28 |
| Legal events d | 4 | 4 |

The shapes differ, but each moves with probability 1/2 to (0,1,1,2) and with probability 1/2 to (0,0,1,3), in canonical geometric coordinates. The general symmetry proof applies even when partners do not have identical individual next-state rows.

## 5. A general lower bound on predictive information

Future activity reveals the earliest time at which an activity level can be reached with positive probability. For 1<=s<=r, let D_s(h) be the fewest legal moves needed to reach p<=s. Then

    D_s(h) = min_(S subset C_r, |S|=s) sum_i h_i dist_(C_r)(i,S).

In words: choose s receiving sites to minimize the total distance all units must travel to reach one of them. This formula applies for H>0; its value is zero if the current support already fits in s sites.

**Lower bound.** Label the units temporarily. Every legal move transports one unit along one edge. In any final configuration supported on S, each initial unit must travel at least its distance to S. Summing gives the bound.

**Upper bound.** Choose a minimizing set S and send each unit along a shortest path to a nearest member of S. Every required transfer is legal because its source contains the unit being transported. There is no occupancy cap and no restriction on temporary support. The total number of moves is the displayed sum, and the final support is contained in S.

All legal moves have positive K probability. Hence D_s is the first t for which P_h(p_t<=s)>0. Any two states in the same activity-preserving strongly lumpable class must have identical D_s for every s. The same first-reachability times hold under A, since it has the same nontrivial support and merely adds waiting.

## 6. Complete three-gap classification

**Theorem.** For r=3 and every H>=0, the coarsest predictive partition retaining p is exactly the geometric shape partition. There are no further mergers.

**Proof.** H=0 is a single frozen shape. For H>0, write the coordinates in sorted order a<=b<=c, with a+b+c=H. On a three-cycle every pair of sites is adjacent, and the dihedral group realizes every permutation. Thus (a,b,c) uniquely identifies the geometric shape.

The first-reachability distances are

    D_2 = a,
    D_1 = H-c = a+b.

To empty a site, at least a units must leave some site; emptying a smallest site attains the bound. To gather all units into one site, at least H-c units must move; transferring the other two piles directly into a largest pile attains the bound.

Therefore future activity determines

    a = D_2,   b = D_1-D_2,   c = H-D_1.

Distinct geometric shapes have different recoverable data and cannot belong to the same strongly lumpable class. Conversely, geometric symmetry itself always gives a strongly lumpable quotient. This proves equality of the partitions for every H.

**Dual corollary.** For H=3 and every r>=2, the exchange theorem maps the problem to the three-gap family. Therefore the geometric shape partition is again the coarsest predictive partition.

Together with Audit 08's two-unit theorem, its two-gap dual, and the trivial H=0,1 cases, this completes the classification whenever min(r,H)<=3 (with r>=2).

### Why this is not yet a proof for every number of gaps

First-reachability distances can coincide while probabilities differ. At r=4,H=5, the distinct states (0,0,2,3) and (0,1,0,4) both have

    (D_1,D_2,D_3,D_4) = (2,0,0,0).

They even have the same one-step activity distribution. Yet their probabilities of p=1 after two moves are 1/16 and 1/8, respectively. They separate at refinement round two. Thus these distance invariants are sufficient for the three-gap proof but are not a complete general invariant.

## 7. Exact computation and independent verification

The main census covers every r=2,...,12 and H=0,...,12: 143 sectors and 240,748 geometric states. The predicted partition uses individual shapes when r!=H, and the exchange pairs {h,T(h)} when r=H. Exact rational refinement agrees with this prediction in every sector.

| Balanced r=H | Shapes | Predictive classes | Refinement depth |
|---|---|---|---|
| 4 | 8 | 7 | 1 |
| 5 | 16 | 13 | 1 |
| 6 | 50 | 35 | 2 |
| 7 | 133 | 85 | 3 |
| 8 | 440 | 257 | 4 |
| 9 | 1,387 | 765 | 5 |
| 10 | 4,752 | 2,518 | 6 |
| 11 | 16,159 | 8,359 | 7 |
| 12 | 56,822 | 28,968 | 8 |

All 132 nonbalanced sectors in this rectangle have no non-geometric mergers. No asymptotic claim is inferred from the apparent depth pattern in the table.

The independent verifier does not import the probe. It constructs the encoded binary words, checks geometric orbit coverage against binomial coefficients, swaps actual adjacent symbols, checks complete event multiplicities, verifies each exact refinement step and terminal stability, and independently constructs the balanced exchange involution. In the main census it checks 2,745,162 swap events, covering 10,400,495 rooted encoded words by orbit counts. It additionally reverses actual original-ring windows for all states with r,H<=8 and selected states in every larger sector: 2,772 original-ring states and 20,702 legal LR4 events. Original LR4 checks are explicitly sampled beyond the smaller rectangle; the encoded-kernel checks are exhaustive throughout.

A further 96 sectors extend the proved thin families: (r,H)=(3,13),...,(3,60) and (13,3),...,(60,3), adding 14,008 geometric states. These also match the theorem. Breadth-first shortest-path calculations independently verify both three-gap distance formulas on all 7,105 shapes for H=1,...,60. The extra sectors receive the same independent encoded-kernel/refinement checks and sampled original LR4 checks, recorded separately in validation_extra.json.

Across both batches: **239 sectors, 254,756 geometric states.** These are targeted family censuses, not a census of all admissible binary rings up to the largest original length tested (306).

## 8. What remains open

The proposed complete classification is:

* If H!=r, every geometric shape is predictively distinct.
* If H=r, the only mergers are the separator/unit exchange pairs.

We have proved that the proposed exchange-orbit partition is always valid, proved that every balanced size r>=4 has a nontrivial pair, and proved completeness for min(r,H)<=3. The general assertion that no further mergers exist for r,H>=4 is still unproved. Matching 254,756 states strengthens the evidence but does not supply that missing necessity proof.

The next substantive target is r=4 with arbitrary H. The two-step example above shows why any proof must retain probability information beyond shortest reachability times.

## Reproduction and files

Run in this directory:

    python3 probe.py --max 12
    python3 verify.py
    python3 thin_families.py
    python3 verify.py --extra
    python3 witness.py

The default verification checks the main rectangle; --extra checks the additional thin-family sectors. The saved main and extra validation files record the disjoint batches described above.

All calculations use the standard library. draw.py additionally uses matplotlib. Each sector certificate contains states, move targets with multiplicities, every refinement labelling, and the predicted exchange partner. results.json and thin_results.json summarize their respective batches. The two-step witness is reproduced in witness.json. Prior audit reports supply the earlier transport and two-unit theorems. This audit has not been published to GitHub.
