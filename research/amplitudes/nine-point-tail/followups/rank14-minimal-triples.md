# EHF-AMP-HOL-BRIDGE-04 — Exact minimum support needed to repair rank-14 tail relations

**Date:** 2026-11-13 (Australia/Brisbane).  
**Status:** exact finite classification at nine points, with full rational source-relation certificates and a separately reproduced rank test. This is a theorem about the **specified nine-point support cuts**, not a new QCD scattering law or evidence of a physical Hamiltonian cocycle.  
**Research direction:** Barry Fensom; derivation, computation and verification assisted by ChatGPT.

## Question and answer

The preceding [two-word audit](rank14-event-pairs.md) found that four rank-14 parity fibres admit two-word repairs, but the cuts with A=(2,5,7) and A=(3,5,7) admit **no** one- or two-word repair. What is the true minimum?

**Answer: exactly THREE excluded words in both remaining fibres.**

| Block A | Original source cut size | Excluded words | KK rank of cut | Source relations | Original residue-image rank | Minimum extra words |
|---|---:|---:|---:|---:|---:|---:|
| (2,5,7) | 324 | 252 | 306 | 18 | 14 | **3** |
| (3,5,7) | 360 | 216 | 342 | 18 | 14 | **3** |

The completed minimum-distance classification across all **six** rank-14 cuts is

| A | (2,5,7) | (2,5,8) | (3,5,7) | (3,5,8) | (4,5,7) | (4,5,8) |
|---|---:|---:|---:|---:|---:|---:|
| Minimum extra words | **3** | 2 | **3** | 2 | 2 | 2 |

The four two-word minima were established in [BRIDGE-03](rank14-event-pairs.md); BRIDGE-04 establishes the remaining two minima.

## Two explicit minimal three-word witnesses

Write each nine-point ordering as a nine-digit word, anchored at label 1. Both examples satisfy the parity-fibre rule and are excluded by the original representative cut (second label > last label). All six individual orderings have **zero signed collision residue**.

### A=(2,5,7)

The three excluded orderings are:

    u = 162374985
    v = 162894735
    w = 169473285

Their KK quotient columns satisfy the **exact** relation

    q(u) - q(v) - q(w) = 0,

where q is the nine-point KK column modulo the span of columns already in the source cut. Its signed-residue lift evaluates to **+1** against the already established one-dimensional missing-target functional L. Adding all three words raises:

    cut:    source words 324, KK rank 306, relation dim 18, residue rank 14
    +three: source words 327, KK rank 308, relation dim 19, residue rank 15

The reconstructed full source KK relation has **135 nonzero word coefficients**, and its residue has 54 nonzero target coordinates. The program verifies every coefficient of the source KK sum cancels and L(residue)=+1.

### A=(3,5,7)

The three excluded orderings are:

    u = 145678923
    v = 163894725
    w = 165894723

Their quotient columns satisfy

    -q(u) + q(v) - q(w) = 0.

The lifted relation evaluates to **−1** under L. The rank accounting is:

    cut:    source words 360, KK rank 342, relation dim 18, residue rank 14
    +three: source words 363, KK rank 344, relation dim 19, residue rank 15

An explicit verified source relation has **123 nonzero coefficients**, with 46 nonzero target-residue coordinates; L(residue)=−1.

For **each witness**, adding any single chosen word or any of its three pairs leaves the target rank at 14. Together with exhaustive exclusion of every one- and two-word repair, this proves minimality.

## Precise general lemma: relative cancellation distance

Let S be a prescribed source-support subspace; let Q map words into the KK coordinate space, and let D be their signed boundary residue. Put

    W = Q(S),    I = D(ker(Q|_S)),

and let L vanish on I but be nonzero on the missing target direction (the target quotient has dimension one at rank 14).

For each excluded zero-residue word e, choose a cut-supported reduction s_e so that the reduced quotient column is

    q_e = Q(e - s_e) ∈ Q(total source)/W.

Define the associated defect scalar by

    ell_e = L(D(e - s_e)).

Although the choices of reductions affect individual coordinates, the value of the *sum* below on a quotient dependence is independent of the choices, because L annihilates I.

A set T of excluded words repairs the missing direction **if and only if** there exist coefficients c_e supported on T such that

    sum_{e∈T} c_e q_e = 0
    and
    sum_{e∈T} c_e ell_e != 0.

