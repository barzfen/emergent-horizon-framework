# COLLATZ-05 · A multiplier band excludes rational lifts

[COLLATZ-03](../survivor-branches-03/README.md) excluded eventually periodic words from the positive-integer part of the coefficient survivor tree. Here we exclude a family of **aperiodic** words by counting the residue classes that their successive orbit values would have to occupy.

**PROVED.** A parity word whose cumulative multipliers stay between two fixed positive bounds has an irrational 2-adic lift. More quantitatively, if a rational lift has a nonrepeating orbit, its multiplier range through step $N$ grows at least as a constant times $N^{0.033343791\ldots}$. In particular, a hypothetical positive integer whose multiplier never contracts must have running multiplier maxima of at least this order.

## Setup

Let $P_i=3^{a_i}/2^i$, where $a_i$ is the number of odd steps in the first $i$ moves of the shortcut map and $P_0=1$. Write a rational 2-adic start as $p_0/q$ with $p_0$ an integer and $q>0$ odd. Use a fixed denominator throughout the orbit, so the iterates are $p_i/q$. Their numerators obey

$$
p_{i+1}=
\begin{cases}
p_i/2 & p_i\text{ even},\\
(3p_i+q)/2 & p_i\text{ odd}.
\end{cases}
$$

The numerator has the same parity as the rational value in the 2-adic sense. The length-$d$ parity words again biject with residues modulo $2^d$. In fact, two lifts of a residue from modulus $2^j$ to $2^{j+1}$ give endpoints differing by $3^{a_j}$, which is odd, so the two lifts have opposite next parities. For $q=1$ this is Terras's classical parity coding. [Terras (1976), Theorem 1.2](https://doi.org/10.4064/aa-30-3-241-252)

## Count the orbit's local windows

Let

$$
H_N=\frac{\max_{0\le i\le N}P_i}{\min_{0\le i\le N}P_i}.
$$

At an odd step, $p_{i+1}/P_{i+1}-p_i/P_i=q/(3P_i)$. At an even step the difference is zero. Since $P_i/P_j\le H_N$ and $P_i\le H_N$ for $i,j\le N$, summing gives

$$
|p_i|\le X_N:=H_N\left(|p_0|+\frac{qN}{3}\right)\qquad (0\le i\le N).
$$

For any window length $1\le d\le N$, each of the first $N-d+1$ numerator values starts a $d$-step window with multiplier $P_{i+d}/P_i\ge1/H_N$. Count the starting residues compatible with this condition. For a length-$d$ word with $a$ odds, let $L=3^a/2^d$ be its window multiplier. The average of $\sqrt L$ over the $2^d$ residue classes is exactly

$$
\rho^d,\qquad \rho=\frac{1+\sqrt3}{2\sqrt2}<1,
$$

by the binomial formula. Every class with $L\ge1/H_N$ contributes at least $1/\sqrt{H_N}$ to this average per class. So the fraction of qualifying classes is at most $\sqrt{H_N}\rho^d$. This counts residues in a complete modulus window. It makes no assumption about independence of consecutive parities along an individual orbit.

Each class contributes at most $2X_N/2^d+1$ integers to $[-X_N,X_N]$. If the orbit values in question are distinct, their number therefore satisfies

$$
N-d+1\le \sqrt{H_N}\rho^d(2X_N+2^d).
$$

Choose $d=\lfloor\log_2 N\rfloor$ for $N\ge\max(2,3|p_0|/q)$. Then $N-d+1\ge N/2$, $2^d\le N$, and $2X_N+2^d\le 3qH_NN$. Rearranging gives

$$
H_N\ge (6q)^{-2/3}\rho^{-2d/3}
\ge \left(\frac{\rho}{6q}\right)^{2/3}N^\delta,\qquad
\delta=\frac23\log_2(1/\rho)=0.033343791\ldots.
$$

The bound applies to every $N$ above the stated threshold when the orbit has no repeats.

If a rational orbit repeats, determinism gives a periodic tail. A period of length $l\ge1$ with $a$ odd steps multiplies $P_i$ by $3^a/2^l\ne1$ each time around. Its multiplier range therefore grows at least exponentially for that fixed orbit. Together with the nonrepeating case, this proves that a bounded positive multiplier band excludes rational lifts. For a coefficient survivor $P_i\ge1$, the minimum is $P_0=1$, so $H_N$ is just the running maximum of the multiplier.

## Apply the bound to the boundary word

The boundary word used in [COLLATZ-04](../offset-bound-04/README.md) has $a_i=\lceil i\log_3 2\rceil$, so $1\le P_i<3$ for every $i$. Its 2-adic lift is therefore irrational. The first 24 bits are `110110110101101101011011`. The boundary construction is Terras's minimax word and is an upper mechanical word in the terminology of López and Stoll. [Terras (1976), Theorem 2.4](https://doi.org/10.4064/aa-30-3-241-252) · [López and Stoll (2009), §§1 and 3](https://doi.org/10.1515/INTEG.2009.014)

This also yields uncountably many irrational coefficient survivors with $1\le P_i<9$. The boundary word has infinitely many occurrences of `01`, because its limiting odd fraction lies strictly between zero and one. These occurrences are disjoint. Independently keep or swap each pair `01` to `10`. A swap adds one to the odd count at its intermediate prefix and leaves the count unchanged after the pair. Consequently the modified word stays in the stated band. Different choices give different words and distinct irrational lifts by the parity coding.

## Scope

For a positive integer coefficient survivor, the proof requires polynomial growth of the running multiplier maximum. It leaves open whether a branch with such growth has a positive integer lift. The offset case is separate and retains the finite horizon of COLLATZ-04.

[COLLATZ-06](../parity-complexity-06/README.md) tests polynomial-growth branches by how many distinct parity windows appear early.

The proof uses the cited parity coding and boundary construction. We inspected the relevant parts of Terras and López and Stoll. The multiplier-range argument and its applications are given here as a self-contained derivation, with no priority or sharpness claim. AI assistance was used for derivation, arithmetic checks and drafting.
