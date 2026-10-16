# WHEELER-13 — Composite Spectrum / Proton–Electron Relation Audit

**Status: PARTIAL PASS for integer composite sectors; NEGATIVE for deriving the proton's specific quark-charge decomposition**

## Setup

Use the `m=3` observer quotient selected in the preceding probes. Represent the nonzero local conjugate classes by signed fractional units

`q_local in {+1/3, -1/3}`

with `0` as the neutral class. Complete composites obey the closure condition that the total residue vanish mod 3, equivalently the sum of signed numerator units is divisible by 3.

## Minimal closed composites

For a single nonzero constituent, closure is impossible.

For two constituents, the only nonzero closed combination is the conjugate pair

`(+1/3) + (-1/3) = 0`,

so the minimal two-body closed composite is neutral.

For three constituents, two new closed sectors appear:

`(+1/3)+(+1/3)+(+1/3)=+1`,

and by conjugation

`(-1/3)+(-1/3)+(-1/3)=-1`.

Thus the first non-neutral complete composites occur at three constituents and form an exactly opposite pair `Q=+1` and `Q=-1`.

A finite enumeration with local symbols `{-1,0,+1}` in units of `1/3` confirms:

- length 1 closed totals: `{0}`;
- length 2 closed totals: `{0}`;
- length 3 closed totals: `{-1,0,+1}`;
- lengths 4 and 5 still contain integer totals only.

This is a direct consequence of `Z_3` closure rather than a particle-specific assignment.

## Proton/electron comparison

This structure reproduces a weaker relation:

- a minimal non-neutral three-constituent composite can carry `+1`;
- its conjugate carries exactly `-1`.

Therefore equal-magnitude opposite integer sectors arise automatically from conjugation.

However, the actual Standard Model proton decomposition

`(+2/3)+(+2/3)+(-1/3)=+1`

is **not** derived by the quotient alone.

At the level of `Z_3`,

`+2/3 ≡ -1/3 (mod 1)`.

So `+2/3` and `-1/3` occupy the same residue class once integer lifts are forgotten. The quotient therefore cannot distinguish an up-type constituent from a down-type constituent using charge alone. Recovering the proton's `uud` charge pattern would require additional structure that selects different integer lifts or introduces another internal label.

Likewise, an elementary electron with charge `-1` is not identified by the present construction. The model only guarantees the existence of a conjugate integer sector, not that its representative is elementary rather than composite.

## Interpretation

**Positive result:**

`Z_3` closure plus additivity forces the first non-neutral complete composite to appear at three constituents, with conjugate totals `+1` and `-1`.

This gives a clean mechanism for exact equal-and-opposite composite charge sectors.

**Negative result:**

The Wheeler branch does not yet derive the Standard Model assignments `+2/3`, `-1/3`, or the proton/electron particle identities. Those require extra structure beyond the finite cyclic charge quotient.

## Next question

A useful next probe would ask whether an independent internal degree of freedom can distinguish integer lifts of the same `Z_3` residue without inserting quark charge values by hand. One candidate is to test whether Hamilton-history orientation, growth class, or another EHF equivalence label naturally splits a single residue class into two dynamically inequivalent lifts.