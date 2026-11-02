# EHF-XBR-05A: Null-Channel Holonomy Definition Lock and Minimal Loop Census

## Purpose

EHF-XBR-04F8B completed the exact rational decomposition of the 216-dimensional aggregate kernel carried by the 11 singular proper OPW3–AMP channels. XBR-05A asks whether those channel kernels already support a mathematically valid ordinary holonomy audit.

The answer must be decided before computing overlap matrices. Holonomy requires:

1. a base graph;
2. a fiber over every base vertex;
3. a reversible, gauge-covariant edge transport;
4. closed paths along which the fiber type is preserved.

XBR-05A locks the first two objects and audits the prerequisite for the third.

## Locked base and fiber

The base vertices are the 11 singular proper channels recorded by XBR-04F6:

\[
A\subset\{2,\ldots,8\},\qquad |A|=3.
\]

The candidate edge relation is Johnson adjacency:

\[
A\sim B
\quad\Longleftrightarrow\quad
|A\cap B|=2.
\]

The fiber is the complete exact chamber adjacency kernel:

\[
K_A=\ker\mathcal A_A.
\]

This choice is deliberately narrow. The word “null” means zero under the finite chamber adjacency action audited in XBR-04F6. It is not a claim of physical invisibility.

## Reversible-transport gate

For ordinary orthogonal or unitary holonomy, every edge transport must be an isomorphism:

\[
T_{B\leftarrow A}:K_A\longrightarrow K_B.
\]

Therefore:

\[
\dim K_A=\dim K_B
\]

is a necessary condition on every transported edge.

If dimensions differ, a rectangular overlap can at most produce a partial isometry after polar decomposition. Its reverse followed by itself is generally a projector rather than the identity:

\[
T_{A\leftarrow B}T_{B\leftarrow A}\ne I_{K_A}.
\]

Such a construction fails the immediate-backtrack control and is not ordinary holonomy.

## Minimal-loop census

The script reconstructs the induced Johnson graph on the singular channels and enumerates its shortest simple cycles. It records:

- vertex and edge counts;
- connected components;
- shortest loop length;
- every shortest loop;
- the kernel-dimension profile around every loop;
- equal- and unequal-dimension edge counts;
- whether whole-fiber reversible transport is admissible.

No loop matrix, eigenphase, trace, or determinant is computed unless a later probe supplies a certified connection.

## Expected locked result

For the completed XBR-04F6 dataset:

\[
|V|=11,\qquad |E|=29.
\]

The induced graph is connected and has:

\[
\operatorname{girth}=3,
\qquad
24\text{ shortest triangles}.
\]

However:

\[
\#\{A\sim B:\dim K_A=\dim K_B\}=0.
\]

Thus the graph is loop-rich but the whole-kernel fibers change dimension on every edge. The expected scientific conclusion is:

```text
holonomy_defined = false
```

This is not a failed probe. It is the definition-lock result: ordinary whole-null-fiber holonomy is not admissible on the candidate Johnson base.

## Inputs

Required XBR-04F6 outputs:

- `run_summary.json` with `strict_pass=true`;
- `kernel_channel_ledger.csv`;
- the exact 11-channel census with aggregate kernel dimension 216.

The script does not need to reload the 216 basis vectors because it does not claim an edge transport.

## Production command

```bash
python3 scripts/ehf_xbr_05a_null_channel_holonomy_definition_lock_minimal_loop_census.py \
  --xbr04f6-dir runs/ehf_xbr_04f6_v7 \
  --out-dir runs/ehf_xbr_05a \
  --strict
```

If the final passing F6 directory on disk is named `ehf_xbr_04f6_v6`, substitute that path.

## Self-test

```bash
python3 scripts/ehf_xbr_05a_null_channel_holonomy_definition_lock_minimal_loop_census.py \
  --self-test
```

Expected:

```text
EHF-XBR-05A self-test PASS
```

## Outputs

- `null_channel_vertex_ledger.csv`
- `null_channel_edge_ledger.csv`
- `minimal_loop_ledger.csv`
- `run_summary.json`
- `report.md`

## Strict checks

Strict PASS requires:

1. the source F6 run passed;
2. 11 unique singular three-subsets are loaded;
3. every kernel dimension is positive;
4. the aggregate kernel dimension is 216;
5. the induced Johnson graph has 29 edges and is connected;
6. its shortest cycles are 24 triangles;
7. no edge joins equal-dimensional whole fibers;
8. no loop is falsely assigned a holonomy matrix.

Expected integrity verdict:

```text
EHF_XBR_05A_NULL_CHANNEL_HOLONOMY_DEFINITION_LOCK_MINIMAL_LOOP_CENSUS_PASS
```

## Next mathematical gate

A genuine XBR-05B holonomy computation should be attempted only after one of the following is constructed exactly:

1. a recurring primitive module that occurs with constant dimension at every vertex of a loop-rich subgraph, together with certified cross-channel intertwiners;
2. a constant-rank spectral or symmetry-defined subbundle preserved by a canonical comparison;
3. a separately defined singular-transport framework with explicit composition, gauge, reversal, and backtrack laws.

Primitive modules with the same dimension are not automatically the same fiber type. Matching requires a common acting group or an explicit cross-channel comparison certificate. XBR-04F8B removes within-channel multiplicity ambiguity, but it does not itself supply cross-channel transport.

## Claim boundary

XBR-05A is an exact finite \(n=9\) graph-and-dimension result. It neither establishes nor rules out every possible generalized holonomy. It rules out only an unqualified ordinary holonomy computation on the complete 11 chamber kernels using the candidate Johnson adjacency.
