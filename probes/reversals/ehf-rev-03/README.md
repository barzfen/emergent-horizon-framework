# EHF-REV-03 — Natural symmetry of the largest n=7 OPW3 chamber

**Date:** 2026-11-19 (Australia/Brisbane)  
**Status:** Exact exhaustive finite result; no physical identification.

## Construction
Enumerate undirected Hamiltonian cycles on K7 modulo rotation and reflection, anchored at label 0. Preserve the canonical even-position label set Pi, and connect distinct states by circular length-3 reversals preserving Pi, following [OPW3 definition](../../../research/source-documents/opw3-v0.6.md).

## Independently reproduced census
360 states, 600 simple LR3 edges, 19 connected components. Component-size multiplicities: 4×1, 8×2, 12×3, 16×3, 20×3, 24×3, 28×2, 32×1, 36×1.

The unique largest chamber has 36 vertices, all degree 4. Its Pi set contains 0 and three other labels; the remaining three labels are in the other parity class.

## Symmetry test
Fix label 0 and independently permute the other three labels in each parity class. These relabellings form S3 × S3, order 36. Exhaustive checks establish:
1. Every group element maps the 36-state chamber to itself.
2. Every group element preserves all adjacency lists.
3. The orbit of one state has size 36.

Hence the action is free and transitive: the chamber's vertex representation is the **regular representation of S3 × S3**. This is an exact finite combinatorial symmetry, not a continuous SU(3) action.

## Representation consequence
The complex irreducible dimensions of S3 are 1,1,2. The nine irreducible dimensions of S3 × S3 are **1,1,1,1,2,2,2,2,4**. In the regular representation each irrep occurs with multiplicity equal to its dimension, giving 4×1² + 4×2² + 1×4² = 36.

There is no 3-dimensional *irreducible* representation in this natural group action. Reducible three-dimensional subspaces can exist; their mere existence would not establish three distinguished sectors or the SU(3) singlet/octect/27 norm ratio. The appearance of two three-label sets comes from the parity-preserve definition, not a newly forced three-colour physical structure.

## Reproduction
Run `python3 probes/reversals/ehf-rev-03/probe.py` from repository root. Standard-library only; exhaustive graph and relabelling checks.

## Next falsifiable question
Determine the adjacency operator's decomposition across these nine isotypic sectors and whether any **canonical** three-block quotient is selected without fitted choices. Compare with n=7 OPW23 and n=9; include symmetry-preserving controls. No 1:2:3 projected-norm result has been established.
