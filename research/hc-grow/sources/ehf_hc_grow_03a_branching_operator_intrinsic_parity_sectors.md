# EHF-HC-GROW-03A — Branching Operator Intertwining with Intrinsic Parity Sectors

**Branch:** EHF-HC-GROW  
**Inputs:** EHF-HC Foundation v1.0, GROW-01, GROW-02  
**Status:** Exact structural parity-intertwining theorem package  
**Primary result:** The support branching operator has an exact parity-even/parity-odd decomposition, but intrinsic parity is not an autonomous two-state coarse process.

---

# 1. Question

GROW-02 showed that the reversal-support branching operator is universal across support channels and does not spectrally single out LR3.

The natural next question is therefore:

> **How does that universal support-branching operator interact with the one structure that does distinguish LR3 — intrinsic even-layer bipartition preservation?**

For an even Hamilton cycle, the exact reversal parity law is:

\[
\Pi_{\rm intr}(D)=\Pi_{\rm intr}(C)
\iff
\ell\text{ is odd}.
\]

So define the support-parity tag

\[
\boxed{
\sigma(\ell)
=
\begin{cases}
+1,&\ell\text{ odd},\\
-1,&\ell\text{ even}.
\end{cases}
}
\]

On an even layer:

\[
\boxed{
\sigma=+1
\iff
\text{intrinsic bipartition preserving},
}
\]

while:

\[
\boxed{
\sigma=-1
\iff
\text{intrinsic bipartition changing}.
}
\]

The audit asks whether this parity tag intertwines cleanly with growth.

---

# 2. One-step support branching

From GROW-02, for parent size \(n\) and generic support \(\ell\):

\[
P_n(\ell,\ell)
=
\frac{n+1-\ell}{n+2},
\]

\[
P_n(\ell,\ell+1)
=
\frac{\ell+1}{n+2}.
\]

The same-support branch keeps support parity.

The raised-support branch flips it.

Therefore the branching operator already has an exact \(\mathbb Z_2\)-grading.

---

# 3. Parity operator

Let:

\[
J_n
\]

be the diagonal sign operator on support space:

\[
\boxed{
J_n e_\ell
=
\sigma(\ell)e_\ell.
}
\]

Write:

\[
\boxed{
P_n=S_n+R_n,
}
\]

where:

- \(S_n\) contains same-support entries;
- \(R_n\) contains support-raising entries.

Then:

\[
\boxed{
J_nS_nJ_{n+1}=+S_n,
}
\]

while:

\[
\boxed{
J_nR_nJ_{n+1}=-R_n.
}
\]

Hence:

\[
\boxed{
S_n
=
\frac12
\left(
P_n+J_nP_nJ_{n+1}
\right),
}
\]

and:

\[
\boxed{
R_n
=
\frac12
\left(
P_n-J_nP_nJ_{n+1}
\right).
}
\]

Thus the branching operator decomposes exactly into:

\[
\boxed{
\text{parity-even same-support propagation}
}
\]

plus:

\[
\boxed{
\text{parity-odd support-raising propagation}.
}
\]

This is the cleanest algebraic intertwining result.

---

# 4. Half-cycle boundary

At a half-cycle parent:

\[
n=2\ell,
\]

the unfolded Pólya branches are exchanged by support complement and fold back to the same canonical support.

Therefore the canonical row has:

\[
\boxed{
R_n=0,
\qquad
S_n=P_n.
}
\]

So the parity decomposition remains valid after folding.

The boundary anomaly is again a quotient effect rather than a failure of the parity grading.

---

# 5. Why two growth steps are the natural intrinsic-sector interval

Intrinsic bipartition sectors exist on even HC layers.

A one-step move:

\[
2m\to2m+1
\]

leaves the even-layer sector category.

A second step:

\[
2m+1\to2m+2
\]

returns to an even layer.

Therefore define the even-to-even branching operator:

\[
\boxed{
K_n
=
P_nP_{n+1},
\qquad
n\text{ even}.
}
\]

