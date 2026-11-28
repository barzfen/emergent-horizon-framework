# EHF Quantum Mechanics Bridge Program

**Working research note**  
**Date:** 2026-05-18; updated 2026-06-14  
**Project:** Emergent Horizon Framework / Relational Kinematics Atlas  
**Status:** Probes QM-01 through QM-12 completed at finite-atlas scale; QM-13 scaling/robustness proposed next

---

## 1. Purpose

This document records the current state of the EHF Quantum Mechanics Bridge Program.

The goal is not to claim that ordinary quantum mechanics has been fully derived from EHF. The goal is narrower and sharper:

> Test whether the core formal machinery of quantum mechanics can arise naturally from finite admissible-comparison atlases.

The bridge program asks whether EHF/RKA constructions can support:

1. a natural Hilbert basis,
2. Hermitian generators,
3. unitary amplitude evolution,
4. interference,
5. measurement as coarse comparison,
6. Born-compatible quadratic readout,
7. Fock-like many-body lifts,
8. delayed-choice / quantum-eraser behaviour,
9. Bell/context diagnostics,
10. connection/curvature phase audits.

The current result is positive at the finite-atlas toy-model level, with important caveats: full unfiltered atlas CHSH scans have not yet found contact-state Bell violation, and the OPW packet-action regime still needs to be integrated into the QM bridge path-sum machinery.

---

## 2. Core bridge dictionary

| Standard QM object | EHF/RKA bridge object |
|---|---|
| configuration basis \(|x\rangle\) | admissible atlas states/classes |
| Hilbert space | \(\ell^2(\mathcal A, \mu)\) over an admissible atlas \(\mathcal A\) |
| wavefunction/amplitude | complex weight on atlas states |
| Hamiltonian/generator | Hermitian adjacency, Laplacian, or normalized atlas operator |
| unitary evolution | \(U(t)=e^{-itH}\) or finite path-sum analogue |
| observable | admissible comparison/coarse-graining map |
| measurement | projector induced by a coarse comparison |
| Born rule | conserved quadratic intensity \(|\psi|^2\) |
| which-path information | comparison map preserving path/gate distinction |
| eraser basis | comparison map recombining alternatives into \(+/-\) marker branches |
| Fock lift | Kronecker-sum/free multi-object lift plus exchange quotienting |

The guiding EHF reading is:

\[
\text{quantum structure} \approx \text{amplitude dynamics on admissible comparison atlases}.
\]

---

## 3. Models used so far

### 3.1 Johnson atlas

The Johnson-side model uses:

\[
\Omega_k = \{S\subset [2k-1] : |S|=k\}
\]

with Johnson adjacency. The main observable is:

\[
h(S)=\sum_{i\in S} i.
\]

This model is clean, regular, connected, and useful as a controlled finite Hilbert-space testbed.

### 3.2 Hamilton-cycle / Odd Preserve atlas

The Hamilton-cycle side uses Hamilton cycles on \(K_n\), with reflection canonicalization and local block-reversal moves of lengths:

\[
L\leq 3, \qquad \ell\in\{2,3\}.
\]

The Odd Preserve / preserve-\(\Pi\) condition imposes a parity-sector constraint. For the official bridge-consistent version at \(n=7\):

- full graph: 360 vertices,
- 840 weak edges,
- 19 components,
- largest component: 36 vertices,
- largest component edges: 108,
- largest component degree: 6-regular.

The official adjacency convention is:

```text
cyclic_all_starts
```

This matches QM-02, QM-03, QM-04, QM-06B, and QM-07.

A stricter variant also exists:

```text
linear_no_zero
```

It produces the same component-size ladder but fewer edges on the selected component:

- 36 vertices,
- 72 edges,
- degree 4-regular.

This stricter variant also passed the Fock check, but the official bridge convention is `cyclic_all_starts`.

---

## 4. Probe summary

| Probe | Name | Status | Main conclusion |
|---|---|---|---|
| QM-01 | Hilbertization audit | Pass | EHF atlases give natural finite Hilbert-basis candidates. |
| QM-02 | Unitary vs Markov walk | Pass | Same atlas supports Markov diffusion and Hermitian/unitary amplitude dynamics. |
| QM-03 | Interference path-sum audit | Pass | Coherent alternatives interfere; which-path alternatives add classically. |
| QM-03B | Interference landscape / phase sensitivity | Strong pass | Odd Preserve phase modes produce constructive and destructive interference. |
| QM-04 | Measurement / coarse-graining audit | Strong pass | Measurement behaves as admissible coarse comparison/projector. |
| QM-05 | Born / quadratic intensity audit | Full pass | \(p=2\), i.e. \(|\psi|^2\), is selected by conservation and projector compatibility. |
| QM-06 | Fock-like lift audit | Strong pass after consistency patch | Free two-body spectra match one-body spectral convolution; exchange sectors are invariant. |
| QM-06B | Fock consistency audit | Pass | Resolved cyclic vs linear adjacency mismatch. Official Odd Preserve result uses cyclic all-starts. |
| QM-07 | Delayed choice / quantum eraser | Strong pass | Conditional eraser branches recover interference while no-signalling identity holds. |
| QM-08 | Bell factorisation / measurement-context audit | Partial pass | Bell machinery works; contact states are entangled, but fixed-setting contact CHSH did not violate. |
| QM-08B | Optimised CHSH / entanglement witness audit | Partial-strong pass | Filtered/postselected and Schmidt-sector witnesses violate; embedded full comparison does not. |
| QM-08C | Full-atlas observable optimisation | Negative/full-atlas result | Broader non-postselected full-atlas scans still found no contact-state CHSH violation. |
| QM-09 | QED connection phase audit | Strong partial pass | Non-flat connection curvature produces interference; flat/pure-gauge controls are invisible. |
| QM-09B | Connection curvature response audit | Strong pass | Response tracks curvature, not arbitrary edge phase. |
| QM-09C | Probe-19 connection import audit | Strong pass | Probe-19 physical edge mode imported cleanly; pure-gauge controls were invisible and curved imported connection produced spectral/interference response. |
| QM-10 | OPW packet-history amplitude audit | Pass | Mature OPW packet MSMs give stochastic actions whose half-action exponential gives amplitude magnitudes exactly. |
| QM-11A | OPW square-relation phase-source audit | Pass as candidate source | OPW square relations project nontrivially to packet transitions and reach all 16 packet states. |
| QM-11B | OPW square-relation phase-candidate construction | Pass | Square-derived non-gradient packet phases have nonzero cycle curvature and produce controlled interference; pure-gradient control is curvature-free. |
| QM-12 | OPW/QED action-phase path-sum audit | Strong pass | OPW packet-action magnitudes and square-derived phases combine into a controlled finite action-phase path-sum model for n=11 and n=13. |

