# EHF-HODGE-LIT-01 — Recent OpenAI Hodge Work and the EHF Bridge

Date checked: 2026-10-20 (Australia/Brisbane)

**Decision:** retain the discrete Hodge/topology track and its C1/C2
conjectures. No direct link to the OpenAI Hodge claims has been established.
A direct homotopy identification of the explicit MICRO circle components
with smooth projective varieties is ruled out by first-Betti parity.

**Important correction:** the K3-products claim mentioned in the earlier
discussion is withdrawn. The individual notice dates the withdrawal to
6 October; the repository history records it under 7 October.
This corrects the earlier account that presented it as a current result.

**Subsequent local-status update (HODGE-04):** C2 is now proved by the
[explicit marker potential](../../formal/hodge/TRANSPORT-POTENTIAL.md).
C1 remains conjectural. The literature assessment below records its
original base-commit status; its manuscript-status findings and
projective-parity obstruction are unchanged.

## 1. Version lock and review depth

OpenAI repository: `openai/math`
Revision: `1581d4cbdd69a0faf34b2089614fe2a814316a6a`

EHF base: `eb2c72ada0227f3488044c904a33fc667c424982`

[Source manifest](openai-hodge-sources-2026-10-20.json) records repository
paths, blob hashes, immutable links, review scope, and status findings.

This is a **source/status and proof-structure review**. It is not an
independent verification of the full CM argument, a Lean build, a review
of every external theorem it cites, or a report of community acceptance.

The CM introduction, four-factor reduction, complete surface criterion,
assembly, and selected theta/arithmetic arguments were inspected.
For the archived K3 argument, its introduction and dependency outline
were inspected alongside the complete current withdrawal notices.
The entire withdrawn proof was not recertified.
TeX sources were used to inspect mathematical statements and arguments;
PDF filenames alone were not treated as evidence of a valid result.

## 2. What is current, and what was withdrawn?

| Manuscript | Status at the pinned revision | Evidence |
|---|---|---|
| Rational Hodge for CM abelian varieties, 6 October edition | Unwithdrawn manuscript claiming the CM special case; not certified by this review | [Version notice](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/The-rational-Hodge-conjecture-for-CM-abelian-varieties-October-6-2026/README.md), introduction |
| Rational Hodge for products of K3 surfaces | Withdrawn; claimed theorem left unproved by the submitted argument | [Withdrawal notice](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/The-rational-Hodge-conjecture-for-products-of-K3-surfaces-October-4-2026/README.md) |
| Algebraicity of Kuga–Satake correspondences for K3 surfaces | Withdrawn; dependent construction has a gap | [Withdrawal notice](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Algebraicity-of-Kuga-Satake-Correspondences-for-K3-Surfaces-October-3-2026/README.md) |
| Algebraicity of Weil classes on split abelian eightfolds | Withdrawn; sign error breaks a required cancellation | [Withdrawal notice](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Algebraicity-of-Weil-classes-on-split-abelian-eightfolds-September-18-2026/README.md) |

The [repository history](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/history.md) connects the three withdrawals.
They invalidate the submitted arguments, not the mathematical statements
themselves. The remaining CM claim is not a proof of the full Hodge conjecture.

### Why the withdrawal matters

In the eightfold notice, an intended signed cancellation instead doubles
the nonzero obstruction: starting at -m, the corrected contribution
gives -2m, not zero. A theorem requiring zero signed count therefore
cannot be applied. The notice identifies the dependent K3 construction
as unsupported.

The historical K3 outline uses geometric realization and exact
Kuga–Satake correspondences, then combines factors. Its dependency
failure is not repaired by the continued availability of a CM claim.
The surviving CM argument uses a different presented route; no direct
citation of the three withdrawn titles was found in its inspected
bibliography. That is not a certification that all of its dependencies
are correct.

A catalogue summary can retain an earlier claim after a paper is
withdrawn. For status, prefer current manuscript notices and history
to the overview, a search snippet, or a news description.

## 3. CM argument: the relevant proof structure

The [CM introduction](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/The-rational-Hodge-conjecture-for-CM-abelian-varieties-October-6-2026/build/sections/01-introduction.tex)
claims algebraicity of rational Hodge classes for all CM abelian
varieties. Its reduction uses balanced embedding-line tensors.
Elementary four-factor relations are realized via nonzero periods on
projective surfaces; theta forms provide analytic inputs, arithmetic
extraction supplies rational CM sources, and algebraic correspondences
assemble the classes.

The [surface criterion](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/The-rational-Hodge-conjecture-for-CM-abelian-varieties-October-6-2026/build/sections/03-surface.tex)
requires actual rational Hodge maps to the same projective surface,
with a nonzero cup-product pairing. A nonzero pairing alone does not
supply algebraic representatives. The [assembly](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/The-rational-Hodge-conjecture-for-CM-abelian-varieties-October-6-2026/build/sections/06-assembly.tex)
depends on both the geometric and arithmetic steps.

These are features of the submitted argument, not established results
imported into EHF. Its analytic-to-rational passage and all-size
algebraic construction remain outside this review's certification scope.

### Verification status

