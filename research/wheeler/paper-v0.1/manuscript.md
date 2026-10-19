---
title: "Entropy and Symmetry in Constrained Cyclic Growth"
author: "Barry Fensom — EHF research working draft"
date: "Version 0.1 · 19 October 2026"
geometry: margin=27mm
fontsize: 11pt
colorlinks: true
linkcolor: blue
urlcolor: blue
header-includes:
  - \usepackage{amsmath,amssymb,booktabs}
  - \usepackage{microtype}
  - \setlength{\emergencystretch}{3em}
---

**Status.** Working draft for mathematical review. The results below have explicit proofs and reproducible arithmetic checks, but have not received independent external review. Literature comparison remains incomplete, particularly with the full classification in Nakata [2]. No priority claim is made. This document consolidates results developed in the Wheeler probe series; it does not present a physical theory.

**AI assistance.** ChatGPT assisted with derivations, computational searches, code and exposition. Authorship details, acknowledgements and any submission-specific AI disclosure require author review before journal submission.

# Abstract

We study binary cyclic words with no isolated symbol, grown by choosing uniformly among admissible labelled insertion events. In a sector with a fixed even number of runs, the ordered run lengths evolve as a classical Pólya urn. The process descends to rotation classes, while uniform sampling of distinct rooted successor words generally does not. Although rooted Shannon entropy and an inherited orbit-weighted entropy are nondecreasing, ordinary Shannon entropy on rotation classes need not be. We give an exact two-source counterexample and a counterexample arising without conditioning from a single deterministic seed. For pair-symmetric four-run seeds, a simple periodicity correction relates ordered and quotient entropies. For the minimal seed with four runs of length two, we evaluate this correction and prove strict quotient-entropy increase at every event. We also give elementary logarithmic entropy bounds, while identifying the leading scaling as a consequence of established Dirichlet-multinomial asymptotics. A bounded extension to larger minimal seeds is reported separately as finite computational evidence.

# 1. Introduction and contribution

A growth process can increase the number of configurations while failing to increase the Shannon entropy of an observed state. Two distinctions matter: different events can produce the same configuration, and different representations can describe the same unlabelled object. In a growing cyclic system, the multiplicities associated with rotational symmetry can change between layers.

Our aim is to separate these effects in an exactly tractable model. The strongest conclusions are a negative and a positive result for the same event-uniform kernel: entropy can decrease along the unconditioned endpoint laws from one seed, but is strictly increasing at every event from the minimal four-run seed.

The urn representation, entropy chain rule and symmetry reduction are established tools. The candidate model-specific contributions are the explicit quotient-entropy counterexamples and the all-time minimal-seed theorem with its exact periodicity bound. The logarithmic scaling is not claimed as a new general entropy law.

## 1.1. Related work and remaining comparison

Mallows and Shepp [1] choose a gap uniformly and insert white if and only if both neighbouring beads are black. Their rule allows isolated white beads and changes the run count. The process below forbids isolated beads of either colour, preserves the run count, and samples admissible gap-colour events rather than gaps alone. Hackl and Prodinger [3] analyze the Mallows–Shepp rule by generating functions.

Nakata [2] classifies more general necklace processes using Pólya urns and studies runs. Its publisher abstract establishes close relevance; its full classification was not available for this draft. We therefore do not claim that the constrained model or its urn reduction is absent from that work. A full comparison remains necessary.

Turowski, Jacquet and Szpankowski [4, Theorem 2] give detailed Dirichlet-multinomial entropy asymptotics with leading term $(d-1)\log t$ for $d$ categories. Symmetry-based Markov reductions have an established literature [5,6]. Geiger and Temmel [7] study lumping and entropy-rate preservation for finite-state chains; our quantity is instead the entropy of the current state in a growing, nonstationary process. These differences of setting should not be read as priority claims.

# 2. Model and exact growth law

