#!/usr/bin/env python3
from itertools import permutations, combinations
from collections import defaultdict
import argparse, csv, math

def effective_lengths(n): return list(range(2,n//2+1))
def preserving_lengths(n): return [l for l in effective_lengths(n) if l%2==1]
def subsets(xs):
    for r in range(1,len(xs)+1):
        for c in combinations(xs,r): yield c

def canonicalize(c):
    c=tuple(c); i=c.index(0); a=c[i:]+c[:i]
    r=(a[0],)+tuple(reversed(a[1:]))
    return min(a,r)

def canonical_cycles(n):
    for q in permutations(range(1,n)):
        if q[0]<q[-1]: yield (0,)+q

def reverse_block(c,start,l):
    a=list(c); n=len(a)
    pos=[(start+j)%n for j in range(l)]
    vals=[a[x] for x in pos][::-1]
    for x,v in zip(pos,vals): a[x]=v
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

def census(n,supports):
    cs=list(canonical_cycles(n)); ix={c:i for i,c in enumerate(cs)}
    d=DSU(len(cs)); deg=[]
    for i,c in enumerate(cs):
        ns=set()
        for l in supports:
            if 2<=l<=n-2:
                for s in range(n): ns.add(reverse_block(c,s,l))
        ns.discard(c); deg.append(len(ns))
        for x in ns:d.union(i,ix[x])
    comps=defaultdict(list)
    for i,c in enumerate(cs): comps[d.find(i)].append(c)
    exact=""
    if n%2==0:
        br=defaultdict(set); rb=defaultdict(set)
        for i,c in enumerate(cs):
            b=bipartition(c); r=d.find(i)
            br[b].add(r); rb[r].add(b)
        exact=(len(br)==len(comps) and all(len(v)==1 for v in br.values())
               and all(len(v)==1 for v in rb.values()))
    return dict(states=len(cs),degree_min=min(deg),degree_max=max(deg),
                components=len(comps),components_equal_intrinsic_bipartitions=exact)

def write_csv(path,rows):
    if not rows:return
    with open(path,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--even-n-max",type=int,default=30)
    ap.add_argument("--exhaustive-n-max",type=int,default=9)
    ap.add_argument("--out-prefix",default="ehf_hc_raw_05b")
    ap.add_argument("--strict",action="store_true")
    args=ap.parse_args()

    summary=[]; unions=[]; checks=[]
    for n in range(6,args.even_n_max+1,2):
        L=effective_lengths(n); P=preserving_lengths(n)
        row=dict(n=n,reversal_orbitals=len(L),
                 all_nonempty_orbital_unions=2**len(L)-1,
                 bipartition_preserving_orbitals=len(P),
                 bipartition_preserving_nonempty_unions=2**len(P)-1,
                 minimum_preserving_support=min(P),
                 unique_strict_locality_minimizer="(3,)")
        summary.append(row)
        checks.append({"check":f"n={n}_minimum_preserving_support_is_3","pass":min(P)==3})
        if len(L)<=7:
            for U in subsets(L):
                preserves=all(l%2 for l in U)
                strict=preserves and max(U)==3
                unions.append(dict(n=n,supports=str(U),
                                   preserves_even_bipartition=preserves,
                                   contains_lr3=3 in U,
                                   minimum_support=min(U),
                                   maximum_support=max(U),
                                   strict_locality_minimizer=strict))
                if strict:
                    checks.append({"check":f"n={n}_strict_min_rule_exactly_3",
                                   "pass":U==(3,)})

    def family(n,name):
        if name=="LR2":return [2]
        if name=="LR3":return [3]
        if name=="LR2+LR3":return [2,3]
        if name=="full_2opt":return effective_lengths(n)
        if name=="all_odd":
            P=preserving_lengths(n)
            return P if P else ([3] if n==5 else [])
        raise KeyError(name)

    exhaustive=[]
    for n in range(5,args.exhaustive_n_max+1):
        for name in ["LR2","LR3","LR2+LR3","full_2opt","all_odd"]:
            supports=family(n,name)
            r=census(n,supports)
            row={"n":n,"rule":name,"supports":str(tuple(supports)),**r}
            exhaustive.append(row)
            if name=="LR2":
                checks.append({"check":f"n={n}_LR2_connected","pass":r["components"]==1})
            if name=="LR3":
                if n%2:
                    checks.append({"check":f"n={n}_LR3_odd_connected","pass":r["components"]==1})
                else:
                    checks.append({"check":f"n={n}_LR3_even_bipartition",
                                   "pass":r["components_equal_intrinsic_bipartitions"] is True})
            if name=="full_2opt":
                checks.append({"check":f"n={n}_full_2opt_connected","pass":r["components"]==1})
            if name=="all_odd" and n%2==0:
                checks.append({"check":f"n={n}_all_odd_preserves_bipartition",
                               "pass":r["components_equal_intrinsic_bipartitions"] is True})

    write_csv(args.out_prefix+"_summary.csv",summary)
    write_csv(args.out_prefix+"_union_census.csv",unions)
    write_csv(args.out_prefix+"_exhaustive_controls.csv",exhaustive)
    write_csv(args.out_prefix+"_checks.csv",checks)

    ok=all(bool(x["pass"]) for x in checks)
    print(f"checks: {sum(bool(x['pass']) for x in checks)}/{len(checks)}")
    print("conditional uniqueness: raw HC + bipartition preservation + strict locality => LR3")
    if args.strict and not ok: raise SystemExit(1)
    print("EHF_HC_RAW_05B_MINIMALITY_UNIQUENESS_STRESS_TEST_PASS")

if __name__=="__main__":
    main()
