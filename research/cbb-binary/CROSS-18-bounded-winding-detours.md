# EHF-CBB-CROSS-18 — Bounded winding detours

Date: 2026-11-10. Status: exhaustive finite verification, not a general theorem.

## Question
For balanced, proper position-indexed cyclic words of length n=3m over A,B,C, define W=(N_forward-N_backward)/3. LR3 and LR4 reverse 3 or 4 cyclically consecutive positions, provided separation remains valid. For each word w define E(w) as the minimum, over all LR3+LR4 paths from w to any maximum-winding word W=m, of W(w)-min_{v on path}W(v). Does E(w)<=2?

## Exact exhaustive results
| n | words | max E | maximum E by starting winding |
| 6 | 24 | 0 | -2:0, 0:0 |
| 9 | 132 | 2 | -3:0, -1:0, +1:2 |
| 12 | 804 | 2 | -4:0, -2:0, 0:0, +2:2 |
| 15 | 5196 | 2 | -5:0, -3:0, -1:0, +1:2, +3:2 |
| 18 | 34872 | 2 | -6:0, -4:0, -2:0, 0:0, +2:2, +4:2 |

For n>=9 tested, bound 2 is sharp: CROSS-17 gives a word of winding +1 at n9 with no nondecreasing-winding path to maximum. The property is a bound on the deepest *excursion*, not on number of moves or total winding variation.

## Exact algorithm
For each starting winding a, consider threshold subgraphs induced by W>=t for t=a,a-2,... . Multi-source flood from all maximum-winding states. The first threshold where every word at winding a is reachable gives the maximum minimum excursion at that starting level. Reversibility makes reverse flood valid.

## Reproducible Python
```python
from collections import deque
for m in range(2,7):
 n=3*m; words=[]
 def rec(w,c):
  if len(w)==n:
   if w[-1]!=w[0]:words.append(tuple(w))
   return
  for x in range(3):
   if c[x]<m and (not w or w[-1]!=x):
    c[x]+=1;w.append(x);rec(w,c);w.pop();c[x]-=1
 rec([],[0]*3)
 S=set(words)
 def W(w):return sum(1 if (w[(i+1)%n]-w[i])%3==1 else -1 for i in range(n))//3
 def neighbors(w):
  for k in (3,4):
   for i in range(n):
    ix=[(i+j)%n for j in range(k)];v=list(w)
    for j,t in zip(ix,reversed([w[t] for t in ix])):v[j]=t
    v=tuple(v)
    if v in S and v!=w:yield v
 levels=sorted(set(map(W,words)));result={}
 for a in levels[:-1]:
  starts=[w for w in words if W(w)==a]
  for t in range(a,levels[0]-1,-2):
   seen={w for w in words if W(w)==m};queue=deque(seen)
   while queue:
    u=queue.popleft()
    for v in neighbors(u):
     if v not in seen and W(v)>=t:seen.add(v);queue.append(v)
   if all(w in seen for w in starts):
    result[a]=a-t;break
  else:raise AssertionError('unreachable')
 print(n,len(words),result,'max',max(result.values()))
```

## Scope and next test
Conjecture: E(w)<=2 for all balanced proper three-colour cyclic words n=3m, m>=2. The five exhaustive cases support it; there is no arbitrary-m proof. Search for a local defect transport/repair lemma that bounds winding excursions and yields a terminating normalization procedure. The result does not establish a 1:2:3 law.
