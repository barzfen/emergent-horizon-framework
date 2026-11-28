# Constant Positive Ollivier Curvature in the Even Johnson Shell Chain
## A RAF Transport-Curvature Note for the Even Johnson Reduction

### Document status

**Version:** v1 technical note  
**Layer:** RAF mathematical/combinatorial layer, with cautious EHF relevance  
**Purpose:** To document the discovery that the even Johnson shell transport chain has constant positive adjacent-shell Ollivier curvature, complementing the already established exact drift/diffusion laws.

---

## 1. Executive summary

The even Johnson reduction of RAF already had a strong exact transport structure:

\[
\text{Hamilton-cycle local admissibility}
\rightarrow
\text{even parity-sector reduction}
\rightarrow
\text{Johnson subset geometry}
\rightarrow
\text{exact shell drift/diffusion}.
\]

A new shell-level Ollivier curvature audit shows that the same shell transport chain also has a constant positive coarse Ricci curvature law.

Let

\[
\Omega_k=\{S\subset[2k-1]: |S|=k\},
\]

with the Johnson single-swap random walk. Define the shell observable

\[
h(S)=\sum_{i\in S}i.
\]

Let \(K(h,h')\) be the exact shell transition kernel induced by the microscopic Johnson walk after averaging uniformly over all states in shell \(h\). Under the line metric

\[
d(h,h')=|h-h'|,
\]

the non-lazy adjacent-shell Ollivier curvature appears to obey the exact law:

\[
\boxed{
\kappa_0(h,h+1)=\frac{2k-3}{k(k-1)}.
}
\]

This curvature is constant across every adjacent shell edge.

Probe 08 validated the formula for

\[
k=3,4,5,6,7,8,9,10,11,
\]

to machine precision.

Thus the even Johnson shell chain now has two exact physics-like transport structures:

\[
\boxed{
A(h)=\frac{2k-1}{k(k-1)}(k^2-h)
}
\]

and

\[
\boxed{
\kappa_0=\frac{2k-3}{k(k-1)}.
}
\]

In words:

> The even Johnson shell quotient has exact restoring drift and exact constant positive Ollivier curvature.

This is a clean even-side companion to the odd preserve-world square-loop result.

---

## 2. Background: the even Johnson reduction

The even side of RAF begins from Hamilton-cycle local admissibility but reduces to a Johnson-type subset geometry.

The effective state space is:

\[
\Omega_k=\{S\subset[2k-1]: |S|=k\}.
\]

The Johnson adjacency relation is single-swap adjacency:

\[
S\sim S'
\quad\Longleftrightarrow\quad
|S\cap S'|=k-1.
\]

Equivalently, one step removes one element \(a\in S\) and inserts one element \(b\notin S\):

\[
S'=(S\setminus\{a\})\cup\{b\}.
\]

The degree of the microscopic Johnson graph is:

\[
d_k=k(k-1),
\]

because:

\[
|S|=k,
\qquad
|[2k-1]\setminus S|=k-1.
\]

The central observable is the shell coordinate:

\[
h(S)=\sum_{i\in S}i.
\]

The shell range is:

\[
h_{\min}=1+2+\cdots+k=\frac{k(k+1)}{2},
\]

\[
h_{\max}=k+(k+1)+\cdots+(2k-1)=\frac{k(3k-1)}{2}.
\]

The central shell is:

\[
h_*=k^2.
\]

---

## 3. Exact shell transport kernel

The microscopic random walk chooses uniformly among all single-swap Johnson neighbours.

This induces a shell transition kernel:

\[
K(h,h')=\mathbb{P}(h(S_{t+1})=h'\mid h(S_t)=h),
\]

where the conditional distribution over states in shell \(h\) is uniform.

The kernel is exact because the shell counts and directed transition counts can be computed combinatorially:

\[
N_h=|\{S\in\Omega_k:h(S)=h\}|,
\]

\[
M(h,h')=|\{(S,S'):h(S)=h,\ h(S')=h',\ S\sim S'\}|.
\]

Then:

\[
K(h,h')=\frac{M(h,h')}{N_h k(k-1)}.
\]

The shell chain satisfies detailed balance:

\[
N_hK(h,h')=N_{h'}K(h',h).
\]

Probe 07 and Probe 08 both confirmed detailed balance to numerical precision.

---

## 4. Previously established drift law

The even Johnson shell chain has exact drift:

\[
A(h)=\mathbb{E}[h(S_{t+1})-h(S_t)\mid h(S_t)=h].
\]

The exact law is:

\[
\boxed{
A(h)=\frac{2k-1}{k(k-1)}(k^2-h).
}
\]

This is a restoring drift toward the central shell:

\[
h_*=k^2.
\]

Thus the shell chain has force-like behaviour:

\[
h<h_*\Rightarrow A(h)>0,
\]

\[
h>h_*\Rightarrow A(h)<0.
\]

The drift is not inserted as a physical force. It emerges from local Johnson admissibility and shell counting.

Probe 07 reconfirmed this formula with maximum absolute error:

\[
\approx 8.88\times10^{-16}\quad(k=8),
\]

\[
\approx 1.78\times10^{-15}\quad(k=10).
\]

Probe 08 reconfirmed the formula across \(k=3\) through \(k=11\).

---

## 5. Ollivier curvature on the shell chain

For a Markov kernel \(K\) on a metric space, Ollivier curvature compares neighbouring transition distributions by Wasserstein distance.

For shell nodes \(h\) and \(h+1\), define the idleness-\(\alpha\) measure:

\[
\mu_h^\alpha=\alpha\delta_h+(1-\alpha)K(h,\cdot).
\]

Then the adjacent-shell Ollivier curvature is:

\[
\kappa_\alpha(h,h+1)=1-\frac{W_1(\mu_h^\alpha,\mu_{h+1}^\alpha)}{d(h,h+1)}.
\]

Since the shell metric is the line metric:

\[
d(h,h+1)=1,
\]

this becomes:

\[
\kappa_\alpha(h,h+1)=1-W_1(\mu_h^\alpha,\mu_{h+1}^\alpha).
\]

Because the shell space is one-dimensional, \(W_1\) can be computed exactly from cumulative distribution differences:

\[
W_1(p,q)=\sum_x |F_p(x)-F_q(x)|.
\]

This makes the curvature audit exact up to floating-point arithmetic.

---

## 6. Probe 07: first exact audits at \(k=8\) and \(k=10\)

Probe 07 computed the exact shell kernel and adjacent-shell Ollivier curvature for \(k=8\) and \(k=10\).

## 6.1 \(k=8\)

For \(k=8\):

\[
\Omega_8=\{S\subset[15]:|S|=8\}.
\]

The run reported:

\[
\text{vertices}=6435,
\]

\[
\text{degree}=56,
\]

\[
\text{shell range}=36\dots92,
\]

\[
h_*=64.
\]

For \(\alpha=0\):

\[
\kappa_0=0.23214285714285715.
\]

This equals:

\[
\frac{2k-3}{k(k-1)}=\frac{13}{56}=0.23214285714285715.
\]

The curvature was constant across all adjacent shell edges to numerical precision.

For \(\alpha=0.5\):

\[
\kappa_{0.5}=0.13392857142857129.
\]

## 6.2 \(k=10\)

For \(k=10\):

\[
\Omega_{10}=\{S\subset[19]:|S|=10\}.
\]

The run reported:

\[
\text{vertices}=92378,
\]

\[
\text{degree}=90,
\]

\[
\text{shell range}=55\dots145,
\]

\[
h_*=100.
\]

For \(\alpha=0\):

\[
\kappa_0=0.18888888888888888.
\]

This equals:

\[
\frac{2k-3}{k(k-1)}=\frac{17}{90}=0.18888888888888888.
\]

For \(\alpha=0.25\):

\[
\kappa_{0.25}=0.1583333333333333.
\]

For \(\alpha=0.5\):

\[
\kappa_{0.5}=0.10555555555555537.
\]

Again, the curvature was constant across all adjacent shell edges to numerical precision.

---

## 7. Probe 08: formula sweep across \(k=3\) to \(k=11\)

Probe 08 swept the formula across:

\[
k=3,4,5,6,7,8,9,10,11.
\]

For each \(k\), it computed the exact shell kernel, validated the drift formula, and measured adjacent-shell Ollivier curvature.

The non-lazy curvature matched:

\[
\kappa_0=\frac{2k-3}{k(k-1)}
\]

with error below \(10^{-12}\) for every tested \(k\).

| \(k\) | vertices | shells | measured \(\kappa_0\) | formula \((2k-3)/(k(k-1))\) |
|---:|---:|---:|---:|---:|
| 3 | 10 | 7 | 0.5 | 0.5 |
| 4 | 35 | 13 | 0.416666666666667 | 0.416666666666667 |
| 5 | 126 | 21 | 0.35 | 0.35 |
| 6 | 462 | 31 | 0.3 | 0.3 |
| 7 | 1716 | 43 | 0.261904761904762 | 0.261904761904762 |
| 8 | 6435 | 57 | 0.232142857142857 | 0.232142857142857 |
| 9 | 24310 | 73 | 0.208333333333333 | 0.208333333333333 |
| 10 | 92378 | 91 | 0.188888888888889 | 0.188888888888889 |
| 11 | 352716 | 111 | 0.172727272727273 | 0.172727272727273 |

The sweep summary reported:

\[
\text{alpha=0 formula pass at tolerance }10^{-12}:\text{ true}.
\]

This provides strong computational evidence for an exact shell Ricci law.

---

## 8. The theorem candidate

### Constant Johnson Shell Ricci Law

Let

\[
\Omega_k=\{S\subset[2k-1]:|S|=k\}
\]

with Johnson single-swap random walk. Let

\[
h(S)=\sum_{i\in S}i
\]

and let \(K(h,h')\) be the exact shell transition kernel induced by the microscopic walk after averaging uniformly over each shell.

Under the line metric

\[
d(h,h')=|h-h'|,
\]

the non-lazy Ollivier curvature between adjacent shells is constant and given by:

\[
\boxed{
\kappa_0(h,h+1)=\frac{2k-3}{k(k-1)}
}
\]

for all adjacent shell pairs \(h,h+1\).

Equivalent statement:

\[
W_1(K(h,\cdot),K(h+1,\cdot))=1-\frac{2k-3}{k(k-1)}.
\]

That is:

\[
W_1(K(h,\cdot),K(h+1,\cdot))=rac{k(k-1)-(2k-3)}{k(k-1)}.
\]

Simplifying:

\[
W_1(K(h,\cdot),K(h+1,\cdot))=\frac{k^2-3k+3}{k(k-1)}.
\]

Thus neighbouring shell distributions contract by a constant amount under one shell-transition step.

---

## 9. Relationship to the exact drift law

The curvature law sits naturally beside the exact drift law.

Exact drift:

\[
A(h)=\frac{2k-1}{k(k-1)}(k^2-h).
\]

Exact non-lazy shell curvature:

\[
\kappa_0=\frac{2k-3}{k(k-1)}.
\]

Both scale like:

\[
O(k^{-1})
\]

for large \(k\).

More precisely:

\[
\frac{2k-1}{k(k-1)}\sim\frac{2}{k},
\]

\[
\frac{2k-3}{k(k-1)}\sim\frac{2}{k}.
\]

Thus the restoring drift coefficient and the adjacent-shell Ricci curvature have the same leading large-\(k\) scale.

This suggests a strong transport-geometric interpretation:

> The entropic restoring force and the positive coarse Ricci curvature are two faces of the same shell-level contraction structure.

This should become a proof target.

---

## 10. Interpretation in RAF

The even Johnson shell chain now has a three-part exact transport structure:

1. exact shell counts;
2. exact restoring drift/diffusion;
3. exact constant positive Ollivier curvature.

The RAF emergence chain is:

\[
\text{local Johnson swaps}
\rightarrow
\text{shell quotient}
\rightarrow
\text{exact Markov kernel}
\rightarrow
\text{drift/diffusion}
\rightarrow
\text{positive Ricci-like transport curvature}.
\]

This strengthens the even side because it shows that the shell quotient does not merely have a force-like drift. It has genuine contraction geometry in the sense of Ollivier transport curvature.

This is important because the raw Johnson graph is too short-cycle dense for Trugenberger-style hard-core local-cycle geometry to be the best diagnostic. The shell chain, however, is the correct coarse observable layer where the even-side physics-like behaviour lives.

So the lesson is:

> Raw Johnson geometry is not the physical-looking layer. The shell transport quotient is.

---

## 11. Even/odd curvature comparison

The new even result pairs naturally with the new odd preserve-world result.

### Even side

\[
\text{Johnson shell quotient}
\rightarrow
\text{exact restoring drift}
\rightarrow
\text{constant positive Ollivier curvature}.
\]

### Odd side

\[
\text{Odd Preserve-World}
\rightarrow
\text{square-only hard-core graph}
\rightarrow
42\text{ square-curvature species}
\rightarrow
42\text{ slot-signature families}.
\]

Thus RAF now has two curvature-like structures in complementary reductions:

\[
\boxed{
\text{Even RAF: transport Ricci curvature on shell space.}
}
\]

\[
\boxed{
\text{Odd RAF: square-loop curvature species on chamber space.}
}
\]

This is a substantial strengthening of the RAF programme because curvature-like structure is appearing in two independent ways:

- as transport contraction in the even shell quotient;
- as local square-loop classification in the odd chamber graph.

---

## 12. EHF relevance

This result is a RAF mathematical result first. It does not prove that physical gravity or spacetime curvature has been derived.

However, it is relevant to EHF because it shows that a geometry-like transport quantity can emerge from local admissible comparison after the correct quotient is taken.

The cautious EHF-compatible statement is:

> The even Johnson shell quotient produces exact force-like drift and exact positive Ollivier transport curvature from local admissible moves. This supports the EHF idea that geometry-like and force-like structures may emerge from constrained comparison, but it is not yet a physical identification with gravitational Ricci curvature.

Avoid overclaim:

> This proves gravity.

Supported claim:

> This gives a controlled finite model where local admissibility induces an exact Ricci-like transport law on a coarse observable space.

---

## 13. Open problems and proof targets

## 13.1 Prove the constant curvature law

The main proof target is:

\[
\kappa_0(h,h+1)=\frac{2k-3}{k(k-1)}.
\]

A likely proof path uses the one-dimensional Wasserstein formula:

\[
W_1(p,q)=\sum_x |F_p(x)-F_q(x)|,
\]

where \(p=K(h,\cdot)\) and \(q=K(h+1,\cdot)\).

Need to show:

\[
\sum_x |F_{K(h,\cdot)}(x)-F_{K(h+1,\cdot)}(x)|
=
\frac{k^2-3k+3}{k(k-1)}
\]

independently of \(h\).

## 13.2 Relate curvature to drift coefficient

The drift coefficient is:

\[
\lambda_A=\frac{2k-1}{k(k-1)}.
\]

The curvature coefficient is:

\[
\kappa_0=\frac{2k-3}{k(k-1)}.
\]

Their difference is:

\[
\lambda_A-\kappa_0=\frac{2}{k(k-1)}.
\]

Open problem:

> Explain why the drift contraction and Ollivier contraction differ by exactly \(2/[k(k-1)]\).

## 13.3 Derive idleness-\(\alpha\) formula

Probe 07 and Probe 08 also measured constant curvature for idleness values \(\alpha=0.25\) and \(\alpha=0.5\).

Open problem:

> Find the exact formula for \(\kappa_\alpha\) as a function of \(k\) and \(\alpha\).

Observed examples:

For \(k=10\):

\[
\kappa_0=0.18888888888888888,
\]

\[
\kappa_{0.25}=0.1583333333333333,
\]

\[
\kappa_{0.5}=0.10555555555555537.
\]

This is not simply \((1-\alpha)\kappa_0\), so the idleness dependence deserves separate derivation.

## 13.4 Compare with full Johnson graph Ollivier curvature

The raw Johnson graph has known high symmetry and strong short-cycle density. Probe 01 showed that it is not in a hard-core local-cycle regime.

Open problem:

> Compare full Johnson graph Ollivier curvature with shell-quotient Ollivier curvature, and determine precisely what is gained or lost by shell coarse-graining.

## 13.5 Compare with odd packet MSM curvature

The odd preserve-world has a 16-state Boolean packet MSM.

Open problem:

> Compute Ollivier curvature on the odd Boolean packet MSM and compare with the even Johnson shell chain.

This may reveal whether the slow staggered boundary mode corresponds to low or negative transport curvature directions.

---

## 14. Conservative statement without EHF interpretation

A conservative graph/Markov-chain statement is:

> Let \(\Omega_k\) be the set of \(k\)-subsets of \([2k-1]\), equipped with the regular Johnson random walk. Let \(h(S)=\sum_{i\in S}i\), and let \(K(h,h')\) be the shell transition kernel obtained by averaging the walk over states with fixed \(h\). Numerical exact enumeration for \(3\le k\le11\) shows that the non-lazy Ollivier curvature of the shell chain between every adjacent pair \(h,h+1\), under the line metric, is constant and equal to \((2k-3)/(k(k-1))\). The same shell kernel satisfies the exact drift law \(A(h)=((2k-1)/(k(k-1)))(k^2-h)\).

This statement requires no physical interpretation.

---

## 15. Summary

The even Johnson shell chain now has an exact transport-curvature profile.

Known before:

\[
A(h)=\frac{2k-1}{k(k-1)}(k^2-h).
\]

Newly audited:

\[
\kappa_0(h,h+1)=\frac{2k-3}{k(k-1)}.
\]

The curvature is constant across shell space and positive for all \(k\ge3\).

Probe 08 validated the formula for \(k=3\) through \(k=11\) to machine precision.

This provides a clean even-side counterpart to the odd preserve-world square-loop result:

\[
\text{Even side: exact Ricci-like shell transport curvature.}
\]

\[
\text{Odd side: exact square-loop chamber curvature species.}
\]

Together, these results materially strengthen RAF’s claim that constrained local admissible comparison can generate geometry-like and force-like structures after the correct quotient or coarse-graining is applied.

