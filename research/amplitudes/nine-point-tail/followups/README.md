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
| [Tail shuffle trace](tail-shuffle-trace.md) | Disjoint shuffle supports and exact identities explain the matched tail swaps. | `PYTHONPATH=.. python3 tail_shuffle_trace.py` |
| [Can support predict the sectors?](support-sector-test.md) | Generic matching misses both exceptions. Sign-only columns give extra directions. | `PYTHONPATH=.. python3 support_sector_test.py` |
| [Doubled shuffle entries](shuffle-doubles.md) | Restoring 28 shared doubles recovered the exception counts on the reference cut and 16 new cuts. | `PYTHONPATH=.. python3 shuffle_doubles.py` |
| [Common-cut holdout](common-cut-holdout.md) | The 28-entry rule matches 61 of 63 cuts. One cut preserves the count while replacing the original cancellation. | `PYTHONPATH=.. python3 common_cut_holdout.py` |
| [Position-7 replacement trace](replacement-trace.md) | Exactly three four-orbit addbacks restore the replacement's decomposition in the separate branches. | `PYTHONPATH=.. python3 replacement_trace.py` |
| [Position-family cancellation trace](position-family-trace.md) | Position 3 retains the original class and adds two directions already in the original branch sum. | `PYTHONPATH=.. python3 position_family_trace.py` |

The chamber pairing explains the local cancellation mechanism. A geometric prediction of the restricted shuffle ranks remains open.

See [Colour channels in the first finite collinear coefficient](../../collinear-colour/README.md) for the full-colour Yang–Mills study that followed this work.

| [Signed orientation bridge](signed-orientation-bridge.md) | Exact all-40,320-word test: signed reflection commutes with collision residue. Adding reflected duplicates leaves all 35 support-cut ranks unchanged; adding two excluded zero-residue words restores the rank-14 missing direction. | `python3 signed_orientation_bridge.py` |

| [Rank-14 event-pair predictor](rank14-event-pairs.md) | Exact census across the six rank-14 fibres: 0,4,0,11,18,20 two-word repairs. A reference-fitted ordering template catches all 53 repairs across those fibres but has 67 false positives; a single missing relation dimension does not guarantee a two-word repair. | `python3 rank14_event_pairs.py` |

| [Minimal rank-14 triple repairs](rank14-minimal-triples.md) | Completes minimum repair sizes for all six rank-14 parity fibres: four require two excluded words, but (2,5,7) and (3,5,7) require exactly three. Explicit exact KK certificates, 66 and 322 successful triples, and a relative cancellation-distance formulation. | `python3 rank14_minimal_triples.py` |
