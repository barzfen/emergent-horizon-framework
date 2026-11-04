# EHF observer compatibility audit 07: an exact bridge between two sampling rules

28 October 2026

## Main result

Let d(x) be the number of legal nontrivial LR4 **start events** at ring x. If the initial observer retains (n,k,B,d), then the accepted-event and attempted-position kernels produce **the same partition at every refinement round**, and hence the same coarsest strongly lumpable refinement of that observation. This holds at every size, not just in the finite census.

The resulting class labels agree; the transition probabilities generally do not. Adding d alone does not always give immediate closure: refinement may still be needed to predict how the retained variables evolve. Nor is retaining d asserted to be necessary for every common description if the observer only cares about B.

Without retaining d, neither kernel universally gives a finer classification. We have exact examples in both directions: a merger under accepted-event sampling that splits under attempted-position sampling at n=14, and the reverse at n=15.

![Common state description for two kernels](common_description.png)

## The two precisely specified kernels

The state space consists of rooted binary rings with no cyclic 010 or 101. Length-four reversals preserve the number k of ones. B is the number of cyclic monochromatic blocks, with homogeneous states assigned B=1.

**K: accepted events.** Count each start position whose reversal is admissible and changes the rooted word. Choose uniformly among these d(x) events. Distinct starts may give the same target and retain their multiplicity. If d=0, remain at x.

**A: attempted positions.** Choose uniformly among all n start positions. Execute a legal nontrivial reversal; otherwise remain at x. Every step counts as an attempt, including rejected and trivial reversals.

A reversal can change the rooted word while preserving its geometric shape. Such an event still contributes to d. Thus d is not the number of distinct next shapes or the number of distinct next observer classes.

The retained observation without activity information is O=(n,k,B). The enriched observation is O+=(n,k,B,d). These are mathematical observations, not assertions about physically accessible measurements.

## The row-wise identity

At every state x,

    A(x,·) = (1 - d(x)/n) δ_x + (d(x)/n) K(x,·).

For d>0, the probability of acceptance on a uniform attempted position is d/n; conditional on acceptance the target law is K. For d=0, both kernels are the self-loop at x and the identity still holds.

This also describes the waiting convention precisely. In an active state, the number of attempted steps up to and including the next accepted event is geometric with mean n/d. Rejections leave the microscopic state unchanged. The two kernels therefore follow the same accepted-event target law, but count steps differently. At a frozen state there is no next accepted event; K's self-loop is a convention, not a real accepted reversal.

These are discrete mathematical step conventions, not claims about physical time.

## The activity-retaining equivalence theorem

**Theorem.** For the stated K and A, a partition refining O+ is strongly lumpable for K if and only if it is strongly lumpable for A. Starting from O+, the standard exact refinement produces identical partitions at every round, up to arbitrary relabelling.

### Proof

Take two states x,x' in the same class of a partition P refining O+. Their n and d agree. For any target class C of P,

    A(x,C) = (1-d/n) 1{x in C} + (d/n) K(x,C).

Because x and x' share a class, the indicator terms are identical. If d>0, equality of the two A probabilities is equivalent to equality of the two K probabilities. If d=0, both states are frozen, so their class-transition distributions agree under both kernels. This proves the equivalence of strong lumpability.

For the stronger round-by-round claim, assume the current partition refines O+. Within each current class the same argument shows that states have equal K signatures exactly when they have equal A signatures. They therefore undergo identical splits. The next partition still refines O+, so induction applies at every round. The finite refinement procedure terminates and gives the same coarsest stable partition for both kernels.

This argument does not depend on n being small or on a particular colour count. It includes frozen states and event multiplicities. No novelty claim is made for the underlying algebraic identity or refinement argument.

### Recovering both quotient kernels

In a stable activity-retaining class c, write d_c and n_c for its common values. If K_bar is the accepted-event quotient, the attempted-position quotient is

    A_bar(c,e) = (1-d_c/n_c) 1{c=e} + (d_c/n_c) K_bar(c,e).

Thus a single class lookup and one quotient matrix, together with n_c,d_c, specify both reduced processes exactly. They do not predict identical probabilities at equal step counts.

This is a sufficient common description under the requirement to retain d. It is not a proof that the smallest partition stable for both kernels while retaining only O must retain d. For instance, a closed family with constant B may still be lumped under both kernels even if d varies inside it.

