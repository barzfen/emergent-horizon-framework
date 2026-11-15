# EHF-CBB-CROSS-58 — Growth phases and the stationary reference

**Date** 2026-11-15 (Australia/Brisbane)  
**Status** Exact phase equivalence and a one-insertion stationarity obstruction, with finite labelled checks.

## Same insertion probabilities, two coherent conventions

Use indexed oriented cycles with distinct labels 0 through n-1. The index seam stays fixed during the pulse. A legal colour-changing LR3 is a transposition of two labels, with degree one on eligible configurations and zero on idle configurations. For a selected window write its generator as H(a)=A+aD, using the supplied quantum model of [CROSS-56](CROSS-56-diagonal-phase.md).

Let J multiply each basis coefficient by the parity of its indexed label permutation and let K conjugate all coefficients. Since every edge flips parity, JAJ=-A and JDJ=D. The antiunitary map T=JK therefore satisfies

    T exp(-it H(a)) T^(-1) = exp(-it H(-a)).

This statement includes each idle configuration and preserves the physical pulse time t. The conjugation of i is essential to the identity.

Let G+ be the normalized all-slot growth map with equal positive amplitude. Inserting the newest and largest label after zero-based position s changes the permutation parity by (-1)^(n-1-s). Consequently Galt=T_(n+1) G+ T_n^(-1) is the alternating-sign growth map:

    Galt |u> = (1/sqrt(n)) sum_s (-1)^(n-1-s) |insert_s(u)>.

Both maps give probability 1/n at every insertion slot from a single labelled parent. Every pulse-and-growth protocol in the paired models (G+, H(a)) and (Galt, H(-a)) has identical final basis probabilities for basis preparations. The state vectors are related by T throughout. Any extra coherent preparation or measurement must also be transformed for this equivalence. In particular, the stationary symmetric reference of the negative Laplacian becomes the stationary antisymmetric reference of the signless Laplacian. A comparison that calibrates the reference in both models with one fixed phase convention can distinguish them.

The same conclusion does not follow for an arbitrary quotient that reroots the word after each move. This statement uses the indexed convention, in which permutation parity flips at every LR3.

## A coherent return with one fixed growth reference

Use the two parent configurations and only the child edges lifting their chosen reversal, as in [CROSS-57](CROSS-57-growth-phase.md). Prepare the symmetric parent reference and grow it with G+ in both runs. Apply a child pulse of duration pi/2, then test whether it remains in the original coherent growth subspace. This test supplies a projection onto the two uniform fibres, equivalently the success outcome of a coherent inverse-growth analyzer on that subspace.

The fraction f=(n-4)/n of the grown reference lies on matched edges, and the rest lies on isolates. For a=-1 the matched symmetric mode and isolates both retain phase +1. For a=+1 the matched mode gains -1 and the isolates retain +1. The successful return amplitudes are 1 and 1-2f, and the probabilities are 1 and (1-2f)^2. On the 22-vertex parent they are 1 and 49/121. This provides a phase-sensitive comparison with one fixed analyzer. The analyzer is a supplied coherent comparison across slots, rather than ordinary deletion followed by a basis read.

## Growth of a single three-colour cycle cannot be stationary for all LR3 pulses

Now retain the full set of proper indexed child cycles, with no restriction to lifts of one chosen parent move. Let the starting parent be a proper cycle of length n>=5 that uses all three colours. Its all-slot grown vector, with a nonzero coefficient on every child, fails to be stationary under at least one fixed-window LR3 generator, for any diagonal energy and any choice of insertion phases.

The local reason is that at least one insertion enables a colour-changing reversal that leads outside the original parent's deletion fibre:

- If every consecutive triple is rainbow, the colours follow ABCABC, with A, B and C distinct. An A B C A segment becomes A B A C A after inserting between B and C. Reversal gives A C A B A. Deleting the inserted A leaves the old labels in a different cyclic order.
- Otherwise the cyclic word has both an alternating triple and a rainbow triple. If all triples were alternating, the cycle would use two colours only. At a transition from an alternating triple to a rainbow triple the word contains A B A C. The next vertex has colour A or B. In the first case A B A C A already permits a reversal. Insert outside its four supporting gaps and perform that reversal, whose projection changes the old tour. In the second case insert A between C and B, creating the needed five-vertex window. Reversing again changes the old cyclic label order.

A fixed-window Hamiltonian has a matching as its off-diagonal graph. The new configuration outside the fibre therefore receives amplitude from exactly one child in the fibre. Slot phases cannot cause cancellation there, and diagonal entries cannot contribute to it. The result also applies to a grown vector with unequal nonzero amplitudes on all slots. At a full pulse, the exhibited outside configuration gets probability 1/n under either equal-magnitude growth convention.

The only proper parents excluded by the use of three colours are the alternating two-colour cycles. In their children the new third colour occurs exactly once, and its two neighbours have distinct colours. This vertex cannot be one of the exchanged labels, which have same-colour neighbours, or one of the three same-colour positions of the A B A C A template. Every child is therefore frozen under colour-changing LR3. Label exchanges between identical colours are outside this pulse model.

The exact labelled check finds a reversal out of the fibre on 156 of the 160 proper words with first colour zero at sizes 5–8. The other four words are the alternating two-colour controls. The obstruction concerns stationarity under every individual reversal window and the growth of one basis cycle. It leaves room for reference states spread across several parent fibres or for a collective generator with different assumptions.

## Reproduction

Run `python3 research/cbb-binary/cross58_growth_reference.py` from the repository root. The standalone verifier compares full complex states across interleaved growth and reversal pulses, evaluates the reference-return formula and scans the small labelled examples. AI assistance was used in deriving and checking the probe.
