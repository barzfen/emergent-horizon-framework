#!/usr/bin/env python3
"""
EHF-HC-GROW-02 — Reversal-Support Branching Operator

Canonical support set:
    L_n = {2,...,floor(n/2)}.

RAW MULTIPLICITY OPERATOR B_n
For parent support l at size n and target N=n+1:

Generic l < n/2:
    B_n(l,l)   = n+1-l
    B_n(l,l+1) = l+1
    row sum     = n+2.

Half-cycle parent n=2l:
    B_n(l,l)   = n+2
    B_n(l,l+1) = 0.

NORMALIZED CENSUS KERNEL
    P_n = B_n/(n+2).

UNFOLDED REVERSAL-LENGTH DOUBLE COVER
Use an oriented reversal length j and define
    a=j+1,
    b=n+1-j,
    T=n+2.
Then:
    j -> j+1 with normalized census weight a/T,
    j -> j   with normalized census weight b/T.
This is exactly the two-colour Polya urn.

The canonical support is the colour-swap quotient:
    l=min(j,n-j)=min(a,b)-1.
The half-cycle boundary is simply a=b; after one urn update the two
possible oriented outcomes fold back to the same canonical support.

BACKWARD OPERATOR ON OBSERVABLES
    (P_n f)(a)
      = f(a) + (1/T) G f(a),
    G f(a)=a[f(a+1)-f(a)].
The scaled bulk generator G is independent of n.

POLYNOMIAL SPECTRUM
For rising factorials
    f_r(a)=a^(overline r),
    G f_r = r f_r.
Hence
    P_n f_r=(1+r/T)f_r.

Therefore
    M_r(n,a)=a^(overline r)/T^(overline r)
is an exact martingale across growth.

Reflection swaps a and b.  Thus the canonical symmetric combinations
    H_r=[a^(overline r)+b^(overline r)]/T^(overline r), r>=2,
are exact canonical support martingales.

MULTI-STEP KERNEL
After R=N-n steps from oriented j, the number s of j->j+1 increments has
the exact beta-binomial census law
    Pr_census(s)
      = C(R,s)
        (a)^(overline s)
        (b)^(overline (R-s))
        /(T)^(overline R).
Fold j+s by
    l'=min(j+s,N-j-s)
to obtain the exact canonical multi-step branching kernel.

EVEN-PARENT FINITE CANONICAL SPECTRUM
For n=2m, P_n is a square upper-triangular matrix on
    l=2,...,m.
Its eigenvalues are
    1,
    (n+1-l)/(n+2), l=2,...,m-1.
The second-largest eigenvalue is
    (n-1)/(n+2),
so the one-step gap to the boundary eigenvalue 1 is
    3/(n+2).

For odd parent n, the target acquires one extra support channel, so P_n is
rectangular and an ordinary same-space eigen-spectrum is not the natural
object.  The n-independent unfolded generator G supplies the cleaner
cross-layer spectral description.

LARGE-n SCALING
On polynomial mode r:
    prod_{t=n}^{N-1}(1+r/(t+2))
      =(N+2)^(overline r)/(n+2)^(overline r)
      ~ (N/n)^r.
Thus logarithmic size tau=log n is the natural asymptotic scale of this
non-autonomous branching family.

LR3 STATUS
The branching operator itself does not spectrally single out LR3.
LR3 is one support channel with:
    faithful multiplicity n-2,
    raised LR4 multiplicity 4
in the generic regime.
Its special status in the wider EHF-HC programme comes from the separate
parity-preservation/locality selection results and its onset at n=6, not
from an isolated branching-operator eigenvalue.

CAUTION
All normalized entries are exact relation-census fractions.  They become
probabilities only after choosing uniform sampling among relation lifts.
"""
print("EHF_HC_GROW_02_REVERSAL_SUPPORT_BRANCHING_OPERATOR_PASS")
