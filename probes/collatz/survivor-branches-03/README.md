# COLLATZ-03 · Which surviving branches lift to positive integers?

This follows the [first-descent census](../parity-descent-02/README.md). The census follows parity prefixes under the shortcut map $T(n)=n/2$ for even $n$ and $T(n)=(3n+1)/2$ for odd $n$. Here $0$ denotes an even input and $1$ an odd input.

**PROVED.** Every eventually periodic parity branch whose multiplier stays at least one has a negative rational lift. Also, neither multiplier survival nor exact no-descent survival can be recognised by a finite graph reading one parity bit per edge. These statements follow from the algebra below, independently of a search cutoff.

## Two ways for a prefix to survive

For a parity word $w$ of length $d$, let its affine map be

$$
F_w(x)=\frac{Ax+B}{M},\qquad A=3^{\#\text{ odd steps}},\quad M=2^d,\quad B\ge0.
$$

The word specifies a single starting residue modulo $M$. Call a prefix a **coefficient survivor** if $A\ge M$ at every stage, so every positive integer in the final residue class stays at or above its own start through that prefix. Call a prefix an **exact survivor** if *some* integer $n>1$ follows it and stays at or above $n$ through the prefix. The second condition allows the offset $B$ to compensate for a contracting coefficient.

Along an infinite word, the least nonnegative starting residues $r_d$ are compatible. The next one is either $r_d$ or $r_d+2^d$. There is a single 2-adic lift, and it is an ordinary nonnegative integer exactly when the $r_d$ are bounded, since then they stabilise. The parity coding is the classical one used by Terras and by Bernstein and Lagarias. [Terras (1976), Theorem 1.2](https://doi.org/10.4064/aa-30-3-241-252) · [Bernstein and Lagarias (1996), §1](https://websites.umich.edu/~lagarias/doc/bernstein.pdf)

## Repeating tails force a negative lift for coefficient survivors

Suppose an infinite coefficient survivor has a finite prelude $u$ followed by repetitions of a nonempty block $v$. Write $A_v,B_v,M_v$ for the coefficients of its block map. After $m$ complete repetitions the multiplier is

$$
\frac{A_u}{M_u}\left(\frac{A_v}{M_v}\right)^m.
$$

Survival for all $m$ requires $A_v/M_v\ge1$. Equality is impossible for a nonempty period, because a power of three cannot equal $2^{|v|}$. Thus $A_v>M_v$, and $v$ contains at least one odd step, giving $B_v>0$.

The repeating tail has the same parity itinerary after one period. Uniqueness of the lift gives its fixed point $y=F_v(y)$, so

$$
y=\frac{B_v}{M_v-A_v}<0.
$$

This rational has odd denominator. Undoing the prelude gives the starting lift $x=(M_u y-B_u)/A_u<0$, also a rational with odd denominator. The inequalities here are the ordinary order on rationals. The parity coding and the relation between rational cycles and periodic words are classical. The sign conclusion here follows by adding the coefficient survival condition. [Laarhoven and de Weger (2013), §4](https://doi.org/10.1016/j.indag.2013.03.003)

| Parity itinerary | Unique lift | Coefficient survivor? |
|---|---:|---|
| $1111\ldots$ | $-1$ | Yes |
| $(110)^\infty$ | $-5$ | Yes |
| $111(011)^\infty$ | $-11/3$ | Yes |
| $(0011)^\infty$ | $20/7$ | No |

For the third row, the tail cycles as $-10\to-5\to-7\to-10$. The prelude $111$ sends $-11/3$ to $-10$. Its multiplier is $27/8$, so the first even step of the tail leaves it at $27/16>1$. Each later tail lap multiplies the accumulated coefficient by $9/8$.

A positive integer on an infinite coefficient-surviving branch would therefore have an aperiodic parity itinerary. Its orbit would have no repeated value and would tend to infinity, because only finitely many distinct positive integers lie below any fixed bound.

The distinction persists arbitrarily far down the tree. Every finite coefficient-surviving prefix can be followed by all ones, giving a negative rational lift. It can also be followed by any concatenation of the equal-length blocks $1111$ and $1110$, since all partial multipliers in both blocks are at least one. This gives uncountably many surviving extensions, of which only countably many are eventually periodic. Finite-prefix survival alone does not force eventual repetition.

## The exact tree retains an offset case

Consider a branch in the exact survivor tree with a contracting prefix. At that prefix, exact survival requires

$$
n\le \left\lfloor\frac{B}{M-A}\right\rfloor .
$$

There are finitely many such $n>1$. The nonempty candidate sets at longer prefixes are nested subsets of this finite set, so they share an integer. Uniqueness of the lift makes that integer the sole candidate for the infinite branch. In particular, **every infinite exact-surviving branch that ever contracts has a positive integer lift $n>1$ whose orbit never falls below $n$**.

This gives the two separate obligations for a first-descent proof of Collatz.

1. Exclude positive integers $n>1$ from the infinite coefficient survivors. The argument above excludes all eventually periodic branches here.
2. Exclude infinite exact-surviving branches that contract at some finite prefix. A nontrivial positive cycle, if one exists, would give such a branch by starting at its smallest element. Over one period $n=(An+B)/M$ with $B>0$, which gives $A<M$.

The depth-30 census found no offset exceptions at the first contraction within that horizon. The two obligations distinguish that bounded check from a global statement. Every counterexample to Collatz has a smallest value $n>1$ in its forward orbit, and starting at that value gives an infinite exact survivor. [Lagarias (1985), coefficient stopping time discussion](https://www.cecm.sfu.ca/organics/papers/lagarias/paper/html/node5.html)

## No finite graph reads all survivor prefixes exactly

For $k\ge1$, let $b_k$ be the largest integer $j\ge0$ such that $3^k\ge2^{k+j}$. The word $1^k0^j$ is a coefficient survivor exactly for $j\le b_k$. It follows $k$ odd steps by $j$ halvings, so its multiplier first rises and then decreases.

The exact tree could in principle admit one more zero because of the offset. However, for $j=b_k+2$ the multiplier $c=3^k/2^{k+j}$ is strictly below $1/2$. On this word's starting class the endpoint is $c(n+1)-2^{-j}<n$ for every $n>1$. Thus this word is rejected in both trees.

The numbers $b_k$ grow without bound. Choose an infinite sequence of $k$'s with successive $b_k$'s differing by at least two. For any two selected $k<\ell$, the suffix $0^{b_k+2}$ is rejected after $1^k$ in both trees and accepted after $1^\ell$ in both trees. Any deterministic finite reader would therefore need distinct states after infinitely many prefixes. A finite labelled graph, even with multiple possible edges of the same label, can be made deterministic by tracking subsets of its finite vertex set. So neither prefix language is regular. A finite parity graph can still organise local moves, as in [COLLATZ-01](../../../research/collatz/README.md). Exact recognition of survival requires additional state, such as the unbounded arithmetic quantities used in the census.

The proofs use the established parity coding and cycle formula. We inspected the cited sections of Bernstein and Lagarias, Laarhoven and de Weger, and Lagarias's coefficient stopping time discussion. As a separate arithmetic check we enumerated all 4,094 binary period words of lengths 1–11 and verified their fixed lifts, signs and parities. The analytic results do not depend on this enumeration. AI assistance was used for source review, derivation, checking and drafting. No priority claim is made.
