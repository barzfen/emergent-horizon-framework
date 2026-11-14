# EHF-CBB-CROSS-54 — Preparing and measuring a Bell pair on separated reversal windows

**Date** 2026-11-14 (Australia/Brisbane)  
**Status** Explicit local circuit on labelled cycles, conditional on a supplied coherent rotation and squared-amplitude readout.

## One coherent primitive

Use the buffered labelled cycles of [CROSS-52](CROSS-52-setting-isolation.md). An LR3 attempt is the unsigned local involution of [CROSS-53](CROSS-53-local-phase.md): exchange the two eligible configurations of a window, or leave an ineligible configuration alone. Its support consists of the five vertices incident to its four signs.

Add a coherent rotation at an eligible reversal window. For the ordered pair of local words -++- and +--+, with the vertex labels carried by the legal reversal, use the matrix with rows (cos(t), -sin(t)) and (sin(t), cos(t)). The same angle applies to every such pair, and the operation is the identity outside the eligible subspace. The pairs are disjoint, so this is unitary on the position-register basis. This rule is supplied. Its off-diagonal transitions follow the actual LR3 edges. Basis readout uses supplied squared amplitudes.

## Shared preparation before the settings

Start at the labelled seed with the recorder R and apparatus M both in their initial configurations. The two selected output windows start at 6 and 12+2k on the 22+4k vertex ring, where k is the number of insertion pairs per buffer. Let a transport schedule start with 6, then append (6+2j, 4+2j) for j=1 through k, then append (9+2k, 6+2k).

1. Execute the transport schedule as unsigned attempts.
2. Rotate by pi/4 at start 12+2k. The local word before rotation is -++-, so both branches have positive amplitude.
3. Attempt LR3 at start 9+2k. Its window overlaps the pulse window at one sign. This attempt fires on the rotated branch only, using the normal eligibility rule. It gets no external branch label.
4. Undo the transport by executing the same attempts in reverse order.

The two output tours are the original labelled seed and that seed with both the R and M reversals applied. Thus the prepared state is (|00>+|11>)/sqrt(2) in the two output windows, with the other vertex registers shared by both terms. The two distinct tours have been verified including every vertex label, for k=0 through 20. There is no closed-form claim about all k. The preparation uses 4k+8 sequential local operations including the coherent pulse and the relay attempt. All overlap and transport occur before either setting is chosen.

## Two independent local measurements

After preparation, choose settings independently of the initial state. During measurements use only the assigned local gates and sign reads. The two measurement supports, including the vertices needed to determine eligibility, are disjoint. Read +1 for a window matching its seed pattern and -1 for its flipped pattern. On this pair of words, the rotation followed by the basis read measures cos(2t) Z + sin(2t) X on R, and cos(2t) Z - sin(2t) X on M, because their seed words have opposite orientations in the rotation convention.

| Reader | Setting 0 rotation | Setting 1 rotation | Observables |
|---|---|---|---|
| R | 0 | pi/4 | Z, X |
| M | -pi/8 | pi/8 | (Z+X)/sqrt(2), (Z-X)/sqrt(2) |

On the prepared pair E(ZZ)=E(XX)=1 and E(ZX)=E(XZ)=0, giving CHSH correlations (1,1,1,-1)/sqrt(2). The score is 2sqrt(2). Each local outcome is unbiased, the order of measurements can be reversed, and all outcomes are kept. With the identical circuit and coherence between the two branches removed, the four correlations become (1,1,0,0)/sqrt(2) and the score drops to sqrt(2). Any classical local model with setting-independent preparation gives S<=2, by the usual pointwise CHSH bound for four deterministic local answers. See [Brunner et al., Bell nonlocality](https://arxiv.org/abs/1303.2849) for the classical and quantum benchmarks.

## What this establishes

The Bell-pair preparation can be routed through actual neighbouring LR3 interactions before the measurement settings, and both incompatible readouts use the same supplied rotation primitive on separated windows. The entangled input and generic two-bit coupling are no longer inserted as starting data. The rotation rule and squared-amplitude readout remain assumptions. If the preparation is classical, the same admissible moves generate correlated alternatives. No probability law for coherent rotation or quantum measurement follows here from the bare comparison relation.

Run `python3 research/cbb-binary/cross54_local_bell.py` from the repository root. The verifier checks labelled branch transport and disjoint measurement support, propagates amplitudes numerically and checks the analytic Bell coefficients exactly. AI assistance was used for the search, construction and verification.
