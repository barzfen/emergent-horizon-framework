# EHF-AMP-FOUND-01
## Anchor-Relative Scaffolds and Global Amplitude Content

**Version:** 0.3 — adds recovered AMP-18–23 source audit and exact n=9→8 geometric incidence ledger  
**Status:** Internal EHF/RAF theory note  
**Purpose:** To formalise the strongest current amplitude interpretation of the Hamilton-cycle work before designing further probes.

---

## 0. Working rule hierarchy

This note keeps four structures separate.

1. **Hamilton-cycle ordering space**
   \[
   X_n=\{\text{canonical Hamilton cycles on }K_n\}/\text{dihedral identification}.
   \]
   This state set is independent of any chosen local move rule.

2. **Anchor-relative parity data**
   For each reference label (anchor) \(a\), cyclic orderings are written with \(a\) first and grouped by the corresponding parity-position label \(\Pi_a\). These groups will be called **RAF \(\Pi\)-fibres** in this note, avoiding ambiguity with the standard amplitudes use of “chamber.”

3. **Local CBB dynamics**
   The foundational CBB move rule is **LR3 only**. OPW3 is the minimal \(\Pi\)-preserving diagnostic derived from LR3. Results obtained with LR23/OPW23 are retained only as enriched diagnostics unless they are independently re-established for LR3/OPW3.

4. **Amplitude structure**
   Parke–Taylor, KK, BCJ, KLT/momentum-kernel and collinear-factorisation structures are defined on the ordering space. Many of these results depend on the ordering and \(\Pi\)-fibre structure, not on graph connectivity under LR3 or LR23.

The first task is therefore to extract the **move-independent amplitude spine** from the older chamber language.

---

## 1. Starting observation

The number of canonical Hamilton cycles is

\[
|X_n|=\frac{(n-1)!}{2}.
\]

This is also the number of colour orderings of an \(n\)-point tree amplitude modulo cyclicity and reflection. Accordingly, the Hamilton-cycle ordering space can be identified with the reflection-reduced trace-ordering basis.

For odd \(n\), colour-ordered partial amplitudes are reflection-odd sections over this basis.

This is an exact identification of indexing structures. It does not yet imply that Hamilton cycles generate gauge theory.

---

## 2. The anchor-relative amplitude atlas

For every anchor \(a\in[n]\), define an anchored presentation

\[
X_n^{(a)}
\]

by rotating each cyclic ordering so that \(a\) is first and then applying the canonical reflection convention.

The anchor determines a partition

\[
\mathcal P_{n,a}=\{F_{n,a,\xi}\}_{\xi}
\]

where each \(F_{n,a,\xi}\subset X_n^{(a)}\) is a \(\Pi_a\)-fibre.

The individual fibres depend on the reference. A cyclic re-anchoring generally scatters one fibre across many fibres of the new anchor. Therefore the fibre decomposition is not itself an anchor-independent physical object.

However, the multiset of fibre sizes and amplitude-relation dimensions can remain invariant under re-anchoring. This motivates the distinction:

\[
\boxed{\text{anchor-relative scaffold} \neq \text{anchor-independent content}.}
\]

---

## 3. Linear amplitude data

Let

\[
\mathcal C_n=\mathbb C^{X_n}
\]

be the coordinate space on the reflection-reduced ordering basis.

### 3.1 Constant-coefficient amplitude layer

Let \(\mathcal E_n^{\mathrm{PT}}\) denote the Parke–Taylor evaluation map into the space of rational functions of generic kinematics. Define the global constant-coefficient relation space

\[
R_n^{\mathrm{KK}}=\ker \mathcal E_n^{\mathrm{PT}}.
\]

For an anchor-relative fibre \(F\), define its local relation space

\[
R_{n,a,F}^{\mathrm{KK}}
=
R_n^{\mathrm{KK}}\cap \mathbb C^F,
\]

where \(\mathbb C^F\) denotes vectors supported only on \(F\).

### 3.2 Kinematics-dependent BCJ layer

At generic fixed kinematics, let \(V_n\subset \mathcal C_n^*\) be the BCJ-reduced span supplied by the bi-adjoint double-partial matrix. Its dimension is

\[
\dim V_n=(n-3)!.
\]