## Opposite effects when d is discarded

All four witness rings below have six ones and four blocks. Within each pair the first ring has d=2 and the second d=4.

### Fourteen bits: attempted sampling separates an accepted merger

    x = 00000011100111
    y = 00001110000111

Their run lengths are (6,3,2,3) and (4,3,4,3), starting with a zero run. They share the same final class under K, but belong to distinct final classes under A. Their exact probabilities of having six blocks after three steps are:

| Kernel | From x | From y |
|---|---:|---:|
| Accepted K | 1/9 | 1/9 |
| Attempted A | 1/686 | 1/343 |

### Fifteen bits: attempted sampling merges an accepted distinction

    x = 000000011100111
    y = 000001110000111

Their run lengths are (7,3,2,3) and (5,3,4,3). They are distinct under K but share the same final class under A. The corresponding probabilities are:

| Kernel | From x | From y |
|---|---:|---:|
| Accepted K | 1/9 | 1/18 |
| Attempted A | 4/3375 | 4/3375 |

Equality at one horizon alone would not establish equivalence. Here the full exact stable partitions certify the stated mergers, so all finite future O-sequence distributions agree within each merged class. The displayed unequal probabilities suffice to witness the separations.

These examples disprove either proposed universal ordering of the two O-based partitions as size varies. They do not claim the two partitions are non-nested at one particular fixed size; in this census each size's two terminal partitions are nested or equal.

## Why (n,k,B,d) alone is not always closed

At n=12, compare

    000000110011   and   000011000011.

Both have k=4, B=4 and d=4. Under K, their probabilities of having two blocks next are 1/2 and 0. Under A they are 1/6 and 0. Thus the enriched raw observation still fails closure. The theorem reconciles the subsequent refinement procedures; it does not remove the need for refinement.

## Exact census

We reuse the complete geometric representatives from audit 04 and independently regenerate transitions and activity counts for both kernels. The 21 sizes n=4..24 represent all **271,434 admissible rooted states** across those sizes. Every activity-retaining refinement history agrees between K and A, not merely its final class count.

| n | K classes retaining O | A classes retaining O | Common classes retaining O+ | O+ refinement rounds |
|---|---:|---:|---:|---:|
| 12 | 24 | 24 | 25 | 1 |
| 14 | 42 | 44 | 46 | 1 |
| 15 | 66 | 64 | 66 | 1 |
| 16 | 92 | 92 | 94 | 2 |
| 18 | 195 | 196 | 200 | 2 |
| 20 | 423 | 423 | 427 | 3 |
| 22 | 958 | 958 | 964 | 4 |
| 24 | 2,194 | 2,195 | 2,205 | 5 |

The common description can have more classes because it retains an additional observable. At n=24, raw O+ has 245 classes and still needs five strict rounds to reach 2,205. There are 2,359 geometric shapes at that size.

## Research implication and open questions

We can now account for a specific source of sampling-rule dependence through one exact scalar, d/n. The geometric classification is still incomplete, but once the observer retains the legal-event count, changing between the two step conventions does not create a different refinement problem.

A useful next structural question is how to characterize the common activity-retaining classes directly in run coordinates. The existing odd-gap transfer model supplies a test family: its legal-event count is twice the number of positive gap coordinates, unless it is frozen. Retaining that count asks more of the observer than predicting the constant block count alone.

No conclusion here proves the six-one conjecture, a full all-size classification, temporal memory for every preparation, quantum dynamics or a connection to the nine-point theorem.

## Reproduction and verification

```sh
python3 probe.py
python3 verify.py
python3 witnesses.py
```

These use standard-library Python. `input/` contains the earlier exact geometric representatives and reference accepted-event certificates. `probe.py` independently regenerates both kernels, checks the row-wise identity, computes four refinement histories per size, and saves each comparison certificate. It verifies agreement with the earlier accepted-event refinement.

`verify.py` independently reconstructs transitions using indexed reversal rather than rotation/string reversal. It checks disjoint orbit coverage against a four-state transfer-matrix census, all event counts, all four refinement histories and terminal stability. It confirms identical activity-retaining histories on all 271,434 represented rooted states.

`witnesses.py` computes the displayed three-step probabilities exactly from the saved kernels and checks the final class memberships. `draw.py` creates the visual using matplotlib. JSON results and `manifest.json` retain the evidence and file hashes. This package has not been published to GitHub.
