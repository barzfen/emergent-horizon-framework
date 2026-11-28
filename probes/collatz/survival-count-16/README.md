# COLLATZ-16 · A sharp count of multiplier survivors

**Proved.** The fraction of residue classes whose Collatz multiplier has stayed at least one through $d$ shortcut steps is of order
$d^{-3/2}2^{-(1-h)d}$, where $h=h_2(\log_3 2)=0.949955527188\ldots$.
Every positive start eventually contracting remains open. By [COLLATZ-15](../escape-tail-15/README.md), this is equivalent to ruling out positive orbits that escape to infinity.

This note gives a self-contained order estimate using a cyclic rotation and an elementary random-walk bound. Terras established the residue-class encoding and the density-one stopping result. The same weighted survival order appears in Lemma 6 of a recent preprint, with a scaling of the walk and a free final bit in its excursion convention. [Terras (1976), Theorems 1.2, 1.14 and 1.17](https://doi.org/10.4064/aa-30-3-241-252) · [*Effective equidistribution and path laws for long Collatz excursions*, Lemma 6 and Appendix A](https://rstation.ai/problems/collatz/papers/87)

## Count the surviving words

For a binary parity word of length $d$, let $a_j$ be the number of odd steps among its first $j$ bits. With the shortcut map, the multiplier through $j$ is $P_j=3^{a_j}/2^j$. Put $\alpha=\log_3 2$ and $S_j=a_j-\alpha j$, with $S_0=0$. The condition $P_j\ge1$ is equivalent to $S_j\ge0$. Write $U_d$ for the number of words satisfying that condition at every prefix. The parity-residue bijection makes $U_d$ the exact number of surviving classes modulo $2^d$. We prove

$$
U_d\asymp 2^{hd}d^{-3/2},\qquad
h=h_2(\alpha)=-\alpha\log_2\alpha-(1-\alpha)\log_2(1-\alpha).
$$

Here $\asymp$ means upper and lower bounds up to positive constants independent of $d$.

### Lower bound

Consider words with exactly $\lceil\alpha d\rceil$ ones. Their total $S_d$ lies in $[0,1)$. In each class of cyclic rotations, start just after an index where $S_j$ is minimal among $0\le j<d$. Prefixes before the wrap have nonnegative sums because the index is a minimum and $S_d\ge0$. After the wrap the prefix sum is $S_d$ plus the difference between another partial sum and that minimum. Thus each class supplies a survivor and has at most $d$ members. By Stirling's formula, since $\lceil\alpha d\rceil-\alpha d$ is bounded,

$$
U_d\ge \frac1d\binom{d}{\lceil\alpha d\rceil}\asymp 2^{hd}d^{-3/2}.
$$

### Upper bound

Assign independent bits with one-probability $\alpha$ as a counting device. The resulting walk $S_j$ has centered increments with variance $\alpha(1-\alpha)$, and a particular word has probability $2^{-hd+\lambda S_d}$ with $\lambda=\log_2(\alpha/(1-\alpha))>0$. If $A_d$ is the event of survival through $d$, then

$$
U_d=2^{hd}\mathbb E_\alpha[2^{-\lambda S_d}\mathbf 1_{A_d}].
$$

Split the word into three consecutive blocks with lengths differing by at most one. Consider $A_d$ together with $S_d\in[x,x+1)$, for an integer $x\ge0$.

- The first block must stay at or above zero. The walk bound below gives probability $O(d^{-1/2})$.
- In the final block read backwards, each partial sum $S_d-S_{d-j}$ is less than $x+1$. Apply the same bound to the negative of the reversed increments with initial height $x+1$, giving $O((x+2)d^{-1/2})$. The first and final block constraints involve independent bits.
- Conditional on the first and final blocks, the sum in the middle block must lie in a half-open unit interval. Its support is spaced by one, and Stirling's formula bounds the largest binomial atom by $O(d^{-1/2})$.

The joint probability is therefore $O((x+2)d^{-3/2})$ for $d\ge3$. Multiplying by $2^{-\lambda x}$ and summing over $x$ gives the upper bound, since $\sum_{x\ge0}(x+2)2^{-\lambda x}<\infty$.

### Walk bound used above

A centered walk with independent identically distributed increments bounded by one in absolute value and variance $\sigma^2>0$, started at height $y\ge0$, stays at or above zero through $m$ steps with probability $O((1+y)/\sqrt m)$. The constant may depend on $\sigma^2$.

Put $b=\sqrt m$, let $Z_j$ be the walk including its initial height, and assume $y<b$, since the other case follows from the bound by one. Let $\tau$ be the first exit from $[0,b)$. The stopped values lie in $[-1,b+1]$. Apply the martingales $Z_j$ and $Z_j^2-\sigma^2j$ at $\tau\wedge k$, a bounded time. The square identity and bounded values give $\mathbb E(\tau\wedge k)\le (b+1)^2/\sigma^2$, so $\mathbb E\tau<\infty$. Taking limits gives $\mathbb E Z_\tau=y$ and $\sigma^2\mathbb E\tau=\mathbb E Z_\tau^2-y^2$.

If $p$ is the upper exit probability, then $y\ge bp-(1-p)$, hence $p\le(y+1)/(b+1)$. The overshoot bound gives $\mathbb E Z_\tau^2\le1+(b+1)^2p$, so $\mathbb E\tau=O(b(1+y))$. Survival through $m$ requires an upper exit first or $\tau>m$. Its probability is at most $p+\mathbb E\tau/m=O((1+y)/\sqrt m)$. The argument applies to either sign of the increments.

## What the count leaves open

For any interval of $X$ consecutive positive integers, choose $d=\lfloor\log_2 X\rfloor$. Each residue class has at most two representatives there. Thus the number of starts that could survive forever in the interval is

$$
O\!\left(\frac{X^h}{(\log X)^{3/2}}\right),
$$

uniformly in the interval location. The bound still grows with $X$.

Let $m_d$ be the least positive start whose first $d$ multipliers all stay at least one. Such a start exists at every depth. For example, the all-odd word corresponds to $-1\bmod 2^d$, by the parity-residue bijection and the fixed point $T(-1)=-1$ of the same rule on integers. The least positive representative of that branch is $2^d-1$, which increases without bound. An all-odd prefix at every depth would require a start congruent to $-1$ modulo every power of two, so the branch represents the single integer $-1$.

The sequence $m_d$ is nondecreasing because the survival conditions are nested. If it stays bounded, it eventually stabilizes at one positive start that survives every depth. If it tends to infinity, each positive start is excluded at some finite depth. **The universal claim is therefore exactly $m_d\to\infty$.** The word count gives the number of classes at each depth. Proving the limit requires control of where their least positive representatives lie. [COLLATZ-14](../backward-terminal-14/README.md) gives an equivalent test for a fixed starting budget. The least-start criterion is also recorded in the [GettysburgResearch Collatz results catalog](https://github.com/GettysburgResearch/collatz/blob/main/research/RESULTS_CATALOG.md#coefficient-stopping-and-orbitwise-tails).

## Arithmetic check

The exact count by endpoint is obtained from $C_{0,0}=1$ using $C_{j,a}=C_{j-1,a}+C_{j-1,a-1}$ when $3^a\ge2^j$, and zero otherwise. Terms outside the valid range of odd counts are zero. Summing $C_{d,a}$ gives $U_d$. Direct trajectory enumeration of a full residue system agreed with this recurrence through depth $14$. The recurrence gives $U_8=19$, $U_{16}=2114$, and $U_{32}=41347483$.
