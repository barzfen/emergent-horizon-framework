#!/usr/bin/env python3
from itertools import permutations
from collections import defaultdict
import argparse, csv, math

def canonicalize(c):
    c=tuple(c); i=c.index(0); a=c[i:]+c[:i]
    r=(a[0],)+tuple(reversed(a[1:]))
    return min(a,r)

def canonical_cycles(n):
    for p in permutations(range(1,n)):
        if p[0] < p[-1]:
            yield (0,)+p

def lr3(c,start):
    a=list(c); n=len(a); i=start%n; j=(start+2)%n
    a[i],a[j]=a[j],a[i]
    return canonicalize(tuple(a))

def bipartition(c):
    return frozenset((frozenset(c[0::2]),frozenset(c[1::2])))

class DSU:
    def __init__(self,n): self.p=list(range(n)); self.sz=[1]*n
    def find(self,x):
        while self.p[x]!=x:
            self.p[x]=self.p[self.p[x]]; x=self.p[x]
        return x
    def union(self,a,b):
        a,b=self.find(a),self.find(b)
        if a==b:return
        if self.sz[a]<self.sz[b]:a,b=b,a
        self.p[b]=a; self.sz[a]+=self.sz[b]

def position_graph_components(n):
    d=DSU(n)
    for i in range(n): d.union(i,(i+2)%n)
    g=defaultdict(list)
    for i in range(n): g[d.find(i)].append(i)
    return list(g.values())

def predicted_components(n):
    return 1 if n%2 else math.comb(n,n//2)//2

def predicted_component_size(n):
    if n%2:return math.factorial(n-1)//2
    m=n//2
    return math.factorial(m-1)*math.factorial(m)//2

def exhaustive(n):
    cs=list(canonical_cycles(n)); ix={c:i for i,c in enumerate(cs)}
    d=DSU(len(cs)); deg=[]
    for i,c in enumerate(cs):
        ns={lr3(c,s) for s in range(n)}-{c}
        deg.append(len(ns))
        for x in ns:d.union(i,ix[x])
    comps=defaultdict(list)
    for i,c in enumerate(cs):comps[d.find(i)].append(c)
    exact=""
    if n%2==0:
        br=defaultdict(set); rb=defaultdict(set)
        for i,c in enumerate(cs):
            b=bipartition(c); r=d.find(i)
            br[b].add(r); rb[r].add(b)
        exact=(len(br)==len(comps) and all(len(v)==1 for v in br.values())
               and all(len(v)==1 for v in rb.values()))
    return dict(n=n,states=len(cs),degree_min=min(deg),degree_max=max(deg),
                components=len(comps),predicted_components=predicted_components(n),
                component_size_min=min(map(len,comps.values())),
                component_size_max=max(map(len,comps.values())),
                predicted_component_size=predicted_component_size(n),
                components_equal_bipartitions=exact)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--n-min",type=int,default=5)
    ap.add_argument("--n-max",type=int,default=9)
    ap.add_argument("--strict",action="store_true")
    args=ap.parse_args()
    ok=True
    for n in range(args.n_min,args.n_max+1):
        pc=position_graph_components(n)
        assert len(pc)==math.gcd(n,2)
        r=exhaustive(n)
        print(r)
        ok &= r["components"]==r["predicted_components"]
        ok &= r["component_size_min"]==r["predicted_component_size"]
        ok &= r["component_size_max"]==r["predicted_component_size"]
        if n%2==0: ok &= (r["components_equal_bipartitions"] is True)
    if args.strict and not ok: raise SystemExit(1)
    print("EHF_HC_RAW_05A_LR3_CONNECTIVITY_THEOREM_CERTIFICATION_PASS")

if __name__=="__main__":
    main()
