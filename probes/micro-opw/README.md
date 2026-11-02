# MICRO–OPW 01–03

2 November 2026. These are reproducible finite probes developed in the current investigation. They combine fixed binary vertex types, cyclic no-isolation (forbid 010/101), and OPW preserve-filtered literal length-2/3 reversals.

| Probe | Result | Entry point |
|---|---|---|
| 01 | MICRO makes some LR3 components distinct that LR2 can reconnect; exhaustive n=5,7,9 and nonconstant colourings | [Report](micro_opw_01/README.md) |
| 02 | The retained seven-vertex pair has a pointwise invariant local neighbour-type readout; unanchored bit patterns fail | [Report](micro_opw_02/README.md) |
| 03 | A continuously active reversible probe gate writes and resets, but fails to protect the record; returning and idle probes undermine retention | [Report](micro_opw_03/README.md) |

These differ from the older [MICRO binary observer audit](../micro/observer-compatibility-01/README.md): here vertices carry material labels and bits, OPW canonicalization quotients reflection, and the probe in 03 uses specified continuous-time rates. Do not transfer kernels or closure claims between the models without matching these conventions.

Keep the three directories as siblings because their explicit imports preserve the tested code. Requires Python 3, NumPy and SciPy. From the repository root:

```bash
python probes/micro-opw/micro_opw_01/probe.py
python probes/micro-opw/micro_opw_01/verify_witness.py
python probes/micro-opw/micro_opw_02/probe.py
python probes/micro-opw/micro_opw_02/verify.py
python probes/micro-opw/micro_opw_03/probe.py
python probes/micro-opw/micro_opw_03/verify.py
```

All results are finite model findings. Initial preparations, fixed types, distinguished ports, rates and readout remain specified assumptions. There is no physical observer, noise-protected autonomous memory, or claim that either OPW model is selected by nature.
