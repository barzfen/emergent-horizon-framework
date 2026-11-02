# EHF-OPW3-AUDIT-05
## LR3-Native Equitable Packet Reconstruction

Audit-02 showed that the four LR3 active signatures and the legacy sixteen
joint LR3/LR2 signatures are useful observables but are not exact Markov
lumpings. This probe computes the coarsest exact equitable refinement of four
starting partitions inside every connected chamber.

For a partition \(\mathcal P\), define

\[
N_{ab}(x)=\#\{y\sim x:y\in P_b\}.
\]

The partition is equitable when \(N_{ab}(x)\) is independent of the chosen
\(x\in P_a\). Then adjacency and the simple random walk descend exactly to the
quotient.

The starting partitions are:

1. `STRUCTURAL`: one initial cell;
2. `LR3_SIGNATURE`: the four foundational LR3 signatures;
3. `LR2_SIGNATURE`: control partition;
4. `JOINT_SIGNATURE`: the LR3 × LR2 sixteen-signature crosswalk.

The probe records final cell counts, compression ratios, exact quotient
transition probabilities, stationary masses, detailed balance, and the
stochastic action

\[
A_{ab}=-\log P_{ab}.
\]

Run:

```bash
python3 scripts/ehf_opw3_audit_05_equitable_packet_reconstruction.py \
  --base-script scripts/ehf_opw3_audit_01_definition_lock_structural_census.py \
  --ns 5,7,9 \
  --graphs OPW3,OPW23 \
  --initial-partitions STRUCTURAL,LR3_SIGNATURE,LR2_SIGNATURE,JOINT_SIGNATURE \
  --out-dir runs/ehf_opw3_audit_05 \
  --strict
```

A pass establishes exact finite stochastic quotients only. It does not assign
quantum phases, physical time, masses, or particle identities.
