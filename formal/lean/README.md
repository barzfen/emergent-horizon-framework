# EHF formal verification — Lean 4

## First candidate: binary edge-splitting invariant

**Status:** Proof source prepared; the GitHub Actions Lean run is the
independent compiler check. Do not label it machine-verified until that
run succeeds.

Source: [`EdgeSplit.lean`](EdgeSplit.lean).

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
- The file deliberately uses Lean's core library only, with no
  `sorry` placeholders and no added axioms.

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
