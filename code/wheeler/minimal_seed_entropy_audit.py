"""WHEELER-62: all-time minimal-seed entropy proof audit.
Standard library. Exact polynomial identities, rational bounds, endpoint
cross-checks and orbit counts. The all-time proof is in WHEELER-62.md.
"""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import json
from unconditioned_entropy_audit import urn_endpoint, log_interval


def add(a,b):
    return [(a[i] if i<len(a) else F(0))+(b[i] if i<len(b) else F(0)) for i in range(max(len(a),len(b)))]


def scale(a,s):return [v*s for v in a]


def mul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out


def binomial_polynomial(a,b,k):
    out=[F(1,factorial(k))]
    for j in range(k):out=mul(out,[F(b-j),F(a)])
    return out


def shift(p,k):
    out=[F(0)]*len(p)
    for i,c in enumerate(p):
        for j in range(i+1):out[j]+=c*comb(i,j)*k**(i-j)
    return out


def evaluate(p,m):return sum(c*m**i for i,c in enumerate(p))


P=[F(x) for x in (84,102,53,12,1)]
D=[F(1)]
for k in (1,3,5,7,9,11):D=mul(D,[F(k),F(2)])


def periodic(t):
    if t%2:return F(0)
    m=t//2
    return 495*evaluate(P,m)/(4*evaluate(D,m))


def convolution_periodic(m):
    return F(sum(comb(u+2,2)**2*comb(m-u+2,2)**2 for u in range(m+1)),comb(2*m+11,11))


def class_count(t):return (comb(t+3,3)+(t//2+1 if t%2==0 else 0))//2


def main():
    # Exact generating-function coefficient polynomial for the convolution.
    A=[F(0)]
    for j,c in enumerate((1,8,18,8,1)):
        A=add(A,scale(binomial_polynomial(1,9-j,9),F(c)))
    B=binomial_polynomial(2,11,11)
    assert add(scale(mul(D,A),4),scale(mul(P,B),-495))==[0]*16
    # G(m)>0 proves rho_(2m)<3/(2m+12) for m>=2.
    G=add(scale(D,2),scale(mul([F(6),F(1)],P),-165))
    shifted=shift(G,2)
    expected=list(map(F,(543510,1112940,756542,246615,42260,3675,128)))
    assert shifted==expected and all(c>0 for c in shifted)
    assert periodic(0)==1 and periodic(2)==F(3,13)
    assert urn_endpoint((2,2,2,2),0)=={(2,2,2,2):F(1)}
    assert urn_endpoint((2,2,2,2),1)=={(2,2,2,3):F(1,2),(2,2,3,2):F(1,2)}
    assert 14**4>2*11**4
    assert F(1,4)-F(3,13)==F(1,52)
    formula_checks=[]
    for m in list(range(41))+[100,1000]:
        assert periodic(2*m)==convolution_periodic(m)
        if m>=2:assert periodic(2*m)<F(3,2*m+12)
        formula_checks.append({'m':m,'convolution_matches':True})
    endpoint_checks=[]
    for t in range(21):
        law=urn_endpoint((2,2,2,2),t)
        observed=sum(v for a,v in law.items() if a[:2]==a[2:])
        assert observed==periodic(t)
        assert len(law)==class_count(t)
        endpoint_checks.append({'t':t,'classes':len(law),'periodic_mass':str(observed)})
    # Display rigorously positive simple lower bounds on sample steps.
    bounds=[]
    for t in (0,1,2,3,4,10,40,100,1000):
        if t==0:bound=F(1)
        elif t==2:bound=F(1,52) # Strictly greater than this.
        else:
            # ln(1+x)>x/(1+x), ln2<1, hence ordered entropy gain>3/(t+12).
            bound=F(3,t+12)+periodic(t+1)-periodic(t)
        assert bound>0
        bounds.append({'t_to_t_plus_1':t,'positive_lower_bound_bits':str(bound),
                       'strict_except_t0':t!=0})
    # Cross-check the logarithmic lower estimate at representative finite sizes.
    for t in (1,2,4,40,1000):
        lnlo,_=log_interval(F(t+12,t+9))
        _,ln2hi=log_interval(F(2))
        assert lnlo/ln2hi>F(3,t+12)
    result={
        'seed':[2,2,2,2],'D':4,'initial_size':8,
        'theorem':'Ordinary rotation-class Shannon entropy increases strictly at every integer growth step.',
        'scope':'This seed only; other seeds have certified decreases in WHEELER-61.',
        'periodic_probability_formula':'rho_(2m)=495*(m^4+12m^3+53m^2+102m+84)/(4*product_(j=0..5)(2m+2j+1)); rho_odd=0',
        'closed_form_polynomial_identity_verified':True,
        'G_shifted_coefficients_constant_first':[int(c) for c in shifted],
        'positive_coefficient_certificate':True,
        'exceptional_steps':{'t0_exact_gain_bits':'1','t2_rho':'3/13','t2_gain_strictly_above_bits':'1/52','integer_inequality':'14^4 > 2*11^4','verified':True},
        'sample_step_bounds':bounds,'convolution_checks':formula_checks,'endpoint_checks':endpoint_checks,
        'entropy_bounds':{'lower':'log2((t+9)*(t+10)*(t+11)/990)-1+rho_t','upper':'log2((binom(t+3,3)+I_even*(t/2+1))/2)'},
        'asymptotic_entropy_bits':'3*log2(t)+O(1)',
        'even_time_periodic_asymptotic':'rho_t ~ 495/(64*t^2), t even',
        'evidence':'All-time conclusions follow from the algebraic proof; finite checks verify implementation.'}
    path=Path(__file__).resolve().parents[2]/'data/wheeler/wheeler-62-results.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
