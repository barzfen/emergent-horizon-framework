"""WHEELER-61: unconditioned single-seed endpoint entropy.
Exact Fraction kernels, independent Dirichlet-multinomial endpoint formula,
and rational logarithm bounds for the negative entropy sign. Standard library.
"""
from collections import defaultdict
from fractions import Fraction as F
from math import comb, fsum, log2
from decimal import Decimal, localcontext
from pathlib import Path
import json
from projective_audit import event_law
from rotation_audit import canonical as word_canonical
from quotient_entropy_audit import canonical_runs, to_word, run_row, entropy, serial


def compositions(t,d):
    if d==1:yield(t,)
    else:
        for x in range(t+1):
            for tail in compositions(t-x,d-1):yield(x,)+tail


def urn_endpoint(seed,t,quotient=True):
    denominator=comb(sum(seed)+len(seed)+t-1,t)
    counts=defaultdict(int)
    for x in compositions(t,len(seed)):
        weight=1
        for length,k in zip(seed,x):weight*=comb(length+k,k)
        target=tuple(length+k for length,k in zip(seed,x))
        if quotient:target=canonical_runs(target)
        counts[target]+=weight
    assert sum(counts.values())==denominator
    return {a:F(v,denominator) for a,v in counts.items()}


def advance(p):
    q=defaultdict(F)
    for a,v in p.items():
        for b,k in run_row(a).items():q[b]+=v*k
    assert sum(q.values())==1
    return dict(q)


def log_series(y,N=32):
    # 1 <= y <= 2; ln(y)=2*atanh((y-1)/(y+1)).
    z=(y-1)/(y+1);z2=z*z;power=z;s=F(0)
    for j in range(N):s+=2*power/(2*j+1);power*=z2
    tail=2*power/((2*N+1)*(1-z2))
    return s,s+tail


LN2=log_series(F(2))


def log_interval(x):
    y=x;k=0
    while y<1:y*=2;k-=1
    while y>=2:y/=2;k+=1
    lo,hi=log_series(y)
    a,b=(k*LN2[0],k*LN2[1]) if k>=0 else (k*LN2[1],k*LN2[0])
    return lo+a,hi+b


def entropy_interval(ps):
    lo=hi=F(0)
    for p in ps:
        if p:
            a,b=log_interval(p);lo-=p*b;hi-=p*a
    return lo,hi


