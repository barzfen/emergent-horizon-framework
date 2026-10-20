# EHF Hodge branch

Start with [the branch guide](research/hodge/README.md), then read
[HODGE-01: discrete Hodge fit and algebraic-geometric bridge audit](probes/hodge/HODGE-01.md).

**Decision:** proceed with a bounded discrete Hodge research track.
A connection to the Clay Hodge conjecture remains unestablished.

This branch starts from holonomy commit
`299313458f68b780e48b575a340f2f2284416ebe` (2026-10-20).
It preserves that work and adds an independently reproducible first audit.
No merger into main is implied.

Reproduce:

```sh
python -m pip install -r code/hodge/requirements.txt
python code/hodge/hodge_01_audit.py --output data/hodge/hodge-01-results.json
```

The retained result distinguishes exact rational incidence ranks from floating-point
transport/decomposition checks. No novel theorem or conjecture is claimed.
