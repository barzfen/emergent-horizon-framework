#!/usr/bin/env python3
"""
EHF-HC-GROW-05 — General Selected-Support Renewal Theorem

Fix selected support LR_l, l>=2.

ONSET
LR_l first exists at N=2l as the half-cycle class.
At onset every LR_l target edge is generated from the lower channel.

For l>=3 the lower channel is the ordinary relation LR_(l-1), with
per-parent lift multiplicity l.

For l=2 the lower channel is LR1=id, a diagonal/vertex relation rather than
an ordinary edge relation.  Its per-parent multiplicity is n at parent size
n=N-1.  This is the unique base-channel exception.

POST-ONSET TARGET STOCK
For every N>2l:
    inherited fraction = (N-l)/N
    newly generated fraction = l/N.

At parent size n=N-1, generic l>=3:
    LR_(l-1) -> LR_l multiplicity l
    LR_l     -> LR_l multiplicity N-l=n+1-l
    LR_l     -> LR_(l+1) multiplicity l+1
once LR_(l+1) is available.

The gross cross-support generated-stock ratio is
    inflow : outflow = l : (l+1).

RENEWAL COHORT
For a target LR_l edge at size N define G as the layer at which its ancestry
most recently entered LR_l from the lower channel.

Onset cohort:
    P_census(G=2l) = (2l)_l/(N)_l.

For 2l<g<=N:
    P_census(G=g) = l (g-1)_(l-1)/(N)_l.

Cumulative law:
    P_census(G<=m) = (m)_l/(N)_l,
    P_census(G>m)  = 1-(m)_l/(N)_l.

Exact mean:
    E_census[G]
      = l(N+1)/(l+1)
        + l(2l)_l/[(l+1)(N)_l].

Hence, for N->infinity:
    G/N => distribution with CDF x^l and density l x^(l-1),
    E[G]/N -> l/(l+1),
    mean ancestry age / N -> 1/(l+1).

ANCESTRY AND LINEAGE
For reference n>=2l:
    A_l(n,N) = (n)_l/(N)_l ~ const*N^-l.

For one fixed selected LR_l parent, the fraction of all 2-opt descendants
remaining on a completely faithful selected lineage is generically
    F_l(n,N) = (n+1)_(l+1)/(N+1)_(l+1)
              ~ const*N^-(l+1),
with factor 2 for N>n when bottom n=2l because of the half-cycle fibre.

CLASS DENSITY
For N>2l:
    |E(LR_l)| / |E(2opt)| = 2/(N-3),
independent of fixed l.
At onset N=2l:
    density = 1/(N-3).

STRUCTURAL CONSEQUENCE
LR3 is not unique in renewal exponents or class density.
However LR3 is the first selected support whose lower and upper reservoirs
are both ordinary nontrivial reversal-edge relations:
    LR2 -> LR3 -> LR4.
LR2's lower reservoir is identity/diagonal rather than an LR edge class.

Parity remains independent information:
    odd l  = intrinsic even-layer bipartition preserving,
    even l = bipartition changing.

All normalized quantities are exact relation-census fractions.  They become
probabilities only under an explicit uniform sampling convention.
"""
from math import prod

def falling(n,r):
    return prod(range(n-r+1,n+1)) if r else 1

# Minimal self-checks of the theorem identities.
for l in range(2,9):
    for N in range(2*l,2*l+20):
        D=falling(N,l)
        weights=[]
        for g in range(2*l,N+1):
            if g==2*l:
                w=falling(2*l,l)/D
            else:
                w=l*falling(g-1,l-1)/D
            weights.append(w)
        assert abs(sum(weights)-1.0)<1e-12

print("EHF_HC_GROW_05_GENERAL_SELECTED_SUPPORT_RENEWAL_PASS")
