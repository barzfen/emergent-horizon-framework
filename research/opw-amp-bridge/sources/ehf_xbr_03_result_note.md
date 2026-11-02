# EHF-XBR-03 Result Note
## Canonical Middle-Block Bridge Operator and Intertwining Obstruction

**Script version:** `ehf_xbr_03_2026-07-26`  
**Validation status:** independently reproduced in the construction environment

## Verdict

```text
EHF_XBR_03_TWO_STEP_MEDIATED_BRIDGE_INTERTWINING_OBSTRUCTION_PASS
```

All 19 strict checks passed.

## Canonical operators

For each AMP channel \(A\),

\[
M_A:\mathbb Q^{360}\to\mathbb Q^{C_A}
\]

is the middle-block growth incidence,

\[
D_A:\mathbb Q^{C_A}\to\mathbb Q^{72}
\]

is signed AMP deletion,

\[
V_A\subseteq\mathbb Q^{72}
\]

is the exact transmitted AMP image, and

\[
A_A:\mathbb Q^{C_A}\to\mathbb Q^{C_A}
\]

is OPW3 chamber adjacency.

The depth-\(k\) bridge is

\[
B_A^{(k)}=V_AD_AA_A^kM_A.
\]

## Exact census

Across the 35 reference channels:

- 19 are reached by middle-block growth;
- 31 have nonzero AMP relation image;
- 16 have both structures;
- the 35 AMP source chambers contain exactly 360 of the global 720
  middle-block incidences.

Every AMP source fibre is exactly an OPW3 chamber.

For every channel,

\[
D_AD_A^{\mathsf T}=2I.
\]

Thus \(D_A^{\mathsf T}/\sqrt2\) is an isometric deletion-adjoint lift.

## Direct obstruction

For all 35 channels,

\[
D_AM_A=0,
\]

and therefore

\[
B_A^{(0)}=0.
\]

The reason is support-theoretic: middle-block growth places the newest labels
in central positions, while AMP deletion is active only when the deleted label
is adjacent to the anchor.

One OPW3 adjacency step is also insufficient:

\[
D_AA_AM_A=0,
\qquad
B_A^{(1)}=0.
\]

In every growth-hit chamber, the graph distance between middle-block support
and deletion-active support is exactly

\[
2.
\]

## Two-step activation

At depth two,

\[
D_AA_A^2M_A\ne0
\]

for all 19 growth-hit channels.

For all 16 channels with both middle-block growth and nonzero AMP image,

\[
B_A^{(2)}\ne0.
\]

Thus the first canonical AMP-visible bridge occurs after exactly two OPW3
adjacency steps.

At depth two, 9 of the 16 joint channels reach full AMP-image rank.

At depth three, 14 of 16 reach full rank.

The two partial channels are

\[
A=\{2,3,7\},
\qquad
A=\{2,6,7\}.
\]

Their depth-three bridge ranks are respectively

\[
6/9,
\qquad
13/15.
\]

## Direct intertwining obstruction

Let

\[
W_A=\operatorname{row}(V_AD_A)
\subseteq\mathbb Q^{C_A}.
\]

For a direct full-image adjacency intertwiner to exist, \(W_A\) must be
\(A_A\)-invariant.

For every one of the 31 nonzero AMP channels,

\[
\operatorname{rank}
\begin{pmatrix}
W_A\\
W_AA_A
\end{pmatrix}
>
\operatorname{rank}(W_A).
\]

Therefore no direct operator \(K_A\) on the full AMP image can satisfy

\[
A_AJ_A=J_AK_A
\]

for the deletion-adjoint lift \(J_A\).

## Exact scientific statement

> The obvious direct middle-block/deletion bridge vanishes, and one OPW3
> adjacency step remains insufficient. Exactly two OPW3 steps activate every
> channel in which both middle-block growth and a nonzero AMP image occur.
> Nevertheless, the complete deletion-adjoint AMP image is never invariant
> under OPW3 adjacency, so a direct full-image adjacency intertwiner is
> obstructed in every nonzero channel.

## Interpretation boundary

This is a finite structural result about exact incidence, deletion, relation,
and adjacency operators. OPW adjacency is not identified with a physical
Hamiltonian or time evolution. The result does not derive amplitudes from
dynamics and does not construct a natural isomorphism between the two branch
functors.
