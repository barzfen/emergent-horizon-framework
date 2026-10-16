# Wheeler / Hamilton-History Probe Series

Origin: re-examination of Wheeler's one-electron intuition through EHF Hamilton-history structure. The physical analogy is secondary; the retained results are the mathematical statements about projected multiplicity, signed crossings, topology, and dynamics.

## WHEELER-01 — Closed Hamilton history / real observer time

**Status: PROVED structure + toy-model interpretation**

For an oriented closed cycle `C` with scalar observer function `T:C -> R`, every regular level has equal numbers of positive- and negative-orientation crossings:

`N_+(t) - N_-(t) = 0`.

Consequences:

- one global history can appear as multiple simultaneous local objects under slicing;
- apparent object number can change with slice;
- orientation-opposed crossings appear in balanced pairs;
- a bare closed cycle with ordinary real-valued slicing cannot support nonzero signed excess.

## WHEELER-02 — Open Hamilton path / endpoint invariant

**Status: PROVED**

For an oriented finite path `P` with scalar observer function `T:P -> R`, the signed crossing number of a regular level depends only on the endpoints:

`I_t(P) = N_+(t) - N_-(t) = H(T_N-t) - H(T_1-t)`.

If the start lies below the slice and the end above it, then:

`I_t(P)=1`.

Interior folds can create arbitrarily many balanced crossing pairs without changing the net signed count.

## WHEELER-03 — Closed history / periodic observer time

**Status: PROVED topological invariant; computationally stress-tested**

For `T:S^1 -> S^1`, the signed crossing number equals the degree/winding number:

`N_+ - N_- = deg(T) = w`.

Local folding changes apparent multiplicity through balanced pairs but cannot change `w` without changing the homotopy/topological sector.

Interpretive caution: this is not a derivation of electric charge. It is a clean example of variable local multiplicity coexisting with an integer-valued global invariant.

## WHEELER-04 — Topological sectors / minimal local dynamics

**Status: MIXED**

Toy dynamics: cyclic orientation words with local exchange

`(+,-) <-> (-,+)`.

Define conserved sector label `W = sum_i s_i`.

Results:

- **PASS:** local dynamics preserve `W` and split state space into disconnected sectors.
- **PASS:** sector sizes/entropies depend strongly on `W`.
- **NEGATIVE:** in the minimal symmetric model, the leading spectral gap is independent of nontrivial `W` sectors.
- **PASS:** the measured gap follows

`lambda_1(n) = 2 - 2 cos(2 pi/n) = 4 sin^2(pi/n)`,

so for large `n`,

`lambda_1 ~ 4 pi^2 / n^2`,

implying diffusive relaxation scaling `tau ~ n^2`.

This last result is currently more important for EHF than the particle analogy: a simple local admissible dynamics yields a recognizable long-wavelength transport law.

## Next proposed probe

**WHEELER-05 — Local admissibility / sector-energy audit**

Question: can purely local interaction rules, with no explicit dependence on the global winding label, generate sector-dependent minimum energies or other dynamical distinctions?

Failure criterion: if sector dependence appears only after inserting `W` explicitly into the energy/Hamiltonian, the mechanism has not emerged.
