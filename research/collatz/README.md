# Collatz working note

9 November 2026 · Emergent Horizon Framework (EHF)

A mathematical case study in what an admissible-move graph preserves about the original integers. The first worked example tests whether a Hamiltonian cycle in a finite parity graph can be followed by a positive integer indefinitely.

## Starting point

On the positive integers, the ordinary Collatz map $C$ sends an odd $n$ to $3n+1$ and an even $n$ to $n/2$. Every step stays a positive integer. The conjecture says every starting value eventually reaches $1$, after which the ordinary rule repeats $1\to4\to2\to1$. The general conjecture remains open. [Lagarias (2010), *The 3x+1 Problem: An Overview*](https://arxiv.org/abs/2111.02635) · [Barina, 2025](https://doi.org/10.1007/s11227-025-07337-0)

The shortcut map $T$ uses $(3n+1)/2$ at odd $n$, folding in the first compulsory halving, and uses $n/2$ at even $n$. Its cycle through $1$ is $1\to2\to1$. Reaching $1$ is equivalent for the two maps.

## PROVED · What follows from the rule

| Starting observation | Precise statement |
|---|---|
| All numbers stay positive integers. | Both branches preserve the positive integers. The even branch divides by two only when the input is divisible by two. |
| Mersenne primes push the numbers up. | The whole family $2^k-1$ starts with exactly $k$ increasing shortcut steps for $k\ge1$. The binary string of $k$ ones drives this behaviour. For example, composite $15$ goes $15\to23\to35\to53\to80$ under $T$. |
| Powers of two bring the numbers down. | Every even step decreases the value. If a trajectory reaches $2^k$, it reaches $1$ in exactly $k$ halvings. In any value $2^a m$ with $m$ odd, the $a$ trailing binary zeros give exactly $a$ halvings to reach $m$. |
| The numbers can be expressed in binary. | Halving an even number drops one trailing zero. The shortcut map also gives a second binary object, the sequence of odd/even decisions along the trajectory. The binary digits of the starting number and its sequence of parity decisions are distinct encodings. |

For the Mersenne calculation, an odd shortcut step gives $T(n)+1=3(n+1)/2$. Starting at $n=2^k-1$, after $j$ steps the value is $3^j2^{k-j}-1$ for $0\le j\le k$. Each of the first $k$ inputs is odd, so its shortcut step increases the value. The $k$-th output is $3^k-1$, which is even and halves on the next step. Since $k$ can be arbitrarily large, there can be no fixed number of steps by which **every** starting value greater than $1$ has dropped below itself.

## What others have established

- **Binary parity coding (proved).** For the shortcut map, the first $r$ parity decisions specify exactly one residue class modulo $2^r$, and every word of $r$ parity bits occurs. On the 2-adic integers, this coding turns the shortcut dynamics into a binary shift. The remaining question for Collatz is what the shift does to the encodings of **positive integer** starts. [Bernstein and Lagarias (1996), *The 3x+1 Conjugacy Map*](https://websites.umich.edu/~lagarias/doc/bernstein.pdf)
- **Almost all starts reach small values (proved).** Tao proved that for any function $f(n)$ tending to infinity, however slowly, the orbit starting at $n$ reaches a value at most $f(n)$ for almost all $n$ in logarithmic density. The theorem allows exceptional starts and does not guarantee a visit to $1$. [Tao (2022), *Almost all orbits of the Collatz map attain almost bounded values*](https://arxiv.org/abs/1909.03562)
- **A large finite range has been checked (computational).** Barina’s published 2025 result verified convergence for every positive start below $2^{71}$. This is finite computational verification. [Barina (2025), *Improved verification limit for the convergence of the Collatz conjecture*](https://doi.org/10.1007/s11227-025-07337-0)

## Can the parts cover infinitely many starts?

One precise reading of Barz’s question is to divide the positive integers into families, prove eventual descent within each family, and prove that the families cover every start greater than $1$. This would be a valid proof by cases and strong induction. Once an orbit from $n$ drops below $n$, the smaller value has already been handled by the induction. In the other direction, convergence would give eventual descent for every $n>1$.

For example, even starts halve immediately. If $n>1$ is $1\bmod4$, then $T^2(n)=(3n+1)/4<n$, so that whole family descends in two shortcut steps. These two cases leave the starts $3\bmod4$. Subdividing by further parity bits is a way to describe more families. The proof obligation is to show that each positive starting integer eventually belongs to a family with a certified descent. The required time may depend on the start, as the Mersenne calculation shows. A density approaching $100\%$ can still leave individual starts outside the covered families.

## COLLATZ-01 · A Hamiltonian cycle in the two-bit parity graph

**PROVED.** Positive integers can follow the displayed Hamiltonian cycle for any prescribed finite number of laps. Each additional lap requires a more restrictive starting residue class, and no positive integer can follow the cycle indefinitely. A rotated four-step parity block certifies descent for a whole family of odd starts.

### The graph

In the ordinary directed Collatz graph, each vertex is a positive integer and has one forced outgoing edge. The edges from $1$, $4$ and $2$ already close a directed cycle. Other trajectories can merge into it, as $8\to4$ shows. For a Hamiltonian construction we instead use a finite graph of parity words.

Record the parity of the current value and its successor under the shortcut map $T$, with $0$ for even and $1$ for odd. A step drops the first bit and appends the next one. Laarhoven and de Weger proved that the modular Collatz graph modulo $2^k$ is isomorphic to the order-$k$ binary de Bruijn graph via this coding. For $k=2$, a directed Hamiltonian cycle is

$$
00\longrightarrow01\longrightarrow11\longrightarrow10\longrightarrow00.
$$

Each move uses the first bit of its source vertex. The four moves therefore use $0011$. To end at vertex $00$, the next two parities must also be $00$. [Laarhoven and de Weger (2013), *The Collatz conjecture and De Bruijn graphs*, Theorem 2.1 and §4](https://doi.org/10.1016/j.indag.2013.03.003)

### Arbitrarily many finite laps, with a different starting class each time

A start has first four parities $0011$ exactly when $n\equiv12\pmod{16}$. Indeed, after the first two halvings, $n/4$ and its successor must both be odd, which requires $n/4\equiv3\pmod4$. The four moves give

$$
F(n)=T^4(n)=\frac{9n+20}{16},\qquad 7F(n)-20=\frac{9}{16}(7n-20).
$$

The one-block condition is equivalently $16\mid(7n-20)$. Since $9$ is coprime to $16$, the factor of $9$ leaves divisibility by powers of two unchanged and the division by $16$ accounts for one block. Induction using the displayed identity gives the first line below. To obtain the second line, the value $F^m(n)$ after $m$ blocks must also be $0\bmod4$, which is equivalent to $4\mid(7F^m(n)-20)$.

| What the trajectory does | Exact condition on its starting value |
|---|---|
| Follows the $0011$ block $m$ times | $7n\equiv20\pmod{16^m}$ |
| Completes $m$ graph laps starting and ending at $00$ | $7n\equiv20\pmod{4\cdot16^m}$ |

For every $m\ge1$, the second condition has a unique residue class because $7$ is invertible modulo powers of two. Each class contains infinitely many positive starts. For instance, $12$ completes one lap and arrives at $8$. The start $588$ completes two laps and has lap endpoints $332$ and $188$, both divisible by $4$.

A single integer making infinitely many laps would require $7n-20$ to be divisible by arbitrarily large powers of two. This forces $7n-20=0$, whose solution $n=20/7$ lies outside the integers. This is an explicit instance of the distinction between finite modular paths and cycles in the extended 2-adic graph discussed by Laarhoven and de Weger.

### A descent certificate for an odd family

Start reading the same cycle at vertex $11$. Its first four moves now use $1100$. The first four parities are $1100$ exactly for $n\equiv3\pmod{16}$. To see this, compose the two odd branches to get $(9n+5)/4$, then require the next two inputs to be even, which gives $16\mid(9n+5)$. Conversely, $n\equiv3\pmod{16}$ makes both initial inputs odd and the next two even.

Every positive start in this class satisfies

$$
T^4(n)=\frac{9n+5}{16}<n,
$$

since $n\ge3$. The inequality needs only those four parities, so it applies even when the next vertex differs from $11$. For example, $3\to5\to8\to4\to2$ already descends below its start. The class $3\bmod16$ is disjoint from the immediate even descent and the two-step $1\bmod4$ descent in the working note above.

## Open question · How far does parity-guided descent reach?

[COLLATZ-02 · Exact census of first-descent families](../../probes/collatz/parity-descent-02/README.md) checks all residue classes through 30 shortcut steps and distinguishes the exact descent test from coefficient-only counting.

[COLLATZ-03 · Which surviving branches lift to positive integers?](../../probes/collatz/survivor-branches-03/README.md) excludes eventually periodic coefficient survivors from the positive integers and separates the exact tree's offset case.

[COLLATZ-04 · Bounding offset exceptions](../../probes/collatz/offset-bound-04/README.md) uses Terras's minimax bound and an exact residue sieve to rule out offset exceptions through 200,000 shortcut steps.

[COLLATZ-05 · A multiplier band excludes rational lifts](../../probes/collatz/multiplier-band-05/README.md) rules out bounded-multiplier rational lifts and gives a polynomial lower bound on the multiplier range of a hypothetical positive coefficient survivor.

[COLLATZ-06 · How many parity blocks must appear early?](../../probes/collatz/parity-complexity-06/README.md) gives an early-window test for polynomial-growth branches and constructs an irrational survivor containing every finite binary word.

[COLLATZ-07 · Distinct parity windows can have impossible residues](../../probes/collatz/residue-size-07/README.md) separates the early-window count from a residue-size check on a family of polynomial-growth branches.

[COLLATZ-08 · When fitting residues force an actual orbit](../../probes/collatz/residue-stabilisation-08/README.md) proves finite reconstruction and gives a sharp lower-density threshold for the starting-window test.

[COLLATZ-09 · How slowly can a regular multiplier grow?](../../probes/collatz/regular-growth-09/README.md) excludes two-sided polynomial multiplier exponents up through $1/h_2(\log_3 2)$ and refines the height used in the residue test.

[COLLATZ-10 · A growth floor for nonrepeating orbits](../../probes/collatz/orbit-height-10/README.md) uses averaged parity counts to give a superlinear lower bound on running orbit height without a power-band assumption.

[COLLATZ-11 · A repetition bound for fast parity branches](../../probes/collatz/repetition-budget-11/README.md) gives exact finite repeat limits and excludes an exponential-growth family with all binary factors.

[COLLATZ-12 · Fast branches with short repeats and oversized residues](../../probes/collatz/fast-residues-12/README.md) separates the repetition test from arithmetic height fitting for exponential-growth branches.

[COLLATZ-13 · Joint residue fits at the growth-rate threshold](../../probes/collatz/joint-window-13/README.md) uses overlap to reject consecutive fits at shorter resolutions and bounds how far apart full fits must be to change seed.

[COLLATZ-14 · A backward test for positive starting values](../../probes/collatz/backward-terminal-14/README.md) reconstructs the least terminal state from the prefix and gives an exact monotone test for a fixed height budget.

[COLLATZ-15 · Every escaping orbit has a coefficient-surviving tail](../../probes/collatz/escape-tail-15/README.md) uses orbit sparsity to show that the fixed-budget survivor search captures the entire divergence case.

[COLLATZ-16 · A sharp count of multiplier survivors](../../probes/collatz/survival-count-16/README.md) bounds the fraction of surviving residue classes and isolates the least positive representative as the remaining universal question.

[COLLATZ-17 · Smaller starts and the limits of short merges](../../probes/collatz/smaller-merge-17/README.md) excludes a progression from being the least survivor and proves a divisibility bound that defeats any fixed two-depth merge search.

[COLLATZ-18 · Choosing a meeting point after the odd run](../../probes/collatz/adaptive-merge-18/README.md) transfers finite survival between different clocks and gives two residue rules that bypass the initial odd run.

[COLLATZ-19 · Coverage of the half-source merge](../../probes/collatz/merge-coverage-19/README.md) counts the exact cofactor and all-start coverage and brackets what the fixed comparison can ever certify.

[COLLATZ-20 · Starting-height bounds from expanding pieces](../../probes/collatz/expanding-pieces-20/README.md) gives an explicit lower bound on the least positive start for surviving prefixes with few expanding periodic pieces.

Can we organise parity prefixes so that each contributes a certified family of starts, then describe exactly which starts remain after each stage? A certificate needs both the residue class that realises the prefix and its affine endpoint map $n\mapsto(an+b)/2^r$. The first gives the domain and the second lets us compare the endpoint with the starting value. Eventual coverage of **every** start greater than $1$ would prove the conjecture by strong induction. An increasing family of starts or arbitrarily long rising prefixes across different starts leaves open whether a single orbit can escape to infinity.

The graph isomorphism and 2-adic setting come from the cited literature. For COLLATZ-01 we inspected the published de Bruijn paper's sections on the graph isomorphism and cycles, and the introduction of the Bernstein–Lagarias paper. The exact residue conditions and descent example above are worked calculations for this note, with no priority claim. Barz (`barzfen`) posed the Hamiltonian and proof-by-parts questions. AI assistance was used to consult the references, derive and check the example, and draft the note.