A rooted state is a tuple $w=(w_0,\ldots,w_{n-1})\in\{0,1\}^n$, $n\ge4$, with cyclic adjacency and no cyclic occurrence of 010 or 101. A nonhomogeneous state consists of an even number $D\ge2$ of alternating runs, each of length at least two. Homogeneous states have $D=0$ and evolve deterministically at the level of words.

An event $(i,b)$, with $0\le i<n$ and $b\in\{0,1\}$, inserts $b$ before position $i$:

$$w\longmapsto w[:i]+(b,)+w[i:].$$

An event is admissible if the resulting cyclic word still has no isolated symbol. Inserting before position zero makes the new bead the first entry; other insertions leave the original first entry first. There is no additional insertion position $n$ in this rooted convention.

Let $K_n(w,v)$ be the number of admissible events producing rooted target $v$, divided by the total admissible event count. All entropy expressions use base-two logarithms. Time $t$ is the number of insertion events.

**Lemma 2.1 (run extension).** Admissible growth preserves $D$. A run of length $\ell$ has exactly $\ell+1$ events extending it. Consequently there are $n+D$ admissible events from a nonhomogeneous word.

*Proof.* Inserting the opposite symbol inside a run creates an isolated symbol and is forbidden. At a boundary, either neighbouring symbol may be inserted and simply extends its run. A run has $\ell-1$ internal gaps and its two boundary gaps, giving $\ell+1$ extensions. Summing over runs gives $n+D$. The same argument shows that no run is created or removed. $\square$

Label the initial runs in cyclic order, starting with a zero-run, and let their lengths be $\ell_1,\ldots,\ell_D$. If run $i$ has received $x_i$ extensions, then

$$P(i\text{ is extended}\mid x)=\frac{\ell_i+x_i+1}{n_0+D+t},\qquad \sum_i x_i=t.$$

Thus the ordered process is a Pólya urn with parameters $\alpha_i=\ell_i+1$. Its endpoint law is

$$P_t(x)=\frac{\prod_{i=1}^{D}\binom{\ell_i+x_i}{x_i}}{\binom{n_0+D+t-1}{t}},\qquad x_i\ge0,\quad\sum_i x_i=t.\tag{1}$$

To verify (1), multiply the sequential probabilities for a fixed sequence of run selections, then multiply by $t!/\prod_i x_i!$ for the sequences sharing the same counts. Normalization also follows by multiplying the generating functions $(1-z)^{-\alpha_i}$.

# 3. Rotation classes and sampling conventions

Let $[w]$ be the rotation class of $w$. We identify rotations only, not reflections or colour exchange. If the run vector starts with a zero-run, rotation equivalence is generated by shifting two run positions. The acting group is $C_{D/2}$.

**Proposition 3.1 (quotient closure).** The event-uniform kernel has a well-defined quotient kernel

$$Q_n(A,B)=\sum_{v\in B}K_n(w,v),\qquad w\in A,$$

independent of the representative $w$.

*Proof.* Rotating a source maps insertion gaps bijectively to the corresponding gaps and preserves the inserted colour and admissibility. Corresponding targets are rotations of each other. All event weights are $1/(n+D)$, independently of the representative. Summing over target classes proves the claim. $\square$

This is strong lumpability of the layer-to-layer kernels. The quotient process is Markov for every initial law. Fixed normalized kernels also define consistent finite-history laws; extending the horizon does not change earlier marginals.

For a run representative $a=(a_1,\ldots,a_D)$ the quotient row can be calculated directly:

$$Q_n([a],B)=\frac{1}{n+D}\sum_{j:[a+e_j]=B}(a_j+1).\tag{2}$$

Symmetry-related extensions retain their event multiplicity.

**Example 3.2 (rooted state-uniform sampling fails closure).** The words 00111 and 11100 represent the same cycle. Under event-uniform growth, the probabilities of classes [000111] and [001111] are respectively $3/7$ and $4/7$ from either word. If instead each distinct rooted successor word receives equal probability, they are $1/3,2/3$ from 00111 and $2/3,1/3$ from 11100. Thus rooted state-uniform sampling does not define a representative-independent quotient kernel.

