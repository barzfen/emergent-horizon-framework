# EHF-HOL-06 — Representation-Sector Generator Audit

**Status: PASS FOR SECTOR SEPARATION / PARTIAL ANALYTIC LIMIT — the `1/q` native refinement obstruction is carried by low symmetry sectors, while the distinguished holonomy-angle drift remains `1/q^2`. A universal cross-substrate generator is not established.**

## Motivation

HOL-05 found two scales for the native loop-refinement defect

`D_n = H_N U - U H_n`:

- `||D_n||_F = O(1/q)` numerically, with `q=n-2`;
- the distinguished nonreal holonomy angle changes only as `Delta theta_q = O(1/q^2)`, with `q^2 Delta theta_q -> 3`.

HOL-06 asks whether this is explained by symmetry sectors rather than by a single full-space generator.

## Exact representation coordinates

RECUR-08 already gives the required decomposition. For a transport between two anchors, the remaining labels form a permutation module. The reflection block

`W_X = 2 J_q/q - I_q`

splits into a one-dimensional trivial representation and a standard zero-sum representation. For Hamilton-cycle pair observers the second block lies in the Johnson scheme `J(q,2)` with

`W_Y = P_triv - P_std`,

and the remaining Johnson irrep is kernel.

The native growth maps are equivariant under permutations of labels that remain old. Consequently `D_n` is an intertwiner for the corresponding old-label stabilizer. Schur decomposition therefore block-diagonalizes the defect by irreducible representation type; arbitrary basis choices inside multiplicity spaces cannot change the block singular values or ranks.

## Perfect-matching control: exact low-sector localization

Fix loop anchors `(0,1,2)` and let the external old labels be permuted by `S_(n-3)`. The old observer space decomposes as

`trivial multiplicity 3  +  standard multiplicity 1`.

A convenient orthonormal trivial basis is

- `e_1`,
- `e_2`,
- the uniform vector on old external labels.

After growth `n -> n+2`, the target trivial sector additionally contains the symmetric uniform vector on the two new labels. Their antisymmetric combination is a separate one-dimensional representation of the new-label swap.

The native loop defect has rank exactly `2` in the audited RECUR-11 family. For `n` beyond the small exceptional dimensions, equivariance plus this rank excludes a nonzero standard block: a nonzero standard intertwiner would contribute rank at least `n-4`. Direct projection confirms that the external zero-sum sector is annihilated. The defect therefore localizes entirely in a finite trivial multiplicity space.

Expanding the exact reflection and normalized growth formulas in this symmetry-adapted basis gives the leading reduced action

`q D_n e_2 -> -2 sqrt(2) u_new`,

where `u_new` is the normalized symmetric vector on the two growth-added labels. All other entries of the reduced `qD_n` matrix vanish at leading order.

Hence the leading PM generator is rank one and

`||q D_n||_op -> 2 sqrt(2)`.

The second singular branch is subleading; numerically it is consistent with `O(q^-2)` before the `q` rescaling.

Representative full calculations:

| old n | q | q ||D||_F | leading singular values of qD |
|---:|---:|---:|---|
| 10 | 8 | 3.06985 | 2.96783, 0.78486 |
| 22 | 20 | 2.91645 | 2.89384, 0.36240 |
| 50 | 48 | 2.86152 | 2.85705, 0.15990 |

These approach the rank-one value `2 sqrt(2) = 2.828427...`.

## Hamilton-cycle control: trivial, standard and residual sectors

For HC growth `n -> n+1`, let `m=n-3` external old labels remain after fixing the three loop anchors. Pair states under `S_m` decompose into:

- a trivial multiplicity sector, represented by uniform combinations of `{1,2}`, `{1,r}`, `{2,r}`, and `{r,s}` categories;
- standard zero-sum sectors carried by the one-external-label incidence channels;
- the residual Johnson `[m-2,2]` sector.

The observed loop-defect rank is

`2n-5 = 2m+1`.

Projection into the symmetry-adapted blocks gives the decomposition

- trivial reduced block: rank `3`;
- standard isotypic block: two active multiplicity channels, contributing `2(m-1)` rank;
- residual Johnson block: zero.

The rank sum is therefore

`3 + 2(m-1) = 2m+1 = 2n-5`,

matching the native defect exactly.

### Trivial block

The singular values of the reduced trivial block after multiplication by `q=n-2` approach

`2, sqrt(2), 0, ...`.

Examples:

| old n | singular values of q D_triv |
|---:|---|
| 20 | 2.12354, 1.45128, 0.27160 |
| 35 | 2.06946, 1.43499, 0.17207 |
| 50 | 2.04829, 1.42864, 0.13188 |

