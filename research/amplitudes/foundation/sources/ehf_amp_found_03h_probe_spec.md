# EHF-AMP-FOUND-03H
## Group-Ring Factor Types and Residual-Normalizer Audit

**Status:** exact structural classification probe  
**Input:** the 21 primitive group-ring templates from 03G  
**Symmetry:** target-fibre stabilizer and the residual normalizer of \(C_2^3\)

---

## 1. Purpose

03G proved that the complete \(720\)-coordinate eight-point KK proof factors as

\[
720\longrightarrow144\longrightarrow21,
\]

where the final objects are primitive rows over

\[
\mathbb Z[C_2^3]
\cong
\mathbb Z[x_1,x_2,x_3]/(x_1^2-1,x_2^2-1,x_3^2-1).
\]

03H asks:

1. whether the individual orbit polynomials have a uniform exact factor form;
2. how many coarse factor types occur among the 21 templates;
3. whether the residual normalizer of the common \(C_2^3\) symmetry reduces the template catalogue further.

The third question is an audit, not an assumed positive result.

---

## 2. Affine-subgroup factor theorem

For a nonzero orbit polynomial

\[
p(x)=\sum_{h\in C_2^3}c_hx^h,
\]

03H tests whether its support is an affine coset

\[
a+H\subset\mathbb F_2^3
\]

of a subgroup \(H\leq\mathbb F_2^3\), with constant nonzero coefficient \(\epsilon\). The target factorisation is

\[
\boxed{
p(x)=\epsilon x^a\sum_{h\in H}x^h.
}
\]

If \(B\) is an \(\mathbb F_2\)-basis of \(H\), then

\[
\boxed{
p(x)=\epsilon x^a\prod_{v\in B}(1+x^v).
}
\]

The script reconstructs every polynomial exactly from \(\epsilon\), \(a\), and \(B\).

---

## 3. Exact character activation formula

For a sign character \(\chi\), affine-subgroup factorisation implies

\[
p(\chi)=0
\]

unless \(\chi\) is trivial on \(H\). If \(\chi|_H=1\), then

\[
\boxed{
p(\chi)=\epsilon\,\chi(a)\,|H|.
}
\]

Therefore a rank-\(d\) factor block is active on exactly

\[
2^{3-d}
\]

characters.

03H checks this prediction for every nonzero block and all eight sign characters.

---

## 4. Expected factor census

The 21 templates contain exactly 54 nonzero orbit-polynomial blocks.

The expected factor-rank distribution is

\[
\boxed{
0^{\times29},\qquad
1^{\times19},\qquad
2^{\times5},\qquad
3^{\times1}.
}
\]

Here rank means \(\dim_{\mathbb F_2}H\).

The sorted block-rank multisets classify the 21 templates into seven coarse profiles:

\[
\begin{array}{c|c|c}
\text{profile} & \text{sorted block ranks} & \text{template count}\\
\hline
F_1&(3)&1\\
F_2&(2)&3\\
F_3&(1,2)&2\\
F_4&(1,1)&6\\
F_5&(0,0,1)&2\\
F_6&(0,0,0,1)&3\\
F_7&(0,0,0,0)&4
\end{array}
\]

This is a coarse factor classification. It does not identify templates that differ by orbit incidence or coset offsets.

---

## 5. Residual normalizer

The reference target fibre is preserved by

\[
S_{\{2,3,4\}}\times S_{\{5,6,7,8\}}
\cong S_3\times S_4,
\]

of order \(144\).

Let

\[
G=\langle(2\,3),(5\,6),(7\,8)\rangle\cong C_2^3.
\]

03H enumerates the exact normalizer

\[
N=N_{S_3\times S_4}(G).
\]

The expected result is

\[
|N|=16,
\qquad
N/G\cong C_2.
\]

A nontrivial residual representative is

\[
\tau=(5\,7)(6\,8),
\]

which acts on the group-ring variables by

\[
x_1\mapsto x_1,
\qquad
x_2\leftrightarrow x_3.
\]

Its exact action on the ten target-state orbits is

\[
(O_1\ O_7)(O_3\ O_8)(O_4\ O_9)(O_6\ O_{10}),
\]

with \(O_2,O_5\) fixed.

