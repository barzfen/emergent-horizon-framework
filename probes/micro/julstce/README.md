# Julstce — reading detector order after MICRO growth

An exact classical probe of records in growing binary rings. The detector order is permanently invisible to the stream of added colours, yet the unmarked final shape retains a statistical trace at every growth horizon.

## Preparation and readout

A MICRO ring has no isolated bit. An active detector reads whether the two bits immediately outside its four-slot window differ. On a yes, it reverses the window if the result satisfies MICRO. This uses MICRO alone and imposes no label-dependent Pi condition.

Start with `0011110011111000`, with A at slot 0 and B at slot 11. The four logged readings are all yes.

| Order | Ring before growth | Lengths of its 1-runs |
|---|---|---|
| A then B | `1100110011111000` | 2, 2, 5 |
| B then A | `0011110011100110` | 4, 3, 2 |

The growth rule samples uniformly from all legal pairs of an edge and an inserted bit. An equal-colour edge permits its own colour, and a mixed edge permits either. Growth preserves all six boundaries. A nonuniform ring of length n with k ones and b boundaries has n+b events, of which k+b/2 add a one. Since both preparations start at (n,k,b) = (16,9,6) and these totals update using only the added colour, the laws of all finite added-colour sequences agree.

We give the two orders equal prior probability and decode using only the final ring, with rotations and reflections identified. At each growth horizon the optimal decoder chooses the order that gives the observed shape greater probability. Its success is one half plus one half the total variation distance between the two shape distributions.

| Insertions | Optimal from full shape | Optimal from longest 1-run alone |
|---:|---:|---:|
| 0 | 100.00% | 100.00% |
| 1 | 93.18% | 88.64% |
| 2 | 86.96% | 78.26% |
| 4 | 79.09% | 71.48% |
| 8 | 71.84% | 65.34% |
| 16 | 66.21% | 60.77% |
| 32 | 62.64% | 58.36% |

The shape distributions use exact probabilities. Each run of length L has L+1 legal growth events, comprising L−1 internal edges and one insertion of that colour at each boundary. Growing the run increases its weight by one. This is a standard Pólya urn with one category per run. For increments j_i totalling t and initial weights a_i, the probability is the product of binomial coefficients C(a_i+j_i−1,j_i), divided by C(sum(a_i)+t−1,t). The calculation aggregates these probabilities by the final shape. The verifier also constructs every legal insertion directly and matches the distributions for zero through three growth steps. The growth kernel respects rotation and reflection, so applying it to the two distributions cannot increase their total variation distance. [Pólya urn background](https://doi.org/10.1017/jpr.2020.59)

## An all-horizon bound

For a final ring, let a_i be the length plus one of each 1-run, let T be their sum, and read the following rotation- and reflection-invariant statistic:

`Q = sum_i a_i(a_i+1) / [T(T+1)]`.

This lies in [0,1]. A zero insertion leaves Q fixed. Conditional on a one insertion, run i grows with probability a_i/T, so the expected numerator is multiplied by (T+2)/T. The denominator changes by the same factor. Thus Q has constant expectation under ordinary growth. Its initial values are 66/156 for A then B and 62/156 for B then A. Their difference is 1/39 at every finite growth horizon. Since the expectation gap of any [0,1]-valued statistic bounds total variation from below, optimal order recovery stays at least **1/2 + 1/78 = 51.28%** for equally likely orders. This bound holds at every horizon. The [Wheeler–Julstce handover](../../../HANDOVER.md#a-result-linking-wheeler-and-julstce) proves a formula for the limit and estimates the full-shape accuracy at **58.3%** as the number of insertions grows.

## Reproduce or demonstrate

Run `python3 probes/micro/julstce/probe.py` from the repository root. It uses only the standard library and prints the exact fractions. Run `python3 probes/micro/julstce/limit_probe.py` with NumPy to estimate the limiting accuracy. For a tabletop version, use two-colour tiles in a ring. Flip a fair coin to pick the order and keep that choice hidden from the reader. For each growth step, list the legal edge-and-colour pairs and sample uniformly from the list. After one insertion, compare how often each order yields six consecutive ones. The exact predictions are 3/11 after A then B and 0 after B then A. The software check covers this case. A physical tile trial remains to be run.

This construction is a classical application of known probability theory. Its contribution is the explicit detector rule, witness and readouts that exhibit a durable trace under uniform MICRO growth. Physical measurement dynamics and external mathematical novelty have not been established.

- [Earlier MICRO growth and observer audit](../observer-compatibility-01/REPORT.md)
- [Earlier reversal admissibility audit](../../reversals/all-length-01/README.md)
