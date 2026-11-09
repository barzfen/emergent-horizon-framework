# COLLATZ-04 · Bounding offset exceptions

This follows the [two survivor cases in COLLATZ-03](../survivor-branches-03/README.md). We use the shortcut map $T(n)=n/2$ for even $n$ and $T(n)=(3n+1)/2$ for odd $n$.

**COMPUTATIONAL CERTIFICATE.** For every integer $n>1$ whose multiplier first falls below one within **200,000 shortcut steps**, the value drops below $n$ at that same step. The calculation covers all starting integers with a first contraction in this horizon. It uses an analytic bound for large starts and an exact residue sieve for the remaining finite range.

## Exact bound from one parity word

For a word of length $d$, the endpoint is

$$
T^d(n)=\frac{An+B}{M},\qquad A=3^a,\qquad M=2^d,
$$

where $a$ is the number of odd steps. The coefficient stopping time $\kappa(n)$ is the first $d$ with $A<M$. The first descent time $\sigma(n)$ is the first $d$ with $T^d(n)<n$. Since $B\ge0$, $\kappa(n)\le\sigma(n)$. At a first contraction, a failure to descend requires

$$
n\le \left\lfloor\frac{B}{M-A}\right\rfloor.
$$

At each prefix length $j$ before contraction, the count of odd steps must be at least $s_j=\min\{a:3^a\ge2^j\}$. The counts $s_j$ increase by at most one per step, so they describe a single word. It chooses an even step whenever that maintains the inequality, and chooses odd otherwise.

A first contraction at depth $d$ must end with an even step, since an odd step increases the multiplier. Its odd count must be at least $s_{d-1}$ and less than $s_d$. Hence it is possible exactly when $s_d=s_{d-1}+1$, and its odd count is then $a=s_{d-1}$. The boundary word just described, stopped at $d-1$ and given a final even step, attains that first contraction.

Write $p_1<\cdots<p_a$ for the zero-based positions of the odd steps. The offset is

$$
B=\sum_{i=1}^{a}3^{a-i}2^{p_i}.
$$

The boundary word delays each odd step as far as the prefix constraints allow. Its $i$-th odd position is at least as late as the $i$-th odd position of every other surviving word with the same final odd count. Thus it maximises $B$, strictly if the positions differ. The denominator $M-A$ is the same for all first contractions at that depth. The largest offset therefore gives the exact largest integer cutoff for the depth. This is an integer-arithmetic implementation of Terras's minimax construction. [Terras (1976), Theorems 2.4 and 2.6 and Corollary 2.7](https://doi.org/10.4064/aa-30-3-241-252)

The [bound generator](bounds.py) traverses only the boundary word. At each possible first-contraction depth it tests the even alternative, records its cutoff, and continues along the odd branch. This uses one update per depth, with integer sizes that grow with depth. An independent exhaustive word check verifies the implementation through depth 16. The maximum cutoff at depth 30 is $108$, also obtained by the separate [COLLATZ-02 census](../parity-descent-02/README.md).

## How the finite range is checked

1. Through depth 200,000, the largest cutoff is **5,205,340,379**. It occurs at depth **125,743**. A larger starting integer automatically descends at its first coefficient contraction if that contraction is within the horizon.
2. Through depth 20, the largest cutoff is **24**. For starts above $24$, any coefficient contraction within 20 steps already certifies first descent.
3. The [verifier](verify.cpp) checks starts $2$ through $24$ directly. For larger starts up to the full cutoff it enumerates only the $27,328$ residue classes modulo $2^{20}$ that are still uncontracted. It lifts their affine endpoints to the starting integers in range and checks those trajectories from step 20. The other classes are covered by step 2.
4. Each directly checked orbit reaches a coefficient contraction at or before step **447**, and drops below its start at that step. The smallest start attaining 447 is **2,788,008,987**. The verifier allows up to 512 steps and fails on an overflow, a disagreement, or a start that exhausts this budget.

The verifier evaluates **135,661,634** starts directly. All starts $2\le n\le5,205,340,379$ are thereby certified to descend by shortcut step 447, with the same first descent and coefficient stopping times. The unbounded range above that cutoff is handled by the analytic estimate whenever $\kappa(n)\le200,000$. A second direct check confirms the maximum-depth witness by iterating it from step zero. The [result snapshot](results.json) records the default certificate.

## Reproduce

From this directory, compile the verifier and regenerate the certificate and results.

```sh
set -eu
c++ -std=c++17 -O3 -Wall -Wextra -Werror verify.cpp -o /tmp/ehf-collatz-04-verify
python3 bounds.py /tmp/ehf-collatz-04-certificate.txt
/tmp/ehf-collatz-04-verify < /tmp/ehf-collatz-04-certificate.txt > /tmp/ehf-collatz-04-results.json
diff -u results.json /tmp/ehf-collatz-04-results.json
```

## Scope

Terras introduced the coefficient stopping time and the minimax construction. Garner later studied the equality of stopping times using continued-fraction bounds and applied his estimates to cycles. We consulted the original papers for this relationship and used the integer minimax recurrence and the residue sieve to obtain the finite certificate above. AI assistance was used for derivation, coding, verification and drafting. We make no priority or record claim. [Garner (1981), §§6–7](https://doi.org/10.1090/S0002-9939-1981-0603593-2) · [Lagarias (1985), coefficient stopping time discussion](https://www.cecm.sfu.ca/organics/papers/lagarias/paper/html/node5.html)

For the exact survivor tree, the certificate excludes the offset case when the first coefficient contraction occurs within 200,000 steps. First contractions at greater depths and branches with no coefficient contraction are outside the certificate.
