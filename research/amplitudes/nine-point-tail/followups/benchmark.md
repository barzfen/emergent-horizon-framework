# Eight-gluon reconstruction benchmark

The target is the splitting-factor-stripped leading 1–9 collinear contribution with parent ordering (1,2,4,6,8,7,5,3). Use tree-level colour-ordered gluon amplitudes, with negative helicity on 2 and 3 and positive helicity elsewhere. The source data are the two lifts and shared residue from the preceding nine-point tail calculation.

The available pool is the union of the 24 orderings in the shared residue and the six orderings in one fundamental BCJ identity. The two sets overlap only at the target, leaving 28 possible other amplitude values. Every relation-based method can use this same pool. Count the distinct other amplitude values required by each reconstruction, with the external kinematics given.

| Reconstruction | Other amplitude inputs |
| --- | ---: |
| Shared residue of either nine-point lift | 23 |
| Direct Kleiss–Kuijf elimination on the same pool | 23 |
| Fundamental BCJ relation, moving label 8 | 5 |
| Direct Parke–Taylor MHV formula, using external momenta | 0 |

The exact KK kernel on the pool is one-dimensional. The shared residue is its generator up to scale, so any KK reconstruction supported in this pool uses the same 23 inputs. The BCJ count is for the displayed strategy and is an upper bound, without a claim of optimality among BCJ combinations. The last row uses the closed MHV formula and counts other amplitude evaluations, with the formula evaluation itself still required.

## Verification

Run `PYTHONPATH=.. python3 benchmark.py`. It checks all three relation-based reconstructions at three rational spinor-helicity points satisfying momentum conservation. It also checks the leading collinear coefficient on the actual source orderings. On the holomorphic pole use the normalization lambda9 = lambda1. The parent has lambda equal to lambda1 and tilde lambda equal to the sum of the original collinear pair. Multiplication by the spinor bracket ⟨9 1⟩ removes the common pole from each active ordering, yielding the parent amplitude. The nonadjacent orderings are regular at the pole. This calculation uses the analytic amplitude and its pole, with rational complexified kinematics.

The benchmark uses the collinear limit described in [Dixon’s amplitude notes](https://arxiv.org/abs/hep-ph/9601359) and the fundamental BCJ amplitude relation discussed by [de la Cruz, Kniss and Weinzierl](https://arxiv.org/abs/1508.01432). It measures input count for a single reconstruction, with no timing or general claim about other helicity sectors or support problems.
