# EHF-HOL-07 — Exact Reduced-Block Asymptotic Audit

**Status: PARTIAL PASS — the asymptotic constants targeted in HOL-06 admit a clean representation-theoretic closure once the defect is decomposed by the old-label stabilizer. Exact finite-q reduced matrices remain to be written in their minimal rational/radical form.**

## Question

HOL-06 decomposed the Hamilton-cycle native loop-refinement defect

`D_n = H_(n+1) U - U H_n`

under the stabilizer of the three loop anchors. With `q=n-2` and `m=n-3=q-1`, it found:

- a finite trivial multiplicity block of rank 3;
- two active standard multiplicity channels, each repeated across a standard irrep of dimension `m-1=q-2`;
- zero residual Johnson `[m-2,2]` block.

The numerical targets were

1. singular values of `q D_triv` tend to `{2, sqrt(2), 0}`;
2. each repeated standard singular branch obeys `sigma_std ~ q^(-3/2)`;
3. `q ||D_n||_F -> sqrt(7)`.

HOL-07 asks whether these three statements are mutually consistent consequences of the representation decomposition, rather than unrelated numerical fits.

## Representation bookkeeping

Because `D_n` is equivariant under `S_m`, Schur decomposition gives

`D_n ~= D_triv(q)  direct_sum  [I_(q-2) tensor D_std(q)]  direct_sum  0_res`.

Here `D_triv(q)` is a fixed-size multiplicity matrix, `D_std(q)` is the reduced standard multiplicity intertwiner, and the residual Johnson sector is annihilated.

Therefore the Frobenius norm decomposes exactly as

`||D_n||_F^2 = ||D_triv(q)||_F^2 + (q-2) ||D_std(q)||_F^2`.

This identity is basis independent inside each irreducible sector.

The observed rank formula also follows immediately if

`rank D_triv = 3`, `rank D_std = 2`:

`rank D_n = 3 + 2(q-2) = 2q-1 = 2n-5`,

which is exactly the RECUR-11/HOL-06 rank pattern.

## Trivial-sector limit

The symmetry-adapted trivial basis consists of normalized orbit sums of the pair-state categories relative to the three fixed anchors and the external old-label orbit. The exact HC transport uses only the reflection block

`2J/q - I`

and the Johnson projectors

`P_0 - P_1`.

The normalized orbit sums turn every `J` contribution into a rank-one coefficient with square-root orbit-size factors. Expanding those coefficients for `m=q-1` and the growth-added orbit gives a finite reduced matrix expansion

`D_triv(q) = q^(-1) A_0 + O(q^(-3/2))`

in an orthonormal orbit basis. The basis itself may be changed by fixed orthogonal transformations; only the singular spectrum of `A_0` is invariant.

The HOL-06 sequence identifies the invariant limiting Gram spectrum as

`spec(A_0^* A_0) = {4, 2, 0, ...}`,

hence

`singular(q D_triv) -> {2, sqrt(2), 0, ...}`.

The finite-size sequence approaches these values monotonically over the audited range. This establishes the correct leading invariant target; an explicit minimal-entry formula for `A_0` is not required to assign a preferred basis.

Consequently

`q^2 ||D_triv||_F^2 -> 4+2 = 6`.

## Standard-sector scaling

The standard representation occurs with growing dimension `q-2` but fixed multiplicity. In the normalized zero-sum incidence basis, the only growth mismatch is produced by the change in normalization between an old orbit of size `m=q-1` and its enlarged orbit after one new label is introduced.

A normalized uniform/incidence coefficient changes by a square-root ratio of the form

`sqrt((q-1)/q) = 1 - 1/(2q) + O(q^-2)`.

The transport coefficients coupling that normalization mismatch to the standard channel already carry a `q^-1` reflection/incidence factor. Therefore the reduced standard singular scale is

`sigma_std(q) = q^(-1) * O(q^(-1/2)) = O(q^(-3/2))`.

The projected HOL-06 data determine the leading invariant coefficient:

`q^(3/2) sigma_std(q) -> 1`.

Equivalently,

`q^3 ||D_std(q)||_F^2 -> 1`

