# EHF-AMP-FOUND-01/02
## Anchor-Relative Scaffolds, Reconstructive Growth, and Complement-Pair Residue Channels

**Version:** 0.5 — consolidated correction and progress note through EHF-AMP-FOUND-02D  
**Date:** 2026-07-13  
**Status:** Internal EHF/RAF research note  
**Supersedes:** `ehf_amp_found_01_anchor_relative_scaffolds_v0_4.md`

---

## 0. Purpose and correction notice

This note consolidates the current amplitude-foundation programme after a full numerical and conceptual audit of the earlier AMP-18–20 claims, the reconstruction of distinct state-growth channels, and the reflection-aware growth–factorisation probes EHF-AMP-FOUND-02A through 02D. It now includes the complete rank-110 residue image, exact branch-reversal covariance, the 38+72 local/nonlocal split, the ten complementary flip-pair channels, and the numerically exact rational residue spectrum.

Version 0.3 must not be used as the current statement of the AMP-20 result. In particular, its sections claiming that the original `amp20_gap_dissolve.py` proved anchor-2 closure are retired. The original test projected onto the square orthogonal completion returned by QR on a wide matrix, so its near-zero residual was guaranteed even for vectors outside the actual residue span.

The corrected programme now distinguishes:

1. a **fixed-chart, multi-channel** calculation, in which the source partition remains \(\Pi_1\) while the factorisation channel is centred on different labels;
2. a **true multi-chart** calculation, in which the partition \(\Pi_a\), local relation spaces, and matching anchor channel are all rebuilt for each anchor \(a\);
3. **state growth**, which inserts labels directly into Hamilton-cycle orderings;
4. **relation growth**, which is not coefficient copying and instead requires a nontrivial section of a factorisation map.

These distinctions are now part of the formal vocabulary of the programme.

---

## 1. Evidence-status codes

To keep the claim boundary explicit, this note uses the following status labels.

| Code | Meaning |
|---|---|
| **E** | Exact finite combinatorial result from exhaustive enumeration or direct identity |
| **R2** | Numerical result reproduced at two independent kinematic seeds |
| **R1** | Numerical result reproduced in one corrected run but not yet repeated independently |
| **C** | Corrected result replacing a retired or invalid earlier computation |
| **H** | Hypothesis or interpretation, not established |
| **Q** | Quarantined or retired claim |

No physical derivation of gauge theory, particle content, chirality, or the Standard Model is claimed here.

---

## 2. Fixed mathematical conventions

### 2.1 Ordering space

Let

\[
X_n=\{\text{canonical cyclic orderings of }[n]\text{ modulo reversal}\}.
\]

With label 1 placed first and the canonical orientation selected by

\[
c_1<c_{n-1},
\]

we have

\[
|X_n|=\frac{(n-1)!}{2}.
\]

This is also the number of colour orderings modulo cyclicity and reflection in the trace basis of an \(n\)-point tree amplitude.

### 2.2 Reflection character

For a Parke–Taylor factor,

\[
\operatorname{PT}(\alpha^{\mathrm{rev}})=(-1)^n\operatorname{PT}(\alpha).
\]

Therefore canonicalisation must carry an orientation character:

- at even multiplicity, reversal contributes sign \(+1\);
- at odd multiplicity, reversal contributes sign \(-1\).

This sign is essential whenever insertion, deletion, relabelling, or re-anchoring recanonicalises an ordering.

### 2.3 Anchor-relative fibres

For each anchor \(a\), rotate an ordering to place \(a\) first, apply the reflection convention, and define the parity-position label

\[
\Pi_a(c)=\bigl(E_a(c),O_a(c)\bigr).
\]

The corresponding partition is

\[
\mathcal P_{n,a}=\{F_{n,a,\xi}\}_\xi.
\]

The individual fibres are reference-dependent. Re-anchoring generally scatters one fibre across many fibres, although the multiset of fibre sizes and relation dimensions can remain invariant.

The preferred language is therefore:

\[
\boxed{\text{anchor-relative scaffold}\neq\text{anchor-independent amplitude content}.}
\]

### 2.4 Relation spaces

Let

\[
\mathcal C_n=\mathbb C^{X_n}
\]

and let \(\mathcal E_n^{\mathrm{PT}}\) be generic Parke–Taylor evaluation. The global constant-coefficient relation space is

\[
R_n=\ker \mathcal E_n^{\mathrm{PT}}.
\]

For a fibre \(F\in\mathcal P_{n,a}\), define

\[
R_{n,a}(F)=R_n\cap\mathbb C^F.
\]

The direct sum of all fibre-local relation spaces in one chart is

\[
\mathcal R^{\mathrm{loc}}_{n,a}
=
\bigoplus_{F\in\mathcal P_{n,a}}R_{n,a}(F).
\]

This local direct sum is generally a proper subspace of the full global relation space \(R_n\).

### 2.5 Move-rule independence