This example does not imply unique selection of event-uniformity. Equal weighting of distinct quotient targets defines another coherent kernel, as do rotation-invariant event weights. It establishes a distinction between the specified prescriptions.

# 4. Entropy that does survive the quotient

**Lemma 4.1 (column bound).** If a row-stochastic kernel has column sums at most $c>0$, then

$$H(pK)-H(p)\ge-\log_2 c.$$

*Proof.* Let $s_y=\sum_xK(x,y)$ and $q_y=\sum_xp_xK(x,y)$. Convexity of $u\ln u$, with weights $K(x,y)/s_y$, gives

$$q_y\ln(q_y/s_y)\le\sum_x K(x,y)p_x\ln p_x.$$

Summing and using the row sums yields $H(q)-H(p)\ge-\sum_yq_y\log_2s_y\ge-\log_2c$. Unreachable columns contribute zero. $\square$

For a rooted target of size $n+1$, deleting the inserted bead at one of the $n$ allowed insertion indices reconstructs each incoming event. All valid predecessors have the same $D$, so its column sum is at most $n/(n+D)\le1$. Hence rooted entropy is nondecreasing.

Let $s(A)$ be the number of distinct rooted words in orbit $A$. Define

$$S_s(P)=H(P)+\sum_A P(A)\log_2s(A).\tag{3}$$

This is entropy relative to inherited, unnormalized counting weights. It is also the maximum rooted entropy among lifts of $P$.

**Proposition 4.2.** For event-uniform growth, $S_s(PQ)\ge S_s(P)$.

*Proof.* Lift $P$ uniformly inside each source orbit, obtaining rooted entropy $S_s(P)$. Rooted entropy does not decrease. The output has class marginal $PQ$ by Proposition 3.1, and its rooted entropy is at most the maximum lift entropy $S_s(PQ)$. Combine the inequalities. $\square$

This does not establish monotonicity of ordinary $H(P)$. The orbit-size term changes with both size and periodicity. Nor should (3) be identified with thermodynamic entropy without an additional physical model.

# 5. Ordinary quotient entropy can decrease

## 5.1. An exact two-source witness

In four-run notation, prepare $A=(2,100,2,100)$ with probability $2/3$ and $B=(2,99,2,101)$ with probability $1/3$. Both have size 204 and four domain walls. Formula (2) gives five target probabilities, in the order specified below:

| Target representative | Probability |
|:--|--:|
| $(2,100,2,101)$ | $21/26$ |
| $(3,100,2,100)$ | $1/52$ |
| $(2,99,2,102)$ | $17/104$ |
| $(3,99,2,101)$ | $1/208$ |
| $(2,99,3,101)$ | $1/208$ |

Thus

$$H_{\rm in}=0.9182958340544895\ldots,\qquad H_{\rm out}=0.8596557583846341\ldots.$$

The negative difference is certified without approximate logarithms: after multiplying by a common denominator and exponentiating, $H_{\rm out}<H_{\rm in}$ is equivalent to

$$2^{1274}13^{624}<3^{1128}7^{504}17^{102}.\tag{4}$$

The supplied code verifies this integer inequality and an independent rational power-product formulation.

## 5.2. A single-seed witness without conditioning

**Theorem 5.1.** Start from the single rotation class $(2,100,2,100)$ and retain its complete unconditioned endpoint law. Its ordinary class entropy decreases between event counts two and three.

*Proof.* Apply (1) and group run vectors under pair exchange. The resulting distributions are given in Appendix A. They have six and ten classes, respectively, and satisfy

$$H(C_2)=1.3213373585771321\ldots,\qquad H(C_3)=1.3076635638158981\ldots.$$

The exact rational enclosure

$$-0.013673795\le H(C_3)-H(C_2)\le-0.013673794<0\tag{5}$$

is reproduced by the logarithm-bound algorithm in Appendix B. Every endpoint is retained with its actual probability. $\square$

This is neither a smallest-size claim nor an optimization of the decrease. It disproves universal monotonicity even when the initial state is deterministic.

## 5.3. A limiting family

