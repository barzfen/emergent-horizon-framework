# EHF-AMP-FOUND-04B  
## Full Multi-Prime Boundary-Corrected Three-Tail Audit

**Status:** multi-prime discovery and partial exact-rank certification  
**Input:** completed 04A GF(2) channel census  
**Primary new fields:** \(\mathbb F_3\) and \(\mathbb F_5\)  
**Chart:** canonical anchor \(1\), delete \(11\)

---

## 1. Purpose

04A completed all

\[
\binom94=126
\]

eleven-to-ten diagonal channels, but its automatic verdict overstated the
result. A four-label suffix is the complete subset

\[
A=\{a<b<c<d\},
\]

so `minimal_constant_tail_width = 4` is tautological. No nontrivial pure tail
law was found at widths one, two, or three.

The actual GF(2) result was more specific:

1. a three-rightmost-label near-law;
2. exactly seven nonconstant suffix classes;
3. every split was one-dimensional;
4. every split occurred at the terminal boundary \(d=10\);
5. the correction switched on when \(a\ge4\);
6. representative GF(3) calculations revealed systematic characteristic-two
   defects
   \[
   35\to36,\qquad59\to60.
   \]

04B performs the full odd-prime audit needed before treating the pattern as a
credible scaling candidate.

---

## 2. Full channel system

For

\[
A=\{a<b<c<d\}\subset\{2,\ldots,10\},
\]

the source and target fibres are

\[
F_A^{(11)}:
E=\{1,11\}\cup A,
\qquad
O=\{2,\ldots,10\}\setminus A,
\]

and

\[
F_A^{(10)}:
E=\{1\}\cup A,
\qquad
O=\{2,\ldots,10\}\setminus A.
\]

Each target fibre has \(1440\) states. Every channel has \(2880\) active
source columns and two active source preimages per target state.

The reduced rank identity is

\[
r_A^{(p)}
=
\operatorname{rank}_{\mathbb F_p}
\begin{bmatrix}C_A\\L_A\end{bmatrix}
-
\operatorname{rank}_{\mathbb F_p}C_A.
\]

04B computes this for all \(126\) channels over both \(\mathbb F_3\) and
\(\mathbb F_5\).

---

## 3. Odd-prime bit-sliced engine

The GF(2) and GF(3) engines in 04A used specialised bit operations. 04B adds a
generic one-hot bit-sliced eliminator for small odd primes.

For GF(5), a vector is stored as four Python integers: one bit plane for each
nonzero residue. Vector addition and scalar multiplication operate on entire
coordinate sets through bitwise Boolean operations.

The eliminator reduces the outside-coordinate column \(C_A\) while carrying
the residue image \(L_A\). Whenever an outside column becomes dependent, its
carried image contributes to the transmitted-image rank.

The same engine is applied to the complete target KK matrix to determine the
target relation dimension over each field.

---

## 4. Mandatory validation

Before the eleven-point audit, 04B must reproduce all 35 known nine-to-eight
ranks over both odd primes:

\[
0^{\times4},
\quad
2^{\times3},
\quad
8^{\times3},
\quad
9^{\times6},
\quad
14^{\times6},
\quad
15^{\times13}.
\]

A smoke validation of the completed script recovered all 35 ranks over both
GF(3) and GF(5), and found

\[
\dim R^{(10)}=296
\]

over GF(2), GF(3), and GF(5).

---

## 5. Boundary-corrected three-tail candidate

For a fixed suffix \((b,c,d)\), let

\[
\bar r_p(b,c,d)
=
\min_a r_p(a,b,c,d).
\]

04B tests the fixed formula

\[
\boxed{
 r_p(a,b,c,d)
 =
 \bar r_p(b,c,d)
 +
 \mathbf 1_{\{d=10,\ b\in\{5,6\},\ a\ge4\}}.
}
\]

The expected seven nonconstant suffixes are

\[
(5,6,10),
(5,7,10),
(5,8,10),
(5,9,10),
\]

\[
(6,7,10),
(6,8,10),
(6,9,10).
\]

This is not a pure three-tail law: the smallest label re-enters through one
binary boundary correction. The ansatz is nontrivial because both the location
and form of that correction are fixed before the odd-prime census.

