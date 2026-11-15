# EHF-CBB-CROSS-57 — Stationary reference and one-step growth of reversal pulses

[Series guide](GROWTH-CLOCKS-AND-BELL.md) · [Verifier](cross57_growth_phase.py)

**Date** 2026-11-15 (Australia/Brisbane)  
**Status** Analytic selection under an added reference axiom, exact one-step lift and leakage formulas, finite labelled checks.

## A stationary coherent reference selects the negative Laplacian

Use the generator H(a)=A+aD from [CROSS-56](CROSS-56-diagonal-phase.md), with coupling one and isolated states at energy zero. On each eligible pair, the normalized equal-phase state (|u>+|v>)/sqrt(2) has eigenvalue a+1. To compare its phase with an idle configuration, prepare a coherent reference with nonzero components on both that mode and the idle state. Requiring the reference ray to remain stationary at all pulse durations forces a+1=0. Thus the added requirement selects H(-1)=A-D.

The condition fixes a relative energy. A common scalar energy shift has no effect on it. Equally weighted classical probabilities impose a different condition: the basis-measured transition matrix of every H(a) is doubly stochastic, so each preserves a uniform probability law. Equal probabilities do not fix whether a coherent reference has aligned or opposite phases. For example, choosing the antisymmetric pair state with the idle reference instead selects a=+1. A rule specifying the physical reference is extra information. For the standard graph operators see [Godsil et al., Australasian Journal of Combinatorics 86 (2023), pp. 373–386](https://ajc.maths.uq.edu.au/pdf/86/ajc_v86_p373.pdf), section 1.

## A proper insertion preserves the chosen reversal in exactly n-4 slots

Fix an oriented labelled n-cycle, n>=5, and a colour-changing legal LR3 with endpoints u and v in the configuration graph. This means that its four signs are -++- or +--+, as in [CROSS-39](CROSS-39-equal-pair-ancestry.md). The moves used here change the colour pattern. Swapping two distinct labels of the same colour has a different survival count and is outside this pulse model.

Insert a new label in any of the n cyclic gaps and give it the unique third colour. Delete that label to project to the parent. Compare the two fibres of children that project to u and v. Retain child LR3 edges between those fibres. This is a comparison of lifts of one chosen parent reversal, with no other child move included in the Hamiltonian.

If the new vertex belongs to the reversed triple, deleting it projects the move to an adjacent old-label swap. The parent reversal swaps the two outer labels of a triple, which are nonadjacent. Hence a surviving lift must leave the new vertex outside its triple. An insertion into either internal gap would break the old triple. An insertion into either boundary gap keeps the triple consecutive but blocks the move by causing equal neighbouring colours in the proposed output. To see this, the five-vertex colour pattern can be written as A B A C A, up to naming colours. Insertion at the left boundary puts C next to B. After reversal that C would sit next to the moved C. The right boundary similarly puts B next to the moved B.

The other n-4 gaps remain unchanged by the reversal. At each of them, the child LR3 is admissible, its projection is the parent move, and the same new colour is used in both children. The lifted graph is a matching of n-4 edges with four isolates in each fibre. This coloured, LR3-only statement concerns the convention in this series. The earlier [HC-GROW working document](../source-documents/hc-grow-v0.8.md) studies support propagation with different move and growth conventions.

## Uniform all-slot growth cannot intertwine the entire pulse

Let G take a parent basis state to the normalized equal-amplitude sum of all n child configurations in its fibre. Both fibres have size n and are disjoint, so G is an isometry. Let H be the parent two-state generator, and H' the generator of the lifted matching and its isolates with the same a. Write f=(n-4)/n. Then the generator seen by projecting back to the uniform fibre is

    G* H' G = f H.

This is a compression, with possible amplitude outside the uniform fibre. On the normalized parent symmetric and antisymmetric modes, the norms of the leaked generator components (I-GG*)H'G are exactly

    sqrt(f(1-f)) |a+1| and sqrt(f(1-f)) |a-1|.

Indeed H' acts with the corresponding eigenvalue on the n-4 matched terms and zero on the other four. Subtracting the mean coefficient across the fibre gives the formula. These modes have orthogonal lifted leakage vectors when both are nonzero. Therefore the maximum instantaneous leakage over normalized parent inputs is sqrt(f(1-f))(1+|a|). It is minimized by adjacency, a=0, for this criterion. At a=-1 the symmetric reference survives exactly, while the antisymmetric mode leaks twice the adjacency worst-case amount. No a eliminates leakage on both modes. Rescaling the parent generator or changing its diagonal cannot remove that component outside the image of G.

For a finite pulse of angle t the leaked norm on each mode is sqrt(f(1-f)) times |exp(-it(a±1))-1|. The failure concerns intertwining at all durations. Special pulse durations may revive both components. The obstruction also disappears if the coherent growth rule includes equal matched weights and gives zero weight to all four affected gaps, but that is a different growth map.

## Echo check using each candidate's own reference

Use the two-relay echo of CROSS-56. On the active arm, two positive relay pulses restore the labelled state and multiply its amplitude by -exp(-ia pi). On the idle arm they do nothing. The return probability is (1-cos(a pi))/2. In this variant all pulses within a given run use the same candidate generator, and the mixer and transport are undone using their inverse pulses. Their own phase factors cancel. The relay pair uses two positive pulses and is the sole part left uncompensated. The verifier finds zero return for adjacency and certain return for the negative Laplacian on all 21 Bell carriers.

## Reproduction

Run `python3 research/cbb-binary/cross57_growth_phase.py` from the repository root. The verifier checks 148 eligible indexed reversals across all proper rooted colour words at sizes 5–8 with first colour fixed, including wraparound. It independently inserts into actual labelled tours and searches every child reversal for a lift. It repeats the count for the active relay at all 21 Bell-carrier sizes, checks the two generator leakage norms, and runs the same-generator echo. AI assistance was used in deriving and checking the probe.
