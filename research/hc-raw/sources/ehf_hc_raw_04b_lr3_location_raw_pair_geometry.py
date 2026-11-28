#!/usr/bin/env python3
from itertools import permutations
from collections import defaultdict
import argparse, csv

def canonicalize(c):
    n=len(c); i=c.index(0)
    a=tuple(c[i:]+c[:i])
    r=(a[0],)+tuple(reversed(a[1:]))
    return min(a,r)

def canonical_cycles(n):
    for p in permutations(range(1,n)):
        if p[0] < p[-1]:
            yield (0,) + p

def edges(c):
    n=len(c)
    return frozenset(tuple(sorted((c[i],c[(i+1)%n]))) for i in range(n))

def reverse_circular(c,start,length):
    n=len(c); arr=list(c)
    pos=[(start+j)%n for j in range(length)]
    vals=[arr[p] for p in pos][::-1]
    for p,v in zip(pos,vals): arr[p]=v
    return canonicalize(tuple(arr))

def common_component_sizes(c,d):
    common=edges(c)&edges(d)
    adj=defaultdict(list)
    for a,b in common:
        adj[a].append(b); adj[b].append(a)
    seen=set(); sizes=[]
    for v in range(len(c)):
        if v in seen: continue
        stack=[v]; seen.add(v); size=0
        while stack:
            x=stack.pop(); size+=1
            for y in adj[x]:
                if y not in seen:
                    seen.add(y); stack.append(y)
        sizes.append(size)
    return tuple(sorted(sizes))

def bipartition(c):
    return frozenset((frozenset(c[0::2]),frozenset(c[1::2])))

def make_orbital_key(n):
    pairs=[]; idx={}
    for a in range(n):
        for b in range(a+1,n):
            idx[(a,b)]=len(pairs); pairs.append((a,b))
    def mask(c):
        m=0
        for a,b in edges(c): m |= 1<<idx[(a,b)]
        return m
    bitperms=[]
    for sign in (1,-1):
        for shift in range(n):
            lab=[(sign*x+shift)%n for x in range(n)]
            bp=[]
            for a,b in pairs:
                u,v=lab[a],lab[b]
                if u>v:u,v=v,u
                bp.append(idx[(u,v)])
            bitperms.append(bp)
    def tmask(m,bp):
        out=0
        while m:
            lb=m&-m; i=lb.bit_length()-1
            out |= 1<<bp[i]; m-=lb
        return out
    def key(c):
        m=mask(c)
        return min(tmask(m,bp) for bp in bitperms)
    return key

class DSU:
    def __init__(self,n): self.p=list(range(n)); self.sz=[1]*n
    def find(self,x):
        while self.p[x]!=x:
            self.p[x]=self.p[self.p[x]]; x=self.p[x]
        return x
    def union(self,a,b):
        a=self.find(a); b=self.find(b)
        if a==b:return
        if self.sz[a]<self.sz[b]: a,b=b,a
        self.p[b]=a; self.sz[a]+=self.sz[b]

