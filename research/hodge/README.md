# EHF Hodge research track

Date: 2026-10-20 (Australia/Brisbane)

## Purpose and decision

**Proceed:** discrete Hodge theory supplies a precise language for separating
potential differences, local circulation, and global cycle components in scalar
comparison data on a specified EHF complex.

**Open / unestablished:** a bridge from EHF to the Clay Hodge conjecture.

These are distinct targets. The first can produce useful EHF mathematics even
if the second never becomes viable.

## Read in this order

1. [RECUR background](../../probes/holonomy/RECUR-BACKGROUND.md):
   Hamilton-cycle microstates, anchored observers, conditional transport and its polar factor.
2. [HODGE-01](../../probes/hodge/HODGE-01.md):
   definitions, exact controls, independently enumerated transport results,
   limitations and a gated next probe.
3. [Audit code](../../code/hodge/hodge_01_audit.py) and
   [retained results](../../data/hodge/hodge-01-results.json).
4. [HOL-07](../../probes/holonomy/HOL-07.md) for the inherited holonomy frontier.
   Its all-size asymptotic certificates remain pending as stated there; this
   branch does not promote those claims to proved status.

## Mathematical scope

A graph does not specify which loops bound faces. Adding triangles or other cells
changes cohomology and the Hodge decomposition. Every probe must state:
vertices, oriented edges, cells, coefficient field, inner product, observable,
and why the cell rule is justified by the EHF construction.

For the first audit, vertices are **observer anchors**, not Hamilton-cycle
microstates. The complete graph of observer comparisons and its filled-triangle
2-skeleton are alternative diagnostic constructions. Neither is declared the
uniquely correct EHF space.

Ordinary scalar Hodge decomposition uses additive cochains. RECUR transports
are generally rank-deficient matrix maps; their polar factors are partial
isometries. Their loop products must not be replaced by sums of angles or entries
without proving that the reduction preserves the relevant invariant.

## Fit assessment

| Target | Current status |
|---|---|
| Finite scalar cochain complex and Hodge decomposition | Established mathematical tool; reference controls reproduced |
| RECUR observer transport | Reconstructed independently for n=5,6,7,8 |
| Distinguish scalar exactness from matrix path dependence | Demonstrated in the stated controls |
| Intrinsically selected EHF faces and scalar comparison observable | Not established |
| Growth maps inducing cochain maps and stable cohomology | Not established |
| Smooth projective complex variety attached meaningfully to EHF | Not established |
| Rational Hodge classes and algebraic cycle map | Not established |
| Progress on the Clay conjecture or a new conjecture | Not claimed |

## What the Clay problem would actually require

For a smooth projective complex algebraic variety X, the conjecture asserts
that every rational cohomology class of type (p,p) is a rational linear
combination of classes of codimension-p algebraic cycles:

`H^(2p)(X,Q) intersect H^(p,p)(X) = span_Q{cl(Z)}.`

A harmonic vector in a graph is not thereby a rational (p,p) class.
A graph cycle is not thereby an algebraic cycle. A finite rank computation
does not establish the algebraicity of a class.

A serious bridge proposal must give:

1. An explicit construction of X, with smoothness and projectivity justified.
2. A justified relation between EHF data and its cohomology; arbitrary embedding
   or association is insufficient evidence of explanatory value.
3. Its rational structure and Hodge decomposition or filtration.
4. Actual algebraic cycles and their cycle-class map.
5. A precise unresolved statement for which the EHF construction adds leverage.
   Reproducing a known case is a calibration, not a solution of the conjecture.

## Evidence and stopping rules

Use the repository's PROVED, COMPUTATIONAL, EMPIRICAL PATTERN, CONJECTURE,
SPECULATIVE and FALSIFIED / NEGATIVE labels.

- Standard Hodge decomposition and simplex homology are existing mathematics.
- HODGE-01 is a reference implementation plus a finite EHF reconstruction.
- No novelty claim is made from matching standard identities.
- A proposed new conjecture needs exact definitions, quantifiers, counterexample
  searches and a literature comparison.
- If no intrinsic face rule or meaningful observable is found, retain the audit
  and pause the track rather than manufacture a topology.
- If the algebraic-geometric bridge remains absent, describe subsequent work
  as discrete Hodge/cohomology work.

## Sources

- Pierre Deligne, *The Hodge Conjecture*, official Clay problem description:
  https://www.claymath.org/wp-content/uploads/2022/06/hodge.pdf
- Xiaoye Jiang, Lek-Heng Lim, Yuan Yao and Yinyu Ye,
  *Statistical ranking and combinatorial Hodge theory*:
  https://arxiv.org/abs/0811.1067
  Established gradient/curl/harmonic treatment of scalar edge flows; it
  does not turn the Clay conjecture into a graph problem.

Both sources were consulted on 2026-10-20. These sources support the standard
mathematics; EHF-specific conclusions are scoped to the attached audit.
