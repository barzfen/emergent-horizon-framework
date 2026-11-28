# EHF-CBB-CROSS-30 — An explicit family with linearly growing LR3 escape depth

Date: 2026-11-11. Status: exact finite BFS for t=1..8; general law is a CONJECTURE, not a proof.

## Construction
For integer t>=1, let
```
F_t = A (BC)^(t+2) (AC)^(t+1) (AB)^(t+1)
n=6t+9=3(2t+3).
```
Each word is cyclically proper and balanced, with each of A,B,C occurring 2t+3 times. Direct finite checks show no legal LR4 moves for t=1..8. The general LR4-frozen property can be established by inspecting the repeating interiors and finitely many block interfaces, but a complete formal proof is not included here.

Define escape depth e(w) as minimum number of legal LR3 reversals to reach any proper word admitting a nontrivial legal LR4 reversal. The colour word must remain balanced (reversals preserve counts).

## Exact finite results
| t | n | LR4 moves initially | BFS shortest LR3 escape depth | BFS states discovered before first active target |
| 1 | 15 | 0 | 1 | 4 |
| 2 | 21 | 0 | 2 | 13 |
| 3 | 27 | 0 | 3 | 40 |
| 4 | 33 | 0 | 4 | 112 |
| 5 | 39 | 0 | 5 | 278 |
| 6 | 45 | 0 | 6 | 526 |
| 7 | 51 | 0 | 7 | 1081 |
| 8 | 57 | 0 | 8 | 2273 |

The discovered-state counts depend on BFS iteration ordering and are diagnostic only. Distances are exact because BFS searches in nondecreasing path length.

## Conjecture
For every integer t>=1, F_t is LR4-frozen and e(F_t)=t. If established, this would prove that LR3 escape depth is unbounded in cycle length, with e(F_t)=(n-9)/6.

**What is proved:** F_t is balanced and proper for all t, by elementary counting and interface checks. **What is computed:** LR4 freezing and exact escape distance for t<=8. **What is not proved:** arbitrary-t freezing and arbitrary-t lower/upper escape bounds.

## Reproducible Python
```python
from collections import deque

def rev(w,k,i):
 n=len(w);ix=[(i+j)%n for j in range(k)];v=list(w)
 for a,b in zip(ix,reversed([w[j] for j in ix])):v[a]=b
 return ''.join(v)

def proper(w):
 return all(w[i]!=w[(i+1)%len(w)] for i in range(len(w)))

def neighbors(w,k):
 return {v for i in range(len(w))
         if (v:=rev(w,k,i))!=w and proper(v)}

def escape_depth(w):
 q=deque([(w,0)]);seen={w}
 while q:
  u,d=q.popleft()
  if neighbors(u,4):return d
  for v in neighbors(u,3):
   if v not in seen:
    seen.add(v);q.append((v,d+1))
 raise RuntimeError('No escape')

for t in range(1,9):
 w='A'+'BC'*(t+2)+'AC'*(t+1)+'AB'*(t+1)
 assert len(w)==6*t+9 and proper(w)
 assert all(w.count(c)==2*t+3 for c in 'ABC')
 assert not neighbors(w,4)
 d=escape_depth(w)
 print(t,len(w),d)
 assert d==t
```

## Next mathematical task
Find a *locality-based invariant* for legal LR3 moves that proves no LR4-active five-edge window can arise in fewer than t steps. Separately construct an explicit t-step LR3 sequence for every t. These would yield the two inequalities e(F_t)>=t and e(F_t)<=t, proving the conjecture. Do not conflate activation with defect reduction or general graph connectivity.
