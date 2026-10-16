# WHEELER-14 — Lift Splitting / Internal-Label Audit

**Status: NEGATIVE for unique quark-like splitting; PASS for existence of distinct integer lifts**

## Question

Can an existing EHF structure split a single observer-level `Z_3` residue into distinct underlying states whose integer lifts differ by one whole unit of normalized charge, without inserting the desired values by hand?

## Microscopic lift structure

Let the microscopic conserved crossing/current count be an integer `c`, and let the observer retain only

`r = c mod 3`.

Then every observer residue has an infinite family of microscopic lifts

`c = r + 3k`,  `k in Z`.

If normalized by three, the observer-compatible charge-like values are

`q = c/3 = r/3 + k`.

Thus values that differ by an integer can share the same `Z_3` residue. In particular,

`+2/3` corresponds to `c=2`,

while

`-1/3` corresponds to `c=-1`,

and both satisfy

`c = 2 mod 3`.

So the quotient does not erase the possibility that two microscopically distinct states project to the same residue.

## Tests of candidate EHF labels

### Orientation reversal

Reversal sends

`c -> -c`.

Therefore

`2 -> -2`,

and

`-1 -> +1`.

So reversal pairs `+2/3` with `-2/3`, and `-1/3` with `+1/3`; it does **not** naturally pair or distinguish `+2/3` and `-1/3` as two members of one internal doublet.

### Minimal local cost

For any monotone cost depending only on magnitude, for example

`E(c)=|c|^p` with `p>0`,

the residue class `r=2` prefers the lift `c=-1` over `c=2` because

`|-1| < |2|`.

Thus simple local economy does not stabilize both candidate lifts. It collapses the class to the nearest-to-zero representative.

### Growth-depth label

A residue-preserving lift change must have the form

`c -> c + 3 ell`.

Therefore a growth process that inserts a neutral triplet can move between lifts without changing `r`.

This supplies a natural *history label* `k`, but by itself it does not make two neighboring lifts distinct stable species. If growth is reversible, the lifts are connected; if growth is irreversible, the distinction is historical rather than an internal conserved quantum number.

### Parity / Hamilton-position labels

A binary parity or Hamilton-position label could be attached to different lifts, but no currently established EHF rule forces a unique correspondence

`label A -> c=2`,

`label B -> c=-1`.

Choosing such an assignment would be hand-tuning.

## Verdict

The EHF Wheeler construction naturally permits **multiple microscopic integer lifts of one finite observer residue**. This is a genuine structural result:

`microscopic integer current -> finite observer quotient + hidden lift index`.

However, the existing EHF ingredients do not yet derive a uniquely selected stable pair corresponding to `+2/3` and `-1/3`.

The specific quark-like split therefore **fails the no-hand-tuning test at WHEELER-14**.

This is an important boundary on the current programme: `Z_3` fractionalization plus integer lifts is mathematically compatible with quark-like charges, but compatibility is not derivation.

## Next useful direction

A stronger future probe should ask whether the lift index `k` can become a genuine superselection or dynamically protected label through growth topology, observer memory, or another independently derived EHF invariant. Only then would distinct lifts of one residue behave like separate particle species rather than alternative representatives of the same quotient class.
