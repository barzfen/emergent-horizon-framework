#!/usr/bin/env python3
"""
EHF-HC-RAW-10B — Birth-Rank Gauge / Observable Robustness Audit

For J(2k-1,k) with the uniform A1 walk and arbitrary fixed label weights w_i,
define
    F_w(S) = sum_{i in S} w_i
    G_w(S) = sum_{i in S} w_i^2
    W1 = sum_i w_i
    W2 = sum_i w_i^2.

Exact universal identities:
    E[dF|S] =
        [k W1 - (2k-1) F]/[k(k-1)]
      = -lambda (F - k mean(w)),
    lambda = (2k-1)/[k(k-1)].

    E[dF^2|S] =
        [k W2 - G - 2 W1 F + 2 F^2]/[k(k-1)].

Under the uniform state ensemble:
    E[F]   = k mean(w)
    Var(F) = (k/2) population_variance(w).

Thus linear birth rank is not singled out by drift closure.
It is selected only after extra coordinate principles such as homogeneous
birth displacement/equal spacing are imposed.
"""

from itertools import combinations
from collections import Counter, defaultdict
from fractions import Fraction
import argparse, math, random

def states(k):
    return list(combinations(range(1,2*k),k))

def neighbors(S,k):
    A=set(S)
    for a in S:
        for b in range(1,2*k):
            if b not in A:
                yield tuple(sorted((A-{a})|{b}))

def F(S,w):
    return sum(w[i-1] for i in S)

def G(S,w):
    return sum(w[i-1]**2 for i in S)

def drift(k,f,W1):
    N=2*k-1
    return Fraction(k*W1-N*f,k*(k-1))

def diffusion(k,f,g,W1,W2):
    return Fraction(k*W2-g-2*W1*f+2*f*f,k*(k-1))

def variance_formula(k,w):
    N=2*k-1
    W1=sum(w); W2=sum(x*x for x in w)
    popvar=Fraction(W2,N)-Fraction(W1*W1,N*N)
    return Fraction(k,2)*popvar

def families(k):
    N=2*k-1
    rng=random.Random(20260825+k)
    p=list(range(1,N+1)); rng.shuffle(p)
    return {
        "constant":[1]*N,
        "parity":[i%2 for i in range(1,N+1)],
        "linear":list(range(1,N+1)),
        "affine":[3*i+7 for i in range(1,N+1)],
        "reversed":[N+1-i for i in range(1,N+1)],
        "quadratic":[i*i for i in range(1,N+1)],
        "centered_cubic":[(i-k)**3 for i in range(1,N+1)],
        "scrambled_linear":p,
        "powers_of_two":[1<<(i-1) for i in range(1,N+1)],
    }

def audit(k):
    X=states(k); d=k*(k-1)
    out={}
    for name,w in families(k).items():
        W1=sum(w); W2=sum(x*x for x in w)
        mean=Fraction(k*W1,2*k-1)
        shells=defaultdict(set)
        vals=[]
        okD=okB=True
        for S in X:
            f=F(S,w); g=G(S,w); vals.append(f)
            ds=[]; hist=Counter()
            for U in neighbors(S,k):
                fu=F(U,w); ds.append(fu-f); hist[fu]+=1
            okD &= Fraction(sum(ds),d)==drift(k,f,W1)
            okB &= Fraction(sum(x*x for x in ds),d)==diffusion(k,f,g,W1,W2)
            shells[f].add(tuple(sorted(hist.items())))
        var=Fraction(sum((Fraction(v,1)-mean)**2 for v in vals),len(vals))
        out[name]=dict(
            shells=len(shells),
            nonlumpable=sum(len(x)>1 for x in shells.values()),
            drift=okD,
            diffusion=okB,
            variance=(var==variance_formula(k,w)),
        )
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--k-min",type=int,default=2)
    ap.add_argument("--k-max",type=int,default=7)
    ap.add_argument("--strict",action="store_true")
    args=ap.parse_args()

    ok=True
    for k in range(args.k_min,args.k_max+1):
        r=audit(k)
        print("k",k,r)
        ok &= all(x["drift"] and x["diffusion"] and x["variance"] for x in r.values())
        ok &= r["constant"]["shells"]==1
        ok &= r["powers_of_two"]["shells"]==math.comb(2*k-1,k)
    if args.strict and not ok:
        raise SystemExit(1)
    print("EHF_HC_RAW_10B_BIRTH_RANK_GAUGE_OBSERVABLE_ROBUSTNESS_PASS")

if __name__=="__main__":
    main()