---

## 6. Fixed-KK-chart closure test

The 21 templates were defined using the standard KK chart with label \(8\) fixed at the right endpoint. The target-fibre normalizer need not preserve that coordinate chart.

For each template \(T\), 03H:

1. applies \(\tau\) to its exact coefficient function on the 72 target states;
2. re-expresses the result in the ten orbit blocks;
3. primitive-normalises it modulo a global group monomial;
4. tests whether the resulting class belongs to the original 21-template catalogue.

The expected audit result is:

\[
\boxed{
8\text{ templates remain inside},
\qquad
13\text{ leave the catalogue}.
}
\]

The internal action is

\[
T_{02}\leftrightarrow T_{17},
\qquad
T_{04}\leftrightarrow T_{18},
\qquad
T_{12}\leftrightarrow T_{13},
\]

with

\[
T_{15},T_{16}
\]

fixed.

Adding the 13 new residual images gives a normalizer-closed catalogue of

\[
\boxed{34}
\]

classes, arranged into

\[
\boxed{18}
\]

residual orbits: two fixed classes and sixteen two-cycles.

Thus the residual symmetry does not reduce the fixed-chart list. It exposes a coordinate-chart obstruction.

---

## 7. Scientific interpretation

03H separates two effects.

### Intrinsic group-ring structure

Every nonzero polynomial is a monomial times a product of simple character-annihilator factors

\[
1+x^v.
\]

This explains exactly which characters survive or vanish.

### Coordinate-chart obstruction

The residual target-fibre normalizer is not a symmetry of the standard KK coordinate chart used in 03G. Closing under that symmetry enlarges the catalogue instead of compressing it.

This is a useful negative result. It prevents an incorrect claim that the 21 templates collapse under the full target-fibre normalizer.

---

## 8. Claim boundary

A successful 03H run proves:

> Every nonzero orbit polynomial in the 21-template catalogue is an affine-subgroup sum in \(\mathbb Z[C_2^3]\), and the residual normalizer \(N/G\cong C_2\) is obstructed by the fixed standard KK chart: only 8 templates close internally, while normalizer closure contains 34 classes.

It does not yet:

- derive the observed 03G multiplicities \(4,8,16\) from an orbit-stabilizer theorem;
- construct an anchor-covariant KK template system;
- replace the 21 templates by one general combinatorial formula;
- generalise to higher multiplicity;
- establish phenomenological utility.

---

## 9. Run command

```bash
caffeinate -i python3 scripts/ehf_amp_found_03h_group_ring_factor_normalizer_audit.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --template-catalog runs/ehf_amp_found_03g/universal_shuffle_template_catalog.csv \
  --template-polynomials runs/ehf_amp_found_03g/universal_shuffle_template_polynomials.csv \
  --out-dir runs/ehf_amp_found_03h \
  --strict
```

---

## 10. Principal outputs

```text
summary.json
verdict.json
run.log
exact_factor_normalizer_certificate.json
orbit_polynomial_factorization.csv
character_activation_audit.csv
factor_profile_census.csv
template_factor_profiles.csv
factor_direction_census.csv
residual_normalizer_elements.csv
residual_target_orbit_permutation.csv
residual_template_action.csv
residual_normalizer_closure_catalog.csv
exact_factor_normalizer_audit.md
```

The target terminal result is:

```text
Affine-subgroup factor census
  nonzero orbit-polynomial blocks:    54
  factor-rank distribution:           {0: 29, 1: 19, 2: 5, 3: 1}
  coarse factor-rank profiles:        7
  character activation formula:       True

Residual-normalizer audit
  target-fibre stabilizer order:       144
  normalizer order:                    16
  quotient N/G order:                  2
  templates staying in catalogue:     8
  templates leaving catalogue:        13
  normalizer closure size:             34
  residual closure orbits:             18

FINAL SUMMARY
All affine-subgroup factors exact:    True
Seven factor profiles exact:          True
Residual normalizer obstruction:      True
Verdict: EHF_AMP_FOUND_03H_AFFINE_SUBGROUP_FACTOR_THEOREM_AND_RESIDUAL_NORMALIZER_OBSTRUCTION_PROVED
strict checks:                        PASS
```
