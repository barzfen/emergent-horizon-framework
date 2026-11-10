# EHF-CBB-CROSS-26 — LR4-only connectivity and an exceptional 15-cycle obstruction

Date: 2026-11-11 AEST. Status: independently executed exhaustive enumeration for n=6,9,12,15,18. General theorem open.

## Definitions
Balanced proper position-indexed cyclic words of length n=3m over A,B,C, each colour occurring m times. LRk reverses k consecutive cyclic vertices, accepted only when cyclic properness is retained. The graph has a vertex for each such word and an undirected edge for each nontrivial legal LRk move.

## New exhaustive LR4-only graph results
| n | vertices | LR4-only components | largest component | isolated vertices |
| 6 | 24 | 1 | 24 | 0 |
| 9 | 132 | 1 | 132 | 0 |
| 12 | 804 | 1 | 804 | 0 |
| 15 | 5196 | 31 | 5166 | 30 |
| 18 | 34872 | 1 | 34872 | 0 |

At n=15 all 30 exceptional components are isolated vertices, not nontrivial small clusters. Of these, 15 have D=6 (winding W=+1) and 15 have D=9 (W=-1). Each has exactly three distinct legal LR3 neighbours, so LR3 is capable of escaping the LR4-only isolation. Full LR3+LR4 connectivity was previously verified through n=18 (CROSS-13).

One explicit isolated n=15 colour word is
```
ABABABCBCBCACAC
```
with cyclic orientation signs
```
+-+-++-+-++-+-+
```
It has D=6 and no admissible LR4 moves. Nevertheless it has three legal LR3 neighbours.

## Additional bounded-repair test using LR4 only
Define D(w)=number of negative orientation edges, a multiple of 3. For each w with d=D(w)>0, find the shortest LR4-only path to any v with D(v)<d subject to D<=d+3 at all intermediate states. Exact results:
| n | reachable repair-length histogram | unreachable starting words |
| 6 | 1:21 | 0 |
| 9 | 1:93, 3:36 | 0 |
| 12 | 1:681, 3:108, 5:12 | 0 |
| 15 | 1:4473, 3:555, 5:135 | 30 |
| 18 | 1:31215, 3:3186, 5:342, 7:126 | 0 |

The 30 unreachable at n=15 are exactly the isolated LR4 vertices. With LR3 restored, CROSS-25 found all words repairable at n=15 within the same defect cap.

## Reproduction
```python
from collections import deque,Counter,defaultdict
for m in range(2,7):
 n=3*m;words=[]
 def rec(w,c):
  if len(w)==n:
   if w[-1]!=w[0]:words.append(tuple(w))
   return
  for x in range(3):
   if c[x]<m and (not w or w[-1]!=x):
    c[x]+=1;w.append(x);rec(w,c);w.pop();c[x]-=1
 rec([],[0]*3);S=set(words)
 def D(w):return sum((w[(i+1)%n]-w[i])%3==2 for i in range(n))
 def nei(w,k):
  for i in range(n):
   ix=[(i+j)%n for j in range(k)];v=list(w)
   for a,b in zip(ix,reversed([w[t] for t in ix])):v[a]=b
   v=tuple(v)
   if v!=w and v in S:yield v
 edges={w:set(nei(w,4)) for w in words}
 seen=set();sizes=[]
 for w in words:
  if w in seen:continue
  q=[w];seen.add(w);size=0
  while q:
   u=q.pop();size+=1
   for v in edges[u]:
    if v not in seen:seen.add(v);q.append(v)
  sizes.append(size)
 hist=Counter();unreach=0
 by=defaultdict(list)
 for w in words:by[D(w)].append(w)
 for d in sorted(by):
  if d==0:continue
  allowed={w for w in words if D(w)<=d+3}
  q=deque(w for w in allowed if D(w)<d);dist={w:0 for w in q}
  while q:
   u=q.popleft()
   for v in edges[u]:
    if v in allowed and v not in dist:dist[v]=dist[u]+1;q.append(v)
  for w in by[d]:
   if w not in dist:unreach+=1
   else:hist[dist[w]]+=1
 print(n,len(words),len(sizes),max(sizes),sizes.count(1),dict(sorted(hist.items())),unreach)
```

## Interpretation
LR4 is not universally sufficient for connectivity even at modest size. The n=15 isolated words show that some balanced proper cyclic configurations admit no LR4 at all; LR3 supplies a qualitatively different local rearrangement. A general defect-transport lemma must use both generators or explicitly exclude these exceptions. The return of LR4-only connectivity at n=18 does not imply monotonicity, and finite evidence alone cannot classify n>=21.

## Next
Classify LR4-frozen sign words via forbidden five-edge windows, intersect that classification with colour closure and exact balance, and seek a general structural characterization. Then derive how LR3 unfreezes these configurations while respecting the D<=d+3 repair band. This may yield a finite local lemma for the broader normalization proof.