Width four is excluded from the verdict logic.

---

## 6. Cross-field audit

For every channel, 04B records

\[
r_2(A),\qquad r_3(A),\qquad r_5(A).
\]

The key tests are:

1. whether GF(3) and GF(5) agree in all 126 channels;
2. which channels exhibit characteristic-two defects;
3. whether the seven boundary splits survive both odd primes;
4. whether componentwise monotonicity survives;
5. whether complete target recovery remains equivalent to
   \[
   b\ge7.
   \]

Agreement of two odd primes is strong evidence for the generic modular rank,
but is not by itself a proof of the rational rank.

---

## 7. Rational lower and upper bounds

For an integer matrix,

\[
\operatorname{rank}_{\mathbb Q}M
\ge
\operatorname{rank}_{\mathbb F_p}M.
\]

Consequently, modular relation dimensions are rational upper bounds.
For every channel 04B computes

\[
\boxed{
L_A
=
\max_{p\in\{2,3,5\}}r_p(A)
}
\]

and

\[
\boxed{
U_A
=
\min\left(
U_{\mathrm{target}},
\min_{p\in\{2,3,5\}}
\dim_{\mathbb F_p}R_A^{(11)}
\right).
}
\]

If

\[
L_A=U_A,
\]

then the rational transmitted rank is exactly certified:

\[
\operatorname{rank}_{\mathbb Q}I_A=L_A.
\]

This certifies, in particular:

- target-saturating channels;
- source-limited channels;
- any additional channels whose independent source and target bounds meet.

The output clearly separates exact rational ranks from unresolved modular
lower bounds.

---

## 8. Verdict logic

The positive full-run verdict requires:

1. all 126 GF(3) channels complete;
2. all 126 GF(5) channels complete;
3. all structural checks pass;
4. GF(3) and GF(5) agree channel by channel;
5. no pure suffix law exists at widths \(1,2,3\);
6. exactly the seven predicted three-tail classes are nonconstant;
7. the fixed one-dimensional boundary formula holds;
8. complete recovery is equivalent to \(b\ge7\).

The target verdict is

```text
EHF_AMP_FOUND_04B_MULTI_PRIME_BOUNDARY_CORRECTED_THREE_TAIL_CANDIDATE_SUPPORTED
```

This remains a discovery statement unless all 126 rational bounds collapse.

---

## 9. Run command

```bash
caffeinate -i python3 scripts/ehf_amp_found_04b_full_multi_prime_boundary_corrected_tail_audit.py \
  --base-script scripts/ehf_amp_found_04a_eleven_to_ten_tail_filtration_discovery_census.py \
  --gf2-census runs/ehf_amp_found_04a/channel_census_gf2.csv \
  --out-dir runs/ehf_amp_found_04b \
  --fields 3,5 \
  --resume \
  --strict
```

The run is checkpointed after every channel and can safely be resumed.

---

## 10. Principal outputs

```text
summary.json
verdict.json
run.log
nine_point_multi_prime_self_check.csv
target_relation_dimension_by_field.csv
channel_census_gf3.csv
channel_census_gf5.csv
multi_prime_channel_census.csv
field_disagreement_audit.csv
tail_width_audit_multi_prime.csv
boundary_corrected_three_tail_audit.csv
componentwise_monotonicity_violations.csv
complete_recovery_channels.csv
exact_rank_certification_summary.csv
```

The decisive fields in `summary.json` are:

```text
GF3_GF5_all_channels_agree
characteristic_two_defect_count
pure_tail_width_less_than_four_found
boundary_corrected_three_tail_formula_exact
complete_recovery_criterion_b_ge_7
exact_rational_rank_certified_channel_count
all_126_rational_ranks_exact_certified
```

---

## 11. Claim boundary

A successful 04B run supports a generic-prime boundary-corrected three-tail
candidate and may certify a substantial subset of exact rational ranks. It
does not automatically prove:

- all 126 rational ranks;
- a closed formula for the base function \(\bar r(b,c,d)\);
- equality of the transmitted subspaces rather than only their dimensions;
- the analogous pattern at \(13\to12\);
- phenomenological significance.

The next exact step should be chosen only after inspecting how many rational
bounds collapse and whether the odd-prime pattern is completely stable.