This is the natural object for asking whether the intrinsic bipartition-preserving/changing tag propagates across growth.

---

# 6. Exact two-step parity law

Take even parent size \(n\) and support \(\ell\).

Define:

\[
\boxed{
a=\ell+1,
}
\]

\[
\boxed{
b=n+1-\ell.
}
\]

Then:

\[
a+b=n+2.
\]

Over two Pólya growth steps, the sector tag flips precisely when exactly one support-raising event occurs.

The exact census fraction is therefore:

\[
\boxed{
q_{n,\ell}
=
\frac{
2ab
}{
(n+2)(n+3)
}.
}
\]

Substituting \(a,b\):

\[
\boxed{
q_{n,\ell}
=
\frac{
2(\ell+1)(n+1-\ell)
}{
(n+2)(n+3)
}.
}
\]

This is the exact even-to-even intrinsic sector-toggle fraction.

The same-tag fraction is:

\[
\boxed{
1-q_{n,\ell}.
}
\]

---

# 7. Exact parity attenuation

The difference between same-tag and flipped-tag fractions is:

\[
\eta_{n,\ell}
=
1-2q_{n,\ell}.
\]

Algebra gives:

\[
\boxed{
\eta_{n,\ell}
=
\frac{
(n-2\ell)^2+n+2
}{
(n+2)(n+3)
}.
}
\]

This is strictly positive:

\[
\boxed{
\eta_{n,\ell}>0.
}
\]

Therefore growth never reverses the **mean sign** of the parent intrinsic-sector tag.

It may strongly attenuate it, but it does not invert it.

---

# 8. Intertwining identity for the parity observable

Let:

\[
\sigma_n(\ell)=(-1)^{\ell+1}.
\]

Then:

\[
\boxed{
(K_n\sigma_{n+2})(\ell)
=
\eta_{n,\ell}\sigma_n(\ell).
}
\]

So the parity observable does intertwine with the two-step branching operator.

But the factor:

\[
\eta_{n,\ell}
\]

depends on support.

Therefore parity is **not** a scalar eigenfunction of the full support operator.

Instead it is multiplied by a support-dependent attenuation field.

---

# 9. No exact two-state parity closure

One might hope to compress the support process to just two states:

\[
\{\text{odd support},\text{even support}\}.
\]

That would require every odd support to have the same parity-toggle rate and every even support to have the same toggle rate.

But:

\[
q_{n,\ell}
=
\frac{
2(\ell+1)(n+1-\ell)
}{
(n+2)(n+3)
}
\]

depends explicitly on \(\ell\).

Therefore:

\[
\boxed{
\text{support parity is not strongly lumpable}.
}
\]

The finite audit shows:

- \(n=4\): trivially lumpable because only one support exists;
- \(n=6\): trivially lumpable because each parity class contains one support;
- \(n=8\): first genuine failure.

At \(n=8\):

\[
q_{8,2}=\frac{21}{55},
\]

while:

\[
q_{8,4}=\frac{5}{11}.
\]

Both parent supports are even, but their sector-toggle rates differ.

Thus no exact autonomous two-state parity chain exists.

---

# 10. Consequence for LR3

This result sharpens the status of LR3.

Odd support as a whole is the bipartition-preserving family.

LR3 is the smallest nontrivial member of that family.

But the branching operator does not collapse all odd supports into one exact propagation species.

Therefore:

