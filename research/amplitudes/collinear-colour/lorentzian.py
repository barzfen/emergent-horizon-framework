"""Test the finite-channel ratio on real Lorentzian momenta."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import permutations
from functools import reduce
from math import lcm
import json
from orders import channel_norms, tensor_rows


def mul(a,b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def bracket(a,b):
    left,right = mul(a[0],b[1]),mul(a[1],b[0])
    return tuple(x-y for x,y in zip(left,right))


def power4(a):
    return mul(mul(a,a),mul(a,a))


def spinor(momentum):
    e,x,y,z = momentum
    sign = 1 if e>0 else -1
    e,x,y,z = (sign*v for v in momentum)
    assert e*e == x*x+y*y+z*z
    if e+z:
        lam = ((e+z,0),(x,y))
        weight = F(sign,e+z)
    else:
        lam = ((0,0),(1,0))
        weight = F(sign*2*e)
    assert weight*sum(x*x for x in lam[0]) == sign*(e+z)
    assert weight*sum(x*x for x in lam[1]) == sign*(e-z)
    cross = mul(lam[1],(lam[0][0],-lam[0][1]))
    assert tuple(weight*v for v in cross) == (sign*x,sign*y)
    return lam,weight


def gaussian_ratio(num, den):
    a,b = num
    c,d = den
    return F(a*c+b*d,c*c+d*d), F(b*c-a*d,c*c+d*d)


def finite(word, angles):
    # For endpoints P+tR and P-tR, the constant term equals the
    # hard Parke–Taylor expression times <i k>/(2 <P i><P k>).
    i,k = word[1],word[-2]
    p = angles[0]
    hard = word[:-1]
    denom = reduce(mul,(bracket(angles[a],angles[b]) for a,b in zip(hard,hard[1:]+hard[:1])),(1,0))
    numerator = mul(power4(bracket(angles[1],angles[2])),bracket(angles[i],angles[k]))
    denominator = reduce(mul,((2,0),denom,bracket(p,angles[i]),bracket(p,angles[k])))
    return gaussian_ratio(numerator,denominator)


def audit(momenta):
    assert all(sum(row[j] for row in momenta) == 0 for j in range(4))
    angles = [spinor(p)[0] for p in momenta]
    n = len(angles)+1
    values = {w:finite(w,angles)
              for w in ((0,*m,n-1) for m in permutations(range(1,n-1)))}
    re,im = defaultdict(F),defaultdict(F)
    for key,w,weight in tensor_rows(n):
        a,b = values[w]
        if a:
            re[key] += weight*a
        if b:
            im[key] += weight*b
    both = [channel_norms({k:v for k,v in part.items() if v},1) for part in (re,im)]
    norms = {key:both[0][key]+both[1][key] for key in both[0]}
    total = sum(norms.values())
    return {k:str(v/total) for k,v in norms.items()}


def beam_case(direction):
    parent, out1, out2 = (3,3,0,0),(4,0,4,0),(5,-3,-4,0)
    assert sum(v*v for v in direction) == 1
    a,b = (-6,*(-6*v for v in direction)),(-6,*(6*v for v in direction))
    momenta = parent,a,b,out1,out2
    scale = lcm(*(F(x).denominator for p in momenta for x in p))
    return tuple(tuple(int(scale*x) for x in p) for p in momenta)


if __name__ == "__main__":
    a,b = (-6,0,0,-6),(-6,0,0,6)
    cases = {
        "five_gluon_control": ((6,6,0,0),a,b,(6,-6,0,0)),
        "six_gluon_planar": beam_case((F(5,13),F(12,13),0)),
        "six_gluon_tilted": beam_case((F(3,13),F(36,65),F(4,5))),
        "six_gluon_perpendicular": beam_case((0,0,1)),
    }
    report = {name:audit(rows) for name,rows in cases.items()}
    expected = {"1":"1/6","8s":"1/3","27":"1/2","8a":"0","10+10bar":"0"}
    assert report["five_gluon_control"] == report["six_gluon_planar"] == expected
    assert report["six_gluon_perpendicular"]["27"] == "11299/13358"
    assert F(report["six_gluon_tilted"]["27"]) > F(1,2)
    print(json.dumps(report,indent=2))
