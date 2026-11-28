# EHF-XBR-05A–05C Result Note

## Exact Obstruction to Conventional Null-Channel Holonomy at \(n=9\)

**Programme:** Emergent Horizon Framework  
**Branch:** OPW3–AMP cross-branch reconstruction  
**Date:** 1 August 2026  
**Status:** Exact finite negative classification; conventional exact-primitive null-channel holonomy route closed at the audited \(n=9\) scale

---

## 1. Purpose

EHF-XBR-04F8B completed the rational representation-theoretic decomposition of the 216-dimensional aggregate kernel carried by the 11 singular proper OPW3–AMP channels. This made it possible to ask a new structural question without unresolved multiplicity or basis ambiguity:

> Do the null-channel kernels support a mathematically valid holonomy audit?

The XBR-05 sequence answers the prerequisite question before attempting any loop-matrix calculation. It distinguishes three logically separate objects:

1. a loop-rich base graph;
2. a constant-rank fiber family on that graph;
3. certified reversible, gauge-covariant transport maps between adjacent fibers.

Holonomy requires all three. A closed path in the base alone is insufficient, and independently chosen nullspace bases cannot supply the missing transport.

The word “null” is used narrowly throughout: these are kernels of the finite chamber adjacency actions audited in the XBR-04F programme. It does not mean physically invisible, dynamically irrelevant, or unobservable.

---

## 2. Mathematical definition lock

The base vertices are the 11 singular proper channels

\[
A\subset\{2,\ldots,8\},
\qquad |A|=3,
\]

with Johnson adjacency

\[
A\sim B
\quad\Longleftrightarrow\quad
|A\cap B|=2.
\]

The whole candidate fiber over \(A\) is

\[
K_A=\ker \mathcal A_A.
\]

For ordinary orthogonal or unitary holonomy, an edge comparison must be an isomorphism

\[
T_{B\leftarrow A}:K_A\longrightarrow K_B.
\]

Therefore equal fiber dimension is necessary on every transported edge:

\[
\dim K_A=\dim K_B.
\]

If the dimensions differ, projector overlap followed by polar decomposition produces at most a partial isometry. The immediate backtrack generally satisfies

\[
T_{A\leftarrow B}T_{B\leftarrow A}
=P
\ne I_{K_A},
\]

so the construction is singular transport, not a reversible connection. XBR-05A–05C consequently compute no loop matrix unless the required bundle and transport gates are certified first.

---

## 3. EHF-XBR-05A: whole-kernel definition lock

### 3.1 Exact census

XBR-05A reconstructs the induced Johnson graph on the 11 nonzero null channels and completely enumerates its minimal loops.

| Quantity | Exact result |
|---|---:|
| Source null channels | 11 |
| Induced Johnson edges | 29 |
| Connected components | 1 |
| Shortest loop length | 3 |
| Minimal triangles | 24 |
| Equal-dimension edges | 0 |
| Unequal-dimension edges | 29 |
| Holonomy matrices computed | 0 |
| Strict checks | 13/13 |

The base graph is therefore connected and loop-rich, but every admissible edge changes the whole-kernel dimension.

### 3.2 05A conclusion

The family \(\{K_A\}\) is not a constant-rank vector bundle on the candidate Johnson base. Ordinary reversible whole-kernel holonomy is undefined.

This is not a statement that the whole-kernel holonomy is trivial. No qualifying whole-kernel connection exists whose loop action could be tested for triviality.

---

## 4. EHF-XBR-05B: primitive persistence on minimal triangles

XBR-05B asks whether the rank-changing whole kernels contain a smaller representation-theoretically certified subbundle on any of the 24 triangles.

It reconstructs the final XBR-04F8/F8B primitive census by replacing the two residual F8 blocks with their certified F8B children. An exact primitive type includes both:

- the literal acting-group identity;
- the exact primitive character.