The pinned repository describes results at different verification
stages. Searching [lean/formalization.yaml](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/formalization.yaml)
found no Hodge, CM-abelian or K3 title; the 242 entries listed in
[lean/docs](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/docs) contained no family 032 document.
No corresponding formalization was identified, and no Lean build
was run. The release-wide formalization percentage is not evidence
that this particular theorem has been formally checked.

This is a bounded catalogue check, not a universal claim that no
formalization could exist elsewhere or be added later.

## 4. Comparison with EHF

| Mathematical requirement | CM manuscript | Current EHF MICRO track |
|---|---|---|
| Underlying objects | Algebraic varieties with CM structure | Valid binary words and a move complex |
| Cohomology | Rational cohomology with specified Hodge types | Ordinary cellular H1/H^1 over Q |
| Elementary relation | Balanced tensor switch with algebraic realizations | Two admissible commuting move orders |
| Pairing used | Surface cup-product period | Sum of an edge cochain around a loop |
| Rational/algebraic realization | An essential construction in the argument | Not constructed |
| Global conclusion sought | Algebraic representatives of Hodge classes | Component topology and winding identities |

Our square relations and the paper's four-label relations are different
objects. Their common appearance as balanced relations does not give
a map between them.

Likewise, an EHF integer winding period is not automatically a period
of a differential form on a projective surface. The word “harmonic”
in a finite cochain decomposition does not identify a rational
(p,p) class.

## 5. A direct bridge obstruction

This is a deduction for EHF from standard Hodge theory, not a new
consequence claimed by OpenAI.

For a smooth projective complex variety Y, compact Kähler Hodge
decomposition and complex conjugation give

`H^1(Y,C)=H^(1,0)(Y) direct_sum H^(0,1)(Y),`
`H^(0,1)(Y)=conjugate(H^(1,0)(Y)).`

Consequently

`b1(Y)=2 dim_C H^(1,0)(Y),`

which is even. See [Deligne's official Clay exposition](https://www.claymath.org/wp-content/uploads/2022/06/hodge.pdf)
for the Hodge decomposition underlying this argument.

By HODGE-02, the adjacent-pair sector of X_n is a component C_n,
a graph cycle, for every n>=5. Its first Betti number is 1.

**Therefore no such component is homotopy equivalent to a smooth
projective complex variety.** The same argument rules out a direct
identification preserving H1 for any other component with b1=1.

This all-size conclusion uses the explicit C_n family, not the
unproved C1 conjecture. In the finite HODGE-03 scan it applies to
each of the 200 moving components, since each has b1=1.
If C1 holds in general, it would extend to every moving component.

A one-dimensional rational H^1 also cannot be the entire underlying
rational vector space of a pure weight-one Hodge structure of the
kind arising from a smooth projective variety.

### What the obstruction does not rule out

It does not prohibit a map into a larger variety, a subspace or
quotient of a larger cohomology group, a different weight, mixed
Hodge structures, or a different EHF construction.
None of those relationships has been established here.

Disjointly grouping two odd-b1 components does not repair the
componentwise obstruction: each connected component of a smooth
projective variety must satisfy the parity condition separately.
Enlarging a model can change the question, but requires a justified
construction and new theorems.

There is also a degree distinction. The current EHF classes lie in
degree one; the Clay conjecture concerns rational classes of type
(p,p) in degree 2p. Products of graph classes would still require an
actual variety, a Hodge structure and an algebraic cycle map.

## 6. Consequences for research direction

1. Keep HODGE-01–03 as discrete Hodge/topology work on the stated
   constructions. Their exact local results do not depend on the
   OpenAI papers.
2. Keep C1 and C2 as precisely defined unproved all-size conjectures.
   Neither the unwithdrawn CM claim nor the withdrawn K3 argument
   proves them or establishes their novelty.
3. Continue the planned HODGE-04 proof audit for
   `dF=(n-2D)j-2(n-2m)kappa`.
   This is a concrete internal mathematical target.
4. Treat a bridge to the Clay problem as a separate gate. Any proposal
   must specify a variety, its smoothness/projectivity, the map from
   EHF data, its rational Hodge types, and candidate algebraic cycles.
   A direct homotopy identification with the circle components
   fails the parity test.
5. Do not add complex structure or double dimensions merely to match
   an anticipated answer. Such choices need independent mathematical
   motivation and must explain what they preserve.

## 7. Evidence ledger

- **SOURCE-CONFIRMED:** three withdrawal notices; unwithdrawn CM
  manuscript and its stated scope at the pinned revision.
- **BOUNDED NEGATIVE CHECK:** no corresponding formalization identified
  in the inspected catalogue/docs; not a Lean verification.
- **PROVED (standard theorem plus EHF construction):** odd-b1 circle
  components cannot be homotopy equivalent to smooth projective
  complex varieties.
- **UNESTABLISHED:** correctness of the complete CM manuscript,
  community acceptance, a useful EHF-to-CM bridge, and any implication
  for solving the full Hodge conjecture.
- **UNCHANGED:** EHF C1/C2 evidence and their novelty boundary.

In plain language: OpenAI did publish relevant work, but part of that
work has been withdrawn. The remaining CM paper operates with structures
we have not derived in EHF. Our branch has useful discrete mathematics
to pursue; it currently supplies no shortcut to the algebraic Hodge problem.

