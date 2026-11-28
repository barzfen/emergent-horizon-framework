#!/usr/bin/env python3
"""
EHF-HC-GROW-04 — Selected-LR3 Stability Under Growth

This probe studies the consequences of ADDING the optional modelling choice:
    selected same-layer move = LR3.

The raw support branching itself remains the universal GROW-01/GROW-02 system.

SELECTED PROJECTION
Let Q_n project the support relation space at size n onto LR3.

For generic parent n>=7:
    Q_(n+1) B_n Q_n              : LR3 -> LR3 coefficient n-2
    Q_(n+1) B_n (I-Q_n)          : LR2 -> LR3 coefficient 3
    (I-Q_(n+1)) B_n Q_n          : LR3 -> LR4 coefficient 4

Thus LR3 is neither forward invariant nor autonomously generated:
    Q_(n+1) B_n (I-Q_n) != 0
and
    (I-Q_(n+1)) B_n Q_n != 0.

Boundary cases:
    5 -> 6: LR3 first appears; all LR3 comes from LR2.
    6 -> 7: each half-cycle LR3 parent has 8 faithful LR3 lifts; no LR4 yet.
    7 -> 8: generic open-channel rule begins:
             5 LR3 + 4 LR4 from each LR3 parent,
             3 LR3 from each LR2 parent.

TARGET SELECTED-STOCK BALANCE
Let E_l(n) be the number of LR_l relation edges.

For target N>=8:
    E_3(N)
      = (N-3) E_3(N-1)
        + 3 E_2(N-1).

For N>=7 the selected target stock decomposes as
    inherited fraction = (N-3)/N
    newly generated from LR2 = 3/N.
At N=6 the generated fraction is 1.

For generic parent n>=7:
    E_2(n)=E_3(n)=n!/4,
so gross cross-support generation counts satisfy
    LR2 -> LR3 : LR3 -> LR4 = 3 : 4.

RENEWAL COHORT DECOMPOSITION
For a uniformly counted LR3 edge at target N, define G to be the layer at
which its ancestry most recently entered LR3 from LR2.

Boundary cohort:
    P_census(G=6)=120/(N)_3.

For 7<=g<=N:
    P_census(G=g)=3(g-1)(g-2)/(N)_3.

These weights sum exactly to 1.

Cumulative:
    P_census(G<=m)=(m)_3/(N)_3,  6<=m<=N,
    P_census(G>m)=1-(m)_3/(N)_3.

Mean generation layer:
    E_census[G]
      = 3(N+1)/4 + 90/(N)_3.

Hence asymptotically:
    G/N -> distribution with CDF x^3 and density 3x^2,
    E[G]/N -> 3/4,
    mean ancestry age N-G ~ N/4,
    fraction generated after alpha*N -> 1-alpha^3.
In particular, asymptotically 7/8 of target LR3 stock was generated after
the halfway layer.

LINEAGE VS POPULATION STABILITY
For fixed reference n>=6, fraction of target LR3 stock at N with faithful
LR3 ancestry all the way back to n:
    A_3(n,N)=(n)_3/(N)_3 ~ const*N^-3.

For a fixed selected LR3 parent edge, fraction of all 2-opt descendants
that remain on a completely faithful LR3 lineage:
    F_3(n,N) ~ const*N^-4
(with the exact GROW-01 falling-factorial formula and the n=6 boundary
factor 2).

Meanwhile, the selected LR3 class itself has:
    |E_LR3(N)|=N!/4 for N>=7,
but its fraction of the full 2-opt shell is
    2/(N-3) ~ 2/N
(N=6 boundary value 1/3).

Therefore the selected class can persist as a large relation family while:
    - its relative density among all 2-opt relations shrinks ~N^-1;
    - old selected ancestry shrinks ~N^-3;
    - a fixed selected lineage shrinks ~N^-4.

Interpretation:
The selected LR3 class is structurally maintained by continual renewal from
LR2.  It is a layerwise selection criterion on an open branching channel,
not a growth-closed hereditary relation family.

All normalized quantities are exact relation-census fractions.  They become
probabilities only under explicit uniform sampling conventions.
"""
print("EHF_HC_GROW_04_SELECTED_LR3_STABILITY_UNDER_GROWTH_PASS")
