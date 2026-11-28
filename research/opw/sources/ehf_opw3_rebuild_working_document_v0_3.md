# EHF OPW3 Rebuild — Working Document

**Programme:** Emergent Horizon Framework  
**Branch:** Odd Preserve World rebuilt under LR3 only  
**Version:** 0.3  
**Date:** 25 July 2026  
**Status:** Living research document

---

## 1. Purpose

This document consolidates the OPW3 reconstruction through **EHF-OPW3-AUDIT-09** and the first LR3-native Hilbert-space audit, **EHF-QM3-01** and fixes the current research baseline before the quantum-mechanics bridge is rebuilt.

The older Odd Preserve World used both length-2 and length-3 circular reversals:

\[
\mathrm{OPW23}=\mathrm{LR2}\cup\mathrm{LR3}.
\]

The corrected programme treats:

- **OPW3** as the foundational LR3-only object;
- **LR2** as an ablation and diagnostic control;
- **OPW23** as an enriched comparison model.

No old OPW23 quantum result will be inherited automatically. Every relevant structure must survive or be reconstructed under LR3.

---

## 2. Definition lock

For odd \(n\):

### 2.1 State space

States are undirected Hamilton cycles on \(K_n\), modulo cyclic rotation and reflection. Internally the labels are

\[
0,1,\ldots,n-1.
\]

Canonicalization:

1. rotate label \(0\) into position \(0\);
2. compare the anchored ordering with its reversal;
3. retain the lexicographically smaller representative.

Therefore

\[
|\Omega_n|=\frac{(n-1)!}{2}.
\]

### 2.2 Preserve label

For a canonical cycle \(c\), \(\Pi(c)\) is the unordered pair of sorted labels appearing in zero-based even and odd positions.

### 2.3 Graphs

- **OPW3:** circular length-3 reversals preserving \(\Pi\);
- **LR2:** circular length-2 reversals preserving \(\Pi\);
- **OPW23:** union of the LR2 and LR3 preserve edges.

### 2.4 Interpretation guardrails

At this stage:

- normalized-Laplacian modes are structural diffusion modes;
- stochastic actions are transition costs;
- growth maps are combinatorial insertion/deletion maps;
- no mode is identified with a physical particle;
- no growth step is identified with Planck time;
- no stochastic action is yet a quantum action.

---

## 3. Audit ledger

| Audit | Title | Result |
|---|---|---|
| OPW3-AUDIT-01 | Definition Lock and Matched Structural Census | PASS |
| OPW3-AUDIT-02 | Square-Complex and Active-Signature Projection Survival | PASS |
| OPW3-AUDIT-03 | Normalized-Laplacian Slow-Sector Survival | PASS |
| OPW3-AUDIT-04 | Canonical Growth Retraction and LR3 Edge-Channel Decomposition | PASS |
| OPW3-AUDIT-05 | LR3-Native Equitable Packet Reconstruction | PASS |
| OPW3-AUDIT-06 | Packet-Closure Equivalence, Spectral Completeness and Action Census | PASS |
| OPW3-AUDIT-07 | Hidden Slow-Sector Families and Minimal Completion | PASS |
| OPW3-AUDIT-08 | Residual Completion by LR3 Edge Labels and Growth History | PASS |
| OPW3-AUDIT-09 | Growth-Descriptor Chart Covariance | PASS |

---

# Part I — Foundational OPW3 structure

## 4. Audit-01: chamber reconstruction

### 4.1 Exact census

| \(n\) | Graph | States | Edges | Components | Degree range | Active signatures |
|---:|---|---:|---:|---:|---:|---:|
| 5 | OPW3 | 12 | 8 | 5 | 0–2 | 4 |
| 5 | LR2 | 12 | 8 | 5 | 0–2 | 4 |
| 5 | OPW23 | 12 | 8 | 5 | 0–2 | 4 |
| 7 | OPW3 | 360 | 600 | 19 | 2–4 | 4 |
| 7 | LR2 | 360 | 240 | 128 | 0–2 | 4 |
| 7 | OPW23 | 360 | 840 | 19 | 2–6 | 16 |
| 9 | OPW3 | 20,160 | 53,760 | 69 | 4–6 | 4 |
| 9 | LR2 | 20,160 | 13,440 | 6,856 | 0–2 | 4 |
| 9 | OPW23 | 20,160 | 67,200 | 69 | 4–8 | 16 |