The amplitude results in this note depend primarily on:

- cyclic orderings;
- reflection parity;
- anchor-relative \(\Pi\)-fibres;
- Parke–Taylor relation spaces;
- insertion and factorisation maps.

They do not require the old LR23/OPW23 connectivity. The current CBB foundational rule remains **LR3 only**, with OPW3 as the minimal preserve diagnostic. The word “chamber” should be replaced by “\(\Pi\)-fibre” whenever graph connectivity is not used.

---

## 3. Correction register

### 3.1 Retired wide-QR AMP-20 verdict — **Q/C**

The original AMP-20 code formed a wide residue matrix \(R\) with 2520 rows and many more than 2520 columns, then used reduced QR and projected onto the returned square matrix \(Q\). For a wide input, this \(Q\) spans the whole ambient coordinate space, so every vector has essentially zero projection residual.

Consequently, the original claim

\[
\text{“anchor 2 closes the gap with residual }1.3\times10^{-15}\text{”}
\]

was void as computed.

House rule adopted after this audit:

> Every span-membership test must report numerical rank and singular gap, and must include both a positive in-span control and a negative complement control.

### 3.2 Fixed-chart, multi-channel correction — **C/R1**

Keep the source \(\Pi_1\)-fibre partition fixed, but collect factorisation residues centred successively on labels \(1,2,\ldots,9\). The corrected randomized range-compression/SVD calculation gives:

| Channels included | Missing-direction residual | Residue-span rank |
|---|---:|---:|
| 1 | 1.000000 | 524 |
| 1–2 | 0.664023 | 1237 |
| 1–3 | 0.546381 | 1562 |
| 1–4 | 0.501946 | 1709 |
| 1–5 | \(8.7\times10^{-15}\) | 1776 |
| 1–9 | approximately 0 | 1800 |

The full rank

\[
1800=2520-720
\]

matches the dimension of the global \(n=8\) constant-coefficient relation space.

The correct statement is:

\[
\boxed{\text{Within the fixed }\Pi_1\text{ chart, channel 5 is the first cumulative channel that closes the exceptional gap.}}
\]

This is a **channel-completion** result, not a true re-anchoring result.

### 3.3 True multi-chart calculation — **R1**

EHF-AMP-FOUND-01B rebuilt, for each anchor \(a\):

1. the source partition \(\Pi_a\);
2. every local relation basis in that chart;
3. the matching anchor-centred residue map;
4. transport into one common target coordinate space.

In the seed-11 run:

- the true \(\Pi_1\) chart gave rank 524 and exceptional overlap \(14/15\);
- the true \(\Pi_2\) chart alone had exceptional overlap \(15/15\);
- combining charts 1 and 2 increased cumulative rank from 524 to 525;
- the missing-direction residual fell to about \(2.6\times10^{-15}\);
- the cumulative span passed a fresh Parke–Taylor test at about \(7\times10^{-14}\).

The run later encountered an SVD convergence failure while processing anchor 6, after closure had already occurred. The anchor-2 closure is therefore a corrected one-seed result, but the complete nine-chart sweep has not yet been repeated at a second seed.

The two corrected closure mechanisms are distinct:

\[
\boxed{
\begin{array}{ll}
\text{fixed chart, varying channels:} & \text{first closure at channel 5},\\[1mm]
\text{rebuilt charts with matching channels:} & \text{closure already in chart }\Pi_2.
\end{array}}
\]

There is no discrepancy because the two probes compute different families of subspaces.

### 3.4 Orientation and vacuity correction in 02A — **C/R2**

The first 02A implementation dropped the reflection character during recanonicalisation. This made the raw \(7\to8\) residue span appear largely invalid and produced the false reduction

\[
110\longrightarrow40.
\]

It also counted zero-dimensional parent relation spaces as successful unchanged-coefficient lifts.

After carrying the reflection sign and excluding vacuous cases:

- all 110 raw \(7\to8\) residue directions are relation-valid;
- the apparent \(18/38\) lift success becomes \(0/20\) genuine successes plus 18 vacuous cases.

The corrected results reproduce at seeds 11 and 29.

---

## 4. AMP-18 exceptional fibre and factorisation geometry

### 4.1 Anchor-1 target ledger — **R2**

At \(n=8\), anchor 1 gives 35 fibres. Every fibre has

\[
|F|=72,
\qquad
\dim R_{8,1}(F)=15.
\]

At \(n=9\), there are 69 source fibres. Correct anchor-collinear deletion maps each source-fibre/channel pair into one target fibre, whereas an interior non-pole deletion can scatter a source fibre across 34 of the 35 target fibres.

The anchor-1 factorisation image generates:

\[
34\text{ target fibres at }15/15,
\]

and one target at

\[
14/15.
\]

The exceptional fibre is

\[
G_*:
\qquad
E=\{1,4,5,6\},
\qquad
O=\{2,3,7,8\}.
\]

