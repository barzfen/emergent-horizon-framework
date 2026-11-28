"""EHF-REV-04 exact n=7 adjacency and S3xS3 character-projector spectrum.
Requires numpy. Run from repo root: python3 probes/reversals/ehf-rev-04/probe.py
"""
from collections import Counter
from itertools import permutations
import numpy as np

n=7
def canon(c):
    c=list(c); k=c.index(0); c=c[k:]+c[:k]
    return min(tuple(c),(0,)+tuple(reversed(c[1:])))
def pi(c): return frozenset(c[::2])
def reverse(c,k):
    a=list(c); ix=[(k+j)%n for j in range(3)]
    for j,v in zip(ix,[a[j] for j in ix][::-1]): a[j]=v
    return canon(a)
states=sorted({canon((0,)+p) for p in permutations(range(1,n))})
idx={s:i for i,s in enumerate(states)}
adj=[set() for _ in states]
for i,s in enumerate(states):
    for k in range(n):
        t=reverse(s,k)
        if t!=s and pi(t)==pi(s):
            j=idx[t];adj[i].add(j);adj[j].add(i)
assert len(states)==360 and sum(map(len,adj))//2==600
remaining=set(range(len(states))); comps=[]
while remaining:
    root=remaining.pop(); comp={root}; stack=[root]
    while stack:
        v=stack.pop()
        for w in adj[v]&remaining:
            remaining.remove(w);comp.add(w);stack.append(w)
    comps.append(comp)
assert len(comps)==19
largest=max(comps,key=len); assert len(largest)==36
verts=sorted(largest); loc={v:i for i,v in enumerate(verts)}
A=np.zeros((36,36))
for v in verts:
    for w in adj[v]:A[loc[v],loc[w]]=1
assert np.all(A.sum(axis=1)==4)
even=sorted(pi(states[verts[0]])-{0})
odd=sorted(set(range(n))-pi(states[verts[0]]))
def character(p,kind):
    if kind=='t':return 1
    if kind=='s':return (-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
    return sum(p[i]==i for i in range(3))-1
G=[]
for pe in permutations(range(3)):
    for po in permutations(range(3)):
        mapping={0:0,**{even[i]:even[pe[i]] for i in range(3)},
                       **{odd[i]:odd[po[i]] for i in range(3)}}
        R=np.zeros((36,36))
        for v in verts:
            w=idx[canon(tuple(mapping[x] for x in states[v]))]
            R[loc[w],loc[v]]=1
        assert np.allclose(R@A,A@R)
        G.append((pe,po,R))
expected={'tt':(1,[4]),'ts':(1,[0]),'st':(1,[0]),'ss':(1,[-4]),
          'td':(4,[1,1,3,3]),'dt':(4,[1,1,3,3]),
          'sd':(4,[-3,-3,-1,-1]),'ds':(4,[-3,-3,-1,-1]),
          'dd':(16,[-2]*4+[0]*8+[2]*4)}
for a in 'tsd':
    for b in 'tsd':
        d=(2 if a=='d' else 1)*(2 if b=='d' else 1)
        projector=sum(character(pe,a)*character(po,b)*R for pe,po,R in G)*d/36
        assert np.allclose(projector@projector,projector)
        values,vectors=np.linalg.eigh(projector)
        basis=vectors[:,values>.5]
        eigs=np.linalg.eigvalsh(basis.T@A@basis)
        rank, expected_eigs=expected[a+b]
        assert basis.shape[1]==rank
        assert np.allclose(eigs,expected_eigs,atol=1e-8)
        print(a+b,rank,np.round(eigs,6).tolist())
assert Counter(np.rint(np.linalg.eigvalsh(A)).astype(int))==Counter({-4:1,-3:4,-2:4,-1:4,0:10,1:4,2:4,3:4,4:1})
print('PASS: exact n=7 OPW3 spectral-sector benchmark (numerical eigenvalue check).')