All 54 strict checks passed:

```text
EHF_OPW3_AUDIT_01_FOUNDATION_REBUILD_PASS
```

### 4.2 Main finite result

At \(n=5,7,9\),

\[
\operatorname{Comp}(\mathrm{OPW3})
=
\operatorname{Comp}(\mathrm{OPW23})
=
\text{realised }\Pi\text{-fibres}.
\]

Thus LR3 alone generates the complete chamber partition.

At \(n=7,9\),

\[
E_{\mathrm{OPW23}}
=
E_{\mathrm{OPW3}}\sqcup E_{\mathrm{LR2}},
\]

with disjoint LR3 and LR2 simple-edge sets.

Working interpretation:

\[
\boxed{\mathrm{OPW3}=\text{minimal chamber skeleton}}
\]

and

\[
\boxed{\mathrm{OPW23}=\text{the same chambers with LR2 internal shortcuts}.}
\]

### 4.3 LR3 active-signature geometry

At \(n=7\),

\[
\mathrm{CORE}_3=\{2,3\},
\qquad
\mathrm{VARIABLE}_3=\{1,4\}.
\]

At \(n=9\),

\[
\mathrm{CORE}_3=\{2,3,4,5\},
\qquad
\mathrm{VARIABLE}_3=\{1,6\}.
\]

Observed finite law:

\[
\mathrm{ACTIVE}_3(c)
=
\{2,\ldots,n-4\}\cup S(c),
\qquad
S(c)\subseteq\{1,n-3\}.
\]

This produces a four-state, two-boundary-bit LR3 grammar. It is exact at \(n=7,9\), but not yet proved for all odd \(n\).

---

## 5. Audit-02: square complex and signature grammar

All 14,350 strict checks passed:

```text
EHF_OPW3_AUDIT_02_SQUARE_AND_SIGNATURE_CENSUS_PASS
```

### 5.1 Square census

| \(n\) | Graph | Triangles | Squares | Cycle rank |
|---:|---|---:|---:|---:|
| 5 | OPW3 | 0 | 1 | 1 |
| 7 | OPW3 | 0 | 240 | 259 |
| 9 | OPW3 | 0 | 42,000 | 33,669 |
| 7 | LR2 | 0 | 0 | 8 |
| 9 | LR2 | 0 | 0 | 136 |
| 7 | OPW23 | 0 | 540 | 499 |
| 9 | OPW23 | 0 | 72,240 | 47,109 |

The foundational square geometry is intrinsic to OPW3. LR2 alone has no squares at \(n=7,9\).

### 5.2 Square-boundary ranks

For OPW3 at \(n=7\):

\[
\operatorname{rank}_{\mathbb F_2}B_\square
=
\operatorname{rank}_{\mathbb F_3}B_\square
=239,
\]

leaving

\[
259-239=20
\]

residual cycle directions.

At \(n=9\):

\[
\operatorname{rank}_{\mathbb F_2}B_\square
=
\operatorname{rank}_{\mathbb F_3}B_\square
=32971,
\]

leaving

\[
33669-32971=698
\]

residual cycle directions.

These are candidates for nonlocal loop or holonomy structure. They are not yet quantum phases.

### 5.3 OPW23 characteristic-two anomaly

At \(n=7\),

\[
\operatorname{rank}_{\mathbb F_2}B_\square=439,
\qquad
\operatorname{rank}_{\mathbb F_3}B_\square=449.
\]

This is a ten-dimensional characteristic-two rank defect in the mixed LR2/LR3 square system. No integer torsion theorem has yet been proved.

### 5.4 Sixteen-signature decomposition

At \(n=7,9\),

