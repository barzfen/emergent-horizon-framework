"""WHEELER-63 bounded extension: minimal seeds with more runs.
Exact endpoint probabilities and orbit sizes; float entropy diagnostics.
No all-time monotonicity is inferred from finite scans.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from math import comb,fsum,log2
from pathlib import Path
import json
from unconditioned_entropy_audit import compositions
from quotient_entropy_audit import canonical_runs,run_row


def endpoint(D,t):
    counts=defaultdict(int);den=comb(3*D+t-1,t)
    for x in compositions(t,D):
        weight=1
        for z in x:weight*=comb(z+2,2)
        counts[canonical_runs(tuple(z+2 for z in x))]+=weight
    assert sum(counts.values())==den
    return {a:F(v,den) for a,v in counts.items()}


def orbit(a):return {a[i:]+a[:i] for i in range(0,len(a),2)}


def h(p):return -fsum(float(v)*log2(float(v)) for v in p if v)


def main():
    scans=[]
    for D,T in ((4,16),(6,16),(8,12),(10,8)):
        rows=[];previous=None;recursive={(2,)*D:F(1)}
        for t in range(T+1):
            p=endpoint(D,t);k=D//2
            if t<=4:
                assert p==recursive
                nxt=defaultdict(F)
                for a,v in p.items():
                    for b,q in run_row(a).items():nxt[b]+=v*q
                recursive=dict(nxt)
            correction=fsum(float(v)*log2(k//len(orbit(a))) for a,v in p.items())
            quotient_h=h(p.values());ordered_h=quotient_h+log2(k)-correction
            # Independently compute ordered entropy from all labelled endpoints.
            den=comb(3*D+t-1,t);terms=[]
            for x in compositions(t,D):
                weight=1
                for z in x:weight*=comb(z+2,2)
                v=weight/den;terms.append(-v*log2(v))
            independent=fsum(terms)
            assert abs(independent-ordered_h)<1e-11
            rows.append({'t':t,'n':2*D+t,'classes':len(p),'H_class_bits':quotient_h,
                         'H_ordered_bits':independent,'expected_log2_stabilizer':correction,
                         'delta_class_bits':None if previous is None else quotient_h-previous})
            previous=quotient_h
        steps=rows[1:];minimum=min(steps,key=lambda r:r['delta_class_bits'])
        scans.append({'D':D,'seed':[2]*D,'horizon':T,'all_observed_increments_positive':all(r['delta_class_bits']>0 for r in steps),
                      'minimum_increment':minimum,'steps':rows})
    result={'probabilities':'exact Fraction','entropy':'floating-point finite diagnostics',
            'quotient_group':'C_(D/2), shifts by two run positions; no reflection or colour exchange',
            'identity':'H(class)=H(ordered)-log2(D/2)+E[log2(stabilizer size)]',
            'all_time_monotonicity_proved_here':False,'recursion_crosscheck_through':4,
            'fixed_D_asymptotic':'(D-1)*log2(t)+O(1); general bounded-quotient corollary, not a novelty claim',
            'scans':scans}
    path=Path(__file__).resolve().parents[2]/'data/wheeler/wheeler-63-results.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in s.items() if k!='steps'} for s in scans],indent=2))

if __name__=='__main__':main()