---

## 5. Probe details

## 5.1 QM-01 — Hilbertization audit

**Question:** Does an admissible atlas naturally define a Hilbert basis and self-adjoint operator structure?

### Johnson \(k=5\)

- vertices: 126,
- weak edges: 1260,
- degree histogram: `{20: 126}`,
- connected: yes,
- adjacency symmetric: yes,
- uniform and degree-stationary measures coincide because the graph is regular.

### HC \(n=7,L=3\), full

- vertices: 360,
- weak edges: 2520,
- degree histogram: `{14: 360}`,
- connected: yes,
- adjacency symmetric: yes.

### HC \(n=7,L=3\), preserve-\(\Pi\)

- vertices: 360,
- weak edges: 840,
- components: 19,
- component-size histogram:

```text
{4: 1, 8: 2, 12: 3, 16: 3, 20: 3, 24: 3, 28: 2, 32: 1, 36: 1}
```

- degree histogram:

```text
{2: 4, 3: 32, 4: 120, 5: 128, 6: 76}
```

**Interpretation:**

The clean Johnson and full HC graphs behave as regular Hilbert-basis candidates. The preserve-\(\Pi\) graph produces chambering and irregular global Markov flow, but amplitude adjacency remains Hermitian under uniform counting. This supports the EHF idea that admissible comparison structure can define the basis before a Hilbert space is postulated.

**EHF verdict:** Strengthens EHF modestly.

---

## 5.2 QM-02 — Unitary vs Markov walk

**Question:** Can the same atlas support both classical diffusion and quantum-like unitary amplitude propagation?

### Main observations

Across Johnson, full HC, and Odd Preserve largest components:

- Markov evolution diffuses probability toward stationary distributions.
- Hermitian atlas generators preserve amplitude norm under unitary evolution.
- Quantum walks remain structured and oscillatory rather than simply flattening into Markov equilibrium.

For the Odd Preserve largest component:

- vertices: 36,
- weak edges: 108,
- degree: 6-regular,
- Markov walk spreads over the component,
- unitary evolution preserves norm to machine precision.

**Interpretation:**

The same finite atlas can carry two distinct dynamics:

\[
\text{Markov diffusion} \neq \text{unitary amplitude evolution}.
\]

This is exactly the distinction needed for a QM bridge.

**EHF verdict:** Strengthens EHF.

---

## 5.3 QM-03 — Interference path-sum audit

**Question:** Do unresolved atlas alternatives interfere?

The probe compared:

\[
P_{\mathrm{coh}}=|A_1+A_2|^2
\]

against:

\[
P_{\mathrm{which}}=|A_1|^2+|A_2|^2.
\]

### Representative results

Johnson \(k=5\):

```text
P coherent:          2.6201601562500053e-07
P which-path:        1.3100800781250026e-07
interference ratio:  1.0
```

Full HC \(n=7,L=3\):

```text
P coherent:          2.1954357140862286e-07
P which-path:        1.0977178570431142e-07
interference ratio:  1.0000000000000002
```

Odd Preserve largest component:

```text
P coherent:          9.302721574455109e-05
P which-path:        4.6513607872275546e-05
interference ratio:  1.0
```

**Interpretation:**

Unresolved path alternatives add as amplitudes, not probabilities. When alternatives are made distinguishable, probabilities add instead.

**EHF verdict:** Strengthens EHF, with the caveat that stronger tests require atlas-induced phases rather than hand-picked slits.

---

## 5.4 QM-03B — Interference landscape / phase sensitivity audit

**Question:** Does destructive interference appear when phases are induced by atlas structure?

### Controls

No-phase and Johnson-delta controls produced constructive-only landscapes in the scanned cases.

### Odd Preserve `hc_length_u1`

- targets scanned: 33,
- destructive fraction: approximately 0.3425,
- best destructive ratio: approximately \(-0.9962\),
- phase gap: approximately \(-\pi\).

### Odd Preserve `hc_local_u1`

- targets scanned: 35,
- destructive fraction: approximately 0.4749 in the earlier 03B scan,
- best destructive ratio: approximately \(-0.4593\),
- phase gap: approximately 2.698.

**Interpretation:**

Phase-sensitive Odd Preserve structure creates both constructive and destructive interference. This is a stronger bridge result than QM-03 because interference appears across a scanned landscape rather than a hand-selected two-slit example.

**Caveat:**

The current phase modes are atlas-motivated but not yet uniquely derived from the QED-style connection. The strongest future version should use the edge connection \(A\) from QED Probe 19.

**EHF verdict:** Strongly strengthens EHF, pending a more physically motivated phase source.

---

## 5.5 QM-04 — Measurement / coarse-graining audit

**Question:** Can measurement be represented as admissible coarse comparison rather than primitive collapse?

The probe treated a measurement as a projector induced by a coarse map:

\[
\pi:\mathcal A_{\mathrm{fine}}\rightarrow \mathcal A_{\mathrm{coarse}}.
\]

### Main behaviours observed

- Born block sums normalized to 1.
- Projectors were idempotent.
- Nonselective measurement removed cross-block coherence.
- Mid-time measurement changed later incompatible readout statistics.
- Selective measurement behaved as conditioning on a coarse block.

### Representative Odd Preserve phase run

For `hc_length_u1`:

```text
A-block coherence before:   13.003290748658548
A-block coherence after:    0.0
B disturbance TV:           0.15758552066605558
selective A->B TV:          0.20945645207278665
```

**Interpretation:**

The measurement-like effects arise from coarse comparison geometry:

\[
\text{measurement} = \text{admissible coarse comparison/projector}.
\]

This avoids treating collapse as primitive at the toy-model level.

**EHF verdict:** Strongly strengthens EHF.

---

## 5.6 QM-05 — Born / quadratic intensity audit

**Question:** Why should readout use \(|\psi|^2\) rather than \(|\psi|^p\) for some other \(p\)?

The probe tested candidate exponents:

\[
p\in\{1,2,3,4\}.
\]

The criteria were:

1. raw intensity conservation under unitary evolution,
2. compatibility with orthogonal projector weights,
3. consistency under mid-time coarse measurement.

### Result

Across Johnson and Odd Preserve phase runs:

\[
p=2
\]

was uniquely selected.

### Johnson \(k=5\)

