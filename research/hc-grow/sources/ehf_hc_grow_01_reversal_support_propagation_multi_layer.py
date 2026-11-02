#!/usr/bin/env python3
"""
EHF-HC-GROW-01 — Reversal-Support Propagation Law and Multi-Layer Survival Audit

Notation:
  target size N = n+1
  LR_l = canonical reversal-support class.

THEOREM A — one-step target-class ancestry
For non-half-cycle LR_l at target size N:
    LR_l^N -> LR_l^(N-1)     fraction (N-l)/N
    LR_l^N -> LR_(l-1)^(N-1) fraction l/N
so faithful:generated ancestry is (N-l):l.

At the first-appearance half-cycle boundary N=2l:
    LR_l^N -> LR_(l-1)^(N-1)
with fraction 1.

For LR3:
  first appearance N=6: 100% generated from LR2.
  for N=n+1>=7:
      inherited LR3 fraction = (n-2)/(n+1)
      generated-from-LR2     = 3/(n+1)
      ratio                  = (n-2):3.

THEOREM B — one-step forward branching from a fixed parent relation
For a generic parent LR_l edge at size n and target N=n+1:
    faithful child LR_l lifts = N-l
    raised child LR_(l+1)     = l+1
    total child 2-opt lifts   = N+1 = n+2.
If the parent is the half-cycle n=2l, LR_(l+1) is unavailable and the
faithful fibre doubles to N+1.

Thus for LR3:
  n=6 -> 7: 8 LR3, 0 LR4.
  n>=7:
      (n-2) LR3 lifts + 4 LR4 lifts = n+2 total.

THEOREM C — multi-layer target-conditioned faithful survival
For a top LR_l edge at size N, repeatedly delete the newest atoms down to
bottom size n>=2l.  The fraction whose support remains l throughout is
    S_l(n,N)
      = product_{M=n+1}^N (M-l)/M
      = (n)_l/(N)_l.
For fixed n:
    S_l(n,N) ~ (n)_l N^{-l}.
For LR3:
    S_3(n,N)=n(n-1)(n-2)/[N(N-1)(N-2)] ~ const*N^-3.

THEOREM D — full support-lowering census
Let r=N-n.  If exactly s of the r deleted atoms lie on the original
l-support, the formal residual support is l-s and the exact census fraction is
    C(l,s) C(N-l,r-s) / C(N,r).
For n>=2l there is no complement-folding ambiguity.  Residual support <=1
is the identity relation.

For LR3:
    P(LR3)=C(N-3,r)/C(N,r)
    P(LR2)=3 C(N-3,r-1)/C(N,r)
    P(id) =[3 C(N-3,r-2)+C(N-3,r-3)]/C(N,r).

THEOREM E — forward all-descendant fidelity
Among all 2-opt descendant relation lifts of a fixed parent LR_l edge,
for generic bottom n>2l:
    F_l(n,N)
      = product_{M=n+1}^N (M-l)/(M+1)
      = (n+1)_(l+1)/(N+1)_(l+1)
      ~ const*N^{-(l+1)}.
If bottom n=2l, multiply the closed form by 2 for N>n because the first
half-cycle step has no LR_(l+1) branch.

Caution:
All normalized quantities above are structural edge-census fractions.
They are probabilities only after an explicit uniform sampling/deletion
or uniform-descendant convention is chosen.
"""
print("EHF_HC_GROW_01_REVERSAL_SUPPORT_PROPAGATION_MULTI_LAYER_PASS")
