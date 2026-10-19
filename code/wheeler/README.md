# Reproducible Wheeler checks

Run from the repository root:

```bash
python code/wheeler/review_audit.py
python code/wheeler/projective_audit.py
python code/wheeler/rotation_audit.py
python code/wheeler/quotient_entropy_audit.py
python code/wheeler/unconditioned_entropy_audit.py
python code/wheeler/minimal_seed_entropy_audit.py
python code/wheeler/many_domain_audit.py
```

`review_audit.py` requires NumPy and SciPy. SymPy is optional: its absence is recorded, not silently treated as a successful symbolic check. The review also checks the symbol-bias algebra separately by hand.

`projective_audit.py` uses only the Python standard library and exact rational probabilities. It checks WHEELER-58, including both event-uniform and state-uniform processes, observer projections and preparation dependence.

`rotation_audit.py` uses standard-library exact rational kernels to check WHEELER-59 rotation lumpability, root dependence, orbit-weighted column bounds and the majorization counterexample. Entropy diagnostics use floating-point logarithms.

`quotient_entropy_audit.py` checks WHEELER-60 using exact rational laws, independent binary insertion enumeration and two integer/rational entropy-sign certificates. It uses only the standard library; Decimal logarithms supply display values.

`unconditioned_entropy_audit.py` checks WHEELER-61 using recursive kernels, an independent urn endpoint formula, binary insertion enumeration and rational logarithm intervals. It also records the minimal-seed scan through 40 events. Standard library only.

`minimal_seed_entropy_audit.py` checks WHEELER-62’s all-time minimal-seed theorem using exact polynomial identities, a positive-coefficient certificate, early-step inequalities and independent endpoint checks. Standard library only.

`many_domain_audit.py` checks WHEELER-63 with exact rational endpoints, recursion through four events, and numerical entropy/stabilizer identities. Larger-sector monotonicity is only checked over the retained finite ranges. Standard library only.

Outputs are written to `data/wheeler/`. These checks reconstruct the written models independently; they do not certify every experiment in the series.

Conventions: cyclic adjacency, labelled/rooted binary tuples, insertion before slots 0,...,n−1. The review graph uses distinct non-self neighbours for cyclic length-3 reversals. Rotation quotienting is used only where explicitly identified.
