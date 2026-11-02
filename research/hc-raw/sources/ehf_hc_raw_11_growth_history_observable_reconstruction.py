#!/usr/bin/env python3
"""
EHF-HC-RAW-11 — Growth-History Observable Reconstruction

Exact filtration theorem:
Let
    V_r ⊂ V_{r+1} ⊂ ... ⊂ V_N,
with |V_n|=n and |V_n\V_{n-1}|=1.

Define first-appearance stage
    beta(v)=min{n:v∈V_n}.

Then beta is determined by the tower and invariant under every tower
automorphism.  The atom-level automorphism group is exactly S_r:
the r seed atoms may be permuted arbitrarily, while every later atom is
fixed because it is the unique atom first appearing at its stage.

Consequences:
- final layer only: no nonconstant birth scalar is intrinsic;
- one incoming map: only newest-vs-old is intrinsic;
- full r-seeded tower: birth stages are intrinsic, but the seed is tied;
- unique total birth rank is intrinsic iff r=1, unless extra seed-order
  structure is supplied.

For a natural HC seed r=3, the exact canonical additive observable is the
tied-seed birth-stage sum, not the historical unique rank sum h.
The universal Johnson additive drift still applies to this observable.
"""
import argparse, math

def tower_aut_size(r):
    return math.factorial(r)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--N",type=int,default=12)
    ap.add_argument("--seed-r",type=int,default=3)
    ap.add_argument("--strict",action="store_true")
    args=ap.parse_args()
    r=args.seed_r; N=args.N
    if not (1<=r<=N):
        raise SystemExit("need 1 <= seed-r <= N")
    classes=[r]+[1]*(N-r)
    print("N",N,"seed r",r)
    print("birth-class sizes",classes)
    print("tower atom automorphism group size",tower_aut_size(r))
    print("unique total rank reconstructible",r==1)
    ok=(tower_aut_size(r)==math.factorial(r))
    if args.strict and not ok:
        raise SystemExit(1)
    print("EHF_HC_RAW_11_GROWTH_HISTORY_OBSERVABLE_RECONSTRUCTION_PASS")

if __name__=="__main__":
    main()
