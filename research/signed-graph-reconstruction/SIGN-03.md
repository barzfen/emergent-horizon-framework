# SIGN-03 — Directional insertion separates mirror starts

**Status:** exact finite computation for unrestricted LR3 at size 7;
the randomized-direction equality follows analytically from reflection
symmetry. No MICRO/Pi or physics inference.

## Protocol

Keep the [SIGN-02](SIGN-02.md) marked set R = {1,2,3} and insert
label 7. A hit means the child's parity class containing 7 is exactly
R ∪ {7}. Fix the unmarked label 0 as an anchor. Retain the orientation
of each cyclic order through each uniform LR3 move; rotate back to
label 0 without reflecting.

Choose the insertion rule without consulting the target outcome:

- Forward: insert immediately after the anchor in the transported direction.
- Backward: insert immediately before it.
- Randomized direction: independently choose forward or backward with
  probability 1/2 just before inserting, and average over that choice.
- Uniform edge: the original BIN-09 control, uniform over all seven edges.

The two starts have the same underlying labelled cycle. Use
(0,4,5,1,6,2,3), with marked word 0001011, and its rooted reflection.
The protocol adds both an anchor and a retained direction; neither is
inferred from the unsigned gap pattern. A hit still uses the original,
reflection-invariant sector definition.

## Results

| Prior LR3 events | Forward, start | Forward, mirror | Randomized direction, either | Uniform edge, either |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1/7 | 1/14 | 1/49 |
| 2 | 0 | 6/49 | 3/49 | 9/343 |
| 3 | 0 | 39/343 | 39/686 | 67/2401 |

Backward insertion swaps the forward probabilities of the two starts.
Among all 360 reflected pairs of rooted oriented labelled cycles, the
forward rule distinguishes 144 after one reversal; randomization
distinguishes none. This is a pairwise mirror comparison, not a claim
that the anchor-randomized-direction protocol reduces to the original
unsigned gap quotient across different underlying cycles.

Run `python3 probe-directional-insertion.py`. It enumerates all reversal
event sequences for the listed horizons, checks the one-step comparison
over every size-7 cycle, and cross-checks insertion outcomes for every
edge using the bipartition of the child adjacency graph.

## What the control establishes

Reflection permutes the LR3 events and exchanges forward and backward
insertion. It preserves the unordered parity partition of the child.
Thus for any number of uniform reversals, reflection swaps the two
directional hit probabilities but leaves their average unchanged.
Randomizing the direction removes the mirror difference exactly. It does
not reproduce uniform-edge insertion: after one reversal the two
controls give 1/14 and 1/49, respectively, because the first still
samples only edges incident to the anchor.

This establishes that a direction-sensitive **controller** can turn
retained orientation into a difference in an otherwise direction-blind
output. It does not establish that closed-loop signs alone predict the
output, explain the BIN-09 decay modes, or derive the direction reference
from the bare comparison graph.
