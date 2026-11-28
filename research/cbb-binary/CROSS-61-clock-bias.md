# EHF-CBB-CROSS-61 — Full local ticks under fixed and switched growth bias

[Series guide](GROWTH-CLOCKS-AND-BELL.md) · [Sign-weighted growth](CROSS-59-growth-ratios.md) · [Local growth counters](CROSS-60-local-growth-clock.md) · [Verifier](cross61_clock_bias.py)

**Date** 2026-11-16 (Australia/Brisbane)

**Status** Exact finite recurrence and labelled verification. Equality of the full-tick laws under fixed weights and strict ordering after a bias switch in the large-cycle limit.

## Compare two clocks in the same ring

These are the passive clocks of [CROSS-60](CROSS-60-local-growth-clock.md). Each observer follows the outgoing edge of a fixed labelled vertex. An insertion into that edge changes its sign from $s$ to $-s$. Two successive flips return the port to its starting sign and count as one full tick. The readout records the number of completed pairs. Observers use local change notifications and receive no global insertion count or notice of a change in weights.

Give each $+$ edge weight $u$ and each $-$ edge weight $v$. At each step select a slot in proportion to its weight and insert the third colour. There are no reversals. On the same ring, one monitored edge starts $+$ and one starts $-$. Grow from $n$ to $2n$, with even $n$ for the convergence tests. In the fixed protocol take $(u,v)=(2,1)$ throughout. In the switched protocol use $(2,1)$ for the first $n/2$ insertions and $(1,2)$ for the rest. The switch occurs at size $3n/2$. Choose initial plus fractions tending to the stationary fraction for $(2,1)$. Uniform selection is a control.

## What an edge experiences

At size $N$ with $K$ plus edges, the total weight is $W=uK+v(N-K)$. The marked port has conditional flip probability $u/W$ or $v/W$ according to its current sign. A $+$ split changes $K$ by $-1$ and a $-$ split by $+2$. The finite recurrence uses the state $(K,H)$, where $H$ is the port's flip count. A hit changes $K$ and adds one to $H$. All other splits change $K$ alone, with total probabilities from the background slot counts of each sign. The completed-tick count is $J=\lfloor H/2\rfloor$.

In the large-cycle limit, use $\tau=\log(N/n)$. The plus fraction follows the deterministic drift of [CROSS-59](CROSS-59-growth-ratios.md), which for fixed weights is

$$
\frac{dq}{d\tau}=F(q)=2-\frac{3uq}{u q+v(1-q)}-q.
$$

Within a stage, write $d(q)=u q+v(1-q)$ and define its exposure as the increment of $\theta$, with $d\theta=d\tau/d(q)$. In $\theta$ the port flips at rate $u$ when it is $+$ and at rate $v$ when it is $-$. Both ports in the experiment share the same deterministic exposure. The switch changes the bulk drift, so the second exposure uses the evolving plus fraction.

<details>
<summary>Convergence and how to compute the exposures</summary>

At one insertion from size $N$, the change in $K/N$ has conditional mean $F(K/N)/(N+1)$, with fluctuation bounded by $3/(N+1)$. Compare with the deterministic solution at successive values of $\log(N/n)$, whose increment equals the same drift step at the reference fraction plus $O(N^{-2})$. For the difference $e_j$ between the random and deterministic fractions, Lipschitz continuity on $[0,1]$ and the zero conditional mean of the fluctuation give

$$
\mathbb E[e_{j+1}^2]\le (1+C/N)\mathbb E[e_j^2]+C/N^2.
$$

Through a bounded growth factor, iteration yields $\sup_j\mathbb E[e_j^2]\le C' (e_0^2+1/n)$. This applies across the switch by joining the two deterministic solutions at $N=3n/2$. Replacing the actual port flip probability by its deterministic-reference value at each step gives a total probability-mass error bounded by a constant times $\sum_j\mathbb E|e_j|/(n+j)=o(1)$. This bound follows by averaging the conditional transitions on full histories and using contraction of the reference stochastic matrices. It applies to any fixed number of flip bins with an overflow bin. In a stage the reference updates have a common generator multiplied by $1/[N d(q)]$, whose sum tends to the exposure and whose squared sum tends to zero. Their product converges to the exponential of that generator times the exposure.

To compute an exposure for a prescribed size factor within a fixed-weight stage, take the deterministic plus and minus counts, $p_+,p_-$, normalized to have sum one at its start. In the variable $\theta$ they satisfy

$$
\frac{d}{d\theta}\begin{pmatrix}p_+\\p_-\end{pmatrix}
=\begin{pmatrix}-u&2v\\2u&-v\end{pmatrix}
\begin{pmatrix}p_+\\p_-\end{pmatrix}.
$$

Indeed the total increases at rate $u p_++v p_-$, and the normalized composition then obeys the drift above. The initial weight density $d_0$ and the two eigenvalues $\lambda_\pm=[-(u+v)\pm\sqrt{(u+v)^2+12uv}]/2$ determine the total as $c e^{\lambda_+\theta}+(1-c)e^{\lambda_-\theta}$ with $c=(d_0-\lambda_-)/(\lambda_+-\lambda_-)$. The total is strictly increasing since both counts are nonnegative and both weights positive. Solve for the $\theta$ that gives the chosen size factor. For the switched doubling from the stationary fraction $q_*=(\sqrt{33}-5)/2$, the exposures are $a\approx 0.295468$ and $b\approx0.188516$. At the start of the second stage the composition is still $q_*$.