\[
4_{\mathrm{LR3}}\times4_{\mathrm{LR2}}=16_{\mathrm{joint}},
\]

with every combination realised.

Therefore the older sixteen-state active grammar decomposes as

\[
\boxed{\text{four-state LR3 core}\times\text{four-state LR2 decoration}.}
\]

Neither the four-state nor sixteen-state active-signature partition is globally Markov-lumpable. Active signatures are observables or identity labels, not complete dynamical states.

---

# Part II — Spectral and growth survival

## 6. Audit-03: normalized-Laplacian slow sectors

All 21,621 strict checks passed:

```text
EHF_OPW3_AUDIT_03_NORMALIZED_LAPLACIAN_SLOW_SECTOR_PASS
```

| \(n\) | Graph | Median gap | Mean gap |
|---:|---|---:|---:|
| 5 | OPW3 | 1.000000 | 1.200000 |
| 5 | OPW23 | 1.000000 | 1.200000 |
| 7 | OPW3 | 0.18566651 | 0.24398633 |
| 7 | OPW23 | 0.40000000 | 0.47008860 |
| 9 | OPW3 | 0.06016920 | 0.06505011 |
| 9 | OPW23 | 0.17242272 | 0.17037189 |

LR2 raises the internal mixing rate and reorganises the slow sector.

Size-weighted mean squared alignment of the first eight nontrivial slow modes:

\[
n=5:1.00000000,
\]

\[
n=7:0.69181089,
\]

\[
n=9:0.26398414.
\]

OPW3 and OPW23 share chambers but do not preserve the same slow eigenspaces. The old OPW23 slow-mode results cannot simply be relabelled as foundational OPW3 results.

---

## 7. Audit-04: exact growth retraction

All 26 strict checks passed:

```text
EHF_OPW3_AUDIT_04_GROWTH_RETRACTION_EDGE_CHANNEL_PASS
```

### 7.1 Exact state growth

For \(5\to7\):

\[
12\times30=360.
\]

For \(7\to9\):

\[
360\times56=20160.
\]

Every target state is generated exactly once from one source state and one sequential insertion descriptor. Deleting the two newest labels recovers the unique source ancestor.

### 7.2 Packet preservation

For \(5\to7\):

| Graph | Preservation rate | Universal descriptors |
|---|---:|---:|
| OPW3 | 0.377777777778 | 0 |
| LR2 | 0.461111111111 | 2 |
| OPW23 | 0.222222222222 | 0 |

For \(7\to9\):

| Graph | Preservation rate | Universal descriptors |
|---|---:|---:|
| OPW3 | 0.450396825397 | 2 |
| LR2 | 0.562500000000 | 12 |
| OPW23 | 0.281448412698 | 2 |

The OPW3 and OPW23 universally preserving descriptors at \(7\to9\) are

\[
(3,3),\qquad(3,4).
\]

The stable packet-preserving growth channel appears at \(7\to9\), not \(5\to7\).

### 7.3 Two-branch ancestry

Under the two universal OPW3 descriptors, every \(n=7\) chamber reaches two \(n=9\) chambers:

\[
s\mapsto9s+108,
\qquad
s\mapsto9s+144.
\]

### 7.4 Edge-channel decomposition

At \(5\to7\):

\[
600=120_{\mathrm{vertical}}+96_{\mathrm{faithful}}+384_{\mathrm{cross}}.
\]

At \(7\to9\):

\[
53760=5760_{\mathrm{vertical}}+18000_{\mathrm{faithful}}+30000_{\mathrm{cross}}.
\]

At both steps there are zero same-source-chamber nonedge edges.

Every \(n=7\) source edge has exactly 30 faithful child edges, and every \(n=7\) source state has exactly 16 vertical child edges.

Thus growth decomposes into

\[
\boxed{\text{vertical development}+\text{faithful adjacency}+\text{new cross-chamber coupling}.}
\]

---

# Part III — Exact packet reconstruction

## 8. Audit-05: equitable packet closure

All 2,979 strict checks passed:

```text
EHF_OPW3_AUDIT_05_EQUITABLE_PACKET_RECONSTRUCTION_PASS
```

