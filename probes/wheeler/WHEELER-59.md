# WHEELER-59 — Root/Rotation Quotient / Measure-and-Entropy Audit

**Date:** 19 October 2026 (Australia/Brisbane). **Status:** PROVED within the specified model, with exact finite checks and one explicitly open entropy question.

**Outcome:** forgetting the root preserves event-uniform Markov dynamics but not the rooted state-uniform rule. Rotation invariance narrows the admissible measures without selecting a unique one. Ordinary majorization fails on rotation classes. An entropy theorem survives with the inherited orbit-size reference measure; ordinary class Shannon monotonicity remains unresolved here.

## 1. What is being identified?

Use the zero-cost binary words and insertion convention of [WHEELER-58](WHEELER-58.md): n≥4, cyclic 010 and 101 forbidden, D cyclic domain walls, and events `(i,b)` inserting b before i, for 0≤i<n. The target is `w[:i]+(b,)+w[i:]`. D is conserved and there are n+D admissible events.

Let π(w)=[w] identify cyclic rotations only. Reflection and bit exchange are **not** identified. An orbit A consists of distinct tuples, with size s(A)≤n; a periodic word can have fewer than n distinct rotations. For example, `000111000111` has s=6, not 12.

The root convention under insertion matters. For i>0, the original first bit stays first; for i=0, the inserted bit becomes first. Rotating the source and moving the insertion gap with it produces the same unrooted target, although the resulting tuple may start at a different place. We require equality of probabilities of **target orbits**, not equality of target tuples under a fixed numerical rotation shift across changing lengths.

A kernel K descends to the quotient when

`Q(A,B) = sum_{v in B} K(w,v)`

is independent of the chosen w∈A. This is strong lumpability of the layer-to-layer kernel. It guarantees a closed quotient Markov law for every initial preparation.

## 2. Event-uniform growth descends exactly

**PROVED.** Rotate a source by r positions. Map each insertion gap to the corresponding rotated gap and keep the inserted bit. This is a bijection on admissible events. Corresponding targets differ only by rotation. Every source representative has the same n and D and hence the same event weight 1/(n+D). Summing over events reaching B proves representative independence.

For a nonhomogeneous word, write its cyclic run lengths as ℓ₁,…,ℓ_D, each at least two. A run of length ℓ_j can be extended by ℓ_j+1 insertion events. Thus the quotient kernel can also be written

`Q(A,B) = [sum over runs j whose extension gives B of (ℓ_j+1)] / (n+D)`.

Repeated or symmetry-related extensions are counted with their multiplicity. The formula is independent of which run is listed first. Homogeneous words have one target orbit with probability one.

Consequently:

- n, N1 and D are unchanged by forgetting the root; their event-uniform macro kernel is the same as before.
- Quotient histories have a consistent probability law for a fixed preparation, by applying π at every step.
- Coordinatewise projection commutes with history truncation. Strong lumpability additionally makes the projected law Markov; consistency alone would not establish this.
- A canonical representative is safe for computing this Q because representative independence has been proved.

This is a theorem about an event-indexed process. It adds no physical clock.

## 3. Rooted state-uniform growth fails the same test

WHEELER-58 proved D+1 distinct rooted successors for D>0. Assigning each such tuple equal probability defines a consistent rooted process, but it does **not** generally descend to rotation classes.

Consider two representatives of the same n=5 cycle:

| Source representative | Measure | P([000111]) | P([001111]) |
|---|---|---:|---:|
| 00111 | Event-uniform | 3/7 | 4/7 |
| 11100 | Event-uniform | 3/7 | 4/7 |
| 00111 | Rooted state-uniform | 1/3 | 2/3 |
| 11100 | Rooted state-uniform | 2/3 | 1/3 |

Both targets represent different N1 values, so this discrepancy survives even that coarser observation.

More generally, under rooted state-uniform growth, for D>0,

`P(insert 1 | w) = (D/2 + w_(n−1))/(D+1)`.

**Proof.** Distinct rooted successors correspond to extending the linear runs, together with one extra boundary insertion when the first and last bits differ. If the first and last bits agree, the root splits one cyclic run into two linear runs. In either case there are D/2 successors inserting 1, plus one precisely when the last bit is 1. Divide by D+1. The homogeneous case is deterministic and is treated separately.

Thus an arbitrary root can affect even the next symbol count. If the root is a physical marker, this is allowed by a model that explicitly retains it. If rotations are intended to represent the same physical state, the unmodified rooted state-uniform rule fails the required representative independence.

This does not invalidate its WHEELER-58 consistency result. A projected history law still exists for any specified rooted preparation. What fails is a universal quotient transition rule independent of that preparation's hidden root information. We do not infer that every particular projected preparation is non-Markov.

## 4. Rotation invariance still does not select a unique measure

There are several coherent alternatives:

1. **Uniform distinct quotient targets:** assign equal probability to each reachable orbit B. The reachable set is representative independent, so this directly defines a quotient kernel. It is not the push-forward of rooted state-uniform growth.
2. **Random re-rooting before each rooted state-uniform step:** choose uniformly among the source's distinct rotations and average their transition laws. This adds a specified operation at every step; randomizing the initial root once is not the same prescription.
3. **Rotation-invariant event weights:** for example, weight an event by q to the length of the cyclic target run containing the inserted bit. Rotation preserves this length and normalization, so this family also descends. q=1 recovers uniform events.

For the source orbit [00111]:

| Kernel | P([000111]) | P([001111]) |
|---|---:|---:|
| Event-uniform | 3/7 | 4/7 |
| Uniform distinct quotient targets | 1/2 | 1/2 |
| Uniform re-rooting, then rooted state-uniform | 7/15 | 8/15 |
| Run-weighted events, q=1/20 | 15/16 | 1/16 |

