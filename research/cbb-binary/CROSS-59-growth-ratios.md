# EHF-CBB-CROSS-59 — Reversal availability under weighted cycle growth

[Series guide](GROWTH-CLOCKS-AND-BELL.md) · [One-insertion result](CROSS-57-growth-phase.md) · [Sign rewrite rules](CROSS-21-orientation-sign-rewrite-rules.md) · [Verifier](cross59_growth_ratios.py)

**Date** 2026-11-15 (Australia/Brisbane)

**Status** Exact formulas and finite recurrence, large-cycle limits under two specified growth rules, finite labelled verification.

## The experiment

Start with a properly three-coloured, oriented, labelled $n$-cycle containing a legal colour-changing length-three reversal (LR3) on three marked vertices. Each insertion selects a slot between adjacent vertices with probability proportional to the slot's weight. Insert a fresh vertex of the third colour. Perform $m$ insertions with no intervening reversals. Ask whether reversing the *same three marked vertices* is legal at the end.

The dimensionless growth ratio is $x=m/n$. Equivalently, the final cycle has $G=1+x$ times as many vertices as the initial cycle. Uniform growth gives about **9.77%** availability after doubling in the large-cycle limit. Reweighting the slots changes that number and can change the power of $G$ governing decay. This probe measures the availability of the original move, which may disappear and return during the run.

## Why four slots matter

Give the colours the cyclic order $0,1,2$. Write $+$ for an edge whose colour increases by one modulo three and $-$ for the reverse. Inserting the third colour replaces $s$ by $-s,-s$. The four signs of a legal colour-changing LR3 are $(s,-s,-s,s)$. The two inner slots lie between the three marked vertices. The two outer slots are the immediate edges into and out of the marked triple.

An insertion in either inner slot permanently separates original neighbours. As long as the triple is intact, its inner signs stay fixed. Inserting into an outer slot changes the sign of the immediate outer edge on that side. Each side must return to its initial sign for the reversal to be legal. This happens after an even number of hits on that side's immediate outer edge. All other insertions leave the four tracked signs alone.

## Weight the slots around the marked reversal

Use relative weight $a>0$ on either inner slot, $b>0$ on either current outer slot, and $1$ elsewhere. After an inner hit the future weights can be taken as uniform because the target event is then impossible. At step $j$, a live history has total weight $D_j=n+j-4+2a+2b$.

Let $h_L,h_R$ count the outer hits on the two sides. The even-parity indicator on side $i$ is $(1+(-1)^{h_i})/2$. The product of the two indicators expands into four terms. A term involving $k$ parity signs, for $k=0,1,2$, loses $2a/D_j$ to inner hits and changes sign with probability $kb/D_j$ from outer hits. Its one-step expectation on live histories is multiplied by $1-(2a+2kb)/D_j$. Summing the four terms gives

$$
P^{a,b}_{n,m}=\frac14\sum_{k=0}^2 {2\choose k}\prod_{j=0}^{m-1}
\left(1-\frac{2a+2kb}{D_j}\right).
$$

Under uniform weights $(a,b)=(1,1)$ this recovers the one-step result $(n-4)/n$. At $m=2$, one outer hit followed by another at that side's new boundary gives a history where the move becomes available again. As $n\to\infty$ and $m/n\to x$ with fixed $a,b$, the sum of reciprocal denominators tends to $\log G$ and the sum of their squares tends to zero. The limit is

$$
P^{a,b}_\infty(x)=G^{-2a}\left(\frac{1+G^{-2b}}2\right)^2.
$$

As $x$ increases in the limiting curve, $P^{a,b}_\infty\sim G^{-2a}/4$. The inner slots set the decay exponent, and the outer slots affect the return probability along the curve.

## Weight colour orientation throughout the ring

Use weight $u>0$ on every $+$ edge and $v>0$ on every $-$ edge. This rule uses the chosen orientation and cyclic colour order. It treats slots of the same sign equally, independently of the marked labels. Write $w_+=u$ and $w_-=v$. At size $N$ with $K$ plus edges, the total weight is $W=uK+v(N-K)$. A $+$ split sends $K$ to $K-1$. A $-$ split sends it to $K+2$.

The exact finite recurrence keeps a probability mass on each live state $(K,\ell,r)$, where $\ell,r$ are the two immediate outer signs. Initially $\ell=r=s$ and the inner signs both equal $-s$. Each inner split removes its mass from the live states. Each outer split flips its own sign and updates $K$. Each background split updates $K$ alone. Its probability is the number of background slots of its sign times its slot weight divided by $W$. Thus the projected event is the sum of the terminal masses with $\ell=r=s$. The verifier implements this recurrence and also checks the reversal directly on full labelled cycles.

