# EHF-CBB-CROSS-62 — Recovering ring growth from blind local records

[Series guide](GROWTH-CLOCKS-AND-BELL.md) · [Local growth counters](CROSS-60-local-growth-clock.md) · [Fixed and switched bias](CROSS-61-clock-bias.md) · [Verifier](cross62_blind_growth.js)

**Date** 2026-11-17 (Australia/Brisbane)

**Status** Exact finite expectation, a sampling bound, a blind numerical check, and an identifiability limit for sign-conditioned records with unknown initial composition.

## Double a counter's contribution every time it flips

Start with an oriented, properly three-coloured ring of $n$ vertices. Each insertion selects a slot by weight and inserts the third colour. An edge of sign $s$ splits into two edges of sign $-s$. At each insertion the two positive sign weights are shared by all edges of the corresponding signs. The bias schedule can vary by insertion number and is hidden from the decoder. There are no reversals.

Sample $k$ of the starting vertices uniformly without replacement. Each vertex can independently volunteer with the same probability. Conditional on a nonempty sample of size $k$, this gives a uniform sample without requiring the ring size. Each observer records $H_i$, the number of times the sign of its outgoing edge flips during growth. An observer that already records full ticks $J_i$ can recover $H_i$ with one extra bit at readout. Use $H_i=2J_i$ if the final sign equals the initial sign, or $H_i=2J_i+1$ if they differ. No global timestamps, initial size, final size, or switch notices enter the decoder.

After $m$ insertions, write $G=(n+m)/n$. For every finite $n,m$, the estimator

$$
\widehat G=\frac1k\sum_{i=1}^k 2^{H_i}
\qquad\text{satisfies}\qquad
\mathbb E[\widehat G]=G.
$$

Thus individual clocks may respond differently to the same bias switch, as in [CROSS-61](CROSS-61-clock-bias.md), while a representative pool can estimate the growth factor with a rule that is independent of that schedule.

## Why the weighting works

Each original slot grows a binary tree of descendants. The leaves present at the readout are the current slots descended from that original slot. If the tree at root $i$ has $L_i$ leaves, then $\sum_i L_i=n+m$.

Imagine an observer that follows one of the two daughters chosen by a fair coin each time its current slot splits. Conditional on the realised tree, the probability of reaching a particular leaf of depth $h$ is $2^{-h}$. The observer has seen $h$ flips along that path. Its contribution $2^h$ cancels the factor $2^{-h}$, giving conditional mean $L_i$ for the tree. A uniform sample of roots therefore gives conditional mean $(n+m)/n$.

The usual observer at a fixed starting vertex always follows its outgoing daughter. It has the same flip-count law, jointly for the sampled roots, as the coin-toss observer. Conditional on the bulk plus and minus counts and the current signs of the marked slots, the weight of each marked slot is fixed by its sign. A hit toggles that sign whichever daughter is taken. The bulk count changes in the same way under either choice. The next-step law of the bulk counts and marked flip counts is consequently the same for both tracking rules. This transfers the conditional-tree calculation for the coin-toss observer to an exact expectation for the usual observer.

For a stratified sample with a deliberately fixed number of $+$ and $-$ observers, write $\mu_s=\mathbb E[2^H\mid s\text{ initially}]$. An unbiased decoder combines the estimates of $\mu_+,\mu_-$ using the initial plus fraction $q_0$,

$$
G=q_0\mu_+ + (1-q_0)\mu_-.
$$

A uniform sample supplies those proportions without a separate census. The full-tick count alone drops the final sign bit used by this decoder.

## How much sampling helps

Assume the ratio of the larger to smaller slot weight is at most $R$ over the experiment. At size $N$ the hit probability for any marked slot is at most $R/N$. Since each hit multiplies $4^H$ by four,

$$
\mathbb E[4^H]\le
\prod_{N=n}^{n+m-1}(1+3R/N)
\le e^{3R/n}G^{3R}.
$$

Conditional on the completed trees, the random-daughter choices in different roots are independent. The variance due to choosing roots without replacement is at most the variance for sampling roots with replacement. Combining it with the conditional variances within roots gives $\operatorname{Var}(\widehat G)\le e^{3R/n}G^{3R}/k$. The conditional mean is the same $G$ for every realised forest, and the fixed outgoing rule has the same joint flip-count law. This gives mean-square recovery as $k$ grows at bounded $G$ and $R$. Large contributions from heavily hit slots can still make a single run noisy.

## Blind test on finite rings

The verifier first enumerates 12,096 complete insertion histories from a six-slot seed over four protocols. For each starting-sign cohort it checks the weighted mean of the fixed-outgoing contributions against the mean descendant counts in exact rational arithmetic. In 8,496 of those histories the unweighted sum of the realised contributions over all starting vertices differs from the final size. The identity is an expectation.

The second test uses 2,048 simulated rings per protocol, all starting at 3,072 vertices. The simulator supplies the hidden growth and bias schedule. The decoder takes only the recorded flip counts from uniformly sampled starting vertices. The initial sign fractions also vary by protocol.

| Hidden protocol | True $G$ | Mean estimate, 512 observers | Single-run RMSE, 128 observers | Single-run RMSE, 512 observers |
| --- | ---: | ---: | ---: | ---: |
| Uniform | 2.000 | 2.002 | 0.172 | 0.086 |
| Fixed 5:1 bias | 1.500 | 1.500 | 0.076 | 0.035 |
| 2:1 becomes 1:2 midway | 2.000 | 1.999 | 0.177 | 0.083 |
| Three successive biases | 2.500 | 2.499 | 0.243 | 0.116 |

The mean in the table is across simulated rings. RMSE is measured against the true growth factor for a single ring. The simulation counts slots and marked signs, with per-slot selection probabilities identical to those of explicit rings under sign-only weighting. The narrow exact census uses the ordered slot lists directly.

## When the sign-conditioned records are ambiguous

Suppose the observer has separately normalised histograms for the two initial signs and knows neither their population proportions nor a representative mixture. Even the two full flip-count distributions can then be ambiguous in the large-ring limit.

Take the constant bias $(u,v)=(2,1)$ and the same exposure $\theta=1/2$ in the two preparations, in the sense of [CROSS-61](CROSS-61-clock-bias.md). In that exposure a marked edge alternates flip rates $2$ and $1$, independently of the initial bulk mix once its own sign is specified. Both preparations therefore have the same two sign-conditioned count laws. Their growth factors differ because the bulk counts start in different proportions.

At the start, the total weight density is $1+q_0$. With $\lambda_\pm=(-3\pm\sqrt{33})/2$, the normalised bulk size at exposure $\theta$ is

$$
G=c e^{\lambda_+\theta}+(1-c)e^{\lambda_-\theta},
\qquad c=\frac{1+q_0-\lambda_-}{\lambda_+-\lambda_-}.
$$

This gives $G\approx1.94615$ at $q_0=1/4$ and $G\approx2.10924$ at $q_0=3/4$. The rate rule is identical. The lost information is the actual mixture used to average the two sign-conditioned records. With a representative pooled flip-count law the mean of $2^H$ identifies $G$, so two distinct growth factors cannot have that same law.

## Reproduce

From the repository root run `node research/cbb-binary/cross62_blind_growth.js`. The verifier uses only standard JavaScript. It includes the exact census, seeded blind simulations, and the hidden-composition example.
