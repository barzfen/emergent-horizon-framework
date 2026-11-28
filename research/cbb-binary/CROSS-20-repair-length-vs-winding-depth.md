# EHF-CBB-CROSS-20 — Repair length grows while winding excursion remains bounded

Date: 2026-11-11 (AEST). Status: exhaustive finite experiment for n=9,12,15,18. No arbitrary-n theorem.

## Setup
Balanced, proper position-indexed cyclic three-colour words n=3m. Signed winding W=(N_forward-N_reverse)/3. Legal LR3/LR4 reversals retain proper cyclic adjacency. An LR3 component at W=a is called *upward trapped* when no member has an LR4 edge to W=a+2.

For each upward-trapped LR3 component, find the minimum number of LR3/LR4 moves from **some member** of the component to **any word with W>a**, restricted to W>=a-2. This measures repair *after free choice of starting state within the component*, not worst-case starting-word repair.

## Exact results
| n | trapped LR3 components | distribution of minimum repair length | largest minimum |
| 9 | 9 | 3:9 | 3 |
| 12 | 48 | 3:36, 5:12 | 5 |
| 15 | 150 | 3:60, 5:90 | 5 |
| 18 | 531 | 3:279, 5:180, 7:72 | 7 |

All components have a repair staying above or equal to a-2. This confirms a finite bounded-*depth* property, while disproving the universal three-move-repair conjecture. It does not prove any length-independent bound on *number* of moves. The repair length grows with n in the tested cases.

## Witness for seven-move repair at n=18
The singleton LR3 component at W=4 containing `ABABCABCACABCABCBC` requires seven moves to reach W=6 while never dropping below W=2. One shortest route (all LR4, zero-based cyclic start indices):
```
ABABCABCACABCABCBC  W=4
LR4 15 -> CBABCABCACABCABACB W=2
LR4 14 -> CBABCABCACABCABCAB W=4
LR4  4 -> CBABCBACACABCABCAB W=2
LR4  5 -> CBABCACABCABCABCAB W=4
LR4  2 -> CBACBACABCABCABCAB W=2
LR4  3 -> CBACABCABCABCABCAB W=4
LR4  0 -> CABCABCABCABCABCAB W=6
```
Every intermediate state is balanced and proper. The final state is a cyclic phase of (ABC)^6.

## Reproduction
```python
from collections import deque,defaultdict,Counter
for m in range(3,7):
 n=3*m; words=[]
 def rec(w,c):
  if len(w)==n:
   if w[-1]!=w[0]:words.append(tuple(w))
   return
  for x in range(3):
   if c[x]<m and (not w or w[-1]!=x):
    c[x]+=1;w.append(x);rec(w,c);w.pop();c[x]-=1
 rec([],[0]*3);S=set(words)
 def W(w):return sum(1 if (w[(i+1)%n]-w[i])%3==1 else -1 for i in range(n))//3
 def nei(w,k):
  for i in range(n):
   ix=[(i+j)%n for j in range(k)];v=list(w)
   for a,b in zip(ix,reversed([w[t] for t in ix])):v[a]=b
   v=tuple(v)
   if v!=w and v in S:yield v,i
 byW=defaultdict(list)
 for w in words:byW[W(w)].append(w)
 result=Counter()
 for a in sorted(byW):
  if a==m:continue
  allowed={w for w in words if W(w)>=a-2};Q=deque();d={}
  for w in allowed:
   if W(w)>a:d[w]=0;Q.append(w)
  while Q:
   u=Q.popleft()
   for k in (3,4):
    for v,_ in nei(u,k):
     if v in allowed and v not in d:d[v]=d[u]+1;Q.append(v)
  seen=set()
  for w in byW[a]:
   if w in seen:continue
   comp=[];st=[w];seen.add(w)
   while st:
    u=st.pop();comp.append(u)
    for v,_ in nei(u,3):
     if v not in seen:seen.add(v);st.append(v)
   if not any(W(v)>a for u in comp for v,_ in nei(u,4)):
    result[min(d.get(u,10**9) for u in comp)]+=1
 print(n,dict(sorted(result.items())))
```

## Interpretation and next proof objective
The empirical repair depth is at most 2 winding units, even when repairs take 7 moves. A useful general lemma would allow a bounded winding excursion but a cycle-length-dependent number of defect-transport moves. Seek a formal representation of local orientation defects and an operation that reduces a well-founded potential (e.g. ordered defect separation) despite temporary winding decreases. Avoid claiming universal connectivity from finite checks.
