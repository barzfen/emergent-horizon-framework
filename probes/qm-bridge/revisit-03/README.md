# QM bridge revisit 03: operational orientation readout

**Evidence status: COMPUTATIONAL + ANALYTIC ARGUMENTS / CLASSICAL CONTROL.**

[Read the full report](REPORT.md). [Series index](../README.md).

An explicit ordered adjacent marker pair carries Revisit 02's orientation through actual LR2/LR3 histories. Two retained five-move histories reach the same carrier. After matching their unordered marker-position distributions, a directional local port reader distinguishes them. Without marker roles the two joint processes have identical reduced future laws, including a control in which marker positions affect carrier motion.

The frozen-carrier reader has ideal success 1. With moves still active, the selected 12-tick three-outcome reader gives equal-prior optimal success 0.6830468891 for passive coupling and 0.7028698275 for the specified marker-gated coupling. Timeout outcomes are retained. Exact fractions and all intermediate horizons are saved.

This makes a history variable operationally accessible in a deliberately enlarged classical model. The markers, co-transport, port and detector are supplied structure; quantum amplitudes, unitary dynamics and the Born rule remain unestablished.

## Reproduce

From the repository root:

```sh
python3 probes/qm-bridge/revisit-03/probe.py
python3 probes/qm-bridge/revisit-03/verify.py
```

Python's standard library is sufficient. The main implementation imports the sibling [Revisit 02 probe](../revisit-02/probe.py), whose hash is retained. The independent verifier imports neither probe. [input_witness.json](input_witness.json) freezes the prior path certificate; [results.json](results.json) contains exact results; [verification.json](verification.json) reports independent implementation checks.

[Why random graphs rather than Hamilton cycles?](RANDOM-GRAPHS.md) explains the distinction between Trugenberger's graph ensemble, an individual Hamilton cycle and EHF's reversal configuration graph. That note is a conceptual source comparison, not a numerical comparison of the two programmes.

Research direction: Barry Fensom. Implementation and exposition assisted by ChatGPT. The separate verifier is not external peer review. No priority claim or physical identification is made.
