# AMP foundation: recovered original source series

Recovered source package, 2 November 2026. [Source scripts, specifications and dated working documents](sources/) cover AMP-FOUND-01, 01B, 02A–H, 03A–L and available 04A–C/T0 continuations. Historical revisions and explicit correction notes remain alongside the later files; do not assume that an earlier unversioned script is the recommended implementation.

## Relation to the nine-point theorem

The existing [nine-point tail theorem draft v1.5 and independent reconstruction](../nine-point-tail/README.md) remain unchanged. The newly preserved 03A–L scripts are original source implementations referenced by that draft; they are distinct from reconstruct.py and have not all been executed in this consolidation. In particular, the available source now includes the 03K/03L chart-covariance stages. **Their presence does not recertify the broad theorem package.**

The original generated runs/ trees, source-relation certificates, output basis files and every historical runtime dependency have not all been recovered. Some scripts require explicit --base-script, --helper-script and --out-dir paths and earlier run outputs. Start by reading the corresponding probe specification and the script's argument parser. Do not expect the sources/ directory to be a ready-made runs/ directory.

This package includes exact-rank audit/correction material for the later 11-to-10 exploration. It must not be merged into the nine-point theorem's claim scope without a separate scientific audit. Finite-field results, exact rational certificates, conjectures and physical interpretations retain different statuses.

[Partial retained historical runs](retained-runs/) include the supplied 02D seed-29 bundle and the 04A discovery output bundle. They were extracted without modifying their bytes, not regenerated. In particular, the 04A finite-field output should be read alongside its result-audit and discrepancy follow-up in sources/; it is not a replacement for an exact rational rank certificate.

Byte hashes, Python syntax checks and the explicit scientific-verification limits are recorded in the [consolidation report](../../consolidation-2026-11-02/README.md). The existing reference-chart reconstruction remains the independently reproduced finite baseline described in its own README.