Thus the leading finite-dimensional HC obstruction also lives in the trivial multiplicity sector, but its limiting singular spectrum differs from PM:

`{2, sqrt(2)}` rather than `{2 sqrt(2)}`.

This already rules out a single universal reduced generator shared unchanged by the two substrates.

### Standard block

A second effect is distributed across the growing standard multiplicity space. The repeated standard singular branch satisfies numerically

`q sigma_std ~ 1/sqrt(q)`.

For example `sqrt(q) q sigma_std` is

`0.9705, 0.9771, 0.9814, 0.9843, 0.9880, 0.9903`

for `q=15,20,25,30,40,50`.

Thus each standard direction becomes negligible in operator norm faster than `1/q`, but there are `O(q)` such directions. Their aggregate Frobenius contribution to `qD_n` remains finite. This explains why the full Frobenius-scaled defect can retain weight that is absent from the finite trivial quotient.

The HC data are consistent with

`||qD_n||_F -> sqrt(7)`,

because the limiting squared contributions are `4 + 2` from the two trivial singular values plus `1` from the diffuse standard family. This `sqrt(7)` value is currently an asymptotic conjecture supported by the sector numerics, not yet an all-n symbolic theorem.

## Where the `1/q^2` angle lives

The exact nonreal loop pair obeys

`cos(theta_q) = 3/q - 4/q^3`.

Therefore

`theta_(q+1)-theta_q = 3/q^2 + O(q^-3)`.

HOL-06 shows why this does not set the scale of the whole defect. The native growth obstruction has first-order `1/q` components in low symmetry/multiplicity sectors. The complex rotation pair is a distinguished lossless spectral sector whose eigenangle changes only at second order.

So the two-scale structure is real:

`native representation rearrangement = first order in 1/q`,

`distinguished holonomy-angle drift = second order in 1/q`.

## Invariant content

This audit does not attach meaning to individual coordinates inside degenerate representations. The robust statements are:

- irreducible sector type;
- block rank;
- singular values of reduced multiplicity intertwiners;
- multiplicity growth;
- the exact conjugacy-invariant holonomy angle.

This is precisely the distinction between representation and invariant structure required by the EHF programme.

## Classification

**HOL-06 passes the sector-separation gate.**

It explains the coexistence of the HOL-05 `1/q` full defect and the exact `1/q^2` angular drift. It also produces a controlled nonzero finite-dimensional `q`-scaled limit in the PM trivial sector and strong asymptotic evidence for the corresponding HC trivial-sector limit.

It does **not** establish one substrate-independent generator. HC and PM have different leading reduced singular spectra. The common feature is structural: the leading obstruction is symmetry-localized and low-sector, while the distinguished holonomy rotation evolves more slowly.

## Theorem-status boundary

Established from exact symmetry formulas plus direct block projection:

- `D_n` is equivariant under the old-label stabilizer;
- PM defect localizes to the finite trivial multiplicity sector in the audited family;
- HC residual Johnson sector is inactive in the projected audits;
- HC defect rank is exhausted by a rank-3 trivial block plus two standard multiplicity channels;
- the `1/q^2` rotation-angle law follows exactly from the known cosine formula.

Analytic/asymptotic result from expansion of the exact PM reduced formulas:

- `q D_n e_2 -> -2 sqrt(2) u_new` and therefore the leading PM singular value tends to `2 sqrt(2)`.

Strong numerical asymptotic evidence, still requiring symbolic all-n closure:

- HC trivial singular limits `{2, sqrt(2), 0}`;
- `sqrt(q) q sigma_std -> 1` for the repeated HC standard branch;
- `q ||D_n||_F -> sqrt(7)` for HC.

No claim is made that these generators are Hamiltonians, curvature tensors, physical time generators, or universal substrate laws.

## Next probe

**HOL-07 — Exact Reduced-Block Formula Audit.**

Derive closed all-n formulas for the HC trivial and standard multiplicity blocks directly from the `J`, incidence, Johnson-projector and growth expressions. The targets are to prove or falsify

- HC trivial `qD` singular limits `{2, sqrt(2)}`;
- HC repeated standard law `sigma_std ~ q^(-3/2)`;
- aggregate `q ||D||_F -> sqrt(7)`;
- the precise relation, if any, between the subleading reduced block and the exact coefficient `3` in `q^2 Delta theta -> 3`.

That would convert the remaining HOL-06 asymptotics from numerical sector evidence into an all-n representation-theoretic theorem.