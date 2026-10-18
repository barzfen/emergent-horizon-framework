# WHEELER-51 — Dynamic Measure / Shannon-Entropy Audit

## Goal

Replace the uniform compatible-state count from WHEELER-50 with the actual observer-level growth measure and ask whether an entropy monotone survives.

We work with the zero-cost cyclic binary growth process and observer macrostate

\[
y=(N_1,D).
\]

Write \(m=N_1\) and \(D=2k\).

## Exact macro growth kernel

From WHEELER-36, the numbers of admissible zero- and one-insertions are

\[
q_0=n-m+k,
\qquad
q_1=m+k,
\]

with total

\[
q_0+q_1=n+2k=n+D.
\]

Under uniform choice among admissible growth events, the observer-level transition probabilities are therefore

\[
K_n^{(k)}(m\to m)=\frac{n-m+k}{n+2k},
\]

\[
K_n^{(k)}(m\to m+1)=\frac{m+k}{n+2k}.
\]

The hidden sector \(D=2k\) is preserved.

## Column-sum structure

For an interior output value \(j\), the total incoming column weight is

\[
K_n^{(k)}(j\to j)+K_n^{(k)}(j-1\to j)
\]

\[
=\frac{n-j+k}{n+2k}+\frac{j-1+k}{n+2k}
\]

\[
=1-\frac{1}{n+2k}<1.
\]

Boundary columns have even smaller incoming weight.

Thus the macro transition matrix is row-stochastic and column-substochastic:

\[
\sum_y K(x,y)=1,
\qquad
\sum_x K(x,y)\le1.
\]

Equivalently, the channel is doubly substochastic.

## Shannon entropy monotonicity

For a probability vector \(p\) over the size-\(n\) observer macrostates, let

\[
q=pK_n.
\]

A doubly-substochastic stochastic map sends \(p\) to a distribution majorized by \(p\) after padding the shorter vector with zeros. Since Shannon entropy is Schur-concave,

\[
\boxed{H(q)\ge H(p).}
\]

Therefore the actual observer-level dynamical measure satisfies a Shannon-entropy monotonicity law for every input distribution, not merely for the uniform compatible-state measure used in WHEELER-50.

For \(D>0\), every feasible macrostate has both insertion branches available, and the channel genuinely splits probability mass. The generic behavior is strict increase. For \(D=0\), all-zero and all-one sectors evolve deterministically and entropy can remain unchanged.

## Relative entropy contraction

For any two observer distributions \(p\) and \(r\) propagated through the same growth channel,

\[
q=pK_n,
\qquad
s=rK_n,
\]

the data-processing inequality gives

\[
\boxed{D_{\rm KL}(q\Vert s)\le D_{\rm KL}(p\Vert r).}
\]

This contraction is generic to stochastic coarse-grained dynamics and should not be mistaken for a uniquely EHF-specific theorem. What is specific here is the exact EHF growth kernel and its column-substochastic structure, which yields Shannon-entropy monotonicity.

## Relation to WHEELER-50

WHEELER-50 established the combinatorial multiplicity entropy

\[
S_\pi=\log\Omega(n,m,D)
\]

and proved that \(\Omega\) increases under every nontrivial zero-cost growth step.

WHEELER-51 now shows that the entropy result is not merely an artifact of treating compatible microstates uniformly. The induced observer-level probability law itself satisfies

\[
H_{n+1}\ge H_n.
\]

So the framework currently has two distinct internal monotones in this restricted model:

1. compatible-state multiplicity \(\log\Omega\), and
2. Shannon entropy of the actual observer macro-distribution.

These should remain conceptually separate.

## Computational checks

Brute-force propagation of the full zero-cost microstate growth process for small \(n\) was used as a consistency check. Uniform layer distributions showed increasing microstate and macrostate Shannon entropy across the tested sizes. Random macro-distribution tests within fixed \(D\) did not produce entropy decreases, in agreement with the analytic column-substochastic proof.

The full microstate growth channel also appeared column-substochastic in the tested range, suggesting a possible stronger microstate-level Shannon monotonicity theorem. That stronger statement is not proved here.

## Verdict

- **PROVED:** exact observer macro transition kernel.
- **PROVED:** macro growth channel is column-substochastic.
- **PROVED:** Shannon entropy of the observer macro-distribution is nondecreasing under one growth step.
- **PROVED / STANDARD:** KL divergence contracts under the same stochastic channel by data processing.
- **COMPUTATIONAL:** full microstate channel also appears entropy-nondecreasing in tested small sizes.
- **OPEN:** prove or refute full microstate-level column-substochasticity for all \(n\).

## Interpretation discipline

This is an internal information-theoretic monotonicity result for the defined growth process. It is not yet a derivation of thermodynamic entropy, heat, temperature, equilibrium, or the physical second law.

The next natural probe is to test the stronger microscopic statement directly:

**WHEELER-52 — Microstate-Channel / Majorization Audit**

Determine whether the full zero-cost growth channel is column-substochastic for all \(n\), and if so prove microstate Shannon entropy monotonicity before observer coarse-graining.