For a triangle \(A_0\sim A_1\sim A_2\sim A_0\), a candidate is recorded only if the same exact primitive type \(\tau\) occurs at all three vertices with the same multiplicity \(m_\tau\). The candidate rank would then be

\[
r_\tau=d_\tau m_\tau.
\]

Constant multiplicity is essential: selecting one copy from a larger multiplicity space would require a noncanonical choice.

### 4.1 Exact census

| Quantity | Exact result |
|---|---:|
| Final certified primitive instances | 140 |
| Minimal triangles audited | 24 |
| Exact persistence candidates | 0 |
| Triangles with exact persistence | 0 |
| Coarse-only triangle candidates | 1 |
| Transport-admissible subbundles | 0 |
| Transport-admissible triangles | 0 |
| Holonomy matrices computed | 0 |
| Strict checks | 20/20 |

Scientific outcome:

```text
coarse_triangle_recurrence_only_no_exact_subbundle
```

### 4.2 Exact versus coarse recurrence

The single apparent triangle recurrence survives only under a coarse fingerprint built from dimensions, group order, and order/trace data. Its vertices do not share one certified exact primitive type.

It is therefore retained only as a control. Matching coarse signatures across different literal acting groups are not module-isomorphism certificates and cannot define a common fiber.

### 4.3 05B conclusion

No certified exact primitive/fixed-multiplicity null subbundle persists around any minimal triangle. The whole-kernel obstruction cannot be repaired on the shortest loops by selecting a primitive representation sector.

---

## 5. EHF-XBR-05C: complete longer-loop closure test

XBR-05C tests the remaining conventional-holonomy possibility: an exact primitive type might recur around a square or longer cycle even though it does not persist around a triangle.

For every exact primitive type \(\tau\) and each multiplicity \(m\) actually present, it constructs the induced support graph

\[
G_{\tau,m}
=
G\big[\{A:\operatorname{mult}_{K_A}(\tau)=m\}\big].
\]

Each support slice has fixed candidate rank

\[
r_{\tau,m}=d_\tau m.
\]

Because the base has only 11 vertices, XBR-05C completely enumerates all vertex-simple cycles rather than sampling them. For each support graph it also computes the cycle rank

\[
\beta_1=E-V+C.
\]

### 5.1 Exact census

| Quantity | Exact result |
|---|---:|
| Final certified primitive instances | 140 |
| Exact primitive types | 48 |
| Type/multiplicity support graphs | 48 |
| Cyclic exact support graphs | 0 |
| Exact supported simple cycles | 0 |
| Shortest exact supported cycle | none |
| Coarse-only control graphs | 1 |
| Coarse-only control cycles | 1 |
| Holonomy matrices computed | 0 |
| Strict checks | 23/23 |

Scientific outcome:

```text
all_exact_support_graphs_are_forests_coarse_cycles_only
```

### 5.2 05C conclusion

All 48 exact primitive-type/fixed-multiplicity support graphs are forests. No certified exact primitive sector supports a closed path of any length on the audited base.

The only cycle occurs in the quarantined coarse control graph. Exact representation classification removes the apparent loop.

---

## 6. Combined exact result

The XBR-05A–05C sequence establishes the following finite classification.

### Proposition: conventional null-channel holonomy obstruction at \(n=9\)

On the induced Johnson graph of the 11 singular proper OPW3–AMP channels:

1. every one of the 29 edges joins whole kernels of unequal dimension;
2. no exact primitive type with fixed multiplicity persists around any of the 24 minimal triangles;
3. for every one of the 48 exact primitive types and every occurring multiplicity, the induced support graph is a forest;
4. hence neither the whole kernels nor the certified exact primitive/fixed-multiplicity sectors provide a closed constant-rank support path on which a reversible connection could be defined.

Therefore:

\[
\boxed{
\text{Conventional exact-primitive null-channel holonomy is structurally unavailable at }n=9.
}
\]

