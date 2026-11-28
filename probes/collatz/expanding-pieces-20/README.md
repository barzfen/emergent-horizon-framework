# COLLATZ-20 · Starting-height bounds from expanding pieces

[COLLATZ-19](../merge-coverage-19/README.md) bounded the coverage of one fixed smaller-partner search. This probe instead bounds the starting integer directly from the structure of a surviving parity prefix. **A fixed number of expanding pieces forces the least positive start to grow exponentially in prefix length.** The contracting pieces may occur arbitrarily often.

Use the shortcut map $T(n)=n/2$ on even inputs and $T(n)=(3n+1)/2$ on odd inputs. A prefix survives if its cumulative multiplier stays at least one at every step. Fix a finite collection of nonempty binary blocks and consider prefixes that admit a decomposition into pieces $v^r$, with $v$ from the collection and $r\ge1$. Each block has an affine map

$$
F_v(x)=\frac{A_vx+B_v}{M_v},\qquad A_v=3^{\#1(v)},\quad M_v=2^{|v|},\quad B_v\ge0.
$$

A block is expanding if $A_v>M_v$ and contracting if $A_v<M_v$. Equality is impossible for a nonempty block. The basic repeat congruence is the one used in [COLLATZ-11](../repetition-budget-11/README.md). Weaver proves stronger asymptotic bounds under a different accounting of periodic pieces in odd-to-odd coordinates. The statement below is an elementary finite estimate in shortcut coordinates. It charges expanding pieces only, uses their actual growth rates, and also applies if a contracting piece runs along a positive cycle. [Weaver, *Height and periodic-dictionary complexity for rational Collatz trajectories*](https://rstation.ai/problems/collatz/papers/15)

## Bound the length of the prefix

Set

$$
C=\max\!\left(1,\max_v \frac{B_v}{|A_v-M_v|}\right),\qquad
D=\max\!\left(1,\max_v(A_v-M_v)\right),\qquad
Y(x)=\max(x+C,2C).
$$

Choose $\delta>0$ no greater than the smallest per-step logarithmic loss $\log_2(M_v/A_v)/|v|$ over the contracting blocks. If there are no contracting blocks, omit terms containing $1/\delta$ below.

For an expanding piece $v^r$ of length $\ell=r|v|$ starting at $x$, the repetition identity gives

$$
2^\ell\mid (A_v-M_v)x+B_v.
$$

Indeed, multiplying $(A_v-M_v)F_v^r(x)+B_v$ by $2^\ell$ gives $A_v^r((A_v-M_v)x+B_v)$. The first expression is an integer at an actual endpoint, and $A_v$ is odd. For an expanding piece the divisible integer is positive and at most $D\,Y(x)$. Consequently

$$
\ell\le\log_2(DY(x)).
$$

Also, $F_v^r(x)+c=(A_v/M_v)^r(x+c)$ for $c=B_v/(A_v-M_v)\le C$. It follows that $Y(F_v^r(x))\le(A_v/M_v)^rY(x)$. If the piece is contracting instead, its endpoint lies between $x$ and the fixed point $B_v/(M_v-A_v)\le C$. Then $Y(F_v^r(x))\le Y(x)$. This holds even at the fixed point itself.

Put $G=\log_2(DY(n))$. Number the expanding pieces $1,\ldots,k$ in occurrence order and let $\gamma_i=\log_2(A_{v_i}/M_{v_i})/|v_i|>0$. For $R_0=1$ and $R_i=\prod_{j=1}^i(1+\gamma_j)$, the shifted log height just before expanding piece $i$ is at most $G R_{i-1}$. This follows by induction. Contracting pieces do not raise it, and an expanding piece of length $\ell_i$ raises it by at most $\gamma_i\ell_i$, with $\ell_i\le GR_{i-1}$.

Thus the expanding lengths sum to at most $G\sum_{i=1}^k R_{i-1}$. Their total logarithmic multiplier gain is at most

$$
G\sum_{i=1}^k \gamma_iR_{i-1}=G(R_k-1).
$$

Survival at the endpoint implies that the contracting pieces lose at most that gain. Each contracting step contributes at least $\delta$ to the loss averaged over its complete piece. The entire length $d$ therefore satisfies the explicit estimate

$$
d\le G\left(\sum_{i=1}^k R_{i-1}+\frac{R_k-1}{\delta}\right).
$$

The proof only needs the endpoint multiplier condition once the decomposition is given. In particular it applies to every coefficient-surviving prefix.

## Consequences for the least start

Let $\lambda=\log_2(3/2)$ and $g=1+\lambda=\log_2 3$. Every expanding piece has $\gamma_i\le\lambda$. Bounding the products by $g^i$ and $Y(n)$ by $n+2C$ yields

$$
d\le (g^k-1)(1/\lambda+1/\delta)\log_2(D(n+2C)).
$$

For a fixed collection and bounded $k$, this forces an exponential lower bound in $d$ for every positive representative, including the least. The bound still diverges with growing $k$. For any fixed $\epsilon>0$, if $k\le(1-\epsilon)\log_g d$, then $n\ge D^{-1}2^{c d^\epsilon}-2C$, with $c=(1/\lambda+1/\delta)^{-1}$. Equivalently, a single fixed positive start that survives arbitrarily long must have at least $\log_g d-O(1)$ expanding pieces in every such decomposition of its length-$d$ prefix, with the constant allowed to depend on the start and the collection.

For example, take expanding blocks $1,110$ and contracting blocks $0,01$. Here $C=5$, $D=1$, and $\delta=\tfrac12\log_2(4/3)$. The contracting part can use an arbitrary sequence of the two contracting blocks. Its number of pieces is immaterial to the bound. The same argument also allows a variable collection of contracting blocks whenever the same constants $C$ and $\delta$ bound all their fixed points and per-step losses.

## Check and scope

For an arithmetic check, use the blocks $1,110,11100,0,10,01,100$. A deterministic Python run generated 15,000 concatenations with an initial $1$-run of length 1–12, followed by 1–8 random pieces with repeat counts 1–7. It decoded the least positive residue for each word, iterated it, and retained 4,974 surviving prefixes, the longest of length 142. Each retained prefix passed exact checks of the divisibility and shifted-height inequalities. The logarithmic aggregate bound was checked numerically. The proof above gives the uniform statement.

This establishes a size bound for a restricted family of prefixes. The remaining gap is to control the number of expanding pieces, or find a different arithmetic constraint, for an arbitrary potential positive survivor. The result permits prefixes with many expanding pieces and does not force the unrestricted $m_d$ to grow.
