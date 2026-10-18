"""WHEELER-59: rotation quotient, exact kernels and entropy diagnostics.
Run from repo root: python code/wheeler/rotation_audit.py
Standard library only; Fraction for kernels, float only for Shannon diagnostics.
"""
from collections import defaultdict, Counter
from fractions import Fraction as F
from pathlib import Path
from math import log2
import json
from projective_audit import states, walls, events, event_law, project


def rotations(w):
    return {w[i:]+w[:i] for i in range(len(w))}


def canonical(w):
    return min(rotations(w))


def quotient_row(w, mode='event'):
    out=defaultdict(F)
    for _,v,p in event_law(w,mode):out[canonical(v)]+=p
    return dict(out)


def entropy(p):
    return -sum(float(x)*log2(float(x)) for x in p if x)


def word(w):return ''.join(map(str,w))


def encoded(row):return {word(v):str(p) for v,p in sorted(row.items())}


def history_check(w,L=3):
    fine={((),(w,)):F(1)};coarse={(canonical(w),):F(1)}
    for _ in range(L):
        nxt={}
        for (es,ws),p in fine.items():
            for e,v,q in event_law(ws[-1],'event'):nxt[(es+(e,),ws+(v,))]=p*q
        fine=nxt;nxt=defaultdict(F)
        for hist,p in coarse.items():
            for v,q in quotient_row(hist[-1]).items():nxt[hist+(v,)]+=p*q
        coarse=dict(nxt)
        assert project(fine,canonical)==coarse
    return {'root':word(w),'horizon':L,'exact_path_law_equality':True}


def main():
    result={'arithmetic':'Fraction; entropy diagnostics use float log2',
            'quotient':'rotations only; no reflection or bit-complement quotient'}
    layers=[]
    for n in range(4,15):
        ws=states(n);groups=defaultdict(list)
        for w in ws:groups[canonical(w)].append(w)
        cols=defaultdict(F);weighted_cols=defaultdict(F);rooted_cols=defaultdict(F);failures=0
        for a,members in sorted(groups.items()):
            row=quotient_row(a);assert sum(row.values())==1
            weighted=quotient_row(a,'weighted')
            state=quotient_row(a,'state')
            for w in members:
                for _,v,p in event_law(w,'event'):rooted_cols[v]+=p
                assert quotient_row(w)==row
                assert quotient_row(w,'weighted')==weighted
                failures+=quotient_row(w,'state')!=state
                D=walls(w)
                if D:
                    actual=sum(p for _,v,p in event_law(w,'state') if sum(v)==sum(w)+1)
                    assert actual==F(D//2+w[-1],D+1)
            for b,p in row.items():
                cols[b]+=p;weighted_cols[b]+=len(members)*p
        assert all(c<=1 for c in rooted_cols.values())
        for b,c in weighted_cols.items():
            assert c==sum(rooted_cols[v] for v in rotations(b))
            assert c<=len(rotations(b))
        worst=max(cols,key=lambda b:(cols[b],b))
        layers.append({'n':n,'rooted_sources':len(ws),'rotation_classes':len(groups),
                       'event_and_run_weighted_lumpability':True,
                       'state_uniform_members_disagreeing_with_canonical':failures,
                       'largest_quotient_column':str(cols[worst]),'target':word(worst),
                       'rooted_and_orbit_weighted_column_bounds':True})
    result['layers']=layers
    example={}
    for s in ('00111','11100'):
        w=tuple(map(int,s));example[s]={mode:encoded(quotient_row(w,mode)) for mode in ('event','state')}
    result['root_dependence_example']=example
    target=tuple(map(int,'0001110001111'));n=len(target)-1
    parents=sorted({canonical(w) for w in states(n) if target in quotient_row(w)})
    assert len(parents)==4
    prior={w:F(1,4) for w in parents};out=defaultdict(F)
    for a,p in prior.items():
        for b,q in quotient_row(a).items():out[b]+=p*q
    assert out[target]==F(17,64)>F(1,4)
    weighted_before=entropy(prior.values())+sum(float(p)*log2(len(rotations(a))) for a,p in prior.items())
    weighted_after=entropy(out.values())+sum(float(p)*log2(len(rotations(b))) for b,p in out.items())
    result['majorization_counterexample']={
        'prior':encoded(prior),'target':word(target),
        'incoming_probabilities':{word(a):str(quotient_row(a)[target]) for a in parents},
        'target_probability':str(out[target]),'largest_source_probability':'1/4',
        'output':encoded(out),'H_before_bits':entropy(prior.values()),'H_after_bits':entropy(out.values()),
        'orbit_weighted_H_before_bits':weighted_before,'orbit_weighted_H_after_bits':weighted_after}
    result['history_checks']=[history_check(tuple(map(int,s))) for s in ('00111','11100','00110011')]
    w=tuple(map(int,'00111'))
    reroot=defaultdict(F)
    for r in rotations(w):
        for b,p in quotient_row(r,'state').items():reroot[b]+=p/len(rotations(w))
    result['alternative_kernels']={'event':encoded(quotient_row(w)),
        'uniform_distinct_quotient_targets':{word(b):str(F(1,len(quotient_row(w)))) for b in quotient_row(w)},
        'uniform_reroot_then_state_uniform':encoded(reroot),
        'rotation_invariant_run_weighted_q_1_over_20':encoded(quotient_row(w,'weighted'))}
    assert reroot!=quotient_row(w)
    path=Path(__file__).resolve().parents[2]/'data/wheeler/wheeler-59-results.json'
    path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
