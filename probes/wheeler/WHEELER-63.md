# WHEELER-63 — Many-Domain Minimal Seeds / Rotation-Symmetry Audit

Date: 19 October 2026

**Status: exact structural identity + bounded computational evidence.** No all-time monotonicity theorem for D ≥ 6 is claimed.

## Setup

Use event-uniform admissible insertion, cyclic adjacency, and rotations only. A minimal seed has D=2k alternating runs, all of length two. Its ordered extension vector x has probability

`P_t(x) = product_i binom(x_i+2,2) / binom(3D+t−1,t)`.

The group C_k shifts run vectors by two positions. Reflections and colour exchange are not identified.

## Symmetry correction

The endpoint law is invariant under C_k. Conditional on its orbit, each ordered vector is equiprobable. Orbit–stabilizer and the entropy chain rule therefore give

`H_class = H_ordered − log₂ k + E[log₂ |Stab(R)|]`.

For composite k, the correction must account for every stabilizer size; a single probability of periodicity is insufficient. This is an application of standard group and entropy identities.

## Bounded scan

| D | Event counts checked | Smallest increment (bits) |
|--:|:--|--:|
| 4 | 0 through 16 | 0.2182959134 |
| 6 | 0 through 16 | 0.3564326326 |
| 8 | 0 through 12 | 0.6195272302 |
| 10 | 0 through 8 | 1.0000000000 |

All tested increments are positive. Probabilities are exact rational numbers; entropy evaluations use floating-point logarithms. The endpoint laws match quotient recursion exactly through four events. The symmetry identity also matches an independent ordered-entropy sum within 1e−11 bits.

These finite observations do not prove that every later increment is positive. WHEELER-62's all-time theorem remains specific to D=4. A larger-D proof would require bounds on changes in the expected log stabilizer strong enough to compare with ordered entropy production.

For fixed D, the ordered column bound gives a lower entropy growth of (D−1) log₂ t + O(1), and the composition count gives the matching upper order. A quotient by the fixed finite group changes entropy by at most log₂ k. This leading scaling does not establish increment-by-increment monotonicity and is consistent with established Dirichlet-multinomial asymptotics.

## Reproduction and publication role

Run `python code/wheeler/many_domain_audit.py` from the repository root.

- [Code](../../code/wheeler/many_domain_audit.py)
- [Results](../../data/wheeler/wheeler-63-results.json)
- [Working paper v0.1](../../research/wheeler/paper-v0.1/README.md)

This bounded extension supports the working paper's scope. Further open-ended probing is not a prerequisite for circulating the existing theorem and counterexample for review.
