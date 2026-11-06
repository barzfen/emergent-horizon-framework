"""Exact leading-soft, finite-collinear colour test for a five-gluon hard event."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import permutations
from math import prod
import json

from orders import coefficients, tensor_rows
from su3_probe import F_TABLE, METRIC, I, pair_channels


def dot(p,q):
    return p[0]*q[0]-sum(a*b for a,b in zip(p[1:],q[1:]))


def hard_amplitude():
    # All outgoing. The two incoming momenta are crossed with negative energy.
    base = ((1,1),(1,0),(0,1),(1,-1),(1,1))
    slopes = ((1,-1),(0,0),(0,0),(0,0),(-1,1))
    values = {w:coefficients(w,base,slopes)[:2]
              for w in ((0,*m,4) for m in permutations(range(1,4)))}
    pole, finite = defaultdict(F), defaultdict(F)
    for key,w,weight in tensor_rows(5):
        a,b = values[w]
        pole[key] += weight*a
        finite[key] += weight*b
    return pole, finite


def current(tensor, weights, gluon):
    out = defaultdict(F)
    for key,value in tensor.items():
        if not value:
            continue
        for leg,w in enumerate(weights):
            if not w:
                continue
            incoming = key[leg]
            for outgoing,coef in F_TABLE[gluon,incoming]:
                changed = key[:leg]+(outgoing,)+key[leg+1:]
                out[changed] += w*value*coef/METRIC[incoming]
    return out


def sum_colour(tensor):
    return sum((v*v/prod(METRIC[a] for a in key) for key,v in tensor.items()),F(0))


def channel_squared(tensor):
    values = defaultdict(F,tensor)
    for key in tensor:
        values.setdefault((key[-1],*key[1:-1],key[0]),F(0))
    return pair_channels(values)


def fractions(norms):
    total = sum(norms.values())
    return {k:str(v/total) for k,v in norms.items()} if total else {}


def main():
    pole, finite = hard_amplitude()
    p = ((3,3,0,0),(-6,0,0,-6),(-6,0,0,6),(6,-6,0,0),(3,3,0,0))
    dp = ((0,0,0,6),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,-6))
    assert all(dot(v,v)==dot(v,dv)==0 for v,dv in zip(p,dp))
    assert all(not sum(v[j] for v in x) for x in (p,dp) for j in range(4))
    q = (1,0,1,0)
    polarizations = ((0,1,0,0),(0,0,0,1))
    names = ("coherent_on_finite", "difference_on_pole", "sum")
    totals = {name:defaultdict(F) for name in names}
    by_pol = {}
    for label,eps in zip(("x","z"),polarizations):
        assert dot(q,q)==dot(q,eps)==0 and dot(eps,eps)==-1
        w0 = [F(dot(v,eps),dot(v,q)) for v in p]
        w1 = [F(dot(dv,eps)*dot(v,q)-dot(v,eps)*dot(dv,q),dot(v,q)**2)
              for v,dv in zip(p,dp)]
        pol = {name:defaultdict(F) for name in names}
        for c in I:
            assert not any(current(finite,[1]*5,c).values())
            assert not any(current(pole,[1]*5,c).values())
            a,b = current(finite,w0,c),current(pole,w1,c)
            joint = {k:a[k]+b[k] for k in a.keys()|b.keys()}
            for name,tensor in zip(names,(a,b,joint)):
                channels = channel_squared(tensor)
                assert not channels["8a"] and not channels["10+10bar"]
                assert sum(channels.values())==sum_colour(tensor)
                for k,v in channels.items():
                    pol[name][k] += v/METRIC[c]
                    totals[name][k] += v/METRIC[c]
        by_pol[label] = {name:fractions(row) for name,row in pol.items()}
    interference = {k:totals["sum"][k]-totals[names[0]][k]-totals[names[1]][k]
                    for k in ("1","8s","27")}
    expected = {"1":"1/6","8s":"1/3","27":"1/2","8a":"0","10+10bar":"0"}
    assert fractions(channel_squared(finite)) == fractions(totals[names[1]]) == expected
    assert sum(totals[names[1]].values()) == 4*9*sum_colour(pole)
    assert any(interference.values())
    assert fractions(totals["sum"])["27"] == "227/284"
    print(json.dumps({"hard_finite":fractions(channel_squared(finite)),
                      "soft_finite":{name:fractions(row) for name,row in totals.items()},
                      "interference":{k:str(v) for k,v in interference.items()},
                      "polarizations":by_pol},indent=2))


if __name__ == "__main__":
    main()