The fibre-restricted BCJ rank measures how much of this global span is visible on one reference-relative fibre. The observed rank deficits show that the \(\Pi\)-fibre grouping is non-generically aligned with the BCJ/momentum-kernel layer.

This alignment is stronger evidence than a generic graph quantum walk because it concerns the kinematics-dependent relation structure used in factorisation and KLT.

---

## 4. Re-anchoring maps

For anchors \(a,b\), cyclic relabelling and recanonicalisation induce a linear permutation map

\[
\rho_{a\to b}:\mathcal C_n^{(a)}\longrightarrow\mathcal C_n^{(b)}.
\]

The map preserves the global amplitude relation space but generally does not preserve individual \(\Pi\)-fibres:

\[
\rho_{a\to b}\bigl(R_{n,a,F}^{\mathrm{KK}}\bigr)
\not\subseteq
R_{n,b,G}^{\mathrm{KK}}
\]

for any single target fibre \(G\) in general.

Thus one reference chart can reveal only part of a relation in a fibre-local form. A different anchor may reveal a direction hidden by the first chart.

The AMP factorisation gap resolved by changing from anchor 1 to anchor 2 is the current concrete model of this phenomenon.

---

## 5. Factorisation maps

For a collinear channel involving the anchor \(a\) and another leg \(j\), define a residue/deletion map

\[
\partial_{a,j}:R_n^{\mathrm{KK}}\longrightarrow R_{n-1}^{\mathrm{KK}}.
\]

On a single Parke–Taylor term, the pole selects orderings in which the two legs are adjacent and deletes the collinear leg after removing the common polar factor.

For the anchor’s own channel, the \(\Pi\)-fibre geometry is single-valued under this deletion in the audited cases: a source fibre maps to one target fibre. Interior deletions without the corresponding pole scatter broadly and do not respect the fibre decomposition.

Therefore the relevant compatibility is not arbitrary deletion but **factorisation-selected deletion**.

---

## 6. First formal target: all-anchor residue generation

The first theorem-shaped target should be stated locally and modestly.

### 6.1 Common-coordinate residue span

Choose one target anchor \(b\) only to provide a common coordinate presentation of
\(\mathcal C_{n-1}\). For every source anchor \(a\), transport each legitimate
anchor-channel residue into that common target coordinate space. Define the full
all-anchor residue span

\[
\mathcal I_{n\to n-1}^{(b)}
=
\operatorname{span}
\left\{
\rho_{a\to b}^{(n-1)}\,\partial_{a,j}(r)
:
\begin{array}{l}
 a\in[n],\\
 j\ne a,\\
 F\in\mathcal P_{n,a},\\
 r\in R_{n,a,F}^{\mathrm{KK}},\\
 (a,j)\text{ is an anchor-collinear channel}
\end{array}
\right\}.
\]

For a target \(\Pi_b\)-fibre \(G\), define the fibre-local content recovered by
all anchors as

\[
\mathcal G_{n\to n-1}(b,G)
=
R_{n-1,b,G}^{\mathrm{KK}}
\cap
\mathcal I_{n\to n-1}^{(b)}.
\]

This intersection formulation is essential. After re-anchoring, a residue vector
need not remain supported in one \(b\)-fibre, and its individual fibre projections
need not themselves be amplitude relations. The invariant local relation may be
reconstructed only after components from several reference charts cancel in the
common ambient coordinate space.

### 6.2 All-Anchor Residue Generation Conjecture

For the physically allowed collinear channels,

\[
\boxed{
\mathcal G_{n\to n-1}(b,G)
=
R_{n-1,b,G}^{\mathrm{KK}}.
}
\]

Interpretation: no single reference chart need generate the full target relation
space in a fibre-local form, but the ambient span of residues from all reference
charts does.

The audited \(n=9\to8\) result, in which anchor 1 generated 14 of 15 target
directions in one exceptional fibre and anchor 2 supplied the missing ambient
direction, is the first supporting example.

### Failure conditions

The conjecture fails if, after all anchors and all legitimate channels are included:

- a nonzero target fibre-local relation remains outside the common-coordinate residue span;
- the missing dimension persists under re-anchoring;
- generation depends on a non-factorising deletion;
- the result is only a generic dimension count and not supported by exact or stable rank gaps.

---

## 7. Atlas-gluing hypothesis

The broader hypothesis is:

> Reference-relative \(\Pi\)-fibres are comparison charts. Their individual memberships are scaffold-dependent, but their amplitude relations, re-anchoring maps and factorisation maps glue into anchor-independent content.

This should be developed first as linear algebra, without importing sheaf or category terminology prematurely.

A minimal atlas object at fixed \(n\) is

\[
\mathfrak A_n
=
\left(
\{\mathcal P_{n,a}\}_{a\in[n]},
\{R_{n,a,F}^{\mathrm{KK}}\},
\{R_{n,a,F}^{\mathrm{BCJ}}\},
\{\rho_{a\to b}\},
\{\partial_{a,j}\}
\right).
\]

The candidate invariant content is not one fibre but a quantity preserved or reconstructible across the full atlas.

Examples already suggested by the AMP work include:

- the global KK and BCJ dimensions;
- fibre-level rank invariants;
- the multiset of \((|F|,\dim R_{n,a,F})\);
- all-anchor factorisation closure;
- sibling relation equality under growth;
- anchor-independent spectra of scaffold statistics.

---

## 8. Three competing interpretations

### H0 — Incidental indexing

Hamilton cycles merely index the trace basis. The \(\Pi\)-fibre structure has no intrinsic amplitude significance beyond accidental finite-rank coincidences.

### H1 — Comparison scaffold

The \(\Pi\)-fibres form an anchor-relative organisational scaffold that exposes genuine amplitude relation and factorisation structure, while invariant physics resides only in the glued output.

This is the strongest interpretation currently supported by the evidence.

### H2 — Generative amplitude atlas

The overlap, re-anchoring, growth and factorisation consistency conditions of the relational atlas force a nontrivial part of the amplitude relation structure.

This is the ambitious EHF hypothesis. It is not yet established.

The research objective is to determine whether H1 can be strengthened toward H2, while retaining H0 as a live falsification alternative.

---

## 9. First particle interpretation

Particle identification should be deferred until the amplitude atlas is defined. The first top-down candidate is not “one Hamilton cycle equals one particle.”

A better working hypothesis is:

> A particle-like entity is a stable intermediate sector through which the global amplitude atlas factorises consistently across anchors and multiplicities.

In an ordinary amplitude, a particle is operationally visible through a pole and residue decomposition. In EHF language, the corresponding object would need:

- a repeatable factorisation channel;
- an anchor-independent intermediate label;
- consistent lower-point composition;
- a stable pole or spectral parameter;
- conserved representation data carried through the channel.

The electron, photon and other species should be considered only after such generic channel identity is understood.

---

## 10. Dependency ledger

### Move-independent or primarily ordering-dependent

- Hamilton-cycle / colour-ordering trace-basis identification.
- Reflection parity of odd-\(n\) partial amplitudes.
- Definition of anchor-relative \(\Pi\)-fibres.
- KK and BCJ global dimensions.
- Fibre-restricted amplitude ranks and relation spaces.
- Re-anchoring covariance/scattering.
- Collinear residue maps.
- Anchor-invariant multiset of fibre size/relation-count pairs.
- Fibre-union rank laws.

### Growth-dependent but not necessarily local-move-dependent

- core insertion ancestry of \(\Pi\)-fibres;
- sibling size pairing;
- sibling relation equality, after rewriting the result in fibre rather than graph-component language.

These must be checked carefully to ensure the statement does not rely on LR23 connectivity.

### Local-dynamics-dependent

- identification of \(\Pi\)-fibres with connected chambers;
- chamber spectra;
- slow modes;
- packet retention and MSM dynamics;
- heat-kernel dimension;
- growth-lift of eigenmodes;
- transport and response claims.

For current foundational CBB work, these use LR3/OPW3. LR23/OPW23 results remain enriched diagnostics only.

---

## 11. Immediate theory tasks

### Task A — Rewrite the amplitude programme in fibre language

Replace every use of “OPW chamber” in an amplitude statement by one of:

- \(\Pi\)-fibre, when only membership is used;
- LR3/OPW3 connected component, when connectivity is essential;
- LR23/OPW23 enriched component, when the result genuinely uses the older enriched dynamics.

### Task B — Build the anchor–fibre–residue diagram

For the audited \(n=9\to8\) case, write an explicit diagram recording:

