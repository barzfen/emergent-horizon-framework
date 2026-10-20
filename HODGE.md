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

## Latest: HODGE-02

[Commuting faces and transport cohomology](probes/hodge/HODGE-02.md)
adds rule-based MICRO square complexes, a closed signed-transport cochain,
and an explicit all-size nonzero winding loop. Exact scans cover n=5,...,12.

The same audit finds cycles missed by net transport and a failed fixed-root
growth map. A bridge to the Clay conjecture remains unestablished.

```sh
OPENBLAS_NUM_THREADS=1 python code/hodge/hodge_02_audit.py --output data/hodge/hodge-02-results.json
```

## Latest: HODGE-03

[Run coordinates and boundary winding](probes/hodge/HODGE-03.md) explains the
cycles missed by signed binary transport. Exact scans through n=18 cover
200 moving components; boundary winding detects the rational H1 direction
on each one.

[Working conjectures C1 and C2](formal/hodge/CONJECTURES.md) state the
all-size classification and period relation. Neither is proved in general;
novelty remains unassessed.

```sh
OPENBLAS_NUM_THREADS=1 python code/hodge/hodge_03_audit.py --output data/hodge/hodge-03-results.json
```