An equitable partition defines an exact quotient of adjacency and the simple random walk.

| \(n\) | Starting partition | Median cells | Mean cells | Maximum | Mean component compression |
|---:|---|---:|---:|---:|---:|
| 7 | Structural | 3 | 4.95 | 14 | 0.2774 |
| 7 | LR3 signature | 5 | 6.05 | 24 | 0.3348 |
| 9 | Structural | 27 | 42.75 | 186 | 0.1487 |
| 9 | LR3 signature | 27 | 50.01 | 360 | 0.1736 |

The four LR3 signatures are not complete dynamical states. A better finite description is

\[
\boxed{\text{structural equitable cell}+\text{LR3 boundary identity}.}
\]

For the quotient transition matrix \(P\), define the stochastic transition cost

\[
A_{ab}=-\log P_{ab}.
\]

This is not yet a quantum action.

---

## 9. Audit-06: closure equality and spectral completeness

All 558 strict checks passed:

```text
EHF_OPW3_AUDIT_06_V3_PACKET_CLOSURE_SPECTRAL_ACTION_PASS
```

### 9.1 Exact closure equality

For every tested OPW3 chamber,

\[
\operatorname{Closure}(\mathrm{LR3})
=
\operatorname{Closure}(\mathrm{LR2})
=
\operatorname{Closure}(\mathrm{LR3}\times\mathrm{LR2}).
\]

Counts:

\[
n=5:5/5,
\qquad
n=7:19/19,
\qquad
n=9:69/69.
\]

Thus LR2 adds no extra exact packet distinction inside foundational OPW3 once adjacency and LR3 identity are included.

One OPW23 chamber at \(n=9\) is exceptional:

\[
\Pi=0,1,5,6,7\mid2,3,4,8.
\]

There the LR3 closure has 9 cells, the LR2 closure 8, and the joint closure 9.

### 9.2 Global exact compression

For OPW3:

\[
n=5:0.583333,
\]

\[
n=7:0.319444,
\]

\[
n=9:0.171181.
\]

At \(n=9\), the exact LR3 packet quotient has approximately 17.1% as many cells as microscopic states.

### 9.3 Slow-gap visibility

Among eligible OPW3 chambers:

\[
n=7:10/15
\]

reproduce the full slowest gap, with state-weighted visibility 0.729730.

At \(n=9\):

\[
47/65
\]

reproduce it, with state-weighted visibility 0.747664.

The exact packet quotient captures most, but not all, of the slow structural sector.

---

# Part IV — Hidden slow sectors

## 10. Audit-07: hidden families and ancestry completion

All 25 strict checks passed:

```text
EHF_OPW3_AUDIT_07_HIDDEN_SLOW_COMPLETION_PASS
```

At \(n=7\), five eligible chambers hide the full slowest mode and reduce to three numerical fingerprint families.

At \(n=9\), eighteen eligible chambers hide it and reduce to ten families. Most occur in exact pairs, indicating structured rather than random failure.

### 10.1 Completion results

At \(n=7\):

| Candidate | Recovered |
|---|---:|
| Square count | 0/5 |
| Parent component | 3/5 |
| Parent packet | 3/5 |
| Parent LR3 signature | 3/5 |
| Square count + parent packet | 3/5 |

At \(n=9\):

| Candidate | Recovered |
|---|---:|
| Square count | 0/18 |
| Parent component | 14/18 |
| Parent packet | 14/18 |
| Parent LR3 signature | 14/18 |
| Square count + parent packet | 14/18 |

The smallest successful ancestry addition is the parent LR3 signature.

\[
\boxed{\text{Most hidden slow modes remember growth ancestry}.}
\]

Raw local square count does not recover them.

Residual chambers after parent-signature completion:

\[
n=7:\{6,17\},
\]

\[
n=9:\{16,22,30,38\}.
\]

---

## 11. Audit-08: residual completion

All 60 strict checks passed:

```text
EHF_OPW3_AUDIT_08_RESIDUAL_COMPLETION_PASS
```

