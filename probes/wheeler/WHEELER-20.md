# WHEELER-20 — Growth Quotient / Persistent-Sector Audit

**Status: PARTIAL PASS; only simple domain-wall sectors persist across growth in tested range**

## Question

Collapse each fixed-size zero-cost MICRO component (after cyclic-translation quotienting) to a node. Connect a node at size `n` to a node at size `n+1` whenever at least one admissible one-bit growth insertion maps a state in the first component to a zero-cost state in the second.

Does any coarse lineage survive growth, even though WHEELER-19 showed that individual fixed-`n` components merge immediately?

MICRO rule used:

- cyclic binary words;
- forbidden patterns `010` and `101`;
- zero cost means every cyclic run has length at least 2;
- dynamics inside a size: zero-cost length-3 reversals;
- growth: insert one bit anywhere, retaining only zero-cost descendants;
- cyclic translations are identified at each size.

## Exact growth invariant

For every admissible zero-cost one-bit insertion tested from `n=4` through `n=16`:

- Hamming weight changes by either `0` or `1`;
- domain-wall count satisfies exactly

`D(n+1) = D(n)`.

This has a direct local explanation. In a zero-cost word, inserting a bit opposite to both neighbours inside a run would create an isolated bit and hence a forbidden `010` or `101` pattern. Therefore an admissible insertion can only:

1. extend an existing run, or
2. shift an existing run boundary by inserting one of the adjacent symbols.

Neither operation creates or removes a domain wall. Hence `D` is an exact growth invariant for the zero-cost MICRO growth rule.

Because a cyclic binary word has an even number of domain walls, the persistent growth sectors are labelled by

`D = 0, 2, 4, 6, ...`.

The minimum size capable of supporting sector `D` is `n = 2D`, since zero-cost requires every one of the `D` cyclic runs to have length at least 2.

## Layered component graph, n=4..16

Translation-quotiented fixed-size component counts were:

| n | components |
|---:|---:|
| 4 | 3 |
| 5 | 4 |
| 6 | 5 |
| 7 | 6 |
| 8 | 8 |
| 9 | 10 |
| 10 | 12 |
| 11 | 14 |
| 12 | 18 |
| 13 | 22 |
| 14 | 29 |
| 15 | 36 |
| 16 | 50 |

When growth edges are added between successive sizes, the many fixed-size splittings collapse dramatically.

Across the full `n=4..16` layered graph there are only six weakly connected lineages:

- one nonuniform lineage with `D=2`, extending across `n=4..16`;
- one nonuniform lineage with `D=4`, first appearing at `n=8`;
- one nonuniform lineage with `D=6`, first appearing at `n=12`;
- one `D=8` node first appearing at `n=16` (the endpoint of the tested range, so continuation is not yet observed);
- the all-zero homogeneous `D=0` lineage;
- the all-one homogeneous `D=0` lineage.

For every tested nonzero `D`, all fixed-size components carrying that `D` belong to a single cross-size growth lineage. Thus the residual organizational labels found in WHEELER-18/19 do not remain distinct once growth is admitted.

## Relation to WHEELER-19

The special `n=12`, `(N1,D)=(6,4)` split, including the balanced `(3,3,3,3)` component, disappears immediately under growth. WHEELER-20 generalizes this: the growth quotient does not reveal a hidden refinement of `D` through `n=16`.

The fixed-size MICRO dynamics therefore contains more organizational information than the growing system retains.

## Verdict

- **PASS:** a genuine cross-size conserved sector exists: domain-wall count `D`.
- **PROVED for the zero-cost insertion rule:** admissible growth preserves `D` exactly.
- **NEGATIVE:** the higher-order fixed-size component labels do not survive as separate growth lineages in the tested range.
- **PARTIAL PASS:** the growing system has persistent sectors, but they are classified by a simple invariant already visible locally rather than by a new emergent vacuum quantum number.
- **CAUTION:** the `D=8` sector first appears at the upper test boundary `n=16`; its continuation is expected from the analytic rule but was not enumerated beyond that size in this audit.

## Interpretation

This closes the MICRO-vacuum detour fairly cleanly. Growth acts as a coarse-graining mechanism: it destroys many finite-size dynamical obstructions while preserving the simpler domain-wall number.

The retained structural lesson is:

`fixed-size constrained dynamics -> many disconnected organizational sectors`

but

`admissible growth -> quotient onto a much smaller persistent sector structure`.

That may be relevant to EHF more broadly: a quantity that appears conserved at fixed state-space size is not automatically fundamental. Surviving the growth map is a substantially stronger criterion.

## Next direction

The Wheeler/MICRO branch should not use the fixed-size residual components as particle-like vacuum labels. A more useful next probe would compare this exact growth invariant `D` with the earlier Wheeler winding/current invariant and ask whether they are independent, coupled, or two descriptions of a common boundary/current quantity.
