# EHF-XBR-04B
## Cross-Prime Ledger Identity and Rational Certification

### Purpose

XBR-04 established exact minimal Krylov closures over three audited finite
fields:

\[
\mathbb F_{1000003},
\qquad
\mathbb F_{65519},
\qquad
\mathbb F_{65521}.
\]

The three headline summaries agree. XBR-04B performs the stronger comparison
and then attempts exact characteristic-zero promotion.

---

## 1. Complete cross-prime identity

For each of the 35 channels and each audited prime, compare:

- initial AMP-lift rank;
- every rank in the block-Krylov rank-growth sequence;
- final closure dimension;
- first stabilization depth;
- invariant-closure flag.

The cross-prime stage passes only when all expected prime rows are present and
the complete rank sequences are identical, not merely the aggregate summary.

---

## 2. Exact rational certificate

For a channel with modular closure dimension \(r\) and stabilization depth
\(d\), reconstruct the integer Krylov matrices

\[
K_{d-1},
\qquad
K_d,
\qquad
K_{d+1}.
\]

Compute their ranks exactly over characteristic zero.

The certificate is:

\[
\operatorname{rank}_{\mathbb Q}K_{d-1}<r,
\]

\[
\operatorname{rank}_{\mathbb Q}K_d=r,
\]

\[
\operatorname{rank}_{\mathbb Q}K_{d+1}=r.
\]

Because

\[
K_0\subseteq K_1\subseteq\cdots,
\]

equality at \(d,d+1\) makes \(K_d\) adjacency-invariant. Strict growth from
\(d-1\) to \(d\) proves that \(d\) is the first stabilization depth.

Thus both the closure dimension and stabilization depth are exact over

\[
\mathbb Q.
\]

---

## 3. Exact backend

The recommended backend is `python-flint`.

Its integer-matrix rank routine computes the rank of an integer matrix exactly.
Install it in the same Python environment used for the EHF scripts:

```bash
python3 -m pip install python-flint
```

Optional installation check:

```bash
python3 -m flint.test --quiet
```

The script includes a SymPy fallback, but the largest channels may be
substantially slower without FLINT.

---

## 4. Run

From the `OPW3` directory:

```bash
python3 scripts/ehf_xbr_04b_cross_prime_rational_certification.py \
  --run-dirs runs/ehf_xbr_04,runs/ehf_xbr_04_two_prime \
  --expected-primes 65519,65521,1000003 \
  --opw-base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --amp-base-script ../AMP/scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --amp-helper-script ../AMP/scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --amp-rank-script ../AMP/scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --amp-lattice-script ../AMP/scripts/ehf_amp_found_03c_exact_tail_filtration_lattice.py \
  --xbr04-script scripts/ehf_xbr_04_minimal_krylov_closure.py \
  --backend flint \
  --rational-subsets all \
  --out-dir runs/ehf_xbr_04b \
  --strict
```

The script checkpoints `rational_certificate_ledger.csv` after every channel.
Resume an interrupted run by adding:

```bash
--resume
```

---

## 5. Preliminary cross-prime-only run

The ledger comparison does not require FLINT:

```bash
python3 scripts/ehf_xbr_04b_cross_prime_rational_certification.py \
  --run-dirs runs/ehf_xbr_04,runs/ehf_xbr_04_two_prime \
  --expected-primes 65519,65521,1000003 \
  --opw-base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --amp-base-script ../AMP/scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --amp-helper-script ../AMP/scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --amp-rank-script ../AMP/scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --amp-lattice-script ../AMP/scripts/ehf_amp_found_03c_exact_tail_filtration_lattice.py \
  --xbr04-script scripts/ehf_xbr_04_minimal_krylov_closure.py \
  --backend off \
  --out-dir runs/ehf_xbr_04b_cross_prime_only
```

This produces an exact cross-prime identity result but deliberately does not
claim rational certification.

---

## 6. Outputs

- `cross_run_channel_identity.csv`
- `cross_prime_rank_sequence_identity.csv`
- `rational_certificate_ledger.csv`
- `run_summary.json`

### Full verdict

```text
EHF_XBR_04B_CROSS_PRIME_IDENTITY_RATIONAL_CERTIFICATION_PASS
```

### Partial verdict

```text
EHF_XBR_04B_CROSS_PRIME_IDENTITY_PASS_RATIONAL_PARTIAL
```

---

## Interpretation boundary

The rational certificate promotes only the finite structural Krylov closure
law. It does not turn OPW adjacency into a physical Hamiltonian and does not
derive scattering amplitudes or physical time evolution.