```text
p=2 raw max drift:        1.1102230246251565e-15
p=2 projector mismatch:   5.551115123125783e-17
```

Non-quadratic exponents drifted or mismatched projector weights.

### Odd Preserve no phase

```text
p=2 raw max drift:        6.661338147750939e-16
p=2 projector mismatch:   1.1102230246251565e-16
```

### Odd Preserve `hc_length_u1`

```text
p=2 raw max drift:        1.1102230246251565e-15
p=2 projector mismatch:   4.996003610813204e-16
```

### Odd Preserve `hc_local_u1`

```text
p=2 raw max drift:        5.551115123125783e-16
p=2 projector mismatch:   7.216449660063518e-16
```

**Interpretation:**

Once the atlas supplies:

1. a Hilbert basis,
2. a Hermitian generator,
3. orthogonal coarse projectors,

then quadratic intensity is not arbitrary. It is the rule compatible with both conservation and measurement geometry.

\[
|\psi|^2
\]

is selected because other exponents require extra renormalization and fail projector compatibility.

**EHF verdict:** Very strong bridge result.

---

## 5.7 QM-06 — Fock-like lift / many-body audit

**Question:** Does the atlas Hilbert structure lift naturally to a many-body/Fock-like construction?

The free two-body Hamiltonian was:

\[
H_2 = H_1\otimes I + I\otimes H_1.
\]

The expected free spectrum is:

\[
E_{ij}=E_i+E_j.
\]

The exchange operator \(S\) swaps the two tensor factors. The key invariant is:

\[
[H_2,S]=0.
\]

### Johnson \(k=4\)

- one-particle dimension: 35,
- distinguishable two-body dimension: 1225,
- bosonic symmetric dimension: 630,
- fermionic antisymmetric dimension: 595,
- dense two-body check: ran,
- max spectrum-vs-convolution error: \(1.33\times 10^{-14}\),
- swap commutator max error: 0,
- contact interaction broke free convolution while preserving swap symmetry.

The exchange dimensions match:

\[
\dim(\mathrm{Sym}^2\mathcal H)=\frac{35(35+1)}{2}=630,
\]

\[
\dim(\wedge^2\mathcal H)=\frac{35(35-1)}{2}=595.
\]

### Odd Preserve cyclic all-starts, \(n=7,L=3\)

Official component:

- selected vertices: 36,
- selected weak edges: 108,
- selected degree: 6-regular,
- one-particle dimension: 36,
- distinguishable two-body dimension: 1296,
- bosonic symmetric dimension: 666,
- fermionic antisymmetric dimension: 630,
- dense two-body check: ran,
- max spectrum-vs-convolution error: \(1.643130076445232\times10^{-14}\),
- swap commutator max error: 0,
- contact free-convolution broken max abs: 0.3498638751700844,
- contact swap commutator max error: 0.

The exchange dimensions match:

\[
\dim(\mathrm{Sym}^2\mathcal H)=\frac{36(36+1)}{2}=666,
\]

\[
\dim(\wedge^2\mathcal H)=\frac{36(36-1)}{2}=630.
\]

**Interpretation:**

The finite-atlas Hilbert structure supports a free Fock-like lift. The free two-body spectrum is exactly the spectral convolution of the one-body spectrum. Symmetric and antisymmetric exchange sectors are dynamically invariant. A contact interaction breaks free additivity while preserving exchange symmetry.

\[
\text{EHF atlas QM} \Rightarrow \text{many-body/Fock-like structure}.
\]

**EHF verdict:** Strongly strengthens EHF.

---

## 5.8 QM-06B — Fock consistency audit

**Question:** Why did the first Odd Preserve QM-06 run produce a 4-regular component when earlier probes used a 6-regular component?

Two adjacency conventions were compared.

### Variant 1: `cyclic_all_starts`

- full graph: 360 vertices / 840 weak edges,
- selected component: 36 vertices / 108 weak edges,
- selected degree: 6-regular.

This matches QM-02, QM-03, QM-04, and QM-07.

### Variant 2: `linear_no_zero`

- full graph: 360 vertices / 600 weak edges,
- selected component: 36 vertices / 72 weak edges,
- selected degree: 4-regular.

This matches the original unpatched QM-06 result.

### Conclusion

The mismatch was not a Fock failure. It was an adjacency-convention mismatch.

Official convention for the QM bridge:

```text
cyclic_all_starts
```

The stricter `linear_no_zero` atlas is still mathematically interesting and also passed internally, but it should be treated as a separate sub-variant.

**EHF verdict:** Strengthens methodology. The inconsistency was diagnosed and resolved rather than hidden.

---

## 5.9 QM-07 — Delayed choice / quantum eraser audit

**Question:** Can the EHF finite-atlas model reproduce the logic of delayed choice and quantum erasure?

The probe compared which-path readout against eraser readout.

Which-path readout:

\[
P_{\mathrm{which}}=|A_1|^2+|A_2|^2.
\]

Eraser branches:

\[
P_+=\frac12|A_1+A_2|^2,
\]

\[
P_-=\frac12|A_1-A_2|^2.
\]

The no-signalling identity is:

\[
P_+ + P_- = P_{\mathrm{which}}.
\]

### `hc_length_u1`

The selected destructive pair was almost perfectly opposite phase:

```text
interference ratio:        -0.9962264150943396
phase gap:                 -3.1415926535428307
```

No-signalling held to numerical precision:

```text
no_signal_l1_unnormalized: 5.413069928547013e-21
no_signal_tv_normalized:   4.434386885465713e-17
```

Conditional branches differed strongly:

```text
plus_vs_which_tv:          0.23691749124489053
minus_vs_which_tv:         0.2473085229662265
plus_vs_minus_tv:          0.484226014211117
```

At the selected target:

```text
which_path_prob_norm:      0.11488179909232546
eraser_plus_prob_norm:     0.00042440881178795536
eraser_minus_prob_norm:    0.23435920865002566
```

So the plus branch nearly erased the target while the minus branch enhanced it.

### `hc_local_u1`

The destructive pair was weaker but still clear:

```text
interference ratio:        -0.49662333493197414
phase gap:                 2.092324011411052
```

No-signalling again held to numerical precision:

```text
no_signal_l1_unnormalized: 5.108667463127499e-21
no_signal_tv_normalized:   9.64939933512099e-17
```

Conditional branches differed:

```text
plus_vs_which_tv:          0.15036179437399155
minus_vs_which_tv:         0.18426527912227994
plus_vs_minus_tv:          0.3346270734962716
```

At the selected target:

```text
which_path_prob_norm:      0.117580413927961
eraser_plus_prob_norm:     0.05374222392748448
eraser_minus_prob_norm:    0.1958127996751056
```

### Interpretation

This is the finite-atlas quantum-eraser analogue.

- Which-path readout keeps the gate/path alternatives distinguishable.
- Eraser readout recombines alternatives in a \(+/-\) marker basis.
- Conditional branches show different interference patterns.
- Their sum exactly recovers the which-path distribution.

Thus:

\[
P_+ + P_- = P_{\mathrm{which}}
\]

but:

\[
P_+ \neq P_{\mathrm{which}}, \qquad P_- \neq P_{\mathrm{which}}.
\]

The EHF reading is:

> Delayed choice is a late choice of admissible comparison map, not retrocausal rewriting of the path.

**EHF verdict:** Strongly strengthens EHF as a comparison-first account of measurement-like phenomena.

---

## 5.10 QM-08 — Bell factorisation / measurement-context audit

**Question:** Does the EHF two-body/Fock lift support Bell-style correlations, and do Bell's factorisation and measurement-context assumptions map cleanly onto comparison-first atlas structure?

QM-08 separated product controls, constructed Bell-state sanity checks, commuting diagonal controls, free-evolved product states, and contact-evolved product states.

### Main result

The implementation behaved correctly:

- product and random-product controls stayed at or below the classical CHSH bound;
- constructed Bell states reached

  \[
  |S|\approx 2.828427 \approx 2\sqrt2;
  \]

- no-signalling diagnostics remained at numerical precision;
- contact-evolved states became entangled/non-factorisable;
- contact-evolved states did **not** violate the fixed-setting CHSH test.

For the Odd Preserve run, the best fixed-setting contact values were below the violation threshold:

```text
contact_evolved_max_entropy_t6 qubit |S|: 1.7094
contact_evolved_max_chsh_t4 qubit |S|:    1.9830
```

For Johnson, the contact fixed-setting values were also below 2.

**Interpretation:**

QM-08 established that the finite-atlas/Fock machinery can host Bell states and can generate entanglement via contact dynamics. It did not show raw Bell violation for contact-generated states under the fixed settings tested.

**EHF verdict:** Supports contextual entanglement structure, not a claim that Bell is wrong.

---

## 5.11 QM-08B — Optimised CHSH / entanglement witness audit

**Question:** If fixed settings do not reveal CHSH violation, do contact-generated states contain Bell-visible sectors under optimisation, filtering, or Schmidt witnesses?

QM-08B separated three levels:

1. **embedded full-atlas pair CHSH** — conservative, non-postselected;
2. **postselected atlas-pair CHSH** — filtered two-qubit sector witness;
3. **Schmidt-filtered CHSH** — ideal entanglement witness, not a raw Bell experiment.

### Main result

For both Odd Preserve and Johnson:

- embedded full-atlas contact CHSH stayed below 2;
- postselected atlas-pair sectors showed strong CHSH violation;
- Schmidt-filtered witnesses showed CHSH violation;
- product controls stayed non-violating;
- constructed Bell controls reached \(2\sqrt2\).

Representative Odd Preserve result:

```text
best contact embedded |S|:          1.99999998218037
best contact atlas-postselected S:  2.81223221893809
postselected mass:                  0.000179734490272615
best contact Schmidt-filtered S:    2.05782456596776
```

Representative Johnson result:

```text
best contact embedded |S|:          1.99999978042609
best contact atlas-postselected S:  2.8223211684098
postselected mass:                  0.00121215188590291
best contact Schmidt-filtered S:    2.15648033085896
```

**Interpretation:**

Contact dynamics generates high-dimensional entangled states. Bell-visible two-dimensional sectors exist after filtering/optimisation, but the full unfiltered comparison remains CHSH-classical in these scans.

**EHF verdict:** Strengthens the comparison-context picture while avoiding overclaiming raw Bell nonlocality.

---

## 5.12 QM-08C — Full-atlas observable optimisation audit

**Question:** Can broader full-atlas, non-postselected observable families reveal CHSH violation for contact-generated states?

QM-08C searched:

1. direct diagonal/commuting atlas observables;
2. Heisenberg-evolved diagonal observables;
3. a combined bank including direct, evolved, and qubit-anchor sanity observables.

### Result

No full non-postselected contact-state CHSH violation was found.

Representative Odd Preserve maxima:

```text
direct diagonal:      |S|=1.99942912988984
Heisenberg diagonal:  |S|=1.99820430978832
full combined:        |S|=1.99975985730766
```

Representative Johnson maxima:

```text
direct diagonal:      |S|=1.99914206562604
Heisenberg diagonal:  |S|=1.99866559740476
full combined:        |S|=1.99958020831133
```

**Interpretation:**

The current evidence is:

\[
\text{entanglement exists, filtered Bell-visible sectors exist, but raw full-atlas CHSH violation has not been found.}
\]

This is a meaningful negative/constraint result.

**EHF verdict:** Supports contextual entanglement visibility rather than raw full-atlas Bell nonlocality.

---

## 5.13 QM-09 — QED connection phase audit

**Question:** Can the hand-built phase modes be replaced by a finite-atlas connection/curvature mechanism?

QM-09 compared:

1. no phase;
2. flat-gradient/pure-gauge phase;
3. non-flat local connection phase.

### Odd Preserve result

The no-phase and flat-gradient controls produced no destructive interference in the scanned cases. The non-flat `qed_local` connection produced nonzero curvature and strong destructive interference:

```text
nonflat fraction:        ~0.8904
destructive fraction:    ~0.4726
best destructive ratio:  ~-0.99985
phase gap:               ~pi
```

Gauge covariance, Hermiticity, spectrum checks, and norm drift remained at numerical precision.

### Johnson control

Johnson also passed the gauge-control tests, but curvature produced a weaker destructive-interference landscape than Odd Preserve.

**Interpretation:**

This improves the phase story:

\[
\text{connection curvature} \Rightarrow \text{phase-sensitive interference}.
\]

It is stronger than arbitrary phase decoration, while still remaining a finite-atlas toy connection rather than physical QED.

**EHF verdict:** Strong partial pass.

---

## 5.14 QM-09B — Connection curvature response audit

**Question:** Do physical response diagnostics track curvature rather than arbitrary edge phase?

QM-09B swept connection strength \(\alpha\) and used a deliberately nontrivial flat-gradient control.

### Main result

The pure-gauge/flat connection had large edge phases but essentially zero curvature and zero physical shift. The curved connection produced curvature-controlled changes in:

- spectrum,
- return probability,
- destructive-interference fraction,
- best destructive ratio.

Representative Odd Preserve result:

```text
flat phase max:             ~3.066
flat curvature max:         ~4.44e-16
flat spectrum shift:        ~6.66e-16
qed_local max curvature:    pi
qed_local destructive frac: ~0.4726
qed_local spectrum shift:   ~0.3222
qed_local return shift:     ~0.0274
```

Representative Johnson result:

```text
flat phase max:             ~3.137
flat curvature max:         ~1.53e-15
qed_local max curvature:    ~3.047
qed_local destructive frac: ~0.0788
qed_local spectrum shift:   ~0.5627
qed_local return shift:     ~0.1009
```

**Interpretation:**

\[
\boxed{\text{phase effects track connection curvature, not arbitrary edge-phase decoration.}}
\]

**EHF verdict:** Strong pass.

---

## 5.15 QM-09C — Probe-19 connection import audit

**Question:** Can a QED Probe-19 physical edge mode be imported into the QM bridge as a connection and reproduce curvature-controlled response?

QM-09C first ran in template/fallback mode, then an exporter was built from the QED folder to reconstruct a Probe-19 physical 1-form mode and write a QM-09C-compatible connection JSON.

### Successful n=6 import test

The imported Probe-19 connection matched all selected edges:

```text
coverage: 1.0
matched: 270 / 270 edges
fallback: False
```

The imported physical edge mode produced nonzero curvature and strong interference response:

```text
max curvature:              ~3.1336
max destructive fraction:   ~0.4559
max spectrum shift:         ~0.2825
max return shift:           ~0.0715
best destructive ratio:     ~-0.999999
```

The flat-gradient control again had large edge phases but essentially zero curvature and no physical response.

**Interpretation:**

This is the first direct bridge:

\[
\text{Probe-19 physical edge mode}
\Rightarrow
\text{QM bridge connection import}
\Rightarrow
\text{curvature-controlled phase response}.
\]

**Caveat:**

The tested import was an \(n=6\) Probe-19 connection. It is not identical to the earlier \(n=7\) OPW bridge testbed or the mature \(n\ge9\) packet-action regime.

**EHF verdict:** Strong bridge result, pending broader import/scaling tests.


---

## 5.16 QM-10 — OPW packet-history amplitude audit

**Question:** Can the mature OPW boundary-packet Markov State Model supply the amplitude-magnitude side of a finite path-sum model?

QM-10 used the 16-state OPW packet transition law on Boolean boundary packets

\[
b\in\{0,1\}^4
\]

and defined packet histories

\[
\gamma=(b_0,b_1,\dots,b_T).
\]

For a packet MSM with stationary distribution \(\mu\) and transition matrix \(T_n\), the stochastic packet-history action is

\[
A_n[\gamma]
=
-\log \mu(b_0)
-
\sum_{t=0}^{T-1}\log T_n(b_t,b_{t+1}).
\]

Equivalently,

\[
P_n[\gamma]
=
\mu(b_0)\prod_t T_n(b_t,b_{t+1}),
\qquad
A_n[\gamma]= -\log P_n[\gamma].
\]

The proposed amplitude magnitude is

\[
|a(\gamma)|=e^{-A_n[\gamma]/2}=\sqrt{P_n[\gamma]}.
\]

### Smoke test

A built-in demo MSM first verified the bookkeeping:

```text
max_prob_vs_amp_sq_error: 5.551e-17
max_enum_vs_direct_error: 7.216e-16
best_is_gray: True
```

This was only a smoke test and is not OPW evidence.

### Official OPW runs

QM-10 was then run on the mature OPW packet MSM outputs for \(n=11\) and \(n=13\), using endpoint coarse-graining and complete enumeration for \(T=4\).

Representative \(n=11,T=4\) result:

```text
official_transition_supplied:       True
enumeration truncated:              False
total enumerated probability:       1
total amplitude-square:             1
direct dynamic total mass:          1
max |prob - amp_sq| by coarse:      2.776e-17
max |enum - direct| by coarse:      3.608e-16
best is Hamming-1 Gray cycle:       True
```

Representative \(n=13,T=4\) result:

```text
official_transition_supplied:       True
enumeration truncated:              False
records:                            133758
max_prob_vs_amp_sq_error:           2.776e-17
max_enum_vs_direct_error:           3.747e-16
best_is_gray:                       True
```

The least-action ordinary packet histories were self-retention dominated, especially around high-retention packet states such as \(1111\), \(0101\), and \(1010\). This supports the structural boundary-inertia reading: low action corresponds to low packet mobility. This should not yet be identified with physical mass.

The Hamiltonian-cycle search found Hamming-1 Gray cycles as the best sampled cycles, consistent with the separate OPW Probe-60 least-action locality result. In QM-10 the Gray-cycle part is corroborative because the cycle search was sampled/truncated; the action-magnitude identity itself was fully verified for the enumerated \(T=4\) path families.

**Interpretation:**

\[
\boxed{
\text{OPW packet histories supply a finite stochastic action whose half-action exponential gives amplitude magnitudes.}
}
\]

**EHF verdict:** Official OPW pass.

---

## 5.17 QM-11A — OPW square-relation phase-source audit

**Question:** Do OPW square relations provide credible candidate data for a phase or holonomy source on the packet-history layer?

QM-11A imported the OPW square-relation rank summaries and chamber/square support data. The key \(n=9\) square-relation facts were:

```text
vertices:                         20160
undirected edges:                  67200
unique square relations:           48720
packet-transition projection rank: 58 / 144
component-packet-edge rank:        1371 / 3534
full directed-edge rank:           39691 / 134400
packet square support:             16 / 16 packet states
```

The square support was nontrivially coupled to packet statistics. Representative correlations from the audit were:

```text
square-vs-mu Spearman/Pearson:              0.78435 / 0.921991
square-vs-self-retention Spearman/Pearson:  0.819801 / 0.57455
square-vs-mobility Spearman/Pearson:       -0.819801 / -0.57455
square-vs-row-entropy Spearman/Pearson:    -0.62039 / -0.38101
```

This means the square-relation geometry is not merely a disconnected chamber invariant. It projects down to the same packet-transition layer used by QM-10 and is strongly coupled to stationary mass, self-retention, and low mobility.

**Interpretation:**

\[
\text{OPW square relations}
\Rightarrow
\text{nontrivial packet-transition rowspace}
\Rightarrow
\text{candidate phase/holonomy source}.
\]