For its residue-image matrix, the smallest retained singular value is approximately

\[
1.701864,
\]

while the first discarded singular value is approximately

\[
5.6\times10^{-15}.
\]

The codimension-one result is therefore numerically unambiguous.

Let

\[
v_*\in R_{8,1}(G_*)
\]

span the direction orthogonal to the 14-dimensional anchor-1 arrival space.

### 4.2 Interpretation

The exceptional direction is not evidence for a particle or new force. Its established significance is narrower:

> One reference-local factorisation family fails to generate one exact local relation direction, while alternative channel or chart families can recover it.

This is the first finite model of incomplete reference-relative views reconstructing complete amplitude content through overlap.

---

## 5. Exact state-growth channels

Growth by insertion is the inverse combinatorial operation to deletion, but there is more than one geometrically distinct insertion channel.

### 5.1 Single-label anchor insertion — **E**

For a canonical \(n\)-cycle, insert the new maximum label \(n+1\) into any one of its \(n\) gaps and recanonicalise.

Exhaustive enumeration at

\[
6\to7,
\qquad
7\to8,
\qquad
8\to9
\]

shows:

1. insertion is a bijection
   \[
   X_n\times\{\text{gaps}\}\cong X_{n+1};
   \]
2. insertion beside the anchor is an exact section of the matching anchor-channel deletion;
3. each individual anchor-side branch is single-valued on fibres;
4. interior insertion scatters across multiple fibres in a structured, nonmaximal way.

The two anchor branches show a parity pattern:

- even-to-odd growth: the two branches land in the same target fibre;
- odd-to-even growth: the two branches land in different target fibres.

### 5.2 Middle-block core growth — **E/R1**

The original AMP-07 core growth from \(n=7\) to \(n=9\) selects descendants having

\[
\{c_4,c_5\}=\{8,9\},
\]

the unique adjacent middle-position pair stable under reversal.

Every one of the 19 parent fibres has two children with sizes

\[
9s+108,
\qquad
9s+144,
\]

where \(s\) is the parent size.

The sibling mechanism uses the label transposition

\[
\tau=(8\,9).
\]

For each sibling pair \(A,B\), with \(A\) the smaller child:

- \(\tau\) injects \(A\) into \(B\);
- all orientation signs are \(+1\) in this map;
- the complement \(B\setminus\tau(A)\) has 36 states;
- every local relation of \(B\) vanishes on that complement;
- the local relation dimensions of the siblings are equal.

This is a concrete relation-level growth mechanism, not merely a size coincidence.

### 5.3 Reconciliation of middle and anchor channels — **E**

Let \(P\) be a realized \(n=7\) parent fibre. Write \(A(P)\) for its \(+144\) child and \(S(P)\) for its \(+108\) child.

The middle-block channel gives

\[
D(P)=\{A(P),S(P)\}.
\]

Sequential anchor growth gives

\[
G(P)=\{A(P),A(\operatorname{flip}P)\},
\]

where

\[
\operatorname{flip}(E,O)
=
\bigl(\{1\}\cup O,\ E\setminus\{1\}\bigr).
\]

Thus:

- both channels share the child \(A(P)\);
- the \(+108\) lineage is invisible to anchor growth;
- the flip-partner \(+144\) lineage is invisible to middle-block growth.

The distinction is controlled by reversal geometry:

- the middle insertion site is reversal-stable;
- the two anchor sites are exchanged by reversal.

### 5.4 Ghost child and tested growth orphans — **E**

Middle-block growth reaches 38 of the 69 \(n=9\) fibres. Anchor-composite growth reaches 20. Their union reaches 39, with intersection 19. Therefore

\[
69-39=30
\]

fibres have no parent under either tested channel.

One anchor child corresponds to the \(+144\) lineage of an unrealized empty \(n=7\) fibre; this is the “ghost child.”

The 30 currently unreached fibres carry

\[
1188
\]

of the total

\[
1962
\]

chamber-local relation dimensions at \(n=9\), approximately \(60.6\%\). The 39 reached fibres carry 774. The four largest fibres,

\[
576,\ 540,\ 504,\ 504,
\]

are all in the unreached set.

The word **orphan** is channel-relative:

> unreached by the tested middle-block and anchor-composite channels, not proven parentless under every possible insertion channel.

---

## 6. EHF-AMP-FOUND-02A: Growth–factorisation compatibility

### 6.1 State section versus relation section

For individual states, anchor insertion \(I\) and matching deletion \(D\) obey

\[
DI=\operatorname{id}.
\]

The naive relation lift applies \(I\) to every ordering in a relation while leaving its coefficients unchanged.

This fails because inserting a new label \(M\) between anchor 1 and adjacent label \(a\) changes a Parke–Taylor factor by a state-dependent kinematic multiplier of the form

\[
\frac{\langle1a\rangle}
{\langle1M\rangle\langle Ma\rangle},
\]

