# Julstce memory under four-slot reversals

**Result.** Detector-order information persists indefinitely under the specified run-count-preserving four-slot reversal protocol. With one attempt after every insertion, the limiting optimal accuracy for equally likely orders is **strictly above 50.7% and below 54.27%**. Both inequalities follow from exact arithmetic and bounds on the infinite tail. The entire inserted-colour sequence remains blind to detector order. This result applies to the transition rule below.

## Protocol

Start with the two preparations in the [Julstce probe](../README.md), `1100110011111000` and `0011110011100110`, with equal priors. At each step:

1. Choose uniformly among legal edge-and-colour insertion events and perform the insertion.
2. With probability $p$, choose one starting slot uniformly on the new ring and attempt to reverse four consecutive slots, wrapping around the seam. Reject the attempt if it creates an isolated bit or changes the number of runs. A rejected attempt leaves the ring as it was and uses up the attempt.
3. At the chosen horizon, read the final ring up to rotation and reflection, preserving the colours. The final insertion's reversal attempt is included.

The protocol counts attempted reversals. At $p=1$, there is one attempt per insertion and only some attempts change the word. Longer reversals and a scheduler that resamples until a valid reversal is found give different dynamics.

Every accepted reversal preserves size, colour totals and the number of runs. The next inserted colour has probability $(k+b/2)/(N+b)$ of being a one, where $N$ is size, $k$ the number of ones and $b$ the number of runs. The two preparations start at the same $(N,k,b)$ and these quantities update identically given the added colour. This proves equality in law of the entire colour stream for every $p$.

## Exact finite calculation

Represent the shape by its six alternating run lengths, starting at a zero run and using the least representative under the colour-preserving rotations and reflections. A run of length $L$ grows with weight $L+1$. A shape-changing four-slot reversal that preserves the run count moves a whole run of length $k=2$ or $3$ along the ring. It transfers $4-k$ sites from one flanking run to the other. Each eligible donor side corresponds to one starting slot. A donor must retain at least two sites.

To see the move rule, a valid four-slot word with two inner colour changes is a palindrome, with a two-site run between its ends. A word with one inner change has different endpoint colours. Preserving the run count then requires the two bits outside the four slots to have the same colour. The intervening run of the opposite colour is therefore fully inside the window, with length two or three. Reversing the window transfers the remaining sites across it.

Propagate the signed difference $d$ between the two shape distributions. For rational $p$, all updates use an integer numerator and one common denominator per horizon. The optimal equal-prior accuracy is $1/2+\sum_s |d(s)|/4$. Its value cannot increase with the number of steps, because each next step applies the same Markov kernel to both distributions.

| Attempt probability per insertion | After 16 insertions | After 32 | After 48 | Bounds on limiting accuracy |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 66.21% | 62.64% | 61.29% | About 58.3% in the [growth-only analysis](../../../../HANDOVER.md#a-result-linking-wheeler-and-julstce) |
| 0.005 | 66.13% | 62.57% | 61.23% | Above 57.18%, below 61.23% |
| 0.25 | 62.65% | 59.75% | 58.71% | Above 54.38%, below 58.71% |
| 1 | 56.40% | 54.80% | 54.27% | Above 50.7%, below 54.27% |

The finite accuracies are rounded for display. The upper bounds use the unrounded 48-step values and monotonicity. The lower bounds use the certificate below.

## Bounding the infinite tail

Use the final-shape event that one run contains strictly more than half of the ones. Starting from any shape $s$ at size $m$, let $g(s)$ be the limiting probability of this event if growth continues without reversals. Under the run urn, the three relative one-run lengths have a Dirichlet distribution with integer parameters $a_i=L_i+1$. Only one run can exceed half. Consequently $g(s)$ is the sum of the three beta tail probabilities at one half, calculated as fair-coin binomial sums. For each run the number of tosses is $\sum_i a_i-1$, with the binomial count running from zero to $a_i-1$.

Couple growth with and without reversal attempts from this same state. Use the same insertion outcomes until the first attempt that changes the ring. Under the reference growth process, each run visits a fixed length $k$ as one uninterrupted stage. From size $N$, it leaves that stage by growing with probability $(k+1)/(N+6)$ on the next insertion. Summing the expected exit indicators across future sizes gives at most one exit. After the first insertion from the checkpoint, $N\ge m+1$. Thus

$$
\sum_{N=m+1}^\infty \frac{\Pr(L_N=k)}{N}
\le \frac{1+6/(m+1)}{k+1}.
$$

At most two possible reversal starts correspond to each short run. Let $n_2$ and $n_3$ count runs of length two and three at the checkpoint. By a union bound, the probability of ever separating the two coupled trajectories is at most

$$
e(s)=\min\left(1,\,2p\left(1+\frac6{m+1}\right)
\left(\frac{n_2}{3}+\frac{n_2+n_3}{4}\right)\right).
$$

A run too long to visit a stage under growth contributes zero. For every future horizon the probability of the event differs between the two processes by at most $e(s)$. Taking the growth-only event probabilities to their limit gives the following lower bound on the limiting optimal accuracy:

$$
\frac12+\frac12\max\left(0,\left|\sum_s d(s)g(s)\right|-\sum_s |d(s)|e(s)\right).
$$

This uses the signed difference at the checkpoint, so already indistinguishable probability mass contributes zero. The checker evaluates the bound with exact rational arithmetic at $m=64$ and asserts that the $p=1$ result exceeds $50.7\%$. The displayed lower bound before rounding is approximately $50.7657\%$. The proof leaves the actual limiting accuracy and the behavior under broader reversal schedules open.

## Reproduce

From this directory, use a C++17 compiler with the GMP development headers and Python 3.

```sh
c++ -std=c++17 -O3 -Wall -Wextra -Wpedantic lr4_probe.cpp -lgmpxx -lgmp -o /tmp/ehf_lr4_probe
python3 check_lr4.py /tmp/ehf_lr4_probe
/tmp/ehf_lr4_probe 0 1 48
/tmp/ehf_lr4_probe 1 200 48
/tmp/ehf_lr4_probe 1 4 48
/tmp/ehf_lr4_probe 1 1 48
```

The Python check enumerates literal slot reversals and uses rational probabilities. It compares the exact finite-horizon calculation at one, two and four insertions for all four rates. The C++ verifier uses exact integers throughout both the propagation and the certificate. Conversion to decimal is for display. Codex assisted in deriving the bounds, writing the code and preparing this note.
