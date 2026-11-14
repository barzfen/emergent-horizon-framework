# EHF-CBB-CROSS-39 — Equal-pair ancestry and exact LR3 escape depth

**Date** 2026-11-13 (Australia/Brisbane)  
**Status** Proved for the family below. Finite checks independently reconstruct the colour-reversal rules.

## Result

For the balanced proper three-colour cycle family
`F_t = A(BC)^(t+2)(AC)^(t+1)(AB)^(t+1)`, with integer `t >= 1`, the minimum number of legal nontrivial length-three reversals (LR3) needed to enable any legal nontrivial length-four reversal (LR4) is **exactly t**. The first possible triple of equal orientation signs occurs after exactly **t+1** LR3 moves. Paths may use any legal LR3 start, including cyclic wraparound.

The sharp lower bound answers the open question in [CROSS-34](CROSS-34-LR3-causal-ancestry.md) and [CROSS-38](CROSS-38-cyclic-dipole-and-transport.md). The upper bound uses the witness from [CROSS-36](CROSS-36-single-front-activation.md).

## Intrinsic pair markers

As in CROSS-34, write the oriented edge increments modulo three as signs. Define `d_j = 1` if signs `s_j, s_(j+1)` are equal and `d_j = 0` otherwise. Pair-marker positions are properties of the current sign word. Colour rotations leave them invariant and colour reflections flip all signs while preserving equality. Rotation or reversal of the cycle simply reindexes their positions. Distances below are cyclic graph distances.

An LR3 rewrite replaces `-++-` by `+--+` or the reverse. If its window starts at `p-1`, the central pair marker at `p` stays occupied, the adjacent markers at `p-1` and `p+1` stay empty, and the markers at `p-2` and `p+2` toggle. All other marker occupancies stay fixed. This follows because the four signs flip together. Only equality comparisons across the two boundaries change.

Every legal nontrivial LR4 window contains either an equal-sign triple or one of `++-++` and `--+--`, by the [fourteen-pattern catalogue](CROSS-28-frozen-automaton-scc-and-LR3-escape.md). In the first case there are occupied pair markers at distance one. In the second there are occupied pair markers at distance three.

## Lower bound by ancestry

Give each initial occupied pair marker a separate ancestry root. Whenever a move creates a marker at `p-2` or `p+2`, trace it to the occupied central marker at `p` just before the move. Retained markers keep their ancestry. In particular, ancestry does not require conservation of the number of markers or conservation of the sign of a pair.

For any pair of occupied markers after `k` moves, trace their chains back to the initial markers. Each parent-to-child link uses a move and displaces the marker by two positions. A move can appear in both chains only if they share a parent at that move, and then they have the same root.

- **Distinct roots.** The two chains use at most `k` moves in total. The cyclic distance between their endpoints is at least the distance between their roots minus `2k`, by the triangle inequality.
- **Same root.** Lift both chains to integer positions from the same starting coordinate, using signed displacements of two. Their lifted separation is even and at most `4k`, since each chain uses at most `k` moves.

The initial sign word is `(++(-+)^t-)^3`. Its three pair markers are at `0, 2t+3, 4t+6` on a ring of length `n=6t+9`. Distinct roots therefore have distance `2t+3`. For `k<t`, their descendants have distance at least five. In the same-root case for `k<=t`, the lifted separation is even and at most `4t<n-3`. It cannot represent cyclic distance one or three. This rules out every LR4 trigger before move `t`. For `k<=t`, distinct-root descendants have distance at least three, so the same argument also excludes equal-sign triples through move `t`.

## Upper bound and correction

Starting from the seed, the sign-window starts `2t+2, 2t, ..., 4` give the single-front construction from CROSS-36. Each rewrite turns `-++-` into `+--+`, which makes the window two positions to its left eligible while the alternating region remains. The final word begins `++-++--`, enabling LR4. One more LR3 at window start 2 produces the prefix `+++`. The lower bounds above therefore give the exact values `t` and `t+1`.

In particular, the global triple-freeness claim of [CROSS-35](CROSS-35-triple-free-LR3-invariant.md) is false. The shortest example from this family has `t=1`:

```text
++-+-++-+-++-+-    initial
++-++--++-++-+-    LR3 at sign-window start 4
+++--+-++-++-+-    LR3 at sign-window start 2
```

A triple may cross a rewrite boundary with **two unchanged signs and one changed sign**. The first-activation reduction in CROSS-35 remains valid for this family because the sharp ancestry bound excludes triples through first activation.

## Scope

This result gives an exact propagation constraint using markers read from the three-colour cycle itself. The two directions are relative to the cycle orientation and are interchanged by reflection. The move budget is a combinatorial resource. Proper time, physical signal propagation, and compatibility with all-slot growth remain open. In particular, a fixed-size LR3 rewrite and an insertion have different effects on the sign word and need a common event model before the result can be used to infer an observer clock.

## Reproduction

From the repository root run `python3 research/cbb-binary/cross39_equal_pair_ancestry.py`. The verifier derives local rewrite tables from actual colour reversals, checks the marker rule, independently enumerates shortest paths through `t=12`, and checks the constructive witnesses through `t=100`. The finite checks support the proof and use no external dependencies. AI assistance was used for derivation, implementation and verification.
