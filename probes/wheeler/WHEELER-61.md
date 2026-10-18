# WHEELER-61 — Reachable Preparations / Unconditioned Entropy Audit

**Date:** 19 October 2026 (Australia/Brisbane). **Status:** PROVED single-seed counterexample; exact endpoint laws and rational entropy-sign bounds. Minimal-seed results remain finite computational evidence.

**Outcome:** ordinary rotation-class Shannon entropy can decrease during unconditioned event-uniform growth from a single fixed cycle. No selection or reweighting of intermediate outcomes is necessary. The minimal seed `(2,2,2,2)` shows no decrease through 40 growth events; that narrower case is not settled for all times here.

## 1. The preparation question

[WHEELER-60](WHEELER-60.md) falsified universal quotient-entropy monotonicity using a specified two-class mixture. The question here is whether a decrease can also occur in the actual endpoint distributions generated from one deterministic starting state.

Use the same cyclic binary words, admissibility rule, event-uniform insertion kernel, and rotation quotient as before. A four-run representative

`(a,b,c,d) = [0^a 1^b 0^c 1^d]`

is identified with `(c,d,a,b)`. Neither reflection nor bit exchange is identified. All run lengths are at least two, and D=4 is conserved.

At time t, meaning t insertion events, retain **all** endpoints with their actual probabilities. No trajectories are discarded, and no endpoint law is chosen afresh.

## 2. Exact endpoint law

Temporarily label the seed's D runs in cyclic order, with lengths ℓ₁,…,ℓ_D. These labels are a calculation device. Growth extends existing runs and never creates or removes one in this sector.

Run i is selected with probability

`(ℓ_i + x_i + 1)/(n₀ + D + t)`,

where x_i is its accumulated number of extensions. Thus the ordered run lengths follow a Pólya urn with parameters `α_i=ℓ_i+1` and total `A=n₀+D`.

For nonnegative increments x₁,…,x_D summing to t,

`P_t(x) = [t! / product_i x_i!] × [product_i (α_i)_(x_i)] / (A)_t`,

where `(a)_k=a(a+1)…(a+k−1)` and `(a)_0=1`. Equivalently,

`P_t(x) = product_i binom(ℓ_i+x_i, x_i) / binom(n₀+D+t−1,t)`.

**Derivation:** every ordered sequence with the same extension counts has the same numerator product and common denominator `(A)_t`. There are `t!/product x_i!` such sequences. Summing their probabilities gives the formula. Summing all x normalizes it, equivalently by the generating function `product_i (1−z)^(-α_i)=(1−z)^(-A)`.

To obtain the rotation-class endpoint law, sum these probabilities over run vectors representing the same class. This performs the quotient after computing the actual growth law; it does not assign equal probabilities to distinct endpoints.

## 3. A deterministic seed with a decreasing step

Start from the single cycle

**`(2,100,2,100) = [00 1^100 00 1^100]`.**

Its initial size is 204. For its first three events, the complete endpoint entropies are:

| Event count t | Size n | Reachable rotation classes | Ordinary class entropy, bits |
|---:|---:|---:|---:|
| 0 | 204 | 1 | 0 |
| 1 | 205 | 2 | 0.1885719560 |
| 2 | 206 | 6 | 1.3213373586 |
| 3 | 207 | 10 | 1.3076635638 |

Therefore,

**`H₃−H₂ = −0.0136737947612340… bits`.**

This is an unconditioned single-seed counterexample. It falsifies the claim that ordinary class entropy must be nondecreasing along growth from every deterministic seed. It does not say that entropy falls below its initial value of zero.

For full reproducibility, the two distributions are:

| t=2 run representative | Probability |
|---|---:|
| (2,100,2,102) | 5151/10868 |
| (2,100,3,101) | 303/10868 |
| (2,100,4,100) | 3/5434 |
| (2,101,2,101) | 10201/21736 |
| (2,101,3,100) | 303/10868 |
| (3,100,3,100) | 9/21736 |

| t=3 run representative | Probability |
|---|---:|
| (2,100,2,103) | 176851/760760 |
| (2,100,3,102) | 15453/760760 |
| (2,100,4,101) | 303/380380 |
| (2,100,5,100) | 1/76076 |
| (2,101,2,102) | 520251/760760 |
| (2,101,3,101) | 30603/760760 |
| (2,101,4,100) | 303/380380 |
| (2,102,3,100) | 15453/760760 |
| (3,100,3,101) | 909/760760 |
| (3,100,4,100) | 9/380380 |

Both columns of probabilities sum to one exactly. More reachable classes do not imply higher Shannon entropy: their probabilities matter.

## 4. Certification without floating-point sign assumptions

The audit bounds every logarithm using rational arithmetic. For 1≤y≤2 and `z=(y−1)/(y+1)`,

`ln y = 2 sum_(j≥0) z^(2j+1)/(2j+1)`.

After N terms the omitted positive tail is at most

`2 z^(2N+1)/[(2N+1)(1−z²)]`.

Because 0≤z≤1/3, this converges rapidly. Any positive rational is reduced to `2^k y`; the same method bounds ln 2, with the interval order reversed when multiplying by a negative k. Entropy sums and division by the positive ln 2 interval preserve rigorous bounds.

With 32 terms, exact rational comparisons certify the outward enclosure

**`−0.013673795 ≤ H₃−H₂ ≤ −0.013673794 < 0`.**

The displayed high-precision decimals are separate from this sign certificate. No optimizer, random sampling, or floating-point tolerance determines the conclusion.

## 5. The symmetry identity explaining the decrease

