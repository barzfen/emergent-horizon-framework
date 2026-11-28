"""DIM-08: exact all-edge Cayley isomorphism, n=7 or n=9. Standard library."""
from itertools import permutations
import sys
def can(c):
 c=list(c);k=c.index(0);c=c[k:]+c[:k]
 return min(tuple(c),(0,)+tuple(reversed(c[1:])))
def rev(c,k,L):
 a=list(c);ix=[(k+j)%len(c) for j in range(L)]
 for j,v in zip(ix,[a[j] for j in ix][::-1]):a[j]=v
 return can(a)
n=int(sys.argv[1]) if len(sys.argv)>1 else 9
assert n in (7,9)
m=(n-1)//2
states=sorted({can((0,)+p) for p in permutations(range(1,n))})
idx={s:i for i,s in enumerate(states)}
adj=[set() for _ in states]
for i,s in enumerate(states):
 for k in range(n):
  t=rev(s,k,3)
  if t!=s and set(t[::2])==set(s[::2]):adj[i].add(idx[t])
unseen=set(range(len(states)));comps=[]
while unseen:
 r=unseen.pop();cc={r};q=[r]
 while q:
  v=q.pop()
  for w in adj[v]&unseen:unseen.remove(w);cc.add(w);q.append(w)
 comps.append(cc)
vs=max(comps,key=len);root=min(vs);s=states[root]
assert len(vs)==(6 if n==7 else 24)**2
E=sorted(set(s[::2])-{0});O=sorted(set(range(n))-set(s[::2]))
ps=list(permutations(range(m)));identity=tuple(range(m))
F={}
for pe in ps:
 for po in ps:
  mapping={0:0,**{E[i]:E[pe[i]] for i in range(m)},
                  **{O[i]:O[po[i]] for i in range(m)}}
  F[(pe,po)]=idx[can(tuple(mapping[x] for x in s))]
assert set(F.values())==vs
G={key for key,v in F.items() if v in adj[root]}
def swap(i):
 a=list(range(m));a[i],a[i+1]=a[i+1],a[i];return tuple(a)
expected_generators={(swap(i),identity) for i in range(m-1)}|{(identity,swap(i)) for i in range(m-1)}
assert G==expected_generators
def mul(p,q):return tuple(p[q[i]] for i in range(m))
for (pe,po),v in F.items():
 expected={F[(mul(pe,x),mul(po,y))] for x,y in G}
 assert adj[v]==expected
print('PASS n=',n,'states=',len(states),'components=',len(comps),'largest=',len(vs),'generators=',len(G))
