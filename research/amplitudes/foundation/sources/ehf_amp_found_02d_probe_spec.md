# EHF-AMP-FOUND-02D
## Exact Residue Spectrum and Two-Fibre Gluing Law

**Status:** executable probe specification  
**Programme:** EHF amplitude foundations  
**Primary transition:** reflection-aware delete-8, equivalently the relation map from eight points to seven points  
**Dependencies:** EHF-AMP-FOUND-02A v0.3 and EHF-AMP-FOUND-02B

---

## 1. Motivation

EHF-AMP-FOUND-02C established at two independent kinematic seeds that the reflection-aware residue map

\[
A=D_8 B_8
\]

from the direct sum of eight-point fibre-local Parke--Taylor relation spaces has

\[
\dim \mathcal R^{\mathrm{loc}}_8=525,
\qquad
\operatorname{rank}A=110,
\qquad
\dim\ker A=415.
\]

Its nonzero singular values appeared in four exact-looking classes. Their squares were

\[
1,\qquad \frac65,\qquad \frac85,\qquad \frac95
\]

with multiplicities

\[
20,\qquad40,\qquad40,\qquad10.
\]

The full Moore--Penrose section used exactly twenty eight-point fibres, all with label \(8\) outside the anchor parity set, and assigned them equal total squared weight. The exceptional AMP-18 residue had a global minimum-norm ancestor supported equally on two fibres.

02D tests whether these observations are consequences of one finite combinatorial decomposition rather than unrelated numerical coincidences.

---

## 2. Active fibres and the flip involution

Every eight-point fibre is labelled by a four-element anchor set

\[
E\subset\{1,\ldots,8\},
\qquad
1\in E.
\]

The delete-8 channel is active precisely when

\[
8\notin E.
\]

There are

\[
\binom63=20
\]

such fibres.

Define the complementary flip on the six non-anchor labels \(2,\ldots,7\):

\[
\phi(E)
=
\{1\}\cup
\left(
\{2,\ldots,7\}\setminus(E\setminus\{1\})
\right).
\]

Because \(E\setminus\{1\}\) has size three, \(\phi\) is a fixed-point-free involution on the twenty active fibres. It therefore partitions them into ten unordered pairs

\[
\{F,\phi(F)\}.
\]

---

## 3. Two-fibre image law

For an active fibre \(F\), let

\[
A_F
\]

be the restriction of the residue map to its 15-dimensional local relation space.

The primary pair-channel conjecture is

\[
\operatorname{rank}A_F=11,
\]

and

\[
\operatorname{im}A_F
=
\operatorname{im}A_{\phi(F)}.
\]

Thus each complementary pair defines one 11-dimensional target channel

\[
\mathcal C_F
=
\operatorname{im}A_F
=
\operatorname{im}A_{\phi(F)}.
\]

02D tests whether the ten pair channels are mutually orthogonal and exhaust the full residue image:

\[
\mathcal I_7
=
\bigoplus_{\{F,\phi(F)\}}
\mathcal C_F,
\qquad
10\times11=110.
\]

This would explain the observed rank without reference to random kinematics.

---

## 4. Exact pair spectrum

The candidate squared singular spectrum of every combined pair map

\[
[A_F\;A_{\phi(F)}]
\]

is

\[
1^{\times2},
\qquad
\left(\frac65\right)^{\times4},
\qquad
\left(\frac85\right)^{\times4},
\qquad
\left(\frac95\right)^{\times1}.
\]

The candidate squared spectrum of either single-fibre map is one half of this:

\[
\left(\frac12\right)^{\times2},
\qquad
\left(\frac35\right)^{\times4},
\qquad
\left(\frac45\right)^{\times4},
\qquad
\left(\frac9{10}\right)^{\times1}.
\]

If all ten pair channels have this same spectrum and are mutually orthogonal, the global multiplicities follow immediately:

\[
10(2,4,4,1)=(20,40,40,10).
\]

---

## 5. Candidate minimal polynomial

Let

\[
K=A A^{\mathsf T}.
\]

The observed spectrum predicts

\[
K(K-I)
\left(K-\frac65 I\right)
\left(K-\frac85 I\right)
\left(K-\frac95 I\right)
=0.
\]

The probe evaluates this identity spectrally, records the residual, and verifies exact rational trace moments

\[
\operatorname{tr}(K^m)
=
20
+40\left(\frac65\right)^m
+40\left(\frac85\right)^m
+10\left(\frac95\right)^m
\]

for several powers \(m\).

Agreement establishes a strong exact-spectrum conjecture. It is not a substitute for an analytic derivation.

---

## 6. Fibre-local content inside each pair channel

Let \(P(F)\) be the set of seven-point parent fibres reached by deleting label \(8\) from the pair \(\{F,\phi(F)\}\).

