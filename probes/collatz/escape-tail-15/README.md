# COLLATZ-15 · Every escaping orbit has a coefficient-surviving tail

[COLLATZ-14](../backward-terminal-14/README.md) asks whether a symbolic branch whose multiplier never contracts can keep fitting a fixed positive starting budget. This note identifies exactly which part of Collatz that question covers.

**PROVED.** A divergent positive integer orbit exists if and only if there is a positive integer start $n>1$ whose coefficient never contracts. Every divergent orbit has such a tail. In addition, its actual values and its cumulative multiplier are asymptotically proportional. The divergence question and the nontrivial-cycle question can therefore be treated separately.

Garcia and Tal proved power-saving sparsity for single orbit sets via uniform interval bounds. The deduction of summable reciprocals and unbounded multiplier drift from their estimate has appeared on MathOverflow. A separate Collatz project also records the reduction to a coefficient-surviving tail. We give a short explicit count for the standard shortcut map and apply it to the height and budget tests developed here. [Garcia and Tal (1999), equation (6) and Corollary 1](https://matwbn.icm.edu.pl/ksiazki/aa/aa90/aa9033.pdf) · [Summability discussion](https://mathoverflow.net/questions/513539/is-it-known-that-a-divergent-collatz-trajectory-must-have-summable-reciprocals) · [Coefficient stopping and orbitwise tails](https://github.com/GettysburgResearch/collatz/blob/main/research/RESULTS_CATALOG.md#coefficient-stopping-and-orbitwise-tails)

## Count the values in one orbit

Let $x_i=T^i(n)$ be a nonrepeating positive integer orbit of the shortcut map, and let $\mathcal O=\{x_i:i\ge0\}$. Nonrepetition makes $T^d$ injective on this set for every fixed $d$, since shifting two different orbit indices by $d$ gives different indices and values.

Take $d=\lfloor\log_2 X\rfloor$ for $X\ge2$. A parity word of length $d$ specifies one residue class modulo $2^d$, so at most two starts in $[1,X]$ realise it. Write $a$ for the odd count of a word. The affine endpoint of a start $u$ obeys

$$
T^d(u)\le \frac{3^a}{2^d}u+(3/2)^d-1 .
$$

The offset bound follows by taking the odd affine step at every position, which maximizes the offset. If $a\le3d/5$ and $u\le X$, then $T^d(u)\le3\cdot 3^{3d/5}$. Thus there are at most $3 X^{(3/5)\log_2 3}$ such starts in the orbit, by injectivity of their images.

Put $\rho=h_2(3/5)=0.9709505944\ldots$, with $h_2$ the binary entropy. For the high-odd words, assign independent symbolic bits with one-probability $3/5$. Each word with $a>3d/5$ has mass at least $2^{-\rho d}$, so at most $2^{\rho d}$ words meet the high-odd condition. This is a count of words, with no probabilistic assumption about the actual orbit. Since $(3/5)\log_2 3<\rho$, the two bounds give

$$
|\mathcal O\cap[1,X]|\le5X^\rho .
$$

The inequality also holds for $1\le X<2$. This uses Terras's finite parity coding. [Terras (1976), Theorem 1.2](https://doi.org/10.4064/aa-30-3-241-252)

## Normalize the multiplier on the actual orbit

Summing the count over dyadic value intervals gives, for $m\ge1$,

$$
\sum_{\substack{x\in\mathcal O\\x\ge m}}\frac1x
\le K m^{\rho-1},\qquad K=\frac{5\,2^\rho}{1-2^{\rho-1}}.
$$

In particular the reciprocal sum of the orbit is finite. Let $P_i=3^{a_i}/2^i$ be the cumulative multiplier from the first $i$ inputs. Each odd step multiplies the actual state by $3/2$ times $1+1/(3x_j)$. Each even step contributes only its multiplier $1/2$. Consequently

$$
\frac{x_i}{P_i}
=n\prod_{\substack{0\le j<i\\ x_j\ {\rm odd}}}\left(1+\frac{1}{3x_j}\right)
\ \longrightarrow\ L,\qquad n\le L<\infty.
$$

The product converges by reciprocal summability. Nonrepetition of positive integer values gives $x_i\to\infty$, so $P_i\to\infty$. Therefore $P_i$ has an attained global minimum at some finite index $j_*$. Starting the orbit at $x_{j_*}$ gives cumulative multipliers $P_{j_*+k}/P_{j_*}\ge1$ for all $k$. This is a coefficient-surviving tail on the same orbit.

Conversely, if $n>1$ has $P_i\ge1$ for every $i$, then $x_i\ge n$ by the nonnegative affine offset. A periodic positive tail has multiplier strictly below one per period. Its affine return equation is $Mx=Ax+B$ with $x>0$ and $B>0$, since a positive cycle must contain an odd step. Repeating such a period would eventually make the original cumulative multiplier less than one. Thus a positive coefficient survivor is nonrepeating and divergent.

## Consequences for the earlier tests

- **Height.** Since $x_i\le L P_i$, the running maximum of $P_i$ has the full [COLLATZ-10](../orbit-height-10/README.md) height floor $c N^{1/h_2(\log_3 2)}(\log N)^{1/(2h_2(\log_3 2))}$ on any divergent orbit, with a trajectory-dependent constant. The earlier loss of a factor $N$ in the general coefficient-survivor estimate disappears.
- **Budget.** The finite ratio $L$ provides a fixed normalized terminal budget for the tail in COLLATZ-14. Conversely, infinitely many fits under a fixed budget on a coefficient-surviving word force a positive integer lift by that probe. This equivalence for divergence requires no exponential-growth hypothesis.
- **Location of a surviving tail.** Restart a divergent orbit at its least value $m$. The reciprocal bound gives $x_i/(mP_i)\le\exp(Km^{\rho-1}/3)$ for all $i$. At the global multiplier minimum $P_{j_*}\le1$, the new coefficient-surviving start therefore lies in $[m,m\exp(Km^{\rho-1}/3)]$, an interval of width $O(m^\rho)$. Any coefficient contraction from the least value $m$ is correspondingly small, since $P_i\ge\exp(-Km^{\rho-1}/3)$.

This gives an exact reformulation of the divergence case. Proving every positive start eventually has a coefficient contraction would exclude divergence. Nontrivial positive cycles remain a separate case. We checked the low-multiplier image bound and parity-class counts on 16,368 finite prefix/start combinations, and the affine product identity on 750 ordinary steps. The proof does not depend on those checks. AI assistance was used for source review, derivation, checks and drafting. No priority claim is made.
