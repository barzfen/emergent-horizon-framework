# QM bridge revisit 02: Orientation transport and exact classical control

**Evidence status: COMPUTATIONAL / NEGATIVE CONTROL.**

[Read the report and analytic arguments](REPORT.md). [Return to the series index](../README.md).

Exhaustive representative-colouring graphs at n=7 and n=9 contain 3/15 and 9/111 components with nonflat orientation transport, respectively. The n=7 parity argument excludes opposite transport signs at the same endpoint and step count. At n=9, a retained seed reaches four endpoints with both orientations after five moves. An independent direct-oriented-tour implementation reproduces the exact finite statistics.

The orientation lift is a specified history bookkeeping choice. A coordinate removed by the undirected state definition has not been made physically observable. Signed cancellation is exactly explained as a difference of positive classical populations, and its squared norm is not conserved.

No third-party Python dependencies are required. [verification.json](verification.json) retains the independent implementation checks and explicit equal-length path witnesses. Code and results do not establish novelty or physical quantum behaviour.

## Reproduce from the repository root

```sh
python3 probes/qm-bridge/revisit-02/probe.py
python3 probes/qm-bridge/revisit-02/verify.py
```

Research direction: Barry Fensom; implementation and exposition assisted by ChatGPT. See the series index for verification scope and attribution.
