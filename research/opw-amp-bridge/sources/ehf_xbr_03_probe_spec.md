# EHF-XBR-03
## Canonical Middle-Block Bridge Operator and Intertwining Obstruction

### Purpose

XBR-02 established two exact lifts over one common chart groupoid:

\[
\mathcal F_{\rm dyn},
\qquad
\mathcal F_{\rm amp}.
\]

That result did not produce a canonical linear map between them. XBR-03 tests
the most direct map assembled from already proved common structures.

---

## 1. Channel data

For each of the 35 reference AMP channels \(A\), let

\[
C_A
\]

be its \(n=9\) source fibre. Audit-01 identifies this fibre with an OPW3
chamber.

Define:

\[
M_A:\mathbb Q^{360}\longrightarrow\mathbb Q^{C_A}
\]

as the restriction of the \(720\)-incidence middle-block growth map;

\[
D_A:\mathbb Q^{C_A}\longrightarrow\mathbb Q^{72}
\]

as the exact signed AMP deletion map;

\[
V_A\subseteq\mathbb Q^{72}
\]

as the exact transmitted AMP relation image;

\[
A_A:\mathbb Q^{C_A}\longrightarrow\mathbb Q^{C_A}
\]

as the OPW3 chamber adjacency operator.

---

## 2. Canonical depth-\(k\) bridge

Define

\[
B_A^{(k)}
=
V_A D_A A_A^k M_A.
\]

This construction contains no fitted coefficients and no chartwise arbitrary
choice.

- \(k=0\): direct state-growth/deletion bridge;
- \(k=1\): one OPW3 adjacency step;
- \(k=2,3\): first mediated depths.

All ranks are computed exactly over \(\mathbb Q\).

---

## 3. Direct-support test

The middle-block channel places the two newest labels in the central positions.
The AMP deletion channel is active only when the deleted label is adjacent to
the anchor.

The probe tests rather than assumes whether

\[
D_A M_A=0.
\]

It also computes the exact graph distance between the middle-block support and
the deletion-active support.

---

## 4. Adjacency-intertwining obstruction

The deletion-adjoint AMP lift is

\[
W_A=\operatorname{row}(V_A D_A)
\subseteq
\mathbb Q^{C_A}.
\]

A direct intertwiner

\[
A_AJ_A=J_AK_A
\]

on the complete AMP image requires \(W_A\) to be \(A_A\)-invariant.

The exact test is

\[
\operatorname{rank}
\begin{pmatrix}
W_A\\
W_AA_A
\end{pmatrix}
=
\operatorname{rank}(W_A).
\]

Failure is a genuine linear-algebraic obstruction to a direct full-image
adjacency intertwiner.

---

## 5. Expected result categories

The probe distinguishes:

- direct canonical bridge;
- one-step mediated bridge;
- two-step mediated bridge;
- partial relation visibility;
- full relation visibility;
- direct intertwiner;
- exact intertwining obstruction.

A bridge at \(k>0\) means structural propagation under OPW adjacency. It does
not mean physical time evolution.

---

## Run

From the `OPW3` directory, with `AMP` as a sibling directory:

```bash
python3 scripts/ehf_xbr_03_canonical_middle_block_bridge.py \
  --opw-base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --amp-base-script ../AMP/scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --amp-helper-script ../AMP/scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --amp-rank-script ../AMP/scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --amp-lattice-script ../AMP/scripts/ehf_amp_found_03c_exact_tail_filtration_lattice.py \
  --xbr02-run-dir runs/ehf_xbr_02 \
  --max-depth 3 \
  --out-dir runs/ehf_xbr_03 \
  --strict
```

### Outputs

- `channel_bridge_ledger.csv`
- `bridge_class_summary.csv`
- `run_summary.json`

### Interpretation boundary

The OPW adjacency is used as a canonical finite structural operator. It is not
identified with a physical Hamiltonian. No claim is made that the bridge
derives scattering amplitudes or quantum time evolution.
