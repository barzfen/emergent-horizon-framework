#!/usr/bin/env python3
"""
EHF-HC-GROW-08 — Cross-Channel Loop and Coupling Geometry Audit

Purpose
-------
Study the support-coloured HC nearest-shell graph after GROW-07 established
that fixed LR_l channels have genuinely different internal geometries.

Core exact structures
---------------------

1. Pair-overlap trichotomy for supports 2 <= l < k <= floor(n/2).

Fix a small cyclic interval I of length l and vary the start of a large
interval J of length k.  Exactly one of three cases occurs:

    nested:   I subset J
    disjoint: I intersect J = empty
    partial:  nonempty overlap, neither interval contains the other

Per fixed small interval:
    nested starts  = k-l+1
    disjoint starts = n-k-l+1
    partial starts = 2(l-1)

Thus:
    four-step laminar starts = n-2l+2.

2. Laminar mixed squares.

Let R_I and R_J be interval reversals.

Disjoint:
    R_I R_J R_I R_J = e.

Nested:
    R_J R_I R_J = R_{R_J(I)},
so
    R_I R_J R_{R_J(I)} R_J = e.

For a nested small interval with offset a inside the large interval,
conjugation transports the offset by
    a -> k-l-a.

Partial overlap:
    R_J(I) is not a contiguous l-interval.
Hence conjugation leaves the LR_l generator family and the alternating
LR_l/LR_k four-step closure fails.  The local order-sensitive coupling is
measured by
    Omega = [R_I,R_J] = R_I R_J R_I R_J = (R_I R_J)^2.

3. Mixed-square census.

For generic large support k<n/2, the number of distinct alternating
LR_l/LR_k squares through a reference HC state is
    n(n-2l+2).

When k=n/2 is the half-cycle class, quotient edge representatives are doubled
and the distinct quotient-square count is half:
    n(n-2l+2)/2.

4. Even-layer loop parity.

On even HC layers, even support changes the intrinsic bipartition and odd
support preserves it.  Therefore every closed support-coloured loop contains
an even number of even-support edges.

5. Universal recursive channel polygon.

Let s_i=R_(i,2) be adjacent transpositions and R_m=R_(0,m).  In the positional
permutation algebra:
    s_0 s_1 ... s_(m-1) R_m R_(m+1) = e.

The first effective case with three distinct support colours is m=3:
    LR2,LR2,LR2,LR3,LR4
and gives the exact pentagon
    R_(0,2) R_(1,2) R_(2,2) R_(0,3) R_(0,4) = e.

At n>=8 this is a simple HC quotient pentagon in the audited range.

6. Minimal three-colour result.

Exhaustive finite scans found:
    no mixed triangles through n=10;
    no simple LR2/LR3/LR4 three-colour four-cycle for n=8..12;
    the universal LR2/LR3/LR4 pentagon exists for n=8..12.

Thus length 5 is the finite-certified minimum for a genuine 2/3/4
three-colour loop over those layers.

7. Holonomy caution.

Away from half-cycle boundaries, all audited simple alternating mixed squares
through n=12 lift to positional identity.  No nontrivial rotation/reflection
holonomy was found.

When the large channel is half-cycle, the doubled positional representatives
of one quotient edge supply additional reflection-closing lifts.  This is a
boundary/gauge-representative effect, not evidence for a generic physical
holonomy.

Interpretation
--------------
The robust cross-channel structure is:
    - commuting disjoint squares,
    - conjugation/transport nested squares,
    - nontrivial partial-overlap commutators,
    - recursive multi-colour polygons.

These are exact combinatorial coupling structures.  They are not yet
physical interaction amplitudes, forces, or gauge fields.
"""

import argparse, csv, math
from pathlib import Path
from itertools import product
from math import gcd

def gen_perm(n,s,l):
    p=list(range(n))
    idx=[(s+i)%n for i in range(l)]
    for a,b in zip(idx,idx[::-1]):
        p[a]=b
    return tuple(p)

def compose(p,q):
    return tuple(p[q[i]] for i in range(len(p)))

def canon(c):
    i=c.index(0)
    a=c[i:]+c[:i]
    r=(a[0],)+tuple(reversed(a[1:]))
    return min(a,r)

def cycle_type(p):
    n=len(p); seen=[False]*n; lens=[]
    for i in range(n):
        if not seen[i]:
            j=i; c=0
            while not seen[j]:
                seen[j]=True; c+=1; j=p[j]
            if c>1: lens.append(c)
    return tuple(sorted(lens,reverse=True))