For seeds $(2,L,2,L)$, with event count fixed and $L\to\infty$, extension of a short run has vanishing probability. The two long-run selection probabilities approach $1/2$. At time two the binomial extension counts fold under pair exchange to probabilities $(1/2,1/2)$; at time three they fold to $(1/4,3/4)$. Continuity on these finite supports gives

$$\lim_{L\to\infty}\bigl[H(C_3)-H(C_2)\bigr]=h_2(1/4)-1=-0.1887218755\ldots.$$

Consequently every sufficiently large integer $L$ has a decrease. We do not identify the smallest threshold here.

# 6. Exact symmetry correction

For a pair-symmetric seed $(a,b,a,b)$, the law of the ordered run vector $R_t$ is invariant under exchanging the two run pairs. A class has two equiprobable representatives unless its run pattern repeats, in which case it has one. If $\rho_t$ is the probability of a repeated pattern, the entropy chain rule gives

$$H(C_t)=H(R_t)-1+\rho_t.\tag{6}$$

For the witness in Theorem 5.1,

$$\rho_2=\frac{5105}{10868},\qquad \rho_3=0,$$

while $H(R_3)-H(R_2)=0.4560538460\ldots$ bits. The loss of the periodicity correction exceeds that positive ordered-run gain, giving (5). Odd total size cannot have a twofold repeated run pattern.

More generally, for a group-invariant law under a finite group $G$,

$$H(\text{orbit})=H(\text{labelled state})-\log_2|G|+\mathbb E\log_2|\operatorname{Stab}(R)|.\tag{7}$$

Equation (7) follows because conditional on an orbit the labelled state is uniform, and the orbit size is $|G|/|\operatorname{Stab}(R)|$. Group invariance is essential for this exact form; without it one retains the conditional-entropy identity and the bound by $\log_2|G|$.

# 7. Strict monotonicity for the minimal four-run seed

**Theorem 7.1.** For the deterministic seed $(2,2,2,2)$ and event-uniform growth,

$$H(C_{t+1})>H(C_t)\qquad\text{for every integer }t\ge0.$$

*Proof.* At source size $n=t+8$, an ordered target has incoming probabilities $y_i/(n+4)$ for those coordinates whose decrement is allowed. Their sum is at most $(n+1)/(n+4)$. Lemma 4.1 therefore gives

$$H(R_{t+1})-H(R_t)\ge\log_2\frac{t+12}{t+9}>\frac3{t+12}.\tag{8}$$

The strict elementary bound follows from $\ln(1+x)>x/(1+x)$ and $\ln2<1$.

At odd $t$, $\rho_t=0$. At $t=2m$, (1) gives

$$\rho_{2m}=\frac{\sum_{u=0}^m\binom{u+2}{2}^2\binom{m-u+2}{2}^2}{\binom{2m+11}{11}}.\tag{9}$$

The generating function

$$\sum_{u\ge0}\binom{u+2}{2}^2z^u=\frac{1+4z+z^2}{(1-z)^5}$$

turns the numerator in (9) into the coefficient of $z^m$ in $(1+8z+18z^2+8z^3+z^4)/(1-z)^{10}$. Expanding and simplifying yields

$$\rho_{2m}=\frac{495P(m)}{4D(m)},\tag{10}$$

$$P(m)=m^4+12m^3+53m^2+102m+84,$$

$$D(m)=(2m+1)(2m+3)(2m+5)(2m+7)(2m+9)(2m+11).$$

For $m\ge2$, the inequality $\rho_{2m}<3/(2m+12)$ is equivalent to $G(m)>0$, where $G(m)=2D(m)-165(m+6)P(m)$. With $u=m-2$,

$$\begin{aligned}
G(u+2)={}&128u^6+3675u^5+42260u^4+246615u^3\\
&+756542u^2+1112940u+543510.
\end{aligned}$$

Every coefficient is positive. Combining this bound with (6) and (8) proves positivity for every even $t\ge4$. For odd $t$, the next periodicity correction is nonnegative, so (8) already suffices.

