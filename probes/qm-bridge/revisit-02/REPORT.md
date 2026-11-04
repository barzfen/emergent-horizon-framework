# EHF QM bridge revisit 02 — orientation transport and its classical control

**Evidence status: COMPUTATIONAL / NEGATIVE CONTROL; analytic arguments are stated explicitly. Physical QM is not derived.**

4 November 2026 · Barry Fensom research collaboration

## Outcome

Actual admissible LR2/LR3 moves support a nontrivial two-valued orientation transport on some MICRO–OPW23 components. This transport was constructed without assigning complex amplitudes, a Hamiltonian wave equation or a Born rule. At nine vertices, different histories of the same length can reach the same undirected carrier state with opposite transported orientations.

The complete tested statistics are reproduced exactly by a classical Markov process on oriented tours. Signed cancellation occurs in a difference of probabilities; ordinary carrier occupancy still adds positively. This establishes a structural candidate for further investigation and a precise boundary on its present meaning. No physical phase, quantum interference, unitary dynamics or quantum probability law has been derived.

## Model and additional choice

Use the fixed assignment type 1 on vertices {1,2,3} and type 0 elsewhere. States are undirected labelled Hamilton cycles, modulo rotation/reflection, satisfying cyclic no-isolation. Keep the existing canonical chart: rotate label 0 to the first position, then choose the lexicographically smaller direction. Pi is the set of labels at even positions in this canonical representative. Allowed moves are circular reversals of length 2 or 3 preserving Pi and MICRO. Geometrically unchanged targets are excluded. Distinct indexed starts remain separate events.

This matches the retained finite state spaces in MICRO–OPW 01. No growth, bit flips or external phase rule is introduced. For stochastic calculations, choose uniformly among the retained indexed LR2/LR3 events; a frozen state has a self-loop. This is a supplied clock and rate rule, different from Revisit 01's distinct-edge continuous-time control.

The new choice is to TRACK orientation along histories instead of discarding it after each move. Each undirected cycle has two oriented tours modulo rotation. Applying the actual reversal to an oriented tour and rotating back to anchor 0 gives another oriented tour. Comparing its direction with the chosen canonical target gives a flip bit b_e, or sign s_e=(-1)^b_e.

This is a particular lift of the existing moves. EHF has not uniquely selected it. The oriented tours have exactly the same undirected edge sets; retaining a direction is history bookkeeping unless an additional physical carrier or access mechanism represents it. Canonicalization alone does not construct a detector of orientation.

## Exact structural checks

For the representative colouring only:

| Vertices | MICRO-valid undirected states | Indexed directed events | Components | Flat orientation transport | Components with a negative closed walk |
|---:|---:|---:|---:|---:|---:|
| 7 | 72 | 168 | 15 | 12 | 3 |
| 9 | 2,160 | 8,160 | 111 | 102 | 9 |

These are exhaustive computations at these two sizes for this assignment, not all assignments or an asymptotic theorem. Every event has the same reverse multiplicity. No pair of distinct base states in these two graphs has both flip and nonflip event channels; the code nevertheless retains event multiplicity.

Flat means the edge signs can be removed throughout the component by choosing opposite canonical directions at selected states. Equivalently, all closed-walk sign products are +1. A negative closed walk prevents such a removal.

Changing the chosen direction at state x by g(x) in {+1,-1} changes s_xy to g(x)s_xy g(y). On a closed walk every g occurs an even number of times, so their product cancels. Thus the negative closed-walk sign does not depend on arbitrary choices of local representative directions. It remains a property of the chosen transport lift, not a proof that nature realizes the lifted variable.

The independent oriented-tour verifier obtains 144 oriented states in 27 components at n=7 and 4,320 oriented states in 213 components at n=9. A flat base component lifts to two disjoint copies; a nonflat component has a connected double cover. The counts satisfy 27=2*12+3 and 213=2*102+9.

## A five-move orientation reversal

At n=7 the following admissible closed walk has transport bits (1,1,1,0,0), whose sign product is -1:

    (0,1,2,3,5,4,6)
    (0,4,5,3,2,1,6)
    (0,4,6,1,2,3,5)
    (0,3,2,1,6,4,5)
    (0,3,2,1,5,4,6)
    (0,1,2,3,5,4,6)

The endpoint is the same undirected cycle. Following the moves on oriented tours reaches the opposite direction of the starting tour. An independent implementation verifies actual moves along the whole lifted walk, rather than merely multiplying supplied signs. Results.json also includes a ten-move negative walk at n=9.

The original six-state carrier of Revisit 01 is flat for this lift. It therefore remains a useful negative control; changing the example is explicitly reported, not hidden as a replacement success on the original carrier.

## A parity boundary at seven vertices

