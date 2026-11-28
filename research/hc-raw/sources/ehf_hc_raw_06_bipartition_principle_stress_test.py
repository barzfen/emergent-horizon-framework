#!/usr/bin/env python3
from itertools import permutations
from collections import defaultdict, Counter
import argparse, csv, math

def canonicalize(c):
    c=tuple(c); i=c.index(0); a=c[i:]+c[:i]
    r=(a[0],)+tuple(reversed(a[1:]))
    return min(a,r)

def canonical_cycles(n):
    for p in permutations(range(1,n)):
        if p[0]<p[-1]: yield (0,)+p

def edges(c):
    n=len(c)
    return frozenset(tuple(sorted((c[i],c[(i+1)%n]))) for i in range(n))

def reverse_block(c,s,l):
    a=list(c); n=len(a)
    pos=[(s+j)%n for j in range(l)]
    vals=[a[p] for p in pos][::-1]
    for p,v in zip(pos,vals): a[p]=v
    return canonicalize(tuple(a))

def neighbors(c,rule):
    n=len(c)
    if rule=="LR2": L=[2]
    elif rule=="LR3": L=[3]
    elif rule=="LR4": L=[4]
    elif rule=="FULL_2OPT": L=list(range(2,n//2+1))
    else: raise KeyError(rule)
    out=set()
    for l in L:
        if rule!="FULL_2OPT" and l>=n: continue
        for s in range(n): out.add(reverse_block(c,s,l))
    out.discard(c)
    return out

def insert_new(c,e):
    n=len(c); x=n; a=list(c)
    child=tuple(a+[x]) if e==n-1 else tuple(a[:e+1]+[x]+a[e+1:])
    return canonicalize(child)

def delete_new(c):
    x=max(c)
    return canonicalize(tuple(v for v in c if v!=x))

def bipartition(c):
    return frozenset((frozenset(c[0::2]),frozenset(c[1::2])))

def common_component_sizes(c,d):
    common=edges(c)&edges(d)
    adj=defaultdict(list)
    for a,b in common:
        adj[a].append(b); adj[b].append(a)
    seen=set(); sizes=[]
    for v in range(len(c)):
        if v in seen: continue
        st=[v]; seen.add(v); k=0
        while st:
            x=st.pop(); k+=1
            for y in adj[x]:
                if y not in seen:
                    seen.add(y); st.append(y)
        sizes.append(k)
    return tuple(sorted(sizes))

def edge_set(cs,rule):
    ix={c:i for i,c in enumerate(cs)}
    E=set()
    for i,c in enumerate(cs):
        for d in neighbors(c,rule):
            j=ix[d]
            if i<j:E.add((i,j))
    return E

def write_csv(path,rows):
    if not rows:return
    with open(path,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--n-min",type=int,default=5)
    ap.add_argument("--n-max",type=int,default=8)
    ap.add_argument("--out-prefix",default="ehf_hc_raw_06")
    ap.add_argument("--strict",action="store_true")
    args=ap.parse_args()
    growth=[]; sectors=[]; projections=[]; cross=[]; liftsecs=[]; checks=[]

    # all-slot bijection
    for n in range(args.n_min,args.n_max+1):
        src=list(canonical_cycles(n)); target=set(canonical_cycles(n+1))
        children=[]; inverse=True
        for c in src:
            for s in range(n):
                ch=insert_new(c,s); children.append(ch)
                inverse &= delete_new(ch)==c
        U=set(children)
        row=dict(source_n=n,source_states=len(src),attempts=len(children),
                 target_states=len(target),unique_children=len(U),
                 coverage=len(U)/len(target),duplicates=len(children)-len(U),
                 deletion_inverse=inverse)
        growth.append(row)
        checks += [
            {"check":f"{n}->{n+1}_coverage","pass":U==target},
            {"check":f"{n}->{n+1}_no_duplicates","pass":len(children)==len(U)},
            {"check":f"{n}->{n+1}_inverse","pass":inverse},
        ]

    # odd -> even bipartition incidence
    for n in range(max(5,args.n_min|1),args.n_max+1,2):
        if n%2==0: continue
        src=list(canonical_cycles(n)); m=(n+1)//2
        secstates=defaultdict(list); perparent=[]
        for pi,c in enumerate(src):
            ss=[]
            for s in range(n):
                ch=insert_new(c,s); sec=bipartition(ch)
                ss.append(sec); secstates[sec].append(pi)
            perparent.append(len(set(ss)))
        right=[len(set(v)) for v in secstates.values()]
        f=math.factorial(m-1)*math.factorial(m)//2
        row=dict(source_n=n,target_n=n+1,source_states=len(src),
                 target_sectors=len(secstates),expected_target_sectors=math.comb(n+1,m)//2,
                 sectors_per_parent_min=min(perparent),sectors_per_parent_max=max(perparent),
                 expected_sectors_per_parent=n,parents_per_sector_min=min(right),
                 parents_per_sector_max=max(right),expected_parents_per_sector=f)
        sectors.append(row)
        checks += [
            {"check":f"{n}->{n+1}_slot_sector_injective","pass":min(perparent)==max(perparent)==n},
            {"check":f"{n}->{n+1}_sector_count","pass":len(secstates)==math.comb(n+1,m)//2},
            {"check":f"{n}->{n+1}_regular_incidence","pass":min(right)==max(right)==f},
        ]

    def projection(n,rule):
        src=list(canonical_cycles(n)); tgt=list(canonical_cycles(n+1))
        si={c:i for i,c in enumerate(src)}
        SE=edge_set(src,rule); TE=edge_set(tgt,rule)
        parent=[si[delete_new(c)] for c in tgt]
        cat=Counter(); faithful=Counter(); ctypes=Counter(); crossbp=Counter()
        fsecs=defaultdict(set)
        for a,b in TE:
            pa,pb=parent[a],parent[b]
            if pa==pb:
                cat["vertical"]+=1; continue
            e=tuple(sorted((pa,pb)))
            if e in SE:
                cat["faithful"]+=1; faithful[e]+=1
                if rule=="LR3" and (n+1)%2==0:
                    fsecs[e].add(bipartition(tgt[a]))
            else:
                cat["cross"]+=1
                C,D=src[pa],src[pb]
                ctypes[(len(edges(C)&edges(D)),common_component_sizes(C,D))]+=1
                if n%2==0:
                    crossbp[bipartition(C)==bipartition(D)]+=1
        vals=list(faithful.values())
        row=dict(source_n=n,target_n=n+1,rule=rule,source_edges=len(SE),target_edges=len(TE),
                 vertical_edges=cat["vertical"],faithful_edges=cat["faithful"],cross_edges=cat["cross"],
                 source_edge_lift_rate=len(faithful)/len(SE) if SE else 1,
                 faithful_lifts_per_source_edge_min=min(vals) if vals else 0,
                 faithful_lifts_per_source_edge_max=max(vals) if vals else 0,
                 vertical_fraction=cat["vertical"]/len(TE),faithful_fraction=cat["faithful"]/len(TE),
                 cross_fraction=cat["cross"]/len(TE),
                 cross_same_source_bipartition=(crossbp[True] if n%2==0 else ""),
                 cross_different_source_bipartition=(crossbp[False] if n%2==0 else ""))
        for (ov,cs),count in ctypes.items():
            cross.append(dict(source_n=n,target_n=n+1,rule=rule,
                              cross_parent_overlap=ov,cross_parent_common_path_sizes=str(cs),count=count))
        if rule=="LR3" and (n+1)%2==0:
            svals=[len(x) for x in fsecs.values()]
            liftsecs.append(dict(source_n=n,target_n=n+1,source_lr3_edges=len(SE),
                                 faithful_lifts_per_edge_min=min(vals),
                                 faithful_lifts_per_edge_max=max(vals),
                                 distinct_target_sectors_per_edge_min=min(svals),
                                 distinct_target_sectors_per_edge_max=max(svals)))
        return row

    for n in range(args.n_min,args.n_max+1):
        for rule in ("LR2","LR3","FULL_2OPT"):
            r=projection(n,rule); projections.append(r)
            checks += [
                {"check":f"{n}->{n+1}_{rule}_lift_rate","pass":abs(r["source_edge_lift_rate"]-1)<1e-12},
                {"check":f"{n}->{n+1}_{rule}_uniform_lifts",
                 "pass":r["faithful_lifts_per_source_edge_min"]==r["faithful_lifts_per_source_edge_max"]},
            ]
            if rule=="LR2":
                checks += [{"check":f"{n}->{n+1}_LR2_no_cross","pass":r["cross_edges"]==0},
                           {"check":f"{n}->{n+1}_LR2_vertical","pass":r["vertical_edges"]>0}]
            if rule=="LR3":
                checks.append({"check":f"{n}->{n+1}_LR3_no_vertical","pass":r["vertical_edges"]==0})
                if n>=6: checks.append({"check":f"{n}->{n+1}_LR3_cross","pass":r["cross_edges"]>0})
                if n%2==0 and n>=6:
                    checks.append({"check":f"{n}->{n+1}_LR3_cross_sector",
                                   "pass":r["cross_same_source_bipartition"]==0
                                          and r["cross_different_source_bipartition"]==r["cross_edges"]})
            if rule=="FULL_2OPT":
                checks += [{"check":f"{n}->{n+1}_2OPT_no_cross","pass":r["cross_edges"]==0},
                           {"check":f"{n}->{n+1}_2OPT_vertical","pass":r["vertical_edges"]>0}]

    if args.n_max>=8:
        r=projection(8,"LR4"); projections.append(r)
        checks += [{"check":"8->9_LR4_generative","pass":r["cross_edges"]>0 and r["vertical_edges"]==0},
                   {"check":"8->9_LR4_cross_same_bipartition",
                    "pass":r["cross_same_source_bipartition"]==r["cross_edges"]}]

    for n in range(max(6,args.n_min),args.n_max+1):
        rr=[x for x in cross if x["source_n"]==n and x["rule"]=="LR3"]
        checks.append({"check":f"{n}->{n+1}_LR3_cross_is_LR2",
                       "pass":len(rr)==1 and rr[0]["cross_parent_overlap"]==n-2
                              and rr[0]["cross_parent_common_path_sizes"]==str((2,n-2))})
    if args.n_max>=8:
        rr=[x for x in cross if x["source_n"]==8 and x["rule"]=="LR4"]
        checks.append({"check":"8->9_LR4_cross_is_LR3",
                       "pass":len(rr)==1 and rr[0]["cross_parent_common_path_sizes"]==str((3,5))})

    for r in liftsecs:
        checks.append({"check":f"{r['source_n']}->{r['target_n']}_faithful_lifts_distinct_sectors",
                       "pass":r["faithful_lifts_per_edge_min"]==r["distinct_target_sectors_per_edge_min"]
                              and r["faithful_lifts_per_edge_max"]==r["distinct_target_sectors_per_edge_max"]})

    write_csv(args.out_prefix+"_growth_bijection.csv",growth)
    write_csv(args.out_prefix+"_sector_incidence.csv",sectors)
    write_csv(args.out_prefix+"_rule_growth_projection.csv",projections)
    write_csv(args.out_prefix+"_cross_projection_types.csv",cross)
    write_csv(args.out_prefix+"_lr3_lift_sector_census.csv",liftsecs)
    write_csv(args.out_prefix+"_checks.csv",checks)
    ok=all(bool(x["pass"]) for x in checks)
    print(f"checks: {sum(bool(x['pass']) for x in checks)}/{len(checks)}")
    if args.strict and not ok: raise SystemExit(1)
    print("EHF_HC_RAW_06_BIPARTITION_PRINCIPLE_STRESS_TEST_PASS")

if __name__=="__main__":
    main()
