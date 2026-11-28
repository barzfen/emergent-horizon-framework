#!/usr/bin/env python3
"""
EHF-HC-GROW-07 — Reversal-Support Intrinsic Channel Geometry Audit

Defines the single-channel graph
    G_(n,l) = (HC_n, LR_l)
and compares channels after factoring out the universal GROW-01..05 laws.

The audit has three layers:

1. Exact positional-generator subgroup census:
       H_(n,l)=<cyclic block reversals of support l>
   with component count
       #components = |HC_n| |H∩D_n| / |H|.
   The script checks the observed S_n/A_n/product-family pattern.

2. Explicit HC graph geometry through configurable n:
   connectivity, component sizes, bipartiteness, triangles, local 4-cycles,
   and extremal adjacency spectrum / normalized component gap.

3. Selected larger even preserving components:
   compare LR3 and LR5 without constructing the entire HC_n state space.

Status caution:
The positional-group family classification is finite-exact over the audited
range unless separately proved.  The LR2/LR3 odd-n conjugacy is exact:
multiplication of cyclic positions by 2 normalizes D_n for odd n and maps
adjacent transpositions (LR2) to distance-two transpositions (LR3), hence
    G_(n,2) ~= G_(n,3)  for odd n.

Key expected qualitative result:
Channels need not have the same internal graph geometry even when they have
the same raw distance, parity, degree, component count, and component size.
At n=12, LR3 and LR5 both preserve the intrinsic bipartition and both have
462 components of size 43200 and degree 12, but their local 4-cycle counts
and spectral gaps differ.
"""

import argparse, math, csv
from pathlib import Path
from itertools import permutations
from collections import deque
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
from sympy.combinatorics import Permutation, PermutationGroup

def block_rev_perm(n,s,l):
    idx=[(s+i)%n for i in range(l)]
    mapping=list(range(n))
    for newpos,oldpos in zip(idx,idx[::-1]):
        mapping[oldpos]=newpos
    return Permutation(mapping)

def dihedral_perms(n):
    out=[]; seen=set()
    for k in range(n):
        for arr in ([(i+k)%n for i in range(n)],
                    [(-i+k)%n for i in range(n)]):
            p=Permutation(arr)
            key=tuple(p(i) for i in range(n))
            if key not in seen:
                seen.add(key); out.append(p)
    return out

def candidate_group_order(n,l):
    sig=block_rev_perm(n,0,l).signature()
    if n%2==0 and l%2==1:
        m=n//2
        b=math.factorial(m)**2
        return b if sig==-1 else b//2
    return math.factorial(n) if sig==-1 else math.factorial(n)//2

def predicted_components(n,l):
    sig=block_rev_perm(n,0,l).signature()
    if n%2:
        return 2 if (sig==1 and n%4==1) else 1
    if l%2==0:
        return 1
    m=n//2
    sectors=math.comb(n,m)//2
    return 2*sectors if (l%4==1 and m%2==1) else sectors

def canon(c):
    c=tuple(c); i=c.index(0)
    a=c[i:]+c[:i]
    r=(a[0],)+tuple(reversed(a[1:]))
    return min(a,r)

def states(n):
    return [(0,)+p for p in permutations(range(1,n)) if p[0]<p[-1]]

def rev_state(c,s,l):
    a=list(c); n=len(a)
    idx=[(s+i)%n for i in range(l)]
    vals=[a[i] for i in idx][::-1]
    for i,v in zip(idx,vals): a[i]=v
    return canon(a)

def build_full(n,l):
    ss=states(n); ix={c:i for i,c in enumerate(ss)}
    adj=[set() for _ in ss]
    for i,c in enumerate(ss):
        for s in range(n):
            d=rev_state(c,s,l); j=ix[d]
            if i!=j:
                adj[i].add(j); adj[j].add(i)
    return ss,adj

def build_component(n,l):
    root=canon(tuple(range(n)))
    ix={root:0}; ss=[root]; adj=[set()]; q=deque([root])
    while q:
        c=q.popleft(); i=ix[c]
        for s in range(n):
            d=rev_state(c,s,l)
            if d not in ix:
                ix[d]=len(ss); ss.append(d); adj.append(set()); q.append(d)
            j=ix[d]
            if i!=j:
                adj[i].add(j); adj[j].add(i)
    return ss,adj

def components(adj):
    seen=set(); out=[]
    for s in range(len(adj)):
        if s in seen: continue
        seen.add(s); q=[s]; cc=[]
        while q:
            u=q.pop(); cc.append(u)
            for v in adj[u]:
                if v not in seen:
                    seen.add(v); q.append(v)
        out.append(cc)
    return out

