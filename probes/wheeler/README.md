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

## WHEELER-06 — Composite charge / additivity audit

**Status: PROVED for the current signed-orientation invariant; computationally stress-tested**

Let an oriented subsystem `A` have invariant

`Q(A) = sum_i s_i`, with `s_i in {-1,+1}`,

and similarly for subsystem `B`.

For the composite obtained by disjoint union or concatenation without relabelling orientations,

`Q(A ⊕ B) = Q(A) + Q(B)`.

This is immediate from finite additivity of the signed sum. In the periodic-time formulation the corresponding topological statement is that winding/degree is additive under concatenation of loops:

`deg(A * B) = deg(A) + deg(B)`.

### Binding and pair annihilation

Allow local binding/rearrangement moves that only permute orientation labels, and local creation/annihilation of balanced pairs

`(+,-) <-> empty`

or

`(-,+) <-> empty`.

Each such move changes the local particle count but contributes net zero to `Q`, so total `Q` is preserved.

Therefore composites can neutralize internally while retaining the correct net invariant. Examples:

- `Q=+1` combined with `Q=-1` gives a neutral composite `Q=0`;
- `Q=+1` combined with `Q=+1` gives `Q=+2`;
- any number of locally created `(+,-)` pairs leaves the composite total unchanged.

### Stress test

50,000 random pairs of finite orientation words were generated. For each pair, the concatenated composite satisfied

`Q(A ⊕ B) = Q(A) + Q(B)`.

Random adjacent opposite-orientation annihilations were then applied repeatedly. Violations of total-`Q` conservation: `0`.

### Interpretation

Additivity is not an emergent surprise here; it is built into the algebraic/topological definition of the invariant. The useful result is narrower: the current EHF Wheeler invariant has the minimum composition property required of a charge-like conserved quantity and remains conserved under pair-changing local moves.

This does **not** identify `Q` with electric charge. A nontrivial next step is to determine whether fractional local contributions can arise from an observer/coarse-graining map while complete admissible composites remain integer-valued, without inserting Standard Model fractions by hand.

## WHEELER-07 — Fractional local / integer global audit

**Status: PASS for generic fractionalization, NEGATIVE for unique thirds selection**

To avoid inserting Standard Model fractions by hand, consider the generic cyclic symmetry class `Z_m`. A local sector is labelled by a residue `r in {0,1,...,m-1}` and is assigned the observer-projected rational contribution

`q_local = r/m`.

A complete admissible composite must satisfy the closure/integrality condition

`sum_a r_a = 0 mod m`.

Then automatically

`Q_total = sum_a r_a/m`

is an integer for every admissible complete composite.

This produces locally fractional but globally integer charge-like values from symmetry/closure alone. Examples include:

- `m=2`: half-units locally, integer totals globally;
- `m=3`: thirds locally, including `1/3` and `2/3`, integer totals globally;
- `m=4`: quarter-units locally;
- and analogously for arbitrary `m`.

### Exhaustive finite check

For `m = 2,3,...,8`, all residue strings up to length 5 satisfying the closure condition `sum r = 0 mod m` were enumerated. Every admissible complete composite had integer `Q_total`; no violations were found.

### Key negative result

The current Wheeler/Hamilton-history structure does **not** select `m=3` over `m=2,4,5,...`.

Therefore the appearance of `1/3` and `2/3` in the `m=3` case is not yet an explanation of quark-like fractional electric charge. Fractionalization is generic once a `Z_m` quotient/closure structure is supplied.

This is an important anti-overfitting result: the framework can accommodate thirds, but does not derive why nature would choose threefold fractionalization.

### Interpretation

The retained structural result is:

`finite cyclic symmetry + local residue labels + global closure -> rational local contributions + integer complete-composite invariant`.

The unresolved question is what, if anything, could force a threefold structure from deeper admissibility/dynamics rather than stipulating `Z_3`.

## Next proposed probe

**WHEELER-08 — Threefold selection / no-hand-tuning audit**

Question: can the existing EHF ingredients (orientation, Hamilton-history closure, local reversals, growth, parity, observer equivalence, or admissibility) select a minimal nontrivial threefold quotient or orbit structure, while excluding equally natural `Z_2`, `Z_4`, etc. constructions?

Failure criterion: if `m=3` must simply be chosen as an input, then EHF has not explained thirds; it has only represented them.