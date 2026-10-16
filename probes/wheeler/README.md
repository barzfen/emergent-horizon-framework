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

## WHEELER-05 — Local imbalance energy / sector-energy audit

**Status: PASS with important qualification**

Choose a local energy that does not reference the global winding label:

`E[s] = sum_i (s_{i-1} + s_i + s_{i+1})^2`, with `s_i in {-1,+1}` on a cycle.

The local exchange dynamics remains `(+,-) <-> (-,+)`, so `W = sum_i s_i` is conserved without appearing explicitly in the energy.

### Computational results

Exact enumeration for `n = 6, 8, 10, 12` shows that different `W` sectors acquire different energy distributions even though the rule is purely local.

The sector minimum energy is not a clean quadratic function of `W`; it contains plateaus and parity/local-packing effects. Therefore the strongest hoped-for result — a natural `E_min(W) proportional to W^2` law — **did not emerge**.

However, the **sector-average energy** is exactly quadratic in `W`.

Expanding the local rule gives

`E = 3n + 4 sum_i s_i s_{i+1} + 2 sum_i s_i s_{i+2}`.

For the uniform ensemble of configurations at fixed `W`, any distinct-site correlation satisfies

`<s_i s_j>_W = (W^2 - n) / [n(n-1)]`.

Hence

`<E>_W = 3n + 6 (W^2 - n)/(n-1)`.

So the local interaction generates an exact sector dependence proportional to `W^2` in the ensemble mean, without any explicit global `W` term being inserted.

### Dynamical consequence

Using continuous-time local exchange with Metropolis rates based only on the same local energy, the relaxation gap becomes sector-dependent. For example at `n=10`, inverse-temperature parameter `beta=0.1` gave approximately:

- `W=0`: gap `0.749936`
- `|W|=2`: gap `0.719395`
- `|W|=4`: gap `0.649355`
- `|W|=6`: gap `0.542341`
- `|W|=8`: gap `0.381966`

Thus the topological/conserved sector now has genuine dynamical consequences once the local energy is coupled to the admissible moves.

### Interpretation

This is not a derivation of electric charge or charge energy. It demonstrates a narrower structural result:

`local rule + conserved global sector -> emergent sector-dependent thermodynamics/dynamics`.

The strongest positive result is the exact quadratic dependence of the **mean** energy on `W`; the strongest caution is that the ground-state sector energy is not generically quadratic.

## Next proposed probe

**WHEELER-06 — Composite charge / additivity audit**

Question: if two independently defined oriented histories are combined into a composite admissible system, is the conserved signed invariant additive under composition and preserved under local pair creation/annihilation and binding transformations?

Target relation:

`Q(A ⊕ B) = Q(A) + Q(B)`.

Only after additivity is established should fractional-local/integer-global constructions be tested.