</details>

## Fixed bias cancels over a complete pair

For constant weights, a port starting $+$ waits an exponential interval of rate $u$ and then one of rate $v$ for its first full tick. A port starting $-$ has the same two independent waits in the opposite order. The sum has the same law either way. At each completed pair the clock returns to its initial sign and starts another such wait. Consequently the distributions of completed tick counts are identical at every exposure in the large-cycle limit. The first single-flip waits still have different rates.

At finite size the two count laws can differ because the early port hit changes the total weight faced by later hits. For example, with weights $(2,1)$ and initial total weight $W$, the probabilities for a full tick in just two insertions are $2/W^2$ for the $+$ port and $2/[W(W+3)]$ for the $-$ port.

## Switching the bias splits every full-tick threshold

Let $u>v>0$ and hold the bias $(u,v)$ for exposure $a>0$, then $(v,u)$ for exposure $b>0$. The $+$ port can collect one fast flip in each stage if it is waiting for the second flip when the switch occurs. The $-$ port begins with the slow step. The probability gap for at least one full tick has the exact form

$$
\Pr(J_+\ge1)-\Pr(J_-\ge1)
=\frac{u+v}{u-v}(e^{-va}-e^{-ua})(e^{-vb}-e^{-ub})>0.
$$

The same direction holds for every positive threshold. To see this, let $y$ mark completed ticks and use the even and odd parity states. For the $+$ port before the switch, the tilted generator in row convention is $A$. After the switch it is $B$.

$$
A=\begin{pmatrix}-u&u\\vy&-v\end{pmatrix},\qquad
B=\begin{pmatrix}-v&v\\uy&-u\end{pmatrix}.
$$

The $-$ port uses $B$ first and then $A$. Both start in even parity. Each matrix exponential can be written $f_t(y)I+g_t(y)M$ for $M=A$ or $B$, using the common trace and determinant. With $\Delta=\sqrt{(u-v)^2+4uvy}$,

$$
g_t(y)=e^{-(u+v)t/2}\frac{2\sinh(t\Delta/2)}{\Delta}.
$$

Write $P_\pm(y)=\mathbb E[y^{J_\pm}]$. Their difference is the even-start row of $e^{aA}e^{bB}-e^{aB}e^{bA}$ summed over both terminal states. The terms linear in $A,B$ vanish upon taking that row sum, so

$$
P_+(y)-P_-(y)=(u^2-v^2)(y-1)g_a(y)g_b(y).
$$

Equivalently, the tail gaps have generating function

$$
\sum_{k\ge1}\left[\Pr(J_+\ge k)-\Pr(J_-\ge k)\right]y^{k-1}
=(u^2-v^2)g_a(y)g_b(y).
$$

For a positive duration, expanding the hyperbolic sine yields a series in $\Delta^2$ with positive coefficients at every degree. Substituting $\Delta^2=(u-v)^2+4uvy$ gives positive coefficients in $y$ as well. Thus the port that started on the initially favoured sign has a strictly greater chance of reaching each full-tick threshold after the switch. Setting $y=0$ gives the displayed first-tick gap.

## Doubling results

Each column pair gives two marginal probabilities for ports in the same ring. The values below are the large-cycle limits.

| Rule | At least one tick, starts $+$ | At least one tick, starts $-$ | At least two ticks, starts $+$ | At least two ticks, starts $-$ |
| --- | ---: | ---: | ---: | ---: |
| Uniform | 15.343% | 15.343% | 0.556% | 0.556% |
| Fixed bias | 15.726% | 15.726% | 0.599% | 0.599% |
| Switched bias | 20.139% | 12.012% | 0.739% | 0.407% |

| Initial size | Fixed bias, at least one tick ($+$ / $-$) | Switched bias, at least one tick ($+$ / $-$) |
| ---: | ---: | ---: |
| 50 | 15.875% / 15.724% | 20.333% / 11.983% |
| 200 | 15.816% / 15.779% | 20.234% / 12.041% |
| 800 | 15.737% / 15.727% | 20.152% / 12.011% |
| Limit | 15.726% / 15.726% | 20.139% / 12.012% |

Under fixed bias, each full tick contains one fast and one slow step, in either order. Under a switch, two ports on the same ring using the same counting rule can accumulate systematically different tick records because the rates change while each port is partway through its own sequence.

[CROSS-62](CROSS-62-blind-growth.md) uses the individual flip counts from a representative pool to estimate growth when the bias schedule is hidden.

## Reproduce

Run `python3 research/cbb-binary/cross61_clock_bias.py` from the repository root. The verifier checks the finite recurrence on both ports against all 47,952 labelled insertion histories through four insertions across three starting sizes and three protocols. It then compares the finite count distributions at doubling for starting sizes 50, 200 and 800 with the limiting distributions. The first two threshold gaps also agree with the generating-function coefficients.
