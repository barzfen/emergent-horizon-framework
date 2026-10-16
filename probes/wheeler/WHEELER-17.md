# WHEELER-17 — MICRO locking / soliton audit

**Status: NEGATIVE for intrinsic locking; useful cross-branch result**

Goal: test whether the existing MICRO admissibility rule supplies the local locking mechanism needed by WHEELER-16, without introducing a new potential.

MICRO rule used:

- binary cyclic word;
- forbidden local patterns `010` and `101`;
- cost = number of forbidden length-3 windows;
- local dynamics = length-3 reversal subject to non-increasing cost;
- growth repair is allowed in the wider MICRO programme but was not needed to identify the zero-cost structure.

## Zero-cost manifold

Exact enumeration for cyclic words of lengths `n=4..10` shows that cost zero is highly degenerate.

Examples:

- `n=4`: 6 zero-cost states;
- `n=5`: 12;
- `n=6`: 20;
- `n=7`: 30;
- `n=8`: 46;
- `n=9`: 74;
- `n=10`: 122.

The zero-cost states are not only the uniform words `000...0` and `111...1`. Any cyclic configuration with no isolated bit is admissible; equivalently, every run of equal bits has length at least 2.

Thus domain boundaries can exist at zero cost, for example periodic patterns built from blocks such as `00...011...1` provided all cyclic runs have length at least 2.

Therefore the MICRO cost does **not** provide a two-vacuum locking potential of the type required to localize a topological winding into a unique domain wall.

## Reversal dynamics inside the zero-cost set

Using cyclic length-3 reversals and retaining only non-increasing-cost moves, the zero-cost manifold remains fragmented rather than collapsing onto a small vacuum set.

Measured zero-cost connected-component counts:

- `n=5`: 12 states, 4 components; largest components 5,5;
- `n=6`: 20 states, 10 components; largest 6,6;
- `n=7`: 30 states, 18 components; largest 7,7;
- `n=8`: 46 states, 32 components; largest 8,8;
- `n=9`: 74 states, 42 components; four components of size 9 plus many isolated states.

So reversal dynamics preserves many distinct zero-cost domain arrangements. It does not dynamically select only the two homogeneous vacua.

## Consequence for WHEELER localization

WHEELER-16 established that nonzero global winding forces nontrivial local structure but does not force localization unless there is an additional locking mechanism.

The existing MICRO forbidden-pattern cost does not supply that locking mechanism in its present form because interfaces can be zero-cost. Therefore:

- **PASS:** MICRO provides a genuine local admissibility landscape;
- **NEGATIVE:** that landscape is too degenerate to force a localized topological defect;
- **NEGATIVE:** existing length-3 reversal dynamics does not reduce the vacuum manifold to a unique conjugate pair;
- **OPEN:** a modified or derived secondary observable on the MICRO zero-cost manifold might still create effective locking, but this would need an independent justification rather than being inserted for WHEELER.

## Interpretation

This is a useful cross-branch failure. The WHEELER and MICRO strands are structurally compatible, but the current MICRO rule cannot be used as evidence that EHF naturally produces particle-like solitons.

The next sensible question is whether the large MICRO zero-cost manifold itself carries a lower-level topological or component label that could serve as an emergent vacuum index. That would be a new result if it arose from the existing transition graph rather than from adding a potential by hand.
