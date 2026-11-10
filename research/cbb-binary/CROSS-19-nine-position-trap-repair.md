# EHF-CBB-CROSS-19 — Nine-position trapped-component repair audit

Status: exact exhaustive n=9 finite computation; no arbitrary-length theorem.

## Setup
Balanced proper position-indexed cyclic words of length 9 over A,B,C. W=(number of forward A->B->C->A edges minus reverse edges)/3. LRk reverses k consecutive cyclic positions; all resulting cyclic adjacencies must remain proper.

At W=+1, there are exactly nine LR3-connected components that have no LR4 edge upward to W=+3 from any member. Each trapped component has four position-indexed words.

## Result
For each of these nine components, at least one member admits a shortest 3-move LR3/LR4 path to W=+3 with minimum winding -1. All nine representatives have such a path using LR4 moves only. The winding profile is +1 -> -1 -> +1 -> +3. This does NOT show that every member of each trapped component can escape in three moves: other members may require LR3 moves first. It also does not imply a bounded-size repair lemma for arbitrary n.

## Explicit certificate
A=0,B=1,C=2. Start 020121012 = ACABCBABC (W=+1).
LR4 start 0: 102021012 = BACACBABC (W=-1).
LR4 start 3: 102012012 = BACABCABC (W=+1).
LR4 start 8: 012012012 = ABCABCABC (W=+3).
All reversals use cyclic position indices 0..8, with wraparound where required.

## Reproducible audit
```python
from itertools import product
from collections import deque,Counter
n=9;m=3
S={w for w in product(range(3),repeat=n) if all(w.count(x)==m for x in range(3)) and all(w[i]!=w[(i+1)%n] for i in range(n))}
def W(w):return sum(1 if (w[(i+1)%n]-w[i])%3==1 else -1 for i in range(n))//3
def nei(w,k):
 for i in range(n):
  ix=[(i+j)%n for j in range(k)];v=list(w)
  for a,b in zip(ix,reversed([w[t] for t in ix])):v[a]=b
  v=tuple(v)
  if v in S and v!=w:yield v,i
seen=set();traps=[]
for w in S:
 if W(w)!=1 or w in seen:continue
 stack=[w];seen.add(w);component=[]
 while stack:
  u=stack.pop();component.append(u)
  for v,_ in nei(u,3):
   if v not in seen:seen.add(v);stack.append(v)
 if not any(W(v)==3 for u in component for v,_ in nei(u,4)):traps.append(component)
assert len(traps)==9 and all(len(c)==4 for c in traps)
for component in traps:
 best=999
 for s in component:
  queue=deque([(s,0)]);visited={s}
  while queue:
   u,d=queue.popleft()
   if W(u)==3:best=min(best,d);break
   for k in (3,4):
    for v,_ in nei(u,k):
     if v not in visited and W(v)>=-1:
      visited.add(v);queue.append((v,d+1))
 assert best==3
print('Nine traps, each with a three-move repair from some member')
```

## Research direction
Classify these trap configurations by local sign-word patterns and identify a defect-transport move that generalizes to all balanced lengths. Test whether one downward winding step always suffices, without conflating finite evidence with a general proof.