- source anchor;
- source fibre;
- source local relation dimension;
- collinear channel;
- target fibre;
- residue-image rank;
- missing target directions;
- which re-anchor supplies each missing direction.

### Task C — State the exact current theorem

The initial exact statement should be limited to the audited finite cases. It should not claim the all-\(n\) conjecture.

### Task D — Identify invariant outputs

Separate quantities that are:

1. invariant under re-anchoring;
2. covariant but scaffold-dependent;
3. genuinely anchor-dependent artifacts.

### Task E — Do not introduce particles yet

Use factorisation-channel language only as a theory target. Do not assign electron, photon or quark labels to existing fibres or modes.

---

## 12. Initial thesis

The current theory thesis is:

> Hamilton-cycle orderings provide reference-relative comparison charts for amplitude data. The \(\Pi\)-fibre decomposition is not itself invariant, but its relation spaces, factorisation maps and re-anchoring structure may reconstruct invariant amplitude content. The first task is to formalise and test this all-anchor gluing mechanism. Only after that should EHF attempt to interpret stable factorisation sectors as particle-like entities.

---

## Source ledger for this draft

- `amplitude_program_current_amp23.pdf` — trace-basis identification, KK/BCJ fibre laws, factorisation, anchor dependence, re-anchoring closure, anchor-invariant spectrum.
- `cbb_P_series_1_to_9B.pdf` — current hierarchy LR3/OPW3 foundation versus LR23/OPW23 enriched diagnostic.
- `raf_core_c_hamilton_cycle_sector_fiber_clean.md` — distinction between full 2-opt Core C and reduced parity-sector structures.
- `relational_atlas_framework_exact_johnson_transport_core.pdf` — exact reduced Johnson transport layer.
- `raf_odd_preserve_world_chamber_and_boundary_dynamics_v6.md` — historical LR2+LR3 chamber and packet record requiring dependency separation.



---

## 13. Audited finite diagram: \(n=9\to8\)

This section records the compressed exact anchor–fibre–residue diagram already
contained in AMP-18 through AMP-20. It is a theorem-level finite-case ledger of
the reported computations. It is not yet the full 69-by-35 source/target incidence
table.

### 13.1 Target layer

Fix target anchor 1. At \(n=8\), the audited decomposition has

\[
35\text{ target }\Pi_1\text{-fibres}.
\]

Every target fibre \(G\) has

\[
|G|=72,
\qquad
\dim R_{8,1,G}^{\mathrm{KK}}=15.
\]

Thus the target layer consists of 35 equal 72-coordinate charts, each carrying
the same 15-dimensional even-point relation module.

### 13.2 Anchor-1 source-to-target geometry

At \(n=9\), let \(B\) be a source \(\Pi_1\)-fibre and let \(j\) be a leg
that becomes collinear with anchor 1 in the anchor channel. The pole-selected
deletion map is single-valued on the scaffold:

\[
\delta_{1,j}:B\longrightarrow G(B,j)
\]

for one target \(n=8\) fibre \(G(B,j)\). The induced map on local relation spaces is

\[
(\delta_{1,j})_*:
R_{9,1,B}^{\mathrm{KK}}
\longrightarrow
R_{8,1,G(B,j)}^{\mathrm{KK}}.
\]

The branch sign is \(+1\) when the collinear leg lies immediately after the
anchor and \(-1\) when it lies immediately before the anchor. After removing the
uniform polar factor, the residue map agrees with the direct collinear limit to
approximately \(10^{-20}\) in the audit.

For each target fibre \(G\), collect all anchor-1 residue images landing in \(G\):

\[
I_1(G)=
\operatorname{span}
\left\{
(\delta_{1,j})_*r:
G(B,j)=G,
\ r\in R_{9,1,B}^{\mathrm{KK}}
\right\}.
\]

### 13.3 Rank ledger

The exact target-rank summary is:

| Target class | Number of target fibres | Target relation dimension | Anchor-1 residue rank | Codimension |
|---|---:|---:|---:|---:|
| Regularly generated targets | 34 | 15 | 15 | 0 |
| Exceptional target \(G_*\) | 1 | 15 | 14 | 1 |

For the 34 regularly generated targets, the span residual against the complete
target relation space is approximately \(10^{-13}\).

The unique exceptional target is

\[
G_*:
\qquad
E=\{1,4,5,6\},
\qquad
O=\{2,3,7,8\}.
\]

