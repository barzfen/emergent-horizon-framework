# SIGN-01 — Orientation signs do not distinguish unrestricted LR3 parity sectors

**Status:** exact finite computation at sizes 5–8 and an analytic obstruction
for the specified observation. No claim about MICRO/Pi-restricted dynamics
or physics.

## Which sectors?

[BIN-08](../cbb-binary/BIN-08-observable-spectral-modes.md) and
[BIN-09](../cbb-binary/BIN-09-analytic-mode-selection.md) define the
unrestricted LR3 walk on distinct labelled Hamiltonian cycles, modulo
rotation and reflection. They identify two **decay eigenvalues**, 5/7 and
2/7, at size 7, not two sectors or sector weights. The actual output
sectors are the 35 size-8 LR3 components (unordered 4+4 partitions).
We therefore compare size 7 with size 8, using sizes 5 and 6 as smaller
controls. No MICRO, Pi filter, fixed marked subset or growth history is
included in the graph observed by this probe.

## Method and finite results

As in [HOL-05](../../probes/reversals/orientation-holonomy-13/README.md),
apply each reversal in the source's canonical orientation, then record
whether the oriented output must be reflected to reach the canonical
target. Compute these signs without consulting parity sectors. Keep every
move event, including parallel edges. Check reciprocal event counts,
solve for a vertex-sign potential on each component (an inconsistency
certifies an unbalanced component), and compare to the sector partition
only after computing the signs. A BFS on the orientation double cover
finds a shortest negative loop based at the identity cycle; a separate
segment-reversal replay verifies the orientation flip.

| Size | Cycles | LR3 components (size each) | Unbalanced | Shortest negative loop at identity |
| --- | ---: | ---: | ---: | ---: |
| 5 | 12 | 1 (12) | 1 | 4 |
| 6 | 60 | 10 (6) | 10 | 2 |
| 7 | 360 | 1 (360) | 1 | 9 |
| 8 | 2,520 | 35 (72) | 35 | 5 |

At size 6, some parallel events have opposite signs: the two-step witness
is not an ordinary traversal of one edge and its inverse. At sizes 5, 7
and 8, the event signs are unambiguous on simple edges. Run
`python3 probe.py` from this directory to reproduce the census and
witness sequences (zero-based segment starts in canonical source charts).

## Why the failure is structural

For unrestricted LR3, any permutation of vertex labels commutes with
reversing a segment on **oriented** cyclic orders, and with orientation
reflection. A relabelling mapping one unordered parity partition to
another thus gives an isomorphism of the oriented move covers over the
corresponding components. Canonical charts may change under relabelling;
those changes only switch incident edge signs. Hence all even-size parity
components are isomorphic **up to switching** as signed event graphs.
No statistic invariant under both relabelling and switching, even one
using the full signed component, can recover which labelled partition it
came from. This does not preclude recovering the components from the
unsigned relation or recovering their labels when vertex identities and
their parity positions are supplied.

There is also a direct explanation for the negative loops. With positions
numbered around a rooted representative, LR3 swaps positions i and i+2.
Those transpositions generate arbitrary permutations on each connected
component of the position graph with edges i~i+2. That graph is connected
at odd size and has the two parity classes at even size. Reflection fixing
position 0 (i maps to -i modulo n) preserves each even-size parity class,
so in both cases the reflected order is reachable by LR3. Projecting the
reversal sequence to unoriented orders yields a negative closed walk.

## What remains

This is a negative result for **unmarked** sector identification, not a
test of the switching-deck reconstruction theorem or a new explanation
of the 5/7 and 2/7 rates. The next comparison should fix an independently
specified marked triple and the BIN-09 insertion observable, and ask
whether a signed observable has predictive content beyond the existing
unsigned marked-gap quotient. The marked data break the symmetry used
above; any resulting distinction depends on what the observer is given.