def bipartite(adj,nodes):
    S=set(nodes); color={}
    for s in nodes:
        if s in color: continue
        color[s]=0; q=[s]
        while q:
            u=q.pop()
            for v in adj[u]:
                if v not in S: continue
                if v not in color:
                    color[v]=1-color[u]; q.append(v)
                elif color[v]==color[u]:
                    return False
    return True

def triangle_count(adj,nodes):
    S=set(nodes); c=0
    for u in nodes:
        for v in adj[u]:
            if v>u and v in S:
                c+=sum(1 for w in adj[u]&adj[v] if w>v and w in S)
    return c

def four_root(adj,root):
    ns=list(adj[root]); c=0
    for i,u in enumerate(ns):
        for v in ns[i+1:]:
            c+=len((adj[u]&adj[v])-{root})
    return c

def spectrum(adj,nodes,k=5):
    pos={v:i for i,v in enumerate(nodes)}
    rr=[]; cc=[]
    for u in nodes:
        for v in adj[u]:
            if v in pos:
                rr.append(pos[u]); cc.append(pos[v])
    A=sp.csr_matrix((np.ones(len(rr)),(rr,cc)),shape=(len(nodes),len(nodes)))
    if len(nodes)<=100:
        vals=np.linalg.eigvalsh(A.toarray())
        top=vals[-min(k,len(vals)):][::-1]
        bot=vals[:min(k,len(vals))]
    else:
        kk=min(k,len(nodes)-2)
        top=np.sort(eigsh(A,k=kk,which="LA",return_eigenvectors=False))[::-1]
        bot=np.sort(eigsh(A,k=kk,which="SA",return_eigenvectors=False))
    return top,bot

def write_csv(path,rows):
    if not rows: return
    with open(path,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--group-n-max",type=int,default=16)
    ap.add_argument("--full-n-max",type=int,default=9)
    ap.add_argument("--out-dir",default="runs/ehf_hc_grow_07")
    args=ap.parse_args()
    out=Path(args.out_dir); out.mkdir(parents=True,exist_ok=True)
    checks=[]; grows=[]; geoms=[]

    for n in range(5,args.group_n_max+1):
        D=dihedral_perms(n); V=math.factorial(n-1)//2
        for l in range(2,n//2+1):
            H=PermutationGroup([block_rev_perm(n,s,l) for s in range(n)])
            order=H.order()
            inter=sum(1 for p in D if H.contains(p))
            comps=V*inter//order
            cand=candidate_group_order(n,l)
            pred=predicted_components(n,l)
            checks += [
                {"check":f"group_order_n{n}_l{l}","pass":order==cand},
                {"check":f"component_pattern_n{n}_l{l}","pass":comps==pred},
            ]
            grows.append({
                "n":n,"l":l,"group_order":order,"candidate_order":cand,
                "H_intersect_D":inter,"components":comps,
                "predicted_components":pred,
                "component_size":order//inter,
            })

    for n in range(5,args.full_n_max+1):
        for l in range(2,n//2+1):
            ss,adj=build_full(n,l)
            cs=components(adj); C=max(cs,key=len)
            d=len(adj[C[0]])
            top,bot=spectrum(adj,C)
            tri=triangle_count(adj,C)
            checks.append({"check":f"triangle_free_n{n}_l{l}","pass":tri==0})
            geoms.append({
                "n":n,"l":l,"vertices":len(ss),"degree":d,
                "components":len(cs),"component_size":len(C),
                "bipartite":bipartite(adj,C),"triangles":tri,
                "four_cycles_through_root":four_root(adj,C[0]),
                "top5":str([float(x) for x in top]),
                "bottom5":str([float(x) for x in bot]),
                "normalized_gap":float(1-top[1]/d),
            })

    for n,l in [(10,3),(10,5),(12,3),(12,5)]:
        ss,adj=build_component(n,l)
        C=list(range(len(ss))); d=len(adj[0]); top,bot=spectrum(adj,C)
        geoms.append({
            "n":n,"l":l,"vertices":math.factorial(n-1)//2,"degree":d,
            "components":"see group census","component_size":len(C),
            "bipartite":bipartite(adj,C),"triangles":triangle_count(adj,C),
            "four_cycles_through_root":four_root(adj,0),
            "top5":str([float(x) for x in top]),
            "bottom5":str([float(x) for x in bot]),
            "normalized_gap":float(1-top[1]/d),
        })

    write_csv(out/"group_census.csv",grows)
    write_csv(out/"channel_geometry.csv",geoms)
    write_csv(out/"checks.csv",checks)
    ok=sum(bool(r["pass"]) for r in checks)
    print(f"EHF-HC-GROW-07: {ok}/{len(checks)} checks PASS")

if __name__=="__main__":
    main()