For this target,

\[
\dim I_1(G_*)=14,
\qquad
\dim R_{8,1,G_*}^{\mathrm{KK}}=15,
\]

with a clean singular-value gap of approximately 14 decades. Let

\[
v_*\in R_{8,1,G_*}^{\mathrm{KK}}
\]

span the one-dimensional quotient

\[
R_{8,1,G_*}^{\mathrm{KK}}/I_1(G_*).
\]

### 13.4 Anchor-2 completion

Re-anchor the \(n=9\) source orderings at leg 2. Take all anchor-2 collinear
residues of anchor-2-local source relations and transport the resulting full
\(n=8\) relation vectors back into the common anchor-1 coordinate presentation.
Let their ambient span be \(I_2^{\mathrm{full}}\).

The AMP-20 audit found

\[
v_*
\in
I_1^{\mathrm{full}}+I_2^{\mathrm{full}}
\]

with residual

\[
1.3\times10^{-15}.
\]

Consequently,

\[
\dim\left(
R_{8,1,G_*}^{\mathrm{KK}}
\cap
(I_1^{\mathrm{full}}+I_2^{\mathrm{full}})
\right)=15.
\]

Anchor 2 therefore contributes exactly one new quotient direction relative to the
14-dimensional anchor-1 image on \(G_*\). The completion may require cancellation
between components that are not individually local in the anchor-1 fibre scaffold;
this is why the common-coordinate intersection definition in Section 6 is required.

### 13.5 Diagram

```text
                    n = 9 source ordering space

        anchor 1 chart                           anchor 2 chart
   {Pi_1-fibres B, local R_9(B)}            {Pi_2-fibres B', local R_9(B')}
             |                                         |
             | anchor-1 collinear residues             | anchor-2 collinear residues
             | single-valued on Pi_1 scaffold          | full vectors after re-anchoring
             v                                         v

       34 ordinary target fibres G              ambient n=8 relation space
       rank I_1(G) = 15/15                              |
                                                        | supplies v_*
       exceptional target G_*                          |
       E={1,4,5,6}, O={2,3,7,8}                        |
       rank I_1(G_*) = 14/15  <-------------------------+
                  |
                  | combine anchor-1 and anchor-2 residue spans
                  v
       rank on R_8(G_*) = 15/15
```

The compressed global conclusion is

\[
\boxed{
\forall G\in\mathcal P_{8,1},
\quad
R_{8,1,G}^{\mathrm{KK}}
\subseteq
I_1^{\mathrm{full}}+I_2^{\mathrm{full}}.
}
\]

Equivalently, anchors \(\{1,2\}\) suffice to generate every one of the 35
anchor-1 target-fibre relation spaces in the audited \(9\to8\) case.

### 13.6 Negative control

The scaffold compatibility is specific to pole-selected factorisation. Deleting an
interior label that is not adjacent to the anchor, and therefore has no corresponding
collinear pole, scatters one \(n=9\) source fibre across 34 of the 35 target fibres.
Thus

```text
anchor-channel residue:
  source fibre -> one target fibre

interior non-pole deletion:
  source fibre -> almost the entire target partition
```

The single-valued fibre map is therefore not generic deletion bookkeeping; it tracks
the pole structure of the Parke–Taylor functions.

### 13.7 Finite theorem statement

**Theorem — Two-anchor generation at \(n=9\to8\), audited finite case.**

In the reported Parke–Taylor relation audit:

1. every anchor-1 \(n=9\) source fibre maps under each anchor-1 collinear
   residue channel to one anchor-1 \(n=8\) target fibre;
2. anchor-1 residue images generate the full 15-dimensional local relation
   space for 34 of the 35 target fibres;
3. on the exceptional target
   \(E=\{1,4,5,6\}, O=\{2,3,7,8\}\), anchor 1 generates a
   14-dimensional subspace;
4. the unique missing local relation direction lies in the ambient span obtained
   after adding anchor-2 collinear residues, with residual
   \(1.3\times10^{-15}\).

Therefore the complete collection of anchor-1 target-fibre relation spaces is
generated by factorisation residues from the two source anchors \(1\) and \(2\).

### 13.8 What remains unavailable in the summary archive

The current PDF records the exact target ranks and the exceptional target, but it
does not print the complete source-level incidence ledger