At $t=2$, $\rho_2=3/13$ and $\rho_3=0$. Since $14^4>2\cdot11^4$, the class-entropy increment exceeds $1/4-3/13=1/52$. Finally, the first step gives two distinct classes, $(2,2,2,3)$ and $(2,2,3,2)$, each with probability $1/2$, so its entropy gain is exactly one bit. These cases exhaust all $t\ge0$. $\square$

The bound on $\rho_{2m}$ was used only for $m\ge2$; it fails at the two exceptional early values, which were handled separately.

## 7.1. Entropy bounds and established asymptotics

Summing the non-strict bound in (8) telescopes, and (6) yields

$$H(C_t)\ge\log_2\frac{(t+9)(t+10)(t+11)}{990}-1+\rho_t.\tag{11}$$

There are $\binom{t+3}{3}$ ordered extension vectors. Pair exchange fixes $t/2+1$ vectors when $t$ is even and none otherwise, giving

$$N_t=\frac{\binom{t+3}{3}+\mathbf1_{2\mid t}(t/2+1)}2,\qquad H(C_t)\le\log_2 N_t.\tag{12}$$

Together (11)–(12) prove $H(C_t)=3\log_2t+O(1)$. This leading scaling also follows from established Dirichlet-multinomial entropy asymptotics [4] and a quotient correction bounded by one bit. We include the elementary bounds for transparency, not as a claim of a new general scaling law. Formula (10) further gives $\rho_t\sim495/(64t^2)$ along even times.

# 8. Bounded extension to more runs

For a minimal seed with $D=2k$ runs, each of length two, the relevant group is $C_k$, acting by shifts of two run positions. The endpoint law (1) is invariant under this group, so (7) becomes

$$H(C_t)=H(R_t)-\log_2 k+\mathbb E\log_2|\operatorname{Stab}(R_t)|.\tag{13}$$

For composite $k$, stabilizers can have several sizes. Replacing the expectation in (13) by a single probability of periodicity would generally be incorrect.

A bounded exact-probability scan gave the following results. Entropies here were evaluated numerically; this table is finite evidence only.

| Domain walls $D$ | Events tested | Smallest observed entropy increment (bits) |
|--:|--:|--:|
| 4 | 16 | 0.2182959134 |
| 6 | 16 | 0.3564326326 |
| 8 | 12 | 0.6195272302 |
| 10 | 8 | 1.0000000000 |

The endpoint formula was checked against dynamic recursion through four events. The symmetry identity was checked by independently summing the ordered entropy. No all-time monotonicity theorem for $D\ge6$ is inferred.

For fixed $D$, the ordered column bound and composition count give $(D-1)\log_2t+O(1)$ entropy growth. A finite rotation quotient changes entropy by at most $\log_2k$, so the leading term survives. This familiar asymptotic conclusion does not settle the signs of individual increments.

# 9. Interpretation, limitations and review status

The positive theorem depends on the initial preparation. It does not contradict the single-seed counterexample, which starts from different run lengths. Both concern ordinary Shannon entropy of the current rotation class, not thermodynamic entropy or the entropy of a complete history record.

The model assumes a binary alphabet, cyclic adjacency, a local exclusion rule and a probability prescription. These are mathematical definitions, not a derivation of physical laws. In particular, the coefficient three in the four-run asymptotic counts independent extension coordinates, not physical spatial dimensions.

The contribution should be evaluated as an explicit theorem–counterexample study of a constrained reinforced process and its symmetry quotient. External proof review and the full Nakata comparison remain outstanding. The broader-sector finite scans should remain separate from proved claims until appropriate stabilizer bounds are established.

# 10. Reproducibility

All retained checks use Python's standard library, except unrelated earlier review scripts. From the repository root, run:

```text
python code/wheeler/rotation_audit.py
python code/wheeler/quotient_entropy_audit.py
python code/wheeler/unconditioned_entropy_audit.py
python code/wheeler/minimal_seed_entropy_audit.py
python code/wheeler/many_domain_audit.py
```

