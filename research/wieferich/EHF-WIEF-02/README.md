# EHF-WIEF-02 — Modular doubling: cycle elongation versus splitting

**Status:** exact finite computation + standard number-theoretic derivation; **not a new theorem or a Collatz result**.  
**Date:** 2026-11-13.  
**Scope:** doubling permutation `D_k(x) = 2x (mod p^k)` on every residue for odd primes `p`.

## Question

When a cyclic system's state space is refined from residues modulo `p` to `p²` and `p³`, must its cycles elongate, or can they split into multiple cycles of unchanged length?

## Exact structure

Let `d_r = ord_{p^r}(2)` and `d = d_1`. Each residue `x` has a `p`-adic valuation `j` (`0 <= j < k`) or is zero. Multiplication by 2 preserves valuation. In valuation layer `j`, every cycle has length `d_{k-j}`, and its number of cycles is

`c_{k-j} = φ(p^{k-j}) / d_{k-j} = (p-1) p^{k-j-1} / d_{k-j}`.

Zero is a fixed point. The **total number of cycles** in the full graph is

`N_k = 1 + Σ_{r=1}^k c_r`.

Let `s = v_p(2^d - 1)`. By the elementary lifting-the-exponent argument for odd primes,

`d_r = d * p^max(0, r-s)`.

Consequently the number of cycles in the unit layer modulo `p^r` is

`c_r = ((p-1)/d) * p^min(r-1,s-1)`.

- **Ordinary base-2 non-Wieferich primes (`s=1`):** a cycle over `p` lifts to one cycle `p` times as long over `p²`. The unit-layer cycle count stays fixed.
- **Wieferich primes with `s=2`:** a cycle over `p` lifts to `p` distinct cycles of the original length over `p²`; the next lift elongates each cycle by `p`. The unit-layer cycle count increases once and then stabilizes.
- **Higher-order Wieferich behaviour (`s>2`):** splitting persists until level `s`.

Equivalently, the return permutation on the `p` lifts over one original `d`-cycle is a single `p`-cycle (ordinary case) or the identity (Wieferich first lift).

## Computed results

| `p` | `d_1` | `d_2` | `d_3` | Unit cycles `c_1,c_2,c_3` | **All** cycles `N_1,N_2,N_3` |
|---:|---:|---:|---:|---:|---:|
| 3 | 2 | 6 | 18 | 1, 1, 1 | 2, 3, 4 |
| 5 | 4 | 20 | 100 | 1, 1, 1 | 2, 3, 4 |
| 7 | 3 | 21 | 147 | 2, 2, 2 | 3, 5, 7 |
| 11 | 10 | 110 | 1210 | 1, 1, 1 | 2, 3, 4 |
| **1093** | **364** | **364** | **397852** | **3, 3279, 3279** | **4, 3283, 6562** |
| **3511** | **1755** | **1755** | **6161805** | **2, 7022, 7022** | **3, 7025, 14047** |

**Important:** the unit cycle count is not the full cycle count. The full graph includes positive-valuation residues and fixed zero. For example, modulo `1093²` there are 3279 unit cycles of length 364, three cycles of nonzero multiples of 1093 (also length 364), and one fixed point: **3283 total**.

Both 1093 and 3511 have `s=2`, checked via `pow(2,d,p²) == 1` but `pow(2,d,p³) != 1`. The corresponding residues `(2^d-1)/p² (mod p)` are 891 and 1781, respectively.

## Validation

Run [probe.py](probe.py) using standard Python (no dependencies). It computes modular orders, derives the valuation-layer counts and **independently enumerates every orbit** for the small prime cubes and both large prime squares:

- `1093² = 1,194,649` states: full enumeration matches **3,283** predicted cycles.
- `3511² = 12,327,121` states: full enumeration matches **7,025** predicted cycles.
- The prime-cube counts for 1093 and 3511 use exact modular arithmetic and the proven valuation-layer formula, **not** exhaustive enumeration of 1.3 billion or 43 billion states.

## EHF interpretation and limitations

This provides a rigorous **control example** where refinement of a deterministic system has two distinct outcomes: lengthening and splitting. The number theory is already known; this probe does not demonstrate a novel EHF theorem or a physical effect.

For a comparable EHF growth system, first define admissible state spaces `X_k`, projections `π_k: X_{k+1} -> X_k`, and transformations satisfying `π_k F_{k+1} = F_k π_k`. Only then is it mathematically meaningful to classify the return-map permutation of the fibers over a base cycle and distinguish lengthening from splitting.

**Next falsifiable test:** build such equivariant refinement maps for RAW, alternating, or MICRO growth, if possible, and test which fiber return permutations their admissibility constraints permit. If no natural projections exist, report that limitation instead of forcing an analogy.

## Established sources

- Keith Conrad, *Wieferich Primes*: https://kconrad.math.uconn.edu/blurbs/ugradnumthy/wieferich-primes.pdf
- OEIS A305184, orders of 2 modulo Wieferich prime squares: https://oeis.org/A305184
- Wolfram MathWorld, *Wieferich Prime*: https://mathworld.wolfram.com/WieferichPrime.html
