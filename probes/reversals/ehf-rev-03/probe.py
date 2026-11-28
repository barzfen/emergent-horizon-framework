"""EHF-REV-03: exact n=7 OPW3 chamber and natural relabelling symmetry."""
from collections import Counter
from itertools import permutations
N=7
def canonical(c):
 c=list(c); k=c.index(0); c=c[k:]+c[:k]
 return min(tuple(c),(0,)+tuple(reversed(c[1:])))
def preserve(c): return frozenset(c[::2])
def reverse(c,start):
 c=list(c); positions=[(start+j)%len(c) for j in range(3)]
 values=[c[j] for j in positions][::-1]
 for j,value in zip(positions,values): c[j]=value
 return canonical(c)
states=sorted({canonical((0,)+p) for p in permutations(range(1,N))})
index={s:i for i,s in enumerate(states)}
adj=[set() for _ in states]
for i,s in enumerate(states):
 for start in range(N):
  t=reverse(s,start)
  if t!=s and preserve(t)==preserve(s):
   j=index[t]; adj[i].add(j);adj[j].add(i)
assert len(states)==360 and sum(map(len,adj))//2==600
unseen=set(range(len(states))); components=[]
while unseen:
 root=min(unseen); comp=set(); frontier=[root];unseen.remove(root)
 while frontier:
  v=frontier.pop();comp.add(v)
  for w in adj[v]&unseen: unseen.remove(w);frontier.append(w)
 components.append(comp)
assert len(components)==19
assert Counter(map(len,components))=={36:1,32:1,28:2,24:3,20:3,16:3,12:3,8:2,4:1}
largest=next(c for c in components if len(c)==36)
assert all(len(adj[i])==4 for i in largest)
representative=states[min(largest)]
even=sorted(preserve(representative)-{0})
odd=sorted(set(range(N))-preserve(representative))
assert len(even)==len(odd)==3
actions=[]
for pe in permutations(even):
 for po in permutations(odd):
  actions.append({0:0,**dict(zip(even,pe)),**dict(zip(odd,po))})
assert len(actions)==36
def act(mapping,state): return index[canonical(tuple(mapping[v] for v in state))]
assert {act(m,representative) for m in actions}==largest
for mapping in actions:
 assert {act(mapping,states[i]) for i in largest}==largest
 for i in largest:
  assert {act(mapping,states[j]) for j in adj[i]}==adj[act(mapping,states[i])]
dims=sorted(a*b for a in (1,1,2) for b in (1,1,2))
assert dims==[1,1,1,1,2,2,2,2,4] and sum(d*d for d in dims)==36
print("PASS: 360 states; 600 LR3 edges; 19 chambers")
print("Chamber sizes:",dict(sorted(Counter(map(len,components)).items())))
print("Largest: 36 vertices, degree 4, free transitive S3 x S3 relabelling action")
print("Irrep dimensions:",dims)
