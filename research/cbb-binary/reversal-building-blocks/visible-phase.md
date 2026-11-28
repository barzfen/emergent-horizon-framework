# A visible phase from overlapping reversals and deterministic growth

**Date** 18 November 2026, Australia/Brisbane  
**Status** Exact construction and period law, with finite checks.  
**Scope** This follows the [fixed-window reversal audit](README.md) using the [three-colour rule](../GROWTH-CLOCKS-AND-BELL.md). Colours travel with vertices and neighbours must differ.

## Setup and visible shift

Write an active block as `Ax1 Ax2 ... Axk`, where each $x_j$ is B or C. Complete the cyclic word with the exterior `ACBCABC` immediately after the block. Its first A is the right flank and its final C is the left flank. We choose this exterior and keep it fixed. The observer reads colour equality and cyclic adjacency on the whole ring.

Let $T_k$ reverse the first $2k-1$ slots of the active block, then its last $2k-1$ slots. These windows overlap by $2k-2$ slots. Their position permutations compose to shift the block right by two slots, so $T_k$ shifts the cells `Ax` by one. Each individual reversal is admissible. It preserves slot parity, so A remains in every even slot and B or C in each odd slot using zero-based indexing. The unchanged flanks still meet A on the left and B or C on the right. A single reversal can preserve the colour readout; legality does not require a colour change.

The shift is visible on the ring. If there are $b$ B entries and $c$ C entries in the active cells, the counts of unordered adjacent colour pairs are

| Pair | Count |
| --- | --- |
| AB | $2b+1$ |
| AC | $2c+3$ |
| BC | $3$ |

For $b,c\ge 2$, BC is uniquely least frequent. This identifies A from the equality pattern. The runs of non-A colours have length one in the active block and lengths three and two in the exterior. The direction from the unique length-three run to the length-two run across a single A determines the reading orientation. The same two runs determine the seam and identify B and C by their positions in the length-two run. Thus re-rooting, reflecting, and renaming the colours of the entire word preserve the decoded cell word. The exterior supplies a physical pattern within the model and the observer recovers it from colours.

Starting with `BCCB`, the decoded orbit is `BCCB → BBCC → CBBC → CCBB → BCCB`. These are four distinct observable patterns. On the real plane of opposite-pattern contrasts, with basis $e_0-e_2$ and $e_1-e_3$ for the four successive readings, $T_4$ sends the first basis vector to the second and the second to the negative of the first. The induced operator $J$ satisfies $J^2=-I$. This plane consists of real scoring vectors indexed by colour patterns.

## A legal growth rule preserves phase and doubles the period

At each gap from an $x_j$ to the following A, including the right flank A, insert the unique third colour $\bar{x}_j$. Next insert A into the gap between $x_j$ and $\bar{x}_j$. Both operations follow the usual third-colour insertion rule. They replace the local string $x_j A$ by $x_j A\bar{x}_j A$. Processing all original cell gaps gives the cell-word substitution $G$.

| Cell colour | Cell colours after growth |
| --- | --- |
| B | BC |
| C | CB |

This is the established Thue–Morse morphism. The construction here realizes it using the cycle growth rule at specified gaps and couples it to the two overlapping reversal windows. [Jean-Paul Allouche and Jeffrey Shallit, *Automatic Sequences* (2003), Example 1.4.2](https://assets.cambridge.org/97805218/23326/excerpt/9780521823326_excerpt.pdf).

Each old cell is replaced by a pair, so a shift by one old cell becomes a shift by two new cells,

$$
G T_k = T_{2k}^{\,2} G.
$$

To see that there is genuinely twice as much resolution, consider the least cyclic period of the new cell word. It cannot be odd. The new word has complementary symbols in pairs starting at each even index. An odd shift preserving the word would force the same property on the odd indices, so the whole word would alternate, which has no odd period. A period of $2d$ is equivalent to the original word having period $d$, by reading the first symbol of each pair. Therefore growth doubles the least cyclic period exactly. The seed `BCCB` is balanced and has period four. Subsequent words remain balanced and have periods $8,16,32,\ldots$.

At the observable group level, growth sends a phase step $j$ on the $k$-cycle to step $2j$ on the $2k$-cycle. Measuring shortest shift distances as fractions of a full turn gives isometric embeddings. The union of these phase groups is the dyadic fractions modulo one, and its metric completion is $U(1)$. Each finite ring has a discrete phase group. The growth schedule provides the embeddings; the normalized metric is the specified scale for the completion.

## Reproduction and scope

Run `python3 research/cbb-binary/reversal-building-blocks/check_visible_phase.py` from the repository root. The verifier constructs growth through actual third-colour insertions and checks admissibility after every reversal and insertion. It checks the growth formula and period doubling on all 2,046 binary words of lengths 1–10. It follows complete observable reversal orbits at periods 4, 8, 16, 32, 64, 128 and 256. At periods 4, 8 and 16 it verifies the decoder across all changes of root, orientation and global colour names for all orbit states, for 10,416 presentations in total.

The active region, ordered sequence of reversal windows and growth schedule are specified by the construction. The exterior is engineered and the readout can inspect the whole ring. Reversal lengths increase with size. The result gives one observable phase direction and a coherent identification of that direction across scales. A model with several interacting directions would also have to recover a shared phase convention and compatible noncommuting comparisons. The construction uses real contrast vectors; interference and quantum detection rates would require a further observation rule.

*AI assistance covered the construction, proofs, finite verification and write-up. We inspected the cited source excerpt for identification of the Thue–Morse morphism.*
