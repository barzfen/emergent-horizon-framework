# EHF-AMP-FOUND-04C-T0
## Odd-Prime Exceptional-Prime and 2-Primary Torsion Precursor Audit

**Status:** Parallel server probe while the direct exact-QQ 04C frontier runs.

## 1. Purpose

The completed 04B census found, for all 126 canonical eleven-to-ten channels,

- exact agreement over GF(3) and GF(5);
- seven one-dimensional rank defects over GF(2);
- a boundary-corrected three-tail law over the two odd fields;
- 34 channels already certified exactly over the rationals by matching lower and upper bounds.

04C-T0 asks whether any additional tested odd prime is exceptional.

For each channel

\[
A=\{a<b<c<d\}\subset\{2,\ldots,10\},
\]

and each requested odd prime \(p\), compute

\[
r_p(A)=\operatorname{rank}_{\mathbb F_p}
\begin{bmatrix}C_A\\L_A\end{bmatrix}
-
\operatorname{rank}_{\mathbb F_p}C_A.
\]

The target comparison is the common GF(3)/GF(5) rank recorded by 04B.

## 2. Scientific hypothesis

### Finite exceptional-prime hypothesis

For the tested channels and odd primes,

\[
r_p(A)=r_3(A)=r_5(A).
\]

### Stronger integral conjecture motivating the probe

All failures of base-change stability in the eleven-to-ten transmitted relation modules are 2-primary. Equivalently, every odd prime should see the rational rank:

\[
r_p(A)=r_{\mathbb Q}(A)
\qquad(p\text{ odd}).
\]

04C-T0 cannot prove the stronger conjecture. Agreement for finitely many primes is evidence only. A proof requires integral kernel, saturation, Smith-normal-form, or determinantal-divisor control.

## 3. Important distinction

Two different seven-element phenomena must not be conflated.

1. **Characteristic-two defect channels:** seven individual channels where GF(2) lies one below GF(3)/GF(5), concentrated at \(d=8\).
2. **Boundary-correction tail classes:** seven nonconstant three-tail classes at \(d=10\), where changing the smallest selected label activates one extra dimension.

The first is an arithmetic/base-change phenomenon. The second is part of the rational tail geometry.

## 4. Scopes

### `defects`

Runs exactly the seven characteristic-two defect channels.

### `frontier`

Runs the union of:

- all characteristic-two defect channels;
- one least-complex representative of every generic odd-prime rank class;
- every member of each nonconstant three-tail class.

This is the recommended first server run.

### `all`

Runs all 126 channels.

### `explicit`

Runs a semicolon-separated user-supplied subset list.

## 5. Arithmetic engine

The script uses exact one-hot bit-sliced Gaussian elimination over GF(\(p\)). Each nonzero residue occupies one Python-integer bit plane. It supports odd primes up to 31, but cost increases substantially with \(p\), approximately quadratically in the number of residue planes during elimination.

Each channel/field calculation runs in an isolated subprocess with:

- timeout protection;
- order-seed retries;
- immediate checkpointing;
- resume support;
- memory release after each worker.

## 6. Recommended server command

```bash
caffeinate -i python3 scripts/ehf_amp_found_04c_t0_odd_prime_exceptional_prime_audit.py \
  --base-script scripts/ehf_amp_found_04a_eleven_to_ten_tail_filtration_discovery_census.py \
  --multi-prime-census runs/ehf_amp_found_04b/multi_prime_channel_census.csv \
  --out-dir runs/ehf_amp_found_04c_t0_frontier \
  --fields 7,11,13 \
  --scope frontier \
  --worker-timeout 7200 \
  --order-seeds 1,2 \
  --resume \
  --require-candidate-agreement \
  --strict
```

If the server is Linux rather than macOS, omit `caffeinate -i`.

A faster first pass is:

```bash
python3 scripts/ehf_amp_found_04c_t0_odd_prime_exceptional_prime_audit.py \
  --base-script scripts/ehf_amp_found_04a_eleven_to_ten_tail_filtration_discovery_census.py \
  --multi-prime-census runs/ehf_amp_found_04b/multi_prime_channel_census.csv \
  --out-dir runs/ehf_amp_found_04c_t0_defects \
  --fields 7,11,13 \
  --scope defects \
  --worker-timeout 7200 \
  --order-seeds 1,2 \
  --resume \
  --require-candidate-agreement \
  --strict
```

## 7. Principal outputs

```text
run.log
channel_census_gf7.csv
channel_census_gf11.csv
channel_census_gf13.csv
multi_odd_prime_audit.csv
exceptional_prime_ledger.csv
rank_distribution_by_field.csv
worker_failures.csv
summary.json
verdict.json
```

## 8. Verdicts

### Supported finite-prime result

```text
EHF_AMP_FOUND_04C_T0_NO_ADDITIONAL_ODD_PRIME_EXCEPTION_FOUND
```

Meaning: every requested channel completed, all newly tested odd primes agreed with one another, and all matched the common GF(3)/GF(5) rank.

### Falsifying result

```text
EHF_AMP_FOUND_04C_T0_ADDITIONAL_ODD_PRIME_EXCEPTION_DETECTED
```

Meaning: at least one tested odd prime disagreed with the GF(3)/GF(5) candidate or with another tested odd prime.

### Incomplete result

```text
EHF_AMP_FOUND_04C_T0_ODD_PRIME_AUDIT_INCOMPLETE
```

## 9. Claim boundary

A complete pass supports the statement:

> No additional exceptional odd prime was found in the audited finite set of fields and channels.

It does **not** prove:

> The integral transmitted-image modules have only 2-primary torsion.

The latter remains an exact algebraic theorem target.