**Caveat:** QM-11A does not construct a phase \(\theta(\gamma)\). It only tests whether the square-relation data are plausible phase-source data.

**EHF verdict:** Pass as a phase-source candidate.

---

## 5.18 QM-11B — OPW square-relation phase-candidate construction

**Question:** Can OPW square-relation packet data be turned into packet-level phase candidates with gauge-style controls and measurable interference response?

QM-11B constructed several packet-edge phase candidates from OPW square-relation support:

```text
zero
pure_gradient_square
oriented_square_flux
mobility_square_flux
retention_square_flux
gray_square_flux
```

The audit kept the QM-10 amplitude magnitude

\[
|a(\gamma)|=\sqrt{P_n[\gamma]}
\]

and tested path amplitudes

\[
a(\gamma)=\sqrt{P_n[\gamma]}e^{i\theta(\gamma)}.
\]

### Gauge-style curvature controls

For both \(n=11\) and \(n=13\), the pure-gradient candidate had large edge phase but zero packet-cycle curvature up to numerical precision:

```text
pure_gradient_square edge_max:       3.29524
curv3_max:                          ~4.44e-16
curv4_max:                          ~8.88e-16
curv4_nonzero:                       0.000
pure-gradient zero-curvature pass:   True
```

Non-gradient square-flux candidates had nonzero cycle curvature. Representative \(n=11\) values were:

```text
oriented_square_flux    curv4_nonzero=0.636
mobility_square_flux    curv4_nonzero=0.996
retention_square_flux   curv4_nonzero=0.996
gray_square_flux        curv4_nonzero=0.914
```

### Interference response

For \(n=11\):

```text
verdict:                         PASS_PHASE_CANDIDATE_CONSTRUCTION
max |prob - amp_sq| by endpoint: 4.163e-17
nontrivial_response_count:        16
best candidate:                   oriented_square_flux alpha=pi
TV_vs_zero:                       0.439125
total_ratio:                      0.000604626
destructive_endpoints:            16
```

For \(n=13\):

```text
verdict:                         PASS_PHASE_CANDIDATE_CONSTRUCTION
max |prob - amp_sq| by endpoint: 2.776e-17
nontrivial_response_count:        16
best candidate:                   oriented_square_flux alpha=pi
TV_vs_zero:                       0.365374
total_ratio:                      0.000767829
destructive_endpoints:            16
```

**Interpretation:**

\[
\text{same packet-action magnitude law}
+
\text{square-derived non-gradient phase}
\Rightarrow
\text{controlled endpoint interference}.
\]

The strongest raw response was consistently from `oriented_square_flux`. The `gray_square_flux` candidate was weaker but conceptually important because it is tied to the Gray-cycle locality story.

**Caveat:** These are packet-level phase candidates, not a derivation of the physical quantum phase.

**EHF verdict:** Pass as a controlled phase-candidate construction.

---

## 5.19 QM-12 — OPW/QED action-phase path-sum audit

**Question:** Can OPW packet-action magnitudes and OPW/QED candidate phases be combined into one controlled finite action-phase path-sum model?

QM-12 combined the pieces into the path-amplitude form

\[
a(\gamma)
=
e^{-A_n[\gamma]/2}e^{i\theta(\gamma)}
=
\sqrt{P_n[\gamma]}e^{i\theta(\gamma)}.
\]

It used source-resolved path sums to make the pure-gradient control stricter. The stochastic MSM is the dephased/history-distinguished limit:

\[
\sum_\gamma |a(\gamma)|^2,
\]

whereas a coherent path sum uses

\[
\left|\sum_\gamma a(\gamma)\right|^2.
\]

These need not agree even at zero phase, because zero phase is still coherent path addition rather than classical history distinction.

### \(n=11,T=4\)

```text
verdict:                                      PASS_ACTION_PHASE_PATHSUM
row sum max abs error:                        1.110e-16
enumeration truncated:                         False
total enumerated stochastic probability:       1
max |prob - amp_sq| by endpoint:               1.388e-17
max |enum - direct Markov| by endpoint:        3.469e-16
zero-phase TV(normalised) vs stochastic MSM:   0.0951092
pure-gradient curvature control pass:          True
pure-gradient source-intensity control pass:   True
```

Best action-phase response for \(n=11\):

```text
candidate:                         oriented_square_flux alpha=pi
curv4:                              5.47197
TV_vs_zero:                         0.142463
TV_vs_stoch:                        0.075397
total_ratio:                        0.0738929
destructive_endpoints:              16
min_ratio:                          0.0427576
```

### \(n=13,T=4\)

```text
verdict:                                      PASS_ACTION_PHASE_PATHSUM
row sum max abs error:                        1.110e-16
enumeration truncated:                         False
total enumerated stochastic probability:       1
max |prob - amp_sq| by endpoint:               1.388e-17
max |enum - direct Markov| by endpoint:        3.608e-16
zero-phase TV(normalised) vs stochastic MSM:   0.0991385
pure-gradient curvature control pass:          True
pure-gradient source-intensity control pass:   True
```

Best action-phase response for \(n=13\):

```text
candidate:                         oriented_square_flux alpha=pi
curv4:                              5.47197
TV_vs_zero:                         0.129891
TV_vs_stoch:                        0.0641761
total_ratio:                        0.0953732
destructive_endpoints:              16
min_ratio:                          0.0577127
```

### Interpretation

QM-12 verifies the combined finite action-phase model:

\[
\boxed{
\text{OPW packet action magnitudes}
+
\text{OPW square-derived phases}
\Rightarrow
\text{controlled finite action-phase path sum}.
}
\]

The pure-gradient candidate is curvature-free and source-intensity equivalent to zero phase. Non-gradient square-flux candidates produce curvature-linked interference. The strongest stable candidate in these runs is `oriented_square_flux`, while `gray_square_flux` remains conceptually important as the bridge to least-action Gray locality.

**Caveat:** This is a finite-atlas action-phase analogue. It is not a derivation of physical quantum mechanics or QED.

**EHF verdict:** Strong synthesis pass.

---

## 6. Current bridge chain

The completed bridge chain is now:

\[
\text{admissible atlas}
\Rightarrow
\text{Hilbert basis}
\Rightarrow
\text{Hermitian generator}
\Rightarrow
\text{unitary evolution}
\Rightarrow
\text{interference}
\Rightarrow
\text{measurement as coarse comparison}
\Rightarrow
|\psi|^2
\Rightarrow
\text{Fock-like lift}
\Rightarrow
\text{delayed-choice/eraser behaviour}
\Rightarrow
\text{contextual entanglement diagnostics}
\Rightarrow
\text{curvature-controlled connection phase response}.
\]

