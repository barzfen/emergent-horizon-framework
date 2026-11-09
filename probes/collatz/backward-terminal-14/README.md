# COLLATZ-14 · A backward test for positive starting values

[COLLATZ-13](../joint-window-13/README.md) reconstructed a finite orbit segment from consecutive fitting windows. Here we use the parity history alone to find the smallest terminal value attainable from a positive starting integer greater than one.

**PROVED.** The least attainable terminal value divided by its cumulative multiplier is nondecreasing as the prefix grows. A fixed bound on this ratio at infinitely many lengths forces one actual starting integer. For the standard map, [COLLATZ-04](../offset-bound-04/README.md) already excludes such fits at depth 447 on every coefficient-surviving branch if the fixed bound is at most $5{,}205{,}340{,}379$.

## Recover the start from the terminal state

Use the numerator map $T_q$ for a fixed odd $q>0$, with even step $p/2$ and odd step $(3p+q)/2$. For a prefix of $N$ parity bits, let

$$
y=\frac{Ap+B}{M},\qquad A=3^{a_N},\quad M=2^N,\quad P_N=A/M .
$$

Here $p$ is the starting numerator, $y$ the terminal numerator, and $B\ge0$ is the prefix offset. The past prefix imposes the terminal congruence

$$
y\equiv M^{-1}B\pmod A .
$$

This is also sufficient for an integer terminal value $y$ to come from some integer start following the prefix. Indeed $p=(My-B)/A$ is integral by the congruence and satisfies $Ap+B\equiv0\pmod M$. Because $A$ is odd and the parity word determines exactly one start class modulo $M$, this congruence gives the required class. If a $D$-bit future window is also prescribed, it imposes its own terminal residue modulo $2^D$. The two terminal residues combine into one class modulo $A2^D$ by the Chinese remainder theorem. Positivity of the reconstructed start is then checked directly. [Terras (1976), Theorem 1.2](https://doi.org/10.4064/aa-30-3-241-252) · [Bernstein and Lagarias (1996), §4](https://websites.umich.edu/~lagarias/doc/bernstein.pdf)

This is an equivalent encoding of the starting-residue condition. It makes a height bound at the terminal state usable without requiring future bits.

## An exact test for a fixed budget

Let $r_N$ be the least integer $p\ge2$ satisfying the $N$-bit starting-residue condition. Because the affine slope is positive, the least attainable terminal value $y_N^{\min}$ over these starts satisfies

$$
\frac{y_N^{\min}}{P_N}=r_N+\frac BA
=r_N+\frac q3\sum_{\substack{0\le j<N\\w_j=1}}\frac{1}{P_j}.
$$

When the prefix grows by one bit, the residue class either retains $r_N$ or advances it by exactly $2^N$. The normalized offset adds $q/(3P_N)$ on an odd step and zero otherwise. Thus $y_N^{\min}/P_N$ is nondecreasing. The condition $y_N^{\min}\le C P_N$ at infinitely many lengths implies $r_N\le C$ at every length. The nondecreasing integers $r_N$ then stabilise, and that constant numerator follows the whole word. The converse holds for a given budget $C$ if the branch has a lift with numerator $p\ge2$ and the normalized terminal values of that lift never exceed $C$.

For a fast branch with $P_N=2^{\chi N+o(N)}$, $\chi>0$, the normalized offset series converges. Hence there exists a finite budget $C$ with infinitely many fits exactly when the word has a lift with numerator $p\ge2$ at the chosen denominator. The same $C$ works at every length. For $q=1$ and a coefficient-surviving branch, such a start would be a counterexample to Collatz.

For a finite exclusion, take $q=1$ and $C\le5{,}205{,}340{,}379$. A fit at depth 447 would produce a start $2\le r_{447}\le C$ following that prefix. COLLATZ-04 certifies a coefficient contraction by step 447 for every start in that range. This contradicts prefix survival. The monotone test therefore excludes all later fits for that budget. [COLLATZ-04 result snapshot](../offset-bound-04/results.json)

## Exponential height cutoffs also work without lookahead

For a branch of exponent $\chi>0$, suppose $y_N^{\min}\le2^{\eta N}$ with $\eta>\chi$. Then $r_N\le2^{(\eta-\chi+o(1))N}$. Two different least starts at passing lengths $N<N'$ differ by a nonzero multiple of $2^N$. Along changes at unbounded passing lengths this gives

$$
\liminf N'/N\ \ge\ \frac{1}{\eta-\chi}.
$$

In particular, infinitely many passes with successive ratios eventually bounded strictly below this factor force a single starting integer. This uses only the first $N$ bits of each pass.

For the biased symbolic family of COLLATZ-12 with odd frequency $\theta>\log_3 2$, write $\chi=\theta\log_2 3-1$ and $h=h_2(\theta)$. If $0<\eta-\chi<h$, the positive terminal test almost surely fails at all sufficiently large $N$. To see this, restrict to the event that $P_N\ge2^{(\chi-\epsilon)N}$ and the prefix has odd frequency within a small fixed distance of $\theta$. These conditions hold eventually almost surely by the strong law. A pass then gives a positive start bounded by $2^{(\eta-\chi+\epsilon)N}$, so at most that many possible $N$-bit words. Each typical word has probability at most $2^{-(h-\delta)N}$, where $\delta$ can be made arbitrarily small by narrowing the frequency interval. For sufficiently small $\epsilon,\delta$, the product of these bounds is summable. The conclusion persists after fixing any finite prefix and intersecting with the positive-probability survival event of COLLATZ-12. This probability argument concerns the symbolic family.

## Reproduce and scope

Run `python3 verify.py` in this directory. The verifier checks 1,530 finite words and 768 past/future junctions across odd denominators $1,3,5$, and reconstructs the genuine start $27$. In the 1,600-bit symbolic example from COLLATZ-13, the smallest positive start has 1,595 bits. Its least terminal state has 1,894 bits, exceeding $2^{312}$, using the prefix alone.

The fixed-budget test is exact. An exclusion for every positive budget, or an actual positive lift that survives indefinitely, would go beyond the results here. AI assistance was used for derivation, checks and drafting. No priority claim is made.
