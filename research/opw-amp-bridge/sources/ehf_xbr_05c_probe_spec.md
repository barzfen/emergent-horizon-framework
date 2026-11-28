# EHF-XBR-05C: Exact Primitive Support-Graph and Longer-Loop Census

## Purpose

EHF-XBR-05A established that the complete null kernels do not form a
constant-rank bundle on the 11-channel Johnson base. EHF-XBR-05B then found:

\[
0
\]

exact primitive persistence candidates on the 24 minimal triangles, together
with one coarse-only cross-group recurrence that is not a certified common
module.

XBR-05C tests the remaining conventional-holonomy prerequisite:

> Can an exactly certified primitive null sector recur with constant rank
> around a square or any longer closed path even though it does not recur
> around a triangle?

The probe is a support-graph census. It does not construct edge transports or
compute holonomy.

## Exact support object

Let \(\tau\) be an exact primitive type from the final merged XBR-04F8/F8B
census, with primitive dimension \(d_\tau\). For each multiplicity \(m\) that
actually occurs across the null channels, define

\[
V_{\tau,m}
=
\left\{
A:
\operatorname{mult}_{K_A}(\tau)=m
\right\}.
\]

The support graph \(G_{\tau,m}\) is the full induced subgraph of the XBR-05A
base on \(V_{\tau,m}\). Its candidate isotypic fiber rank is

\[
r_{\tau,m}=d_\tau m.
\]

Splitting by the *actual* multiplicity is essential. If a type occurs once at
one channel and twice at another, selecting one of the two copies at the
second channel would introduce a noncanonical choice. Those vertices therefore
belong to different support slices.

## Closed-path test

For every \(G_{\tau,m}\), XBR-05C records:

- vertex and induced-edge counts;
- connected components and component sizes;
- cycle rank

  \[
  \beta_1=E-V+C;
  \]

- whether the graph is a forest;
- every undirected vertex-simple cycle;
- the shortest supported cycle;
- the exact rank \(r_{\tau,m}\) that a later transport constructor would need
  to preserve.

Because the base has only 11 vertices, the script performs a complete
simple-cycle enumeration rather than sampling cycles. The safety limit
`--max-enumerated-cycles-per-graph` defaults to 100,000 and causes an explicit
failure rather than a silently truncated census.

Cycle rank and simple-cycle count are different quantities. A graph can have
cycle rank two but contain more than two simple cycles. Both are reported.

## Exact identity gate

A support graph contributes to the scientific verdict only when:

1. every block is certified rationally irreducible;
2. one exact primitive type hash is used throughout;
3. that exact hash has one primitive dimension;
4. that exact hash has one literal acting-group identity;
5. the multiplicity is fixed by construction.

The exact type hash contains the literal group identity and exact primitive
character inherited through the certified XBR-04F8/F8B construction.

## Coarse-only control

The single coarse-only triangle found by XBR-05B is reconstructed separately.
Its coarse support graph and cycles are written to control ledgers, including
the distinct exact-type profile at each vertex.

A coarse collision is never promoted to:

- exact primitive identity;
- a constant-rank exact subbundle;
- transport admissibility;
- holonomy.

The strict audit requires the XBR-05B coarse triangle to reappear as a cycle in
the coarse control graph while remaining excluded from the exact census.

## Production command

```bash
python3 scripts/ehf_xbr_05c_exact_primitive_support_graph_longer_loop_census.py \
  --xbr05a-dir runs/ehf_xbr_05a \
  --xbr05b-dir runs/ehf_xbr_05b \
  --out-dir runs/ehf_xbr_05c \
  --strict
```

No XBR-04F8 or XBR-04F8B directory is required. XBR-05B already wrote the
final certified merged primitive ledger and recorded source hashes.

## Self-test

```bash
python3 scripts/ehf_xbr_05c_exact_primitive_support_graph_longer_loop_census.py \
  --self-test
```

The self-test verifies:

- bare, parenthesized, and bracketed subset parsing;
- complete canonical cycle enumeration on a graph containing two triangles
  and one square;
- the distinction between cycle rank and simple-cycle count;
- exact splitting of one primitive type into multiplicity-one and
  multiplicity-two support graphs;
- the refusal to compute any holonomy matrix.

## Outputs

- `exact_primitive_support_graph_ledger.csv`
- `exact_primitive_support_component_ledger.csv`
- `exact_primitive_simple_cycle_ledger.csv`
- `coarse_support_graph_control_ledger.csv`
- `coarse_simple_cycle_control_ledger.csv`
- `coarse_triangle_reproduction_ledger.csv`
- `run_summary.json`
- `report.md`

The exact simple-cycle ledger is intentionally empty if every exact support
graph is a forest.

## Scientific outcomes

### Exact longer loop found

```text
exact_longer_loop_support_found_transport_not_defined
```

At least one exact fixed-multiplicity primitive support graph contains a
cycle. Its shortest cycle is the correct target for a subsequent exact edge
transport constructor. A supported loop is not yet holonomy.

### Exact supports are forests, coarse cycles remain

```text
all_exact_support_graphs_are_forests_coarse_cycles_only
```

No certified exact primitive sector supports a closed path of any length.
Only the quarantined coarse collision closes a loop. This closes the
conventional exact-primitive null-channel holonomy route at the audited
\(n=9\) scale.

### No closed support path

```text
all_exact_primitive_support_graphs_are_forests
```

Neither an exact primitive support nor a coarse control supplies another
closed path.

## Interpretation discipline

If an exact cycle exists, XBR-05C certifies only:

\[
\text{same exact primitive type}
+
\text{same multiplicity}
+
\text{closed induced support path}.
\]

It does **not** certify:

\[
\text{canonical edge transport},
\qquad
\text{reversibility},
\qquad
\text{backtrack identity},
\qquad
\text{gauge covariance},
\qquad
\text{holonomy}.
\]

Those require a later exact construction with a certificate on every edge of
the selected cycle.

## Claim boundary

XBR-05C is an exact finite \(n=9\) primitive support-graph and complete
simple-cycle census. A closed exact support path is not a connection. A coarse
collision is not a module identity. The probe assigns no physical phase,
gauge field, particle, memory, observable, or other physical interpretation.
