# EHF-AMP-FOUND-03D  
## Exact Quotient Generators and Orbit Compression

**Status:** exact proof-compression probe  
**Input:** the exact target-space lattice from 03C  
**Symmetry:** \(G\cong C_2^3\)

---

## 1. Purpose

03C explains the six transmitted ranks as dimensions of exact target
subspaces:

\[
V_0,\ V_2,\ V_8,\ V_9,\ V_{14},\ V_{15}.
\]

The lattice is

\[
V_2\subset V_8,V_9,
\qquad
V_3=V_8\cap V_9,
\qquad
V_{14}=V_8+V_9,
\qquad
V_{15}=R^{(8)}.
\]

This is structurally explanatory, but it still describes the spaces through
machine-generated RREF bases.

03D asks for a smaller human-facing description:

> How many explicit relation seeds are required to generate the complete
> lattice under its common \(C_2^3\) symmetry?

---

## 2. Successive quotient layers

The independent increments are

\[
L_2=V_2/V_0,
\]

\[
L_3=V_3/V_2,
\]

\[
L_8=V_8/V_3,
\]

\[
L_9=V_9/V_3,
\]

and

\[
L_{15}=V_{15}/V_{14}.
\]

Their dimensions are

\[
2,\quad1,\quad5,\quad6,\quad1,
\]

which sum to

\[
15.
\]

The identity

\[
V_{14}=V_8+V_9
\]

means there is no additional quotient generator at dimension \(14\).

---

## 3. Common symmetry

The exact common symmetry is

\[
G=
\langle
g_1=(2\,3),\
g_2=(5\,6),\
g_3=(7\,8)
\rangle
\cong C_2^3.
\]

Every irreducible representation of \(C_2^3\) over \(\mathbb Q\) is a
one-dimensional sign character

\[
\chi=(\chi_1,\chi_2,\chi_3),
\qquad
\chi_i\in\{+1,-1\}.
\]

For a quotient layer \(L\), write

\[
L=\bigoplus_\chi \mathbb Q^{m_\chi}\otimes\chi.
\]

---

## 4. Minimal cyclic-generator theorem

### Proposition

The minimum number of vectors whose \(G\)-orbits span \(L\) is

\[
\boxed{
\max_\chi m_\chi.
}
\]

### Reason

The group algebra of \(C_2^3\) acts by a scalar on each copy of a fixed
character. The orbit span of one seed contributes at most one independent
vector inside each multiplicity space. Therefore at least \(m_\chi\) seeds
are needed for a character occurring \(m_\chi\) times.

Conversely, choosing \(\max_\chi m_\chi\) generic seeds supplies a basis in
each character multiplicity space, so the bound is attained.

Because all characters are rational, no field extension is required.

---

## 5. Expected layer decompositions

The exact character tables from 03C imply:

### \(L_2=V_2\)

\[
L_2=(+-+)\oplus(---).
\]

Every character occurs once, so one cyclic seed is sufficient.

### \(L_3=V_3/V_2\)

\[
L_3=(+--).
\]

One seed is necessary and sufficient.

### \(L_8=V_8/V_3\)

\[
L_8=(-++)\oplus(-+-)\oplus2(--+)\oplus(---).
\]

The maximum multiplicity is \(2\), so precisely two seeds are required.

### \(L_9=V_9/V_3\)

\[
L_9=(++-)\oplus2(+--)\oplus(-+-)\oplus(--+)\oplus(---).
\]

Again, precisely two seeds are required.

### \(L_{15}=V_{15}/V_{14}\)

\[
L_{15}=(-+-).
\]

One seed is required.

The predicted total is therefore

\[
\boxed{
1+1+2+2+1=7.
}
\]

---

## 6. Exact sparse-seed construction

The script loads

```text
runs/ehf_amp_found_03c/exact_subspace_rref_bases.json
```

and performs the following exact operations:

1. construct an exact complement for each quotient \(V/W\);
2. clear denominators and primitive-normalise the rows;
3. apply LLL to obtain a lower-norm integer basis;
4. generate deterministic ternary combinations of that basis;
5. compute every candidate’s exact \(C_2^3\)-orbit span modulo \(W\);
6. select the minimum number of seeds allowed by the character theorem;
7. verify that their combined orbit span is the full quotient.

Each selected relation is written explicitly as

\[
\sum_{d\in F_{\{2,3,4\}}^{(8)}}
c_d\,\operatorname{PT}(d)=0,
\qquad c_d\in\mathbb Z.
\]

The output records:

- support size;
- coefficient alphabet;
- \(L_1\) norm;
- individual orbit rank;
- joint orbit reconstruction rank.

---

## 7. The theorem targeted by 03D

A successful run proves:

> The fifteen-dimensional target relation module is generated
> layer-by-layer by seven primitive relation seeds under the common
> \(C_2^3\) action. The layers \(L_2,L_3,L_{15}\) are cyclic. The layers
> \(L_8,L_9\) require exactly two seeds because one joint character occurs
> with multiplicity two.

This explains the only noncyclic parts of the lattice.

---

## 8. Practical significance

03D produces a compact constructive basis:

- seven seed identities rather than a \(15\times72\) RREF table;
- exact orbit rules generating all target directions;
- a representation-theoretic proof that fewer seeds are impossible.

This is closer to something an amplitude theorist could inspect or implement
than the raw subspace matrices.

It still does not prove that the seed identities belong to a known closed
family of shuffle relations. That is the next compression problem.

---

## 9. Claim boundary

03D proves a finite minimal orbit-generator theorem for the exact \(n=9\)
tail-filtration lattice. It does not yet:

- derive the seeds from a closed analytic KK formula;
- prove anchor covariance;
- generalise to \(11\to10\);
- demonstrate a computational speed-up in a standard amplitude package;
- establish physical meaning.

---

## 10. Run command

```bash
caffeinate -i python3 scripts/ehf_amp_found_03d_exact_quotient_orbit_generators.py \
  --base-script scripts/ehf_amp_found_01_reproduce_amp18_20.py \
  --subspace-bases-json runs/ehf_amp_found_03c/exact_subspace_rref_bases.json \
  --out-dir runs/ehf_amp_found_03d \
  --strict
```

No numerical relation cache is required.

---

## 11. Principal outputs

```text
summary.json
verdict.json
run.log
exact_orbit_generator_certificate.json
quotient_layer_summary.csv
quotient_character_multiplicities.csv
orbit_seed_summary.csv
sparse_seed_coefficients.csv
sparse_orbit_seed_relations.md
```

The target terminal result is:

```text
Exact quotient dimensions:            True
Character-theoretic seed minima:      True
All quotient layers reconstructed:    True
Total primitive orbit seeds:          7
Expected total:                       7
Verdict: EHF_AMP_FOUND_03D_EXACT_SEVEN_SEED_ORBIT_COMPRESSION_PROVED
strict checks:                        PASS
```