def reference_class_audit(n):
    ref=tuple(range(n)); re=edges(ref); okey=make_orbital_key(n)
    rows=[]; union=set(); orbitals=set()
    for l in range(2,n//2+1):
        ns={reverse_circular(ref,s,l) for s in range(n)}
        ns.discard(ref); union|=ns
        oks={okey(d) for d in ns}; orbitals|=oks
        ovs={len(re&edges(d)) for d in ns}
        comps={common_component_sizes(ref,d) for d in ns}
        bp=""
        if n%2==0:
            bp={bipartition(d)==bipartition(ref) for d in ns}=={True}
        expected=n//2 if (n%2==0 and l==n//2) else n
        rows.append({
            "n":n,"effective_reversal_length":l,
            "unique_neighbors":len(ns),"expected_neighbors":expected,
            "overlap":next(iter(ovs)) if len(ovs)==1 else str(sorted(ovs)),
            "raw_distance":n-next(iter(ovs)) if len(ovs)==1 else "",
            "common_component_sizes":str(next(iter(comps))) if len(comps)==1 else str(sorted(comps)),
            "orbital_count":len(oks),
            "preserves_intrinsic_bipartition":bp
        })
    return rows,len(union),len(orbitals)

def lr3_components(n):
    cycles=list(canonical_cycles(n)); ix={c:i for i,c in enumerate(cycles)}
    dsu=DSU(len(cycles)); degs=[]
    for i,c in enumerate(cycles):
        ns={reverse_circular(c,s,3) for s in range(n)}
        ns.discard(c); degs.append(len(ns))
        for d in ns: dsu.union(i,ix[d])
    comps=defaultdict(list)
    for i,c in enumerate(cycles): comps[dsu.find(i)].append(c)
    bp_count=""; exact=""
    if n%2==0:
        bp_roots=defaultdict(set)
        for i,c in enumerate(cycles): bp_roots[bipartition(c)].add(dsu.find(i))
        bp_count=len(bp_roots)
        exact=(len(bp_roots)==len(comps) and all(len(v)==1 for v in bp_roots.values()))
    return {
        "n":n,"states":len(cycles),"degree_min":min(degs),"degree_max":max(degs),
        "components":len(comps),"component_size_min":min(map(len,comps.values())),
        "component_size_max":max(map(len,comps.values())),
        "intrinsic_bipartitions":bp_count,
        "components_equal_bipartitions":exact,
        "connected":len(comps)==1
    }

def write_csv(path,rows):
    with open(path,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--class-n-max",type=int,default=20)
    ap.add_argument("--component-n-max",type=int,default=9)
    ap.add_argument("--out-prefix",default="ehf_hc_raw_04b")
    ap.add_argument("--strict",action="store_true")
    args=ap.parse_args()

    class_rows=[]; summaries=[]; checks=[]
    for n in range(5,args.class_n_max+1):
        rows,u,o=reference_class_audit(n)
        class_rows += rows
        s={"n":n,"nearest_shell_degree":u,"expected_2opt_degree":n*(n-3)//2,
           "nearest_shell_orbitals":o,"expected_reversal_classes":n//2-1}
        summaries.append(s)
        checks.append({"check":f"n={n}_2opt_partition","pass":u==s["expected_2opt_degree"]})
        checks.append({"check":f"n={n}_orbital_count","pass":o==s["expected_reversal_classes"]})
        for r in rows:
            l=r["effective_reversal_length"]
            checks.append({"check":f"n={n}_l={l}_degree","pass":r["unique_neighbors"]==r["expected_neighbors"]})
            checks.append({"check":f"n={n}_l={l}_distance2","pass":r["overlap"]==n-2 and r["raw_distance"]==2})
            checks.append({"check":f"n={n}_l={l}_one_orbital","pass":r["orbital_count"]==1})
            checks.append({"check":f"n={n}_l={l}_component_sizes","pass":r["common_component_sizes"]==str((l,n-l))})
            if n%2==0:
                checks.append({"check":f"n={n}_l={l}_bipartition_parity",
                               "pass":r["preserves_intrinsic_bipartition"]==(l%2==1)})

    comps=[]
    for n in range(5,args.component_n_max+1):
        c=lr3_components(n); comps.append(c)
        if n%2:
            checks.append({"check":f"n={n}_lr3_connected","pass":c["connected"]})
        else:
            checks.append({"check":f"n={n}_lr3_components=bipartitions",
                           "pass":c["components_equal_bipartitions"] is True})

    for n in range(6,args.class_n_max+1,2):
        preserving=[r["effective_reversal_length"] for r in class_rows
                    if r["n"]==n and r["preserves_intrinsic_bipartition"] is True]
        checks.append({"check":f"n={n}_lr3_minimal_preserver",
                       "pass":bool(preserving) and min(preserving)==3})

    write_csv(args.out_prefix+"_summary.csv",summaries)
    write_csv(args.out_prefix+"_reversal_classes.csv",class_rows)
    write_csv(args.out_prefix+"_components.csv",comps)
    write_csv(args.out_prefix+"_checks.csv",checks)

    ok=all(bool(x["pass"]) for x in checks)
    print(f"checks: {sum(bool(x['pass']) for x in checks)}/{len(checks)}")
    for c in comps: print(c)
    if args.strict and not ok: raise SystemExit(1)

if __name__=="__main__":
    main()
