# EHF QM bridge revisits

**Status: COMPUTATIONAL + ANALYTIC ARGUMENTS + NEGATIVE CONTROLS.**

These working research notes ask whether a quantum description could emerge from an explicitly specified admissible-comparison construction. Admissible comparison is the chosen primitive data of EHF. Neither probe derives physical quantum mechanics or establishes that QM is nonfundamental.

| Probe | Result | Limit |
| --- | --- | --- |
| [Revisit 01: assumptions and six-state control](revisit-01/README.md) | Rebuilds a locally readable six-state MICRO–OPW carrier and compares supplied Markov and coherent dynamics. | Coherent evolution and complex preparations are added controls. |
| [Revisit 02: orientation transport](revisit-02/README.md) | Actual LR2/LR3 histories induce a two-valued transport with negative closed walks in some components. At n=9 equal-length paths can arrive with opposite orientations. | All tested statistics have an exact classical explanation on oriented tours; the signed difference is not a detection probability. |

Read the reports before reusing the result labels. The seven-vertex parity argument, the original flat six-state carrier and the explicit classical lift are essential controls. There is no priority claim or completed external literature review.

## Reproduce from the repository root

Revisit 01 requires Python 3, NumPy and SciPy; the recorded versions are in its requirements file. Revisit 02 and its independent verifier need only Python's standard library.

```sh
python3 probes/qm-bridge/revisit-01/probe.py
python3 probes/qm-bridge/revisit-02/probe.py
python3 probes/qm-bridge/revisit-02/verify.py
```

The scripts regenerate JSON beside themselves. Publication checks used Python 3.12.14; the finite calculations and independent verification passed. No code in the old bridge or earlier source censuses was reverified merely by including source notes.

## Provenance and contribution

Research direction: Barry Fensom. Implementation, source review and exposition: assisted by ChatGPT. The independent verifier is a separate implementation generated in the same AI-assisted workflow, not external peer review. The maintainer remains responsible for scientific review.

The source snapshots in Revisit 01 retain the earlier EHF notes and their stated limits. Their historical statements about repository publication describe the time those notes were prepared; they do not describe the current repository contents. See [CONTRIBUTING.md](../../CONTRIBUTING.md) and [licensing scope](../../LICENSE.md).

The next target is an explicit relational carrier/reference that makes a transported orientation operationally accessible, followed by a comparison against the complete classical model. A physical phase, coherent recombination, the Born rule, composite systems and Bell correlations remain unestablished.