### 11.1 \(n=7\)

Residual chambers:

\[
6,17.
\]

| Candidate | Recovered | Mean compression |
|---|---:|---:|
| Baseline | 0/2 | 0.166667 |
| Parent signature | 0/2 | 0.375000 |
| Insertion descriptor | 2/2 | 0.583333 |
| Parent signature + descriptor | 2/2 | 0.750000 |
| Two-level descriptor history | 2/2 | 1.000000 |
| LR3 edge-labelled refinement | 0/2 | 0.166667 |
| Oriented square profile | 0/2 | 0.166667 |

### 11.2 \(n=9\)

Residual chambers:

\[
16,22,30,38.
\]

| Candidate | Recovered | Mean compression |
|---|---:|---:|
| Baseline | 0/4 | 0.075521 |
| Parent signature | 0/4 | 0.437500 |
| Insertion descriptor | 4/4 | 0.833333 |
| Parent signature + descriptor | 4/4 | 0.875000 |
| Two-level descriptor history | 4/4 | 1.000000 |
| LR3 edge-labelled refinement | 0/4 | 0.075521 |
| Oriented square profile | 0/4 | 0.075521 |

### 11.3 Main finite result

The exact current \(n-2\to n\) insertion descriptor recovers every tested residual slow mode:

\[
\boxed{2/2\text{ at }n=7,\qquad4/4\text{ at }n=9.}
\]

The residual modes are not recovered by:

- raw square count;
- oriented square profile;
- LR3 edge-slot labels;
- a second level of signature history;
- a second level of packet history.

The missing information is specifically tied to the current growth channel.

---

## 12. Audit-09: growth-descriptor chart covariance

All 144 strict checks passed:

```text
EHF_OPW3_AUDIT_09_GROWTH_DESCRIPTOR_CHART_COVARIANCE_PASS
EHF_QM3_01_HILBERT_LIFT_INTRINSIC_PROJECTORS_PASS
```

### 12.1 Chart census

The audit varied:

- every surviving old-label anchor;
- lexicographically minimum and maximum anchored orientations;
- both orders for inserting the two newest labels.

This produced:

\[
20\text{ charts for }5\to7,
\]

\[
28\text{ charts for }7\to9.
\]

### 12.2 Parent invariance

The undirected \(n-2\) ancestor is identical in every chart:

\[
\boxed{\text{growth ancestry is chart-invariant}.}
\]

The insertion descriptor itself is not generally invariant.

After conditioning on the source dihedral chart transition, the descriptor
transition becomes deterministic in every tested chart. The descriptor is
therefore legitimate coordinate data in a discrete growth atlas.

### 12.3 Packet closures are chart-dependent

The chart-relative LR3-signature equitable partition equals the reference
partition in only

\[
70/190
\]

orientation-chart/chamber cases at \(n=7\), and

\[
190/966
\]

at \(n=9\).

Thus packet cells and slot labels are not intrinsic objects.

### 12.4 Complete slow-sector covariance

The canonical parent-signature completion leaves residual chambers

\[
n=7:\quad\{6,15,17\},
\]

\[
n=9:\quad\{16,22,30,38,62\}.
\]

The additional components \(15\) and \(62\) had one-cell baseline quotients and
were previously spectrally ineligible; the chart audit exposes their missing
slow structure once a nontrivial ancestry quotient is formed.

For \(n=7\), over 60 chart/chamber cases:

| Completion | Gap recovered | Complete lowest eigenspace |
|---|---:|---:|
| Current LR3 signature | 36/60 | 28/60 |
| Current + parent signature | 36/60 | 36/60 |
| Current + descriptor | 60/60 | 60/60 |
| Current + parent signature + descriptor | 60/60 | 60/60 |

For \(n=9\), over 140 chart/chamber cases:

| Completion | Gap recovered | Complete lowest eigenspace |
|---|---:|---:|
| Current LR3 signature | 76/140 | 64/140 |
| Current + parent signature | 76/140 | 76/140 |
| Current + descriptor | 140/140 | 128/140 |
| Current + parent signature + descriptor | 140/140 | 140/140 |

