# WHEELER-25 — Kinetic Geometry / Expander Audit

**Status: PROMISING / CONJECTURAL; existing Core-C/RAF data is compatible with strong expander-like scaling, but only two audited sizes are currently available**

## Question

WHEELER-24 showed that the MICRO boundary-pair mechanism remains gapless because its mobile excitation graph behaves like a one-dimensional cycle, with Laplacian gap scaling as `n^-2`.

The natural next question is whether another already-existing EHF state graph has a fundamentally different kinetic geometry: one whose connectivity grows sufficiently strongly that the normalized spectral gap remains bounded away from zero as system size increases.

The existing Core-C/RAF audits are the strongest current candidate.

## Existing audited data

For Core C, prior audits gave:

| n | V | degree d | second adjacency eigenvalue λ2 | adjacency gap d-λ2 |
|---:|---:|---:|---:|---:|
| 8 | 2,520 | 20 | 7 | 13 |
| 10 | 181,440 | 35 | 9 | 26 |

These two points fit the simple laws

`d_n = n(n-3)/2`

and

`λ2(n) = n-1`.

Therefore the adjacency gap would be

`g_n = d_n - λ2(n) = (n^2 - 5n + 2)/2`.

This is only an interpolation from two exact audited sizes, not yet a theorem.

## Normalized gap

For a d-regular graph, a useful expansion diagnostic is

`γ_n = 1 - λ2/d = (d-λ2)/d`.

The audited values are:

- `n=8`: `γ = 13/20 = 0.65`;
- `n=10`: `γ = 26/35 ≈ 0.742857`.

Under the conjectured laws,

`γ_n = 1 - 2(n-1)/(n(n-3))`,

so

`γ_n -> 1` as `n -> infinity`.

That would be much stronger than merely retaining a nonzero normalized gap: the second adjacency eigenvalue would grow only linearly while the degree grows quadratically.

## Predicted values if the pattern continues

These are predictions, not audited facts:

| n | predicted d | predicted λ2 | predicted gap | predicted normalized gap |
|---:|---:|---:|---:|---:|
| 12 | 54 | 11 | 43 | 0.796296 |
| 14 | 77 | 13 | 64 | 0.831169 |
| 16 | 104 | 15 | 89 | 0.855769 |

The contrast with the WHEELER-23 mobile-boundary graph is sharp:

- boundary graph: `λ1 ~ 4π²/n² -> 0`;
- Core-C conjecture: normalized gap remains O(1) and may approach 1.

## Important qualification: degree growth

Core C is not a bounded-degree expander family if `d_n ~ n²`.

Therefore the mathematically precise statement is not currently “Core C is an expander family” in the standard bounded-degree sense.

What the data suggests is **expander-like kinetic geometry after degree normalization**: the random-walk spectral gap may remain large even as the graph degree increases.

For the normalized Laplacian,

`L_norm = I - A/d`,

the first nonzero eigenvalue is

`μ1 = 1 - λ2/d = γ_n`.

Thus the conjectured law would imply a size-stable or improving normalized mixing gap.

## Why this matters for the mass-gap discussion

This does not solve a physical mass-gap problem. However, it establishes a mechanism that the MICRO boundary model lacked:

`local primitive moves -> highly connected global state graph -> no diffusive one-dimensional soft mode`.

A graph with a normalized spectral gap bounded away from zero can mix in O(log |V|) steps up to constants in appropriate random-walk models, rather than diffusing over distances with `n²` relaxation.

The structural lesson is that the existence or absence of a low mode can be controlled by **kinetic geometry**, not just by static defect energy.

This is directly relevant to EHF because admissible comparison is the chosen primitive data of the framework: changing the admissible-comparison graph changes the emergent kinetic geometry.

## Verdict

- **PASS:** existing Core-C data is qualitatively incompatible with the `n^-2` one-dimensional diffusion seen in WHEELER-23.
- **PASS:** normalized gaps at `n=8,10` are already large: 0.65 and approximately 0.743.
- **PROMISING:** the two audited points fit `d=n(n-3)/2`, `λ2=n-1`, implying normalized gap tending to 1.
- **NOT PROVED:** two sizes are insufficient to establish the scaling law.
- **NOT a standard bounded-degree expander claim:** degree appears to grow approximately quadratically.
- **NOT a Yang-Mills mass-gap result:** this is a discrete state-graph spectral phenomenon.

## Next probe

**WHEELER-26 — Core-C Spectral Law / n=12 Validation Audit**

Priority:

1. Reconstruct the exact Core-C graph definition from the canonical EHF branch.
2. Compute or derive `d`, `λ2`, gap multiplicity, and normalized gap for `n=12` if computationally feasible.
3. Test the conjectures `d=n(n-3)/2` and `λ2=n-1`.
4. If direct diagonalization is too large, exploit symmetry, quotienting, representation structure, or sparse eigensolvers.
5. Determine whether a proof route exists from the move generators rather than continued numerical fitting.

A correct `n=12` result is the critical next discriminator. If it gives `(d,λ2)=(54,11)`, the conjecture becomes substantially more credible; if not, the apparent scaling law should be discarded immediately.
