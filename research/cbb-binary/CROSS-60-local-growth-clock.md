# EHF-CBB-CROSS-60 — Can a local clock measure logarithmic growth?

[Series guide](GROWTH-CLOCKS-AND-BELL.md) · [Protected LR3 clock](CROSS-46-local-clock.md) · [Growth scaling](CROSS-59-growth-ratios.md) · [Verifier](cross60_local_growth_clock.py)

**Date** 2026-11-15 (Australia/Brisbane)

**Status** Exact indistinguishability witness, finite count laws and a large-cycle limit under specified rates.

Start with a properly three-coloured labelled $n$-cycle and grow it by proper insertions. For an experiment ending after $m$ insertions, write

$$
G=\frac{n+m}{n},\qquad \ell=\log G.
$$

Can the observer estimate $\ell$ from events visible in its own patch? The experimenter sets the readout checkpoint. The observer receives neither the size, the insertion count, global event indices, nor an external time readout. A tick is a tracked local reversal or a detectable change of an adjacent sign, depending on the construction. Counting ticks across the interval assumes the observer can keep a local record.

## Two different growth histories give exactly the same clock reading

The [CROSS-46](CROSS-46-local-clock.md) clock keeps six successive phases within a 12-sign window. Its rule specifies the next reversal from the current phase. There are $N-12$ insertion slots outside that window at size $N$, all preserving the phase and its next move.

Run one lap of six reversals from the 21-vertex seed. In one run, make no insertions. In the other, insert 21 vertices outside the protected window between the third and fourth reversals. The full 12-sign readout at every local step is identical. The final ring sizes are 21 and 42 respectively. More generally any finite number of these insertions can be placed between two clock moves. The observed sequence of phases, including the tick count, therefore cannot determine growth under the admissible interleavings alone.

## Give each allowed event a fixed rate

Use the protected clock with a supplied scheduler. Give each of its $N-12$ eligible growth slots weight $1$ and the unique selected clock reversal weight $r>0$. At each event, choose proportionally to these weights. Omit other reversals. The same event order can be obtained by letting local events compete with independent exponential timers at their given rates. The clock reads its own ticks. Its input does not include $N$.

Let $T$ count clock reversals before the $m$-th insertion, starting at zero. At size $N$, the number of ticks before the next insertion has the geometric distribution on $0,1,2,\ldots$ with insertion probability $(N-12)/(N-12+r)$. Each clock tick changes the phase while leaving the event weights and growth-slot count the same. The counts at different sizes are independent, because the conditional distribution at a given size is the same for every earlier history. Hence

$$
\mathbb E[z^T]
 =\prod_{j=0}^{m-1}\frac{n+j-12}{n+j-12+r(1-z)},\qquad
\mathbb E[T]=r\sum_{j=0}^{m-1}\frac{1}{n+j-12}.
$$

Take $n\to\infty$ at fixed limiting $G$. The reciprocal sum tends to $\ell$ and the squared reciprocal sum tends to zero. The generating function tends to $\exp(r\ell(z-1))$, so $T$ converges in distribution to $\operatorname{Poisson}(r\ell)$. Dividing the tick count by the calibrated rate $r$ estimates $\ell$. The limiting variance is $\ell/r$.

For $r=1$ the no-tick probability telescopes exactly to $(n-12)/(n+m-12)$. After doubling it tends to $1/2$. A single unit-rate clock accumulates an average of about 0.693 reversal ticks per doubling in the large-cycle limit. The phase at one endpoint gives the number of reversals modulo six. Full tick counts require recording the individual phase transitions or completed laps.

## Count insertions directly through a local sign

In the insertion-only model of [CROSS-59](CROSS-59-growth-ratios.md), choose one fixed labelled vertex and monitor its outgoing sign. An insertion at that edge flips the sign because $s$ is replaced by $-s,-s$. The new outgoing edge remains the one the observer monitors. All other insertions are invisible there. With local change notifications, the observer can count these flips without receiving any notice of intervening insertions elsewhere. An endpoint-only observer sees the parity of the count.

With $k$ distinct anchored outgoing edges, each insertion hits one of the monitored slots with conditional probability $k/N$ under uniform growth. This remains true after any previous history. Thus the total count $C$ is a sum of independent Bernoulli variables with these probabilities. Individual port hits are mutually exclusive within one insertion. The calibration for the pooled count and its variance are

$$
\mathbb E[C/k]=\sum_{j=0}^{m-1}\frac{1}{n+j},\qquad
\operatorname{Var}(C/k)=\sum_{j=0}^{m-1}\left[\frac{1}{k(n+j)}-\frac{1}{(n+j)^2}\right].
$$

The mean differs from $\log G$ by at most $1/n$, by bounding the sum with the integral of $1/N$. For fixed $k$ the limit is $C\sim\operatorname{Poisson}(k\ell)$, since the log of the generating function $\prod_{j=0}^{m-1}[1+k(z-1)/(n+j)]$ tends to $k\ell(z-1)$. Consequently

$$
\Pr(C=0)\longrightarrow G^{-k},\qquad
\operatorname{SD}(C/k)\longrightarrow\sqrt{\frac{\ell}{k}}.
$$

| Passive ports pooled | Chance of zero ticks after doubling | Standard deviation of estimated log growth at doubling |
| ---: | ---: | ---: |
| 1 | 50% | 0.833 |
| 2 | 25% | 0.589 |
| 16 | 0.00153% | 0.208 |
| 64 | $5.42\times10^{-18}\%$ | 0.104 |

For comparison, the true log growth at doubling is $\log 2\approx0.693$. A silent local transcript is compatible with both zero growth and doubling. A passive observer with a fixed number of ports continues to see such ambiguous runs even as the initial cycle size tends to infinity. If the number of pooled ports grows with $n$, the finite variance bound $\operatorname{Var}(C/k)\le (\log G+1/n)/k$ makes the estimate converge in mean square for a fixed growth factor. This construction requires local event records and a way to pool them for the final readout.

## What the clock measures

The six-reversal oscillator records the phase of successive selected moves. Its tick count acquires information about growth once its event rate is specified relative to the rate per insertion slot. The passive observer acquires the same logarithmic scaling directly from uniform insertion opportunities. These calibrations give a noisy estimate of growth from local data, with the remaining uncertainty set by the amount of local activity that was observed.

[CROSS-61](CROSS-61-clock-bias.md) compares two passive clocks under fixed and switched orientation weights, counting a full tick when the local sign returns.

## Reproduce

Run `python3 research/cbb-binary/cross60_local_growth_clock.py` from the repository root. The verifier replays the identical clock traces at final sizes 21 and 42, compares the clock count law with 19,800 indexed event histories per rate at weights $r=1,2$, and checks the passive count law against all 3,024 labelled histories through four insertions for each of the one-port and two-port readouts.
