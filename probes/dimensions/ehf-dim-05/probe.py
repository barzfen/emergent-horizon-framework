"""EHF-DIM-05: reproduce weighted LR2 sector spectra. Requires numpy."""
from itertools import permutations
import numpy as np
def canon(c):
 c=list(c);k=c.index(0);c=c[k:]+c[:k]
 return min(tuple(c),(0,)+tuple(reversed(c[1:])))
def rev(c,k,L):
 a=list(c); ix=[(k+j)%7 for j in range(L)]
 for i,x in zip(ix,[a[j] for j in ix][::-1]):a[i]=x
 return canon(a)
states=sorted({canon((0,)+p) for p in permutations(range(1,7))})
idx={s:i for i,s in enumerate(states)}
def graph(lengths):
 adj=[set() for _ in states]
 for i,s in enumerate(states):
  for L in lengths:
   for k in range(7):
    t=rev(s,k,L)
    if t!=s and frozenset(t[::2])==frozenset(s[::2]):
     j=idx[t];adj[i].add(j);adj[j].add(i)
 return adj
g3,g23=graph((3,)),graph((2,3))
unseen=set(range(360));comps=[]
while unseen:
 root=unseen.pop();comp={root};stack=[root]
 while stack:
  v=stack.pop()
  for w in g3[v]&unseen:
   unseen.remove(w);comp.add(w);stack.append(w)
 comps.append(comp)
verts=sorted(max(comps,key=len));assert len(verts)==36
loc={v:i for i,v in enumerate(verts)}
def matrix(g):
 A=np.zeros((36,36))
 for v in verts:
  for w in g[v]:A[loc[v],loc[w]]=1
 return A
A3=matrix(g3);A2=matrix(g23)-A3
even=sorted(set(states[verts[0]][::2])-{0})
odd=sorted(set(range(7))-set(states[verts[0]][::2]))
def chi(p,kind):
 if kind=='t':return 1
 if kind=='s':return (-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
 return sum(p[i]==i for i in range(3))-1
G=[]
for pe in permutations(range(3)):
 for po in permutations(range(3)):
  m={0:0,**{even[i]:even[pe[i]] for i in range(3)},**{odd[i]:odd[po[i]] for i in range(3)}}
  R=np.zeros((36,36))
  for v in verts:
   w=idx[canon(tuple(m[x] for x in states[v]))]
   R[loc[w],loc[v]]=1
  G.append((pe,po,R))
for a,b in [('t','d'),('d','t')]:
 P=2/36*sum(chi(pe,a)*chi(po,b)*R for pe,po,R in G)
 eig,V=np.linalg.eigh(P);B=V[:,eig>.5]
 assert B.shape==(36,4)
 X=B.T@A3@B;Y=B.T@A2@B
 traces=[np.trace(M) for M in [X,Y,X@Y,Y@Y,X@X]]
 assert np.allclose(traces,[8,0,-2,4,20]),traces
 for w in [0,.1,.25,.5,.75,1,1.5,2]:
  vals=np.linalg.eigvalsh(X+w*Y)
  target=[2-np.sqrt(1-w+w*w)]*2+[2+np.sqrt(1-w+w*w)]*2
  assert np.allclose(vals,target,atol=1e-10),(w,vals,target)
  print(a+b,'w=',w,'eigenvalues=',np.round(vals,9).tolist())
print('PASS: DIM-05 weighted-sector spectrum')
