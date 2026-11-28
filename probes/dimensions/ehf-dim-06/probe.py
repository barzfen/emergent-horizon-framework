"""EHF-DIM-06: exact integer verification of projected reversal algebra."""
import numpy as np
from itertools import permutations
def can(c):
 c=list(c);k=c.index(0);c=c[k:]+c[:k]
 return min(tuple(c),(0,)+tuple(reversed(c[1:])))
def rev(c,k,L):
 a=list(c); ix=[(k+j)%7 for j in range(L)]
 for i,v in zip(ix,[a[j] for j in ix][::-1]):a[i]=v
 return can(a)
states=sorted({can((0,)+p) for p in permutations(range(1,7))})
idx={s:i for i,s in enumerate(states)}
def graph(Ls):
 adj=[set() for _ in states]
 for i,s in enumerate(states):
  for L in Ls:
   for k in range(7):
    t=rev(s,k,L)
    if t!=s and set(t[::2])==set(s[::2]):
     j=idx[t];adj[i].add(j);adj[j].add(i)
 return adj
g3=graph((3,));g23=graph((2,3))
unseen=set(range(360));comps=[]
while unseen:
 r=unseen.pop();cc={r};q=[r]
 while q:
  v=q.pop()
  for w in g3[v]&unseen:
   unseen.remove(w);cc.add(w);q.append(w)
 comps.append(cc)
verts=sorted(max(comps,key=len));assert len(verts)==36
loc={v:i for i,v in enumerate(verts)}
def mat(g):
 A=np.zeros((36,36),dtype=int)
 for v in verts:
  for w in g[v]:A[loc[v],loc[w]]=1
 return A
A=mat(g3);B=mat(g23)-A
E=sorted(set(states[verts[0]][::2])-{0})
O=sorted(set(range(7))-set(states[verts[0]][::2]))
def ch(p,k):
 if k=='t':return 1
 if k=='s':return (-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
 return sum(p[i]==i for i in range(3))-1
G=[]
for pe in permutations(range(3)):
 for po in permutations(range(3)):
  m={0:0,**{E[i]:E[pe[i]] for i in range(3)},**{O[i]:O[po[i]] for i in range(3)}}
  R=np.zeros((36,36),dtype=int)
  for v in verts:
   w=idx[can(tuple(m[x] for x in states[v]))]
   R[loc[w],loc[v]]=1
  G.append((pe,po,R))
I=np.eye(36,dtype=int)
X=A-2*I;Y=B
for a,b in [('t','d'),('d','t')]:
 Q=sum((ch(pe,a)*ch(po,b)*R for pe,po,R in G),np.zeros((36,36),dtype=int))
 assert np.array_equal(Q@Q,18*Q)
 for M in (X@X-I,Y@Y-I,X@Y+Y@X+I):
  assert not np.any(M@Q)
 print(a+b,'exact integer identities PASS')
print('PASS')
