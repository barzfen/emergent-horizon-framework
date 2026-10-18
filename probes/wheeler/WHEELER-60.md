# WHEELER-60 — Quotient Shannon Entropy / Symmetry Audit

**Date:** 19 October 2026 (Australia/Brisbane). **Status:** PROVED counterexample; exact rational kernels and integer entropy-sign certificate.

**Outcome:** ordinary Shannon entropy of rotation classes can decrease under the unchanged event-uniform growth rule. This resolves the open question in [WHEELER-59](WHEELER-59.md). The rooted entropy theorem and inherited orbit-weighted entropy theorem remain intact.

> **Subsequent result:** [WHEELER-61](WHEELER-61.md) supplies an unconditioned single-seed counterexample. The preparation distinction below describes the scope established at the WHEELER-60 stage.

## 1. The question and the answer

WHEELER-59 showed that event-uniform MICRO growth descends to rotation classes. It also falsified universal ordinary majorization there, but its witness still increased Shannon entropy. Majorization failure alone was insufficient to settle Shannon monotonicity.

Here a distribution on **two source classes** yields five target classes with strictly less ordinary Shannon entropy after one insertion. The source size is n=204, D=4. Both sources have 200 ones and four zeros. All transition probabilities follow the existing event-uniform rule; no new event weights or root-dependent choices are introduced.

We choose an initial probability law, as permitted in a claim of monotonicity for every preparation. We do not claim this law is the unconditional distribution produced by growing from one earlier seed. The distinction matters for the next probe.

## 2. Run notation and the quotient kernel

Write a four-run cycle as

`(a,b,c,d) = [0^a 1^b 0^c 1^d]`,

where brackets mean rotation equivalence. Every run length is at least two. Choosing the other zero run as the start identifies `(a,b,c,d)` with `(c,d,a,b)`. Bit exchange and reflection are not quotiented.

A run of length ℓ has ℓ+1 admissible insertion events extending it. For a source of size n with four walls, each such event has weight 1/(n+4). Add the weights of extensions that land in the same target class.

This run description is verified independently against full binary-word event enumeration in the accompanying code.

## 3. A two-source family

For an integer L≥10, prepare

`A=(2,L,2,L)` with probability **2/3**,

`B=(2,L−1,2,L+1)` with probability **1/3**.

Both sources have `n=2L+4`, `N1=2L`, and `D=4`. Source A repeats its two-run block twice; source B is asymmetric. Their distinct rooted orbit sizes are n/2 and n respectively.

There are five target classes:

| Target | Run representative | Q(A,target) | Q(B,target) |
|---|---|---:|---:|
| T | (2,L,2,L+1) | (2L+2)/(2L+8) | L/(2L+8) |
| C | (3,L,2,L) | 6/(2L+8) | 0 |
| U | (2,L−1,2,L+2) | 0 | (L+2)/(2L+8) |
| V | (3,L−1,2,L+1) | 0 | 3/(2L+8) |
| W | (2,L−1,3,L+1) | 0 | 3/(2L+8) |

For A, extending either long one-run gives T; extending either short zero-run gives C. For B, extending the shorter one-run gives T, while extending its longer one-run gives U. Its two zero-run extensions remain distinct as V and W. Every row sums to one.

Combining the rows with the specified preparation gives

`q_L = (5L+4, 12, L+2, 3, 3)/(6L+24)`

in the order T,C,U,V,W. The source entropy is the constant

`H(p)=h₂(2/3)=0.9182958340544895… bits`.

## 4. Explicit witness and exact sign

Choose **L=100**, so the source size is 204 and the target size is 205. Then

`q = (21/26, 1/52, 17/104, 1/208, 1/208)`

`  = (168,4,34,1,1)/208`.

The ordinary class entropies are:

| Quantity | Bits |
|---|---:|
| Source entropy H(p) | 0.9182958340544895 |
| Target entropy H(q) | 0.8596557583846341 |
| Change H(q)−H(p) | **−0.0586400756698554** |

These decimal values are explanatory. The sign has an exact certificate.

Using any common logarithm base,

`H(q) = log 208 − (168 log 168 + 4 log 4 + 34 log 34)/208`,

`H(p) = log 3 − (2/3) log 2`.

Multiply their difference by 624 and exponentiate. After prime-factor cancellation, `H(q)<H(p)` is equivalent to

**`2^1274 × 13^624 < 3^1128 × 7^504 × 17^102`.**

The audit checks this using exact Python integers. The left integer has 3,584 binary digits; the right has 3,620, independently making their strict order transparent. A second calculation checks the equivalent rational power-product inequality directly from p and q, with common denominator 624. Neither certificate relies on floating-point logarithms or an optimizer.

This single witness falsifies universal ordinary class-Shannon nondecrease. We make no claim that n=204 is the smallest possible counterexample or that this preparation maximizes the decrease.

## 5. An infinite family, not an isolated numerical accident

As L tends to infinity,

`q_L → (5/6,0,1/6,0,0)`.

Consequently,

`H(q_L)−H(p) → h₂(1/6)−h₂(1/3)`

`                = −0.2682734124061353… bits`.

The limiting sign is also immediate because binary entropy is strictly increasing on (0,1/2) and 1/6<1/3.

