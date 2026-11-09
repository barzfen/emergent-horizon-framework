# COLLATZ-25 · How frequent could cofactor returns be on an escape?

[COLLATZ-23](../cofactor-returns-23/README.md) excludes short cofactor returns near high future minima. [COLLATZ-24](../cofactor-avoidance-24/README.md) constructs arbitrarily long finite segments with distinct cofactors. Here we allow arbitrary drops between the endpoints. **If a positive Collatz orbit diverges, visits to any fixed stripped cofactor have zero density in the sequence of odd-run starts.** The proof gives a finite frequency bound on a segment that stays high.

## A short return forces a drop

Use the shortcut map, and write its successive odd-run starts as $x_i$, with

$$
x_i+1=2^{L_i}u_i,\qquad
u_i=3^{v_i}w_i,\qquad 3\nmid w_i.
$$

Thus $w_i$ is the stripped cofactor. Put $g=\log_2 3$, $h_i=\log(x_i+1)$ and $z_i=\log h_i$, where $\log$ is natural. As in COLLATZ-23, $h_{i+1}\le g h_i$, so $z_{i+1}-z_i\le\log g$. The shortcut length of one join is at most $(1+g)\log_2(x_i+1)$. Consequently the total step count in $k=j-i\ge1$ joins is $O(g^k h_i)$.

If $w_j=w_i$, the telescoped join identity of COLLATZ-23 is

$$
0<\Theta=s\log 2-(A-v_j+v_i)\log 3
 <\sum_{t=i+1}^{j}\frac1{x_t},
$$

where $A$ is the total odd count, and $s$ is the step count plus $L_j-L_i$. Both exponents in the two-logarithm form have absolute value $O(g^k h_i)$. For the ternary valuations, this uses $v_t\le\log_3(x_t+1)$. The two-logarithm estimate gives, for an absolute $c>0$ and $\nu=4.117$,

$$
\Theta\ge c(g^k h_i)^{-\nu}.
$$

The lower bound applies with any sign of the exponent of three and uses $s\ge1$. Let $m=\min_{i<t\le j}x_t$. The reciprocal sum is at most $k/m$. It follows that

$$
m\le C k g^{\nu k} h_i^\nu
$$

with an absolute constant $C$. From the location of $m$, there are at most $k$ joins remaining, each increasing log height by at most a factor $g$. Therefore

$$
h_j\le g^k\log(1+C k g^{\nu k}h_i^\nu). \tag{1}
$$

For fixed $k$, this means $x_j+1\ll_k(1+\log(x_i+1))^{\nu g^k}$. A return after a bounded number of joins forces an eventual drop from a large starting value to a power of its logarithm. [Fan, Queffélec and Queffélec, Theorem 2.1, citing Wu and Wang](https://ems.press/content/serial-article-files/47663?nt=1)

The same argument works if the reduced numerator and denominator of $w_j/w_i$ are bounded by a fixed $H_0$. In that case the form has an extra term $\log(w_j/w_i)$. Matveev's bound gives (1) with a larger exponent $\nu$ and constant $C$ depending on $H_0$. The sharper exponent above is for exact returns. [Explicit form of Matveev's bound, Theorem 2.3](https://link.springer.com/article/10.1007/s10998-025-00649-x)

## Count the returns on a high segment

For all sufficiently large $z_i$, equation (1) implies

$$
k\le z_i/2\quad\Longrightarrow\quad z_j\le z_i/2
$$

at an exact return. To see this, take logarithms in (1). The first term is $k\log g\le(\log g)z_i/2$. The second term is $O(\log(1+z_i))$, since $k\le z_i/2$ and $h_i=e^{z_i}$. As $\log g<1$, their sum is at most $z_i/2$ for sufficiently large $z_i$.

Consider a segment $x_p,\ldots,x_{p+N}$ whose starts are all at least $X$. Write $Z=\log\log(X+1)$, and assume $Z$ exceeds the threshold above. Fix any stripped cofactor $w$ and consider gaps between consecutive visits to $w$ within the segment. Put $K=\lfloor Z/2\rfloor$.

- A gap of at most $K$ decreases $z$ by at least $Z/2$.
- A gap of more than $K$ consumes at least $K+1$ joins, so at most $N/(K+1)$ such gaps fit.
- The short-gap intervals are disjoint in their joins. Between them, $z$ can rise by at most $\log g$ per join. Since the final $z$ is at least $Z$, their total decrease is at most $z_p-Z+N\log g$.

Including the first visit, the number of occurrences of $w$ in the segment is at most

$$
1+\frac{2(z_p-Z+N\log g)}{Z}+\frac{N}{K+1}.
$$

On a divergent orbit, for any large $X$ there is a fixed tail starting at $p$ whose values are all at least $X$. First let $N\to\infty$ in this bound. The upper frequency is $O(1/Z)$, uniformly in $w$. Then let $X\to\infty$ to obtain zero density. A finite union of such cofactors also has zero density. This is a frequency statement along an individual orbit, with joins as the time unit.

In particular, if a fixed stripped cofactor has positive upper frequency along a positive orbit, the orbit is bounded and eventually periodic. If an orbit were unbounded, its states would be distinct and would tend to infinity. Any positive cycle contracts the multiplier per period, by the affine return identity used in COLLATZ-22.

## An elementary case with no return

A single join with exactly one halving can return to the same stripped cofactor only at $1$. Write the two odd cofactors as $u=w3^a$ and $v=w3^b$. The single-join identity gives

$$
w(2^{1+R}3^b-3^{L+a})=1.
$$

Hence $w=1$, and reduction modulo three gives $b=0$. Now $2^{1+R}=3^{L+a}+1$. A positive even exponent on three gives $2\bmod8$, incompatible with a power of two at least four. A positive odd exponent gives $4\bmod8$, so the power of two is four and $L+a=1$. Thus $L=1,a=0$ and the starting value is $1$.

Exact arithmetic verified the telescoping product and height inequalities on 65,536 finite windows. It also found only the $1$-to-$1$ one-halving return below $2^{20}$. The statements follow from the proofs above.

Zero density allows infinitely many sparse returns. Whether a hypothetical escape has even one fixed stripped cofactor that recurs infinitely often remains unresolved here. No recurrence forcing an escape into the excluded window near its future minima follows.
