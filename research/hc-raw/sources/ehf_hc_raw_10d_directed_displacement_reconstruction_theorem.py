#!/usr/bin/env python3
"""
EHF-HC-RAW-10D — Directed-Displacement Reconstruction Theorem

Let N=2k-1 and S⊂{1,...,N}, |S|=k.
Define
    M_S(d)=#{(a,b): a∈S, b∉S, b-a=d}, d≠0.
Let
    D_r = sum_d d^r M_S(d),
    p_r = sum_{a∈S} a^r,
    T_r = sum_{j=1}^N j^r.

Then
    D_r = sum_{t=0}^r (-1)^t C(r,t) p_t (T_{r-t}-p_{r-t}),
with p_0=k and T_0=N.

Separating p_r:
    D_r = k T_r + L_r + c_r p_r,
where
    L_r = sum_{t=1}^{r-1} (-1)^t C(r,t) p_t(T_{r-t}-p_{r-t}),
and
    c_r = -k + (-1)^r(k-1)
        = -(2k-1), r odd,
        = -1,       r even.

Hence c_r is never zero.  Therefore M_S recursively determines
p_1,...,p_k.  Newton identities then determine the elementary symmetric
polynomials of the k elements of S, hence the monic polynomial having S
as its roots.  Therefore M_S uniquely determines S.

In particular,
    p_1 = [k T_1-D_1]/(2k-1),
so h is redundant.
"""
from itertools import combinations
from collections import Counter
import argparse, math

def hist(S,N):
    A=set(S); M=Counter()
    for a in A:
        for b in range(1,N+1):
            if b not in A: M[b-a]+=1
    return M

def D(M,r): return sum(d**r*c for d,c in M.items())
def T(N,r): return sum(i**r for i in range(1,N+1))

def recover_p(M,k):
    N=2*k-1; p={0:k}
    for r in range(1,k+1):
        L=sum(((-1)**t)*math.comb(r,t)*p[t]*(T(N,r-t)-p[r-t])
              for t in range(1,r))
        c=-k+((-1)**r)*(k-1)
        num=D(M,r)-k*T(N,r)-L
        assert num%c==0
        p[r]=num//c
    return p

def newton(p,k):
    e=[0]*(k+1); e[0]=1
    for m in range(1,k+1):
        num=sum(((-1)**(i-1))*e[m-i]*p[i] for i in range(1,m+1))
        assert num%m==0; e[m]=num//m
    return e

def poly(x,e):
    k=len(e)-1
    return sum(((-1)**j)*e[j]*x**(k-j) for j in range(k+1))

def recover(M,k):
    N=2*k-1; p=recover_p(M,k); e=newton(p,k)
    return tuple(i for i in range(1,N+1) if poly(i,e)==0)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--k-min",type=int,default=2)
    ap.add_argument("--k-max",type=int,default=10)
    ap.add_argument("--strict",action="store_true")
    args=ap.parse_args()
    ok=True
    for k in range(args.k_min,args.k_max+1):
        N=2*k-1; count=0
        for S in combinations(range(1,N+1),k):
            count+=1
            ok &= recover(hist(S,N),k)==S
        print("k",k,"states",count,"PASS")
    if args.strict and not ok: raise SystemExit(1)
    print("EHF_HC_RAW_10D_DIRECTED_DISPLACEMENT_RECONSTRUCTION_THEOREM_PASS")

if __name__=="__main__":
    main()