up to the reflection character. Different terms of a parent relation generally have different adjacent labels \(a\), so their original coefficient cancellation is not preserved.

This obstructs the diagonal coefficient-copy lift. It does **not** prove that every possible constant linear lift with nonlocal mixing is impossible.

### 6.2 Reproduced transition ledger — **R2**

The reflection-aware probe was run at seeds 11 and 29 with identical ranks and containment verdicts.

| Transition | Valid global residue-span rank | Nonzero parent-local spaces fully recovered | Genuine unchanged-coefficient lifts |
|---|---:|---:|---:|
| \(6\to7\) | 7 | \(7/10\) | \(0/20\) |
| \(7\to8\) | 110 | \(10/10\) | \(0/20\) |
| \(8\to9\) | 363 | \(13/35\) | \(0/70\) |

At \(7\to8\), nine additional parent fibres have zero relation dimension; their 18 branch cases are excluded as vacuous.

Across all transitions,

\[
\boxed{0/110\text{ genuine unchanged-coefficient lifts succeed}.}
\]

The residue spans pass fresh Parke–Taylor tests at approximately \(10^{-14}\) to \(10^{-12}\).

### 6.3 Complete local recovery at \(7\to8\) — **R2**

The total direct-sum dimension of the nonzero seven-point fibre-local relation sector is

\[
\dim\mathcal R^{\mathrm{loc}}_7=38.
\]

Every one of its ten nonzero fibre summands is contained in the delete-8 residue image of eight-point fibre-local relations.

Therefore some linear right inverse exists on this sector:

\[
L_{7\to8}:\mathcal R^{\mathrm{loc}}_7
\longrightarrow
\mathcal R^{\mathrm{loc}}_8,
\qquad
D_8L_{7\to8}=\operatorname{id}.
\]

The existence of this section does not follow from state insertion; it is a separate relation-level reconstruction result.

### 6.4 Exceptional direction under delete 8 — **R2**

Inside the exceptional fibre,

\[
\dim R_8(G_*)=15,
\]

and the restricted delete-8 map has

\[
\operatorname{rank}(D_8|_{R_8(G_*)})=11,
\qquad
\dim\ker(D_8|_{R_8(G_*)})=4.
\]

The AMP-18 missing direction satisfies

\[
\|D_8v_*\|=\frac1{\sqrt2},
\]

and lies completely outside the deletion kernel.

After the reflection correction, \(D_8v_*\) is a valid global seven-point relation. However, it is not produced by unchanged-coefficient insertion. The corrected guarded verdict is

```text
RELATION_VALID_RESIDUE_VISIBLE_NOT_NAIVELY_INHERITED
```

The correct interpretation is transformed ancestry, not simple copying and not residue invisibility.

---

## 7. EHF-AMP-FOUND-02B: Minimal nontrivial growth sections

### 7.1 Global local-sector map — **R2**

For anchor 1 at \(7\to8\),

\[
\dim\mathcal R^{\mathrm{loc}}_7=38,
\qquad
\dim\mathcal R^{\mathrm{loc}}_8=525.
\]

Restrict delete 8 to the eight-point local direct sum:

\[
D_8:\mathcal R^{\mathrm{loc}}_8\to\mathcal C_7.
\]

At both seeds 11 and 29,

\[
\operatorname{rank}D_8=110,
\qquad
\dim\ker D_8=415.
\]

The complete 38-dimensional seven-point local sector lies inside the 110-dimensional image.

Using the rank-truncated Moore–Penrose inverse gives an explicit section

\[
L=B_8(D_8B_8)^+B_7
\]

with

\[
D_8L=B_7
\]

to residuals of approximately \(3\times10^{-15}\). The lifted eight-point vectors and reconstructed seven-point vectors pass independent Parke–Taylor checks at approximately \(10^{-13}\).

Thus:

\[
\boxed{\text{Every seven-point fibre-local relation has an exact transformed eight-point ancestor.}}
\]

### 7.2 Fibre locality of the section — **R2**

For all ten nonzero seven-point parent fibres:

- the pair of direct state-growth children suffices;
- the plus child alone suffices when its full two-sided residue is used;
- the minus child alone suffices when its full two-sided residue is used;
- at least one single incident child fibre suffices.

Therefore

\[
\boxed{10/10\text{ nonzero parents admit a one-child exact relation lift}.}
\]

The growth law is nontrivial in coefficient space, but it need not be globally diffuse across many child fibres.

### 7.3 Branch asymmetry observed in 02B — **R2, resolved in 02C**

The matching-branch audit gives, at both seeds:

\[
D_+\text{-only section residual}=1,
\]

while

\[
D_-\text{-only section residual}\sim10^{-15}.
\]

Per parent:

\[
\text{plus matching branch: }0/10,
\qquad
\text{minus matching branch: }10/10.
\]

The plus child is not deficient, because its full residue still provides a section. The useful relation content of the plus child is exposed through the opposite branch or through the combined residue.

