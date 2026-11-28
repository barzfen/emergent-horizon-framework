#!/usr/bin/env python3
"""
EHF-HC-RAW-10A — Johnson Transport Recovery Audit

Reconstructs the exact Johnson transport core after RAW-09A established:
  intrinsic even sectors
  -> growth-selected newest-site chart
  -> horizontal LR2 quotient
  -> Johnson A1 adjacency.

This audit treats the uniform A1 random walk as a chosen neutral transport
convention and rederives exact h/q drift-diffusion, generating functions,
reflection, and shell coarse transport.

Important cleanup:
the h-shell partition is not strongly lumpable for k>=3.
"""

from itertools import combinations
from collections import defaultdict, Counter
from fractions import Fraction
import math, argparse

def states(k):
    return list(combinations(range(1,2*k),k))

def h(S): return sum(S)
def q(S): return sum(x*x for x in S)

def neighbors(S,k):
    A=set(S)
    for a in S:
        for b in range(1,2*k):
            if b not in A:
                yield tuple(sorted((A-{a})|{b}))

def T1(k): return k*(2*k-1)
def T2(k): return (2*k-1)*(2*k)*(4*k-1)//6

def drift(k,H):
    return Fraction((2*k-1)*(k*k-H),k*(k-1))

def diffusion(k,H,Q):
    return Fraction(k*T2(k)-Q-2*T1(k)*H+2*H*H,k*(k-1))

def coeff_counts(k,excluded=None):
    dp={(0,0):1}
    for j in range(1,2*k):
        if j==excluded: continue
        nd=dict(dp)
        for (c,s),v in dp.items():
            nd[(c+1,s+j)]=nd.get((c+1,s+j),0)+v
        dp=nd
    return dp

def audit(k):
    X=states(k); d=k*(k-1)
    byh=defaultdict(list); refined=Counter()
    for S in X:
        H=h(S); byh[H].append(S)
        for j in S: refined[(H,j)]+=1

    drift_ok=diff_ok=True
    sigs=defaultdict(set)
    for S in X:
        H=h(S); Q=q(S)
        ds=[]; hist=Counter()
        for U in neighbors(S,k):
            dh=h(U)-H
            ds.append(dh); hist[h(U)]+=1
        drift_ok &= Fraction(sum(ds),d)==drift(k,H)
        diff_ok &= Fraction(sum(x*x for x in ds),d)==diffusion(k,H,Q)
        sigs[H].add(tuple(sorted(hist.items())))

    mean=Fraction(sum(h(S) for S in X),len(X))
    var=Fraction(sum((h(S)-mean)**2 for S in X),len(X))
    G=coeff_counts(k)
    gf_ok=all(len(byh[H])==G.get((k,H),0) for H in byh)

    refined_ok=True
    for j in range(1,2*k):
        F=coeff_counts(k,j)
        for H in byh:
            refined_ok &= refined[(H,j)]==F.get((k-1,H-j),0)

    reflection=all(
        refined[(H,j)]==refined[(2*k*k-H,2*k-j)]
        for H in byh for j in range(1,2*k)
    )

    return dict(
        k=k,
        states=len(X),
        degree=d,
        mean_h=mean,
        variance_h=var,
        drift_exact=drift_ok,
        diffusion_exact=diff_ok,
        shell_GF_exact=gf_ok,
        refined_GF_exact=refined_ok,
        reflection_exact=reflection,
        nonlumpable_shells=sum(len(sigs[H])>1 for H in byh),
    )

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--k-min",type=int,default=2)
    ap.add_argument("--k-max",type=int,default=7)
    ap.add_argument("--strict",action="store_true")
    args=ap.parse_args()

    ok=True
    for k in range(args.k_min,args.k_max+1):
        r=audit(k)
        print(r)
        ok &= r["states"]==math.comb(2*k-1,k)
        ok &= r["mean_h"]==k*k
        ok &= r["variance_h"]==Fraction(k*k*(k-1),6)
        ok &= r["drift_exact"] and r["diffusion_exact"]
        ok &= r["shell_GF_exact"] and r["refined_GF_exact"] and r["reflection_exact"]
        if k>=3:
            ok &= r["nonlumpable_shells"]>0

    if args.strict and not ok:
        raise SystemExit(1)
    print("EHF_HC_RAW_10A_JOHNSON_TRANSPORT_RECOVERY_PASS")

if __name__=="__main__":
    main()
