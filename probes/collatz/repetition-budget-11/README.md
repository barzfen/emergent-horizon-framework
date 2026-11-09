# COLLATZ-11 · A repetition bound for fast parity branches

[COLLATZ-10](../orbit-height-10/README.md) gave a growth floor for any nonrepeating rational orbit. Here we look at branches whose multipliers grow exponentially. A long repeated block near the beginning can still exclude a rational lift.

**PROVED.** Every finite coefficient-surviving prefix has uncountably many aperiodic extensions whose odd frequency tends to $3/4$, whose multiplier grows exponentially, and whose parity word contains every finite binary word. All of these extensions have irrational 2-adic lifts. The obstruction is the timing of long repeated blocks.

## Exact finite repetition rule

Use the shortcut map in fixed-denominator coordinates $x=p/q$, with $q>0$ odd. For a nonempty parity block $v$ of length $d$, its affine map on numerators is

$$
F(p)=\frac{Ap+B}{M},\qquad A=3^{\#1(v)},\qquad M=2^d.
$$

Here $B$ includes the numerator offset $q$ on odd steps. Put $\Delta=(A-M)p+B$. The identity

$$
(A-M)F^r(p)+B=\frac{A^r}{M^r}\Delta
$$

shows that $r$ copies of $v$ require $M^r\mid\Delta$, because $F^r(p)$ is an integer and $A$ is odd. This condition is also sufficient. Since $A-M$ is odd, it specifies one residue modulo $M^r$. The parity bijection for the word $v^r$ already gives one such residue, so they coincide. [Terras (1976), Theorem 1.2](https://doi.org/10.4064/aa-30-3-241-252) · [Bernstein and Lagarias (1996), §4](https://websites.umich.edu/~lagarias/doc/bernstein.pdf)

The maximum number of complete copies is therefore $\lfloor \nu_2(\Delta)/d\rfloor$ when $\Delta\ne0$. If $\Delta=0$, the numerator is the fixed point of the block and follows it forever. [COLLATZ-01](../../../research/collatz/README.md) used a special case for the four-bit Hamiltonian example. Related repetition budgets have also been written down in odd-to-odd coordinates, which require the final state to be odd. [Exact repetition in the odd-to-odd map](https://github.com/Sodelin/Collatz-Conjecture-Work/blob/main/research/blind-2026-09-05/SymbolicNotes.md) · [Periodic-dictionary bounds](https://rstation.ai/problems/collatz/papers/15)

## A long repeat must start late enough

Suppose $v^r$ starts at position $i$ of a nonrepeating rational orbit. At the first boundary, $\Delta=M(p_{i+d}-p_i)$. Since $p_{i+d}\ne p_i$,

$$
2^{(r-1)d}\le |p_{i+d}-p_i|.
$$

In the fixed-denominator map, $|p_j|+q\le(3/2)^j(|p_0|+q)$ by the one-step inequality. Hence

$$
(r-1)d\le(i+d)\log_2(3/2)+\log_2\!\bigl(2(|p_0|+q)\bigr).
$$

For a square ($r=2$) this forces $i/d\ge 0.7095112914\ldots-O(1/d)$. In particular, squares with unbounded half-length and a fixed starting position are impossible on such an orbit. This is the familiar comparison between parity separation and orbit height, applied at the repeat boundary. [Dubickas (2009), Theorem 5 and §5](https://doi.org/10.1017/S0017089508004655) · [Related repetition and height discussion](https://rstation.ai/r/collatz/posts/6)

If the odd frequency tends to $\theta>\log_3 2$, write $\chi=\theta\log_2 3-1>0$. Then $P_j=2^{\chi j+o(j)}$ and the normalized affine sum in [COLLATZ-05](../multiplier-band-05/README.md) converges, since $\sum_j 1/P_j<\infty$. Therefore $|p_j|\le C P_j$. For squares with half-lengths tending to infinity, the preceding inequality with this sharper height bound gives $\liminf i/d\ge 1/\chi-1$. For $\theta=3/4$, the bound is $4.2988027866\ldots$.

## Build fast branches with early squares and full language

Enumerate the nonempty binary words $v_j$ by length and then lexicographically. If $\ell=|v_j|$ and $a=\#1(v_j)$, use the block

$$
U_j=1^{2\ell}v_j1^{\ell-a}0^a.
$$

It has length $4\ell$, with exactly $3\ell$ ones. Its multiplier stays at least one on each prefix. The initial $2\ell$ odd steps supply a factor $(3/2)^{2\ell}$, enough to cover even an all-zero target of length $\ell$. After the target the extra ones increase the multiplier, and the trailing zeros decrease it only to the final factor $(27/16)^\ell$.

Set $W_1=\mathrm{1110}$. For each $j$, independently choose a marker $S_j$ equal to $\mathrm{1110}$ or $\mathrm{1101}$, and set

$$
W_{j+1}=W_jW_jU_jS_j.
$$

Both markers have odd fraction $3/4$ and survive at every prefix. Concatenation preserves prefix survival and the odd fraction at block boundaries. The $W_j$ are nested prefixes of an infinite word $W$, and $W$ begins with $W_j^2$ for every $j$.

Every $v_j$ occurs in $U_j$. Hence $W$ has all $2^d$ binary words of length $d$, for every $d$, and is aperiodic. Each complete component in the construction has zero discrepancy from the odd fraction $3/4$, so the maximum prefix discrepancy in $W_{j+1}$ is bounded by the largest within-component discrepancy through stage $j$. This is $O(\log(j+2))$, since $|v_j|=O(\log(j+2))$. Because the $W_j$ at least double in length, the odd count in the first $N$ bits is $3N/4+O(\log\log(N+3))$. In particular, $P_N=2^{(0.1887218755\ldots)N+O(\log\log(N+3))}$, with leading exponent $(3/4)\log_2 3-1$.

Distinct marker sequences give distinct infinite words because the stage lengths are fixed independently of the choices. Any rational lift would have a nonrepeating orbit, since $W$ is aperiodic. Its prefix squares of unbounded length contradict the repeat-boundary inequality. Prepending any finite coefficient-surviving prefix preserves growth and survival. The squares then start at one fixed offset, so the same contradiction applies.

## Reproduce and scope

Run `python3 verify.py` in this directory. It checks the exact congruence for 1,134 combinations of parity blocks, odd denominators and repetition counts, including signed representatives. It also checks a 13,360-bit prefix of the construction. The infinite result follows from the proof.

The construction separates exponential symbolic growth and full whole-word complexity from rational liftability. It leaves open fast branches without the early repeats used in this argument. [COLLATZ-12](../fast-residues-12/README.md) shows that a family of these branches still fails the residue-size test. The parity and repetition tools have the precedents cited above. No priority claim is made. AI assistance was used for source review, derivation, checks and drafting.