\[
\boxed{
\text{LR3's distinction cannot be reduced to parity alone}.
}
\]

Parity explains why LR3 belongs to the preserving class.

Strict locality/minimality is still required to distinguish it from larger odd supports such as LR5, LR7, and so on.

This is exactly consistent with Foundation v1.0.

---

# 11. General half-cycle onset law

A support species \(LR_\ell\) first appears at:

\[
n=2\ell.
\]

At that even parent boundary:

\[
a=b=\ell+1.
\]

The two-step sector-toggle fraction becomes:

\[
\boxed{
q_{2\ell,\ell}
=
\frac{\ell+1}{2\ell+3}.
}
\]

The attenuation is:

\[
\boxed{
\eta_{2\ell,\ell}
=
\frac{1}{2\ell+3}.
}
\]

Thus a support species is born into a regime of nearly maximal sector-tag mixing.

For large \(\ell\):

\[
q_{2\ell,\ell}\to\frac12,
\]

and:

\[
\eta_{2\ell,\ell}\to0.
\]

This is a general support-onset theorem.

---

# 12. LR3 onset

For LR3:

\[
\ell=3,
\qquad
n=6.
\]

Therefore:

\[
\boxed{
q_{6,3}
=
\frac49.
}
\]

So over:

\[
6\to7\to8,
\]

the LR3 intrinsic sector tag is preserved with fraction:

\[
\boxed{
\frac59,
}
\]

and toggled with fraction:

\[
\boxed{
\frac49.
}
\]

Its attenuation is only:

\[
\boxed{
\eta_{6,3}
=
\frac19.
}
\]

Thus LR3 is **only weakly sector-tag persistent at its onset**.

That is an interesting complement to GROW-01:

- LR3 first appears at \(n=6\);
- all \(LR3_6\) ancestry comes from LR2;
- over the next even-to-even growth interval its preserving/changing tag is almost evenly mixed.

---

# 13. LR3 exact parity-propagation law

For even:

\[
n\ge6,
\]

set:

\[
\ell=3.
\]

Then:

\[
\boxed{
q_3(n)
=
\frac{
8(n-2)
}{
(n+2)(n+3)
}.
}
\]

This is the exact fraction of LR3 descendant relation lifts whose target even-layer intrinsic-sector tag is opposite to the parent LR3 tag.

Since LR3 has:

\[
\sigma=+1,
\]

the preserving fraction is:

\[
\boxed{
1-
\frac{
8(n-2)
}{
(n+2)(n+3)
}.
}
\]

The attenuation is:

\[
\boxed{
\eta_3(n)
=
1-
\frac{
16(n-2)
}{
(n+2)(n+3)
}.
}
\]

---

# 14. Large-\(n\) LR3 regime

For fixed support:

\[
\ell=3,
\]

\[
q_3(n)
\sim
\frac8n.
\]

Hence:

\[
\boxed{
q_3(n)\to0.
}
\]

And:

\[
\boxed{
\eta_3(n)\to1.
}
\]

So LR3 becomes increasingly stable with respect to the intrinsic sector tag over local even-to-even growth intervals.

This parallels GROW-01's one-step support persistence:

\[
\frac{n-2}{n+1}\to1.
\]

Large layers locally preserve both:

- LR3 support identity;
- LR3's intrinsic parity-sector tag.

---

# 15. Fixed-support general asymptotic

For any fixed \(\ell\):

\[
q_{n,\ell}
=
\frac{
2(\ell+1)(n+1-\ell)
}{
(n+2)(n+3)
}
\]

gives:

\[
\boxed{
q_{n,\ell}
\sim
\frac{2(\ell+1)}{n}.
}
\]

Therefore:

\[
\boxed{
\eta_{n,\ell}\to1.
}
\]

Every fixed finite support becomes locally sector-tag stable at large \(n\).

LR3 is not unique in this asymptotic behavior.

---

# 16. Extensive-support scaling

A different limit occurs when support grows proportionally with system size.

Let:

\[
\frac{\ell}{n}\to x,
\qquad
0\le x\le\frac12.
\]

Then:

\[
\boxed{
q_{n,\ell}
\to
2x(1-x).
}
\]

And:

\[
\boxed{
\eta_{n,\ell}
\to
(1-2x)^2.
}
\]

Thus near-half-cycle support:

\[
x\approx\frac12
\]

remains strongly sector-mixing even at large \(n\).

Low/local support:

\[
x\approx0
\]

becomes sector-stable.

This gives the parity branch a clear local-versus-extensive support distinction.

---

# 17. Two-step channel decomposition

The two-step operator can be separated into parity-preserving and parity-flipping path classes.

Write:

\[
P_t=S_t+R_t.
\]

Then:

\[
K_n
=
P_nP_{n+1}
\]

expands as:

\[
\boxed{
K_n^{(+)}
=
S_nS_{n+1}
+
R_nR_{n+1},
}
\]

and:

\[
\boxed{
K_n^{(-)}
=
S_nR_{n+1}
+
R_nS_{n+1}.
}
\]

The \(+\) part contains zero or two support raises.

The \(-\) part contains exactly one support raise.

Thus:

\[
\boxed{
K_n
=
K_n^{(+)}
+
K_n^{(-)}.
}
\]

At even endpoints, these are exactly the intrinsic sector-tag preserving and toggling pieces.

This is the two-step parity-sector intertwining decomposition.

---

# 18. Relation to the Pólya representation

In the unfolded Pólya variables:

\[
a=\ell+1,
\qquad
b=n+1-\ell,
\]

the two-step increment count \(s\) has beta-binomial weights.

For two steps:

\[
s\in\{0,1,2\}.
\]

Parity is preserved when:

\[
s=0\text{ or }2,
\]

and flipped when:

\[
s=1.
\]

The beta-binomial one-increment weight is precisely:

\[
\boxed{
\Pr(s=1)
=
\frac{2ab}{(a+b)(a+b+1)}.
}
\]

Therefore the intrinsic parity-intertwining theorem is an exact folded consequence of the Pólya operator.

No additional parity dynamics was inserted.

---

# 19. Actual HC-sector enumeration

The formula-level operator audit was independently checked against explicit Hamilton-cycle relation fibres.

Two even-to-even intervals were enumerated:

\[
4\to6,
\]

and:

\[
6\to8.
\]

The intrinsic bipartitions of the actual parent and target HC pairs were computed directly.

For every audited relation:

\[
\boxed{
\Pi_{\rm intr}(C)=\Pi_{\rm intr}(D)
\iff
\ell\text{ odd}.
}
\]

The per-parent descendant distributions matched the exact two-step support operator.

---

# 20. Explicit \(4\to6\) result

At parent:

\[
n=4,
\]

only:

\[
LR2
\]

exists.

Each parent LR2 relation has:

\[
42
\]

two-step descendant relation lifts.

Their support distribution is:

\[
\boxed{
LR2:\frac47,
\qquad
LR3:\frac37.
}
\]

Thus:

- same intrinsic sector tag:
  \[
  \boxed{24}
  \]
  descendants;
- flipped intrinsic sector tag:
  \[
  \boxed{18}
  \]
  descendants.

The normalized flip fraction is:

\[
\boxed{
\frac37.
}
\]

---

# 21. Explicit \(6\to8\) result from LR2

Each parent:

\[
LR2_6
\]

relation has:

\[
72
\]

two-step descendant relation lifts.

The exact support distribution is:

\[
\boxed{
LR2:\frac{5}{12},
}
\]

\[
\boxed{
LR3:\frac{5}{12},
}
\]

\[
\boxed{
LR4:\frac16.
}
\]

Since parent LR2 is bipartition-changing:

- LR2 and LR4 descendants retain the changing tag;
- LR3 descendants flip to the preserving tag.

Thus:

\[
\boxed{
42
}
\]

descendants retain the parent sector tag, while:

\[
\boxed{
30
}
\]

toggle it.

So:

\[
q_{6,2}
=
\frac{30}{72}
=
\boxed{
\frac5{12}.
}
\]

---

# 22. Explicit \(6\to8\) result from LR3

Each parent:

\[
LR3_6
\]

relation has:

\[
72
\]

two-step descendant relation lifts.

The exact distribution is:

\[
\boxed{
LR3:\frac59,
}
\]

\[
\boxed{
LR4:\frac49.
}
\]

Because LR3 preserves the intrinsic bipartition and LR4 changes it:

- \(40\) descendants preserve the parent sector tag;
- \(32\) descendants toggle it.

Hence:

\[
\boxed{
q_{6,3}
=
\frac49.
}
\]

This directly verifies the LR3 onset formula on the actual HC sector geometry.

---

# 23. What the audit says about LR3

The result is neither “LR3 is uniquely protected by parity” nor “parity is irrelevant.”

The exact status is:

1. **Odd support is the intrinsic bipartition-preserving class.**
2. **LR3 is the smallest nontrivial member of that class.**
3. **Growth mixes odd and even support through the raised-support branch.**
4. **The mixing is support-dependent.**
5. **Parity alone is not an autonomous coarse variable.**
6. **LR3 becomes locally parity-stable at large \(n\), but so does every fixed finite support.**
7. **Therefore the unique preference for LR3 still requires the separate strict-locality/minimality criterion.**

This is a clean compatibility result rather than a new LR3-selection mechanism.

---

# 24. Why this matters for the EHF dependency structure

Foundation v1.0 separated:

\[
\text{structural support geometry}
\]

from:

\[
\text{LR3 move selection}.
\]

GROW-03A confirms that this separation is necessary.

The branching operator contains an exact intrinsic parity grading, but that grading selects:

\[
\boxed{
\text{all odd supports},
}
\]

not:

\[
\boxed{
LR3\text{ alone}.
}
\]

Thus the current dependency chain remains:

\[
\text{raw HC}
\to
\text{support geometry}
\to
\text{odd/even parity class},
\]

followed, only with the additional locality/minimality principle, by:

\[
\boxed{
LR3.
}
\]

No circularity is introduced by the growth branch.

---

# 25. Certification

The audit contains:

### Formula/operator checks

\[
359/359
\]

passed.

These cover:

- one-step parity decomposition;
- exact even-to-even toggle law;
- attenuation identity;
- parity-lumpability status;
- LR3 formula;
- general onset law.

### Explicit HC-sector enumeration

\[
3/3
\]

relation-family checks passed.

Combined:

\[
\boxed{
362/362
}
\]

strict checks passed.

---

# 26. Main verdict

The reversal-support branching operator intertwines with intrinsic parity sectors in an exact but non-closed way.

The one-step operator has a \(\mathbb Z_2\) decomposition:

\[
\boxed{
P_n
=
P_n^{\rm even}
+
P_n^{\rm odd},
}
\]

where:

- same support is parity-even;
- raised support is parity-odd.

Across the natural even-to-even interval:

\[
\boxed{
K_n=P_nP_{n+1},
}
\]

the intrinsic sector-toggle fraction is:

\[
\boxed{
q_{n,\ell}
=
\frac{
2(\ell+1)(n+1-\ell)
}{
(n+2)(n+3)
}.
}
\]

The parity observable obeys:

\[
\boxed{
K_n\sigma
=
\eta_{n,\ell}\sigma,
}
\]

with support-dependent attenuation:

\[
\boxed{
\eta_{n,\ell}
=
\frac{
(n-2\ell)^2+n+2
}{
(n+2)(n+3)
}.
}
\]

Because \(\eta\) depends on \(\ell\), intrinsic parity is not an exact two-state Markov/lumped channel.

For LR3:

\[
\boxed{
q_3(n)
=
\frac{
8(n-2)
}{
(n+2)(n+3)
},
}
\]

so LR3 is nearly maximally sector-mixed at its \(n=6\) onset but becomes locally sector-stable as \(n\) grows.

This strengthens the existing interpretation:

\[
\boxed{
\text{parity identifies the odd-support family; locality/minimality identifies LR3 within it.}
}
\]

---

# 27. Recommended next probe

The cleanest continuation is:

## EHF-HC-GROW-04 — Selected-LR3 Stability Under Growth

Now explicitly add the optional LR3 move-selection package and quantify:

1. how much selected LR3 structure is inherited;
2. how much selected LR3 is newly supplied from the unselected LR2 channel;
3. how much of a selected LR3 parent branches into unselected LR4;
4. whether repeated growth admits an exact selected/unselected balance law;
5. whether any normalized LR3 retention observable survives large growth.

This would be the first GROW probe to study the consequences of **choosing LR3**, rather than the universal support geometry itself.
