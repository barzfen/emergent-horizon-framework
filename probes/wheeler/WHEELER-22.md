# WHEELER-22 — Boundary Energy / Mass-Gap Audit

**Status: PASS for a finite boundary-excitation gap in the MICRO/Wheeler toy system; NOT a Yang–Mills mass-gap result**

## Question

Using the oriented boundary field from WHEELER-21,

- `j_i = +1` for a `0->1` boundary,
- `j_i = -1` for a `1->0` boundary,
- `j_i = 0` otherwise,

can a natural local boundary energy produce a nonzero excitation gap above the vacuum, and does that gap survive growth?

## Simplest energy

Take

`E = sum_i |j_i| = D`,

where `D` is the MICRO domain-wall count.

For a closed binary cycle, boundaries alternate orientation, so the number of domain walls is even. Therefore

`D = 0, 2, 4, ...`

and the first non-vacuum sector has

`D = 2`.

Exact enumeration of zero-cost MICRO states for `n = 4..14` confirms that whenever non-vacuum zero-cost states exist, the smallest positive value is always `D=2`.

Hence for `E=D`,

`Delta E = 2`.

This gap is independent of system size over the tested range.

## General local additive boundary energy

Let

`E[j] = sum_i e(j_i)`

with

- `e(0)=0`,
- `e(+1)>0`,
- `e(-1)>0`.

On a closed binary cycle, every `+1` boundary is paired with a `-1` boundary. The smallest nontrivial excitation therefore contains one of each, giving

`Delta E = e(+1) + e(-1) > 0`.

Thus the finite gap follows from closure plus positive local boundary cost; it is not specific to the symmetric choice `e(+1)=e(-1)=1`.

For the quadratic choice `e(j)=j^2`, the same result is recovered because `j in {-1,0,+1}` and therefore `j^2=|j|`.

## Growth stability

WHEELER-20 established that admissible zero-cost growth preserves domain-wall number `D` exactly. Therefore any energy depending only on `D` remains unchanged under such growth.

So for `E=D`, the gap is growth-stable:

`Delta E(n) = 2`

through all sizes reached by admissible growth.

## Sector structure

In the closed binary MICRO cycle, the signed current

`Q = sum_i j_i`

is identically zero. Therefore this specific closed binary model does **not** provide distinct nonzero `Q` sectors whose low-energy spectra can be compared.

Nonzero signed sectors require either

- open histories/endpoints, where `Q` reduces to endpoint imbalance, or
- a lifted periodic construction, where `Q` can become a winding number.

Those are structurally available from earlier Wheeler probes, but they are not simultaneously realized by the present closed binary MICRO model without extending the state space.

## Interpretation

This is a genuine finite excitation gap for the toy boundary model:

`vacuum D=0 -> first excitation D=2`.

However, the result is limited. The energy was chosen as a positive local cost on already-identified boundary excitations. The gap is therefore structurally natural but not dynamically surprising.

It does **not** constitute evidence for the Yang–Mills mass gap. In Yang–Mills, one must establish a nonzero spectral gap for the interacting quantum Hamiltonian in the continuum/infinite-volume theory. Here we have instead shown a discrete combinatorial excitation-cost gap in a constrained binary system.

The useful EHF lesson is narrower:

`closure + quantized local boundary excitations + positive local energy -> size-independent finite excitation gap`.

This provides a benchmark mechanism that a more serious EHF quantum model would need to reproduce without putting the gap in by hand.

## Verdict

- **PASS:** `E=D` gives a nonzero gap `Delta E=2`.
- **PASS:** the gap is size-independent for exact enumeration `n=4..14`.
- **PASS:** the gap is preserved by the existing admissible zero-cost growth rule because growth preserves `D`.
- **PASS (generalized):** any positive local additive boundary cost gives `Delta E=e(+1)+e(-1)` on a closed binary cycle.
- **NEGATIVE / limitation:** the closed binary MICRO model has only `Q=0`, so there is no nontrivial signed-sector spectral comparison here.
- **CAUTION:** this is a combinatorial excitation gap, not a Yang–Mills mass-gap derivation.

## Next probe

A stronger next step is **WHEELER-23 — Dynamical Spectral Gap / Boundary-Hamiltonian Audit**.

Instead of assigning static excitation costs only, define a Hamiltonian or Markov generator from the existing admissible local moves and test whether the lowest nonzero eigenvalue remains positive or follows a controlled scaling law as `n` grows. That would distinguish a static cost gap from a true dynamical/spectral gap.