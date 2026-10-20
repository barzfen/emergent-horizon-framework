# EHF-HODGE-04 — Explicit Transport-Potential Proof Audit

Date: 2026-10-20 (Australia/Brisbane)

**Status: PASS — C2 proved within the specified MICRO model by an
explicit integer potential. C1 remains conjectural.**

Base commit: `210500a8f1b6ef451f1594438fb072509636b80f`.

## Main result

The [complete proof](../../formal/hodge/TRANSPORT-POTENTIAL.md) constructs
an integer-valued state function F such that every admissible edge obeys

`dF=(n-2D)j-2(n-2m)kappa.`

This holds for every n>=5, not only the scanned sizes.
Summing around a closed path proves the C2 winding relation.
The proof does not assume one-dimensional first homology.

## Construction in plain language

Remove the first two bits of each run and mark the excess bits.
A legal move shifts one marked bit four sites without passing any
other marker, so the cyclic order of marker colours is conserved.

Give a 1 marker weight equal to the number of 0 markers, and a 0
marker the negative of the number of 1 markers. The total weight
is zero, eliminating dependence on a common positional offset.

Use the invariant cyclic colour word to choose where to unwrap
the ring. If that word repeats, all equivalent canonical cuts
give the same weighted sum. That sum is F.

An elementary move changes F by exactly the weighted transport
difference in the displayed formula. This is a state formula,
not a potential reconstructed by integrating along a spanning tree.

## Proof gates resolved

| Gate | Resolution |
|---|---|
| Does marker creation preserve the state information needed for F? | F is a deterministic function of the original word; markers add no dynamics |
| What happens to markers under a move? | One opposite-colour marker moves four sites; all others remain fixed |
| Can cyclic marker labels become inconsistent? | No marker passes another |
| What if the marker-colour word repeats? | Equivalent cuts enclose zero total weight |
| What happens at the ring seam? | Common lifts have zero effect; marker motion is tracked on the unwrapped ring |
| Does the D=2 case require distinct donor and receiver runs? | No; comparison of discarded pairs gives the same marker motion |
| Does the proof require C1? | No |
| Does it import the recent OpenAI Hodge claims? | No |

## Exact implementation audit

A separate standard-library implementation enumerates all valid words
through n=18 and checks the potential identity on every admissible
undirected edge, with the direction fixed by word order.

It additionally checks:
- Exact marker counts E_0 and E_1.
- Single-marker displacement and no passing.
- Invariance of the cyclic colour word.
- Equality of F across all cuts giving the canonical word.
- Invariance of F under the generating cyclic relabelling.
- The local weighted-displacement identity.

All arithmetic is integer arithmetic. No face-rank calculation, SVD,
least-squares fit or floating-point tolerance is used.

| n | States | Edges checked | Edges with nonzero dF |
|---|---:|---:|---:|
| 5 | 12 | 10 | 0 |
| 6 | 20 | 12 | 0 |
| 7 | 30 | 14 | 0 |
| 8 | 46 | 16 | 0 |
| 9 | 74 | 36 | 0 |
| 10 | 122 | 80 | 20 |
| 11 | 200 | 154 | 66 |
| 12 | 324 | 264 | 144 |
| 13 | 522 | 442 | 260 |
| 14 | 842 | 756 | 476 |
| 15 | 1362 | 1320 | 900 |
| 16 | 2206 | 2304 | 1696 |
| 17 | 3572 | 3978 | 3094 |
| 18 | 5780 | 6804 | 5508 |

Total: 15,112 states and 16,190 edges. All checks pass.
The audit includes 3,952 marker seam-crossing edges and 226 states
with a mixed-colour periodic marker signature.

### Nonzero edge example

At n=10, take

`0001100111 -> 0011000111`

by the move at i=2. Here m=5,D=4,E=2,
j=-2 and kappa=-1. The explicit formula gives F=7 at the source
and F=3 at the target. Thus dF=-4=2(-2)-0, as required.

The disappearing 0 marker at position 2 reappears at position 6,
a signed +4 displacement with weight -1.

## Consequences now proved

- C2 holds in integral H^1 for the stated square complex, and hence over Q.
- Balanced moving components have exact binary-transport cochain j.
- On an open path, the weighted transport discrepancy depends only on
  its endpoint values of F.
- Boundary winding obeys a necessary arithmetic divisibility condition.
- For any fixed positive cochain metric, harmonic representatives obey
  the corresponding proportionality relation.

The full derivations and scope are in the proof note.

## Evidence status

- **PROVED within this model:** the explicit potential theorem and its
  listed corollaries.
- **COMPUTATIONAL, exact finite:** independent state-formula checks
  through n=18.
- **CONJECTURE:** C1, the all-size one-direction component classification.
- **UNESTABLISHED:** broader novelty, an independent proof review,
  formal verification, complete component invariants and growth maps.
- **UNCHANGED:** the algebraic-geometric bridge remains unestablished;
  the parity obstruction in LITERATURE-01 still applies.

## Reproduce

```sh
python code/hodge/hodge_04_audit.py --output data/hodge/hodge-04-results.json
```

[Code](../../code/hodge/hodge_04_audit.py).
[Retained results](../../data/hodge/hodge-04-results.json).
Python 3.10+; no third-party dependencies. Default --max-n is 18.

## Next: HODGE-05 — Component invariant and classification audit

Use the conserved cyclic excess-marker word to investigate C1.
Determine what information is still needed about root phase and
marker realizability before claiming it classifies components.
A proof of C2 does not establish that every component has only one
homology direction.
