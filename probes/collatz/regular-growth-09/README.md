# COLLATZ-09 · How slowly can a regular multiplier grow?

[COLLATZ-08](../residue-stabilisation-08/README.md) showed that frequent positive residue fits would force an actual starting integer. Here we prove an obstruction for branches with two-sided polynomial multiplier growth.

**PROVED.** Write $P_N=3^{a_N}/2^N$, where $a_N$ counts the odd inputs to the first $N$ shortcut steps. Suppose that for some $\beta\ge0$ and fixed $0<c\le C$,

$$
c(N+1)^\beta\le P_N\le C(N+1)^\beta
$$

for all $N$. If the parity word has a rational 2-adic lift, then

$$
\beta>\frac{1}{h_2(\log_3 2)}=1.0526808586\ldots,
$$

where $h_2(t)=-t\log_2 t-(1-t)\log_2(1-t)$. The strict inequality includes exclusion of the endpoint. Both sides of the multiplier assumption matter.

## Bound the orbit height

Use the fixed-denominator numerator map of [COLLATZ-05](../multiplier-band-05/README.md), with $x_i=p_i/q$, $q>0$ odd. The affine identity from that probe is

$$
\frac{p_i}{P_i}=p_0+\frac{q}{3}\sum_{\substack{0\le j<i\\w_j=1}}\frac{1}{P_j},
$$

where $w_j$ is the parity bit at step $j$. Bounding the sum by $c^{-1}\sum_{j<i}(j+1)^{-\beta}$ gives a height envelope $Y_N$ for all $|p_i|$ with $i\le N$:

| Multiplier exponent | Height envelope $Y_N$, up to a fixed constant |
|---|---|
| $0\le\beta<1$ | $N+1$ |
| $\beta=1$ | $(N+1)\log(N+2)$ |
| $\beta>1$ | $(N+1)^\beta$ |

In the last case the normalized sum converges. For a positive start $x_0>0$ its limit after adding $p_0$ is strictly positive, so $p_N/P_N$ tends to a positive constant.

A repeated orbit value would make the tail periodic. Repeating a nonempty period of $d$ bits with $a$ odd steps multiplies $P_i$ by $3^a/2^d\ne1$ on each lap. The result would be exponential growth or exponential decay, both incompatible with the two-sided polynomial hypothesis. Thus the orbit values of any hypothetical rational lift are distinct.

## The available windows are too few

Let $\alpha=\log_3 2$. For any length-$d$ window starting at position $i$, its multiplier satisfies

$$
\frac{P_{i+d}}{P_i}\ge \frac{c}{C}\left(\frac{i+d+1}{i+1}\right)^\beta\ge \frac{c}{C}.
$$

So the window must have at least $\alpha d-\log_3(C/c)$ odd bits. The number of possible length-$d$ words with that many odds is

$$
O\!\left(\frac{2^{h_2(\alpha)d}}{\sqrt d}\right).
$$

To see this, take $t_d=\lceil\alpha d-\log_3(C/c)\rceil$ for large $d$. Because $\alpha>1/2$, the ratios of successive binomial coefficients for $k\ge t_d$ stay below a fixed number less than one. The tail sum is bounded by a constant times $\binom d{t_d}$. Stirling's formula gives the displayed estimate, since $t_d=\alpha d+O(1)$.

Choose $d=\lceil\log_2(2Y_N+1)\rceil$. The height is smaller than half the modulus $2^d$. By [COLLATZ-06](../parity-complexity-06/README.md), distinct numerators in the height range require distinct length-$d$ parity windows. This is the parity-separation argument of Dubickas, applied to the fixed-denominator map. Therefore

$$
N-d+1 \ \le\ O\!\left(\frac{Y_N^{h_2(\alpha)}}{\sqrt{\log N}}\right).
$$

Here $d=O(\log N)$. For $\beta\le1$, the right side is $o(N)$ since $h_2(\alpha)<1$, even with the logarithm in the height envelope at $\beta=1$. For $1<\beta\le1/h_2(\alpha)$, it is also $o(N)$, including equality because of the square-root factor. This contradicts the required number of distinct windows. [Dubickas (2009), Theorem 5 and §5](https://doi.org/10.1017/S0017089508004655)

## What changes in the residue test

For any two-sided multiplier law of exponent $\beta>1$, a genuine orbit would fit the residue-size bound of COLLATZ-08 with height exponent $s=\beta$. The earlier bound used $s=\beta+1$ from an upper envelope alone. For the exponent $\beta=4\log_2 3$ and resolution $D=30$ in [COLLATZ-07](../residue-size-07/README.md), the sufficient lower density for stabilisation improves to $\beta/30=0.2113283334\ldots$. This is a threshold for the fitting test with the refined height bound, and supplies no evidence that a positive branch actually passes.

## Odd-density literature check

López and Stoll's 2021 preprint states a broader conclusion that a divergent rational orbit must have lower odd density exactly $\log_3 2$. In §6, the supercritical exclusion invokes equations (15)–(16) to pass from a real irrational limit to a 2-adic irrational limit of the same partial sums. Those equations describe the 2-adic inverse limit of the partial sums. The step from real irrationality to 2-adic irrationality needs a separate argument. The result above uses the affine height bound and integer congruences directly. [López and Stoll (2021), Theorem 1, equations (15)–(16), and §6](https://arxiv.org/abs/2101.12747v1) · [Related review discussion](https://rstation.ai/problems/collatz/papers/16/v1)

For a control on that inference, set

$$
z_n=-\frac{2^n}{3^{2n}}
\left\lfloor(\sqrt2-2^{-n})\,\frac{3^{2n}}{2^n}\right\rfloor,\qquad n\ge1.
$$

The rational terms have denominators that are powers of three and are zero modulo $2^n$. They decrease in the real order to $-\sqrt2$, since $z_n+\sqrt2$ lies in $[2^{-n},\,2^{-n}+(2/9)^n)$, and successive error intervals are strictly separated. Their 2-adic limit is $0$. This is a control sequence for the general inference. It is outside the special Collatz partial sums, so it does not decide the truth of the preprint's odd-density claim.

The polynomial-growth exclusion leaves open regular exponents above $1.0526808586\ldots$ and branches without a two-sided polynomial envelope. We checked the numerical threshold, the binomial-tail calculation and the control arithmetic. The proof makes no priority claim. AI assistance was used for source review, derivation, checks and drafting.