In fact, the certificate at L=100 proves negativity for **every integer L≥100**. For L≥10 the descending order of q_L is T,U,C,V,W. Its first four cumulative probabilities are

`(5L+4)/(6L+24)`,

`(6L+6)/(6L+24)`,

`(6L+18)/(6L+24)`,

`(6L+21)/(6L+24)`.

Each increases with L. Thus later q_L majorizes earlier q_L, and its Shannon entropy is nonincreasing. Since the source entropy is fixed and the change is already negative at 100, the full stated family follows.

This use of majorization compares the **output distributions of this particular family at different L**. It does not reinstate the falsified claim that every one-step quotient output is majorized by its input.

## 6. What causes the decrease?

Let X be the source class and Y the target class. The exact identity

`H(Y)−H(X)=H(Y|X)−H(X|Y)`

separates newly generated target uncertainty from unresolved source uncertainty.

At L=100,

- `H(Y|X)=0.5218823977832862… bits`;
- `H(X|Y)=0.5805224734531416… bits`.

Only T can come from both source classes. Given T, their posterior probabilities are 101/126 and 25/126. All four other targets identify their source uniquely. Thus the source ambiguity hidden by the final snapshot exceeds the uncertainty added by the step.

In plain English: the periodic source has two long runs whose extensions look identical once rotations are forgotten. The asymmetric source can also grow into that same target. With the specified preparation, enough probability accumulates in this shared outcome to reduce uncertainty about the current class.

This is a decrease of **ensemble entropy of the current class**, not a statement that every trajectory gets simpler. Five outcomes are possible instead of two, yet their probabilities are more concentrated. Counting possible states alone does not determine Shannon entropy.

## 7. What remains true about information and entropy?

The dynamics and probability measure have not changed. WHEELER-59's event-uniform quotient is still strongly lumpable and its history laws are still consistent.

The inherited reference entropy is

`S_s(P)=H(P)+E_P log₂ s(class)`.

The source orbit sizes are 102 and 204. Every target has orbit size 205: a nontrivial repeat would have to divide both its four domain walls and its odd total length, which is impossible. Therefore

`ΔS_s = ΔH + log₂(205/204) + 2/3`

`     = +0.6150813485307617… bits`.

The orbit-weighted theorem is satisfied, despite the ordinary class-entropy decrease. The rooted theorem is also unaffected. Rooted entropy, ordinary class entropy, and inherited-reference class entropy are different quantities; they cannot be substituted for one another.

Keeping the source in the record also changes the entropy question:

`H(X,Y)=H(X)+H(Y|X) ≥ H(X)`.

Thus the joint two-time record gains entropy even while the final snapshot loses it. This does not by itself establish microscopic reversibility or a physical information-conservation law. No physical erasure, heat cost, quantum entropy, or thermodynamic violation follows from this calculation.

The counterexample also does not invalidate the `(n,N1,D)` macro kernel. Both sources have the same macrostate and the same next-symbol probabilities; their differing run arrangements are information that this observer does not record.

## 8. Preparation and scope

The theorem being falsified quantified over all initial class distributions, so a two-point preparation is sufficient. Each of the two source cycles is individually reachable from the minimal four-run seed `(2,2,2,2)` by admissible growth. However, that fact does **not** make their chosen 2:1 mixture the unconditional endpoint law of that seed: many other endpoints occur, with probabilities fixed by the process.

Whether ordinary class entropy is nondecreasing along particular naturally generated, unconditioned preparations is a separate and potentially useful question. It must be tested using the actual endpoint laws rather than reweighting or discarding unwanted outcomes without saying so.

## 9. Reproducible audit

Run `python code/wheeler/quotient_entropy_audit.py`. The standard-library script writes [wheeler-60-results.json](../../data/wheeler/wheeler-60-results.json).

It verifies:

- exact normalized source and target laws, including all five target classes;
- the run-extension kernel against independent full binary-word event enumeration for both sources at L=10,38,80,100;
- two independent exact arithmetic certificates for the negative entropy sign;
- the conditional-entropy identity and posterior source probabilities;
- source and target orbit sizes and the positive inherited-reference entropy change;
- high-precision display values and selected members of the explicit family.

Numerical optimization helped locate the mechanism during exploration. The retained counterexample and its proof require no optimization, sampling, NumPy or SciPy.

## 10. Verdict and next probe

- **FALSIFIED:** universal ordinary Shannon entropy nondecrease for event-uniform growth on rotation classes.
- **PROVED:** an explicit two-source counterexample and an infinite family with the same mechanism.
- **RETAINED:** event-uniform quotient Markov closure, consistent histories, rooted entropy monotonicity, and inherited orbit-weighted entropy monotonicity.
- **NOT CLAIMED:** smallest counterexample, globally largest decrease, a naturally generated unconditioned counterexample, or any thermodynamic violation.

**WHEELER-61 — Reachable Preparations / Unconditioned Entropy Audit.** Follow the actual endpoint laws from specified single seeds, especially `(2,2,2,2)`, and determine whether ordinary quotient entropy can decrease without reweighting or conditioning. Use the exact run-growth urn law where available and keep current-state entropy distinct from history-record entropy.
