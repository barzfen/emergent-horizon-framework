# COLLATZ-07 · Distinct parity windows can have impossible residues

[COLLATZ-06](../parity-complexity-06/README.md) showed that a nonrepeating rational orbit with polynomially bounded multipliers needs distinct parity windows early. This probe separates that requirement from an arithmetic check on the **sizes** of the residues those windows encode.

**PROVED.** There are uncountably many coefficient-surviving parity words with $P_N=\Theta((N+1)^\beta)$, where $\beta=4\log_2 3$, that pass the early-window test. Nevertheless, for every fixed odd denominator, all their early windows at a suitable logarithmic resolution encode residues too large for the hypothetical rational orbit.

## The family

Start with the upper mechanical boundary word of slope $\alpha=\log_3 2$, as in [COLLATZ-05](../multiplier-band-05/README.md). Its prefix odd count is $\lceil N\alpha\rceil$ and its multiplier is in $[1,3)$. In any length-$d$ window the count of zeros is within one of $\lambda d$, where $\lambda=1-\alpha\in(1/3,1/2)$. Every zero is followed by a one because $\alpha>1/2$, so the `01` pairs beginning at zeros are disjoint. [López and Stoll (2009), §1](https://doi.org/10.1515/INTEG.2009.014)

1. For every $k\ge4$, mark the first four zeros in the length-12 block starting at bit position $2^k$. At least four zeros are available since $12\alpha<8$. The marking blocks are disjoint. Flip each marked zero to a one and leave its partner alone.
2. At each unmarked zero independently keep its pair as `01` or swap it to `10`, with equal probabilities.

The marked flips add $4\log_2(N+1)+O(1)$ ones to the first $N$ bits. The swaps add either zero or one to any prefix count, since the only possible incomplete pair lies at the end. All changes to the prefix count are nonnegative. This proves $P_N\ge1$ and $P_N=\Theta((N+1)^\beta)$ for **every** choice of switches.

## How likely is a particular window or a collision?

For a length-$d$ window, let $u$ be the number of unmarked original zero positions in it. These are the first cells of independent switched pairs. Any length-$d$ interval intersects at most $1+\log_2(d+12)$ marking blocks. Indeed, the powers of two anchoring such blocks lie in an interval of length at most $d+11$, while $r$ distinct nonnegative powers of two span at least $2^{r-1}-1$. Thus

$$
u\ge\lambda d-1-4\bigl(1+\log_2(d+12)\bigr).
$$

Any specified window word has probability at most $2^{-u}$, since it fixes the independent bits at those $u$ first cells. The **same upper bound** applies to equality between this window and a second length-$d$ window starting strictly later, even when the windows overlap. For each selected first cell $t$ in the earlier window, its aligned cell in the later window is at $t+s$, with $s>0$. That later cell is either fixed, controlled by a pair starting strictly after $t$, or is the second cell of the pair at $t$. The last case makes equality impossible because the cells are complementary. Otherwise, condition on the switches outside the selected $u$ switches. In descending order of $t$, the equality at each selected cell determines its switch from constants and switches already determined. At most one of the $2^u$ assignments can give equality.

Both bounds are uniform in window position, and are $O((d+12)^4\,2^{-\lambda d})$.

## First test · Early windows are distinct

Take $N_m=2^m$ and $d_m=6m$. Among windows starting at positions $0,\ldots,N_m-1$, a union bound over pairs gives a collision probability of at most

$$
O\!\left(m^4\,2^{(2-6\lambda)m}\right).
$$

The sum over $m$ converges since $\lambda>1/3$. The probability of any failure beyond a given index is bounded by the corresponding tail of this sum, which tends to zero. Thus with probability one all those windows are distinct for all sufficiently large $m$.

For an arbitrary large prefix of length $N$, take $m=\lceil\log_2 N\rceil$. Distinctness extends to longer windows at the same starts. In particular it holds at the length $(\beta+1)\log_2 N+O(1)$ used in COLLATZ-06, because $\beta+1>6$. This includes every window contained in that prefix at the stated length.

## Second test · The same branches fail the residue-size check

Fix a positive odd denominator $q$. A length-$D$ parity window encodes one residue $r$ modulo $2^D$ for the numerator $p$ of a rational state $p/q$. This is the parity bijection of COLLATZ-05, extending the usual integer coding. Write $R=\min(r,2^D-r)$ for the smallest absolute value of a signed representative. If $R>X$, no integer numerator of absolute value at most $X$ realises the window. [Terras (1976), Theorem 1.2](https://doi.org/10.4064/aa-30-3-241-252) · [Bernstein and Lagarias (1996), §1](https://websites.umich.edu/~lagarias/doc/bernstein.pdf)

For a hypothetical rational lift with starting numerator $p_0$, the height estimate in COLLATZ-05 gives, for $i<N_m$,

$$
|p_i|\le H_{N_m}(|p_0|+q N_m/3)\le K N_m^{\beta+1}
$$

for some positive integer $K$ independent of $m$. Here $H_{N_m}=\max_{i\le N_m}P_i$ since $P_0=1$ and $P_i\ge1$.

Now use $D_m=30m$. For any fixed $q,K$, at most $2K N_m^{\beta+1}+1$ residue classes have $R\le K N_m^{\beta+1}$. Each class corresponds to one specified parity word. The probability of even one such small residue among the first $N_m$ starting positions is therefore at most

$$
O_{K}\!\left(m^4\,2^{(\beta+2-30\lambda)m}\right).
$$

This is summable since $\beta+2<10<30\lambda$. Consequently almost surely **every** window at that resolution among those starts is too large for the bound, for all sufficiently large $m$. The countable intersection over all positive odd $q$ and positive integer $K$ still has probability one. In particular, there is no rational lift.

These length-$D_m$ windows are distinct by the first test, since their length-$d_m$ prefixes are distinct. At that same longer resolution the data therefore pass the distinctness test and fail the size test. There are uncountably many such words because the switches are independent, infinitely many are available, and an individual word specifies every switch and has probability zero.

## Finite illustration

Run `python3 verify.py` from this directory. With the fixed seed in the script, all 1,024 windows are distinct at lengths 60 and 300. At length 300, every signed residue exceeds the height bound for starting numerators of absolute value at most $10^9$, for each of $q=1,3,5$. The script decodes the residues and checks their parity words by iteration. The finite example illustrates the two tests. The infinite conclusion follows from the summable probability bounds.

## Scope

The early-window count alone cannot distinguish this family from the necessary condition for rational lifts. The size check rejects the family using the actual residue values. Its proof concerns a specified distribution of symbolic words. It does not address all coefficient-surviving words, and supplies no distributional assumption about an actual Collatz orbit. The open case includes branches whose early residues do fit the height bound.

[COLLATZ-08](../residue-stabilisation-08/README.md) shows when fitting residues at larger scales force a single rational lift.

We used the cited parity coding and mechanical-word construction. The separation of the two tests is proved above without a priority claim. AI assistance was used for derivation, verification and drafting.
