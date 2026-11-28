# EHF-DIM-07 — Elementary reversals yield a 6×6 toroidal grid

**Date:** 2026-11-19. **Status:** Exact exhaustive graph isomorphism verified for the n=7, 36-state OPW3 chamber.

## Result

The 36-state chamber is the Cartesian product C6 □ C6 of two six-cycles. This is a finite toroidal square grid (a graph), **not** a derivation of physical 2D spacetime.

Choose root canonical cycle `(0,1,4,2,5,3,6)`. Its nonzero even-position labels are E={4,5,6}, and odd-position labels O={1,2,3}. Independent permutations give a free transitive action of S3×S3 on the chamber.

Write e=(0,1,2), a=(1,0,2), b=(0,2,1), c=(2,1,0) as permutations of the three positions. Exhaustive LR3 enumeration at the root gives precisely four Cayley generators:

- (a,e), (b,e), (e,a), (e,b).

These generators are involutions. The graph Cay(S3,{a,b}) is a six-cycle because a and b are distinct transpositions and ab has order 3. Therefore

`Cay(S3×S3,{(a,e),(b,e),(e,a),(e,b)}) ≅ C6 □ C6`.

The companion verifier checks the exact adjacency relation at all 36 states, not merely graph invariants.

LR2 adds the two Cayley generators (c,b) and (a,c), where c is the third transposition. Thus OPW23 is the same toroidal grid with two additional mixed-coordinate edges per vertex. The elementary generators explain why both dynamics preserve the S3×S3 relabelling symmetry.

## Immediate consequences

- 36 states, degree 4, graph diameter 6, graph-ball sizes [1,5,13,23,31,35,36].
- Spectrum of C6 adjacency: {2,1,1,-1,-1,-2}. Spectrum of C6□C6 is all pairwise sums, exactly matching EHF-REV-04.
- The apparent two-dimensional local graph geometry is genuine in this finite chamber, but no scaling limit or large-n dimension has been established.
- The 1,2,4 symmetry-representation dimensions are **different** from the graph's two-dimensional toroidal geometry.
- The DIM-06 projected quadratic algebra can now be approached through standard 2D representations of the explicit Cayley generators. The full graph does not satisfy the projected identities.

## Next

1. Derive the DIM-06 identities symbolically from the four LR3 and two LR2 Cayley generators in the standard 2D representation of S3.
2. Determine whether other chambers at n=7 are related to quotient grids, cylinders, or other Cayley/Schreier graphs.
3. Check n=9 before claiming dimensional flow.
4. Compare OPW23 shortcuts against the torus's distance and diffusion geometry.

Run `python3 probes/dimensions/ehf-dim-07/probe.py` (Python standard library only).
