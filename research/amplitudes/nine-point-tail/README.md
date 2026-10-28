# Nine-point odd-to-even tail theorem

[Original theorem draft v1.5](theorem-v1.5.md) — Barry Fensom, 17 July 2026. The supplied draft is preserved byte-for-byte.

This package studies signed, adjacency-restricted deletion of label 9 from fibre-local Parke–Taylor relations. Across the 35 source fibres, the transmitted ranks are 0, 2, 8, 9, 14 and 15. After transport to a reference fibre, the images form six subspaces with the lattice described in the draft.

## Verification status

The accompanying independent reconstruction uses exact rational arithmetic and standard-library Python. It checks the reference (1,9) chart: all 35 fibres, the rank law, the six-space collapse, the subspace lattice and character multiplicities. It also checks 363 image generators with source lifts, exact collision-residue evaluations and common-numerator MHV evaluations.

The original draft contains broader claims. This reconstruction does **not** independently recertify all 72 anchor/deletion charts, minimum-support claims, the seven-seed construction or all 21 templates. The original draft and the scope of this later computational check must be distinguished. Neither establishes new physical dynamics or a demonstrated application to scalar scaffolding.

## Reproduce

From the repository root, run:

```sh
python3 research/amplitudes/nine-point-tail/reconstruct.py
```

The script asserts its exact checks and writes `results.json` and `certificates.json` beside itself. The latter contains the generated source lifts and reference images and is omitted from version control because it is reproducible. `results.json` includes an elapsed-time field that varies between runs.

No third-party Python packages are required. The retained results document the computational check; the theorem's full statement and conventions are in the original draft.
