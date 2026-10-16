# Data

Keep only datasets that are necessary for reproducibility and are not cheap to regenerate.

For each retained dataset, document:

- generating probe/code;
- parameters and random seed if applicable;
- schema/format;
- reason it is retained rather than regenerated.

Large generated arrays and binary artifacts should normally remain outside Git and be reproducible from `code/`.
