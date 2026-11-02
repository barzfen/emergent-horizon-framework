# Source consolidation — 2 November 2026

Requested by Barry Fensom. Recovery, navigation and checks assisted by ChatGPT. This addition preserves available EHF scientific sources and the three recent MICRO–OPW probes. It does not promote historical reports into newly verified theorems.

## Reading map

| Branch | What is included | Entry point |
|---|---|---|
| HC-RAW | Working snapshots through filename v0.20; available RAW-01–14 scripts, individual notes and ledgers | [RAW](../hc-raw/README.md) |
| HC-GROW | Working snapshots through filename v0.8; available GROW-01–08 notes, scripts and tables; later Pólya/onset corrections | [GROW](../hc-grow/README.md) |
| OPW3 / OPW23 | Both working documents, earlier versions, OPW3 audits 01–10, corrections and available spectral material | [OPW](../opw/README.md) |
| QM3 | Five structural slow-sector/Hilbert-lift probe sources and specifications | [QM3](../opw/qm3/README.md) |
| AMP foundation | Available original 01–04C/T0 sources and specifications, including nine-point 03A–L; partial 02D/04A historical run outputs | [AMP sources](../amplitudes/foundation/README.md) |
| XBR / OPW–AMP | Available common-growth, operator, invariant-module, primitive-representation and null-holonomy source sequence | [XBR](../opw-amp-bridge/README.md) |
| MICRO–OPW 01–03 | Complete current reports, source, outputs and independent checkers | [New probes](../../probes/micro-opw/README.md) |

The existing Wheeler work, nine-point draft/reconstruction, older MICRO observer audit, boundary-history probes and foundation audits remain in place. The current changes add navigation and a source-recovery note to the nine-point README; they do not rewrite its theorem draft or independent reconstruction.

## Provenance

[source-manifest.json](source-manifest.json) records **398 source entries mapped to 388 distinct preserved files**, totalling about 11 MB, before counting the new navigation and MICRO–OPW files. Each entry records the original filename, destination, size and SHA-256. For files extracted from retained bundles, it also records the enclosing archive hash. Native account identifiers and local retrieval paths are not needed to verify these bytes and are not published.

Exact duplicates within a branch are collapsed. When the same filename has different bytes, the later stored item uses the unsuffixed name and the other snapshot receives a content-hash suffix. Both source entries remain in the manifest. Timestamp is a storage timestamp, not proof of scientific precedence or correctness. Original version headers can disagree with filenames; the originals are deliberately not silently edited.

All preserved source text/code/data bytes match their imported source hashes. Their scientific claims retain the evidence status established by their own development and any later explicit audit. Inconsistent claims or historical interpretations are not made current merely by preservation.

## What was checked now

* [verify_import.py](verify_import.py) checks every manifest size/hash and parses every preserved Python file using Python's source-byte decoding rules. It does not execute those historical programs.
* [validation.json](validation.json) retains the byte-integrity and syntax results, the UTF-8 BOM inventory, and the scripts that contain no computational checks.
* All six main/independent-checker commands for the three current MICRO–OPW probes were rerun from their repository location. [micro-opw-verification.json](micro-opw-verification.json) records their exit statuses. Their own result files retain the substantive checks.

Run integrity/syntax verification from the repository root:

```bash
python research/consolidation-2026-11-02/verify_import.py
```

Run current MICRO probes using their [documented commands](../../probes/micro-opw/README.md). Python 3, NumPy and SciPy are needed. Historical scripts have varying additional packages and runtime/output dependencies; no single tested environment is claimed for all of them.

## Known limits and recovery gaps

1. **Print-only PASS messages are not certificates.** RAW-12, RAW-13, RAW-14 and GROW-01, GROW-02, GROW-03A, GROW-04 contain explanatory text and print PASS without executing the described scientific checks. GROW-05 runs only a limited floating-point normalization check. The associated reports/ledgers are preserved, but a complete computational certification cannot be obtained by running those print-only files.
2. **Original run trees remain incomplete.** The available AMP 03A–L source implementations are now present, but all corresponding original basis files, generated certificates and run outputs are not. The existing independently reconstructed reference-chart verification is unchanged in scope. No new all-chart verification is claimed.
3. **XBR substage coverage is partial.** The available XBR scripts, versions and result notes are retained; sources/ is not a complete original runs/ workspace or a full set of every named substage. In particular, do not infer that every certificate referenced in the OPW3 addenda can be regenerated from this recovered set without further inputs.
4. **Do not conflate reversal conventions.** RAW/GROW's canonical support labels and OPW's literal segment lengths are not interchangeable at all sizes. The OPW overview explains the small-size example.
5. **Keep corrections with proposals.** The later LR3-onset GROW audit corrects the source/initialization issue in the preceding conditional audit. A Beta(4,4) unfolded limit has a half mean but persistent fluctuations; neither result proves criticality or a CFT. Historical AMP finite-field discovery output likewise retains its discrepancy/audit notes.
6. **No new physical claim or novelty assessment.** No full legacy series was rerun, no external proof review was conducted, and no researcher was contacted. This is source preservation, a more reviewable research map, and a rerun of the recent finite benchmarks.

Additional recovery should append a manifest entry and state whether the added file is a source implementation, reported result, generated certificate, independent reconstruction or merely a specification. These categories should remain separate.