def certify_delta(before,after):
    a,b=entropy_interval(before.values());c,d=entropy_interval(after.values())
    lo,hi=c-b,d-a
    bounds=[x/y for x in (lo,hi) for y in LN2]
    lower,upper=min(bounds),max(bounds)
    assert upper<0
    # Store a simple outward rational enclosure, checked with exact arithmetic.
    scale=10**9
    lower_int=lower.numerator*scale//lower.denominator
    upper_int=-((-upper.numerator*scale)//upper.denominator)
    lower_simple=F(lower_int,scale);upper_simple=F(upper_int,scale)
    assert lower_simple<=lower<=upper<=upper_simple<0
    return {'delta_bits_lower':str(lower_simple),'delta_bits_upper':str(upper_simple),
            'series_terms':32,'exact_rational_negative_upper_bound':True}


def main():
    seed=(2,100,2,100);p={seed:F(1)};laws=[p];binary={to_word(seed):F(1)}
    checks=[]
    for t in range(4):
        assert p==urn_endpoint(seed,t)
        projected=defaultdict(F)
        for w,v in binary.items():projected[word_canonical(w)]+=v
        expected={word_canonical(to_word(a)):v for a,v in p.items()}
        assert dict(projected)==expected
        checks.append({'t':t,'quotient_states':len(p),'rooted_states':len(binary),
                       'urn_formula_and_binary_enumeration_match':True})
        if t<3:
            p=advance(p);laws.append(p);nxt=defaultdict(F)
            for w,v in binary.items():
                for _,target,k in event_law(w,'event'):nxt[target]+=v*k
            binary=dict(nxt)
    certificate=certify_delta(laws[2],laws[3])
    with localcontext() as ctx:
        ctx.prec=60
        h2=entropy(laws[2].values());h3=entropy(laws[3].values())
        delta=h3-h2
        periodic=sum(v for a,v in laws[2].items() if a[:2]==a[2:])
        assert periodic==F(5105,10868)
        weighted_delta=delta+(Decimal(207)/206).ln()/Decimal(2).ln()+Decimal(periodic.numerator)/periodic.denominator
        result={'model':'unconditioned event-uniform growth from one rotation class',
                'seed_runs':list(seed),'seed_size':204,'D':4,
                'laws':[{'t':t,'n':204+t,'law':serial(p),'entropy_bits':str(entropy(p.values()))} for t,p in enumerate(laws)],
                'H_t2_bits':str(h2),'H_t3_bits':str(h3),'delta_t2_to_t3_bits':str(delta),
                'sign_certificate':certificate,'independent_checks':checks,
                'periodic_class_mass_t2':str(periodic),'periodic_class_mass_t3':'0',
                'orbit_weighted_entropy_delta_bits':str(weighted_delta),
                'large_L_limit_delta_bits':str(entropy([F(3,4),F(1,4)])-1)}
        labelled=[]
        for t,law in enumerate(laws):
            ordered=urn_endpoint(seed,t,quotient=False)
            h_ordered=entropy(ordered.values())
            per=sum(v for a,v in law.items() if a[:2]==a[2:])
            expected=entropy(law.values())+1-Decimal(per.numerator)/per.denominator
            assert abs(h_ordered-expected)<Decimal('1e-55')
            labelled.append({'t':t,'ordered_run_entropy_bits':str(h_ordered),'periodic_probability':str(per)})
        result['symmetry_entropy_identity']=labelled
        result['ordered_run_entropy_delta_bits']=str(entropy(urn_endpoint(seed,3,quotient=False).values())-entropy(urn_endpoint(seed,2,quotient=False).values()))
    # The minimal seed scan is a finite diagnostic, not an all-time proof.
    scan=[];p={(2,2,2,2):F(1)};last=None
    for t in range(41):
        exact=urn_endpoint((2,2,2,2),t)
        if t<=12:
            assert p==exact
            p=advance(p)
        h=-fsum(float(v)*log2(float(v)) for v in exact.values())
        scan.append({'t':t,'n':8+t,'quotient_states':len(exact),'entropy_bits_float':h,
                     'delta_bits_float':None if last is None else h-last})
        last=h
    minimum=min(scan[1:],key=lambda r:r['delta_bits_float'])
    result['minimal_seed_scan']={'seed_runs':[2,2,2,2],'horizon':40,
        'exact_endpoint_probabilities':True,'entropy_evaluation':'float; finite diagnostic only',
        'dynamic_recursion_crosscheck_through':12,'minimum_step':minimum,
        'all_steps_positive_in_scan':all(r['delta_bits_float']>0 for r in scan[1:]),'steps':scan}
    # Fixed short horizons, varied seeds: independent endpoint formula and signs.
    family=[]
    for L in (2,10,38,100,200,1000):
        p2=urn_endpoint((2,L,2,L),2);p3=urn_endpoint((2,L,2,L),3)
        with localcontext() as ctx:
            ctx.prec=50
            d=entropy(p3.values())-entropy(p2.values())
        item={'L':L,'seed_size':2*L+4,'delta_t2_to_t3_bits':str(d)}
        if L>=100:item['sign_certificate']=certify_delta(p2,p3)
        family.append(item)
    result['family_samples']=family
    path=Path(__file__).resolve().parents[2]/'data/wheeler/wheeler-61-results.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('laws','minimal_seed_scan')},indent=2))
    print('Minimal-seed scan:',minimum)

if __name__=='__main__':main()
