"""Exact normal-to-plane derivatives of the finite six-gluon colour tensor."""
from collections import defaultdict
from fractions import Fraction as F
from functools import reduce
from itertools import permutations
import json

from orders import channel_norms, tensor_rows
from lorentzian import audit

CHANNELS = ("1","8s","27")
SHARES = dict(zip(CHANNELS,(F(1,6),F(1,3),F(1,2))))


def mul(a,b):
    # Pair represents a real value and the imaginary part of its derivative.
    return a[0]*b[0], a[0]*b[1]+a[1]*b[0]


def bracket(a,b):
    u,v = mul(a[0],b[1]),mul(a[1],b[0])
    return u[0]-v[0],u[1]-v[1]


def angles(momentum, dy):
    e,x,y,z = momentum
    assert not y
    sign = 1 if e>0 else -1
    e,x,z = sign*e,sign*x,sign*z
    # A nonsingular chart at all test points.
    assert e+z != 0
    return ((e+z,0),(x,sign*dy))


def finite(word, spinors):
    p,i,k = (spinors[j] for j in (0,word[1],word[-2]))
    hard = word[:-1]
    edges = (bracket(spinors[a],spinors[b]) for a,b in zip(hard,hard[1:]+hard[:1]))
    denominator = reduce(mul, (bracket(p,i),bracket(p,k),*edges),(2,0))
    numerator = reduce(mul, (bracket(spinors[1],spinors[2]),)*4+(bracket(i,k),))
    a,b = numerator
    c,d = denominator
    return F(a,c), F(b*c-a*d,c*c)


def momenta(x,z,triangle=(3,4,5)):
    assert x*x+z*z==1
    a,b,c = triangle
    assert a*a+b*b==c*c
    e = F(a+b+c,2)
    return ((a,a,0,0),(-e,-e*x,0,-e*z),(-e,e*x,0,e*z),
            (b,0,0,b),(c,-a,0,-b))


def curvature(rows):
    n = len(rows)+1
    twice_energy = -2*rows[1][0]
    spinors = [angles(p,dy) for p,dy in zip(rows,(0,-twice_energy,twice_energy,0,0))]
    values = {w:finite(w,spinors)
              for w in ((0,*m,n-1) for m in permutations(range(1,n-1)))}
    tensors = (defaultdict(F),defaultdict(F))
    for key,word,weight in tensor_rows(n):
        for tensor,c in zip(tensors,values[word]):
            tensor[key] += weight*c
    base,tangent = (channel_norms({key:v for key,v in tensor.items() if v},1)
                    for tensor in tensors)
    base_total,tangent_total = sum(base.values()),sum(tangent.values())
    assert all(base[k]/base_total==SHARES[k] for k in CHANNELS)
    return {k:2*(tangent[k]-SHARES[k]*tangent_total)/base_total for k in CHANNELS}


def tilted(rows,t):
    # Rotate beam direction out of the plane by angle 2 arctan(t).
    factor = (1-t*t)/(1+t*t)
    out = list(rows)
    for j,sign in ((1,-1),(2,1)):
        e,x,y,z = rows[j]
        out[j] = (e,factor*x,sign*(-2*e)*t/(1+t*t),factor*z)
    # Clear denominators before passing momenta to the Gaussian-integer audit.
    from math import lcm
    scale = lcm(*(F(v).denominator for p in out for v in p))
    return tuple(tuple(int(scale*v) for v in p) for p in out)


def main():
    cases = ((5,12,13),(12,5,13),(4,3,5),(-5,12,13),(-12,5,13),
             (-3,4,5),(-4,3,5))
    result = []
    for (a,b,c),triangle in [(beam,(3,4,5)) for beam in cases] + [
            ((5,12,13),(8,15,17)), ((-5,12,13),(7,24,25))]:
        rows = momenta(F(a,c),F(b,c),triangle)
        coeffs = curvature(rows)
        assert not sum(coeffs.values())
        result.append({"triangle":triangle,"beam":(str(F(a,c)),str(F(b,c))),
                       "quadratic_in_t":{k:str(v) for k,v in coeffs.items()}})
    rows = momenta(F(5,13),F(12,13))
    t = F(1,1000)
    observed = audit(tilted(rows,t))
    mirror = audit(tilted(rows,-t))
    assert observed==mirror
    for k,c in result[0]["quadratic_in_t"].items():
        measured = (F(observed[k])-SHARES[k])/t**2
        assert abs(measured-F(c)) < F(1,50)
    print(json.dumps({"curvatures":result,"finite_t":str(t),"finite_t_shares":observed},indent=2))


if __name__ == "__main__":
    main()
