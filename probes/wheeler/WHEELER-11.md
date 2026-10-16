# WHEELER-11 — Derive the move rule from EHF primitives

**Status: PARTIAL PASS**

## Question
Can the unit nearest-neighbour residue-transfer rule used in WHEELER-09/10 be derived from existing EHF primitives rather than chosen as a convenient dynamics?

## EHF ingredients used
- oriented histories / signed crossings;
- local reversal as an elementary move;
- Hamilton-history closure;
- growth by local insertion;
- observer coarse-graining into adjacent cells;
- residue labels obtained by quotienting a coarse signed crossing count modulo `m`.

## Coarse variables
Let `c_i` be the signed crossing count associated with coarse cell/boundary `i`, and define the observer-level residue

`r_i = c_i mod m`.

A single elementary local reversal has support on a finite segment. Interior crossing changes cancel in opposite-sign pairs. Only the two coarse boundaries of the reversed segment carry uncancelled changes.

With a consistent orientation convention, one boundary gains one signed crossing and the adjacent boundary loses one:

`c_i -> c_i + 1`

`c_{i+1} -> c_{i+1} - 1`.

Therefore after quotienting modulo `m`:

`(r_i, r_{i+1}) -> (r_i + 1, r_{i+1} - 1) mod m`.

This is exactly the unit nearest-neighbour residue-transfer rule used in WHEELER-09/10.

## Why total charge-like residue is conserved
The local change is a discrete divergence:

`Delta r = (+1, -1)`.

Hence

`sum_i Delta r_i = 0 mod m`.

For a closed Hamilton history the total residue is therefore invariant under elementary reversals. This is the discrete analogue of an internal current with no source/sink.

## Role of growth
If growth inserts a locally neutral pair or a subdivision whose new internal boundary contributions cancel, then the total residue is unchanged. Growth may change the number of coarse cells while preserving the same global residue sector.

This is an admissibility condition, not yet a theorem about every possible EHF growth rule: growth operations that introduce unmatched boundary contributions would act as explicit sources/sinks and would change the sector.

## Unit step versus larger steps
A single elementary reversal changes the boundary count by one unit. Multi-unit transfers arise only by composing elementary reversals. Thus the primitive connected dynamics has generator step `k=1`.

This matters because WHEELER-10 found that arbitrary step sizes can fragment `Z_m` when `gcd(k,m)>1`; deriving `k=1` from the elementary reversal removes that arbitrary freedom in the minimal model.

## Consequence for threefold selection
Combining this derivation with WHEELER-08/09/10 gives the current chain:

1. reversal provides a conjugation `r -> -r`;
2. the smallest cyclic structure with neutral plus one distinct conjugate pair is `Z_3`;
3. elementary reversal induces the connected unit-transfer rule;
4. for that rule, `m=3` has the largest spectral gap among `m>=3`;
5. broad monotone local repair costs also make `m=3` the cheapest admissible member.

So the earlier unit-transfer dynamics is no longer merely an arbitrary modelling choice.

## Limitation
The derivation depends on the chosen coarse variable — signed boundary-crossing count modulo `m` — and on treating local reversal as the elementary move. EHF has not yet shown that this quotient is uniquely forced, nor that every admissible observer coarse-graining must produce the same residue dynamics.

Therefore this is a **partial pass**, not a derivation of quark charge or the Standard Model `Z_3` structure.

## Next probe

**WHEELER-12 — Quotient uniqueness / observer-independence audit**

Test whether alternative natural observer coarse-grainings of the same reversal histories produce equivalent conserved residue dynamics, or whether the `Z_m` quotient used here is just one convenient representation. A robust result would require the charge-like invariant to survive admissible changes of coarse-graining.