This is stronger than merely obtaining identity loop matrices, but narrower than ruling out every possible generalized transport theory. There are no legitimate loop matrices in the audited category; accordingly, the probes correctly compute zero of them.

---

## 7. Why the coarse control matters

The contrast between the exact and coarse censuses is methodologically important:

\[
\text{coarse classification}
\longrightarrow
\text{one apparent cycle},
\]

whereas

\[
\text{exact group-and-character classification}
\longrightarrow
\text{48 forests and zero cycles}.
\]

A calculation based only on dimensions or coarse character fingerprints could therefore manufacture an apparent “holonomy target.” XBR-04F8B’s exact resolution is not decorative detail: it is what prevents unlike fibers from being identified and transported as though they were one bundle.

The control demonstrates a concrete false-positive mechanism rather than merely warning that one might exist.

---

## 8. What the result does not establish

The result does not prove that the null channels are inert or globally redundant. It does not exclude:

- singular or rank-changing correspondences;
- partial-isometry systems with explicitly modified backtrack laws;
- flag, quiver, or zigzag-persistence descriptions;
- a constant-rank subspace defined by data other than the audited exact primitive types;
- a different admissible base graph;
- a different value of \(n\);
- a later canonical cross-channel construction with a different fiber definition.

Each would be a new mathematical object with its own composition, gauge, reversal, and equivalence laws. None should be called ordinary holonomy without those laws.

The sequence also assigns no physical meaning to a kernel, representation type, coarse collision, support forest, or potential singular transport. In particular, it identifies no gauge field, phase, particle, memory degree of freedom, or observable.

---

## 9. Reproducibility record

### XBR-05A

```bash
python3 scripts/ehf_xbr_05a_null_channel_holonomy_definition_lock_minimal_loop_census.py \
  --xbr04f6-dir runs/ehf_xbr_04f6_v7 \
  --out-dir runs/ehf_xbr_05a \
  --strict
```

```text
EHF_XBR_05A_NULL_CHANNEL_HOLONOMY_DEFINITION_LOCK_MINIMAL_LOOP_CENSUS_PASS
```

### XBR-05B

```bash
python3 scripts/ehf_xbr_05b_primitive_null_subbundle_persistence_triangle_admissibility_audit.py \
  --xbr05a-dir runs/ehf_xbr_05a \
  --xbr04f8-dir runs/ehf_xbr_04f8 \
  --xbr04f8b-dir runs/ehf_xbr_04f8b \
  --out-dir runs/ehf_xbr_05b \
  --strict
```

```text
EHF_XBR_05B_PRIMITIVE_NULL_SUBBUNDLE_PERSISTENCE_TRIANGLE_ADMISSIBILITY_AUDIT_PASS
```

### XBR-05C

```bash
python3 scripts/ehf_xbr_05c_exact_primitive_support_graph_longer_loop_census.py \
  --xbr05a-dir runs/ehf_xbr_05a \
  --xbr05b-dir runs/ehf_xbr_05b \
  --out-dir runs/ehf_xbr_05c \
  --strict
```

```text
EHF_XBR_05C_EXACT_PRIMITIVE_SUPPORT_GRAPH_LONGER_LOOP_CENSUS_PASS
```

---

## 10. Programme decision

The friend’s holonomy suggestion was productive. It did not reveal a nontrivial phase; it exposed a sharper structural obstruction and a verified coarse-classification false positive.

The conventional holonomy route should now be treated as closed at the audited \(n=9\) exact-primitive level. The next programme should be chosen explicitly between:

1. **rank-changing null transport:** first define a singular correspondence, flag, quiver, or zigzag object and its laws, without importing holonomy terminology prematurely; or
2. **the OPW3–quantum-mechanics bridge:** use the closed XBR structural foundation to ask what physical-style structures can actually be reconstructed, while retaining the existing interpretation guardrails.

No XBR-05D is required merely to extend the census.
