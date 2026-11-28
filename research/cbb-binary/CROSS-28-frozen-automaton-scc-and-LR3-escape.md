# EHF-CBB-CROSS-28 — SCC structure and LR3 escape depth of LR4-frozen cycles

Date: 2026-11-11 AEST. Status: exact finite automaton analysis and exhaustive enumeration of LR4-frozen balanced cycles at n=15,21. General arbitrary-n connectivity theorem OPEN.

## Forbidden-window automaton
LR4 is legal and nontrivial exactly for five-sign windows in:
```
----- ----+ ---+- --+-- -+--- +---- +---+
-+++- -++++ +-+++ ++-++ +++-+ ++++- +++++
```
Define 16 states as four-sign words over {+,-}. There is an edge abcd -> bcdx if abcdx is not in the forbidden set. There are exactly 18 directed edges.

Strongly connected components: one nontrivial component of size 10,
```
++-+ ++-- +-++ +-+- +--+ -++- -+-+ -+-- --++ --+-
```
and six singleton SCCs: `++++`, `+++-`, `+---`, `-+++`, `---+`, `----`. None of the singleton SCCs has a self-loop. Consequently every cyclic LR4-frozen sign word corresponds to a closed walk entirely within the 10-state core. This classification applies to orientation signs; colour closure and exact balance remain additional global conditions.

## LR3 exits from balanced frozen words
At n=15 there are 30 balanced LR4-frozen position-indexed colour words. Each has 3 legal LR3 moves, and all 3 immediately lead to LR4-active words.

At n=21 there are 168 balanced LR4-frozen position-indexed words:
- 126 have 5 legal LR3 moves, of which 4 immediately lead to LR4-active words;
- 42 have 3 legal LR3 moves, none immediately leading to an LR4-active word.
For these 42, a second LR3 move always reaches an LR4-active word. Thus every frozen balanced word at n=21 is within at most **two LR3 moves** of an LR4-active configuration. This is a finite result only.

One of the depth-two frozen words is `ABCBCBCBCACACACABABAB` (length 21). An LR3-only component containing an n=21 frozen word has 229 words, of which 225 are LR4-active. There are 18 such LR3 components encountered when starting from the 56 balanced frozen sign patterns with c0=0 (three colour phases give corresponding translated components). This component-level statement is not an enumeration of all LR3 components in the full n=21 graph.

## Why this matters
The fact that every frozen word has an LR3 move does not by itself establish escape from the LR4-frozen set. The 42 depth-two examples disprove the stronger one-step escape claim. Escape from *frozen* status also does not automatically mean progress toward fewer defects: the newly available LR4 move may increase, rather than decrease, the defect count.

## Reproducible algorithm
```python
from itertools import product
from collections import deque,Counter
bad={'-----','----+','---+-','--+--','-+---','+----','+---+',
     '-+++-','-++++','+-+++','++-++','+++-+','++++-','+++++'}
states=[''.join(s) for s in product('+-',repeat=4)]
edges={s:[s[1:]+x for x in '+-' if s+x not in bad] for s in states}
assert sum(map(len,edges.values()))==18
def rev(w,k,i):
 n=len(w);ix=[(i+j)%n for j in range(k)];v=list(w)
 for a,b in zip(ix,reversed([w[t] for t in ix])):v[a]=b
 return tuple(v)
def legal(w):return all(w[i]!=w[(i+1)%len(w)] for i in range(len(w)))
def neighbors(w,k):return {v for i in range(len(w)) if (v:=rev(w,k,i))!=w and legal(v)}
for n in (15,21):
 hist=Counter();num=0
 for s in product('+-',repeat=n):
  if any(''.join(s[(i+j)%n] for j in range(5)) in bad for i in range(n)):continue
  if s.count('-')%3:continue
  w=[0]
  for x in s[:-1]:w.append((w[-1]+(1 if x=='+' else -1))%3)
  if any(w.count(c)!=n//3 for c in range(3)):continue
  w=tuple(w);num+=3
  q=deque([(w,0)]);seen={w}
  while q:
   u,d=q.popleft()
   if neighbors(u,4):
    hist[d]+=3;break
   for v in neighbors(u,3):
    if v not in seen:seen.add(v);q.append((v,d+1))
 print(n,num,dict(hist))
assert num==168
```

## Next
Find a structural characterization of the 10-state SCC cycles that satisfy colour balance. Determine whether LR3 escape depth is bounded independently of n or grows with n, and whether LR3 escape can be followed by an LR4 defect-eliminating move within the conjectured D+3 band. Neither conclusion follows from the present results.