\[
(B,j,r(B),G(B,j),\operatorname{rank}(\delta_{1,j})_*).
\]

Producing the full expanded diagram requires extracting the result rows from
`amp18_factorization.py`, `amp18f_f2_clean.py`, `amp18h_gap.py`, and
`amp20_gap_dissolve.py`. This is a bookkeeping expansion of the established finite
result, not a new physical hypothesis.

### 13.9 Theoretical consequence

The finite case exhibits a genuine atlas-gluing pattern:

\[
\text{one chart gives a codimension-one local view}
\quad+
\text{a second chart supplies the missing ambient direction}
\quad\Longrightarrow\quad
\text{complete invariant relation content}.
\]

This is presently the cleanest concrete model for the EHF statement that
reference-relative comparison scaffolds may collectively reconstruct content that no
single scaffold displays completely.


---

## 14. Recovered AMP-18–23 source bundle audit

The recovered archives contain the scripts underlying AMP-18 through AMP-23 and successive snapshots of the AMP v3 note.

The files directly relevant to the anchor–fibre–residue construction are:

- `amp18_factorization.py`: anchor-channel deletion/factorisation geometry;
- `amp18b_control.py`: physical-pole deletion versus interior non-pole deletion;
- `amp18f_f2_clean.py`: target-relation generation by source residue images;
- `amp18h_gap.py`: identification and seed-stability of the exceptional `14/15` target fibre;
- `amp19_cyclic_cov.py`: reflection covariance and cyclic re-anchoring scatter;
- `amp20_gap_dissolve.py`: anchor-2 recovery of the missing target direction;
- `amp21_invariance_audit.py`: anchor-invariance of the fibre `(size, relation-dimension)` spectrum;
- `amp22_decisive.py`, `amp22b_sn_decomp.py`, and `amp23_branching.py`: comparison with global symmetric-group data and closure of the branching caveat.

The archives are source bundles, not complete run directories. They do not contain raw logs, cached nullspaces, CSV outputs, or the imported helper `replicate_opw.py`. The canonicalisation and parity-position helper was reconstructed directly from the documented definitions, allowing the light geometric layer to be rerun independently.

### 14.1 Independently rerun geometric results

The recovered light scripts reproduce:

1. At `n=9 -> 8`, there are exactly 69 source fibres and 35 target fibres.
2. Every anchor-collinear source-fibre/channel map is single-valued on the target-fibre scaffold.
3. Interior non-pole deletion can scatter one source fibre over 34 of the 35 target fibres.
4. Reflection maps fibres cleanly, while cyclic re-anchoring scatters them; at `n=9` the maximum target valence is 55.

This independently restores the geometric part of the factorisation diagram without relying only on the prose record.

### 14.2 Exact finite incidence ledger

The recovered `n=9 -> 8` geometry gives an exact ledger with 448 nonempty source-fibre/channel rows. Each row records:

\[
(\text{source fibre},\ j,\ \text{right/left polar counts},\ \text{target fibre}).
\]

It also gives two exact `69 x 35` incidence matrices:

- number of factorisation channels connecting each source fibre to each target fibre;
- number of contributing polar states connecting each source fibre to each target fibre.

Across all rows, the total directed polar-state count is

\[
40320.
\]

Each of the 35 target fibres has size 72 and receives total polar count 1152. The number of source-channel arrivals varies, but every target is covered.

### 14.3 Rank layer status

The source code for the heavy Parke–Taylor nullspace and residue-rank computations is present, but cached numerical outputs are absent. The current target-rank ledger therefore distinguishes:

- **independently rerun geometry**, recorded by the exact incidence files;
- **recorded AMP rank result**, namely `15/15` for 34 fibres and `14/15` for the exceptional fibre under anchor 1;
- **recorded AMP-20 closure**, where anchor 2 supplies the missing ambient direction with residual `1.3e-15`.

A fresh full nullspace rerun is a separate reproducibility task and should not be silently conflated with the recovered geometric audit.

### 14.4 Consequence for the atlas hypothesis

The recovered source code strengthens the intended interpretation:

\[
\boxed{\text{factorisation selects a single target chart, while arbitrary deletion does not.}}
\]

The atlas compatibility is therefore tied to the pole/residue operation, not merely to deleting one label from a cyclic ordering.
