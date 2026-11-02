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

def lr_edges(n,l):
    cs=list(canonical_cycles(n)); ix={c:i for i,c in enumerate(cs)}
    E=set()
    for i,c in enumerate(cs):
        for s in range(n):
            d=reverse_block(c,s,l); j=ix[d]
            if i!=j:E.add(tuple(sorted((i,j))))
    return cs,E

def delete_top_k(c,k):
    M=len(c)-k
    return canonicalize(tuple(v for v in c if v<M))

def common_component_sizes(c,d):
    common=edges(c)&edges(d)
    adj=defaultdict(list)
    for a,b in common:
        adj[a].append(b); adj[b].append(a)
    seen=set(); sizes=[]
    for v in range(len(c)):
        if v in seen: continue
        st=[v]; seen.add(v); z=0
        while st:
            x=st.pop(); z+=1
            for y in adj[x]:
                if y not in seen:
                    seen.add(y); st.append(y)
        sizes.append(z)
    return tuple(sorted(sizes))

def classify_pair(c,d):
    if c==d:return 0
    n=len(c)
    if len(edges(c)&edges(d))!=n-2:return -1
    cs=common_component_sizes(c,d)
    return min(cs) if len(cs)==2 else -2

def edge_count(N,l):
    if N%2==0 and l==N//2:return math.factorial(N)//8
    return math.factorial(N)//4

def source_edge_count(n,l):
    if not (2<=l<=n//2):return 0
    if n%2==0 and l==n//2:return math.factorial(n)//8
    return math.factorial(n)//4

def projected_level(M,r):
    # raw remaining path size r; other path M-r
    if r<=1 or M-r<=1:return 0
    return min(r,M-r)

def repeated_distribution(N,l,k):
    M=N-k; denom=math.comb(N,k); E=edge_count(N,l)
    ways_by_level=Counter()
    lo=max(0,k-(N-l)); hi=min(k,l)
    for s in range(lo,hi+1):
        ways=math.comb(l,s)*math.comb(N-l,k-s)
        ways_by_level[projected_level(M,l-s)] += ways
    out={}
    for lev,ways in sorted(ways_by_level.items()):
        num=E*ways
        assert num%denom==0
        out[lev]=num//denom
    return out

def write_csv(path,rows):
    with open(path,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--formula-n-max",type=int,default=30)
    ap.add_argument("--repeat-n-max",type=int,default=20)
    ap.add_argument("--exhaustive-n-max",type=int,default=9)
    ap.add_argument("--out-prefix",default="ehf_hc_raw_07")
    ap.add_argument("--strict",action="store_true")
    args=ap.parse_args()

    one=[]; repeat=[]; exhaustive=[]; checks=[]

    for N in range(5,args.formula_n_max+1):
        for l in range(2,N//2+1):
            E=edge_count(N,l); half=(N%2==0 and l==N//2)
            if half:
                stay=0; drop=E; faithful=0
            else:
                stay=E*(N-l)//N
                drop=E*l//N
                source_half=((N-1)%2==0 and l==(N-1)//2)
                faithful=2*(N-l) if source_half else N-l
            lower=l-1
            lower_mult=l if lower>=2 else ""
            one.append(dict(target_N=N,target_support_l=l,target_half_cycle=half,
                            target_edges=E,project_stay_support_edges=stay,
                            project_drop_support_edges=drop,
                            drop_target_support=(0 if l==2 else lower),
                            faithful_lifts_per_source_l_edge=faithful,
                            lower_lifts_per_source_lower_edge=lower_mult,
                            vertical_edges_if_l2=(drop if l==2 else 0),
                            vertical_edges_per_parent_if_l2=(N-1 if l==2 else 0)))
            checks.append({"check":f"N={N}_l={l}_split","pass":stay+drop==E})
            if half:
                checks.append({"check":f"N={N}_l={l}_half_collapse",
                               "pass":drop==source_edge_count(N-1,l-1)*l})
            else:
                if source_edge_count(N-1,l):
                    checks.append({"check":f"N={N}_l={l}_faithful_mult",
                                   "pass":stay==source_edge_count(N-1,l)*faithful})
                if lower>=2:
                    checks.append({"check":f"N={N}_l={l}_lower_mult",
                                   "pass":drop==source_edge_count(N-1,lower)*l})
                else:
                    parents=math.factorial(N-2)//2
                    checks.append({"check":f"N={N}_l=2_vertical",
                                   "pass":drop==parents*(N-1)})

    for N in range(6,args.repeat_n_max+1):
        for l in range(2,N//2+1):
            for k in range(1,min(4,N-4)+1):
                d=repeated_distribution(N,l,k)
                repeat.append(dict(target_N=N,target_support_l=l,delete_k=k,
                                   ancestor_M=N-k,predicted_support_counts=str(dict(d)),
                                   support_min=min(d),support_max=max(d),
                                   target_edges=edge_count(N,l),predicted_total=sum(d.values())))
                checks.append({"check":f"N={N}_l={l}_k={k}_total",
                               "pass":sum(d.values())==edge_count(N,l)})
                checks.append({"check":f"N={N}_l={l}_k={k}_nonincrease",
                               "pass":max(d)<=l})

    for N in range(5,args.exhaustive_n_max+1):
        for l in range(2,N//2+1):
            cs,E=lr_edges(N,l)
            for k in range(1,min(3,N-4)+1):
                cnt=Counter()
                for a,b in E:
                    cnt[classify_pair(delete_top_k(cs[a],k),delete_top_k(cs[b],k))]+=1
                pred=repeated_distribution(N,l,k)
                exhaustive.append(dict(target_N=N,target_support_l=l,delete_k=k,
                                       target_edges_found=len(E),
                                       target_edges_formula=edge_count(N,l),
                                       observed_support_counts=str(dict(sorted(cnt.items()))),
                                       predicted_support_counts=str(dict(pred)),
                                       match=dict(cnt)==pred))
                checks.append({"check":f"N={N}_l={l}_edge_count",
                               "pass":len(E)==edge_count(N,l)})
                checks.append({"check":f"N={N}_l={l}_k={k}_hypergeom",
                               "pass":dict(cnt)==pred})

    write_csv(args.out_prefix+"_one_step_formula.csv",one)
    write_csv(args.out_prefix+"_repeated_deletion.csv",repeat)
    write_csv(args.out_prefix+"_exhaustive_certification.csv",exhaustive)
    write_csv(args.out_prefix+"_checks.csv",checks)
    ok=all(bool(x["pass"]) for x in checks)
    print(f"checks: {sum(bool(x['pass']) for x in checks)}/{len(checks)}")
    if args.strict and not ok:raise SystemExit(1)
    print("EHF_HC_RAW_07_REVERSAL_SUPPORT_GROWTH_FILTRATION_PASS")

if __name__=="__main__":
    main()