The OPW packet/action work adds a second, path-history layer:

\[
\text{OPW packet MSM}
\Rightarrow
A_n[\gamma]=-
\log P_n[\gamma]
\Rightarrow
|a(\gamma)|=e^{-A_n[\gamma]/2}
\Rightarrow
\text{square-derived candidate phase}
\Rightarrow
\text{finite action-phase path sum}.
\]

In compressed form:

\[
\boxed{
\text{admissible comparison structure can support both a finite QM skeleton and a controlled OPW action-phase path-sum analogue.}
}
\]

---

## 7. What this does and does not prove

## 7.1 What the probes support

The probes support the following finite-atlas claims:

1. Hilbert-space-like structure can be built from an admissible atlas.
2. Hermitian generators arise naturally from symmetric local comparison moves.
3. Unitary dynamics is available without imposing classical Markov flow.
4. Coherent alternatives interfere.
5. Atlas-induced phase modes can generate destructive interference.
6. Measurement-like behaviour can be represented as coarse comparison/projector structure.
7. The Born rule is selected by conservation and projector compatibility.
8. Fock-like many-body lifting works through Kronecker sums and exchange sectors.
9. Delayed-choice / quantum-eraser logic appears as late basis/comparison choice.
10. Two-body/Fock states support entanglement and Bell-state controls.
11. Contact dynamics generates entangled states with filtered Bell-visible sectors.
12. Full unfiltered atlas CHSH violation has not yet been found.
13. Connection phases behave gauge-covariantly: flat phases are physically invisible, while curvature drives spectral/interference response.
14. Probe-19 physical edge modes can be imported as finite-atlas connections.
15. OPW packet histories supply a finite stochastic action \(A_n[\gamma]=-
\log P_n[\gamma]\).
16. The half-action exponential \(e^{-A_n[\gamma]/2}\) gives amplitude magnitudes whose squared weights reproduce OPW packet-history probabilities.
17. OPW square relations project nontrivially onto the 16-state packet-transition layer and are coupled to packet retention/mobility structure.
18. OPW square-relation data can construct non-gradient packet-level phase candidates with nonzero cycle curvature.
19. Pure-gradient packet phases are curvature-free and source-intensity equivalent to zero phase under the QM-12 source-resolved control.
20. OPW packet-action magnitudes and square-derived phase candidates combine into a controlled finite action-phase path-sum model for \(n=11\) and \(n=13\).

## 7.2 What the probes do not yet prove

The probes do **not** yet prove:

1. that physical quantum mechanics is fully derived from EHF,
2. that the Standard Model Hilbert space has been recovered,
3. that physical constants, masses, charges, and coupling constants have been derived,
4. that Lorentz invariance or relativistic QFT has been obtained,
5. that the phase modes used here are uniquely forced by EHF,
6. that raw full-atlas Bell/CHSH violation has been reproduced for natural contact dynamics,
7. that Bell's theorem is wrong or evaded,
8. that the continuum limit exists,
9. that actual laboratory quantum experiments are explained better than standard QM.

The strongest immediate caveat has shifted again. Early hand-built phase modes have now been partly replaced by finite-atlas connection/curvature audits, a Probe-19 import test, and OPW square-derived phase-candidate audits. The OPW packet-action magnitude and square-phase path-sum have now been combined at the packet level. The remaining caveats are uniqueness, physical interpretation, scaling, and alignment: the phase candidates are not yet uniquely forced, the packet-level model is not yet physical QED, and the OPW packet/square phase must still be aligned with the QED-atlas connection import through explicit comparison maps.

---

## 8. Relation to QED-atlas work

The QED Probe 19 work produced a gauge-atlas toy model with:

- edge connection \(A\),
- plaquette curvature \(F=dA\),
- Bianchi-style closure,
- conserved current,
- charge as matter-transport boundary,
- back-reaction,
- Coulomb-like interaction energy,
- wave-like field modes,
- plaquette-filling transition from localized/floppy modes to extended coherent modes.

The QM bridge program supplies complementary amplitude machinery:

\[
\text{Hilbert basis} + \text{Hermitian evolution} + \text{interference} + \text{Born readout} + \text{Fock lift}.
\]

QM-09 through QM-09C began the direct phase bridge:

\[
\text{QED connection } A
\Rightarrow
\text{finite-atlas phase/holonomy}
\Rightarrow
\text{curvature-controlled spectral/interference response}.
\]

The local QM-09C confirmation imported a Probe-19 physical 1-form mode on the \(n=6,L=3\) Hamilton-cycle atlas, matched all 270 selected edges, and produced nontrivial curvature, spectrum shift, return shift, and near-perfect destructive interference while pure-gauge controls remained invisible.

The OPW packet/action work adds the magnitude side:

\[
A_n[\gamma]=-
\log P_n[\gamma],
\qquad
|a(\gamma)|=e^{-A_n[\gamma]/2}.
\]

The emerging synthesis target is therefore:

\[
a(\gamma)
=
e^{-A_n[\gamma]/2}e^{i\theta(\gamma)},
\]

where \(\theta(\gamma)\) should eventually be obtained from QED-atlas connection holonomy, OPW square-loop curvature, or an explicit comparison map between the two.

---

## 9. OPW Update: Packet Action, Large-n Retraction, and Square-Loop Geometry

Since QM-07, Odd Preserve-World has developed a more mature boundary-packet regime for odd \(n \ge 9\). This is important for the next stage of the QM bridge because it gives a concrete finite-state substrate for path histories, action weights, and possible holonomy-derived phases.

This update should be treated as a bridge refinement, not as a replacement for the earlier QM-01...QM-07 testbed. The earlier QM bridge OPW probes used the \(n=7\) largest component under the `cyclic_all_starts` convention. The newer OPW packet/action/square-loop results mostly use the mature \(n \ge 9\) boundary-packet regime. These structures are related but should not be casually identified.

### 9.1 New OPW ingredients

The new OPW ingredients are:

1. **Exact 16-state Boolean boundary packet MSM for \(n \ge 9\).**  OPW now has a finite packet-level Markov State Model on four-bit Boolean boundary packets.
2. **Large-\(n\) packet retraction.**  Deleting and reinserting the newest labels \(n+1,n+2\) gives a packet-level retraction. Core/core insertion preserves the four-bit packet exactly; packet disturbance is bounded by \(O(1/n)\); finite boundary-order refinement gives packet disturbance approximately \(703/(90n)\).
3. **Packet path action.**  For packet histories \(\gamma=(b_0,b_1,\dots,b_T)\),

   \[
   A_n[\gamma]
   =
   -\log \mu(b_0)
   -
   \sum_t \log T_n(b_t,b_{t+1})
   =
   -\log P_n[\gamma].
   \]

   This is a discrete stochastic action derived from the packet transition law, not a postulated Lagrangian.
