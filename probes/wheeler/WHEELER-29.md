# WHEELER-29 — Growth-Clock / Comparison-Rate Derivation Audit

> **Review correction — 18 October 2026:** The linear rate derived from insertion sites is the **growth rate R_G**, not automatically the **comparison rate R_C**. Every substitution into the Core-C comparison gap below additionally assumes a scheduler with R_C=R_G. That connection has not been derived. The finite limit is a conditional frozen-layer relaxation result, not the gap of the full growing process. See [ERRATA-01](ERRATA-01.md).

**Status: PARTIAL PASS; linear growth opportunity count derived, physical rate law still conditional**

## Question

WHEELER-28 showed that the Core-C effective continuous-time gap is

\[
\Delta_n = R_n\frac{n-1}{d_n}
=R_n\frac{2(n-1)}{n(n-3)},
\]

where

\[
d_n=\frac{n(n-3)}2
\]

and \(R_n\) is the total comparison-event rate per state in physical/internal time.

A finite nonzero large-\(n\) limit requires the critical scaling

\[
R_n\sim c n.
\]

The question is whether that scaling follows from existing EHF growth structure rather than being inserted by hand.

## Existing growth structure

For a Hamilton cycle on \(n\) labels, the existing all-slot insertion rule inserts the new label on any cycle edge.

A cycle on \(n\) vertices has exactly \(n\) edges, so the number of distinct elementary growth locations is

\[
G_n=n.
\]

Thus the framework naturally supplies a linear count of growth opportunities.

This is structural, not fitted:

\[
\boxed{G_n=n}.
\]

## Relation to the required rate

If internal time is organized so that each growth opportunity carries an \(n\)-independent attempt rate \(r\), then the total event rate associated with the growth layer is

\[
R_n=rG_n=rn.
\]

Substituting into WHEELER-28 gives

\[
\Delta_n
=rn\frac{2(n-1)}{n(n-3)}
=2r\frac{n-1}{n-3}
\longrightarrow 2r.
\]

So under fixed rate per insertion opportunity,

\[
\boxed{\Delta_\infty=2r>0}.
\]

This is exactly the critical scaling required for a finite continuum relaxation gap.

## What is and is not derived

### Derived

- the all-slot growth rule has exactly \(n\) insertion locations;
- therefore growth opportunity count is linear in system size;
- a fixed local rate per growth opportunity produces \(R_n\propto n\);
- with the exact Core-C graph gap \(n-1\), that normalization yields a finite nonzero limiting effective gap.

### Not derived

The framework does not yet contain an independently justified stochastic/quantum scheduling law saying that every growth opportunity fires at a fixed size-independent physical rate.

The distinction matters:

- **fixed total rate per state:** \(R_n=O(1)\Rightarrow\Delta_n\to0\);
- **fixed rate per growth site:** \(R_n\propto n\Rightarrow\Delta_n\to\text{constant}>0\);
- **fixed rate per admissible Core-C comparison:** \(R_n\propto d_n\sim n^2\Rightarrow\Delta_n\sim n\).

Combinatorics determines the available event counts, but not by itself which events define one unit of physical/internal time.

## Interpretation

This is stronger than choosing \(R_n\sim n\) arbitrarily: the EHF growth primitive already contains a natural linear extensive quantity, namely the number of insertion sites.

However, turning that extensive count into a clock rate requires an additional dynamical principle.

The correct current statement is therefore:

\[
\boxed{\text{EHF naturally supplies the critical linear opportunity count, but not yet the clock law.}}
\]

## Verdict

- **PASS:** growth-site count is exactly \(G_n=n\).
- **PASS:** fixed local rate per insertion site implies the critical \(R_n\sim n\) scaling.
- **PASS (conditional):** under that local-rate clock, the Core-C effective gap tends to \(2r\).
- **UNRESOLVED:** why physical/internal time should use fixed rate per growth site rather than fixed rate per state or per admissible comparison.

## Next probe

**WHEELER-30 — Clock-Naturality / Local-Rate Uniqueness Audit**

Test whether locality, relabelling covariance, compositional independence, and growth consistency force an equal fixed rate per elementary insertion site. If those principles determine the clock up to one overall constant, then the \(R_n\propto n\) normalization becomes derived rather than conditional.
