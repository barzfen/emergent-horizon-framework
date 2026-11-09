# COLLATZ-13 · Joint residue fits at the growth-rate threshold

[COLLATZ-12](../fast-residues-12/README.md) used the size of each decoded residue separately. Here we use consecutive windows together. If every window in a run fits, the overlaps reconstruct one exact orbit segment, and its endpoint bounds how many starting values were possible.

**PROVED.** For the biased symbolic family, the joint test can reject fast branches with a window-length coefficient arbitrarily close above their exponential growth rate $\chi$. It can also reject long **runs** of fitting windows, even when some windows pass individually. A separate deterministic bound shows when full fits at increasing scales force an actual rational lift.

## One fitting run gives one orbit segment

Fix an odd positive denominator $q$ and use the numerator map $T_q$, which sends even $p$ to $p/2$ and odd $p$ to $(3p+q)/2$. A length-$D$ parity window gives one numerator residue modulo $2^D$. At scale $N$, put

$$
D=\lceil\gamma N\rceil,\qquad X=2^{\eta N},\qquad 0<\eta<\gamma .
$$

A window fits if its signed representative has absolute value at most $X$. In a consecutive run of fitting windows, adjacent representatives satisfy $T_q(p_j)\equiv p_{j+1}\pmod{2^{D-1}}$ by their $D-1$ overlapping bits. Since $|T_q(p_j)-p_{j+1}|\le(5X+q)/2$, the congruence is an equality for large $N$. A run of $s$ fitting windows therefore gives an exact orbit for its $s+D-1$ parity bits. This is the finite stitching lemma of [COLLATZ-08](../residue-stabilisation-08/README.md). [Terras (1976), Theorem 1.2](https://doi.org/10.4064/aa-30-3-241-252) · [Bernstein and Lagarias (1996), §4](https://websites.umich.edu/~lagarias/doc/bernstein.pdf)

## Entropy bound for consecutive fits

Use independent symbolic bits with probability $\theta\in(\log_3 2,1)$ for a one, and write

$$
\chi=\theta\log_2 3-1>0,\qquad h=h_2(\theta).
$$

Let $P_j=3^{a_j}/2^j$ be the cumulative multiplier, where $a_j$ counts the ones before position $j$. Fix $0<\tau\le1$ and set $s=\lceil\tau N\rceil$. We show that almost surely there is eventually **no run of $s$ fitting windows starting at any of the first $N$ positions**, provided

$$
h(\tau+\gamma)>\max(0,\eta-\chi\tau).
$$

For any fixed $\epsilon>0$, the strong law gives $|\log_2 P_j-\chi j|\le\epsilon N$ uniformly for $j\le N+s+D$, for all sufficiently large $N$. Call this the good-growth condition. It follows by applying $\log_2 P_j-\chi j=o(j)$ up to a fixed multiple of $N$, and absorbing the finitely many early errors.

Suppose a fitting run starts at $i<N$. Let $Q_{i,j}=P_j/P_i$ be the multiplier along the segment from $i$ to $j$. Applying the normalized affine identity of [COLLATZ-05](../multiplier-band-05/README.md) to its last reconstructed state gives

$$
|p_i|\le \frac{|p_{i+s-1}|}{Q_{i,i+s-1}}
  +\frac{q}{3}\sum_{\substack{i\le j<i+s-1\\w_j=1}}\frac1{Q_{i,j}} .
$$

Under the good-growth condition, $Q_{i,j}\ge2^{\chi(j-i)-2\epsilon N}$, and the last numerator is bounded by $X$. Thus the number of possible integer starting numerators is at most a constant times

$$
(N+1)\,2^{[\max(0,\eta-\chi\tau)+2\epsilon]N}.
$$

For each $i$, each such starting numerator determines one word of length $s+D-1$. On the good-growth condition, that word's odd fraction differs from $\theta$ by $O(\epsilon)$, using the difference of the two cumulative log multipliers at its endpoints. Its Bernoulli probability is therefore at most $2^{-(h-O(\epsilon))(s+D-1)}$. Multiplying by the number of starting numerators and by the $N$ possible positions gives a summable bound if $\epsilon$ is small enough, by the strict inequality above. Good growth itself holds eventually almost surely, so the claim follows. A fixed finite prefix preserves the probability-one conclusion. The survival construction of [COLLATZ-12](../fast-residues-12/README.md) can then impose $P_j\ge1$ at all times with positive probability.

Taking $\tau=1$, for any $\gamma>\chi$ we can choose $\eta>\chi$ sufficiently close to $\chi$ that both inequalities hold. A genuine fixed-denominator orbit with $P_j=2^{\chi j+o(j)}$ would fit all these bounds eventually, by the convergent normalized affine sum. For $\gamma\le\chi$ and $\eta>\chi$, every signed representative already lies below $X$, since its magnitude is at most $2^{D-1}$. Thus $\chi$ is the infimum of useful resolution coefficients for this joint test with an exponential cutoff above the growth rate.

## If full fits keep recurring

There is also a deterministic consequence. Suppose $P_j=2^{\chi j+o(j)}$, with $\chi>0$, and all the first $N$ windows fit at a scale $N$. The decoded starting numerator $p^{(N)}_0$ follows the whole prefix of length $N+D-1$. Since $\sum_j1/P_j$ converges, the same normalized affine identity at the last fitted state gives

$$
|p^{(N)}_0|\le 2^{(\eta-\chi+o(1))N}+O(1)
$$

for fixed $q$. If a later full fit $N'>N$ gives a different starting numerator, the two starts differ by a nonzero multiple of $2^{N+D-1}$. It follows that along changes at unbounded scales,

$$
\liminf \frac{N'}{N}\ge\frac{1+\gamma}{\eta-\chi},
\qquad \chi<\eta<\gamma .
$$

Indeed, for any $\delta>0$ the difference is at most a fixed constant times $2^{(\eta-\chi+\delta)N'}$ at large scales. Comparing with $2^{N+D-1}$ gives the inequality after letting $\delta$ tend to zero. If infinitely many full-fit scales have successive ratios eventually bounded strictly below this threshold, the seed stabilises and realises the entire word. For $q=1$, a stabilised seed greater than one on a coefficient-surviving branch would be an actual Collatz counterexample. This leaves the existence of such a branch open.

## Finite illustration and scope

At $\theta=3/4$, take $\gamma=1/5$, $\eta=39/200$, and $\tau=1/25$. These meet the strict conditions, so eventually there is no fitting run as long as four percent of the scale in the biased symbolic family. The deterministic seed-change factor for full fits is $191.139887\ldots$.

Run `python3 verify.py` in this directory. At $N=1600$, with 320-bit windows and cutoff $2^{312}$, the symbolic example has 9 individually fitting windows for $q=1$, with longest run 2. The $q=3,5$ cases also have individual fits and only short runs. A positive integer control and a signed rational control stitch exactly. These examples illustrate the finite tests. The asymptotic exclusion comes from the summable bounds.

The probability argument concerns the specified symbolic construction. It makes no randomness assumption about genuine Collatz trajectories. We make no priority claim. AI assistance was used for derivation, arithmetic checks and drafting.