For the limiting experiment, choose initial plus fractions tending to the stationary fraction $q_*$. With $q=K/N$, the expected change in $q$ from one insertion is $F(q)/(N+1)$, where

$$
F(q)=2-\frac{3u q}{u q+v(1-q)}-q.
$$

Since $F$ strictly decreases from $2$ to $-2$, $q_*$ is the unique root in $(0,1)$, equivalently

$$
2v-(u+3v)q_*-(u-v)q_*^2=0.
$$

Let $d=u q_*+v(1-q_*)$. The live triple has a constant rate of loss $2w_{-s}/d$ in the variable $\log G$. Each outer sign jumps from $s$ to $-s$ at rate $w_s/d$ and back at rate $w_{-s}/d$. The two outer processes are independent in the limiting formula. The initial-sign return probability for either is $\big[w_{-s}+w_s G^{-(u+v)/d}\big]/(u+v)$, so

$$
P_\infty(x\mid s)=G^{-2w_{-s}/d}
\left(\frac{w_{-s}+w_s G^{-(u+v)/d}}{u+v}\right)^2.
$$

<details>
<summary>Why replacing the changing total weight by its limiting density works</summary>

Run the full growth process, including histories whose marked triple has already broken. The one-step drift of $q$ points toward $q_*$, so the cross term in the expected square of $q-q_*$ is nonpositive. The change in $q$ has absolute value at most $2/(N+1)$. Consequently, if the initial plus fraction is $q_n$, then $\mathbb E[(q-q_*)^2]\le(q_n-q_*)^2+4/n$ at every later size.

At each size, the transition of the four live boundary states has a contribution from each local hit proportional to $1/W$. Replacing it by $1/(Nd)$ incurs a one-step error in total absolute mass bounded by $C\mathbb E|q-q_*|/N$, with $C$ depending on the two fixed weights. This uses the full process bound with a live-event indicator. For fixed $x$, summing these errors gives a quantity tending to zero because $\sum_{N=n}^{n+m-1}1/N\to\log G$. The reference transition at each step is a substochastic matrix of the form $I+Q/N$, for sufficiently large $n$, so propagation cannot amplify the sum of absolute mass errors. The fixed matrix $Q$ comprises the two boundary generators and a constant killing term. The product of reference transitions tends to $\exp(Q\log G)$ since the reciprocal squares sum to zero. This factorizes into the two boundary transition laws and the common survival factor.

</details>

Both one-insertion probabilities are $1-2(u+v)/W$ for the same $N,K$, irrespective of which boundary sign the motif starts with. Their large-cycle curves also have the same initial slope $-2(u+v)/d$ with respect to $x$. The difference at doubling comes from subsequent insertions. When $u>v$, a motif with $+$ outer edges has $-$ inner edges, giving a slower rate of permanent interruption. Its late-growth decay exponent is $2v/d$, compared with $2u/d$ for the opposite motif.

## Results at doubling

| Insertion rule | Available at $G=2$, large-cycle limit |
| --- | ---: |
| Uniform slots | $25/256 \approx 9.7656\%$ |
| Double the two current outer weights | $289/4096 \approx 7.0557\%$ |
| Double the two inner weights | $25/1024 \approx 2.4414\%$ |
| Double all $+$ weights, starting with $+$ outer signs | $8.3837\%$ |
| Double all $+$ weights, starting with $-$ outer signs | $7.2594\%$ |

For the final two rows, $q_*=(\sqrt{33}-5)/2\approx 0.3723$. At each finite starting size, use the closest compatible initial plus count $K$ satisfying $2K-n\equiv0\pmod 3$ and $2\le K\le n-2$. The two motifs can use the same $K$.

| Initial size $n$ | $+$ outer signs | $-$ outer signs |
| ---: | ---: | ---: |
| 50 | 7.9545% | 6.7901% |
| 200 | 8.2407% | 7.1050% |
| 800 | 8.3557% | 7.2288% |
| Limit | 8.3837% | 7.2594% |

Thus $m/n$ indexes comparable amounts of growth and gives a size-independent limiting curve for each of the tested preparations and rules. The dimensionless slot-weight ratios enter the curve too. For sign weighting away from the chosen initial composition, the bulk plus fraction can change during the run, and the stationary-fraction formula above does not apply. The logarithm appears here because a fixed number of local slots competes with a total weight proportional to the current size. These calculations use insertion counts and classical probabilities. They supply no calibration of a physical clock.

## Reproduce

From the repository root, run `python3 research/cbb-binary/cross59_growth_ratios.py`. It uses the standard library. It compares the exact formulas and recurrence against 127,872 complete insertion histories across sizes 6, 7 and 8, both initial boundary signs, and four insertion rules. It checks availability at each step through four insertions and compares the sign-weighted finite recurrence at doubling with the large-cycle limit.