No physical directionality follows from this one-sided result. EHF-AMP-FOUND-02C subsequently shows, with zero operator discrepancy, that reversal of the canonical representative exchanges the two branch labels. The asymmetry is therefore a chart-orientation effect rather than an invariant chirality.

### 7.4 Exceptional direction and local/nonlocal gluing — **R2**

The residue of \(v_*\) has distance 1 from the seven-point fibre-local direct sum:

\[
\operatorname{dist}
\left(D_8v_*,\mathcal R^{\mathrm{loc}}_7\right)=1.
\]

Combined with the valid global Parke–Taylor test from 02A, this means:

> \(D_8v_*\) is a valid global seven-point relation spanning multiple parent fibres, but it is not a sum of independently fibre-local seven-point relations.

The global 38-dimensional local-sector section is therefore not defined on this residue. Any reported “global minimum-norm lift” obtained by first projecting this residue into the local target sector is merely the near-zero projection and has no interpretive content.

Inside the exceptional eight-point fibre itself, however, solve

\[
\min_{v\in R_8(G_*)}\|v\|
\quad\text{subject to}\quad
D_8v=D_8v_*.
\]

The solution reproduces \(v_*\) with cosine 1 and relative error approximately \(10^{-15}\). Therefore:

\[
\boxed{v_*\text{ is the fibre-local Moore–Penrose preimage of its nonlocal seven-point residue}.}
\]

This uniqueness is relative to the chosen Euclidean inner product. It is a precise linear-algebraic property, not yet a physical canonicality theorem.

---

## 8. Current structural picture

The audited results support the following hierarchy.

### 8.1 Direct state growth

At the ordering level, label insertion is exact and reversible by matching deletion:

\[
DI=\operatorname{id}.
\]

### 8.2 Reconstructive relation growth

At the amplitude-relation level, coefficient copying fails universally in the tested genuine cases:

\[
DI_{\mathrm{naive}}\neq\operatorname{id}.
\]

Nevertheless, at \(7\to8\), a transformed section exists:

\[
DL=\operatorname{id}
\quad\text{on }\mathcal R^{\mathrm{loc}}_7.
\]

Thus:

\[
\boxed{\text{Hamilton-cycle state growth is direct, while amplitude-relation growth is reconstructive}.}
\]

### 8.3 Local and nonlocal ancestry

There are at least two relation-growth modes:

1. **local-to-local ancestry:** each seven-point fibre-local relation has a one-child eight-point ancestor;
2. **local-to-nonlocal residue:** the exceptional eight-point direction descends to a global seven-point relation spanning multiple fibres.

The second mode is a concrete example of why the atlas must be glued in the ambient relation space before projecting into individual fibres.

### 8.4 Two completion mechanisms

Amplitude completeness can be restored by:

- varying factorisation channels within one fixed chart;
- rebuilding the reference chart and its matching local relation spaces.

These are complementary rather than competing mechanisms.

---

## 9. Finite theorem candidates and open conjectures

### 9.1 Finite statement A — anchor-1 exceptional codimension

**Status: R2.** At \(n=9\to8\), anchor-1 collinear residues generate all 15 local relations in 34 target fibres and a 14-dimensional subspace in the unique exceptional fibre \(G_*\).

### 9.2 Finite statement B — fixed-chart channel completion

**Status: C/R1.** In the fixed \(\Pi_1\) chart, cumulative channels 1–5 first recover the exceptional direction; all channels 1–9 generate the complete 1800-dimensional global \(n=8\) relation space.

### 9.3 Finite statement C — true chart completion

**Status: R1.** A genuinely rebuilt \(\Pi_2\) source chart contains the exceptional missing direction, and charts 1 and 2 together raise the corrected cumulative rank from 524 to 525.

### 9.4 Finite statement D — universal failure of coefficient-copy growth

**Status: R2.** Across \(6\to7\), \(7\to8\), and \(8\to9\), unchanged-coefficient insertion succeeds in none of 110 genuine parent-branch cases.

### 9.5 Finite statement E — exact one-child sections at \(7\to8\)

**Status: R2.** Every nonzero seven-point fibre-local relation space admits an exact section supported on a single incident eight-point child fibre.

### 9.6 Finite statement F — full residue-image quotient

**Status: R2.** The delete-8 image of the 525-dimensional eight-point local source has dimension 110, contains the complete 38-dimensional seven-point local sector, and has a 72-dimensional cross-fibre quotient.

### 9.7 Finite statement G — complement-pair channel decomposition

**Status: R2.** The 20 active eight-point fibres form ten complementary pairs. Each pair has a common rank-11 residue image, and the ten pair images form the complete rank-110 residue space.

### 9.8 Finite statement H — rational channel spectrum

**Status: R2 theorem candidate.** Every pair channel has squared spectrum

\[
1^{\times2},\qquad
\left(\frac65\right)^{\times4},\qquad
\left(\frac85\right)^{\times4},\qquad
\left(\frac95\right)^{\times1}.
\]

