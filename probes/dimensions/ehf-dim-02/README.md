# EHF-DIM-02 — Same symmetry, different dynamics

**Date:** 2026-11-19 (Australia/Brisbane)  
**Status:** Finite exhaustive numerical linear-algebra probe, n=7 largest chamber.

## Question
Do the microscopic symmetry representations determine the large-scale reversal dynamics, or can the same symmetry support different geometry and diffusion? This is distinct from the separate question of constructing SU(3) from more elementary ingredients.

## Setup
Use the canonical Hamiltonian cycles and parity-preserving circular LR3 and LR2+LR3 rules defined in [OPW3](../../../research/source-documents/opw3-v0.6.md). The 36-state largest chamber is invariant under independent permutations of the three nonzero labels in each parity class, giving the natural regular S3×S3 action from [REV-03](../../reversals/ehf-rev-03/README.md). The [REV-04](../../reversals/ehf-rev-04/README.md) character projectors are used for both operators.

## Findings
- Both adjacency operators commute with all 36 relabelling matrices. They preserve **the same nine isotypic sectors** of dimensions 1,1,1,1,4,4,4,4,16.
- OPW3 has degree 4, integral adjacency spectrum and normalized random-walk spectral gap **1/4**.
- OPW23 has degree 6, a partly nonintegral adjacency spectrum and normalized gap **1/2**.
- The adjacency matrices **do not commute** (their commutator is nonzero), despite both commuting with the group action. Shared isotypic sectors do not imply identical eigenvectors or dynamics.

Selected isotypic adjacency eigenvalues (t=trivial, s=sign, d=standard 2D representation):

| Sector | Dimension | OPW3 | OPW23 |
|---|---:|---|---|
| tt | 1 | 4 | 6 |
| ts, st | 1 each | 0 | -2 |
| ss | 1 | -4 | -2 |
| td, dt | 4 each | 1×2, 3×2 | 1×2, 3×2 |
| sd, ds | 4 each | -3×2, -1×2 | (-2-sqrt(3))×2, (-2+sqrt(3))×2 |
| dd | 16 | -2×4, 0×8, 2×4 | ((-1-sqrt(33))/2)×4, 0×4, 1×4, ((-1+sqrt(33))/2)×4 |

**Important correction to interpretation:** SU(3) is not derived; S3×S3 is a finite relabelling symmetry. The representation dimensions are not graph-geometric or spatial dimensions. These results do not imply a 1:2:3 amplitude-norm law.

## Reproduction
Run `python3 probes/dimensions/ehf-dim-02/probe.py` (NumPy required). It independently enumerates states, edges, chambers, both adjacency matrices, the 36 group actions and the nine character projectors.

## Next
Measure representation-resolved diffusion under both transition operators, test how the comparison changes for n=9 and under degree-matched null controls, and investigate whether any coarse-graining naturally links microscopic sectors to an effective graph dimension. Do not fit a dimensional exponent to the 36-state chamber.
