# WHEELER-16 — Global-to-Local Defect Audit

**Status: PARTIAL PASS / NEGATIVE for automatic localization**

## Question

Can a protected global winding force a localized defect, endpoint, boundary class, or excitation whose local observer signature inherits that topological protection?

## Setup

Let a lifted closed history carry total winding `w`, so the lifted local increments `d_i` around a cycle satisfy

`sum_i d_i = 3 w`.

The factor of 3 corresponds to the current `Z_3` quotient used in the Wheeler branch. The key question is whether `w != 0` requires a localized nontrivial object, rather than merely some distributed nonzero local structure.

## Result 1 — nonzero winding forces nontrivial local structure

If `w != 0`, then `sum_i d_i != 0`, so at least one `d_i` must be nonzero. Therefore a nontrivial topological sector cannot be represented by an everywhere-trivial local configuration.

This is a genuine global-to-local implication:

`w != 0 -> exists i with d_i != 0`.

However, this does not imply localization.

## Result 2 — smooth local stiffness spreads the winding

For the natural quadratic stiffness

`E = sum_i d_i^2`

subject to fixed total `sum_i d_i = 3w`, the minimum-energy configuration distributes the required winding as evenly as the integer constraint allows.

For `w=1`:

- `n=4`: minima are permutations of `(1,1,1,0)` with `E_min=3`;
- `n=5`: minima are permutations of `(1,1,1,0,0)` with `E_min=3`;
- `n=6`: minima are permutations of `(1,1,1,0,0,0)` with `E_min=3`.

So the topological burden is spread over several locations rather than concentrated into one particle-like defect.

In a continuous phase/stiffness analogue, the minimizer spreads winding uniformly around the cycle, making the same point even more strongly.

## Result 3 — localization requires an additional local mechanism

If the local cost instead strongly favors a vacuum value `d_i=0` and penalizes only the number of nonzero sites, e.g.

`E_vac = count(i : d_i != 0)`,

then the same total winding is minimized by concentrating the entire shift at one location, e.g. `(3,0,0,...)` for `w=1`.

Thus a localized topological defect can emerge only after adding a local vacuum/locking mechanism that favors concentration.

The topology supplies the conserved global obstruction; the local potential determines whether that obstruction is smeared or localized.

## Result 4 — open boundaries are different

For an open history/current, a discrete continuity relation has the form

`partial J = source - sink`.

Then endpoints/boundaries can carry a nonzero net mismatch. In that case localization at a boundary is structural rather than energetic. For a closed nonzero-winding history, by contrast, there is no required point source: the winding can remain globally distributed.

## Verdict

- **PASS:** nonzero global winding forces some nontrivial local structure.
- **FAIL:** global winding alone does not force a localized defect or particle-like excitation.
- **PASS CONDITIONALLY:** a localized defect can inherit the topological sector if an independent local admissibility/energy rule favors discrete vacua or boundary localization.

This means the Wheeler branch has not yet derived a particle from topology alone. It has identified the precise extra ingredient required: a local locking mechanism that converts distributed topological winding into a stable localized defect.

## Next probe

**WHEELER-17 — Locking Mechanism / Soliton Audit**

Test whether an already-existing EHF ingredient (forbidden local patterns, MICRO admissibility cost, growth repair, parity, or observer-record constraints) naturally supplies the required local vacuum structure. The mechanism must not be invented solely to localize winding.