An analytic derivation remains open.

### 9.9 Atlas-generation hypothesis

**Status: H.** The collection of reference-relative fibre relation spaces, re-anchoring maps, factorisation maps, and growth sections reconstructs invariant amplitude relation content that no one chart or channel displays completely.

### 9.10 Generative-strength alternatives

- **H0 — incidental indexing:** Hamilton cycles only label the trace basis.
- **H1 — comparison scaffold:** the fibre atlas organises genuine amplitude content, while physics resides in the glued output.
- **H2 — generative atlas:** overlap, growth, and factorisation consistency force a nontrivial part of the amplitude structure.

The present evidence supports H1. H2 remains the research target.

---

## 10. Claim boundary

The current work does **not** establish:

- that Hamilton cycles derive Yang–Mills theory;
- that the \(\Pi\)-fibres are physical gauge patches;
- that the Euclidean Moore–Penrose section or the exact 50/50 split is physically preferred;
- that the 30 tested growth orphans are intrinsically parentless;
- that the exceptional relation represents a particle;
- that LR3 dynamics generates the amplitude relations;
- that the rational spectrum or the candidate \(2+4+4+1\) symmetry decomposition has yet been analytically proved.

A particle interpretation remains a later target. The least speculative operational proposal is:

> A particle-like entity would be a stable intermediate sector through which globally glued amplitude content factorises consistently across charts and multiplicities.

No existing fibre is assigned a Standard Model particle label.

---

## 11. Reproducibility ledger

### Foundational and corrected amplitude scripts

- `ehf_amp_found_01_reproduce_amp18_20.py`
  - reproduces local relation bases and the AMP-18 \(34/35+1\) target-rank pattern;
- `amp20b_fixed.py`
  - corrected fixed-chart channels 1+2 test with positive and negative controls;
- `amp20c_all_anchors.py`
  - fixed-chart cumulative channel sweep, closure at channel 5, saturation at rank 1800;
- `ehf_amp_found_01b_true_all_anchor_residue_closure.py`
  - true chart rebuilding; seed-11 closure in chart 2; later SVD convergence failure;
- `ehf_amp_found_01b_true_all_anchor_residue_closure_v2.py`
  - robust span-update patch, full rerun still to be archived.

### Growth geometry and sibling mechanism

- `grow01_insertion.py`
  - exact single-label insertion bijection and branch geometry;
- `amp07_sibling_mechanism.py`
  - middle-block sibling injection, 36-state complement, and relation-space equality mechanism;
- `core_growth_reconciliation.md`
  - unified middle-block versus anchor-composite child laws.

### Growth–factorisation probes

- `ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py`
  - reflection-aware residues, vacuity-safe lift counts, seeds 11 and 29;
- `ehf_amp_found_02b_minimal_nontrivial_growth_sections.py`
  - explicit Moore–Penrose sections, locality audit, exceptional-fibre audit, seeds 11 and 29.
- `ehf_amp_found_02c_branch_reversal_full_image_sections.py`
  - full rank-110 residue-image section, 38+72 quotient, exact branch-reversal covariance, seeds 11 and 29;
- `ehf_amp_found_02d_exact_residue_spectrum_two_fibre_gluing.py`
  - ten complement-pair channels, rational spectrum, channelwise local/nonlocal law, and universal two-fibre minimum-norm audit, seeds 11 and 29.

### Numerics rules now mandatory

1. carry the reflection character through every recanonicalisation;
2. exclude zero-dimensional spaces from success denominators;
3. distinguish global relation validity from fibre-local containment;
4. never use an untruncated wide QR basis for span membership;
5. report rank, singular gap, positive control, and negative control;
6. distinguish a valid section from a chosen “natural” section;
7. distinguish metric-independent subspace statements from Euclidean Moore–Penrose statements;
8. do not call a numerically exact rational spectrum a theorem before an analytic derivation.

---

## 12. EHF-AMP-FOUND-02C: Branch-reversal equivariance and the full residue image

### 12.1 Exact section on the complete image — **R2**

The reflection-aware delete-8 map on the 525-dimensional eight-point fibre-local source has

\[
\operatorname{rank}D_8=110,
\qquad
\dim\ker D_8=415.
\]

A rank-truncated Moore--Penrose section was constructed on the complete residue image

\[
\mathcal I_7=\operatorname{im}D_8,
\qquad
\dim\mathcal I_7=110,
\]

and satisfies

\[
D_8L_{110}=\operatorname{id}_{\mathcal I_7}
\]

to residuals between approximately \(10^{-15}\) and \(10^{-14}\) at seeds 11 and 29. Fresh Parke--Taylor validations remain at approximately \(10^{-13}\).

### 12.2 Local/nonlocal quotient — **R2**

The complete seven-point fibre-local sector has dimension 38 and is contained in \(\mathcal I_7\). Therefore

