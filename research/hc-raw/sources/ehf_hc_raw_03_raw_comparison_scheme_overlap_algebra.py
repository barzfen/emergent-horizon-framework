#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv
from itertools import permutations
from collections import Counter, defaultdict
from pathlib import Path

def canonical_cycles(n):
    for p in permutations(range(1,n)):
        if p[0] < p[-1]:
            yield (0,) + p

def make_mask_tools(n):
    pairs=[]; idx={}
    for a in range(n):
        for b in range(a+1,n):
            idx[(a,b)] = len(pairs); pairs.append((a,b))

    def emask(c):
        m=0
        for i in range(n):
            a,b=c[i],c[(i+1)%n]
            if a>b: a,b=b,a
            m |= 1 << idx[(a,b)]
        return m

    bitperms=[]
    for sign in (1,-1):
        for shift in range(n):
            lab=[(sign*x+shift)%n for x in range(n)]
            bp=[]
            for u,v in pairs:
                a,b=lab[u],lab[v]
                if a>b:a,b=b,a
                bp.append(idx[(a,b)])
            bitperms.append(bp)

    def tmask(m,bp):
        out=0
        while m:
            lb=m & -m
            i=lb.bit_length()-1
            out |= 1 << bp[i]
            m -= lb
        return out

    def orbital_key(m):
        return min(tmask(m,bp) for bp in bitperms)

    return emask, orbital_key

def overlap(a,b):
    return (a & b).bit_count()

def profile_signature(ref,y,masks):
    return tuple(sorted(Counter((overlap(ref,z),overlap(y,z)) for z in masks).items()))

def inverse_orbital_key(n, cycle, emask, orbital_key):
    inv=[0]*n
    for i,x in enumerate(cycle):
        inv[x]=i
    tr=tuple(inv[x] for x in range(n))
    return orbital_key(emask(tr))

def relation_orbital_key(n, source, target, emask, orbital_key):
    inv=[0]*n
    for i,x in enumerate(source):
        inv[x]=i
    tr=tuple(inv[x] for x in target)
    return orbital_key(emask(tr))

def audit_n(n, do_symmetrized_test=True):
    cycles=list(canonical_cycles(n))
    emask, orbital_key = make_mask_tools(n)
    masks=[emask(c) for c in cycles]
    refc=tuple(range(n)); ref=emask(refc)

    byov=defaultdict(list)
    for i,m in enumerate(masks):
        byov[overlap(ref,m)].append(i)

    sig_for={}
    sig_classes={}
    assoc=True
    witness=None
    for k in sorted(byov):
        gs=defaultdict(list)
        for i in byov[k]:
            sig=profile_signature(ref,masks[i],masks)
            sig_for[i]=sig
            gs[sig].append(i)
        sig_classes[k]=gs
        if len(gs)>1:
            assoc=False
            if witness is None:
                items=list(gs.items())
                s1,ids1=items[0]; s2,ids2=items[1]
                d1,d2=dict(s1),dict(s2)
                diff=next((q,d1.get(q,0),d2.get(q,0)) for q in sorted(set(d1)|set(d2))
                          if d1.get(q,0)!=d2.get(q,0))
                witness=dict(overlap_class=k, cycle_1=cycles[ids1[0]], cycle_2=cycles[ids2[0]],
                             intersection_pair_i_j=diff[0], count_1=diff[1], count_2=diff[2])

    orbital_for={}
    og=defaultdict(list)
    orbital_ov={}
    for i,m in enumerate(masks):
        key=orbital_key(m)
        orbital_for[i]=key
        og[key].append(i)
        orbital_ov[key]=overlap(ref,m)

    sig_to_orb=defaultdict(set); orb_to_sig=defaultdict(set)
    for i in range(len(cycles)):
        sig=sig_for.get(i) or profile_signature(ref,masks[i],masks)
        key=orbital_for[i]
        sig_to_orb[sig].add(key); orb_to_sig[key].add(sig)
    bij=(all(len(v)==1 for v in sig_to_orb.values())
         and all(len(v)==1 for v in orb_to_sig.values()))

    orb_by_ov=Counter(orbital_ov[k] for k in og)

    reps={k:cycles[v[0]] for k,v in og.items()}
    invkey={k:inverse_orbital_key(n,c,emask,orbital_key) for k,c in reps.items()}
    selfT=sum(k==v for k,v in invkey.items())
    Tp=(len(invkey)-selfT)//2

    sym_pass=None; sym_n=None; sym_fail=None
    if do_symmetrized_test:
        pairs=sorted({tuple(sorted((k,invkey[k]))) for k in invkey})
        pid={p:i for i,p in enumerate(pairs)}
        sid={k:pid[tuple(sorted((k,invkey[k])))] for k in invkey}
        targets=defaultdict(list)
        for i in range(len(cycles)):
            targets[sid[orbital_for[i]]].append(i)
        fails=0
        for _,ids in targets.items():
            ss=set()
            for yi in ids:
                y=cycles[yi]
                cnt=Counter()
                for z in cycles:
                    k1=orbital_key(emask(z))
                    k2=relation_orbital_key(n,y,z,emask,orbital_key)
                    cnt[(sid[k1],sid[k2])] += 1
                ss.add(tuple(sorted(cnt.items())))
            if len(ss)>1:fails+=1
        sym_pass=(fails==0); sym_n=len(pairs); sym_fail=fails

    rows=[]
    for k in sorted(byov):
        rows.append(dict(n=n,overlap=k,states_in_overlap_class=len(byov[k]),
                         intersection_profile_classes=len(sig_classes[k]),
                         orbital_classes=orb_by_ov[k],
                         profile_matches_orbitals=(len(sig_classes[k])==orb_by_ov[k])))

    summary=dict(
        n=n,states=len(cycles),overlap_relation_count=len(byov),
        overlap_association_scheme_pass=assoc,
        intersection_profile_classes=len(sig_to_orb),
        orbital_classes=len(og),
        profile_orbital_bijection=bij,
        self_transpose_orbitals=selfT,
        transpose_orbital_pairs=Tp,
        symmetrized_orbital_classes=sym_n,
        symmetrized_association_scheme_pass=sym_pass,
        symmetrized_fail_classes=sym_fail
    )
    return summary,rows,witness

def write_csv(path,rows):
    if not rows:return
    with open(path,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--n-min",type=int,default=4)
    ap.add_argument("--n-max",type=int,default=8)
    ap.add_argument("--symmetrized-max-n",type=int,default=7)
    ap.add_argument("--out-prefix",default="ehf_hc_raw_03")
    ap.add_argument("--strict",action="store_true")
    args=ap.parse_args()
    sums=[]; rows=[]; wit=[]
    for n in range(args.n_min,args.n_max+1):
        s,r,w=audit_n(n,n<=args.symmetrized_max_n)
        sums.append(s);rows.extend(r)
        if w:wit.append({"n":n,**w})
        print(n,s)
    write_csv(args.out_prefix+"_summary.csv",sums)
    write_csv(args.out_prefix+"_overlap_refinement.csv",rows)
    write_csv(args.out_prefix+"_association_failure_witnesses.csv",wit)

if __name__=="__main__":
    main()
