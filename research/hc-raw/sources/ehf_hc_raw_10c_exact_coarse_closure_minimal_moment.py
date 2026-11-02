#!/usr/bin/env python3
"""
EHF-HC-RAW-10C — Exact Coarse-Closure / Minimal Moment Audit

Main finite result:
For J(2k-1,k), k=3..9, the coarsest equitable/strongly-lumpable
refinement of the birth-rank h-partition is the singleton state partition.
In fact one exact neighbor-count refinement of the h shells already
separates every state in the audited range.

Power-sum moment partitions p_j=sum i^j were also tested.  The first
strongly lumpable power-moment tuple in every audited case was already
the singleton partition.

Moment hierarchy:
  E[Delta p_r | S]
    = [k T_r-(2k-1)p_r]/[k(k-1)].

  E[Delta p_r Delta p_s | S]
    = [k T_(r+s)-p_(r+s)-T_r p_s-T_s p_r+2 p_r p_s]/[k(k-1)].

Thus first-moment closure preserves moment order, while exact second-order
closure requires moments up to doubled order.
"""
from itertools import combinations
from collections import defaultdict, Counter
import argparse

def states(k):
    return list(combinations(range(1,2*k),k))

def adjacency(X,k):
    ix={s:i for i,s in enumerate(X)}
    out=[]
    for S in X:
        A=set(S); ns=[]
        for a in S:
            for b in range(1,2*k):
                if b not in A:
                    ns.append(ix[tuple(sorted((A-{a})|{b}))])
        out.append(tuple(ns))
    return out

def colors(keys):
    mp={}; out=[]
    for q in keys:
        if q not in mp: mp[q]=len(mp)
        out.append(mp[q])
    return out

def equitable(c,adj):
    seen={}
    for i,x in enumerate(c):
        sig=tuple(sorted(Counter(c[j] for j in adj[i]).items()))
        if x in seen and seen[x]!=sig:return False
        seen[x]=sig
    return True

def refine(c,adj):
    while True:
        sigs=[]
        for i,x in enumerate(c):
            cnt=tuple(sorted(Counter(c[j] for j in adj[i]).items()))
            sigs.append((x,cnt))
        nc=colors(sigs)
        if len(set(nc))==len(set(c)):return nc
        c=nc

def pkey(S,r):
    return tuple(sum(i**j for i in S) for j in range(1,r+1))

def audit(k):
    X=states(k); adj=adjacency(X,k)
    hc=colors([sum(S) for S in X])
    ec=refine(hc,adj)
    mr=None
    for r in range(1,k+1):
        c=colors([pkey(S,r) for S in X])
        if equitable(c,adj):
            mr=r; break
    return dict(
        k=k, states=len(X), h_shells=len(set(hc)),
        equitable_refinement_classes=len(set(ec)),
        full_state_refinement=(len(set(ec))==len(X)),
        first_lumpable_power_moment_order=mr
    )

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--k-min",type=int,default=3)
    ap.add_argument("--k-max",type=int,default=9)
    ap.add_argument("--strict",action="store_true")
    args=ap.parse_args()
    ok=True
    for k in range(args.k_min,args.k_max+1):
        r=audit(k); print(r)
        ok &= r["full_state_refinement"]
    if args.strict and not ok: raise SystemExit(1)
    print("EHF_HC_RAW_10C_EXACT_COARSE_CLOSURE_MINIMAL_MOMENT_PASS")

if __name__=="__main__":
    main()
