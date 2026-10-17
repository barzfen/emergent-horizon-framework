# WHEELER-27 — Core-C Representation / Exact Gap Proof Audit

**Status: PROVED, assuming Core C is the undirected Hamilton-cycle 2-opt graph identified from the archived audits**

Let `m=n-1`. Anchor one vertex of an undirected Hamilton cycle of `K_n`. The remaining labels form a word in `S_m`, with a word identified with its full reversal because those are the two orientations of the same undirected cycle.

A Core-C 2-opt move is exactly a contiguous substring reversal of the anchored word. Before quotienting by orientation, the covering graph is therefore the standard substring-reversal graph `R_m`. Full-word reversal changes only orientation, so it becomes the identity in the quotient and is omitted as a loop.

Hence

`d_C = binom(m,2)-1 = n(n-3)/2`.

Chung and Tobin proved for the substring-reversal graph `R_m` that

`mu_1(R_m)=binom(m,2)`

and

`mu_2(R_m)=binom(m,2)-m`,

so its adjacency/Laplacian gap is exactly `m`.

Reference: Fan Chung and Josh Tobin, *The Spectral Gap of Graphs Arising From Substring Reversals*, Electronic Journal of Combinatorics 23(3), 2017, Theorem 1.

On the orientation-invariant quotient, the full-reversal operator acts as `+1`. Removing that loop changes the lifted adjacency operator from `A_R` to `A_R-I`; therefore all surviving adjacency eigenvalues shift by `-1`, while spectral differences are unchanged.

Since the quotient spectrum is contained in the covering spectrum,

`mu_2(C_n) <= binom(m,2)-m-1 = d_C-m`.

WHEELER-26 already identified an exact Core-C eigenmode with adjacency eigenvalue

`mu = d_C-m`.

Therefore both bounds coincide:

`mu_2(C_n)=d_C-m`.

Thus

`lambda_gap(C_n)=m=n-1`.

Exact formulas:

- `|V|=(n-1)!/2`
- `d_n=n(n-3)/2`
- `mu_2=d_n-(n-1)=(n^2-5n+2)/2`
- `lambda_Lap,1=n-1`

For `n=12`:

- `|V|=19,958,400`
- `d=54`
- `mu_2=43`
- `lambda_gap=11`

So the WHEELER-26 prediction is proved without constructing the full matrix.

The normalized Laplacian gap is

`gamma_n=(n-1)/d_n = 2(n-1)/(n(n-3)) ~ 2/n`,

so Core C is not a standard normalized expander family.

## Verdict

- **PROVED:** `d_n=n(n-3)/2`.
- **PROVED:** `mu_2=d_n-(n-1)`.
- **PROVED:** `lambda_gap=n-1`.
- **PROVED:** for `n=12`, `(d,mu_2,lambda_gap)=(54,43,11)`.
- **NEGATIVE:** normalized gap tends to zero like `2/n`.

## Next probe

**WHEELER-28 — Rate Normalization / Continuum-Limit Audit**

Compare unnormalized dynamics, fixed-total-rate degree normalization, and any independently motivated growth/observer-time normalization before drawing physical conclusions from the gap.