\[
\dim\left(\mathcal I_7/\mathcal R^{\mathrm{loc}}_7\right)=110-38=72.
\]

Using the standard Euclidean target metric gives an orthogonal representative

\[
\mathcal I_7
=
\mathcal R^{\mathrm{loc}}_7\oplus\mathcal N_7,
\qquad
38+72=110.
\]

The quotient dimension 72 is basis-independent. The particular orthogonal complement \(\mathcal N_7\) is metric-dependent.

### 12.3 Branch-reversal equivariance — **E/R2**

In the standard canonical chart, the largest label 8 cannot occur immediately after anchor 1, so

\[
\operatorname{rank}D_+=0,
\qquad
\operatorname{rank}D_-=110.
\]

Under the opposite canonical representative convention, the active side swaps. With signed reversal operators \(J_8\) and \(J_7\), the computed identities are

\[
D^{\mathrm{opp}}_+=J_7D^{\mathrm{std}}_-J_8^{-1},
\]

\[
D^{\mathrm{opp}}_-=J_7D^{\mathrm{std}}_+J_8^{-1},
\]

\[
D^{\mathrm{opp}}=J_7D^{\mathrm{std}}J_8^{-1},
\]

with relative Frobenius error exactly zero in both corrected runs. The successful one-sided section swaps with the chart.

Hence

\[
\boxed{\text{the plus/minus asymmetry is a canonical-chart effect, not detected physical chirality}.}
\]

### 12.4 Exceptional residue in the full image — **R2**

The AMP-18 exceptional direction \(v_*\) satisfies

\[
D_8v_*\in\mathcal I_7,
\qquad
D_8v_*\perp\mathcal R^{\mathrm{loc}}_7,
\qquad
D_8v_*\in\mathcal N_7
\]

within numerical precision. Thus it is fibre-local upstairs but purely cross-fibre downstairs.

Its unrestricted global minimum-norm ancestor has

\[
\|v_{\mathrm{MP}}^{\mathrm{global}}\|=\frac1{\sqrt2},
\qquad
\cos(v_*,v_{\mathrm{MP}}^{\mathrm{global}})=\frac1{\sqrt2},
\]

and is supported equally on two eight-point fibres. The difference

\[
v_*-v_{\mathrm{MP}}^{\mathrm{global}}
\]

lies in \(\ker D_8\). Within the exceptional fibre alone, \(v_*\) remains the unique Euclidean minimum-norm preimage of its residue.

---

## 13. EHF-AMP-FOUND-02D: Exact residue spectrum and two-fibre gluing law

### 13.1 Rational spectrum — **R2 theorem candidate**

For

\[
K=D_8P_{\mathcal R^{\mathrm{loc}}_8}D_8^{\mathsf T}=AA^{\mathsf T},
\]

restricted to its rank-110 image, the squared singular values reproduce at two independent kinematic seeds as

\[
1^{\times20},
\qquad
\left(\frac65\right)^{\times40},
\qquad
\left(\frac85\right)^{\times40},
\qquad
\left(\frac95\right)^{\times10}.
\]

The maximum deviation from the candidate rational values is below \(4.0\times10^{-15}\). The candidate minimal polynomial

\[
K(K-I)
\left(K-\frac65I\right)
\left(K-\frac85I\right)
\left(K-\frac95I\right)=0
\]

has relative numerical residual below \(1.6\times10^{-17}\), and the first five rational trace moments agree to approximately \(10^{-12}\).

This is a numerically exact theorem candidate. An analytic derivation is still required.

### 13.2 Complementary active-fibre pairs — **E/R2**

The 35 eight-point fibres split into 20 active fibres and 15 inactive fibres contained in the delete-8 kernel. An active fibre is indexed by a three-subset

\[
S\subset\{2,3,4,5,6,7\},
\qquad |S|=3,
\]

through anchor set \(\{1\}\cup S\). Complementation \(S\leftrightarrow S^c\) pairs the active fibres into

\[
\frac12\binom63=10
\]

unordered pairs.

For every pair \(F,\phi(F)\),

\[
\operatorname{rank}A_F=\operatorname{rank}A_{\phi(F)}=11,
\]

and

\[
\operatorname{im}A_F=\operatorname{im}A_{\phi(F)}.
\]

The ten common images form the complete residue space:

\[
\mathcal I_7=\bigoplus_{j=1}^{10}\mathcal C_j,
\qquad
\dim\mathcal C_j=11,
\qquad
110=10\times11.
\]

In the standard target metric, these ten channels are mutually orthogonal to numerical precision.

### 13.3 Universal channel spectrum — **R2 theorem candidate**

Every pair channel has squared spectrum

\[
1^{\times2},
\qquad
\left(\frac65\right)^{\times4},
\qquad
\left(\frac85\right)^{\times4},
\qquad
\left(\frac95\right)^{\times1}.
\]

Each single active fibre has exactly half of this operator spectrum:

