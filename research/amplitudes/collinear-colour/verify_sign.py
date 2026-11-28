from orders import tensor_rows
from su3_probe import METRIC,D_TABLE
from itertools import permutations, combinations, product
from collections import defaultdict
from math import gcd
from functools import reduce
import numpy as np
import json

words=list((0,*w,5) for w in permutations(range(1,5)))
widx={w:j for j,w in enumerate(words)}
C=np.zeros((8,)*6+(24,),dtype=np.int64)
for key,w,c in tensor_rows(6):
    assert (432*c).denominator==1
    C[key+(widx[w],)]+=int(432*c)
C=C+C.swapaxes(0,5)
assert np.max(np.abs(C)) <= 100000
def gram(T, metrics):
    x=T.reshape(-1,24)
    W=np.array([3**len(key)//reduce(lambda a,b:a*b,key,1) for key in product(*metrics)])
    assert int(np.max(np.abs(x)))**2 * int(W.sum()) < 2**60
    return x.T@(W[:,None]*x)
G=gram(C,[METRIC]*6)
S=sum(C[a,:,:,:,:,a]*(3//METRIC[a]) for a in range(8))
SG=gram(S,[METRIC]*4)
D=np.zeros((8,)*5+(24,),dtype=np.int64)
for (a,b),row in D_TABLE.items():
    for c,v in row:
        factor=18*v/(METRIC[a]*METRIC[b])
        assert factor.denominator==1
        D[c]+=C[a,:,:,:,:,b]*int(factor)
DG=gram(D,[METRIC]*5)
assert sum(scale*int(np.max(np.abs(g))) for scale,g in ((180,G),(45,SG),(2,DG))) < 2**62
Q=180*G-45*SG-2*DG
Q=Q//reduce(gcd,map(int,Q.flat))
assert np.array_equal(Q,Q.T)

def add(a,b,scale=1):
    r=defaultdict(int,a)
    for k,v in b.items():r[k]+=scale*v
    return {k:v for k,v in r.items() if v}
def mul(a,b):
    r=defaultdict(int)
    for (i,j),v in a.items():
        for (k,l),w in b.items():r[i+k,j+l]+=v*w
    return {k:v for k,v in r.items() if v}
Z=[{}, {}, {(0,0):1},{(0,0):1,(1,0):1},{(0,0):1,(1,0):1,(0,1):1}]
edges=set(combinations(range(1,5),2))
dp=[[],[]]
for w in words:
    hard=w[1:-1]
    path=list(zip(hard,hard[1:]))
    complementary=sorted(edges-{tuple(sorted(e)) for e in path})
    factors=[(hard[0],hard[-1]),*complementary]
    sign=(-1)**sum(a>b for a,b in path)
    for index,spectator in enumerate((3,4)):
        deriv={}
        for i,(a,b) in enumerate(factors):
            c=int(b==spectator)-int(a==spectator)
            if not c:continue
            p=reduce(mul,[add(Z[v],Z[u],-1) for j,(u,v) in enumerate(factors) if j!=i],{(0,0):1})
            deriv=add(deriv,p,c*sign)
        dp[index].append(deriv)
def form(a,b):
    r={}
    for i,u in enumerate(a):
        for j,v in enumerate(b):
            if Q[i,j]:r=add(r,mul(u,v),int(Q[i,j]))
    return r
a,b,c=form(dp[0],dp[0]),form(dp[0],dp[1]),form(dp[1],dp[1])
det=add(mul(a,c),mul(b,b),-1)
assert a and det and min(a.values())>0 and min(det.values())>0
print(json.dumps({name:[[i,j,v] for (i,j),v in sorted(poly.items())]
                  for name,poly in (("M11",a),("M12",b),("M22",c),("determinant",det))},
                 indent=2))