The local-content conjecture is

\[
\dim\left(
\mathcal C_F\cap\mathcal R^{\mathrm{loc}}_7
\right)
=
\sum_{P\in P(F)}\dim R_7(P).
\]

The complementary cross-fibre dimension is then

\[
11-
\sum_{P\in P(F)}\dim R_7(P).
\]

The reduced functional test exposed the sorted pattern

\[
11,7,4,4,4,4,1,1,1,1
\]

for the local dimensions and

\[
0,4,7,7,7,7,10,10,10,10
\]

for their cross-fibre complements. These numbers sum to

\[
38+72=110,
\]

matching 02C. The full cached run must determine whether this pattern reproduces at scientific resolution.

The probe also measures whether the exact spectral decomposition and the fibre-local decomposition commute. They need not be the same decomposition.

---

## 7. Equal two-fibre Moore--Penrose law

Because the two fibres in a pair have the same image, every target vector

\[
y\in\mathcal C_F
\]

has ancestors in either fibre separately.

02D tests whether their induced minimum-norm source metrics agree and whether the pair-restricted Moore--Penrose ancestor always divides its squared norm equally:

\[
\frac{\|x_F\|^2}{\|x_F\|^2+\|x_{\phi(F)}\|^2}
=
\frac12.
\]

This is tested for a complete orthonormal basis of each 11-dimensional pair channel, not only for the exceptional direction.

The equality of the two image subspaces is metric-independent. The exact 50/50 minimum-norm split additionally depends on the Euclidean inner product chosen on source relation coefficients.

---

## 8. Exceptional AMP-18 direction

Let \(v_*\) be the exceptional eight-point relation in

\[
E=\{1,4,5,6\},
\qquad
O=\{2,3,7,8\}.
\]

Its complementary flip partner is

\[
E'=\{1,2,3,7\},
\qquad
O'=\{4,5,6,8\}.
\]

02D reconstructs \(v_*\), computes its residue, and tests whether:

1. the residue lies entirely in the corresponding 11-dimensional pair channel;
2. the global Moore--Penrose ancestor equals the pair-restricted ancestor;
3. exactly the two flip-partner fibres carry support;
4. the squared support is \(1/2+1/2\);
5. the original one-fibre representative remains the minimum-norm preimage when support is restricted to its own fibre;
6. the difference between the one-fibre and two-fibre ancestors lies in the delete-8 kernel.

A positive result would show that the AMP-18 exceptional 50/50 split is not exceptional at all. It would be one instance of a general ten-channel gluing law.

---

## 9. Numerical controls and verdict boundaries

The probe uses:

- reflection-aware deletion inherited from 02A v0.3;
- orthonormal local relation bases inherited from the independently validated cache;
- rank-truncated SVD;
- two-way image-containment tests;
- principal-angle tests between all pair channels;
- rational candidate matching for squared singular values;
- exact fractional trace targets;
- per-column rather than aggregate 50/50 tests;
- explicit source-kernel checks for the exceptional direction.

A successful run supports a finite exact theorem candidate. It does not itself prove the rational values analytically, identify the governing representation, or establish a physical growth law.

---

## 10. Run command

Place the script and specification in `scripts/`, then run:

```bash
caffeinate -i python3 scripts/ehf_amp_found_02d_exact_residue_spectrum_two_fibre_gluing.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --section-script scripts/ehf_amp_found_02b_minimal_nontrivial_growth_sections.py \
  --base-run-dir runs/ehf_amp_found_01_amp18_20 \
  --out-dir runs/ehf_amp_found_02d_seed11 \
  --seed 11
```

The shared cache should make basis loading nearly immediate. The new pair-channel SVD audit is denser than 02C but should still be modest at these dimensions.

A second independent run should use:

```bash
caffeinate -i python3 scripts/ehf_amp_found_02d_exact_residue_spectrum_two_fibre_gluing.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --helper-script scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --section-script scripts/ehf_amp_found_02b_minimal_nontrivial_growth_sections.py \
  --base-run-dir runs/ehf_amp_found_01_amp18_20 \
  --out-dir runs/ehf_amp_found_02d_seed29 \
  --seed 29
```

---

## 11. Output files

The principal outputs are:

```text
summary.json
exact_spectrum_audit.json
flip_pair_audit.json
exceptional_two_fibre_audit.json
spectral_cluster_summary.csv
trace_moment_audit.csv
spectral_local_alignment.csv
flip_pair_channel_summary.csv
flip_pair_overlap_matrix.csv
operator_data.npz
run.log
```

The terminal summary should report five verdicts:

```text
Exact rational spectrum supported
Ten flip-pair channels
Parent-dimension locality law
Equal two-fibre MP law
Exceptional is generic pair instance
```