The scripts write deterministic JSON under `data/wheeler/`. For the single-seed witness, the quotient recursion, closed-form urn law and full binary insertion enumeration agree exactly through three events. Entropy signs for the central negative example use rational enclosures. The all-time positive theorem is backed by exact polynomial identities and exceptional-step checks. These computations check the implementation and certificates; they are not a replacement for the proofs.

# Appendix A. Single-seed endpoint distributions

Starting from $(2,100,2,100)$, the complete distributions at event counts two and three are:

| $t=2$ representative | Probability |
|:--|--:|
| $(2,100,2,102)$ | $5151/10868$ |
| $(2,100,3,101)$ | $303/10868$ |
| $(2,100,4,100)$ | $3/5434$ |
| $(2,101,2,101)$ | $10201/21736$ |
| $(2,101,3,100)$ | $303/10868$ |
| $(3,100,3,100)$ | $9/21736$ |

| $t=3$ representative | Probability |
|:--|--:|
| $(2,100,2,103)$ | $176851/760760$ |
| $(2,100,3,102)$ | $15453/760760$ |
| $(2,100,4,101)$ | $303/380380$ |
| $(2,100,5,100)$ | $1/76076$ |
| $(2,101,2,102)$ | $520251/760760$ |
| $(2,101,3,101)$ | $30603/760760$ |
| $(2,101,4,100)$ | $303/380380$ |
| $(2,102,3,100)$ | $15453/760760$ |
| $(3,100,3,101)$ | $909/760760$ |
| $(3,100,4,100)$ | $9/380380$ |

Each distribution sums to one exactly. The complete machine-readable data are in `data/wheeler/wheeler-61-results.json`.

# Appendix B. Rational entropy-sign bounds

For a positive rational $x$, choose an integer $j$ such that $x=2^j y$ and $1\le y<2$. Put $z=(y-1)/(y+1)$. Then

$$\ln y=2\sum_{r=0}^{N-1}\frac{z^{2r+1}}{2r+1}+R_N,$$

$$0\le R_N\le\frac{2z^{2N+1}}{(2N+1)(1-z^2)}.$$

Use the same series at $y=2$ to bound $\ln2$. Combine intervals with the appropriate order reversal when $j<0$, sum $-p\ln p$ exactly, and divide by the positive interval for $\ln2$. With $N=32$, this procedure produces (5). The endpoints in (5) are outward-rounded rational numbers, compared with the internal bounds by exact integer arithmetic.

# References

[1] C. Mallows and L. Shepp. *The necklace process*. Journal of Applied Probability 45(1), 271–278 (2008). <https://doi.org/10.1239/jap/1208358967>.

[2] T. Nakata. *Necklace Processes Via Pólya Urns*. Journal of Applied Probability 46(1), 284–295 (2009). <https://doi.org/10.1239/jap/1238592130>. Publisher abstract inspected; full classification comparison pending.

[3] B. Hackl and H. Prodinger. *The necklace process: A generating function approach*. Statistics & Probability Letters 142, 57–61 (2018). Author manuscript: <https://arxiv.org/abs/1801.09934>.

[4] K. Turowski, P. Jacquet and W. Szpankowski. *Asymptotics of Entropy of the Dirichlet-Multinomial Distribution*. ISIT (2019), Theorem 2. <https://www.cs.purdue.edu/homes/spa/papers/isit19-dirichlet.pdf>.

[5] S. Boyd, P. Diaconis, P. Parrilo and L. Xiao. *Symmetry Analysis of Reversible Markov Chains*. Author manuscript revised 29 November 2004. <https://web.stanford.edu/~boyd/papers/pdf/symmetry.pdf>.

[6] M. Niepert. *Markov Chains on Orbits of Permutation Groups* (2012). <https://arxiv.org/abs/1206.5396>.

[7] B. C. Geiger and C. Temmel. *Lumpings of Markov chains, entropy rate preservation, and higher-order lumpability* (preprint, 2012). <https://arxiv.org/abs/1212.4375>.
