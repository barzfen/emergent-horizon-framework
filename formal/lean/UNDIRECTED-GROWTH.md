# EHF-LEAN-03 — Undirected all-slot growth under dihedral equivalence

**Status (2026-11-24):** Mathematical bijection proof supplied below;
the stated quotient/deletion/insertion ancestry lemmas have passed
Lean 4.36.0 in [`UndirectedCycles.lean`](UndirectedCycles.lean).
**The complete bijection and cardinality recurrence are not yet
machine-checked in Lean.** Do not claim otherwise.

This documents the original CBB all-slot rule using **uncoloured**
Hamiltonian cycles on complete labelled graphs, as distinct from
strictly alternating-colour systems or graph-restricted cycles.

## Theorem: all-slot insertion is a bijection

Let `H_n` be the set of undirected Hamiltonian cycles on
`V_n = {0,...,n-1}`, modulo cyclic rotation and reversal, with
`n ≥ 3`. Put `w = n`.

Let `I_n = {(C,e) : C ∈ H_n, e ∈ E(C)}`, where `E(C)` is
the set of unordered edges in cycle `C`.

There is a bijection

```text
F_n : I_n  ↔  H_(n+1)
F_n(C,e) = cycle obtained by replacing e={u,v}
             with {u,w} and {w,v}.
```

Consequently `|H_(n+1)| = n |H_n|`. Since `|H_3| = 1`,
induction gives `|H_n| = (n-1)! / 2` for all `n ≥ 3`.

### Proof (ordinary mathematics; pending full Lean translation)

1. **Well-definedness under dihedral equivalence.** Rotating a
   listing changes only the first written vertex. Reversing it
   reverses traversal. Neither operation changes the *unordered*
   edges of the cycle. Thus choosing an edge `e` of the undirected
   cycle and subdividing that edge with `w` is independent of the
   listing and orientation used to represent `C`.

2. **Valid growth.** Replacing one cycle edge by a two-edge path
   through fresh vertex `w` preserves the property that every
   old vertex appears exactly once, and `w` appears exactly once.
   The resulting closed walk is a simple cycle visiting all
   `n+1` vertices, so it is in `H_(n+1)`.

3. **Inverse.** In a child cycle `D ∈ H_(n+1)`, the distinguished
   vertex `w` has two distinct neighbours `u` and `v`.
   Remove `w` and its two incident edges and join `u` directly
   to `v`. The result is an undirected n-vertex Hamiltonian cycle
   `C`. Remember the *specific* edge `e={u,v}` in `C`.
   This produces `(C,e) ∈ I_n`.

4. **Inverse laws.** Removing `w` from an inserted cycle
   restores the exact parent cycle and marked edge. Conversely,
   reinserting `w` into the marked edge recovered from any child
   reproduces that child. Thus the maps are mutual inverses.

5. **Counting.** Every `C ∈ H_n` has exactly `n` distinct
   undirected cycle edges (for `n ≥ 3`). Hence
   `|I_n| = n|H_n|`. Bijection proves the recurrence. Starting
   at the sole triangle cycle for `n=3` yields
   `|H_n|=(n-1)!/2`.

This is an elementary known combinatorial fact; the objective is
precise, independently repeatable EHF formalisation, **not** a
novel discovery.

## What Lean actually checks today

[The Lean source](UndirectedCycles.lean) has general lemmas that:

- the relation `xs = ys` or `xs = ys.reverse` is an equivalence;
- a quotient by this relation precisely models reversal of a tail
  once the distinguished root has been fixed at the start;
- deleting a label by filtering descends to this quotient;
- deletion following insertion recovers the parent when the new
  label is fresh;
- **two insertion histories producing the same undirected child
  quotient have the same undirected parent quotient**;
- deleting and reinserting a known list entry reconstructs it;
- each oriented child containing the inserted label admits such an
  insertion reconstruction.

These Lean statements are about generic lists / their quotients.
Valid cyclic vertex listings require the existing
`HamiltonianCycle` no-duplication, coverage and length assumptions.
Those are formalised separately in [`CycleGrowth.lean`](CycleGrowth.lean)
for root-fixed oriented complete-graph cycles.

### Remaining full-formalisation gap

Formalise the **unoriented marked edge** type and prove, *in Lean*,
that the insertion function on equivalence classes is well-defined
under reflection with the corresponding reflected insertion slot,
then establish inverse functions, their proofs and finite cardinality
recurrence on fully valid cycle quotients. The quotient above
normalises **rotation by fixing the root**; a formal equivalence to
the unrestricted dihedral quotient also remains to be established.

Do **not** promote the elementary paper proof to a Lean theorem
based on the present file alone.

## Independent finite audit

Run:

```sh
python3 formal/lean/verify_undirected_growth.py
```

The [finite oracle](verify_undirected_growth.py) enumerates every
undirected cycle represented with root 0 and canonical choice
of forward/reverse orientation, verifies all n insertion slots,
checks unique ancestry and checks complete coverage against an
independent enumeration at n+1.

| Parent n | Parents | Distinct children |
| ---: | ---: | ---: |
| 3 | 1 | 3 |
| 4 | 3 | 12 |
| 5 | 12 | 60 |
| 6 | 60 | 360 |
| 7 | 360 | 2,520 |
| 8 | 2,520 | 20,160 |

No collisions or missing children were found for these finite cases.
This is **testing**, not a proof for all n.

## Context

- [Binary growth programme](../../research/cbb-binary/README.md)
- [EHF-LEAN-01 and EHF-LEAN-02](README.md)
- The elementary recurrence is for the complete ambient graph;
  restricting which edges are admissible, imposing colour constraints,
  or allowing history-dependent moves changes the problem.
