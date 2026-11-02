# EHF-AMP-FOUND-04C

## Exact Rational Rank Certificate Sweep

## Purpose

EHF-AMP-FOUND-04B completed the full eleven-to-ten modular census in the canonical anchor-1, delete-11 chart. It established:

- 126/126 channels over GF(2), GF(3), and GF(5);
- exact agreement between GF(3) and GF(5);
- seven characteristic-two defects;
- the boundary-corrected three-tail law over the tested fields;
- complete recovery exactly when the second selected label satisfies \(b\ge 7\);
- 34 exact rational ranks from source/target saturation bounds.

The remaining 92 ranks are strongly constrained but not yet proved over \(\mathbb Q\).

04C performs direct exact sparse rank calculations over \(\mathbb Q\).

---

## Mathematical identity

For every

\[
A=\{a<b<c<d\}\subset\{2,\ldots,10\},
\]

04A constructs integer matrices \(C_A\) and \(L_A\) satisfying, over any field \(K\),

\[
r_A(K)
=
\operatorname{rank}_K
\begin{bmatrix}
C_A\\L_A
\end{bmatrix}
-
\operatorname{rank}_K C_A.
\]

Therefore a completed 04C worker gives the exact rational certificate

\[
\boxed{
r_A(\mathbb Q)
=
\operatorname{rank}_{\mathbb Q}
\begin{bmatrix}
C_A\\L_A
\end{bmatrix}
-
\operatorname{rank}_{\mathbb Q}C_A.
}
\]

No probabilistic reconstruction or floating-point singular-value threshold is used.

---

## Exact engine

The script uses SymPy's sparse `DomainMatrix` representation over \(\mathbb Q\).

Each channel is isolated in a fresh subprocess so that:

- memory is released after every channel;
- hard timeouts are possible;
- a failed channel does not corrupt the ledger;
- the run can resume safely.

Three column orders are available:

```text
natural
nnz_asc
nnz_desc
```

They are mathematically equivalent but can lead to very different sparse-elimination runtimes.

---

## Scopes

### `frontier`

Processes one smallest representative from each unresolved structural class indexed by:

- generic odd-prime rank;
- source-dimension upper bound;
- terminal label;
- boundary-correction flag.

This is the recommended first run. It tests the exact engine across the unresolved landscape without immediately committing to all 92 open channels.

### `unresolved`

Processes every channel not already certified in 04B.

### `all`

Directly recomputes all 126 channels over \(\mathbb Q\), including the 34 already certified by bounds.

### `explicit`

Processes only subsets supplied through `--subsets`, for example:

```text
--scope explicit --subsets '2,3,4,8;2,5,6,10'
```

---

## Self-check

Unless disabled, the script recomputes all 35 nine-to-eight channels exactly over \(\mathbb Q\) and must recover

\[
0^{\times4},\quad
2^{\times3},\quad
8^{\times3},\quad
9^{\times6},\quad
14^{\times6},\quad
15^{\times13}.
\]

This validates the exact sparse construction and rank-difference implementation before the eleven-point sweep.

---

## Principal outputs

```text
exact_qq_channel_ledger.csv
exact_qq_worker_failures.csv
exact_rational_rank_master_ledger.csv
exact_rational_rank_distribution.csv
unresolved_exact_rank_channels.csv
direct_QQ_candidate_mismatches.csv
summary.json
verdict.json
run.log
```

Every row marked `status=exact` is an exact rational result, even if the full sweep is incomplete.

---

## Verdict logic

### Complete theorem

The strongest verdict is issued only when:

1. all 126 channels have exact rational ranks;
2. every direct exact rank agrees with the 04B odd-prime candidate;
3. the boundary-corrected three-tail formula holds over \(\mathbb Q\);
4. complete recovery satisfies
   \[
   r_A(\mathbb Q)=296\iff b\ge7;
   \]
5. all structural checks pass.

Target verdict:

```text
EHF_AMP_FOUND_04C_EXACT_RATIONAL_BOUNDARY_CORRECTED_THREE_TAIL_RANK_THEOREM_PROVED
```

### Partial exact progress

If only part of the sweep completes but all completed workers agree with the modular candidate:

```text
EHF_AMP_FOUND_04C_PARTIAL_EXACT_RATIONAL_CERTIFICATION_ADVANCED
```

### Candidate revision

Any exact rank differing from the GF(3)/GF(5) candidate triggers:

```text
EHF_AMP_FOUND_04C_MODULAR_CANDIDATE_REVISED_BY_EXACT_QQ
```

---

## Recommended run sequence

### 1. Frontier run

```bash
caffeinate -i python3 scripts/ehf_amp_found_04c_exact_rational_rank_certificate_sweep.py \
  --base-script scripts/ehf_amp_found_04a_eleven_to_ten_tail_filtration_discovery_census.py \
  --multi-prime-census runs/ehf_amp_found_04b/multi_prime_channel_census.csv \
  --out-dir runs/ehf_amp_found_04c_frontier \
  --scope frontier \
  --worker-timeout 3600 \
  --column-orders natural,nnz_asc,nnz_desc \
  --resume \
  --strict
```

### 2. Full unresolved sweep

```bash
caffeinate -i python3 scripts/ehf_amp_found_04c_exact_rational_rank_certificate_sweep.py \
  --base-script scripts/ehf_amp_found_04a_eleven_to_ten_tail_filtration_discovery_census.py \
  --multi-prime-census runs/ehf_amp_found_04b/multi_prime_channel_census.csv \
  --out-dir runs/ehf_amp_found_04c \
  --scope unresolved \
  --worker-timeout 7200 \
  --column-orders natural,nnz_asc,nnz_desc \
  --resume \
  --strict
```

The sweep is expected to become expensive for the larger unresolved channels. Timeouts do not invalidate completed rows; they identify where a more structural exact proof or a more advanced sparse exact backend is needed.

---

## Scientific interpretation

04C separates two possible outcomes.

### Outcome A: the modular law exactifies cleanly

Then the eleven-to-ten rank theorem is established over \(\mathbb Q\):

\[
r_{\mathbb Q}(a,b,c,d)
=
\bar r_{\mathbb Q}(b,c,d)
+
\mathbf 1_{\{d=10,\ b\in\{5,6\},\ a\ge4\}}.
\]

This would be the exact rational continuation of the nine-point ordered-tail law.

### Outcome B: direct rational ranks differ

Then the multi-prime census found a stable odd-characteristic pattern that is not the rational theorem. The exact ledger will identify precisely where the revision occurs.

### Outcome C: large channels time out

Then the brute-force exact route has reached its practical limit. The completed exact frontier will still guide a structural proof based on transported subspaces, inclusions, quotient layers, or representation theory.

The probe is therefore useful whether it completes fully or exposes the need for a non-brute-force theorem.
