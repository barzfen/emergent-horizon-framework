"""EHF-DIM-02: symmetry-preserving but noncommuting reversal dynamics. Requires numpy."""
from itertools import permutations
import numpy as np
def canonical(c):
 c=list(c);k=c.index(0);c=c[k:]+c[:k]
 return min(tuple(c),(0,)+tuple(reversed(c[1:])))
def reverse(c,k,L):
 a=list(c);ix=[(k+j)%7 for j in range(L)]
 for i,x in zip(ix,[a[j] for j in ix][::-1]):a[i]=x
 return canonical(a)
states=sorted({canonical((0,)+p) for p in permutations(range(1,7))})
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
assert sum(map(len,g3))//2==600 and sum(map(len,g23))//2==840
unseen=set(range(360));components=[]
while unseen:
 root=unseen.pop();component={root};stack=[root]
 while stack:
  v=stack.pop()
  for w in g3[v]&unseen:unseen.remove(w);component.add(w);stack.append(w)
 components.append(component)
assert len(components)==19
verts=sorted(max(components,key=len));assert len(verts)==36
local={v:i for i,v in enumerate(verts)}
def adjacency(graph):
 A=np.zeros((36,36))
 for v in verts:
  for w in graph[v]:A[local[v],local[w]]=1
 return A
A3,A23=adjacency(g3),adjacency(g23)
assert np.all(A3.sum(axis=1)==4) and np.all(A23.sum(axis=1)==6)
even=sorted(set(states[verts[0]][::2])-{0})
odd=sorted(set(range(7))-set(states[verts[0]][::2]))
def character(p,t):
 if t=='t':return 1
 if t=='s':return (-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
 return sum(p[i]==i for i in range(3))-1
G=[]
for pe in permutations(range(3)):
 for po in permutations(range(3)):
  m={0:0,**{even[i]:even[pe[i]] for i in range(3)},**{odd[i]:odd[po[i]] for i in range(3)}}
  R=np.zeros((36,36))
  for v in verts:R[local[index[canonical(tuple(m[x] for x in states[v]))]],local[v]]=1
  assert np.allclose(R@A3,A3@R) and np.allclose(R@A23,A23@R)
  G.append((pe,po,R))
assert len(G)==36
assert not np.allclose(A3@A23,A23@A3)
for a in 'tsd':
 for b in 'tsd':
  d=(2 if a=='d' else 1)*(2 if b=='d' else 1)
  projector=sum(character(pe,a)*character(po,b)*R for pe,po,R in G)*d/36
  assert np.allclose(projector@projector,projector)
  values,vectors=np.linalg.eigh(projector)
  basis=vectors[:,values>.5]
  assert basis.shape[1]==d*d
  print(a+b,'dimension',d*d,'OPW3',np.round(np.linalg.eigvalsh(basis.T@A3@basis),6).tolist(),
        'OPW23',np.round(np.linalg.eigvalsh(basis.T@A23@basis),6).tolist())
assert np.isclose(1-np.linalg.eigvalsh(A3)[-2]/4,.25)
assert np.isclose(1-np.linalg.eigvalsh(A23)[-2]/6,.5)
assert not np.allclose(np.linalg.eigvalsh(A23),np.rint(np.linalg.eigvalsh(A23)))
print('PASS: identical isotypic sectors; distinct, noncommuting adjacency dynamics.')
