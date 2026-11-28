# EHF-AMP-FOUND-04A
## Eleven-to-Ten Tail-Filtration Discovery Census

**Status:** finite-field discovery probe  
**Reference chart:** anchor 1, delete 11  
**Primary field:** \(\mathbb F_2\)  
**Claim boundary:** discovery only; not an exact \(\mathbb Q\) theorem

---

## 1. Purpose

The completed nine-to-eight programme proved that all anchor and deleted-leg
charts reduce to one six-node target-space lattice. The next nontrivial
odd-to-even transition is

\[
11\to10.
\]

04A asks:

> For a selected four-subset \(A=\{a<b<c<d\}\), does the transmitted local
> KK-relation rank depend only on a bounded ordered tail of \(A\)?

The probe is a scaling census, not an attempted theorem. Its purpose is to
identify the rank classes and the minimum tail width that could support an
exact 04B law.

---

## 2. Canonical diagonal channels

Let

\[
U=\{2,3,\ldots,10\}.
\]

For every \(A\in\binom U4\), define

\[
F_A^{(11)}:
\quad E=\{1,11\}\cup A,
\quad O=U\setminus A,
\]

and

\[
F_A^{(10)}:
\quad E=\{1\}\cup A,
\quad O=U\setminus A.
\]

There are

\[
\binom94=126
\]

diagonal channels. Each target fibre has

\[
\frac{4!5!}{2}=1440
\]
canonical states. Each source channel has \(4!5!=2880\) active delete-11
states, and every target state has exactly two active source preimages.

---

## 3. Source-fibre size

Define

\[
\operatorname{inv}(A)
=
\#\{(a,b):a\in A,\ b\in U\setminus A,\ a>b\}.
\]

Then

\[
\boxed{
|F_A^{(11)}|
=(4!)^2\bigl(5+\operatorname{inv}(A)\bigr)
=576\bigl(5+\operatorname{inv}(A)\bigr).
}
\]

The inactive-column count is \(576\operatorname{inv}(A)\).

---

## 4. Active-column reduction

The 2880 active source columns end in label 11. Their KK expansions are
single distinct endpoint-basis coordinates, so the active block of the exact
source KK matrix is an embedded identity matrix.

After eliminating these active variables, let:

- \(C_A\) be the inactive-column KK coordinates outside the active row set;
- \(L_A\) be the active-coordinate rows composed with the deletion map.

Over any coefficient field,

\[
\boxed{
r_A
=
\operatorname{rank}
\begin{bmatrix}
C_A\\L_A
\end{bmatrix}
-
\operatorname{rank}C_A
=
\operatorname{rank}\left(L_A|_{\ker C_A}\right).
}
\]

04A reduces \(C_A\) while carrying the \(L_A\) image. Whenever a column becomes
dependent in \(C_A\), its carried image is inserted into a second target-space
basis. This computes \(\operatorname{rank}C_A\), \(\dim\ker C_A\), and \(r_A\)
in one paired elimination.

---

## 5. Finite-field strategy

### Complete \(\mathbb F_2\) census

The full 126-channel discovery census uses Python integer bitsets and XOR. The
result is exact over \(\mathbb F_2\).

### Optional \(\mathbb F_3\) audit

A two-plane bitset engine audits one minimum-source-size representative of
each observed \(\mathbb F_2\) rank class. Agreement across the two
characteristics is strong evidence, but it does not prove the rational rank.

---

## 6. Mandatory nine-point self-check

Before running \(11\to10\), the same reduction and \(\mathbb F_2\) engine are
applied to all 35 known \(9\to8\) channels. It must reproduce

\[
0^{\times4},\quad
2^{\times3},\quad
8^{\times3},\quad
9^{\times6},\quad
14^{\times6},\quad
15^{\times13}.
\]

This validates fibre enumeration, active-coordinate elimination, two-preimage
deletion structure, and the bitset rank implementation.

---

## 7. Ordered-tail audit

For \(A=\{a<b<c<d\}\), channels are grouped by the suffixes

\[
(d),\qquad(c,d),\qquad(b,c,d),\qquad(a,b,c,d).
\]

For each width \(w\), 04A asks whether the modular residue rank is constant in
every group sharing the last \(w\) labels. The smallest successful width is
the candidate tail width for an exact follow-up theorem.

The five-gap composition

\[
(g_0,g_1,g_2,g_3,g_4)
=
(a-2,\ b-a-1,\ c-b-1,\ d-c-1,\ 10-d)
\]

is also recorded.

---

## 8. Execution and resume

Sparse pivot orders can produce substantial intermediate fill. Each
11-point channel is therefore run in a fresh spawned process with:

- a configurable timeout;
- deterministic retry order seeds;
- immediate CSV checkpointing;
- optional resume.

This prevents memory accumulation across the 126-channel run.

---

## 9. Run commands

Full discovery census:

```bash
caffeinate -i python3 scripts/ehf_amp_found_04a_eleven_to_ten_tail_filtration_discovery_census.py \
  --out-dir runs/ehf_amp_found_04a \
  --gf3-audit representatives \
  --resume \
  --strict
```

Short smoke test:

```bash
python3 scripts/ehf_amp_found_04a_eleven_to_ten_tail_filtration_discovery_census.py \
  --out-dir runs/ehf_amp_found_04a_smoke \
  --max-channels 6 \
  --gf3-audit none \
  --strict
```

Single-channel audit:

```bash
python3 scripts/ehf_amp_found_04a_eleven_to_ten_tail_filtration_discovery_census.py \
  --out-dir runs/ehf_amp_found_04a_A23410 \
  --subset 2,3,4,10 \
  --gf3-audit all \
  --strict
```

---

## 10. Principal outputs

```text
summary.json
verdict.json
run.log
nine_point_engine_self_check.csv
channel_census_gf2.csv
rank_distribution_gf2.csv
tail_width_audit.csv
tail_signature_table.csv
gf3_representative_audit.csv
```

---

## 11. Verdict semantics

A complete modular census with no bounded-tail collapse receives

```text
EHF_AMP_FOUND_04A_ELEVEN_TO_TEN_MODULAR_DISCOVERY_CENSUS_COMPLETE
```

A complete census with a constant suffix law receives

```text
EHF_AMP_FOUND_04A_ELEVEN_TO_TEN_MODULAR_TAIL_LAW_CANDIDATE_FOUND
```

Neither verdict is an exact rational theorem.

---

## 12. Claim boundary

04A does not establish:

- exact \(\mathbb Q\) ranks at \(11\to10\);
- equality of transported target subspaces at fixed tail signature;
- a higher-point lattice theorem;
- a general odd-to-even law;
- physical or phenomenological significance.

Its main deliverable is the 126-channel modular rank ledger and its
ordered-tail classification.
