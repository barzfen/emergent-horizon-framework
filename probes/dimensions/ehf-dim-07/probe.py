"""DIM-07 exact Cayley identification; Python standard library only."""
from itertools import permutations
def can(c):
 c=list(c);k=c.index(0);c=c[k:]+c[:k]
 return min(tuple(c),(0,)+tuple(reversed(c[1:])))
def rev(c,k,L):
 a=list(c);ix=[(k+j)%7 for j in range(L)]
 for i,v in zip(ix,[a[j] for j in ix][::-1]):a[i]=v
 return can(a)
states=sorted({can((0,)+p) for p in permutations(range(1,7))})
idx={s:i for i,s in enumerate(states)}
def graph(L):
 adj=[set() for _ in states]
 for i,s in enumerate(states):
  for k in range(7):
   t=rev(s,k,L)
   if t!=s and set(t[::2])==set(s[::2]):adj[i].add(idx[t])
 return adj
g3,g2=graph(3),graph(2)
unseen=set(range(360));comps=[]
while unseen:
 r=unseen.pop();comp={r};stack=[r]
 while stack:
  v=stack.pop()
  for w in g3[v]&unseen:unseen.remove(w);comp.add(w);stack.append(w)
 comps.append(comp)
vs=sorted(max(comps,key=len));assert len(vs)==36
root=vs[0];E=sorted(set(states[root][::2])-{0})
O=sorted(set(range(7))-set(states[root][::2]))
perms=list(permutations(range(3)))
def action(pe,po,s):
 m={0:0,**{E[i]:E[pe[i]] for i in range(3)},**{O[i]:O[po[i]] for i in range(3)}}
 return can([m[x] for x in s])
f={(pe,po):idx[action(pe,po,states[root])] for pe in perms for po in perms}
assert set(f.values())==set(vs)
e=(0,1,2);a=(1,0,2);b=(0,2,1);c=(2,1,0)
def mul(p,q):return tuple(p[q[i]] for i in range(3))
S3=set(perms)
generators3={(a,e),(b,e),(e,a),(e,b)}
generators2={(c,b),(a,c)}
assert {key for key,v in f.items() if v in g3[root]}==generators3
assert {key for key,v in f.items() if v in g2[root]}==generators2
for pe in S3:
 for po in S3:
  v=f[(pe,po)]
  for generators,graph_ in ((generators3,g3),(generators2,g2)):
   expected={f[(mul(pe,x),mul(po,y))] for x,y in generators}
   assert graph_[v]==expected
# Six-cycle order and Cartesian product adjacency
order=[e];prev=None;cur=e
for k in range(5):
 candidates=[mul(cur,x) for x in (a,b) if mul(cur,x)!=prev]
 nxt=candidates[0];order.append(nxt);prev,cur=cur,nxt
assert len(set(order))==6
coord={p:i for i,p in enumerate(order)}
for pe in S3:
 for po in S3:
  v=f[(pe,po)];i,j=coord[pe],coord[po]
  expected={f[(order[(i-1)%6],po)],f[(order[(i+1)%6],po)],
            f[(pe,order[(j-1)%6])],f[(pe,order[(j+1)%6])]}
  assert g3[v]==expected
print('PASS: n=7 36-state OPW3 chamber is exactly C6 Cartesian C6')
print('LR3 generators:',sorted(generators3))
print('LR2 generators:',sorted(generators2))