4. **Least-action Gray cycles.**  OPW Probe 60 found that minimum-action Hamiltonian packet cycles over all positive packet transitions are Hamming-1 Gray cycles. The standard reflected Gray code is admissible, but it is not the minimum-action representative.
5. **Boundary inertia.**  As \(n\) grows, packet self-retention increases and packet mobility decreases. This gives a structural inertia analogue, not yet physical mass.
6. **Square-loop geometry.**  At \(n=9\), OPW is triangle-free, pentagon-free, square-supported, and hard-core clean. Square-curvature species recover the same chamber-family taxonomy as weighted slot-signature quotients.

### 9.2 Bridge implication now tested by QM-10 through QM-12

The original bridge proposal was:

\[
|a(\gamma)| \sim e^{-A_n[\gamma]/2},
\qquad
|a(\gamma)|^2 \sim e^{-A_n[\gamma]}.
\]

QM-10 verified this magnitude bridge on real OPW packet MSMs for \(n=11\) and \(n=13\). QM-11A showed that OPW square relations project nontrivially to the packet-transition layer and are a plausible phase-source geometry. QM-11B constructed square-derived packet phase candidates with gauge-style controls. QM-12 combined the pieces into a source-resolved finite action-phase path-sum:

\[
a(\gamma)=e^{-A_n[\gamma]/2}e^{i\theta(\gamma)}.
\]

The current OPW bridge result is therefore stronger than the original proposal:

\[
\text{packet path probability}
\Rightarrow
\text{action magnitude}
\Rightarrow
\text{square-derived candidate phase}
\Rightarrow
\text{finite-atlas action-phase path sum}.
\]

### 9.3 Conservative interpretation

The OPW update strengthens the substrate of the QM bridge, especially for action-weighted packet histories and possible holonomy-derived phases. It does **not** show that EHF has derived quantum mechanics.

The safe statement is:

> Odd Preserve-World now provides a stronger finite-atlas substrate for the QM bridge: exact boundary-packet MSM dynamics, a discrete packet action \(A_n=-\log P_n\), least-action Gray-cycle histories, large-\(n\) boundary inertia, square-loop relation geometry, and a tested finite action-phase path-sum analogue. These results motivate scaling and alignment audits, not a claim of physical derivation.

---

## 10. Proposed next probes

The probe numbering now preserves the actual completed chronology:

- **Completed:** QM-01 through QM-12.
- **Next stage:** scaling, robustness, and alignment of the OPW action-phase model with the QED-atlas connection branch.

### 10.1 QM-13 — Scaling, robustness, and ablation audit

Repeat the key packet/action/phase probes across mature odd values \(n\ge9\), time horizons, phase candidates, and coarse-graining choices.

Core checks:

1. Does the action-magnitude identity remain exact for available \(n=9,11,13\) packet MSMs and nontruncated path horizons?
2. Is the observed phase-candidate ordering stable?

   ```text
   oriented_square_flux strongest raw response
   gray_square_flux conceptually linked to least-action Gray locality
   retention_square_flux linked to boundary inertia
   pure_gradient_square trivial/gauge-like
   ```

3. Are pure-gradient phases always curvature-free and source-intensity equivalent to zero phase?
4. Are the main non-gradient responses stable under endpoint, source-resolved, and other admissible coarse-grainings?
5. Do the sampled Gray-cycle minima remain compatible with the OPW Probe-60 least-action theorem?
6. Do the results survive changes in \(T\), especially \(T=3,4\) exactly and \(T=5\) when enumeration is truncated or replaced by dynamic programming?

### 10.2 QM-14 — OPW/QED phase-alignment audit

The packet-level OPW square phases and the QED Probe-19 edge connection currently live on different but related finite atlases. QM-14 should ask whether they can be aligned by an explicit comparison map rather than analogy.

Questions:

1. Can a QED Probe-19 connection be projected or retracted to packet-transition phases?
2. Can OPW square-derived phases be lifted to edge-level or loop-level connection data?
3. Does the imported QED connection and the OPW square phase agree on cycle-curvature signs, destructive sectors, or chamber-family taxonomy?
4. Can the \(n=7\) OPW bridge testbed, the mature \(n\ge9\) packet regime, and the \(n=6\) Probe-19 connection import be related through explicit admissible comparison maps?

This is the next high-value synthesis target:

\[
\text{QED Probe-19 connection}
\quad\leftrightarrow\quad
\text{OPW square phase}
\quad\leftrightarrow\quad
\text{packet action-phase path sum}.
\]

---

## 11. Working conclusion

The EHF Quantum Mechanics Bridge Program has not derived physical quantum mechanics. What it has established is a coherent finite-atlas skeleton:

\[
\text{admissible comparison atlas}
\Rightarrow
\text{Hilbert basis}
\Rightarrow
\text{unitary evolution}
\Rightarrow
\text{interference}
\Rightarrow
\text{coarse-comparison measurement}
\Rightarrow
|\psi|^2
\Rightarrow
\text{Fock-like lift}
\Rightarrow
\text{contextual entanglement diagnostics}
\Rightarrow
\text{curvature-controlled phase response}.
\]

It has also established a more concrete OPW path-history bridge:

\[
\text{packet path probability}
\Rightarrow
A_n[\gamma]=-
\log P_n[\gamma]
\Rightarrow
|a(\gamma)|=e^{-A_n[\gamma]/2}
\Rightarrow
\text{square-derived phase candidate}
\Rightarrow
\text{finite-atlas action-phase path sum}.
\]

The combined tentative amplitude is

\[
a(\gamma)
=
e^{-A_n[\gamma]/2}e^{i\theta(\gamma)}.
\]

The conservative claim is:

> EHF/OPW now has a controlled finite-atlas analogue of an action-weighted path amplitude. The OPW packet MSM supplies stochastic action magnitudes; OPW square-relation data supplies non-gradient candidate phases with gauge-style controls; and QED Probe-19 connection imports independently support curvature-controlled phase response. This is bridge evidence, not a derivation of physical quantum mechanics or QED.

The immediate next task is robustness and alignment, not a new conceptual leap.
