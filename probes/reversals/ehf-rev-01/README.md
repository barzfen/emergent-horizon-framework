# EHF-REV-01 — Reversal paths and the 1:2:3 colour-sector question

**Date:** 2026-11-19 (Australia/Brisbane)  
**Status:** Baseline audit complete; representation-theoretic bridge open.

## Question

Can admissible Hamiltonian-cycle reversals, without importing a particle representation by assumption, yield an invariant three-sector decomposition whose squared projection norms follow 1:2:3? Compare to the reported tree-level MHV collinear SU(3) singlet/symmetric-octet/27 norm relationship. This is a comparison hypothesis, not an established identification.

## Source definitions

- [OPW3 working document](../../../research/source-documents/opw3-v0.6.md): odd-n Hamiltonian cycles modulo rotation/reflection; preserve label Pi; OPW3 uses LR3, OPW23 uses LR2 union LR3.
- [CROSS-48](../../../research/cbb-binary/CROSS-48-reversal-interference.md): two legal LR3 reversal paths forming a commuting square; a **chosen** Clifford/Pin lift gives a relative minus sign. The underlying graph does not select that lift or coherent amplitudes.
- [CROSS-08](../../../research/cbb-binary/CROSS-08-lr4-winding-break.md): distinguishes colour-word winding counts from the separately reported collinear SU(3) norm ratio.
- [Collinear colour programme](../../../research/amplitudes/collinear-colour/literature.md).

## Baseline result: simple edge-count hypothesis fails

The published exhaustive OPW3 audit records the following simple undirected edge counts (LR2 and LR3 edge sets disjoint for n=7,9):

| n | LR3 | LR2 | OPW23 total | LR3 fraction | LR2 fraction |
|---|---:|---:|---:|---:|---:|
| 7 | 600 | 240 | 840 | 5/7 | 2/7 |
| 9 | 53,760 | 13,440 | 67,200 | 4/5 | 1/5 |

Therefore the LR3:LR2 ratio is 5:2 at n=7 and 4:1 at n=9. These are **two move types**, not three representation sectors; neither count supports a universal 1:2:3 reversal law. The 5/7 and 2/7 figures are finite-size edge fractions, not physical probabilities without a sampling rule.

Reproduce arithmetic:

```python
from fractions import Fraction
for n, lr3, lr2 in [(7, 600, 240), (9, 53760, 13440)]:
    assert lr3 + lr2 == {7: 840, 9: 67200}[n]
    print(n, 'LR3 fraction', Fraction(lr3, lr3+lr2),
          'LR2 fraction', Fraction(lr2, lr3+lr2),
          'LR3/LR2', Fraction(lr3, lr2))
```

## Why 1:2:3 is a different question

For SU(3), Sym^2(8)=1 ⊕ 8 ⊕ 27, with dimensions 1+8+27=36. Representation dimensions are **not** the claimed 1:2:3 projected squared norms. The earlier collinear result is conditional on its amplitude setup and still requires independent validation. A reversal-path model must independently produce a group action, a representation, an invariant inner product, a specified vector/amplitude, and projection operators before a squared-norm comparison is meaningful.

## CROSS-48 relevance and limitation

The two reversal orders give a common endpoint. Their ordinary permutations commute; the **chosen** Pin/Clifford lift anticommutes. With additionally supplied coherent pulse and readout, this yields interference. It does **not** derive the coherent rule, SU(3), or a 1:2:3 law from admissibility alone.

## Next falsifiable tests

1. Independently rerun CROSS-48 verifier and confirm all route-pair and sign claims.
2. Construct the natural permutation action of the automorphism group on a small OPW3 chamber; compute irreducible invariant subspaces without imposing SU(3).
3. Test whether any natural action yields exactly three nontrivial sectors, robust under n=7 to n=9 and OPW3 versus OPW23. Include trivial/symmetric random-graph controls.
4. If such sectors exist, define a **non-fitted** amplitude and invariant inner product, compute squared projection norms, and compare to 1:2:3 with explicit error metric.
5. If no three-sector structure appears, record a negative result. Do not compare arbitrary three chosen bins or adjust weights after seeing outcomes.

**Interpretation:** Baseline edge-count explanation is ruled out for these sizes. No reversal-derived SU(3) representation or 1:2:3 norm law has yet been established.
