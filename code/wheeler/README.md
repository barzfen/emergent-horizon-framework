# Reproducible Wheeler checks

Run from the repository root:

```bash
python code/wheeler/review_audit.py
python code/wheeler/projective_audit.py
```

`review_audit.py` requires NumPy and SciPy. SymPy is optional: its absence is recorded, not silently treated as a successful symbolic check. The review also checks the symbol-bias algebra separately by hand.

`projective_audit.py` uses only the Python standard library and exact rational probabilities. It checks WHEELER-58, including both event-uniform and state-uniform processes, observer projections and preparation dependence.

Outputs are written to `data/wheeler/`. These checks reconstruct the written models independently; they do not certify every experiment in the series.

Conventions: cyclic adjacency, labelled/rooted binary tuples, insertion before slots 0,...,n−1. The review graph uses distinct non-self neighbours for cyclic length-3 reversals. Rotation quotienting is used only where explicitly identified.