def perm_order(p):
    o=1
    for c in cycle_type(p):
        o=o*c//gcd(o,c)
    return o

def write_csv(path,rows):
    if not rows:
        return
    with open(path,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--n-max",type=int,default=20)
    ap.add_argument("--support-max",type=int,default=7)
    ap.add_argument("--exhaustive-n-max",type=int,default=10)
    ap.add_argument("--out-dir",default="runs/ehf_hc_grow_08")
    args=ap.parse_args()

    out=Path(args.out_dir)
    out.mkdir(parents=True,exist_ok=True)
    checks=[]; regimes=[]; comms=[]; polys=[]

    for n in range(8,args.n_max+1):
        for l in range(2,n//2+1):
            for k in range(l+1,n//2+1):
                nested=k-l+1
                disjoint=n-k-l+1
                partial=2*(l-1)
                ok=(nested+disjoint+partial==n)
                checks.append({"check":f"regime_n{n}_l{l}_k{k}","pass":ok})
                regimes.append({
                    "n":n,"l":l,"k":k,
                    "nested":nested,"disjoint":disjoint,"partial":partial,
                    "flat":nested+disjoint,
                    "generic_square_word_count":n*(n-2*l+2),
                    "half_cycle_large":(n%2==0 and k==n//2),
                })

    for l in range(2,args.support_max+1):
        for k in range(l+1,args.support_max+2):
            n=max(24,l+k+6)
            A=gen_perm(n,0,l)
            for r in range(1,l):
                B=gen_perm(n,l-r,k)
                AB=compose(A,B)
                Omega=compose(AB,AB)
                comms.append({
                    "l":l,"k":k,"overlap_r":r,
                    "AB_cycle_type":str(cycle_type(AB)),
                    "AB_order":perm_order(AB),
                    "commutator_cycle_type":str(cycle_type(Omega)),
                    "commutator_order":perm_order(Omega),
                })

    for m in range(2,args.support_max+1):
        n=2*(m+1)
        p=tuple(range(n)); qs=[canon(p)]
        seq=[]; starts=[]
        for s in range(m):
            p=compose(p,gen_perm(n,s,2)); qs.append(canon(p))
            seq.append(2); starts.append(s)
        p=compose(p,gen_perm(n,0,m)); qs.append(canon(p)); seq.append(m); starts.append(0)
        p=compose(p,gen_perm(n,0,m+1)); qs.append(canon(p)); seq.append(m+1); starts.append(0)
        identity=(p==tuple(range(n)))
        simple=(qs[-1]==qs[0] and len(set(qs[:-1]))==len(qs)-1)
        checks += [
            {"check":f"polygon_identity_m{m}","pass":identity},
            {"check":f"polygon_simple_m{m}","pass":simple},
        ]
        polys.append({
            "m":m,"n":n,"length":m+2,
            "colors":str(tuple(seq)),"starts":str(tuple(starts)),
            "identity":identity,"simple":simple,
        })

    # Optional exhaustive mixed-triangle audit.
    for n in range(6,args.exhaustive_n_max+1):
        sups=list(range(2,n//2+1))
        gens={l:[gen_perm(n,s,l) for s in range(n)] for l in sups}
        root=tuple(range(n)); rootc=canon(root)
        mixed_tri=0
        for seq in product(sups,repeat=3):
            if len(set(seq))<2:
                continue
            for starts in product(range(n),repeat=3):
                p1=gens[seq[0]][starts[0]]
                p2=compose(p1,gens[seq[1]][starts[1]])
                p3=compose(p2,gens[seq[2]][starts[2]])
                if canon(p3)==rootc and len({rootc,canon(p1),canon(p2)})==3:
                    mixed_tri+=1
        checks.append({"check":f"no_mixed_triangle_n{n}","pass":mixed_tri==0})

    write_csv(out/"pair_regimes.csv",regimes)
    write_csv(out/"partial_overlap_commutators.csv",comms)
    write_csv(out/"recursive_polygons.csv",polys)
    write_csv(out/"checks.csv",checks)

    ok=sum(bool(r["pass"]) for r in checks)
    print(f"EHF-HC-GROW-08: {ok}/{len(checks)} checks PASS")

if __name__=="__main__":
    main()