Let epsilon(c) denote the permutation sign of the canonical representative. For any odd n, rotating a tuple has even permutation sign. LR2 and LR3 are both single transpositions and hence odd. Reflecting an anchored tuple has sign (-1)^((n-1)/2).

For n congruent to 3 modulo 4, reflection is odd. Therefore an event with orientation sign s_e satisfies

    s_(c,d) = -epsilon(c)epsilon(d).

Along every k-step path this telescopes to

    s_path = (-1)^k epsilon(start)epsilon(end).

Consequently, two paths with the same start, endpoint AND step count cannot have opposite signs in this lift at n=7. Negative odd closed walks can still occur. Comparing a five-step loop to a zero-step history does not demonstrate cancellation at a common clock time. This explains why the n=7 exact calculations show no overlapping orientation channels at a fixed step count.

At n=9 reflection is even. This particular parity argument instead forces opposite permutation parity across each base edge, without fixing orientation transport. It does not exclude opposite orientation histories of equal length.

## Equal-length history test at nine vertices

Start from (0,1,2,3,5,4,7,6,8), with orientation chosen as written. Evolve the classical accepted-event process while tracking orientation. At five steps, four undirected endpoints receive positive probability from BOTH orientations. For one such endpoint,

    c = (0,3,2,1,8,6,7,4,5),
    P_plus(c)  = 299/20000,
    P_minus(c) = 1/1200.

Hence

    carrier occupancy = P_plus + P_minus = 947/60000,
    signed difference = P_plus - P_minus = 847/60000.

The independent verifier reconstructs two explicit five-step oriented histories to this same undirected endpoint, ending in opposite directions. They are retained in verification.json. Each branch has positive probability. The reduced signed difference exhibits partial cancellation; the endpoint occupancy does not.

No exactly zero signed difference with positive occupancy occurred in the saved seed calculations through 12 steps. The result is not presented as perfect destructive cancellation.

## Exact classical explanation

Write P_t(x,+),P_t(x,-) for probabilities on the two oriented tours above carrier x. Define

    p_t(x)=P_t(x,+)+P_t(x,-),
    z_t(x)=P_t(x,+)-P_t(x,-).

An event e:x->y transports orientation with sign s_e and has probability w_e. Then exactly

    p_(t+1)(y) = sum_(e:x->y) w_e p_t(x),
    z_(t+1)(y) = sum_(e:x->y) w_e s_e z_t(x).

The signed update is closed and contains minus signs, but is simply the antisymmetric part of a nonnegative classical process on the doubled state space. Conversely,

    P_t(x,+)=(p_t(x)+z_t(x))/2,
    P_t(x,-)=(p_t(x)-z_t(x))/2.

In particular |z_t(x)|<=p_t(x). A sign-dependent expectation can cancel even while both populations are present. Replacing the positive occupancy by |z|^2 as a detection probability would add a new rule requiring justification.

The signed square norm is not conserved. In the selected n=9 run, sum_x z_0(x)^2=1 and sum_x z_1(x)^2=1/5. At step five it is 57790069583/1215000000000. Thus this evolution has not produced unitary amplitude dynamics. Its exact classical representation already explains every result tested here.

## What is worth retaining

The useful advance is an explicit sign transport tied to actual move histories and closed-loop structure. It improves on freely painting phases onto edges by fixing a reproducible geometric rule. It also supplies immediate controls: the original flat carrier, the n=7 parity restriction, and the exact oriented classical lift.

The next question is operational access: can any retained carrier/probe interaction distinguish the transported orientation histories when their undirected carrier state agrees? Under the original state definition every instantaneous edge-set or neighbour-type readout is identical for the two orientations. They therefore cannot reveal the sign without an additional represented variable or interaction. A detector cannot be declared sensitive to a coordinate that the state definition quotients away.

A worthwhile next probe would represent that extra carrier/reference within the allowed relational construction, test its dynamics and backreaction, and then compare all readouts with the explicit classical lift above. Finding only a classical history record would still be a meaningful negative result for this proposed route to QM. A successful quantum bridge must additionally explain coherent recombination, the probability rule and its range of validity.

## Reproduction and independent verification

Run:

    python3 probe.py
    python3 verify.py

Only the Python standard library is required. Probe.py enumerates the two representative state spaces, transports actual reversals, solves the sign constraints, constructs negative closed walks, explicitly explores the double cover, and propagates exact rational probabilities for steps 0 through 12. Verify.py does not import probe.py: it constructs oriented tours directly, uses endpoint swaps for LR2/LR3, checks MICRO through undirected neighbour edge sets, checks reverse multiplicities and oriented components, follows the negative loops on actual tours, and independently reproduces every saved rational signed norm and example probability.

All checks passed. The finite checks establish the stated finite-model results. No full review of earlier EHF holonomy work or external novelty assessment was performed. No physical experiment, repository update or researcher contact occurred.
