# EHF-CBB-CROSS-55 — Symmetric reversal hopping and the Bell threshold

**Date** 2026-11-14 (Australia/Brisbane)  
**Status** Conditional Hamiltonian model, analytic Bell curve, matched stochastic control.

## A symmetric rule from each reversal matching

Use the indexed labelled cycles and local schedule of [CROSS-54](CROSS-54-local-bell.md). At a fixed window, legal LR3 attempts pair configurations into disjoint two-state edges. Assume a linear Hilbert-space model and a Hermitian local generator. On each eligible edge, require real matrix entries and invariance under exchanging the two endpoints. The resulting block is aI+bX, where X exchanges the two words. We choose a=0 and the same positive coupling b=1 across eligible pairs and windows, and zero on ineligible states. The bare graph gives the matching and the exchange symmetry. It leaves the diagonal energies and couplings unspecified, including their relation to ineligible states. Those diagonals can matter for relative phases when the evolution includes other blocks.

With the supplied Schrödinger evolution, a dimensionless pulse of angle t on an eligible pair is cos(t)I-i sin(t)X. On an ineligible word it is the identity. No orientation of a word or of its reverse is needed to sign the two off-diagonal entries. A corresponding classical kernel stays or jumps with probabilities cos²(t) and sin²(t), exactly matching the quantum pulse on any one basis input. This is a local instance of the distinction between a graph-supported Hamiltonian walk and a stochastic walk. See [Farhi and Gutmann, Quantum Computation and Decision Trees](https://arxiv.org/abs/quant-ph/9706062), especially section II.

## Preparation phase from the local schedule

Use pi/2 pulses for the transport schedule, a variable pulse t on the selected window, and a pi/2 relay pulse. Undo transport with inverse pulses in reverse order. Every successful full pulse contributes -i, and every ineligible attempt contributes one. After the variable pulse, the relay fires only on its moved branch. The two branches along the transport schedule from their respective output endpoints have k+2 successful reversals each on the 22+4k vertex preparation. Inverse transport removes their transport phases. The moved branch keeps two factors of -i, one from the variable pulse and one from the relay. The final state is cos(t)|00> - sin(t)|11>. The sign therefore follows from the chosen symmetric generator and the legal schedule, without a separate phase gate.

The return can also use positive pi/2 pulses throughout. This changes the prepared state by the common sign (-1)^(k+2) and has no effect on any outcome. Both versions were checked with all vertex labels retained for the 21 tested preparations. The classical kernel gives the same two final basis-state weights, without the off-diagonal terms. The preparation uses transport before either setting is selected.

## CHSH as a function of the mixing pulse

Use the same pulse primitive on the two disjoint readout windows. Alice uses angles 0 and pi/4. Bob uses angles b and -b. Reading the window after the pulse is equivalent to the qubit observable cos(2b)Z+sin(2b)Y at angle b, with the analogous expression for Alice. The state has ZZ correlation one and YY correlation sin(2t), with the crossed ZY and YZ terms zero. For 0<=t<=pi/2 the signed CHSH combination is

    S(t,b) = 2[cos(2b) + sin(2t) sin(2b)].

Fix Bob at the previous settings b=pi/8. Then S=sqrt(2)[1+sin(2t)] and violation requires sin(2t)>sqrt(2)-1. For t increasing from zero to pi/4, the threshold is t=arcsin(sqrt(2)-1)/2, at a single-pulse jump probability (1-sqrt(2sqrt(2)-2))/2, about 4.49%. The symmetric upper threshold on pi/4 through pi/2 is obtained by replacing t with pi/2-t. Retuning Bob to b=atan(sin(2t))/2 gives S=2sqrt(1+sin²(2t)), which exceeds two for every interior t. This is the optimal value within the tested one-parameter Bob family. Local marginals at partial mixing need not be unbiased, and disjoint measurement supports ensure no setting-dependent remote marginal under this model.

| Preparation pulse t | Fixed CHSH | Retuned CHSH |
|---|---:|---:|
| 0 | 1.414214 | 2.000000 |
| pi/24 | 1.780239 | 2.065902 |
| pi/12 | 2.121320 | 2.236068 |
| pi/8 | 2.414214 | 2.449490 |
| pi/4 | 2.828427 | 2.828427 |

The stochastic control uses the same probability for every individual pulse from a basis state, keeps both arms, and uses the same schedule. Its CHSH is 2cos(2b). For the fixed measurements it remains sqrt(2) at all mixing angles. This provides two descriptions on the same legal moves with the same isolated basis-state pulse probabilities and different correlations under composition.

## Scope and reproduction

Symmetry fixes the two-state generator's form within the stated real Hermitian ansatz. The off-diagonal strength, pulse duration, time evolution and squared-amplitude readout are supplied. Neither coherent evolution nor a privileged rotation angle follows from the comparison relation. The exact phase count and Bell curve identify what those assumptions yield on the existing carrier.

Run `python3 research/cbb-binary/cross55_symmetric_hopping.py` from the repository root. The verifier compares both return schedules, tracks labelled branches, checks the pulse sweep against the analytic formula and repeats the balanced case at 21 cycle sizes from 22 through 102 vertices. AI assistance was used for design, implementation and verification.
