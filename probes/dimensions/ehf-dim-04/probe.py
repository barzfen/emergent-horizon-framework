"""EHF-DIM-04 standalone audit; requires numpy."""
from itertools import permutations
import numpy as np
def canon(c):
 c=list(c); k=c.index(0);c=c[k:]+c[:k]
 return min(tuple(c),(0,)+tuple(reversed(c[1:])))
def reverse(c,k,L):
 a=list(c);ix=[(k+j)%7 for j in range(L)]
 for i,x in zip(ix,[a[j] for j in ix][::-1]):a[i]=x
 return canon(a)
states=sorted({canon((0,)+p) for p in permutations(range(1,7))})
index={s:i for i,s in enumerate(states)}
def graph(lengths):
 adj=[set() for _ in states]
 for i,s in enumerate(states):
  for L in lengths:
   for k in range(7):
    t=reverse(s,k,L)
    if t!=s and frozenset(t[::2])==frozenset(s[::2]):
     j=index[t];adj[i].add(j);adj[j].add(i)
 return adj
g3,g23=graph((3,)),graph((2,3))
unseen=set(range(360));components=[]
while unseen:
 root=unseen.pop();comp={root};stack=[root]
 while stack:
  v=stack.pop()
  for w in g3[v]&unseen:unseen.remove(w);comp.add(w);stack.append(w)
 components.append(comp)
verts=sorted(max(components,key=len));assert len(verts)==36
loc={v:i for i,v in enumerate(verts)}
def matrix(g):
 A=np.zeros((36,36))
 for v in verts:
  for w in g[v]:A[loc[v],loc[w]]=1
 return A
A3,A23=matrix(g3),matrix(g23);A2=A23-A3
E=sorted(set(states[verts[0]][::2])-{0})
O=sorted(set(range(7))-set(states[verts[0]][::2]))
def chi(p,kind):
 if kind=='t':return 1
 if kind=='s':return (-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
 return sum(p[i]==i for i in range(3))-1
G=[]
for pe in permutations(range(3)):
 for po in permutations(range(3)):
  m={0:0,**{E[i]:E[pe[i]] for i in range(3)},**{O[i]:O[po[i]] for i in range(3)}}
  R=np.zeros((36,36))
  for v in verts:
   w=index[canon(tuple(m[x] for x in states[v]))]
   R[loc[w],loc[v]]=1
  assert np.allclose(R@A3,A3@R) and np.allclose(R@A23,A23@R)
  G.append((pe,po,R))
for a in 'tsd':
 for b in 'tsd':
  d=(2 if a=='d' else 1)*(2 if b=='d' else 1)
  P=d/36*sum(chi(pe,a)*chi(po,b)*R for pe,po,R in G)
  z,V=np.linalg.eigh(P);B=V[:,z>.5]
  vals3=np.linalg.eigvalsh(B.T@A3@B)
  vals23=np.linalg.eigvalsh(B.T@A23@B)
  print(a+b,'OPW3',np.round(vals3,6),'OPW23',np.round(vals23,6))
  if a+b in ('td','dt'):
   assert np.allclose(vals3,[1,1,3,3]) and np.allclose(vals23,[1,1,3,3])
   ew,U=np.linalg.eigh(B.T@A3@B);T=B@U[:,ew>2.5]
   assert np.allclose(T.T@A2@T,-0.5*np.eye(2))
   assert np.isclose(np.linalg.norm(A2@T-T@(T.T@A2@T)),np.sqrt(1.5))
assert np.isclose(np.linalg.norm(A3@A2-A2@A3),12)
print('PASS: DIM-04 finite-sector identities')
