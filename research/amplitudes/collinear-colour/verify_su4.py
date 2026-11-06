"""Exact SU(4) Casimir projection of a five-gluon finite colour tensor."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import prod
import json

N = 4
G, METRIC = [], []
for a,b in combinations(range(N),2):
    for value in (1,1j):
        G.append(tuple(tuple(value if (i,j)==(a,b) else value.conjugate()
                             if (i,j)==(b,a) else 0 for j in range(N))
                       for i in range(N)))
        METRIC.append(1)
for k in range(1,N):
    G.append(tuple(tuple((1 if i<k else -k if i==k else 0) if i==j else 0
                         for j in range(N)) for i in range(N)))
    METRIC.append(k*(k+1)//2)
I = range(len(G))
PAIRS = list(product(I,repeat=2))
EIGENVALUES = (-4,-2,-1,1)


def trace3(a,b,c):
    # Matrix entries are small Gaussian integers, exactly represented.
    return sum(G[a][i][j]*G[b][j][k]*G[c][k][i]
               for i,j,k in product(range(N),repeat=3))


F_TABLE = {}
for a,b in PAIRS:
    entries = []
    for c in I:
        val = trace3(a,b,c)-trace3(b,a,c)
        assert val.real == 0 and val.imag == int(val.imag)
        if val:
            entries.append((c,F(int(val.imag),4)))
    F_TABLE[a,b] = entries


def operator_columns():
    # Covariant pair coordinates. Raise the two input indices with METRIC.
    out = {}
    for a,b in PAIRS:
        column = defaultdict(F)
        for x in I:
            for i,u in F_TABLE[x,a]:
                for j,v in F_TABLE[x,b]:
                    column[i,j] -= u*v/(METRIC[x]*METRIC[a]*METRIC[b])
        out[a,b] = {k:v for k,v in column.items() if v}
    return out


OP = operator_columns()


def action(vec, shift=0):
    out = defaultdict(F)
    for pair,c in vec.items():
        out[pair] -= shift*c
        for k,v in OP[pair].items():
            out[k] += c*v
    return {k:v for k,v in out.items() if v}


def projector(vec, eigenvalue):
    den = 1
    for other in EIGENVALUES:
        if other != eigenvalue:
            vec = action(vec,other)
            den *= eigenvalue-other
    return {k:v/den for k,v in vec.items()}


def check_dimensions():
    dims = dict.fromkeys(EIGENVALUES,F(0))
    for a in I:
        for b in range(a,len(G)):
            basis = {(a,b):F(1),(b,a):F(1)}
            annihilator = basis
            for eigenvalue in EIGENVALUES:
                annihilator = action(annihilator,eigenvalue)
            assert not annihilator
            for eig in EIGENVALUES:
                dims[eig] += projector(basis,eig).get((a,b),0)
    assert tuple(dims.values()) == (1,15,20,84)
    return dims


def chains():
    for a,i in PAIRS:
        for u,x in F_TABLE[a,i]:
            for j in I:
                for v,y in F_TABLE[u,j]:
                    for k in I:
                        for b,z in F_TABLE[v,k]:
                            yield (a,i,j,k,b),x*y*z/(METRIC[u]*METRIC[v])


def norm(vec):
    return sum((v*v/(METRIC[a]*METRIC[b]) for (a,b),v in vec.items()), F(0))


def audit(z):
    coeffs = {}
    for word in permutations(range(3)):
        coeffs[word] = F(z[word[-1]]-z[word[0]],
                         prod(z[j]-z[i] for i,j in zip(word,word[1:])))
    by_spectators = defaultdict(lambda:defaultdict(F))
    for (a,i,j,k,b),color in chains():
        for word,coeff in coeffs.items():
            spectators = [0]*3
            for idx,c in zip(word,(i,j,k)):
                spectators[idx] = c
            by_spectators[tuple(spectators)][a,b] += color*coeff
    norms = dict.fromkeys(EIGENVALUES,F(0))
    total = F(0)
    for hard,vec in by_spectators.items():
        assert all(vec.get((b,a),0)==v for (a,b),v in vec.items())
        metric = prod(METRIC[a] for a in hard)
        total += norm(vec)/metric
        vec = {k:v for k,v in vec.items() if v}
        for eig in EIGENVALUES:
            norms[eig] += norm(projector(vec,eig))/metric
    assert total and sum(norms.values()) == total
    assert [v/total for v in norms.values()] == [F(k,45) for k in (4,15,5,21)]
    return {eig:str(v/total) for eig,v in norms.items()}


if __name__ == "__main__":
    print(json.dumps({
        "dimensions": {k:int(v) for k,v in check_dimensions().items()},
        "five_gluon_shares": {str(z):audit(z) for z in ((-3,0,5),(-7,2,9))},
    },indent=2))
