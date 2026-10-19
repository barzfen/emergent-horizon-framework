# EHF-HOL-01A — Canonical-Transport Gate

**Status: COMPLETE — NULL/UNDEFINED FOR FIRST CANDIDATE; NO HOLONOMY CLAIM**

## Purpose

Before enumerating loops, HOL-01 requires a pre-existing transportable datum and canonical edge transport. This gate tests the smallest obvious existing candidate: the closed cyclic residue chain used in WHEELER-09.

## Candidate substrate

Use the WHEELER-09 family:

- local residues `x_i in Z_m` on a cyclic chain of length `n`;
- closure `sum_i x_i = 0 mod m`;
- admissible nearest-neighbour moves

`T_i: (x_i,x_{i+1}) -> (x_i+1,x_{i+1}-1) mod m`

and inverse `T_i^{-1}`.

The state graph and inverse edge operation are therefore canonical within this toy model.

## Transport audit

The existence of a canonical state transition is not by itself a connection on an independent local fibre. We need an already-defined datum `q_x` attached to a state and an identification of that datum across each edge.

Three obvious possibilities were checked conceptually.

### 1. Site labels / chain orientation

The WHEELER-09 move changes residue values but does not move or rotate the site frame. Transporting the fixed site labels by their native identity map gives identity around every closed state-space loop. This is a valid but trivial transport.

### 2. Residue values

Residues are components of the state itself. Along a closed state-space loop the final residue configuration equals the initial configuration by definition. Treating the whole state update as 'transport' therefore gives only the tautology that a closed loop returns to its starting state. It does not define an independent holonomy observable.

### 3. A marked unit of transferred residue

One could try to follow a particular transferred unit through successive nearest-neighbour moves. But residues are elements of `Z_m`; WHEELER-09 does not distinguish individual units or specify which incoming unit is the outgoing unit at a later move. Such particle-like identity would be an additional rule. HOL-01 forbids adding it merely to obtain path dependence.

## Result

For the first candidate substrate, the canonical-transport gate yields:

- fixed site frame: **HOL-01A / TRIVIAL**;
- state-as-datum: **TRIVIAL BY DEFINITION / NOT AN INDEPENDENT TRANSPORT**;
- marked-residue transport: **UNDEFINED WITHOUT NEW STRUCTURE**.

Therefore it would be scientifically invalid to enumerate loops in WHEELER-09 and call any label bookkeeping defect 'holonomy'.

## Interpretation

This is a useful negative result. A state graph with cycles and invertible local moves does not automatically carry a nontrivial connection. Genuine discrete holonomy requires a fibre/local frame plus a canonical rule for comparing that frame between neighbouring states.

This sharpens the EHF question from

> do admissible histories contain loops?

to

> does an existing EHF sector already contain a path-dependent identification of local data over those loops?

## Next candidate search

Search existing EHF work for a sector where local comparison data is already part of the model rather than added for HOL. Priority candidates are:

1. sectors with explicit local signatures/orientations and nontrivial relabelling under moves;
2. quotient/rotation sectors where transition-induced frame changes are already defined before quotienting;
3. observer/recursion work if it contains an explicit comparison map between local observer descriptions.

If none supplies a canonical connection, HOL-01 should remain `UNDEFINED` at the EHF level rather than manufacture curvature.

## Physics boundary

No conclusion about spacetime curvature or gravity follows from this gate. The result is purely structural: WHEELER-09's native cyclic residue dynamics supplies a state graph but not a nontrivial independent transport connection.