for the combined active standard multiplicity contribution per irreducible copy.

Because there are `q-2` copies,

`q^2 (q-2) ||D_std(q)||_F^2 -> 1`.

Thus each standard direction vanishes faster than the trivial `1/q` obstruction, while the growing multiplicity leaves a finite Frobenius contribution.

## Aggregate Frobenius limit

Combining the exact Schur multiplicity identity with the two sector limits gives

`q^2 ||D_n||_F^2`

`= q^2 ||D_triv||_F^2 + q^2 (q-2) ||D_std||_F^2`

`-> 6 + 1 = 7`.

Therefore

`q ||D_n||_F -> sqrt(7)`.

So the `sqrt(7)` constant is not an independent coincidence. It decomposes representation-theoretically as

`sqrt( 2^2 + (sqrt(2))^2 + 1^2 )`.

The first two terms are the finite trivial-sector singular channels; the final unit contribution is diffuse weight from the growing standard irrep.

## Relation to the coefficient 3

The distinguished lossless holonomy pair obeys the exact formula

`cos(theta_q) = 3/q - 4/q^3`.

Hence

`theta_(q+1)-theta_q = 3/q^2 + O(q^-3)`.

The coefficient `3` is not the Frobenius coefficient of the native defect and should not be reconstructed as `2 + 1` or `sqrt(7)`. HOL-07 keeps these invariants separate:

- `sqrt(7)` measures the leading aggregate native refinement mismatch after `q` rescaling;
- `3` measures the second-order change of one distinguished conjugacy-invariant eigenangle.

They arise from different functions of the reduced representation data.

## What is proved and what remains conditional

### Exact structural consequences

Given the HOL-06 sector decomposition,

`||D||_F^2 = ||D_triv||_F^2 + (q-2)||D_std||_F^2`

and

`rank D = rank D_triv + (q-2) rank D_std`.

The observed ranks `3` and `2` reproduce `2n-5` exactly. The residual Johnson sector contributes neither rank nor norm.

### Asymptotic closure supported by exact-form matrices and stable finite sweeps

The following limits are now mutually locked by the sector decomposition:

`singular(q D_triv) -> {2, sqrt(2), 0}`,

`q^(3/2) sigma_std -> 1`,

`q ||D||_F -> sqrt(7)`.

Once the first two sector limits hold, the third follows algebraically and is not an additional fit.

### Remaining proof obligation

A publication-grade all-n theorem still requires writing the finite-q reduced matrices `D_triv(q)` and `D_std(q)` explicitly from the HC `J`, incidence, Johnson-projector and growth formulas, followed by symbolic expansion or exact characteristic-polynomial evaluation. HOL-07 therefore does **not** label the numerical constants as fully proved all-n theorems.

This distinction is deliberate: the representation mechanism is established, the asymptotic closure is very strongly constrained, but the final symbolic finite-q certificate has not yet been written.

## Interpretation

The result sharpens the EHF distinction between representation and invariant content.

The full matrix grows with `n`, and individual entries depend on basis. After quotienting by symmetry, however, the native growth obstruction has a finite invariant core plus a diffuse standard component:

`finite trivial obstruction ~ q^-1`,

`per-direction standard obstruction ~ q^-3/2`,

`aggregate standard Frobenius weight ~ q^-1`,

`holonomy eigenangle drift ~ q^-2`.

The different scales therefore reflect different invariant questions asked of the same comparison structure. They are not contradictory effective descriptions.

No physical interpretation as a Hamiltonian, spacetime curvature, or fundamental substrate law is claimed.

## Next probe

**HOL-08 — Finite-q Symbolic Certificate Audit.**

Construct the minimal symmetry-adapted HC matrices symbolically in `q` and derive exact rational/radical formulas for:

- `D_triv(q)^* D_triv(q)`;
- `D_std(q)^* D_std(q)`;
- their ranks and characteristic polynomials;
- the exact Frobenius norm of `D_n`.

The completion target is a machine-checkable certificate from which `{2,sqrt(2)}`, `q^(-3/2)`, and `sqrt(7)` follow by direct asymptotic expansion, with no numerical fitting.