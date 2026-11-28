# COLLATZ-22 · The exact join between two odd runs

[COLLATZ-21](../planted-orbit-21/README.md) constructed sparse perturbations of Collatz with a planted divergent orbit. Here the exact additive constant gives a bound across consecutive odd runs. **Every positive integer trajectory with bounded reduced cofactor ratios at its successive joins is bounded and eventually has a multiplier contraction.** A sparse perturbation with all cofactor ratios equal to one can escape.

## The arithmetic of one join

Use the shortcut map $T(n)=n/2$ on even $n$ and $T(n)=(3n+1)/2$ on odd $n$. At a positive odd input, write $x+1=2^L u$ with $u$ odd. Since $T(x)+1=(3/2)(x+1)$ on odd inputs, there are exactly $L$ consecutive odd steps, with even endpoint $3^L u-1$. There are then exactly $E=v_2(3^L u-1)\ge1$ even steps to the next odd value $y$. Write $y+1=2^R v$, with $v$ odd. The two expressions for $y$ give

$$
2^E y=3^L u-1,\qquad
2^{E+R}v-3^L u=2^E-1. \tag{1}
$$

The shifted odd-run map is standard in the analysis of Collatz cycles. We apply it here to the ratio of the cofactors at two consecutive starts, without imposing a cycle. [Hercher, *There are no Collatz m-Cycles with m ≤ 91*](https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/hercher5.pdf)

Let $s=E+R$ and $H=\max(u/g,v/g)$, where $g=\gcd(u,v)$. Thus $H$ is the height of the positive rational $v/u$ written in lowest terms. Equation (1) gives

$$
0<\Gamma=2^s 3^{-L}(v/u)-1
 =\frac{2^E-1}{3^L u}<\frac1y. \tag{2}
$$

Also $2^E\le 3^L u-1$, so $2^s v<2\cdot3^L u$ and

$$
s<1+L\log_2 3+\log_2 H.
$$

These inequalities use the exact $+1$ throughout the odd run. The ordinary height of either cofactor may be large. The bound on $s$ depends only on the reduced ratio.

## A height bound from logarithms

Write $\log$ for the natural logarithm. Use Matveev's lower bound in its positive-real product-minus-one form with rational bases $2,3,v/u$ and exponents $s,-L,1$. The rational field has degree one. The logarithmic heights of the bases are $\log 2,\log 3,\log H$. The absolute logarithm of $v/u$ is at most $\log H$, and the third height parameter can be taken as $1+\log H$. If $v/u=1$, omit the third factor. For $B=\max(3,s,L)$, the same constant $C=2\cdot10^{11}$ bounds the numerical factors in both cases. Therefore

$$
\log|\Gamma|>-C(1+\log H)(1+\log B).
$$

Together with (2) and $B\le4(1+L+\log H)$, this yields

$$
\boxed{\displaystyle
\log y<C(1+\log H)
 \left[1+\log\!\bigl(4(1+L+\log H)\bigr)\right].
} \tag{3}
$$

This is an effective estimate with a large generic constant. The logarithmic bound is a standard Diophantine input. [Matveev, original paper](https://www.mathnet.ru/links/a2f51e40892b11727729f702fb18a72a/im190_eng.pdf) · [Explicit form in Theorem 2.3 of *On a problem of Pillai involving S-units and Lucas numbers*](https://link.springer.com/article/10.1007/s10998-025-00649-x)

### What (3) forces

- **Bounded ratios throughout a trajectory.** If $H\le H_0$ at every join beyond some finite point, then $L\le\log_2(x+1)$ implies $y\le C_0(1+\log(x+1))^{C_1}$ with effective constants depending only on $H_0$. This is smaller than $x$ for all sufficiently large $x$. From below that threshold the same inequality bounds the next join, so the odd-run starts remain bounded. The intermediate peaks also remain bounded by $3^L u=(3/2)^L(x+1)$. The integer orbit is eventually periodic. On any positive cycle the affine return relation has the form $x=Px+Q$ with $Q>0$, since a positive cycle includes an odd step. Hence $P<1$. Repeating the cycle eventually contracts the cumulative multiplier from the original start.
- **A join that keeps most of its height.** For any fixed $\eta>0$, if $y\ge x^\eta$, then for all sufficiently large $x$ equation (3) gives $\log H\ge c_\eta\log x/\log\log x$, with $c_\eta>0$. To see this, the case $\log H>\log x$ already suffices. Otherwise $B=O(1+\log x)$ by the bound on $L$, so the claim follows from $\log y\ge\eta\log x$. In particular, a join whose multiplier from $x$ to $y$ is at least one has $y\ge x$ by its positive affine offset, and must satisfy the bound with $\eta=1$.

These statements do not bound $H$ for arbitrary trajectories. In particular, a later join may lose multiplier while the cumulative multiplier from the original start remains above one.

## A planted orbit with constant cofactor

The all-odd control from COLLATZ-21 has no completed join, so construct one with infinitely many. Fix $K\ge2$, $u=2^K-1$, and $L_0$ a positive multiple of $2^K$. Set $L_j=2^jL_0$ and $x_j=2^{L_j}u-1$. Follow $T$ for $L_j-1$ steps from $x_j$. The last odd input is $b_j=2\cdot3^{L_j-1}u-1$. At $b_j$ add the jump

$$
J_j=2^{2L_j+1}u-3^{L_j}u-1
$$

to $T(b_j)$. It is positive and divisible by $2^K$, since $3^{L_j}\equiv1\bmod2^K$. The output is now $2x_{j+1}$, and one halving reaches $x_{j+1}$. The odd states increase strictly along the planted orbit and across the joins, so the changed inputs do not conflict with its other odd states. Even steps are unchanged.

Every run has the same cofactor $u$, so every $H$ is one. There is one even step per join and the multiplier between successive starts is $(3/2)^{L_j}/2>1$. Every prefix survives. The genuine join equation would have a right side of $1$ at these joins. The planted one instead has a right side of $1+J_j$, which removes the small quantity in (2). That is the exact point where the argument distinguishes the maps.

As in COLLATZ-21, the jumps are divisible by a prescribed power of two, and the edits form a sparse set. There are $O(\log\log(3+X))$ edited inputs up to $X$, so all fixed-length orbit statistics in natural density are unchanged by the same preimage argument. The jumps here can be large relative to the current value. This control is designed to keep the cofactor fixed across complete joins.

## Checks and scope

Exact arithmetic verified the genuine identities on all 32,768 odd starts below $2^{16}$, including the inequality in (2), and checked 36 planted joins for $2\le K\le10$. The asymptotic bound follows from the stated logarithmic theorem, not the finite checks.

The result gives a constraint on how a hypothetical divergent trajectory can maintain its height. It establishes coefficient contraction for the bounded-ratio family. No bound on the reduced ratios of general Collatz orbits follows here.
