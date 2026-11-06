# Nine-point odd-to-even tail theorem

[Original theorem draft v1.5](theorem-v1.5.md) — Barry Fensom, 17 July 2026. The supplied draft is preserved byte-for-byte.

This package studies signed, adjacency-restricted deletion of label 9 from fibre-local Parke–Taylor relations. Across the 35 source fibres, the transmitted ranks are 0, 2, 8, 9, 14 and 15. After transport to a reference fibre, the images form six subspaces with the lattice described in the draft.

## Verification status

The accompanying independent reconstruction uses exact rational arithmetic and standard-library Python. It checks the reference (1,9) chart: all 35 fibres, the rank law, the six-space collapse, the subspace lattice and character multiplicities. It also checks 363 image generators with source lifts, exact collision-residue evaluations and common-numerator MHV evaluations.

The original draft contains broader claims. This reconstruction does **not** independently recertify all 72 anchor/deletion charts, minimum-support claims, the seven-seed construction or all 21 templates. The original draft and the scope of this later computational check must be distinguished. Neither establishes new physical dynamics or a demonstrated application to scalar scaffolding.

## Reproduce

From the repository root, run:

```sh
python3 research/amplitudes/nine-point-tail/reconstruct.py
```

The script asserts its exact checks and writes `results.json` and `certificates.json` beside itself. The latter contains the generated source lifts and reference images and is omitted from version control because it is reproducible. `results.json` includes an elapsed-time field that varies between runs.

No third-party Python packages are required. The retained results document the computational check; the theorem's full statement and conventions are in the original draft.

## Follow-up studies

See the [follow-up index](followups/README.md) for the exact audits, explicit lifts, boundary analysis and gluon amplitude benchmark.

The [support-reduction study](followups/support-reduction.md) uses simple relations among shuffle coefficients to shrink the exact rank calculation. Removing any one of the 36 branch-specific symmetry orbits preserved the transmitted subspaces and both exceptional cancellation dimensions in the reference chart.

The [sector-selection study](followups/sector-selection.md) identifies where the two exceptions arise and shows that removing different position families can switch them off separately while preserving the transmitted union subspace.

The [orbit thresholds](followups/sector-threshold.md) and [mixed-family deletions](followups/mixed-orbits.md) measure how robust those exceptions are when the allowed orderings are changed.

The [shared-residue deletion rule](followups/shared-residue-rule.md) explains which combinations of deletions remove the `+−` exception in the reference chart.

The [union-cancellation deletion rule](followups/union-cancellation-rule.md) settles the reference-chart minima among branch-exclusive orbits at two deletions for `+−` and four for `−−`.

The [ordering geometry test](followups/ordering-geometry.md) shows that a local window around label 9 cannot determine whether the two exceptions survive a cut.

The [tail shuffle trace](followups/tail-shuffle-trace.md) identifies the distant ordering change behind the matched counterexamples.

The [support test](followups/support-sector-test.md) shows why generic row matching misses both exceptions and what changes when the signs or magnitudes are simplified.

The [doubled-shuffle study](followups/shuffle-doubles.md) traces the factor of two and tests a selective restoration on 16 new cuts.
