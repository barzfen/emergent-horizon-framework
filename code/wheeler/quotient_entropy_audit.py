"""WHEELER-60: exact two-source quotient Shannon counterexample.
Standard library only. Integer arithmetic certifies the entropy sign;
Decimal logarithms provide display values, not the sign certificate.
"""
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path
import json
from projective_audit import event_law
from rotation_audit import canonical as word_canonical, rotations


def canonical_runs(a):
    # Start with a zero run. Rotations preserving this convention shift by pairs.
    return min(a[i:]+a[:i] for i in range(0,len(a),2))


def to_word(a):
    return tuple(b for i,length in enumerate(a) for b in [i%2]*length)


def run_row(a):
    out=defaultdict(F);den=sum(a)+len(a)
    for j,length in enumerate(a):
        b=list(a);b[j]+=1
        out[canonical_runs(tuple(b))]+=F(length+1,den)
    return dict(out)


def entropy(ps):
    with localcontext() as ctx:
        ctx.prec=70
        values=[Decimal(p.numerator)/Decimal(p.denominator) for p in ps if p]
        return -sum(p*p.ln()/Decimal(2).ln() for p in values)


def serial(law):
    return [{'zero_one_alternating_run_lengths':list(a),'probability':str(p)} for a,p in sorted(law.items())]


def witness(L):
    a=(2,L,2,L);b=(2,L-1,2,L+1)
    prior={a:F(2,3),b:F(1,3)};out=defaultdict(F)
    for source,p in prior.items():
        for target,q in run_row(source).items():out[target]+=p*q
    d=6*L+24
    expected={canonical_runs((2,L,2,L+1)):F(5*L+4,d),
              canonical_runs((3,L,2,L)):F(12,d),
              canonical_runs((2,L-1,2,L+2)):F(L+2,d),
              canonical_runs((3,L-1,2,L+1)):F(3,d),
              canonical_runs((2,L-1,3,L+1)):F(3,d)}
    assert dict(out)==expected and sum(out.values())==1
    return prior,dict(out)


def main():
    # Independent representation check: enumerate each labelled insertion and
    # quotient its full binary target, without using the run-extension formula.
    checks=[]
    for L in (10,38,80,100):
        prior,out=witness(L)
        for a in prior:
            actual=defaultdict(F)
            for _,v,p in event_law(to_word(a),'event'):actual[word_canonical(v)]+=p
            expected={word_canonical(to_word(b)):p for b,p in run_row(a).items()}
            assert dict(actual)==expected
        checks.append({'L':L,'n':2*L+4,'full_binary_event_enumeration_matches':True})
    prior,out=witness(100)
    assert sorted(out.values())==sorted(map(F,('21/26','1/52','17/104','1/208','1/208')))
    # Delta H < 0 iff this exact integer inequality holds. See report derivation.
    left=2**1274*13**624;right=3**1128*7**504*17**102
    assert left<right
    # Independent direct rational-product entropy comparison with common
    # denominator 624: H(q)<H(p) iff product(q**(624*q))>product(p**(624*p)).
    def power_product(law):
        result=F(1)
        for p in law.values():
            exponent=624*p;assert exponent.denominator==1
            result*=p**exponent.numerator
        return result
    assert power_product(out)>power_product(prior)
    with localcontext() as ctx:
        ctx.prec=60
        h0=entropy(prior.values());h1=entropy(out.values());delta=h1-h0
        forward=sum((Decimal(p.numerator)/Decimal(p.denominator))*entropy(run_row(a).values()) for a,p in prior.items())
        reverse=Decimal(21)/26*entropy([F(101,126),F(25,126)])
        assert abs(delta-(forward-reverse))<Decimal('1e-55')
        weighted_delta=delta+(Decimal(205)/204).ln()/Decimal(2).ln()+Decimal(2)/3
        source_sizes={str(a):len(rotations(to_word(a))) for a in prior}
        target_sizes={str(a):len(rotations(to_word(a))) for a in out}
        assert sorted(source_sizes.values())==[102,204]
        assert set(target_sizes.values())=={205}
        limit=entropy([F(5,6),F(1,6)])-h0
        result={
            'model':'event-uniform MICRO growth; rotations only; ordinary class Shannon entropy',
            'L':100,'n_source':204,'n_target':205,'D':4,'N1_source':200,
            'prior':serial(prior),'output':serial(out),
            'rows':[{'source':list(a),'targets':serial(run_row(a))} for a in prior],
            'H_source_bits':str(h0),'H_target_bits':str(h1),'delta_H_bits':str(delta),
            'H_target_given_source_bits':str(forward),'H_source_given_target_bits':str(reverse),
            'ambiguous_target_posterior':{'periodic_source':'101/126','asymmetric_source':'25/126'},
            'source_orbit_sizes':source_sizes,'target_orbit_sizes':target_sizes,
            'orbit_weighted_entropy_delta_bits':str(weighted_delta),
            'integer_sign_certificate':{'inequality':'2^1274 * 13^624 < 3^1128 * 7^504 * 17^102',
                                        'verified':True,'left_bit_length':left.bit_length(),'right_bit_length':right.bit_length(),
                                        'independent_rational_power_product_verified':True},
            'family_limit_delta_H_bits':str(limit),
            'independent_binary_checks':checks,
            'family_samples':[{'L':L,'n':2*L+4,'delta_H_bits':str(entropy(witness(L)[1].values())-h0)} for L in (38,64,80,100,128,200)],
            'scope':'Explicit counterexample; no claim of smallest n or global entropy minimum.'}
    path=Path(__file__).resolve().parents[2]/'data/wheeler/wheeler-60-results.json'
    path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
