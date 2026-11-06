# Nine-point tail follow-ups

Run the commands from this directory. The scripts use Python’s standard library and the shared reconstruction in the parent directory. Each note has a matching `*-results.json` file.

| Study | Result | Reproduce |
| --- | --- | --- |
| [Orientation audit](orientation.md) | Removing the representative cut gives rank 15 in all 35 fibres. | `PYTHONPATH=.. python3 audit.py` |
| [Rank-14 certificate](rank14.md) | A two-coefficient functional detects the missing direction. | `PYTHONPATH=.. python3 certificate.py` |
| [Branch certificates](branches.md) | Explicit liftability conditions for the rank-8 and rank-9 cuts. | `PYTHONPATH=.. python3 branches.py` |
| [Shared residue](shared-lifts.md) | Two different lifts yield the same extra residue. See the [side-by-side coefficients](Lifts.md). | `PYTHONPATH=.. python3 probe.py` |
| [Boundary cancellations](boundary.md) | The two extra cancellation directions have distinct symmetry types. | `PYTHONPATH=.. python3 boundary.py` |
| [Shuffle sectors](shuffle-sectors.md) | Exact shuffle ranks identify which sectors contain the extra directions. | `PYTHONPATH=.. python3 shuffle_sectors.py` |
| [Amplitude benchmark](benchmark.md) | The two lifts reproduce the target but offer no input savings in the tested collinear calculation. | `PYTHONPATH=.. python3 benchmark.py` |
| [Support reduction and modified cuts](support-reduction.md) | Two-term exterior equations reduce the exact rank problem. Both exceptions survive all 36 single-orbit deletions. | `PYTHONPATH=.. python3 support_reduction.py` |
| [Sector selection and position-family deletions](sector-selection.md) | The two exceptional directions arise at different steps and can be removed separately. | `PYTHONPATH=.. python3 sector_ablation.py` |
| [Orbit deletion thresholds](sector-threshold.md) | Within the three sensitive families, removing the corresponding exception takes at least three, four, or six orbits. | `PYTHONPATH=.. python3 sector_threshold.py` |
| [Mixed-family orbit deletions](mixed-orbits.md) | Ten of 630 pairs remove the shared residue. Every pair preserves the union cancellation. | `PYTHONPATH=.. python3 mixed_orbits.py` |
| [Shared-residue deletion rule](shared-residue-rule.md) | Affine lift constraints explain all ten conflicting pairs and predict 22 minimal rank-8 triples. | `PYTHONPATH=.. python3 shared_residue_rule.py` |
| [Union-cancellation deletion rule](union-cancellation-rule.md) | All triples preserve `−−`. Exactly four quadruples remove it. | `PYTHONPATH=.. python3 union_cancellation_rule.py 4` |
| [Local ordering geometry](ordering-geometry.md) | Holdout cuts and matched counterexamples rule out the tested local features. | `PYTHONPATH=.. python3 ordering_collisions.py` |

The chamber pairing explains the local cancellation mechanism. A geometric prediction of the restricted shuffle ranks remains open.

See [Colour channels in the first finite collinear coefficient](../../collinear-colour/README.md) for the full-colour Yang–Mills study that followed this work.