\[
\left(\frac12\right)^{\times2},
\qquad
\left(\frac35\right)^{\times4},
\qquad
\left(\frac45\right)^{\times4},
\qquad
\left(\frac9{10}\right)^{\times1}.
\]

Ten identical pair channels explain the global multiplicities \(20,40,40,10\).

### 13.4 Channelwise local/nonlocal law — **R2**

The local dimensions of the ten channels are

\[
11,7,4,4,4,4,1,1,1,1,
\]

and their complementary cross-fibre dimensions are

\[
0,4,7,7,7,7,10,10,10,10.
\]

For every channel,

\[
\dim\left(\mathcal C_j\cap\mathcal R^{\mathrm{loc}}_7\right)
=
\sum_{P\text{ reached by }\mathcal C_j}\dim R_7(P).
\]

The local dimensions sum to 38 and the nonlocal dimensions sum to 72.

The local-sector projector does not commute with \(K\): the normalized commutator error is approximately

\[
0.0988445527.
\]

Therefore the rational spectral eigenspaces do not simply coincide with the local/nonlocal split.

### 13.5 Universal two-fibre minimum-norm law — **R2, metric-qualified**

For every complementary pair, the two fibres induce the same target image and the same source preimage metric. Relative to the standard Euclidean coefficient metric, the pair-restricted Moore--Penrose ancestor of every channel vector divides its squared norm equally:

\[
\frac{\|x_F\|^2}{\|x_F\|^2+\|x_{\phi(F)}\|^2}=\frac12.
\]

This succeeds for all ten pairs with maximum numerical error below \(4.5\times10^{-16}\). The equal-image and rank statements are metric-independent; the exact 50/50 split is metric-qualified.

### 13.6 AMP-18 exceptional direction is a generic pair instance — **R2**

The exceptional fibre

\[
E=\{1,4,5,6\},\qquad O=\{2,3,7,8\}
\]

is paired with

\[
E=\{1,2,3,7\},\qquad O=\{4,5,6,8\}.
\]

The pair-only minimum-norm ancestor agrees with the unrestricted global minimum-norm ancestor to approximately \(2\times10^{-15}\), and its support is exactly the two complementary fibres with squared weights \(1/2,1/2\).

Hence the AMP-18 direction is exceptional only in the fixed-chart arrival audit. Its growth--factorisation mechanism is a generic instance of the universal complement-pair law.

---

## 14. Next mathematical target

The next task is:

# EHF-AMP-FOUND-02E
## Complement-Pair Symmetry Decomposition and Proof Certificate

The numerical spectrum is now sufficiently rigid that further random-seed tests have little value. The next target is an analytic explanation.

The active fibres are indexed by the middle layer of the six-cube,

\[
\binom{\{2,3,4,5,6,7\}}{3},
\]

modulo the antipodal involution \(S\sim S^c\). The permutation group \(S_6\) acts transitively on the ten complement pairs. For a reference pair, the stabilizer is expected to be

\[
H\cong(S_3\times S_3)\rtimes C_2,
\qquad |H|=72.
\]

The proof programme should establish:

1. exact covariance of the ten channels under the signed \(S_6\) action;
2. invariance of one reference channel under \(H\);
3. a multiplicity-free decomposition of its 11-dimensional target representation into dimensions
   \[
   2+4+4+1;
   \]
4. scalar action of the channel operator on those four irreducible sectors;
5. exact eigenvalues \(1,6/5,8/5,9/5\);
6. transport of the reference-channel result to all ten channels by label permutation;
7. a combinatorial derivation of the parent-dimension local/nonlocal law.

The associated computational probe should produce a symmetry certificate, not claim to replace the analytic proof. It should test the stabilizer size, channel covariance, commutant dimension, character norm, spectral-projector ranks, and irreducibility of the four candidate blocks.

The decisive target is

\[
\boxed{
\mathcal C
\cong V_2\oplus V_4^{(a)}\oplus V_4^{(b)}\oplus V_1,
\qquad
K|_{\mathcal C}
=1P_2+\frac65P_{4a}+\frac85P_{4b}+\frac95P_1.
}
\]

---

## 15. Current thesis

The current, corrected thesis is:

> Hamilton-cycle orderings provide anchor-relative comparison scaffolds for amplitude relations. State growth is a direct insertion process, but amplitude-relation growth is reconstructive: unchanged coefficients never suffice in the genuine cases tested, while exact transformed sections exist and can remain supported on a single child fibre. The reflection-aware \(8	o7\) residue image is a 110-dimensional glued relation space containing a 38-dimensional fibre-local sector and a 72-dimensional cross-fibre quotient. Its active source fibres organize into ten complementary pairs, each producing the same rank-11 channel type and the same numerically exact four-level rational spectrum. The AMP-18 direction is a generic instance of this two-fibre gluing law. These results support an amplitude-atlas interpretation and a concrete symmetry-proof programme, but not yet a derivation of physical gauge theory.

