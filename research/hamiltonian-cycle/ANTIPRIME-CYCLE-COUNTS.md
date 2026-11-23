# EHF-HC-ANTIPRIME-01 — Last highly composite cycle count

**Result (2026-11-24): PROVED (elementary number theory).**

For the complete, labelled, uncoloured Hamiltonian-cycle model with
undirected cycles considered modulo cyclic rotation and reversal,
the number of cycles on `n >= 3` vertices is

```text
H(n) = (n - 1)! / 2.
```

The exact members of this sequence that are **highly composite numbers**
(also called antiprimes) are

```text
n = 3, 5, 6, 7, 8, 9
H = 1, 12, 60, 360, 2520, 20160.
```

**No term H(n) with n >= 10 is highly composite.** This claim is
universal: the proof does not rely on searching beyond a finite bound.

A highly composite number N has strictly more positive divisors than
every *smaller positive integer*. A smaller number with even the
**same** number of divisors disqualifies N.

## Computation near the cutoff

| n | H(n) | d(H(n)) | Highly composite? |
|---:|---:|---:|:---:|
| 3 | 1 | 1 | yes |
| 4 | 3 | 2 | no (2 has two divisors) |
| 5 | 12 | 6 | yes |
| 6 | 60 | 12 | yes |
| 7 | 360 | 24 | yes |
| 8 | 2520 | 48 | yes |
| 9 | 20160 | 84 | yes |
| 10 | 181440 | 140 | no |
| 11 | 1814400 | 240 | no |
| 12 | 19958400 | 480 | no |
| 13 | 239500800 | 720 | no |
| 14 | 3113510400 | 1440 | no |

The six positive cases are checked by a complete divisor-count sieve
through 20,160 and independently matched to OEIS A002182.

For n = 10, a concrete smaller rival is **166,320**, which has **160**
divisors, whereas H(10) = **181,440** has only **140**.

## Theorem: H(n) is not highly composite for every n >= 11

Write `k = n - 1 >= 10` and `N = k!/2`.
By **Bertrand's postulate** choose a prime `q` with

```text
k < q < 2k.
```

Let `m` be the least positive integer such that `q < 2^m`, and let
`a = v_2(N)` (the exponent of 2 in the prime factorization of N).

Provided `a >= m`, form the integer

```text
M = (N / 2^m) q.
```

Because `q < 2^m`, **M < N**. Because `q > k`, this is a **new**
prime factor of M, not already present in `N`.

Let `T` be the contribution of all prime factors other than 2 to the
divisor count of N. Then

```text
d(N) = (a + 1) T
d(M) = 2 (a - m + 1) T.
```

In particular,

```text
d(M) >= d(N)  <=>  a >= 2m - 1.
```

This also ensures `a >= m`. Thus the presence of the smaller M with
as many or more divisors disproves that N is highly composite.

### Verify the inequality at every k >= 10

For k = 10, 11, 12, 13 direct arithmetic suffices:

| k | q | m | a = v2(k!/2) | a >= 2m - 1 |
|---:|---:|---:|---:|:---:|
| 10 | 11 | 4 | 7 | yes (equality) |
| 11 | 13 | 4 | 7 | yes (equality) |
| 12 | 13 | 4 | 9 | yes |
| 13 | 17 | 5 | 9 | yes (equality) |

For k = 14, 15 use `q = 17`, `m = 5`, `a = 10`;
the inequality holds.

For every **k >= 16**, choose integer `r >= 4` satisfying
`2^r <= k < 2^(r+1)`. From Bertrand's postulate,

```text
q < 2k < 2^(r+2),     hence m <= r+2.
```

The exponent of 2 in `(2^r)!` is `2^r - 1`, by Legendre's
valuation formula (or by summing the powers of 2). Consequently

```text
a = v2(k!) - 1 >= 2^r - 2 >= 2r + 3 >= 2m - 1
```

where `2^r - 2 >= 2r + 3` holds for all `r >= 4` (base r=4
and induction). This proves the required inequality for all
`k >= 16`, hence for all `k >= 10`.

Combining the explicit n=10 rival, the general n>=11 argument,
and the finite classification for n<=9 proves the stated theorem.

### Constructive examples

| n | H(n) | Smaller rival M | d(H(n)) | d(M) |
|---:|---:|---:|---:|---:|
| 10 | 181440 | 166320 | 140 | 160 |
| 11 | 1814400 | 1247400 | 240 | 240 |
| 12 | 19958400 | 16216200 | 480 | 480 |
| 13 | 239500800 | 194594400 | 720 | 864 |
| 14 | 3113510400 | 1654052400 | 1440 | 1440 |

Equal divisor counts are sufficient because a highly composite number
must break the *strict* record at its own size.

## Reproduction

```sh
python3 research/hamiltonian-cycle/verify_antiprime_counts.py
```

The pure Python checker confirms the record cases through 20,160
by enumerating their smaller integers; validates the n=10 witness;
and tests the constructive inequality for every `10 <= k <= 1000`.
This finite test is a **sanity check**, not the justification of
the general result. That is provided by the Bertrand/valuation proof.

## EHF significance and limits

The antiprime run is caused by the **factorial count** of uncoloured
complete-graph Hamiltonian cycles under all-slot insertion. This
number-theoretic property does not imply a new symmetry,
physical law, or growth invariant for EHF. Different constrained
growth systems have different counts and require separate checks.

The mathematical argument was prepared with AI assistance and has
**not been formalised in Lean**. EHF-LEAN-02/03
address related cycle growth but should not be cited as Lean
verification of this antiprime theorem.

### External sources

- [OEIS A002182 — Highly composite numbers](https://oeis.org/A002182)
- [Wolfram MathWorld — Highly Composite Number](https://mathworld.wolfram.com/HighlyCompositeNumber.html)
- [Erdos proof of Bertrand's postulate (Notre Dame notes)](https://academicweb.nd.edu/~dgalvin1/pdf/bertrand.pdf)
