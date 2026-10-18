# WHEELER-49 — Observer Thermodynamics / Record-Erasure Audit

**Corrected 18 October 2026 after [REVIEW-01](../../research/wheeler/REVIEW-01.md).**

**Status: CONDITIONAL compatibility with information thermodynamics; previous capacity-based reset lower bound withdrawn.**

## Question

Does retaining, updating and resetting a sufficient observer record force thermodynamic dissipation, and does it change the memory/processing tradeoff?

## Separate three quantities

1. Storage capacity: an exact counter for values 0,...,n requires `M=ceil(log2(n+1))` bits.
2. Uncertainty: a counter distribution P has Shannon entropy `H_bits(P) <= log2(n+1) <= M`.
3. Dissipation: heat depends on entropy change and the physical reset protocol, not merely on M.

The previous argument inferred `Q_reset >= M k_B T ln 2` from “at most M bits of information.” That inference was incorrect and is withdrawn.

## Correct conditional Landauer statement

In the standard initially uncorrelated memory/thermal-bath setting, resetting the classical memory distribution P to a known value gives the entropy lower bound

`Q_reset >= k_B T ln(2) H_bits(P)`.

This imports an external physical principle; EHF has not derived the bath, temperature or physical implementation. With useful side information, correlations or different Hamiltonian constraints, the appropriate thermodynamic accounting must be specified.

An n=21 counter uses five bits but has only 22 valid values. If uniform on those values, its uncertainty is `log2(22) ~= 4.4594` bits. If its value is known, its Shannon uncertainty is zero despite the five-bit representation. Zero entropy decrease supplies no positive compulsory heat from this bound; it does not guarantee that a particular implementation dissipates no heat.

Thus O(log n) storage bounds the counter's possible entropy contribution from above. It is neither a universal positive lower bound on heat nor an upper bound on actual implementation dissipation.

## Updates and discarded records

An increment controlled by a retained event bit can be embedded in a reversible transformation. This does not justify ignoring the event bit or temporary records when the complete device is reset. An update with inputs discarded may be many-to-one even if the counter alone is small.

The accounting must say which information remains in the observer, substrate, environment or auxiliary register. Reversible computation can avoid compulsory logical erasure in suitable implementations, but a small output register alone does not prove that the whole computation is reversible.

## Architectural implication

WHEELER-48's operational tradeoff between storing a sufficient statistic and repeatedly reconstructing it remains conditional on its chosen memory and processing prices. It cannot be upgraded to an intrinsic thermodynamic preference by replacing storage capacity with erased entropy.

To evaluate a concrete reset cycle, specify the joint initial memory distribution, accessible side information, final logical state, bath assumptions and processing history. Without those, no unique thermodynamic cost has been obtained.

## Verdict

- RETAIN: a size counter does not automatically dissipate one bit's Landauer cost per event.
- RETAIN: sufficient-statistic storage can reduce computational work in the stated access model.
- CORRECTED: heat bounds involve entropy decrease, not allocated bit count.
- WITHDRAWN: a universal logarithmic positive reset-heat lower bound based on counter capacity alone.
- NOT DERIVED: an intrinsic EHF thermodynamic law.

## Relation to later probes

WHEELER-50–54 define combinatorial and stochastic entropies directly. Those results do not depend on the withdrawn reset bound and remain distinct from physical thermodynamics.

## Source

David Reeb and Michael M. Wolf, *An improved Landauer Principle with finite-size corrections*, New Journal of Physics 16, 103011 (2014), especially the entropy-decrease formulation and its assumptions: https://arxiv.org/abs/1306.4352 .

The pre-correction report is preserved in Git history at commit `106783d120bf5895cdcd67c8086ab382feebfb8c`.