The combined chart-relative data

\[
\boxed{
\text{current LR3 identity}
+
\text{parent LR3 identity}
+
\text{insertion descriptor}
}
\]

contains the complete lowest nontrivial normalized-Laplacian eigenspace in
every tested chart.

The completed partitions themselves remain chart-dependent:

\[
28/60
\]

equal the reference partition at \(n=7\), and

\[
92/140
\]

at \(n=9\).

Therefore the correct invariant content is not the packet cells or raw
descriptor values. It is the completed slow subspace:

\[
\boxed{
\text{chart-relative coordinates, chart-covariant slow sector}.
}
\]

This result justifies constructing the rebuilt QM programme from intrinsic
spectral projectors rather than promoting packet labels or insertion
descriptors to physical quantum numbers.

---

# Part V — LR3-native Hilbert lift

## 13. QM3-01: intrinsic slow-sector projectors

All 1,240 strict checks passed:

```text
EHF_QM3_01_HILBERT_LIFT_INTRINSIC_PROJECTORS_PASS
```

For every OPW3 chamber \(C\), the audit constructs the exact finite Hilbert
space

\[
\mathcal H_C=\mathbb C^{|C|}
\]

in the canonical cycle-state basis.

The symmetric normalized Laplacian

\[
L_{\rm norm}=I-D^{-1/2}AD^{-1/2}
\]

is used as a canonical self-adjoint structural operator. This is not yet a
claim that \(L_{\rm norm}\) is the physical Hamiltonian.

### 13.1 Intrinsic projectors

The audit constructs:

\[
P_0
\]

onto the stationary direction and

\[
P_{\rm slow}
\]

onto the complete lowest nontrivial normalized-Laplacian eigenspace, including
its full multiplicity.

It verifies:

- Hermiticity;
- idempotence;
- stationary/slow orthogonality;
- commutation of \(P_{\rm slow}\) with \(L_{\rm norm}\);
- exact nesting of the reference packet, ancestry and growth-completion
  quotient spaces.

### 13.2 All-chart completion

At \(n=7\):

\[
18/19
\]

chambers have the complete lowest eigenspace contained in every chart
completion.

The unique chart-critical chamber is:

\[
C_{18}.
\]

At \(n=9\):

\[
68/69
\]

chambers have complete all-chart slow capture.

The unique chart-critical chamber is:

\[
C_{68}.
\]

### 13.3 Degenerate critical chambers

The critical chambers are degenerate slow-multiplet cases:

\[
n=7,\ C_{18}:
\qquad
|C|=4,\quad \dim E_{\rm slow}=2,
\]

\[
n=9,\ C_{68}:
\qquad
|C|=36,\quad \dim E_{\rm slow}=4.
\]

Their all-chart common completed quotient does not contain the complete
degenerate slow eigenspace:

\[
n=7:\quad \dim \mathcal Q_{\cap}=2,
\]

\[
n=9:\quad \dim \mathcal Q_{\cap}=6.
\]

In each case the common intersection captures only part of the lowest
multiplet.

This establishes:

\[
\boxed{
\text{matching the lowest eigenvalue is weaker than containing the complete
lowest eigenspace}.
}
\]

Different charts can select different directions inside a degenerate slow
eigenspace even when they reproduce the same gap.

### 13.4 Correct intrinsic object

The chart packet cells, ancestry labels and insertion descriptors are useful
coordinates, but the complete spectral projector

\[
P_{\rm slow}
\]

is the unambiguous intrinsic finite object.

The rebuilt QM programme should therefore be based on spectral projectors and
their invariant subspaces, not on promoting one chart's packet basis to a
physical basis.

---

# Part VI — Current structural picture

## 14. Best present hierarchical description

The tested evidence supports

\[
\boxed{\text{current LR3 packet identity}+\text{parent LR3 identity}+\text{current insertion descriptor}}
\]

as a finite description sufficient to recover every tested chamber’s slowest normalized-Laplacian mode through \(n=9\).

