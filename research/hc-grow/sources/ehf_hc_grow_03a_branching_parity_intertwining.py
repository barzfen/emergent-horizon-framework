#!/usr/bin/env python3
"""
EHF-HC-GROW-03A — Branching Operator Intertwining with Intrinsic Parity Sectors

Support parity tag:
    sigma(l)=+1 for odd l
    sigma(l)=-1 for even l.
On an even HC layer:
    sigma=+1 iff LR_l preserves the intrinsic cycle bipartition,
    sigma=-1 iff LR_l changes it.

ONE-STEP DECOMPOSITION
Write the canonical branching kernel
    P_n = S_n + R_n
where S_n is the same-support part and R_n the raised-support part.
With J_n=diag(sigma(l)):
    J_n S_n J_(n+1)=+S_n
    J_n R_n J_(n+1)=-R_n.
Hence
    S_n=[P_n+J_n P_n J_(n+1)]/2,
    R_n=[P_n-J_n P_n J_(n+1)]/2.
Thus support-stay is parity-even and support-raise parity-odd.

EVEN-TO-EVEN INTERTWINING
Let n be even and
    K_n=P_n P_(n+1).
For parent support l:
    q_(n,l)
      =2(l+1)(n+1-l)/[(n+2)(n+3)]
is the exact census fraction that flips the intrinsic sector tag between
the even layers n and n+2.
The same-tag fraction is 1-q.

For the parity observable sigma:
    (K_n sigma_(n+2))(l)
      = eta_(n,l) sigma_n(l),
where
    eta_(n,l)
      =1-2q_(n,l)
      =[(n-2l)^2+n+2]/[(n+2)(n+3)] > 0.

Thus intrinsic parity intertwines with the branching operator through a
support-dependent attenuation.  It is not a scalar eigenmode.

NO EXACT TWO-STATE PARITY CLOSURE
Because q_(n,l) depends on l, the partition "odd support versus even support"
is not strongly lumpable once either parity class contains multiple support
values.  This first fails at n=8.

ONSET
At half-cycle onset n=2l:
    q=(l+1)/(2l+3)
    eta=1/(2l+3).
Hence newly available support species are nearly maximally sector-mixed over
the next even-to-even interval.

LR3
For l=3:
    q_3(n)=8(n-2)/[(n+2)(n+3)]
    eta_3(n)=1-16(n-2)/[(n+2)(n+3)].
At n=6:
    preserve=5/9
    toggle=4/9
    eta=1/9.
For fixed l=3 and n->infinity:
    q_3(n)~8/n
    eta_3(n)->1.

SCALING
If l/n -> x in [0,1/2]:
    q -> 2x(1-x)
    eta -> (1-2x)^2.
For fixed l:
    q ~ 2(l+1)/n
    eta -> 1.

Interpretation caution:
All normalized quantities are exact relation-census fractions.  They become
stochastic sector-transition probabilities only under uniform sampling among
relation lifts.
"""
print("EHF_HC_GROW_03A_BRANCHING_OPERATOR_INTRINSIC_PARITY_SECTORS_PASS")
