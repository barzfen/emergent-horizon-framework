"""Exact checks for the real-spinor pole-induction argument."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import permutations
from math import prod
import json

from orders import tensor_rows, channel_norms
from su3_probe import F_TABLE, METRIC


def ordering_coefficients(z, collision=None):
    m = len(z)
    out = {}
    for word in permutations(range(1,m+1)):
        edges = list(zip(word,word[1:]))
        sign = 1
        if collision:
            a,b = collision
            if (a,b) in edges:
                edges.remove((a,b))
            elif (b,a) in edges:
                edges.remove((b,a))
                sign = -1
            else:
                continue
        out[(0,*word,m+1)] = F(sign*(z[word[-1]-1]-z[word[0]-1]),
                                  prod(z[j-1]-z[i-1] for i,j in edges))
    return out


def assemble(n, coefficients):
    result = defaultdict(F)
    for key,word,color in tensor_rows(n):
        if word in coefficients:
            result[key] += color*coefficients[word]
    return {key:value for key,value in result.items() if value}


def norm_report(z):
    tensor = assemble(len(z)+2, ordering_coefficients(z))
    norms = channel_norms(tensor,1)
    return {k:str(v/sum(norms.values())) for k,v in norms.items()}


def residue_check(z, collision):
    a,b = collision
    assert z[a-1] == z[b-1]
    expected = assemble(len(z)+1, ordering_coefficients(z[:b-1]+z[b:]))
    actual = assemble(len(z)+2, ordering_coefficients(z, collision))
    expanded = defaultdict(F)
    for key, value in expected.items():
        for (c,d), targets in F_TABLE.items():
            for e, f in targets:
                if e == key[a]:
                    lifted = list(key)
                    lifted[a] = c
                    lifted.insert(b,d)
                    expanded[tuple(lifted)] += value*f/METRIC[e]
    expanded = {k:v for k,v in expanded.items() if v}
    # The overall sign is conventional and drops out of the norm.
    assert actual and (actual == expanded or actual == {k:-v for k,v in expanded.items()})
    return len(actual)


if __name__ == "__main__":
    cases = ((-2,3),(-3,0,5),(-8,-2,1,7))
    report = {str(len(z)+2): norm_report(z) for z in cases}
    expected = {"1":"1/6","8s":"1/3","27":"1/2","8a":"0","10+10bar":"0"}
    assert all(row == expected for row in report.values())
    print(json.dumps({"ratios":report, "residue_support":[
        residue_check((-4,2,2,7),(2,3)),
        residue_check((-4,2,7,-4),(1,4))
    ]},indent=2))
