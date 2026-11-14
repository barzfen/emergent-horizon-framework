# EHF-CBB-CROSS-53 — Local phase readout and joint correlations

**Date** 2026-11-14 (Australia/Brisbane)  
**Status** Exact reduced-state checks for a specified quantum control, with a classical parity model and a supplied CHSH benchmark.

## Use the same region for both models

Take the buffered indexed labelled cycles of [CROSS-52](CROSS-52-setting-isolation.md). Let A contain the vertices incident to the three observed sign windows P, Q and R. Let the remaining vertex positions be B. The remote M reversal has support entirely in B. Work in a supplied position-register Hilbert space with orthogonal basis vectors for different vertex labels. Assign each label its original colour. Every sign read by A is determined by the labels in A.

Write |rm> for the tour basis states produced by the two disjoint reversals R and M, with P and Q initially unset. Thus |rm> factorizes across the A/B cut on this four-state subspace, although coherent superpositions need not factorize. A remote operation is local here if it acts on B and any private apparatus, and any later intervention must obey the same region and schedule restrictions. There is no postselection on private outcomes.

A B-only trace-preserving operation cannot change the immediate reduced state on A. Equivalently a B-only unitary commutes with every A-only measurement operator. The same conclusion holds after later gates if the backward causal cone of the measurement misses the setting operation. See [Beckman, Gottesman, Nielsen and Preskill, Causal and localizable quantum operations](https://preskill.caltech.edu/pubs/preskill-2001-causal.pdf), especially sections I and II. The CROSS-52 shortest-leak times concern a particular classical update rule. They are not assumed to give causal-cone bounds for arbitrary quantum gates.

## Exact coherent extension of the common attempts

Supply one particular coherent extension. An attempted LR3 permutes the full labelled-tour basis, doing nothing on an ineligible word and reversing an eligible one. The rule is an involution because the reversed window is again eligible for its inverse. Use its unsigned linear extension as a unitary. This uses the same read/write window and eligibility rule as the classical attempts. It deliberately supplies no new Clifford phase at an attempt.

Compare the superpositions (|00>+|10>)/sqrt(2) and (|01>+|11>)/sqrt(2), related by the remote M reversal. For each common sequence of attempts, evolve all four basis histories together. To obtain the reduced density matrix on A, retain the two local diagonal contributions and retain their off-diagonal terms only if the two outside label words are identical. The verifier uses integer numerators with denominator two.

Also test a remote phase setting on the supplied entangled input (|00>+|11>)/sqrt(2). A diagonal Z on M changes the relative sign. Compare the reduced states for the two signs after every common attempt sequence within each bound.

| Vertices | Common attempts checked through | Distinct joint histories by endpoint tuple |
|---|---:|---:|
| 22 | 0 | 1 |
| 26 | 2 | 46 |
| 30 | 3 | 272 |
| 34 | 4 | 1,360 |
| 38 | 5 | 6,784 |
| 42 | 6 | 30,048 |

The reduced states agree across settings in both tests throughout these windows. In the 34-vertex flag test the fifth attempt along 12, 15, 12, 10, 8 gives different reduced states. This is an explicit example of ordinary local propagation. The equality inside the windows is a finite result for the supplied unsigned unitary, not a universal claim about all allowed coherent dynamics.

## Where the phase can be read

Without a transport stage, the relative sign in (|00> +/- |11>)/sqrt(2) has no effect on A alone. Apply a supplied Hadamard on each of the two disjoint reversal bits and measure each in its basis. The verifier checks that the underlying R and M flips are legal moves on the 34-vertex carrier. Hadamard uses a coherent linear combination of a flip and a diagonal operation. It is a supplied local gate.

| Remote phase | A alone | B alone | Joint outcomes after comparing records |
|---|---|---|---|
| Plus | Fair bit | Fair bit | 00 or 11, equally likely |
| Minus | Fair bit | Fair bit | 01 or 10, equally likely |

These particular parity tables have an exact classical model. The readers share a fair bit before the setting, and B XORs its setting into its reported bit. Comparing records gives the parity. This compares a single phase setting and readout family.

For a stronger supplied benchmark, prepare the plus state before the settings. Give A two observables Z and X, and B two observables (Z+X)/sqrt(2) and (Z-X)/sqrt(2). Here X exchanges the two reversal configurations and Z changes their relative sign. The verifier computes correlations (1,1,1,-1)/sqrt(2), so CHSH is 2sqrt(2), with unbiased local outcomes. See [Brunner et al., Bell nonlocality](https://arxiv.org/abs/1303.2849), sections II and III. This is a Bell-pair calculation in a supplied model. The coherent shared preparation, local basis rotations and measurement rule have not been obtained from admissible comparisons.

## Relation to CROSS-51

The 100% versus 0% arrival comparison in CROSS-51 changes one recombiner's marginal. If the setting is chosen remotely and its influence cannot reach that recombiner, ordinary local quantum operations cannot implement that comparison in the certified window. The earlier classical 25-percentage-point obstruction is conditional on the original one-reader targets and the classical restriction. It does not by itself establish a quantum advantage under jointly matched locality. Either transport the effect to the recombiner within an allowed schedule or use joint correlations from separated outcomes. In the latter case, the research problem is to construct the shared preparation and two incompatible local measurements operationally, rather than supply them algebraically.

Run `python3 research/cbb-binary/cross53_local_phase.py` from the repository root. AI assistance was used in design, implementation and interpretation.