A useful structural decomposition is

\[
\mathcal H_{\mathrm{micro}}
\supset
\mathcal H_{\mathrm{packet}}
\oplus
\mathcal H_{\mathrm{ancestry}}
\oplus
\mathcal H_{\mathrm{growth\ residual}}.
\]

This notation is preparatory. It is not yet a physical Hilbert-space decomposition.

### Layer 1 — packet-visible sector

Generated by the exact LR3-signature equitable closure.

### Layer 2 — ancestry-visible sector

Additional slow structure recovered by the parent LR3 signature.

### Layer 3 — growth-channel residual sector

Final slow structure recovered by the current insertion descriptor.

---

## 15. Established finite results

- OPW3 alone generates the realised \(\Pi\)-chamber partition at \(n=5,7,9\).
- OPW23 differs by internal LR2 edges, not by chambers.
- OPW3 has a substantial triangle-free square complex.
- OPW3 has nontrivial residual cycle-space directions.
- OPW3 and OPW23 have different slow eigenspaces.
- Sequential insertion/deletion gives an exact state bijection at \(5\to7\) and \(7\to9\).
- Every source OPW3 edge survives with uniform multiplicity.
- At \(7\to9\), two universal packet-preserving descriptors exist.
- Exact equitable packet quotients exist.
- LR3-, LR2-, and joint-seeded exact closures coincide in every tested OPW3 chamber.
- The exact packet quotient captures most slowest chamber modes.
- Parent LR3 identity recovers most hidden modes.
- The current insertion descriptor recovers all tested residual modes.
- The undirected growth ancestor is invariant across all tested charts.
- Chart descriptors transform deterministically after conditioning on the source dihedral chart transition.
- Current identity + parent identity + descriptor contains the complete lowest eigenspace in every tested chart for all noncritical chambers and for the residual chambers audited in Audit-09.
- The complete lowest spectral projector is intrinsic even when individual charts select only part of a degenerate slow multiplet.
- Exactly one chart-critical degenerate chamber occurs at each of \(n=7\) and \(n=9\).

---

## 16. Not established

- No all-\(n\) theorem for the LR3 active-core law.
- No all-\(n\) theorem for universal growth descriptors.
- No full \(9\to11\) census.
- The insertion descriptor is not chart-independent; it is chart coordinate data.
- No all-\(n\) proof that the completed slow sector remains chart-covariant.
- No natural quantum phase reconstructed.
- No physical Hamiltonian selected.
- No dispersion relation derived.
- No particle sector identified.
- No continuum, Lorentz or Standard Model limit.
- No experimental prediction.

---

## 17. Working conjectures

### Conjecture A — LR3 chamber sufficiency

For odd \(n\) beyond the small seed regime, LR3 connects every realised \(\Pi\)-fibre.

### Conjecture B — boundary grammar

For odd \(n\ge7\),

\[
\mathrm{ACTIVE}_3(c)
=
\{2,\ldots,n-4\}\cup S(c),
\qquad
S(c)\subseteq\{1,n-3\}.
\]

### Conjecture C — stable universal growth core

For sufficiently large odd \(n\), a core family of insertion descriptors preserves LR3 packet identity universally.

### Conjecture D — bounded-depth slow completion

The full slow structural sector is recoverable from a bounded-depth hierarchy of current packet identity, ancestor identity and growth-channel data.

### Conjecture E — all-\(n\) chart-covariant growth residual

The finite chart-covariance result through \(n=9\) extends to higher odd multiplicity: raw packet and descriptor coordinates may vary by chart while the completed slow subspace remains invariant.

---

# Part VI — Next steps

## 18. Immediate next programme

### EHF-QM3-02 — Degenerate Slow-Multiplet Chart-Orbit Resolution

For the two chart-critical chambers, restrict every chart-completion projector
to the complete lowest eigenspace:

\[
R_\chi
=
B_{\rm slow}^{\mathsf T}
Q_\chi
B_{\rm slow}.
\]

Determine:

1. the rank selected by each chart;
2. the number of distinct chart-selected slow subspaces;
3. their intersection and union;
4. their principal-angle classes;
5. whether the chart family forms a tight or non-tight fusion frame;
6. whether the full intrinsic projector can be reconstructed from the chart
   orbit without selecting a preferred chart.

No physical spin, gauge or particle interpretation should be assigned to the
degenerate multiplet at this stage.

---

## 19. QM bridge rebuild sequence

The QM rebuild now begins:

1. **QM3-01 — Hilbert lift and intrinsic projectors**  
   For each OPW3 chamber \(C\), define
   \[
   \mathcal H_C=\mathbb C^{|C|}.
   \]

2. **QM3-02 — Natural operators**  
   Compare adjacency, combinatorial Laplacian, normalized Laplacian and growth/deletion-derived Hermitian operators.

3. **QM3-03 — Exact packet projector**  
   Construct the orthogonal projector onto the exact LR3 packet sector.

4. **QM3-04 — Ancestry and residual projectors**  
   Construct projectors onto parent-signature and chart-covariant residual sectors.

5. **QM3-05 — Unitary dynamics**  
   For a justified Hermitian generator \(H\), define
   \[
   U(t)=e^{-itH}.
   \]

6. **QM3-06 — Interference and measurement**  
   Rebuild path interference, projectors, distinguishability and Born-rule consistency.

7. **QM3-07 — LR3 square connection and curvature**  
   Test phase assignments, curvature and holonomy on the intrinsic OPW3 square complex.

8. **QM3-08 — Growth compatibility**  
   Test whether operators, sectors and observables transport coherently under \(n\to n+2\).

No OPW23 quantum result should be inherited without passing through this LR3-only sequence.

---

## 20. Current working assessment

The rebuild has separated three roles:

\[
\boxed{\mathrm{LR3}=\text{foundational chamber, square and slow-dynamics substrate};}
\]

\[
\boxed{\mathrm{LR2}=\text{nonfoundational shortcut and diagnostic enrichment};}
\]

\[
\boxed{\text{growth history}=\text{essential information for completing hidden slow sectors}.}
\]

The strongest current statement is:

> Through \(n=9\), the foundational OPW3 slow sector is recovered in every tested growth chart by chart-relative current LR3 identity, parent LR3 identity and insertion-descriptor coordinates, while the complete lowest eigenspace—not the packet cells or raw descriptor—is the chart-covariant structural content.

This is a finite structural result. It is not yet a derivation of quantum mechanics or particle physics.

---

## 21. Reproducibility record

```text
EHF_OPW3_AUDIT_01_FOUNDATION_REBUILD_PASS
EHF_OPW3_AUDIT_02_SQUARE_AND_SIGNATURE_CENSUS_PASS
EHF_OPW3_AUDIT_03_NORMALIZED_LAPLACIAN_SLOW_SECTOR_PASS
EHF_OPW3_AUDIT_04_GROWTH_RETRACTION_EDGE_CHANNEL_PASS
EHF_OPW3_AUDIT_05_EQUITABLE_PACKET_RECONSTRUCTION_PASS
EHF_OPW3_AUDIT_06_V3_PACKET_CLOSURE_SPECTRAL_ACTION_PASS
EHF_OPW3_AUDIT_07_HIDDEN_SLOW_COMPLETION_PASS
EHF_OPW3_AUDIT_08_RESIDUAL_COMPLETION_PASS
EHF_OPW3_AUDIT_09_GROWTH_DESCRIPTOR_CHART_COVARIANCE_PASS
EHF_QM3_01_HILBERT_LIFT_INTRINSIC_PROJECTORS_PASS
```

Latest QM3-01 local result:

```text
strict checks: 1240/1240
elapsed: 14.52s
```

---

## 22. Document policy

Every future statement should be labelled as one of:

- **Exact finite result**
- **Numerically supported candidate**
- **Working conjecture**
- **Speculative physical interpretation**
- **Failed hypothesis**
- **Open computational question**

No statement should be promoted between categories without an explicit audit or proof.
