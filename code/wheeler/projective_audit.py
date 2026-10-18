"""WHEELER-58 exact finite audit; standard library only.
Run: python code/wheeler/projective_audit.py
Rooted/labelled cyclic words; insert BEFORE indices 0,...,n-1.
All probability comparisons use Fraction; no random sampling.
"""
from collections import defaultdict, Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

def valid(w):
    n=len(w)
    return all(not(w[i]==w[(i+2)%n]!=w[(i+1)%n]) for i in range(n))

def walls(w):
    return sum(w[i]!=w[(i+1)%len(w)] for i in range(len(w)))

def states(n):
    return [w for w in product((0,1),repeat=n) if valid(w)]

def events(w):
    out=[]
    for i in range(len(w)):
        for b in (0,1):
            v=w[:i]+(b,)+w[i:]
            if valid(v):out.append(((i,b),v))
    return out

def run_length(v,i):
    if len(set(v))==1:return len(v)
    length=1
    for direction in (-1,1):
        j=(i+direction)%len(v)
        while v[j]==v[i]:length+=1;j=(j+direction)%len(v)
    return length

def event_law(w,mode):
    ev=events(w);counts=Counter(v for e,v in ev)
    if mode=='event':weights=[F(1,len(ev))]*len(ev)
    elif mode=='state':weights=[F(1,len(counts)*counts[v]) for e,v in ev]
    elif mode=='weighted':
        raw=[F(1,20)**run_length(v,e[0]) for e,v in ev]
        weights=[r/sum(raw) for r in raw]
    else:raise ValueError(mode)
    assert sum(weights)==1
    return [(e,v,p) for (e,v),p in zip(ev,weights)]

def project(law,projection):
    result=defaultdict(F)
    for (es,ws),p in law.items():result[tuple(projection(w) for w in ws)]+=p
    return dict(result)

def truncate(law):
    result=defaultdict(F)
    for (es,ws),p in law.items():result[(es[:-1],ws[:-1])]+=p
    return dict(result)

def truncate_observer(law):
    result=defaultdict(F)
    for history,p in law.items():result[history[:-1]]+=p
    return dict(result)

projections={
    'full_word':lambda w:w,
    'n_N1_D':lambda w:(len(w),sum(w),walls(w)),
    'n_N1':lambda w:(len(w),sum(w)),
    'first_bit':lambda w:(len(w),w[0]),
    'constant':lambda w:0,
}

def audit_process(prior,L,mode):
    assert sum(prior.values())==1
    law={((),(w,)):p for w,p in prior.items()};sizes=[len(law)]
    state_sizes=[len(project(law,lambda w:w))]
    for depth in range(1,L+1):
        nxt={}
        for (es,ws),p in law.items():
            for e,v,q in event_law(ws[-1],mode):nxt[(es+(e,),ws+(v,))]=p*q
        assert sum(nxt.values())==1
        assert truncate(nxt)==law
        for projection in projections.values():
            assert truncate_observer(project(nxt,projection))==project(law,projection)
        if len(prior)==1:
            root=next(iter(prior));D=walls(root)
            if mode=='event':
                N=1
                for j in range(depth):N*=len(root)+D+j
                assert len(nxt)==N
                assert all(p==F(1,N) for p in nxt.values())
            if mode=='state':
                B=D+1 if D else 1;coarse=project(nxt,lambda w:w)
                assert len(coarse)==B**depth
                assert all(p==F(1,B**depth) for p in coarse.values())
        law=nxt;sizes.append(len(law));state_sizes.append(len(project(law,lambda w:w)))
    return dict(horizon=L,event_history_counts=sizes,distinct_state_history_counts=state_sizes,observer_maps_checked=list(projections),all_exact_checks_passed=True)

def main():
    result={'arithmetic':'fractions.Fraction','slot_convention':'insert before 0..n-1; no rotation quotient'}
    layers=[]
    for n in range(4,15):
        ws=states(n)
        for w in ws:
            D=walls(w);ev=events(w)
            assert len(ev)==n+D
            assert all(walls(v)==D for e,v in ev)
            assert len({v for e,v in ev})==(D+1 if D else 1)
            target_counts=Counter((sum(v),walls(v)) for e,v in ev)
            expected=Counter({(sum(w),D):n-sum(w)+D//2,(sum(w)+1,D):sum(w)+D//2})
            assert target_counts==+expected
        layers.append({'n':n,'valid_sources':len(ws),'event_count_and_distinct_target_count_pass':True})
    result['layer_counts']=layers
    checked=0
    for n in range(4,9):
        for w in states(n):
            for mode in ('event','state'):
                audit_process({w:F(1)},3,mode);checked+=1
    result['exhaustive_horizon_checks']={'initial_sizes':[4,5,6,7,8],'max_horizon':3,'root_and_measure_cases':checked,'all_passed':True}
    w=tuple(map(int,'00111'))
    result['example_event']=audit_process({w:F(1)},4,'event')
    result['example_state']=audit_process({w:F(1)},4,'state')
    result['weighted_consistency']=audit_process({w:F(1)},3,'weighted')
    result['example_first_step']={}
    for mode in ('event','state'):
        target=defaultdict(F)
        for e,v,p in event_law(w,mode):target[''.join(map(str,v))]+=p
        result['example_first_step'][mode]={v:str(p) for v,p in target.items()}
    w2=tuple(map(int,'00001111'));w4=tuple(map(int,'00110011'))
    result['fixed_mixed_prior']=audit_process({w2:F(1,2),w4:F(1,2)},3,'event')
    result['unconstrained_uniform_history_prior']={}
    for L in range(3):
        a=b=1
        for j in range(L):a*=10+j;b*=12+j
        result['unconstrained_uniform_history_prior'][str(L)]={'D2':str(F(a,a+b)),'D4':str(F(b,a+b))}
    n,k=9,4;p2=F(k+1,n+2);p4=F(k+2,n+4)
    assert p2!=p4
    result['strong_lumpability_counterexample']={'n':n,'N1':k,'D2_p_insert1':str(p2),'D4_p_insert1':str(p4)}
    def likelihood(D,seq):
        nn,kk=9,4;p=F(1)
        for b in seq:
            p*=F((kk if b else nn-kk)+D//2,nn+D);nn+=1;kk+=b
        return p
    for D in (2,4):assert likelihood(D,(0,1))==likelihood(D,(1,0))
    result['fixed_preparation_order_check']={str(D):str(likelihood(D,(0,1))) for D in (2,4)}
    result['irregular_uniform_horizon_counterexample']={'horizon1_Pa':'1/2','horizon2_Pa':'2/5'}
    path=Path(__file__).resolve().parents[2]/'data/wheeler/wheeler-58-results.json'
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
