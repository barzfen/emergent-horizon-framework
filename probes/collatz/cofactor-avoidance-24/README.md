# COLLATZ-24 · How long can cofactor returns be postponed?

[COLLATZ-23](../cofactor-returns-23/README.md) showed that a return at high odd-run starts takes time. Here we test whether a recurrence can be forced on a bounded horizon. **For every prescribed number of joins, the genuine Collatz rule has arbitrarily large positive starts whose cofactors are pairwise distinct after removing powers of two and three from the run starts plus one.** This can hold even when every one of those cofactors is identical modulo a prescribed modulus. There are also explicitly convergent examples whose first exact repetition occurs in the cycle through one.

## A construction with identical residues

At the start $x$ of an odd run, define $L=v_2(x+1)$, $u=(x+1)/2^L$, and $w=u/3^{v_3(u)}$. We call $w$ the stripped cofactor. Use the shortcut map $T(x)=x/2$ for even $x$ and $T(x)=(3x+1)/2$ for odd $x$.

Fix an integer $r\ge1$, a modulus $Q\ge1$, and any positive multiple $b$ of $3Q$. Start at

$$
x_0=2^{3(r+1)}b-5.
$$

The shortcut word $110$ has map $F(x)=(9x+5)/8$ on its residue class $3\bmod8$, and $F(x)+5=(9/8)(x+5)$. Thus the next $r+1$ blocks all use $110$, with run starts

$$
x_i=9^i2^{3(r+1-i)}b-5,\qquad 0\le i\le r.
$$

Indeed, each of the displayed inputs is $3\bmod8$, and substituting its value into $F$ gives the next state at the block boundary. These run starts increase. Every cumulative multiplier through the $r+1$ blocks is at least one, since the three within-block factors are $3/2,\ 9/4,\ 9/8$. This is the known affine shadow of the negative cycle through $-5$. [MathWorld, *Collatz Conjecture*](https://mathworld.wolfram.com/CollatzConjecture.html)

At each displayed start $L_i=2$, and

$$
w_i=u_i=9^i 2^{3(r+1-i)-2}b-1.
$$

The equality $w_i=u_i$ holds because $b$ is a multiple of three. The cofactors increase strictly, since $u_{i+1}+1=(9/8)(u_i+1)$. Nevertheless, $w_i\equiv-1\bmod Q$ for every $i$. A repeat in a fixed residue system therefore gives no uniform bound on the time to an exact return, even for genuine coefficient-surviving segments. A finite list of moduli is covered by taking their least common multiple.

## The first return can occur inside the cycle through one

The same construction admits explicitly convergent choices if we only require $3\mid b$. Put $m=r+1$. Choose $e$ arbitrarily large in a residue class such that

$$
2^e\equiv -5\pmod{3\cdot9^m}.
$$

This is possible because $2$ generates the units modulo every power of three. Its order modulo $3^t$ is $2\cdot3^{t-1}$, as follows from $v_3(4^k-1)=1+v_3(k)$. Set $b=(2^e+5)/9^m$, a positive multiple of three. The prescribed $m$ blocks end at $9^m b-5=2^e$, which then halves to $1$. Take $e$ large enough that all displayed cofactors exceed one.

The only odd-run starts before $1$ are $x_0,\ldots,x_r$. Their stripped cofactors are distinct and all exceed one. The next run starts at $1$ and has stripped cofactor one, which first repeats on the next lap of the trivial cycle. Thus even a trajectory known to reach $1$ can avoid all earlier cofactor returns.

## More joins at the same starting scale

A second construction gives about $0.53246\log n$ joins with distinct stripped cofactors, with $\log$ denoting the natural logarithm. Let $\lambda=\log_2(3/2)$ and $a_j=\lceil j/\lambda\rceil$ for $0\le j\le r+1$. Use $r+1$ blocks $1^{a_j-a_{j-1}}0$ for $1\le j\le r+1$. Each odd run has length one or two. After block $j$ the base-two logarithm of the cumulative multiplier is $\lambda a_j-j\ge0$, so the word survives. Every join between the observed run starts uses exactly one halving.

The word has length $d=a_{r+1}+r+1$. Its positive starts form one class $n=n_*+2^d t$, with $1\le n_*\le2^d$, by the finite parity-residue bijection. At run start $i$, $0\le i\le r$, the cofactor $u_i(t)$ is an affine integer function of $t$ with slope

$$
3^{a_i}2^{d-a_i-i-(a_{i+1}-a_i)}.
$$

The slopes have different powers of three, so a pair of cofactors can coincide for at most one $t$. Also, every run start after the first has $x_i\equiv1\bmod3$, because an odd shortcut followed by a halving always has that residue. Hence $3\nmid u_i(t)$ for $i>0$. For the first cofactor, whose slope is a power of two, choose one class of $t\bmod3$ with $3\nmid u_0(t)$. Among $\binom{r+1}{2}+1$ positive candidates in that class at least one avoids all the pair collisions. All the stripped cofactors then equal the distinct $u_i(t)$.

The chosen $t$ can be at most $3\binom{r+1}{2}+5$. This yields $\log n=d\log 2+O(\log r)$, hence

$$
r=\frac{1-\log_3 2}{\log 2}\log n+O(\log\log n),
\qquad
\frac{1-\log_3 2}{\log 2}=0.5324558\ldots .
$$

This is a construction of finite genuine trajectories. It gives no upper bound on how long distinctness can last for an arbitrary start. [Terras (1976), Theorem 1.2](https://doi.org/10.4064/aa-30-3-241-252)

## What remains open

The examples rule out forcing a return within a fixed number of joins, including by pigeonholing cofactors modulo any fixed set of moduli. They also show that a return is unnecessary before a trajectory enters the cycle through one. The question left by COLLATZ-23 concerns a hypothetical infinite escape. A recurrence theorem that applies to such an orbit at sufficiently large future minima and within the window of COLLATZ-23 would still give a contradiction. These finite constructions do not supply that theorem or an infinite escape.

Direct iteration checked 128 pairs of congruence parameters, 100 balanced word lengths, and six constructions ending at a power of two. The unbounded families follow from the identities above.