Its **relative cancellation distance** is therefore

    d_L(S) = min { |supp(c)| : sum c_e q_e = 0, sum c_e ell_e != 0 }.

This is a standard linear-algebra / matroid-circuit / sparse-codeword formulation, here applied to the explicit EHF rank-14 liftability problem. A missing target space of dimension **one** does not determine d_L: these six source restrictions give **d_L=2 or 3**.

### Why this resembles EHF admissible comparisons

The numbers count **minimum additional admissible configurations** needed to support a relation, not missing target dimensions and not Hamiltonian orbit periods. The rank-14 obstruction is one-dimensional in every fibre, but its **support complexity** is not constant. That is a rigorous example of reconstruction cost depending on available relations.

**Do not confuse** the generic three-words / two-new-KK-directions / one-new-relation dimension count with the unrelated planar **1:2:3 SU(3) colour norm law**. There is no derivation of the latter from the former.

## Exhaustive successful-triple counts

To count all three-word repairs without repeating an enormous matrix elimination for each triple, first contract by the cut KK span, remove zero quotient columns, and group proportional quotient columns. The grouped counts are:

| A | Excluded words | Zero quotient columns | Nonzero projective quotient classes | Repairing classes of 3 | Actual distinct repairing triples |
|---|---:|---:|---:|---:|---:|
| (2,5,7) | 252 | 8 | 214 | 3 | **66** |
| (3,5,7) | 216 | 10 | 153 | 4 | **322** |

The difference between **3 versus 66**, and **4 versus 322**, reflects proportional variants of the same quotient-column class. Since the exact one/two-word audit found no repairs, proportional classes also have proportional defect scalars; choosing different representatives within such a class does not alter whether the triple repairs the rank. The per-class multiplicities are retained in [the exact snapshot](rank14-minimal-triples-results.json).

### Exhaustiveness of the search

The script projects the rational KK quotient columns into three coordinates modulo the prime 1,000,003 using a fixed deterministic seed. A genuinely dependent rational triple **must** remain dependent under this linear modular projection provided denominators are invertible, which the script checks. Consequently this is a **lossless candidate filter**: there may be false positives but never a missed exact rational dependency.

The script checks that no two distinct projective classes become proportional under the chosen projection. Each screened triple is subsequently tested with **exact rational** linear algebra and evaluated under the dual L, and a full residue-image-rank calculation confirms every repairing projective class. This yields three successful classes for A=(2,5,7) and four for A=(3,5,7). Both explicit source-relation certificates are generated afresh and verified term by term.

The modular arithmetic is a filtering optimization, **not** the source of the theorem's exactness.

## Reproduce

From this directory, run:

    python3 rank14_minimal_triples.py
    python3 verify_rank14_minimal_triples.py

The primary script uses only the standard library and imports the existing independently written [signed orientation/remainder module](signed_orientation_bridge.py). It writes a complete [results JSON](rank14-minimal-triples-results.json) including all successful quotient triple classes and the full rational source KK certificates. The committed JSON retains the summary counts and witness metadata; running the script regenerates the larger detailed file.

The second script tests the witnesses by **direct rational KK rank computations**, and independently invokes the previous [two-word exhaustive oracle](rank14_event_pairs.py) to check that no smaller repair is possible. The two verifiers have different internal routes.

## Limitations and next experiment

- This is a complete **minimum support size** result for the six rank-14 nine-point parity fibres, not a closed-form prediction for every future multiplicity or arbitrary cut.
- We have an exact quotient linear-algebra criterion. We do **not** yet have a genuinely local reversal/event rule that predicts which triple of excluded words will work *without* consulting its KK quotient or related relation data.
- The two triple repairs use orderings at distinct positions of label 9, suggesting that strictly local features near the collision are unlikely to suffice on their own. This is a research hypothesis, not a proved impossibility.
- Next measure **certificate sparsity** separately from the number of newly admitted source words, and attempt a support-only or event-labelled rule predicting the difference between d_L=2 and d_L=3. Any proposed rule must be tested on additional cuts not used to construct it.

## Related EHF findings

- [BRIDGE-03 two-word exhaustive audit](rank14-event-pairs.md)
- [Rank-14 dual certificate](rank14.md)
- [Signed reflection and tail support](signed-orientation-bridge.md)
- [Original nine-point theorem and reference-chart reconstruction](../README.md)
- [HOL-06 event-labelled Hamiltonian transport](../../../../probes/reversals/event-groupoid-14/README.md)
