# COLLATZ-23 · Cofactor returns across several odd runs

[COLLATZ-22](../odd-run-join-22/README.md) bounds one join between successive odd runs. Multiplying the join identities cancels every intermediate cofactor. **An exact cofactor return above height $X$ takes at least a constant times $X^{1/5.117}$ shortcut steps.** A bounded reduced endpoint ratio gives a weaker power bound. The same argument also restricts returns after powers of three are removed from the cofactors.

## Multiply the joins

Let $x_0,\ldots,x_r$, $r\ge1$, be successive odd-run starts in a positive integer trajectory of the shortcut map $T$. Write $x_i+1=2^{L_i}u_i$ with $u_i$ odd. Each completed block from $x_i$ to $x_{i+1}$ consists of $L_i$ odd steps and then $E_i\ge1$ halvings. Assume every $x_i\ge X\ge1$. Only these run starts enter the height hypothesis.

Set

$$
A=\sum_{i<r} L_i,\qquad
d=\sum_{i<r}(L_i+E_i),\qquad
s=\sum_{i<r}(E_i+L_{i+1})=d+L_r-L_0 .
$$

The single-join equation from COLLATZ-22 gives

$$
\frac{2^{E_i+L_{i+1}}u_{i+1}}{3^{L_i}u_i}
=1+\frac{2^{E_i}-1}{3^{L_i}u_i},
\qquad
0<\frac{2^{E_i}-1}{3^{L_i}u_i}<\frac1{x_{i+1}} .
$$

Multiplying and taking natural logarithms gives the exact constraint

$$
0<\Theta=s\log 2-A\log 3+\log(u_r/u_0)
<\sum_{i=1}^{r}\frac1{x_i}\le\frac rX . \tag{1}
$$

The strictly positive sign comes from the exact $+1$ in the original rule. No coefficient-survival or nonrepetition hypothesis is needed. Let $H$ be the maximum of the reduced numerator and denominator of $u_r/u_0$, and $B=\max(3,s,A)$. Since $A\le d$, $r\le d$, and $|\log(u_r/u_0)|\le\log H$, equation (1) gives $B=O(d+\log H+1)$.

## A return needs time

If $u_r=u_0$, equation (1) has just two logarithms. Wu and Wang's linear-independence estimate, in the form $\|m\log 2/\log 3\|\gg m^{-4.117}$, gives

$$
\Theta=s\log 2-A\log 3\gg B^{-4.117}.
$$

Here $B=O(d)$. Comparing with (1) gives $r\,d^{4.117}\gg X$. In particular, using $r\le d$,

$$
d\gg X^{1/5.117}=X^{0.195427\ldots}.
$$

Keeping $r$ instead gives a stronger lower bound when the number of joins is small. The implicit constants are independent of the orbit segment. [Wu and Wang, *On the irrationality measure of log 3*, Theorem 1](https://doi.org/10.1016/j.jnt.2014.03.007) · [Fan, Queffélec and Queffélec, Theorem 2.1](https://ems.press/content/serial-article-files/47663?nt=1)

For a general endpoint ratio apply the same Matveev bound as in COLLATZ-22 to $e^\Theta-1$. With $C=2\cdot10^{11}$, it gives $e^\Theta-1>e^{-C(1+\log H)(1+\log B)}$. For $0<z\le1$, $\log(1+z)\ge z/2$. Thus

$$
X<2r\exp\!\left(C(1+\log H)(1+\log B)\right). \tag{2}
$$

For any fixed $H_0$, this gives $d\gg_{H_0} X^{1/(1+C(1+\log H_0))}$ whenever $H\le H_0$. The exponent from this general estimate is very small. [Explicit form of Matveev's bound, Theorem 2.3](https://link.springer.com/article/10.1007/s10998-025-00649-x)

## Distinct cofactors even after removing powers of three

Define $w_i=u_i/3^{v_3(u_i)}$. If $w_j=w_i$, the endpoint ratio $u_j/u_i$ is $3^q$ for an integer $q$. Applying (1) to this subwindow again gives a two-logarithm form,

$$
\Theta_{i,j}=s_{i,j}\log 2-(A_{i,j}-q)\log 3 .
$$

The exponent $A_{i,j}-q$ may have either sign. The same Diophantine bound applies.

**Proposition.** Start at $x_0=X$, and assume the next $k=\lfloor\tfrac12\log X\rfloor$ odd-run starts all stay at or above $X$. For all sufficiently large $X$, the $k+1$ integers $w_0,\ldots,w_k$ are pairwise distinct.

To prove this, put $g=\log_2 3$. For a single block, the bound on $L_i$ and the all-odd growth formula give

$$
x_{i+1}+1\le(3/2)^{L_i}(x_i+1)\le(x_i+1)^g,\qquad
L_i+E_i\le(1+g)\log_2(x_i+1).
$$

Hence $\log(x_i+1)\le g^i\log(X+1)$ and the total elapsed steps through $k$ joins are $O(g^k\log X)$, by geometric summation. Every $s_{i,j}$ is bounded by those steps plus $L_j$. A possible $q=v_3(u_j)-v_3(u_i)$ has absolute value at most $\max(\log_3 u_i,\log_3 u_j)$. The exponents in a putative two-logarithm return are therefore $O(g^k\log X)$. The lower bound and (1) would force

$$
X\ll k\,g^{4.117k}(\log X)^{4.117}
\ll X^{0.948065}(\log X)^{5.117}.
$$

The last exponent uses $4.117\log(g)/2<0.948065<1$. This inequality fails for sufficiently large $X$.

Every divergent positive orbit has arbitrarily large odd-run starts that are minima of their own future sequence of odd-run starts. Apply the proposition at each such minimum. A divergent orbit must produce increasingly many different $w_i$, and in particular **no positive orbit with only finitely many such cofactors after stripping powers of three can diverge**. A positive integer orbit that is not divergent is eventually periodic, since an orbit with distinct states tends to infinity. Every positive cycle contracts the multiplier on each period, as shown in COLLATZ-22.

The proposition gives a separation requirement on any escape. It does not force a return in an arbitrary sequence of stripped cofactors.

## Arithmetic check

Exact rational arithmetic checked the product in (1), the elapsed-step relation, and the power-of-three cancellation on all 112,640 windows among the first ten joins of the 2,048 odd starts below $4096$. For example, $55$ and $167$ are separated by 27 shortcut steps through seven joins, with every odd-run start at least $47$. Their odd cofactors are $7$ and $21$, which agree after stripping powers of three. These checks concern the identities. The time and distinctness bounds use the cited logarithmic estimates.
