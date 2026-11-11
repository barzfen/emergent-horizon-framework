# EHF-CBB-CROSS-29 — LR3 escape depth grows in frozen balanced cycles

Date: 2026-11-11 AEST. Status: exact exhaustive enumeration of LR4-frozen sign patterns and BFS escape depth at selected lengths. No arbitrary-n theorem.

## Definitions
Balanced proper cyclic colour words n=3m, each colour m times. LRk reverses k consecutive cyclic vertices retaining properness. A word is LR4-frozen if no legal nontrivial LR4 move exists. Its *escape depth* is the shortest number of LR3 moves needed to reach any word with at least one legal LR4 move. This is NOT the number of moves required to reduce the defect count.

## New exact enumeration
Enumerate sign words with no forbidden five-sign LR4 windows, enforce sign closure and exact colour balance. Each balanced sign word lifts to exactly three global colour phases. For each phase representative, BFS via LR3 until an LR4-active word is found.

| n | balanced frozen sign words | balanced frozen colour words | escape depth distribution among sign words | max depth |
| 15 | 10 | 30 | 1:10 | 1 |
| 21 | 56 | 168 | 1:42, 2:14 | 2 |
| 24 | 0 | 0 | — | — |
| 27 | 522 | 1566 | 1:450, 2:54, 3:18 | 3 |
| 30 | 160 | 480 | 1:160 | 1 |
| 33 | 5038 | 15114 | 1:4400, 2:550, 3:66, 4:22 | 4 |

Counts for n15 and n21 reproduce CROSS-28. The sequence 15,21,27,33 exhibits increasing maximum escape depths 1,2,3,4. This disproves any conjecture that a universal escape bound <=3 suffices. It does NOT prove unbounded escape depth for arbitrary n.

## Example maximum-depth words
n15 depth1: `ABCBCBCACACABAB`
n21 depth2: `ABCBCBCBCACACACABABAB`
n27 depth3: `ABCBCBCBCBCACACACACABABABAB`
n33 depth4: `ABCBCBCBCBCBCACACACACACABABABABAB`

These display a clear repeating block family. Deriving a closed-form escape-depth theorem for this family is the next proof task.

## Reproduction
```python
from collections import deque,Counter
bad={'-----','----+','---+-','--+--','-+---','+----','+---+',
     '-+++-','-++++','+-+++','++-++','+++-+','++++-','+++++'}
def rev(w,k,i):
 n=len(w);ix=[(i+j)%n for j in range(k)];v=list(w)
 for a,b in zip(ix,reversed([w[t] for t in ix])):v[a]=b
 return tuple(v)
def proper(w):return all(w[i]!=w[(i+1)%len(w)] for i in range(len(w)))
def nei(w,k):return {v for i in range(len(w)) if (v:=rev(w,k,i))!=w and proper(v)}
for n in (15,21,24,27,30,33):
 frozen=[]
 def rec(s):
  if len(s)==n:
   if any(''.join((s+s[:4])[i:i+5]) in bad for i in range(n-4,n)):return
   if s.count('-')%3:return
   w=[0]
   for x in s[:-1]:w.append((w[-1]+(1 if x=='+' else -1))%3)
   if any(w.count(c)!=n//3 for c in range(3)):return
   frozen.append(tuple(w));return
  for x in '+-':
   if len(s)>=4 and s[-4:]+x in bad:continue
   rec(s+x)
 rec('')
 hist=Counter()
 for w in frozen:
  q=deque([(w,0)]);seen={w}
  while q:
   u,d=q.popleft()
   if nei(u,4):hist[d]+=1;break
   for v in nei(u,3):
    if v not in seen:seen.add(v);q.append((v,d+1))
 print(n,len(frozen),3*len(frozen),dict(sorted(hist.items())))
```

## Interpretation
The growing escape-depth sequence indicates that local LR3 rearrangements can require a number of moves that increases with cycle length, even to activate *any* LR4 move. A bounded winding excursion conjecture remains logically compatible with unbounded repair *length*. No physics claim follows from the finite automaton computations.

## Next
Formalize the repeating family, prove its escape-depth lower bound using a finite-speed/locality argument, and then test whether an LR4 activation can be followed by defect reduction within D+3.
