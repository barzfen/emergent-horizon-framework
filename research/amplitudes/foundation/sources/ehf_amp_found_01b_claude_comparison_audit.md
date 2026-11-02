# EHF-AMP-FOUND-01B — Claude comparison audit

## Verdict

The reported “anchor 5” closure and the EHF-AMP-FOUND-01B “anchor 2” closure are not results of the same calculation.

### Claude AMP-20C

`amp20c_all_anchors.py` constructs the source chamber decomposition once:

```python
Csrc = chambers(9)
```

Here `chambers(9)` uses the original `Pi` function, which is anchored at label 1. It then caches one set of local relation bases on those fixed `Pi_1` fibres. For each `a`, `push(a)` changes only the label whose two neighbours define the residue channels.

Therefore Claude AMP-20C computes:

> fixed `Pi_1` chart + cumulative residue channels centred at labels 1,2,...,9.

It does **not** rebuild `Pi_a` or recompute local relation spaces for each anchor.

Its result is still meaningful:

- channels centred at labels 1–4 do not recover the missing direction;
- adding the channel centred at label 5 does;
- all label-centred channels together span the full 1800-dimensional global n=8 relation space.

A more accurate name is:

> **Fixed-Chart Multi-Channel Closure**.

### EHF-AMP-FOUND-01B

The EHF-AMP-FOUND-01B script constructs, for each anchor `a`:

```python
source_fibre_map = anchor_fibres(n, a, source_cycles)
```

and recomputes the local relation spaces on those `Pi_a` fibres before applying anchor-`a` residues.

Therefore it computes:

> true anchor-relative chart `Pi_a` + its matching anchor-`a` residue channels.

In the seed-11 run:

- `Pi_1` gave 14/15 in the exceptional target;
- the genuinely rebuilt `Pi_2` chart gave 15/15;
- the cumulative rank increased from 524 to 525 by exactly one direction;
- the missing-direction residual fell to approximately 2.6e-15;
- the fresh Parke–Taylor residual remained approximately 7e-14.

A more accurate name is:

> **True Multi-Chart Closure**.

## Reconciliation

Both statements can be true simultaneously:

1. Holding the `Pi_1` source chart fixed, one must add label-centred residue channels through label 5 before the gap closes.
2. Changing the source chart itself to `Pi_2`, and using the matching anchor-2 residue map, already supplies the missing direction.

Thus there is no numerical contradiction. The two probes vary different pieces of the construction.

## Scientific interpretation

The distinction separates two mechanisms:

- **channel completion:** one fixed chart contains enough local relation data, but several factorisation channels are needed to expose the global relation space;
- **chart completion:** changing the reference-relative partition changes which local relations are available, and another chart can expose a direction hidden in the first.

Both support an atlas-style interpretation, but they should not be merged into one claim.

## Growth files

`GROW-01` is a useful exact combinatorial bridge between insertion and factorisation:

- all-gap insertion is a bijection between `(n-cycle, gap)` and `(n+1)-cycle`;
- anchor-gap insertion is an exact section of anchor-channel deletion;
- anchor branches are chamber-single-valued;
- interior insertions scatter across chambers;
- chamber branching alternates with parity.

This is a tier-2 combinatorial insertion law. It is not yet the foundational CBB growth law and it does not use LR3 dynamics.

The uploaded script directly reproduces Q0–Q3 for 6→7, 7→8 and 8→9. The extra composite 7→9 law in the results note is not implemented in the uploaded `grow01_insertion.py`, so it remains recorded but not independently reproduced from the supplied code.
