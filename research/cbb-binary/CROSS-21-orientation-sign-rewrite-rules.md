# EHF-CBB-CROSS-21 — Exact orientation-sign rewrite rules

Date: 2026-11-11 AEST. Status: local algebraic identities plus exhaustive n=9 admissible move audit. No general connectivity theorem.

## Sign encoding
Encode colours A,B,C as 0,1,2 modulo 3. For each cyclic edge i -> i+1, set s_i=+1 when c_{i+1}-c_i=+1 mod 3, and s_i=-1 when the difference is -1 mod 3. Properness ensures the difference is always +/-1. A cyclic sign word closes iff sum_i s_i = 0 mod 3. Given the starting colour, the signs reconstruct the entire colour word. **Balance of A,B,C is an additional restriction**; not every closed sign word represents a balanced colour word.

Let D be the number of negative edges and n=3m. Then W=(n-2D)/3=m-2D/3. Closure forces D divisible by 3. Thus LR3 preserves D, while any admissible LR4 changes D by exactly +/-3.

## Exact LR3 rule
Consider k=3 consecutive reversed vertices, with the four surrounding oriented edges, including the two boundary edges. Exhaustive local colour case analysis gives exactly:
```
-++- <-> +--+
```
The rule is applied cyclically. Both patterns contain two negative signs. Every such local rewrite corresponds to a legal LR3 reversal of the corresponding proper colour word. LR3 exchanges the distribution of defects while keeping D and W constant. This is not literally a one-step translation of an isolated negative sign.

## Exact LR4 rules
An LR4 reversal acts on the five edges surrounding four reversed vertices. Exhaustive local colour case analysis yields seven reversible pairs (14 oriented cases):
```
----- <-> -+++-
----+ <-> -++++
---+- <-> +-+++
--+-- <-> ++-++
-+--- <-> +++-+
+---- <-> ++++-
+---+ <-> +++++
```
Every LR4 rule replaces three more negative signs with positive signs, or vice versa: Delta D=+/-3 and Delta W=-/+2. In particular:
```
+++++ -> +---+
```
creates a three-edge reverse-orientation patch, and the inverse eliminates it. Other rules change the shape and location of defect patches while creating or removing three negative edges.

## Exhaustive finite check at n=9
All 132 balanced proper position-indexed words were enumerated. Across directed nontrivial legal moves, LR3 gave 108 moves, exactly the two four-edge sign rules, all with Delta W=0. LR4 gave 648 moves, exactly the 14 five-edge sign rules, split equally between Delta W=+2 and -2. This finite check confirms the algebraic local classification but does not prove any global normalization statement.

## Reproduction
```python
from itertools import product
from collections import defaultdict,Counter
n=9;m=3
S=[w for w in product(range(3),repeat=n) if all(w.count(x)==m for x in range(3)) and all(w[i]!=w[(i+1)%n] for i in range(n))]
def sign(w):return tuple(1 if (w[(i+1)%n]-w[i])%3==1 else -1 for i in range(n))
def rev(w,k,i):
 ix=[(i+j)%n for j in range(k)];v=list(w)
 for a,b in zip(ix,reversed([w[t] for t in ix])):v[a]=b
 return tuple(v)
for k in (3,4):
 patterns=defaultdict(Counter);deltas=Counter()
 for w in S:
  for i in range(n):
   v=rev(w,k,i)
   if v==w or any(v[t]==v[(t+1)%n] for t in range(n)):continue
   a=sign(w);b=sign(v)
   ix=[(i-1+j)%n for j in range(k+1)]
   patterns[tuple(a[t] for t in ix)][tuple(b[t] for t in ix)]+=1
   deltas[(sum(b)-sum(a))//3]+=1
 print(k,len(patterns),deltas)
 for a,bs in sorted(patterns.items()):
  print(''.join('+' if t==1 else '-' for t in a),'->',','.join(''.join('+' if t==1 else '-' for t in b) for b in bs))
```

## Important distinctions
- The sign representation loses the absolute initial colour (three possible global colour phases) but preserves the relative cyclic transition structure.
- Local sign rewrite rules do not by themselves prove that a path remains in the balanced sector for arbitrary sign words. Applying them to a balanced proper colour word via actual vertex reversal does preserve counts by construction.
- A sign pattern with D=0 means the word is one of the three cyclic phases of (ABC)^m. This provides a clean normalization target.
- No theorem that arbitrary defects can be transported/eliminated is established yet.

## Next proof goal
Classify trapped configurations in the sign representation and seek a finite family of admissible LR3/LR4 macro-moves that reduces D after a bounded temporary increase of three defects. A proof must track the colour-balance constraint and phase alignment, not only sign patterns.
