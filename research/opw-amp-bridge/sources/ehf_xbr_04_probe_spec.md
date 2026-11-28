# EHF-XBR-04
## Minimal Krylov Closure and Delayed Intertwiner

### Purpose

XBR-03 proved that the canonical AMP lift

\[
W_A=\operatorname{row}(V_AD_A)
\]

is not invariant under OPW3 chamber adjacency \(A_A\).

The direct intertwiner therefore fails.

XBR-04 asks whether the smallest adjacency-invariant enlargement remains
compact or expands through most of the chamber.

---

## 1. Minimal closure

For each nonzero AMP channel \(A\), define

\[
\mathcal K_A^{(d)}
=
\operatorname{span}
\left(
W_A,\,
W_AA_A,\,
\ldots,\,
W_AA_A^d
\right).
\]

The minimal invariant closure is

\[
\mathcal K_A
=
\bigcup_{d\ge0}\mathcal K_A^{(d)}.
\]

The stabilization depth is the smallest \(d\) such that

\[
\mathcal K_A^{(d)}
=
\mathcal K_A^{(d+1)}.
\]

Once this occurs,

\[
\mathcal K_AA_A\subseteq\mathcal K_A,
\]

so adjacency restricts to an exact operator on \(\mathcal K_A\).

This restricted operator is the delayed intertwiner.

---

## 2. Multi-prime exact audit

Large sparse rational closure calculations are expensive. The probe computes the entire closure exactly over one or more finite fields.
The default reference field is:

\[
\mathbb F_{1000003}.
\]

Additional primes may be supplied for independent modular replication.

For each field it records:

- initial AMP-lift rank;
- closure dimension;
- stabilization depth;
- full-chamber versus proper closure;
- complete rank-growth sequence.

Agreement across all primes is a strong diagnostic for the corresponding
rational dimensions.

It is not, by itself, an exact proof over \(\mathbb Q\). The output preserves
this distinction explicitly.

---

## 3. Questions answered

The probe determines:

1. Does the AMP lift generate the whole OPW chamber?
2. When it does not, how large is the proper invariant closure?
3. How many adjacency powers are needed before stabilization?
4. Does the minimal delayed intertwiner remain compact?
5. Are the closure dimensions stable across unrelated large primes?

---

## 4. Interpretation categories

- **FULL-CHAMBER CLOSURE:** the canonical AMP lift is cyclic for the complete
  OPW chamber over the audited field.
- **PROPER INVARIANT CLOSURE:** the bridge selects a nontrivial invariant
  module smaller than the chamber.
- **COMPACT CLOSURE:** a proper closure occupying only a small fraction of the
  chamber.
- **EXPANSIVE CLOSURE:** the minimal invariant module occupies most of the
  chamber.
- **PRIME-SENSITIVE:** different fields give different dimensions or depths;
  rational interpretation must be deferred.

No physical Hamiltonian or time evolution is asserted.

---

## Run

From the `OPW3` directory:

```bash
python3 scripts/ehf_xbr_04_minimal_krylov_closure.py \
  --opw-base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --amp-base-script ../AMP/scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --amp-helper-script ../AMP/scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --amp-rank-script ../AMP/scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --amp-lattice-script ../AMP/scripts/ehf_amp_found_03c_exact_tail_filtration_lattice.py \
  --xbr03-run-dir runs/ehf_xbr_03 \
  --primes 1000003 \
  --max-depth 600 \
  --out-dir runs/ehf_xbr_04 \
  --strict
```

### Outputs

- `krylov_channel_ledger.csv`
- `krylov_prime_ledger.csv`
- `krylov_class_summary.csv`
- `run_summary.json`

### Verdict

```text
EHF_XBR_04_FINITE_FIELD_KRYLOV_CLOSURE_DELAYED_INTERTWINER_PASS
```


### Optional multi-prime replication

After the reference run, repeat with:

```bash
python3 scripts/ehf_xbr_04_minimal_krylov_closure.py \
  --opw-base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --amp-base-script ../AMP/scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --amp-helper-script ../AMP/scripts/ehf_amp_found_02a_growth_factorisation_compatibility_v0_3.py \
  --amp-rank-script ../AMP/scripts/ehf_amp_found_03b_exact_two_rightmost_rank_law.py \
  --amp-lattice-script ../AMP/scripts/ehf_amp_found_03c_exact_tail_filtration_lattice.py \
  --xbr03-run-dir runs/ehf_xbr_03 \
  --primes 65519,65521 \
  --max-depth 600 \
  --out-dir runs/ehf_xbr_04_two_prime \
  --strict
```

The one-prime run is exact over the stated finite field. Multi-prime agreement
strengthens, but does not prove, the corresponding \(\mathbb Q\)-rank claim.
