# EHF-RW-001 — retained results

**COMPUTATIONAL:** exhaustive finite enumeration, 30 October 2026. See [probe.py](probe.py) and [results.json](results.json) for definitions, all rows, component-size histograms and witnesses. A component is a maximal group of states mutually reachable under the declared rule.

## Path controls

| Host | N | Hamiltonian paths modulo reversal | Components |
| --- | --- | --- | --- |
| Complete K_N | 4, 5, 6, 7, 8 | 12, 60, 360, 2520, 20160 | 1 at each size |
| Squared path P_N² | 4, 5, 6, 7, 8 | 6, 10, 17, 28, 44 | 1 at each size |
| Clique plus two leaves | 6, 7, 8 | 2, 6, 24 | 2, 6, 24; every path frozen |
| Paper's A_1(H_2) | 8 | 4 | 2, each of size 2 |
| Paper's A_2(H_2) | 10 | 24 | 2, each of size 12 |

The first two controls agree with the paper's squared-path theorem in the tested range. The two lifts reproduce its section-7 preserved internal path and disconnection. These are finite checks, not an independent proof of its general theorem. The clique-plus-leaves control retains the clique edge between the attachment vertices, unlike H_t in the paper; this extra edge cannot occur in a spanning path with both leaves as endpoints.

## Single-cycle controls

| N | Tours modulo rotation/reflection | LR3 components | Size of each LR3 component |
| --- | --- | --- | --- |
| 4 | 3 | 3 | 1 |
| 5 | 12 | 1 | 12 |
| 6 | 60 | 10 | 6 |
| 7 | 360 | 1 | 360 |
| 8 | 2520 | 35 | 72 |

LR2, LR23 and unrestricted 2opt each give one component at every tested size. The odd/even LR3 distinction agrees with the alternating-slot argument given in the main note.

## Constrained triads

Cycle labels and vertex labels are retained in the main count. Duplicate component cycles are allowed when they satisfy no triple-used edge. The last column forgets cycle labels but retains vertex labels; quotient state counts need not equal labelled counts divided by six because some states have stabilizers.

| N | Rule | Valid labelled triads | Components | Frozen labelled states | Components after forgetting cycle labels |
| --- | --- | --- | --- | --- | --- |
| 4 | LR2 | 6 | 6 | 6 | 1 |
| 4 | LR3 | 6 | 6 | 6 | 1 |
| 4 | LR23 | 6 | 6 | 6 | 1 |
| 4 | 2opt | 6 | 6 | 6 | 1 |
| 5 | LR2 | 516 | 1 | 0 | 1 |
| 5 | LR3 | 516 | 1 | 0 | 1 |
| 5 | LR23 | 516 | 1 | 0 | 1 |
| 5 | 2opt | 516 | 1 | 0 | 1 |
| 6 | LR2 | 80,940 | 1 | 0 | 1 |
| 6 | LR3 | 80,940 | 1,110 | 120 | 230 |
| 6 | LR23 | 80,940 | 1 | 0 | 1 |
| 6 | 2opt | 80,940 | 1 | 0 | 1 |

For N=6, LR3 component sizes are:

| Component size | Number of components |
| --- | --- |
| 1 | 120 |
| 42 | 270 |
| 96 | 360 |
| 97 | 360 |

The weighted total is 80,940. The triads realize 1,000 ordered alternating-partition signatures, while there are 1,110 components. Since that signature is invariant under LR3, at least one fixed-signature class is itself disconnected: the three single-cycle invariants do not completely explain the constrained triad fragmentation. There are 110 components beyond the one-per-signature lower bound. Forgetting cycle labels leaves 230 components, of which 20 are single states; the obstruction therefore cannot be removed merely by relabelling the three cycles.

N=4 is a useful exception to any general claim that adjacent swaps always connect constrained triads. Its six isolated labelled states describe different labellings of one unordered triad. N=5 and 6 connectivity must not be extrapolated into a general theorem.

## What changes in our interpretation

**Supported:** the paper's reconfiguration viewpoint is useful for EHF. A proposed memory experiment should first report reachable components and invariants under its actual moves. In the declared LR3 triad model, persistent distinctions can be exact restrictions on reachability, even with no energy landscape or slow stochastic process.

**Not established:** novel mathematical priority, long mixing times, recoverable records, emergent quantum memory, physical conserved charges, particles or dimensional selection. Some sector distinctions may be invisible to a chosen coarse observer, so the next experiment must specify both dynamics and observables.

**Next hypothesis:** a small positive LR2 proposal rate may erase the LR3 sector restrictions for N=5 and 6, while leaving long finite-time persistence. Test sector residence times and within-sector relaxation separately with a stated proposal kernel. General-N connectivity, geometric locality, and growth across changing state spaces remain separate questions.
