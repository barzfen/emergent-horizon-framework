"""Resolve the five-gluon pole and finite terms into SU(3) pair colours."""
from collections import defaultdict
from fractions import Fraction as F
from functools import cache
from itertools import permutations, product
from math import prod
import json

from color_probe import bracket, laurent, spinors

G = (
    ((0,1,0),(1,0,0),(0,0,0)),
    ((0,-1j,0),(1j,0,0),(0,0,0)),
    ((1,0,0),(0,-1,0),(0,0,0)),
    ((0,0,1),(0,0,0),(1,0,0)),
    ((0,0,-1j),(0,0,0),(1j,0,0)),
    ((0,0,0),(0,0,1),(0,1,0)),
    ((0,0,0),(0,0,-1j),(0,1j,0)),
    ((1,0,0),(0,1,0),(0,0,-2)),
)
METRIC = (1,)*7+(3,)
I = range(8)
PAIRS = tuple(product(I, repeat=2))
DDM = tuple((1,*w,5) for w in permutations((2,3,4)))
TRACE = tuple((1,*w) for w in permutations((2,3,4,5)))


@cache
def trace(seq):
    m = ((1,0,0),(0,1,0),(0,0,1))
    for a in seq:
        m = tuple(tuple(sum(row[k]*G[a][k][j] for k in range(3))
                        for j in range(3)) for row in m)
    return sum(m[j][j] for j in range(3))


def f(a,b,c):
    val = trace((a,b,c))-trace((b,a,c))
    assert val.real == 0
    return F(int(val.imag),4)


def d(a,b,c):
    val = trace((a,b,c))+trace((b,a,c))
    assert val.imag == 0
    return F(int(val.real),4)


F_TABLE = {(a,b): [(c, x) for c in I if (x := f(a,b,c))]
           for a,b in PAIRS}
D_TABLE = {(a,b): [(c, x) for c in I if (x := d(a,b,c))]
           for a,b in PAIRS}


@cache
def chain(seq):
    a,b,c,d_,e = seq
    return sum(v*x*f(y,d_,e)/(METRIC[u]*METRIC[y])
               for u,v in F_TABLE[a,b] for y,x in F_TABLE[u,c])


def norm2(tensor):
    return sum((value**2/prod(METRIC[i] for i in key)
               for key,value in tensor.items()), F(0))


def pair_channels(tensor):
    singlet, octet_s, octet_a = (defaultdict(F) for _ in range(3))
    symmetric, antisymmetric = {}, {}
    for (a,b,c,d_,e), value in tensor.items():
        swapped = tensor[e,b,c,d_,a]
        symmetric[a,b,c,d_,e] = (value+swapped)/2
        antisymmetric[a,b,c,d_,e] = (value-swapped)/2
        weight = value/(METRIC[a]*METRIC[e])
        if a == e:
            singlet[b,c,d_] += value/METRIC[a]
        for k, coef in D_TABLE[a,e]:
            octet_s[k,b,c,d_] += coef*weight
        for k, coef in F_TABLE[a,e]:
            octet_a[k,b,c,d_] += coef*weight
    s1, s8, a8 = norm2(singlet)/8, 3*norm2(octet_s)/5, norm2(octet_a)/3
    return {"1": s1, "8s": s8, "27": norm2(symmetric)-s1-s8,
            "8a": a8, "10+10bar": norm2(antisymmetric)-a8}


def check_gram(rows):
    reps = [j for j, w in enumerate(DDM) if w[1:-1] < w[1:-1][::-1]]
    symmetric = [{key: F(row[j]+rows[(key[4],*key[1:4],key[0])][j],2)
                  for key,row in rows.items()} for j in reps]
    for i in range(3):
        for j in range(i,3):
            values = pair_channels({key:v+symmetric[j][key] for key,v in symmetric[i].items()})
            signs = (1,-1,-1)
            singlet = F(27,4)*(signs[i]+signs[j])**2
            octet = 27*(4 if i==j else 2)
            assert values == {"1":singlet, "8s":octet, "27":4*octet-5*singlet,
                              "8a":0, "10+10bar":0}


def main():
    colors = tuple(product(I, repeat=5))
    rows = {key: [chain(tuple(key[i-1] for i in w)) for w in DDM] for key in colors}
    check_gram(rows)
    report = []
    for sample in (1,2,3):
        base, slopes = spinors(sample)
        terms = [laurent(w,base,slopes) for w in DDM]
        p,i,j,k,_ = base
        u,v = bracket(p,i)*bracket(j,k), bracket(p,k)*bracket(i,j)
        assert bracket(p,j)*bracket(i,k) == u+v
        common = -F(bracket(i,j)**4,2*prod(bracket(p,w)**2 for w in (i,j,k))
                    *bracket(i,j)*bracket(j,k)*bracket(i,k))
        assert [terms[index][1] for index in (0,1,2)] == [
            common*(u+v)**2, -common*v*v, -common*u*u]
        tensors = [{key: sum(c*v[k] for c,v in zip(row,terms)) for key,row in rows.items()}
                   for k in (0,1)]
        pole, finite = map(pair_channels,tensors)
        assert pole["8a"] > 0 and all(not v for k,v in pole.items() if k!="8a")
        assert all(finite[k] > 0 for k in ("1","8s","27"))
        assert finite["8a"] == finite["10+10bar"] == 0
        assert finite["8s"] == 2*finite["1"] and finite["27"] == 3*finite["1"]
        # Independently check the two contractions in the trace decomposition.
        trace_terms = [laurent(w,base,slopes) for w in TRACE]
        ddm_contract = [[F(0), F(0)] for _ in range(2)]
        trace_contract = [[F(0), F(0)] for _ in range(2)]
        for key in colors:
            a,b,c,d_,e = key
            factors = (f(a,e,b)*(c==d_)*METRIC[c], (a==e)*METRIC[a]*f(b,c,d_))
            if not any(factors):
                continue
            for j, factor in enumerate(factors):
                weight = F(factor, prod(METRIC[i] for i in key))
                for k in (0,1):
                    ddm_contract[j][k] += weight*tensors[k][key]
                    trace_contract[j][k] += weight*sum(
                        F(int(trace(tuple(key[i-1] for i in w)).imag),-16)*value[k]
                        for w,value in zip(TRACE,trace_terms))
        assert ddm_contract == trace_contract
        encode = lambda row: {k: str(v) for k,v in row.items()}
        report.append(dict(sample=sample, pole_norm2=encode(pole), finite_norm2=encode(finite),
                           finite_fractions=encode({k: v/sum(finite.values()) for k,v in finite.items()}),
                           invariant_contractions=[[str(v) for v in row] for row in ddm_contract]))
    print(json.dumps(report,indent=2))


if __name__ == "__main__":
    main()