Each normalized kernel defines a consistent quotient history process with a fixed initial law. Therefore root independence distinguishes the two original candidates, but does not prove uniqueness of event-uniformity. A further sampling or reference-measure principle would be needed.

## 5. Ordinary majorization does not survive quotienting

The rooted event-uniform kernel has column sums at most one, giving the earlier majorization and Shannon theorem. The unweighted quotient kernel need not have that property.

At n=12, D=4, consider target B=[0001110001111]. Its nonzero incoming quotient probabilities are:

| Source orbit representative | Q(A,B) |
|---|---:|
| 000110001111 | 3/16 |
| 000111000111 | 1/2 |
| 000111001111 | 3/16 |
| 000111100111 | 3/16 |

Their sum is **17/16**. The periodic source has orbit size six; each of the other three has size twelve. Its symmetry-related run extensions accumulate at the same target orbit.

Put probability 1/4 on each of these four sources. Then the target B receives **17/64 > 1/4**. The largest output probability exceeds the largest input probability, disproving the first majorization inequality even after zero-padding the vectors to equal length. Thus universal ordinary majorization on rotation classes is **FALSIFIED**.

This is **not** a Shannon-entropy counterexample. For this exact distribution,

`H(source classes)=2 bits`,

`H(target classes)=3.1200657856 bits`.

The column-sum argument and the stronger majorization conclusion fail; that alone does not settle the weaker statement that ordinary Shannon entropy might always increase. That weaker statement is left open in this probe.

## 6. The inherited-reference entropy theorem survives

Let s(A)=|A| be the number of distinct rooted tuples in orbit A. Define

`S_s(P) = -sum_A P(A) log2(P(A)/s(A))`

`         = H(P) + sum_A P(A) log2 s(A)`.

This is entropy relative to the inherited **unnormalized** counting measure s, not ordinary entropy with one unit of reference weight per orbit. It is the maximum rooted Shannon entropy among lifts of P, attained by distributing P(A) uniformly among the s(A) tuples. It is not asserted to be thermodynamic entropy.

**PROVED:** for event-uniform growth, `S_s(PQ) ≥ S_s(P)` for every class distribution P.

For completeness, fix a rooted target of length n+1. Each incoming event is recovered by deleting its inserted bit at one of the n allowed insertion positions, 0,…,n−1. Hence there are at most n incoming events, all with denominator n+D because D is conserved. Its rooted column sum is at most n/(n+D)≤1.

Strong lumpability and this rooted column bound give

`sum_A s(A) Q(A,B)`

`= sum_{v in B} sum_w K(w,v) ≤ s(B)`.

The s(B) here belongs to the next size layer. Ordinary quotient column sums omit precisely these orbit weights.

For a direct entropy proof, lift P uniformly inside each source orbit. The lifted rooted entropy is S_s(P). The rooted entropy theorem makes its output entropy at least S_s(P). Its class marginal is PQ by lumpability, and any rooted lift of PQ has entropy at most S_s(PQ). Combining these inequalities proves the result. The output lift need not be uniform within its orbits.

For an arbitrary actual rooted distribution p with class marginal P, the exact identity is

`H(p)=H(P)+H(rooted tuple | rotation class)`.

The conditional term lies between zero and `E_P log2 s(A)`. One must not substitute log2 n for log2 s(A) in periodic classes, or identify S_s(P) with the entropy of an arbitrary rooted preparation.

The counterexample above illustrates the distinction: S_s increases from approximately **5.3349625007** to **6.8205055037** bits while the ordinary majorization test fails. The inherited-reference theorem does not establish monotonicity of H(P) alone because its orbit-size term also changes.

## 7. Reproducible audit

Run `python code/wheeler/rotation_audit.py`. It imports the WHEELER-58 model implementation and writes [wheeler-59-results.json](../../data/wheeler/wheeler-59-results.json). Kernels and probability comparisons use exact rational arithmetic; displayed Shannon values use floating-point logarithms.

- Every valid rooted source at n=4…14: event-uniform and q=1/20 run-weighted quotient rows agree across all rotations.
- The rooted state-uniform insertion-count formula is checked for every nonhomogeneous source in those layers; failures of representative independence are recorded.
- The inherited orbit-weighted column inequality is checked throughout those layers.
- Ordinary quotient columns exceed one at n=12 (17/16) and n=14 (10/9); all source/target details for the n=12 majorization witness are retained.
- Three initial words, including a periodic one, are checked through horizon three: projecting the full event-history law equals the law generated directly by Q, exactly.
- The four alternative kernels and the entropy diagnostics above are reproduced.

The all-size conclusions rest on the proofs; the finite audit checks their implementation and the explicit counterexamples. It neither proves nor falsifies universal ordinary class-Shannon monotonicity.

## 8. Verdict and next probe

- **PROVED:** event-uniform growth is strongly lumpable under rotations, with coherent Markov history laws.
- **FALSIFIED:** unmodified rooted state-uniform growth is representative independent.
- **NEGATIVE:** rotation invariance plus horizon consistency does not uniquely select event-uniformity.
- **FALSIFIED:** universal ordinary majorization on rotation classes.
- **PROVED:** event-uniform entropy nondecrease survives with the inherited orbit-size reference measure.
- **OPEN:** ordinary Shannon entropy monotonicity for event-uniform growth on rotation classes.

**WHEELER-60 — Quotient Shannon Entropy / Symmetry Audit.** Determine whether ordinary class Shannon entropy can decrease under the event-uniform quotient kernel. Focus on periodic-source symmetry, separate Shannon from stronger majorization claims, and seek either an explicit reproducible negative distribution or an all-size proof. This is a precise remaining question, not a mandate to obtain a preferred answer.
