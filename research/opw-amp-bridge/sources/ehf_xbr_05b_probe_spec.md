# EHF-XBR-05B: Primitive Null-Subbundle Persistence and Triangle Admissibility Audit

## Purpose

EHF-XBR-05A established an exact obstruction to ordinary whole-kernel
holonomy: the 11 null channels form a connected graph with 29 Johnson edges
and 24 minimal triangles, but every edge changes the complete kernel
dimension.

XBR-05B asks whether the obstruction disappears inside a smaller,
representation-theoretically certified part of the kernel.

For a minimal triangle

\[
A_0\sim A_1\sim A_2\sim A_0,
\]

the audit searches for an exact primitive type \(\tau\) whose isotypic part
occurs at every vertex:

\[
E_{\tau,A_i}\subseteq K_{A_i}.
\]

It then separates primitive persistence from the stronger existence of a
connection.

## Final primitive census

The source census is reconstructed exactly:

1. load the XBR-04F8 primitive-module ledger;
2. retain every F8 block already certified rationally irreducible;
3. remove the residual F8 blocks classified by XBR-04F8B;
4. insert the certified F8B children;
5. for a split \(M_2(\mathbb Q)\) residual block, inherit the exact type of the
   certified sibling only when F8B supplies the exact full-rank module
   isomorphism and character-equality certificates;
6. for a quaternion-division residual block, retain the source exact character
   type only after the division commutant certifies rational irreducibility.

Subset fields may use either the canonical parenthesized serialization emitted
by XBR-04F8/F8B, such as `(2, 3, 4)`, or the bare comma-separated serialization
emitted by XBR-05A, such as `2,3,4`. Both normalize to the same internal key.

The merged inventory must reproduce every channel-kernel dimension, total
dimension \(216\), and the final F8B certified-block count.

## Three evidence levels

### 1. Exact primitive persistence

An exact primitive type hash contains:

- the literal acting-group identity;
- the exact primitive character.

A candidate triangle subbundle is recorded only if:

1. the same exact type occurs at all three vertices;
2. all blocks are certified rationally irreducible;
3. the primitive dimension is constant;
4. the literal acting group is identical;
5. the multiplicity is constant.

If the primitive dimension is \(d_\tau\) and its common multiplicity is
\(m_\tau\), the candidate isotypic subbundle has rank

\[
r_\tau=d_\tau m_\tau.
\]

Constant multiplicity is required because selecting one copy from an
unequal-multiplicity isotypic space would introduce a noncanonical choice.

### 2. Coarse recurrence control

F8 also supplies a coarse type hash formed from dimension, group-order, and
order/trace data. A coarse match across different literal groups is useful as
a search heuristic, but it is not a certified module isomorphism.

Coarse-only triangle matches are written to a control ledger and can never
make a triangle transport-admissible.

### 3. Transport admissibility

Exact persistence does not define an edge map. A triangle becomes
transport-admissible only when all three edges have an external exact
certificate with:

- a canonically defined comparison;
- source and target subbundle dimensions equal to \(r_\tau\);
- full-rank forward and reverse maps;
- exact forward–reverse and reverse–forward identities;
- exact gauge covariance;
- a passing source audit and nonempty certificate provenance hash.

Without those certificates, 05B reports a persistence candidate but does not
call it a connection and does not compute holonomy.

## Optional transport-certificate ledger

The default 05B run does not consume a transport ledger, because F8/F8B do
not provide cross-channel maps. A later exact construction can be audited by
passing:

```text
--transport-certificate-ledger PATH
```

Each row must contain:

```text
exact_primitive_type_hash
source_subset
target_subset
subbundle_rank
source_subbundle_dimension
target_subbundle_dimension
forward_rank
reverse_rank
canonical_comparison_defined
forward_reverse_identity_exact
reverse_forward_identity_exact
gauge_covariance_exact
strict_pass
certificate_sha256
```

The source and target order is irrelevant because both directions and both
backtracks must be certified.

## Production command

```bash
python3 scripts/ehf_xbr_05b_primitive_null_subbundle_persistence_triangle_admissibility_audit.py \
  --xbr05a-dir runs/ehf_xbr_05a \
  --xbr04f8-dir runs/ehf_xbr_04f8 \
  --xbr04f8b-dir runs/ehf_xbr_04f8b \
  --out-dir runs/ehf_xbr_05b \
  --strict
```

If the passing F8 or F8B directory on disk has a suffix, substitute its exact
path.

## Self-test

```bash
python3 scripts/ehf_xbr_05b_primitive_null_subbundle_persistence_triangle_admissibility_audit.py \
  --self-test
```

The self-test verifies:

- the bare, parenthesized, and bracketed upstream subset serializations all
  normalize to one validated three-subset;
- exact constant-multiplicity persistence without edge certificates does not
  become transport-admissible;
- three complete exact edge certificates do make the synthetic triangle
  transport-admissible;
- an F8 split residual block is replaced by its F8B children;
- child type inheritance is allowed only through the certified sibling
  isomorphism.

## Outputs

- `final_primitive_module_ledger.csv`
- `primitive_type_persistence_ledger.csv`
- `triangle_persistence_ledger.csv`
- `exact_triangle_subbundle_candidate_ledger.csv`
- `coarse_triangle_candidate_control_ledger.csv`
- `transport_certificate_requirement_ledger.csv`
- `run_summary.json`
- `report.md`

The requirements ledger is particularly important. If exact persistence is
found, it gives the precise type, edge, and expected rank that a subsequent
cross-channel transport constructor must certify.

## Scientific outcomes

The audit reports one of four conclusions:

```text
no_primitive_triangle_persistence
coarse_triangle_recurrence_only_no_exact_subbundle
exact_primitive_persistence_found_transport_not_certified
transport_admissible_primitive_triangles_found
```

The integrity verdict is separate. A strict PASS means the census and gates
were applied exactly; it does not force a positive persistence result.

## Claim boundary

XBR-05B is an exact finite \(n=9\) primitive-module persistence and
transport-admissibility audit. Matching coarse signatures are not module
isomorphisms. Matching exact primitive types do not by themselves define
cross-channel comparison maps. The probe computes no loop product, assigns no
holonomy, and makes no identification with a physical phase, gauge field,
particle, memory, or observable.
