# EHF-CBB-CROSS-32 — Exact lower-bound checks to t=12 and three-seed sign structure

Date: 2026-11-11. Status: exact finite BFS through t=12; arbitrary-t lower bound OPEN.

## Family and sign decomposition
For integer t>=1, define F_t=A(BC)^(t+2)(AC)^(t+1)(AB)^(t+1), n=6t+9. With + for A->B->C->A and - for reverse, its position-indexed sign string is exactly
```
++(-+)^t -++(-+)^t -++(-+)^t -
```
where concatenation is literal. Equivalently it has three '++' pairs separated by alternating sign regions. Cyclic windows of length five can be checked to exclude all 14 LR4-active patterns for every t>=1; thus the family is LR4-frozen for arbitrary t. LR3 legality is exactly the sign rewrite -++- <-> +--+.

## Exact shortest LR3 activation distance
A breadth-first search over all proper, balanced words reachable by LR3, terminating at the first word with a legal nontrivial LR4 move, gives:

| t | n | shortest escape depth | discovered states before first active state (implementation-dependent) |
| 1 | 15 | 1 | 4 |
| 2 | 21 | 2 | 13 |
| 3 | 27 | 3 | 35 |
| 4 | 33 | 4 | 86 |
| 5 | 39 | 5 | 194 |
| 6 | 45 | 6 | 415 |
| 7 | 51 | 7 | 844 |
| 8 | 57 | 8 | 1654 |
| 9 | 63 | 9 | 3133 |
| 10 | 69 | 10 | 5773 |
| 11 | 75 | 11 | 10372 |
| 12 | 81 | 12 | 18240 |

The discovered-state counts are diagnostic only and depend on enumeration order. BFS proves no shorter path exists for each tested t. CROSS-31 already supplied the explicit all-t t-move construction (LR3 at starts 0,2,...,2t-2), so the upper bound is unconditional.

## Reproducible independent test
```python
from collections import deque

def rev(w,k,i):
 n=len(w);ix=[(i+j)%n for j in range(k)];v=list(w)
 for a,b in zip(ix,reversed([w[j] for j in ix])):v[a]=b
 return ''.join(v)

def proper(w):
 return all(w[i]!=w[(i+1)%len(w)] for i in range(len(w)))

def moves(w,k):
 return [v for i in range(len(w))
         if (v:=rev(w,k,i))!=w and proper(v)]

def distance(w):
 seen={w};q=deque([(w,0)])
 while q:
  u,d=q.popleft()
  if moves(u,4):return d
  for v in moves(u,3):
   if v not in seen:
    seen.add(v);q.append((v,d+1))
 raise RuntimeError('No LR3 route to LR4-active word')

for t in range(1,13):
 w='A'+'BC'*(t+2)+'AC'*(t+1)+'AB'*(t+1)
 assert len(w)==6*t+9
 assert all(w.count(c)==2*t+3 for c in 'ABC')
 assert proper(w)
 signs=''.join('+' if ('ABC'.index(w[(i+1)%len(w)])-
                            'ABC'.index(w[i]))%3==1 else '-'
               for i in range(len(w)))
 assert signs=='++'+'-+'*t+'-++'+'-+'*t+'-++'+'-+'*t+'-'
 assert not moves(w,4)
 assert distance(w)==t
 print(t,len(w),t)
```

## Candidate lower-bound mechanism (NOT YET PROVED)
Each LR3 move rewrites a four-edge sign window -++- <-> +--+. The family has three separated ++ pairs embedded in alternating background. A plausible lower bound would quantify how many local rewrites are required before any forbidden five-edge LR4 pattern can appear. It must account for all legal moves at all three interfaces and cyclic wraparound, not just the explicit construction. No valid arbitrary-t 1-Lipschitz potential or locality lemma is yet established. Do not assert that unbounded escape depth has been proved.

## Next
Represent the LR3 dynamics as a rewriting system on distances between three marked double-plus seeds, identify any possible creation or annihilation of seeds, and prove a lower bound for the first LR4-active window. Alternatively seek an inductive certificate for the set of all LR3-reachable states at depth <t.
