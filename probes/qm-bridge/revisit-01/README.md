# QM bridge revisit 01: Assumptions audit and six-state control

**Evidence status: COMPUTATIONAL / NEGATIVE CONTROL.**

[Read the report and analytic arguments](REPORT.md). [Return to the series index](../README.md).

A bounded review of the retained QM bridge v5, observer audits 07–10, probe-dependent geometry 01 and MICRO–OPW 01–03. The fresh six-state calculation compares a classical graph walk with an explicitly supplied coherent control. At benchmark t=0.5 the two phase preparations give B-readout probabilities 0.879313248492 and 0.106516078487 despite identical initial carrier probabilities. This demonstrates what added phase information can do; it does not derive that information or dynamics from the carrier.

Dependencies are recorded in [requirements.txt](requirements.txt). The included source notes are provenance, not a new verification of their full censuses. [source_manifest.json](source_manifest.json) records unchanged source hashes and included paths. Its source_path fields identify the original package locations, rather than additional required repository files.

## Reproduce from the repository root

```sh
python3 probes/qm-bridge/revisit-01/probe.py
```

Research direction: Barry Fensom; implementation and exposition assisted by ChatGPT. See the series index for verification scope and attribution.
