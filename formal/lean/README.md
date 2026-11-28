# EHF formal verification — Lean 4

## EHF-LEAN-03: undirected quotient and predecessor uniqueness

**Status:** Lean 4.36.0 verifies the
[reversal quotient, orientation-independent deletion, insertion inverse,
unique undirected parent and child reconstruction](UndirectedCycles.lean).
A [mathematical proof of the full undirected all-slot bijection](UNDIRECTED-GROWTH.md)
and an [independent complete small-order enumeration](verify_undirected_growth.py)
are included.

**Important:** The full edge-marked bijection, dihedral normalization
equivalence and factorial count have **not** yet been proved in Lean.
The mathematical argument and finite numerical checks are separate
from the formal proof status.

## EHF-LEAN-02: whole-cycle all-slot growth and unique ancestry

**Status: MACHINE-VERIFIED.** Lean 4.36.0 accepted
[`CycleGrowth.lean`](CycleGrowth.lean) in
[GitHub Actions run 45178161757](https://github.com/barzfen/emergent-horizon-framework/actions/runs/45178161757)
on 2026-11-23. No `sorry` placeholders or new axioms were introduced.
The declarations depend only on Lean's ordinary logical axioms
(`propext`, `Classical.choice`, `Quot.sound`), as shown by
`#print axioms`.

**Representation.** A cycle is an ordered list of distinct vertices
covering an explicitly declared finite label set, of length at least
three. Successive vertices are adjacent, and the last is connected to
the first. All edges are admissible because the ambient graph is
**complete**. Fixing the list's first entry and direction gives a
*rooted, oriented* representation; cyclic rotations and reversal are
**not** quotiented yet.

**Growth.** For an n-vertex parent, every `slot : Fin n` selects an
edge *after* a vertex. The final slot chooses the closing edge.
Inserting fresh vertex `w` directly after the selected vertex gives
a child on the original labels plus `w`.

Verified properties:

1. `insertAfter` builds a valid Hamiltonian cycle: all labels occur
   exactly once, and the new child has at least three vertices.
2. `insertion_length`: the child has n + 1 vertices.
3. `insertion_membership`: the child's labels are exactly the original
   labels plus `w`.
4. `delete_inserted`: erasing the entry at the insertion position
   recovers the original ordered parent.
5. `distinct_slots`: two different slots of a fixed parent produce
   different ordered children.
6. `unique_ancestry`: if two generated children are identical as
   ordered lists, their insertion positions and parent listings are
   identical, even when the proposed parent label lists differ.

The last result is the **non-overlap** direction of the full CBB
ancestry claim for rooted, oriented cycle listings. It does not by
itself show that **every** possible (n+1)-vertex directed cycle is in
the generated image under a fixed-root convention, nor does it prove
the bijection of undirected cycles modulo the dihedral symmetry group.
Those require an explicit normalization/quotient and a converse
existence theorem.

**Reproduce:**

```sh
lean formal/lean/CycleGrowth.lean
```

**Physical scope:** No cosmological interpretation follows from this
combinatorial result. Growth restrictions in a non-complete ambient
graph, alternating colours, reversal dynamics, and quotient counting
remain separate research tasks.

---

## EHF-LEAN-01: binary edge-splitting invariant

**Status: MACHINE-VERIFIED.** Lean 4.36.0 accepted the theorem in
[GitHub Actions run 45176260310](https://github.com/barzfen/emergent-horizon-framework/actions/runs/45176260310)
on 2026-11-23. The compiler reported that the theorem **does not depend
on any axioms**. This status applies to the unchanged proof in
[`EdgeSplit.lean`](EdgeSplit.lean); later changes must be rechecked.

This formalises a local relationship already discussed in
[EHF-CBB-BIN](../../research/cbb-binary/README.md), not a new physical
result and not a proof of general Hamiltonian-cycle growth.

Let vertex labels `u`, `v` and inserted label `w` be Boolean.
Define the edge-comparison bit as XOR:
`edgeBit u v = u XOR v`.

For the edge-splitting operation

```text
u --- v     becomes     u --- w --- v
```

the theorem establishes, for **all** labels `u`, `w`, `v`:

```text
(u XOR w) XOR (w XOR v) = u XOR v
```

This holds because the inserted label occurs twice and cancels. It
holds for both choices of `w`; there is no distinguished inserted
colour. The proof performs exhaustive case-splitting on the three
Booleans, which is exhaustive by construction (8 cases).

### Scope and limitations

- This concerns one replaced edge with **all existing endpoint labels
  held fixed**. It does not address the rest of the cycle.
- The underlying EHF all-slot Hamiltonian-cycle growth works for both
  odd and even cycle lengths. Strictly alternating vertex colours
  would introduce an additional parity restriction and are **not**
  assumed here.
- The result is an elementary XOR identity. It validates one formal
  building block of the binary extension; it is not evidence for a
  physical interpretation of EHF.
- The proof uses Lean's core library only, with no `sorry` placeholders
  and no added axioms.

### Reproduce

From the repository root, install Lean via the pinned
[`lean-toolchain`](../../lean-toolchain), then run:

```sh
lean formal/lean/EdgeSplit.lean
```

The [EHF Lean proofs workflow](../../.github/workflows/ehf-lean.yml)
runs this command on PRs and relevant changes to `main`.

Future work should state a complete cycle type and insertion operator,
then prove the corresponding lift/deletion statement. This local
result alone does **not** do so.
