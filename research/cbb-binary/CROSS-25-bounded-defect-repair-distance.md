# EHF-CBB-CROSS-25 — Bounded-defect repair distances and a candidate progress rank

Date: 2026-11-11 AEST. Status: independently computed exhaustive finite audit n=6,9,12,15. General theorem OPEN.

## Setup
Balanced proper position-indexed cyclic three-colour words of length n=3m. Orientation sign s_i is + if c_(i+1)-c_i=1 mod 3, else -. D(w)=# negative signs, a multiple of 3. LR3/LR4 are legal consecutive cyclic vertex reversals retaining properness. A *repair* from a word with D=d>0 is a path to any word with D<d, with every intermediate word satisfying D<=d+3. No lower restriction is imposed; the target can be any lower D. The repair length is the minimum number of moves.

## Exhaustive results
| n | all states | max shortest repair | unreachable within D<=d+3 | repair length histogram |
| 6 | 24 | 1 | 0 | 1:21 |
| 9 | 132 | 3 | 0 | 1:93, 3:36 |
| 12 | 804 | 5 | 0 | 1:681, 3:108, 5:12 |
| 15 | 5196 | 5 | 0 | 1:4473, 2:15, 3:555, 4:15, 5:135 |

The histograms exclude D=0 states (3 at each size). The 2- and 4-move shortest repairs at n15 are real possibilities: an LR3 move can reposition defects without changing D, before an LR4 eliminates three.

## Reproducible code
```python
from collections import deque,defaultdict,Counter
for m in range(2,6):
 n=3*m; words=[]
 def rec(w,c):
  if len(w)==n:
   if w[-1]!=w[0]:words.append(tuple(w))
   return
  for x in range(3):
   if c[x]<m and (not w or w[-1]!=x):
    c[x]+=1;w.append(x);rec(w,c);w.pop();c[x]-=1
 rec([],[0]*3);S=set(words)
 def D(w):
  return sum((w[(i+1)%n]-w[i])%3==2 for i in range(n))
 def nei(w):
  for k in (3,4):
   for i in range(n):
    ix=[(i+j)%n for j in range(k)];v=list(w)
    for a,b in zip(ix,reversed([w[t] for t in ix])):v[a]=b
    v=tuple(v)
    if v!=w and v in S:yield v
 by=defaultdict(list)
 for w in words:by[D(w)].append(w)
 hist=Counter();unreach=0
 for d in sorted(by):
  if d==0:continue
  allowed={w for w in words if D(w)<=d+3}
  q=deque([w for w in allowed if D(w)<d]);dist={w:0 for w in q}
  while q:
   u=q.popleft()
   for v in nei(u):
    if v in allowed and v not in dist:
     dist[v]=dist[u]+1;q.append(v)
  for w in by[d]:
   if w not in dist:unreach+=1
   else:hist[dist[w]]+=1
 print(n,len(words),max(hist),unreach,dict(sorted(hist.items())))
```

## Candidate rank, and why it is not yet a theorem
For a state w with D(w)=d>0, define r_d(w) as its shortest path distance, inside the subgraph D<=d+3, to the set of states with D<d. The finite experiment establishes r_d(w)<infinity for all enumerated w. Along a shortest repair path, r_d decreases by one each move **with d held fixed as the original repair threshold**; D itself can temporarily increase, so the pair (D(w),r_{D(w)}(w)) is NOT guaranteed to decrease lexicographically at each elementary move.

A rigorous general result would show r_d(w)<infinity for every balanced proper cyclic word at every n=3m, m>=2. Then iterating these finite repair paths strictly decreases D after each macro-step, yielding termination at D=0 in at most D(start)/3 macro-steps. Phase alignment of the three D=0 words is a separate task (CROSS-15 LR4 construction).

## Limitations
This is a graph-defined potential, not yet an explicit local formula in gap lengths. Finite BFS establishes no arbitrary-n bound on r_d or connectivity. The 3-defect excursion bound remains a conjecture outside the tested sizes.

## Next
Seek an analytic upper bound on r_d in terms of n or cyclic gap lengths, and a finite set of defect transport macro-moves with a well-founded local potential. Probe n18 with optimized enumeration.
