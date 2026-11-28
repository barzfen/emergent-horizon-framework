# COLLATZ-21 · Plant a divergent orbit as a proof control

A proposed nondivergence argument should identify which exact part of the shortcut rule it uses. This note constructs positive-integer maps with an explicit divergent all-odd orbit that agree with the original rule on prescribed finite tests, reproduce every fixed-length orbit statistic in natural density, and differ only by small relative changes above any prescribed height.

The idea of testing arguments against modified maps has precedents, including sign comparisons and countermodels for occupation statistics. This construction keeps the odd multiplier $3/2$, keeps all odd offsets positive, and makes the changes on a single sparse orbit. We make no priority claim. [Sign-sensitivity discussion](https://rstation.ai/r/collatz/posts/25) · [*What an occupation measure cannot see*](https://amral.evemisslab.com/en/collatz/papers/casp-no-gos/)

## Construction

Let $T(n)=n/2$ for even $n$ and $T(n)=(3n+1)/2$ for odd $n$. Fix a modulus $M=2^v u$ with $u$ odd, a time horizon $h\ge1$, and a height threshold. Put

$$
K=v+h+1,\qquad J=2^{K-1}u=M2^h .
$$

Choose a positive integer $a_0$ large enough that $n_0=2^K a_0-1$ exceeds the height threshold. Define

$$
a_{j+1}=
\begin{cases}
3a_j/2,&a_j\text{ even},\\
(3a_j+u)/2,&a_j\text{ odd},
\end{cases}
\qquad n_j=2^K a_j-1.
$$

The $a_j$ are positive integers and grow at least by a factor $3/2$. Let $E=\{n_j:a_j\text{ odd}\}$ and define $S(n)=T(n)+J$ on $E$, with $S(n)=T(n)$ elsewhere. Since $T(n_j)=3\cdot 2^{K-1}a_j-1$, we have $S(n_j)=n_{j+1}$ in both cases. Thus $n_0,n_1,\ldots$ is a divergent orbit of $S$. Every state is odd and its cumulative affine multiplier through $d$ steps is $(3/2)^d$. The changed odd numerators are $3n+1+2J$. Both available offsets are positive.

For example, $M=1,h=2,a_0=1$ gives $K=3,J=4$ and a planted path $7\to15\to23\to39\to63\to95\to\cdots$. The first edited step sends $7$ to $15$ in place of $11$.

## What the control preserves

1. **Any prescribed finite observations.** The two maps agree pointwise below $n_0$. Given a finite collection of finite $T$-orbit segments, choose $n_0$ above every state in those segments.
2. **Residues through the chosen horizon, uniformly in the start.** For any positive $n$, induction gives $S^i(n)-T^i(n)\equiv0\bmod M2^{h-i}$ for $0\le i\le h$. At time $i<h$, the difference is even, so both inputs have the same parity. Applying $T$ divides the difference by two or multiplies it by $3/2$. The extra term from $S$ is a multiple of $J$, so the induction continues. In particular the first $h$ parity decisions agree for every start, and the states agree modulo $M$ through time $h$. Take $M$ to be a common multiple to handle any finite list of moduli.
3. **Every fixed-length orbit statistic in natural density.** The edits satisfy $|E\cap[1,X]|=O(\log(2+X))$ by geometric growth. If a start $n\le X$ first encounters an edit at time $i<d$, both maps have followed $T$ up to that input. The ordinary shifted height satisfies $T^i(n)+1\le(3/2)^i(X+1)$, and each edited input has at most $2^i$ preimages under $T^i$. Summing over $0\le i<d$ gives at most $O_d(\log(2+X))$ starts $n\le X$ whose first $d$ transitions differ. This holds for every fixed $d$ on the same constructed map. In particular, each fixed-length parity word has the same natural density under $S$ and $T$, although the exact finite parity laws for individual starts are only guaranteed through the prescribed horizon.
4. **Arbitrarily small relative changes.** At an edited input the difference is exactly $J$, so $|S(n)-T(n)|/n\le J/n_0$. The planted path itself satisfies
   $$
   0\le (n_d+1)(2/3)^d-(n_0+1)\le 2J,
   $$
   since each step's added term is either zero or $J$, and the geometric sum of its normalized weights is at most $2$. Increasing $a_0$ makes the relative error from the formal all-odd height profile as small as prescribed, uniformly in $d$.

The assertions about limiting statistics concern events on finite orbit segments and natural density over starts. They do not transfer a statement about each individual infinite trajectory.

## Use as a test

Any proposed nondivergence certificate deduced solely from these preserved observations would apply to $S$ as well, where the conclusion is false. The useful test is to mark the first lemma that fails on the planted orbit. A candidate using exact affine offsets at overlapping time cuts has an arithmetic input that this control can change. A candidate using only fixed-horizon frequencies, positive odd offsets, or approximate multiplier growth still needs an additional input.

This is a way to diagnose a proof attempt. It supplies neither an invariant for $T$ nor a proof of its nondivergence. A direct arithmetic check covered 63 modulus/horizon choices, constructed 100 path states for each, and verified the residue congruences on both ordinary and planted-path starts. The argument above gives the unbounded statement.
