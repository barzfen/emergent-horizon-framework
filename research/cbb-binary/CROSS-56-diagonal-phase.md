# EHF-CBB-CROSS-56 — Identical reversal probabilities can hide different phases

**Date** 2026-11-14 (Australia/Brisbane)  
**Status** Analytic phase and Bell curves, checked on 21 indexed labelled carriers.

## Two generators on the same admissible moves

For each attempted LR3 window, the configuration graph is a matching with isolated vertices. Let A be its adjacency matrix and D its degree matrix. D is one on eligible states and zero on isolated states. Compare H(a)=A+aD with off-diagonal coupling one, supplied Schrödinger evolution, and supplied squared-amplitude probabilities. The CROSS-55 adjacency generator has a=0. With a=-1 the generator is the negative graph Laplacian A-D.

On an eligible pair, a pulse of angle t is exp(-iat)[cos(t)I-i sin(t)X]. On an isolated state it is the identity. Thus for every basis-state input and pulse angle, all choices of a give identical stay and reversal probabilities. Within an eligible pair the extra factor is common. In a superposition of an eligible state and an isolated state, it is relative and may become observable at recombination. For background on adjacency and Laplacian quantum walks, see [Wong and Lockhart, 2021](https://doi.org/10.1103/PhysRevA.104.042221).

## Bell preparation and fixed settings

Use the pulse and transport schedule of [CROSS-55](CROSS-55-symmetric-hopping.md). The two forward transport witnesses use k+2 successful attempts each. Inverse transport cancels those phases. A positive-pulse return also gives the same relative phase because the successful transport counts agree. The mixing pulse acts on a common eligible pair. The relay acts on the moved arm only, contributing -i exp(-ia pi/2) for a pi/2 pulse. Including the first move's factor -i, the state after transport is, up to a global phase,

    cos(t)|00> - exp(-ia pi/2) sin(t)|11>.

Both readout windows are eligible throughout the four-state output cube. Thus the a term contributes only global phases during the local readout rotations. The CROSS-55 readouts measure Z and Y on one side and (Z+Y)/sqrt(2) and (Z-Y)/sqrt(2) on the other. The state has ZZ=1, YY=sin(2t)cos(a pi/2), and zero crossed ZY and YZ correlations. The fixed-setting CHSH score for 0<=t<=pi/2 is

    S(t,a) = sqrt(2)[1+sin(2t)cos(a pi/2)].

| Balanced preparation | Adjacency, a=0 | Negative Laplacian, a=-1 |
|---|---:|---:|
| Basis probabilities on 00 and 11 | 1/2 each | 1/2 each |
| Relative amplitude of 11 to 00 | -1 | -i |
| Fixed-setting CHSH | 2sqrt(2) | sqrt(2) |
| Return probability with common inverse adjacency preparation | 1 | 1/2 |

The negative-Laplacian output still has equal Schmidt coefficients. The change in the fixed measurement result comes from the measured phase quadrature. The phase difference is removable by a local diagonal phase rotation if that extra control is available. This comparison holds the readout protocol fixed and does not exclude Bell violation with other operations.

## A shorter phase-sensitive echo

For an independent test use a common adjacency reference mixer and transport, and change only the two intervening relay pulses:

1. Transport and apply a pi/4 adjacency mixer, as in CROSS-55.
2. Apply two positive pi/2 pulses at the relay window. Use H(a) for both.
3. Undo the adjacency mixer and transport, with no measurement between the pulses.

On the active arm the relay is an involution at the level of labelled tours. After two full pulses the original labelled configurations and their basis weights are restored, but the active arm gains -exp(-ia pi). The idle arm is ineligible and remains fixed. The common inverse mixer returns to the seed with probability (1-cos(a pi))/2. Adjacency therefore gives zero return and the negative Laplacian gives certain return. The inverse operations use an explicitly supplied adjacency phase reference in both runs. Running each model's own inverse of the entire circuit would instead return to the seed in both runs.

## What is fixed

This is a direct ambiguity within coherent, symmetric local evolution on the same graph. Specifying all admissible reversals and their isolated basis-state pulse probabilities leaves the eligible-versus-idle energy difference open. The echo shows how to measure it with a supplied phase reference. For a derivation from admissible comparisons, a further principle would have to fix that difference or independently define an observable that selects a phase convention. The experiment does not select either generator as the physical law.

Run `python3 research/cbb-binary/cross56_diagonal_phase.py` from the repository root. The verifier checks basis probabilities for both generators at several angles, propagates the labelled states with both return schedules, and compares the Bell and echo formulas across 21 carriers from 22 to 102 vertices. AI assistance was used for construction, verification and writing.
