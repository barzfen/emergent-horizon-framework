# MICRO observer compatibility audit 01

[Read the report and analytic argument](REPORT.md).

![Two rings with identical colour counts and different growth probabilities](observer_comparison.png)

For the specified binary no-isolation model, two nine-bit rings with five zeros and four ones have different probabilities of inserting a one: 5/11 versus 6/13. Retaining the block count restores predictive closure under the specified uniform growth kernel. Counts plus blocks and oriented necklaces also close under the specified LR3 kernel.

Exact enumeration covers all 2,198 admissible rooted states of sizes 4–14. All tested observers agree on reachable observation supports; the counts-only failure concerns probabilities. The report gives an analytic closure argument valid beyond that census.

The witness states belong to different conserved block-count sectors. This is a failure of strong lumpability across arbitrary preparations, not a demonstration of physical memory, quantum behaviour or a connection to the nine-point theorem.

## Reproduce

From the repository root:

```sh
python3 probes/micro/observer-compatibility-01/probe.py
```

Python's standard library is sufficient. The script checks the exact distributions, invariants and growth formula and regenerates `results.json` beside itself.

The figure is included. To regenerate it, run `python3 probes/micro/observer-compatibility-01/draw.py`; this optional step requires Pillow and DejaVu Sans fonts at the Linux paths specified in that script.
