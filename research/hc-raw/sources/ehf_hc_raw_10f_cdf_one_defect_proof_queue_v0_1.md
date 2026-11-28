# EHF-HC-RAW-10F — CDF One-Defect Proof Queue v0.1

## Status

**Queued theorem-completion side target. Do not interrupt RAW-11.**

RAW-10E reduced the all-\(k\) linear-shell Ollivier theorem to:

\[
C_h(x)=F_{K(h,\cdot)}(x)-F_{K(h+1,\cdot)}(x),
\]

with the already proved local identity:

\[
C_h(h)=-\frac1{d},
\qquad
d=k(k-1).
\]

Exact rational certification through \(k=11\) found:

\[
C_h(x)\ge0
\qquad
(x\ne h).
\]

## Target theorem

For every \(k\ge3\), every adjacent birth-rank shell pair \(h,h+1\), and every threshold \(x\ne h\),

\[
\boxed{
F_{K(h,\cdot)}(x)\ge F_{K(h+1,\cdot)}(x).
}
\]

Equivalently, the adjacent-shell CDF difference has exactly one negative interval:

\[
\boxed{
C_h(h)=-1/d,
\qquad
C_h(x)\ge0\ (x\ne h).
}
\]

## Consequences

The lemma immediately gives:

\[
\kappa_0^{\rm shell}
=
\frac{2k-3}{k(k-1)}
\]

for all \(k\), and the exact piecewise idleness law from RAW-10E.

## Candidate proof routes

1. injection/coupling between threshold-crossing swaps from shells \(h+1\) and \(h\);
2. generating-function coefficient inequalities;
3. monotone transport after removing the single forced rank defect;
4. use the exact directed-displacement reconstruction structure from RAW-10D;
5. representation-theoretic or total-positivity properties of the \(q\)-binomial shell counts.

Do not claim the all-\(k\) shell theorem until this sign lemma is proved.
