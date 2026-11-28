# HC-GROW: reversal-support propagation across growing HC layers

Recovered source package, 2 November 2026.

* [Cumulative working document, filename v0.8](sources/ehf_hc_grow_working_document_v0_8.md).
* [Individual GROW-01–08 notes, scripts and result tables](sources/).
* [Later support-limit corrections](audits/): read the LR3 onset v0.2 audit alongside the earlier Pólya support-limit v0.1 audit. The later note resolves the source/initial-condition ambiguity; it does not establish criticality or a CFT.
* [HC-RAW source layer](../hc-raw/README.md).

The series studies canonical reversal-support ancestry, forward lifts, branching kernels, intrinsic parity, renewal and cross-channel geometry. Structural census fractions become probabilities only under an explicit sampling convention. The support-channel symbol LR3 is not automatically the literal OPW length-3 convention at small sizes; see [OPW's convention warning](../opw/README.md).

## Keep the corrections visible

For the declared unfolded uniform-lift recurrence, the onset LR3 initialization is (n,l)=(6,3), yielding balanced urn counts (4,4). Its unfolded limiting fraction has Beta(4,4) law: a half mean with persistent variance, not a deterministic half-density limit. Neither the mean nor the urn identification establishes a critical point, scale invariance or conformal field theory. The earlier conditional audit and the later source correction are both retained to make the change in interpretation reviewable.

The newest recovered working-document filename is v0.8, but its opening header still says v0.1. A same-name earlier snapshot is preserved with a content-hash suffix because its bytes differ; the manifest records both rather than overwriting one.

## Verification limits

**The recovered GROW-01, GROW-02, GROW-03A and GROW-04 Python files contain explanatory docstrings and print a PASS message without running a census.** GROW-05 performs a limited floating-point normalization self-check, not all the enumeration described in its report. The GROW-07/08 scripts contain substantive implementations, but were not rerun in this import. There is no recovered standalone GROW-06 Python implementation in this package.

Historical tables are preserved evidence records, not newly validated outputs. See the [consolidation report](../consolidation-2026-11-02/README.md) for what was checked and what remains unavailable. This is not a derivation of physical growth or time.
