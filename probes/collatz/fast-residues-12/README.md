# COLLATZ-12 · Fast branches with short repeats and oversized residues

[COLLATZ-11](../repetition-budget-11/README.md) excluded an exponentially growing family because it had long repeats early. Here we construct a different fast family. Its early repeats are short enough to satisfy that test, but its decoded residues are too large for an ordinary rational orbit.

**PROVED.** Fix an odd-step frequency $\theta\in(\log_3 2,1)$ and let

$$
\chi=\theta\log_2 3-1,\qquad
h=h_2(\theta)=-\theta\log_2\theta-(1-\theta)\log_2(1-\theta).
$$

For any fixed $\gamma>\chi/h$ and $\chi<\eta<\gamma h$, every finite coefficient-surviving prefix has uncountably many extensions with all the following properties.

- The word survives at every prefix and $P_N=2^{\chi N+o(N)}$.
- It contains every finite binary word, and two windows with later start $j$ can agree for at most $O(\log(j+2))$ bits.
- For every fixed odd denominator $q>0$, all windows of length $\lceil\gamma N\rceil$ starting at positions $0,\ldots,N-1$ have smallest absolute numerator representative greater than $2^{\eta N}$, for all sufficiently large $N$.

In particular, these words have irrational 2-adic lifts. At $\theta=3/4$, one can take $\gamma=1/4$ and $\eta=1/5$.

## Product measure and survival

First use independent bits with probability $\theta$ for a one. Let $a_N$ be the odd count and $P_N=3^{a_N}/2^N$. The strong law gives $\log_2 P_N=\chi N+o(N)$ almost surely. Every finite binary word occurs almost surely, by testing disjoint blocks of its length and taking a countable intersection over target words.

These probability-one statements and the bounds below remain true if we fix any finite prefix, since that conditioning event has positive probability. To extend a given surviving prefix, append a fixed run of ones and then sample an independent tail. The tail's log multiplier has positive drift, so its infimum is finite almost surely. For some finite $C$, the event that the tail's log multiplier stays at least $-C$ has positive probability. A long enough appended run of ones supplies that buffer. Intersecting this survival event with the probability-one properties gives a positive-measure family of surviving words. The product measure has no atoms, and distinct words have distinct lifts by the classical parity coding. Thus the family is uncountable. [Bernstein and Lagarias (1996), §1](https://websites.umich.edu/~lagarias/doc/bernstein.pdf)

## Short matches satisfy the repetition bound

For two windows of length $d$ at $i<j$, expose the bits at $j,j+1,\ldots,j+d-1$ in order. Each bit in the later window must equal a previously exposed bit in the earlier window. Even when the windows overlap, the conditional probability of each required equality is at most $\theta$, since $\theta>1/2$. So the match probability is at most $\theta^d$.

For $N=2^m$, take $d=\lceil C_1m\rceil$, with $C_1>2/\log_2(1/\theta)$. A union bound over the first $N$ starting positions gives a summable bound $N^2\theta^d$. Thus almost surely all matches among those starts have length less than $d$ for all sufficiently large $m$. Choosing the first dyadic $N>j$ gives the claimed logarithmic bound in $j$.

In particular, if $r$ consecutive copies of a block of length $d$ occur, the first and second copies begin a match of length $(r-1)d$. With $j$ the start of the second copy, this is $O(\log(j+2))$. That is compatible with the linear upper bounds in COLLATZ-11, including the version for a specified $\chi>0$, with a fixed additive constant to cover finitely many early matches.

## Entropy and the residue-size test

For fixed $q$, use the fixed-denominator numerator map from [COLLATZ-05](../multiplier-band-05/README.md). A parity word of length $D$ fixes exactly one numerator residue modulo $2^D$. This is the same coding as for integers, with numerator residues scaled by $q$. [Terras (1976), Theorem 1.2](https://doi.org/10.4064/aa-30-3-241-252) · [Bernstein and Lagarias (1996), §4](https://websites.umich.edu/~lagarias/doc/bernstein.pdf)

A typical word of length $D$ with odd fraction close to $\theta$ has probability at most $2^{-(h-\delta)D}$, for any chosen $\delta>0$ if the allowed frequency interval is narrow enough. This follows from the probability $\theta^a(1-\theta)^{D-a}$ of a word with $a$ ones. The probability of falling outside that frequency interval is $O(e^{-cD})$ by a binomial Chernoff bound.

Take $D=\lceil\gamma N\rceil$. At most $2\lfloor2^{\eta N}\rfloor+1$ residues have a signed representative of absolute value at most $2^{\eta N}$. By the bijection, they account for at most that many words. Therefore the probability of such a residue in any of the first $N$ windows is bounded by

$$
O\!\left(N e^{-cD}+N 2^{\eta N-(h-\delta)D}\right).
$$

Choose $\delta$ so that $\gamma(h-\delta)>\eta$. The probabilities are summable over integer $N$, so almost surely there are no such small residues at any of these positions for all sufficiently large $N$. Take a countable intersection over the odd positive denominators $q$. As before, fixing any finite prefix preserves this probability-one conclusion.

If a branch had a rational lift $p_0/q$, the affine identity would give $|p_i|\le C_2 P_i$, because $P_i=2^{\chi i+o(i)}$ makes $\sum_i1/P_i$ finite. Since $\eta>\chi$, the first $N$ actual numerators would all have magnitude at most $2^{\eta N}$ for sufficiently large $N$. They would realise the corresponding parity windows, contradicting the residue-size conclusion.

For the example $\theta=3/4$, $\chi=0.1887218755\ldots$ and $h/4=0.2028195311\ldots$, so $1/5$ lies strictly between them.

## Finite illustration and scope

Run `python3 verify.py` in this directory. The seeded prefix survives throughout the checked range. Among its 1,280 windows of length 320, the longest match is 24 bits. For $q=1,3,5$, all signed residue magnitudes exceed $2^{256}$. The smallest signed magnitude for $q=1$ has 309 bits. This is an illustration at one scale. The infinite conclusion uses the summable bounds.

The distribution is a construction on symbolic words. Its probability bounds do not assume that parity bits along a genuine Collatz orbit are independent. The result excludes a class of fast branches that satisfies the repetition test, while leaving open fast branches whose decoded residues also fit the arithmetic height bound. [COLLATZ-13](../joint-window-13/README.md) applies the residue bound jointly across overlapping windows. The proof uses the cited coding and makes no priority claim. AI assistance was used for derivation, checks and drafting.
