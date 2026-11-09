# COLLATZ-06 · How many parity blocks must appear early?

[COLLATZ-05](../multiplier-band-05/README.md) put a lower bound on multiplier growth for a hypothetical positive integer whose coefficient never contracts. Here we test branches with enough growth to pass that bound.

**PROVED.** A nonrepeating rational orbit with a polynomially bounded multiplier range must produce order $N$ different parity windows of length $O(\log N)$ within its first $N$ steps. We construct a coefficient survivor with multiplier $N^{\log_2 3+o(1)}$ that eventually contains every finite binary word, yet has only $O((\log N)^2)$ different windows at that early scale. Its 2-adic lift is irrational.

## Equal parity windows impose a minimum separation

Let $w$ be the parity word for a rational 2-adic start $p_0/q$, with $q>0$ odd, using the fixed-denominator numerators $p_i$ from COLLATZ-05. Write $p_{w,N}(d)$ for the number of distinct length-$d$ windows contained in its first $N$ bits. Let $X_N=\max_{0\le i\le N}|p_i|$.

Two identical parity windows starting at $i$ and $j$ give the same affine update, with odd numerator multiplier $A$. Thus

$$
p_{i+d}-p_{j+d}=\frac{A(p_i-p_j)}{2^d},
\qquad 2^d\mid(p_i-p_j).
$$

For a nonrepeating orbit the difference is nonzero. In particular,

$$
2^d>2X_N\quad\Longrightarrow\quad p_{w,N}(d)=N-d+1 \qquad (1\le d\le N).
$$

Every one of the eligible windows is distinct at such a scale. This is the height-sensitive form of the parity-separation argument used by Dubickas for divergent positive integer orbits. A related treatment explicitly uses signed numerators with a fixed odd denominator. [Dubickas (2009), Theorem 5 and §5](https://doi.org/10.1017/S0017089508004655) · [Height-sensitive Collatz factor discussion](https://rstation.ai/r/collatz/posts/6)

## What polynomial growth requires

Let $P_i=3^{a_i}/2^i$ be the cumulative multiplier, where $a_i$ counts odd steps, and let $H_N=\max_{i\le N}P_i/\min_{i\le N}P_i$. COLLATZ-05 gives $X_N\le H_N(|p_0|+qN/3)$. If $H_N=O(N^\beta)$ for a fixed $\beta\ge0$, then $X_N\le K(N+1)^{\beta+1}$ for some $K>0$. For sufficiently large $N$, choose

$$
d_N=\left\lceil\log_2\!\left(2K(N+1)^{\beta+1}+1\right)\right\rceil.
$$

The first $N$ bits must contain $N-d_N+1$ distinct length-$d_N$ windows. There is also a consequence for the whole word's factor count $p_w(d)$. For each large $d$, choose $N=\lfloor c\,2^{d/(\beta+1)}\rfloor$ with a sufficiently small fixed $c>0$. Then $2X_N<2^d$ and $d\le N/2$, so $p_w(d)\ge N/2$. Thus

$$
\liminf_{d\to\infty}\frac{\log_2 p_w(d)}{d}\ge\frac{1}{\beta+1}.
$$

For a coefficient survivor, $P_i\ge1$ for all $i$ and $P_0=1$, so $H_N$ is the running maximum of $P_i$.

The early-window test can be stronger than the whole-word condition. Suppose an aperiodic word $w$ differs in $E_N=o(N/\log N)$ positions of its first $N$ bits from a reference word $v$ with subexponential factor count, meaning $\log p_v(d)=o(d)$. One changed bit can affect at most $d$ windows. Hence

$$
p_{w,N}(d)\le p_v(d)+d E_N.
$$

At any $d=O(\log N)$, this is $o(N)$. Therefore, if $w$ also has $H_N=O(N^\beta)$, it has no rational lift. Aperiodicity ensures that a rational orbit with this word would be nonrepeating.

## A branch that contains every binary word

Start with the upper mechanical boundary word $v$ of slope $\alpha=\log_3 2$ from COLLATZ-05. It has $d+1$ length-$d$ factors and $1\le P_i<3$. In any block of length $l$ its odd count is either $\lfloor l\alpha\rfloor$ or $\lceil l\alpha\rceil$, by subtracting its prefix counts $\lceil i\alpha\rceil$. [López and Stoll (2009), §1](https://doi.org/10.1515/INTEG.2009.014)

1. **Give the multiplier polynomial growth.** With zero-based bit positions, for each $k\ge3$ flip the first zero at or after $2^k$ to a one. A length-three block of $v$ always contains a zero because $\alpha<2/3$, so the flip is at one of $2^k,2^k+1,2^k+2$. The number of flips through the first $N$ bits is $\log_2 N+O(1)$, and each flip multiplies the later cumulative multiplier by $3$. The resulting multiplier is therefore $\Theta(N^{\log_2 3})$.
2. **Place every finite binary word somewhere.** List all nonempty binary words in order of length and then lexicographically, with the index $j$ starting at $4$. Let $l_j\le j$ be the length of the $j$-indexed word in this list. At position $M_j=2^{j^2}+4j$, replace the next $3l_j$ bits by a block that starts with the listed word and has the same total number of ones as the original block. The original interval has no dyadic flip because it lies strictly between $2^{j^2}+2$ and $2^{j^2+1}$. Since $1/2<\alpha<2/3$, the original block contains at least $l_j$ ones and at least $l_j$ zeros. Any listed word can therefore be followed by filler with the required counts. The replacement intervals are disjoint.

A replacement can change a prefix odd count inside its interval by at most $3l_j\le3j$, and the change is zero once the interval ends. At its start there have already been $j^2-2$ dyadic flips. Since $j^2-2\ge3j$ for $j\ge4$, all cumulative multipliers stay at least one. The temporary count error is $O(\sqrt{\log N})$ at prefix length $N$, so the final word has $P_N=N^{\log_2 3+o(1)}$. Its multiplier range is polynomially bounded.

The final word has $p_w(d)=2^d$ for every $d$, since every word was placed somewhere. Yet its first $N$ bits differ from $v$ in only $O(\log N)$ places. The dyadic flips contribute $O(\log N)$. The replacement intervals contribute at most $\sum_{j^2\le\log_2 N}3j=O(\log N)$. Consequently the number of early windows at length $O(\log N)$ is $O((\log N)^2)$. The word is aperiodic because its whole-word factor count is unbounded, and the early-window test excludes every rational lift.

## Scope

This construction clears the previous multiplier lower bound and has the largest possible whole-word factor count. The obstruction comes from when the factors occur. The proof leaves open whether a coefficient survivor with enough distinct early windows can have a positive integer lift. The polynomial-growth argument also leaves branches with faster multiplier growth open.

The congruence argument and mechanical word use the cited literature. We read Dubickas's proof of Theorem 5 and the relevant parts of López and Stoll. The finite-window criterion and the construction are worked out here without a priority claim. AI assistance was used for derivation, arithmetic checks and drafting.
