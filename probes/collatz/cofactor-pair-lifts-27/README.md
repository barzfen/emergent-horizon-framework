# COLLATZ-27 · Finite lifts of a fixed pair of cofactors

[COLLATZ-26](../cofactor-observer-26/README.md) reconstructed a join from two exact stripped cofactors and their run lengths. **If the run lengths are discarded, a fixed pair of exact stripped cofactors and a fixed number of intervening joins still have only finitely many genuine positive integer histories.** The number of possible ending integers has a bound that depends only on the number of joins. Along an escaping orbit, every fixed cofactor pair at any fixed lag occurs only finitely often.

## Expand a window without losing the exact offsets

Use the shortcut Collatz map and let $x_0,\ldots,x_r$, $r\ge1$, be successive odd-run starts. Write

$$
Y_i=x_i+1=2^{L_i}3^{a_i}w_i,\qquad \gcd(w_i,6)=1.
$$

The block from $x_i$ to $x_{i+1}$ consists of $L_i$ odd steps followed by $E_i\ge1$ halvings. Its exact identity is

$$
2^{L_i+E_i}Y_{i+1}=3^{L_i}Y_i+2^{L_i+E_i}-2^{L_i}.
$$

Put $D_i=\sum_{j=0}^i(L_j+E_j)$, $D_{-1}=0$, $d=D_{r-1}$, $A=\sum_{j=0}^{r-1}L_j$, and $A_i=\sum_{j=i+1}^{r-1} L_j$. Define $U=3^A Y_0$, $V=2^dY_r$, and

$$
C_i^-=2^{D_i-E_i}3^{A_i},\qquad C_i^+=2^{D_i}3^{A_i}.
$$

Composing the joins gives

$$
U+\sum_{i=0}^{r-1}(C_i^+-C_i^-)-V=0. \tag{1}
$$

Here the superscripts mark the sign in (1). Both $C_i^-$ and $C_i^+$ are positive integers.

## The valuations rule out partial cancellation

In the list $C_0^-,C_0^+,C_1^-,C_1^+,\ldots,C_{r-1}^-,C_{r-1}^+,V$, the powers of two dividing the terms increase strictly. This follows from $L_i,E_i\ge1$ and from $v_2(V)=d+L_r>d$. A sum of signed integers with a unique term of least two-adic valuation cannot vanish. So a nonempty zero subsum of (1) must contain $U$, and must also contain $-C_0^-$, the only term at the same valuation as $U$.

The same argument propagates through the window. Just before the two terms for join $i$, the forced partial sum is

$$
2^{D_{i-1}}3^{A_i+L_i}Y_i.
$$

Its valuation $D_{i-1}+L_i$ matches only the next negative term. Subtracting that term gives $2^{D_i}3^{A_i}x_{i+1}$, of valuation $D_i$ because $x_{i+1}$ is odd. Hence the positive term at $D_i$ must also be included. Adding it gives $2^{D_i}3^{A_i}Y_{i+1}$, the partial sum for the next join. After the last join the partial sum is $V$, so the terminal term $-V$ must be included too.

Thus the only zero subsums are the empty sum and the whole equation. This uses the exact offset at every join and the exact halving lengths.

## Count lifts with the run lengths hidden

Divide (1) by $2^d=C_{r-1}^+$ and move that last positive offset to the right with the sign orientation below:

$$
Y_r-\frac{3^A}{2^d}Y_0
-\sum_{i=0}^{r-2}\frac{C_i^+}{2^d}
+\sum_{i=0}^{r-1}\frac{C_i^-}{2^d}=1. \tag{2}
$$

Fix $w_0,w_r$. Treat these as fixed coefficients in the first two terms. The other coefficients are $1$ or $-1$, and all $n=2r+1$ variables are rational products of powers of two and three. Their coordinatewise multiplicative group has rank $2n$.

The theorem of Evertse, Schlickewei and Schmidt bounds the number of nondegenerate solutions of a linear equation with right side one over a rank-$t$ multiplicative group by $\exp((6n)^{3n}(t+1))$. The no-partial-cancellation proof gives precisely the required nondegeneracy for (2). Thus the number of solutions arising from genuine windows is at most

$$
B_r=\exp\!\left((6(2r+1))^{3(2r+1)}(4r+3)\right).
$$

This uniform bound does not depend on the fixed cofactor values. It is a counting bound and gives no practical enumeration or height bound. [Evertse, Schlickewei and Schmidt, Theorem 1.1](https://annals.math.princeton.edu/2002/155-3/p04)

Each solution specifies $Y_r$ through its first coordinate, hence specifies $x_r$. It also has only finitely many possible starting integers. Indeed the ratio of the source variable, after removing its coefficient $w_0$, to the first negative-offset magnitude $C_0^-/2^d$ is $3^{L_0+a_0}$. The exponent $L_0+a_0$ is thus fixed by the solution. There are finitely many splits with $L_0\ge1,a_0\ge0$, each specifying one starting integer. From a start the actual orbit is deterministic. The bound $B_r$ applies to destinations, not to the number of starting integers per destination.

There can be several lifts. For example, $15\to5$ and $5\to1$ are genuine one-join windows, both with $(w_0,w_1)=(1,1)$, and their destinations differ.

## Consequence on a hypothetical escape

Every positive integer in a divergent orbit is visited at most once, so a fixed ordered pair of stripped cofactors at lag $r$ occurs at most $B_r$ times. For a finite set of cofactor labels and any $K$, only finitely many pairs of visits to that set can lie at most $K$ joins apart. Sum the finite bounds over the ordered pairs of labels and $1\le r\le K$.

Therefore if a divergent orbit returns to one fixed cofactor, or to a fixed finite set of cofactors, infinitely often, its consecutive visit gaps **tend to infinity**. This strengthens the zero-density result of [COLLATZ-25](../cofactor-frequency-25/README.md). It still allows returns with unbounded gaps and does not establish that any return is forced.

Exact arithmetic checked the identity and valuation chain on 14,336 windows and exhausted all subsets of the terms on a further bounded selection of 320 windows. The proof gives the unrestricted fixed-lag result.
