"""EHF-DIM-03: leading symmetry sectors of OPW3 and OPW23 at n=7. Requires numpy."""
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
index={s:i for i,s in enumerate(states)}
def graph(lengths):
 adj=[set() for _ in states]
 for i,s in enumerate(states):
  for L in lengths:
   for k in range(7):
    t=rev(s,k,L)
    if t!=s and frozenset(t[::2])==frozenset(s[::2]):
     j=index[t];adj[i].add(j);adj[j].add(i)
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
def mat(g):
 A=np.zeros((36,36))
 for v in verts:
  for w in g[v]:A[loc[v],loc[w]]=1
 return A
A3,A23=mat(g3),mat(g23)
assert np.all(A3.sum(axis=1)==4) and np.all(A23.sum(axis=1)==6)
even=sorted(set(states[verts[0]][::2])-{0})
odd=sorted(set(range(7))-set(states[verts[0]][::2]))
def chi(p,t):
 if t=='t':return 1
 if t=='s':return (-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
 return sum(p[i]==i for i in range(3))-1
G=[]
for pe in permutations(range(3)):
 for po in permutations(range(3)):
  m={0:0,**{even[i]:even[pe[i]] for i in range(3)},**{odd[i]:odd[po[i]] for i in range(3)}}
  R=np.zeros((36,36))
  for v in verts:
   w=index[canon(tuple(m[x] for x in states[v]))]
   R[loc[w],loc[v]]=1
  assert np.allclose(R@A3,A3@R) and np.allclose(R@A23,A23@R)
  G.append((pe,po,R))
sectors={}
for a in 'tsd':
 for b in 'tsd':
  d=(2 if a=='d' else 1)*(2 if b=='d' else 1)
  P=d/36*sum(chi(pe,a)*chi(po,b)*R for pe,po,R in G)
  assert np.allclose(P@P,P)
  values,vectors=np.linalg.eigh(P);B=vectors[:,values>.5]
  assert B.shape[1]==d*d
  sectors[a+b]=[np.linalg.eigvalsh(B.T@A@B) for A in (A3,A23)]
for label,j,degree in [('OPW3',0,4),('OPW23',1,6)]:
 nonconstant={s:float(max(v[j])) for s,v in sectors.items() if s!='tt'}
 top=max(nonconstant.values())
 leaders=sorted(s for s,x in nonconstant.items() if abs(x-top)<1e-8)
 assert np.isclose(top,3) and leaders==['dt','td']
 assert np.allclose(sectors['dt'][j],[1,1,3,3])
 assert np.allclose(sectors['td'][j],[1,1,3,3])
 lazy=np.linalg.eigvalsh((np.eye(36)+(A3,A23)[j]/degree)/2)
 assert np.isclose(lazy[-2],(1+3/degree)/2)
 print(label,'slow sectors',leaders,'normalized eigenvalue',top/degree,'lazy second',lazy[-2])
print('PASS')
