# CROSS-33 — Three LR3 fronts and failure of naive ++-pair conservation

Status: exact local algebra and finite sign-space BFS. General lower bound remains OPEN.

For t>=1, the balanced cyclic family F_t=A(BC)^(t+2)(AC)^(t+1)(AB)^(t+1) has sign word S_t=++(-+)^t-++(-+)^t-++(-+)^t-. The only legal LR3 sign rewrites are -++- <-> +--+, on four consecutive cyclic edges. At the initial state there are exactly three LR3 windows, starting at sign indices 2t+2, 4t+5 and 6t+8 (zero-based). Their cyclic spacing is 2t+3.

The number of adjacent ++ pairs is not invariant. For example, with one sign of context on each side, +-++-+ -> ++--++ increases the count of ++ from 1 to 2; --++-- -> -+--+- decreases it from 1 to 0. Therefore no lower-bound proof may treat the original ++ pairs as conserved particles.

Exact sign-space breadth-first search, stopping expansion when LR4 is active, gives the following number of distinct states per depth:
- t=1: 1,3
- t=2: 1,3,9
- t=3: 1,3,9,22
- t=4: 1,3,9,22,51
- t=5: 1,3,9,22,51,108
These are sign-word states, without colour-phase multiplicity. LR4 activation is detected using the fourteen five-edge windows listed in CROSS-28. First activation depths are t=1..5, consistent with CROSS-32.

## Reproducible Python
```python
from collections import deque,Counter
bad={'-----','----+','---+-','--+--','-+---','+----','+---+',
     '-+++-','-++++','+-+++','++-++','+++-+','++++-','+++++'}
def sign(t):return '++'+'-+'*t+'-++'+'-+'*t+'-++'+'-+'*t+'-'
def moves(s):
 n=len(s)
 for i in range(n):
  p=''.join(s[(i+j)%n] for j in range(4))
  if p not in ('-++-','+--+'):continue
  v=list(s)
  for j,x in enumerate('+--+' if p=='-++-' else '-++-'):
   v[(i+j)%n]=x
  yield i,''.join(v)
def active(s):
 n=len(s)
 return any(''.join(s[(i+j)%n] for j in range(5)) in bad for i in range(n))
for t in range(1,6):
 s=sign(t)
 starts=[i for i,v in moves(s)]
 assert starts==[2*t+2,4*t+5,6*t+8]
 q=deque([(s,0)]);seen={s};layers=Counter()
 while q:
  u,d=q.popleft();layers[d]+=1
  if active(u) or d>=t:continue
  for i,v in moves(u):
   if v not in seen:seen.add(v);q.append((v,d+1))
 print(t,dict(layers))
```

## Next proof obligation
Seek a causal-cone or interval-front invariant valid under *all* LR3 rewrites, including moves across region boundaries and cyclic wraparound. Show no LR4-active five-edge window can occur before t moves. Current observations alone do not establish such a bound; neither conservation of ++ pairs nor a naive single-front speed limit is justified.
