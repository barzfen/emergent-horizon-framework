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

The initial retained result distinguishes exact rational incidence ranks from
floating-point transport/decomposition checks. Later probes add exact
cohomological results. No broader novelty claim is made.

## HODGE-02

[Commuting faces and transport cohomology](probes/hodge/HODGE-02.md)
adds rule-based MICRO square complexes, a closed signed-transport cochain,
and an explicit all-size nonzero winding loop. Exact scans cover n=5,...,12.

The same audit finds cycles missed by net transport and a failed fixed-root
growth map. A bridge to the Clay conjecture remains unestablished.

```sh
OPENBLAS_NUM_THREADS=1 python code/hodge/hodge_02_audit.py --output data/hodge/hodge-02-results.json
```

## HODGE-03

[Run coordinates and boundary winding](probes/hodge/HODGE-03.md) explains the
cycles missed by signed binary transport. Exact scans through n=18 cover
200 moving components; boundary winding detects the rational H1 direction
on each one.

[C1 and C2](formal/hodge/CONJECTURES.md) were introduced as working
conjectures here. C2 is subsequently proved in HODGE-04 and C1 in HODGE-05.
Novelty remains unassessed.

```sh
OPENBLAS_NUM_THREADS=1 python code/hodge/hodge_03_audit.py --output data/hodge/hodge-03-results.json
```

## Current literature assessment

[OpenAI Hodge literature audit](research/hodge/LITERATURE-01.md), checked
20 October 2026, corrects the K3-products claim to withdrawn and separately
assesses the unwithdrawn CM manuscript. No corresponding Lean formalization
was identified in the inspected catalogue.

A direct homotopy identification of the explicit MICRO circle components
with smooth projective varieties is ruled out by first-Betti parity.
A more general bridge remains unestablished. The local period-identity
proof target is completed in HODGE-04 below.

## HODGE-04 — C2 proved

[HODGE-04](probes/hodge/HODGE-04.md) gives an explicit integer potential
with dF=(n-2D)j-2(n-2m)kappa for every n>=5.
The [complete proof](formal/hodge/TRANSPORT-POTENTIAL.md) handles repeated
cyclic marker patterns and ring seams without assuming C1.

The standard-library implementation verifies all 16,190 edges through n=18.
The component-classification target is subsequently resolved in HODGE-05.

```sh
python code/hodge/hodge_04_audit.py --output data/hodge/hodge-04-results.json
```

## Latest: HODGE-05 — C1 and component classification

[HODGE-05](probes/hodge/HODGE-05.md) derives the full moving-component
label (D,chi,rho), with rho modulo gcd(4,l), and proves pi_1=Z and H_1=Z.
Boundary winding has image (l/gcd(4,l))Z.
[The full proof](formal/hodge/COMPONENT-CLASSIFICATION.md) uses ordered
marker-gap coordinates and commuting diamonds.

Exact JavaScript checks through n=18 reproduce all 200 moving components.
Independent proof review and broader novelty assessment remain open.
Next is HODGE-06, a higher-cell completion audit.

```sh
node code/hodge/hodge_05_audit.mjs > data/hodge/hodge-05-results.json
```
