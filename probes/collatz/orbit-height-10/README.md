# COLLATZ-10 · A growth floor for nonrepeating orbits

[COLLATZ-09](../regular-growth-09/README.md) used a two-sided power band to force enough odd steps in **each** window. This probe replaces that condition with an average over overlapping windows. It gives a bound on actual orbit height without a power-band assumption.

**PROVED.** Let $p_i/q$ be a nonrepeating rational orbit of the shortcut map, with the fixed odd denominator $q>0$ and integer numerators $p_i$. Set $X_N=\max_{0\le i\le N}|p_i|$, $\alpha=\log_3 2$, and $h=h_2(\alpha)$, where $h_2(t)=-t\log_2t-(1-t)\log_2(1-t)$. For all sufficiently large $N$,

$$
X_N\ \ge\ c\,N^{1/h}(\log N)^{1/(2h)}
$$

for some $c>0$. The exponents are $1/h=1.0526808586\ldots$ and $1/(2h)=0.5263404293\ldots$. This concerns the running maximum. Individual orbit values can decrease.

## Averaging the log changes

In fixed-denominator coordinates the even step is $p\mapsto p/2$, and the odd step is $p\mapsto(3p+q)/2$. Since the $p_i$ are distinct integers, $|p_i|\to\infty$. Choose a fixed index $L$ after which $|p_i|>q$. With $w_i$ the parity bit, for $i\ge L$ we have the exact identity

$$
\log_2|p_{i+1}|-\log_2|p_i|
=w_i\log_2 3-1+\epsilon_i,\qquad
\epsilon_i=w_i\log_2\left|1+\frac{q}{3p_i}\right|.
$$

The absolute correction satisfies $|\epsilon_i|=O_q(1/|p_i|)$. Each positive magnitude occurs at most twice, so $\sum_{i=L}^{N-1}|\epsilon_i|=O_q(\log(N+2))$. The implied constant can depend on $q$. This harmonic bound uses distinctness and holds even if the smallest magnitude in the late part of the orbit grows slowly.

Let $a_i(d)$ count odd inputs in the length-$d$ window starting at $i$, and sum the log identity over all windows with $L\le i\le N-d$. Write $M=N-d-L+1$. When $M\ge d$, the sum of log endpoint differences telescopes to the last $d$ logarithms minus the first $d$, hence is at least $-d\log_2 X_N$. Each $\epsilon_i$ is counted at most $d$ times. Consequently

$$
\frac1M\sum_{i=L}^{N-d} a_i(d)
\ \ge\ \alpha d -
O_q\!\left(\frac{d\,(\log X_N+\log(N+2))}{M}\right).
$$

The average is taken within one trajectory, using an exact telescope.

## Pack distinct windows of that average weight

If $X_N>N^2$, the claimed lower bound holds for large $N$, since $1/h<2$. Otherwise choose $d=\lceil\log_2(2X_N+1)\rceil=O(\log N)$, so $M$ is of order $N$. Any two identical length-$d$ parity words force the difference between their starting numerators to be divisible by $2^d$. Distinct numerators in $[-X_N,X_N]$ cannot have that difference. Thus the $M$ words in the average above are distinct. This is the parity separation used by Dubickas and in [COLLATZ-06](../parity-complexity-06/README.md), here applied to a fixed odd denominator. [Terras (1976), Theorem 1.2](https://doi.org/10.4064/aa-30-3-241-252) · [Dubickas (2009), Theorem 5 and §5](https://doi.org/10.1017/S0017089508004655)

The average odd count is at least $\alpha d-1$ for all sufficiently large $N$, because the error in the average is $O_q((\log N)^2/N)$. Put $t=\lfloor\alpha d\rfloor-2$ and write $z_+=\max(z,0)$. Then

$$
M\le\sum_{i=L}^{N-d}(a_i(d)-t)
\le\sum_{i=L}^{N-d}(a_i(d)-t)_+
\le\sum_{k>t}(k-t)\binom dk .
$$

The last inequality uses distinctness. The binomial ratios above $t$ are bounded by a constant $r<1$ for large $d$, since $\alpha>1/2$. Thus the weighted tail is at most $\binom dt\sum_{j\ge1}jr^j=O(\binom dt)$. Stirling's formula and $t=\alpha d+O(1)$ give $O(2^{hd}/\sqrt d)$. Finally $2^d=O(X_N)$, and $d$ is at least of order $\log N$ because $N+1$ distinct integers in $[-X_N,X_N]$ require $X_N\ge N/2$. We obtain

$$
N\ \le\ C\,\frac{X_N^h}{\sqrt{\log N}},
$$

which gives the stated growth floor. This weighted count allows some windows to contain relatively few odd steps. Their deficit must be balanced by the available words of higher odd count.

## Consequences for coefficient survivors

For a hypothetical positive-integer coefficient survivor, $P_i=3^{a_i}/2^i\ge1$ for every $i$, where $a_i$ counts odd steps in the first $i$ moves. [COLLATZ-03](../survivor-branches-03/README.md) excludes repetition in this case. Let $B_N=\max_{i\le N}P_i$. The affine height estimate in [COLLATZ-05](../multiplier-band-05/README.md) gives $X_N\le B_N(p_0+N/3)$, hence

$$
B_N\ge c'\,N^{1/h-1}(\log N)^{1/(2h)}.
$$

In particular, a running multiplier bounded above by a constant times $N^{0.0526808586\ldots}$, with the exact exponent $1/h-1$, is impossible even with irregular fluctuations. For a branch with $\sum_{i:w_i=1}1/P_i<\infty$, the same affine estimate gives $X_N=O(B_N)$, so the full height exponent applies to $B_N$.

The result supplies a necessary growth floor. It leaves open nonrepeating positive integer trajectories whose heights grow quickly enough. [COLLATZ-11](../repetition-budget-11/README.md) rules out a family of fast symbolic branches with long early repeats. The argument uses classical parity coding and the height-sensitive separation of parity words. We checked the log identities as exact rational products for signed fixed-denominator trajectories and compared the finite weighted-tail bound with the optimal mean-weight packing at small lengths. The proof does not depend on those finite checks. AI assistance was used for derivation, checks and drafting. No priority claim is made.
