# Entropy and Symmetry in Constrained Cyclic Growth — v0.1

19 October 2026. Working draft for review, not a journal submission or a claim of priority.

- [Readable manuscript (PDF)](entropy-and-symmetry-v0.1.pdf)
- [Editable manuscript](manuscript.md)
- [Literature comparison and remaining work](LITERATURE-COMPARISON.md)
- [WHEELER-63 bounded extension](../../../probes/wheeler/WHEELER-63.md)
- [Reproduction instructions](../../../code/wheeler/README.md)

## Plain-language account

Imagine a ring of black and white beads. No bead may be alone between two beads of the other colour. We grow the ring by choosing uniformly among the permitted insertion events. Long blocks have more opportunities to grow.

If we remember where the ring starts, uncertainty grows. If we treat rotated copies as the same ring, symmetry changes the accounting: uncertainty can briefly fall, even when we begin with one definite ring and discard no outcomes. We give an exact example. But for the smallest ring with four blocks of two beads each, we prove uncertainty increases at every step.

The mathematical interest is the contrast between that theorem and the counterexample, and the exact symmetry correction explaining both. The physics relevance is a caution about how entropy depends on what an observer distinguishes. This is not yet a derivation of thermodynamics or a physical arrow of time.

## What is ready, and what remains

The paper contains definitions, proofs, rational endpoint distributions, entropy-sign certificates and reproducible code. The D=6,8,10 extension gives positive increments over finite tested ranges, not an all-time theorem. Established urn theory and entropy asymptotics are credited explicitly.

Before journal submission or a priority claim:

1. Obtain Nakata's full 2009 paper and compare its classification, definitions and results directly.
2. Have an external mathematician check the rooted insertion convention and column bound, quotient closure, both counterexamples, and the all-time four-run proof, including the exceptional early steps.
3. Check whether the exact model-specific results already occur elsewhere; this focused comparison is not an exhaustive novelty search.
4. Confirm authorship, acknowledgements, AI disclosure and target venue requirements with the author.

No external reviewer has been contacted, and no independent external review has been completed. Code reconstructions and symbolic certificates are internal verification.

## Build

From the repository root, with Pandoc and a LaTeX installation:

```sh
pandoc research/wheeler/paper-v0.1/manuscript.md --standalone --pdf-engine=pdflatex -o research/wheeler/paper-v0.1/entropy-and-symmetry-v0.1.pdf
```

The manuscript maps WHEELER-59 to Sections 3–4, WHEELER-60 to Section 5.1, WHEELER-61 to Sections 5.2–6, WHEELER-62 to Section 7, and WHEELER-63 to Section 8. The earlier series contains other topics outside this paper's scope.