Let R_t denote the ordered four-run vector and C_t its rotation class. For a seed `(a,b,a,b)`, the ordered endpoint law is invariant under exchanging the two run pairs. Each quotient class therefore has either:

- two equally probable ordered representatives; or
- one representative, when the run pattern repeats: `(u,v,u,v)`.

Let ρ_t be the probability of the latter periodic case. The entropy chain rule gives the exact identity

**`H(C_t)=H(R_t)−1+ρ_t`.**

Hence

`ΔH(C)=ΔH(R)+ρ_(t+1)−ρ_t`.

For the witness,

`ρ₂ = 5105/10868 = 0.4697276408…`,

`ρ₃ = 0`.

The second equality is forced by parity: a repeated two-run block has even total length, whereas the t=3 size is 207.

The ordered-run entropy increases by **0.4560538460… bits**, but the symmetry correction drops by **0.4697276408… bits**. Their difference is the observed negative class-entropy change.

Ordered-run entropy itself is nondecreasing: for a target vector of total length n+1, summing incoming increment probabilities gives at most `(n+1)/(n+4)<1`. Each allowed predecessor comes from decrementing one coordinate, contributing that target coordinate divided by n+4. The standard column-substochastic entropy argument therefore applies before the pair-exchange quotient.

This identifies the mechanism precisely. The underlying run uncertainty grows; the changing symmetry correction makes the entropy of the observed classes fall.

## 6. Why a whole family can exhibit it

Consider seeds `(2,L,2,L)` and hold t fixed while L tends to infinity. The chance of extending a short zero-run tends to zero. Each long one-run has selection probability tending to 1/2, and the finite number of reinforcements does not change that limit.

At t=2, the ordered long-run extension counts follow the limiting binomial probabilities `(1/4,1/2,1/4)`. Rotation identifies the two outer outcomes, giving class probabilities `(1/2,1/2)` and entropy 1 bit.

At t=3, the binomial probabilities `(1/8,3/8,3/8,1/8)` fold into class probabilities `(1/4,3/4)`, with entropy `h₂(1/4)`.

Thus

`lim_(L→∞) [H₃−H₂] = h₂(1/4)−1`

`                           = −0.1887218755408671… bits`.

The finite support at these fixed horizons and continuity of Shannon entropy prove that all sufficiently large integer L give a decrease. The explicit rational certificates verify L=100,200,1000. We do not claim L=100 is the first such seed or a proved threshold for the entire family.

## 7. What happens for the minimal seed?

For `(2,2,2,2)`, the exact endpoint law was evaluated through t=40, corresponding to size 48. Every ordinary class-entropy increment in that finite scan was positive. The smallest observed increment was approximately **0.0959195330 bits**, from t=38 to t=39.

Endpoint probabilities were exact rationals; entropy values for this larger scan used floating-point logarithms. An independent dynamic recursion matched the urn endpoint formula through t=12. These are finite computational results, not an all-time monotonicity proof.

The symmetry identity above also applies to this seed and gives a concrete route to the remaining question: bound ordered-run entropy production against the periodic-class probability at even times. Merely being able to reach the large counterexample seed from the minimal seed does not transfer its conditional future entropy decrease to the minimal seed's full unconditioned ensemble.

## 8. Entropy statements retained

For four-run classes, the number of distinct rooted binary representatives is n for an asymmetric class and n/2 for a periodic class. Therefore

`S_s(C_t)=H(C_t)+log₂ n−ρ_t=H(R_t)+log₂(n/2)`.

For the witness step,

`ΔS_s = ΔH(C)+log₂(207/206)+ρ₂`

`      = +0.4630402763351452… bits`.

So the inherited orbit-weighted theorem remains valid, as does the rooted entropy theorem. The actual quotient process remains Markov and horizon-consistent. Keeping an accumulating history record also has nondecreasing Shannon entropy by the entropy chain rule.

The counterexample concerns the ensemble entropy of a current coarse observation. It establishes neither thermodynamic entropy decrease nor fundamental information destruction. It does show that a universal arrow of increasing snapshot entropy cannot be inferred merely from admissible growth, event-uniformity, or deterministic preparation.

## 9. Reproducible audit

Run `python code/wheeler/unconditioned_entropy_audit.py`. It uses only the standard library and writes [wheeler-61-results.json](../../data/wheeler/wheeler-61-results.json).

For the witness, three calculations agree exactly through t=3:

1. recursive growth on rotation classes;
2. the independent ordered-run urn formula followed by quotienting;
3. full binary-word insertion from a fixed rooted representative, followed by rotation projection.

The third calculation includes every rooted endpoint: counts 1,5,15,35, projecting to 1,2,6,10 classes. The script also checks the symmetry entropy identity, the positive orbit-weighted entropy change, the rational sign certificate, the minimal-seed finite scan, and selected members of the large-L family.

## 10. Verdict and next probe

- **FALSIFIED:** ordinary rotation-class Shannon entropy is nondecreasing for every unconditioned single-seed growth process.
- **PROVED:** an exact deterministic-seed witness, a rigorous negative entropy interval, and an asymptotic family mechanism.
- **PROVED:** the ordered-run/class entropy identity for pair-symmetric four-run seeds.
- **COMPUTATIONAL:** minimal-seed entropy increases through 40 events.
- **OPEN:** all-time ordinary class-entropy monotonicity from the minimal seed `(2,2,2,2)`.

**WHEELER-62 — Minimal-Seed Entropy / Symmetry Bound Audit.** Use the exact urn law and `H(C_t)=H(R_t)−1+ρ_t` to compare ordered-run entropy production with the periodic-class correction. Seek an all-time bound for the minimal seed or an explicit later counterexample, keeping this preparation-specific question separate from the universal claim already falsified.
