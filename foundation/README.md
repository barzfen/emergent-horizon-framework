# Foundation

This directory holds the minimal EHF definitions and assumptions.

Planned documents:

- `primitives.md` — primitive objects/relations retained by the framework.
- `admissibility.md` — admissible comparison and transformation rules.
- `growth.md` — intrinsic state-space enlargement.
- `histories.md` — admissible histories and recurrence.
- `observers-records-time.md` — internal records, observers, and clock construction.

Rule: foundational documents should state mathematics first and physical interpretation separately.

Completed audits:

- [Assumption audit 01: when are different relational roles forced?](assumption-audit-01/README.md) — a precise graph model, an all-size forcing criterion, assumption-removal counterexamples and exhaustive checks through six vertices. Static structure is distinguished from persistent records.
- [Assumption audit 02: minimum requirements for a record](assumption-audit-02/README.md) — exact preservation, inaccessible information, invariant readouts, and a rational-arithmetic noise benchmark; separates retained information from a derived recording mechanism.
- [Assumption audit 03: can a boundary crossing write a record?](assumption-audit-03/README.md) — an explicit event-coupled register, acquisition from blank, noisy retention, saturation and reversible-toggle controls; accounts for the added observer assumptions.
- [Assumption audit 04: writing a record into cycle structure](assumption-audit-04/README.md) — one allowed event-triggered rearrangement stores a boundary-readable distinction; exhaustive move-graph and retention checks expose the limits of protection by conserved sectors.
