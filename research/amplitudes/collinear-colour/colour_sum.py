"""Colour-summed leading-soft intensity to quadratic collinear order."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import permutations
from math import prod
import json

from color_probe import bracket
from orders import tensor_rows
from soft_probe import I, METRIC, current, sum_colour, hard_amplitude


def hard_series():
    # Momentum-conserving recoil through t². For the two physical incoming
    # momenta E=6+3t², px=-3t² and pz=±(6+3t²)+O(t⁴).
    base = ((1,1),(1,0),(0,1),(1,-1),(1,1))
    first = ((1,-1),(0,0),(0,0),(0,0),(-1,1))
    second = ((0,0),(0,F(-1,4)),(F(-1,4),0),(0,0),(0,0))
    series = {}
    for mid in permutations(range(1,4)):
        word = (0,*mid,4)
        edges = list(zip(word,word[1:]))
        constant, linear, quadratic = [], [], []
        for a,b in edges:
            constant.append(bracket(base[a],base[b]))
            linear.append(bracket(base[a],first[b])+bracket(first[a],base[b]))
            quadratic.append(bracket(base[a],second[b])+bracket(first[a],first[b])
                             +bracket(second[a],base[b]))
        # <5 1> = -4t and <2 3> has no t or t² term.
        assert bracket(base[4],first[0])+bracket(first[4],base[0]) == -4
        slope = sum(F(x,y) for x,y in zip(linear,constant))
        degree2 = sum(F(x,y) for x,y in zip(quadratic,constant))
        degree2 += sum(F(linear[i]*linear[j],constant[i]*constant[j])
                       for i in range(4) for j in range(i+1,4))
        pole = F(1,-4*prod(constant))
        series[word] = pole,-pole*slope,pole*(slope*slope-degree2)
    tensors = [defaultdict(F) for _ in range(3)]
    for key,w,weight in tensor_rows(5):
        for tensor,c in zip(tensors,series[w]):
            tensor[key] += weight*c
    assert tensors[:2] == list(hard_amplitude())
    return tensors


def add(*vectors):
    out = defaultdict(F)
    for vec in vectors:
        for key,c in vec.items():
            out[key] += c
    return out


def inner(a,b):
    return sum((v*b.get(k,0)/prod(METRIC[j] for j in k) for k,v in a.items()),F(0))


def finite_check():
    # Choose t so sqrt(1+t²) is rational and the exact beam recoil is null.
    u = F(1,1000)
    t = 2*u/(1-u*u)
    e, x, z = 6+3*t*t, -3*t*t, 6*(1+u*u)/(1-u*u)
    r = x/(e+z)
    angles = ((1+t,1-t),(1,r),(r,1),(1,-1),(1-t,1+t))
    momenta = ((3*(1+t*t),3*(1-t*t),0,6*t),(-e,-x,0,-z),
               (-e,-x,0,z),(6,-6,0,0),(3*(1+t*t),3*(1-t*t),0,-6*t))
    assert all(not sum(p[j] for p in momenta) for j in range(4))
    assert all(p[0]**2==sum(v*v for v in p[1:]) for p in momenta)
    partial = {}
    for mid in permutations(range(1,4)):
        w = (0,*mid,4)
        partial[w] = bracket(angles[1],angles[2])**4/prod(
            bracket(angles[a],angles[b]) for a,b in zip(w,w[1:]+w[:1]))
    full = defaultdict(F)
    for key,w,weight in tensor_rows(5):
        full[key] += weight*partial[w]
    radiation = sum(sum_colour(current(full,[F(-p[j],p[0]) for p in momenta],a))/METRIC[a]
                    for j in (1,3) for a in I)
    return t,radiation/sum_colour(full)


def main():
    l,b,c = hard_series()
    soft = defaultdict(F)
    # q along +y, physical polarizations along +x and +z.
    weights = (((-1,0,0,1,-1),(0,0,0,0,0),(2,F(1,2),F(1,2),0,2)),
               ((0,-1,1,0,0),(-2,0,0,0,2),(0,0,0,0,0)))
    for w0,w1,w2 in weights:
        for a in I:
            pole = current(l,w0,a)
            finite = add(current(b,w0,a),current(l,w1,a))
            higher = add(current(c,w0,a),current(b,w1,a),current(l,w2,a))
            assert inner(pole,finite) == 0
            weight = F(1,METRIC[a])
            soft["pole_squared"] += weight*sum_colour(pole)
            soft["finite_squared"] += weight*sum_colour(finite)
            soft["pole_higher_interference"] += 2*weight*inner(pole,higher)
    hard_pole = sum_colour(l)
    hard_constant = sum_colour(b)+2*inner(l,c)
    leading = soft["pole_squared"]/hard_pole
    constant = soft["finite_squared"]+soft["pole_higher_interference"]
    quadratic = (constant-leading*hard_constant)/hard_pole
    assert (leading,quadratic)==(14,F(14,3))
    t,check = finite_check()
    assert abs((check-leading)/t**2-quadratic)<F(1,1000)
    print(json.dumps({k:str(v) for k,v in {
        **soft,"soft_constant":constant,"hard_pole_squared":hard_pole,
        "hard_constant":hard_constant,"normalized_leading":leading,
        "normalized_quadratic":quadratic,"finite_check_t":t,"finite_check_ratio":check}.items()},indent=2))


if __name__ == "__main__":
    main()
